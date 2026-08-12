# Archive manifest — frozen data assets (the paper's inputs)

These files are the paper's **frozen primary data**. Do **not** regenerate them; any
correction requires a new versioned file plus a changelog entry here. The SHA-256 of
every asset is pinned in `data/MANIFEST.sha256` and verified at the start of
`reproduce.sh`.

## Reproducibility model

The disclosure labels were produced by point-in-time SEC EDGAR full-text search
(network, time-sensitive) and two-pass human-validated coding. As with a frozen
model-output dataset, that retrieval is **not re-executed**; instead the **coded table
and coding logs are frozen**, and the pipeline reproduces every published number and
figure from them 100% offline. The retrieval protocol that produced the logs is
documented in `pilot/codebook.md` and `pilot/preregistration.md`.

## Key frozen assets

| Asset | Role | SHA-256 |
|-------|------|---------|
| `data/disclosure_coding.csv` | frozen four-tier coded table (307 incidents) | `ee93ac504a1985c3bc774a774a7c30bb7ef367f02cbcddc73d1ecf1d06b0a4d4` |
| `data/incident_firm_map.csv` | frozen entity-resolution map | `8880bf85537a3d3d9fb8c40f135313705cb44979a0d2775dc85e71c3d0162ed1` |
| `data/validation_sheet.csv` | resolution validation sheet | `93a4448224916d80f532cdfa0bf3777baa9fd3883ecc1fd960c3a67b6de61e20` |
| `data/incidents.csv` | AIID incident fields (id/date/title/description/deployer/developer) used by the analysis | see `data/MANIFEST.sha256` |
| `data/inbox/aiid_incidents.csv` | parsed AIID incidents | `6fc38b31dd5178c5874deb9d53e19acc03490ef039bf1ebeaaf3a37997783df8` |
| `coding/…` | per-incident EDGAR search records (batches, pass2), results | see `data/MANIFEST.sha256` |

## Upstream source (not bundled; referenced by hash)

- AI Incident Database snapshot `backup-20260727110451.tar.bz2` (27 Jul 2026), SHA-256
  `fa13c2093c09ce039a9576ef7d69ef892b4e5e8dd47fd0b3b73badab7643d2f7`. Publicly available
  from the Responsible AI Collaborative; `incidents.csv` is extracted from it. To
  re-verify, place the snapshot in `data/raw/` and confirm the SHA-256 matches
  `data/raw/MANIFEST.sha256`.

## Evidentiary chain (incident → issuer → filing → evidence → tier → statistic)

Every coded incident preserves the full chain needed to reconstruct its verdict, so the
result is auditable end-to-end, not only re-runnable:

- `data/disclosure_coding.csv` carries, per incident: `incident_id` (AIID), `matched_company`,
  `ticker`, `CIK`, `role`, `severity_tier` + `severity_source` (CSET vs rubric),
  `disclosure_code` (T1–T4), `code_confidence`, `accounting_filing_item`,
  `accounting_booked_impact`, the `evidence` excerpt/hit, and the coding `rationale`.
- `coding/batches/` and `coding/results/` hold the pass-1 per-incident search records;
  `coding/pass2/` holds the independent blind second-coding of the reliability subsample.
- `pilot/edgar_query_manifest.csv` logs the deterministic EDGAR query URLs behind each verdict.
- `revision/inputs/retrieval_*.json` hold the full-filing retrieval-validation audit records.

The disclosure labels are frozen because point-in-time EDGAR full-text search is a network,
time-sensitive service; the coded table and these logs are the immutable record from which
every published number is regenerated offline. Where practical, filing identifiers
(accession-level references) are retained in the evidence field so the chain survives future
changes to EDGAR's search index.

## Corrections log

- **2026-08 (v1.1):** Incident 127 (Microsoft; disclosure code T4) had study severity
  "Limited" while carrying the identical CSET record (harm level "none"; tangible harm
  "tangible harm definitively occurred"; 0 lives lost; 0 injuries) as four incidents coded
  Severe (92, 116, 149, 220). Under the stated CSET-precedence rule, this was a coding
  error; severity was corrected Limited → Severe. Effect: severe tier 41 → 42, limited tier
  216 → 215; the four-tier disclosure distribution, shadow rate, and inter-coder reliability
  are unaffected (127's disclosure code is unchanged). The by-severity permutation test
  recomputes to p = 0.61 (was 0.49); the conclusion (no severity gradient) is unchanged.
  `data/MANIFEST.sha256` updated to the corrected `disclosure_coding.csv` hash.
