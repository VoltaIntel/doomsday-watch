from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from predictions import (  # noqa: E402
    brier_score,
    build_forecast_review_queue,
    compute_horizon_calibration,
    generate_forecast_ladder,
    resolve_forecast,
    summarize_forecast_resolution_ledger,
    upsert_forecast_resolution,
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


def test_resolve_forecast_requires_source_evidence_and_records_brier_score():
    forecast = generate_forecast_ladder(
        _sample_trackers(),
        _sample_state(),
        "2026-06-15T12:00:00Z",
    )[0]

    try:
        resolve_forecast(
            forecast,
            outcome=True,
            resolved_at="2026-06-15T18:00:00Z",
            evidence=[],
        )
    except ValueError as exc:
        assert "evidence" in str(exc).lower()
    else:
        raise AssertionError("resolving a forecast without source evidence should fail")

    resolved = resolve_forecast(
        forecast,
        outcome=True,
        resolved_at="2026-06-15T18:00:00Z",
        evidence=[{
            "title": "IAEA confirms emergency board action",
            "url": "https://www.iaea.org/news/example",
            "source": "IAEA",
        }],
        resolved_by="operator",
        notes="Verified against IAEA public release.",
    )

    assert resolved["schema_version"] == "forecast_v2"
    assert resolved["evaluation_status"] == "resolved"
    assert resolved["resolved_outcome"] is True
    assert resolved["outcome"] is True
    assert resolved["resolved_at"] == "2026-06-15T18:00:00Z"
    assert resolved["resolved_by"] == "operator"
    assert resolved["resolution_evidence"][0]["source"] == "IAEA"
    assert resolved["brier"] == brier_score(forecast["probability"], True)


def test_upsert_forecast_resolution_dedupes_by_forecast_id_and_feeds_calibration():
    forecast = generate_forecast_ladder(
        _sample_trackers(),
        _sample_state(),
        "2026-06-15T12:00:00Z",
    )[0]
    resolved_true = resolve_forecast(
        forecast,
        outcome=True,
        resolved_at="2026-06-15T18:00:00Z",
        evidence=[{"title": "Wire confirms event", "url": "https://reuters.com/example", "source": "Reuters"}],
    )
    resolved_false = resolve_forecast(
        forecast,
        outcome=False,
        resolved_at="2026-06-15T19:00:00Z",
        evidence=[{"title": "Correction: event did not occur", "url": "https://reuters.com/correction", "source": "Reuters"}],
    )

    ledger = upsert_forecast_resolution({"version": "forecast_resolutions_v1", "forecasts": []}, resolved_true)
    ledger = upsert_forecast_resolution(ledger, resolved_false)

    assert ledger["version"] == "forecast_resolutions_v1"
    assert ledger["updated_at"] == "2026-06-15T19:00:00Z"
    assert len(ledger["forecasts"]) == 1
    assert ledger["forecasts"][0]["resolved_outcome"] is False

    calibration = compute_horizon_calibration(ledger["forecasts"])
    horizon = forecast["horizon_label"]
    assert calibration["horizons"][horizon]["count"] == 1
    assert calibration["horizons"][horizon]["mean_brier"] == brier_score(forecast["probability"], False)


def test_summarize_forecast_resolution_ledger_counts_resolved_and_current_pending():
    forecasts = generate_forecast_ladder(
        _sample_trackers(),
        _sample_state(),
        "2026-06-15T12:00:00Z",
    )
    resolved = resolve_forecast(
        forecasts[0],
        outcome=True,
        resolved_at="2026-06-15T18:00:00Z",
        evidence=[{"title": "IAEA confirms event", "url": "https://www.iaea.org/news/example", "source": "IAEA"}],
    )
    ledger = upsert_forecast_resolution({"version": "forecast_resolutions_v1", "forecasts": []}, resolved)

    status = summarize_forecast_resolution_ledger(ledger, forecasts)

    assert status["version"] == "forecast_resolution_status_v1"
    assert status["total_resolved"] == 1
    assert status["current_resolved"] == 1
    assert status["current_pending"] == len(forecasts) - 1
    assert status["last_resolved_at"] == "2026-06-15T18:00:00Z"
    assert status["by_horizon"][forecasts[0]["horizon_label"]]["resolved"] == 1


def test_build_forecast_review_queue_lists_only_expired_unresolved_forecasts():
    old_forecasts = generate_forecast_ladder(
        _sample_trackers(),
        _sample_state(),
        "2026-06-15T12:00:00Z",
    )
    current_forecasts = generate_forecast_ladder(
        _sample_trackers(),
        _sample_state(),
        "2026-07-20T12:00:00Z",
    )
    resolved = resolve_forecast(
        old_forecasts[0],
        outcome=False,
        resolved_at="2026-06-16T18:00:00Z",
        evidence=[{"title": "No qualifying event before expiry", "url": "https://reuters.com/example", "source": "Reuters"}],
    )
    ledger = upsert_forecast_resolution({"version": "forecast_resolutions_v1", "forecasts": []}, resolved)

    queue = build_forecast_review_queue(
        old_forecasts + current_forecasts,
        ledger,
        "2026-07-20T12:00:00Z",
        limit=50,
    )

    assert queue["version"] == "forecast_review_queue_v1"
    assert queue["generated_at"] == "2026-07-20T12:00:00Z"
    queued_ids = {item["forecast_id"] for item in queue["items"]}
    assert old_forecasts[0]["forecast_id"] not in queued_ids, "resolved forecasts should not re-enter review"
    assert all(f["forecast_id"] not in queued_ids for f in current_forecasts), "unexpired current forecasts should not enter review"
    assert queued_ids, "expected expired unresolved forecasts to require operator review"
    first = queue["items"][0]
    assert first["review_status"] == "needs_manual_resolution"
    assert first["resolution_evidence_required"] is True
    assert first["auto_resolution"] is False
    assert first["age_hours"] > 0
    assert first["resolution_command"].startswith("python3 scripts/resolve_forecast.py --forecast-id")
    assert first["suggested_queries"], "review queue should provide source-search prompts, not guesses"
