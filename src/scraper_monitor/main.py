"""CLI entrypoint for scraper monitor."""

from __future__ import annotations

import argparse
import json

from .config import load_settings
from .models import SpiderContext
from .monitor import run_monitor


def _parse_spider_parameters(raw: str) -> dict:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("spider_parameters must be valid JSON") from exc
    if not isinstance(parsed, dict):
        raise ValueError("spider_parameters must be a JSON object")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scraper monitor CLI")
    parser.add_argument("--spider-name", required=True, help="Spider name")
    parser.add_argument("--spider-id", required=True, help="Spider id")
    parser.add_argument("--spider-parameters", default="{}", help="Spider parameters JSON")
    parser.add_argument("--file-name", default="", help="Output file name")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    context = SpiderContext(
        spider_name=args.spider_name,
        spider_id=args.spider_id,
        spider_parameters=_parse_spider_parameters(args.spider_parameters),
        file_name=args.file_name,
    )
    settings = load_settings()
    result = run_monitor(context, settings)
    print(
        f"spider_id={result.spider_id} task_id={result.task_id} status={result.status} "
        f"raw_status={result.raw_status} success_rate={result.success_rate:.2%} "
        f"download_url={result.download_url} updated_at={result.updated_at.isoformat()}"
    )


if __name__ == "__main__":
    main()
