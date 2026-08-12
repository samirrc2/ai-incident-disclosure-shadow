# Provenance — how the frozen coding logs were produced (NOT part of the reproducible run)

The disclosure codes in `data/coding_logs/` were produced by point-in-time full-text search of
SEC EDGAR (`efts.sec.gov`) over each issuer's 8-K/10-K/10-Q in the 12 months after each incident,
followed by two-pass human-validated coding. That retrieval **requires network access** and is
inherently point-in-time, so — exactly as an LLM-API dataset is frozen rather than re-called — it is
**not re-executed** by the reproducible run. The scripts here document the deterministic query
protocol that generated the logs:

- `edgar_search.py` — emits the exact, logged `efts.sec.gov` query URLs per incident
  (specific + legal-proceedings + generic term families). With `--run` (network) it re-executes them.
- `shadow_lib.py` — the deterministic EDGAR-URL builder + disclosure-window helper.

To re-derive the logs from scratch (with network), a reviewer runs these against the pinned AIID
snapshot (SHA-256 in `../../archive_manifest.md`). The offline capsule reproduces every published
number and figure from the frozen logs without them.
