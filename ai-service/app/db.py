"""PostgreSQL (with pgvector) connection pool and schema migrations for the policy search index.

The index is a rebuildable copy of the knowledge base; ServiceNow stays the source of truth.
The schema lives in numbered SQL files in app/migrations, applied in order at startup; see the
COMMENT statements there for what each table and column holds.
"""

import threading
from contextlib import contextmanager
from pathlib import Path

import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import get_settings

MIGRATIONS = Path(__file__).parent / "migrations"

_pool: ConnectionPool | None = None
_pool_lock = threading.Lock()


def migrate(conn: psycopg.Connection, embed_dim: int) -> list[str]:
    """Applies migrations not run yet, each in its own transaction. Returns their names."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migration "
        "(name text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())"
    )
    done = {r[0] for r in conn.execute("SELECT name FROM schema_migration").fetchall()}
    applied = []
    for path in sorted(MIGRATIONS.glob("*.sql")):
        if path.name in done:
            continue
        with conn.transaction():
            conn.execute(path.read_text().replace("{embed_dim}", str(embed_dim)))
            conn.execute("INSERT INTO schema_migration (name) VALUES (%s)", [path.name])
        applied.append(path.name)
    return applied


def _configure(conn: psycopg.Connection) -> None:
    register_vector(conn)
    # Keep scanning the HNSW graph until enough rows pass the country filter (pgvector 0.8+), so a
    # country with few policies still gets a full candidate list.
    conn.execute("SET hnsw.iterative_scan = strict_order")
    conn.commit()


def init_db() -> None:
    """Migrates the schema and opens the connection pool. Safe to call more than once."""
    global _pool
    with _pool_lock:
        if _pool is not None:
            return
        settings = get_settings()
        with psycopg.connect(settings.database_url, autocommit=True) as conn:
            migrate(conn, settings.embed_dim)
        _pool = ConnectionPool(
            settings.database_url, min_size=1, max_size=5, configure=_configure, open=True
        )


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


@contextmanager
def article_lock(sys_id: str):
    """Serializes indexing of one article across requests and processes (a Postgres advisory lock).

    Uses its own connection, so holding the lock never takes a slot the indexing itself needs.
    """
    with psycopg.connect(get_settings().database_url, autocommit=True) as conn:
        conn.execute("SELECT pg_advisory_lock(hashtext(%s))", [sys_id])
        try:
            yield
        finally:
            conn.execute("SELECT pg_advisory_unlock(hashtext(%s))", [sys_id])
