"""Storage helpers for monitoring artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def dump_json(data: dict[str, Any], file_name: str) -> None:
    Path(file_name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
