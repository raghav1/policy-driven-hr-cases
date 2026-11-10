"""MCP client for the agent's tools.

The tool server (app.agent.mcp_server) runs as a stdio subprocess; one session is kept open for
the lifetime of the API process and shared by all requests.

Bound parameters (the employee's country, the case number) are removed from the schemas the model
sees and always filled from the request, so the model cannot widen what it may read.
"""

import asyncio
import copy
import json
import os
import sys
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.agent.mcp_server import BOUND_PARAMS

TOOL_TIMEOUT_SECONDS = 30


def _without(schema: dict, names: set[str]) -> dict:
    schema = copy.deepcopy(schema)
    for name in names:
        schema.get("properties", {}).pop(name, None)
    if "required" in schema:
        schema["required"] = [r for r in schema["required"] if r not in names]
    return schema


class ToolClient:
    def __init__(self):
        self._stack = AsyncExitStack()
        self._session: ClientSession | None = None
        self.tools: list[dict] = []  # as the model sees them

    async def start(self) -> None:
        params = StdioServerParameters(
            command=sys.executable, args=["-m", "app.agent.mcp_server"], env=dict(os.environ)
        )
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self._session = await self._stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()
        listed = await self._session.list_tools()
        self.tools = [
            {
                "name": t.name,
                "description": t.description or "",
                "input_schema": _without(t.inputSchema, BOUND_PARAMS.get(t.name, set())),
            }
            for t in listed.tools
        ]

    async def stop(self) -> None:
        await self._stack.aclose()

    async def call(self, name: str, arguments: dict, bound: dict[str, str]):
        """Calls a tool and returns its decoded JSON result. Raises on tool errors and timeouts.

        bound: request values for the tool's bound parameters; they replace anything the model sent.
        """
        if self._session is None:
            raise RuntimeError("tool server not started")
        names = BOUND_PARAMS.get(name, set())
        args = {k: v for k, v in arguments.items() if k not in names}
        args.update({k: bound.get(k, "") for k in names})
        result = await asyncio.wait_for(self._session.call_tool(name, args), TOOL_TIMEOUT_SECONDS)
        text = "".join(c.text for c in result.content if getattr(c, "type", "") == "text")
        if result.isError:
            raise RuntimeError(text or f"tool {name} failed")
        return json.loads(text)
