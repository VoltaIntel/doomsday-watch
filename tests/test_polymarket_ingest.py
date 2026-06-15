"""Unit tests for Polymarket cache ingestion freshness logic."""
from __future__ import annotations

from datetime import datetime, timezone

from scripts.ingest import polymarket


def test_cache_age_and_freshness_helpers():
    now = datetime(2026, 5, 4, 12, 0, tzinfo=timezone.utc)
    fixed_fresh = {"fetched_at": "2026-05-04T06:30:00Z", "markets": {"x": {}}}
    fresh = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "markets": {"x": {}}}
    stale = {"fetched_at": "2026-05-03T00:00:00Z", "markets": {"x": {}}}

    age = polymarket.cache_age_hours(fixed_fresh, now=now)
    assert age is not None
    assert round(age, 1) == 5.5
    assert polymarket.cache_is_fresh(fresh, max_age_hours=12)
    assert polymarket.cache_is_fresh(fresh, max_age_hours=12, slugs=["x"])
    assert not polymarket.cache_is_fresh(fresh, max_age_hours=12, slugs=["missing"])
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


def test_refresh_cache_if_stale_refreshes_when_requested_slug_missing(monkeypatch):
    existing = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "markets": {"x": {}}}
    refreshed = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "markets": {"mapped": {}}}
    seen = {}
    monkeypatch.setattr(polymarket, "load_cache", lambda: existing)

    def refresh_cache(**kwargs):
        seen.update(kwargs)
        return refreshed

    monkeypatch.setattr(polymarket, "refresh_cache", refresh_cache)
    assert polymarket.refresh_cache_if_stale(slugs=["mapped"], max_age_hours=12) is refreshed
    assert seen["slugs"] == ["mapped"]


def test_refresh_cache_if_stale_refreshes_old_cache(monkeypatch):
    stale = {"fetched_at": "2026-04-22T00:00:00Z", "markets": {"old": {}}}
    refreshed = {"fetched_at": "2026-05-04T00:00:00Z", "markets": {"new": {}}}
    monkeypatch.setattr(polymarket, "load_cache", lambda: stale)
    monkeypatch.setattr(polymarket, "refresh_cache", lambda **kwargs: refreshed)
    assert polymarket.refresh_cache_if_stale(max_age_hours=12) is refreshed


def test_build_cache_fetches_requested_slugs_directly(monkeypatch):
    def fetch_slug(slug):
        if slug == "mapped":
            return {
                "slug": "mapped",
                "question": "Mapped geopolitical market?",
                "outcomePrices": '["0.25", "0.75"]',
                "volume24hr": "1234.5",
                "active": True,
                "closed": False,
            }
        return None

    def fail_page_fetch(*args, **kwargs):  # pragma: no cover - direct slug path should be used
        raise AssertionError("requested slugs must not depend on capped active-market pages")

    monkeypatch.setattr(polymarket, "_fetch_slug", fetch_slug)
    monkeypatch.setattr(polymarket, "fetch_active_markets", fail_page_fetch)
    cache = polymarket.build_cache(slugs=["mapped", "missing"])
    assert set(cache["markets"]) == {"mapped"}
    assert cache["markets"]["mapped"]["yes_price"] == 0.25
