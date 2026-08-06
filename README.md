# The AI Incident Disclosure Shadow — reproducibility capsule

Reproducibility artifact for *"The AI Incident Disclosure Shadow: An Incident-Level Study Matching
AIID-Recorded AI Failures to U.S.-Listed Companies' Investor Disclosures, 2019–2026."* From a frozen,
SHA-256-pinned AI Incident Database snapshot and the frozen disclosure-coding logs, this capsule
regenerates **every number and figure in the paper, 100% offline and byte-identical across runs.**

## One-line reproduction

Code Ocean: press **Reproducible Run** (entry point `code/run`). Locally:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r code/requirements.txt
bash reproduce.sh
```

## What the run does (all offline; ~1 minute)

| Step | Script | Produces / checks |
|---|---|---|
| 0 | `p13_00_verify_inputs.py` | verifies SHA-256 of all 27 frozen data assets against `data/MANIFEST.sha256` |
| 1 | `p13_02_resolve.py` | reproduces entity resolution from `incidents.csv`; asserts **N_matchable = 307** and exact match to the frozen map |
| 2 | `rebuild_coded_table.py` | rebuilds all 307 disclosure codes from the shipped logs + documented corrections; asserts equality to the frozen coded table |
| 3 | `p13_20_analysis.py` | headline four-tier distribution + Wilson CIs + strata → `results/P13_results.{json,md}` |
| 4 | `p13_21_extended.py` | concentration (HHI, leave-one-out, drop-top-k), issuer-clustered bootstrap, formal tests, categories, window robustness, retrieval-validation summary → `results/P13_extended.{json,md}` |
| 5 | `p13_22_reliability_ext.py` | Cohen's κ, PABAK, Gwet's AC1, per-tier agreement, confusion matrix → `results/P13_reliability_ext.{json,md}` |
| 6 | `p13_30_figures.py` | Figures 1–5 → `results/figures/*.png` |
| 7 | `check_claims.py` | independently re-derives and asserts every headline number |
| 8 | `check_claims_ext.py` | independently re-derives and asserts every extended number |
| — | determinism | re-runs the analysis and asserts byte-identical outputs |
| — | `pytest` | locks the headline results as unit tests |

## Headline result (regenerated)

Incident-specific disclosure **1.3%** [0.5, 3.3]; substantive (T1+T2) **2.3%** [1.1, 4.6]; **shadow
(T3+T4) 97.7%** [95.4, 98.9] (issuer-clustered bootstrap 97.5% [93.9, 99.6]). Distribution
T1/T2/T3/T4 = 4/3/278/22 over N = 307 incidents · 21 issuers.

## Layout

```
code/
  run                     Code Ocean Reproducible Run entry point
  scripts/reproduce.sh    full offline pipeline (8 steps + determinism + tests)
  src/                    analysis + verifiers (numpy/scipy/matplotlib only)
  provenance/             the (network) EDGAR retrieval protocol that produced the frozen logs — NOT executed
  tests/                  pytest reproducibility tests
  requirements.txt        pinned deps
data/                     frozen, read-only inputs (SHA-256 pinned in MANIFEST.sha256; see archive_manifest.md)
environment/Dockerfile    Code Ocean image (pinned)
metadata/metadata.yml     capsule metadata
results/                  generated outputs (created by the run)
```

## Reproducibility model (please read)

The disclosure labels come from point-in-time SEC EDGAR full-text search (network, time-sensitive)
plus two-pass human-validated coding. Exactly as a frozen LLM-API dataset is not re-called, that
retrieval is **not re-executed** here: the **coded table and per-incident search logs are frozen and
SHA-256-pinned**, and the capsule reproduces all published results from them offline. `rebuild_coded_table.py`
proves the codes are a deterministic function of the shipped logs + documented corrections; the
retrieval protocol itself is in `code/provenance/` for anyone who wishes to re-derive the logs with
network access against the pinned snapshot. See `archive_manifest.md`.

## Legal / scope note

Outputs are aggregate rates and counts. The incident-to-issuer match table ships as data; the study
measures **disclosure behavior, not compliance**, and makes no assertion that any named company
violated a disclosure duty ("no related disclosure located" is a search-scoped finding). See `LICENSE`.
