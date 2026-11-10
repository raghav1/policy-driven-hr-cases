"""Turns article HTML into normalized text with a section path and offsets for every unit.

A unit is the smallest citable piece: one sentence of prose, one list item sentence, or one
table row. Every unit's text is an exact slice of the normalized article text, so a citation
can always be traced back to a position in a specific article version.
"""
import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup, NavigableString, Tag

_SENTENCE_END = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"(“])')
_ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "approx.", "no.", "vs.", "Mr.", "Ms.", "Dr.")


@dataclass
class Unit:
    text: str
    start: int
    end: int


@dataclass
class Section:
    path: list[str]
    units: list[Unit] = field(default_factory=list)


@dataclass
class ParsedArticle:
    text: str
    sections: list[Section]


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def split_sentences(paragraph: str) -> list[str]:
    parts = _SENTENCE_END.split(paragraph)
    merged: list[str] = []
    for part in parts:
        if merged and merged[-1].endswith(_ABBREVIATIONS):
            merged[-1] = f"{merged[-1]} {part}"
        else:
            merged.append(part)
    return [p for p in merged if p]


def _table_rows(table: Tag) -> list[str]:
    rows = table.find_all("tr")
    if not rows:
        return []
    header = [_clean(c.get_text(" ")) for c in rows[0].find_all(["th", "td"])]
    out = []
    for row in rows[1:]:
        cells = [_clean(c.get_text(" ")) for c in row.find_all(["th", "td"])]
        # Each row carries its headers, so a row read on its own still makes sense.
        # Rows can be ragged; zip stops at the shorter list.
        pairs = [f"{h}: {v}" for h, v in zip(header, cells, strict=False) if v]
        if pairs:
            out.append("; ".join(pairs) + ".")
    return out


def parse_html(title: str, html: str) -> ParsedArticle:
    soup = BeautifulSoup(html, "html.parser")
    buf: list[str] = []
    pos = 0
    sections: list[Section] = []
    headings: list[tuple[int, str]] = []  # open headings as (level, text)
    current = Section(path=[title])

    def emit(text: str, sep: str = "\n\n") -> tuple[int, int]:
        nonlocal pos
        if buf:
            buf.append(sep)
            pos += len(sep)
        start = pos
        buf.append(text)
        pos += len(text)
        return start, pos

    def add_units(pieces: list[str]) -> None:
        first = True
        for piece in pieces:
            start, end = emit(piece, "\n\n" if first else " ")
            current.units.append(Unit(piece, start, end))
            first = False

    def walk(node: Tag) -> None:
        nonlocal current
        for child in node.children:
            if isinstance(child, NavigableString):
                text = _clean(str(child))
                if text:
                    add_units(split_sentences(text))
                continue
            if not isinstance(child, Tag):
                continue
            name = child.name.lower()
            if name in ("h1", "h2", "h3"):
                level = int(name[1])
                heading = _clean(child.get_text(" "))
                if not heading:
                    continue
                if current.units:
                    sections.append(current)
                while headings and headings[-1][0] >= level:
                    headings.pop()
                headings.append((level, heading))
                current = Section(path=[title, *(h for _, h in headings)])
                emit(heading)
            elif name in ("p", "li"):
                text = _clean(child.get_text(" "))
                if text:
                    add_units(split_sentences(text))
            elif name == "table":
                rows = _table_rows(child)
                if rows:
                    for row in rows:
                        start, end = emit(row, "\n")
                        current.units.append(Unit(row, start, end))
            else:
                walk(child)

    walk(soup)
    if current.units:
        sections.append(current)
    return ParsedArticle(text="".join(buf), sections=sections)
