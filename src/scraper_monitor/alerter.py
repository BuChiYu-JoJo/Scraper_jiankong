"""Alert integrations for monitor events."""

from __future__ import annotations


def send_alert(webhook: str, message: str) -> None:
    """Placeholder alert sender (e.g. DingTalk)."""
    if webhook:
        print(f"[ALERT] {message}")
