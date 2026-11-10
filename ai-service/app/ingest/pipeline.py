"""Keeps the search index in sync with the knowledge base."""
import hashlib
import logging

from psycopg.types.json import Jsonb

from app.config import get_settings
from app.db import connection
from app.ingest.chunk import chunk_article
from app.ingest.parse import parse_html
from app.search.models import embed_documents
from app.sources import Article, get_source

log = logging.getLogger(__name__)


def _deactivate(conn, sys_id: str) -> None:
    conn.execute("UPDATE policy_article SET active = false WHERE sys_id = %s", [sys_id])
    conn.execute("UPDATE policy_chunk SET active = false WHERE article_sys_id = %s", [sys_id])


def _source_hash(article: Article) -> str:
    # Versions alone can miss changes (a renumbered or re-imported article), so compare content too.
    parts = [article.number, article.title, article.category or "", article.country or "", article.html]
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()


def _is_current(conn, article: Article) -> bool:
    row = conn.execute(
        "SELECT 1 FROM policy_article WHERE sys_id = %s AND version = %s AND source_hash = %s AND active",
        [article.sys_id, article.version, _source_hash(article)],
    ).fetchone()
    return row is not None


def index_article(article: Article) -> str:
    """Indexes one article version. Returns what happened, for logs and the API response."""
    s = get_settings()
    with connection() as conn:
        if not article.published:
            _deactivate(conn, article.sys_id)
            return "retired"
        if _is_current(conn, article):
            return "unchanged"

    parsed = parse_html(article.title, article.html)
    chunks = chunk_article(parsed, s.chunk_target_words, s.chunk_overlap_words)
    hashes = [c.content_hash(article.title) for c in chunks]

    with connection() as conn:
        # Reuse embeddings for chunks whose text didn't change between versions.
        known = {
            r["content_hash"]: r["embedding"]
            for r in conn.execute(
                "SELECT DISTINCT ON (content_hash) content_hash, embedding FROM policy_chunk WHERE content_hash = ANY(%s)",
                [hashes],
            ).fetchall()
        }
    missing = [i for i, h in enumerate(hashes) if h not in known]
    fresh = embed_documents([chunks[i].embed_text(article.title) for i in missing]) if missing else []
    vectors = dict(known)
    for i, vec in zip(missing, fresh, strict=True):
        vectors[hashes[i]] = vec

    with connection() as conn, conn.transaction():
        _deactivate(conn, article.sys_id)
        # Chunk IDs are number#version#index, so clear rows for this number and version from any source.
        conn.execute("DELETE FROM policy_chunk WHERE (article_sys_id = %s OR number = %s) AND version = %s",
                     [article.sys_id, article.number, article.version])
        conn.execute(
            """INSERT INTO policy_article (sys_id, number, version, title, category, country, normalized_text, updated_at, active, source_hash)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, true, %s)
               ON CONFLICT (sys_id, version) DO UPDATE SET active = true, number = EXCLUDED.number, title = EXCLUDED.title,
               category = EXCLUDED.category, country = EXCLUDED.country,
               normalized_text = EXCLUDED.normalized_text, source_hash = EXCLUDED.source_hash""",
            [article.sys_id, article.number, article.version, article.title, article.category,
             article.country or "GLOBAL", parsed.text, article.updated_at, _source_hash(article)],
        )
        for chunk, h in zip(chunks, hashes, strict=True):
            conn.execute(
                """INSERT INTO policy_chunk (id, article_sys_id, number, version, title, section_path, category, country,
                   chunk_index, text, start_char, end_char, sentences, content_hash, embedding, active)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true)""",
                [f"{article.number}#v{article.version}#c{chunk.index}", article.sys_id, article.number,
                 article.version, article.title, chunk.section_path, article.category, article.country or "GLOBAL",
                 chunk.index, chunk.text, chunk.start, chunk.end,
                 Jsonb([{"text": u.text, "start": u.start, "end": u.end} for u in chunk.units]), h, vectors[h]],
            )
    log.info("indexed %s v%s: %d chunks (%d embedded)", article.number, article.version, len(chunks), len(missing))
    return f"indexed {len(chunks)} chunks"


def ingest(sys_id: str) -> str:
    article = get_source().get_article(sys_id)
    if article is None:
        with connection() as conn:
            _deactivate(conn, sys_id)
        return "not found; deactivated"
    return index_article(article)


def reconcile() -> dict:
    """Brings the index in line with every article in the knowledge base."""
    articles = get_source().list_articles()
    seen = {a.sys_id for a in articles}
    results: dict[str, int] = {}
    for article in articles:
        outcome = index_article(article).split(" ")[0]
        results[outcome] = results.get(outcome, 0) + 1
    with connection() as conn:
        stale = conn.execute("SELECT DISTINCT sys_id FROM policy_article WHERE active").fetchall()
        for row in stale:
            if row["sys_id"] not in seen:
                _deactivate(conn, row["sys_id"])
                results["removed"] = results.get("removed", 0) + 1
    return results
