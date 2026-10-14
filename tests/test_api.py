"""API tests for the Q&A service using FastAPI's TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_reports_index(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["document_count"] == 6
    assert body["chunks_indexed"] >= 20


def test_ask_returns_answer_with_citation(client):
    response = client.post("/ask", json={"question": "How much does the Pro plan cost?"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] is not None
    assert "$29" in body["answer"]
    top = body["passages"][0]
    assert top["document"] == "billing-and-plans.md"
    assert top["score"] > 0.1
    assert body["citations"][0]["document"] == "billing-and-plans.md"


def test_ask_security_question(client):
    response = client.post(
        "/ask", json={"question": "How do I turn on two-factor authentication?"}
    )
    assert response.status_code == 200
    assert response.json()["passages"][0]["document"] == "security-and-privacy.md"


def test_ask_off_topic_question(client):
    response = client.post(
        "/ask", json={"question": "What is the airspeed velocity of an unladen swallow?"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] is None
    assert body["passages"] == []


def test_ask_rejects_empty_question(client):
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422
