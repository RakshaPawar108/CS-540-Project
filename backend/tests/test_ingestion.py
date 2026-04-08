"""Tests for Person 1 — Ingestion Pipeline"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ingestion_status():
    response = client.get("/api/v1/ingestion/status")
    assert response.status_code == 200
    data = response.json()
    assert "document_count" in data
    assert "collection" in data


def test_ingest_not_implemented():
    response = client.post("/api/v1/ingestion/ingest", json={"query": "diabetes", "max_results": 10})
    assert response.status_code == 501
