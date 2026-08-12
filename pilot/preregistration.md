# preregistration — Pre-registration-style analysis plan (committed BEFORE full coding)

**"The AI Incident Disclosure Shadow"** · target *Frontiers in AI* · date 2026-08-03
Pilot numbers are known; this plan fixes taxonomy, strata, endpoints, and robustness set in advance
of any T1–T4 coding. The SHA-256 of this file is recorded in DECISIONS.md; coding starts only after
the hash is logged and Samir's match validation is ingested.

## 1. Data & scope (fixed)
- Corpus: AIID full snapshot **backup-20260727110451.tar.bz2** (SHA-256 in `data/raw/MANIFEST.sha256`).
- Universe: incidents with `date` in **2019-01-01 … 2026-12-31** (n = 1,389).
- Match: ≥1 deployer/developer slug resolving to a **US-listed** company via `crosswalk.py`.
  Primary population = **domestic 8-K/10-K/10-Q filers** (status LISTED or PARENT). Secondary,
  reported separately: DELISTED-was-listed (date-dependent) and FOREIGN (20-F/6-K filers).
- **N_matchable (primary) = 307** (pre-registered as the enumerated figure; frozen at this snapshot).

## 2. Disclosure taxonomy (Amendment 2 — fixed 4-tier, exactly one per incident)
- **T1 DISCLOSED-SPECIFIC** — a window filing references the incident as such.
- **T2 LEGAL-PROCEEDINGS-ONLY** — the legal/regulatory consequence (settlement, recall,
  investigation) appears **without** framing it as an AI/algorithmic-system incident.
- **T3 GENERIC-RISK-LANGUAGE** — new/materially-changed AI risk-factor language plausibly prompted
  by the incident; event never named. Coded conservatively; uncertainty flagged.
- **T4 NO DISCLOSURE LOCATED.**

## 3. Search protocol (Amendment 1 — fixed, three term families per incident)
For every matched incident, over incident_date → +12 months, forms 8-K/10-K/10-Q, per CIK:
(a) incident-specific terms (product/system/event); (b) **legal-proceedings vocabulary** (consent
decree, civil investigative demand, settlement, recall, the regulator's name, docket/case numbers
where they exist); (c) generic AI-incident terms. **Plus** a mandatory hand-read of the **Legal
Proceedings and Risk Factors** sections of the first annual report (10-K) following the incident —
eyes on the sections, not only search. All queries logged as deterministic `efts` URLs; per-incident
search records shipped.

## 4. Coding protocol (Amendment 3 — fixed)
Pass 1 codes from the search records. **Pass 2 is independent**: a second coding run against the raw
filings directly, with **no access** to pass-1 evidence summaries or verdicts. Report **Cohen's
kappa per tier and overall**; resolve disagreements with written rationale; ship the disagreement
log. **Stop rule: if overall kappa < 0.70 on the T1–T4 scheme, halt and report before proceeding.**

## 5. Severity tiers (fixed rubric; CSET where available else rubric-coded)
T3-severe / T2-moderate / T1-limited per `codebook.md`. CSET v1 covers 40/307 matched incidents;
the remainder are rubric-coded from report evidence with the same human-verifiable design. Severity
coverage and method reported transparently.

## 6. Endpoints (fixed)
1. **T1–T4 distribution**, overall and stratified by **severity, year, sector, developer-vs-deployer
   role**, with exact counts and **Wilson 95% confidence intervals** on each rate.
2. **Shadow rate** = T4 alone, and T3+T4 (no *substantive* disclosure), overall and by stratum.
3. **Accounting-channel table** (Amendment 4): for every T1/T2 incident, the filing item/section that
   carried it and whether a **booked financial impact** accompanied it. Pre-registered hypothesis:
   *disclosure occurs when (and only when) the incident becomes a financial-statement event — the
   materiality regime transmits AI incidents through the accounting channel, not the risk channel.*
4. **Cyber benchmark**: Debevoise Item 1.05 series (29 material / 50 voluntary, 2026-05-21), reported
   with the **disclosure-under-mandate vs disclosure-per-known-incident** asymmetry stated in Results.

## 7. Robustness set (fixed, pre-committed)
(a) search-window length **6 / 12 / 24 months**; (b) **excluding pre-2021** incidents;
(c) **excluding parent-only** matches (listed entity is parent, not direct operator);
(d) **coder-1-only vs resolved** codes. Each reported as a shift in the headline shadow rate + CI.

## 8. Legal care (binding, unchanged)
Aggregate rates/counts in the manuscript text. The match table ships as data; the text never asserts
any named company violated a disclosure duty. Neutral phrasing only ("no related disclosure
located"). Materiality is a legal judgment the paper explicitly does not make.

## 9. What is NOT pre-committed (exploratory, labeled as such if reported)
Sector taxonomy beyond AIID/CSET fields; any post-hoc company-level narrative beyond the documented
Cruise/Zillow/marquee cases; any modeling beyond the descriptive endpoints above.
