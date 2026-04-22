#!/usr/bin/env python3
"""
probabilities.py — Zone classification and global probability calculation.

Extracted from pipeline.py for DoomsdayWatch modular architecture.
"""


def classify_zone(p, zone_thresholds):
    """Map a probability value (0-100) to a threat zone string.

    Uses config-defined thresholds with sensible defaults.
    """
    if p >= zone_thresholds.get("imminent", {}).get("min", 60):
        return "imminent"
    elif p >= zone_thresholds.get("critical", {}).get("min", 30):
        return "critical"
    elif p >= zone_thresholds.get("elevated", {}).get("min", 15):
        return "elevated"
    else:
        return "deterrent"


def calculate_global_probability(all_probs, cfg):
    """Compute weighted global threat score from per-tracker probabilities.

    Uses global_weights from tracker_config.json. Falls back to equal weighting
    (0.08 each) for trackers not listed in weights.

    Returns (global_prob_int, zone_string).
    """
    weights = cfg.get("global_weights", {
        "iran_nuclear": 0.12,
        "iran_conventional": 0.18,
        "israel_lebanon": 0.14,
        "russia_ukraine": 0.16,
        "turkey": 0.06,
        "india": 0.06,
        "pakistan_afghanistan": 0.08,
        "russia": 0.06,
        "china": 0.06,
        "north_korea": 0.08,
    })
    gp = round(
        sum(all_probs.get(k, 10) * weights.get(k, 0.08) for k in all_probs)
    )
    zone_thresholds = cfg.get("scoring", {}).get("zones", {})
    tz = classify_zone(gp, zone_thresholds)
    return gp, tz
