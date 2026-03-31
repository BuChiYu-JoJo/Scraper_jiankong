"""Analyze crawler execution metrics."""

from __future__ import annotations


def classify_health(success_rate: float, severe_rate_threshold: float, success_rate_threshold: float) -> str:
    if success_rate < severe_rate_threshold:
        return "severe"
    if success_rate < success_rate_threshold:
        return "warning"
    return "healthy"
