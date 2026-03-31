"""Domain models for scraper monitor."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SpiderContext:
    spider_name: str
    spider_id: str
    spider_parameters: dict[str, Any] = field(default_factory=dict)
    file_name: str = ""


@dataclass
class MonitorResult:
    spider_id: str
    status: str
    success_rate: float
    updated_at: datetime
