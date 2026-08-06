# Archive manifest — frozen data assets (the paper's inputs)

These files are the paper's **frozen primary data**. Do **not** regenerate them; any correction
requires a new versioned file plus a changelog entry here. SHA-256 of every asset is pinned in
`data/MANIFEST.sha256` and verified at the start of every run by `code/src/p13_00_verify_inputs.py`.

## Reproducibility model
The disclosure labels were produced by point-in-time SEC EDGAR full-text search (network,
time-sensitive) and two-pass human-validated coding. As with a frozen LLM-API dataset, that
retrieval is **not re-executed** in the capsule; instead the **coded table and coding logs are
frozen**, and the capsule reproduces every published number and figure from them 100% offline. The
retrieval protocol that produced the logs is documented (non-executed) in `code/provenance/`.

## Key frozen assets
| Asset | Role | SHA-256 |
|-------|------|---------|
| `data/P13_disclosure_coding.csv` | frozen four-tier coded table (307 incidents) | `ee93ac504a1985c3bc774a774a7c30bb7ef367f02cbcddc73d1ecf1d06b0a4d4` |
| `data/P13_incident_firm_map.csv` | frozen entity-resolution map | `8880bf85537a3d3d9fb8c40f135313705cb44979a0d2775dc85e71c3d0162ed1` |
| `data/raw_extracted/incidents.csv` | AIID incidents (extracted from the pinned snapshot) | `ca8cb38946a031c1c48860ef725a11502fe7e4a1d7c8ce1fbc74a2b7b6c69fd1` |
| `data/coding_logs/…` | per-incident EDGAR search records (pass1, pass2), retrieval audit, window sensitivity, corrections | see `data/MANIFEST.sha256` |

## Upstream source (not bundled; referenced by hash)
- AI Incident Database snapshot `backup-20260727110451.tar.bz2` (27 Jul 2026), SHA-256
  `fa13c2093c09ce039a9576ef7d69ef892b4e5e8dd47fd0b3b73badab7643d2f7`. Publicly available from the Responsible AI Collaborative; `incidents.csv` and
  `classifications_CSETv1.csv` are extracted from it and shipped under `data/raw_extracted/`.
  To re-verify, place the snapshot in `data/raw/` and confirm the SHA-256 matches.
