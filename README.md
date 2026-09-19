# The AI Incident Disclosure Shadow

**Tracking AI Incidents into U.S. Securities Filings**

**Authors:** Samir Chincholikar (independent researcher) · Robin Chawla (independent researcher, corresponding author)
**ORCID:** [0009-0007-2779-3492](https://orcid.org/0009-0007-2779-3492) · [0009-0007-2807-3948](https://orcid.org/0009-0007-2807-3948)
**Contact:** robin.chawla.cse14@iitbhu.ac.in · samir.chincholikar@gmail.com
Under review at *Frontiers in Artificial Intelligence* (AI in Finance).

This repository is the reproducibility artifact for the article. It holds the frozen,
SHA-256-pinned inputs and the deterministic pipeline that regenerates **every reported
number, table and figure**, then verifies them against the manuscript.

> **What the study measures.** When a publicly recorded AI incident involves a U.S.-listed
> company, does it become identifiable in that company's securities filings? We link AI
> Incident Database (AIID) incidents dated 2019–2026 (n = 1,389) to the organizations named
> as developers or deployers, retain those resolving to U.S.-listed domestic filers
> (**N = 307 across 21 issuers**), search each issuer's 8-K, 10-K and 10-Q over the
> following 12 months, and assign one of four disclosure tiers.
>
> Incident-specific disclosure occurs in **1.3%** of incidents (Clopper–Pearson 95% CI
> 0.4–3.3). The remaining **97.7%** (95.4–99.1) form the disclosure shadow. Splitting the
> generic-language tier by relatedness, **70.4%** (64.9–75.4) of incidents have at most
> weakly related filing language.
>
> **The estimates are conditional** on an incident being AIID-recorded and issuer-matchable.
> They measure disclosure *behaviour* in a defined SEC filing universe — not legal
> compliance, and not all investor-facing communication.

## Reproduce

Offline, deterministic, no API keys and no network.

```bash
pip install -r requirements.txt
bash reproduce.sh
```

Each frozen input is checked against `data/MANIFEST.sha256` before anything runs; a
mismatch stops the pipeline. The run rebuilds the derived data, the results, the figures
and the supplementary tables, then applies **77 standing checks** that tie every
number in the manuscript back to a generated output. It fails if any check fails.

Expected tail line:

```
OK: reproduced. Key result: shadow (T3+T4) = 97.7% (Clopper-Pearson 95% CI [95.4, 99.1]); T1 specific = 1.3%.
```

Outputs are byte-identical across runs.

## Layout

```
data/        frozen inputs, hashed in data/MANIFEST.sha256, plus the derived tables
             the pipeline rebuilds (t3_split, attribution, asofdate, crosswalk_review,
             cocandidates, role_loo, t2_adjudication, entity_audit_sample)
coding/      per-incident filing-search records and coding batches
scripts/     the pipeline, seed 42
results/     everything the run generates
frontiers/   manuscript.tex, references.bib, figures/, and submission/ (supplementary,
             cover letter, tracked-changes build, the as-submitted v1 sources)
docs/        reviewer reports, revision log, citation verification, editorial audits
pilot/       hashed pre-registration, codebook, pilot verdict
recon/       phase-0 data reconnaissance
environment/ Dockerfile for the pinned container
codeocean/   the Code Ocean capsule (capsule_v3, submitted) and the previously
             published capsule, kept frozen
```

### The pipeline

`reproduce.sh` runs these in order. The first four reproduce the original analysis; the
rest were added in revision.

| stage | scripts |
|---|---|
| core analysis | `analysis` · `extended` · `reliability` · `inference` |
| relatedness split | `t3_split` (uses `taxonomy`) |
| entity resolution | `cocandidates` · `asofdate` · `crosswalk_review` · `attribution` |
| adjudication | `t2_adjudicate` |
| inference detail | `severity_power` · `role_loo` |
| second-coder audit | `entity_audit_sample` · `entity_reliability` |
| assembly | `tables` · `make_figures` · `make_tables_tex` · `supplementary` |
| provenance | `author_review` · `family_triggers` · `number_audit` |
| verification | `check_claims` · `check_claims_ext` · `audit_manuscript` · `verify_all` |

`config`, `paths`, `stats_lib`, `shadow_lib`, `crosswalk` and `taxonomy` are libraries.

`parse_aiid`, `entity_resolve`, `edgar_search` and `code_shadow` are the original
data-gathering path. They need the network and a live EDGAR full-text search, so they are
**not** part of the offline reproduction; the coded table and search logs they produced are
frozen inputs here.

## Guardrails

- **Frozen inputs.** Every primary asset is SHA-256-pinned and checked before analysis.
  Inputs no script can regenerate — the second coder's returned codings, the adjudication
  record, the retrieval and alternative-window samples — are hashed too.
- **Traceability.** `results/number_audit.csv` maps each reported number to the script that
  produces it and the output file it lands in. `results/family_triggers.csv` records the
  word behind every taxonomy match, so the coding is readable rather than opaque.
- **Legal care (binding).** Published outputs are aggregate rates and counts. The study
  never states or implies that any named company violated a disclosure duty. Neutral
  phrasing only — *"no related disclosure located"*, never *"failed to disclose"* or
  *"concealed"*. Materiality is a legal judgment we do not make.
- **Determinism.** Seed 42 throughout; no network; outputs byte-stable across runs.

## Data availability

Everything needed to reproduce the study is in this repository (MIT for code, CC0 for
data). A deterministic Code Ocean capsule containing the same material has been submitted;
its DOI will be added at proof stage.

## Citation

See `CITATION.cff`.

## Licence

Code MIT, data CC0 — see `LICENSE`.
