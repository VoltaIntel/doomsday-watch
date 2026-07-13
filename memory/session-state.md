# Session State

Last update: 2026-07-13T03:07Z

DoomsdayWatch 03Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published state: **73% / imminent** (raw **69.8%**); no numeric probability mover.
- Canonical signal change: `iran_conventional:oil_infrastructure_threat` cleared after expiry/decay review. The broader Hormuz conflict remains represented by `ceasefire_violation`, `diplomacy_active`, and `hormuz_closed`; Iran War remains 100%.
- Fresh evidence: Al Jazeera/NYT and RSS reporting reinforced the latest U.S. action near Hormuz and Iranian retaliation. No additional tracker crossed an evidence threshold.
- Energy: OilPriceAPI showed Brent **$79.02** and WTI **$74.28** at deploy.
- Full coupled table: Iran War **100 / imminent**, Russia-Ukraine **99 / imminent**, Israel-Lebanon **94 / imminent**, Sudan **90 / imminent**, Israel-Palestine **88 / imminent**, Eastern DR Congo **58 / imminent**, Iran Nuclear **54 / imminent**, Russia-NATO **52 / critical**, Pakistan-Afghanistan **46 / critical**, China-Taiwan **28 / elevated** (coupled score), DPRK **18 / elevated**, South Sudan/Abyei **12 / elevated**, India-Pakistan **11 / elevated**, Turkey **5 / deterrent**.
- No untracked crisis met the configured three-mention/two-source threshold.
- Live web search worked; Google News RSS and direct UN/NATO/EIA pages provided fallback/corroboration. Direct IAEA/OPEC returned 403 and configured OCHA/UN Sudan feed paths returned 404.
- Polymarket exact-slug sanity check refreshed at 03:06Z: U.S. invasion Iran 17.5%, Iran weapon 5.05%, Iran test 4.5%, NPT withdrawal 12.5%, NATO Article 5 6.5%, China invasion 3.85%, China-Taiwan clash 5.15%, DPRK invasion 2.0%, Ukraine peace deal 19.5%, Israel-Lebanon normalization 15.5%. Horizon/definition mismatch; not used for scoring.
- `data/current_state.json` was written atomically. `bash scripts/deploy.sh` succeeded twice (second run reconciled the expired signal), pushed, and passed JSON/canonical checks, all three Command Deck markers, clean worktree, and origin parity.
- Published head: `050053c`.
