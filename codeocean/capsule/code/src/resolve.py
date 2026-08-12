#!/usr/bin/env python3
"""resolve — reproduce entity resolution from the frozen extracted AIID incidents.
Reads data/raw_extracted/incidents.csv (+ classifications_CSETv1.csv), resolves deployer/developer
slugs to US-listed issuers via crosswalk, and regenerates the incident-firm map. Asserts
N_matchable (primary domestic-listed) == 307 and that the regenerated primary set matches the
frozen map on (incident_id, matched_company, CIK, listing_status). Deterministic (seed 42).
"""
import sys, csv, json, re, random
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
from crosswalk import CROSSWALK
csv.field_size_limit(10_000_000)
random.seed(C.SEED)

GENERIC=re.compile(r"(developers?|creators?|deployers?|operators?|actors?|scammers?|users?|unknown|"
 r"government|spreaders|manipulation|criminals|launderers|students?|lawyers?|doctors?|hospitals?|"
 r"technology$|technologies$|-technology-|providers?|researchers?|companies|firms|agencies|police|"
 r"department|victims|perpetrators|individuals|people|public$|customers|employees|passengers|"
 r"drivers?|patients?|citizens|community|group$|network$|militar|state$|regime|party|campaign|"
 r"nation|professionals?|professors?|educators?|minors?|boys|girls|teams|sheriff|bureau|forces?|"
 r"enforcement|phishers|hackers|blackmailers|extortionists|sextortionists|universit|schools?|"
 r"unnamed|^none$|channels?|ecosystem|media$)")
RANK={"LISTED":0,"PARENT":1,"DELISTED":2,"FOREIGN":3}

def parse_slugs(s):
    s=(s or "").strip()
    if not s: return []
    try:
        v=json.loads(s); return v if isinstance(v,list) else [v]
    except json.JSONDecodeError:
        return [t.strip() for t in s.strip("[]").replace('"','').split(",") if t.strip()]

def severity(c):
    def num(v):
        try: return float(v)
        except: return 0.0
    if not c: return "UNSCORED"
    if num(c.get("Lives Lost"))>0 or num(c.get("Injuries"))>0 or \
       (c.get("AI Harm Level","") or "").strip()=="AI tangible harm event" or \
       (c.get("Impact on Critical Services","") or "").strip()=="yes":
        return "T3-severe"
    if (c.get("Rights Violation","") or "").strip() in ("yes","maybe") or \
       (c.get("Involving Minor","") or "").strip()=="yes" or \
       "near-miss" in (c.get("Tangible Harm","") or "") or "issue" in (c.get("Tangible Harm","") or ""):
        return "T2-moderate"
    th=(c.get("Tangible Harm","") or "").strip(); hl=(c.get("AI Harm Level","") or "").strip()
    if hl in ("none","AI tangible harm near-miss","AI tangible harm issue","unclear") or th:
        return "T1-limited"
    return "UNSCORED"

def main():
    C.ensure_out()
    inc=list(csv.DictReader(open(C.INCIDENTS)))
    cset={str(r.get("Incident ID","")).strip():r for r in csv.DictReader(open(C.CSET))}
    win=[r for r in inc if r["date"] and "2019-01-01"<=r["date"][:10]<="2026-12-31"]
    matched=[]
    for r in win:
        dep=parse_slugs(r["Alleged deployer of AI system"]); dev=parse_slugs(r["Alleged developer of AI system"])
        best=None
        for s in dict.fromkeys(dep+dev):
            if s in CROSSWALK:
                co,tk,cik,st,conf=CROSSWALK[s]
                if st in RANK:
                    role="both" if (s in dep and s in dev) else ("deployer" if s in dep else "developer")
                    cand=(RANK[st],s,co,tk,cik,st,conf,role)
                    if best is None or cand[0]<best[0]: best=cand
        if best:
            _,slug,co,tk,cik,st,conf,role=best
            matched.append(dict(incident_id=str(r["incident_id"]),incident_date=r["date"][:10],
                entity_slug=slug,matched_company=co,ticker=tk,CIK=cik,listing_status=st,
                match_confidence=conf,role=role,match_method="crosswalk",
                severity_tier=severity(cset.get(str(r["incident_id"]))),title=r.get("title","")))
    fields=["incident_id","incident_date","entity_slug","matched_company","ticker","CIK",
            "listing_status","match_confidence","role","match_method","severity_tier","title"]
    with open(C.MAP_REGEN,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader()
        for m in matched: w.writerow(m)
    prim=[m for m in matched if m["listing_status"] in ("LISTED","PARENT")]
    N=len(prim)
    # assert against frozen map (primary set)
    frozen=[r for r in csv.DictReader(open(C.FROZEN_MAP)) if r["listing_status"] in ("LISTED","PARENT")]
    fz={r["incident_id"]:(r["matched_company"],str(r["CIK"]),r["listing_status"]) for r in frozen}
    rg={m["incident_id"]:(m["matched_company"],str(m["CIK"]),m["listing_status"]) for m in prim}
    fails=[]
    if N!=307: fails.append(f"N_matchable={N} (expected 307)")
    if set(fz)!=set(rg): fails.append(f"incident-id set differs: only-frozen={len(set(fz)-set(rg))}, only-regen={len(set(rg)-set(fz))}")
    mism=[i for i in set(fz)&set(rg) if fz[i]!=rg[i]]
    if mism: fails.append(f"{len(mism)} rows differ on (company,CIK,status), e.g. {mism[:3]}")
    if fails:
        print("RESOLVE: FAIL"); [print("  -",f) for f in fails]; sys.exit(1)
    print(f"RESOLVE: PASS — window {len(win)}; N_matchable (domestic-listed) = {N} "
          f"(+{sum(1 for m in matched if m['listing_status']=='DELISTED')} delisted, "
          f"+{sum(1 for m in matched if m['listing_status']=='FOREIGN')} foreign); "
          f"regenerated primary map matches frozen map exactly.")

if __name__=="__main__": main()
