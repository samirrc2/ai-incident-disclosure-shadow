# Paste this into Cursor

Open **this folder only** (`audit-kit`) in Cursor — not the full repository. Then paste everything
below the line.

---

You are building a small local data-entry harness for a blind inter-rater coding exercise. You are
**not** doing the coding. I am. Your output is a tool; my output is 80 judgements.

## Hard constraints

1. **Never propose, rank, guess or pre-fill an issuer, role or attribution basis** — not even as a
   "suggestion to confirm", not even if I ask. If I ask, refuse and remind me that the resulting
   statistic is only meaningful if the judgements are mine.
2. **Do not answer substantive questions about a case while I am coding it.** Not "who owns this
   company", not "is this a deployer", not "what does this product do". If I am unsure, I record
   `low` confidence and write the doubt in the notes field. That uncertainty is data.
3. **Do not fetch anything from the network**, and do not look for the parent repository, other
   branches, or any file outside this folder. This folder is deliberately missing the study's own
   mapping; finding it would invalidate the exercise.
4. Do not edit `incidents_to_code.csv`. Write only to `entity_audit_return_rev1.csv`.

## Build `code_incidents.py`, run as `python3 code_incidents.py`

**Input** — `incidents_to_code.csv`, 80 rows, columns:
`incident_id, incident_date, aiid_title, aiid_summary, organizations_named_in_aiid`,
then five empty columns:
`second_coder_issuer, second_coder_role, second_coder_attribution_basis,
second_coder_confidence, second_coder_notes`.

**Behaviour**

- Present **one incident at a time**, clearing the screen between cases. Display only: `case n of 80`,
  the incident id, the date, the title, the summary, and the organizations named in the AIID record.
  Wrap the summary to the terminal width so it is readable.
- Prompt for the five fields in order, validating each and re-prompting on an invalid value:
  - `second_coder_issuer` — free text. Also accept exactly: `NONE`, `NONE-not-listed`,
    `NONE-not-owned-at-incident-date`.
  - `second_coder_role` — one of `developer`, `deployer`, `both`.
  - `second_coder_attribution_basis` — one of `developer`, `deployer-operator`, `both`,
    `platform-venue`, `mentioned-only`.
  - `second_coder_confidence` — one of `high`, `medium`, `low`.
  - `second_coder_notes` — free text, may be empty.
- Accept these at any prompt: `?` reprints the coding rules from `CODING_RULES.md`; `b` steps back
  one case and lets me re-enter it; `q` saves and exits.
- **Autosave the whole sheet after every completed case** to `entity_audit_return_rev1.csv`, and on
  startup resume at the first row whose `second_coder_issuer` is empty. I will do this across several
  sittings and must not lose work.
- Keep a running count of how many cases are left, and on `q` print it.
- When all 80 are done, print exactly this and stop:
  `All 80 coded. Send entity_audit_return_rev1.csv back to the first coder.`
  Do not analyse the file, do not summarise my answers, and do not comment on what the agreement
  might be.

## The rules to print on `?`

Read them from `CODING_RULES.md` in this folder and print them verbatim. Do not paraphrase or
summarise them, and do not add examples of your own.

## When the tool is built

Test that it resumes correctly from a partially filled `entity_audit_return_rev1.csv`, delete any
test rows you created, confirm in one line that it works, and stop. **Do not start coding cases.**
