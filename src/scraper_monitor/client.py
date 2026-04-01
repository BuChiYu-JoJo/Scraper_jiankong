"""API client for Thordata service."""

from __future__ import annotations

import json
from typing import Any
from urllib import error, request

from .config import Settings


class ThorDataClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _request(self, path: str, payload: dict[str, Any], include_auth: bool = False) -> dict[str, Any]:
        url = f"{self.settings.thordata_base_url.rstrip('/')}/{path.lstrip('/')}"
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "token": self.settings.thordata_token,
        }
        if include_auth:
            headers["Authorization"] = self.settings.thordata_authorization

        req = request.Request(url=url, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=30) as response:
                content = response.read().decode("utf-8")
        except error.HTTPError as exc:
            raise RuntimeError(f"Thordata API HTTP error: {exc.code}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Thordata API network error: {exc.reason}") from exc

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Thordata API returned non-JSON response") from exc
        if not isinstance(parsed, dict):
            raise RuntimeError("Thordata API returned unexpected response structure")
        return parsed

    def create_task(self, spider_name: str, spider_id: str, spider_parameters: dict[str, Any], file_name: str) -> str:
        payload = self._request(
            "/web-scraper-api/tasks-create",
            {
                "spider_name": spider_name,
                "spider_id": spider_id,
                "spider_parameters": json.dumps(spider_parameters, ensure_ascii=False),
                "spider_errors": "true",
                "file_name": file_name or "{{TasksID}}.json",
            },
            include_auth=True,
        )
        data = payload.get("data", {})
        if payload.get("code") != 200 or not isinstance(data, dict) or not data.get("task_id"):
            raise RuntimeError(f"Failed to create task: {payload}")
        return str(data["task_id"])

    def fetch_task_status(self, task_id: str) -> str:
        payload = self._request("/web-scraper-api/tasks-status", {"tasks_ids": task_id})
        data = payload.get("data", [])
        if payload.get("code") != 200 or not isinstance(data, list) or not data:
            raise RuntimeError(f"Failed to fetch task status: {payload}")
        record = data[0]
        if not isinstance(record, dict) or "status" not in record:
            raise RuntimeError(f"Task status missing in response: {payload}")
        return str(record["status"])

    def fetch_task_metrics(self, task_id: str) -> dict[str, Any]:
        payload = self._request("/web-scraper-api/tasks-list", {"page": 1, "size": 100})
        data = payload.get("data", {})
        records = data.get("list", []) if isinstance(data, dict) else []
        if payload.get("code") != 200 or not isinstance(records, list):
            raise RuntimeError(f"Failed to fetch task list: {payload}")
        for item in records:
            if isinstance(item, dict) and str(item.get("task_id")) == task_id:
                return item
        return {}

    def fetch_download_url(self, task_id: str) -> str:
        payload = self._request("/web-scraper-api/tasks-download", {"tasks_id": task_id, "type": "json"})
        data = payload.get("data", {})
        if payload.get("code") != 200 or not isinstance(data, dict):
            return ""
        return str(data.get("download", "") or "")
