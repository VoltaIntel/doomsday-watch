# DoomsdayWatch 24h Prediction System — Design Analysis

**Date:** 2026-03-17
**Status:** 🔴 System is fundamentally broken — 0/200 predictions have been evaluated after ~3 days of operation

---

## Executive Summary

The prediction-evaluation system has **three cascading failures** that make accuracy tracking impossible. The first is a fatal architectural bug (predictions rotate out before expiry). The second is a data compatibility issue (old predictions lack required fields). The third is a timing gap that confirms the system can never work as designed. Together they guarantee that **accuracy will永远 be 0%**.

---

## Root Causes (Ranked by Severity)

### 🔴 ROOT CAUSE #1: 200-Entry Rotation Kills 24h Predictions (Fatal)

**The Math:**
- Deploy runs hourly, generating ~15 predictions per cycle
- Predictions expire after 24 hours
- The evaluation file keeps only the **last 200 predictions**
- 200 predictions ÷ 15 per cycle = **~13.3 hours of retention**
- Predictions need 24 hours to expire
- **Predictions are deleted 10+ hours BEFORE they ever get evaluated**

**This is a race the system can never win.** Every deploy adds ~15 new predictions and trims the oldest ~15. The window slides forward faster than predictions can expire.

```
Hour 0:  Predictions A1-A15 created (expire at Hour 24)
Hour 1:  Predictions A1-A15, B1-B15 (200-entry limit fine)
...
Hour 13: A1 starts getting rotated out
Hour 14: All A-predictions are GONE — they expire at Hour 24
Hour 24: Nothing to evaluate. A1-A15 were deleted hours ago.
```

### 🔴 ROOT CAUSE #2: Early Predictions Missing eval_type (Fatal for historical data)

Files from **Mar 14 20:00 through Mar 16 09:00** (37 files, ~370 predictions) lack `eval_type` and `eval_value` fields. These were generated before the eval mapping was added to deploy.sh.

When the evaluation loop encounters these predictions:
```python
pred_type = pred.get("eval_type", pred["type"])  # Falls back to "military_operation", "status_quo", etc.
```
Then:
```python
if pred_type == "probability_above":  # "military_operation" ≠ "probability_above"
    ...
elif pred_type == "probability_below":
    ...
# Falls to else:
else:
    pred["evaluated"] = False  # Permanently unevaluable
```

These ~370 predictions are **permanently unevaluable** — no eval_type means no branch matches.

### 🟡 ROOT CAUSE #3: eval_type Mismatch Between Generation and Evaluation

The narrative `type` field (military_operation, diplomatic, border_conflict, etc.) and the `eval_type` field (probability_above, probability_below, trend_rising, signal_triggered, zone_change) serve different purposes but are conflated in the fallback logic.

The evaluation loop's fallback uses `pred.get("eval_type", pred["type"])` — if eval_type is missing, it tries the narrative type, which **never matches** any eval branch. The `else` clause silently marks these as unevaluated.

Additionally, the available eval types (`probability_above/below`, `trend_rising`, `signal_triggered`, `zone_change`) don't align well with the narrative predictions:
- `"military_operation"` → evaluates as `probability_above` (what threshold? the current prob?)
- `"diplomatic"` → never evaluated
- `"status_quo"` → evaluates as `probability_above` (predicting "no change" as "probability stays above X")
- `"nuclear_development"` → never evaluated

---

## Additional Issues

### Issue #4: State Staleness

The evaluation loop uses `state` loaded from `current_state.json` at script start. If multiple deploys happen without state updates between them, evaluations use stale tracker values. Not a primary failure cause but degrades accuracy.

### Issue #5: Redundant Persistence

Predictions are stored in THREE places:
1. Individual files (`data/predictions/YYYY-MM-DD-HH.json`) — archival, never read back
2. `evaluations.json` — the evaluation target, but capped at 200 entries
3. Embedded in `index.html` — the display layer, read-only

The individual files serve no purpose in the evaluation pipeline. They're write-only archives. The HTML embedding is the only place users see predictions.

### Issue #6: No Separation of Concerns

Prediction generation, evaluation, and rendering are all in a single deploy.sh script (~1120 lines). This makes the system fragile and hard to debug. The evaluation step re-runs the entire deploy pipeline rather than being a standalone process.

---

## Why Accuracy Is Always 0%

The system has been running for ~3 days (60 hourly prediction files). Here's the math:

| Factor | Value |
|--------|-------|
| Predictions generated total | ~900 (60 files × 15 avg) |
| Predictions in evaluations.json | 200 (capped) |
| Predictions with eval_type | ~150 (Mar 16 10:00 onward) |
| Predictions that have expired (24h ago) | ~0 (all in eval file are from last ~13h) |
| Predictions actually evaluated | **0** |

**The system has never had a single expired, evaluable prediction to score.** The 200-entry rotation guarantees it.

---

## Recommended Redesign

### Quick Fixes (Low Effort, Partial Improvement)

**Fix 1: Increase rotation cap to 1000 entries**
```python
evaluations["predictions"] = evaluations["predictions"][-1000:]
```
This extends retention to ~67 hours, giving 24h predictions ~43 hours of window. Quick win but doesn't solve the fundamental architecture issue.

**Fix 2: Backfill eval_type for old predictions**
```python
# In evaluations.json, add eval_type/eval_value to old predictions
for pred in evaluations["predictions"]:
    if "eval_type" not in pred:
        pred["eval_type"] = "probability_above"
        pred["eval_value"] = max(0, pred.get("value", 50) - 10)
```
This makes ~370 old predictions evaluable once they expire (if rotation is also fixed).

**Fix 3: Never delete expired predictions until evaluated**
```python
# Only trim predictions that have been evaluated
unevaluated = [p for p in evaluations["predictions"] if not p.get("evaluated")]
evaluated = [p for p in evaluations["predictions"] if p.get("evaluated")]
evaluations["predictions"] = unevaluated + evaluated[-200:]  # Keep last 200 evaluated for stats
```

### Architectural Changes (Medium Effort, Proper Fix)

**Architecture: Separate prediction lifecycle from display pipeline**

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  GENERATE    │────▶│  PERSIST (append) │     │  RENDER      │
│  (hourly)    │     │  evaluations.json │     │  (on deploy) │
└─────────────┘     │  (append-only)    │     └─────────────┘
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  EVALUATE         │
                    │  (separate cron)  │
                    │  runs every 6h    │
                    └──────────────────┘
```

1. **evaluations.json becomes append-only** — never delete predictions, just mark evaluated
2. **Separate evaluation process** — runs on its own schedule (every 6h), checks for expired unevaluated predictions, evaluates them, updates stats
3. **No rotation** — the file grows (200 entries/day × 365 = 73KB/year, trivially manageable)
4. **Individual prediction files** become the archival source of truth; evaluations.json is derived

**Improved evaluation logic:**
```python
# Every 6 hours, evaluate all expired predictions
now = datetime.now(timezone.utc)
for pred in predictions:
    if pred.get("evaluated"):
        continue
    if datetime.fromisoformat(pred["expires_at"].replace("Z", "+00:00")) > now:
        continue  # Not expired yet
    
    # Evaluate using fresh state
    actual_state = load_current_state()  # Fresh, not stale
    tracker = actual_state["trackers"].get(pred["tracker_id"], {})
    
    eval_type = pred["eval_type"]  # Required field, no fallback
    actual = tracker.get("current_probability", 0)
    
    if eval_type == "probability_above":
        pred["correct"] = actual >= pred["eval_value"]
    elif eval_type == "probability_below":
        pred["correct"] = actual <= pred["eval_value"]
    # ... etc
    
    pred["evaluated"] = True
    pred["evaluated_at"] = now.isoformat()
    pred["actual_value"] = actual
```

---

## Answers to Design Questions

### Q1: Is the prediction-evaluation cycle fundamentally sound?
**No.** The cycle is sound in concept but fatally broken in implementation. The 200-entry rotation destroys predictions before they can expire. Fix the rotation, and the cycle works.

### Q2: Should predictions be persisted differently?
**Yes.** The current triple-redundancy (individual files + evaluations.json + HTML) is wasteful and confusing. Best approach:
- Individual files: archival source of truth (keep)
- evaluations.json: append-only evaluation tracking (change from rotation to append-only)
- HTML embedding: display-only, reads from evaluations.json (keep, but source should be clean)

### Q3: What would make this system actually useful?
1. Fix the rotation bug (immediate)
2. Separate evaluation from generation
3. Add calibration metrics (not just "correct/incorrect" but Brier scores)
4. Add per-tracker accuracy breakdowns
5. Add confidence-weighted accuracy (a 90% confidence miss is worse than a 40% confidence miss)

### Q4: Are the prediction types correct?
**Mostly.** The dual-type system (narrative `type` + evaluable `eval_type`) is the right idea — separate what you tell users from what you can actually measure. The problem is:
- eval_type must be **required**, never optional/fallback
- The narrative types (military_operation, diplomatic, etc.) are fine for display
- The eval types need expansion to cover all narrative types (e.g., `event_occurred` for diplomatic/nuclear_development predictions)
- The mapping from narrative to eval should be explicit, not `prob - 10`

---

## Impact Assessment

| Metric | Current State | After Quick Fixes | After Redesign |
|--------|---------------|-------------------|----------------|
| Evaluations ever completed | 0 | ~50 (from backfill) | Growing continuously |
| Accuracy metric | Always 0% | Meaningful after 24h | Reliable tracking |
| Data loss risk | High (rotation) | Medium | Low (append-only) |
| Predictions tracked | 200 max | 1000 max | Unlimited |
| Time to first real accuracy score | Never | Next 24h | Next 24h |

---

## Priority Action Items

1. **[P0] Fix rotation cap** — change `[-200:]` to `[-1000:]` or switch to append-only. This unblocks everything.
2. **[P0] Backfill eval_type** — add missing eval_type/eval_value to old predictions in evaluations.json
3. **[P1] Require eval_type** — make it a required field, fail loudly if missing
4. **[P1] Separate evaluation** — decouple evaluation from the deploy script
5. **[P2] Add per-tracker stats** — break down accuracy by tracker to surface which predictions are reliable
6. **[P2] Add calibration metrics** — Brier score, reliability diagrams
