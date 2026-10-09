"""Shared API schemas."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Machine-readable error information."""

    code: str = Field(..., description="Stable error code.", examples=["INVALID_IMAGE"])
    message: str = Field(
        ..., description="Human-readable explanation.",
        examples=["Uploaded file is not a supported image."],
    )
    details: Any | None = Field(
        default=None,
        description="Optional extra context (e.g. field-level validation errors).",
    )


class ErrorResponse(BaseModel):
    """Uniform error envelope returned by every failing endpoint."""

    error: ErrorDetail
