#!/usr/bin/env bash
# ============================================================================
# The AI Incident Disclosure Shadow — REPRODUCE (offline, $0, no network)
# ============================================================================
# Regenerates the full analysis from the FROZEN coded table and logs, then
# re-derives every reported statistic through two independent verifiers. This
# NEVER calls a vendor API, never touches the network, and never spends money —
# it is a pure, deterministic function of the frozen inputs in data/ and coding/.
#
#   bash reproduce.sh
#
# The original data-gathering path (network, time-sensitive) is documented below
# but is NOT part of this reproduction:
#   python3 scripts/parse_aiid.py       # extract AIID snapshot -> incidents table
#   python3 scripts/entity_resolve.py   # resolve -> data/incident_firm_map.csv (N=307)
#   python3 scripts/edgar_search.py     # point-in-time SEC EDGAR full-text search
#   python3 scripts/code_shadow.py      # apply the four-tier taxonomy
# ============================================================================
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONHASHSEED=0 MPLBACKEND=Agg

echo "== reproduce: offline · \$0 · no network =="

# ---- (0) dependency preflight ------------------------------------------------
# On a clean machine the system python may lack the pinned analysis stack. Fail
# fast with an actionable message rather than a bare ModuleNotFoundError deep in
# the run. To reproduce exactly, install the pinned versions first:
#   python3 -m pip install -r requirements.txt      # (or: docker build/run)
python3 - <<'PY' || { echo "!! Missing dependencies. Run: python3 -m pip install -r requirements.txt"; exit 3; }
import importlib.util, sys
missing = [m for m in ("numpy", "scipy", "matplotlib") if importlib.util.find_spec(m) is None]
if missing:
    print("  [FAIL] missing modules:", ", ".join(missing)); sys.exit(1)
import numpy, scipy, matplotlib
print(f"  [OK ] numpy {numpy.__version__} · scipy {scipy.__version__} · matplotlib {matplotlib.__version__}")
PY

# ---- (1) integrity: frozen inputs must match recorded SHA-256 ----------------
python3 - <<'PY'
import hashlib, sys
from pathlib import Path
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
pinned = {}
for line in Path("data/MANIFEST.sha256").read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    h, _, path = line.partition("  ")
    pinned[path] = h
core = ["data/disclosure_coding.csv", "data/incident_firm_map.csv",
        "data/validation_sheet.csv", "data/incidents.csv", "data/inbox/aiid_incidents.csv"]
ok = True
for p in core:
    got = sha(p)
    match = (got == pinned.get(p))
    ok &= match
    print(f"  [{'OK ' if match else 'FAIL'}] {p}  {got[:16]}…")
sys.exit(0 if ok else 2)
PY
[ $? -ne 0 ] && { echo "!! INTEGRITY FAILED — frozen inputs do not match recorded hashes."; exit 2; }
echo "  [OK ] frozen inputs verified against data/MANIFEST.sha256"

# ---- (2) regenerate the analysis from the frozen coded table -----------------
python3 scripts/analysis.py       # headline distribution + Wilson CIs + strata
python3 scripts/extended.py       # concentration/HHI, clustered bootstrap, tests
python3 scripts/reliability.py    # Cohen's kappa, PABAK, Gwet AC1, confusion
python3 scripts/inference.py      # Clopper-Pearson + Monte-Carlo exact permutation
python3 scripts/make_figures.py   # the four publication figures -> frontiers/figures/

# ---- (3) independent verification of every reported number -------------------
python3 scripts/check_claims.py
python3 scripts/check_claims_ext.py
python3 scripts/audit_manuscript.py    # manuscript-wide numerical consistency audit

echo "OK: reproduced. Key result: shadow (T3+T4) = 97.7% (Clopper-Pearson 95% CI [95.4, 99.1]); T1 specific = 1.3%."
