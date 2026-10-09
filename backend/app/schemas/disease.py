"""Schemas for the disease information API."""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.disease import DiseaseRecord


class DiseaseResponse(BaseModel):
    """Disease information contract (served once the catalogue is connected)."""

    name: str = Field(..., examples=["tomato-late-blight"])
    display_name: str = Field(..., examples=["Tomato Late Blight"])
    crop: str = Field(..., examples=["Tomato"])
    description: str
    symptoms: list[str]
    causes: str
    severity: str = Field(..., description="low | medium | high")

    @classmethod
    def from_record(cls, record: DiseaseRecord) -> "DiseaseResponse":
        return cls(
            name=record.name,
            display_name=record.display_name,
            crop=record.crop,
            description=record.description,
            symptoms=list(record.symptoms),
            causes=record.causes,
            severity=record.severity,
        )
