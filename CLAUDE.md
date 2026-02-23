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
- **Local Model**: Ollama (Llama 3.1 8B)
- **Cloud Models**: OpenAI GPT-4o (primary), Groq Llama 3.1 70B (free tier), Anthropic Claude
- **Vector DB**: ChromaDB / Pinecone
- **Backend**: FastAPI
- **Frontend**: React or Streamlit
- **Language**: Python 3.11

## Datasets
- **MedMCQA**: 194k+ medical MCQs (training + evaluation)
- **PubMedQA**: Biomedical yes/no/maybe QA
- **PubMed Abstracts**: 100k-500k documents for RAG retrieval corpus

## Evaluation Metrics
- Medical accuracy (MedMCQA benchmark)
- Latency: p50, p95, p99
- Cost per query
- Hallucination rate

## Conventions
- **Python**: 3.11, conda env `medical-chatbot`
- **Source code**: `src/`
- **Tests**: `tests/` (pytest)
- **Scripts**: `scripts/` (manual/ad-hoc utilities)
- **Config**: `src/config.py` for model definitions and shared settings

## Current Status
- **Task 1**: Complete — ModelFactory implemented with support for OpenAI, Anthropic, Groq, and Ollama
