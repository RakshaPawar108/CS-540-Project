"""
OWNER: Person 3 (Single RAG) & Person 5 (Multi-Turn RAG)

Retrieves relevant PubMed chunks from ChromaDB.

TODO (Person 3):
  - Implement `retrieve` — similarity search, return ranked chunks

TODO (Person 5):
  - Implement `retrieve_with_history` — optionally rewrite query using conversation
    history before retrieval (HyDE or query condensation)
"""
from langchain_chroma import Chroma
from app.models.schemas import RetrievedChunk, Message


def retrieve(query: str, vector_store: Chroma, top_k: int = 5) -> list[RetrievedChunk]:
    """
    Similarity search against the ChromaDB collection.

    Returns up to `top_k` chunks sorted by relevance score (descending).

    TODO:
      - Call vector_store.similarity_search_with_relevance_scores(query, k=top_k)
      - Map results to RetrievedChunk (content, source from metadata["pmid"], score)
    """
    raise NotImplementedError("TODO: implement RAG retrieval")


def format_context(chunks: list[RetrievedChunk]) -> str:
    """
    Format retrieved chunks into a single context string to pass to the LLM.
    """
    parts = [f"[Source: {c.source}]\n{c.content}" for c in chunks]
    return "\n\n---\n\n".join(parts)


def retrieve_with_history(
    query: str,
    history: list[Message],
    vector_store: Chroma,
    top_k: int = 5,
) -> list[RetrievedChunk]:
    """
    S4 variant — optionally condense multi-turn history into a standalone query
    before retrieval. Falls back to plain retrieval if not implemented.

    TODO (Person 5):
      - Use an LLM call to rewrite `query` given `history` into a self-contained
        question, then call `retrieve(rewritten_query, ...)`.
    """
    # Fallback: ignore history, retrieve on raw query
    return retrieve(query, vector_store, top_k)
