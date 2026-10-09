"""Schemas for the treatment recommendation API.

Contract-only for now: the engine is not implemented, so valid requests get
HTTP 501. The schemas define the target shape for the future implementation.
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RecommendationContext(BaseModel):
    """Optional extra context provided by the client.

    Extra fields are accepted so the contract can grow without a breaking
    change (e.g. weather, irrigation, soil data added later).
    """

    model_config = ConfigDict(extra="allow")

    location: str | None = Field(default=None, max_length=200)
    growth_stage: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None, max_length=500)


class RecommendationRequest(BaseModel):
    """Request body for POST /api/v1/recommendations."""

    crop: str = Field(..., min_length=1, max_length=100, examples=["tomato"])
    disease: str = Field(..., min_length=1, max_length=200, examples=["late blight"])
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    context: RecommendationContext | None = None


class RecommendationItem(BaseModel):
    """A single recommended action."""

    category: Literal["treatment", "prevention", "monitoring"]
    title: str
    description: str


class RecommendationResponse(BaseModel):
    """Recommended actions for a detected disease."""

    crop: str
    disease: str
    recommendations: list[RecommendationItem]
    generated_at: datetime
