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
from app.ml.predictor import CropDiseasePredictor
from app.repositories.disease_repository import InMemoryDiseaseRepository
from app.repositories.prediction_repository import InMemoryPredictionRepository
from app.services.disease_service import DiseaseService
from app.services.prediction_service import PredictionService
from app.services.recommendation_service import RecommendationService
from app.storage.image_storage import ImageStorage

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
        "description": "Treatment recommendations (API contract; engine not connected yet).",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown logic (replaces deprecated on_event hooks)."""
    settings: Settings = app.state.settings
    storage: ImageStorage = app.state.storage

    # Make sure the upload directory exists before the first request.
    storage.ensure_ready()

    # Best effort: no trained model exists yet, so this only logs.
    app.state.predictor.warm_up()

    logger.info(
        "Starting %s v%s (environment=%s, upload_dir=%s)",
        settings.app_name,
        settings.app_version,
        settings.environment,
        settings.upload_dir,
    )
    yield
    logger.info("%s stopped.", settings.app_name)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application (factory pattern)."""
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    # --- Shared, process-wide objects (one instance per app) --------------
    # TEMPORARY data layer: in-memory repositories, swapped for SQLAlchemy
    # implementations in the Database Integration task. Nothing outside
    # `app/repositories/` needs to change when that happens.
    storage = ImageStorage(settings.upload_dir)
    predictor = CropDiseasePredictor()
    prediction_service = PredictionService(
        repository=InMemoryPredictionRepository(),
        storage=storage,
        predictor=predictor,
    )
    disease_service = DiseaseService(repository=InMemoryDiseaseRepository())
    recommendation_service = RecommendationService()

    app = FastAPI(
        title="Crop Care Crop API",
        description="AI-powered crop disease detection and recommendation backend.",
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        openapi_tags=_OPENAPI_TAGS,
    )

    # Exposed to dependencies (app/api/deps.py) via request.app.state.
    app.state.settings = settings
    app.state.storage = storage
    app.state.predictor = predictor
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


if __name__ == "__main__":  # `python -m app.main`
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
