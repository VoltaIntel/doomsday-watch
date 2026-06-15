#!/usr/bin/env python3
"""
predictions.py — Prediction identity, deduplication, merging, generation,
and evaluation.

Extracted from pipeline.py for DoomsdayWatch modular architecture.
"""

from datetime import datetime, timedelta, timezone
import re


# ── Structured Forecasts v2 ──────────────────────────────────────────────────

FORECAST_HORIZONS = (
    ("24h", 24, 0.55),
    ("72h", 72, 0.70),
    ("7d", 24 * 7, 0.85),
    ("30d", 24 * 30, 0.95),
)

FORECAST_MODEL_VERSION = "base_rate_evidence_v1"

EVENT_BASE_RATES_24H = {
    "nuclear_threshold": 4,
    "gulf_conventional_escalation": 12,
    "border_war_escalation": 18,
    "nato_war_escalation": 6,
    "taiwan_pressure_escalation": 5,
    "dprk_military_escalation": 8,
    "border_conflict_escalation": 14,
    "de_escalation_continuation": 18,
    "escalation_watch": 10,
}

HORIZON_BASE_MULTIPLIER = {"24h": 1.0, "72h": 1.8, "7d": 2.7, "30d": 4.5}
HORIZON_THREAT_WEIGHT = {"24h": 0.18, "72h": 0.24, "7d": 0.30, "30d": 0.36}

TIER1_SOURCES = {
    "reuters", "associated press", "ap", "afp", "bbc", "iaea", "un", "united nations",
    "nato", "white house", "state department", "pentagon",
}
TIER2_SOURCES = {"al jazeera", "cbs", "nbc", "abc", "cnn", "dw", "france 24", "the guardian", "financial times"}

RESOLUTION_CRITERIA = {
    "iran_nuclear": "Resolved true if a verified IAEA, official government, Reuters/AP/AFP/BBC-level report confirms a new nuclear threshold event, enrichment/access escalation, strike, or sanctions/snapback trigger before expiry.",
    "iran_conventional": "Resolved true if verified wire/official reporting confirms new direct Iranian conventional strike, Gulf shipping attack, Strait closure/disruption, or US/Israeli regional military exchange before expiry.",
    "israel_lebanon": "Resolved true if verified wire/official reporting confirms additional Israel-Hezbollah strikes, ground expansion, significant retaliation, or ceasefire collapse before expiry.",
    "russia": "Resolved true if verified wire/official reporting confirms new Russia-NATO direct incident, nuclear deployment signal, unscheduled nuclear exercise, or explicit NATO-targeted escalation before expiry.",
    "russia_ukraine": "Resolved true if verified wire/official reporting confirms a material battlefield, strike, sabotage, nuclear-rhetoric, or negotiation-shift event before expiry.",
    "china": "Resolved true if verified wire/official reporting confirms PLA live-fire/blockade activity, major Taiwan-zone air/naval surge, cable/cyber disruption tied to pressure, or emergency political response before expiry.",
    "north_korea": "Resolved true if verified wire/official reporting confirms a missile/device test, nuclear-status escalation, border clash, or direct military provocation before expiry.",
    "india": "Resolved true if verified wire/official reporting confirms a new India-Pakistan cross-border clash, strike, major mobilization, or nuclear/missile escalation signal before expiry.",
    "pakistan_afghanistan": "Resolved true if verified wire/official reporting confirms a new Afghanistan-Pakistan border clash, cross-border strike, airstrike, or major diplomatic rupture before expiry.",
}

DEESCALATION_TERMS = (
    "ceasefire", "deal", "diplomacy", "talk", "negotiation", "stand-down",
    "de-escal", "reopen", "withdraw", "inspection", "access restored",
)


def _parse_utc(ts):
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return datetime.now(timezone.utc)


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "_", str(text).lower()).strip("_") or "forecast"


def _clamp_probability(value):
    return int(round(max(0.0, min(100.0, float(value)))))


def brier_score(probability_pct, outcome):
    """Return binary-event Brier score using the stated probability.

    `outcome` may be bool or 0/1. The returned value is rounded for stable JSON
    and test output.
    """
    p = max(0.0, min(1.0, float(probability_pct) / 100.0))
    o = 1.0 if bool(outcome) else 0.0
    return round((p - o) ** 2, 4)


def _event_base_rate(event_type, horizon_label):
    base = EVENT_BASE_RATES_24H.get(event_type, EVENT_BASE_RATES_24H["escalation_watch"])
    return round(min(60.0, base * HORIZON_BASE_MULTIPLIER.get(horizon_label, 1.0)), 2)


def _source_quality_delta(tracker, state):
    tid = tracker.get("id")
    delta = 0.0
    matched_sources = []
    for news in state.get("latest_news", []) or []:
        if news.get("zone") not in (None, "", tid, tracker.get("name")):
            continue
        for source in news.get("sources", []) or []:
            source_l = str(source).lower()
            matched_sources.append(str(source))
            if any(s in source_l for s in TIER1_SOURCES):
                delta += 3.0
            elif any(s in source_l for s in TIER2_SOURCES):
                delta += 1.5
            else:
                delta += 0.5
    return round(min(10.0, delta), 2), matched_sources[:6]


def _signal_delta(tracker, state, evidence_for, evidence_against):
    tid = tracker.get("id")
    delta = 0.0
    for sig in tracker.get("signals", []) or []:
        if not isinstance(sig, dict):
            delta += 1.0
            continue
        weight = sig.get("original_weight", sig.get("weight", 0))
        try:
            weight = float(weight)
        except Exception:
            weight = 1.0
        delta += (-0.35 * abs(weight)) if sig.get("positive") else (0.65 * abs(weight))
    for sig in state.get("trackers", {}).get(tid, {}).get("active_signals", []) or []:
        label = str(sig).lower().replace("_", " ")
        delta += -2.0 if any(term in label for term in DEESCALATION_TERMS) else 2.5
    if evidence_for and not evidence_for[0].startswith("No discrete"):
        delta += min(5.0, len(evidence_for) * 1.25)
    if evidence_against and not evidence_against[0].startswith("No clear"):
        delta -= min(6.0, len(evidence_against) * 1.5)
    return round(max(-15.0, min(20.0, delta)), 2)


def build_probability_model(tracker, state, event_type, horizon_label, *, evidence_for=None, evidence_against=None):
    """Build auditable base-rate + evidence model for one forecast."""
    evidence_for = evidence_for or []
    evidence_against = evidence_against or []
    threat_score = float(tracker.get("prob", 0) or 0)
    base_rate = _event_base_rate(event_type, horizon_label)
    threat_component = round(threat_score * HORIZON_THREAT_WEIGHT.get(horizon_label, 0.18), 2)
    signal_delta = _signal_delta(tracker, state, evidence_for, evidence_against)
    trend_delta = {"rising": 5.0, "stable": 0.0, "falling": -6.0}.get(tracker.get("trend"), 0.0)
    source_delta, matched_sources = _source_quality_delta(tracker, state)
    contradiction_delta = 0.0
    if evidence_against and not evidence_against[0].startswith("No clear"):
        contradiction_delta = round(-min(10.0, len(evidence_against) * 2.0), 2)
    raw = base_rate + threat_component + signal_delta + trend_delta + source_delta + contradiction_delta
    final_probability = _clamp_probability(raw)
    return {
        "version": FORECAST_MODEL_VERSION,
        "formula": "base_rate + threat_component + signal_delta + trend_delta + source_delta + contradiction_delta",
        "base_rate_pct": base_rate,
        "threat_score_pct": round(threat_score, 2),
        "threat_component_pp": threat_component,
        "signal_delta_pp": signal_delta,
        "trend_delta_pp": trend_delta,
        "source_delta_pp": source_delta,
        "contradiction_delta_pp": contradiction_delta,
        "raw_probability_pct": round(raw, 2),
        "final_probability_pct": final_probability,
        "matched_sources": matched_sources,
    }


def _calibration_bucket(probability_pct):
    p = int(max(0, min(100, float(probability_pct))))
    low = min(90, (p // 10) * 10)
    high = 100 if low == 90 else low + 9
    return f"{low}-{high}"


def compute_horizon_calibration(forecasts):
    """Group resolved forecast_v2 records by horizon and 10pp probability bucket."""
    horizons = {}
    for forecast in forecasts or []:
        if forecast.get("schema_version") != "forecast_v2":
            continue
        if "outcome" in forecast:
            outcome = forecast.get("outcome")
        elif "resolved_outcome" in forecast:
            outcome = forecast.get("resolved_outcome")
        else:
            continue
        horizon = forecast.get("horizon_label") or "unknown"
        probability = float(forecast.get("probability", 0) or 0)
        brier = brier_score(probability, outcome)
        bucket = _calibration_bucket(probability)
        h = horizons.setdefault(horizon, {"count": 0, "sum_brier": 0.0, "mean_brier": None, "buckets": {}})
        h["count"] += 1
        h["sum_brier"] += brier
        b = h["buckets"].setdefault(bucket, {"count": 0, "sum_brier": 0.0, "mean_brier": None, "observed_rate": None, "observed_true": 0})
        b["count"] += 1
        b["sum_brier"] += brier
        b["observed_true"] += 1 if bool(outcome) else 0
    for h in horizons.values():
        h["mean_brier"] = round(h["sum_brier"] / h["count"], 4) if h["count"] else None
        h["sum_brier"] = round(h["sum_brier"], 4)
        for b in h["buckets"].values():
            b["mean_brier"] = round(b["sum_brier"] / b["count"], 4) if b["count"] else None
            b["sum_brier"] = round(b["sum_brier"], 4)
            b["observed_rate"] = round(b.get("observed_true", 0) / b["count"], 4) if b["count"] else None
            b.pop("observed_true", None)
    return {"version": "forecast_calibration_v1", "horizons": horizons}


def _tracker_event_type(tracker_id, trend, prob):
    if tracker_id == "iran_nuclear":
        return "nuclear_threshold"
    if tracker_id == "iran_conventional":
        return "gulf_conventional_escalation"
    if tracker_id == "israel_lebanon":
        return "border_war_escalation"
    if tracker_id in ("russia", "russia_ukraine"):
        return "nato_war_escalation"
    if tracker_id == "china":
        return "taiwan_pressure_escalation"
    if tracker_id == "north_korea":
        return "dprk_military_escalation"
    if tracker_id in ("india", "pakistan_afghanistan"):
        return "border_conflict_escalation"
    if trend == "falling" and prob < 20:
        return "de_escalation_continuation"
    return "escalation_watch"


def _forecast_description(tracker_name, event_type, horizon_label, probability):
    readable_event = event_type.replace("_", " ")
    return (
        f"{tracker_name}: {readable_event} risk over the next {horizon_label} "
        f"is estimated at {probability}%."
    )


def _extract_forecast_evidence(tracker, state):
    evidence_for = []
    evidence_against = []

    for sig in tracker.get("signals", []) or []:
        if isinstance(sig, dict):
            label = sig.get("name") or sig.get("signal") or sig.get("id") or "signal"
            weight = sig.get("original_weight", sig.get("weight", 0))
            item = f"{label} ({weight:+} signal weight)" if isinstance(weight, (int, float)) else str(label)
            if sig.get("positive"):
                evidence_against.append(item)
            else:
                evidence_for.append(item)
        elif sig:
            evidence_for.append(str(sig))

    tid = tracker.get("id")
    tracker_state = state.get("trackers", {}).get(tid, {})
    for sig in tracker_state.get("active_signals", []) or []:
        label = str(sig).replace("_", " ")
        if any(term in label.lower() for term in DEESCALATION_TERMS):
            evidence_against.append(label)
        else:
            evidence_for.append(label)

    for news in state.get("latest_news", []) or []:
        if news.get("zone") not in (None, "", tid, tracker.get("name")):
            continue
        text = (news.get("headline") or news.get("text") or "").strip()
        if not text:
            continue
        item = text[:180]
        if any(term in text.lower() for term in DEESCALATION_TERMS):
            evidence_against.append(item)
        else:
            evidence_for.append(item)

    notes = tracker_state.get("notes") or ""
    if notes:
        if any(term in notes.lower() for term in DEESCALATION_TERMS):
            evidence_against.append(notes[:180])
        elif len(evidence_for) < 3:
            evidence_for.append(notes[:180])

    # De-duplicate while preserving order and keep payload compact.
    def _dedupe(items):
        seen = set()
        out = []
        for item in items:
            key = str(item).lower()
            if key in seen:
                continue
            seen.add(key)
            out.append(str(item))
        return out[:4]

    evidence_for = _dedupe(evidence_for) or ["No discrete escalation signal isolated; forecast is driven by current threat score."]
    evidence_against = _dedupe(evidence_against) or ["No clear de-escalation or contradiction signal isolated."]
    return evidence_for, evidence_against


def _forecast_confidence(tracker, state, evidence_for, evidence_against):
    tid = tracker.get("id")
    source_count = 0
    for news in state.get("latest_news", []) or []:
        if news.get("zone") in (None, "", tid, tracker.get("name")):
            source_count += len(news.get("sources", []) or []) or 1
    signal_count = len(tracker.get("signals", []) or []) + len(
        state.get("trackers", {}).get(tid, {}).get("active_signals", []) or []
    )
    score = min(100, 25 + source_count * 12 + signal_count * 8 + min(20, len(evidence_for) * 4))
    if len(evidence_against) > len(evidence_for):
        score = max(0, score - 12)
    label = "HIGH" if score >= 70 else "MEDIUM" if score >= 45 else "LOW"
    return score, label


def generate_forecast_ladder(trackers_js, state, now_iso, *, max_trackers=6):
    """Generate auditable multi-horizon Forecast Engine v2 records.

    These are not auto-resolved against future internal probabilities. They are
    explicit event forecasts with manual/source-verified resolution criteria so
    the dashboard can evolve away from circular self-scoring.
    """
    now_dt = _parse_utc(now_iso)
    ranked = sorted(
        trackers_js,
        key=lambda t: (float(t.get("prob", 0)), {"rising": 2, "stable": 1, "falling": 0}.get(t.get("trend"), 1)),
        reverse=True,
    )
    active = [
        t for t in ranked
        if float(t.get("prob", 0)) >= 15 or t.get("zone") in {"elevated", "critical", "imminent"}
    ][:max_trackers]

    forecasts = []
    for tracker in active:
        tid = tracker.get("id")
        tname = tracker.get("name", tid)
        prob = float(tracker.get("prob", 0))
        trend = tracker.get("trend", "stable")
        event_type = _tracker_event_type(tid, trend, prob)
        evidence_for, evidence_against = _extract_forecast_evidence(tracker, state)
        confidence_score, confidence_label = _forecast_confidence(tracker, state, evidence_for, evidence_against)

        trend_adj = {"rising": 6, "stable": 0, "falling": -8}.get(trend, 0)
        contradiction_penalty = min(12, max(0, len(evidence_against) - 1) * 3)
        support_bonus = min(10, max(0, len(evidence_for) - 1) * 2)

        for horizon_label, horizon_hours, multiplier in FORECAST_HORIZONS:
            expires = (now_dt + timedelta(hours=horizon_hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
            probability_model = build_probability_model(
                tracker,
                state,
                event_type,
                horizon_label,
                evidence_for=evidence_for,
                evidence_against=evidence_against,
            )
            event_probability = probability_model["final_probability_pct"]
            forecast_id = f"{_slug(tid)}:{_slug(event_type)}:{horizon_label}:{expires}"
            forecasts.append({
                "schema_version": "forecast_v2",
                "forecast_id": forecast_id,
                "generated_at": now_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "tracker_id": tid,
                "tracker_name": tname,
                "event_type": event_type,
                "horizon_label": horizon_label,
                "horizon_hours": horizon_hours,
                "probability": event_probability,
                "base_rate_pct": probability_model["base_rate_pct"],
                "model_version": FORECAST_MODEL_VERSION,
                "probability_model": probability_model,
                "confidence_score": confidence_score,
                "confidence_label": confidence_label,
                "description": _forecast_description(tname, event_type, horizon_label, event_probability),
                "resolution_criteria": RESOLUTION_CRITERIA.get(
                    tid,
                    "Resolved true if verified official or Reuters/AP/AFP/BBC-level reporting confirms the forecast event before expiry.",
                ),
                "resolution_method": "manual_or_source_verified",
                "evaluation_status": "pending",
                "expires_at": expires,
                "evidence_for": evidence_for,
                "evidence_against": evidence_against,
            })

    return forecasts


# ── Identity & Dedup ──────────────────────────────────────────────────────────

def prediction_identity(pred):
    """Canonical key for deduplication: (tracker_id, expires_at)."""
    return (pred.get("tracker_id"), pred.get("expires_at"))


def merge_prediction_records(existing, incoming):
    """Merge two prediction dicts — incoming wins on non-None values,
    existing wins on evaluation metadata once evaluated."""
    merged = dict(existing)
    for key, value in incoming.items():
        if value is not None:
            merged[key] = value

    # Preserve existing evaluation if already done
    if existing.get("evaluated") and not incoming.get("evaluated"):
        for key in ("evaluated", "evaluated_at", "actual_value", "correct"):
            if key in existing:
                merged[key] = existing[key]

    # Fill in description fields from existing if missing
    for key in (
        "eval_type", "eval_value", "type", "value",
        "description", "confidence", "signal_name"
    ):
        if merged.get(key) is None and existing.get(key) is not None:
            merged[key] = existing[key]

    return merged


def dedupe_predictions(predictions):
    """Deduplicate predictions by (tracker_id, expires_at), merging records."""
    deduped = {}
    order = []
    for pred in predictions:
        key = prediction_identity(pred)
        if key not in deduped:
            deduped[key] = pred
            order.append(key)
        else:
            deduped[key] = merge_prediction_records(deduped[key], pred)
    return [deduped[key] for key in order]


# ── Narrative → Evaluable Type Mapping ────────────────────────────────────────

NARRATIVE_TO_EVAL = {
    "military_operation": ("probability_above", 0.7),
    "ground_operation": ("probability_above", 0.7),
    "diplomatic": ("probability_below", 0.5),
    "status_quo": ("probability_above", 0.5),
    "border_conflict": ("probability_above", 0.6),
    "nuclear_development": ("probability_above", 0.3),
    "economic_impact": ("probability_above", 0.5),
    "humanitarian": ("probability_above", 0.3),
    "arms_deal": ("probability_above", 0.4),
    "cyber_operation": ("probability_above", 0.3),
    "political_crisis": ("probability_above", 0.4),
}


# ── Evaluation ────────────────────────────────────────────────────────────────

def evaluate_prediction(pred, state, now_iso, narrative_to_eval=None):
    """Evaluate a single expired prediction against current state.

    Returns the mutated pred dict with eval fields set.
    """
    if narrative_to_eval is None:
        narrative_to_eval = NARRATIVE_TO_EVAL

    pred_tid = pred["tracker_id"]
    pred_type = pred.get("eval_type")
    pred_value = pred.get("eval_value")

    # Map old narrative types to evaluable types (backward compat)
    if not pred_type:
        narrative_type = pred.get("type", "")
        if narrative_type in narrative_to_eval:
            mapped_type, default_threshold = narrative_to_eval[narrative_type]
            pred_type = mapped_type
            if narrative_type == "status_quo":
                pred_value = pred.get("value", 50) * 0.7
            else:
                pred_value = default_threshold * 100
        else:
            pred_type = "probability_above"
            pred_value = 50

    actual_state = state.get("trackers", {}).get(pred_tid, {})

    if pred_type == "probability_above":
        actual_prob = actual_state.get(
            "current_probability_with_coupling",
            actual_state.get("current_probability", 0)
        )
        pred["actual_value"] = actual_prob
        pred["correct"] = actual_prob >= pred_value
        pred["evaluated"] = True
        pred["evaluated_at"] = now_iso

    elif pred_type == "probability_below":
        actual_prob = actual_state.get(
            "current_probability_with_coupling",
            actual_state.get("current_probability", 0)
        )
        pred["actual_value"] = actual_prob
        pred["correct"] = actual_prob <= pred_value
        pred["evaluated"] = True
        pred["evaluated_at"] = now_iso

    elif pred_type == "trend_rising":
        actual_trend = actual_state.get("trend", "stable")
        pred["actual_value"] = actual_trend
        pred["correct"] = actual_trend == "rising"
        pred["evaluated"] = True
        pred["evaluated_at"] = now_iso

    elif pred_type == "signal_triggered":
        actual_signals = actual_state.get("active_signals", [])
        sig_name = pred.get("signal_name", "")
        pred["actual_value"] = sig_name in actual_signals
        pred["correct"] = sig_name in actual_signals
        pred["evaluated"] = True
        pred["evaluated_at"] = now_iso

    elif pred_type == "zone_change":
        actual_zone = actual_state.get("zone", "deterrent")
        pred["actual_value"] = actual_zone
        pred["correct"] = actual_zone == pred_value
        pred["evaluated"] = True
        pred["evaluated_at"] = now_iso

    else:
        # Unknown eval type — leave unevaluated
        pred["evaluated"] = False

    return pred


def evaluate_all_predictions(evaluations, state, now_iso):
    """Evaluate all expired, unevaluated predictions in-place."""
    for pred in evaluations.get("predictions", []):
        if not pred.get("evaluated") and pred.get("expires_at", "") < now_iso:
            evaluate_prediction(pred, state, now_iso)
    return evaluations


# ── Generation ────────────────────────────────────────────────────────────────

def generate_predictions(trackers_js, state, now_iso):
    """Generate event-based 24-hour predictions from news + signals + trends.

    Returns list of prediction dicts (max 15, sorted by confidence).
    """
    utc_now = datetime.now(timezone.utc)
    sorted_trackers = sorted(trackers_js, key=lambda t: t["prob"], reverse=True)
    expires_at = (utc_now + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")

    news_texts = [
        (n.get("headline", "") or n.get("text", "")).lower()
        for n in state.get("latest_news", [])
    ]
    combined_news = " ".join(news_texts)

    new_predictions = []
    for t in sorted_trackers:
        prob = t["prob"]
        trend = t["trend"]
        tid = t["id"]
        tname = t["name"]
        confidence = 0
        event = ""
        etype = ""

        # IRAN CONVENTIONAL
        if tid == "iran_conventional" and prob >= 30:
            if "hormuz" in combined_news or "blockade" in combined_news:
                event = ("Strait of Hormuz expected to remain under Iranian blockade. "
                         "Additional shipping attacks probable within 12 hours.")
                confidence = 75; etype = "military_operation"
            elif "dubai" in combined_news or "uae" in combined_news:
                event = ("Iranian strikes on UAE infrastructure expected to continue. "
                         "Further drone and missile attacks on Gulf state targets likely within 24 hours.")
                confidence = 70; etype = "military_operation"
            elif confidence == 0 and trend == "rising":
                event = ("Current escalation trajectory suggests Iran will sustain offensive "
                         "operations against US and Israeli regional assets over the next 24 hours.")
                confidence = 55; etype = "military_operation"

        # ISRAEL-LEBANON
        elif tid == "israel_lebanon" and prob >= 20:
            if "ground" in combined_news or "invasion" in combined_news:
                event = ("Israeli ground operation in southern Lebanon expected to continue "
                         "beyond Litani River. Further displacement and infrastructure destruction likely.")
                confidence = 70; etype = "ground_operation"
            elif confidence == 0 and trend == "rising":
                event = ("Continued escalation in Lebanon with increased Israeli operations "
                         "and Hezbollah retaliatory strikes expected.")
                confidence = 55; etype = "military_operation"

        # PAKISTAN-AFGHANISTAN
        elif tid == "pakistan_afghanistan" and prob >= 20:
            if "taliban" in combined_news or "border" in combined_news or "kills" in combined_news:
                event = ("Border escalation between Afghanistan and Pakistan likely to intensify. "
                         "Cross-border strikes expected within 24 hours.")
                confidence = 65; etype = "border_conflict"
            elif confidence == 0:
                event = ("Afghan-Pakistan border tensions likely to persist. "
                         "Additional clashes probable based on recent trajectory.")
                confidence = 50; etype = "border_conflict"

        # TURKEY
        elif tid == "turkey" and prob >= 15:
            if "incirlik" in combined_news or "nato" in combined_news:
                event = ("Turkish military posture shift expected. NATO alliance consultations "
                         "likely as Turkey repositions forces.")
                confidence = 55; etype = "alliance_shift"
            elif trend == "rising":
                event = ("Turkey expected to continue escalating rhetoric and military "
                         "positioning in Eastern Mediterranean.")
                confidence = 45; etype = "escalation"

        # RUSSIA-NATO
        elif tid == "russia" and prob >= 50:
            if "ceasefire" in combined_news or "deal" in combined_news:
                event = ("Diplomatic negotiations may produce ceasefire framework within "
                         "24-72 hours, though implementation remains uncertain.")
                confidence = 45; etype = "diplomatic"
            elif trend == "rising":
                event = ("Russian military operations expected to continue at current tempo. "
                         "No significant de-escalation indicators.")
                confidence = 40; etype = "status_quo"

        # IRAN NUCLEAR
        elif tid == "iran_nuclear" and prob >= 20:
            if "iaea" in combined_news or "enrichment" in combined_news:
                event = ("IAEA monitoring likely to produce findings within 72 hours. "
                         "Iran may announce further enrichment activity.")
                confidence = 40; etype = "nuclear_development"
            else:
                event = ("No immediate nuclear threshold events anticipated. "
                         "Status quo enrichment posture likely maintained.")
                confidence = 35; etype = "status_quo"

        # Generic fallback
        if confidence == 0:
            if trend == "rising":
                event = (f"Current escalation indicators suggest {tname} will remain on "
                         "upward trajectory. Monitor for trigger events.")
                confidence = 40; etype = "escalation"
            elif trend == "falling":
                event = (f"{tname} showing de-escalation signals. "
                         "Probability expected to decline gradually.")
                confidence = 40; etype = "de_escalation"
            else:
                event = f"{tname} remains stable at current levels. No significant changes anticipated."
                confidence = 35; etype = "status_quo"

        # Map narrative intent to evaluable prediction type
        eval_type = "probability_above"
        eval_value = max(0, prob - 10)
        if etype in ("de_escalation",):
            eval_type = "probability_below"
            eval_value = prob
        elif etype in ("status_quo", "diplomatic", "nuclear_development"):
            eval_type = "probability_above"
            eval_value = max(0, prob - 15)

        # Differentiated forecast value so escalation/de-escalation survive the
        # trivial-prediction filter below.
        prob_f = float(prob)
        if etype == "escalation":
            pred_value = int(round(min(100.0, prob_f * 1.15)))
        elif etype == "de_escalation":
            pred_value = int(round(max(0.0, prob_f * 0.85)))
        else:
            pred_value = int(round(prob_f))

        new_predictions.append({
            "tracker_id": tid,
            "tracker_name": tname,
            "type": etype,
            "value": pred_value,
            "description": event,
            "confidence": confidence,
            "expires_at": expires_at,
            "eval_type": eval_type,
            "eval_value": eval_value,
        })

    # Drop status_quo forecasts that don't say anything new (pred == current).
    # Escalation / de_escalation carry a differentiated value so they survive.
    filtered = []
    for pred in new_predictions:
        tid = pred["tracker_id"]
        current_prob = next((t["prob"] for t in sorted_trackers if t["id"] == tid), 0)
        pred_prob = pred["value"]
        if pred["type"] == "status_quo" and abs(pred_prob - current_prob) <= 3:
            continue
        filtered.append(pred)

    # Sort by confidence, take top 15
    filtered.sort(key=lambda x: x["confidence"], reverse=True)
    return filtered[:15]


# ── Accuracy Stats ────────────────────────────────────────────────────────────

def compute_eval_stats(evaluations):
    """Return (total_evaluated, correct_count, accuracy_pct)."""
    evaluated = [p for p in evaluations.get("predictions", []) if p.get("evaluated")]
    total = len(evaluated)
    correct = sum(1 for p in evaluated if p.get("correct"))
    pct = round(correct / total * 100) if total > 0 else 0
    return total, correct, pct
