"""Time helpers."""
from __future__ import annotations

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Timezone-aware current UTC time (never use naive datetimes)."""
    return datetime.now(timezone.utc)
