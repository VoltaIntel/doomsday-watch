#!/usr/bin/env python3
"""Flight tracking via Aviationstack API (free tier: 100 req/month).
Runs once daily to get accurate baseline from commercial flight data.
Supplemented by OpenSky (free, unlimited) for secondary checks.
Stores in data/flight_tracking.json."""

import json
import os
import urllib.request
from datetime import datetime, timezone, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
FLIGHT_FILE = os.path.join(DATA_DIR, "flight_tracking.json")

# API key — get free at aviationstack.com/signup (100 req/month)
API_KEY = os.environ.get("AVIATIONSTACK_KEY", "")

# Key airports in conflict zones — query each = 1 request
# Grouped by zone, pick the most representative airport per zone
ZONE_AIRPORTS = {
    "persian_gulf": {
        "name": "Persian Gulf / Strait of Hormuz",
        "airports": ["DXB", "DOH", "AUH"],  # Dubai, Doha, Abu Dhabi
        "baseline_daily_flights": 1200,  # normal daily departures from these 3
    },
    "red_sea": {
        "name": "Red Sea / Jeddah",
        "airports": ["JED", "MED"],  # Jeddah, Medina
        "baseline_daily_flights": 250,
    },
    "eastern_med": {
        "name": "Eastern Mediterranean",
        "airports": ["LCA", "BEY", "TLV"],  # Larnaca, Beirut, Tel Aviv
        "baseline_daily_flights": 350,
    },
    "turkey_south": {
        "name": "Southern Turkey / Northern Syria",
        "airports": ["IST", "GZT", "ADA"],  # Istanbul, Gaziantep, Adana
        "baseline_daily_flights": 500,
    },
    "iraq": {
        "name": "Iraq",
        "airports": ["BGW", "EBL"],  # Baghdad, Erbil
        "baseline_daily_flights": 100,
    },
}

def fetch_airport_flights(airport_code, date_str):
    """Fetch flights for an airport from Aviationstack."""
    url = (f"https://api.aviationstack.com/v1/flights"
           f"?access_key={API_KEY}"
           f"&dep_iata={airport_code}"
           f"&limit=100")
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DoomsdayWatch/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  API error for {airport_code}: {e}")
        return None

def analyze_airport(data):
    """Extract flight count and status from airport response."""
    if not data or "data" not in data:
        return None
    
    flights = data["data"]
    total = len(flights)
    
    # Count by status
    statuses = {}
    for f in flights:
        status = f.get("flight_status", "unknown")
        statuses[status] = statuses.get(status, 0) + 1
    
    # Active flights (scheduled, en-route, landed = operating)
    active = statuses.get("scheduled", 0) + statuses.get("en-route", 0) + statuses.get("landed", 0)
    cancelled = statuses.get("cancelled", 0)
    
    return {
        "total": total,
        "active": active,
        "cancelled": cancelled,
        "statuses": statuses,
    }

def load_tracking():
    try:
        with open(FLIGHT_FILE) as f:
            return json.load(f)
    except:
        return {"zones": {}, "history": [], "signals": [], "last_updated": ""}

def save_tracking(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FLIGHT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main():
    if not API_KEY:
        print("ERROR: Set AVIATIONSTACK_KEY environment variable")
        print("Get free key at https://aviationstack.com/signup")
        return
    
    data = load_tracking()
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    
    print(f"Aviationstack flight tracking — {date_str}")
    print(f"Requests remaining: ~100/month (twice daily = ~60/month)")
    
    zone_results = {}
    new_signals = []
    requests_used = 0
    
    for zone_id, zone in ZONE_AIRPORTS.items():
        zone_flights = 0
        zone_active = 0
        zone_cancelled = 0
        airport_results = []
        
        for airport in zone["airports"]:
            print(f"  Querying {airport}...", end=" ")
            result = fetch_airport_flights(airport, date_str)
            requests_used += 1
            
            if not result:
                print("ERROR")
                continue
            
            analysis = analyze_airport(result)
            if not analysis:
                print("NO DATA")
                continue
            
            print(f"{analysis['active']} active, {analysis['cancelled']} cancelled")
            zone_flights += analysis["total"]
            zone_active += analysis["active"]
            zone_cancelled += analysis["cancelled"]
            airport_results.append({"airport": airport, **analysis})
            
            import time
            time.sleep(1)  # Small delay between requests
        
        # Calculate disruption
        baseline = zone["baseline_daily_flights"]
        if baseline > 0:
            expected_per_request = baseline / len(zone["airports"])
            disruption_pct = max(0, round((1 - zone_active / max(baseline, 1)) * 100))
            # Adjust: compare against fraction of baseline we actually queried
            expected_fractional = baseline * (len(airport_results) / len(zone["airports"]))
            disruption_pct = max(0, round((1 - zone_active / max(expected_fractional, 1)) * 100))
        else:
            disruption_pct = 0
        
        zone_results[zone_id] = {
            "name": zone["name"],
            "airports": airport_results,
            "total_flights": zone_flights,
            "active_flights": zone_active,
            "cancelled_flights": zone_cancelled,
            "baseline_daily_flights": baseline,
            "disruption_pct": disruption_pct,
            "updated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        
        print(f"  → {zone['name']}: {zone_active} active flights, {disruption_pct}% disruption")
        
        # Generate signals
        if disruption_pct >= 70:
            new_signals.append({
                "signal": f"airspace_{zone_id}_closed",
                "zone": zone_id,
                "zone_name": zone["name"],
                "type": "airspace_closed",
                "disruption_pct": disruption_pct,
                "active_flights": zone_active,
                "baseline": baseline,
                "confidence": "high" if disruption_pct >= 90 else "medium",
                "source": "aviationstack",
                "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            })
        elif disruption_pct >= 40:
            new_signals.append({
                "signal": f"airspace_{zone_id}_restricted",
                "zone": zone_id,
                "zone_name": zone["name"],
                "type": "airspace_restricted",
                "disruption_pct": disruption_pct,
                "active_flights": zone_active,
                "baseline": baseline,
                "confidence": "medium",
                "source": "aviationstack",
                "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            })
        
        # High cancellation rate signal
        if zone_cancelled > 0 and zone_flights > 0:
            cancel_pct = round(zone_cancelled / zone_flights * 100)
            if cancel_pct >= 20:
                new_signals.append({
                    "signal": f"flights_cancelled_{zone_id}",
                    "zone": zone_id,
                    "zone_name": zone["name"],
                    "type": "high_cancellations",
                    "cancellation_pct": cancel_pct,
                    "cancelled": zone_cancelled,
                    "confidence": "medium",
                    "source": "aviationstack",
                    "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                })
    
    # Update data
    data["zones"] = zone_results
    data["last_updated"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    data["signals"] = new_signals
    data["api_used"] = "aviationstack"
    data["requests_this_run"] = requests_used
    
    # Add to history (keep 31 entries = 1 month at daily)
    history_entry = {
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "zones": {zid: {"active": zd["active_flights"], "disruption": zd["disruption_pct"]} for zid, zd in zone_results.items()}
    }
    data["history"] = data.get("history", [])
    data["history"].append(history_entry)
    data["history"] = data["history"][-31:]
    
    save_tracking(data)
    
    print(f"\nRequests used: {requests_used}")
    print(f"Signals: {len(new_signals)}")
    for s in new_signals:
        print(f"  [{s['confidence'].upper()}] {s['zone_name']}: {s['type']} — {s.get('disruption_pct', s.get('cancellation_pct', '?'))}%")

if __name__ == "__main__":
    main()
