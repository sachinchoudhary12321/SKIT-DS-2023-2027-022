"""Schemas for the prediction API."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.prediction import PredictionRecord, PredictionStatus


class PredictionCreatedResponse(BaseModel):
    """Returned by POST /api/v1/predictions (201)."""

    prediction_id: UUID = Field(..., description="Unique id of the prediction request.")
    status: PredictionStatus = Field(..., description="Current lifecycle status.")
    filename: str = Field(
        ...,
        description="Server-generated storage filename. Safe to display; never a filesystem path.",
    )


class PredictionResponse(BaseModel):
    """Returned by GET /api/v1/predictions/{prediction_id}.

    `crop`, `disease` and `confidence` remain null until the status becomes
    `completed` (after the real ML model is connected). No results are
    invented before then.
    """

    prediction_id: UUID
    status: PredictionStatus
    crop: str | None = Field(default=None, examples=[None])
    disease: str | None = Field(default=None, examples=[None])
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    created_at: datetime

    @classmethod
    def from_record(cls, record: PredictionRecord) -> "PredictionResponse":
        """Map an internal domain record onto the public API shape."""
        return cls(
            prediction_id=record.prediction_id,
            status=record.status,
            crop=record.crop,
            disease=record.disease,
            confidence=record.confidence,
            created_at=record.created_at,
        )
