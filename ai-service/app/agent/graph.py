"""Agent workflows, built as LangGraph graphs.

Triage (new case)                         Chat (@ai request from HR staff)

        +--> classify --------+                 model <--> tools
START --+                     +--> verify           |
        +--> model <--> tools |                 cite_check (one repair pass)
                |             |                     |
             cite_check ------+                 verify --> close_check --> END
           (one repair pass)

- classify: structured classification (category, topics, priority, severity, confidence).
- model/tools: the tool-use loop; search results come back as citable passages.
- cite_check: if a sentence has no citation, ask the model once to rewrite it with the policy wording.
- verify: check every citation against the stored policy text; drop sentences that are still uncited.
- close_check: if staff asked to close and the model held back, record a proposal anyway (a person decides).

The graphs only return a recommendation. Nothing here writes to ServiceNow.
"""
import asyncio
import logging
import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.agent import citations
from app.agent.llm import LLMProvider, TextBlock, ToolResult
from app.agent.mcp_client import ToolClient
from app.agent.prompts import (CHAT_SYSTEM, CLASSIFY_SCHEMA, CLASSIFY_SYSTEM, CLOSE_CHECK_SCHEMA, CLOSE_CHECK_SYSTEM,
                               PROPOSE_CLOSE_TOOL, REPAIR_INSTRUCTION, TRIAGE_SYSTEM)
from app.config import get_settings
from app.schemas import ChatRequest, TriageRequest
from app.search.hybrid import get_chunks

log = logging.getLogger(__name__)

SEARCH_TOOLS = {"search_policies", "get_policy_section"}
MAX_REPAIRS = 1


class State(TypedDict, total=False):
    # inputs
    system: str
    user: str
    tools: list[dict]
    # tool-use loop
    messages: list
    pending_calls: list
    llm_turns: int
    tool_calls_used: int
    tools_used: Annotated[list[str], operator.add]  # merged across parallel branches
    # drafting
    final_blocks: list[TextBlock]
    repairs: int
    repair_needed: bool
    # outputs
    classification: dict
    answer: dict
    proposal: dict | None


class Agent:
    def __init__(self, llm: LLMProvider, tools: ToolClient):
        self.llm = llm
        self.tools = tools
        self.max_tool_calls = get_settings().max_tool_calls
        self.triage_graph = self._build(triage=True)
        self.chat_graph = self._build(triage=False)

    # ---- entry points ------------------------------------------------------------------

    async def triage(self, req: TriageRequest) -> dict[str, Any]:
        employee = req.employee
        user = (
            f"<case number=\"{req.number}\">\n"
            f"Title: {req.title}\n"
            f"Description: {req.description}\n"
            f"Employee country: {employee.country or 'unknown'}; employee type: {employee.employee_type or 'unknown'}\n"
            f"</case>"
        )
        state = await self.triage_graph.ainvoke(self._initial(TRIAGE_SYSTEM, user, self._tools({"search_policies"})))
        return {"classification": state["classification"], "answer": state["answer"], "tools_used": state["tools_used"]}

    async def chat(self, req: ChatRequest) -> dict[str, Any]:
        user = f"<case number=\"{req.number}\"/>\n<request author=\"{req.author}\">\n{req.message}\n</request>"
        tools = [*self._tools(SEARCH_TOOLS | {"get_case"}), PROPOSE_CLOSE_TOOL]
        state = await self.chat_graph.ainvoke(self._initial(CHAT_SYSTEM, user, tools))
        return {"answer": state["answer"], "proposal": state.get("proposal"), "tools_used": state["tools_used"]}

    @staticmethod
    def _initial(system: str, user: str, tools: list[dict]) -> State:
        return {"system": system, "user": user, "tools": tools, "llm_turns": 0, "tool_calls_used": 0,
                "tools_used": [], "repairs": 0, "proposal": None}

    def _tools(self, names: set[str]) -> list[dict]:
        return [t for t in self.tools.tools if t["name"] in names]

    # ---- nodes ---------------------------------------------------------------------------

    async def classify(self, state: State) -> dict:
        result = await self.llm.structured(CLASSIFY_SYSTEM, state["user"], CLASSIFY_SCHEMA)
        result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))
        return {"classification": result}

    async def call_model(self, state: State) -> dict:
        messages = state.get("messages") or [self.llm.user_message(state["user"])]
        turn = await self.llm.turn(state["system"], messages, state["tools"])
        messages = [*messages, self.llm.assistant_message(turn)]
        turns = state["llm_turns"] + 1
        if turn.tool_calls and turns <= self.max_tool_calls + 1:
            return {"messages": messages, "llm_turns": turns, "pending_calls": turn.tool_calls}
        return {"messages": messages, "llm_turns": turns, "pending_calls": [], "final_blocks": turn.text_blocks}

    async def run_tools(self, state: State) -> dict:
        used, proposal = state["tool_calls_used"], state.get("proposal")
        results, names = [], []
        for call in state["pending_calls"]:
            names.append(call.name)
            if call.name == "propose_close":  # handled here: a proposal is recorded, never executed
                proposal = {"action": "close", "resolution": str(call.input.get("resolution", "")).strip()}
                results.append(ToolResult(call.id, text="Proposal recorded. An HR agent must approve it."))
                continue
            if used >= self.max_tool_calls:
                results.append(ToolResult(call.id, text="Tool budget used up. Answer with what you have.", is_error=True))
                continue
            used += 1
            try:
                data = await self.tools.call(call.name, call.input)
            except Exception as exc:  # report a failed tool to the model instead of failing the request
                log.warning("tool %s failed: %s", call.name, exc)
                results.append(ToolResult(call.id, text=f"Tool error: {exc}", is_error=True))
                continue
            if call.name in SEARCH_TOOLS:
                results.append(ToolResult(call.id, search_results=[
                    {"source": d["chunk_id"], "title": f"{d['title']} > {d['section']}", "passages": d["passages"]}
                    for d in data
                ]))
            else:
                results.append(ToolResult(call.id, text=str(data)))
        return {"messages": [*state["messages"], self.llm.tool_results_message(results)],
                "tool_calls_used": used, "pending_calls": [], "tools_used": names, "proposal": proposal}

    async def cite_check(self, state: State) -> dict:
        """Models sometimes paraphrase without citing; give them one chance to fix it."""
        if state["repairs"] >= MAX_REPAIRS:
            return {"repair_needed": False}
        answer = await self._check(state.get("final_blocks") or [])
        uncited = citations.uncited_sentences(answer)
        if not uncited:
            return {"repair_needed": False}
        note = "These sentences have no citation:\n- " + "\n- ".join(uncited) + "\n\n" + REPAIR_INSTRUCTION
        return {"repair_needed": True, "repairs": state["repairs"] + 1,
                "messages": [*state["messages"], self.llm.user_message(note)]}

    async def draft_done(self, state: State) -> dict:
        """Join point: in triage, verify waits for both this and classify."""
        return {}

    async def verify(self, state: State) -> dict:
        blocks = state.get("final_blocks") or []
        answer = await self._check(blocks)
        if not answer["all_claims_cited"]:
            # Still uncited after the repair pass: remove those sentences so nothing unverifiable is shown.
            keep = [b for b, claim in zip(blocks, answer["claims"], strict=True) if not citations.is_uncited(claim)]
            answer = await self._check(keep)
            answer["removed_uncited"] = len(blocks) - len(keep)
        return {"answer": answer}

    async def close_check(self, state: State) -> dict:
        """A staff request to close always yields a proposal; the model's doubts go into the resolution."""
        if state.get("proposal"):
            return {}
        decision = await self.llm.structured(
            CLOSE_CHECK_SYSTEM,
            f"{state['user']}\n\n<assistant_reply>\n{state['answer']['text']}\n</assistant_reply>",
            CLOSE_CHECK_SCHEMA,
        )
        if not decision.get("close_requested"):
            return {}
        return {"proposal": {"action": "close", "resolution": decision.get("resolution", "").strip()}}

    async def _check(self, blocks: list[TextBlock]) -> dict:
        """Verifies citations against the stored chunks (database read off the event loop)."""
        sources = sorted({c.source for b in blocks for c in b.citations})
        chunks = await asyncio.to_thread(get_chunks, sources) if sources else {}
        return citations.verify(blocks, chunks)

    # ---- wiring --------------------------------------------------------------------------

    @staticmethod
    def _after_model(state: State) -> str:
        return "tools" if state.get("pending_calls") else "cite_check"

    @staticmethod
    def _after_cite_check(state: State) -> str:
        return "model" if state.get("repair_needed") else "draft_done"

    def _build(self, triage: bool):
        g = StateGraph(State)
        g.add_node("model", self.call_model)
        g.add_node("tools", self.run_tools)
        g.add_node("cite_check", self.cite_check)
        g.add_node("draft_done", self.draft_done)
        g.add_node("verify", self.verify)

        g.add_edge(START, "model")
        g.add_conditional_edges("model", self._after_model, {"tools": "tools", "cite_check": "cite_check"})
        g.add_edge("tools", "model")
        g.add_conditional_edges("cite_check", self._after_cite_check, {"model": "model", "draft_done": "draft_done"})

        if triage:
            g.add_node("classify", self.classify)
            g.add_edge(START, "classify")  # runs in parallel with drafting
            g.add_edge(["classify", "draft_done"], "verify")
            g.add_edge("verify", END)
        else:
            g.add_node("close_check", self.close_check)
            g.add_edge("draft_done", "verify")
            g.add_edge("verify", "close_check")
            g.add_edge("close_check", END)
        return g.compile()
