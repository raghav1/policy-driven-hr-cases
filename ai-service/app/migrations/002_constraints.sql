-- Only the current version of an article keeps chunks; older versions are deleted on re-index, so the
-- vector index holds nothing a filter has to skip. Chunks now belong to their article row.

DELETE FROM policy_chunk WHERE NOT active;
DELETE FROM policy_chunk c
 WHERE NOT EXISTS (SELECT 1 FROM policy_article a WHERE a.sys_id = c.article_sys_id AND a.version = c.version);

ALTER TABLE policy_article DROP COLUMN IF EXISTS normalized_text;
ALTER TABLE policy_article DROP COLUMN IF EXISTS updated_at;

-- If an older bug left two active versions, keep the newest.
UPDATE policy_article a SET active = false
 WHERE active AND EXISTS (SELECT 1 FROM policy_article b WHERE b.sys_id = a.sys_id AND b.active AND b.version > a.version);
CREATE UNIQUE INDEX IF NOT EXISTS policy_article_one_active_idx ON policy_article (sys_id) WHERE active;

ALTER TABLE policy_chunk
    ADD CONSTRAINT policy_chunk_article_fk FOREIGN KEY (article_sys_id, version)
    REFERENCES policy_article (sys_id, version) ON DELETE CASCADE;

ALTER TABLE policy_article ALTER COLUMN country SET NOT NULL;
ALTER TABLE policy_chunk ALTER COLUMN country SET NOT NULL;

COMMENT ON TABLE policy_article IS 'One row per indexed knowledge article version. A rebuildable copy of the ServiceNow knowledge base.';
COMMENT ON COLUMN policy_article.sys_id IS 'kb_knowledge sys_id in ServiceNow';
COMMENT ON COLUMN policy_article.number IS 'Article number, for example KB0090002';
COMMENT ON COLUMN policy_article.version IS 'ServiceNow sys_mod_count when indexed';
COMMENT ON COLUMN policy_article.category IS 'Policy area from the article meta field (area:...)';
COMMENT ON COLUMN policy_article.country IS 'ISO country code from the meta field, or GLOBAL';
COMMENT ON COLUMN policy_article.source_hash IS 'Hash of number, title, meta and body; detects changes the version misses';
COMMENT ON COLUMN policy_article.active IS 'True for the version currently published; at most one per sys_id';

COMMENT ON TABLE policy_chunk IS 'Searchable pieces of the active article versions, with embeddings and the sentences citations point at.';
COMMENT ON COLUMN policy_chunk.id IS 'number#vVERSION#cINDEX; the source id the model cites';
COMMENT ON COLUMN policy_chunk.section_path IS 'Heading path, for example Entitlement > Standard entitlement';
COMMENT ON COLUMN policy_chunk.country IS 'Copied from the article; every search filters on it';
COMMENT ON COLUMN policy_chunk.chunk_index IS 'Position of the chunk in the article';
COMMENT ON COLUMN policy_chunk.text IS 'Chunk text as searched and reranked';
COMMENT ON COLUMN policy_chunk.start_char IS 'Start offset of the chunk in the parsed article text';
COMMENT ON COLUMN policy_chunk.end_char IS 'End offset of the chunk in the parsed article text';
COMMENT ON COLUMN policy_chunk.sentences IS '[{text, start, end}]: the citable units, in order';
COMMENT ON COLUMN policy_chunk.content_hash IS 'Hash of the embedded text; unchanged chunks reuse their embedding';
COMMENT ON COLUMN policy_chunk.embedding IS 'Passage embedding (cosine distance, HNSW index)';
COMMENT ON COLUMN policy_chunk.tsv IS 'Full-text index of title, section and text';
COMMENT ON COLUMN policy_chunk.active IS 'True while the article version is current';
