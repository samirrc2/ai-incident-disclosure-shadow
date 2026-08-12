#!/usr/bin/env python3
"""analysis — compute all manuscript numbers from the coded table. Deterministic; no network.
Input : data/disclosure_coding.csv (307 primary domestic-listed incidents, T1-T4 coded)
Output: pilot/results.json  (machine-readable, consumed by check_claims.py and the manuscript)
        pilot/results.md    (human-readable results)
"""
from __future__ import annotations
import csv, json, math
from collections import Counter, defaultdict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import PILOT, DATA

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0, 0.0)
    p = k/n
    d = 1 + z*z/n
    c = p + z*z/(2*n)
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return (p, (c-h)/d, (c+h)/d)

def rate_block(rows, pred):
    n=len(rows); k=sum(1 for r in rows if pred(r))
    p,lo,hi=wilson(k,n)
    return {"k":k,"n":n,"rate":round(p,4),"ci95":[round(lo,4),round(hi,4)]}

def main():
    rows=list(csv.DictReader(open(DATA/"disclosure_coding.csv")))
    N=len(rows)
    code=lambda r:r["disclosure_code"]
    T1=lambda r:code(r)=="T1"; T2=lambda r:code(r)=="T2"; T3=lambda r:code(r)=="T3"; T4=lambda r:code(r)=="T4"
    specific=T1
    substantive=lambda r:code(r) in ("T1","T2")            # names or legally records the event
    shadow_strict=lambda r:code(r) in ("T3","T4")          # no substantive disclosure of the event
    no_disc=T4                                             # nothing located at all

    R={}
    R["N"]=N
    R["distribution"]={t:sum(1 for r in rows if code(r)==t) for t in ["T1","T2","T3","T4"]}
    R["headline"]={
        "T1_specific": rate_block(rows,specific),
        "T1T2_substantive": rate_block(rows,substantive),
        "T3_generic_only": rate_block(rows,T3),
        "T4_no_disclosure": rate_block(rows,no_disc),
        "shadow_T3plusT4": rate_block(rows,shadow_strict),
    }
    # strata
    def strat(keyfn,label):
        out={}
        groups=defaultdict(list)
        for r in rows: groups[keyfn(r)].append(r)
        for g,rs in sorted(groups.items()):
            out[str(g)]={"n":len(rs),
                "T1":rate_block(rs,specific),"T1T2":rate_block(rs,substantive),
                "shadow_T3T4":rate_block(rs,shadow_strict),"T4":rate_block(rs,no_disc),
                "dist":{t:sum(1 for r in rs if code(r)==t) for t in ["T1","T2","T3","T4"]}}
        return out
    R["by_severity"]=strat(lambda r:r["severity_tier"],"severity")
    R["by_year"]=strat(lambda r:r["incident_date"][:4],"year")
    R["by_role"]=strat(lambda r:r["role"],"role")
    R["by_company"]={c:{"n":n} for c,n in Counter(r["matched_company"] for r in rows).most_common()}

    # accounting channel table (T1/T2 only)
    R["accounting_channel"]=[{
        "incident_id":r["incident_id"],"company":r["matched_company"],"code":r["disclosure_code"],
        "filing_item":r["accounting_filing_item"],"booked_impact":r["accounting_booked_impact"],
        "title":r["title"][:70]} for r in rows if r["disclosure_code"] in ("T1","T2")]
    R["booked_impact_among_disclosed"]={
        "T1T2_total":sum(1 for r in rows if r["disclosure_code"] in ("T1","T2")),
        "with_booked_impact":sum(1 for r in rows if r["disclosure_code"] in ("T1","T2")
                                 and str(r["accounting_booked_impact"]).strip().lower().startswith("yes"))}

    # robustness
    rob={}
    rob["b_exclude_pre2021"]={"filter":"incident_date>=2021-01-01",
        **rate_block([r for r in rows if r["incident_date"]>="2021-01-01"],shadow_strict)}
    rob["c_exclude_parent_only"]={"filter":"listing_status==LISTED (drop PARENT subsidiary maps)",
        **rate_block([r for r in rows if r["listing_status"]=="LISTED"],shadow_strict)}
    rob["c_parent_only_subset"]={"filter":"listing_status==PARENT",
        **rate_block([r for r in rows if r["listing_status"]=="PARENT"],shadow_strict)}
    rob["full_sample_shadow"]=rate_block(rows,shadow_strict)
    R["robustness"]=rob
    R["robustness_note"]=("Window-length sensitivity (6/12/24 mo) and coder-1-vs-resolved are computed "
        "on the reliability subsample in extended (kappa) once pass-2 raw-filing coding completes; "
        "primary coding uses the pre-registered 12-month window.")

    # cyber benchmark (Debevoise, disclosure-under-mandate; see recon recon.md section 6)
    R["cyber_benchmark"]={"regime_start":"2023-12-18","as_of":"2026-05-21",
        "item_1_05_material_issuers":29,"item_8_01_voluntary_issuers":50,"both":5,
        "total_filings":79,"total_issuers":74,
        "framing":"disclosure-under-mandate (count of filings under a legal duty); NOT a cyber shadow rate"}

    (PILOT/"results.json").write_text(json.dumps(R,indent=2))
    # markdown
    h=R["headline"]
    def pct(b): return f"{100*b['k']/b['n']:.1f}% [{b['ci95'][0]*100:.1f}, {b['ci95'][1]*100:.1f}]"
    L=[f"# Results (N={N} US-listed-matched AI incidents, 2019–2026)","",
       "## Four-tier disclosure distribution",
       "| Tier | meaning | n | share |","|---|---|---|---|",
       f"| T1 | disclosed-specific | {R['distribution']['T1']} | {pct(h['T1_specific'])} |",
       f"| T2 | legal-proceedings-only | {R['distribution']['T2']} | {100*rate_block(rows,T2)['k']/rate_block(rows,T2)['n']:.1f}% |",
       f"| T3 | generic-risk-language | {R['distribution']['T3']} | {pct(h['T3_generic_only'])} |",
       f"| T4 | no disclosure located | {R['distribution']['T4']} | {pct(h['T4_no_disclosure'])} |","",
       f"**Incident-specific disclosure (T1): {pct(h['T1_specific'])}.** "
       f"Substantive disclosure naming/recording the event (T1+T2): {pct(h['T1T2_substantive'])}. "
       f"**Shadow (T3+T4, event never named): {pct(h['shadow_T3plusT4'])}.**","",
       "## By severity tier","| tier | n | T1 specific | T1+T2 | shadow T3+T4 |","|---|---|---|---|---|"]
    for g,b in R["by_severity"].items():
        L.append(f"| {g} | {b['n']} | {100*b['T1']['k']/b['n']:.1f}% | {100*b['T1T2']['k']/b['n']:.1f}% | {100*b['shadow_T3T4']['k']/b['n']:.1f}% |")
    L+=["","## By year","| year | n | T1 | shadow T3+T4 |","|---|---|---|---|"]
    for g,b in R["by_year"].items():
        L.append(f"| {g} | {b['n']} | {b['T1']['k']} | {b['shadow_T3T4']['rate']*100:.1f}% |")
    L+=["","## By role","| role | n | T1 | shadow T3+T4 |","|---|---|---|---|"]
    for g,b in R["by_role"].items():
        L.append(f"| {g} | {b['n']} | {b['T1']['k']} | {b['shadow_T3T4']['rate']*100:.1f}% |")
    L+=["","## Accounting channel (all T1/T2 incidents)",
        f"Of {R['booked_impact_among_disclosed']['T1T2_total']} substantively-disclosed incidents, "
        f"{R['booked_impact_among_disclosed']['with_booked_impact']} carried a booked financial-statement impact.","",
        "| id | company | code | filing item | booked |","|---|---|---|---|---|"]
    for a in R["accounting_channel"]:
        L.append(f"| {a['incident_id']} | {a['company'][:20]} | {a['code']} | {a['filing_item'][:38]} | {a['booked_impact'][:26]} |")
    L+=["","## Robustness (shadow T3+T4)",
        f"- Full sample: {rob['full_sample_shadow']['rate']*100:.1f}% (n={rob['full_sample_shadow']['n']})",
        f"- Exclude pre-2021: {rob['b_exclude_pre2021']['rate']*100:.1f}% (n={rob['b_exclude_pre2021']['n']})",
        f"- Direct listed only (drop parent maps): {rob['c_exclude_parent_only']['rate']*100:.1f}% (n={rob['c_exclude_parent_only']['n']})",
        f"- Parent-map subset only: {rob['c_parent_only_subset']['rate']*100:.1f}% (n={rob['c_parent_only_subset']['n']})","",
        "## Cyber benchmark (disclosure-under-mandate; not a shadow rate)",
        f"Item 1.05 material: {R['cyber_benchmark']['item_1_05_material_issuers']} issuers; "
        f"Item 8.01 voluntary: {R['cyber_benchmark']['item_8_01_voluntary_issuers']}; "
        f"as of {R['cyber_benchmark']['as_of']}."]
    (PILOT/"results.md").write_text("\n".join(L)+"\n")
    print("\n".join(L))

if __name__=="__main__": main()
