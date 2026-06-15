from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from predictions import generate_forecast_ladder  # noqa: E402


def _sample_forecast():
    forecasts = generate_forecast_ladder(
        [{
            "id": "iran_nuclear",
            "name": "IRAN NUCLEAR",
            "prob": 70,
            "trend": "rising",
            "zone": "imminent",
            "signals": [{"name": "IAEA access denied", "original_weight": 8, "positive": False}],
        }],
        {
            "latest_news": [{
                "headline": "IAEA says access dispute escalated",
                "sources": ["Reuters", "IAEA"],
                "zone": "iran_nuclear",
            }],
            "trackers": {"iran_nuclear": {"active_signals": ["iaea_access_denied"]}},
        },
        "2026-06-15T12:00:00Z",
    )
    return forecasts[0]


def test_resolve_forecast_cli_updates_operator_ledger_and_reports_calibration(tmp_path):
    data_dir = tmp_path / "data" / "predictions"
    data_dir.mkdir(parents=True)
    forecast = _sample_forecast()
    (data_dir / "2026-06-15-12.json").write_text(json.dumps({"forecast_ladder": [forecast]}, indent=2))

    script = REPO_ROOT / "scripts" / "resolve_forecast.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--forecast-id", forecast["forecast_id"],
            "--outcome", "true",
            "--resolved-at", "2026-06-15T18:00:00Z",
            "--evidence-title", "IAEA confirms emergency action",
            "--evidence-url", "https://www.iaea.org/news/example",
            "--evidence-source", "IAEA",
            "--notes", "operator verified",
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "forecast_resolved" in result.stdout
    ledger = json.loads((data_dir / "forecast_resolutions.json").read_text())
    assert ledger["count"] == 1
    resolved = ledger["forecasts"][0]
    assert resolved["forecast_id"] == forecast["forecast_id"]
    assert resolved["resolved_outcome"] is True
    assert resolved["resolution_evidence"][0]["url"] == "https://www.iaea.org/news/example"
    assert "calibration" in ledger
    assert ledger["calibration"]["horizons"][forecast["horizon_label"]]["count"] == 1


def test_review_forecasts_cli_writes_expired_unresolved_queue_without_resolving(tmp_path):
    data_dir = tmp_path / "data" / "predictions"
    data_dir.mkdir(parents=True)
    expired = _sample_forecast()
    future = dict(expired)
    future["forecast_id"] = expired["forecast_id"].replace("2026_06_16", "2026_07_21") if "2026_06_16" in expired["forecast_id"] else expired["forecast_id"] + ":future"
    future["expires_at"] = "2026-07-21T12:00:00Z"
    (data_dir / "2026-06-15-12.json").write_text(json.dumps({"forecast_ladder": [expired, future]}, indent=2))
    (data_dir / "forecast_resolutions.json").write_text(json.dumps({"version": "forecast_resolutions_v1", "forecasts": []}, indent=2))

    script = REPO_ROOT / "scripts" / "review_forecasts.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--predictions-dir", str(data_dir),
            "--now", "2026-06-20T12:00:00Z",
            "--output", str(data_dir / "forecast_review_queue.json"),
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] == "forecast_review_queue_built"
    queue = json.loads((data_dir / "forecast_review_queue.json").read_text())
    assert queue["version"] == "forecast_review_queue_v1"
    assert queue["expired_unresolved"] == 1
    assert queue["items"][0]["forecast_id"] == expired["forecast_id"]
    assert queue["items"][0]["auto_resolution"] is False
    ledger_after = json.loads((data_dir / "forecast_resolutions.json").read_text())
    assert ledger_after["forecasts"] == [], "review queue must not mutate the resolution ledger"
