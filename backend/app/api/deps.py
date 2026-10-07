"""FastAPI dependency injection providers."""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from app.core.config import Settings
from app.repositories.disease_repository import DiseaseRepository
from app.repositories.prediction_repository import PredictionRepository
from app.services.disease_service import DiseaseService
from app.services.prediction_service import PredictionService
from app.services.recommendation_service import RecommendationService


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_prediction_repository(request: Request) -> PredictionRepository:
    return request.app.state.prediction_repository


def get_disease_repository(request: Request) -> DiseaseRepository:
    return request.app.state.disease_repository


def get_prediction_service(request: Request) -> PredictionService:
    return request.app.state.prediction_service


def get_disease_service(request: Request) -> DiseaseService:
    return request.app.state.disease_service


def get_recommendation_service(request: Request) -> RecommendationService:
    return request.app.state.recommendation_service


SettingsDep = Annotated[Settings, Depends(get_settings)]
PredictionServiceDep = Annotated[PredictionService, Depends(get_prediction_service)]
DiseaseServiceDep = Annotated[DiseaseService, Depends(get_disease_service)]
RecommendationServiceDep = Annotated[RecommendationService, Depends(get_recommendation_service)]
