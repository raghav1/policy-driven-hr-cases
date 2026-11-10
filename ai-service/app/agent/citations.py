"""Citation verification and reply formatting.

Each citation points at a range of sentences in a retrieved chunk. It is accepted only if the
quoted text matches the stored sentences word for word (ignoring whitespace), so an answer can
always be traced to an exact place in a specific article version.
"""
import re

from app.agent.llm import Citation, TextBlock

# A text block longer than this without a citation counts as an uncited claim.
# Shorter ones are connective text such as "Here is what the policy says:".
UNCITED_LIMIT = 80


def verify(blocks: list[TextBlock], chunks: dict[str, dict]) -> dict:
    """Checks every citation and builds the reply.

    Returns text with [n] markers, a formatted version with a numbered reference list, the claims
    with their verified references, and whether every substantive claim is cited.
    """
    claims, references, ref_numbers = [], [], {}
    dropped = 0
    for block in blocks:
        cites = []
        for citation in block.citations:
            ref = _reference(citation, chunks.get(citation.source))
            if ref is None:
                dropped += 1
                continue
            key = (citation.source, citation.start_block, citation.end_block)
            if key not in ref_numbers:
                ref_numbers[key] = len(references) + 1
                references.append({"n": ref_numbers[key], **ref})
            cites.append(references[ref_numbers[key] - 1])
        claims.append({"text": block.text, "citations": cites})

    text = _render(claims)
    formatted = text
    if references:
        formatted += "\n\n" + "\n".join(
            f"[{r['n']}] {r['title']}, {r['section']} ({r['article']} v{r['version']}): \"{r['quote']}\""
            for r in references
        )
    public_claims = [
        {"text": c["text"], "citations": [{**{k: v for k, v in r.items() if k != "n"}, "ref": r["n"]} for r in c["citations"]]}
        for c in claims
    ]
    return {
        "text": text,
        "formatted": formatted,
        "claims": public_claims,
        "references": references,
        "all_claims_cited": dropped == 0 and not any(is_uncited(c) for c in public_claims),
        "dropped_citations": dropped,
        "removed_uncited": 0,
    }


def is_uncited(claim: dict) -> bool:
    return not claim["citations"] and len(claim["text"].strip()) > UNCITED_LIMIT


def uncited_sentences(answer: dict) -> list[str]:
    return [c["text"].strip() for c in answer["claims"] if is_uncited(c)]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _reference(citation: Citation, chunk: dict | None) -> dict | None:
    """The reference for a citation, or None if its quote does not match the stored text."""
    sentences = chunk["sentences"][citation.start_block:citation.end_block] if chunk else []
    if not sentences:
        return None
    texts = [s["text"] for s in sentences]
    if _norm(citation.cited_text) not in (_norm(" ".join(texts)), _norm("".join(texts))):
        return None
    return {
        "article": chunk["number"],
        "version": chunk["version"],
        "chunk_id": citation.source,
        "title": chunk["title"],
        "section": chunk["section_path"],
        "quote": " ".join(texts),
        "start_char": sentences[0]["start"],
        "end_char": sentences[-1]["end"],
    }


def _render(claims: list[dict]) -> str:
    """Joins claim text and appends [n] markers, keeping natural spacing and punctuation."""
    reply = ""
    for claim in claims:
        segment = claim["text"]
        # Keep a space between a marker and the next word ("[1] Submit", not "[1]Submit").
        if reply and not reply[-1].isspace() and segment and not segment[0].isspace() and segment[0] not in ".,;:!?)":
            reply += " "
        reply += segment.rstrip() + "".join(f" [{c['n']}]" for c in claim["citations"])
    return re.sub(r"[ \t]+([.,;:])", r"\1", reply.strip())
