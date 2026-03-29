"""
Shared embedding model — sentence-transformers/all-MiniLM-L6-v2 (384-dim, runs locally).
Loaded once at startup and injected via FastAPI dependency.
"""
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import get_settings


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    settings = get_settings()
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
