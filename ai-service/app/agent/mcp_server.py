"""MCP server exposing the agent's tools. Runs as a stdio subprocess of the API.

Every tool is read-only. Tool descriptions are what the model reads to decide when to call them.

Some parameters are bound by the API, never chosen by the model (see BOUND_PARAMS): the
employee's country, which decides whose policies are visible, and the case being worked on.
mcp_client strips them from the schemas the model sees and fills them from the request.

Tools are async and run blocking work (database, models, HTTP) in a thread, so concurrent
requests sharing this one server do not wait for each other.
"""

import asyncio
import atexit
import json
import logging
import sys
from functools import cache
from typing import get_args

from mcp.server.fastmcp import FastMCP

from app.config import get_settings
from app.schemas import Category
from app.search.hybrid import Chunk, get_section, search
from app.sources import Source, make_source

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
mcp = FastMCP("hr-policy-tools")

# Parameters filled from the request, per tool. Kept in sync with the signatures below.
BOUND_PARAMS = {
    "search_policies": {"country"},
    "get_policy_section": {"country"},
    "get_case": {"case_number"},
}

POLICY_AREAS = [c for c in get_args(Category) if c != "unknown"]


@cache
def _source() -> Source:
    source = make_source(get_settings())
    atexit.register(source.close)
    return source


def _passage(chunk: Chunk) -> dict:
    """A chunk as the model sees it: where it comes from, plus its sentences (the citable units)."""
    return {
        "chunk_id": chunk["id"],
        "article": chunk["number"],
        "version": chunk["version"],
        "title": chunk["title"],
        "section": chunk["section_path"],
        "country": chunk["country"],
        "passages": [s["text"] for s in chunk["sentences"]],
    }


@mcp.tool(
    description="Search the employee's HR policies (their country's and global ones). Returns the "
    "most "
    f"relevant passages. category is optional: one of {', '.join(POLICY_AREAS)}."
)
async def search_policies(query: str, country: str = "", category: str | None = None) -> str:
    chunks = await asyncio.to_thread(search, query, country or None, category)
    return json.dumps([_passage(c) for c in chunks])


@mcp.tool()
async def get_policy_section(
    article: str, section: str | None = None, query: str | None = None, country: str = ""
) -> str:
    """Read one of the employee's HR policy articles by number (for example KB0010003).
    Narrow it with section (a phrase from the heading, for example 'Eligibility') or query (what
    you are looking for inside the article, for example 'notice period'). Without either, returns
    the start of the article.
    Returns nothing for articles that do not apply to this employee."""
    if query and not section:
        chunks = await asyncio.to_thread(search, query, country or None, None, 6, article)
    else:
        chunks = await asyncio.to_thread(get_section, article, country or None, section)
    return json.dumps([_passage(c) for c in chunks])


@mcp.tool()
async def get_case(case_number: str = "") -> str:
    """Read the HR case being worked on: description, state, category, assignment and the comment
    history. Read-only."""
    case = await asyncio.to_thread(_source().get_case, case_number) if case_number else None
    return json.dumps(case if case else {"error": "case not found"})


if __name__ == "__main__":
    mcp.run()
