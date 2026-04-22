#!/usr/bin/env python3
"""
predictions.py — Prediction identity, deduplication, merging, generation,
and evaluation.

Extracted from pipeline.py for DoomsdayWatch modular architecture.
"""

from datetime import datetime, timedelta, timezone


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
