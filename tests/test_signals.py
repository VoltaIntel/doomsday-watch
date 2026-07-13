from scripts.signals import merge_news_signals_into_state


def test_merge_news_signals_rejects_signal_not_configured_for_tracker():
    state = {"trackers": {"yemen_red_sea": {"active_signals": []}}}
    enriched_news = [
        {
            "zone": "yemen_red_sea",
            "signals": [
                {"name": "infrastructure_strike", "weight": 5, "duplicate": False},
                {"name": "missile_range_test", "weight": 6, "duplicate": False},
            ],
        }
    ]
    signal_weights = {("yemen_red_sea", "infrastructure_strike"): 5}
    timeline = {}
    confirmed = []

    def get_timeline_details(key, create=False):
        timestamp = timeline.setdefault(key, "2026-07-13T18:00:00Z") if create else timeline.get(key)
        return None, timestamp, None

    merge_news_signals_into_state(
        enriched_news,
        state,
        signal_weights,
        apply_temporal_decay_fn=lambda weight, activated_at: weight,
        get_timeline_details_fn=get_timeline_details,
        confirm_signal_fn=lambda tracker_id, signal_name: confirmed.append((tracker_id, signal_name)),
        now_iso="2026-07-13T18:00:00Z",
    )

    assert state["trackers"]["yemen_red_sea"]["active_signals"] == ["infrastructure_strike"]
    assert confirmed == [("yemen_red_sea", "infrastructure_strike")]
    assert "yemen_red_sea:missile_range_test" not in timeline
