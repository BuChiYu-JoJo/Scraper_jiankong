"""Analyze crawler execution metrics."""

from __future__ import annotations

from typing import Any


def classify_health(success_rate: float, severe_rate_threshold: float, success_rate_threshold: float) -> str:
    if success_rate < severe_rate_threshold:
        return "severe"
    if success_rate < success_rate_threshold:
        return "warning"
    return "healthy"


def parse_success_rate(value: Any) -> float:
    try:
        rate = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(1.0, rate))


def assess_status(raw_status: str, success_rate: float, error_number: int, api_code: int, api_error_msg: str, severe_rate_threshold: float, success_rate_threshold: float) -> str:
    normalized = raw_status.strip().lower()
    if normalized == "failed":
        return "severe"
    if normalized == "running":
        return "warning"
    if error_number > 0:
        return "warning"
    if api_error_msg.strip():
        return "warning"
    if api_code not in (0, 200):
        return "warning"
    return classify_health(success_rate, severe_rate_threshold, success_rate_threshold)
