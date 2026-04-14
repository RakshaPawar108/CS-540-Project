"""
Pipeline wrappers for LangSmith tracing.

Each function wraps one full strategy pipeline under a single @traceable root,
so all sub-calls (retrieval, condense-query, LLM) appear as nested child runs.
"""
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langsmith import traceable

from app.models.schemas import Message
from app.services import rag_service
from app.services.llm_service import _get_llm


@traceable(name="S2-pipeline", run_type="chain", tags=["strategy:S2", "rag"])
def run_s2(query: str, vector_store: Chroma, top_k: int) -> dict:
    """S2: retrieve → generate. Both steps nested under this trace."""
    chunks = rag_service.retrieve(query, vector_store, top_k)
    context = rag_service.format_context(chunks)

    llm = _get_llm()
    system = SystemMessage(content=(
        "You are a helpful medical assistant. "
        "Answer the user's question using only the PubMed context provided. "
        "If the context does not contain enough information, say so. "
        "Be concise and cite the source PMIDs when relevant.\n\n"
        f"Context from PubMed:\n{context}"
    ))
    response = llm.invoke([system, HumanMessage(content=query)])
    usage = response.response_metadata.get("token_usage", {})

    return {
        "answer": response.content,
        "model": llm.model_name,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "chunks": chunks,
    }


@traceable(name="S4-pipeline", run_type="chain", tags=["strategy:S4", "multi-turn", "rag"])
def run_s4(query: str, history: list[Message], vector_store: Chroma, top_k: int) -> dict:
    """S4: condense → retrieve → generate. All steps nested under this trace."""
    # Step 1: condense query using history
    standalone_query = rag_service._condense_query(query, history)

    # Step 2: retrieve chunks
    chunks = rag_service.retrieve(standalone_query, vector_store, top_k)
    context = rag_service.format_context(chunks)

    # Step 3: generate answer
    llm = _get_llm()
    system = SystemMessage(content=(
        "You are a helpful medical assistant. "
        "Answer the user's question using only the PubMed context provided. "
        "If the context does not contain enough information, say so. "
        "Be concise and cite the source PMIDs when relevant.\n\n"
        f"Context from PubMed:\n{context}"
    ))
    messages = [system]
    for m in history:
        if m.role == "user":
            messages.append(HumanMessage(content=m.content))
        else:
            messages.append(AIMessage(content=m.content))
    messages.append(HumanMessage(content=query))

    response = llm.invoke(messages)
    usage = response.response_metadata.get("token_usage", {})

    return {
        "answer": response.content,
        "model": llm.model_name,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "chunks": chunks,
    }
