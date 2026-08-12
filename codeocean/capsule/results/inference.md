# Exact inference & reviewer-proofing robustness

## Clopper-Pearson exact 95% intervals (headline)
- T1 incident-specific: 1.3% [0.4, 3.3]
- T1+T2 substantive: 2.3% [0.9, 4.6]
- Shadow T3+T4: 97.7% [95.4, 99.1]

## Monte-Carlo exact permutation tests (substantive T1+T2)
- By role: chi2=10.434, p(MC-exact)=0.0234
- By severity: chi2=1.349, p(MC-exact)=0.6056

## Match-yield funnel (1,389 window incidents)
| class | n |
|---|---|
| named non-crosswalk entity | 400 |
| generic/individual/non-corporate only | 398 |
| US-listed (primary) | 307 |
| private firm | 243 |
| foreign US-listed / foreign-private | 26 |
| delisted-was-listed | 15 |

_Primary US-listed yield = 22.1% (307/1389); non-matches are dominated by private AI labs and generic/individual actors._

## Right-censoring robustness
- Complete-window incidents: 252 (shadow 97.2% [94.4,98.9]); 55 right-censored.

## Plausibly-material subset
- Severe tier (n=42): shadow 95.2%, 2 substantive.
- Top-5 issuers (n=254): shadow 98.8%.
