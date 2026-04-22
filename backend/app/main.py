import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ingestion, single_llm, single_rag, multi_turn_llm, multi_turn_rag
from app.core.vector_store import get_vector_store
from app.config import get_settings
from app.services import seeding


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if settings.pubmed_email:
        vs = get_vector_store()
        if vs._collection.count() == 0:
            def _seed():
                seeding.run_seed(
                    vector_store=vs,
                    email=settings.pubmed_email,
                    ncbi_api_key=settings.ncbi_api_key,
                )
            threading.Thread(target=_seed, daemon=True, name="pubmed-seeder").start()
        else:
            seeding._state.update({
                "status": "ready",
                "chunks_stored": vs._collection.count(),
                "message": "DB already populated — skipping seed.",
            })
    yield


app = FastAPI(
    title="Medical Chatbot Strategy Comparison API",
    description=(
        "CS 540 — Team Pentacle\n\n"
        "Compares four LLM strategies on medical Q&A:\n"
        "S1 Single LLM · S2 Single RAG · S3 Multi-Turn LLM · S4 Multi-Turn RAG"
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
