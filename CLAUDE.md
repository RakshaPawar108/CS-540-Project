# Medical Chatbot Strategy Comparison

## Project Overview
CS540 Advanced Software Engineering project comparing three medical chatbot strategies:
1. **Non-RAG** — direct LLM calls without retrieval
2. **Single-Turn RAG** — retrieval-augmented generation (one question at a time)
3. **Multi-Turn RAG** — RAG with conversation history

5-person team, 10-week timeline.

## Task Breakdown
1. Model selection & simple LLM call (ModelFactory + Ollama setup)
2. Vector DB & ingestion pipeline (ChromaDB/Pinecone + document processing)
3. Single-turn RAG chain
4. Multi-turn simple LLM (conversation memory, no retrieval)
5. Multi-turn RAG (conversation memory + retrieval)
6. Chatbot UI & performance evaluation

## Tech Stack
- **LLM Framework**: LangChain + LangGraph
- **Active Model**: Groq Llama 3.3 70B (`llama-3.3-70b-versatile`) — free tier, priority
- **Local Model**: Ollama Llama 3.1 8B — benchmark/evaluation only
- **Cloud Models**: OpenAI GPT-4o (optional fallback), Anthropic Claude
- **Vector DB**: ChromaDB (persisted to `backend/chroma_db/`)
- **Backend**: FastAPI (entry point: `backend/app/main.py`)
- **Frontend**: React or Streamlit
- **Language**: Python 3.11, conda env `medical-chatbot`

## Datasets
- **MedMCQA**: 194k+ medical MCQs (training + evaluation)
- **PubMedQA**: Biomedical yes/no/maybe QA
- **PubMed Abstracts**: 100k-500k documents for RAG retrieval corpus

## Evaluation Metrics
- Medical accuracy (MedMCQA benchmark)
- Latency: p50, p95, p99
- Cost per query
- Hallucination rate

## Project Structure
```
medical-chatbot/
├── src/                         # Benchmark tooling (ModelFactory, multi-provider)
│   └── models/model_factory.py  # Registry for OpenAI, Anthropic, Groq, Ollama
├── scripts/                     # Standalone evaluation scripts
│   └── demo_non_rag.py          # Non-RAG benchmark against PubMedQA
├── tests/                       # Unit tests for src/
├── backend/                     # FastAPI server (team integration target)
│   ├── app/
│   │   ├── main.py              # Server entry point — registers all routers
│   │   ├── config.py            # Pydantic Settings (reads backend/.env)
│   │   ├── models/schemas.py    # Shared request/response schemas (do not modify)
│   │   ├── routers/             # Routes pre-wired — each person edits their service only
│   │   └── services/
│   │       ├── llm_service.py   # MEDICAL_SYSTEM_PROMPT + ask_single() implemented (S1)
│   │       │                    # ask_with_context(), ask_multi_turn(),
│   │       │                    # ask_multi_turn_with_context() → stubs for teammates
│   │       ├── rag_service.py   # Stubs for Person 3 & 5
│   │       ├── ingestion_service.py # Stub for Person 1
│   │       └── conversation_store.py # In-memory session store — fully implemented
│   ├── requirements.txt         # Backend deps (no torch — RAG heavy deps commented out)
│   └── .env.example             # Copy to .env, fill in GROQ_API_KEY
└── requirements.txt             # Root deps for benchmark scripts
```

## Conventions
- **Integration rule**: Keep all routing in FastAPI. Each person only edits their service stub.
- **Shared system prompt**: `MEDICAL_SYSTEM_PROMPT` in `backend/app/services/llm_service.py` — all strategies must use this.
- **API keys**: All read from `backend/.env` via `get_settings()` — never hardcode.
- **Config**: `backend/app/config.py` for FastAPI settings; `src/config.py` for benchmark ModelFactory.
- **No torch**: Do not install `sentence-transformers` — pulls in PyTorch (~900MB). RAG embeddings are lazy.

## Running the Server
```bash
cd backend
conda activate medical-chatbot
uvicorn app.main:app --reload
# Swagger UI: http://localhost:8000/docs
# S1 test: POST http://localhost:8000/api/v1/chat/single-llm/  {"query": "..."}
```

## Current Status
- **Task 1 (S1)**: Complete — ModelFactory + Non-RAG benchmark (`scripts/demo_non_rag.py`)
- **FastAPI integration**: Complete — `backend/` added to `llm-call` branch; S1 (`ask_single`) implemented and tested via Groq; `MEDICAL_SYSTEM_PROMPT` defined for team reuse
- **Task 2 (S2)**: Vector DB & ingestion pipeline — teammate's branch (`vector-pipeline`)
- **Task 3 (S3/S4)**: Multi-turn variants — teammate branches (`multi-turn-llm-chatbot`, `multi_turn_rag`)
- **Next**: Integration merge — combine all branches into a single working server
