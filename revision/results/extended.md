# Extended Analysis (revision)

## Concentration
- Issuers: 21; HHI = **0.1813** (top-2 share 0.544, top-5 0.827).
- Top issuers: Alphabet Inc. 86, Meta Platforms, Inc. 81, Tesla, Inc. 36, Microsoft Corporation 35, Amazon.com, Inc. 16, General Motors Company 14, Apple Inc. 9

## Concentration robustness (shadow rate)
- Full: 97.7%
- Leave-one-issuer-out range: 96.8%–98.6%
- Drop top-2 (Alphabet+Meta): 96.4% (n=140)
- Drop top-5: 92.5% (n=53)

## Clustered inference
- Shadow, incident-level Wilson: 97.7% [95.4, 98.9]
- Shadow, issuer-clustered bootstrap: 97.5% [93.9, 99.6] (B=10k, seed 42)
- T1, issuer-clustered bootstrap: 1.4% [0.0, 4.0]
- Issuer-level mean shadow: 94.0%

## Formal tests (substantive T1+T2 across strata)
- Severity: chi2 p=0.5095, Cramér's V=0.066
- Role: chi2 p=0.0054, V=0.184
- Parent vs direct: fisher_exact p=0.2917, V=0.026
- Year trend (Cochran–Armitage): z=-0.282, p=0.7779
- _Only 7 substantive (T1+T2) positives -> tests are low-powered; non-significant results indicate 'no detectable difference', not evidence of equality._

## Issuer-level outcomes
- Issuers with ≥1 substantive disclosure: **4/21 (19%)**

| issuer | n | T1 | T2 | T3 | T4 | shadow |
|---|---|---|---|---|---|---|
| Alphabet Inc. | 86 | 0 | 0 | 86 | 0 | 100% |
| Meta Platforms, Inc. | 81 | 1 | 1 | 78 | 1 | 98% |
| Tesla, Inc. | 36 | 0 | 1 | 34 | 1 | 97% |
| Microsoft Corporation | 35 | 0 | 0 | 30 | 5 | 100% |
| Amazon.com, Inc. | 16 | 0 | 0 | 14 | 2 | 100% |
| General Motors Company | 14 | 2 | 1 | 10 | 1 | 79% |
| Apple Inc. | 9 | 0 | 0 | 5 | 4 | 100% |
| SoundThinking, Inc. | 4 | 0 | 0 | 4 | 0 | 100% |
| McDonald's Corporation | 4 | 0 | 0 | 3 | 1 | 100% |
| UnitedHealth Group Inc. | 3 | 0 | 0 | 1 | 2 | 100% |
| Uber Technologies, Inc. | 3 | 0 | 0 | 3 | 0 | 100% |
| Serve Robotics Inc. | 3 | 0 | 0 | 2 | 1 | 100% |

## By incident category
| category | n | T1 | T2 | T3 | T4 | substantive |
|---|---|---|---|---|---|---|
| misinformation_content | 70 | 0 | 0 | 70 | 0 | 0 |
| autonomous_vehicle | 66 | 2 | 1 | 63 | 0 | 3 |
| generative_error | 57 | 0 | 0 | 53 | 4 | 0 |
| other | 47 | 0 | 1 | 41 | 5 | 1 |
| safety_physical | 19 | 0 | 0 | 14 | 5 | 0 |
| discrimination_bias | 16 | 0 | 1 | 14 | 1 | 1 |
| privacy_surveillance | 11 | 0 | 0 | 10 | 1 | 0 |
| employment_hiring | 11 | 1 | 0 | 7 | 3 | 1 |
| copyright_ip | 10 | 1 | 0 | 6 | 3 | 1 |

## Retrieval validation (false negatives)
- Audited 40 incidents (20 T3 + 20 T4); **0 missed disclosures found**; upper 95% bound ≈ 0.075.

## Window robustness (shadow rate)
- 6mo 99.0% · 12mo 97.7% · 18mo 97.7% · 24mo 97.7%
- _Substantive disclosures fall in the fiscal-year 10-K ~9-11 months post-incident; robust to lengthening (12=18=24), only shortening to 6mo drops 4 of 7 into T3._
