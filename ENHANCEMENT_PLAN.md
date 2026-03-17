# DoomsdayWatch Enhancement Plan

**Date:** 2026-03-17
**Author:** Healer Alpha (Strategic Orchestrator)
**Status:** Recommendations for implementation

---

## Executive Summary

The DoomsdayWatch dashboard has a critical design flaw: **probabilities are manually set by a cron agent and never recalibrated against actual signal strength.** This causes three visible failures:

1. **DPRK at 78% IMMINENT with zero signals** — coupling from other zones inflates a dead zone
2. **Stale probabilities** — cron agent sets them once, they never decay without manual intervention
3. **Coupling runs wild** — boosts can push zones over 100%, creating impossible states

The fix is not cosmetic. It requires a **fundamental shift from manual probability setting to signal-derived auto-calculation**, with coupling as an advisory influence rather than a hard modifier.

---

## 1. Core Architecture Change: Signal-Derived Probabilities

### The Problem

Currently: Agent reads news → manually types a probability number → deploy.sh reads it → applies coupling → displays it.

There is **zero mathematical relationship** between the signals a tracker has and the probability it shows. A zone can have 15 active signals at 78% or zero signals at 78% — the agent just picks a number.

### The Fix

**Auto-calculate probability from signals every deploy cycle.** The agent's role shifts from "set the number" to "ensure the signals are correct." This is cleaner, more auditable, and eliminates the DPRK class of bugs entirely.

### The Formula

```
P_final = clamp(P_base + P_signal + P_coupling + P_decay, P_floor, P_ceiling)
```

Where:

#### P_base — Base Rate (from tracker_config.json)

The equilibrium probability when nothing is happening. Set once per tracker based on historical conflict probability.

| Tracker | Recommended Base Rate | Rationale |
|---------|----------------------|-----------|
| Iran Nuclear | 3% | Extremely high threshold for nuclear use |
| Iran Conventional | 30% | Already in active war; base reflects sustained conflict |
| Israel-Lebanon | 20% | Active operations, but not full war |
| Turkey-NATO | 5% | Low base; needs strong triggers |
| India-Pakistan | 8% | Periodic tension, rare escalation |
| Pakistan-Afghanistan | 20% | Active conflict baseline |
| Russia-Ukraine | 22% | Sustained war baseline |
| Russia-NATO | 5% | Low base; needs direct confrontation |
| China-Taiwan | 10% | Pre-conflict posture |
| DPRK | 5% | Provocation-prone but low escalation probability |

#### P_signal — Signal Contribution

```
P_signal = Σ (signal_weight × temporal_decay(t) × source_credibility)
```

Each active signal contributes its weight, attenuated by:
- **Temporal decay** (how long since activation)
- **Source credibility** (tier-weighted)

Signal weights are already defined in `tracker_config.json`. No new config needed.

#### P_coupling — Cross-Zone Influence

```
P_coupling = Σ (coupling_boost × (source_P_active / 100))
```

Coupling is **proportional**, not absolute. If Iran-Conventional is at 85% and has a coupling boost of +6 to Turkey, Turkey gets `6 × (85/100) = 5.1`, not a flat +6.

**Critical change:** Coupling is capped at +25% maximum per zone, regardless of how many sources feed it.

#### P_decay — No-News Decay

```
P_decay = -1.5 × hours_since_last_signal / 24
```

For every 24 hours without new signal activations, probability drops by 1.5%. After 7 days of silence: -10.5%. After 30 days: -45%.

This is the mechanism that would prevent DPRK from sitting at 78% with zero signals.

#### Floors and Ceilings

| Zone | Floor | Ceiling | Rationale |
|------|-------|---------|-----------|
| Deterrent | 2% | 20% | Can't go below 2% (nothing is ever zero risk). Can't exceed 20% (would make it Elevated). |
| Elevated | 10% | 35% | Floor overlaps with Deterrent ceiling. Ceiling prevents false Critical. |
| Critical | 20% | 70% | Floor ensures Critical zones don't collapse to Elevated on one quiet day. |
| Imminent | 40% | 100% | Floor at 40% reflects reality: once you're Imminent, de-escalation is gradual, not instant. |

**Zone classification happens AFTER probability calculation:**

```python
def classify_zone(p):
    if p >= 60: return "imminent"
    elif p >= 30: return "critical"
    elif p >= 15: return "elevated"
    else: return "deterrent"
```

### Worked Example: DPRK

Current state: base_rate=8%, zero active signals, last signal activation >72h ago.

```
P_base = 8
P_signal = 0 (no active signals)
P_coupling = 0 (no active source at Imminent targeting DPRK currently)
P_decay = -1.5 × (72/24) = -4.5

P_final = clamp(8 + 0 + 0 - 4.5, 5, 100)
        = clamp(3.5, 5, 100)
        = 5%

Zone: DETERRENT (5% < 15%)
```

vs. current: 78% IMMINENT (wrong by ~73 points).

### Worked Example: Iran Conventional

Current state: 15 active signals, many high-weight, most activated <24h ago.

```
P_base = 30
P_signal = sum of ~15 weighted signals with decay factors ≈ 55 (estimated)
P_coupling = from Israel-Lebanon at Imminent: 3 × 0.95 = 2.85
P_decay = 0 (signals fresh)

P_final = clamp(30 + 55 + 2.85 + 0, 30, 100)
        = 87.85 ≈ 88%

Zone: IMMINENT (88% >= 60%)
```

This is more honest than the current 100% (which is a ceiling effect hiding the actual signal strength).

---

## 2. Temporal Decay Improvements

### Current System (broken)

Signals decay to 0 after 72h regardless of zone:
- 0-6h: 100%
- 6-24h: 75%
- 24-48h: 50%
- 48-72h: 25%
- 72h+: 0% (expired)

**Problem:** A nuclear test should not expire after 72 hours. Neither should a carrier group deployment. But "diplomacy started" absolutely should fade.

### Proposed: Tiered Decay by Signal Weight

| Signal Weight | Half-life | Full Decay Time | Rationale |
|--------------|-----------|-----------------|-----------|
| ≥ 15 (nuclear test, ICBM launch, Article 5) | 168h (7 days) | 336h (14 days) | Irreversible events persist |
| 8-14 (major military action) | 72h | 144h (6 days) | Current behavior is fine here |
| 4-7 (rhetoric, buildup) | 24h | 72h | News cycle relevance |
| ≤ 3 (minor events) | 12h | 36h | Noise — decay fast |
| Negative (diplomacy) | 18h | 54h | De-escalation signals fade faster than escalation (asymmetric) |

**Implementation:** Add `decay_class` to each signal in `tracker_config.json`:

```json
"enrichment_90": {
  "weight": 15,
  "description": "Iran enriches to 90%+ (weapons grade)",
  "decay_class": "persistent"
}
```

Or compute from weight automatically:
```python
def get_half_life(weight):
    w = abs(weight)
    if w >= 15: return 168
    elif w >= 8: return 72
    elif w >= 4: return 24
    else: return 12

def decay_factor(weight, hours_old):
    half_life = get_half_life(weight)
    return 0.5 ** (hours_old / half_life)
```

This replaces the fixed 4-step decay with a smooth exponential curve that respects signal importance.

---

## 3. Confidence Dimension

### Proposal

Add a **confidence level** to each probability score, derived from:

```python
def calc_confidence(active_signals, avg_source_tier, signal_recency):
    score = 0
    score += min(40, len(active_signals) * 5)       # Signal volume
    score += avg_source_tier * 20                      # Source quality (0-5 scale)
    score += min(30, signal_recency * 10)              # How fresh are signals (0-3 scale)
    
    if score >= 70: return "HIGH"
    elif score >= 40: return "MEDIUM"
    else: return "LOW"
```

### Display

Each tracker card shows: **88% [HIGH]** or **35% [LOW]**

A 35% with HIGH confidence means "we're confident it's low-risk."
A 35% with LOW confidence means "we don't have enough data — could be anything."

This solves the problem of "DPRK shows 5% but we have no idea if that's reliable or just default values."

### Dashboard Rendering

- **HIGH confidence:** Solid border/glow on tracker card
- **MEDIUM confidence:** Dashed border
- **LOW confidence:** Faded/transparent card, with a "?" indicator

---

## 4. Update Cadence

### Current

- Hourly deploy (cron)
- 4x daily briefings (agent)
- Signal updates only when cron agent runs

### Recommended

| Layer | Cadence | What It Does |
|-------|---------|--------------|
| **Signal ingestion** | Every 30 min | Cron agent searches news, adds/removes signals in `current_state.json`. NO probability changes. |
| **Deploy/render** | Every hour | `deploy.sh` recalculates all probabilities from signals, applies coupling, regenerates HTML. |
| **Briefings** | 4x daily (unchanged) | Agent reads dashboard state, provides narrative context. |
| **Deep calibration** | Weekly (Sunday 06:00 UTC) | Review all base rates, signal weights, coupling rules. Adjust if any tracker has been consistently over/under-predicting. |

**Key principle:** The agent manages signals. The code manages probabilities. Separation of concerns.

---

## 5. Coupling Improvements

### Current Problems

1. Coupling is additive — can push probabilities over 100
2. Coupling from multiple sources stacks without limit
3. A zone at Imminent with coupling to a quiet zone keeps that zone artificially high

### Proposed Rules

```
1. Coupling is PROPORTIONAL, not absolute:
   boost = raw_boost × (source_probability / 100)
   
2. Coupling is CAPPED per target:
   total_coupling(target) ≤ 25%
   
3. Coupling BOOSTS only, never REDUCES:
   coupling can only raise probability, never lower it
   (de-escalation should come from decay + negative signals)
   
4. Imminent coupling has DIMINISHING RETURNS:
   First 10% of coupling: full strength
   Next 10%: 50% strength
   Above 20%: 25% strength
```

### Example: Turkey (current case)

Turkey has coupling boosts from Iran-Conventional (+6) and Iran-Nuclear (+4) totaling +16, pushing it to 92% IMMINENT despite only 3 active signals.

Under new rules:
```
Iran-Conventional at ~88% → Turkey: 6 × 0.88 = 5.28
Iran-Nuclear at ~49% → Turkey: 4 × 0.49 = 1.96
Total coupling: 7.24 (capped at 25, so 7.24 stands)

Turkey base signal score: ~62%
Final: 62 + 7.24 = 69% IMMINENT
```

More honest: Turkey is elevated by the Iran conflict but its own signals don't support 92%.

---

## 6. Quick Wins (Implement This Week)

These require minimal code changes and solve the most visible problems:

### QW1: Auto-calculate probabilities from signals

**Effort:** ~40 lines of Python in deploy.sh
**Impact:** Eliminates stale/manual probability problem

Insert after the signal merge section in deploy.sh:

```python
# Auto-calculate probability from signals
for t in trackers_js:
    tid = t["id"]
    base = cfg.get("trackers", {}).get(tid, {}).get("base_rate", 10)
    
    # Sum active signal weights with decay
    signal_sum = 0
    for s in t.get("signals", []):
        decayed_w = s.get("decayed_weight", s.get("original_weight", 0))
        signal_sum += decayed_w if not s.get("positive", False) else -decayed_w
    
    # Apply: base + signals, clamped to [0, 100]
    t["prob"] = min(100, max(0, base + signal_sum))
```

### QW2: No-news decay

**Effort:** ~10 lines
**Impact:** Prevents dead zones from staying high

```python
# Apply no-news decay
hours_since_last_signal = max(
    (now - activation_time).hours for each tracker's signals
) if signals else 999

if hours_since_last_signal > 24:
    decay = -1.5 * (hours_since_last_signal / 24)
    t["prob"] = max(5, t["prob"] + decay)  # Floor at 5%
```

### QW3: Fix coupling cap

**Effort:** ~5 lines (change in existing coupling code)
**Impact:** Prevents probabilities exceeding 100

```python
# In coupling application:
all_probs[tgt] = min(100, old_val + min(boost, 25))  # Cap single boost at 25
```

### QW4: DPRK base rate correction

**Effort:** Change one number
**Impact:** Fixes the most visible bug

In `current_state.json`, change DPRK `current_probability` from 35 to 5. But with QW1 in place, this becomes unnecessary — the auto-calc will set it correctly.

### QW5: Signal activation timestamps for all existing signals

**Effort:** One-time script
**Impact:** Enables proper decay from day one

```python
# In deploy.sh, when a signal has no timeline entry:
if timeline_key not in timeline["signals"]:
    timeline["signals"][timeline_key] = now_iso
    # Mark as "just activated" for current cycle
```

This already exists in the current code. Verify it's working.

---

## 7. Long-Term Improvements (Next 2-4 Weeks)

### LT1: Signal Confidence Scoring

Add source-tier weighting to signal contribution. Already partially implemented in `apply_credibility_weight()` but not used in probability calculation.

**Action:** Feed credibility-weighted signal scores into the auto-calc formula.

### LT2: Probability History Analysis

Use the existing `probability_history.json` to:
- Track prediction accuracy (already started with the prediction system)
- Identify zones where actual events consistently deviate from predictions
- Auto-suggest base rate adjustments

### LT3: Cross-Zone Correlation Matrix

Instead of hardcoded coupling rules, compute actual correlation between zones based on historical signal co-occurrence.

**Approach:** `correlation(i,j) = co_activations(i,j) / total_activations(i)`

Use this to suggest coupling adjustments or flag unexpected correlations.

### LT4: Automated Signal Quality Audit

Weekly scan of all signals:
- Flag signals that have never been triggered (dead weight)
- Flag signals triggered >50 times (might need splitting into sub-signals)
- Suggest weight adjustments based on correlation with zone changes

### LT5: Narrative Consistency Check

Compare the auto-calculated probability against the narrative notes in `current_state.json`. If probability says IMMINENT but notes say "no change" or "declining," flag for human review.

---

## 8. Implementation Priority

| Priority | Change | Effort | Impact |
|----------|--------|--------|--------|
| 🔴 P0 | Auto-calc probabilities from signals (QW1) | 1h | Eliminates core bug class |
| 🔴 P0 | No-news decay (QW2) | 30min | Fixes DPRK-type issues |
| 🟡 P1 | Coupling cap at 25% (QW3) | 15min | Prevents >100 probabilities |
| 🟡 P1 | Tiered decay by weight | 2h | More realistic signal persistence |
| 🟢 P2 | Confidence dimension | 3h | Adds epistemic humility |
| 🟢 P2 | Proportional coupling | 1h | More honest cross-zone effects |
| 🔵 P3 | Probability history analysis | 4h | Self-improving system |
| 🔵 P3 | Cross-zone correlation matrix | 6h | Data-driven coupling |

---

## 9. What NOT to Change

1. **Don't remove human judgment from signal selection.** The agent deciding *which* signals to activate is valuable. Automating signal extraction from raw news is a separate, harder problem.

2. **Don't add more zones without removing existing ones.** 10 is already a lot. Each new zone dilutes attention and coupling complexity.

3. **Don't try to predict beyond 24h.** The prediction system is useful for calibration, not for actual forecasting. Geopolitical events are inherently unpredictable beyond short horizons.

4. **Don't make coupling bi-directional by default.** Not everything that affects Iran affects DPRK. Keep coupling rules explicit and sparse.

---

## 10. Success Metrics

After implementation, measure:

1. **DPRK probability:** Should be <15% when no signals are active. Currently 78%.
2. **Probability-signal correlation:** Each tracker's probability should correlate >0.7 with its active signal count.
3. **Global probability:** Should never exceed 95% (reserving 100% for actual confirmed nuclear detonation or Article 5 invocation).
4. **Zone change accuracy:** When a zone changes classification, the narrative should explain why within 1 cycle.
5. **Prediction accuracy:** The existing prediction eval system should show >60% accuracy within 2 weeks of auto-calc implementation.

---

*This plan prioritizes fixing the probability calculation pipeline over adding new features. Get the math right first, then add sophistication.*
