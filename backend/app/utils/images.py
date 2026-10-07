"""Upload validation for image files.

Validation order (cheap -> expensive, fail fast):
  1. allowlisted content type (from the multipart headers);
  2. bounded read — never buffer more than max_size + 1 bytes;
  3. emptiness check;
  4. size check;
  5. magic-byte sniff — the bytes must actually be a JPEG / PNG / WebP.
"""
from __future__ import annotations

from dataclasses import dataclass

from fastapi import UploadFile

from app.core.exceptions import FileTooLargeError, InvalidImageError

# content type -> storage extension
ALLOWED_IMAGE_TYPES: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_JPEG_SIGNATURE = b"\xff\xd8\xff"


@dataclass(frozen=True)
class ValidatedImage:
    """A validated upload, ready to be stored and (later) analysed."""

    data: bytes
    content_type: str
    extension: str
    size_bytes: int


def _matches_magic_bytes(data: bytes, content_type: str) -> bool:
    """Return True when `data` really starts like the declared image format."""
    if content_type == "image/jpeg":
        return data.startswith(_JPEG_SIGNATURE)
    if content_type == "image/png":
        return data.startswith(_PNG_SIGNATURE)
    if content_type == "image/webp":
        # RIFF container: "RIFF" <size> "WEBP"
        return len(data) >= 12 and data[0:4] == b"RIFF" and data[8:12] == b"WEBP"
    return False


async def read_validated_image(upload: UploadFile, *, max_size_bytes: int) -> ValidatedImage:
    """Validate an uploaded image and return its bytes + metadata.

    Raises:
        InvalidImageError: unsupported content type, empty file, or the file
            content does not match a supported image format.
        FileTooLargeError: file larger than `max_size_bytes`.
    """
    raw_content_type = (upload.content_type or "").split(";", 1)[0].strip().lower()
    if raw_content_type not in ALLOWED_IMAGE_TYPES:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_TYPES))
        raise InvalidImageError(
            f"Unsupported content type '{raw_content_type or 'unknown'}'. Allowed types: {allowed}."
        )

    # Read at most max_size + 1 bytes: oversized uploads are detected without
    # ever loading the whole file into memory.
    data = await upload.read(max_size_bytes + 1)

    if not data:
        raise InvalidImageError("Uploaded file is empty.")

    if len(data) > max_size_bytes:
        raise FileTooLargeError(
            f"Uploaded file exceeds the maximum allowed size of {max_size_bytes // (1024 * 1024)} MB."
        )

    if not _matches_magic_bytes(data, raw_content_type):
        raise InvalidImageError(
            "Uploaded file is not a supported image (content does not match its declared type)."
        )

    return ValidatedImage(
        data=data,
        content_type=raw_content_type,
        extension=ALLOWED_IMAGE_TYPES[raw_content_type],
        size_bytes=len(data),
    )
