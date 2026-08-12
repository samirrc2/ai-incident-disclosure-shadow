#!/usr/bin/env python3
"""rebuild_coded_table — integrity chain. Reconstruct each incident's disclosure code from the
shipped pass-1 coding logs (data/coding_logs/pass1/*.json) plus the documented corrections
(CORRECTIONS.json), and assert it equals the frozen coded table's disclosure_code for all 307
incidents. This proves the analysis input (the labels) is a deterministic function of the shipped
logs, not an unexplained artifact. Free-text evidence/rationale are carried in the frozen table as
provenance and are not reconstructed here. Writes results/coding_chain.csv.
"""
import sys, csv, json, glob
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
csv.field_size_limit(10_000_000)

def main():
    C.ensure_out()
    codes={}
    for f in sorted(C.LOGS.glob("pass1/*.json")):
        for k,v in json.load(open(f)).items():
            if not str(k).startswith("_") and isinstance(v,dict) and "code" in v:
                codes[str(k)]=v["code"]
    corr=json.load(open(C.LOGS/"CORRECTIONS.json"))
    for iid,ov in corr.get("code_overrides",{}).items():
        codes[str(iid)]=ov["to"]
    frozen=list(csv.DictReader(open(C.CODED)))
    fz={r["incident_id"]:r["disclosure_code"] for r in frozen}
    rows=[]; fails=[]
    for iid,fc in fz.items():
        rc=codes.get(iid,"<absent-in-logs>")
        rows.append((iid,rc,fc,"OK" if rc==fc else "MISMATCH"))
        if rc!=fc: fails.append(f"{iid}: logs+corrections={rc} vs frozen={fc}")
    with open(C.RESULTS/"coding_chain.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["incident_id","code_from_logs","code_frozen","status"]); w.writerows(rows)
    if fails:
        print(f"REBUILD_CHAIN: FAIL ({len(fails)} mismatches)"); [print("  -",x) for x in fails[:10]]; sys.exit(1)
    from collections import Counter
    dist=Counter(fz.values())
    print(f"REBUILD_CHAIN: PASS — all {len(fz)} disclosure codes reproduced from shipped logs "
          f"+ {len(corr.get('code_overrides',{}))} documented override(s). "
          f"Distribution T1/T2/T3/T4 = {dist['T1']}/{dist['T2']}/{dist['T3']}/{dist['T4']}.")

if __name__=="__main__": main()
