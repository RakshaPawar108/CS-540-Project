"""
Shared embedding model — sentence-transformers/all-MiniLM-L6-v2 (384-dim, runs locally).
Import of langchain_huggingface (which pulls in torch) is deferred until first call
so uvicorn can bind its port before the heavy model library loads.
"""
from functools import lru_cache
from app.config import get_settings


@lru_cache(maxsize=1)
def get_embedding_model():
    from langchain_huggingface import HuggingFaceEmbeddings  # lazy — keeps torch off the startup path
    settings = get_settings()
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
