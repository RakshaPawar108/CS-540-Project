from pydantic import BaseModel, Field
from typing import List, Optional


# ---------------------------------------------------------------------------
# ChatMessage
# ---------------------------------------------------------------------------
# Represents a single message in a conversation.
# OpenAI's API expects messages in exactly this shape:
#   { "role": "user" | "assistant" | "system", "content": "..." }
#
# By defining this as a Pydantic model, Python will automatically validate
# that 'role' is always a string and 'content' is always a string.
# If either is missing or the wrong type, FastAPI raises a 400 error for us.
class ChatMessage(BaseModel):
    role: str       # who sent this message: "user", "assistant", or "system"
    content: str    # the actual text of the message


# ---------------------------------------------------------------------------
# ChatRequest
# ---------------------------------------------------------------------------
# This is the body of the POST /chat request that the frontend (or a teammate's
# integration code) will send to our endpoint.
#
# Fields:
#   session_id  - a unique string that identifies one conversation session.
#                 We use this as a key to look up stored chat history.
#                 Optional: if not provided, we treat it as a brand-new session.
#
#   message     - the user's latest message (e.g., "What are symptoms of flu?")
#
#   strategy    - which chatbot strategy to use. Defaults to "multi_turn_llm".
#                 At integration time, teammates will add their own strategy
#                 names here (e.g., "rag_single_turn", "rag_multi_turn").
class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this conversation session. "
                    "Pass the same ID on follow-up turns to maintain history."
    )
    message: str = Field(
        ...,                          # the '...' means this field is REQUIRED
        description="The user's message to the chatbot."
    )
    strategy: str = Field(
        default="multi_turn_llm",
        description="The chatbot strategy to use for this request."
    )


# ---------------------------------------------------------------------------
# ChatResponse
# ---------------------------------------------------------------------------
# This is what our /chat endpoint sends BACK to the caller.
#
# Fields:
#   session_id  - echoed back so the client knows which session this belongs to
#                 (especially useful when the server auto-generated it)
#
#   reply       - the assistant's response text
#
#   history     - the full conversation so far, as a list of ChatMessage objects.
#                 Returning this lets the client display or debug the full thread.
#
#   strategy    - echoes back which strategy was used, useful for the comparison UI
class ChatResponse(BaseModel):
    session_id: str = Field(
        description="The session ID for this conversation (auto-generated if not provided)."
    )
    reply: str = Field(
        description="The assistant's response to the user's message."
    )
    history: List[ChatMessage] = Field(
        description="The full conversation history for this session, including this turn."
    )
    strategy: str = Field(
        description="The strategy that produced this response."
    )
