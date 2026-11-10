"""Safety gates, tested through the HTTP API the way ServiceNow calls it.

The real graph, MCP tools, search index and citation checks run; only the LLM is scripted.
Gates enforced in ServiceNow (confidence threshold, @ai only from HR agents' work notes, approving
only a pending close proposal) are covered by servicenow-app/scripts/check-safety-gates.js.
"""

import asyncio

import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.agent.llm import Citation, TextBlock, ToolCall
from app.config import get_settings
from app.errors import AgentError
from app.search.hybrid import search
from tests.scripted import ScriptedLLM

pytestmark = pytest.mark.integration

QUESTION = {
    "title": "Parental leave",
    "description": "How many weeks of parental leave can I take?",
}


@pytest.fixture
def api(monkeypatch):
    """Starts the app with a given scripted LLM; returns a function that posts a triage request."""
    clients = []

    def start(llm) -> TestClient:
        monkeypatch.setattr(main, "get_provider", lambda: llm)
        client = TestClient(main.app, headers={"X-API-Key": get_settings().service_api_key})
        client.__enter__()
        clients.append(client)
        return client

    yield start
    for client in clients:
        client.__exit__(None, None, None)


def triage(client: TestClient, country: str | None) -> tuple[int, dict]:
    body = {"case_id": "x", "number": "HRC0001001", **QUESTION, "employee": {"country": country}}
    response = client.post("/triage", json=body)
    return response.status_code, response.json()


def test_given_a_cited_answer_for_a_known_country_when_triaged_then_it_may_be_posted(api):
    status, body = triage(api(ScriptedLLM()), "DE")
    assert status == 200
    assert body["suggestion_allowed"], body["suggestion_blocked_reason"]


def test_given_an_unknown_country_when_triaged_then_the_suggestion_goes_to_hr(api):
    status, body = triage(api(ScriptedLLM()), None)
    assert status == 200
    assert not body["suggestion_allowed"]
    assert "country is unknown" in body["suggestion_blocked_reason"]


def test_given_an_unmapped_country_name_when_triaged_then_it_counts_as_unknown(api):
    status, body = triage(api(ScriptedLLM()), "Atlantis")
    assert status == 200 and "country is unknown" in body["suggestion_blocked_reason"]


def test_given_a_german_employee_when_the_model_asks_for_us_policies_then_it_only_gets_german_ones(
    api,
):
    llm = ScriptedLLM(
        tool_call=ToolCall(
            "t1", "search_policies", {"query": "parental leave weeks", "country": "US"}
        )
    )
    status, body = triage(api(llm), "DE")
    assert status == 200
    titles = {r["title"] for r in body["suggestion"]["references"]}
    assert titles and all("United States" not in t for t in titles)


def test_given_a_german_employee_when_the_model_cites_a_us_policy_then_the_citation_is_rejected(
    api,
):
    us = search("paid parental leave weeks", country="US")
    us_chunk = next(c for c in us if c["country"] == "US")
    quote = us_chunk["sentences"][0]["text"]

    def cite_us(messages):
        return [TextBlock("You get the US entitlement.", [Citation(us_chunk["id"], 0, 1, quote)])]

    status, body = triage(api(ScriptedLLM(answer=cite_us)), "DE")
    assert status == 200
    assert not body["suggestion_allowed"]
    assert quote not in body["suggestion"]["formatted"]


def test_given_a_short_uncited_fact_when_triaged_then_it_is_removed_and_not_posted(api):
    llm = ScriptedLLM(answer=lambda messages: [TextBlock("You get 16 weeks.")])
    status, body = triage(api(llm), "DE")
    assert status == 200
    assert not body["suggestion_allowed"]
    assert "16 weeks" not in body["suggestion"]["text"]
    assert body["suggestion"]["removed_uncited"] == 1


def test_given_the_model_refuses_when_triaged_then_a_stable_error_code_is_returned(api):
    class Refusing(ScriptedLLM):
        async def structured(self, system, user, schema):
            raise AgentError("llm_refused", "the language model declined the request")

    status, body = triage(api(Refusing()), "DE")
    assert status == 502
    assert body == {"error": "llm_refused", "detail": "the language model declined the request"}


def test_given_every_run_slot_is_busy_when_triaged_then_it_fails_fast_with_busy(api):
    client = api(ScriptedLLM())
    rt = main.app.state.runtime
    rt.runs = asyncio.Semaphore(0)
    rt.settings = rt.settings.model_copy(update={"queue_timeout_seconds": 0.1})
    status, body = triage(client, "DE")
    assert status == 503 and body["error"] == "busy"


def test_given_a_wrong_api_key_when_called_then_it_is_refused(api):
    client = api(ScriptedLLM())
    response = client.post(
        "/triage",
        json={"case_id": "x", "number": "n", "title": "t"},
        headers={"X-API-Key": "wrong"},
    )
    assert response.status_code == 401
