# The AI Incident Disclosure Shadow

**An Incident-Level Study Matching AIID-Recorded AI Failures to U.S.-Listed
Companies' Investor Disclosures, 2019–2026**

**Authors:** Samir Chincholikar (Independent researcher) · Robin Chawla (Independent researcher, corresponding author)
**ORCID:** [0009-0007-2779-3492](https://orcid.org/0009-0007-2779-3492) · [0009-0007-2807-3948](https://orcid.org/0009-0007-2807-3948)
**Contact:** robin.chawla.cse14@iitbhu.ac.in · samir.chincholikar@gmail.com
Submitted to *Frontiers in Artificial Intelligence* (AI in Finance).

This repository is the reproducibility artifact for the article. It contains the code,
the frozen SHA-256-pinned inputs, and the deterministic pipeline that regenerate **every
quantitative result, table, and figure** in the manuscript.

> **What the study measures.** When a publicly recorded AI incident involves a U.S.-listed
> company, does the incident reach investors through that company's securities filings?
> We link every AI Incident Database (AIID) incident dated 2019–2026 (n = 1,389) to the
> organizations alleged to have deployed or developed the system, retain those resolving
> to a U.S.-listed issuer (N = 307 across 21 issuers), search each issuer's 8-K/10-K/10-Q
> over the following 12 months, and classify disclosure into a four-tier taxonomy. The
> headline: incident-specific disclosure is rare (**1.3%**, Clopper–Pearson 95% CI
> 0.4–3.3), and 97.7% of incidents form a disclosure "shadow" dominated by substitution
> into generic AI risk-factor language. **We report aggregate rates only and measure
> disclosure *behavior*, not legal compliance.**

## Repository layout

```
.
├── README.md                 — this file
├── CITATION.cff              — how to cite (article + artifact; both authors, ORCIDs)
├── DATA_AVAILABILITY.md      — repository / Zenodo / Code Ocean links
├── LICENSE                   — MIT
├── DECISIONS.md              — decision log + spend tracker ($0.00 external spend)
├── archive_manifest.md       — frozen data assets + SHA-256
├── environment.txt           — pinned versions (offline reproduction)
├── requirements.txt          — Python dependencies
├── reproduce.sh              — one-command offline reproduction
├── .zenodo.json              — Zenodo deposit metadata
│
├── scripts/                  — the pipeline (seed 42)
│   ├── parse_aiid.py         — extract snapshot → incidents table
│   ├── entity_resolve.py     — resolve deployer/developer → U.S.-listed issuer (N=307)
│   ├── edgar_search.py       — point-in-time EDGAR full-text search
│   ├── code_shadow.py        — apply the four-tier taxonomy
│   ├── analysis.py           — headline distribution + Wilson CIs + strata
│   ├── extended.py           — concentration/HHI, clustered bootstrap, formal tests
│   ├── inference.py          — Clopper–Pearson + Monte-Carlo exact permutation tests
│   ├── reliability.py        — Cohen's κ, PABAK, Gwet's AC1, confusion matrix
│   ├── make_figures.py       — the four publication figures
│   ├── make_cset_appendix.py — the CSET-severity appendix (Table 6)
│   ├── check_claims.py       — independent verifier (headline numbers)
│   ├── check_claims_ext.py   — independent verifier (extended numbers)
│   └── audit_manuscript.py   — manuscript-wide numerical-consistency audit
│
├── data/                     — frozen inputs (SHA-256 in data/MANIFEST.sha256)
│   ├── disclosure_coding.csv — frozen four-tier coded table (307 incidents)
│   ├── incident_firm_map.csv — frozen entity-resolution map
│   ├── validation_sheet.csv  — resolution validation sheet
│   ├── incidents.csv         — AIID incident fields used by the analysis (1,597 rows)
│   ├── inbox/                — parsed AIID incidents
│   └── raw/                  — pinned snapshot (referenced by hash) + MANIFEST
│
├── coding/                   — frozen per-incident EDGAR search logs (provenance)
├── pilot/                    — hashed pre-registration, codebook, pilot verdict
├── recon/                    — Phase-0 data reconnaissance
├── revision/                 — extended results, inputs, and figures
├── frontiers/                — the manuscript (manuscript.tex/.pdf, references.bib,
│                               Frontiers class/style files, figures/, logos) and
│                               submission/ (portal upload bundle: Figure1–4, cover letter)
├── environment/              — Dockerfile + notes (pinned reproduction container)
├── metadata/                 — deposit metadata + reproduction verification log
├── docs/                     — standby reviewer-response note
└── codeocean/                — the published Code Ocean capsule (frozen; do not edit)
```

## Reproduce

Reproduction is **100% offline, deterministic, and free** — a pure function of the frozen
inputs. No API keys, network, or paid services are used.

```bash
pip install -r requirements.txt
bash reproduce.sh
```

`reproduce.sh` verifies the frozen inputs against `data/MANIFEST.sha256`, regenerates the
analysis from `data/disclosure_coding.csv`, rebuilds the figures, and re-derives every
reported statistic through two independent verifiers and a manuscript-wide
numerical-consistency audit. Expected tail line:

```
OK: reproduced. Key result: shadow (T3+T4) = 97.7% [95.4, 98.9]; T1 specific = 1.3%.
```

The original data-gathering path (AIID parse → point-in-time EDGAR search) is documented
but **not** part of the offline reproduction, because EDGAR full-text search is a
network, time-sensitive service; the coded table and search logs it produced are frozen.

## Provenance & guardrails

- **Frozen inputs.** Every primary asset is SHA-256-pinned (`data/MANIFEST.sha256`,
  `archive_manifest.md`) and checked before analysis. Seed is fixed at 42.
- **Independent verification.** All headline and extended numbers are re-derived by
  `scripts/check_claims.py` and `scripts/check_claims_ext.py`.
- **Legal care (binding).** Published outputs are aggregate rates/counts. The study never
  states or implies that any named company violated a disclosure duty. Neutral phrasing
  only — *"no related disclosure located,"* never *"failed to disclose"* or *"concealed."*
  Materiality is a legal judgment we do not make; we measure disclosure **behavior**, not
  compliance.
- **Cost.** External-API spend cap was **$15**, tracked in `DECISIONS.md`. This project
  spent **$0.00**.

## Citation

See `CITATION.cff`. Please cite both the article (*Frontiers in Artificial Intelligence*,
2026) and this artifact.

## License

MIT — see `LICENSE`.
