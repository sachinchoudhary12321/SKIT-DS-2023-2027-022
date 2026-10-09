"""Service health endpoint."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import SettingsDep
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service health check",
    description="Liveness probe used by the frontend, CI and monitoring.",
)
async def health_check(settings: SettingsDep) -> HealthResponse:
    """Return the liveness payload."""
    return HealthResponse(status="ok", service=settings.app_name)
