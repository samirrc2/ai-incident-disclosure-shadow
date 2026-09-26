"""consolidate every provisional decision made by the revision run into one file for author
review. One row per decision: file, incident id, field, proposed value, confidence, rationale."""
import csv,json,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
R=[]
def add(src,iid,field,val,conf,why):
    R.append(dict(source_file=src,incident_id=iid,field=field,proposed_value=val,
                  confidence=conf,rationale=why))
# 1. T3a/T3b split
for r in csv.DictReader(open(L.out("t3_split.csv"),newline='',encoding='utf-8',errors='replace')):
    add("data/t3_split.csv",r['incident_id'],"t3_split",r['t3_split'],r['confidence'],
        f"incident families app=[{r['incident_app_families']}] harm=[{r['incident_harm_families']}]; "
        f"filing matched app=[{r['app_family_matched']}] harm=[{r['harm_family_matched']}]")
# 2. attribution basis
for r in csv.DictReader(open(L.out("attribution.csv"),newline='',encoding='utf-8',errors='replace')):
    add("data/attribution.csv",r['incident_id'],"attribution_basis",
        r['attribution_basis'],r['confidence'],r['rationale'])
# 3. crosswalk verdicts
for r in csv.DictReader(open(L.out("crosswalk_review.csv"),newline='',encoding='utf-8',errors='replace')):
    v=r['REVIEW_verdict(OK/FIX)']
    add("data/crosswalk_review.csv",r['incident_id'],"REVIEW_verdict",v,
        "high" if v in ("OK-excluded","FIX") else "medium",r['REVIEW_notes'])
# 4. as-of-date ownership
for r in csv.DictReader(open(L.out("asofdate.csv"),newline='',encoding='utf-8',errors='replace')):
    add("data/asofdate.csv",r['incident_id'],"asof_verdict",r['asof_verdict'],
        "medium" if r['date_status']=="asserted" else "high",
        f"parent control from {r['parent_control_from']} ({r['date_status']}): {r['basis']}")
# 5. T2 adjudication
for r in csv.DictReader(open(L.out("t2_adjudication.csv"),newline='',encoding='utf-8',errors='replace')):
    add("data/t2_adjudication.csv",r['incident_id'],"adjudicated_code",
        r['adjudicated_code'],r['confidence'],r['rationale'])
# 6. one-off editorial and data decisions
add("data/disclosure_coding.csv","350","disclosure_code","T3","high",
    "the coding log (coding/results) records T3 with a written rationale; the analytical CSV carries "
    "T4. Treated as a transcription error in the CSV. Both tiers are inside the shadow, so the "
    "headline is unaffected; Table 1 tier counts shift by one")
add("frontiers/manuscript.tex","-","title","AI Incident Disclosure Shadow: SEC Filing Visibility of "
    "AIID-Recorded AI Incidents at U.S.-Listed Issuers, 2019-2026","medium",
    " selected title; keeps 'Disclosure Shadow', replaces 'Investor Disclosures' with "
    "SEC-filing wording, and signals the AIID-recorded conditional denominator. Two alternatives "
    "are listed in the response letter")
add("frontiers/manuscript.tex","-","generative_ai_statement","expanded to cover revision-stage "
    "recoding proposals produced by an AI system under author review","medium",
    "the authors must confirm this is how they wish to describe the revision workflow "
    "before submission")
add("frontiers/manuscript.tex","-","severity_label","sev_limited / sev_moderate / sev_severe","high",
    "the original severity values T1-limited/T2-moderate/T3-severe collide with the disclosure "
    "codes T1-T4 in the same table; renamed in all derived outputs")
with open(L.res("AUTHOR_REVIEW.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=["source_file","incident_id","field","proposed_value","confidence","rationale"])
    w.writeheader(); w.writerows(R)
c=collections.Counter(r['confidence'] for r in R)
print(f"AUTHOR_REVIEW.csv rows: {len(R)}")
for k in ("high","medium","low"): print(f"   {k}: {c.get(k,0)}")
print("  by source:")
for k,v in collections.Counter(r['source_file'] for r in R).most_common(): print(f"   {v:5d}  {k}")
