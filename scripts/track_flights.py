#!/usr/bin/env python3
"""Flight tracking via OpenSky Network API.
Detects airspace closures and unusual patterns over conflict zones.
Stores results in data/flight_tracking.json for deploy script."""

import json
import os
import urllib.request
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
FLIGHT_FILE = os.path.join(DATA_DIR, "flight_tracking.json")

# Conflict zones: bounding boxes [lamin, lomin, lamax, lomax]
CONFLICT_ZONES = {
    "persian_gulf": {
        "name": "Persian Gulf / Strait of Hormuz",
        "bbox": [24.0, 49.0, 28.5, 57.0],
        "baseline_flights": 80,  # normal hourly flight count (pre-conflict)
    },
    "eastern_mediterranean": {
        "name": "Eastern Mediterranean / Cyprus",
        "bbox": [33.0, 28.0, 36.5, 37.0],
        "baseline_flights": 120,
    },
    "red_sea_south": {
        "name": "Red Sea / Bab el-Mandeb",
        "bbox": [11.0, 41.0, 15.0, 45.0],
        "baseline_flights": 60,
    },
    "red_sea_north": {
        "name": "Red Sea / Jeddah",
        "bbox": [19.0, 37.0, 23.0, 42.0],
        "baseline_flights": 50,
    },
    "turkey_syria": {
        "name": "Turkey-Syria-Iraq Border",
        "bbox": [35.0, 35.0, 38.5, 41.0],
        "baseline_flights": 40,
    },
}

def fetch_flights(bbox):
    """Fetch flights in a bounding box from OpenSky."""
    lamin, lomin, lamax, lomax = bbox
    url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "DoomsdayWatch/1.0",
            "Accept": "application/json"
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
            return data.get("states", []) or []
    except Exception as e:
        return None

def fetch_all_zones():
    """Fetch all zones in parallel using threading."""
    import concurrent.futures
    
    results = {}
    def fetch_one(zone_id, zone):
        states = fetch_flights(zone["bbox"])
        return zone_id, zone, states
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_one, zid, z): zid for zid, z in CONFLICT_ZONES.items()}
        for future in concurrent.futures.as_completed(futures):
            zone_id, zone, states = future.result()
            results[zone_id] = (zone, states)
    
    return results

def analyze_flights(states, zone_config):
    """Analyze flight data for a zone."""
    if states is None:
        return None
    
    flights = []
    country_counts = {}
    military = []
    high_speed = []
    
    for s in states:
        callsign = (s[1] or "").strip()
        country = s[2] or "Unknown"
        lon = s[5]
        lat = s[6]
        alt = s[7]  # meters
        on_ground = s[8]
        velocity = s[9] or 0  # m/s
        heading = s[10]
        squawk = s[14]
        category = s[17] if len(s) > 17 else 0
        
        # Track country counts
        country_counts[country] = country_counts.get(country, 0) + 1
        
        # Build flight record
        flight = {
            "callsign": callsign,
            "country": country,
            "lat": round(lat, 4) if lat else None,
            "lon": round(lon, 4) if lon else None,
            "alt_m": round(alt) if alt else None,
            "velocity_ms": round(velocity),
            "heading": round(heading) if heading else None,
            "on_ground": on_ground,
            "squawk": squawk,
        }
        flights.append(flight)
        
        # Military detection (squawk 7700/7600/7500 or military country patterns)
        if country in ["United States", "United Kingdom", "France", "Turkey", "Israel", "Iran"]:
            if callsign.startswith(("UAE", "BAF", "FAF", "RCH", "SAM", "NWO", "TUAF", "IRI")):
                military.append({"callsign": callsign, "country": country, "alt": alt})
        
        # High speed detection (fighter jets)
        if velocity > 250 and alt > 3000 and not on_ground:  # >250 m/s = 900 km/h
            high_speed.append({"callsign": callsign, "speed_kmh": round(velocity * 3.6), "alt": alt})
    
    # Calculate disruption
    flight_count = len(flights)
    baseline = zone_config["baseline_flights"]
    disruption_pct = round((1 - flight_count / baseline) * 100) if baseline > 0 else 0
    
    return {
        "flight_count": flight_count,
        "baseline_flights": baseline,
        "disruption_pct": disruption_pct,
        "top_countries": dict(sorted(country_counts.items(), key=lambda x: -x[1])[:5]),
        "military": military[:10],
        "high_speed": high_speed[:5],
    }

def load_tracking():
    try:
        with open(FLIGHT_FILE) as f:
            return json.load(f)
    except:
        return {"zones": {}, "history": [], "signals": []}

def save_tracking(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FLIGHT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main():
    data = load_tracking()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    print(f"Flight tracking update — {now}")
    
    # Fetch all zones in parallel
    print("  Fetching all zones (parallel)...")
    all_zones = fetch_all_zones()
    
    new_signals = []
    zone_results = {}
    
    for zone_id, (zone, states) in all_zones.items():
        analysis = analyze_flights(states, zone)
        
        if analysis is None:
            print(f"  {zone['name']}: API ERROR")
            continue
        
        print(f"  {zone['name']}: {analysis['flight_count']} flights ({analysis['disruption_pct']}% disruption)")
        
        zone_results[zone_id] = {
            "name": zone["name"],
            **analysis,
            "updated_at": now,
        }
        
        # Generate signals for significant disruptions
        if analysis["disruption_pct"] >= 70 and analysis["flight_count"] > 0:
            sig = f"airspace_{zone_id}_closed"
            new_signals.append({
                "signal": sig,
                "zone": zone_id,
                "zone_name": zone["name"],
                "type": "airspace_closed",
                "disruption_pct": analysis["disruption_pct"],
                "flights_remaining": analysis["flight_count"],
                "confidence": "high" if analysis["disruption_pct"] >= 90 else "medium",
                "time": now,
            })
            print(f"  ⚠️  SIGNAL: {zone['name']} largely closed to traffic")
        elif analysis["disruption_pct"] >= 40:
            sig = f"airspace_{zone_id}_restricted"
            new_signals.append({
                "signal": sig,
                "zone": zone_id,
                "zone_name": zone["name"],
                "type": "airspace_restricted",
                "disruption_pct": analysis["disruption_pct"],
                "flights_remaining": analysis["flight_count"],
                "confidence": "medium",
                "time": now,
            })
        
        # Military activity signal
        if len(analysis["military"]) > 3:
            sig = f"military_activity_{zone_id}"
            new_signals.append({
                "signal": sig,
                "zone": zone_id,
                "zone_name": zone["name"],
                "type": "military_activity",
                "military_count": len(analysis["military"]),
                "confidence": "medium",
                "time": now,
            })
    
    # Update data
    data["zones"] = zone_results
    data["last_updated"] = now
    data["signals"] = new_signals
    
    # Add to history (keep last 48 entries = 48 hours at hourly)
    history_entry = {"timestamp": now, "zones": {}}
    for zid, zdata in zone_results.items():
        history_entry["zones"][zid] = {
            "flight_count": zdata["flight_count"],
            "disruption_pct": zdata["disruption_pct"],
        }
    data["history"].append(history_entry)
    data["history"] = data["history"][-48:]
    
    save_tracking(data)
    
    print(f"\nSignals generated: {len(new_signals)}")
    for s in new_signals:
        print(f"  [{s['confidence'].upper()}] {s['zone_name']}: {s['type']} — {s.get('disruption_pct', '?')}% disruption")
    
    print(f"\nData saved to {FLIGHT_FILE}")

if __name__ == "__main__":
    main()
