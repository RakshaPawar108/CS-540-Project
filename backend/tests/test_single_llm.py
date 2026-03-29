"""Tests for Person 2 — S1 Single LLM"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_single_llm_not_implemented():
    response = client.post("/api/v1/chat/single-llm/", json={"query": "What is hypertension?"})
    assert response.status_code == 501


def test_single_llm_empty_query():
    response = client.post("/api/v1/chat/single-llm/", json={"query": ""})
    assert response.status_code == 422   # Pydantic validation error
