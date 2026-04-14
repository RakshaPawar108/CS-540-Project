from dotenv import load_dotenv
load_dotenv()  # must run before LangChain imports so LANGCHAIN_TRACING_V2 is set

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ingestion, single_llm, single_rag, multi_turn_llm, multi_turn_rag

app = FastAPI(
    title="Medical Chatbot Strategy Comparison API",
    description=(
        "CS 540 — Team Pentacle\n\n"
        "Compares four LLM strategies on medical Q&A:\n"
        "S1 Single LLM · S2 Single RAG · S3 Multi-Turn LLM · S4 Multi-Turn RAG"
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten for production
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

app.include_router(ingestion.router,       prefix=API_PREFIX)
app.include_router(single_llm.router,      prefix=API_PREFIX)
app.include_router(single_rag.router,      prefix=API_PREFIX)
app.include_router(multi_turn_llm.router,  prefix=API_PREFIX)
app.include_router(multi_turn_rag.router,  prefix=API_PREFIX)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
