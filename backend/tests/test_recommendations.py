"""Tests for the recommendation endpoint (contract only for now)."""
from __future__ import annotations

from fastapi.testclient import TestClient

RECOMMENDATIONS_URL = "/api/v1/recommendations"

_VALID_PAYLOAD: dict = {
    "crop": "tomato",
    "disease": "late blight",
    "confidence": 0.92,
    "context": {"location": "Pune", "growth_stage": "flowering"},
}


def test_valid_request_returns_501(client: TestClient) -> None:
    response = client.post(RECOMMENDATIONS_URL, json=_VALID_PAYLOAD)

    assert response.status_code == 501
    error = response.json()["error"]
    assert error["code"] == "NOT_IMPLEMENTED"
    assert set(error) >= {"code", "message", "details"}


def test_empty_context_is_accepted(client: TestClient) -> None:
    payload = {**_VALID_PAYLOAD, "context": {}}
    response = client.post(RECOMMENDATIONS_URL, json=payload)

    # Empty context is valid — the engine (not the schema) is what's missing.
    assert response.status_code == 501
    assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"


def test_missing_required_field_returns_422(client: TestClient) -> None:
    response = client.post(RECOMMENDATIONS_URL, json={"crop": "tomato"})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["details"]  # field-level details present


def test_invalid_confidence_returns_422(client: TestClient) -> None:
    payload = {**_VALID_PAYLOAD, "confidence": 1.5}  # outside [0, 1]

    response = client.post(RECOMMENDATIONS_URL, json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_empty_body_returns_422(client: TestClient) -> None:
    response = client.post(RECOMMENDATIONS_URL, json={})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
