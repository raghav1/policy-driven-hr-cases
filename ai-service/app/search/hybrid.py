"""Hybrid retrieval: vector + keyword search, merged with reciprocal rank fusion, then reranked."""
import re

from app.config import get_settings
from app.db import connection
from app.search.models import embed_query, rerank

_CHUNK_COLUMNS = "id, number, version, title, section_path, category, country, text, start_char, end_char, sentences"


def rrf(rankings: list[list[str]], k: int = 60) -> list[str]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=lambda item: scores[item], reverse=True)


def _keyword_query(query: str) -> str | None:
    words = re.findall(r"[A-Za-z0-9]+", query.lower())
    return " | ".join(words) if words else None


def _filters(country: str | None, category: str | None, number: str | None = None) -> tuple[str, list]:
    clauses, params = ["active"], []
    if number:
        clauses.append("number = %s")
        params.append(number.upper())
    if country:
        clauses.append("country = ANY(%s)")
        params.append([country.upper(), "GLOBAL"])
    if category:
        clauses.append("category = %s")
        params.append(category.lower())
    return " AND ".join(clauses), params


def search(query: str, country: str | None = None, category: str | None = None, top_k: int | None = None,
           number: str | None = None) -> list[dict]:
    s = get_settings()
    top_k = top_k or s.search_top_k
    where, params = _filters(country, category, number)
    vector = embed_query(query)

    with connection() as conn:
        by_vector = conn.execute(
            f"SELECT id FROM policy_chunk WHERE {where} ORDER BY embedding <=> %s LIMIT %s",
            [*params, vector, s.search_candidates],
        ).fetchall()
        by_keyword = []
        tsquery = _keyword_query(query)
        if tsquery:
            by_keyword = conn.execute(
                f"SELECT id FROM policy_chunk, to_tsquery('english', %s) q "
                f"WHERE {where} AND tsv @@ q ORDER BY ts_rank_cd(tsv, q) DESC LIMIT %s",
                [tsquery, *params, s.search_candidates],
            ).fetchall()

        fused = rrf([[r["id"] for r in by_vector], [r["id"] for r in by_keyword]])[: s.rerank_pool]
        if not fused:
            return []
        rows = conn.execute(f"SELECT {_CHUNK_COLUMNS} FROM policy_chunk WHERE id = ANY(%s)", [fused]).fetchall()

    by_id = {r["id"]: r for r in rows}
    candidates = [by_id[i] for i in fused if i in by_id]
    scores = rerank(query, [f"{c['title']} > {c['section_path']}\n{c['text']}" for c in candidates])
    ranked = sorted(zip(candidates, scores, strict=True), key=lambda pair: pair[1], reverse=True)
    return [dict(c, score=round(score, 3)) for c, score in ranked if score >= s.rerank_min_score][:top_k]


def get_section(number: str, section: str | None = None, limit: int = 6) -> list[dict]:
    """Chunks of the active version of an article, optionally limited to sections matching a phrase."""
    params: list = [number.upper()]
    clause = ""
    if section:
        clause = " AND section_path ILIKE %s"
        params.append(f"%{section}%")
    with connection() as conn:
        return conn.execute(
            f"SELECT {_CHUNK_COLUMNS} FROM policy_chunk WHERE active AND number = %s{clause} "
            f"ORDER BY chunk_index LIMIT %s",
            [*params, limit],
        ).fetchall()


def get_chunks(ids: list[str]) -> dict[str, dict]:
    with connection() as conn:
        rows = conn.execute(f"SELECT {_CHUNK_COLUMNS} FROM policy_chunk WHERE id = ANY(%s)", [ids]).fetchall()
    return {r["id"]: r for r in rows}
