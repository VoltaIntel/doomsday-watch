# DoomsdayWatch — Debug & Implementation Plan

**Created:** 2026-03-17 08:17 UTC+1
**Status:** DRAFT — awaiting Kenan's approval
**Sources:** DEBUG_REPORT.md (Coder), ENHANCEMENT_PLAN.md (Healer Alpha)

---

## Guiding Principle

> **Agent manages signals. Code manages probabilities.**

The cron agent's job is to search news and activate/deactivate signals. Probability calculation is the deploy script's job — mathematically derived from signals, not manually typed.

---

## Phase 0 — Critical Bug Fixes (Do First, No Logic Changes)

These are pure bug fixes with no design changes. Safe to deploy immediately.

### P0.1: Fix timeline dictionary path
- **File:** `deploy.sh` — `apply_temporal_decay()` and signal merge section
- **Bug:** `timeline.get(timeline_key)` should be `timeline["signals"].get(timeline_key)`
- **Impact:** Agent-set signals never decay, accumulate forever
- **Fix:** One-line change in ~3 places

### P0.2: Add `pakistan_afghanistan` to global weights
- **File:** `deploy.sh` — global probability calculation (~line 420)
- **Bug:** Missing from weights dict, falls to default 0.08
- **Fix:** Add `"pakistan_afghanistan": 0.08` to weights dict, rebalance so weights sum to 1.0

### P0.3: Remove dead `calc_confidence()` function
- **File:** `deploy.sh`
- **Bug:** Impossible threshold (`>= 5` when max is 3.0), never called
- **Fix:** Remove function, or fix threshold and wire it in

### P0.4: Fix empty coupling loop
- **File:** `deploy.sh` — `for rule in coupling_rules: pass`
- **Fix:** Remove dead loop

### P0.5: Fix zone alert `prob` field
- **File:** `deploy.sh` — zone alert object
- **Bug:** `"prob": new_zones[tid]` stores zone name string, not probability number
- **Fix:** Store actual probability: `"prob": new_probs.get(tid, 0)`

**Deliverable:** Deploy these fixes, verify dashboard still works.

---

## Phase 1 — Auto-Calculate Probabilities (Core Fix)

Replace manual probability setting with signal-derived calculation.

### P1.1: Auto-calc formula in deploy.sh

Insert after signal merge, before coupling:

```python
# Auto-calculate probability from signals
for t in trackers_js:
    tid = t["id"]
    base = cfg.get("trackers", {}).get(tid, {}).get("base_rate", 10)
    
    # Sum active signal weights with decay
    signal_sum = 0
    for s in t.get("signals", []):
        decayed_w = s.get("decayed_weight", s.get("original_weight", 0))
        if s.get("positive", False):  # de-escalation signal
            signal_sum -= decayed_w
        else:
            signal_sum += decayed_w
    
    # No-news decay: -1.5% per 24h without any signal activation
    max_age_hours = 0
    for s in t.get("signals", []):
        activated = s.get("activated_at", "")
        if activated:
            age_h = (now_dt - datetime.fromisoformat(activated.replace("Z",""))).total_seconds() / 3600
            max_age_hours = max(max_age_hours, age_h)
    
    if not t.get("signals"):  # zero signals
        max_age_hours = 999  # force decay
    
    no_news_decay = 0
    if max_age_hours > 24:
        no_news_decay = -1.5 * (max_age_hours / 24)
    
    # Final probability
    t["prob"] = min(100, max(0, base + signal_sum + no_news_decay))
```

### P1.2: Add `base_rate` to tracker_config.json

Each tracker needs a `base_rate` field:

| Tracker | Base Rate | Rationale |
|---------|-----------|-----------|
| iran_nuke | 3 | Nuclear use is extremely rare |
| iran_conventional | 30 | Active war, sustained conflict |
| israel_lebanon | 20 | Active operations |
| turkey | 5 | Low base, needs triggers |
| india | 8 | Periodic tension |
| pakistan_afghanistan | 20 | Active conflict baseline |
| russia_ukraine | 22 | Sustained war |
| russia | 5 | Low base, needs direct confrontation |
| china | 10 | Pre-conflict posture |
| north_korea | 5 | Provocation-prone, low escalation |

### P1.3: Remove manual probability writes from cron job instructions

Update all 5 nuke-watch cron jobs: agents should NO LONGER set `current_probability`. Only set `active_signals` and `zone` (zone can be auto-derived from probability, but keeping manual override is OK for now).

**Deliverable:** Probabilities auto-calculate from signals. DPRK with zero signals → ~5%. Iran Conventional with 15 signals → ~85-90%.

---

## Phase 2 — Coupling Improvements

### P2.1: Proportional coupling

Change from absolute to proportional boosts:
```
effective_boost = raw_boost × (source_prob / 100)
```

### P2.2: Per-target coupling cap

Total coupling to any single tracker capped at +25%.

### P2.3: Add coupling config to tracker_config.json

Move hardcoded coupling weights into config for maintainability.

**Deliverable:** No probability can exceed 100%. Coupling is proportional, not absolute.

---

## Phase 3 — Temporal Decay Improvements

### P3.1: Tiered decay by signal weight

| Signal Weight | Half-life | Full Decay |
|--------------|-----------|------------|
| ≥ 15 (nuclear, ICBM) | 168h (7d) | 336h (14d) |
| 8-14 (major military) | 72h | 144h (6d) |
| 4-7 (rhetoric, buildup) | 24h | 72h |
| ≤ 3 (minor) | 12h | 36h |

Replace fixed 4-step decay with exponential curve:
```python
def decay_factor(weight, hours_old):
    half_life = get_half_life(abs(weight))
    return 0.5 ** (hours_old / half_life)
```

**Deliverable:** Nuclear-grade signals persist longer; minor signals decay fast.

---

## Phase 4 — Quality of Life

### P4.1: Confidence dimension

Show HIGH/MEDIUM/LOW next to each probability based on signal count + source quality + recency.

### P4.2: Split IMMINENT zone

- 60-80%: IMMINENT (high probability)
- 80-100%: ACTIVE (conflict underway)

### P4.3: Store base + boosted probabilities in history

Keep both values for accurate trend analysis.

### P4.4: Centralize zone thresholds in config

Single source of truth for zone boundaries.

---

## Implementation Order & Timeline

| Phase | When | Estimated Time | Risk |
|-------|------|----------------|------|
| **P0** — Bug fixes | Now | 30 min | Low (pure fixes) |
| **P1** — Auto-calc | After P0 verified | 1-2 hr | Medium (changes core logic) |
| **P2** — Coupling | After P1 stable | 1 hr | Low (config changes) |
| **P3** — Decay | After P2 stable | 1 hr | Low (isolated function) |
| **P4** — QoL | When ready | 2-3 hr | Low (additive features) |

---

## Verification Checklist

After each phase, verify:
- [ ] Deploy script runs without errors
- [ ] Dashboard renders all 10 trackers
- [ ] Probabilities are reasonable (DPRK < 20% with zero signals)
- [ ] Global probability ≤ 100%
- [ ] Coupling boosts are visible and proportional
- [ ] Signal decay works (old signals fade, new ones are strong)
- [ ] No JS errors in browser console
- [ ] Probability history entries show correct values
- [ ] Git committed and pushed

---

## Cron Job Changes Required

After Phase 1, update cron job instructions:
1. Agents should **NOT** set `current_probability` — it's auto-calculated
2. Agents should **ONLY** set `active_signals` based on news evidence
3. Zone can be set manually or auto-derived (we'll keep manual for now as a safety net)
4. Add rule: "If you find no evidence for a zone, set `active_signals = []`"
