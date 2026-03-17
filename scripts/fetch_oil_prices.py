#!/usr/bin/env python3
"""Fetch oil prices from OilPriceAPI demo endpoint (no key required).
Stores in data/energy_prices.json with history for charting."""

import json
import os
import urllib.request
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
PRICES_FILE = os.path.join(DATA_DIR, "energy_prices.json")

def fetch_prices():
    """Fetch current oil/gas prices from demo endpoint."""
    url = "https://api.oilpriceapi.com/v1/demo/prices"
    req = urllib.request.Request(url, headers={"User-Agent": "DoomsdayWatch/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"API fetch failed: {e}")
        return None
    
    if data.get("status") != "success":
        print(f"API error: {data}")
        return None
    
    return data["data"]["prices"]

def load_prices():
    """Load existing price history."""
    try:
        with open(PRICES_FILE) as f:
            return json.load(f)
    except:
        return {"current": {}, "history": [], "baselines": {}}

def save_prices(data):
    """Save price data."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PRICES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main():
    prices = fetch_prices()
    if not prices:
        print("Failed to fetch prices")
        return
    
    data = load_prices()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Update current prices
    current = {}
    for p in prices:
        code = p["code"]
        current[code] = {
            "name": p["name"],
            "price": p["price"],
            "currency": p["currency"],
            "updated_at": p["updated_at"],
            "change_24h": p.get("change_24h", 0)
        }
    
    data["current"] = current
    data["last_updated"] = now
    
    # Ensure all baselines exist (pre-conflict prices from ~March 1 2026)
    # Merge mode: adds missing baselines without overwriting existing ones
    default_baselines = {
        "BRENT_CRUDE_USD": {"price": 67.4, "date": "2026-03-01", "note": "Pre-conflict baseline"},
        "WTI_USD": {"price": 63.8, "date": "2026-03-01", "note": "Pre-conflict baseline"},
        "NATURAL_GAS_USD": {"price": 2.85, "date": "2026-03-01", "note": "Pre-conflict baseline"},
        "GOLD_USD": {"price": 2890.0, "date": "2026-03-01", "note": "Pre-conflict baseline"},
        "EUR_USD": {"price": 1.0420, "date": "2026-03-01", "note": "Pre-conflict baseline"},
        "GBP_USD": {"price": 1.2480, "date": "2026-03-01", "note": "Pre-conflict baseline"},
        "HEATING_OIL_USD": {"price": 2.38, "date": "2026-03-01", "note": "Pre-conflict baseline"},
        "GASOLINE_USD": {"price": 2.12, "date": "2026-03-01", "note": "Pre-conflict baseline"},
        "DIESEL_USD": {"price": 2.45, "date": "2026-03-01", "note": "Pre-conflict baseline"},
    }
    for code, baseline in default_baselines.items():
        if code not in data.get("baselines", {}):
            data.setdefault("baselines", {})[code] = baseline
    
    # Add to history (keep last 168 entries = 1 week at hourly)
    history_entry = {"timestamp": now, "prices": {}}
    for p in prices:
        history_entry["prices"][p["code"]] = p["price"]
    data["history"].append(history_entry)
    data["history"] = data["history"][-168:]
    
    # Calculate changes from baseline
    changes = {}
    for code, info in current.items():
        baseline = data["baselines"].get(code, {}).get("price")
        if baseline:
            pct = round((info["price"] - baseline) / baseline * 100, 1)
            changes[code] = {
                "baseline": baseline,
                "current": info["price"],
                "change_pct": pct,
                "change_usd": round(info["price"] - baseline, 2)
            }
    data["changes"] = changes
    
    save_prices(data)
    
    # Print summary
    print(f"Energy prices updated — {now}")
    for code, info in current.items():
        chg = changes.get(code, {})
        pct = chg.get("change_pct", 0)
        arrow = "▲" if pct > 0 else "▼" if pct < 0 else "●"
        print(f"  {arrow} {info['name']}: ${info['price']} ({'+' if pct > 0 else ''}{pct}% from pre-conflict)")

if __name__ == "__main__":
    main()
