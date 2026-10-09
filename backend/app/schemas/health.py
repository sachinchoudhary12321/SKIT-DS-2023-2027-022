"""Schemas for the health endpoint."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Liveness payload returned by GET /api/v1/health."""

    status: Literal["ok"] = "ok"
    service: str = Field(..., examples=["crop-care-backend"])
