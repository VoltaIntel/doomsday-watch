"""End-to-end smoke test for the DoomsdayWatch pipeline.

Runs the real pipeline against the current data/ fixture (repo state) and
checks the output dashboard contains the expected state-block marker, every
tracker id, and at least one prediction when signals are live.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TRACKER_IDS = [
    "iran_nuclear",
    "iran_conventional",
    "israel_lebanon",
    "turkey",
    "india",
    "russia",
    "china",
    "north_korea",
    "russia_ukraine",
    "pakistan_afghanistan",
]


@pytest.fixture()
def pipeline_run(tmp_path):
    """Copy repo into tmp_path, run pipeline, return (workdir, html, state)."""
    workdir = tmp_path / "nuke-watch"
    shutil.copytree(REPO_ROOT, workdir, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "*.pyc", "tests", "no_chart.png",
        "test_no_baseline.png", "verify.png",
    ))
    result = subprocess.run(
        [sys.executable, "scripts/pipeline.py"],
        cwd=workdir,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "NUKE_WATCH_AUTO_GIT": "0"},
        timeout=60,
    )
    assert result.returncode == 0, (
        f"pipeline exited non-zero: stdout={result.stdout[-500:]} "
        f"stderr={result.stderr[-500:]}"
    )
    index_html = (workdir / "index.html").read_text()
    state = json.loads((workdir / "data" / "current_state.json").read_text())
    return workdir, index_html, state


def test_pipeline_writes_state_marker(pipeline_run):
    _, html, _ = pipeline_run
    assert "const state = {" in html, "state injection marker missing"


def test_pipeline_includes_all_trackers(pipeline_run):
    _, html, _ = pipeline_run
    missing = [tid for tid in TRACKER_IDS if tid not in html]
    assert not missing, f"missing trackers in dashboard: {missing}"


def test_pipeline_produces_predictions_when_active(pipeline_run):
    _, _, state = pipeline_run
    active = [
        t for tid, t in state.get("trackers", {}).items()
        if t.get("zone") in ("elevated", "critical", "imminent")
    ]
    if not active:
        pytest.skip("no active trackers in fixture — prediction assertion skipped")
    preds = state.get("predictions", [])
    assert preds, "expected predictions to be non-empty when trackers are active"


def test_pipeline_exposes_forecast_engine_v2_ladder(pipeline_run):
    _, html, state = pipeline_run
    forecasts = state.get("forecast_ladder", [])
    assert forecasts, "expected structured forecast_v2 ladder in state"
    assert {"24h", "72h", "7d", "30d"}.issubset({f.get("horizon_label") for f in forecasts})
    first = forecasts[0]
    assert first.get("schema_version") == "forecast_v2"
    assert first.get("resolution_method") == "manual_or_source_verified"
    assert first.get("resolution_criteria", "").startswith("Resolved true if")
    assert isinstance(first.get("evidence_for"), list) and first["evidence_for"]
    assert isinstance(first.get("evidence_against"), list) and first["evidence_against"]
    assert "forecast_ladder" in html
    assert "FORECAST ENGINE V2" in html


def test_pipeline_coupling_fires(pipeline_run):
    _, _, state = pipeline_run
    boosts = [
        t.get("coupling_boost", 0)
        for t in state.get("trackers", {}).values()
        if t.get("coupling_boost")
    ]
    assert any(b > 0 for b in boosts), (
        "coupling_boost was zero for every tracker — coupling may be broken"
    )


def test_pipeline_doomsday_clock_sane(pipeline_run):
    _, _, state = pipeline_run
    ddc = state.get("doomsday_clock_minutes")
    assert ddc is None or (isinstance(ddc, (int, float)) and 0 <= ddc <= 10), (
        f"doomsday_clock_minutes={ddc} is outside the plausible 0-10 window"
    )


def test_pipeline_lifetime_stats_written(pipeline_run):
    workdir, _, _ = pipeline_run
    stats = json.loads(
        (workdir / "data" / "predictions" / "lifetime_stats.json").read_text()
    )
    assert "total_evaluated" in stats
    assert "sum_brier" in stats
    assert stats["total_evaluated"] >= 0


def test_dashboard_exposes_probability_attribution_and_watch_triggers(pipeline_run):
    _, html, state = pipeline_run
    tracker = next(t for t in state["dashboard_trackers"] if t["id"] == "iran_conventional")
    attribution = tracker.get("attribution")
    assert attribution, "tracker cards should expose probability attribution"
    assert attribution["base_rate"] >= 0
    assert "signal_delta" in attribution
    assert "coupling_boost" in attribution
    assert attribution["final_probability"] == tracker["prob"]
    assert tracker.get("watch_triggers", {}).get("up"), "missing upward watch triggers"
    assert tracker.get("watch_triggers", {}).get("down"), "missing downward watch triggers"
    assert "WHY THIS MOVED" in html
    assert "NEXT WATCH" in html


def test_dashboard_exposes_evidence_quality_and_polymarket_staleness(pipeline_run):
    _, html, state = pipeline_run
    tracker = next(t for t in state["dashboard_trackers"] if t["id"] == "iran_conventional")
    quality = tracker.get("evidence_quality")
    assert quality, "tracker cards should expose evidence quality"
    assert quality["label"] in {"HIGH", "MEDIUM", "LOW"}
    assert "source_count" in quality
    assert "newest_signal_age_hours" in quality
    pm = state.get("polymarket", {})
    assert "stale" in pm, "polymarket payload should include staleness flag"
    assert "age_hours" in pm, "polymarket payload should include cache age"
    assert "EVIDENCE" in html
    assert "PM CACHE" in html
