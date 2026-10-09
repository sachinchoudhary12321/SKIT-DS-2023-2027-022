"""Tests for the disease information endpoint."""
from __future__ import annotations

from fastapi.testclient import TestClient

DISEASES_URL = "/api/v1/diseases"


def test_unknown_disease_returns_404(client: TestClient) -> None:
    """The catalogue ships empty, so every lookup is a clean 404."""
    response = client.get(f"{DISEASES_URL}/tomato-late-blight")

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "DISEASE_NOT_FOUND"
    assert "message" in error


def test_invalid_disease_name_returns_422(client: TestClient) -> None:
    response = client.get(f"{DISEASES_URL}/bad@name!")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
