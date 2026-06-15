#!/usr/bin/env python3
"""Resolve Forecast Engine v2 records into the operator calibration ledger.

This is intentionally manual/source-verified. It does not scrape or infer
outcomes; the operator supplies outcome + evidence, and the script computes the
Brier score and updates data/predictions/forecast_resolutions.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from predictions import compute_horizon_calibration, resolve_forecast, upsert_forecast_resolution  # noqa: E402


def _parse_bool(value: str) -> bool:
    value_l = str(value).strip().lower()
    if value_l in {"true", "t", "yes", "y", "1", "occurred", "hit"}:
        return True
    if value_l in {"false", "f", "no", "n", "0", "missed", "not_occurred"}:
        return False
    raise argparse.ArgumentTypeError("outcome must be true/false")


def _load_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc


def _iter_forecasts(predictions_dir: Path):
    for path in sorted(predictions_dir.glob("*.json")):
        if path.name in {"evaluations.json", "lifetime_stats.json", "brier_history.json", "forecast_resolutions.json"}:
            continue
        payload = _load_json(path, {})
        for forecast in payload.get("forecast_ladder", []) or []:
            yield forecast, path


def _find_forecast(predictions_dir: Path, forecast_id: str):
    for forecast, path in _iter_forecasts(predictions_dir):
        if forecast.get("forecast_id") == forecast_id:
            return forecast, path
    raise SystemExit(f"forecast_id not found in {predictions_dir}: {forecast_id}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Resolve a Forecast Engine v2 forecast into the calibration ledger")
    parser.add_argument("--forecast-id", required=True, help="forecast_ladder forecast_id to resolve")
    parser.add_argument("--outcome", required=True, type=_parse_bool, help="true/false outcome")
    parser.add_argument("--resolved-at", required=True, help="UTC timestamp, e.g. 2026-06-15T18:00:00Z")
    parser.add_argument("--predictions-dir", default="data/predictions", help="Directory containing prediction JSON files")
    parser.add_argument("--evidence-title", required=True, help="Evidence headline/title")
    parser.add_argument("--evidence-url", default="", help="Evidence URL")
    parser.add_argument("--evidence-source", default="operator_supplied", help="Evidence source/publisher")
    parser.add_argument("--resolved-by", default="operator", help="Resolver identity label")
    parser.add_argument("--notes", default="", help="Optional operator notes")
    args = parser.parse_args(argv)

    predictions_dir = Path(args.predictions_dir)
    predictions_dir.mkdir(parents=True, exist_ok=True)
    forecast, source_file = _find_forecast(predictions_dir, args.forecast_id)

    resolved = resolve_forecast(
        forecast,
        outcome=args.outcome,
        resolved_at=args.resolved_at,
        evidence=[{
            "title": args.evidence_title,
            "url": args.evidence_url,
            "source": args.evidence_source,
        }],
        resolved_by=args.resolved_by,
        notes=args.notes,
    )

    ledger_path = predictions_dir / "forecast_resolutions.json"
    ledger = _load_json(ledger_path, {"version": "forecast_resolutions_v1", "forecasts": []})
    ledger = upsert_forecast_resolution(ledger, resolved)
    ledger["calibration"] = compute_horizon_calibration(ledger.get("forecasts", []))
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")

    print(json.dumps({
        "status": "forecast_resolved",
        "forecast_id": args.forecast_id,
        "source_file": str(source_file),
        "ledger": str(ledger_path),
        "outcome": args.outcome,
        "brier": resolved.get("brier"),
        "resolved_count": ledger.get("count", len(ledger.get("forecasts", []))),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
