"""Main monitor process orchestration."""

from __future__ import annotations

from datetime import datetime
import time

from .alerter import send_alert
from .analyzer import assess_status, parse_success_rate
from .client import ThorDataClient
from .config import Settings
from .models import MonitorResult, SpiderContext
from .storage import dump_json


def run_monitor(context: SpiderContext, settings: Settings) -> MonitorResult:
    client = ThorDataClient(settings)
    task_id = client.create_task(
        spider_name=context.spider_name,
        spider_id=context.spider_id,
        spider_parameters=context.spider_parameters,
        file_name=context.file_name,
    )

    elapsed = 0
    raw_status = "Running"
    while elapsed <= settings.max_running_time:
        raw_status = client.fetch_task_status(task_id)
        if raw_status.lower() in {"ready", "failed"}:
            break
        time.sleep(settings.poll_interval)
        elapsed += settings.poll_interval

    metrics = client.fetch_task_metrics(task_id)
    success_rate = parse_success_rate(metrics.get("success_rate"))
    error_number = int(metrics.get("error_number", 0) or 0)
    api_code = int(metrics.get("api_code", 0) or 0)
    api_error_msg = str(metrics.get("api_error_msg", "") or "")
    file_size = int(metrics.get("file_size", 0) or 0)

    if elapsed > settings.max_running_time and raw_status.lower() == "running":
        status = "severe"
        api_error_msg = "monitor timeout reached before task completion"
    else:
        status = assess_status(
            raw_status=raw_status,
            success_rate=success_rate,
            error_number=error_number,
            api_code=api_code,
            api_error_msg=api_error_msg,
            severe_rate_threshold=settings.severe_rate_threshold,
            success_rate_threshold=settings.success_rate_threshold,
        )

    download_url = client.fetch_download_url(task_id) if raw_status.lower() == "ready" else ""

    if status != "healthy":
        send_alert(
            settings.dingtalk_webhook,
            f"Spider {context.spider_name} task_id={task_id} status={status} raw_status={raw_status}",
        )

    if context.file_name:
        dump_json(
            {
                "spider_name": context.spider_name,
                "spider_id": context.spider_id,
                "task_id": task_id,
                "raw_status": raw_status,
                "status": status,
                "success_rate": success_rate,
                "error_number": error_number,
                "api_code": api_code,
                "api_error_msg": api_error_msg,
                "file_size": file_size,
                "download_url": download_url,
                "updated_at": datetime.utcnow().isoformat(),
                "metrics": metrics,
            },
            context.file_name,
        )

    return MonitorResult(
        spider_id=context.spider_id,
        task_id=task_id,
        status=status,
        success_rate=success_rate,
        raw_status=raw_status,
        error_number=error_number,
        api_code=api_code,
        api_error_msg=api_error_msg,
        file_size=file_size,
        download_url=download_url,
        updated_at=datetime.utcnow(),
    )
