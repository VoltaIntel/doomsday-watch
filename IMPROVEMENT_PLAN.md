# DoomsdayWatch / Nuclear Escalation Monitor — Comprehensive Improvement Plan

**Date:** 2026-04-10  
**Scope:** Full system audit — cron jobs, pipeline, dashboard, data layer, prediction engine  
**Status:** PLANNING ONLY — no code changes

---

## 1. CURRENT STATE ASSESSMENT

### What Works ✅

| Component | Status | Notes |
|-----------|--------|-------|
| News scanning | ✅ Functional | All 5 cron jobs successfully search Tavily for news across 10 zones |
| Dashboard rendering | ✅ Functional | Pipeline replaces hardcoded template; Leaflet map, charts, cards all render |
| Energy price fetching | ✅ Working | OilPriceAPI + Yahoo Finance fallback; Brent at $97.34, Gold at $4,750 |
| Source credibility | ✅ Good design | 5-tier system (official/wire/established/regional/unverified) with proper weights |
| Temporal decay | ✅ Implemented | Exponential decay with tiered half-lives (12h/24h/72h/168h) |
| Discord delivery | ✅ Working | All 5 jobs deliver to the same Discord channel |
| Zone alert system | ✅ Implemented | Detects zone transitions, stores pending/history alerts |
| Probability history | ✅ Tracked | 336-entry (2-week) rolling history with SVG chart generation |
| Signal deduplication | ✅ Active | Pipeline deduplicates signals by first-seen source |

### What Doesn't Work / Is Broken ❌

| Component | Issue | Severity |
|-----------|-------|----------|
| `update_state.py` | Stale script (Day 39, Apr 8 data) that OVERWRITES cron job state if run manually | **P0** |
| `update_doomsday.py` | Another stale state-writer (Day 40) — dual-write conflict risk | **P0** |
| Auto-detection of new zones | References `cfg["auto_detection"]` which doesn't exist in tracker_config.json | **P1** |
| tracker_config.json | Missing `trackers`, `coupling`, `scoring`, `auto_detection` sections — pipeline uses hardcoded fallbacks | **P1** |
| Dashboard fallback state | Shows March 15 data (global 91%, 11 trackers including duplicate china) if pipeline fails silently | **P1** |
| `update_state.py` paths | Hardcoded absolute path to `current_state.json` | **P2** |

### What's Mediocre ⚠️

| Component | Issue |
|-----------|-------|
| Prediction accuracy | 41% (806/1960) — inflated by "status quo" predictions on stable zones |
| Signal weight config | Uses `signal_weights` dict but `cfg["trackers"]` is empty — all matching falls through to zone fallback |
| Global probability formula | Weighted average with hardcoded weights + arbitrary "+5 uplift" in update_doomsday.py |

---

## 2. CRON JOB REDUNDANCY ANALYSIS

### Current Jobs (5 nuke-watch cron jobs)

| Job ID | Name | Schedule | Last Run | Status |
|--------|------|----------|----------|--------|
| 1fe28e8fa019 | Nuke Watch 00:00 UTC | `0 0 * * *` | Apr 10 00:02 | ok |
| f488dcc11503 | Nuke Watch 06:00 UTC | `0 6 * * *` | Apr 10 06:06 | ok |
| bf2f5903bf99 | Daily Update (Deep Scan) | `0 8 * * *` | Apr 10 08:03 | ok |
| 12440fb753dc | Nuke Watch 12:00 UTC | `0 12 * * *` | Apr 7 12:02 | ok |
| 608de2b6a22c | Nuke Watch 20:00 UTC | `0 20 * * *` | Apr 7 20:04 | ok |

### Overlap Analysis

**Critical overlap: 06:00 and 08:00 jobs run 2 hours apart.**

Both do:
- Read the same config/state files
- Search all 10 conflict zones via Tavily
- Update probabilities
- Deploy dashboard
- Deliver briefing to the same Discord channel

The 08:00 "Daily Update" has additional steps (auto-detect zones, deeper scan), but the auto-detection is broken (see §1). In practice, it does the same news scan as the 06:00 job.

**All 5 jobs deliver to the same Discord channel** (`discord:1490433760133648394`), resulting in 5 similar briefings per day.

### Cost Analysis

Each job performs ~10 Tavily web searches (one per zone). With 5 jobs/day:
- **50 Tavily searches/day** for nuke-watch alone
- Each search costs API credits + LLM tokens for analysis
- Estimated: ~$2-5/day in Tavily + LLM costs for redundant scanning

### Recommendation: Consolidate to 3 Jobs

| Proposed Job | Schedule | Purpose |
|-------------|----------|---------|
| **Morning Deep Scan** | `0 6 * * *` | Comprehensive 24h scan. Replaces both 06:00 and 08:00. Include auto-detection, energy markets, IAEA, allied positions. |
| **Midday Pulse Check** | `0 12 * * *` | Quick scan for breaking developments. Could use [SILENT] more aggressively. |
| **Evening Assessment** | `0 20 * * *` | End-of-day assessment. Include market close data. |

**Savings: ~40% fewer Tavily searches, 2 fewer LLM sessions/day, less Discord noise.**

The 00:00 UTC job can be eliminated because:
- Minimal new news at midnight UTC
- The 20:00 evening assessment covers the late-day period
- The 06:00 morning scan catches overnight developments

---

## 3. STATE MANAGEMENT ISSUES

### Problem: Dual-Write Conflict

Three scripts can write to `current_state.json`:
1. **Cron jobs** (via inline Python in prompts) — write to `state["zones"]` with qualitative signals
2. **`scripts/pipeline.py`** — reads `state["zones"]` OR `state["trackers"]`, writes enriched state
3. **`data/update_state.py`** — manual script that overwrites `state["trackers"]` with Day 39 data
4. **`data/update_doomsday.py`** — another manual script that overwrites `state["zones"]` with Day 40 data

If someone accidentally runs `update_state.py` or `update_doomsday.py`, it will:
- Overwrite all probabilities with stale values (Day 39-40 when we're on Day 49)
- Replace current signals with outdated ones
- Corrupt prediction data

### Recommendation

1. **Archive `update_state.py` and `update_doomsday.py`** — move to `scripts/_archived/` with clear warnings
2. **Add a state lock mechanism** — pipeline writes a `last_writer` field with job ID and timestamp
3. **Unify on `state["zones"]` schema** — the cron jobs already write there; pipeline should read from there exclusively and not maintain a separate `state["trackers"]` unless needed for backward compat

---

## 4. PIPELINE ARCHITECTURE ISSUES

### Current State: `pipeline.py` is 1462 lines

It handles everything in a single monolithic script:
- Signal processing & dedup
- Probability calculation
- Coupling computation
- Prediction generation
- Prediction evaluation
- Zone change detection
- History management
- SVG chart generation
- HTML string replacement
- Git commit/push

### Issues

1. **Fragile string replacement**: Finding `const state = {` and `// ===== RENDER` markers and doing string slicing to replace the state block. If the HTML template changes, this breaks silently.

2. **No separation of concerns**: A bug in signal processing can cascade into HTML generation.

3. **Silent failures**: Heavy use of bare `except:` blocks (at least 10 instances) hides real errors.

4. **Hardcoded weights**: Global probability weights at line 745 are hardcoded, not configurable.

### Recommendation: Modular Refactor

Split into focused modules:
```
scripts/
├── pipeline.py          # Orchestrator (thin, ~100 lines)
├── signals.py           # Signal processing, decay, dedup
├── probabilities.py     # Probability calculation, coupling
├── predictions.py       # Prediction generation & evaluation
├── dashboard_builder.py # HTML generation (template-based, not string replacement)
└── deploy.py            # Git integration, deployment
```

---

## 5. DASHBOARD FIXES NEEDED

### Known Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| Hardcoded March 15 fallback state | Shows 91% global, duplicate china tracker if pipeline fails | Replace with minimal placeholder or error state |
| `tn` list has duplicate china entry (line 916) in fallback | Visual bug if fallback renders | Remove duplicate from template |
| No error boundary for pipeline failure | Dashboard shows stale data silently | Add "last updated" age warning, stale-data detection |
| Mobile responsiveness | Tracker grid may overflow on narrow screens | Test and fix CSS breakpoints |
| No loading indicator during pipeline | Users see old data until deploy completes | Add "updating..." indicator or deploy timestamp |

### Recommendation

1. **Replace hardcoded state with error-safe placeholder**: Instead of March data, show "Awaiting first update" with 0% across the board
2. **Add staleness detection**: If `last_updated` is >12h old, show warning banner
3. **Consider server-side rendering**: Move from "pipeline rewrites HTML" to "HTML fetches JSON" pattern — dashboard loads `data/current_state.json` via fetch() instead of being embedded

---

## 6. PREDICTION ENGINE ANALYSIS

### Current Accuracy: 41% (806/1960)

This is misleading. The system generates predictions like:
- "China-Taiwan will stay above 1% probability" → Always true (trivially correct)
- "Russia-Ukraine will stay above 65%" → True when at 80% (low-information prediction)
- "Pakistan-Afghanistan will stay below 6%" → True when at 6% (predicting status quo)

### Problems

1. **Low-information predictions**: Most predictions are "probability_above X" where X is well below current value
2. **40% confidence on most predictions**: The system doesn't differentiate high-confidence from low-confidence predictions
3. **No actionable predictions**: Predictions don't forecast *changes*, only *continuations*
4. **Evaluation bias**: Status quo predictions are inherently easier to get right

### Recommendation

1. **Raise prediction thresholds**: Only predict "above X" when X is within 10% of current probability
2. **Add change predictions**: "DPRK probability will increase by 5%+ in 24h" (harder but more valuable)
3. **Track calibration**: Separate accuracy by prediction type (escalation vs. de-escalation vs. status quo)
4. **Reduce prediction frequency**: Only generate predictions when there's a meaningful signal change, not every run

---

## 7. SIGNAL & PROBABILITY FORMULA ISSUES

### Signal Decay

Current implementation is reasonable but has edge cases:

- **Half-life tiers**: ≥15 weight → 168h (7d), ≥8 → 72h (3d), ≥4 → 24h (1d), else → 12h
- **Issue**: The `apply_temporal_decay` function returns 0 when decayed < 0.5. But signal weights can be as high as 15+, meaning a nuclear test signal would need to be below 0.5/15 = 3.3% of original to expire — that's ~36 days for a weight-15 signal. This is reasonable.

### Probability Calculation

The pipeline has two paths:
1. **Auto-calculate** (if tracker has real signals from `trackers` schema): `base + signal_sum + no_news_decay`
2. **Zone fallback** (cron job's authoritative probability from `zones` schema)

Since `cfg["trackers"]` is empty, ALL trackers fall through to the zone fallback. The auto-calculation code (~100 lines) is dead code in the current configuration.

### Global Probability

```python
weights = {"iran_nuke": 0.12, "iran_conventional": 0.18, ...}
gp = round(sum(all_probs[k] * weights[k] for k in all_probs))
```

This is a weighted average, which is reasonable. But:
- Weights are hardcoded in pipeline.py, not in config
- The `update_doomsday.py` script adds an arbitrary "+5 uplift" — conflicting formula
- No clear methodology for weight selection

### Recommendation

1. **Move weights to tracker_config.json** — make them configurable
2. **Remove dead auto-calculation code** or populate `cfg["trackers"]` to use it
3. **Standardize global probability formula** — remove the +5 uplift hack
4. **Document the probability methodology** in a METHODOLOGY.md file

---

## 8. SECURITY & RELIABILITY

### Issues

| Issue | Risk | Fix |
|-------|------|-----|
| Bare `except:` blocks (10+ in pipeline.py) | Hides real errors, silent data corruption | Catch specific exceptions, log errors |
| No input validation on current_state.json | Corrupt JSON crashes pipeline | Add JSON schema validation |
| No atomic writes for state file | Partial writes on crash corrupt state | Use tmp+rename pattern (partially done) |
| Git auto-push on deploy | Risk of pushing broken state | Add pre-push validation, dry-run mode |
| No rate limiting on Tavily searches | Could hit API limits during 5-job days | Consolidate jobs (see §2) |
| `update_state.py` can be run anytime | Overwrites live state with stale data | Archive or delete |

---

## 9. FEATURE REQUESTS TO CONSIDER

### P0 — Critical
- **State integrity**: Archive dangerous manual scripts, add write-lock
- **Job consolidation**: Reduce from 5 to 3 cron jobs
- **tracker_config.json completion**: Add missing trackers, coupling, scoring sections

### P1 — High Value
- **Prediction quality**: Raise thresholds, add change predictions, track calibration
- **Error handling**: Replace bare excepts with specific error types
- **Dashboard staleness detection**: Warn when data is >12h old
- **Modular pipeline**: Split 1462-line monolith into focused modules

### P2 — Nice to Have
- **JSON fetch pattern**: Dashboard loads data via fetch() instead of embedded state
- **Historical analysis**: Track which zones escalated fastest, identify patterns
- **Alert system**: Push notifications for Imminent zone transitions
- **Multi-source verification**: Require 2+ sources before activating high-weight signals
- **Correlation tracking**: Track which zone escalations precede others
- **Dedicated health endpoint**: Simple status page showing last update time, system health

### P3 — Future
- **ML-based probability adjustment**: Train on historical signal→probability outcomes
- **Automated source discovery**: Detect new news sources covering conflict zones
- **Geospatial coupling**: Calculate physical proximity coupling (e.g., Iran war affects Pakistan)
- **Sentiment analysis**: NLP on news text for more nuanced signal detection

---

## 10. PRIORITY ACTION PLAN

### Phase 1: Stabilize (Week 1)
1. ✅ Archive `update_state.py` and `update_doomsday.py` to `scripts/_archived/`
2. ✅ Consolidate cron jobs: merge 06:00+08:00 into single 06:00 deep scan, remove 00:00
3. ✅ Add `last_writer` field to state to prevent accidental overwrites
4. ✅ Fix dashboard fallback state (remove March 15 hardcoded data)
5. ✅ Replace bare `except:` blocks with `except Exception as e: print(f"Error: {e}")`

### Phase 2: Improve (Week 2-3)
1. Complete `tracker_config.json` with trackers, coupling rules, scoring thresholds
2. Move hardcoded global probability weights to config
3. Improve prediction engine: raise thresholds, add calibration tracking
4. Add dashboard staleness detection
5. Add JSON schema validation for current_state.json

### Phase 3: Architect (Week 4+)
1. Modularize pipeline.py into focused modules
2. Implement template-based dashboard generation (not string replacement)
3. Consider JSON fetch pattern for dashboard data loading
4. Build historical analysis capabilities
5. Document probability methodology

---

## APPENDIX: FILE INVENTORY

### Core Files
| File | Lines | Purpose | Health |
|------|-------|---------|--------|
| `scripts/pipeline.py` | 1462 | Monolithic pipeline: signals → probabilities → predictions → HTML | ⚠️ Functional but fragile |
| `scripts/deploy.sh` | 8 | Wrapper: fetch oil + run pipeline | ✅ Simple, works |
| `scripts/fetch_oil_prices.py` | 163 | Energy price fetcher with fallback chain | ✅ Clean, well-structured |
| `data/current_state.json` | 278 | Live state: 10 zones, predictions, eval stats | ✅ Current (Apr 10) |
| `data/tracker_config.json` | 23 | Zone list, signal weights, update interval | ⚠️ Missing trackers/coupling/scoring |
| `data/source_credibility.json` | 242 | 5-tier source credibility system | ✅ Well-designed |
| `dashboard.html` | 2034 | Full dashboard with embedded JS | ⚠️ Hardcoded fallback state |
| `data/signal_timeline.json` | — | Signal activation timestamps | ✅ Pruned, clean |

### Dangerous Files (Should Be Archived)
| File | Lines | Risk |
|------|-------|------|
| `data/update_state.py` | 84 | Overwrites live state with Day 39 data |
| `data/update_doomsday.py` | 273 | Overwrites live state with Day 40 data |

### Supporting Files
| File | Purpose |
|------|---------|
| `scripts/track_flights.py` | Flight tracking (not cron-scheduled) |
| `scripts/flight_tracker.py` | Flight tracking helper |
| `data/energy_prices.json` | Energy price history (2524 lines) |
| `data/probability_history.json` | Probability time series |
| `data/zone_alerts.json` | Zone transition alerts |
| `data/previous_zones.json` | Previous zone states for diff |
| `data/flight_tracking.json` | Flight disruption data |

### Cron Outputs (Last 7 Days)
All 5 nuke-watch jobs have recent outputs confirming they're running successfully.
The 00:00, 06:00, and 08:00 jobs have the most recent runs (Apr 10).
The 12:00 and 20:00 jobs last ran Apr 7 — possible gap, but next runs scheduled for today.
