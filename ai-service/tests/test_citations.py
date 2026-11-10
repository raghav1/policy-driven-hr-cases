from app.agent.citations import verify
from app.agent.llm import Citation, TextBlock
from app.search.hybrid import rrf

CHUNKS = {
    "KB0010002#v1#c5": {
        "number": "KB0010002",
        "version": 1,
        "title": "Parental leave (Germany)",
        "section_path": "Entitlement > Standard entitlement",
        "sentences": [
            {"text": "Employees in Germany are entitled to up to 3 years of parental leave per child.", "start": 100, "end": 180},
            {"text": "Leave must be requested in writing at least 7 weeks before it starts.", "start": 181, "end": 250},
        ],
    }
}


def test_valid_citation_is_kept_with_exact_quote_and_offsets():
    blocks = [TextBlock("You can take up to three years of parental leave per child.", [
        Citation("KB0010002#v1#c5", 0, 1, "Employees in Germany are entitled to up to 3 years of parental leave per child.")
    ])]
    out = verify(blocks, CHUNKS)
    assert out["all_claims_cited"]
    ref = out["references"][0]
    assert ref["quote"].startswith("Employees in Germany")
    assert (ref["start_char"], ref["end_char"]) == (100, 180)
    assert out["text"].endswith("[1]")
    assert '[1] Parental leave (Germany), Entitlement > Standard entitlement (KB0010002 v1)' in out["formatted"]


def test_quote_that_does_not_match_the_source_is_dropped():
    blocks = [TextBlock("You get five years.", [Citation("KB0010002#v1#c5", 0, 1, "Employees get 5 years of leave.")])]
    out = verify(blocks, CHUNKS)
    assert out["references"] == []
    assert out["dropped_citations"] == 1
    assert not out["all_claims_cited"]


def test_long_uncited_claim_fails_the_citation_rule():
    blocks = [TextBlock("Parental leave in Germany is generous and you can take as much as you like whenever it suits you.", [])]
    assert not verify(blocks, CHUNKS)["all_claims_cited"]


def test_multi_block_citation_joins_sentences():
    both = " ".join(s["text"] for s in CHUNKS["KB0010002#v1#c5"]["sentences"])
    blocks = [TextBlock("Up to three years, with seven weeks' notice.", [Citation("KB0010002#v1#c5", 0, 2, both)])]
    out = verify(blocks, CHUNKS)
    assert out["all_claims_cited"] and out["references"][0]["end_char"] == 250


def test_rrf_rewards_items_ranked_well_in_both_lists():
    assert rrf([["a", "b", "c"], ["c", "a", "d"]])[:2] == ["a", "c"]
