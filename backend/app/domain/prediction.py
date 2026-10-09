"""Domain types for the prediction lifecycle."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class PredictionStatus(str, Enum):
    """Lifecycle states of a prediction request.

    received   - upload accepted and stored; no inference has run yet
    processing - the ML layer is currently analysing the image
    completed  - a prediction result is available (crop/disease/confidence)
    failed     - processing stopped; see `error_code`
    """

    RECEIVED = "received"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PredictionRecord:
    """One prediction request and its lifecycle state (storage-agnostic)."""

    prediction_id: UUID
    status: PredictionStatus
    stored_filename: str          # server-generated; NEVER the client's filename
    content_type: str
    size_bytes: int
    created_at: datetime
    updated_at: datetime
    # Filled only when status == COMPLETED (produced by the real model):
    crop: str | None = None
    disease: str | None = None
    confidence: float | None = None
    # Filled only when status == FAILED:
    error_code: str | None = None
