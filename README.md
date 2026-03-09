# Medical Chatbot — Strategy Comparison

CS540 Advanced Software Engineering project comparing three medical chatbot strategies to measure the impact of Retrieval-Augmented Generation (RAG) on medical question answering.

## Project Overview

Three strategies are implemented and evaluated:

1. **Non-RAG** — direct LLM calls with no retrieval (baseline)
2. **Single-Turn RAG** — retrieval-augmented generation, one question at a time
3. **Multi-Turn RAG** — RAG with full conversation history

Datasets: PubMedQA (yes/no/maybe), MedMCQA (MCQ). Evaluation: accuracy, latency (p50/p95/p99), cost per query, hallucination rate.

---

## Repository Structure

```
medical-chatbot/
├── src/
│   ├── config.py            # Shared model definitions and settings
│   └── models/
│       └── model_factory.py # ModelFactory — creates LangChain chat models
├── scripts/
│   ├── download_pubmedqa.py # Downloads PubMedQA labeled split to data/
│   ├── demo_non_rag.py      # Non-RAG baseline demo (Task 1 deliverable)
│   └── test_local_model.py  # Quick smoke test for local Ollama connection
├── tests/
│   └── test_model_factory.py
├── data/                    # Gitignored — populated by download scripts
├── requirements.txt
└── .env.example
```

---

## Setup

```bash
# 1. Create and activate conda environment
conda create -n medical-chatbot python=3.11 -y
conda activate medical-chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull the local model (one-time, ~5 GB)
ollama pull llama3.1

# 4. Copy env template and fill in API keys (optional for Task 1)
cp .env.example .env
```

> **Note:** For the non-RAG demo, only Ollama is needed. Cloud API keys (OpenAI, Anthropic, Groq) are not required until later tasks.

---

## Downloading the Dataset

```bash
python scripts/download_pubmedqa.py
```

Saves ~1000 labeled PubMedQA records to `data/raw/pubmedqa/pqa_labeled.jsonl`.

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Running the Demo

### Non-RAG Baseline (Task 1)

```bash
# In one terminal — keep running while you run the demo
ollama serve

# In another terminal
python scripts/demo_non_rag.py
```

Runs 5 PubMedQA questions through the local Llama 3.1 8B model with no context, prints expected vs. actual answers and latency, then shows a summary score. Results are auto-saved to `results/non_rag_YYYYMMDD_HHMMSS.json` on every run.

#### Sample Output

A pre-run sample output is committed at [`results/non_rag_sample_run.json`](results/non_rag_sample_run.json)
for teammates who don't have Ollama set up yet. Each run of the demo also auto-saves a timestamped
JSON to `results/` locally.

### Ollama Smoke Test

```bash
python scripts/test_local_model.py
```

---

## Supported Models

| Key | Provider | Model ID | Cost (input/output per 1k tokens) |
|-----|----------|----------|-----------------------------------|
| `llama3.1-local` | Ollama | `llama3.1` | Free (local) |
| `llama3.1-groq` | Groq | `llama-3.3-70b-versatile` | Free (cloud) |
| `gpt-4o` | OpenAI | `gpt-4o` | $0.0025 / $0.01 |
| `gpt-4o-mini` | OpenAI | `gpt-4o-mini` | $0.00015 / $0.0006 |
| `claude-sonnet-4.5` | Anthropic | `claude-sonnet-4-5-20250929` | $0.003 / $0.015 |
| `claude-haiku-4.5` | Anthropic | `claude-haiku-4-5-20251001` | $0.0008 / $0.004 |

---

## Task Status

| Task | Description | Status |
|------|-------------|--------|
| 1 | Model selection & simple LLM call (ModelFactory + Non-RAG demo) | Complete |
| 2 | Vector DB & ingestion pipeline (ChromaDB + document processing) | Planned |
| 3 | Single-turn RAG chain | Planned |
| 4 | Multi-turn simple LLM (conversation memory, no retrieval) | Planned |
| 5 | Multi-turn RAG (conversation memory + retrieval) | Planned |
| 6 | Chatbot UI & performance evaluation | Planned |
