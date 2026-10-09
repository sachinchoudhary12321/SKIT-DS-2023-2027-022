"""Disease information business logic."""
from __future__ import annotations

from app.core.exceptions import DiseaseNotFoundError
from app.domain.disease import DiseaseRecord
from app.repositories.disease_repository import DiseaseRepository


class DiseaseService:
    """Looks up disease catalogue entries."""

    def __init__(self, repository: DiseaseRepository) -> None:
        self._repository = repository

    async def get_disease(self, name: str) -> DiseaseRecord:
        """Return the catalogue entry for `name`.

        Raises:
            DiseaseNotFoundError: when the name is not in the catalogue
                (currently always — the catalogue is connected in a later task).
        """
        record = await self._repository.get_by_name(name)
        if record is None:
            raise DiseaseNotFoundError(f"Disease '{name}' is not in the catalogue.")
        return record
