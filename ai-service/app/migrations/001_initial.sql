-- The schema as first deployed. Idempotent, so it also adopts indexes created before migrations existed.
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
ALTER TABLE policy_article ADD COLUMN IF NOT EXISTS source_hash text;

CREATE TABLE IF NOT EXISTS policy_chunk (
    id             text        PRIMARY KEY,
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
    sentences      jsonb       NOT NULL,
    content_hash   text        NOT NULL,
    embedding      vector({embed_dim}) NOT NULL,
    tsv            tsvector GENERATED ALWAYS AS
                   (to_tsvector('english', title || ' ' || section_path || ' ' || text)) STORED,
    active         boolean     NOT NULL DEFAULT true
);

CREATE INDEX IF NOT EXISTS policy_chunk_embedding_idx ON policy_chunk USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS policy_chunk_tsv_idx ON policy_chunk USING gin (tsv);
CREATE INDEX IF NOT EXISTS policy_chunk_filter_idx ON policy_chunk (active, country, category);
CREATE INDEX IF NOT EXISTS policy_chunk_hash_idx ON policy_chunk (content_hash);
CREATE INDEX IF NOT EXISTS policy_chunk_article_idx ON policy_chunk (article_sys_id, version);
