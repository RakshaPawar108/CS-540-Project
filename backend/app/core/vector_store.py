"""
ChromaDB client — persisted to disk, shared by ingestion and RAG services.
"""
from functools import lru_cache
from langchain_chroma import Chroma
from app.config import get_settings
from app.core.embeddings import get_embedding_model


@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    settings = get_settings()
    return Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=get_embedding_model(),
        persist_directory=settings.chroma_persist_dir,
    )
