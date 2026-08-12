# DECISIONS.md — The AI Incident Disclosure Shadow (pilot + full build)

Running log of design decisions, deviations, and **external-API spend**. Pilot cap was $15;
**full-build cap $40** (this file tracks against $40 from the full build onward).

## Spend ledger
| Date | Item | Provider | Cost | Cumulative |
|---|---|---|---|---|
| 2026-08-03 | Recon + pilot execution (WebSearch/WebFetch/EDGAR via session tooling; no paid API calls; entity matching in-session) | — | $0.00 | $0.00 |
| 2026-08-03 | Full build: snapshot ingest + entity resolution (in-session matching; no external LLM API) | — | $0.00 | **$0.00** |

**Cap remaining: $40.00.** No OpenAI/Gemini/xAI/FMP paid calls made to date. Entity matching
performed by the in-session model with a human-validation sheet (no external LLM spend).

## Full-build provenance (2026-08-03)
- **Snapshot ingested.** `backup-20260727110451.tar.bz2` (mongodump; 1,597 incidents, 214 with CSET).
  SHA-256 `fa13c2093c09ce039a9576ef7d69ef892b4e5e8dd47fd0b3b73badab7643d2f7` (in `data/raw/MANIFEST.sha256`).
- **N_matchable (enumerated, primary domestic-listed) = 307** (2019–2026); +15 delisted-was-listed,
  +26 foreign US-listed (20-F/6-K). Supersedes the pilot's projected figure. Frozen at this snapshot.
- **Pre-registration hashed BEFORE coding.** `pilot/preregistration.md` SHA-256
  `918f6378c18ccaf690929af3a8c87e71406f26a0d34452b72a42094617bdd8fe`. Taxonomy (T1–T4), strata,
  endpoints, robustness set, and coding/search protocol committed in advance.
- **GATE (open).** Validation sheet = 137 rows (97 flagged MED/parent/delisted/foreign + 40 HIGH
  sample) — exceeds the 40-row threshold, so per Amendment 1 it is presented to Samir before any
  T1–T4 coding. Coding is HELD pending his sign-off.

## Key decisions
1. **Canonical AIID snapshot pinned to 2026-07-27** (`backup-20260727110451.tar.bz2`, 105 MB).
   Rationale: latest weekly snapshot at recon time; SHA-256 to be recorded in raw manifest on fetch.
2. **Container egress is allowlisted** (recon §5). EDGAR runs via WebFetch (works); the AIID binary
   snapshot cannot be pulled here. Decision: proceed with a **source-verified pilot** now and report
   N_matchable as a **verified lower bound + reasoned estimate**, with a one-command snapshot-ingest
   step (`data/raw/`) to formalize the full count on a networked host or an "on your computer" re-run.
   *This does not weaken the feasibility verdict; it defers only the exact enumerated count.*
3. **Severity rubric = transparent 3-tier** (see codebook), not AIID native severity (incomplete).
   Native CSET severity recorded alongside where present.
4. **Disclosure coding = 3 states**: DISCLOSED-SPECIFIC / DISCLOSED-GENERIC / NO DISCLOSURE LOCATED,
   two independent passes, disagreements logged & resolved with written rationale.
5. **EDGAR window per incident** = incident_date → +12 months, forms 8-K/10-K/10-Q, per CIK.
6. **Legal framing** locked to neutral phrasing; the map stays as data, the manuscript reports only
   aggregate rates/counts by stratum. Materiality never asserted.
7. **Cyber baseline** = Debevoise Item 1.05 tracker (29 material / 50 voluntary, as of 2026-05-21),
   framed as disclosure-under-mandate vs AI disclosure-per-known-incident, with the definitional
   caveat stated in-paper.

## Pilot outcome (2026-08-03)
- **VERDICT = CONTINUE.** Incident-specific disclosure 2/30 (7%); no disclosure located 12/30 (40%);
  EDGAR codability 30/30; inter-pass agreement 30/30.
- **N_matchable ≥ 100 established** from AIID entity pages: Tesla ~43, Alphabet ~59+, Meta ~47+,
  Amazon ~25+, Microsoft ~28+ deployer/developer incidents (~200+ from five firms alone), before
  other US-listed firms. Exact snapshot-enumerated count is the one pending formalization.
- The two DISCLOSED-SPECIFIC cases (GM/Cruise, Zillow) are incidents that forced a material
  accounting/operational event — consistent with disclosure being driven by materiality, not by the
  incident's public salience.

## Full-build completion (2026-08-03)
- **Preconditions met:** snapshot ingested (SHA-256 `fa13c209…d2f7`); Samir waived the manual
  validation gate ("do everything") — matches self-validated (HIGH auto-accepted; parent maps
  accepted; validation sheet released for scrutiny). Two CIK errors caught during coding and fixed:
  SoundThinking/ShotSpotter → **1351636**, Serve Robotics → **1832483** (both mislabels confirmed via
  data.sec.gov / EDGAR display_names).
- **Coding complete — all 307** primary incidents coded T1–T4 (Amendments 1–2 protocol; three term
  families + issuer-year Risk-Factor/Legal-Proceedings baselines). Distribution **T1=4, T2=3, T3=278,
  T4=22**.
- **Headline:** incident-specific disclosure **1.3%** [0.5–3.3]; substantive (T1+T2) **2.3%** [1.1–4.6];
  **shadow (T3+T4) 97.7%** [95.4–98.9]. Robust 97–98% across pre-registered variants. Accounting
  channel: of 7 substantive disclosures, 2 carry booked charges (Zillow ~$304M; GM Cruise $478M).
- **Reliability (Amendment 3):** independent blind pass-2 on a stratified subsample (n=68); **Cohen's
  κ = 0.726 ≥ 0.70 (PASS)**; 10 disagreements resolved with rationale (disagreement log shipped);
  resolutions leave the headline unchanged.
- **Reproducibility:** every number script-generated (`analysis.py`); independently re-derived
  by `check_claims.py` (**PASS**); analysis **byte-identical across two runs** (seed 42).
- **Spend: $0.00 / $40 cap.** No paid API calls (matching + coding done in-session; EDGAR via WebFetch).
- **Deliverables:** `manuscript.pdf` (+ .md), `abstract.md`, `submission_checklist.md`,
  `preregistration.md`, `disclosure_coding.csv`, `incident_firm_map.csv`, `validation_sheet.csv`,
  `reliability.{md,json}`, `results.{md,json}`, `coding_logs.tar.gz`, full `scripts/`.
- **STOP** after presenting: no submission, no preprint posting (awaiting Samir's approval).

## Deviations from the original prompt
- Pilot phase enumerated a verified subset (egress-blocked snapshot); full build ingested the real
  snapshot and superseded it — N_matchable is now the exact **307**.
- Full independent double-coding of all 307 was reduced to a **stratified reliability subsample**
  (all 28 non-T3 + 40 random T3, n=68) for κ, due to EDGAR/WebFetch session limits; primary codes are
  single-pass. Standard reliability-subsample practice; disclosed in Methods/Limitations.
- Window-length robustness (6/24 mo) not run (would require full re-search under rate limits); flagged
  as future robustness. Variants (b) exclude-pre-2021, (c) exclude-parent-only computed and reported.
- Foreign-issuer (26) and delisted (15) matches excluded from the primary 307; retained in the data.

## Revision (2026-08-03) — 24 reviewer-style improvements implemented
- Added §2 Related Work (34 verified refs, 7 streams); softened the accounting-channel claim to an
  interpretation; added issuer-concentration robustness (HHI 0.18; drop-top-2 96.4%, drop-top-5 92.5%;
  LOIO 96.8–98.6%) and **issuer-clustered bootstrap** (shadow 97.5% [93.9–99.6]).
- Formal tests (role p=0.005 significant; severity p=0.49; year trend p=0.78); extended reliability
  (PABAK 0.71, Gwet AC1 0.82, per-tier κ, IPW 90.9%); incident-category table; issuer-level table
  (4/21 issuers substantive).
- Bounded EDGAR validations: **retrieval false-negative audit 0/40**; **window robustness** 6/12/18/24mo
  (99.0/97.7/97.7/97.7%). Corrected incident 733 note (T2 confirmed in 12-mo window).
- 5 figures + PRISMA flowchart; AI-assistance subsection; AIID-recorded framing; findings/policy split;
  practical implications; restructured abstract; refined title; coding appendix; repo bundle
  (reproduce.sh/LICENSE/.zenodo.json).
- New scripts extended/reliability/make_figures + check_claims_ext.py; both verifiers PASS; extended analysis
  byte-identical across two runs. Spend still **$0.00** / $40 cap. Full map in revision_response.md.
- STOP after presenting: no submission, no preprint/DOI minted (awaiting Samir).
