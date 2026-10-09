"""Dependency-injection wiring.

Routes depend on the objects below; FastAPI resolves them per request.
Tests can replace any of them via `app.dependency_overrides`.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from app.core.config import Settings
from app.services.disease_service import DiseaseService
from app.services.prediction_service import PredictionService
from app.services.recommendation_service import RecommendationService


def get_app_settings(request: Request) -> Settings:
    """Return the Settings the application was created with."""
    return request.app.state.settings


def get_prediction_service(request: Request) -> PredictionService:
    """Return the process-wide prediction service."""
    return request.app.state.prediction_service


def get_disease_service(request: Request) -> DiseaseService:
    """Return the process-wide disease service."""
    return request.app.state.disease_service


def get_recommendation_service(request: Request) -> RecommendationService:
    """Return the process-wide recommendation service."""
    return request.app.state.recommendation_service


SettingsDep = Annotated[Settings, Depends(get_app_settings)]
PredictionServiceDep = Annotated[PredictionService, Depends(get_prediction_service)]
DiseaseServiceDep = Annotated[DiseaseService, Depends(get_disease_service)]
RecommendationServiceDep = Annotated[RecommendationService, Depends(get_recommendation_service)]
