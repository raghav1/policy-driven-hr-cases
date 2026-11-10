from app.ingest.chunk import chunk_article
from app.ingest.parse import parse_html, split_sentences

HTML = """
<h2>Eligibility</h2>
<p>Employees in Germany are eligible after 6 months.
Parental leave applies to every parent, e.g. adoptive parents.</p>
<h2>Entitlement</h2>
<h3>Standard entitlement</h3>
<p>Employees in Germany are entitled to up to 3 years of parental leave per child.</p>
<ul><li>Leave can be taken in blocks.</li><li>Each block lasts at least two weeks.</li></ul>
<h3>Key figures</h3>
<table><tr><th>Item</th><th>Value</th></tr><tr><td>Notice period</td><td>7 weeks</td></tr></table>
"""


def test_sentence_split_keeps_abbreviations():
    assert split_sentences("Applies to all, e.g. adoptive parents. Second one.") == [
        "Applies to all, e.g. adoptive parents.",
        "Second one.",
    ]


def test_every_unit_is_an_exact_slice_of_the_article_text():
    parsed = parse_html("Parental leave (Germany)", HTML)
    for section in parsed.sections:
        for unit in section.units:
            assert parsed.text[unit.start : unit.end] == unit.text


def test_sections_carry_their_heading_path():
    parsed = parse_html("Parental leave (Germany)", HTML)
    paths = [" > ".join(s.path) for s in parsed.sections]
    assert "Parental leave (Germany) > Entitlement > Standard entitlement" in paths
    assert "Parental leave (Germany) > Entitlement > Key figures" in paths


def test_table_rows_repeat_their_headers():
    parsed = parse_html("T", HTML)
    rows = [u.text for s in parsed.sections for u in s.units if "Notice period" in u.text]
    assert rows == ["Item: Notice period; Value: 7 weeks."]


def test_chunks_stay_within_a_section_and_overlap():
    sentences = " ".join(f"Sentence number {i} has exactly seven words." for i in range(60))
    parsed = parse_html("T", f"<h2>A</h2><p>{sentences}</p><h2>B</h2><p>Short.</p>")
    chunks = chunk_article(parsed, target_words=70, overlap_words=14)
    a_chunks = [c for c in chunks if c.section_path == "A"]
    assert len(a_chunks) > 1
    assert all(sum(len(u.text.split()) for u in c.units) <= 70 for c in a_chunks)
    # consecutive chunks share their boundary sentences
    assert (
        a_chunks[0].units[-1].text == a_chunks[1].units[0].text
        or a_chunks[0].units[-2].text == a_chunks[1].units[0].text
    )
    assert [c.section_path for c in chunks][-1] == "B"
    assert all(len(c.units) for c in chunks)
