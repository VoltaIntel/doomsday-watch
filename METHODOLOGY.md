# DoomsdayWatch — Methodology

## Overview

DoomsdayWatch monitors geopolitical escalation across 10+ conflict zones,
computes threat probabilities from open-source intelligence signals, and
publishes a real-time dashboard with predictions and trend analysis.

---

## 1. Probability Formula

Each tracker's probability is computed as:

```
P = base_rate + Σ(decayed_signal_weights) + no_news_decay
```

| Component | Description |
|---|---|
| `base_rate` | Config-defined baseline probability (typically 5-15%) |
| `signal_weights` | Sum of active signal weights after temporal decay |
| `no_news_decay` | -1.5% per 24h without fresh signal activity |

The result is clamped to `[2, 100]` — no event is ever assigned zero risk.

### Global Probability

The global threat score is a weighted average:

```
G = Σ(P_i × weight_i)
```

Default weights (from `tracker_config.json`):

| Tracker | Weight |
|---|---|
| Iran Conventional | 0.18 |
| Russia-Ukraine | 0.16 |
| Israel-Lebanon | 0.14 |
| Iran Nuclear | 0.12 |
| Pakistan-Afghanistan | 0.08 |
| DPRK | 0.08 |
| Turkey-NATO | 0.06 |
| Russia-NATO | 0.06 |
| China-Taiwan | 0.06 |
| India-Pakistan | 0.06 |

---

## 2. Signal Classification

### Source Credibility Tiers

Sources are classified into 5 tiers based on keyword matching:

| Tier | Label | Weight | Examples |
|---|---|---|---|
| `1_official` | Government/Int'l Bodies | 3.0 | White House, Pentagon, IAEA, NATO |
| `2_wire` | Wire Services | 2.0 | Reuters, AP, AFP, Bloomberg |
| `3_established` | Established Media | 1.5 | BBC, NYT, WSJ, Guardian |
| `4_regional` | Regional Media | 1.0 | Al Jazeera, SCMP, Haaretz |
| `5_unverified` | Unverified/Unknown | 0.3 | Social media, blogs |

### Credibility-Weighted Signals

Signal weights are scaled by source tier:

- Tier 1-2: 100% of weight
- Tier 3: 75% of weight
- Tier 4: 50% of weight
- Tier 5: 20% of weight

### Confidence Labels

Confidence is derived from source count and max credibility weight:

| Condition | Label |
|---|---|
| ≥3 sources OR max_cred ≥ 3 | `confirmed` |
| ≥2 sources OR max_cred ≥ 2 | `reported` |
| Otherwise | `rumored` |

---

## 3. Signal Decay

Signals decay exponentially using tiered half-lives:

```
remaining = weight × 0.5^(hours_since_activation / half_life)
```

| Signal Weight | Half-Life | Rationale |
|---|---|---|
| ≥ 15 | 168h (7 days) | Nuclear tests, ICBM launches, Article 5 |
| ≥ 8 | 72h (3 days) | Major military operations |
| ≥ 4 | 24h (1 day) | Rhetoric, buildup, minor events |
| < 4 | 12h | Noise, minor indicators |

A signal is considered **expired** when its decayed weight drops below 0.5.

### Re-confirmation

When a signal is re-detected, `last_confirmed` is updated while
`activated_at` remains stable. This prevents decay from resetting on
every news mention while keeping the signal fresh.

---

## 4. Zone Coupling

When a tracker enters CRITICAL or IMMINENT zone, coupling rules boost
connected trackers. The system uses **proportional coupling**:

```
effective_boost = raw_boost × (source_prob / 100)
```

Rules:

- Only the **highest-threshold** matching rule per source is applied
- Per-target cap: **+25%** maximum total coupling boost
- Boosts are applied before zone classification

Example: If Iran Conventional is at 85% (IMMINENT), and the coupling
rule says "boost Israel-Lebanon by +15%", the effective boost is
`15 × 0.85 = 12.75%`.

---

## 5. Predictions

### Generation

Every pipeline run generates up to 15 event-based 24-hour predictions.
Predictions are scored by:

1. **Tracker probability** — higher prob = higher base confidence
2. **Trend direction** — rising trends get escalation predictions
3. **News keywords** — specific triggers (e.g., "hormuz") boost confidence
4. **Tracker-specific logic** — each zone has tailored prediction templates

### Evaluable Types

Each prediction is mapped to an evaluable type:

| Eval Type | Meaning |
|---|---|
| `probability_above` | Prob will stay above threshold |
| `probability_below` | Prob will drop below threshold |
| `trend_rising` | Trend will be "rising" |
| `signal_triggered` | Specific signal will be active |
| `zone_change` | Zone will match target |

### Evaluation

Predictions are evaluated when they expire (24h after generation).
Accuracy is tracked as:

```
accuracy = correct_predictions / total_evaluated × 100
```

---

## 6. Threat Zones

Zones are defined by probability thresholds:

| Zone | Min % | Colour | Meaning |
|---|---|---|---|
| IMMINENT | 60 | 🔴 | Conflict likely imminent |
| CRITICAL | 30 | 🟠 | Significant escalation risk |
| ELEVATED | 15 | 🟡 | Above-normal tension |
| DETERRENT | 0 | 🟢 | Baseline deterrence posture |

---

## 7. Module Architecture

```
scripts/
├── pipeline.py          # Main orchestrator
├── signals.py           # Signal classification, decay, matching
├── probabilities.py     # Zone classification, global probability
├── predictions.py       # Prediction generation, evaluation, dedup
├── dashboard_builder.py # HTML dashboard construction & injection
└── deploy.py            # Git commit/push automation
```

---

## 8. Data Flow

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  News Scanner   │────▶│  signals.py  │────▶│ current_state   │
│  (cron job)     │     │  classify +  │     │ .json           │
└─────────────────┘     │  match       │     └────────┬────────┘
                        └──────────────┘              │
┌─────────────────┐     ┌──────────────┐              ▼
│  tracker_config │────▶│ probabilities│     ┌─────────────────┐
│  .json          │     │  .py         │────▶│  index.html     │
└─────────────────┘     │  zone calc   │     │  (dashboard)    │
                        └──────────────┘     └────────┬────────┘
┌─────────────────┐     ┌──────────────┐              │
│  source_credib. │────▶│ predictions  │              ▼
│  .json          │     │  .py         │     ┌─────────────────┐
└─────────────────┘     │  gen + eval  │────▶│  deploy.py      │
                        └──────────────┘     │  git push       │
                                             └─────────────────┘
```

---

*Generated for DoomsdayWatch modular architecture refactor.*
