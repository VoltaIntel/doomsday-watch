"""Unit tests for scripts.scoring.polymarket_check — pure-function coverage.

Exercises the hazard translator, divergence classifier, and end-to-end
check_all() against synthetic caches so tests do not depend on network.
"""
from __future__ import annotations

import pytest

from scripts.scoring.polymarket_check import (
    hazard_translate,
    _classify_divergence,
    _tracker_implied,
    check_all,
    DIVERGENCE_PP,
    DRIFT_PP,
)


def test_hazard_translate_boundaries():
    assert hazard_translate(0.0, 100) == 0.0
    assert hazard_translate(1.0, 100) == 1.0
    assert hazard_translate(-1, 50) == 0.0
    assert hazard_translate(2.0, 50) == 1.0


def test_hazard_translate_monotonic():
    a = hazard_translate(0.5, 50, 1)
    b = hazard_translate(0.5, 200, 1)
    assert a > b > 0


def test_classify_divergence_aligned():
    d = _classify_divergence(20.0, 21.0, 0.3)
    assert d["flag"] == "aligned"
    assert d["color"] == "green"
    assert abs(d["delta_pp"] - (-1.0)) < 1e-6


def test_classify_divergence_drift():
    d = _classify_divergence(30.0, 22.0, 0.3)
    assert d["flag"] == "drift"
    assert d["color"] == "yellow"
    assert d["abs_delta_pp"] >= DRIFT_PP


def test_classify_divergence_red():
    d = _classify_divergence(50.0, 20.0, 0.3)
    assert d["flag"] == "divergence"
    assert d["color"] == "red"
    assert d["abs_delta_pp"] >= DIVERGENCE_PP


def test_classify_divergence_critical_sanity_floor():
    d = _classify_divergence(40.0, 0.5, 0.01)
    assert d["flag"] == "critical"


def test_tracker_implied_with_invert():
    mapping = [
        {"slug": "ceasefire", "weight": 1.0, "horizon_days": 60, "invert": True},
    ]
    cache = {"ceasefire": {"yes_price": 0.8, "volume_24h": 500_000, "question": "?"}}
    implied = _tracker_implied("fake_tracker", mapping, cache)
    assert implied is not None
    assert abs(implied["implied_raw"] - 0.2) < 1e-6


def test_tracker_implied_no_markets():
    implied = _tracker_implied(
        "x",
        [{"slug": "missing", "weight": 1.0, "horizon_days": 60, "invert": False}],
        {},
    )
    assert implied is None


def test_check_all_returns_banner_when_divergent():
    cache = {
        "fetched_at": "2026-04-22T00:00:00Z",
        "markets": {
            "iran-nuke-before-2027": {
                "slug": "iran-nuke-before-2027",
                "yes_price": 0.04,
                "volume_24h": 1_000_000,
                "question": "Iran nuke before 2027?",
            }
        },
    }
    mapping = {
        "iran_nuclear": [
            {"slug": "iran-nuke-before-2027", "weight": 1.0, "horizon_days": 250, "invert": False},
        ]
    }
    state = {"trackers": {"iran_nuclear": {"current_probability_with_coupling": 45.0}}}
    out = check_all(cache=cache, mapping=mapping, state=state, append_log=False)
    comp = out["comparisons"]["iran_nuclear"]
    assert comp["status"] == "ok"
    assert comp["flag"] in ("divergence", "critical")
    assert out["banner"]["any_divergence"] is True


def test_check_all_skips_meta_and_empty_entries():
    mapping = {
        "_meta": {"ignore": True},
        "empty": [],
        "valid": [{"slug": "x", "weight": 1.0, "horizon_days": 1, "invert": False}],
    }
    out = check_all(cache={"markets": {}}, mapping=mapping, state={}, append_log=False)
    assert "_meta" not in out["comparisons"]
    assert "empty" not in out["comparisons"]
    assert out["comparisons"]["valid"]["status"] == "no_market"
