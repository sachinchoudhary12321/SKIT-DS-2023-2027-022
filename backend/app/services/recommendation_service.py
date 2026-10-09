"""Recommendation business logic foundation."""
from __future__ import annotations

from app.core.exceptions import FeatureNotImplementedError


class RecommendationService:
    """Turns a detected disease into actionable treatment steps."""

    async def recommend(self, *args, **kwargs):
        """Foundation stub for recommendation engine."""
        raise FeatureNotImplementedError(
            "The recommendation engine is not implemented yet; "
            "the API contract is already available."
        )
