# Session State

Last update: 2026-07-17T21:10Z

DoomsdayWatch 21Z morning deep scan completed from `/home/openclaw/.openclaw/workspace/nuke-watch`.

- Published assessment remains **74% / imminent**; weighted coupled score **73.50%**. No tracker probability or canonical signal moved.
- Fresh late-window evidence: Lebanon said Israeli forces destroyed three southern schools; later Gaza coverage raised the funeral toll from seven to eight. Neither crossed a new configured threshold; the Lebanon claim was not independently verified.
- Coupled table: Iran War **100**, Russia-Ukraine **99**, Israel-Lebanon **94**, Sudan **90**, Israel-Palestine **88**, Iran Nuclear **54**, Russia-NATO **52**, Eastern DR Congo **52**, Pakistan-Afghanistan **46**, Yemen/Red Sea **38**, China-Taiwan **28**, DPRK **18**, South Sudan/Abyei **12**, India-Pakistan **11**, Turkey **5**.
- Active canonical signals: `iran_conventional:{ceasefire_violation,hormuz_controlled_not_closed}`, `israel_lebanon:diplomacy_active`, `iran_nuclear:iaea_access_denied`, `yemen_red_sea:external_backing`.
- OilPriceAPI: Brent **$88.08**, WTI **$82.08**, gasoline **$3.39**, diesel **$4.08**.
- Exact-slug Polymarket sanity: U.S.-Iran invasion **26.5%**, NATO Article 5 **8.0%**, China-Taiwan clash **4.95%**, China invasion **3.95%**, Iran weapon **5.4%**, Iran test **4.5%**, NPT withdrawal **13.55%**. Horizon/definition mismatch; sanity-only.
- Auto-detection added no tracker. Ethiopia/Tigray, Thailand-Cambodia, South China Sea, Syria, Sahel, Kosovo-Serbia, Guyana-Venezuela and Armenia-Azerbaijan did not meet the fresh three-mention/two-source gate.
- All **20 Tavily searches** failed HTTP 432. Google News RSS for every configured tracker, targeted supplements, direct UN/NATO/EIA, browser, terminal HTTP, OilPriceAPI and Gamma completed fallback coverage. IAEA browser hit Cloudflare; direct IAEA/OPEC returned 403 and configured OCHA/UN Sudan paths returned 404.
- Atomic state update and deploy/push succeeded. Canonical IDs/signals, timeline, Command Deck markers and origin parity passed. Final head: `c09c156d`.
- Test caveat: **31 passed**; the 11 smoke cases all errored at their shared fixture because its pipeline subprocess exceeded the hard 60-second timeout. Production deploy succeeded in about 64 seconds; no smoke assertion failed.
