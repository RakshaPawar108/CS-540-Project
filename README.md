# CS-540-Project — Medical Chatbot Strategy Comparison

Team Pentacle · CS 540 · UIC

Compares four LLM strategies on medical Q&A (MedMCQA / PubMedQA):

| Strategy | RAG | Memory |
|----------|-----|--------|
| S1 — Single LLM | — | — |
| S2 — Single RAG | ✓ | — |
| S3 — Multi-Turn LLM | — | ✓ |
| S4 — Multi-Turn RAG | ✓ | ✓ |

---

## Project structure

```
backend/
├── app/
│   ├── main.py                        # FastAPI app entry point — registers all routers
│   ├── config.py                      # All settings (reads from .env)
│   ├── dependencies.py                # Shared FastAPI dependency re-exports
│   ├── models/
│   │   └── schemas.py                 # All request/response Pydantic models (shared)
│   ├── core/
│   │   ├── embeddings.py              # Embedding model singleton (all-MiniLM-L6-v2)
│   │   └── vector_store.py            # ChromaDB client singleton
│   ├── services/
│   │   ├── ingestion_service.py       # ← Person 1: implement ingest()
│   │   ├── llm_service.py             # ← Person 2: ask_single()
│   │   │                              #   Person 3: ask_with_context()
│   │   │                              #   Person 4: ask_multi_turn()
│   │   │                              #   Person 5: ask_multi_turn_with_context()
│   │   ├── rag_service.py             # ← Person 3: implement retrieve()
│   │   │                              #   Person 5: implement retrieve_with_history()
│   │   └── conversation_store.py      # Session history for S3/S4 — already implemented
│   └── routers/
│       ├── ingestion.py               # Routes wired — Person 1 only touches service
│       ├── single_llm.py              # Routes wired — Person 2 only touches service
│       ├── single_rag.py              # Routes wired — Person 3 only touches service
│       ├── multi_turn_llm.py          # Routes wired — Person 4 only touches service
│       └── multi_turn_rag.py          # Routes wired — Person 5 only touches service
├── tests/
│   ├── test_ingestion.py
│   ├── test_single_llm.py
│   ├── test_single_rag.py
│   ├── test_multi_turn_llm.py
│   └── test_multi_turn_rag.py
├── requirements.txt
├── .env.example                       # copy to .env and fill in keys
└── .gitignore
```

> **Rule of thumb:** each person only edits their service file(s). Routers, schemas, and core infrastructure are shared — coordinate before changing them.

---

## Backend setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in keys (see below)
uvicorn app.main:app --reload
```

Interactive docs: http://localhost:8000/docs

### Required `.env` values

| Key | Where to get it |
|-----|----------------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — free, no credit card |
| `PUBMED_EMAIL` | Your UIC email (required by NCBI Entrez) |
| `OPENAI_API_KEY` | Optional — only needed if switching back to OpenAI models |

The project uses **Groq** (free tier) with `llama-3.3-70b-versatile` by default.

### Seed ChromaDB (run once)

ChromaDB is file-persisted — you only need to do this once per machine. The data survives server restarts.

```bash
cd backend
python seed_db.py
```

This fetches ~250 PubMed abstracts across 5 medical topics and stores them locally in `chroma_db/`. Takes 3–5 minutes (PubMed rate limits). You'll see batch progress printed as it runs.

> If `chroma_db/` already exists (e.g. a teammate seeded it), skip this step.

---

## API quick-reference

### Health check
```
GET /health
```

### Ingestion (Person 1)
```
POST /api/v1/ingestion/ingest          # body: { "query": "...", "max_results": 100 }
GET  /api/v1/ingestion/status          # check collection size
```
Run ingestion once before using any RAG strategy.

### S1 — Single LLM (Person 2)
```
POST /api/v1/chat/single-llm/          # body: { "query": "..." }
```

### S2 — Single RAG (Person 3)
```
POST /api/v1/chat/single-rag/          # body: { "query": "...", "top_k": 5 }
```

### S3 — Multi-Turn LLM (Person 4)
```
POST   /api/v1/chat/multi-turn-llm/              # body: { "session_id": "<uuid>", "query": "..." }
DELETE /api/v1/chat/multi-turn-llm/{session_id}  # reset conversation
```

### S4 — Multi-Turn RAG (Person 5) ✓ implemented
```
POST   /api/v1/chat/multi-turn-rag/              # body: { "session_id": "<uuid>", "query": "...", "top_k": 5 }
DELETE /api/v1/chat/multi-turn-rag/{session_id}  # clear session history
```

**`session_id`** — generate once per user conversation (e.g., `uuid.uuid4()` in the frontend). Pass the same ID on every follow-up turn to maintain history.

**Example — first turn:**
```bash
curl -s -X POST http://localhost:8000/api/v1/chat/multi-turn-rag/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "my-session-1",
    "query": "What are the treatments for type 2 diabetes?",
    "top_k": 3
  }'
```

**Example — follow-up turn (same session_id):**
```bash
curl -s -X POST http://localhost:8000/api/v1/chat/multi-turn-rag/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "my-session-1",
    "query": "Can you elaborate on the diet programme mentioned?",
    "top_k": 3
  }'
```

The follow-up query is automatically condensed into a standalone question using conversation history before retrieval, so vague references like "the diet programme mentioned" resolve correctly.

---

## Implementation status

| Strategy | Service | Status |
|----------|---------|--------|
| S1 — Single LLM | `llm_service.ask_single` | pending (Person 2) |
| S2 — Single RAG | `rag_service.retrieve` + `llm_service.ask_with_context` | pending (Person 3) |
| S3 — Multi-Turn LLM | `llm_service.ask_multi_turn` | pending (Person 4) |
| S4 — Multi-Turn RAG | `rag_service.retrieve_with_history` + `llm_service.ask_multi_turn_with_context` | **done** |

Unimplemented endpoints return HTTP 501.

## Integration notes

- ChromaDB is file-persisted (`chroma_db/`). Seed it once with `python seed_db.py` before testing S2/S4.
- The conversation store is in-memory — sessions reset on server restart.
- Each response includes a `strategy` field (`"S1-single-llm"` etc.) for frontend labelling.
- S4 uses **query condensation**: follow-up questions are rewritten into standalone queries before retrieval, so history-dependent references resolve correctly in ChromaDB.

---

## Tests

```bash
cd backend
pytest                              # run all
pytest tests/test_single_llm.py    # run one file
```
