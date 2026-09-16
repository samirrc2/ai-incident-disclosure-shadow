# Second-coder entity audit — working kit

This branch contains **only** the 80 incidents to be coded and the rules for coding them. It
deliberately does not contain the study's own issuer mapping, the disclosure codes, or the analysis
code. The audit is blind: its whole value is that the second coder reaches a judgement without
seeing what the study decided.

## Files

| file | what it is |
|---|---|
| `incidents_to_code.csv` | the 80 incidents. Six columns describe each case; five are blank for you to fill |
| `CODING_RULES.md` | how to decide each field. Read this first, in full |
| `CURSOR_PROMPT.md` | paste into Cursor to build a one-case-at-a-time entry tool |

## How to run it

```bash
git clone --branch second-coder-audit --single-branch \
  https://github.com/samirrc2/ai-incident-disclosure-shadow.git audit-kit
cd audit-kit
```

Open **this folder only** in Cursor — not the full repository. Then paste `CURSOR_PROMPT.md` into
Cursor and follow it. It builds an entry tool that shows one incident at a time and saves after every
case, so you can stop and resume.

When all 80 are coded, send back `entity_audit_return_rev1.csv`. Do not run any analysis on it; the
reliability computation happens in the main repository, against the mapping you could not see.

## Three rules that decide whether this is worth anything

1. **Do not look at the study's mapping** before you finish — not in the main repo, not in the Code
   Ocean capsule, not by asking. If you already know how a particular incident was mapped, code it
   anyway on your own reading and say so in the notes.
2. **Do not let an AI decide the cases.** Cursor's role is data entry and validation. If a model
   assigns the issuers, the agreement statistic measures a model re-applying a rule, not two coders
   agreeing, and reporting it as inter-rater reliability would be false.
3. **Do not discuss ambiguous cases with the first coder until you have returned the sheet.**
   Reconciliation happens after the comparison is computed, never before. If you are unsure, record
   `low` confidence and write the doubt in the notes — that uncertainty is itself a finding.
