"""
LLM service — stubs for integration.

Owners:
  Person 2  →  ask_single
  Person 3  →  ask_with_context
  Person 4  →  ask_multi_turn
  Person 5  →  ask_multi_turn_with_context

All functions return a plain dict so routers can map to their response schemas.
"""
from app.models.schemas import Message


def ask_single(query: str) -> dict:
    """S1: bare LLM call, no history, no context."""
    raise NotImplementedError


def ask_with_context(query: str, context: str) -> dict:
    """S2: LLM call augmented with retrieved PubMed context string."""
    raise NotImplementedError


def ask_multi_turn(query: str, history: list[Message]) -> dict:
    """S3: LLM call with full conversation history, no retrieval."""
    raise NotImplementedError


def ask_multi_turn_with_context(query: str, history: list[Message], context: str) -> dict:
    """S4: LLM call with conversation history + retrieved context."""
    raise NotImplementedError
