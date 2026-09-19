"""Record the word that triggered every application/harm family match.

The T3a/T3b split is driven by pattern matching, so a pattern that fires inside an unrelated
word silently changes the result. "fee" once matched "Feed", "llm" matched "fulfillment".
Those are invisible in the output CSV, which records only the family name.

This writes results/family_triggers.csv - one row per incident, side, family - naming the
pattern and the surface word it matched, so the classification can be read and checked
rather than trusted. verify_all.py fails if a trigger looks like an inside-word match that
has not been reviewed.
"""
import csv, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths as L, taxonomy as T

E, B = L.evidence(), L.descriptions()
rows = []
for r in csv.DictReader(open(L.out("t3_split.csv"), newline="", encoding="utf-8", errors="replace")):
    iid = r["incident_id"]
    for side, txt in (("filing", T.affirmative((E.get(iid, {}) or {}).get("evidence", "") or "")),
                      ("incident", str(B.get(iid, "") or ""))):
        for kind, D in (("app", T.APP_FAMILIES), ("harm", T.HARM_FAMILIES)):
            for fam, pats in D.items():
                for p in pats:
                    m = re.search(p, txt, re.I)
                    if not m:
                        continue
                    w = re.search(r"\w*" + p + r"\w*", txt[max(0, m.start() - 30):], re.I)
                    rows.append(dict(incident_id=iid, side=side, kind=kind, family=fam,
                                     pattern=p, matched_word=(w.group(0) if w else m.group(0))[:40]))
                    break
with open(L.res("family_triggers.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=["incident_id", "side", "kind", "family", "pattern", "matched_word"])
    wr.writeheader(); wr.writerows(rows)
print(f"wrote results/family_triggers.csv  ({len(rows)} family matches)")
