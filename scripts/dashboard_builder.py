#!/usr/bin/env python3
"""
dashboard_builder.py — Tracker card construction and dashboard HTML injection.

Extracted from pipeline.py for DoomsdayWatch modular architecture.
"""

import html as html_lib
import json
import re
from datetime import datetime, timezone

from .signals import normalize_trend, build_signal_data
from .probabilities import classify_zone

# ── State injection marker ────────────────────────────────────────────────────
__STATE_INJECTION__ = "const state = {"


def build_tracker_cards(state, cfg, tn, signal_weights, timeline, now_dt, now_iso):
    """Build enriched tracker card dicts from state + config.

    Returns list of card dicts with id, name, emoji, prob, zone, trend,
    signals, confidence, base_rate.
    """
    trackers_src = state.get("trackers", {}) or state.get("zones", {})
    zone_thresholds = cfg.get("scoring", {}).get("zones", {})
    cards = []

    for tid, name, emoji in tn:
        tracker = trackers_src.get(tid, {})
        signal_data, confidence = build_signal_data(
            tid, state, signal_weights, timeline, now_dt, now_iso
        )
        trend = normalize_trend(tracker.get("trend", "stable"))
        prob = tracker.get("current_probability", tracker.get("current_prob", 0))

        zone = tracker.get("zone")
        if not zone:
            zone = classify_zone(prob, zone_thresholds)

        base_rate = tracker.get(
            "base_rate",
            cfg.get("trackers", {}).get(tid, {}).get("base_rate", 0)
        )

        cards.append({
            "id": tid,
            "name": name,
            "emoji": emoji,
            "prob": prob,
            "zone": zone,
            "trend": trend,
            "signals": signal_data,
            "confidence": confidence,
            "base_rate": base_rate,
        })

    return cards


def build_dashboard(html_template, trackers_js, news_js, gp, tz,
                    history, zone_alerts, energy_data,
                    predictions_js, eval_stats_js, narrative,
                    state):
    """Inject all data into dashboard HTML template.

    Uses string slicing anchored on __STATE_INJECTION__ and // ===== RENDER
    markers to replace the state block.

    Returns the full HTML string.
    """
    start = html_template.find(__STATE_INJECTION__)
    end = html_template.find("// ===== RENDER", start)

    if start == -1 or end == -1:
        print(f"[dashboard] ERROR: markers not found start={start} end={end}")
        return html_template

    # ── Build state JS block ──────────────────────────────────────────────
    lines = []
    lines.append("const state = {")
    lines.append("  last_updated: " + json.dumps(state.get("last_updated", "")) + ",")
    lines.append("  global_war_probability: " + str(gp) + ",")
    lines.append("  global_zone: " + json.dumps(tz) + ",")

    # Trackers array
    lines.append("  trackers: [")
    for t in trackers_js:
        signals_str = json.dumps(t["signals"])
        prob_int = int(round(float(t["prob"])))
        lines.append(
            "    { id: " + json.dumps(t["id"])
            + ", name: " + json.dumps(t["name"])
            + ", emoji: " + json.dumps(t["emoji"])
            + ", prob: " + str(prob_int)
            + ", zone: " + json.dumps(t["zone"])
            + ", trend: " + json.dumps(t["trend"])
            + ", confidence: " + json.dumps(t.get("confidence", "LOW"))
            + ", signals: " + signals_str + " },"
        )
    lines.append("  ],")

    # News array
    lines.append("  news: [")
    for n in news_js[:10]:
        txt = json.dumps(n.get("text", ""))
        hl = json.dumps(n.get("headline", ""))
        src = json.dumps(n.get("sources", []))
        src_types = json.dumps(n.get("source_types", []))
        sigs = json.dumps(n.get("signals", []))
        lines.append(
            "    { zone: " + json.dumps(n.get("zone", ""))
            + ", time: " + json.dumps(n.get("time", ""))
            + ", text: " + txt
            + ", headline: " + hl
            + ", impact: " + json.dumps(n.get("impact", "neutral"))
            + ", sources: " + src
            + ", source_types: " + src_types
            + ", confidence: " + json.dumps(n.get("confidence", "reported"))
            + ", severity: " + str(n.get("severity", 1))
            + ", signals: " + sigs + " },"
        )
    lines.append("  ],")

    # Probability history
    hist_entries = history.get("entries", [])[-48:]
    hist_js = json.dumps(hist_entries)
    lines.append("  history: " + hist_js + ",")

    # Zone alerts
    alerts_js = json.dumps(zone_alerts.get("pending", []))
    lines.append("  zone_alerts: " + alerts_js + ",")

    # Energy prices
    energy_js = json.dumps({
        "current": energy_data.get("current", {}),
        "baselines": energy_data.get("baselines", {}),
        "changes": energy_data.get("changes", {}),
        "history": energy_data.get("history", [])[-48:],
    })
    lines.append("  energy: " + energy_js)
    lines.append("};")
    lines.append("")
    lines.append("// ===== RENDER")

    new_state_block = "\n".join(lines)
    new_html = html_template[:start] + new_state_block + html_template[end:]

    # ── Chart SVG ─────────────────────────────────────────────────────────
    chart_svg = _generate_chart_svg(hist_entries)
    chart_placeholder = '<div id="probChart" style="width:100%;height:120px"></div>'
    if chart_svg:
        new_html = new_html.replace(chart_placeholder, chart_svg)

    # ── Narrative injection ───────────────────────────────────────────────
    narrative_placeholder = (
        '<div id="narrative-content" '
        'style="font-size:12px;line-height:1.7;color:#8b949e;white-space:normal;"></div>'
    )
    safe_narrative = html_lib.escape(narrative).replace("\n", "<br>")
    new_html = new_html.replace(
        narrative_placeholder,
        '<div id="narrative-content" '
        'style="font-size:12px;line-height:1.7;color:#8b949e;white-space:normal;">'
        + safe_narrative + '</div>'
    )

    # ── Predictions injection ─────────────────────────────────────────────
    pred_inject = (
        ",\n  predictions: " + predictions_js
        + ",\n  eval_stats: " + eval_stats_js
    )
    new_html = new_html.replace(
        "\n};\n\n// ===== RENDER",
        pred_inject + "\n};\n\n// ===== RENDER"
    )

    return new_html


def _generate_chart_svg(hist_entries):
    """Generate a compact SVG probability chart from history entries."""
    if len(hist_entries) < 2:
        return ""

    W, H = 600, 120
    padL, padR, padT, padB = 30, 10, 10, 20
    cW, cH = W - padL - padR, H - padT - padB

    svg = (
        f'<div id="probChart" style="width:100%;overflow:hidden">'
        f'<svg width="100%" height="120" viewBox="0 0 {W} {H}">'
    )

    # Zone backgrounds
    for mx, col in [
        (15, "rgba(0,230,118,0.06)"),
        (30, "rgba(255,170,0,0.06)"),
        (60, "rgba(255,170,0,0.08)"),
        (100, "rgba(255,45,45,0.06)"),
    ]:
        y1 = padT + cH * (1 - mx / 100)
        prev_mx = {15: 0, 30: 15, 60: 30, 100: 60}[mx]
        y2 = padT + cH * (1 - prev_mx / 100)
        svg += (
            f'<rect x="{padL}" y="{y1:.1f}" width="{cW}" '
            f'height="{y2 - y1:.1f}" fill="{col}"/>'
        )

    # Threshold lines
    for th in [15, 30, 60]:
        y = padT + cH * (1 - th / 100)
        svg += (
            f'<line x1="{padL}" y1="{y:.1f}" x2="{padL + cW}" y2="{y:.1f}" '
            f'stroke="rgba(255,255,255,0.08)" stroke-dasharray="3,3"/>'
        )
        svg += (
            f'<text x="2" y="{y + 3:.1f}" fill="#484f58" '
            f'font-size="8" font-family="monospace">{th}%</text>'
        )

    # Global line
    pts = []
    for i, e in enumerate(hist_entries):
        x = padL + (i / max(len(hist_entries) - 1, 1)) * cW
        y = padT + cH * (1 - (e.get("global", 0) / 100))
        pts.append(f"{x:.1f},{y:.1f}")

    svg += (
        '<defs><filter id="cglow"><feGaussianBlur stdDeviation="2" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
        '</feMerge></filter></defs>'
    )
    svg += (
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="#ff2d2d" '
        f'stroke-width="2" filter="url(#cglow)"/>'
    )

    # Current dot
    last = hist_entries[-1]
    lx = padL + cW
    ly = padT + cH * (1 - last.get("global", 0) / 100)
    svg += f'<circle cx="{lx}" cy="{ly:.1f}" r="4" fill="#ff2d2d"/>'
    svg += (
        f'<text x="{lx - 35}" y="{ly - 8:.1f}" fill="#e6edf3" '
        f'font-size="10" font-weight="bold" font-family="monospace">'
        f'{last.get("global", 0)}%</text>'
    )

    # Time labels
    ft = (hist_entries[0].get("timestamp", ""))[5:16].replace("T", " ")
    lt = (hist_entries[-1].get("timestamp", ""))[5:16].replace("T", " ")
    svg += (
        f'<text x="{padL}" y="{H - 4}" fill="#484f58" '
        f'font-size="8" font-family="monospace">{ft}</text>'
    )
    svg += (
        f'<text x="{W - padR}" y="{H - 4}" fill="#484f58" '
        f'font-size="8" font-family="monospace" text-anchor="end">{lt}</text>'
    )
    svg += '</svg></div>'

    return svg


def generate_narrative(trackers_js, hist_entries, gp, now_dt):
    """Generate CIA-style threat assessment narrative string.

    Returns a multi-line plain-text narrative.
    """
    utc_now = datetime.now(timezone.utc)
    date_str = utc_now.strftime("%B %d, %Y")
    time_str = utc_now.strftime("%H:%M UTC")

    sorted_trackers = sorted(trackers_js, key=lambda t: t["prob"], reverse=True)

    # Key developments (signals activated in last 6 hours)
    key_devs = []
    for t in sorted_trackers:
        for s in t.get("signals", []):
            try:
                activated = datetime.fromisoformat(
                    s["activated_at"].replace("Z", "+00:00")
                )
                hours_ago = (utc_now - activated).total_seconds() / 3600
                if hours_ago < 6:
                    key_devs.append((
                        t["name"], t["emoji"],
                        s["name"].replace("_", " "), hours_ago
                    ))
            except Exception:
                pass

    # Zone summary
    zone_counts = {}
    for t in sorted_trackers:
        z = t["zone"]
        if z not in zone_counts:
            zone_counts[z] = []
        zone_counts[z].append(t)

    # Probability changes
    prob_changes = {}
    if len(hist_entries) >= 2:
        prev = hist_entries[-2]
        curr = hist_entries[-1]
        for tid in curr.get("trackers", {}):
            p_old = prev.get("trackers", {}).get(tid, 0)
            p_new = curr.get("trackers", {}).get(tid, 0)
            diff = p_new - p_old
            if diff != 0:
                prob_changes[tid] = diff

    rising = [t for t in sorted_trackers if t["trend"] == "rising"]
    falling = [t for t in sorted_trackers if t["trend"] == "falling"]

    # Overall assessment
    gp_change = ""
    if len(hist_entries) >= 2:
        prev_g = hist_entries[-2].get("global", gp)
        diff_g = gp - prev_g
        if diff_g > 0:
            gp_change = f" (+{diff_g} from prior hour)"
        elif diff_g < 0:
            gp_change = f" ({diff_g} from prior hour)"

    if gp >= 60:
        severity_word = "ELEVATED"
        overall = (
            f"The global security environment remains {severity_word.lower()} "
            f"with a composite threat score of {gp}%{gp_change}."
        )
    elif gp >= 30:
        severity_word = "CONCERNING"
        overall = f"The global threat posture is {severity_word.lower()} at {gp}%{gp_change}."
    else:
        severity_word = "STABLE"
        overall = f"Global threat levels remain {severity_word.lower()} at {gp}%{gp_change}."

    # Immediate threats
    immediate = []
    for z in ["imminent", "critical"]:
        if z in zone_counts:
            for t in zone_counts[z]:
                sig_names = [
                    s["name"].replace("_", " ")
                    for s in t.get("signals", [])[:3]
                ]
                sig_text = "; ".join(sig_names) if sig_names else "dormant"
                trend_word = (
                    "escalating" if t["trend"] == "rising"
                    else "de-escalating" if t["trend"] == "falling"
                    else "holding"
                )
                immediate.append(
                    f"  {t['emoji']} {t['name']} — {t['prob']}% "
                    f"({trend_word}). {sig_text}."
                )

    # Notable developments
    notable = []
    for tname, emoji, sig_name, hrs in key_devs[:5]:
        time_ref = f"{int(hrs * 60)}m" if hrs < 1 else f"{hrs:.1f}h"
        notable.append(f"  {emoji} {tname} — {sig_name} ({time_ref} ago)")

    # Trend analysis
    trend_parts = []
    if rising:
        names = ", ".join(t["name"] for t in rising[:3])
        trend_parts.append(f"Escalating: {names}")
    if falling:
        names = ", ".join(t["name"] for t in falling[:3])
        trend_parts.append(f"De-escalating: {names}")
    if not trend_parts:
        trend_parts.append("No significant directional shifts this cycle")

    # Outlook
    outlook_parts = []
    if rising:
        outlook_parts.append(
            f"Monitor {rising[0]['name']} for continued escalation — "
            f"currently {rising[0]['prob']}% and trending upward."
        )
    if prob_changes:
        biggest = max(prob_changes.items(), key=lambda x: abs(x[1]))
        name = next(
            (t["name"] for t in sorted_trackers if t["id"] == biggest[0]),
            biggest[0]
        )
        sign = "+" if biggest[1] > 0 else ""
        outlook_parts.append(
            f"{name} showed largest probability shift ({sign}{biggest[1]}%)."
        )
    if not outlook_parts:
        outlook_parts.append("No immediate escalation catalysts identified.")

    total_signals = sum(len(t.get("signals", [])) for t in sorted_trackers)
    confidence_label = (
        "HIGH" if len(key_devs) >= 5
        else "MEDIUM" if len(key_devs) >= 2
        else "LOW"
    )

    narrative = f"""THREAT ASSESSMENT — {date_str} {time_str}

{overall}

IMMEDIATE THREATS:
{chr(10).join(immediate) if immediate else "  None currently in IMMINENT/CRITICAL zone."}

NOTABLE DEVELOPMENTS:
{chr(10).join(notable) if notable else "  No significant developments this cycle."}

TREND: {' | '.join(trend_parts)}

OUTLOOK: {' '.join(outlook_parts)}

CONFIDENCE: {confidence_label} | {total_signals} active signals | {len(key_devs)} new this cycle"""

    return narrative
