"""Citation verification and reply formatting.

Each citation points at a range of sentences in a retrieved chunk. It is accepted only if the
quoted text matches the stored sentences word for word (ignoring whitespace) and the chunk is a
policy for the employee's country or a global one. So an answer can always be traced to an exact
place in a specific article version, and never to another country's policy.
"""

import re
from collections.abc import Collection

from app.agent.llm import Citation, TextBlock
from app.schemas import Answer, ChunkId, Claim, Reference
from app.search.hybrid import Chunk

# Text without a citation is allowed only as short connective text ("Here is what the policy
# says:", "The HR team will follow up."). It must be at most this long and contain nothing that
# reads as a policy fact.
CONNECTIVE_MAX_CHARS = 80
_FACT = re.compile(
    r"\d|[$€£₹%]"
    r"|\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty"
    r"|thirty|hundred"
    r"|half|double|full|days?|weeks?|months?|years?|hours?|annual|daily|weekly|monthly|percent"
    r"|salary|pay|paid|unpaid|entitled|entitlement|eligible|eligibility|must|deadline|notice"
    r"|allowance|reimburs\w*|contribut\w*|match\w*|cover\w*|limit\w*|maximum|minimum)\b",
    re.IGNORECASE,
)


def verify(
    blocks: list[TextBlock], chunks: dict[ChunkId, Chunk], countries: Collection[str]
) -> Answer:
    """Checks every citation and builds the reply.

    countries: the policy countries this employee may be told about (their own and GLOBAL).
    """
    claims: list[Claim] = []
    references: list[Reference] = []
    ref_numbers: dict[tuple, int] = {}
    dropped = 0
    for block in blocks:
        cites = []
        for citation in block.citations:
            ref = _reference(citation, chunks.get(ChunkId(citation.source)), countries)
            if ref is None:
                dropped += 1
                continue
            key = (citation.source, citation.start_block, citation.end_block)
            if key not in ref_numbers:
                ref_numbers[key] = len(references) + 1
                references.append(ref.model_copy(update={"ref": ref_numbers[key]}))
            cites.append(references[ref_numbers[key] - 1])
        claims.append(Claim(text=block.text, citations=cites))

    text = _render(claims)
    formatted = text
    if references:
        formatted += "\n\n" + "\n".join(
            f'[{r.ref}] {r.title}, {r.section} ({r.article} v{r.version}): "{r.quote}"'
            for r in references
        )
    return Answer(
        text=text,
        formatted=formatted,
        claims=claims,
        references=references,
        all_claims_cited=dropped == 0 and not any(is_uncited(c) for c in claims),
        dropped_citations=dropped,
    )


def is_uncited(claim: Claim) -> bool:
    """True when a block states something without a citation."""
    if claim.citations:
        return False
    text = claim.text.strip()
    return len(text) > CONNECTIVE_MAX_CHARS or bool(_FACT.search(text))


def uncited_sentences(answer: Answer) -> list[str]:
    return [c.text.strip() for c in answer.claims if is_uncited(c)]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _reference(
    citation: Citation, chunk: Chunk | None, countries: Collection[str]
) -> Reference | None:
    """The reference for a citation, or None unless verified quote from an allowed policy."""
    if chunk is None or chunk["country"] not in countries:
        return None
    sentences = chunk["sentences"][citation.start_block : citation.end_block]
    if not sentences:
        return None
    texts = [s["text"] for s in sentences]
    if _norm(citation.cited_text) not in (_norm(" ".join(texts)), _norm("".join(texts))):
        return None
    return Reference(
        ref=0,
        article=chunk["number"],
        version=chunk["version"],
        chunk_id=ChunkId(citation.source),
        title=chunk["title"],
        section=chunk["section_path"],
        country=chunk["country"],
        quote=" ".join(texts),
        start_char=sentences[0]["start"],
        end_char=sentences[-1]["end"],
    )


def _render(claims: list[Claim]) -> str:
    """Joins claim text and appends [n] markers, keeping natural spacing and punctuation."""
    reply = ""
    for claim in claims:
        segment = claim.text
        # Keep a space between a marker and the next word ("[1] Submit", not "[1]Submit").
        if (
            reply
            and not reply[-1].isspace()
            and segment
            and not segment[0].isspace()
            and segment[0] not in ".,;:!?)"
        ):
            reply += " "
        reply += segment.rstrip() + "".join(f" [{c.ref}]" for c in claim.citations)
    return re.sub(r"[ \t]+([.,;:])", r"\1", reply.strip())
