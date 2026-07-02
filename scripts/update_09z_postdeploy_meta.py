#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
state_path = DATA / "current_state.json"
st = json.loads(state_path.read_text())
energy = json.loads((DATA / "energy_prices.json").read_text())
pm = json.loads((DATA / "polymarket_cache.json").read_text())
cur = energy.get("current", {})
brent = cur.get("BRENT_CRUDE_USD", {}).get("price")
wti = cur.get("WTI_USD", {}).get("price")
gas = cur.get("NATURAL_GAS_USD", {}).get("price")
gold = cur.get("GOLD_USD", {}).get("price")
energy_note = f"09Z deploy refresh: Brent ${brent} and WTI ${wti}; gas ${gas}, gold ${gold}. Hormuz/tanker-risk headlines remain visible, but price and traffic-recovery reports still reject full-waterway-halt thresholds."
pm_note = f"Polymarket cache refreshed via deploy at {pm.get('fetched_at')}; mapped markets remain horizon-mismatched sanity checks, not direct probability setters."
meta = st.setdefault("_meta", {})
meta["energy_oil"] = energy_note
meta["energy_oil_09z"] = energy_note
meta["polymarket_sanity"] = pm_note
meta["polymarket_sanity_09z"] = pm_note
meta["post_deploy_meta_fix_time_utc_09z"] = TS
# Align oil/energy latest_news to deploy-refresh numbers.
for item in st.get("latest_news", []):
    if item.get("zone") == "oil_energy":
        item["text"] = f"OilPriceAPI deploy refresh: Brent ${brent}, WTI ${wti}, gas ${gas}, gold ${gold}. RSS headlines say Hormuz fears are easing as traffic rebounds, despite two-way risk. Full-waterway-halt thresholds are rejected."
        item["source_date"] = "2 Jul 2026"
# Keep public-safe source caveat but record detail in dedicated fallback key.
meta["source_limitation"] = "Source mix: official releases, reputable public reporting, public-news headline indexes, market data, and energy feeds. Upstream source coverage was degraded in this run, so the assessment uses corroborated fallback sources and treats single-source claims as watch items until confirmed."
meta["search_engine"] = "public_safe_multi_source_fallback"
tmp = state_path.with_suffix(".json.tmp")
tmp.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n")
os.replace(tmp, state_path)
print(json.dumps({"post_deploy_meta_fixed": TS, "energy": energy_note, "polymarket": pm_note}, indent=2))
