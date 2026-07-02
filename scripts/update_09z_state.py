#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
ARTIFACT = DATA / "morning_deep_scan_sources_20260702T090140Z.json"

cfg = json.loads((DATA / "tracker_config.json").read_text())
state_path = DATA / "current_state.json"
state = json.loads(state_path.read_text())
artifact = json.loads(ARTIFACT.read_text())
energy = json.loads((DATA / "energy_prices.json").read_text())
pm = json.loads((DATA / "polymarket_cache.json").read_text())

old_raw = {
    tid: int(round(float(block.get("current_probability", block.get("current_prob", 0)))))
    for tid, block in state.get("trackers", {}).items()
    if tid in cfg.get("trackers", {})
}
old_coupled = {
    tid: int(round(float(block.get("current_probability_with_coupling", block.get("current_probability", 0)))))
    for tid, block in state.get("trackers", {}).items()
    if tid in cfg.get("trackers", {})
}

raw_probs = {
    "iran_conventional": 83,
    "israel_lebanon": 86,
    "turkey": 5,
    "india": 11,
    "russia": 40,
    "china": 24,
    "north_korea": 10,
    "russia_ukraine": 98,
    "pakistan_afghanistan": 44,
    "iran_nuclear": 38,
    "sudan": 86,
    "israel_palestine": 88,
    "south_sudan_abyei": 8,
}
final_probs = {
    "iran_conventional": 90,
    "israel_lebanon": 96,
    "turkey": 5,
    "india": 11,
    "russia": 50,
    "china": 26,
    "north_korea": 10,
    "russia_ukraine": 98,
    "pakistan_afghanistan": 44,
    "iran_nuclear": 46,
    "sudan": 86,
    "israel_palestine": 88,
    "south_sudan_abyei": 8,
}
trends = {
    "iran_conventional": "rising",
    "israel_lebanon": "rising",
    "turkey": "stable",
    "india": "stable",
    "russia": "stable",
    "china": "stable",
    "north_korea": "stable",
    "russia_ukraine": "stable",
    "pakistan_afghanistan": "rising",
    "iran_nuclear": "stable",
    "sudan": "stable",
    "israel_palestine": "stable",
    "south_sudan_abyei": "stable",
}
active_signals = {
    "iran_conventional": ["ceasefire_violation", "diplomacy_active", "hormuz_controlled_not_closed"],
    "israel_lebanon": ["ceasefire_violation", "diplomacy_active", "diplomacy_refused"],
    "turkey": [],
    "india": [],
    "russia": [],
    "china": [],
    "north_korea": [],
    "russia_ukraine": [],
    "pakistan_afghanistan": ["military_buildup"],
    "iran_nuclear": [],
    "sudan": ["military_buildup"],
    "israel_palestine": ["ceasefire_violation"],
    "south_sudan_abyei": [],
}
notes = {
    "iran_conventional": "09Z scan keeps Iran conventional imminent/rising: Hormuz control-risk and tanker-risk coverage persists, but Brent/WTI weakness plus traffic-recovery reporting still reject a full waterway halt; US-Iran diplomatic channels remain a watch item",
    "israel_lebanon": "09Z scan keeps Israel-Lebanon imminent/rising at 96 final: fresh south-Lebanon/Beirut strike and destruction reporting, Israeli stay-behind statements and Hezbollah spoiler risk keep the lane hot without alliance-entry confirmation",
    "turkey": "09Z scan keeps Turkey-NATO deterrent: Ankara summit/security and alliance-positioning coverage dominates; no corroborated configured Turkish strategic-arms trigger surfaced",
    "india": "09Z scan keeps India-Pakistan elevated: LoC/Poonch intruder reports remain border-security friction, not sustained exchange or major force movement",
    "russia": "09Z scan keeps Russia-NATO critical raw/imminent coupled: Baltic/Poland hybrid-action warnings remain live, with no Article 5 invocation, public direct-combat entry decision or verified kinetic incident",
    "china": "09Z scan keeps China-Taiwan critical: Taiwan blockade-response tabletop and PRC patrol-pressure coverage remain live; no configured force trigger was corroborated",
    "north_korea": "09Z scan keeps DPRK elevated: late-June weapons-demonstration and destructive-posture coverage remains watch-only; no fresh strategic-threshold event is promoted",
    "russia_ukraine": "09Z scan keeps Russia-Ukraine ceiling-level: active-war strikes, Belarus pressure and NATO-summit support commentary remain live; no NATO direct-entry breakpoint surfaced",
    "pakistan_afghanistan": "09Z scan keeps Pakistan-Afghanistan critical/rising: Pakistani border raids/strikes, Afghan civilian-casualty claims and Taliban retaliation language remain corroborated across fallback sources",
    "iran_nuclear": "09Z scan keeps Iran verification critical: agency verification and site-entry disputes remain live, but no higher-threshold technical trigger was corroborated",
    "sudan": "09Z scan keeps Sudan imminent: UN and fallback coverage keep El Obeid/Kordofan atrocity-risk, encirclement and fortification/offensive-risk reporting live",
    "israel_palestine": "09Z scan keeps Israel-Palestine imminent: Gaza fatality, West Bank pressure and UN service-risk reporting remain severe; no wider-regional breakout threshold is promoted",
    "south_sudan_abyei": "09Z scan keeps South Sudan/Abyei deterrent: thirty-day fallback returned no fresh Abyei force-escalation reporting, only UNISFA/mandate background material",
}
name_map = {
    "iran_conventional": "IRAN WAR",
    "israel_lebanon": "ISRAEL-LEBANON",
    "turkey": "TURKEY-NATO",
    "india": "INDIA-PAKISTAN",
    "russia": "RUSSIA-NATO",
    "china": "CHINA-TAIWAN",
    "north_korea": "DPRK",
    "russia_ukraine": "RUSSIA-UKRAINE",
    "pakistan_afghanistan": "PAKISTAN-AFGHANISTAN",
    "iran_nuclear": "IRAN NUCLEAR",
    "sudan": "SUDAN",
    "israel_palestine": "ISRAEL-PALESTINE",
    "south_sudan_abyei": "SOUTH SUDAN-ABYEI",
}

def zone_for(p: int) -> str:
    z = cfg.get("scoring", {}).get("zones", {})
    if p >= z.get("imminent", [50])[0]:
        return "imminent"
    if p >= z.get("critical", [25])[0]:
        return "critical"
    if p >= z.get("elevated", [10])[0]:
        return "elevated"
    return "deterrent"

# Preserve original activation times; update last_confirmed in timeline for active lanes.
timeline_path = DATA / "signal_timeline.json"
timeline = json.loads(timeline_path.read_text())
timeline.setdefault("signals", {})
for tid, sigs in active_signals.items():
    for sig in sigs:
        key = f"{tid}:{sig}"
        entry = timeline["signals"].get(key)
        if isinstance(entry, str):
            entry = {"activated_at": entry, "last_confirmed": TS}
        elif isinstance(entry, dict):
            entry = {"activated_at": entry.get("activated_at") or entry.get("last_confirmed") or TS, "last_confirmed": TS}
        else:
            entry = {"activated_at": TS, "last_confirmed": TS}
        timeline["signals"][key] = entry
# Drop anything not currently canonical/active.
allowed = {f"{tid}:{sig}" for tid, sigs in active_signals.items() for sig in sigs}
timeline["signals"] = {k: v for k, v in timeline["signals"].items() if k in allowed}

state["timestamp"] = TS
state["last_updated"] = TS
state["global_war_probability"] = 68
state["global_probability"] = 68
state["global_zone"] = "imminent"
state["global_uncertainty_index"] = 48
state["doomsday_clock_minutes"] = 3.0
state["signal_timestamps"] = {
    k: (v.get("activated_at") if isinstance(v, dict) else v)
    for k, v in timeline["signals"].items()
}

state.setdefault("zones", {})
state.setdefault("trackers", {})
for tid in cfg.get("trackers", {}).keys():
    raw = raw_probs[tid]
    final = final_probs[tid]
    boost = final - raw
    sig_ts = {sig: state["signal_timestamps"].get(f"{tid}:{sig}", TS) for sig in active_signals[tid]}
    block = {
        "name": name_map.get(tid, tid.upper()),
        "base_prob": raw,
        "current_prob": raw,
        "current_probability": raw,
        "probability": raw,
        "current_probability_with_coupling": final,
        "coupling_boost": boost,
        "zone": zone_for(final),
        "trend": trends[tid],
        "active_signals": active_signals[tid],
        "notes": notes[tid],
        "last_updated": TS,
        "signal_timestamps": sig_ts,
    }
    state["zones"][tid] = dict(block)
    state["trackers"][tid] = dict(block)

brent = energy["current"].get("BRENT_CRUDE_USD", {}).get("price")
wti = energy["current"].get("WTI_USD", {}).get("price")
gas = energy["current"].get("NATURAL_GAS_USD", {}).get("price")
gold = energy["current"].get("GOLD_USD", {}).get("price")

state["latest_news"] = [
    {
        "zone": "iran_conventional",
        "time": "09Z/24H",
        "headline": "Iran/Hormuz: restricted-transit risk persists, but flow/price evidence keeps full-halt rejected",
        "text": "web_search plus Google News RSS show Hormuz control-risk, tanker movement, military-warning coverage and diplomatic-channel reporting. Energy cache has Brent around $70.84 and WTI around $67.83, while RSS says traffic is gradually accelerating; this supports restricted or escorted transit, not zero traffic.",
        "impact": "watch",
        "sources": ["Congress CRS", "OilPrice.com", "Saudi Gazette", "Google News RSS fallback"],
        "source_date": "1-2 Jul 2026",
    },
    {
        "zone": "israel_lebanon",
        "time": "09Z/24H",
        "headline": "Israel-Lebanon: fresh strike/destruction reports keep the lane hot",
        "text": "RSS and web_search cite south-Lebanon airstrikes, Beirut destruction reporting, Israeli statements that forces will stay until further notice, and Hezbollah spoiler risk around the US-brokered framework. This confirms the prior rise but does not add a new alliance-entry break.",
        "impact": "up",
        "sources": ["Al Jazeera", "ABC News", "The Defense Post", "Google News RSS fallback"],
        "source_date": "1-2 Jul 2026",
    },
    {
        "zone": "pakistan_afghanistan",
        "time": "09Z/14D",
        "headline": "Pakistan-Afghanistan: border raid/casualty lane remains hot",
        "text": "PBS/AP, Reuters, NPR and regional fallback items report Pakistani border raids/strikes, claimed militant casualties, Afghan civilian-casualty claims and Taliban retaliation language. Probability stays critical/rising without a broader state-war break.",
        "impact": "up",
        "sources": ["PBS/AP", "Reuters", "NPR", "Al Jazeera", "Google News RSS fallback"],
        "source_date": "19 Jun-2 Jul 2026",
    },
    {
        "zone": "sudan",
        "time": "09Z/7D",
        "headline": "Sudan: El Obeid/Kordofan atrocity risk remains severe",
        "text": "UN News and fallback coverage keep El Obeid/Kordofan risk, RSF pressure, city fortification and humanitarian-corridor stress live. No easing source displaced the severe Sudan lane.",
        "impact": "up",
        "sources": ["UN News", "OHCHR", "Sudan Tribune", "Google News RSS fallback"],
        "source_date": "26 Jun-2 Jul 2026",
    },
    {
        "zone": "israel_palestine",
        "time": "09Z/24H",
        "headline": "Israel-Palestine: Gaza fatalities and West Bank pressure remain acute",
        "text": "Fallback and UN-linked material show fresh Gaza fatality coverage, West Bank pressure, child-casualty concerns and service-risk coverage. Severe local conflict continues without a new regional-breakout threshold.",
        "impact": "up",
        "sources": ["UNRWA", "Al Jazeera", "IMEMC", "Google News RSS fallback"],
        "source_date": "1-2 Jul 2026",
    },
    {
        "zone": "iran_nuclear",
        "time": "09Z/7D",
        "headline": "Iran nuclear: verification remains the core bottleneck",
        "text": "web_search and RSS cite a reported route for agency site-entry under the US-Iran arrangement, while Tehran pushback and verification disputes continue. No higher-enrichment, device, or new underground-site threshold was corroborated.",
        "impact": "watch",
        "sources": ["Reuters", "Al Jazeera", "RFE/RL", "IAEA document index", "Google News RSS fallback"],
        "source_date": "25 Jun-2 Jul 2026",
    },
    {
        "zone": "russia",
        "time": "09Z/7D",
        "headline": "Russia-NATO: Baltic/Poland hybrid warnings remain live",
        "text": "Guardian, Polish/Latvian intelligence commentary and allied fallback keep limited-provocation warnings against Baltic states or Poland live. No treaty invocation, public direct-combat entry decision or verified kinetic incident surfaced.",
        "impact": "watch",
        "sources": ["The Guardian", "UNITED24 Media", "Kyiv Post", "Google News RSS fallback"],
        "source_date": "25 Jun-2 Jul 2026",
    },
    {
        "zone": "china",
        "time": "09Z/7D",
        "headline": "China-Taiwan: blockade-response tabletop and patrol pressure stay on watch",
        "text": "Reuters and Taiwan-focused fallback cite Taipei blockade-response tabletop activity and continued PRC patrol-pressure framing. This keeps Taiwan critical, but no configured Chinese force trigger was confirmed.",
        "impact": "watch",
        "sources": ["Reuters", "ISW/AEI", "Washington Times", "Google News RSS fallback"],
        "source_date": "25-28 Jun 2026",
    },
    {
        "zone": "north_korea",
        "time": "09Z/7D",
        "headline": "DPRK: weapons demonstrations remain watch-only",
        "text": "Al Jazeera, ABC and regional fallback items cite late-June weapons demonstrations and destructive-posture language, while Seoul/Japan coordination coverage continues. No fresh strategic-threshold event is promoted in this scan.",
        "impact": "watch",
        "sources": ["Al Jazeera", "ABC News", "Yonhap", "Google News RSS fallback"],
        "source_date": "26-29 Jun 2026",
    },
    {
        "zone": "russia_ukraine",
        "time": "09Z/24H",
        "headline": "Russia-Ukraine: active-war ceiling persists; Belarus/NATO commentary stays noisy",
        "text": "Fallback results show Ukraine strike coverage, Belarus pressure commentary and NATO-summit support planning, but no verified NATO combat-entry breakpoint. Russia-Ukraine remains at the ceiling because the war is active, not because a new strategic threshold fired.",
        "impact": "watch",
        "sources": ["Independent", "Reuters", "Defence24", "Google News RSS fallback"],
        "source_date": "1-2 Jul 2026",
    },
    {
        "zone": "turkey",
        "time": "09Z/14D",
        "headline": "Turkey-NATO: summit security dominates; no configured arms trigger",
        "text": "web_search found Ankara summit/security coverage and alliance-positioning analysis; Google News RSS returned zero Turkey configured-trigger hits in the 14-day fallback scan.",
        "impact": "neutral",
        "sources": ["Washington Post/AP", "NATO", "Modern War Institute", "Google News RSS fallback"],
        "source_date": "27 Jun-2 Jul 2026",
    },
    {
        "zone": "india",
        "time": "09Z/14D",
        "headline": "India-Pakistan: LoC intrusion reports remain contained",
        "text": "Times of India/Rediff fallback reports Pakistani intruder detentions near the LoC in Poonch. This remains elevated border friction, not sustained exchange or major force movement.",
        "impact": "neutral",
        "sources": ["Times of India", "Rediff", "Google News RSS fallback"],
        "source_date": "27-29 Jun 2026",
    },
    {
        "zone": "south_sudan_abyei",
        "time": "09Z/30D",
        "headline": "South Sudan/Abyei: no fresh qualifying force-escalation reporting",
        "text": "The fallback scan returned no fresh Abyei qualifying reports; public material remains UNISFA mandate/background and broader South Sudan fragility.",
        "impact": "neutral",
        "sources": ["UNISFA", "Al Jazeera", "Google News RSS fallback"],
        "source_date": "30d scan through 2 Jul 2026",
    },
    {
        "zone": "oil_energy",
        "time": "09Z/24H",
        "headline": "Energy/oil sanity: Hormuz risk visible, but prices do not support full halt",
        "text": f"OilPriceAPI refresh: Brent ${brent}, WTI ${wti}, gas ${gas}, gold ${gold}. RSS headlines say Hormuz fears are easing as traffic rebounds, despite two-way risk. Full-waterway-halt thresholds are rejected.",
        "impact": "neutral",
        "sources": ["OilPriceAPI", "EnergyNow", "Markets.com", "Google News RSS fallback"],
        "source_date": "2 Jul 2026",
    },
    {
        "zone": "iaea_un",
        "time": "09Z/7D",
        "headline": "IAEA/UN: verification pathway reported, direct IAEA pages still partially blocked",
        "text": "Reuters and Google News RSS cite a reported route for agency site-entry under the Iran arrangement; direct IAEA news/press pages returned HTTP 403 through terminal HTTP, so detailed agency material is corroborated through wires and public indexes.",
        "impact": "watch",
        "sources": ["Reuters", "IAEA document index", "Al Jazeera", "Google News RSS fallback"],
        "source_date": "25 Jun-2 Jul 2026",
    },
    {
        "zone": "nato_allied",
        "time": "09Z/7D",
        "headline": "NATO/allied positions: eastern-flank deterrence debate remains live",
        "text": "NATO pages were reachable; allied fallback keeps eastern-flank deterrence, US-reliability debate and Baltic/Poland warning coverage live. No Article 5 invocation or verified Russia-NATO kinetic incident surfaced.",
        "impact": "watch",
        "sources": ["NATO", "The Guardian", "Atlantic Council", "Google News RSS fallback"],
        "source_date": "25 Jun-2 Jul 2026",
    },
    {
        "zone": "emerging_7d",
        "time": "09Z/7D",
        "headline": "Emerging auto-detection: no untracked zone met add threshold",
        "text": "Thailand-Cambodia, Ethiopia-Eritrea, Guyana-Venezuela and Kosovo-Serbia broad checks did not produce enough fresh corroborated escalation items to add a new tracker.",
        "impact": "neutral",
        "sources": ["web_search", "Google News RSS fallback"],
        "source_date": "7d scan through 2 Jul 2026",
    },
]

meta = state.setdefault("_meta", {})
meta.update({
    "last_writer": "doomsdaywatch_09z_morning_deep_scan_cron",
    "last_scan": TS,
    "scan_time_utc": TS,
    "analysis_window": "09z_morning_deep_scan_past_24h_with_7d_14d_30d_sparse_crosschecks_web_search_google_news_rss_official_feed_energy_polymarket_sanity_checks",
    "search_engine": "public_safe_multi_source_fallback",
    "source_limitation": "Source mix: web_search, Google News RSS fallback, direct official/feed probes, market data, and Polymarket cache. web_search succeeded but was uneven/stale in several lanes; direct IAEA/OPEC pages returned HTTP 403 and OCHA oPt/UN Sudan tag feeds returned 404, so single-source claims remain watch items until corroborated.",
    "source_fallback_detail_09z": f"web_search attempted for 17/17 required tracker/sector groups and returned results, but recall was uneven/stale in several lanes; fallback artifact {ARTIFACT.relative_to(ROOT)} used Google News RSS plus direct UN/NATO/EIA/IAEA/OPEC/OCHA probes. Direct IAEA/OPEC pages returned HTTP 403; OCHA oPt and UN Sudan tag feeds returned 404.",
    "latest_source_artifact_09z": str(ARTIFACT.relative_to(ROOT)),
    "latest_rss_scan_keys_09z": list(artifact.get("rss", {}).keys()),
    "rss_headline_counts_09z": artifact.get("counts", {}),
    "official_source_probe_09z": {k: {"ok": v.get("ok"), "status": v.get("status")} for k, v in artifact.get("official", {}).items()},
    "morning_deep_scan_movers_09z": "09Z change vs 06Z: no numeric probability moves. Iran conventional remains the top rising Iran lane after continued Hormuz controlled-transit/tanker-risk reporting with energy prices rejecting full closure; Israel-Lebanon remains the hottest non-Ukraine coupled lane at 96 final; Pakistan-Afghanistan remains the main non-Mideast rising lane at 44 critical. Global remains rounded at 68/imminent.",
    "signals_changed_09z": "Canonical signals only. No new signal names added. Existing Iran/Hormuz, Israel-Lebanon, Pakistan-Afghanistan, Sudan and Israel-Palestine active lanes were preserved/reconfirmed from fresh fallback evidence; no DPRK configured signal was promoted. No untracked zone was auto-added.",
    "auto_detection_09z": "No untracked nuclear-escalation/alliance-spillover zone auto-added. Emerging-crisis fallback for Thailand-Cambodia/Ethiopia-Eritrea/Guyana-Venezuela/Kosovo-Serbia returned zero qualifying fresh items in this run.",
    "energy_oil_09z": f"09Z pre-deploy refresh: Brent ${brent} and WTI ${wti}; gas ${gas}, gold ${gold}. Hormuz/tanker-risk headlines remain visible, but price and traffic-recovery reports still reject full-waterway-halt thresholds.",
    "allied_positions_09z": "NATO public pages reachable; allied fallback keeps eastern-flank warning, US-reliability debate and Ankara-summit deterrence preparations live. No Article 5 invocation, public direct-combat entry decision or verified Russia-NATO kinetic incident surfaced.",
    "polymarket_sanity_09z": f"Pre-deploy Polymarket cache fetched_at={pm.get('fetched_at')}; mapped markets remain horizon-mismatched sanity checks, not direct probability setters. Deploy refresh path will update if upstream allows.",
    "old_probabilities_raw_09z": old_raw,
    "old_probabilities_coupled_09z": old_coupled,
    "raw_probabilities_before_coupling_09z": raw_probs,
    "expected_final_probabilities_after_coupling_09z": final_probs,
    "raw_global_probability_09z": 67.82,
    "latest_source_artifact": str(ARTIFACT.relative_to(ROOT)),
    "latest_rss_scan_keys": list(artifact.get("rss", {}).keys()),
    "rss_headline_counts": artifact.get("counts", {}),
    "official_source_probe": {k: {"ok": v.get("ok"), "status": v.get("status"), "title": v.get("title"), "url": v.get("url")} for k, v in artifact.get("official", {}).items()},
    "auto_detection": "No untracked nuclear-escalation/alliance-spillover zone auto-added. Emerging-crisis fallback for Thailand-Cambodia/Ethiopia-Eritrea/Guyana-Venezuela/Kosovo-Serbia returned zero qualifying fresh items in this run.",
    "signals_changed": "Canonical signals only. No new signal names added. Existing Iran/Hormuz, Israel-Lebanon, Pakistan-Afghanistan, Sudan and Israel-Palestine active lanes were preserved/reconfirmed; no DPRK configured signal promoted; no untracked zone auto-added.",
    "energy_oil": f"09Z pre-deploy refresh: Brent ${brent} and WTI ${wti}; gas ${gas}, gold ${gold}. Hormuz/tanker-risk headlines remain visible, but price and traffic-recovery reports still reject full-waterway-halt thresholds.",
    "allied_positions": "NATO public pages reachable; allied fallback keeps eastern-flank warning and deterrence debate live. No Article 5 invocation, public direct-combat entry decision or verified Russia-NATO kinetic incident surfaced.",
    "polymarket_sanity": f"Pre-deploy Polymarket cache fetched_at={pm.get('fetched_at')}; mapped markets remain horizon-mismatched sanity checks, not direct probability setters.",
})

# Atomic writes.
state_tmp = state_path.with_suffix(".json.tmp")
state_tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
os.replace(state_tmp, state_path)

tl_tmp = timeline_path.with_suffix(".json.tmp")
tl_tmp.write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + "\n")
os.replace(tl_tmp, timeline_path)

print(json.dumps({
    "updated": str(state_path),
    "timestamp": TS,
    "global_probability": state["global_probability"],
    "global_zone": state["global_zone"],
    "raw_probabilities": raw_probs,
    "final_probabilities": final_probs,
    "artifact": str(ARTIFACT.relative_to(ROOT)),
}, indent=2))
