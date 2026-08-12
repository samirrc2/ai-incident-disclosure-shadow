# Shadow Measurement Results

_n = 30 matched incidents (US-listed involved company), stratified across severity tiers and years
2019–2024. EDGAR full-text search of each company's 8-K/10-K/10-Q over incident_date → +12 months.
Two coding passes; inter-pass agreement 30/30 (100%; see codebook limitation). All counts
script-generated (`code_shadow.py`) from the coded table; every EDGAR query logged as a
deterministic URL in `edgar_query_manifest.csv`._

## Headline

| Measure | Count | Rate |
|---|---|---|
| **Incident-SPECIFIC disclosure** (a filing references the incident) | **2 / 30** | **7%** |
| Any related disclosure located (specific **or** generic risk language) | 18 / 30 | 60% |
| **No disclosure located** (the "shadow") | 12 / 30 | 40% |
| Incident-specific shadow (no *specific* disclosure) | 28 / 30 | **93%** |

Code distribution: DISCLOSED-SPECIFIC 2 · DISCLOSED-GENERIC 16 · NO-DISCLOSURE-LOCATED 12.

Both incident-specific disclosures — **GM/Cruise** (10-K discloses the October 2023 pedestrian
incident, the California DMV permit suspension, the voluntary operations pause, and the
NHTSA/DOJ/SEC investigations) and **Zillow** (8-K, Item 2.05, winds down Zillow Offers citing the
home-pricing-model failure) — are cases where the incident produced an unavoidable, large financial
or operational consequence (restructuring charges; exit of a business line). Where an AI incident
was reputational, regulatory, or litigation-driven but not itself a large accounting event, we
located **no filing that names it** — including a ~2-million-vehicle Autopilot recall (Tesla), a
$170M YouTube COPPA settlement (Alphabet), an FTC facial-recognition ban (Rite Aid), and several
algorithmic-bias lawsuits (UnitedHealth/naviHealth, Cigna, Workday, Wells Fargo).

## By severity tier

| Tier | n | disclosed (any) | of which SPECIFIC | no disclosure located | shadow rate |
|---|---|---|---|---|---|
| T3-severe | 7 | 4 (57%) | 2 | 3 | 43% |
| T2-moderate | 15 | 9 (60%) | 0 | 6 | 40% |
| T1-limited | 8 | 5 (62%) | 0 | 3 | 38% |

The gradient is flat: incident-**specific** disclosure does not rise with severity except where the
incident is also a material accounting/operational event. Generic AI risk-factor language is broadly
present across tiers (it tracks the firm's AI activity, not the specific incident).

## Cyber baseline (benchmark) — disclosure-under-mandate

Under the mandatory Item 1.05 regime (effective 2023-12-18), the Debevoise tracker counts, over two
years (as of 2026-05-21): **29 issuers** filing a *material* cybersecurity incident (Item 1.05) and
**50 issuers** filing *voluntary* cyber disclosures (Item 8.01) — 79 filings across 74 issuers.

**Definitional caveat (must appear in the manuscript).** These are not two comparable "shadow
rates." The cyber figure is **disclosure-under-mandate** — the count of incidents companies *chose to
file* under a legal duty; it does **not** measure the cyber shadow (material cyber incidents that
occurred but were never disclosed), which is unobservable from the tracker. The AI figure is
**disclosure-per-known-incident under no mandate**. The contrast the paper draws is therefore
regime-level: *AI incidents have no disclosure mandate and a ~7% incident-specific disclosure rate;
cyber incidents, under a mandate, produce a compelled disclosure stream.* Both definitions are stated
precisely; no claim is made that any specific firm failed a duty.

## Legal framing (binding)

All results are aggregate rates/counts. "No disclosure located" is a neutral, search-scoped finding
— **not** an assertion that any company failed to disclose, concealed, or violated any duty.
Materiality is a legal judgment this study does not make; the pilot measures disclosure **behavior**.

_Per-incident evidence and codes: `pilot_shadow_table.csv`; query URLs: `edgar_query_manifest.csv`._
