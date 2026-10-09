"""Disease catalogue data access."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from app.domain.disease import DiseaseRecord


class DiseaseRepository(ABC):
    """Abstract catalogue interface."""

    @abstractmethod
    async def get_by_name(self, name: str) -> DiseaseRecord | None:
        """Return the disease entry for a slug/name, or None."""


class InMemoryDiseaseRepository(DiseaseRepository):
    """Process-local catalogue. TEMPORARY.

    Ships EMPTY on purpose: the real catalogue (PostgreSQL table or a curated
    dataset) is connected in a later task, and no scientific content is
    invented before then. Until that happens, every lookup returns None and
    the API answers 404 DISEASE_NOT_FOUND.
    """

    def __init__(self, records: Iterable[DiseaseRecord] | None = None) -> None:
        self._records: dict[str, DiseaseRecord] = {
            record.name.strip().lower(): record for record in (records or ())
        }

    async def get_by_name(self, name: str) -> DiseaseRecord | None:
        return self._records.get(name.strip().lower())
