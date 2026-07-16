from scripts.signals import (
    extract_signals_from_notes,
    find_matching_signals,
    merge_news_signals_into_state,
)


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


def test_extract_signals_from_notes_rejects_signal_not_configured_for_tracker():
    state = {
        "zones": {
            "yemen_red_sea": {
                "notes": "The airport was hit by strikes despite ceasefire and ballistic missiles were fired."
            }
        },
        "trackers": {"yemen_red_sea": {"active_signals": []}},
    }
    signal_weights = {("yemen_red_sea", "ceasefire_violation"): 6}

    extract_signals_from_notes(state, signal_weights)

    assert state["trackers"]["yemen_red_sea"]["active_signals"] == ["ceasefire_violation"]


def test_extract_signals_from_notes_ignores_locally_negated_keywords():
    state = {
        "zones": {
            "north_korea": {
                "notes": (
                    "No credible fresh missile launch, nuclear test, or abrupt posture "
                    "change was found in the focused scan."
                )
            }
        },
        "trackers": {"north_korea": {"active_signals": []}},
    }
    signal_weights = {
        ("north_korea", "missile_range_test"): 6,
        ("north_korea", "nuclear_test"): 12,
    }

    extract_signals_from_notes(state, signal_weights)

    assert state["trackers"]["north_korea"]["active_signals"] == []


def test_find_matching_signals_ignores_negated_exact_mentions():
    cfg = {
        "trackers": {
            "north_korea": {
                "signals": {
                    "missile_range_test": {"weight": 6},
                    "nuclear_test": {"weight": 12},
                }
            }
        }
    }
    signal_weights = {
        ("north_korea", "missile_range_test"): 6,
        ("north_korea", "nuclear_test"): 12,
    }

    matched = find_matching_signals(
        "No credible fresh missile range test or nuclear test was found.",
        "north_korea",
        cfg,
        signal_weights,
        {},
    )

    assert matched == []


def test_find_matching_signals_preserves_positive_exact_mentions():
    cfg = {
        "trackers": {
            "north_korea": {
                "signals": {"nuclear_test": {"weight": 12}}
            }
        }
    }

    matched = find_matching_signals(
        "Officials confirmed a nuclear test overnight.",
        "north_korea",
        cfg,
        {("north_korea", "nuclear_test"): 12},
        {},
    )

    assert [signal["name"] for signal in matched] == ["nuclear_test"]
