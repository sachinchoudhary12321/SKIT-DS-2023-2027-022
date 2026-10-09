"""Shared pytest fixtures.

Each test gets a fresh app instance with isolated settings (temporary upload
directory, no .env reading) and fresh in-memory repositories.
"""
from __future__ import annotations

import struct
import zlib
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def make_test_png() -> bytes:
    """Build a genuinely valid 1x1 red PNG without external libraries."""
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = _png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    raw_scanline = b"\x00\xff\x00\x00"          # filter byte + one red RGB pixel
    idat = _png_chunk(b"IDAT", zlib.compress(raw_scanline))
    iend = _png_chunk(b"IEND", b"")
    return signature + ihdr + idat + iend


@pytest.fixture()
def app_settings(tmp_path) -> Settings:
    """Isolated settings: temporary upload dir, no .env file, 1 MB size limit."""
    return Settings(
        _env_file=None,
        upload_dir=tmp_path / "uploads",
        max_upload_size_mb=1,
    )


@pytest.fixture()
def client(app_settings: Settings) -> Iterator[TestClient]:
    """TestClient with lifespan startup/shutdown, like a real server run."""
    app = create_app(app_settings)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def png_bytes() -> bytes:
    """A valid 1x1 PNG image."""
    return make_test_png()
