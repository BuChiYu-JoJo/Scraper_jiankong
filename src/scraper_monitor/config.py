"""Configuration loading for scraper monitor."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    thordata_token: str
    thordata_authorization: str
    thordata_base_url: str = "https://openapi.thordata.com/api"
    poll_interval: int = 10
    max_running_time: int = 1800
    success_rate_threshold: float = 0.95
    severe_rate_threshold: float = 0.8
    dingtalk_webhook: str = ""


def _get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _get_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer") from exc


def _get_float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be a float") from exc


def _validate_threshold(name: str, value: float) -> None:
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1, got {value}")


def load_settings() -> Settings:
    """Load and validate settings from environment variables."""

    success_rate_threshold = _get_float_env("SUCCESS_RATE_THRESHOLD", 0.95)
    severe_rate_threshold = _get_float_env("SEVERE_RATE_THRESHOLD", 0.8)

    _validate_threshold("SUCCESS_RATE_THRESHOLD", success_rate_threshold)
    _validate_threshold("SEVERE_RATE_THRESHOLD", severe_rate_threshold)

    return Settings(
        thordata_token=_get_required_env("THORDATA_TOKEN"),
        thordata_authorization=_get_required_env("THORDATA_AUTHORIZATION"),
        thordata_base_url=os.getenv("THORDATA_BASE_URL", "https://openapi.thordata.com/api"),
        poll_interval=_get_int_env("POLL_INTERVAL", 10),
        max_running_time=_get_int_env("MAX_RUNNING_TIME", 1800),
        success_rate_threshold=success_rate_threshold,
        severe_rate_threshold=severe_rate_threshold,
        dingtalk_webhook=os.getenv("DINGTALK_WEBHOOK", "").strip(),
    )
