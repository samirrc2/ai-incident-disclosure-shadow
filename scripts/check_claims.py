#!/usr/bin/env python3
"""check_claims — independently recompute every number destined for the manuscript from the raw
coded table and assert it matches pilot/results.json. Also verifies internal consistency.
Exit 0 on success. Run twice + diff results.json for the byte-identical reproducibility gate.
"""
import csv, json, math, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import PILOT, DATA

def wilson(k,n,z=1.96):
    if n==0: return (0.0,0.0,0.0)
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return (p,(c-h)/d,(c+h)/d)

def main():
    rows=list(csv.DictReader(open(DATA/"disclosure_coding.csv")))
    R=json.load(open(PILOT/"results.json"))
    fails=[]
    def chk(name,a,b,tol=1e-9):
        ok=abs(a-b)<=tol if isinstance(a,(int,float)) else a==b
        if not ok: fails.append(f"{name}: recomputed {a} != stored {b}")

    N=len(rows); chk("N",N,R["N"])
    dist=Counter(r["disclosure_code"] for r in rows)
    for t in ["T1","T2","T3","T4"]:
        chk(f"dist.{t}",dist.get(t,0),R["distribution"][t])
    chk("sum==N",sum(dist.values()),N)

    # headline rates recomputed
    def rate(pred):
        k=sum(1 for r in rows if pred(r)); return k,*wilson(k,N)
    for key,pred in [("T1_specific",lambda r:r["disclosure_code"]=="T1"),
                     ("T1T2_substantive",lambda r:r["disclosure_code"] in ("T1","T2")),
                     ("T3_generic_only",lambda r:r["disclosure_code"]=="T3"),
                     ("T4_no_disclosure",lambda r:r["disclosure_code"]=="T4"),
                     ("shadow_T3plusT4",lambda r:r["disclosure_code"] in ("T3","T4"))]:
        k,p,lo,hi=rate(pred); b=R["headline"][key]
        chk(f"{key}.k",k,b["k"]); chk(f"{key}.rate",round(p,4),b["rate"])
        chk(f"{key}.ci_lo",round(lo,4),b["ci95"][0]); chk(f"{key}.ci_hi",round(hi,4),b["ci95"][1])

    # accounting channel counts
    t1t2=[r for r in rows if r["disclosure_code"] in ("T1","T2")]
    chk("T1T2_total",len(t1t2),R["booked_impact_among_disclosed"]["T1T2_total"])
    booked=sum(1 for r in t1t2 if str(r["accounting_booked_impact"]).strip().lower().startswith("yes"))
    chk("booked",booked,R["booked_impact_among_disclosed"]["with_booked_impact"])

    # internal sanity: CI brackets point estimate; rates in [0,1]; strata sum to N
    for key,b in R["headline"].items():
        if not (b["ci95"][0]<=b["rate"]<=b["ci95"][1]): fails.append(f"CI brackets {key}")
    chk("severity strata sum",sum(v["n"] for v in R["by_severity"].values()),N)
    chk("year strata sum",sum(v["n"] for v in R["by_year"].values()),N)
    chk("role strata sum",sum(v["n"] for v in R["by_role"].values()),N)

    if fails:
        print("CHECK_CLAIMS: FAIL"); [print("  -",f) for f in fails]; sys.exit(1)
    print(f"CHECK_CLAIMS: PASS — {N} incidents; T1-T4=({dist['T1']},{dist['T2']},{dist['T3']},{dist['T4']}); "
          f"all headline rates, CIs, strata sums, and accounting counts verified against results.json.")

if __name__=="__main__": main()
