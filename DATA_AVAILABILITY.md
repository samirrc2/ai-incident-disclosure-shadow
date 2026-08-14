# Data availability statement

*(For the Frontiers in Artificial Intelligence submission — deposit supporting
materials in a repository, then cite and link them from the article.)*

All data and code required to reproduce every number, table, and figure in this
article are openly available on GitHub, archived on Zenodo, and packaged as an
executable Code Ocean capsule:

- **Source repository:** https://github.com/samirrc2/ai-incident-disclosure-shadow
- **Executable capsule (Code Ocean):** https://doi.org/10.24433/CO.2340354.v2
- **Archive (Zenodo):** https://doi.org/10.5281/zenodo.\<ID\>  *(insert minted DOI on release)*

> Chincholikar, S. & Chawla, R. (2026). *The AI Incident Disclosure Shadow —
> reproducibility artifact* [data set + software]. Zenodo.
> https://doi.org/10.5281/zenodo.\<ID\>

Insert the minted Zenodo DOI here, in `CITATION.cff`, `.zenodo.json`, and the
manuscript's Data Availability statement / reference list.

## The deposit contains

- **Frozen four-tier disclosure coding** (`data/disclosure_coding.csv`, 307 incidents)
  and the **entity-resolution map** (`data/incident_firm_map.csv`), each SHA-256-pinned
  in `data/MANIFEST.sha256` and `archive_manifest.md`.
- **Frozen per-incident EDGAR search logs** (`coding/`) — pass-1 and pass-2 records,
  retrieval audit, and window-sensitivity checks — the provenance behind every label.
- **Analysis code** (`scripts/`): entity resolution, the four-tier analysis, extended
  concentration/robustness tests, exact inference, reliability, figures, and two
  independent claim verifiers.
- **Provenance**: hashed pre-registration and codebook (`pilot/`), decision log
  (`DECISIONS.md`), and the pilot verdict.

## Reproduction is offline, deterministic, and free

`bash reproduce.sh` regenerates the full analysis from the frozen coded table and logs
and re-derives every reported statistic through two independent verifiers
(`scripts/check_claims.py`, `scripts/check_claims_ext.py`). It makes **no vendor API
calls and requires no network or keys**.

The disclosure labels were produced by point-in-time SEC EDGAR full-text search
(network, time-sensitive) plus two-pass human-validated coding. As with a frozen
model-output dataset, that retrieval is **not re-executed**; the coded table and coding
logs are frozen, and the pipeline reproduces every published number from them.

## Upstream source (referenced by hash, not redistributed here)

AI Incident Database snapshot `backup-20260727110451.tar.bz2` (27 Jul 2026), SHA-256
`fa13c2093c09ce039a9576ef7d69ef892b4e5e8dd47fd0b3b73badab7643d2f7`, publicly available
from the Responsible AI Collaborative. `incidents.csv` is extracted from it.

No proprietary, personal, or confidential data are used or distributed. Only aggregate
rates and counts are reported; the study measures disclosure behavior, not compliance,
and makes no claim that any named company breached a disclosure obligation.
