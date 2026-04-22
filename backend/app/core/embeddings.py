"""
Shared embedding model — all-MiniLM-L6-v2 via fastembed (ONNX, no torch).
fastembed releases the GIL during inference so the async event loop stays responsive.
"""
from functools import lru_cache
from app.config import get_settings


class _FastEmbedWrapper:
    """Minimal LangChain-compatible wrapper around fastembed.TextEmbedding."""

    def __init__(self, model_name: str):
        from fastembed import TextEmbedding   # lazy — deferred until first call
        self._model = TextEmbedding(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [emb.tolist() for emb in self._model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        return next(self._model.embed([text])).tolist()


@lru_cache(maxsize=1)
def get_embedding_model() -> _FastEmbedWrapper:
    settings = get_settings()
    return _FastEmbedWrapper(model_name=settings.embedding_model)
