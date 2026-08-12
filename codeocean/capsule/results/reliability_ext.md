# Extended Reliability (revision)

n (double-coded subsample) = 68. **Cohen's κ = 0.726** (PASS).
Observed agreement = 85.3%; **PABAK = 0.706**; **Gwet's AC1 = 0.821** (prevalence-robust, higher than κ because T3 dominates).
IPW-projected agreement to the full 307 = **90.9%** (weighting T3 by 278/40).

## Per-tier one-vs-rest agreement
| tier | n (pass1) | % agree | κ |
|---|---|---|---|
| T1 | 4 | 97% | 0.734 |
| T2 | 3 | 94% | -0.023 |
| T3 | 40 | 88% | 0.755 |
| T4 | 21 | 91% | 0.793 |

## Confusion matrix (pass-1 rows × pass-2 cols)
| | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| **T1** | 3 | 0 | 1 | 0 |
| **T2** | 1 | 0 | 1 | 1 |
| **T3** | 0 | 1 | 37 | 2 |
| **T4** | 0 | 0 | 3 | 18 |

_High T3 prevalence deflates chance-corrected kappa; prevalence-robust PABAK and Gwet's AC1 are reported alongside. Per-tier one-vs-rest kappa localizes reliability: the T1/T4 tiers are cleanly separated; residual uncertainty concentrates at the T2/T3 boundary._

_Severity: CSET authoritative for 40/307 incidents; the remaining 267 rubric-coded. Rubric-vs-CSET cross-check not a kappa (CSET takes precedence by design); severity strata read as indicative._
