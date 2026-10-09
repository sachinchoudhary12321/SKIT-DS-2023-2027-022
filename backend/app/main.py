"""FastAPI application entry point.

Run locally with:
    uvicorn app.main:app --reload --port 8000
"""
from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import Settings, get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.repositories.disease_repository import InMemoryDiseaseRepository
from app.repositories.prediction_repository import InMemoryPredictionRepository
from app.services.disease_service import DiseaseService
from app.services.prediction_service import PredictionService
from app.services.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)

_OPENAPI_TAGS = [
    {"name": "health", "description": "Service liveness."},
    {
        "name": "predictions",
        "description": "Upload crop images and track prediction requests.",
    },
    {"name": "diseases", "description": "Disease information catalogue."},
    {
        "name": "recommendations",
        "description": "Treatment recommendations.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown logic."""
    settings: Settings = app.state.settings
    logger.info(
        "Starting %s v%s (environment=%s)",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory."""
    if settings is None:
        settings = get_settings()

    configure_logging(settings.log_level)

    prediction_repo = InMemoryPredictionRepository()
    prediction_service = PredictionService(repository=prediction_repo)
    disease_service = DiseaseService(repository=InMemoryDiseaseRepository())
    recommendation_service = RecommendationService()

    app = FastAPI(
        title="Crop Care Crop API",
        version="1.0.0",
        description=(
            "Crop Care Crop — Agricultural disease detection and treatment advisory API. "
            "Backend architecture milestone."
        ),
        openapi_tags=_OPENAPI_TAGS,
        lifespan=lifespan,
    )

    app.state.settings = settings
    app.state.prediction_repository = prediction_repo
    app.state.prediction_service = prediction_service
    app.state.disease_service = disease_service
    app.state.recommendation_service = recommendation_service

    # Middleware — LAST added runs FIRST (outermost).
    app.add_middleware(RequestLoggingMiddleware)   # inner
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )                                               # outer

    register_exception_handlers(app)
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
