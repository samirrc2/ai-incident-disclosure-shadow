# Reliability — independent double-coding (Amendment 3)

**Design.** Pass 1 coded all 307 incidents from the search records (company-batched). Pass 2 was an
**independent** re-code of a stratified reliability subsample **from the raw filings directly**, with
no access to pass-1 evidence summaries or verdicts. The subsample (n = **68**) over-samples the rare
tiers to make the coefficient informative: **all 28 non-T3 incidents** (every T1/T2/T4) plus a
**seed-42 random 40 of the 279 T3** incidents.

**Result.**
- Observed agreement: **58/68 = 85.3%**
- Expected agreement (chance): 46.3%
- **Cohen's κ = 0.726** → **PASS** the pre-registered ≥ 0.70 gate; coding proceeds.

**Confusion matrix (pass-1 rows × pass-2 columns):**

| | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| **T1** | 3 | 0 | 1 | 0 |
| **T2** | 1 | 0 | 1 | 1 |
| **T3** | 0 | 1 | 37 | 2 |
| **T4** | 0 | 0 | 3 | 18 |

**Headline stability.** Applying the resolved codes (below) to the full sample leaves the primary
result **unchanged**: shadow (T3+T4) = **97.7%** under both pass-1 and resolved coding; substantive
disclosure (T1+T2) = **7** under both. Six of ten disagreements are T3↔T4 (both inside the shadow),
so they cannot move the headline shadow rate; the remaining four reshuffle within the small
substantive set without changing its size.

## Disagreement log (all 10, with written resolution)

| id | pass 1 | pass 2 | resolved | rationale |
|---|---|---|---|---|
| 1376 | T4 | T3 | **T4** | Amazon's in-window AI-harm risk language does not clearly cover a GPS/navigation logistics failure (weak same-family fit). No headline effect. |
| 1401 | T4 | T3 | **T4** | WA-DOL-deployed AI phone system; Amazon's nexus is AWS-vendor only. No headline effect. |
| 386 | T3 | T4 | **T4** | Adopt pass-2: Amazon FY2019 10-K carries no worker-monitoring/algorithm risk factor ("AI" only in business text). No headline effect. |
| 83 | T4 | T3 | **T4** | Defer to pass-1's multi-year Microsoft baseline: AI-harm risk factor debuts FY2023; the FY2021 "AI" mention is business/competitive. No headline effect. |
| 881 | T3 | T4 | **T3** | CIK error surfaced by pass-2 (1826681≠Serve); corrected to 1832483 — Serve's FY2024 10-K does carry AI/autonomy risk language → T3. |
| 997 | T1 | T3 | **T1** | Keep pass-1: "Kadrey" returns 13 hits across Meta filings; the specific AI-training-copyright matter (LibGen/Llama) is named. |
| 534 | T2 | T3 | **T2** | Keep pass-1: FY2021 10-K Contingencies note discloses the securities class actions from the algorithm/metrics allegations, framed as securities law without AI-incident framing. |
| 646 | T3 | T2 | **T2** | Adopt pass-2: Snap discloses product-liability litigation involving minors (+ My AI FTC→DOJ referral) in generic product-liability terms without recommendation-algorithm framing. |
| 711 | T2 | T1 | **T2** | Keep pass-1: Tesla discloses NHTSA Autopilot investigations generally (regulatory-risk framing), not this specific April-2024 probe as a narrated event; T1 reserved for uniquely-named events (e.g., Cruise). |
| 733 | T2 | T4 | **T4** | Adopt pass-2: the OnStar FTC consent order/privacy suits are disclosed only in a Q1-2025 filing, **outside** the incident's 12-month window → nothing in-window. A window-sensitivity example. |

**Note.** Primary analysis reports pass-1 codes for all 307 (a single consistent coding pass), with
this κ and the resolution set as the reliability evidence; the resolved subsample is available for the
coder-1-vs-resolved robustness check and does not alter the headline.
