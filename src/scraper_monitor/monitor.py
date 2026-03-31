"""Main monitor process orchestration."""

from __future__ import annotations

from datetime import datetime

from .alerter import send_alert
from .analyzer import classify_health
from .client import ThorDataClient
from .config import Settings
from .models import MonitorResult, SpiderContext
from .storage import dump_json


def run_monitor(context: SpiderContext, settings: Settings) -> MonitorResult:
    client = ThorDataClient(settings)
    payload = client.fetch_spider_status(context.spider_id)

    success_rate = float(payload.get("success_rate", 0))
    status = classify_health(success_rate, settings.severe_rate_threshold, settings.success_rate_threshold)

    if status != "healthy":
        send_alert(settings.dingtalk_webhook, f"Spider {context.spider_name} status is {status}")

    if context.file_name:
        dump_json(payload, context.file_name)

    return MonitorResult(
        spider_id=context.spider_id,
        status=status,
        success_rate=success_rate,
        updated_at=datetime.utcnow(),
    )
