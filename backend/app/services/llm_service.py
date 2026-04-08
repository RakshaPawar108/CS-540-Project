"""
LLM service — stubs for integration.

Owners:
  Person 2  →  ask_single
  Person 3  →  ask_with_context
  Person 4  →  ask_multi_turn
  Person 5  →  ask_multi_turn_with_context

All functions return a plain dict so routers can map to their response schemas.
"""
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.config import get_settings
from app.models.schemas import Message

# Shared system prompt used across all four strategies (S1–S4).
# S2/S3/S4 stubs should prepend this before their additional context or history.
MEDICAL_SYSTEM_PROMPT = (
    "You are a knowledgeable medical assistant. "
    "Answer questions accurately and concisely using established medical knowledge. "
    "If you are unsure or the question is outside your knowledge, say so clearly."
)


def ask_single(query: str) -> dict:
    """S1: bare LLM call, no history, no context."""
    settings = get_settings()
    llm = ChatGroq(
        model=settings.groq_model,
        temperature=settings.temperature,
        api_key=settings.groq_api_key,
    )
    messages = [
        SystemMessage(content=MEDICAL_SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]
    response = llm.invoke(messages)
    usage = response.response_metadata.get("token_usage", {})
    return {
        "answer": response.content,
        "model": settings.groq_model,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
    }


def ask_with_context(query: str, context: str) -> dict:
    """S2: LLM call augmented with retrieved PubMed context string."""
    raise NotImplementedError


def ask_multi_turn(query: str, history: list[Message]) -> dict:
    """S3: LLM call with full conversation history, no retrieval."""
    raise NotImplementedError


def ask_multi_turn_with_context(query: str, history: list[Message], context: str) -> dict:
    """S4: LLM call with conversation history + retrieved context."""
    raise NotImplementedError
