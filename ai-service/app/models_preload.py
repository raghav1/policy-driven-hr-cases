"""Downloads the embedding and reranking models at image build time, so startup needs no network."""

from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder

from app.config import get_settings

settings = get_settings()
TextEmbedding(settings.embed_model)
TextCrossEncoder(settings.rerank_model)
print(f"cached {settings.embed_model} and {settings.rerank_model}")
