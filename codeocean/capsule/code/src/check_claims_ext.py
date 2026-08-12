#!/usr/bin/env python3
"""check_claims_ext — independently re-derive the extended (revision) numbers from the coded table
and assert they match extended.json / reliability_ext.json. Exit 0 on success.
"""
import csv, json, math, glob
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
csv.field_size_limit(10_000_000)
REV=C.RESULTS
rows=list(csv.DictReader(open(C.CODED)))
E=json.load(open(C.EXT_JSON)); RL=json.load(open(C.REL_JSON))
N=len(rows); fails=[]
def chk(name,a,b,tol=1e-6):
    ok=(abs(a-b)<=tol) if isinstance(a,(int,float)) and isinstance(b,(int,float)) else a==b
    if not ok: fails.append(f"{name}: {a} != {b}")

# concentration
byi=Counter(r["matched_company"] for r in rows)
HHI=sum((n/N)**2 for n in byi.values())
chk("N",N,E["N"]); chk("HHI",round(HHI,4),E["concentration"]["HHI"])
chk("n_issuers",len(byi),E["concentration"]["n_issuers"])
# drop-top-k shadow
def shadow(rs):
    return sum(1 for r in rs if r["disclosure_code"] in ("T3","T4"))/len(rs) if rs else 0
top2=set(c for c,_ in byi.most_common(2)); top5=set(c for c,_ in byi.most_common(5))
chk("drop_top2_shadow",round(shadow([r for r in rows if r['matched_company'] not in top2]),4),
    E["robustness_concentration"]["drop_top2"]["shadow"])
chk("drop_top5_shadow",round(shadow([r for r in rows if r['matched_company'] not in top5]),4),
    E["robustness_concentration"]["drop_top5"]["shadow"])
# issuer-level substantive
subst_iss=sum(1 for iss in byi if any(r["disclosure_code"] in ("T1","T2") for r in rows if r["matched_company"]==iss))
chk("issuers_with_substantive",subst_iss,E["issuer_level"]["n_issuers_with_substantive"])
# category substantive total == 7
cat_subst=sum(v["substantive"] for v in E["by_category"].values())
chk("category_substantive_total",cat_subst,sum(1 for r in rows if r["disclosure_code"] in ("T1","T2")))
# retrieval validation: recount from agent outputs
fn=ftot=0
for f in ["retrieval_A.json","retrieval_B.json"]:
    p=C.LOGS/f
    if p.exists():
        for v in json.load(open(p)).values():
            ftot+=1
            if str(v.get("audit_verdict","")).upper().startswith("REVISE"): fn+=1
chk("retrieval_audited",ftot,E["retrieval_validation"]["audited"])
chk("retrieval_false_neg",fn,E["retrieval_validation"]["false_negatives_found"])
# reliability recompute
p1={r["incident_id"]:r["disclosure_code"] for r in rows}
p2={}
for f in glob.glob(str(str(C.PASS2/"results_*.json"))):
    for k,v in json.load(open(f)).items():
        if isinstance(v,dict) and "code" in v: p2[str(k)]=v["code"]
pairs=[(p1[i],p2[i]) for i in p2 if i in p1]; n=len(pairs)
po=sum(1 for a,b in pairs if a==b)/n
chk("pass2_n",n,RL["pass2_n"]); chk("observed_agreement",round(po,3),RL["observed_agreement"])
chk("PABAK",round(2*po-1,3),RL["PABAK"])

if fails:
    print("CHECK_CLAIMS_EXT: FAIL"); [print("  -",f) for f in fails]; sys.exit(1)
print(f"CHECK_CLAIMS_EXT: PASS — HHI={round(HHI,4)}, drop-top2/5 shadow="
      f"{E['robustness_concentration']['drop_top2']['shadow']}/{E['robustness_concentration']['drop_top5']['shadow']}, "
      f"{subst_iss}/21 issuers substantive, retrieval {fn}/{ftot} false-neg, kappa n={n}. All verified.")
