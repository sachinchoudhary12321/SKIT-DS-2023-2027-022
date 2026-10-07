"""Prediction lifecycle business logic.

Lifecycle: received -> processing -> completed | failed
"""
from __future__ import annotations

import logging
from uuid import UUID

from app.core.exceptions import PredictionNotFoundError
from app.domain.prediction import PredictionRecord
from app.repositories.prediction_repository import PredictionRepository

logger = logging.getLogger(__name__)


class PredictionService:
    """Coordinates the prediction lifecycle."""

    def __init__(
        self,
        repository: PredictionRepository,
        storage=None,
        predictor=None,
    ) -> None:
        self._repository = repository
        self._storage = storage
        self._predictor = predictor

    async def get_prediction(self, prediction_id: UUID) -> PredictionRecord:
        """Fetch a prediction record by its UUID, or raise 404."""
        record = await self._repository.get(prediction_id)
        if record is None:
            raise PredictionNotFoundError(prediction_id)
        return record
