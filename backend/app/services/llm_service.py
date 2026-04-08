"""
LLM service — stubs for integration.

Owners:
  Person 2  →  ask_single
  Person 3  →  ask_with_context
  Person 4  →  ask_multi_turn
  Person 5  →  ask_multi_turn_with_context

All functions return a plain dict so routers can map to their response schemas.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.config import get_settings
from app.models.schemas import Message

load_dotenv()  # ensures .env values are in os.environ for os.getenv() calls


_SYSTEM_PROMPT = (
    "You are a medical AI assistant specializing in answering questions based on "
    "scientific literature. Provide accurate, evidence-based answers. "
    "Maintain context across the conversation to give coherent follow-up responses. "
    "If you are uncertain about something, say so clearly. "
    "Never fabricate medical facts, drug names, or study results."
)


def _get_client() -> tuple[OpenAI, str]:
    """
    Return an (OpenAI client, model name) pair.

    Priority:
      1. Groq  — if GROQ_API_KEY is set in the environment
      2. OpenAI — fallback using settings.openai_api_key / settings.openai_model

    Groq's API is OpenAI-compatible, so the same openai package works for both.
    To switch providers, set/unset GROQ_API_KEY in your .env — no code changes needed.
    """
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    else:
        settings = get_settings()
        client = OpenAI(api_key=settings.openai_api_key)
        model = settings.openai_model
    return client, model


def ask_single(query: str) -> dict:
    """S1: bare LLM call, no history, no context."""
    raise NotImplementedError


def ask_with_context(query: str, context: str) -> dict:
    """S2: LLM call augmented with retrieved PubMed context string."""
    raise NotImplementedError


def ask_multi_turn(query: str, history: list[Message]) -> dict:
    """
    S3: LLM call with full conversation history, no retrieval.

    Builds the message list as:
        [system prompt] + [previous turns from history] + [current user query]

    Returns a dict with at least {"answer": str}.
    """
    client, model = _get_client()
    settings = get_settings()

    messages: list[dict] = [{"role": "system", "content": _SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=model,
        temperature=settings.temperature,
        messages=messages,
    )

    return {"answer": response.choices[0].message.content}


def ask_multi_turn_with_context(query: str, history: list[Message], context: str) -> dict:
    """S4: LLM call with conversation history + retrieved context."""
    raise NotImplementedError
