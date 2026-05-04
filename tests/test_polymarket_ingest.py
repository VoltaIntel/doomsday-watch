"""Unit tests for Polymarket cache ingestion freshness logic."""
from __future__ import annotations

from datetime import datetime, timezone

from scripts.ingest import polymarket


def test_cache_age_and_freshness_helpers():
    now = datetime(2026, 5, 4, 12, 0, tzinfo=timezone.utc)
    fresh = {"fetched_at": "2026-05-04T06:30:00Z", "markets": {"x": {}}}
    stale = {"fetched_at": "2026-05-03T00:00:00Z", "markets": {"x": {}}}

    assert round(polymarket.cache_age_hours(fresh, now=now), 1) == 5.5
    assert polymarket.cache_is_fresh(fresh, max_age_hours=12)
    assert not polymarket.cache_is_fresh(stale, max_age_hours=12)
    assert not polymarket.cache_is_fresh({"fetched_at": "bad", "markets": {"x": {}}})
    assert not polymarket.cache_is_fresh({"fetched_at": "2026-05-04T06:30:00Z", "markets": {}})


def test_refresh_cache_if_stale_uses_existing_fresh_cache(monkeypatch):
    existing = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "markets": {"x": {}}}
    monkeypatch.setattr(polymarket, "load_cache", lambda: existing)

    def fail_refresh(*args, **kwargs):  # pragma: no cover - should not run
        raise AssertionError("fresh cache should not hit network refresh")

    monkeypatch.setattr(polymarket, "refresh_cache", fail_refresh)
    assert polymarket.refresh_cache_if_stale(max_age_hours=12) is existing


def test_refresh_cache_if_stale_refreshes_old_cache(monkeypatch):
    stale = {"fetched_at": "2026-04-22T00:00:00Z", "markets": {"old": {}}}
    refreshed = {"fetched_at": "2026-05-04T00:00:00Z", "markets": {"new": {}}}
    monkeypatch.setattr(polymarket, "load_cache", lambda: stale)
    monkeypatch.setattr(polymarket, "refresh_cache", lambda **kwargs: refreshed)
    assert polymarket.refresh_cache_if_stale(max_age_hours=12) is refreshed
