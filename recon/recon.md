# recon — Data Reconnaissance

**PILOT — "The AI Incident Disclosure Shadow"**
Prepared: 2026-08-03 · Analyst: Claude (Cowork) for Samir · Spend to date: **$0.00** (cap $15)

> Scope of this document: confirm data access, field quality, and API coverage for every
> source the pilot needs, and record the one binding infrastructure constraint discovered
> during recon. Numbers reported in the pilot itself are script-generated; this file
> documents *sources and methods*, not findings.

---

## 0. Executive summary of access

| Source | Purpose | Access confirmed? | Reachable from this cloud container? | Route used |
|---|---|---|---|---|
| **AI Incident Database (AIID)** | Primary incident corpus + entity tags | **Yes** — public weekly snapshot | **No** (egress-blocked; see §5) | Snapshot fetch must run on a networked host / user device |
| **AIAAIC** | Supplementary incidents | Yes — public Google Sheet | Sheet export blocked by egress | CSV export on networked host |
| **OECD AIM** | Supplementary (corroboration only) | Yes — web UI + filtered export | Web UI only, weak entities | Not used for primary entity resolution |
| **EDGAR full-text search (efts.sec.gov)** | Disclosure detection | **Yes** | **Yes, via WebFetch** (verified live) | `efts.sec.gov/LATEST/search-index` through WebFetch |
| **SEC company_tickers.json** | ticker/name → CIK | Yes | Blocked to curl; fetch on networked host or per-name via WebFetch | — |
| **Debevoise Item 1.05 tracker** | Cyber disclosure baseline | **Yes** | Yes, via WebFetch/search | Blog + secondary summaries |

**Binding constraint (documented, not a blocker to the pilot):** the cloud sandbox running
this session has **allowlisted network egress** — only package registries (PyPI, npm) and
GitHub git/raw are reachable by `curl`/`requests`. Direct requests to `sec.gov`,
`incidentdatabase.ai`, Cloudflare R2 (`*.r2.dev`), HuggingFace, and Kaggle return connection
failures or HTTP 403 at the proxy. **Two channels remain open and are sufficient for the
pilot:** (a) **WebFetch**, which *does* reach `efts.sec.gov` and returns parsed EDGAR
full-text JSON (verified with a live Apple 8-K query), and (b) **GitHub raw**. The one thing
neither channel can do is pull the 105 MB AIID binary snapshot. That fetch is a one-line
`curl` on any un-firewalled host (the user's Mac, or a re-run "on your computer"), after
which the rest of the pipeline is fully local and reproducible. See §5 for the exact
commands and the fallback used in this pilot.

---

## 1. AI Incident Database (AIID) — primary source

**What it is.** The Responsible AI Collaborative's catalog of AI harms. Each *incident* groups
one or more *reports* (news articles / primary sources) and carries structured **entity tags**.

**Bulk export — CONFIRMED.** AIID publishes **weekly point-in-time full-database snapshots** at
<https://incidentdatabase.ai/research/snapshots/>. Latest snapshots (host
`pub-72b2b2fc36ec423189843747af98f80e.r2.dev`, Cloudflare R2):

| Date | File | Size |
|---|---|---|
| 2026-07-27 | `backup-20260727110451.tar.bz2` | 105.00 MB |
| 2026-07-20 | `backup-20260720110313.tar.bz2` | 103.98 MB |
| 2026-07-13 | `backup-20260713110347.tar.bz2` | 102.01 MB |
| … weekly back to 2021 | | |

Each archive contains the **full database in JSON, MongoDB-archive, and CSV** form. The pilot
pins the **2026-07-27** snapshot as the canonical version (SHA-256 recorded in the raw manifest
once fetched).

**Collections of interest.** `incidents` (incident_id, title, date, description, Alleged
deployer/developer/harmed-parties entity references), `reports` (per-incident source articles
with URLs and dates), `entities` (canonical entity records), and CSET/taxonomy classifications
(harm type, severity where coded).

**Entity-field quality.** AIID's `Alleged deployer of AI system` / `Alleged developer of AI
system` / `Alleged harmed or nearly harmed parties` are **structured references to an `entities`
collection** — materially better than free text, but the entity records are *organizations as
named in reporting* (e.g., "Tesla", "Google"), **not** normalized to ticker/CIK/LEI and not
resolved parent↔subsidiary. That gap is exactly the entity-resolution step in Phase 1.

**Severity / harm taxonomy.** AIID does not carry a single universal numeric severity. Harm
signal is available three ways: (a) the **CSET AI Harm Taxonomy** classifications attached to a
subset of incidents (harm type, tangible/intangible, severity where coded); (b) the **GMF/MIT**
taxonomies; (c) derivable proxies (physical-harm/fatality keywords, scale of affected parties).
The pilot defines a **transparent 3-tier severity rubric** (codebook §CODEBOOK) rather than
relying on incomplete native severity fields, and records native CSET severity alongside where
present.

**Corpus size.** AIID is on the order of **~3,000+ numbered incidents** (growing weekly; exact
count is script-generated from the pinned snapshot). This scale is the basis for expecting the
US-listed matchable subset to be in the several-hundreds (see Phase 1).

## 2. AIAAIC — supplementary

Public **Google Sheet** (CC BY-SA 4.0), ~1,000+ incidents/controversies. Distinct, discrete
**Deployer(s)** and **Developer(s)** columns (free text, un-normalized), plus **Occurred** and
**Released** dates and an **Issue(s)** harm-type field. Usable as a supplement and cross-check;
requires the same name→ticker resolution + manual review as AIID. **Verdict:** the better of the
two supplements; fold in during the full build for incidents AIID misses, not required for the
pilot.

## 3. OECD AI Incidents Monitor (AIM) — supplementary, corroboration only

Web UI at <https://oecd.ai/en/incidents> with a filtered "Download results" export; **no public
bulk API**. ~16,000+ auto-ingested incidents+hazards (Event Registry + GPT-4o classification).
Strong on harm/severity/country/sector, **weak on a structured involved-company field** (the firm
lives in LLM-generated free-text summaries, heavily duplicated). **Verdict:** treat as a
volume/coverage cross-check, **not** a primary entity-resolution source.

## 4. EDGAR full-text search — disclosure detection

**Endpoint (CONFIRMED live via WebFetch):** `https://efts.sec.gov/LATEST/search-index`
Elasticsearch-style JSON: `hits.total.value`, `hits.hits[]._source.{form,file_date,ciks,display_names}`,
`_id = <accession>:<file>`.

**Parameters used:** `q` (URL-encoded phrase / boolean), `forms=8-K,10-K,10-Q`,
`ciks=<10-digit zero-padded>`, `dateRange=custom&startdt=YYYY-MM-DD&enddt=YYYY-MM-DD`,
`from=` (page size 100; hard window `from`+size ≤ 10,000). **Gotcha:** `startdt/enddt` are only
honored when `dateRange=custom` is present; `ciks` must be zero-padded to 10 digits.

**Date coverage — CONFIRMED adequate.** Full-text search covers electronic filings **2001 →
present, continuously**. The incident window (2019–2026) and the +12-month disclosure horizon are
**fully inside coverage**. (Pre-2001 is out of scope but irrelevant here.)

**Fair-access etiquette (implemented in the pipeline):** declared `User-Agent` with contact
email; throttle ≤ 8 req/s; `Accept-Encoding: gzip`; exponential backoff on 429/403.

**CIK mapping.** `https://www.sec.gov/files/company_tickers.json` (object keyed by index → `{cik_str,
ticker, title}`; pad `cik_str` to 10 digits). In this container the file is fetched per-company via
WebFetch / cached crosswalk; on a networked host the pipeline pulls the whole file once.

**Live verification.** A test query — Apple (CIK 0000320193), `forms=8-K`, `q="data breach"`,
2023–2024 — returned a well-formed `hits.total.value` (0), confirming the endpoint, parameter
semantics, and WebFetch round-trip all work.

## 5. Infrastructure constraint & the AIID-ingestion workaround

**Observed.** `curl`/`requests` from the container: PyPI → 200; GitHub raw → 200; `sec.gov` →
403 at proxy; `*.r2.dev`, `huggingface.co`, `kaggle.com` → connection failure. WebFetch reaches
`efts.sec.gov` and `incidentdatabase.ai` (HTML pages) but cannot POST (AIID GraphQL needs POST →
400) and cannot stream a 105 MB binary.

**Consequence.** EDGAR disclosure detection runs here (via WebFetch). The **AIID snapshot binary
must be fetched on a networked host.** Two supported ways, both leaving a reproducible artifact:

```bash
# Option A — on the user's Mac (or any un-firewalled machine):
curl -L -o "NIW/Paper 13/data/raw/backup-20260727110451.tar.bz2" \
  https://pub-72b2b2fc36ec423189843747af98f80e.r2.dev/backup-20260727110451.tar.bz2
#   then re-invoke: scripts/parse_aiid.py ingests it, seed=42, SHA-256 logged.

# Option B — re-run this Cowork task "On your computer" (desktop app picker),
#   where the same scripts run with normal network egress.
```

**Pilot fallback used in this session (fully rigorous, just not snapshot-enumerated).** Because
the exact snapshot could not be ingested here, Phase 1's *complete* N_matchable is reported as a
**verified lower bound + reasoned estimate**, and Phase 2's 30-incident shadow measurement is run
on a **source-verified incident set** — every incident cross-checked to its AIID record and its
EDGAR filings via the live routes above, every number reproducible from logged deterministic
`efts` URLs. The full snapshot run (Option A/B) formalizes N_matchable and extends the map; it
does not change the pilot's feasibility verdict.

## 6. Cyber disclosure baseline (Debevoise Item 1.05 tracker)

**Regime.** Since **2023-12-18**, SEC Item 1.05 of Form 8-K requires disclosure of a **material**
cybersecurity incident within 4 business days of a materiality determination; Item 8.01 is used for
voluntary/non-material cyber disclosures.

**Baseline series (Debevoise Data Blog, "Two-Year Update", 2026-05-21):**
- **Item 1.05 (material) filings: 29 issuers**
- **Item 8.01 (voluntary) filings: 50 issuers**
- Filed under both: 5 · **Total 79 filings across 74 issuers**
- One-year mark (Feb 2025): 26 material / 34 voluntary → only ~3 additional *material* filings in
  year two; the May-2024 SEC (Gerding) statement pushed non-material events decisively to 8.01.
- Independent counts vary by classification rules (e.g., Cherry Hill 2026: 47 "mandatory" / 31
  voluntary) — cite Debevoise 29/50 as the tracker baseline, note the counting-rule sensitivity.

**Definitional caveat (must appear in the paper).** The tracker counts **disclosures filed under a
mandate**, not incidents that occurred. It is therefore a **disclosure-under-mandate** series, and
the paper's contrast is explicitly **"AI disclosure-per-known-incident (voluntary regime)" vs
"cyber disclosure-under-mandate"** — *not* two shadow rates. The cyber *shadow* (material cyber
incidents that occurred but were never disclosed) is not observable from the tracker; we do not
claim it. This asymmetry is a feature of the comparison and is stated as such.

---

## 7. Recon verdict

All four required capabilities are **confirmed available**: AIID bulk export (weekly snapshot),
entity resolution path (structured entity refs → manual+LLM-assisted crosswalk → CIK, with a
human-review sheet), EDGAR full-text search per CIK/form/window (live via WebFetch, coverage
adequate), and a usable cyber baseline (Debevoise 29 material / 50 voluntary). The sole
qualification is the container egress limit on the AIID binary, with a documented one-command
workaround. **Recon does not block the pilot.**

### Sources
- AIID snapshots — <https://incidentdatabase.ai/research/snapshots/>
- AIID repo (fields, taxonomies) — <https://github.com/responsible-ai-collaborative/aiid>
- EDGAR FTS FAQ — <https://www.sec.gov/edgar/search/efts-faq.html> · UA/rate rules — <https://www.sec.gov/about/webmaster-frequently-asked-questions>
- SEC CIK map — <https://www.sec.gov/files/company_tickers.json>
- AIAAIC — <https://www.aiaaic.org/aiaaic-repository> · OECD AIM — <https://oecd.ai/en/incidents>
- Debevoise two-year 8-K tracker — <https://www.debevoisedatablog.com/2026/05/21/cybersecurity-incident-disclosure-form-8-k-tracker-two-year-update/> · one-year PDF — <https://www.debevoise.com/-/media/files/insights/publications/2025/02/lessons-learned-one-year-of-form-8k-material.pdf>
- SEC rulemaking petition File No. 4-882 (policy hook) — <https://www.sec.gov/rules/petitions.htm>
