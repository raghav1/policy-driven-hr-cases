"""Service configuration, read from environment variables (and .env in development).

Every setting can be overridden by an environment variable of the same name in upper case,
for example LLM_MODEL=claude-sonnet-5-5.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- API -----------------------------------------------------------------------------
    # Shared secret ServiceNow sends in the X-API-Key header. Requests are refused while it is
    # empty.
    service_api_key: str = ""
    log_level: str = "INFO"
    # Agent runs (triage and chat) in progress at once; each holds model calls open. Requests over
    # the
    # limit wait up to queue_timeout_seconds, then get a "busy" error and ServiceNow routes to
    # manual.
    max_concurrent_runs: int = 4
    queue_timeout_seconds: float = 30.0

    # --- LLM -----------------------------------------------------------------------------
    # "offline" swaps the model for a deterministic stand-in, for running without a provider key.
    llm_provider: Literal["anthropic", "offline"] = "anthropic"
    llm_model: str = "claude-sonnet-5-5"
    llm_max_tokens: int = 8000
    max_tool_calls: int = 5  # tool calls the agent may make per request

    # --- Policy source ---------------------------------------------------------------------
    # "servicenow" reads the HR knowledge base; "local" reads ./corpus (development and tests).
    kb_source: Literal["servicenow", "local"] = "local"
    corpus_dir: str = "/srv/corpus"

    # Read-only integration user for the ServiceNow Table API.
    sn_instance_url: str = ""
    sn_user: str = ""
    sn_password: str = ""
    sn_hr_kb_sys_id: str = ""
    sn_case_table: str = "x_2312287_hrorch_hr_case"

    # --- Search index ----------------------------------------------------------------------
    database_url: str = "postgresql://hr:hr@localhost:5432/hr_policies"
    embed_model: str = "BAAI/bge-small-en-v1.5"
    embed_dim: int = 384  # must match embed_model
    rerank_model: str = "Xenova/ms-marco-MiniLM-L-6-v2"

    chunk_target_words: int = 320
    chunk_overlap_words: int = 50
    search_candidates: int = 30  # per retriever (vector and keyword) before fusion
    rerank_pool: int = 20  # fused candidates sent to the reranker
    search_top_k: int = 5
    # Cross-encoder score below which a chunk counts as not relevant. Paraphrased questions score
    # around -8 and unrelated ones around -11 on the default reranker.
    rerank_min_score: float = -10.0

    # Full knowledge-base sync, as a safety net for missed publish events.
    reconcile_interval_hours: float = 24.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
