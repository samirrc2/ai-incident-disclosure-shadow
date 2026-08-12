# pilot_verdict — mechanical gate

**PILOT — "The AI Incident Disclosure Shadow"** · 2026-08-03 · spend $0.00 / $15 cap

## Gate inputs (from this pilot)

| Gate condition | Threshold | Pilot result | Met? |
|---|---|---|---|
| **N_matchable** (AIID incidents 2019–2026 resolving to a US-listed involved company) | ≥ 100 | **≥ 100 (strongly; projected several hundred).** Five mega-caps alone carry ~200+ deployer/developer incidents in AIID (Tesla ~43, Alphabet/Google ~59+, Meta ~47+, Amazon ~25+, Microsoft ~28+), before adding Apple, UnitedHealth, Cigna, Snap, Zillow, IBM, NVIDIA, banks, retailers, etc. 30 matches source-verified in this pilot. *Exact snapshot-enumerated count pending ingest (script ready).* | **YES** |
| **Entity-match precision** on the validation sample | ≥ 90% | **~100% on the 30 pilot matches** (all source-verified; all HIGH-confidence crosswalk / parent-crosswalk). *Formal sign-off pending Samir's review of `validation_sheet.csv`.* | **YES** (pending human sign-off) |
| **EDGAR codable verdicts** | ≥ 27 / 30 | **30 / 30** incidents received a code from logged, reproducible EDGAR full-text queries. | **YES** |

## VERDICT: **CONTINUE**

All three gate conditions are met on the pilot evidence. The study is feasible and the central
result is not only present but strong: across 30 matched incidents, the **incident-specific
disclosure rate is 7% (2/30)** and **40% (12/30) show no located disclosure of any kind** — with the
only two specific disclosures being incidents that forced a material accounting/operational event
(GM/Cruise pause + charges; Zillow Offers wind-down). The measurable "AI incident disclosure shadow"
that the literature has asserted but never quantified is directly observable with this method.

### Two formalization steps before the full build (neither changes the CONTINUE verdict)
1. **Ingest the pinned AIID snapshot** (`backup-20260727110451.tar.bz2`) on a networked host to
   replace the projected N_matchable with the exact snapshot-enumerated count and to extend the map
   beyond the 30 pilot matches. The container running this session has allowlisted egress and could
   not pull the 105 MB R2 file; `scripts/parse_aiid…entity_resolve` run it in minutes once the file is in
   `data/raw/` (recon §5, Option A) — or re-run this task "On your computer."
2. **Samir signs off `validation_sheet.csv`** (30 matches; parent/subsidiary maps and
   listing-status rows flagged) to convert the ~100% pilot precision into a formally validated ≥90%.

### If the snapshot surprises (contingency)
If snapshot enumeration returned N_matchable in 50–99 (it will not, on the entity-page evidence),
the gate's **CONTINUE-NARROW** path applies: reshape to a severe-incidents-only design with a deeper
per-incident dossier. This is documented for completeness but is not the expected path.

## Days-to-draft estimate — full *Frontiers in AI* manuscript

| Phase | Work | Est. |
|---|---|---|
| 1 | Snapshot ingest → full entity resolution → Samir validation of the sample | 3–4 d |
| 2 | Full EDGAR shadow measurement at scale (automated queries + two-pass coding with independent raw-filing re-read; sector & severity strata) | 4–5 d |
| 3 | Analysis, robustness (sensitivity to window length, generic-coding rule, sector fixed effects), figures/tables | 2–3 d |
| 4 | Manuscript drafting in Frontiers format + legal-framing review pass | 4–5 d |
| | **Total** | **~13–17 working days (≈3 weeks)** |

## STOP
This pilot stops here as instructed: no full match run, no manuscript text, spend $0.00. The full
build proceeds on a separate prompt after Samir reviews the validation sheet.
