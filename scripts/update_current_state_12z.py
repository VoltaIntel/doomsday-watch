#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STATE_PATH = DATA / "current_state.json"
CFG_PATH = DATA / "tracker_config.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def zone_for(p: float, cfg: dict) -> str:
    zones = cfg.get("scoring", {}).get("zones", {})
    def mn(k, default):
        v = zones.get(k, [])
        return v[0] if isinstance(v, list) and v else default
    if p >= mn("imminent", 50):
        return "imminent"
    if p >= mn("critical", 25):
        return "critical"
    if p >= mn("elevated", 10):
        return "elevated"
    return "deterrent"


def latest_artifact() -> Path:
    files = sorted(DATA.glob("morning_deep_scan_sources_*.json"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise SystemExit("no morning_deep_scan_sources artifact found")
    return files[-1]


cfg = json.loads(CFG_PATH.read_text())
state = json.loads(STATE_PATH.read_text())
artifact_path = latest_artifact()
artifact = json.loads(artifact_path.read_text())
ts = artifact.get("generated_at") or now_iso()
counts = artifact.get("counts", {})
official = artifact.get("official", {})

canonical = set(cfg.get("trackers", {}))
for tid, trk in list(state.get("trackers", {}).items()):
    if tid not in canonical:
        raise SystemExit(f"noncanonical tracker in state before update: {tid}")
    bad = [s for s in trk.get("active_signals", []) if s not in cfg["trackers"][tid].get("signals", {})]
    if bad:
        raise SystemExit(f"noncanonical active signals for {tid}: {bad}")

old_coupled = {tid: state.get("trackers", {}).get(tid, {}).get("current_probability_with_coupling", state.get("trackers", {}).get(tid, {}).get("current_probability")) for tid in cfg.get("trackers", {})}
old_raw = {tid: state.get("trackers", {}).get(tid, {}).get("current_probability") for tid in cfg.get("trackers", {})}

notes = {
    "iran_conventional": "12Z scan keeps Iran conventional imminent but not worse: fallback reporting shows Hormuz transit friction and tanker-risk premia while shipping and oil pricing still reject a complete waterway-stop threshold.",
    "israel_lebanon": "12Z scan keeps Israel-Lebanon imminent: south-Lebanon strike, tunnel-damage, displacement and Hezbollah-activity claims persist; no wider alliance-entry breakpoint surfaced.",
    "turkey": "12Z scan keeps Turkey-NATO deterrent: fourteen-day fallback returned no qualifying Turkey-specific strategic-arms declaration or configured weapons event.",
    "india": "12Z scan keeps India-Pakistan elevated: repeated Poonch/LoC intruder items remain border-security friction, not corroborated sustained cross-border fire or major force movement.",
    "russia": "12Z scan keeps Russia-NATO critical raw and imminent after Ukraine coupling: Poland/Baltic hybrid-action warning language remains live, but no treaty invocation, public direct-combat entry decision, or verified kinetic incident surfaced.",
    "china": "12Z scan keeps China-Taiwan posture-watch critical: blockade-tabletop, patrol-pressure and maritime-authority coverage remain live; no execution order or configured force trigger surfaced.",
    "north_korea": "12Z scan keeps DPRK elevated: late-week weapons-drill and naval-posture coverage remains watch-only; no fresh corroborated configured event surfaced in the 24h pass.",
    "russia_ukraine": "12Z scan keeps Russia-Ukraine ceiling-level: strike/bluster reporting and Belarus-pressure context remain active-war context; no NATO direct-entry breakpoint surfaced.",
    "pakistan_afghanistan": "12Z scan keeps Pakistan-Afghanistan critical/rising: fallback reporting continues to corroborate Pakistani cross-border action, civilian casualty claims and Taliban retaliation language; the existing configured force-posture lane remains active.",
    "iran_nuclear": "12Z scan keeps Iran verification critical: public reporting describes watchdog-access claims and Tehran pushback over timing and terms; no higher-threshold technical trigger was corroborated.",
    "sudan": "12Z scan keeps Sudan imminent: El Obeid/Kordofan atrocity-risk and siege-pressure reporting remains live; no material easing signal surfaced.",
    "israel_palestine": "12Z scan keeps Israel-Palestine imminent: Gaza fatality and West Bank harm/accountability reporting remain severe; no wider-regional breakout threshold is promoted.",
    "south_sudan_abyei": "12Z scan keeps South Sudan/Abyei deterrent: thirty-day fallback returned no fresh Abyei force-escalation reporting.",
}

for tid, trk in state.get("trackers", {}).items():
    trk["last_updated"] = ts
    trk["notes"] = notes.get(tid, trk.get("notes", ""))
    final = trk.get("current_probability_with_coupling", trk.get("current_probability", trk.get("current_prob", 0)))
    raw = trk.get("current_probability", trk.get("current_prob", final))
    trk["current_prob"] = raw
    trk["probability"] = raw
    trk["zone"] = zone_for(final, cfg)
    if tid in state.get("zones", {}):
        z = state["zones"][tid]
        z.update({
            "last_updated": ts,
            "notes": trk["notes"],
            "current_prob": raw,
            "current_probability": raw,
            "probability": raw,
            "current_probability_with_coupling": final,
            "coupling_boost": trk.get("coupling_boost", 0),
            "zone": trk["zone"],
            "trend": trk.get("trend", z.get("trend", "stable")),
            "active_signals": list(trk.get("active_signals", [])),
            "signal_timestamps": dict(trk.get("signal_timestamps", {})),
        })

latest_news = [
    {"zone":"iran_conventional","time":"12Z/24H","headline":"Iran/Hormuz: transit friction persists, no full stoppage confirmation","text":"OilPrice, Houston Chronicle, Barchart, UANI, FXLeaders and Economic Times fallback items show tanker-risk and firmer crude pricing, while public traffic and supply reporting still argue against a complete waterway-stop threshold.","impact":"watch","sources":["OilPrice.com","Houston Chronicle","Barchart","United Against Nuclear Iran","FXLeaders","The Economic Times","Google News RSS fallback"],"source_date":"29-30 Jun 2026"},
    {"zone":"pakistan_afghanistan","time":"12Z/14D","headline":"Pakistan-Afghanistan remains the active rising lane","text":"Public fallback reporting continues to describe Pakistani cross-border action, civilian casualty claims and Taliban retaliation language. This reconfirms the existing configured force-posture lane; no new signal name was added.","impact":"up","sources":["PBS","NPR","Al Jazeera","France24","Google News RSS fallback"],"source_date":"28-30 Jun 2026"},
    {"zone":"israel_lebanon","time":"12Z/24H","headline":"Israel-Lebanon: south Lebanon strike/tunnel items persist","text":"i24NEWS, Al Jazeera, France24, Arab Weekly, Kurdistan24 and Times of Israel fallback items show south-Lebanon strike context, tunnel damage, displacement stress and Hezbollah activity claims. No wider alliance-entry breakpoint surfaced.","impact":"watch","sources":["i24NEWS","Al Jazeera","France24","The Arab Weekly","Kurdistan24","The Times of Israel","Google News RSS fallback"],"source_date":"29-30 Jun 2026"},
    {"zone":"iran_nuclear","time":"12Z/7D","headline":"Iran verification: watchdog-access claims remain disputed","text":"NPR, CBS, NBC, Al-Monitor, SCMP and Al Jazeera-style fallback items describe a UN nuclear-monitoring debate while Tehran disputes timing and terms. No higher-threshold technical trigger is promoted.","impact":"watch","sources":["NPR","CBS News","NBC News","Al-Monitor","South China Morning Post","Al Jazeera","Google News RSS fallback"],"source_date":"23-30 Jun 2026"},
    {"zone":"russia","time":"12Z/7D","headline":"Russia-NATO: Poland/Baltic warning language remains below direct-entry threshold","text":"Guardian, Ukrainian Pravda, UNITED24 Media and regional fallback keep Polish/Baltic hybrid-action warning language live. No treaty invocation, public direct-combat entry decision or verified kinetic incident surfaced.","impact":"watch","sources":["The Guardian","Ukrainian Pravda","UNITED24 Media","Meta-Defense","Google News RSS fallback"],"source_date":"26-30 Jun 2026"},
    {"zone":"china","time":"12Z/7D","headline":"China-Taiwan: blockade-tabletop and patrol-pressure coverage remains posture-watch","text":"Reuters, ISW, Washington Times, WSJ and Taipei Times fallback items keep Taiwan blockade-tabletop coverage, PRC patrol/authority pressure and allied concern live. No configured force trigger surfaced.","impact":"stable","sources":["Reuters","Institute for the Study of War","Washington Times","WSJ","Taipei Times","Google News RSS fallback"],"source_date":"24-30 Jun 2026"},
    {"zone":"north_korea","time":"12Z/7D","headline":"DPRK: late-week weapons-drill coverage remains watch-only","text":"Al Jazeera, ABC, Guardian, Military.com and regional fallback items surfaced late-week weapons-drill and naval-posture coverage. No newer corroborated configured event was promoted in the 24h pass.","impact":"stable","sources":["Al Jazeera","ABC News","The Guardian","Military.com","Google News RSS fallback"],"source_date":"24-30 Jun 2026"},
    {"zone":"russia_ukraine","time":"12Z/24H","headline":"Russia-Ukraine: strike/bluster context remains live, no NATO-entry breakpoint","text":"Kyiv Post, MSN, War on the Rocks and open-source fallback show Belarus pressure, Russian strike/bluster context and NATO-adjacent posture debate. No allied direct-entry breakpoint surfaced.","impact":"watch","sources":["Kyiv Post","MSN","War on the Rocks","Substack/open-source fallback","Google News RSS fallback"],"source_date":"29-30 Jun 2026"},
    {"zone":"sudan","time":"12Z/7D","headline":"Sudan: El Obeid/Kordofan atrocity-risk warnings persist","text":"CFR, NYT, Washington Post, Genocide Watch, HRW and UN/OCHA fallback keep El Obeid/Kordofan atrocity-risk and siege-pressure reporting live. No material easing signal surfaced.","impact":"watch","sources":["Council on Foreign Relations","The New York Times","The Washington Post","Genocide Watch","Human Rights Watch","Google News RSS fallback"],"source_date":"23-30 Jun 2026"},
    {"zone":"israel_palestine","time":"12Z/24H","headline":"Gaza/West Bank: fatality and harm reporting keeps lane imminent","text":"AP-style, Al Jazeera, Guardian, Palestine Chronicle and regional fallback items describe fresh Gaza deaths, West Bank harm and child-casualty/accountability concerns. No wider-regional breakout threshold is promoted.","impact":"watch","sources":["Associated Press-style wire pickup","Al Jazeera","The Guardian","Palestine Chronicle","Google News RSS fallback"],"source_date":"29-30 Jun 2026"},
    {"zone":"india","time":"12Z/14D","headline":"India-Pakistan: Poonch/LoC intruder cluster remains watch-only","text":"Times of India, Bhaskar English, Daily Guardian/Magzter and other Indian fallback items report repeated Poonch/LoC intruder incidents. The cluster does not corroborate sustained cross-border fire or major force movement.","impact":"stable","sources":["The Times of India","Bhaskar English","Magzter/Daily Guardian","Public TV English","Google News RSS fallback"],"source_date":"27-30 Jun 2026"},
    {"zone":"turkey","time":"12Z/14D","headline":"Turkey configured-trigger review remains quiet","text":"Fourteen-day fallback returned no fresh qualifying Turkey-specific strategic-arms declaration or configured weapons event. Turkey remains deterrent in this framework.","impact":"stable","sources":["NATO public pages","Google News RSS fallback"],"source_date":"30 Jun 2026"},
    {"zone":"south_sudan_abyei","time":"12Z/30D","headline":"South Sudan/Abyei no-trigger review remains quiet","text":"Thirty-day fallback returned no fresh Abyei force-escalation reporting in the Google News RSS query. Deterrent status is unchanged.","impact":"stable","sources":["Google News RSS fallback","UN/OCHA page fallback"],"source_date":"30 Jun 2026"},
    {"zone":"oil_energy","time":"ENERGY/24H","headline":"Oil sanity check: supply risk visible, no panic pricing","text":"OilPrice, FXLeaders, Barchart, Business Post Nigeria and Economic Times fallback items show Hormuz-risk headlines while local price cache before deploy still sat in the low/mid-$70s Brent and near-$70 WTI band. This rejects full-waterway-stop pricing.","impact":"watch","sources":["OilPrice.com","FXLeaders","Barchart","Business Post Nigeria","The Economic Times","Yahoo/local energy cache","Google News RSS fallback"],"source_date":"29-30 Jun 2026"},
    {"zone":"iaea_un","time":"OFFICIAL/FALLBACK","headline":"Official-source probe: UN/NATO/EIA reachable; several pages blocked from this node","text":"Direct probes reached UN News RSS, UN Press RSS, NATO news/media pages and EIA RSS. IAEA, OPEC, OCHA oPt and UN Sudan pages returned blocked or failed responses from this node, so Iran/Sudan/Gaza judgments use reachable official feeds plus corroborated public reporting.","impact":"watch","sources":["UN News RSS","UN Press RSS","NATO public pages","EIA RSS","Google News RSS fallback"],"source_date":"30 Jun 2026"},
    {"zone":"nato_allied","time":"12Z/7D","headline":"NATO/allied posture: warnings live, no direct-entry decision","text":"NATO public pages were reachable, while Guardian, Atlantic Council/GLOBSEC-style and UNITED24 fallback showed eastern-flank warning and deterrence debate. No public direct-combat entry decision, treaty invocation or verified Russia-NATO kinetic incident surfaced.","impact":"stable","sources":["North Atlantic Treaty Organization","The Guardian","UNITED24 Media","Google News RSS fallback"],"source_date":"27-30 Jun 2026"},
    {"zone":"emerging","time":"AUTO-DETECT","headline":"Auto-detection review: no untracked crisis crosses tracker-add threshold","text":"Emerging-crisis query for Thailand-Cambodia, Ethiopia-Eritrea, Guyana/Venezuela and Kosovo-Serbia returned zero qualifying fresh items in this run. No untracked nuclear-escalation or alliance-spillover tracker was added.","impact":"stable","sources":["Google News RSS fallback","prior watch set"],"source_date":"23-30 Jun 2026"},
]

state["timestamp"] = ts
state["last_updated"] = ts
state["latest_news"] = latest_news
state["global_war_probability"] = 67
state["global_probability"] = 67
state["global_zone"] = "imminent"
state["raw_global_probability"] = 67.22

_meta = state.setdefault("_meta", {})
_meta.update({
    "last_writer": "doomsdaywatch_morning_deep_scan_cron",
    "last_scan": ts,
    "scan_time_utc": ts,
    "analysis_window": "morning_deep_scan_12z_past_24h_with_7d_14d_30d_sparse_crosschecks_official_feed_energy_polymarket_sanity_checks",
    "search_engine": "web_search_failed_http_432_then_public_safe_multi_source_fallback",
    "source_limitation": "web_search/Tavily returned HTTP 432 on 17/17 required tracker/sector searches. This run continued with Google News RSS, direct official/feed probes, terminal HTTP, local energy cache, and Polymarket cache. Single-source claims are treated as watch items until corroborated.",
    "source_fallback_detail_12z": "web_search/Tavily HTTP 432 on 17/17 initial required tracker/sector groups at 12Z; fallback used Google News RSS, direct UN/NATO/EIA/IAEA/OPEC/OCHA probes, terminal HTTP, energy cache and Polymarket cache.",
    "latest_source_artifact_12z": str(artifact_path.relative_to(ROOT)),
    "latest_rss_scan_keys_12z": list(counts.keys()),
    "rss_headline_counts_12z": counts,
    "official_source_probe_12z": {k: {"ok": bool(v.get("ok")), "source": k, "status": v.get("status"), "error": v.get("error")} for k, v in official.items()},
    "morning_deep_scan_movers_12z": "12Z change vs 09Z: no numeric probability moves. Pakistan-Afghanistan remains the main active rising lane at 40 critical; global remains rounded at 67/imminent.",
    "signals_changed_12z": "Canonical signals only. No new signal names added. Existing Iran/Hormuz, Israel-Lebanon, Pakistan-Afghanistan and Sudan active-signal lanes were preserved/reconfirmed in narrative; DPRK weapons-drill coverage remains watch-only and no north_korea signal was promoted.",
    "auto_detection_12z": "No untracked nuclear-escalation/alliance-spillover zone auto-added. Emerging-crisis fallback for Thailand-Cambodia/Ethiopia-Eritrea/Guyana-Venezuela/Kosovo-Serbia returned zero qualifying fresh items in this run.",
    "energy_oil_12z": "12Z pre-deploy cache: Brent $73.69 and WTI $70.48; gas $3.210, gold $4029.20. Hormuz/tanker-risk headlines are live, but pricing and traffic reports reject full-waterway-stop thresholds.",
    "allied_positions_12z": "NATO public pages reachable; allied fallback keeps eastern-flank warning language live. No treaty invocation, public direct-combat entry decision or verified Russia-NATO kinetic incident surfaced.",
    "polymarket_sanity_12z": "Polymarket cache from 2026-06-30T09:09:24Z was within the deploy refresh window; mapped markets remain horizon-mismatched sanity checks, not direct probability setters.",
    "old_probabilities_raw_12z": old_raw,
    "old_probabilities_coupled_12z": old_coupled,
    "raw_probabilities_before_coupling": {tid: state.get("trackers", {}).get(tid, {}).get("current_probability") for tid in cfg.get("trackers", {})},
    "expected_final_probabilities_after_coupling": {tid: state.get("trackers", {}).get(tid, {}).get("current_probability_with_coupling") for tid in cfg.get("trackers", {})},
    "expected_global_after_coupling": 67,
})

# Re-validate canonical signal use after update.
for tid, trk in state.get("trackers", {}).items():
    if tid not in canonical:
        raise SystemExit(f"noncanonical tracker after update: {tid}")
    bad = [s for s in trk.get("active_signals", []) if s not in cfg["trackers"][tid].get("signals", {})]
    if bad:
        raise SystemExit(f"noncanonical active signals after update for {tid}: {bad}")

fd, tmp_name = tempfile.mkstemp(prefix="current_state.", suffix=".json.tmp", dir=str(DATA))
try:
    with os.fdopen(fd, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp_name, STATE_PATH)
finally:
    if os.path.exists(tmp_name):
        os.unlink(tmp_name)

print(json.dumps({"updated": str(STATE_PATH), "timestamp": ts, "artifact": str(artifact_path), "counts": counts}, indent=2))
