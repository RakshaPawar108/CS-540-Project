"""
Ingestion service — stub for integration.
Owner: Person 1 (Ingestion Pipeline)

Expected interface used by the ingestion router:
    ingest(query, max_results, vector_store, email) -> int   # returns chunks stored
    get_collection_count(vector_store) -> int
"""
from langchain_chroma import Chroma


def ingest(query: str, max_results: int, vector_store: Chroma, email: str) -> int:
    """Fetch PubMed abstracts, chunk, embed, and store in ChromaDB. Returns chunk count."""
    raise NotImplementedError


def get_collection_count(vector_store: Chroma) -> int:
    """Return total number of documents stored in the collection."""
    return vector_store._collection.count()
