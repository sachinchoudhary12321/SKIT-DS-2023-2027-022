"""Domain types for disease information."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiseaseRecord:
    """Disease catalogue entry.

    The concrete catalogue (names, symptoms, causes, descriptions) is loaded
    in a later task (PostgreSQL table or curated dataset). No scientific
    content is invented at this stage — the repository ships empty.
    """

    name: str                       # canonical slug, e.g. "tomato-late-blight"
    display_name: str               # e.g. "Tomato Late Blight"
    crop: str                       # e.g. "Tomato"
    description: str
    symptoms: tuple[str, ...]
    causes: str
    severity: str                   # "low" | "medium" | "high"
