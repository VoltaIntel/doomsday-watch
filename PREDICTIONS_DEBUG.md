# DoomsdayWatch 24h Predictions — Debug Report

## Summary

The prediction system **generates predictions correctly** but **never evaluates them**, so accuracy is always 0%. There are two root causes, both in the evaluation pipeline.

---

## Root Cause #1: History window too small — predictions are discarded before they expire

**File:** `scripts/deploy.sh`, line ~948

```python
evaluations["predictions"] = evaluations["predictions"][-200:]
```

**The math:**
- Predictions expire 24 hours after creation (`expires_at = now + 24h`)
- System generates ~10 predictions per run (one per tracker)
- 200 slots ÷ 10 per run = 20 runs of history ≈ 20 hours
- **After 20 hours, predictions are pushed out BEFORE they reach 24h expiry**

**Evidence:**
- `evaluations.json` has 200 entries, all with `expires_at` on `2026-03-18` (tomorrow)
- The oldest prediction expires at `2026-03-18T06:05:31Z` — created ~26h ago
- Predictions from March 14-16 that expired on March 15-17 are GONE from the file
- Zero predictions have ever been evaluated (`evaluated` field never appears)

**Fix:** Increase the history window to at least 300 entries (30 hours) or 500 (50 hours):

```python
# Line ~948: Change from 200 to 500
evaluations["predictions"] = evaluations["predictions"][-500:]
```

---

## Root Cause #2: Evaluation loop only reads `evaluations.json`, never loads old prediction files

**File:** `scripts/deploy.sh`, lines ~760-810

**The problem:**
- Individual prediction files (`data/predictions/YYYY-MM-DD-HH.json`) are created every hour
- 59 files exist, dating back to March 14 20:00 UTC
- But the evaluation loop ONLY iterates over `evaluations["predictions"]`
- Old prediction files are never loaded back into the evaluation system
- If a prediction was generated before the evaluation code was added (before March 16 10:00 UTC), it was never tracked in `evaluations.json`

**Evidence:**
- Files `2026-03-14-20.json` through `2026-03-16-09.json` lack `eval_type`/`eval_value` fields
- These 36 files (360 predictions) are **unevaluable** — they were generated before eval metadata was added
- Files `2026-03-16-10.json` onward have `eval_type`/`eval_value` but were pushed out by the 200-entry limit before reaching 24h expiry

**Fix:** Add a fallback that loads expired prediction files when `evaluations.json` has no evaluable entries:

After line ~765 (the evaluation loop), add:

```python
# Fallback: load expired predictions from individual files if evaluations.json has none
evaluated_in_loop = sum(1 for p in evaluations.get("predictions", []) if p.get("evaluated"))
if evaluated_in_loop == 0:
    import glob
    pred_files = sorted(glob.glob(f"{predictions_dir}/*.json"))
    for pf in pred_files:
        if pf.endswith("evaluations.json"):
            continue
        try:
            with open(pf) as f:
                pdata = json.load(f)
            for pred in pdata.get("predictions", []):
                if pred.get("expires_at", "") < now_iso and pred.get("eval_type"):
                    # Not in evaluations.json — add it for evaluation
                    pred["evaluated"] = False
                    evaluations["predictions"].append(pred)
        except:
            pass
```

Then re-run the evaluation loop on the newly added entries.

---

## Root Cause #3: Predictions not written to `current_state.json`

**File:** `scripts/deploy.sh`, lines ~1090-1100

**The problem:**
The deploy script writes predictions and eval_stats directly into the **HTML** (`index.html`) via string replacement:

```python
pred_inject = ",\n  predictions: " + predictions_js + ",\n  eval_stats: " + eval_stats_js
new_html = new_html.replace("\n};\n\n// ===== RENDER", pred_inject + "\n};\n\n// ===== RENDER")
```

But it **never writes them to `current_state.json`**. The state file only gets updated by the scoring Python script (separate process), which doesn't know about predictions.

**Evidence:**
- `current_state.json` has no `predictions` or `eval_stats` keys
- `index.html` (deployed output) DOES have them injected
- The dashboard works from `index.html`, so predictions ARE visible on the deployed site
- This is a minor issue — the deployed HTML has correct data, but `current_state.json` is out of sync

**Fix (optional):** Add prediction data to state write-back at the end of the deploy script, before the HTML injection:

```python
# Write predictions to current_state.json too
state["predictions"] = final_predictions
state["eval_stats"] = {"total": total_eval, "correct": correct_count, "accuracy": accuracy_pct}
with open("data/current_state.json", "w") as f:
    json.dump(state, f, indent=2)
```

---

## Non-Issues (things that work correctly)

1. **Prediction generation** ✅ — Generates 10 predictions per run with proper eval_type/eval_value
2. **Prediction files** ✅ — 59 files exist, each with 10 predictions and accuracy metadata
3. **HTML injection** ✅ — Predictions and eval_stats ARE injected into `index.html`
4. **JS rendering** ✅ — `openPredictions()` correctly reads `s.predictions` and `s.eval_stats`
5. **Evaluation logic** ✅ — The comparison logic for each eval_type (probability_above, probability_below, etc.) is correct

---

## Why all individual files show `accuracy_pct: 0`

Every prediction file embeds an `accuracy` block:

```json
"accuracy": {"total_evaluated": 0, "correct": 0, "accuracy_pct": 0}
```

This is computed at generation time from `evaluations.json`. Since no predictions have ever been evaluated (due to bugs #1 and #2), accuracy is always 0.

---

## Fixes Summary (Priority Order)

| Priority | Fix | File:Line | Effort |
|----------|-----|-----------|--------|
| **P0** | Increase history window from 200→500 | deploy.sh:~948 | 1-line change |
| **P0** | Add fallback to load expired prediction files | deploy.sh:~810 | ~15 lines |
| **P1** | Write predictions to current_state.json | deploy.sh:~1095 | ~5 lines |

## Verification

After applying fixes:
1. Run deploy script: `bash scripts/deploy.sh`
2. Check `evaluations.json` — should now contain predictions from individual files that have expired
3. Check the `accuracy` block in the latest prediction file — should show non-zero `total_evaluated`
4. Check the deployed dashboard — "TRACK RECORD" should show actual numbers
5. After 24 hours, the first batch of evaluable predictions should show correct/incorrect scoring
