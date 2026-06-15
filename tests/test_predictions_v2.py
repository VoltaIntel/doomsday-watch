from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from predictions import brier_score, generate_forecast_ladder  # noqa: E402


def _sample_trackers():
    return [
        {
            "id": "iran_nuclear",
            "name": "IRAN NUCLEAR",
            "prob": 70,
            "trend": "falling",
            "zone": "imminent",
            "signals": [
                {"name": "IAEA access denied", "original_weight": 8, "positive": False},
                {"name": "diplomacy active", "original_weight": 6, "positive": True},
            ],
        },
        {
            "id": "turkey",
            "name": "TURKEY-NATO",
            "prob": 8,
            "trend": "stable",
            "zone": "deterrent",
            "signals": [],
        },
    ]


def _sample_state():
    return {
        "latest_news": [
            {
                "headline": "IAEA says access dispute continues while diplomacy remains active",
                "confidence": "confirmed",
                "sources": ["Reuters", "IAEA"],
                "zone": "iran_nuclear",
            }
        ],
        "trackers": {
            "iran_nuclear": {
                "active_signals": ["iaea_access_denied", "diplomacy_active"],
                "notes": "60 percent enrichment risk active, but talks continue.",
            }
        },
    }


def test_generate_forecast_ladder_emits_structured_multi_horizon_forecasts():
    forecasts = generate_forecast_ladder(
        _sample_trackers(),
        _sample_state(),
        "2026-06-15T12:00:00Z",
    )

    assert forecasts, "expected at least one structured forecast"
    horizon_labels = {f["horizon_label"] for f in forecasts}
    assert {"24h", "72h", "7d", "30d"}.issubset(horizon_labels)

    forecast = forecasts[0]
    assert forecast["schema_version"] == "forecast_v2"
    assert forecast["forecast_id"]
    assert forecast["tracker_id"] == "iran_nuclear"
    assert forecast["event_type"]
    assert 0 <= forecast["probability"] <= 100
    assert forecast["confidence_label"] in {"LOW", "MEDIUM", "HIGH"}
    assert forecast["resolution_criteria"].startswith("Resolved true if")
    assert forecast["resolution_method"] == "manual_or_source_verified"
    assert forecast["evaluation_status"] == "pending"
    assert forecast["evidence_for"], "forecast should expose escalation evidence"
    assert forecast["evidence_against"], "forecast should expose contradiction/de-escalation evidence"


def test_generate_forecast_ladder_prioritizes_active_risk_over_deterrent_noise():
    forecasts = generate_forecast_ladder(
        _sample_trackers(),
        _sample_state(),
        "2026-06-15T12:00:00Z",
    )

    tracker_ids = [f["tracker_id"] for f in forecasts[:4]]
    assert tracker_ids == ["iran_nuclear"] * 4
    assert all(f["tracker_id"] != "turkey" for f in forecasts[:4])


def test_brier_score_uses_probability_not_binary_correctness():
    assert brier_score(75, True) == 0.0625
    assert brier_score(75, False) == 0.5625
    assert brier_score(0, False) == 0.0
    assert brier_score(100, True) == 0.0
