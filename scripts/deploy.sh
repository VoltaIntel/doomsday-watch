#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 scripts/fetch_oil_prices.py 2>/dev/null || true
python3 scripts/ingest/polymarket.py 2>/dev/null || true
NUKE_WATCH_AUTO_GIT=1 python3 scripts/pipeline.py
