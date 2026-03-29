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
cp .env.example .env          # fill in OPENAI_API_KEY and PUBMED_EMAIL
uvicorn app.main:app --reload
```

Interactive docs: http://localhost:8000/docs

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

### S4 — Multi-Turn RAG (Person 5)
```
POST   /api/v1/chat/multi-turn-rag/              # body: { "session_id": "<uuid>", "query": "...", "top_k": 5 }
DELETE /api/v1/chat/multi-turn-rag/{session_id}
```

**`session_id`** — generate once per user conversation (e.g., `uuid.uuid4()` in the frontend). Pass the same ID on every follow-up turn to maintain history.

---

## Integration notes

- All chat endpoints return HTTP 501 until implemented. The frontend can use this to show a "coming soon" state.
- ChromaDB is file-persisted (`chroma_db/`). Run ingestion before testing S2/S4.
- The conversation store is in-memory — sessions reset on server restart.
- Each strategy response includes a `strategy` field (`"S1-single-llm"` etc.) so the frontend can label results for comparison.

---

## Tests

```bash
cd backend
pytest                              # run all
pytest tests/test_single_llm.py    # run one file
```
