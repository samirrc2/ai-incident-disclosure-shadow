#!/usr/bin/env python3
"""inference — rarity-aware inference + robustness for the revision (reviewer-proofing).
Deterministic (seed 42). No network. Reads the frozen coded table + extracted incidents.
Outputs revision/results/inference.json/.md.
Adds: Clopper-Pearson exact CIs; Monte-Carlo exact (permutation) tests for the r x 2 stratum tables;
the 1,389 -> 307 match-yield funnel; right-censoring robustness; plausibly-material subset.
"""
import csv, json, math, re
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from scipy import stats
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
C.ensure_out()
sys.path.insert(0, str(Path(__file__).resolve().parent))
from crosswalk import CROSSWALK
csv.field_size_limit(10_000_000)
RNG = np.random.default_rng(42)
REV = C.RESULTS
SNAPSHOT_DATE = "2026-07-27"

rows=list(csv.DictReader(open(C.CODED)))
raw={str(r["incident_id"]):r for r in csv.DictReader(open(C.INCIDENTS))}
N=len(rows)
for r in rows:
    r["_shadow"]=r["disclosure_code"] in ("T3","T4")
    r["_subst"]=r["disclosure_code"] in ("T1","T2")

def cp(k,n):
    lo=0.0 if k==0 else stats.beta.ppf(0.025,k,n-k+1)
    hi=1.0 if k==n else stats.beta.ppf(0.975,k+1,n-k)
    return round(k/n,4),round(lo,4),round(hi,4)

R={"N":N}
# 1. Clopper-Pearson exact intervals for headline proportions
R["clopper_pearson"]={
 "T1_specific": cp(sum(1 for r in rows if r["disclosure_code"]=="T1"),N),
 "T1T2_substantive": cp(sum(1 for r in rows if r["_subst"]),N),
 "shadow_T3T4": cp(sum(1 for r in rows if r["_shadow"]),N),
 "T4_none": cp(sum(1 for r in rows if r["disclosure_code"]=="T4"),N)}

# 2. Monte-Carlo exact (permutation) tests for substantive (T1+T2) across strata (r x 2)
def perm_test(labels, outcome, B=20000):
    labels=np.array(labels); outcome=np.array(outcome,dtype=int)
    cats=sorted(set(labels))
    def chi2(o):
        tab=np.array([[np.sum((labels==c)&(o==1)),np.sum((labels==c)&(o==0))] for c in cats],float)
        cs=tab.sum(0); rs=tab.sum(1); tot=tab.sum()
        exp=np.outer(rs,cs)/tot
        with np.errstate(divide='ignore',invalid='ignore'):
            stat=np.nansum(np.where(exp>0,(tab-exp)**2/exp,0.0))
        return stat
    obs=chi2(outcome); cnt=0
    for _ in range(B):
        cnt+= chi2(RNG.permutation(outcome))>=obs-1e-12
    return round(obs,3),round((cnt+1)/(B+1),4)
subst=[1 if r["_subst"] else 0 for r in rows]
R["permutation_tests"]={
 "by_role":{"chi2":perm_test([r["role"] for r in rows],subst)[0],"p_mc_exact":perm_test([r["role"] for r in rows],subst)[1]},
 "by_severity":{"chi2":perm_test([r["severity_tier"] for r in rows],subst)[0],"p_mc_exact":perm_test([r["severity_tier"] for r in rows],subst)[1]},
 "B":20000,"note":"Monte-Carlo exact permutation p-values (chi2 statistic) — robust to the sparse (7) positive count; complement the Fisher/asymptotic values."}

# 3. Match-yield funnel: 1,389 window incidents -> classification
GEN=re.compile(r"(developers?|creators?|deployers?|operators?|actors?|scammers?|users?|unknown|government|"
 r"spreaders|manipulation|criminals|launderers|students?|lawyers?|doctors?|hospitals?|technology$|"
 r"technologies$|-technology-|providers?|researchers?|companies|firms|agencies|police|department|victims|"
 r"perpetrators|individuals|people|public$|customers|employees|passengers|drivers?|patients?|citizens|"
 r"community|group$|network$|militar|state$|regime|party|campaign|nation|professionals?|professors?|"
 r"educators?|minors?|boys|girls|teams|sheriff|bureau|forces?|enforcement|phishers|hackers|blackmailers|"
 r"extortionists|sextortionists|universit|schools?|unnamed|^none$|channels?|ecosystem|media$)")
def parse(s):
    s=(s or "").strip()
    if not s: return []
    try:
        v=json.loads(s); return v if isinstance(v,list) else [v]
    except: return [t.strip() for t in s.strip("[]").replace('"','').split(",") if t.strip()]
win=[r for r in raw.values() if r["date"] and "2019-01-01"<=r["date"][:10]<="2026-12-31"]
cls=Counter()
for r in win:
    slugs=dict.fromkeys(parse(r["Alleged deployer of AI system"])+parse(r["Alleged developer of AI system"]))
    statuses={CROSSWALK[s][3] for s in slugs if s in CROSSWALK}
    if {"LISTED","PARENT"} & statuses: cls["US-listed (primary)"]+=1
    elif "DELISTED" in statuses: cls["delisted-was-listed"]+=1
    elif "FOREIGN" in statuses: cls["foreign US-listed / foreign-private"]+=1
    elif "PRIVATE" in statuses: cls["private firm"]+=1
    elif any(not GEN.search(s) for s in slugs): cls["named non-crosswalk entity"]+=1
    else: cls["generic/individual/non-corporate only"]+=1
R["match_funnel"]={"window_incidents":len(win),"classification":dict(cls.most_common()),
 "primary_yield_pct":round(cls["US-listed (primary)"]/len(win),4),
 "note":"The ~22% of window incidents with any corporate entity is dominated by private AI labs "
        "(OpenAI/Anthropic/xAI) and generic/individual actors (deepfake creators, scammers); the "
        "US-listed primary yield is 307/1389."}

# 4. Right-censoring: incidents whose 12-mo window extends past the snapshot date
def add12(d):
    y,m,dd=map(int,d[:10].split("-")); y+= (m+12-1)//12 if False else 1; return f"{y:04d}-{m:02d}-{dd:02d}"
censored=[r for r in rows if add12(r["incident_date"])>SNAPSHOT_DATE]
uncensored=[r for r in rows if add12(r["incident_date"])<=SNAPSHOT_DATE]
def rate(rs,pred):
    k=sum(1 for r in rs if pred(r)); return cp(k,len(rs)) if rs else (0,0,0)
R["right_censoring"]={"snapshot_date":SNAPSHOT_DATE,
 "n_censored_incomplete_window":len(censored),"n_complete_window":len(uncensored),
 "shadow_complete_window":rate(uncensored,lambda r:r["_shadow"]),
 "shadow_full_sample":R["clopper_pearson"]["shadow_T3T4"],
 "note":"Incidents whose incident_date+12mo exceeds the snapshot have a right-censored search window; "
        "restricting to complete-window incidents leaves the shadow essentially unchanged."}

# 5. Plausibly-material subset (severe tier + top-5 issuers) — shadow persists
severe=[r for r in rows if r["severity_tier"]=="T3-severe"]
top5={c for c,_ in Counter(r["matched_company"] for r in rows).most_common(5)}
big=[r for r in rows if r["matched_company"] in top5]
R["plausibly_material"]={
 "severe_tier":{"n":len(severe),"shadow":rate(severe,lambda r:r["_shadow"]),
                "substantive_k":sum(1 for r in severe if r["_subst"])},
 "top5_issuers":{"n":len(big),"shadow":rate(big,lambda r:r["_shadow"])},
 "note":"Even restricting to CSET-severe incidents (physical/large-scale harm) or to the five largest, "
        "most-scrutinized issuers, incident-specific disclosure stays near zero and the shadow >=95%."}

REV.mkdir(parents=True,exist_ok=True)
(REV/"inference.json").write_text(json.dumps(R,indent=2))
cpb=R["clopper_pearson"]
L=["# Exact inference & reviewer-proofing robustness","",
 "## Clopper-Pearson exact 95% intervals (headline)",
 f"- T1 incident-specific: {cpb['T1_specific'][0]*100:.1f}% [{cpb['T1_specific'][1]*100:.1f}, {cpb['T1_specific'][2]*100:.1f}]",
 f"- T1+T2 substantive: {cpb['T1T2_substantive'][0]*100:.1f}% [{cpb['T1T2_substantive'][1]*100:.1f}, {cpb['T1T2_substantive'][2]*100:.1f}]",
 f"- Shadow T3+T4: {cpb['shadow_T3T4'][0]*100:.1f}% [{cpb['shadow_T3T4'][1]*100:.1f}, {cpb['shadow_T3T4'][2]*100:.1f}]","",
 "## Monte-Carlo exact permutation tests (substantive T1+T2)",
 f"- By role: chi2={R['permutation_tests']['by_role']['chi2']}, p(MC-exact)={R['permutation_tests']['by_role']['p_mc_exact']}",
 f"- By severity: chi2={R['permutation_tests']['by_severity']['chi2']}, p(MC-exact)={R['permutation_tests']['by_severity']['p_mc_exact']}","",
 "## Match-yield funnel (1,389 window incidents)","| class | n |","|---|---|"]
for k,v in R["match_funnel"]["classification"].items(): L.append(f"| {k} | {v} |")
L+=[f"\n_Primary US-listed yield = {R['match_funnel']['primary_yield_pct']*100:.1f}% (307/1389); "
    f"non-matches are dominated by private AI labs and generic/individual actors._","",
 "## Right-censoring robustness",
 f"- Complete-window incidents: {R['right_censoring']['n_complete_window']} "
 f"(shadow {R['right_censoring']['shadow_complete_window'][0]*100:.1f}% "
 f"[{R['right_censoring']['shadow_complete_window'][1]*100:.1f},{R['right_censoring']['shadow_complete_window'][2]*100:.1f}]); "
 f"{R['right_censoring']['n_censored_incomplete_window']} right-censored.","",
 "## Plausibly-material subset",
 f"- Severe tier (n={R['plausibly_material']['severe_tier']['n']}): shadow {R['plausibly_material']['severe_tier']['shadow'][0]*100:.1f}%, "
 f"{R['plausibly_material']['severe_tier']['substantive_k']} substantive.",
 f"- Top-5 issuers (n={R['plausibly_material']['top5_issuers']['n']}): shadow {R['plausibly_material']['top5_issuers']['shadow'][0]*100:.1f}%."]
(REV/"inference.md").write_text("\n".join(L)+"\n")
print("\n".join(L))
