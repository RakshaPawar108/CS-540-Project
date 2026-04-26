"""Tests for Person 4 — S3 Multi-Turn LLM"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_multi_turn_llm_returns_answer():
    response = client.post(
        "/api/v1/chat/multi-turn-llm/",
        json={"session_id": "test-session-1", "query": "What is hypertension?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert data["strategy"] == "S3-multi-turn-llm"
    assert data["session_id"] == "test-session-1"
    assert data["history_length"] == 1


def test_multi_turn_llm_memory():
    """Second query in the same session should increment history_length."""
    session_id = "test-session-memory"

    client.post(
        "/api/v1/chat/multi-turn-llm/",
        json={"session_id": session_id, "query": "What is hypertension?"},
    )
    response = client.post(
        "/api/v1/chat/multi-turn-llm/",
        json={"session_id": session_id, "query": "What medications are used to treat it?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["history_length"] == 2
    assert data["session_id"] == session_id


def test_multi_turn_llm_independent_sessions():
    """Different session IDs should have independent history."""
    client.post(
        "/api/v1/chat/multi-turn-llm/",
        json={"session_id": "session-a", "query": "What is diabetes?"},
    )
    response = client.post(
        "/api/v1/chat/multi-turn-llm/",
        json={"session_id": "session-b", "query": "What is hypertension?"},
    )
    assert response.status_code == 200
    assert response.json()["history_length"] == 1  # session-b has no prior turns


def test_clear_session():
    session_id = "test-session-clear"
    client.post(
        "/api/v1/chat/multi-turn-llm/",
        json={"session_id": session_id, "query": "What is diabetes?"},
    )
    response = client.delete(f"/api/v1/chat/multi-turn-llm/{session_id}")
    assert response.status_code == 204
