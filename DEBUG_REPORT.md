# DoomsdayWatch Dashboard — Debug Report

**Date:** 2026-03-17
**Auditor:** Hunter Alpha (Coder Agent)
**Files Reviewed:**
- `scripts/deploy.sh` (~800 lines)
- `data/tracker_config.json`
- `data/current_state.json`
- `data/source_credibility.json`
- `data/probability_history.json`

---

## CRITICAL BUGS (Must Fix)

### 1. Timeline Dictionary Path Mismatch — Expired Signals Never Cleaned

**Severity:** HIGH — Signals never expire, they accumulate forever.

In `apply_temporal_decay()` and the signal merge section, the timeline is read as:
```python
activated_at = timeline.get(timeline_key)  # timeline["signals"] is a DICT, not the root
```

But `timeline` is the **full object** `{"signals": {key: timestamp}}`. The correct path is `timeline["signals"].get(timeline_key)`.

**Consequence:** Every signal that's in `active_signals` but was set by the cron agent (not found via news) will have `activated_at = None` (because `timeline.get("tracker:signal")` returns `None`), causing this branch to fire:
```python
else:
    timeline["signals"][timeline_key] = now_iso
    still_valid.add(s)
```
This means:
- Signals get a **fresh timestamp every cycle**, resetting their decay clock
- Expired signals are never removed
- The timeline grows unboundedly with stale entries
- Agent-set signals effectively **never expire**

**Fix:** Change `timeline.get(timeline_key)` → `timeline["signals"].get(timeline_key)`

---

### 2. Zone Threshold Mismatch Between Config and Deploy Script

**Severity:** HIGH — Global probability uses wrong zone boundaries.

`tracker_config.json` defines:
```
deterrent: 0-15, elevated: 15-30, critical: 30-60, imminent: 60-100
```

`deploy.sh` global probability zone calculation uses:
```
deterrent: 0-15, elevated: 15-30, critical: 30-60, imminent: 60-100
```

**BUT** the comments and the original task spec say:
```
0-10=deterrent, 10-25=elevated, 25-50=critical, 50+=imminent
```

This confusion exists because per-tracker zones use the `scoring.zones` from config, while the global zone calculation is hardcoded in the deploy script with **different thresholds** (0-15-30-60 vs the comment's 0-10-25-50). Currently the global zone code matches the config, but this needs to be either:
- Centralized into the config (single source of truth)
- Or clearly documented that global and per-tracker use the same zones

**Fix:** Extract zone thresholds from config, use them for both tracker zones AND global zone. Remove hardcoded thresholds from deploy.sh.

---

### 3. De-Escalation Filter Blocks Negative De-Escalation Signals

**Severity:** MEDIUM — De-escalation signals that should reduce probability are skipped.

In `find_matching_signals()`:
```python
if is_deesc and weight > 0:
    continue  # Skip positive signals in de-escalation context
```

This correctly skips positive (escalatory) signals when the text is about de-escalation. But it does **nothing** for negative (de-escalation) signals — they pass through and fire normally, which is correct. HOWEVER, the check doesn't account for the case where a text contains BOTH escalation AND de-escalation keywords.

Example: "Ceasefire talks fail, strikes resume" → `deesc_count > esc_count` is false (1 vs 2), so it's treated as escalation and de-escalation signals won't fire even though "ceasefire" is present.

This is actually a **feature**, not a bug, but the threshold of `>` means equal counts default to escalation, which could miss mixed signals. Consider using `>=` or a more nuanced scoring.

**Recommendation:** Change to weight-based keyword scoring instead of simple count.

---

### 4. `calc_confidence()` — Impossible Threshold for "Confirmed"

**Severity:** MEDIUM — The "confirmed" confidence level can never be reached.

```python
def calc_confidence(sources_count, max_credibility_weight=0):
    if max_credibility_weight >= 5 or sources_count >= 3:
        return "confirmed"
```

But `max_credibility_weight` is from tier weights: `{"1_official": 3.0, "2_wire": 2.0, ...}`. The highest possible value is **3.0** (official). The condition `>= 5` is **never true**.

The function is defined but **never actually used for signal matching** — signals get their confidence from `find_matching_signals()` which hardcodes it based on `source_tier`. This is dead code / duplicated logic.

**Fix:** Either fix the threshold to `>= 3.0` or remove the function and use the confidence from `find_matching_signals()` consistently.

---

## LOGIC ISSUES (Should Fix)

### 5. Dedup Doesn't Prevent Duplicate Signal Weight in State

**Severity:** MEDIUM

The dedup logic zeroes out duplicate signal weights:
```python
sig["weight"] = 0  # Don't double-count
sig["duplicate"] = True
```

But the merge logic later checks:
```python
if not sig.get("duplicate") and sig.get("weight", 0) != 0:
    new_active_signals[zone].add(sig["name"])
```

This correctly prevents duplicates from being added to `new_active_signals`. However, the deduped signals still appear in the enriched news JS output with `"duplicate": true` and `"weight": 0`, which clutters the UI. The frontend might display these as active signals with zero weight, confusing users.

**Fix:** Filter out `duplicate=True` signals from the final `enriched_news` output, or at least hide them from the frontend.

---

### 6. Probability History Stores Boosted Probabilities

**Severity:** MEDIUM — Historical data is misleading.

```python
history["entries"].append({
    "trackers": {t["id"]: t["prob"] for t in trackers_js}  # t["prob"] includes coupling boost
})
```

The `trackers_js` probabilities include coupling boosts applied during that run. This means the history records **display probabilities** (with coupling), not the **base probabilities** set by the cron agent. When you later compare historical data, you're comparing apples to oranges — coupling boosts change based on which other trackers are hot.

**Fix:** Store both `base_prob` and `boosted_prob` in history entries. Or store only base and recalculate boosts when displaying.

---

### 7. Global Probability Formula — Missing Weights + Hardcoded Defaults

**Severity:** MEDIUM

```python
weights = {"iran_nuke": 0.14, "iran_conventional": 0.20, "israel_lebanon": 0.16,
           "russia_ukraine": 0.18, "turkey": 0.07, "india": 0.08, "russia": 0.07,
           "china": 0.06, "north_korea": 0.07}
gp = round(sum(all_probs.get(k, 10) * weights.get(k, 0.08) for k in all_probs))
```

Issues:
1. **Missing weight for `pakistan_afghanistan`** — it's at 100% probability and IMMINENT but has no explicit weight. It falls back to `0.08` default, significantly underweighting it.
2. **Default weight `0.08`** is applied to any tracker not in the hardcoded dict — this is arbitrary.
3. **Weights don't sum to 1.0** — the sum is `0.14+0.20+0.16+0.18+0.07+0.08+0.07+0.06+0.07 = 1.03`. Minor rounding, but with `pakistan_afghanistan` using `0.08` default, the total is ~1.11, meaning the global is slightly inflated.
4. **Auto-detected trackers** (from `auto_detection`) would all use the default `0.08` weight, regardless of importance.

**Fix:** Define weights in `tracker_config.json` as part of each tracker's config. Make them sum to 1.0. Add weight for `pakistan_afghanistan`.

---

### 8. Signal Matching — "deescalation_refused" / "diplomacy_refused" vs De-Escalation Filter

**Severity:** LOW-MEDIUM

`diplomacy_refused` has positive weight (+6 or +4) and description "Iran refuses diplomatic overtures." This is an escalation signal. But the de-escalation filter checks if the text contains de-escalation keywords like "diplomacy". If a news article says "Iran refuses diplomacy," the word "diplomacy" triggers the de-escalation check, which could incorrectly classify the whole text as de-escalation context.

Result: The `diplomacy_refused` signal might be **skipped** by the de-escalation filter even though it's clearly an escalation signal.

**Fix:** The de-escalation filter should exclude keywords that are part of negation phrases ("refuses diplomacy", "rejects ceasefire", "no talks"). This requires more sophisticated NLP or a negation-aware keyword matching approach.

---

### 9. Bare `except` Clauses Mask Real Errors

**Severity:** LOW-MEDIUM

Throughout the script, `except:` (bare) is used, catching ALL exceptions including `KeyboardInterrupt`, `SystemExit`, and `SyntaxError`. This hides bugs.

Examples:
```python
except:
    energy_data = {"current": {}, ...}
except:
    pass
except:
    return signal_weight  # In apply_temporal_decay — masks parsing errors
```

**Fix:** Use `except (FileNotFoundError, json.JSONDecodeError):` for specific, expected failures.

---

## CODE QUALITY (Nice to Have)

### 10. Redundant Config File Read

`tracker_config.json` is loaded once at the top but then **re-loaded** inside the Python block for coupling rules. The `cfg` variable is already available.

**Fix:** Remove the redundant `with open("data/tracker_config.json") as cf:` inside the coupling section.

### 11. Dead/Unused Functions

- `classify_source()` — defined but never called (only `classify_source_credibility()` is used)
- `calc_confidence()` — defined but never called (confidence is set in `find_matching_signals()`)

**Fix:** Remove dead functions or wire them in properly.

### 12. Empty Loop

```python
for rule in coupling_rules:
    pass  # skip
```
This loop iterates through all coupling rules and does nothing. Leftover from refactoring?

**Fix:** Remove the dead loop.

### 13. Signal Timeline Grows Unboundedly

The `signal_timeline.json` never has entries removed. As new signals are discovered (via news merging and the `still_valid` / `new_active_signals` path), fresh timeline entries are created for signals that aren't in the config's signal definitions. Over time, this file will grow without bound.

**Fix:** Periodically prune timeline entries for signals not in any tracker's signal config.

### 14. Zone Alert "prob" Field Set to Zone Name

```python
alert = {
    "prob": new_zones[tid]  # This is the zone name like "imminent", not a probability
}
```

The `prob` field contains a zone name string, not a number. Misleading field name.

**Fix:** Either rename to `zone` or store the actual probability value.

### 15. Source Parsing Inconsistency

News items have `"source": "NBC News"` (string), but the code tries to split on `/`:
```python
sources = [s.strip() for s in n["source"].split("/")]
```

This works for "Guardian/IDF" → ["Guardian", "IDF"] but single sources like "NBC News" → ["NBC News"]. The issue is that the credibility lookup matches against these substrings. "NBC News" matches "nbc news" → tier 3_established. "Guardian" matches "guardian" → tier 3_established. "IDF" matches "idf" → tier 1_official. This actually works correctly, but the logic is fragile — if someone writes "NBC/DoD", "DoD" won't match anything in the credibility list and falls to "5_unverified".

### 16. `apply_credibility_weight` Doesn't Use `TIER_WEIGHTS`

The function has its own hardcoded tier mapping instead of using `TIER_WEIGHTS`:
```python
def apply_credibility_weight(signal_weight, source_tier):
    tier_order = {"1_official": 3, "2_wire": 2, ...}
    # ...
    if tier_val >= 2:
        return signal_weight * 1.0
```

This is duplicated logic with different multipliers than `TIER_WEIGHTS`. The `TIER_WEIGHTS` from config say `1_official: 3.0`, but `apply_credibility_weight` says `1_official: * 1.0` (full weight, no reduction). These serve different purposes but should be unified.

**Fix:** Use a single, configurable credibility weighting scheme.

---

## ZONE THRESHOLDS ANALYSIS

### Current (per-tracker): 0-15=deterrent, 15-30=elevated, 30-60=critical, 60-100=imminent

**Assessment:**
- **Deterrent (0-15):** Reasonable. Below 15% is baseline peacetime risk.
- **Elevated (15-30):** A bit narrow. Only 15 points of range. Could be 15-35.
- **Critical (30-60):** Wide range — covers "concerning" to "very serious". Good.
- **Imminent (60-100):** Very wide. At 60%, it's "likely." At 100%, it's "already happening." These are very different states.

**Recommendation:** Consider splitting IMMINENT into two zones:
- `60-80`: IMMINENT (high probability, not yet materialized)
- `80-100`: ACTIVE (conflict is underway or effectively certain)

Several trackers are at 100% (iran_conventional, israel_lebanon, russia_ukraine, pakistan_afghanistan) — they've effectively maxed out the scale and can't differentiate between "very likely" and "currently happening."

---

## GLOBAL PROBABILITY FORMULA ANALYSIS

### Current: Weighted average of tracker probabilities

**Pros:** Simple, interpretable, easy to adjust.
**Cons:**
1. **Assumes independence** — Trackers are NOT independent (coupling rules exist because they're correlated). A weighted average assumes each event is a separate coin flip, but Iran going hot cascades to Turkey/Russia/Israel.
2. **Over-counts systemic risk** — When Iran is at 100% and Turkey is at 92% (boosted by Iran), both contribute to the global score. But Turkey's high probability is *caused by* Iran. The coupling boost AND the global formula double-count the Iran risk.
3. **Under-counts tail risks** — A single tracker at 100% with weight 0.20 only contributes 20 to the global. But a nuclear test by Iran would be a black swan event regardless of other trackers.
4. **No time dynamics** — Doesn't account for how fast things are changing.

**What auto-calculation would look like:**
```python
# Bayesian approach: P(global_conflict) = 1 - Π(1 - P_i)
# where P_i = adjusted probability per tracker considering coupling

# Or simpler: take the MAX probability as anchor, then add contributions
# from independent trackers (subtracting correlated ones)

# Current approach could be improved to:
# 1. Identify which trackers are "root causes" vs "consequences"
# 2. Only count root causes in global formula
# 3. Use consequence trackers as confirmation/amplification, not independent signals
```

**Recommendation:** Keep weighted average for now (it's understandable and works for a dashboard), but add a "systemic risk" indicator that flags when multiple trackers are elevated simultaneously due to coupling.

---

## NEWS ENRICHMENT ANALYSIS

### Source Credibility: Mostly Solid

The 5-tier system is well-designed. Issues:
1. **"Downing street" has a leading space** in the config — won't match unless the source string happens to have that exact spacing.
2. **"Fars News"** is tier 4_regional, but it's used as "Fars News via NBC" in the data. The matching finds "fars news" → tier 4_regional, but the "via NBC" part is ignored. The credibility of a wire service *relaying* state media should arguably be higher.
3. **No "via" / "citing" handling** — When a reliable source reports what an unreliable source said, the system doesn't account for the intermediary's credibility.

### Deduplication: Functional but Naive

The dedup tracks `"{zone}:{signal_name}"` — if the same signal appears in two news items, only the first source counts. This is correct for preventing double-counting but:
- Doesn't handle cross-zone signals (same signal name in different trackers)
- First-seen wins, not highest-credibility-wins

---

## PREDICTIONS SYSTEM ANALYSIS

### Strengths:
- Event-based templates per tracker are thoughtful
- Confidence scoring based on news keywords
- Evaluation system tracks accuracy over time

### Weaknesses:
1. **Prediction templates are hardcoded** in deploy.sh — adding a new tracker requires modifying the script
2. **Evaluation only checks the most recent state** — if a prediction says "probability above 80" and it was 85 at eval time but spiked to 100 and dropped to 70 in between, the snapshot-based eval misses the dynamics
3. **"Unknown eval type" sets `evaluated: False`** but doesn't set `actual_value`, which could cause the accuracy calculation to silently skip these

---

## PRIORITIZED ENHANCEMENT LIST

### Priority 1 (Immediate):
1. Fix timeline dictionary path bug (#1) — signals never expire
2. Fix zone threshold mismatch (#2) — centralize in config
3. Add `pakistan_afghanistan` weight to global formula (#7)
4. Fix `calc_confidence()` impossible threshold (#4)

### Priority 2 (Next Sprint):
5. Store base + boosted probabilities in history (#6)
6. Fix de-escalation filter for negation phrases (#8)
7. Replace bare `except` clauses (#9)
8. Remove dead code and redundant config reads (#10, #11, #12)

### Priority 3 (Future):
9. Add ACTIVE zone for 80-100% trackers
10. Implement systemic risk indicator
11. Make prediction templates config-driven
12. Add "via" / citation chain handling for credibility
13. Add signal timeline pruning
14. Add prediction evaluation with time-window checks (not just snapshot)
15. Add `pakistan_afghanistan` to tracker display ordering list (it's auto-detected but not in the `tn` tuple with emoji)

---

## SUMMARY

| Category | Count | Severity |
|----------|-------|----------|
| Critical Bugs | 4 | Timeline path, zone mismatch, calc_confidence, de-esc filter |
| Logic Issues | 5 | Dedup leakage, history data, weights, bare excepts, source parsing |
| Code Quality | 7 | Dead code, redundant reads, empty loops, field naming |
| Zone Thresholds | 1 | IMMINENT too wide, needs ACTIVE split |
| Global Formula | 1 | Double-counts systemic risk, missing weights |

The dashboard is functional and the core logic is sound. The **timeline path bug (#1)** is the most impactful — it means agent-set signals effectively never decay. The **zone threshold mismatch (#2)** means global probability zones are calculated with different boundaries than the config specifies. Both should be fixed immediately.
