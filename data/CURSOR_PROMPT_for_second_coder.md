# Cursor prompt for the second-coder entity audit

**Read this line first.** The reliability figure this produces is only meaningful if the 80 judgments
are **Robin's own**. If an AI assigns the issuers, the resulting kappa measures a model re-applying a
rule, not two independent coders agreeing — and reporting it as inter-rater reliability would be
false, and would contradict the manuscript's own Generative AI Statement. So Cursor's job here is to
be a **data-entry harness**: show one case at a time, keep the original mapping hidden, record what
Robin decides, and run the analysis at the end. It must not suggest, rank or pre-fill an answer.

Paste everything below into Cursor, with the repo `ai-incident-disclosure-shadow` open.

---

You are building a small local coding harness. You are **not** doing the coding.

## Hard constraints

1. **Do not read, open, grep, print or summarise any of these files at any point**, and do not let
   the harness load them: `data/incident_firm_map.csv`, `data/disclosure_coding.csv`,
   `data/validation_sheet.csv`, `revision/data/crosswalk_rev1.csv`,
   `revision/data/attribution_rev1.csv`, `scripts/crosswalk.py`, `scripts/entity_resolve.py`.
   They contain the mapping being audited. This audit is blind; seeing them invalidates it.
2. **Never propose an issuer, role or attribution basis**, and never pre-fill any field, not even as
   a "suggestion to confirm". If I ask you to, refuse and remind me why.
3. **Do not answer substantive questions about a case while I am coding it** — not "which company
   owns X", not "is this a deployer". If I am unsure, I record low confidence and write the doubt in
   the notes field. That uncertainty is data.
4. Do not modify anything under `data/`. Write only to the paths named below.

## What to build

A single script, `scripts/rev1_entity_audit_cli.py`, that I run with
`python3 scripts/rev1_entity_audit_cli.py`. It should:

- Load `revision/data/entity_audit_sample_rev1.csv` (80 rows). Columns present:
  `incident_id, incident_date, stratum, aiid_title, aiid_summary, organizations_named_in_aiid`,
  then five empty columns `second_coder_issuer, second_coder_role,
  second_coder_attribution_basis, second_coder_confidence, second_coder_notes`.
- Present **one incident at a time**, clearing the screen between cases, showing only:
  the incident id, the date, the AIID title, the AIID summary, and the organizations named in the
  AIID record. **Do not display the `stratum` column** — it hints at which cases are hard.
- Prompt for the five fields in order, with validation:
  - `second_coder_issuer` — free text. Accept the shortcuts `NONE`, `NONE-not-listed`,
    `NONE-not-owned-at-incident-date`.
  - `second_coder_role` — one of `developer`, `deployer`, `both`.
  - `second_coder_attribution_basis` — one of `developer`, `deployer-operator`, `both`,
    `platform-venue`, `mentioned-only`.
  - `second_coder_confidence` — one of `high`, `medium`, `low`.
  - `second_coder_notes` — free text, may be empty.
  Re-prompt on an invalid value rather than silently accepting it.
- Allow `?` at any prompt to reprint the coding rules (below), `b` to go back one case, and `q` to
  quit and resume later.
- **Autosave after every case** to `revision/data/entity_audit_return_rev1.csv`, and on startup
  resume from the first row with an empty `second_coder_issuer`. I will do this over several
  sittings and must not lose work.
- Show progress as `case n of 80`.
- On completion, print exactly: `All 80 coded. Now run: python3 scripts/rev1_entity_reliability.py
  revision/data/entity_audit_return_rev1.csv` — and stop. Do not run it for me, and do not comment
  on what the numbers might be.

## The coding rules, to print on `?`

These are from `revision/data/entity_audit_INSTRUCTIONS.md`, which you may read.

**Issuer** — the U.S.-listed domestic issuer (a company filing Forms 8-K / 10-K / 10-Q) to which the
incident should be attributed.
- Attribute to the **listed parent** if the named entity is a subsidiary, product or platform of one,
  **but only if the parent controlled it on the incident date**. If control began later, write
  `NONE-not-owned-at-incident-date`.
- If the entity is private, foreign-listed (20-F/6-K), or was not a listed filer on the incident date,
  write `NONE-not-listed`.
- If more than one listed issuer is genuinely implicated, name the one **most responsible for the
  system that produced the harm**, and list the others in notes.
- If no listed issuer is implicated, write `NONE`.

**Role** — `developer` (built the system), `deployer` (ran it in the context that produced the harm),
`both`.

**Attribution basis**
| value | meaning |
|---|---|
| `developer` | the issuer built the model or system |
| `deployer-operator` | the issuer ran it in the context that produced the harm, or made the deployment decision |
| `both` | both of the above |
| `platform-venue` | the issuer hosted third-party content or third-party use; the harm-producing system was not its own deployment decision |
| `mentioned-only` | named, but no development, deployment or venue relationship is evident — including where the issuer is the harmed party, or one of several vendors named in a comparative study |

Hosting third-party content, being a customer of an unrelated vendor, or being named in press
coverage does **not** by itself make an issuer a developer or deployer.

**Confidence** — `high`, `medium`, `low`.

## After the build

Confirm to me in one line that the script runs and resumes correctly on a partially filled file, then
stop. Do not begin coding cases.
