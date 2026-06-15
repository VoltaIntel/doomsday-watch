#!/usr/bin/env python3
"""Build the manual review queue for expired Forecast Engine v2 records.

This script does not resolve forecasts. It only finds expired unresolved forecasts
and writes an operator queue with suggested evidence searches and exact
resolution commands.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from predictions import build_forecast_review_queue, summarize_forecast_review_queue  # noqa: E402

META_FILES = {
    "evaluations.json",
    "lifetime_stats.json",
    "brier_history.json",
    "forecast_resolutions.json",
    "forecast_review_queue.json",
}


def _load_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc


def _iter_forecasts(predictions_dir: Path):
    for path in sorted(predictions_dir.glob("*.json")):
        if path.name in META_FILES:
            continue
        payload = _load_json(path, {})
        for forecast in payload.get("forecast_ladder", []) or []:
            yield forecast


def _default_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build expired Forecast Engine v2 manual review queue")
    parser.add_argument("--predictions-dir", default="data/predictions", help="Directory containing prediction JSON files")
    parser.add_argument("--now", default=_default_now(), help="UTC timestamp for expiry comparison")
    parser.add_argument("--limit", type=int, default=50, help="Maximum queue items to write")
    parser.add_argument("--output", default=None, help="Output JSON path; defaults to forecast_review_queue.json in predictions dir")
    args = parser.parse_args(argv)

    predictions_dir = Path(args.predictions_dir)
    predictions_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = predictions_dir / "forecast_resolutions.json"
    ledger = _load_json(ledger_path, {"version": "forecast_resolutions_v1", "forecasts": []})

    queue = build_forecast_review_queue(
        list(_iter_forecasts(predictions_dir)),
        ledger,
        args.now,
        limit=args.limit,
    )
    queue["status"] = summarize_forecast_review_queue(queue)

    output = Path(args.output) if args.output else predictions_dir / "forecast_review_queue.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(queue, indent=2) + "\n")

    print(json.dumps({
        "status": "forecast_review_queue_built",
        "output": str(output),
        "expired_unresolved": queue.get("expired_unresolved", 0),
        "items": len(queue.get("items", [])),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
