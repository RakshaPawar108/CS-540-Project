"""Tests for Person 5 — S4 Multi-Turn RAG"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_multi_turn_rag_not_implemented():
    response = client.post(
        "/api/v1/chat/multi-turn-rag/",
        json={"session_id": "test-session-1", "query": "What is hypertension?"},
    )
    assert response.status_code == 501


def test_clear_session():
    response = client.delete("/api/v1/chat/multi-turn-rag/test-session-1")
    assert response.status_code == 204
