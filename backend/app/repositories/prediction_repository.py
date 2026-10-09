"""Prediction data access."""
from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.prediction import PredictionRecord


class PredictionRepository(ABC):
    """Abstract persistence interface for prediction records."""

    @abstractmethod
    async def add(self, record: PredictionRecord) -> PredictionRecord:
        """Persist a new record and return it."""

    @abstractmethod
    async def get(self, prediction_id: UUID) -> PredictionRecord | None:
        """Return the record, or None when it does not exist."""

    @abstractmethod
    async def update(self, record: PredictionRecord) -> PredictionRecord:
        """Persist changes to an existing record and return it."""


class InMemoryPredictionRepository(PredictionRepository):
    """Process-local, non-persistent storage. TEMPORARY — not for production.

    Limitations (by design, for this milestone):
      * data disappears when the process restarts;
      * data is not shared between multiple Uvicorn workers.

    Replaced by an SQLAlchemy + PostgreSQL implementation in the Database
    Integration task.
    """

    def __init__(self) -> None:
        self._records: dict[UUID, PredictionRecord] = {}

    async def add(self, record: PredictionRecord) -> PredictionRecord:
        self._records[record.prediction_id] = record
        return record

    async def get(self, prediction_id: UUID) -> PredictionRecord | None:
        return self._records.get(prediction_id)

    async def update(self, record: PredictionRecord) -> PredictionRecord:
        self._records[record.prediction_id] = record
        return record
