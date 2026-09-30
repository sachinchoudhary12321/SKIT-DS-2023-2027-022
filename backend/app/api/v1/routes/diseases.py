"""Disease information endpoint.

Contract-only: the catalogue repository ships empty, so every lookup returns
404 DISEASE_NOT_FOUND until the catalogue is connected in a later task.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Path, status

from app.api.deps import DiseaseServiceDep
from app.schemas.common import ErrorResponse
from app.schemas.disease import DiseaseResponse

router = APIRouter(prefix="/diseases", tags=["diseases"])

DiseaseName = Annotated[
    str,
    Path(
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9 _-]+$",
        description="Disease identifier/slug, e.g. 'tomato-late-blight'.",
    ),
]


@router.get(
    "/{disease_name}",
    response_model=DiseaseResponse,
    summary="Get disease information",
    description=(
        "Returns catalogue information for a disease slug. The catalogue is "
        "connected in a later task; until then this endpoint answers 404."
    ),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Disease not found in the catalogue",
        },
        getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422): {
            "model": ErrorResponse,
            "description": "Malformed disease name",
        },
    },
)
async def get_disease(
    disease_name: DiseaseName,
    service: DiseaseServiceDep,
) -> DiseaseResponse:
    """Return information about one disease."""
    record = await service.get_disease(disease_name)
    return DiseaseResponse.from_record(record)
