"""API client for Thordata service."""

from __future__ import annotations

from typing import Any

from .config import Settings


class ThorDataClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def fetch_spider_status(self, spider_id: str) -> dict[str, Any]:
        """Placeholder for API call to query spider status."""
        return {"spider_id": spider_id, "status": "running", "success_rate": 1.0}
