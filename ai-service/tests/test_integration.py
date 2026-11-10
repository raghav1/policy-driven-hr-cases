"""Runs against the real database, models and MCP tool server, with a scripted LLM in place of the provider.

Run inside the stack: docker compose run --rm agent pytest -m integration
"""
import pytest

from app.agent.graph import Agent
from app.agent.llm import AnthropicProvider, Citation, LLMTurn, TextBlock, ToolCall
from app.agent.mcp_client import ToolClient
from app.ingest.pipeline import reconcile
from app.schemas import ChatRequest, Employee, TriageRequest
from app.search.hybrid import search

pytestmark = pytest.mark.integration

# Question, employee country, expected article title.
RETRIEVAL_SET = [
    ("How long is parental leave?", "DE", "Parental leave (Germany)"),
    ("How much notice do I need to give before parental leave?", "DE", "Parental leave (Germany)"),
    ("How many weeks of paid parental leave do I get?", "US", "Parental leave (United States)"),
    ("maternity leave weeks", "IN", "Parental leave (India)"),
    ("Is parental leave paid?", "GB", "Parental leave (United Kingdom)"),
    ("How many vacation days do I get per year?", "DE", "Annual leave (Germany)"),
    ("Can I carry over unused holiday to next year?", "US", "Annual leave (United States)"),
    ("When do I need a doctor's note for being ill?", "GB", "Sick leave (United Kingdom)"),
    ("How many paid sick days do I have?", "IN", "Sick leave (India)"),
    ("My father passed away, how much time off can I take?", "US", "Bereavement leave (United States)"),
    ("Can I add my spouse to my health insurance?", "US", "Health insurance (United States)"),
    ("What is the out of pocket maximum for medical costs?", "GB", "Health insurance (United Kingdom)"),
    ("Does the company match 401k contributions?", "US", "Retirement plan (United States)"),
    ("How much does Larkspur contribute to my pension?", "GB", "Retirement plan (United Kingdom)"),
    ("Provident fund contribution", "IN", "Retirement plan (India)"),
    ("When is open enrollment for benefits?", "US", "Benefits enrollment (United States)"),
    ("I got married, can I change my benefits?", "DE", "Benefits enrollment (Germany)"),
    ("Can I expense my gym membership?", "DE", "Wellbeing allowance (Germany)"),
    ("When is payday?", "GB", "Pay schedule (United Kingdom)"),
    ("How often am I paid?", "US", "Pay schedule (United States)"),
    ("My salary was wrong this month, how do I get it fixed?", "DE", "Payroll corrections (Germany)"),
    ("I was overpaid, how will the money be recovered?", "IN", "Payroll corrections (India)"),
    ("What is the daily meal limit when travelling?", "US", "Expense reimbursement (United States)"),
    ("mileage rate for using my own car", "GB", "Expense reimbursement (United Kingdom)"),
    ("Am I paid extra for working more than 40 hours?", "US", "Overtime (United States)"),
    ("Can I take time off instead of overtime pay?", "DE", "Overtime (Germany)"),
    ("How many days a week can I work from home?", "US", "Remote and hybrid work"),
    ("Can I work from another country for a month?", "IN", "Remote and hybrid work"),
    ("How long does HR take to respond to my case?", "GB", "How HR handles your case"),
    ("How long do you keep my personnel records?", "DE", "Employee data privacy"),
]


@pytest.fixture(scope="module", autouse=True)
def indexed():
    reconcile()


def test_country_filter_only_returns_that_country_or_global():
    results = search("parental leave entitlement", country="DE")
    assert results and all(r["country"] in ("DE", "GLOBAL") for r in results)


def test_retrieval_recall_at_5():
    misses = []
    for question, country, expected in RETRIEVAL_SET:
        titles = [r["title"] for r in search(question, country=country, top_k=5)]
        if expected not in titles:
            misses.append((question, expected, titles[:3]))
    recall = 1 - len(misses) / len(RETRIEVAL_SET)
    print(f"\nrecall@5 = {recall:.2f}")
    for miss in misses:
        print("MISS", miss)
    assert recall >= 0.9


class ScriptedLLM:
    """Plays the provider's part: one search, then an answer citing the first returned sentence."""

    model = "scripted"

    def __init__(self):
        self.calls = 0

    async def structured(self, system, user, schema):
        return {"category": "leave", "topics": ["parental_leave"], "priority": 3, "severity": "low",
                "confidence": 0.9, "reasoning": "Asks about parental leave."}

    async def turn(self, system, messages, tools):
        self.calls += 1
        if self.calls == 1:
            return LLMTurn([], [ToolCall("t1", "search_policies", {"query": "parental leave length", "country": "DE"})], [])
        tool_message = messages[-1]
        first = tool_message["content"][0]["content"][0]
        return LLMTurn([TextBlock("You can take up to three years of parental leave per child.",
                                  [Citation(first["source"], 0, 1, first["content"][0]["text"])])], [], [])

    def user_message(self, text):
        return {"role": "user", "content": text}

    def assistant_message(self, turn):
        return {"role": "assistant", "content": turn.raw_assistant}

    def tool_results_message(self, results):
        return AnthropicProvider.tool_results_message(results)


async def test_triage_graph_end_to_end_with_scripted_llm():
    tools = ToolClient()
    await tools.start()
    try:
        agent = Agent(ScriptedLLM(), tools)
        out = await agent.triage(TriageRequest(case_id="x", number="HRC0001001", title="Parental leave",
                                               description="How long can I take?", employee=Employee(country="DE")))
    finally:
        await tools.stop()
    assert out["classification"]["category"] == "leave"
    assert out["tools_used"] == ["search_policies"]
    answer = out["answer"]
    assert answer["all_claims_cited"]
    assert answer["references"][0]["article"].startswith("KB")
    assert "[1]" in answer["formatted"]


async def test_chat_records_a_close_proposal_without_acting():
    class ProposingLLM(ScriptedLLM):
        async def turn(self, system, messages, tools):
            self.calls += 1
            if self.calls == 1:
                return LLMTurn([], [ToolCall("p1", "propose_close", {"resolution": "Answered with the policy."})], [])
            return LLMTurn([TextBlock("I proposed closing this case; an HR agent needs to approve it.")], [], [])

    tools = ToolClient()
    await tools.start()
    try:
        out = await Agent(ProposingLLM(), tools).chat(ChatRequest(case_id="x", number="HRC0001001", message="@ai close this please"))
    finally:
        await tools.stop()
    assert out["proposal"] == {"action": "close", "resolution": "Answered with the policy."}
    assert out["answer"]["references"] == []
