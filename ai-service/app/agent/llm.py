"""LLM provider adapter.

The agent graph talks to models only through the neutral types and the LLMProvider protocol
defined here, so a provider can be swapped (or replaced by the offline stand-in) without
touching the workflow.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Protocol

import anthropic

from app.config import get_settings
from app.errors import AgentError

log = logging.getLogger(__name__)


@dataclass
class Citation:
    """Points at a range of sentences in one retrieved passage."""

    source: str  # chunk id, for example KB0090002#v1#c5
    start_block: int  # first sentence index (inclusive)
    end_block: int  # last sentence index (exclusive)
    cited_text: str


@dataclass
class TextBlock:
    text: str
    citations: list[Citation] = field(default_factory=list)


@dataclass
class ToolCall:
    id: str
    name: str
    input: dict


@dataclass
class LLMTurn:
    text_blocks: list[TextBlock]
    tool_calls: list[ToolCall]
    raw_assistant: Any  # provider-specific content, replayed unchanged on the next turn


@dataclass
class ToolResult:
    """What a tool returned: citable passages (search tools) or plain text."""

    call_id: str
    search_results: list[dict] | None = None  # [{"source", "title", "passages": [sentence, ...]}]
    text: str | None = None
    is_error: bool = False


class LLMProvider(Protocol):
    model: str

    async def structured(self, system: str, user: str, schema: dict) -> dict:
        """One call whose answer must match the JSON schema."""

    async def turn(self, system: str, messages: list, tools: list[dict]) -> LLMTurn:
        """One step of the tool-use loop."""

    def user_message(self, text: str) -> Any: ...

    def assistant_message(self, turn: LLMTurn) -> Any: ...

    def tool_results_message(self, results: list[ToolResult]) -> Any: ...


class AnthropicMessages:
    """Anthropic Messages API formats, shared by the real provider and the offline stand-in."""

    @staticmethod
    def user_message(text: str) -> dict:
        return {"role": "user", "content": text}

    @staticmethod
    def assistant_message(turn: LLMTurn) -> dict:
        return {"role": "assistant", "content": turn.raw_assistant}

    @staticmethod
    def tool_results_message(results: list[ToolResult]) -> dict:
        content = []
        for r in results:
            if r.search_results is not None:
                # One text block per sentence, so a citation can point at whole sentences.
                body = [
                    {
                        "type": "search_result",
                        "source": sr["source"],
                        "title": sr["title"],
                        "content": [
                            {"type": "text", "text": sentence} for sentence in sr["passages"]
                        ],
                        "citations": {"enabled": True},
                    }
                    for sr in r.search_results
                ] or [{"type": "text", "text": "No relevant policy found."}]
            else:
                body = [{"type": "text", "text": r.text or ""}]
            content.append(
                {
                    "type": "tool_result",
                    "tool_use_id": r.call_id,
                    "content": body,
                    "is_error": r.is_error,
                }
            )
        return {"role": "user", "content": content}


class AnthropicProvider(AnthropicMessages):
    """Claude through the official Anthropic SDK.

    Search results are sent as search_result blocks with citations enabled, so the model's answer
    comes back with each statement tied to the exact sentences it relied on.
    """

    def __init__(self):
        s = get_settings()
        self.model = s.llm_model
        self._max_tokens = s.llm_max_tokens
        self._client = anthropic.AsyncAnthropic(max_retries=2, timeout=90)

    async def _create(self, **kwargs):
        try:
            if self.model.startswith("claude-haiku"):
                # Haiku has no server-side refusal fallback; a refusal surfaces as llm_refused
                # below.
                response = await self._client.messages.create(
                    model=self.model, max_tokens=self._max_tokens, **kwargs
                )
            else:
                # Server-side fallback re-runs a declined request on another model within the same
                # call.
                response = await self._client.beta.messages.create(
                    model=self.model,
                    max_tokens=self._max_tokens,
                    betas=["server-side-fallback-2026-07-01"],
                    fallbacks="default",
                    **kwargs,
                )
        except anthropic.APIError as exc:
            log.warning("model call failed: %s", exc)
            raise AgentError("llm_unavailable", "the language model could not be reached") from exc
        if response.stop_reason == "refusal":
            raise AgentError("llm_refused", "the language model declined the request")
        if response.stop_reason == "max_tokens":
            raise AgentError("llm_truncated", "the language model's answer was cut off")
        return response

    async def structured(self, system: str, user: str, schema: dict) -> dict:
        response = await self._create(
            system=system,
            messages=[{"role": "user", "content": user}],
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": schema}},
        )
        text = next((b.text for b in response.content if b.type == "text"), None)
        try:
            return json.loads(text or "")
        except json.JSONDecodeError as exc:
            raise AgentError(
                "llm_invalid_output", "the language model returned invalid structured output"
            ) from exc

    async def turn(self, system: str, messages: list, tools: list[dict]) -> LLMTurn:
        response = await self._create(
            system=system,
            messages=messages,
            tools=[
                {
                    "name": t["name"],
                    "description": t["description"],
                    "input_schema": t["input_schema"],
                }
                for t in tools
            ],
            output_config={"effort": "low"},
        )
        texts, calls = [], []
        for block in response.content:
            if block.type == "text":
                cites = [
                    Citation(c.source, c.start_block_index, c.end_block_index, c.cited_text)
                    for c in (block.citations or [])
                    if c.type == "search_result_location"
                ]
                texts.append(TextBlock(block.text, cites))
            elif block.type == "tool_use":
                calls.append(ToolCall(block.id, block.name, dict(block.input)))
        return LLMTurn(texts, calls, response.content)


def get_provider() -> LLMProvider:
    if get_settings().llm_provider == "offline":
        from app.agent.offline import OfflineProvider

        return OfflineProvider()
    return AnthropicProvider()
