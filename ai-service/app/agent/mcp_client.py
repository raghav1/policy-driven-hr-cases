"""MCP client for the agent's tools.

The tool server (app.agent.mcp_server) runs as a stdio subprocess; one session is kept open for
the lifetime of the API process and shared by all requests.
"""
import asyncio
import json
import os
import sys
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


TOOL_TIMEOUT_SECONDS = 30


class ToolClient:
    def __init__(self):
        self._stack = AsyncExitStack()
        self._session: ClientSession | None = None
        self.tools: list[dict] = []

    async def start(self) -> None:
        params = StdioServerParameters(command=sys.executable, args=["-m", "app.agent.mcp_server"], env=dict(os.environ))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self._session = await self._stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()
        listed = await self._session.list_tools()
        self.tools = [{"name": t.name, "description": t.description or "", "input_schema": t.inputSchema} for t in listed.tools]

    async def stop(self) -> None:
        await self._stack.aclose()

    async def call(self, name: str, arguments: dict):
        """Calls a tool and returns its decoded JSON result. Raises on tool errors and timeouts."""
        if self._session is None:
            raise RuntimeError("tool server not started")
        result = await asyncio.wait_for(self._session.call_tool(name, arguments), TOOL_TIMEOUT_SECONDS)
        text = "".join(c.text for c in result.content if getattr(c, "type", "") == "text")
        if result.isError:
            raise RuntimeError(text or f"tool {name} failed")
        return json.loads(text)
