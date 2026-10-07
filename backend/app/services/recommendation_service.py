"""Recommendation business logic (contract only).

TODO(Recommendation task): knowledge base + prediction history + risk
analysis. No scientific treatment content is invented at this stage — valid
requests receive HTTP 501.
"""
from __future__ import annotations

from app.core.exceptions import FeatureNotImplementedError
from app.schemas.recommendation import RecommendationContext, RecommendationItem


class RecommendationService:
    """Turns a detected disease into actionable treatment steps."""

    async def recommend(
        self,
        *,
        crop: str,
        disease: str,
        confidence: float | None,
        context: RecommendationContext | None,
    ) -> list[RecommendationItem]:
        """Return recommended actions.

        Raises:
            FeatureNotImplementedError: until the engine is implemented.
        """
        raise FeatureNotImplementedError(
            "The recommendation engine is not implemented yet; "
            "the API contract is already available."
        )
