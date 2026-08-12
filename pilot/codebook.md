# Codebook — severity tiers, disclosure codes, EDGAR search protocol

## Severity rubric (3-tier, transparent; applied from AIID harm evidence)
- **T3-severe** — death, serious physical injury, or large-scale deprivation of a legal right /
  essential service / financial harm (safety-critical failure, wrongful benefit denial at scale,
  wrongful arrest).
- **T2-moderate** — material individual harm short of death/serious injury, or documented
  discrimination / privacy violation affecting an identifiable group.
- **T1-limited** — reputational, service-quality, or contained harm; no documented physical or
  large-scale rights/financial harm.
Native CSET severity is recorded alongside where present; the tier is the coding unit.

## Disclosure codes (per incident, over the incident_date → +12-month window, forms 8-K/10-K/10-Q)
- **DISCLOSED-SPECIFIC** — a window filing contains language a reasonable investor would connect
  to THIS incident: it names the event / investigation / lawsuit / settlement / recall, or
  describes the same facts. Requires a filing citation + quote.
- **DISCLOSED-GENERIC** — no specific reference, but the company's in-window filings contain
  risk-factor / MD&A language about the **same technology or harm family** as the incident (e.g.,
  Autopilot safety risk language for an Autopilot incident; generative-AI accuracy/reputation risk
  factors for that firm's genAI-product incident; ad-discrimination risk language for an
  ad-discrimination incident). Coded conservatively; uncertainty flagged.
- **NO-DISCLOSURE-LOCATED** — neither. Distinctive incident terms absent AND no topically-matched
  risk language. Hits that are subsidiary lists, compensation-plan exhibits, or routine
  product/segment names with no tie to the incident do **not** count as disclosure.

**Non-disclosure decision rules (applied consistently):**
- A product/segment/subsidiary name appearing routinely (e.g., "Cruise" as a unit, "Zillow Offers"
  as a segment, "naviHealth" in an Exhibit-21 subsidiary list) is NOT, by itself, disclosure of the
  incident.
- Compensation-plan exhibits and promotional earnings-release AI language are NOT risk disclosure.
- "Generic" requires the risk language to concern the **same** technology/harm implicated, not any
  AI mention anywhere.

## EDGAR search protocol (deterministic, reproducible)
Per incident: (1) run each incident-specific phrase and a generic AI-terms query, restricted to the
company CIK (10-digit padded), forms 8-K/10-K/10-Q, and the 12-month window; (2) for specific-term
hits, open the 1–2 most relevant filings and verify whether the incident is actually referenced;
(3) assign a code. Every query is logged as a full `efts.sec.gov` URL in
`edgar_query_manifest.csv`, so results are reproducible. Generic AI terms:
"artificial intelligence", "machine learning", "algorithm", "automated decision", "AI system",
"model risk".

## Two-pass coding
Pass 1 (coder A) and Pass 2 (coder B, independent) each assign codes; agreement recorded and
disagreements resolved with written rationale. **Limitation (stated honestly):** in this pilot both
passes coded from a shared, pre-summarized evidence table (hit counts + filing-read notes), so the
100% agreement reflects consistency of *codebook application*, not fully independent re-reading of
raw filings. The full build should run Pass 2 as an independent re-read of the underlying filings.
