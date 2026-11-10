"""Self-hosted embedding and reranking models (ONNX, CPU)."""
from functools import lru_cache

import numpy as np
from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder

from app.config import get_settings


@lru_cache
def _embedder() -> TextEmbedding:
    return TextEmbedding(get_settings().embed_model)


@lru_cache
def _reranker() -> TextCrossEncoder:
    return TextCrossEncoder(get_settings().rerank_model)


def embed_documents(texts: list[str]) -> list[np.ndarray]:
    return list(_embedder().passage_embed(texts))


def embed_query(text: str) -> np.ndarray:
    return next(iter(_embedder().query_embed(text)))


def rerank(query: str, documents: list[str]) -> list[float]:
    return [float(s) for s in _reranker().rerank(query, documents)]
