"""Aggregates every v1 router. Mounted under /api/v1 by app.main.

Adding a feature = create a router in routes/ and include it here.
A future v2 gets its own app/api/v2/ package — nothing else moves.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.routes import diseases, health, predictions, recommendations

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(predictions.router)
api_v1_router.include_router(diseases.router)
api_v1_router.include_router(recommendations.router)
