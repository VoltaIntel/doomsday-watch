"""Unit tests for `sanitize_public_meta` in scripts/pipeline.py.

`data/current_state.json` is force-published to GitHub Pages, so `_meta` is
viewer-facing. These tests pin the honest public distinction between a run
where primary web search succeeded and a degraded fallback-only run, without
leaking vendor names, API errors, credentials, URLs, or status codes.

pipeline.py has no __main__ guard (it chdirs and reads data/ at import time),
so we exec only the definition prefix that precedes the script body.
"""
from __future__ import annotations

from pathlib import Path

import pytest


PIPELINE = Path(__file__).resolve().parent.parent / "scripts" / "pipeline.py"
BODY_MARKER = "ROOT = Path(__file__).resolve().parent.parent"

SANCTIONED_SUCCESS_ENGINE = "web_search_plus_public_safe_multi_source_fallback"
FALLBACK_ENGINE = "public_safe_multi_source_fallback"
CLEAN_ENGINE = "public_safe_multi_source"


@pytest.fixture(scope="module")
def pipeline_ns():
    """Exec pipeline.py's definitions without running its script body."""
    source = PIPELINE.read_text()
    head, sep, _ = source.partition(BODY_MARKER)
    assert sep, f"body marker not found in {PIPELINE}"
    ns = {"__file__": str(PIPELINE), "__name__": "pipeline_defs"}
    exec(compile(head, str(PIPELINE), "exec"), ns)
    return ns


@pytest.fixture
def sanitize(pipeline_ns):
    return pipeline_ns["sanitize_public_meta"]


def _state(web_search_status=None, **meta_extra):
    meta = {
        # A prior degraded run leaves this sticky in the state file.
        "source_limitation": (
            "Source mix: official releases, reputable public reporting. "
            "Upstream source coverage was degraded in this run."
        ),
        "search_engine": FALLBACK_ENGINE,
    }
    meta.update(meta_extra)
    if web_search_status is not None:
        meta["source_fallback_detail"] = {"web_search_status": web_search_status}
    return {"_meta": meta}


def test_successful_web_search_sets_success_engine_label(sanitize):
    meta = sanitize(_state("successful: 16 grouped queries"))["_meta"]
    assert meta["search_engine"] == SANCTIONED_SUCCESS_ENGINE


def test_successful_web_search_publishes_success_source_limitation(sanitize):
    meta = sanitize(_state("successful: 16 grouped queries"))["_meta"]
    text = meta["source_limitation"].lower()
    assert "primary web search" in text and "succeed" in text
    assert "corroborat" in text
    assert "degraded" not in text


def test_successful_web_search_notes_sparse_results_are_not_calm(sanitize):
    meta = sanitize(_state("successful: 16 grouped queries"))["_meta"]
    text = meta["source_limitation"].lower()
    assert "sparse" in text and "stale" in text
    assert "calm" in text


def test_successful_status_match_is_case_insensitive(sanitize):
    meta = sanitize(_state("  SUCCESSFUL (16/16 queries)  "))["_meta"]
    assert meta["search_engine"] == SANCTIONED_SUCCESS_ENGINE


def test_success_path_leaks_no_vendor_error_url_or_status_code(sanitize):
    dirty = "successful via tavily key sk-abc123 https://api.tavily.com http 403 forbidden"
    meta = sanitize(_state(dirty))["_meta"]
    published = " ".join(
        str(meta.get(k, "")) for k in ("source_limitation", "search_engine")
    ).lower()
    for token in ("tavily", "sk-abc123", "http", "403", "forbidden", "://"):
        assert token not in published, f"leaked {token!r} into public meta"


def test_failed_web_search_preserves_degraded_fallback_behavior(sanitize):
    meta = sanitize(_state("failed: upstream error 432"))["_meta"]
    assert meta["search_engine"] == FALLBACK_ENGINE
    text = meta["source_limitation"].lower()
    assert "degraded" in text
    assert "432" not in text and "failed" not in text


def test_unsuccessful_prefix_is_not_treated_as_success(sanitize):
    meta = sanitize(_state("unsuccessful: no primary results"))["_meta"]
    assert meta["search_engine"] == FALLBACK_ENGINE


def test_missing_web_search_status_preserves_existing_fallback_behavior(sanitize):
    meta = sanitize(_state())["_meta"]
    assert meta["search_engine"] == FALLBACK_ENGINE


def test_missing_web_search_status_with_empty_meta_stays_clean(sanitize):
    meta = sanitize({"_meta": {}})["_meta"]
    assert meta["search_engine"] == CLEAN_ENGINE


def test_non_dict_source_fallback_detail_is_ignored(sanitize):
    state = _state()
    state["_meta"]["source_fallback_detail"] = "successful"
    meta = sanitize(state)["_meta"]
    assert meta["search_engine"] == FALLBACK_ENGINE


def test_non_string_web_search_status_is_ignored(sanitize):
    meta = sanitize(_state(True))["_meta"]
    assert meta["search_engine"] == FALLBACK_ENGINE


def test_official_source_probe_scrubbing_still_applies_on_success_path(sanitize):
    state = _state("successful: 16 grouped queries")
    state["_meta"]["official_source_probe"] = {
        "iaea": {"ok": False, "url": "https://iaea.org/x", "error": "HTTPError 403"},
    }
    probe = sanitize(state)["_meta"]["official_source_probe"]
    assert probe["iaea"]["ok"] is False
    assert "error" not in probe["iaea"]
    assert "403" not in str(probe["iaea"]["source"])
