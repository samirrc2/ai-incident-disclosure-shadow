# Extended Related Work — Verified References

Compiled 2026-08-03. Every item below was checked against a primary source (publisher page, DOI, arXiv, official reporter, or author CV) during this pass. Verification notes and any residual uncertainty are flagged in **[VERIFY]** tags. Nothing here is fabricated; items that could not be verified were dropped and are listed at the end.

Our study ("the paper") = matching AI Incident Database incidents to U.S.-listed companies' SEC filings and measuring disclosure rates via a 4-tier taxonomy (97.7% "shadow"/undisclosed).

---

## Stream 1 — Securities disclosure & materiality (legal + empirical)

1. **TSC Industries, Inc. v. Northway, Inc.**, 426 U.S. 438 (1976). U.S. Supreme Court. URL: https://supreme.justia.com/cases/federal/us/426/438
   - *Delta:* Supplies the "substantial likelihood a reasonable investor would consider it important" materiality test that our paper operationalizes empirically for AI incidents rather than argues doctrinally.

2. **Basic Inc. v. Levinson**, 485 U.S. 224 (1988). U.S. Supreme Court. URL: https://supreme.justia.com/cases/federal/us/485/224
   - *Delta:* Extends materiality to contingent/probabilistic events via probability-×-magnitude; we treat individual AI incidents as exactly such contingent events and measure whether firms actually disclosed them.

3. **Christensen, H. B., Hail, L., & Leuz, C. (2016).** Capital-Market Effects of Securities Regulation: Prior Conditions, Implementation, and Enforcement. *Review of Financial Studies*, 29(11), 2885–2924. DOI: 10.1093/rfs/hhw055
   - *Delta:* Shows disclosure mandates bind only where enforcement does; we provide micro-evidence of near-zero de facto enforcement/compliance for a harm class (AI incidents) with no dedicated mandate.

4. **Leuz, C., & Wysocki, P. D. (2016).** The Economics of Disclosure and Financial Reporting Regulation: Evidence and Suggestions for Future Research. *Journal of Accounting Research*, 54(2), 525–622. DOI: 10.1111/1475-679X.12115
   - *Delta:* Canonical survey framing the costs/benefits of mandated disclosure; our incident-to-filing gap is a concrete, quantified instance of the "real-effects vs. disclosure" wedge they call for evidence on.

5. **Christensen, H. B., Hail, L., & Leuz, C. (2013).** Mandatory IFRS Reporting and Changes in Enforcement. *Journal of Accounting and Economics*, 56(2–3, Supplement 1), 147–177. DOI: 10.1016/j.jacceco.2013.10.007
   - *Delta:* Disentangles regulation from enforcement empirically; complements our finding that absent a targeted enforcement regime, AI-harm information stays out of filings. **[VERIFY]** Existence and JAE 2013 venue confirmed via SSRN/ECGI/NBER working-paper record; confirm exact issue/pages against the published JAE PDF before final submission.

---

## Stream 2 — Risk-factor / 10-K textual disclosure & boilerplate informativeness

6. **Campbell, J. L., Chen, H., Dhaliwal, D. S., Lu, H., & Steele, L. B. (2014).** The Information Content of Mandatory Risk Factor Disclosures in Corporate Filings. *Review of Accounting Studies*, 19(1), 396–455. DOI: 10.1007/s11142-013-9258-3
   - *Delta:* Finds Item 1A risk factors are informative in aggregate; we show that for a specific, verifiable harm (a realized AI incident) the corresponding risk-factor/event disclosure is almost always absent.

7. **Kravet, T., & Muslu, V. (2013).** Textual Risk Disclosures and Investors' Risk Perceptions. *Review of Accounting Studies*, 18(4), 1088–1122. DOI: 10.1007/s11142-013-9228-9
   - *Delta:* Links risk-disclosure text to investor risk perception; our ground-truth incident dataset lets us ask whether the underlying events even enter that text in the first place.

8. **Hope, O.-K., Hu, D., & Lu, H. (2016).** The Benefits of Specific Risk-Factor Disclosures. *Review of Accounting Studies*, 21(4), 1005–1045. DOI: 10.1007/s11142-016-9371-1
   - *Delta:* Shows specificity of risk factors is value-relevant; we document the opposite margin — that concrete AI incidents are rarely converted into any specific disclosure.

9. **Loughran, T., & McDonald, B. (2011).** When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. *The Journal of Finance*, 66(1), 35–65. DOI: 10.1111/j.1540-6261.2010.01625.x
   - *Delta:* Foundational finance-domain textual-analysis methodology; we build on this NLP-of-filings tradition but anchor text to an external incident ground truth rather than dictionary sentiment.

10. **Cazier, R. A., & Pfeiffer, R. J.** 10-K Disclosure Repetition and Managerial Reporting Incentives. SSRN Working Paper No. 2487259. URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2487259
   - *Delta:* Evidence that 10-K text is padded/repeated for incentive reasons, motivating why boilerplate can crowd out event-specific AI disclosure. **[VERIFY]** Confirmed as a real, citable Cazier & Pfeiffer working paper; the final published venue/year was not confirmed in this pass — cite as SSRN working paper or locate the journal version before submission.

---

## Stream 3 — Voluntary-disclosure / disclosure theory

11. **Verrecchia, R. E. (2001).** Essays on Disclosure. *Journal of Accounting and Economics*, 32(1–3), 97–180. DOI: 10.1016/S0165-4101(01)00025-8
   - *Delta:* Provides the discretionary/proprietary-cost disclosure framework; we supply field evidence on where discretionary non-disclosure dominates for a novel harm class.

12. **Healy, P. M., & Palepu, K. G. (2001).** Information Asymmetry, Corporate Disclosure, and the Capital Markets: A Review of the Empirical Disclosure Literature. *Journal of Accounting and Economics*, 31(1–3), 405–440. DOI: 10.1016/S0165-4101(01)00018-0
   - *Delta:* Sets the empirical agenda for disclosure research; our incident-to-filing matching adds a new observable "withholding" measure to that agenda.

13. **Dye, R. A. (1985).** Disclosure of Nonproprietary Information. *Journal of Accounting Research*, 23(1), 123–145. DOI: 10.2307/2490910
   - *Delta:* Formalizes rational non-disclosure when investors are uncertain whether managers are informed; AI incidents (managers plausibly uninformed/deniable) are a clean setting for Dye-type withholding.

14. **Grossman, S. J. (1981).** The Informational Role of Warranties and Private Disclosure about Product Quality. *Journal of Law and Economics*, 24(3), 461–483. DOI: 10.1086/466995
   - *Delta:* Origin of the unraveling result predicting full disclosure; our 97.7% shadow rate is direct evidence of where unraveling empirically fails.

15. **Milgrom, P. R. (1981).** Good News and Bad News: Representation Theorems and Applications. *The Bell Journal of Economics*, 12(2), 380–391. DOI: 10.2307/3003562
   - *Delta:* The complementary unraveling/persuasion result; our data quantify the wedge between its full-disclosure prediction and observed AI-incident silence.

---

## Stream 4 — Safety / incident & near-miss reporting (non-AI precedent)

16. **Reynard, W. D. (1984).** The Aviation Safety Reporting System. In *Flight Training Technology for Regional/Commuter Airline Operations* (NASA Ames Research Center). NASA Technical Reports Server, accession 19850009712. URL: https://ntrs.nasa.gov/citations/19850009712
   - *Delta:* Documents ASRS's confidential, non-punitive reporting design that drove high reporting rates; our paper is the mirror image — a domain (AI) with no such channel and correspondingly near-zero disclosure. **[VERIFY]** This 1984 primary-source conference paper is verified; if a broader citation is wanted, the frequently cited NASA Reference Publication 1114 (1986) form was *not* independently confirmed this pass — do not cite RP-1114 without checking.

17. **Barach, P., & Small, S. D. (2000).** Reporting and Preventing Medical Mishaps: Lessons from Non-Medical Near Miss Reporting Systems. *BMJ*, 320(7237), 759–763. DOI: 10.1136/bmj.320.7237.759
   - *Delta:* Argues near-miss reporting requires confidentiality and non-punishment to surface events; frames AI incidents as an under-built near-miss regime, which our disclosure gap empirically confirms.

18. **Vincent, C., Stanhope, N., & Crowley-Murphy, M. (1999).** Reasons for Not Reporting Adverse Incidents: An Empirical Study. *Journal of Evaluation in Clinical Practice*, 5(1), 13–21. DOI: 10.1046/j.1365-2753.1999.00147.x
   - *Delta:* Identifies fear/blame and low perceived value as under-reporting drivers; we show an analogous under-reporting equilibrium in corporate AI disclosure, where incentives, not ignorance, likely dominate.

19. **Classen, D. C., Resar, R., Griffin, F., Federico, F., Frankel, T., Kimmel, N., Whittington, J. C., Frankel, A., Seger, A., & James, B. C. (2011).** 'Global Trigger Tool' Shows That Adverse Events in Hospitals May Be Ten Times Greater Than Previously Measured. *Health Affairs*, 30(4), 581–589. DOI: 10.1377/hlthaff.2011.0190
   - *Delta:* Quantifies a ~10× gap between voluntarily reported and actual adverse events; our 97.7% shadow rate is the analogous "measured vs. disclosed" gap for AI harms.

---

## Stream 5 — AI harms / incident taxonomies / audits

20. **Weidinger, L., Mellor, J., Rauh, M., Griffin, C., Uesato, J., Huang, P.-S., ... Gabriel, I. (2021).** Ethical and Social Risks of Harm from Language Models. arXiv:2112.04359. URL: https://arxiv.org/abs/2112.04359
   - *Delta:* Provides a canonical risk taxonomy for LMs; we map *realized* incidents (not prospective risks) onto firms and disclosures.

21. **Weidinger, L., Uesato, J., Rauh, M., Griffin, C., Huang, P.-S., Mellor, J., ... Gabriel, I. (2022).** Taxonomy of Risks Posed by Language Models. In *Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency (FAccT '22)*, 214–229. DOI: 10.1145/3531146.3533088
   - *Delta:* The peer-reviewed taxonomy version; our taxonomy is disclosure-tier-based (shadow→full) rather than harm-type-based, and is applied to filings.

22. **Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J., Theron, D., & Barnes, P. (2020).** Closing the AI Accountability Gap: Defining an End-to-End Framework for Internal Algorithmic Auditing. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (FAT* '20)*, 33–44. DOI: 10.1145/3351095.3372873
   - *Delta:* Proposes internal audit machinery for accountability; we measure the *external* accountability output (investor disclosure) and find it largely missing.

23. **McGregor, S. (2021).** Preventing Repeated Real World AI Failures by Cataloging Incidents: The AI Incident Database. *Proceedings of the AAAI Conference on Artificial Intelligence*, 35(17), 15458–15463. DOI: 10.1609/aaai.v35i17.17817
   - *Delta:* The AIID data source we build on; we extend it by linking incidents to specific public issuers and their SEC filings.

24. **OECD (2024).** Defining AI Incidents and Related Terms. *OECD Artificial Intelligence Papers*, No. 16. OECD Publishing, Paris. DOI: 10.1787/d1a8d965-en. URL: https://www.oecd.org/en/publications/defining-ai-incidents-and-related-terms_d1a8d965-en.html
   - *Delta:* Supplies standardized incident definitions; we adopt incident-level granularity but pivot to whether incidents reach investors.

25. **Dixon, R. B. L., & Frase, H. (2025).** AI Incidents: Key Components for a Mandatory Reporting Regime. Center for Security and Emerging Technology (CSET), Georgetown University. URL: https://cset.georgetown.edu/publication/ai-incidents-key-components-for-a-mandatory-reporting-regime/
   - *Delta:* Argues (normatively) for a mandatory AI-incident reporting regime; our study is the empirical baseline showing why one is needed — voluntary channels leave 97.7% of matched incidents undisclosed.

---

## Stream 6 — Cybersecurity-disclosure empirics (closest disclosure-regime precedent)

26. **Amir, E., Levi, S., & Livne, T. (2018).** Do Firms Underreport Information on Cyber-Attacks? Evidence from Capital Markets. *Review of Accounting Studies*, 23(3), 1177–1206. DOI: 10.1007/s11142-018-9452-4
   - *Delta:* The methodological template — firms withhold severe cyber incidents; we transpose the "external ground truth vs. filing" design from cyber to AI incidents.

27. **Gordon, L. A., Loeb, M. P., & Sohail, T. (2010).** Market Value of Voluntary Disclosures Concerning Information Security. *MIS Quarterly*, 34(3), 567–594. URL: https://aisel.aisnet.org/misq/vol34/iss3/11/
   - *Delta:* Shows markets price voluntary infosec disclosures, implying incentives to disclose; our AI setting shows those incentives rarely produce incident disclosure.

28. **Gordon, L. A., Loeb, M. P., Lucyshyn, W., & Sohail, T. (2006).** The Impact of the Sarbanes-Oxley Act on the Corporate Disclosures of Information Security Activities. *Journal of Accounting and Public Policy*, 25(5), 503–530. DOI: 10.1016/j.jaccpubpol.2006.07.005
   - *Delta:* Documents how a disclosure-regime shock changed infosec disclosure; frames AI as a domain still awaiting such a regime shock.

29. **Ashraf, M., Jiang, J. (X.), & Wang, I. Y. (2022).** Are There Trade-Offs with Mandating Timely Disclosure of Cybersecurity Incidents? Evidence from State-Level Data Breach Disclosure Laws. *The Journal of Finance and Data Science*, 8, 253–275. DOI: 10.1016/j.jfds.2022.09.002. URL: https://www.sciencedirect.com/science/article/pii/S2405918822000101
   - *Delta:* Analyzes costs/benefits of *mandated* timely breach disclosure; our evidence characterizes the pre-mandate state for AI incidents (predominantly no disclosure). **[VERIFY]** Article/journal/2022 confirmed; confirm exact page range (8, 253–275) against the publisher PDF.

30. **Ashraf, M., & Sunder, J. (2023).** Can Shareholders Benefit from Consumer Protection Disclosure Mandates? Evidence from Data Breach Disclosure Laws. *The Accounting Review*, 98(4), 1–27. 
   - *Delta:* Shows shareholder effects of breach-disclosure mandates; supports our argument that AI-incident disclosure mandates would have measurable investor relevance. **[VERIFY]** Confirmed from the author's CV (The Accounting Review, July 2023); confirm exact volume/issue/page range and DOI against the published article.

---

## Stream 7 — AI in corporate / financial disclosure

31. **Strauss, I., O'Reilly, T., Rosenblat, S., & Moure, I. (2025).** Governing AI Through SEC Disclosure: Materiality Standards and Incident Reporting — Lessons from Cybersecurity. SSRC AI Disclosures Project, Working Paper No. 04, 2025/10. Social Science Research Council. DOI: 10.35650/AIDP.4120.d.2025
   - *Delta:* Argues (conceptually, drawing on cyber) for AI materiality/incident disclosure; we supply the matched-incident empirics quantifying the current disclosure shortfall. **[VERIFY / correction]** Author is **Isobel Moure** (not "Moore") and **Sruly Rosenblat**; adjust from the placeholder spellings in the brief.

32. **Uberti-Bona Marin, L. G., Rijsbosch, B., Spanakis, G., & Kollnig, K. (2025).** Are Companies Taking AI Risks Seriously? A Systematic Analysis of Companies' AI Risk Disclosures in SEC 10-K Forms. arXiv:2508.19313 (to appear, SoGood workshop, ECML PKDD 2025). URL: https://arxiv.org/abs/2508.19313
   - *Delta:* Analyzes *prospective* AI risk-factor language in 10-Ks; we complement it by matching *realized* incidents to filings, measuring omission rather than risk-factor content.

33. **Ante, L., & Saggu, A. (2025).** Quantifying a Firm's AI Engagement: Constructing Objective, Data-Driven, AI Stock Indices Using 10-K Filings. *Technological Forecasting and Social Change*. arXiv:2501.01763. URL: https://www.sciencedirect.com/science/article/pii/S0040162524007637
   - *Delta:* Uses 10-K AI language to measure firm AI *engagement/exposure*; we use filings to measure AI *incident disclosure*, a distinct (and largely empty) signal. **[VERIFY]** Journal (TFSC) and authorship confirmed via arXiv + ScienceDirect; confirm exact volume/article number/DOI at the publisher.

34. **Song, X., Hou, W., Ouyang, Z., & Hao, F. (2026).** AI Washing: Strategic Disclosure and Backlash. *Finance Research Letters*, 95, article 108xxx. URL: https://www.sciencedirect.com/science/article/pii/S1544612326002151
   - *Delta:* Studies *over*-claiming of AI in disclosures ("AI washing"); the flip side of our finding — firms amplify favorable AI narratives while omitting adverse AI incidents. **[VERIFY]** Journal (Finance Research Letters, vol. 95, 2026) and authors confirmed via publisher/RePEc; fill exact article number/DOI at the publisher.

---

## Items considered but NOT included (could not fully verify or out of scope)

- **NASA Reference Publication 1114 (Reynard, Billings, Cheaney & Hardy, 1986)** — frequently cited as the foundational ASRS report, but the exact RP-1114 bibliographic record was not independently confirmed this pass; replaced with the verified Reynard (1984) primary source (#16). Do not cite RP-1114 without checking NTRS.
- **Eisfeldt, Schubert, Zhang & Taska, "Generative AI and Firm Values" (NBER WP 31222, 2023)** — real and verified, but it measures AI *exposure via labor tasks*, not disclosure in filings; dropped as off-topic for the "AI-in-filings disclosure" stream (available if you want a firm-value/AI-exposure cite instead).

## Summary of flags requiring a final human check before submission
- #5 Christensen/Hail/Leuz (2013): confirm JAE issue/pages.
- #10 Cazier & Pfeiffer: confirm published venue vs. SSRN working paper.
- #16 Reynard (1984): verified; RP-1114 alternative NOT verified.
- #29 Ashraf/Jiang/Wang (2022): confirm page range & DOI.
- #30 Ashraf & Sunder (2023): confirm volume/issue/pages & DOI.
- #31 SSRC: fix author spellings (Moure, Rosenblat).
- #33 Ante & Saggu: confirm TFSC volume/DOI.
- #34 Song et al.: confirm FRL article number/DOI.
