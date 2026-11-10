"""Runs against the real database, models and MCP tool server, with a scripted LLM as provider.

Run inside the stack against a scratch database (see README, Tests).
"""

import pytest

from app.agent.graph import Agent
from app.agent.llm import LLMTurn, TextBlock, ToolCall
from app.agent.mcp_client import ToolClient
from app.config import get_settings
from app.ingest.pipeline import reconcile
from app.schemas import ChatRequest, Employee, TriageRequest
from app.search.hybrid import search
from app.sources import make_source
from tests.scripted import ScriptedLLM

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module", autouse=True)
def indexed():
    source = make_source(get_settings())
    reconcile(source)
    source.close()


def test_search_only_returns_the_employees_country_and_global_policies():
    results = search("parental leave entitlement", country="DE")
    assert results and all(r["country"] in ("DE", "GLOBAL") for r in results)


def test_search_without_a_country_only_returns_global_policies():
    results = search("How many days a week can I work from home?", country=None)
    assert results and all(r["country"] == "GLOBAL" for r in results)


def test_country_with_no_policies_of_its_own_still_finds_global_ones():
    titles = [
        r["title"] for r in search("Can I work from another country for a month?", country="IT")
    ]
    assert "Remote and hybrid work" in titles


async def _run(llm, call):
    tools = ToolClient()
    await tools.start()
    try:
        return await call(Agent(llm, tools, max_tool_calls=5))
    finally:
        await tools.stop()


async def test_triage_graph_end_to_end_with_scripted_llm():
    req = TriageRequest(
        case_id="x",
        number="HRC0001001",
        title="Parental leave",
        description="How long can I take?",
        employee=Employee(country="DE"),
    )
    out = await _run(ScriptedLLM(), lambda agent: agent.triage(req))
    assert out["classification"]["category"] == "leave"
    assert out["tools_used"] == ["search_policies"]
    answer = out["answer"]
    assert answer.all_claims_cited
    assert answer.references[0].article.startswith("KB") and answer.references[0].country in (
        "DE",
        "GLOBAL",
    )
    assert "[1]" in answer.formatted


async def test_chat_records_a_close_proposal_without_acting():
    llm = ScriptedLLM(
        tool_call=ToolCall("p1", "propose_close", {"resolution": "Answered with the policy."}),
        answer=lambda messages: [
            TextBlock("I proposed closing this case; an HR agent needs to approve it.")
        ],
    )
    req = ChatRequest(case_id="x", number="HRC0001001", message="@ai close this please")
    out = await _run(llm, lambda agent: agent.chat(req))
    assert out["proposal"] == {"action": "close", "resolution": "Answered with the policy."}
    assert out["answer"].references == []


async def test_tool_failure_reaches_the_model_without_internal_details():
    llm = ScriptedLLM(
        tool_call=ToolCall("t1", "get_policy_section", {"article": ["not", "a", "string"]})
    )
    req = ChatRequest(
        case_id="x",
        number="HRC0001001",
        message="@ai check the article",
        employee=Employee(country="DE"),
    )
    await _run(llm, lambda agent: agent.chat(req))
    tool_message = llm.seen[1][-1]["content"][0]
    assert tool_message["is_error"]
    assert tool_message["content"][0]["text"] == "get_policy_section is unavailable right now."


def test_scripted_turn_shape_matches_the_provider():
    # Guards the scripted stand-in itself: it must speak the same message format as the real
    # provider.
    turn = LLMTurn([TextBlock("x")], [], [{"type": "text", "text": "x"}])
    assert ScriptedLLM.assistant_message(turn) == {
        "role": "assistant",
        "content": [{"type": "text", "text": "x"}],
    }
