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
    task_id: str
    status: str
    success_rate: float
    raw_status: str
    updated_at: datetime
    error_number: int = 0
    api_code: int = 0
    api_error_msg: str = ""
    file_size: int = 0
    download_url: str = ""
