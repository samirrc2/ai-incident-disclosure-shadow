#!/usr/bin/env python3
"""entity_resolve — resolve AIID incidents (2019-2026) to US-listed involved companies.

Input : data/inbox/aiid_incidents.csv (from parse_aiid)
Method: for each incident, parse deployer+developer slug lists; map via crosswalk.CROSSWALK.
        A slug not in the crosswalk that is NOT a generic-category / individual token is recorded
        as an UNRESOLVED named candidate (surfaced for review, never auto-matched).
Severity (CSET where available, else UNSCORED): T3 if lives_lost>0 or injuries>0 or harm_level ==
        'AI tangible harm event' or critical_services=='yes'; T2 if rights_violation in {yes,maybe}
        or minor=='yes' or a near-miss/issue tangible harm; else T1.
Role  : developer / deployer / both (from which field the matched slug came).
Outputs:
  data/incident_firm_map.csv   — every matched incident (primary + delisted + foreign)
  data/validation_sheet.csv    — ALL flagged rows (MED conf, parent-map, delisted, foreign)
                                     + a seed-42 random sample of HIGH-confidence rows
  prints N_matchable and strata (year, company, role, severity, status).
"""
from __future__ import annotations
import sys, csv, json, re, random
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import INBOX, DATA, SEED
from crosswalk import CROSSWALK
random.seed(SEED)
csv.field_size_limit(10_000_000)

GENERIC=re.compile(r"(developers?|creators?|deployers?|operators?|actors?|scammers?|users?|unknown|"
 r"government|spreaders|manipulation|criminals|launderers|students?|lawyers?|doctors?|hospitals?|"
 r"technology$|technologies$|-technology-|providers?|researchers?|companies|firms|agencies|police|"
 r"department|victims|perpetrators|individuals|people|public$|customers|employees|passengers|"
 r"drivers?|patients?|citizens|community|group$|network$|militar|state$|regime|party|campaign|"
 r"nation|professionals?|professors?|educators?|minors?|boys|girls|teams|sheriff|bureau|forces?|"
 r"enforcement|phishers|hackers|blackmailers|extortionists|sextortionists|universit|schools?|"
 r"unnamed|^none$|channels?|ecosystem|media$)")

RANK={"LISTED":0,"PARENT":1,"DELISTED":2,"FOREIGN":3}

def severity(r):
    def num(v):
        try: return float(v)
        except: return 0.0
    if num(r["cset_lives_lost"])>0 or num(r["cset_injuries"])>0 or \
       r["cset_harm_level"]=="AI tangible harm event" or r["cset_critical_services"]=="yes":
        return "T3-severe"
    if r["cset_rights_violation"] in ("yes","maybe") or r["cset_minor"]=="yes" or \
       "near-miss" in r["cset_tangible_harm"] or "issue" in r["cset_tangible_harm"]:
        return "T2-moderate"
    if r["cset_harm_level"] in ("none","AI tangible harm near-miss","AI tangible harm issue","unclear") \
       or r["cset_tangible_harm"]:
        return "T1-limited"
    return "UNSCORED"

def main():
    src=INBOX/"aiid_incidents.csv"
    if not src.exists(): sys.exit("run parse_aiid first")
    rows=list(csv.DictReader(open(src)))
    win=[r for r in rows if r["date"] and "2019-01-01"<=r["date"]<="2026-12-31"]
    matched=[]; unresolved=Counter()
    for r in rows if False else win:
        dep=json.loads(r["deployers"] or "[]"); dev=json.loads(r["developers"] or "[]")
        best=None
        for s in dict.fromkeys(dep+dev):
            if s in CROSSWALK:
                co,tk,cik,st,conf=CROSSWALK[s]
                if st in RANK:
                    role="both" if (s in dep and s in dev) else ("deployer" if s in dep else "developer")
                    cand=(RANK[st],s,co,tk,cik,st,conf,role)
                    if best is None or cand[0]<best[0]: best=cand
            elif not GENERIC.search(s):
                unresolved[s]+=1
        if best:
            _,slug,co,tk,cik,st,conf,role=best
            matched.append(dict(incident_id=r["incident_id"],incident_date=r["date"],
                entity_slug=slug,matched_company=co,ticker=tk,CIK=cik,listing_status=st,
                match_confidence=conf,role=role,match_method="crosswalk",severity_tier=severity(r),
                title=r["title"]))
    fields=["incident_id","incident_date","entity_slug","matched_company","ticker","CIK",
            "listing_status","match_confidence","role","match_method","severity_tier","title"]
    with open(DATA/"incident_firm_map.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader()
        for m in matched: w.writerow(m)

    prim=[m for m in matched if m["listing_status"] in ("LISTED","PARENT")]
    delisted=[m for m in matched if m["listing_status"]=="DELISTED"]
    foreign=[m for m in matched if m["listing_status"]=="FOREIGN"]
    print(f"window incidents 2019-2026: {len(win)}")
    print(f"N_matchable (domestic-listed LISTED/PARENT): {len(prim)}")
    print(f"  + delisted-was-listed: {len(delisted)} | + foreign US-listed (20-F/6-K): {len(foreign)}")
    print(f"  TOTAL any-US-listed match: {len(matched)}")
    print("by year:", dict(sorted(Counter(m['incident_date'][:4] for m in prim).items())))
    print("by role:", dict(Counter(m['role'] for m in prim)))
    print("by severity:", dict(Counter(m['severity_tier'] for m in prim)))
    print("top companies:", Counter(m['matched_company'] for m in prim).most_common(12))

    # validation sheet: ALL flagged (MED / parent / delisted / foreign) + seed-42 sample of HIGH
    flagged=[m for m in matched if m["match_confidence"]=="MED" or m["listing_status"] in ("DELISTED","FOREIGN")]
    high=[m for m in matched if m not in flagged]
    sample=random.sample(high,min(40,len(high)))
    review=sorted(flagged+sample,key=lambda m:(m["incident_date"]))
    vf=fields+["FLAG","REVIEW_verdict(OK/FIX)","REVIEW_notes"]
    with open(DATA/"validation_sheet.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=vf,extrasaction="ignore"); w.writeheader()
        for m in review:
            m=dict(m)
            m["FLAG"]=("parent-map" if m["match_method"]=="crosswalk" and m["match_confidence"]=="MED" and m["listing_status"]=="PARENT"
                       else m["listing_status"] if m["listing_status"] in ("DELISTED","FOREIGN")
                       else "MED-listed" if m["match_confidence"]=="MED" else "sample")
            m["REVIEW_verdict(OK/FIX)"]=""; m["REVIEW_notes"]=""; w.writerow(m)
    print(f"\nvalidation sheet rows: {len(review)} (flagged {len(flagged)} + sample {len(sample)})")
    # unresolved named candidates (for completeness review)
    with open(DATA/"unresolved_named_slugs.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["slug","incident_count"])
        for s,c in unresolved.most_common():
            if c>=2: w.writerow([s,c])
    print(f"unresolved named-entity slugs (freq>=2) written for completeness review")

if __name__=="__main__": main()
