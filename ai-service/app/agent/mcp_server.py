"""MCP server exposing the agent's tools. Runs as a stdio subprocess of the API.

Every tool is read-only. Tool descriptions are what the model reads to decide when to call them.
"""
import json
import logging
import sys

from mcp.server.fastmcp import FastMCP

from app.search.hybrid import get_section, search
from app.sources import get_source

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
mcp = FastMCP("hr-policy-tools")


def _passage(chunk: dict) -> dict:
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


@mcp.tool()
def search_policies(query: str, country: str | None = None, category: str | None = None) -> str:
    """Search HR policy articles. Returns the most relevant passages, already filtered to active
    policies for the given country (ISO code such as DE or US) plus global policies.
    category is optional: leave, benefits or payroll."""
    return json.dumps([_passage(c) for c in search(query, country=country, category=category)])


@mcp.tool()
def get_policy_section(article: str, section: str | None = None, query: str | None = None) -> str:
    """Read an HR policy article by number (for example KB0010003). Narrow it with section (a phrase
    from the heading, for example 'Eligibility') or query (what you are looking for inside the article,
    for example 'notice period'). Without either, returns the start of the article."""
    if query and not section:
        return json.dumps([_passage(c) for c in search(query, top_k=6, number=article)])
    return json.dumps([_passage(c) for c in get_section(article, section)])


@mcp.tool()
def get_case(number: str) -> str:
    """Read an HR case by number (for example HRC0001001): description, state, category,
    assignment and the comment history. Read-only."""
    case = get_source().get_case(number)
    return json.dumps(case if case else {"error": f"case {number} not found"})


if __name__ == "__main__":
    mcp.run()
