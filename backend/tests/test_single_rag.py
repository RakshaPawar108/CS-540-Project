"""Tests for Person 3 — S2 Single RAG"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_single_rag_not_implemented():
    response = client.post("/api/v1/chat/single-rag/", json={"query": "What is hypertension?"})
    assert response.status_code == 501


def test_single_rag_top_k_validation():
    response = client.post("/api/v1/chat/single-rag/", json={"query": "hypertension", "top_k": 0})
    assert response.status_code == 422
