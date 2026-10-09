"""Treatment recommendation endpoint.

Contract-only for the moment: the request/response schemas are final, but the
engine is not implemented, so valid requests receive HTTP 501 with code
NOT_IMPLEMENTED. No scientific content is invented.
"""
from __future__ import annotations

from fastapi import APIRouter, status

from app.api.deps import RecommendationServiceDep
from app.schemas.common import ErrorResponse
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.utils.time import utcnow

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post(
    "",
    response_model=RecommendationResponse,
    summary="Get treatment recommendations for a detected disease",
    description=(
        "Validates crop/disease/optional context and returns recommended "
        "actions. The engine is not implemented yet, so valid requests "
        "receive HTTP 501 (code NOT_IMPLEMENTED)."
    ),
    responses={
        status.HTTP_501_NOT_IMPLEMENTED: {
            "model": ErrorResponse,
            "description": "Recommendation engine not implemented yet",
        },
        getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422): {
            "model": ErrorResponse,
            "description": "Malformed request body",
        },
    },
)
async def create_recommendation(
    payload: RecommendationRequest,
    service: RecommendationServiceDep,
) -> RecommendationResponse:
    """Return recommended actions for a disease (not implemented yet)."""
    items = await service.recommend(
        crop=payload.crop,
        disease=payload.disease,
        confidence=payload.confidence,
        context=payload.context,
    )
    return RecommendationResponse(
        crop=payload.crop,
        disease=payload.disease,
        recommendations=items,
        generated_at=utcnow(),
    )
