"""Application settings, loaded from environment variables / `.env`.

Nothing sensitive is hard-coded: every value comes from the environment and
can be overridden (see `.env.example`). Field names map to upper-case env
variables, e.g. `app_name` is read from `APP_NAME`.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_name: str = "crop-care-backend"
    app_version: str = "0.2.0"
    environment: Literal["local", "development", "staging", "production"] = "local"
    debug: bool = False
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"

    # --- CORS (comma-separated string, parsed by cors_origin_list) ---
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # --- Image uploads ---
    upload_dir: Path = Path("storage/uploads")
    max_upload_size_mb: int = Field(default=10, gt=0)

    # Later tasks add: database_url, ml_model_dir, ollama_* (see .env.example).

    @property
    def cors_origin_list(self) -> list[str]:
        """`cors_origins` parsed into a list for CORSMiddleware."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings object (cached)."""
    return Settings()
