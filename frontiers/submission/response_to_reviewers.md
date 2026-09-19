# Response to Reviewer — "The AI Incident Disclosure Shadow"
*Frontiers in Artificial Intelligence (AI in Finance) · major revision · response to Reviewer 1*

We thank the reviewer for a close and useful report. Every point has been acted on. The largest
changes: the estimand is now stated formally as a conditional probability and carried into the title,
abstract, figures and conclusion; T3 has a full operational definition with worked examples and is
split into T3a and T3b by relatedness, which shows that only 28% of the generic-language mass matches both
the incident's technology and harm families; entity resolution is documented in detail, with the
137-row crosswalk now populated, an as-of-incident-date ownership check performed, an
attribution-basis layer added, and two corrections made; severity is reframed as exploratory with
explicit detectable-effect calculations; and the role result is presented as descriptive after a
leave-one-positive-out analysis showed it fragile. Three findings not asked for are reported because
the review's probing surfaced them. The pre-registered primary estimand is unchanged.

---

## Point 1 — Estimand and denominator

> 1. The denominator is not a neutral population of "AI incidents," and the interpretation of the 97.7% shadow rate needs to be narrowed substantially.
>
> The manuscript treats 307 conservatively matched AIID incidents as the analytical denominator. However, AIID is a media-derived incident repository rather than a census of events, and the inclusion process further selects incidents that can be linked with sufficient confidence to 21 U.S.-listed domestic issuers. This creates at least three layers of selection: (i) an incident must become sufficiently public to enter AIID; (ii) the organization must be identifiable; and (iii) the organization must be resolvable to a U.S.-listed issuer within the study protocol.
>
> The authors acknowledge these limitations, but the headline "97.7% disclosure shadow" can still easily be interpreted as a rate applying to corporate AI incidents generally. The denominator is more accurately "externally documented, AIID-recorded, conservatively issuer-matchable incidents." This distinction should be carried consistently into the title, abstract, discussion, conclusion, and figures.
>
> I suggest that the authors explicitly discuss the selection mechanism as part of the estimand. In particular, the paper should clarify whether the intended estimand is:
> (a) the probability of substantive SEC disclosure conditional on an AIID-recorded and matchable incident, or
> (b) a broader statement about corporate AI-incident transparency.
>
> The current design supports (a) much more strongly than (b).

**Response.** The reviewer is right, and the intended estimand is (a).

- **Estimand stated formally.** New Section 3.1.1, "Estimand and selection mechanism", states it as
  $\Pr($substantive disclosure in Forms 8-K, 10-K or 10-Q within 12 months $\mid$ the incident is
  recorded in AIID, the organization involved is identifiable in that record, and that organization is
  conservatively resolvable to a U.S.-listed domestic periodic-report filer under the study protocol$)$,
  and says explicitly that the design supports (a) and not (b).
- **The three selection layers are named and quantified**: publicity (AIID is media-derived);
  organizational identifiability (398 window incidents name only generic or individual actors); and
  resolvability (243 private, 400 unresolved, 26 foreign, 15 delisted). We also state that the
  direction of the resulting bias is not signed by the design, and why.
- **Carried through the paper.** A new closing paragraph of the Introduction states the conditioning
  before any number appears. `revision/edits/denominator_language.csv` lists 20 sentences in the
  abstract, introduction, results, discussion, conclusion and captions where "AI incidents" was used
  as if it were the population, each with its replacement; all are applied.
- **Abstract.** Now contains the sentence: "The estimand is therefore conditional... It is not a
  population statement about corporate AI-incident transparency."
- **Limitations reordered** so the estimand and selection limitation is first.
- **Title.** Changed to *"The AI Incident Disclosure Shadow: Tracking AI Incidents into U.S. Securities
  Filings"*. This drops
  "Investor Disclosures" (Point 7) and the census reading of "Matching AIID-Recorded AI Failures to
  ... Disclosures". The denominator itself is stated in the first sentence of the abstract, on the
  first page, and formally in the new Section 3.1.1, rather than carried as a qualifier in the
  title.

---

## Point 2 — T3 definition and sensitivity

> 2. The conceptual meaning of T3 is too broad and may mechanically inflate the "shadow."
>
> T3 includes cases in which an issuer disclosed generic risk language involving the same technology or harm family but did not identify the incident. Because large technology firms frequently include extensive AI, platform, safety, content, privacy, autonomous-system, legal, and operational risk language in periodic filings, many incidents may qualify as T3 almost automatically.
>
> This raises two issues.
>
> First, the threshold for "same technology or harm family" appears potentially permissive. A generic statement about AI errors, misinformation, automated systems, or regulatory risk may have only a weak substantive relationship to a specific AIID incident. The paper should provide a much more detailed operational definition of T3, with several positive and negative coding examples.
>
> Second, since T3 accounts for 278 of 307 incidents, the main "shadow" result is overwhelmingly driven by how T3 is defined. Readers need to understand whether T3 means a genuinely relevant generic acknowledgment of the realized risk or merely a broad risk-factor statement that could apply to many unrelated events.
>
> I strongly recommend reporting additional sensitivity analyses using narrower T3 definitions. For example, the authors could distinguish:
> T3a: generic language matching both the relevant AI application and harm category;
> T3b: language matching only one broad risk family;
> T4: no related language.
>
> If the 97.7% result is robust to materially stricter definitions of generic relatedness, the contribution would be much stronger.

**Response.** This was the most consequential point in the report, and acting on it changed what the
paper claims.

- **Operational definition (Section 3.4).** T3 now requires that a passage name the *class* of
  technology or the *class* of harm implicated in the incident. Both taxonomies are listed in full:
  nine technology or application families (recommender and ranking; automated content moderation;
  generative models and chatbots; autonomous vehicles and driver assistance; computer vision and
  biometrics; speech and NLP; advertising delivery and targeting; predictive scoring, pricing and
  eligibility; robotics and physical automation) and nine harm families (misinformation and content;
  discrimination and bias; privacy and surveillance; physical safety; economic and financial; IP and
  training data; minors and self-harm; service quality and error; legal rights and due process).
  Exclusions are explicit: statements about "technology risks", "regulatory risks", "litigation
  risks" or "operational risks" in the abstract do **not** qualify, nor does any AI mention untied to
  the implicated class, nor compensation-plan exhibits, subsidiary lists or promotional
  earnings-release language.
- **Pre-incident presence was not checked.** We state this plainly rather than leave it implicit: the
  original protocol did not test whether the same risk language pre-dated the incident, and neither
  does this revision, so T3 means "the same risk family was being discussed in the window", not "the
  issuer wrote this because of the incident".
- **Coding examples.** Supplementary Section S2 gives eight worked examples — four T3a and four T3b —
  spanning content/misinformation, generative-AI error, autonomous systems and bias/discrimination,
  each with the AIID id, issuer, which families qualified, and a verbatim fragment from the filing
  record.
- **T3a/T3b/T4 sensitivity, and the reviewer's suspicion is partly confirmed.** All 278 T3 incidents
  were re-coded. **T3a = 84** (27.4% of the sample, 22.5--32.7) and **T3b = 194**
    (63.2%, 57.5--68.6). T3a is a **minority** of the generic-language mass, 30.2% of it.
  Thin or ambiguous evidence resolves to T3b, the conservative direction. New **Table 3** reports the
  five-way distribution with three aggregates: shadow-broad 97.7% (= primary, unchanged),
  **T3b+T4 = 216/307 = 70.4%** (64.9--75.4), and T4 only = 7.2%.
- **Is the 97.7% robust to a stricter T3?** Yes, and for a reason we now state explicitly rather than
  claim as a result: T3a, T3b and T4 all sit outside the substantive tiers, so the shadow rate is
  *invariant* to the T3a/T3b and T3/T4 boundaries **by construction**. The split therefore addresses
  the interpretation of the T3 mass, not the headline rate. We say so in Section 4.2 and in the
  Table 3 caption rather than presenting invariance as evidence of robustness.
- **Discussion recalibrated.** The claim that the shadow is "mostly not silence" is gone. The text now
  reads: filings routinely discuss AI risk at class level, that discussion most often relates to a
  realized incident along only one dimension, and the incident itself is almost never identified. On
  the stricter reading, 70.4% of incidents have at most weakly related language.
- **Subgroup breakdowns** of the five-way split by severity, role and year are in Supplementary
  Tables S8--S9.
- One transparency note: a spot-check found the coding lexicon missed some domain synonyms (for
  example "fair lending" for discrimination). We report both the lexicon fixed before any value was
  computed (T3a = 80, 28.8% of T3) and the completed lexicon (T3a = 84, 30.2%), so the effect of the
  fix is visible rather than absorbed.

---

## Point 3 — "Disclosure shadow" terminology

> 3. The "disclosure shadow" terminology is memorable but normatively loaded.
>
> The authors repeatedly state that the construct is descriptive and does not imply legal noncompliance. I agree with this clarification. Nevertheless, the phrase "disclosure shadow" implicitly suggests hidden or withheld information. In many cases, however, an AIID incident may simply be immaterial to investors, operationally trivial, attributable only indirectly to the issuer, already public through another channel, or unrelated to any SEC disclosure requirement.
>
> Thus, the label may encourage stronger interpretation than the underlying empirical design warrants.
>
> I do not necessarily recommend abandoning the term, but the paper should define it more neutrally and repeatedly emphasize that it means "not identifiable in the specified SEC filing universe under the study protocol," rather than "undisclosed information that should have been disclosed." A useful robustness presentation would separately report:
> - incident-specific disclosure (T1),
> - formal consequence disclosure (T2),
> - generic related risk language (T3),
> - no related language (T4),
> without always collapsing T3+T4 into a single headline measure.

**Response.** We have kept the term and defined it neutrally, as the reviewer suggests.

- **Boxed definition, Section 3.4.** "An incident for which neither incident-specific disclosure (T1)
  nor disclosure of a directly related formal legal consequence (T2) could be identified in the
  issuer's Forms 8-K, 10-K and 10-Q filed within the observation window, under this study's search and
  coding protocol. The term is descriptive. It does not imply that the incident was material, that a
  disclosure obligation existed, that any information was withheld, or that any issuer failed to
  comply with a legal requirement. It means only: not identifiable in the specified SEC filing
  universe under the stated protocol."
- **Usage audit.** `revision/edits/shadow_usage.csv` lists all 29 uses of "shadow" with a flag for
  whether the surrounding sentence admits a normative reading; 2 were flagged and both are reworded
  (notably "rather than complete disclosure silence" → "rather than an absence of all related
  language").
- **Tiers first, aggregate second.** Section 4.1 now reports the four-tier distribution as the primary
  presentation and introduces T3+T4 explicitly as a labelled summary measure. **Table 2** is ordered
  the same way, with the two aggregates below a rule. The abstract now gives the tier counts — "4 T1,
  3 T2, 278 T3 and 22 T4" — *before* the 97.7% figure.
- **Figure 2** is now stacked T1/T2/T3a/T3b/T4 bars by severity rather than the collapsed shadow rate;
  the collapsed version with Wilson intervals is retained as supplementary Figure S1.
- **Benign explanations.** A new Discussion paragraph enumerates them: the incident may have been
  immaterial; operationally trivial; only indirectly attributable (the 14 platform-venue and 8
  mentioned-only incidents identified in this revision); already public through a channel this design
  does not search; or outside any SEC requirement, since filings are not an incident register and no
  U.S. rule required AI-incident reporting in the sample period. We state that the shadow rate is
  consistent with all of these and distinguishes among none of them.

---

## Point 4 — Entity resolution

> 4. The validity of the entity-resolution procedure requires more evidence.
>
> The manuscript reports a 137-row validation crosswalk and states that two incident-level mapping errors were corrected. However, entity resolution is central to the entire study, particularly because AI incidents often involve complex relations among developers, model providers, platform operators, customers, subsidiaries, and corporate parents.
>
> The paper should provide more information on:
> - the criteria used to attribute an incident to an issuer;
> - how multi-party incidents were handled;
> - whether one AIID incident could map to multiple issuers;
> - how responsibility was distinguished from mere mention or ecosystem involvement;
> - how subsidiaries and historical ownership structures were treated;
> - whether mappings were date-sensitive;
> - the number of ambiguous cases excluded at each stage;
> - the inter-rater reliability of issuer matching itself.
>
> The current reliability exercise focuses on disclosure classification, but issuer matching is another important source of measurement error. A second-coder audit of a sample of entity mappings would substantially strengthen the paper.

Each bullet is answered in turn. Section 3.2 is rewritten and Supplementary Tables S3--S5 added.

1. **Criteria used to attribute an incident to an issuer.** Stated honestly, including what it was
   not: the original procedure attributed an incident to an issuer when a resolvable organization
   appeared in AIID's own `deployers` or `developers` fields, so it inherited AIID's attribution
   rather than applying an independent responsibility test, and it had no category for an issuer that
   merely hosted third-party content. The revision adds that layer (see bullet 4).
2. **Multi-party incidents.** The discarded candidates were never persisted, so we re-derived them
   (`scripts/cocandidates.py`): **27 of 307** incidents (8.8%) had at least two distinct
   listed-issuer candidates and 22 had at least two domestic candidates, with a maximum of
   5 candidates on one incident. Every case is listed in Supplementary Table S3.
3. **Could one incident map to multiple issuers?** No, and we now say so openly together with how the
   single issuer was chosen: by listing status (domestic filer, then domestic parent, then delisted,
   then foreign), **with ties broken by the order in which organizations appear in the AIID record**
   (deployers before developers). We state that this tie-break is arbitrary with respect to
   responsibility, and we test it: preferring the developer reassigns 2 incidents and preferring
   the listed parent reassigns 5. Because those issuers' filings were never searched, the affected
   incidents are dropped rather than recoded; the shadow stays at 97.7% and 97.7% respectively
   (Table 8).
4. **Responsibility versus mention or ecosystem involvement.** All 307 incidents were coded at
   revision into five attribution bases: developer (49), deployer-operator
   (14), both (222), **platform-venue (14)** and **mentioned-only (8)**.
   New **Table 5** gives the distribution overall, by tier and by issuer. No platform-venue or
   mentioned-only incident received T1 or T2. Excluding platform-venue gives a shadow of
   97.6% on N = 293; excluding both gives 97.5% on N = 285 (Table 8).
5. **Subsidiaries and historical ownership.** 47 incidents are parent-linked, predominantly Waymo (17)
   and Cruise (12). The rule is now stated, with examples, and the crosswalk's static nature is
   disclosed.
6. **Were mappings date-sensitive?** **No — and we say so.** The crosswalk assigns one parent per slug
   for the whole 2019--2026 window with no as-of-date logic, and the original manuscript's claim that
   ownership was confirmed "for the date of the incident" was not supported by the artifact. That
   sentence is removed. The check was performed at revision for all 47 parent-linked incidents:
   44 hold, 2 are in-house products with no acquisition date, and **1 fails** — incident 501
   (3 June 2019) maps naviHealth to UnitedHealth Group, which acquired naviHealth only in 2020.
7. **Ambiguous cases excluded at each stage.** Supplementary Table S4 gives the stage-by-stage
   accounting; the five categories sum to exactly 1,082 = 1,389 − 307, and we note that foreign and
   delisted exclusions occur *after* a successful match (348 = 307 + 26 + 15).
8. **Inter-rater reliability of issuer matching.** The reviewer is right that this was missing. Two
   things were done. First, a correction of the record: the 137-row validation crosswalk distributed
   with the original package **had its verdict and note columns empty**, so the review the manuscript
   described left no trace, and the claim that "two incident-level mapping errors" were corrected
   could not be substantiated. That sentence is removed. The review was performed at revision and
   every row now carries a verdict: 88 stand, 40 correctly excluded, 7 stand with a
   qualification, **2 require correction** — incident 501 above and incident 350, which maps to
   Serve Robotics, a company that became an SEC reporting issuer only at its August 2023 reverse
   merger. A corrected sample is reported in Table 8 at 97.7%. Second, **we ran the blind second-coder
   audit**: 80 incidents (seed 42), stratified to oversample the ambiguous cases, coded by someone
   who saw the AIID record but not our mapping.

   **Agreement on issuer identity is 82.5% (66/80), kappa = 0.79, AC1 = 0.82** — a lower bound,
   since the sample is weighted toward the hard cases. All 14 disagreements are multi-candidate
   incidents; agreement is complete in the other three strata, and **none touches an incident coded
   T1 or T2**. Dropping all 14 gives 97.6% (95.1-99.0) on N = 293, now the last row of Table 8.

   Every disagreement is adjudicated against the attribution rules and published (Supplementary
   Tables S11-S12): ten resolve in favour of our mapping, four in favour of the second coder. The
   four reassigned incidents join the corrected sample, which is N = 303 and still 97.7%.

---

## Point 5 — Severity analysis

> 5. The severity analysis is too weak to support much substantive interpretation.
>
> Only 40 of 307 incidents have external CSET severity information, while the remaining incidents are classified using a study-specific rubric. The manuscript appropriately acknowledges this limitation, but then still gives the severity analysis considerable interpretive weight.
>
> There are only seven substantive disclosures in the entire sample. With such sparse outcomes, the absence of a statistically significant severity gradient is expected to have very low power. A p-value of 0.61 should not be used to suggest that severity is unimportant.
>
> I recommend reframing this section as explicitly exploratory. The authors should report exact counts rather than emphasizing percentages, provide uncertainty intervals for each severity group, and ideally conduct a simple power or detectable-effect discussion. It would also help to report whether the conclusions change when restricting the analysis to the externally classified subset, even if this subset is too small for formal inference.

**Response.** We agree, and the p-value is now presented as uninformative rather than as evidence.

- **Section 4.3 retitled** "Incident severity and substantive disclosure (exploratory)".
- **Exact counts first.** Table 4 leads with counts: 2 of 42 Severe, 1 of 50 Moderate, 4 of 215
  Limited. Clopper--Pearson exact intervals are given for T1 and for T1+T2 in every group, and all
  intervals overlap.
- **Detectable-effect discussion.** New `scripts/severity_power.py` computes power exactly
  (binomial-weighted Fisher rejection region, no normal approximation, which would be unreliable at
  4/215 and 2/42). Detecting a difference from the Limited group's 1.9% at 80% power would
  require the Severe rate to reach **13.4%** — **7.2× the Limited rate**, a 11.5
  percentage-point difference, or 6/42 vs 4/215. Power is **23.3%** against a threefold
  difference and **56.1%** against a fivefold one. Post-hoc power at the observed effect is
  16.7%, labelled post-hoc and for orientation only.
- **No claim that severity is unimportant.** The sentence stating that observable harm severity fails
  to explain disclosure is removed. The text now says only that no gradient is detectable on a design
  that could not have detected less than roughly a sevenfold difference, and states that we do not
  claim severity is irrelevant.
- **CSET-only subset.** Supplementary Table S6 gives the tier distribution for the 40 externally
  classified incidents. The subset contains **one** substantive disclosure, so no test is performed
  and we say so.
- **H3 restated** in the Introduction as an exploratory expectation rather than a powered hypothesis,
  with the 23.3% figure cited at the point of statement.

---

## Point 6 — Developer versus deployer

> 6. The developer-versus-deployer result (p = 0.02) may be fragile and should be presented more cautiously.
>
> The role analysis is potentially interesting, but it is based on only seven substantive disclosures and four T1 cases. A statistically significant exact test in such a sparse table can be highly sensitive to only one or two observations.
>
> The manuscript already warns against causal interpretation, which is appropriate, but I would go further. Please provide the underlying contingency table with exact counts, not only percentages or p-values. Also consider a leave-one-positive-case-out sensitivity analysis to show how stable the result is to the removal or reclassification of any one T1/T2 incident.
>
> Given the small number of positive cases, this result should be framed as descriptive hypothesis generation rather than an inferential secondary finding.

**Response.** The reviewer's concern is well founded; the result is more fragile than the original
presentation implied, and in one respect the original prose did not match the test.

- **Full contingency table with counts.** New **Table 6**: developer-only n = 58 with 0 T1 and 0 T2;
  deployer-only n = 14 with 1 T1 and 1 T2; both n = 235 with 3 T1 and 2 T2 (pre-registered coding),
  plus the T3a/T3b/T4 columns and marginals, and the 2×2 contrast below.
- **Which contrast produced p = 0.02.** Documented: it is the **three-way** contrast (role × substantive),
  chi-square, Monte-Carlo exact permutation, B = 20,000, seed 42. Re-run, $\chi^2$ = 10.434,
  p = 0.024. **The 2×2 contrast the prose described — developer-only versus
  any-deployer — does not reject: $\chi^2$ = 1.669, p = 0.355.** Both are now reported. The
  association is a property of the three-level specification, in which the 14-incident deployer-only
  cell carries two of the seven positives, not of the developer/deployer dichotomy.
- **Leave-one-positive-out.** `scripts/role_loo.py` drops, downgrades by one tier, and reclassifies
  to T3 each of the seven substantive incidents, recomputing both contrasts — 22 perturbations,
  reported in full in Supplementary Table S7. The three-way p ranges **0.016 to 0.225** and
  reaches or exceeds 0.05 in **5 of 22** cases; dropping either deployer-only positive alone
  moves it to about 0.22. The 2×2 p ranges 0.355 to 0.708 and never rejects. Promoting a
  single developer-only T3 incident to T1 gives p = 0.054.
- **Reframed as hypothesis-generating.** Section 4.4 and the corresponding Discussion paragraph now
  present the pattern descriptively and report the LOO range. **"exact p = 0.02" is removed from the
  abstract**, replaced by: "all incident-specific disclosures involved issuers in a deployer or dual
  developer-deployer role, a pattern fragile to single-case changes."
- **A correction the reviewer's scrutiny surfaced.** The original sentence "All four T1 disclosures
  featured an issuer as a deployer of the implicated system" is **false as written**: only one of the
  four T1 incidents carries `role = deployer`; the other three are `role = both`. It is true only
  under a deployer-or-both reading. Every instance is replaced with: "All four incident-specific (T1)
  disclosures involved issuers coded in a deployer or dual developer-deployer role; none of the 58
  developer-only incidents received T1 or T2 disclosure." Replacements are logged in
  `revision/edits/deployer_claim.csv`. We cross-checked the four T1 issuers against the new
  attribution coding: none is platform-venue or mentioned-only.

---

## Point 7 — SEC filing disclosure versus investor-facing disclosure

> 7. The paper should more clearly distinguish "SEC filing disclosure" from "investor-facing disclosure" in general.
>
> The manuscript frequently uses language such as "investor disclosure" or "information provided to investors," but the empirical search universe is limited to Forms 8-K, 10-K, and 10-Q. Public companies communicate with investors through many additional channels, including earnings calls, investor presentations, press releases, litigation disclosures outside periodic reports, regulatory announcements, websites, and conference communications.
>
> The current design therefore measures visibility in a specific SEC filing universe, not all investor-facing communication.
>
> This distinction matters because some AI incidents may be publicly acknowledged elsewhere even if not repeated in periodic filings. The title, abstract, and discussion should be more precise. At minimum, I suggest replacing broad phrases such as "investor disclosure" with "SEC filing disclosure" or "disclosure in Forms 8-K, 10-K, and 10-Q" where appropriate.

**Response.** Agreed throughout; the distinction is now carried in the title.

- **Wording.** `revision/edits/investor_language.csv` lists 20 sentences using "investor
  disclosure", "information provided to investors", "investor-facing", "investor reporting" or
  "visible to investors", each with its SEC-filing replacement; all applied. The title no longer uses
  "investor disclosure"; the abstract says "Forms 8-K, 10-K and 10-Q" throughout.
- **Channels not searched (Section 3.3).** A new paragraph lists them explicitly: earnings-call
  transcripts and prepared remarks; investor presentations and investor-day materials; press releases
  and newsroom posts not furnished as exhibits; litigation dockets outside SEC filings; regulator
  announcements and enforcement releases; corporate websites, product blogs and transparency reports;
  and conference or analyst communications. We state that an incident acknowledged in any of those but
  not repeated in a periodic report is recorded here as not identifiable.
- **New Limitations item**, placed second: the estimate is a lower bound on total investor-facing
  acknowledgement and an accurate measure of periodic-filing visibility.
- **Future research.** Applying the same four-tier coding to earnings-call transcripts, investor
  presentations and press releases is named as the most direct extension, because it would separate
  "not disclosed to investors" from "not repeated in periodic filings".

---

## Point 8 — Cybersecurity disclosure literature

> 8. The relationship between the paper and the cybersecurity disclosure literature could be developed more deeply.
>
> The manuscript correctly identifies cybersecurity disclosure as the closest empirical analog. However, the comparison currently functions mainly as motivation. The paper would benefit from a more explicit explanation of what is methodologically or institutionally different about AI incidents.
>
> For example:
> - Cybersecurity events often have clearer event boundaries and notification regimes.
> - Data breaches may generate measurable affected-person counts.
> - AI incidents can involve diffuse harms, content effects, model errors, discrimination, misinformation, autonomous-system failures, and third-party deployment.
> - The attribution of responsibility is often more ambiguous for AI systems.
> - Materiality pathways may differ substantially.
>
> These distinctions could help explain why incident-level AI disclosure is an important separate research problem rather than simply a replication of the cybersecurity disclosure design.

**Response.** The paragraph is expanded from 5 sentences to roughly 380 words and restructured around
the reviewer's five dimensions, under the heading "the closest analog, and where the analogy stops".

- **Event boundaries.** A breach has a discovery date, scope and end; an AI incident may be a
  continuing property of a deployed system, which is why the window is anchored on the AIID incident
  date rather than a firm-declared event.
- **Notification regimes.** Contrasted explicitly: the SEC's 2023 rules requiring Form 8-K Item 1.05
  current reporting and Regulation S-K Item 106 annual disclosure `\citep{SEC2023Cyber}`, layered on
  state breach-notification statutes since 2003 `\citep{RomanoskyTelangAcquisti2011}`, against the
  absence of any U.S. AI-incident reporting duty in the sample period — only voluntary frameworks
  `\citep{NIST2023AIRMF}` and, outside the U.S., the EU AI Act's serious-incident duty
  `\citep{EUAIAct2024}`.
- **Affected-person counts.** Breaches produce them; a recommender amplifying misinformation does not.
- **Diffuse harms.** Named: content effects, model error, discrimination, misinformation, degraded
  service, autonomous-system failure.
- **Third-party deployment chains and attribution ambiguity.** A model built by one firm, deployed by a
  second, distributed on a third's platform `\citep{Cobbe2023,OECD2024}` — and we tie this directly to
  the entity-resolution problem of Point 4 rather than leaving it abstract.
- **Materiality pathways.** In this sample, incidents reach filings through booked charges or legal
  process, not notification duty.
- **Closing claim.** The cyber literature supplies the design template but not the expected disclosure
  rate, the unit of analysis, or the attribution procedure, each of which had to be built for AI.
- **Five new citations, all verified** before inclusion: three DOIs resolved against the Crossref API
  with matching metadata (10.1002/pam.20567, 10.1145/3593013.3594073, 10.6028/NIST.AI.100-1), the SEC
  rule against the Federal Register API (88 FR 51896, 4 August 2023), and the AI Act against EUR-Lex
  (OJ L, 2024/1689, 12.7.2024).
- **Discussion link.** A new sentence connects the T3-dominant pattern to the generic-versus-specific
  finding in `\citet{WangKannanUlmer2013}` and `\citet{Hope2016}`: class-level AI risk language is
  near-ubiquitous among these issuers and mostly matches the realized incident along one dimension, so
  its presence does not let an investor identify what occurred.

---

## Change table

| Reviewer item | Manuscript location | Nature of change |
|---|---|---|
| 1 estimand | Title; Abstract; §1 final ¶; new §3.1.1; Limitations item 1 | new text; global rewording (20 sentences) |
| 1 denominator wording | abstract, §1, §4, §5, §6, captions | rewording (`edits/denominator_language.csv`) |
| 2 T3 definition | §3.4; Supplementary S2 | new text; 8 worked examples |
| 2 T3a/T3b sensitivity | §4.2; **Table 3**; Table 8; Suppl. S8--S10 | new analysis; new table; 278 incidents recoded |
| 2 Discussion recalibration | §5 ¶2 | rewording of a claim that overstated relatedness |
| 3 neutral definition | §3.4 boxed definition | new text |
| 3 shadow usage | 29 sentences, 2 reworded | rewording (`edits/shadow_usage.csv`) |
| 3 tiers before aggregate | §4.1; **Table 2**; Abstract | restructuring |
| 3 stacked figure | **Figure 2**; new Figure S1 | figure regenerated |
| 3 benign explanations | §5 new ¶ | new text |
| 4.1 attribution criteria | §3.2 | new text (states what was inherited from AIID) |
| 4.2 multi-party | §3.2; Suppl. S3 | new analysis + table |
| 4.3 one-to-many | §3.2; Table 8 | new text; 2 tie-break sensitivities |
| 4.4 responsibility vs mention | §3.2.1; **Table 5**; Table 8 | new coding of all 307; new table; 2 exclusion sensitivities |
| 4.5 subsidiaries | §3.2 | new text |
| 4.6 date sensitivity | §3.2; Table 8 | new analysis (47 incidents); 1 failure; claim removed |
| 4.7 exclusion stages | Suppl. S4 | new table |
| 4.8 entity reliability | §3.2; Table 8; Limitations; Suppl. S11–S12 | audit completed: 82.5%, kappa 0.79, AC1 0.82; 4 mappings changed |
| 5 exact counts | **Table 4** | table rebuilt with counts and CIs |
| 5 power | §4.3; new script | new analysis |
| 5 exploratory framing | §4.3 heading; §1 H3; §5 | rewording |
| 5 CSET subset | Suppl. S6 | new table |
| 6 contingency table | **Table 6** | new table |
| 6 which contrast | §4.4 | both contrasts now reported |
| 6 LOO | §4.4; Suppl. S7 | new analysis, 22 perturbations |
| 6 framing | §4.4; §5; Abstract | rewording; p-value removed from abstract |
| 7 wording | title, abstract, body, captions | rewording (`edits/investor_language.csv`) |
| 7 channels not searched | §3.3 | new ¶ |
| 7 limitation | Limitations item 2 | new item |
| 7 future research | §6 | new sentence |
| 8 cyber contrast | §2 | ¶ expanded to ~380 words, 5 dimensions |
| 8 citations | references | 5 verified additions |
| 8 generic-vs-specific link | §5 | new sentence |

## Changes we made that were not requested

1. **The 137-row validation crosswalk was empty**, so the original claim that two mapping errors were
   identified and corrected could not be substantiated. The sentence is removed; the review was
   performed at revision and the populated crosswalk is in the package.
2. **T2 has no demonstrated inter-coder reliability**: one tier against the rest, Cohen's kappa is
   **−0.023**, the second coder having disagreed with all three pass-one T2 codes. This was in the
   replication package but not in the manuscript. It is now reported in §4.7 and Supplementary
   Table S9, T1 is designated the primary measure, and T1+T2 is presented as an upper bound with the
   substantive count given as a range. All three T2 incidents were re-read and adjudicated: one moves
   to T1 (GM's 10-Q names the OnStar Smart Driver product and the conduct, which satisfies T1 without
   AI framing), giving 5 T1 and 2 T2 with the substantive total unchanged at 7.
3. **The deployer claim was factually wrong as written** (Point 6 above) and is corrected everywhere.
4. **A coding-log discrepancy**: incident 350 carries T4 in the analytical table and T3 in the coding
   log, where a written rationale supports T3. Both are inside the shadow so no rate changes; the
   variant is reported in Table 8.
5. **Two entity tie-break sensitivities** (prefer-developer, prefer-parent) were added because the
   original tie-break is arbitrary with respect to responsibility.
6. **Severity labels renamed** `sev_limited` / `sev_moderate` / `sev_severe`, because the original
   values `T1-limited` / `T2-moderate` / `T3-severe` collide with the disclosure codes T1--T4 in the
   same table and invite a mis-join by anyone reproducing from the CSV.
7. **The Generative AI Statement is expanded** to record that an AI system produced proposed values for
   three revision-stage recoding tasks under author review, each with a per-case rationale and
   confidence flag in `AUTHOR_REVIEW.csv`.

## What the audit changed

Four mappings out of 307, and one attribution basis. No disclosure code, no tier count, no reported
aggregate: 97.7% pre-registered, 97.7% corrected, 97.6% with every disputed mapping dropped. Sample,
instructions, returned codings and adjudications are all in `data/`.

## Provisional coding decisions

Every coding judgment made during this revision is recorded in `AUTHOR_REVIEW.csv`, one row per
decision with file, incident id, field, proposed value, confidence and rationale: 776 rows in
total (126 high confidence, 560 medium, 90 low). The authors have reviewed this file; it is
included in the package so a reader can see exactly which values rest on judgment and how much.


---

# Response to Reviewer 2

We thank Reviewer 2. All four points are addressed below.

**A note on numbering before the individual responses.** Reviewer 2's table numbers refer to the
originally submitted manuscript, where Table 2 was the severity table and Table 3 the list of
substantively disclosed incidents. In the revised manuscript those are **Table 4** and **Table 7**,
because answering Reviewer 1's point 2 inserted a new Section 4.2 and its table, shifting the later
tables down by one. Both of the tables Reviewer 2 identifies have been fixed, and we describe them by
content below as well as by number so there is no ambiguity.

## Point 1 — exact counts in the Figure 1 flowchart

> 1. Add the exact sample counts for dropped categories into the Figure 1 flowchart so they match the numbers in the written text.

**Response.** Done. Figure 1 is rebuilt and is now generated by `scripts/make_figures.py`.

- **Every dropped category now carries its count on its own branch**, grouped by the stage at which
  the exclusion applies: incident date outside 2019--2026 **208**; then generic or individual actors
  only **398**, named entity not in the crosswalk **400**, privately held firm **243** (subtotal
  1,041); then, after a successful organization-to-registrant match, foreign private issuer **26** and
  delisted on the incident date **15** (subtotal 41).
- **They match the written text exactly, and the figure shows the arithmetic** so a reader can check
  it without turning back to Section 3.1: 1,597 − 208 = 1,389; 1,389 − 398 − 400 − 243 = 348;
  348 − 26 − 15 = 307. A second line gives the total as 398 + 400 + 243 + 26 + 15 = 1,082, which is the
  figure stated in Section 3.1, and 1,389 − 1,082 = 307. All four identities are asserted in the script
  before the figure is drawn, so a regeneration that broke the correspondence would fail rather than
  silently render a figure that disagrees with the text.
- An intermediate box for the 348 matched incidents was added, because 348 → 307 is where the foreign
  and delisted exclusions apply and the original figure did not show that step.
- A terminal box carries the corrected sample of 305 used in the robustness table, fed by a branch
  naming both removed incidents (**501** and **350**).
- **Presentation.** The figure is monochrome — white boxes, black rules, emphasis by line weight, and
  dashed exclusion branches — so it reads in greyscale and in print. Every arrow has a clear gap at
  both ends, computed from each box's visual border rather than its nominal rectangle, and all six
  boxes sit at uniform vertical spacing so the connectors are equal in length. Eight assertions, four
  arithmetic and four geometric, run before the figure is drawn.
- Mirrored to `frontiers/submission/Figure1.png`, byte-identical. That mirroring now happens inside
  the figure script; the previous arrangement copied figures before the revision script overwrote two
  of them, which had left the portal copies stale.

## Point 2 — exact counts for developer versus deployer, and the severity power caveat

> 2. Show the exact table counts for the developer vs. deployer comparison, and remind readers that the severity test had low statistical power due to having only 7 disclosed incidents.

**Response.** Done, both parts.

- **Exact counts.** New **Table 6** gives the full contingency table as counts rather than
  percentages: developer-only n = 58 with 0 T1 and 0 T2; deployer-only n = 14 with 1 T1 and 1 T2;
  both n = 235 with 3 T1 and 2 T2, with the T3a, T3b and T4 columns and all marginals. A labelled
  lower panel gives the two-by-two contrast: developer-only, 0 substantive of which 0 are T1; any
  deployer, 7 substantive of which 5 are T1. Table 6 is referenced from Section 4.4, the section that
  analyses it.
- Reviewer 1's point 6 led us further on the same result, and the outcome is reported alongside: the
  three-way contrast gives p = 0.024 while the two-by-two contrast the prose described does **not**
  reject (p = 0.355), and across 22 single-case perturbations the three-way p ranges 0.016 to 0.225,
  crossing 0.05 in 5 of them. The finding is now presented as descriptive and hypothesis-generating,
  and the p-value has been removed from the abstract.
- **The low-power reminder now appears twice, in bold, naming the seven incidents and the figure.**
  Immediately after the p = 0.61 result in Section 4.3: "That test has very low power: with only
  **seven** substantively disclosed incidents in the entire sample, the design has approximately
  **23.3%** power to detect even a threefold difference in substantive-disclosure rates between the
  Severe and Limited groups, so p = 0.61 is close to uninformative about whether a severity gradient
  exists." And again in the Discussion severity paragraph, in the sentence beginning "The honest
  reading is that the design cannot resolve this question, and the reason is the seven substantively
  disclosed incidents on which the whole contrast rests".
- The section heading is now "Incident severity and substantive disclosure (exploratory)", and the
  sentence implying that observable harm severity fails to explain disclosure has been removed.

## Point 3 — text overlap in Table 2, run-together text in Table 3

> 3. Correct text overlap in Table 2, fix run-together text in Table 3.

**Response.** Done, and the overlap had a single cause affecting every table in the paper, so the fix
is general rather than local.

- **Text overlap.** In the submitted manuscript the table's top rule was set level with the last line
  of the caption — in the original Table 2 the rule sat beside "across tiers: p = 0.61", and in the
  original Table 4 beside "where shown". The cause is that this document class's `\caption` does not
  close the paragraph, so a following `\centering` leaves the tabular in the same horizontal list and
  it rides up beside the caption whenever the last caption line is short. We tested four candidate
  fixes and only one works in this class: replacing `\centering` with an explicit
  `\begin{center} ... \end{center}` environment, which forces the paragraph to close. (`\par`,
  `\newline` and `\vskip` all leave the overlap in place.) **All seven tables** now use the center
  environment, and the compiled PDF shows a clean 7.1pt gap between the caption and the first rule in
  every one of them, measured from the rendered page rather than assumed.
- **Run-together text.** The original Table 3 listed two General Motors T1 rows with identical
  "10-K Item 1/1A" filing locations and no way to tell them apart, and its rightmost column ran to the
  block edge. It is now **Table 7**, generated from the coded data rather than maintained by hand,
  with an AIID incident id on every row, a fixed-width column for booked impact, and the tier shown as
  "T2 → T1" where the revision-stage adjudication changed it. That last point also repaired a
  substantive inconsistency: the hand-written table still showed incident 733 as T2 after Section 4.7
  moved it to T1.
- **We inspected every other table for the same defects**, as rendered PDF pages rather than as
  source. Three further problems were found and fixed: Table 3 repeated the tier label in its
  description column ("T1 | T1 incident-specific"); Table 5 stacked three panels with no headings, now
  labelled Panels A, B and C with the abbreviated column heads spelled out; and Table 6's two-by-two
  panel contained genuinely run-together text, "substantive 0 (T1 0)", now "0 substantive, of which 0
  are T1". The LaTeX log reports zero overfull boxes inside any tabular.
- Tables 2 through 8 are now produced by `scripts/make_tables_tex.py`, so none can drift out of
  step with the data or reacquire these defects.

## Point 4 — the framework under newer regulations

> 4. Briefly mention how future studies could use this framework under newer regulations, such as the EU AI Act.

**Response.** Done. Three sentences were added to Future Research:

> The most informative such comparison is already scheduled by regulation. Article 73 of the EU AI
> Act obliges providers of high-risk AI systems to report serious incidents to national
> market-surveillance authorities within defined deadlines, which will for the first time create a
> mandatory incident record running alongside the voluntary, media-derived one this study uses.
> Re-applying the incident-level design to issuers within that regime --- and to any future SEC
> guidance specific to AI, whether through interpretive releases or an Item 1.05-style
> current-reporting requirement of the kind already in force for cybersecurity --- would test
> directly whether mandatory incident reporting narrows the difference between externally recorded
> incidents and the incidents identifiable in securities filings. Because the four-tier coding and
> the conditional estimand travel unchanged to that setting, the estimates reported here provide the
> pre-regime baseline against which any such narrowing would be measured.

The closing sentence states what makes the present estimates useful to that future work: they are a
pre-regime baseline. `EUAIAct2024` and `SEC2023Cyber` were already in the bibliography, added in
response to Reviewer 1's point 8 and verified then against EUR-Lex and the Federal Register API
respectively; no new references were introduced.

## Change table, Reviewer 2

| Item | Manuscript location | Nature of change |
|---|---|---|
| 1 dropped-category counts | Figure 1 | figure rebuilt from script; every branch count added; both reconciliations printed and asserted in code |
| 1 corrected-sample branch | Figure 1 | new terminal box, incidents 501 and 350 named |
| 1 presentation | Figure 1 | monochrome, gapped arrows, uniform spacing, full text width |
| 1 mirroring | `frontiers/submission/Figure1.png` | mirroring moved inside the figure script |
| 2 exact role counts | Table 6, §4.4 | new table with counts and marginals, plus the two-by-two panel |
| 2 low-power reminder | §4.3, immediately after p = 0.61 | new bold sentence naming seven incidents and 23.3% |
| 2 low-power reminder | Discussion, severity paragraph | second statement of the same caveat |
| 3 caption / rule overlap | **all seven tables** | `\centering` replaced by the center environment; 7.1pt gap verified in the compiled PDF |
| 3 run-together rows | Table 7 | regenerated from data; AIID ids added; fixed-width impact column; "T2 → T1" shown |
| 3 further defects found | Tables 2, 4, 5 | duplicate tier label removed; panels labelled; two-by-two panel rewritten |
| 4 future research | §6 | three sentences on Article 73 and future SEC guidance |
| — | `results/number_audit.csv` | entries added for the Figure 1 reconciliation counts and the power figure |
