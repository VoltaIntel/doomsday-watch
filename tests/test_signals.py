from scripts.signals import (
    calc_confidence,
    calc_severity,
    classify_source_category,
    enrich_news,
    extract_signals_from_notes,
    find_matching_signals,
    merge_news_signals_into_state,
)


# Representative record in the legacy `latest_news` schema that the cron
# writer still emits (title/summary/tracker/source/timestamp).
LEGACY_NEWS_ITEM = {
    "timestamp": "2026-08-09T18:05:51Z",
    "source_date": "2026-08-09",
    "title": "Syria-Russia deal reorganizes Tartous and Hmeimim bases",
    "summary": (
        "AP and Reuters report Syria will assume civil control of Hmeimim "
        "airport and Tartous's commercial berth while the military facilities "
        "transition into joint training centers."
    ),
    "source": "Associated Press; Reuters",
    "url": "https://apnews.com/article/syria-russia-latakia-tartus-bases",
    "tracker": "russia",
    "importance": "high",
}

# Record in the current dashboard/enrichment schema.
CURRENT_NEWS_ITEM = {
    "zone": "north_korea",
    "time": "LIVE",
    "text": "DPRK signal update: missile activity elevated.",
    "headline": "Signal update: missile activity",
    "impact": "up",
    "sources": ["NUCLEAR ESCALATION WATCH"],
}


def _enrich(raw_news):
    return enrich_news(
        raw_news,
        classify_credibility=lambda s: ("1_wire", 3, "wire service"),
        classify_category=classify_source_category,
        find_matching_signals_fn=lambda text, zone, tier: [],
        calc_confidence_fn=calc_confidence,
        calc_severity_fn=calc_severity,
    )


def test_enrich_news_normalizes_legacy_title_summary_tracker():
    enriched = _enrich([dict(LEGACY_NEWS_ITEM)])

    assert enriched[0]["headline"] == LEGACY_NEWS_ITEM["title"]
    assert enriched[0]["text"] == LEGACY_NEWS_ITEM["summary"]
    assert enriched[0]["zone"] == "russia"


def test_enrich_news_keeps_legacy_source_and_timestamp_visible():
    enriched = _enrich([dict(LEGACY_NEWS_ITEM)])

    assert any("Associated Press" in s for s in enriched[0]["sources"])
    assert enriched[0]["time"]


def test_enrich_news_preserves_current_schema_item_alongside_legacy_item():
    enriched = _enrich([dict(LEGACY_NEWS_ITEM), dict(CURRENT_NEWS_ITEM)])

    current = enriched[1]
    assert current["headline"] == CURRENT_NEWS_ITEM["headline"]
    assert current["text"] == CURRENT_NEWS_ITEM["text"]
    assert current["zone"] == CURRENT_NEWS_ITEM["zone"]
    assert current["time"] == CURRENT_NEWS_ITEM["time"]
    assert current["sources"] == CURRENT_NEWS_ITEM["sources"]
    assert current["impact"] == CURRENT_NEWS_ITEM["impact"]


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
