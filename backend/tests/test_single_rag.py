"""Tests for Person 3 — S2 Single RAG"""
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import RetrievedChunk

client = TestClient(app)

# --- Validation (no mocking needed) ---

def test_single_rag_empty_query():
    response = client.post("/api/v1/chat/single-rag/", json={"query": ""})
    assert response.status_code == 422

def test_single_rag_top_k_too_low():
    response = client.post("/api/v1/chat/single-rag/", json={"query": "hypertension", "top_k": 0})
    assert response.status_code == 422

def test_single_rag_top_k_too_high():
    response = client.post("/api/v1/chat/single-rag/", json={"query": "hypertension", "top_k": 21})
    assert response.status_code == 422

# --- Happy path (mocked services) ---

@patch("app.routers.single_rag.llm_service.ask_with_context")
@patch("app.routers.single_rag.rag_service.format_context")
@patch("app.routers.single_rag.rag_service.retrieve")
def test_single_rag_success(mock_retrieve, mock_format, mock_ask):
    mock_retrieve.return_value = [
        RetrievedChunk(content="Metformin is first-line therapy.", source="12345", score=0.87),
    ]
    mock_format.return_value = "[Source: 12345]\nMetformin is first-line therapy."
    mock_ask.return_value = {
        "answer": "Metformin is the first-line treatment.",
        "model": "llama-3.3-70b-versatile",
        "prompt_tokens": 100,
        "completion_tokens": 25,
    }

    response = client.post("/api/v1/chat/single-rag/", json={"query": "How is diabetes treated?", "top_k": 3})

    assert response.status_code == 200
    data = response.json()
    assert data["strategy"] == "S2-single-rag"
    assert data["answer"] == "Metformin is the first-line treatment."
    assert len(data["retrieved_chunks"]) == 1
    assert data["retrieved_chunks"][0]["source"] == "12345"

    mock_retrieve.assert_called_once()
    mock_ask.assert_called_once()

# --- LLM error handling ---

@patch("app.routers.single_rag.llm_service.ask_with_context", side_effect=Exception("Groq API down"))
@patch("app.routers.single_rag.rag_service.format_context", return_value="some context")
@patch("app.routers.single_rag.rag_service.retrieve", return_value=[])
def test_single_rag_llm_failure(mock_retrieve, mock_format, mock_ask):
    response = client.post("/api/v1/chat/single-rag/", json={"query": "What is cancer?"})
    assert response.status_code == 500
