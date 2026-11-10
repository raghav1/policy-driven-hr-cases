"""A scripted stand-in for the LLM provider, for tests that run the real graph, tools and index."""

from app.agent.llm import AnthropicMessages, Citation, LLMTurn, TextBlock, ToolCall

LEAVE = {
    "category": "leave",
    "topics": ["parental_leave"],
    "priority": 3,
    "severity": "low",
    "confidence": 0.9,
    "reasoning": "Asks about parental leave.",
}


def first_result(messages: list) -> dict | None:
    """The first search result in the latest tool message, as the model would see it."""
    for message in reversed(messages):
        if isinstance(message["content"], list) and message["role"] == "user":
            for block in message["content"]:
                for item in block.get("content", []):
                    if item.get("type") == "search_result":
                        return item
            return None
    return None


class ScriptedLLM(AnthropicMessages):
    """Turn 1: one tool call. Turn 2 onwards: answer() builds the reply from the tool results.

    Default answer: one sentence citing the first returned passage word for word.
    """

    model = "scripted"

    def __init__(
        self, tool_call: ToolCall | None = None, answer=None, classification: dict | None = None
    ):
        self.tool_call = tool_call or ToolCall(
            "t1", "search_policies", {"query": "parental leave length"}
        )
        self.answer = answer or self.cite_first
        self.classification = classification or LEAVE
        self.calls = 0
        self.seen: list[list] = []  # messages the model received on each turn

    async def structured(self, system, user, schema):
        if "close_requested" in schema["properties"]:
            return {"close_requested": False, "resolution": ""}
        return dict(self.classification)

    async def turn(self, system, messages, tools):
        self.calls += 1
        self.seen.append(messages)
        if self.calls == 1:
            return LLMTurn([], [self.tool_call], [])
        blocks = self.answer(messages)
        return LLMTurn(blocks, [], [{"type": "text", "text": b.text} for b in blocks])

    @staticmethod
    def cite_first(messages: list) -> list[TextBlock]:
        result = first_result(messages)
        if result is None:
            return [TextBlock("I couldn't find a policy that covers this.")]
        quote = result["content"][0]["text"]
        return [TextBlock("Here is the rule.", [Citation(result["source"], 0, 1, quote)])]
