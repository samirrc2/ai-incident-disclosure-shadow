#!/usr/bin/env bash
# Paper 13 — full offline reproduction (Code Ocean Reproducible Run target).
# 100% offline: reads only frozen data assets under data/; writes only under results/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/code/src"
export MPLBACKEND=Agg
export PYTHONHASHSEED=0
export SOURCE_DATE_EPOCH=1735689600   # deterministic
mkdir -p results/figures

echo "############################################################"
echo "# Paper 13 — The AI Incident Disclosure Shadow — reproduce  #"
echo "############################################################"

step () { echo; echo ">>> $1"; python3 "code/src/$2"; }

step "0/8  Verify SHA-256 of frozen inputs"        p13_00_verify_inputs.py
step "1/8  Reproduce entity resolution (N=307)"     p13_02_resolve.py
step "2/8  Rebuild disclosure codes from logs"      rebuild_coded_table.py
step "3/8  Headline analysis (distribution, CIs)"   p13_20_analysis.py
step "4/8  Extended analysis (concentration/tests)" p13_21_extended.py
step "5/8  Extended reliability (kappa/AC1)"         p13_22_reliability_ext.py
step "6/8  Figures"                                 p13_30_figures.py
step "7/8  Verify every headline number"            check_claims.py
step "8/8  Verify every extended number"            check_claims_ext.py

echo; echo ">>> Determinism: byte-identical double-run check"
h1=$(sha256sum results/P13_results.json results/P13_extended.json results/P13_reliability_ext.json | sha256sum | cut -d' ' -f1)
python3 code/src/p13_20_analysis.py            >/dev/null
python3 code/src/p13_21_extended.py            >/dev/null
python3 code/src/p13_22_reliability_ext.py     >/dev/null
h2=$(sha256sum results/P13_results.json results/P13_extended.json results/P13_reliability_ext.json | sha256sum | cut -d' ' -f1)
if [[ "$h1" == "$h2" ]]; then echo "    PASS — analysis outputs byte-identical across two runs (sha ${h1:0:16}…)"; else echo "    FAIL — non-deterministic output"; exit 1; fi

echo; echo ">>> Unit tests"
python3 -m pytest -q code/tests

echo; echo "############################################################"
echo "# REPRODUCTION COMPLETE. Headline: incident-specific disclosure"
echo "# 1.3% [0.5,3.3]; shadow (T3+T4) 97.7% [95.4,98.9]; N=307.       "
echo "# All outputs in results/.                                       "
echo "############################################################"
