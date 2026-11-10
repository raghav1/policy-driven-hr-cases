"""Deterministic stand-in for the LLM, for running the whole system without a provider key.

It classifies with keyword rules, always searches the policies through the real MCP tools, and
answers with the retrieved policy sentences that best match the question, cited the way a model
would. Everything around it (API, graph, tools, search, citation checks) runs for real.
Enable with LLM_PROVIDER=offline.
"""
import re

from app.agent.llm import AnthropicProvider, Citation, LLMTurn, TextBlock, ToolCall

_STOPWORDS = set(
    "a an and are as at be by can do does for from get how i if in is it my of on or the to what when where "
    "which who why will with you your me am this that have has much many long".split()
)

_CATEGORY_WORDS = {
    "leave": "leave vacation holiday holidays sick ill illness bereavement maternity paternity parental "
             "time-off off funeral passed".split(),
    "benefits": "insurance health dental vision pension retirement 401k provident benefit benefits enrollment "
                "enroll gym wellbeing dependant spouse".split(),
    "payroll": "pay paid payday salary payslip payroll overtime expense expenses reimburse reimbursement "
               "mileage overpaid underpaid".split(),
}

_URGENT_WORDS = {"urgent", "asap", "immediately", "missing"}


def _words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in _STOPWORDS]


class OfflineProvider(AnthropicProvider):
    """Reuses the Anthropic message format so the graph code path is identical."""

    def __init__(self):  # no client: nothing leaves the machine
        self.model = "offline-stub"

    async def structured(self, system: str, user: str, schema: dict) -> dict:
        words = set(_words(user))
        hits = {category: len(words & set(terms)) for category, terms in _CATEGORY_WORDS.items()}
        category, score = max(hits.items(), key=lambda kv: kv[1])
        urgent = bool(words & _URGENT_WORDS)
        return {
            "category": category if score else "unknown",
            "topics": sorted(words & set(_CATEGORY_WORDS[category]))[:3] if score else [],
            "priority": 2 if urgent else 3 if score else 4,
            "severity": "medium" if urgent else "low",
            "confidence": 0.85 if score >= 2 else 0.65 if score == 1 else 0.3,
            "reasoning": f"Offline keyword classifier matched {score} {category} terms."
                         if score else "No HR topic keywords found.",
        }

    async def turn(self, system: str, messages: list, tools: list[dict]) -> LLMTurn:
        last = messages[-1]
        if isinstance(last["content"], str):
            return self._choose_tools(last["content"], {t["name"] for t in tools})
        return self._answer_from_results(messages)

    @staticmethod
    def _choose_tools(prompt: str, available: set[str]) -> LLMTurn:
        question = re.sub(r"<[^>]+>", " ", prompt)
        calls = []
        article = re.search(r"\bKB\d{7}\b", question)
        if article and "get_policy_section" in available:
            rest = " ".join(w for w in _words(question) if w != article.group(0).lower())
            calls.append(ToolCall("call_1", "get_policy_section", {"article": article.group(0), "query": rest or "policy"}))
        else:
            args = {"query": " ".join(_words(question))[:300]}
            country = re.search(r"Employee country: ([A-Z]{2})\b", prompt)
            if country:
                args["country"] = country.group(1)
            calls.append(ToolCall("call_1", "search_policies", args))
        if "propose_close" in available and re.search(r"\bclose\b", question, re.I):
            calls.append(ToolCall("call_2", "propose_close", {"resolution": "Question answered with the relevant policy."}))
        content = [{"type": "tool_use", "id": c.id, "name": c.name, "input": c.input} for c in calls]
        return LLMTurn([], calls, content)

    @staticmethod
    def _answer_from_results(messages: list) -> LLMTurn:
        """Quotes the two retrieved sentences that share the most words with the question."""
        question = next(m["content"] for m in messages if m["role"] == "user" and isinstance(m["content"], str))
        q = set(_words(re.sub(r"<[^>]+>", " ", question)))
        results = [r for block in messages[-1]["content"] if block.get("type") == "tool_result" for r in block["content"]]
        candidates = []
        for rank, result in enumerate(r for r in results if r.get("type") == "search_result"):
            for i, sentence in enumerate(result["content"]):
                overlap = len(q & set(_words(sentence["text"])))
                if overlap:
                    candidates.append((overlap, -rank, -i, result["source"], i, sentence["text"]))
        best = sorted(candidates, reverse=True)[:2]
        if not best:
            blocks = [TextBlock("I couldn't find a policy that covers this. The HR team will follow up.")]
        else:
            best.sort(key=lambda c: (-c[1], -c[2]))  # back to reading order
            blocks = [TextBlock("Here is what the policy says: ")]
            blocks += [TextBlock(text + " ", [Citation(source, i, i + 1, text)]) for _, _, _, source, i, text in best]
        return LLMTurn(blocks, [], [{"type": "text", "text": b.text} for b in blocks])
