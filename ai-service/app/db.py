"""PostgreSQL (with pgvector) connection pool and schema for the policy search index.

The index is a rebuildable copy of the knowledge base; ServiceNow stays the source of truth.

policy_article  one row per article version; only the current published version is active
policy_chunk    searchable pieces of an article, with their embedding, a keyword index and the
                sentences (with character offsets) that citations point at
"""
import threading
from contextlib import contextmanager

import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import get_settings

_pool: ConnectionPool | None = None
_pool_lock = threading.Lock()


def _schema(dim: int) -> str:
    return f"""
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS policy_article (
    sys_id          text        NOT NULL,
    number          text        NOT NULL,
    version         integer     NOT NULL,
    title           text        NOT NULL,
    category        text,
    country         text,
    normalized_text text        NOT NULL,
    source_hash     text,
    updated_at      timestamptz,
    active          boolean     NOT NULL DEFAULT true,
    PRIMARY KEY (sys_id, version)
);
-- For indexes created before source_hash existed.
ALTER TABLE policy_article ADD COLUMN IF NOT EXISTS source_hash text;

CREATE TABLE IF NOT EXISTS policy_chunk (
    id             text        PRIMARY KEY,          -- number#vVERSION#cINDEX
    article_sys_id text        NOT NULL,
    number         text        NOT NULL,
    version        integer     NOT NULL,
    title          text        NOT NULL,
    section_path   text        NOT NULL,
    category       text,
    country        text,
    chunk_index    integer     NOT NULL,
    text           text        NOT NULL,
    start_char     integer     NOT NULL,
    end_char       integer     NOT NULL,
    sentences      jsonb       NOT NULL,             -- [{{text, start, end}}], the citable units
    content_hash   text        NOT NULL,             -- reuse embeddings when text is unchanged
    embedding      vector({dim}) NOT NULL,
    tsv            tsvector GENERATED ALWAYS AS
                   (to_tsvector('english', title || ' ' || section_path || ' ' || text)) STORED,
    active         boolean     NOT NULL DEFAULT true
);

CREATE INDEX IF NOT EXISTS policy_chunk_embedding_idx ON policy_chunk USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS policy_chunk_tsv_idx ON policy_chunk USING gin (tsv);
CREATE INDEX IF NOT EXISTS policy_chunk_filter_idx ON policy_chunk (active, country, category);
CREATE INDEX IF NOT EXISTS policy_chunk_hash_idx ON policy_chunk (content_hash);
CREATE INDEX IF NOT EXISTS policy_chunk_article_idx ON policy_chunk (article_sys_id, version);
"""


def init_db() -> None:
    """Creates the schema (idempotent) and opens the connection pool."""
    global _pool
    with _pool_lock:
        if _pool is not None:
            return
        settings = get_settings()
        # The extension must exist before the pool registers the vector type on each connection.
        with psycopg.connect(settings.database_url, autocommit=True) as conn:
            conn.execute(_schema(settings.embed_dim))
        _pool = ConnectionPool(settings.database_url, min_size=1, max_size=5, configure=register_vector, open=True)


def close_db() -> None:
    global _pool
    with _pool_lock:
        if _pool is not None:
            _pool.close()
            _pool = None


@contextmanager
def connection():
    """A pooled connection that returns rows as dicts. Commits on success, rolls back on error."""
    if _pool is None:
        init_db()
    with _pool.connection() as conn:
        conn.row_factory = dict_row
        yield conn
