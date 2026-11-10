from app.agent.citations import is_uncited, verify
from app.agent.llm import Citation, TextBlock
from app.schemas import Claim
from app.search.hybrid import rrf

DE_CHUNK = "KB0010002#v1#c5"
US_CHUNK = "KB0010001#v1#c2"
CHUNKS = {
    DE_CHUNK: {
        "id": DE_CHUNK,
        "number": "KB0010002",
        "version": 1,
        "title": "Parental leave (Germany)",
        "section_path": "Entitlement > Standard entitlement",
        "country": "DE",
        "sentences": [
            {
                "text": "Employees in Germany are entitled to up to 3 years of parental leave "
                "per child.",
                "start": 100,
                "end": 180,
            },
            {
                "text": "Leave must be requested in writing at least 7 weeks before it starts.",
                "start": 181,
                "end": 250,
            },
        ],
    },
    US_CHUNK: {
        "id": US_CHUNK,
        "number": "KB0010001",
        "version": 1,
        "title": "Parental leave (United States)",
        "section_path": "Entitlement",
        "country": "US",
        "sentences": [
            {
                "text": "Employees are entitled to 16 weeks of paid parental leave.",
                "start": 0,
                "end": 58,
            }
        ],
    },
}
GERMANY = ["DE", "GLOBAL"]


def test_valid_citation_is_kept_with_exact_quote_and_offsets():
    quote = "Employees in Germany are entitled to up to 3 years of parental leave per child."
    blocks = [
        TextBlock(
            "You can take up to three years of parental leave per child.",
            [Citation(DE_CHUNK, 0, 1, quote)],
        )
    ]
    out = verify(blocks, CHUNKS, GERMANY)
    assert out.all_claims_cited and out.found_policy
    ref = out.references[0]
    assert ref.quote.startswith("Employees in Germany")
    assert (ref.start_char, ref.end_char) == (100, 180)
    assert out.text.endswith("[1]")
    assert (
        "[1] Parental leave (Germany), Entitlement > Standard entitlement (KB0010002 v1)"
        in out.formatted
    )


def test_quote_that_does_not_match_the_source_is_dropped():
    blocks = [
        TextBlock(
            "You get five years.", [Citation(DE_CHUNK, 0, 1, "Employees get 5 years of leave.")]
        )
    ]
    out = verify(blocks, CHUNKS, GERMANY)
    assert out.references == []
    assert out.dropped_citations == 1
    assert not out.all_claims_cited


def test_citation_to_another_countrys_policy_is_dropped():
    quote = "Employees are entitled to 16 weeks of paid parental leave."
    blocks = [TextBlock("You get 16 weeks of paid leave.", [Citation(US_CHUNK, 0, 1, quote)])]
    out = verify(blocks, CHUNKS, GERMANY)
    assert out.references == [] and out.dropped_citations == 1
    assert not out.all_claims_cited


def test_long_uncited_claim_fails_the_citation_rule():
    text = (
        "Parental leave in Germany is generous and you can take as much as you like whenever "
        "it suits you."
    )
    assert not verify([TextBlock(text, [])], CHUNKS, GERMANY).all_claims_cited


def test_short_uncited_fact_fails_the_citation_rule():
    for text in (
        "You get 16 weeks.",
        "Leave is paid.",
        "You are eligible.",
        "Notice is required.",
        "It's €400.",
    ):
        assert is_uncited(Claim(text=text, citations=[])), text
        assert not verify([TextBlock(text, [])], CHUNKS, GERMANY).all_claims_cited, text


def test_short_connective_text_is_allowed():
    for text in ("Here is what the policy says:", "The HR team will follow up.", "\n\n"):
        assert not is_uncited(Claim(text=text, citations=[])), text


def test_multi_block_citation_joins_sentences():
    both = " ".join(s["text"] for s in CHUNKS[DE_CHUNK]["sentences"])
    blocks = [
        TextBlock("Up to three years, with seven weeks' notice.", [Citation(DE_CHUNK, 0, 2, both)])
    ]
    out = verify(blocks, CHUNKS, GERMANY)
    assert out.all_claims_cited and out.references[0].end_char == 250


def test_rrf_rewards_items_ranked_well_in_both_lists():
    assert rrf([["a", "b", "c"], ["c", "a", "d"]])[:2] == ["a", "c"]
