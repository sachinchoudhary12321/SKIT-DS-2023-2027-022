"""Prediction request and lifecycle endpoints."""
from __future__ import annotations

import logging
from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import PredictionServiceDep
from app.core.exceptions import AppError
from app.schemas.prediction import (
    PredictionCreatedResponse,
    PredictionResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post(
    "",
    response_model=PredictionCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload crop image for disease prediction",
)
async def create_prediction():
    """Stub endpoint for prediction creation in API milestone."""
    raise AppError(
        code="NOT_IMPLEMENTED",
        message="Image storage and validation is introduced in upload milestone.",
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
    )


@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get prediction status and result",
)
async def get_prediction(
    prediction_id: UUID,
    service: PredictionServiceDep,
) -> PredictionResponse:
    """Fetch prediction status and result by UUID."""
    record = await service.get_prediction(prediction_id)
    return PredictionResponse.from_record(record)
