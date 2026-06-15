from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from predictions import (  # noqa: E402
    brier_score,
    compute_horizon_calibration,
    generate_forecast_ladder,
)


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


def test_forecast_ladder_exposes_auditable_probability_model_components():
    forecasts = generate_forecast_ladder(
        _sample_trackers(),
        _sample_state(),
        "2026-06-15T12:00:00Z",
    )

    forecast = next(f for f in forecasts if f["horizon_label"] == "24h")
    model = forecast.get("probability_model")
    assert model, "forecast should expose auditable scoring components"
    assert model["version"] == "base_rate_evidence_v1"
    assert model["formula"].startswith("base_rate + threat_component")
    assert model["base_rate_pct"] >= 0
    assert model["threat_component_pp"] >= 0
    assert model["signal_delta_pp"] > 0
    assert model["contradiction_delta_pp"] <= 0
    assert model["final_probability_pct"] == forecast["probability"]
    assert forecast["base_rate_pct"] == model["base_rate_pct"]
    assert forecast["model_version"] == "base_rate_evidence_v1"


def test_compute_horizon_calibration_groups_resolved_forecasts_by_horizon_and_bucket():
    resolved = [
        {"schema_version": "forecast_v2", "horizon_label": "24h", "probability": 72, "outcome": True},
        {"schema_version": "forecast_v2", "horizon_label": "24h", "probability": 68, "outcome": False},
        {"schema_version": "forecast_v2", "horizon_label": "7d", "probability": 32, "resolved_outcome": True},
        {"schema_version": "legacy", "horizon_label": "24h", "probability": 10, "outcome": False},
    ]

    calibration = compute_horizon_calibration(resolved)

    assert calibration["version"] == "forecast_calibration_v1"
    assert calibration["horizons"]["24h"]["count"] == 2
    assert calibration["horizons"]["24h"]["mean_brier"] == 0.2704
    assert calibration["horizons"]["24h"]["buckets"]["70-79"]["count"] == 1
    assert calibration["horizons"]["24h"]["buckets"]["60-69"]["count"] == 1
    assert calibration["horizons"]["7d"]["count"] == 1
