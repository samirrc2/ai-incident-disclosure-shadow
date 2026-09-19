# Second-coder instructions — entity-mapping audit (rev1 §5B)

You are coding **which U.S.-listed issuer, if any, an AI incident should be attributed to**. This is
a blind audit: the sheet does not show the mapping the study made. Do not look it up in
`data/incident_firm_map.csv` or `data/disclosure_coding.csv` before you finish.

**Input:** `entity_audit_sample_rev1.csv`, 80 incidents. For each row you see the AIID incident id,
date, title, summary, and every organization named in the AIID record.

**Fill in five columns.** Leave a row blank only if you cannot form a view at all.

## 1. `second_coder_issuer`
The U.S.-listed domestic issuer (a company filing Forms 8-K / 10-K / 10-Q) to which the incident
should be attributed, using the company's name. Rules:

- Attribute to the **listed parent** if the named entity is a subsidiary, product or platform of one,
  **but only if the parent controlled that entity on the incident date.** If control began later,
  write `NONE-not-owned-at-incident-date`.
- If the named entity is privately held, foreign-listed (files 20-F/6-K), or was not a listed filer
  on the incident date, write `NONE-not-listed`.
- If more than one listed issuer is genuinely implicated, name the one you judge **most
  responsible for the system that produced the harm**, and list the others in `notes`.
- If no listed issuer is implicated, write `NONE`.

## 2. `second_coder_role`
One of `developer`, `deployer`, `both` — whether the issuer built the system, ran it in the context
that produced the harm, or both.

## 3. `second_coder_attribution_basis`
One of:

| basis | meaning |
|---|---|
| `developer` | the issuer built the model or system |
| `deployer-operator` | the issuer ran the system in the context that produced the harm, or made the deployment decision |
| `both` | both of the above |
| `platform-venue` | the issuer hosted third-party content or third-party use; the system that produced the harm was not the issuer's own decision |
| `mentioned-only` | the issuer is named but no developer, deployer or venue relationship is evident — including where the issuer is the harmed party, or is one of several vendors named in a comparative study |

Hosting third-party content, being a customer of an unrelated vendor, or being named in press
coverage does **not** by itself make an issuer a developer or deployer.

## 4. `second_coder_confidence`
`high`, `medium`, or `low`.

## 5. `second_coder_notes`
Anything that affected the decision: other candidate issuers, ownership timing, why you rejected an
obvious candidate.

## What happens next
`scripts/rev1_entity_reliability.py` computes raw agreement, Cohen's kappa and Gwet's AC1 on issuer
identity and on role, lists every disagreement for reconciliation, and re-estimates the primary
disclosure rates under your mappings. Disagreements are reconciled **after** the comparison is run,
never before.

**Do not reconcile with the original coder while coding.** Code independently, return the sheet, then
reconcile.
