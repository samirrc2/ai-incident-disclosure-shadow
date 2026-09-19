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

# ---- (0a) use a local pinned virtualenv if one exists ------------------------
# If you created ./.venv (python3 -m venv .venv && .venv/bin/pip install -r
# requirements.txt), use it automatically so the system python is never touched.
if [ -z "${VIRTUAL_ENV:-}" ] && [ -f ".venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  . .venv/bin/activate
  echo "  [venv] using $(command -v python3)"
fi

# ---- (0b) dependency preflight -----------------------------------------------
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

# ---- (2b) revision analyses --------------------------------------------------
# Everything added in response to review. Order matters: each step consumes the
# outputs of the ones above it.
python3 scripts/t3_split.py          # T3 -> T3a / T3b relatedness split
python3 scripts/cocandidates.py      # co-candidate issuers + tie-break variants
python3 scripts/asofdate.py          # as-of-date ownership for parent-linked incidents
python3 scripts/crosswalk_review.py  # row-by-row verdicts on the 137-row crosswalk
python3 scripts/attribution.py       # attribution basis for all 307 incidents
python3 scripts/t2_adjudicate.py     # adjudication of the three T2 codes
python3 scripts/severity_power.py    # exact power and MDE for the severity contrast
python3 scripts/role_loo.py          # leave-one-positive-out on the role contrast
python3 scripts/entity_audit_sample.py   # the blind 80-incident sample (seed 42, deterministic)
python3 scripts/entity_reliability.py data/entity_audit_return.csv
python3 scripts/tables.py            # every table -> results/tables.json
python3 scripts/make_figures.py      # figures -> frontiers/figures/ + submission/
python3 scripts/make_tables_tex.py   # typeset table bodies
python3 scripts/supplementary.py     # frontiers/submission/supplementary.tex
python3 scripts/author_review.py      # AUTHOR_REVIEW.csv, cited in the manuscript
python3 scripts/family_triggers.py   # the word behind every family match, for audit
python3 scripts/number_audit.py      # ledger: every number -> script -> output

# ---- (3) independent verification of every reported number -------------------
python3 scripts/check_claims.py
python3 scripts/check_claims_ext.py
python3 scripts/audit_manuscript.py    # manuscript-wide numerical consistency audit
python3 scripts/verify_all.py     # standing checks: every number tied back to an output

echo "OK: reproduced. Key result: shadow (T3+T4) = 97.7% (Clopper-Pearson 95% CI [95.4, 99.1]); T1 specific = 1.3%."
