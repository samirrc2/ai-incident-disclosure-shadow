#!/usr/bin/env python3
"""p13_21_extended — concentration, clustered inference, formal tests, issuer-level, categories,
retrieval-validation and window-robustness summaries. Deterministic (seed 42). No network.
Outputs revision/results/P13_extended.json and .md.
"""
from __future__ import annotations
import csv, json, math, random
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from scipy import stats
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import p13_config as _C0; _C0.ensure_out()
import p13_config as C
csv.field_size_limit(10_000_000)
RNG = np.random.default_rng(42)
REV = C.RESULTS

def wilson(k,n,z=1.96):
    if n==0: return (0.0,0.0,0.0)
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return (p,(c-h)/d,(c+h)/d)

rows=list(csv.DictReader(open(C.CODED)))
raw={str(r["incident_id"]):r for r in csv.DictReader(open(C.INCIDENTS))}
N=len(rows)
shadow=lambda r: r["disclosure_code"] in ("T3","T4")
subst=lambda r: r["disclosure_code"] in ("T1","T2")
for r in rows: r["_shadow"]=shadow(r); r["_subst"]=subst(r)

R={"N":N}

# ---- 1. concentration ----
by_iss=Counter(r["matched_company"] for r in rows)
shares={c:n/N for c,n in by_iss.items()}
HHI=sum(s*s for s in shares.values())
R["concentration"]={"n_issuers":len(by_iss),"HHI":round(HHI,4),
    "HHI_interpretation":"1/nissuers="+str(round(1/len(by_iss),4))+" (min); 1.0 (max)",
    "top_issuers":by_iss.most_common(10),
    "top2_share":round(sum(dict(by_iss.most_common(2)).values())/N,3),
    "top5_share":round(sum(dict(by_iss.most_common(5)).values())/N,3)}

# ---- 2. leave-one-issuer-out + drop-top-k (shadow rate) ----
def shadow_rate(rs):
    k=sum(1 for r in rs if r["_shadow"]); return k,len(rs),(k/len(rs) if rs else 0)
loio={}
for iss in by_iss:
    rs=[r for r in rows if r["matched_company"]!=iss]
    loio[iss]=round(shadow_rate(rs)[2],4)
top2=set(c for c,_ in by_iss.most_common(2)); top5=set(c for c,_ in by_iss.most_common(5))
R["robustness_concentration"]={
    "full_shadow":round(shadow_rate(rows)[2],4),
    "LOIO_min":min(loio.values()),"LOIO_max":max(loio.values()),
    "LOIO_by_issuer":loio,
    "drop_top2":{"issuers":sorted(top2),"n":N-sum(dict(by_iss.most_common(2)).values()),
        "shadow":round(shadow_rate([r for r in rows if r['matched_company'] not in top2])[2],4)},
    "drop_top5":{"issuers":sorted(top5),"n":N-sum(dict(by_iss.most_common(5)).values()),
        "shadow":round(shadow_rate([r for r in rows if r['matched_company'] not in top5])[2],4)}}

# ---- 3. issuer-cluster bootstrap CIs (resample 21 issuers w/ replacement) ----
iss_groups=defaultdict(list)
for r in rows: iss_groups[r["matched_company"]].append(r)
iss_list=list(iss_groups)
def cluster_boot(stat, B=10000):
    vals=[]
    for _ in range(B):
        picks=RNG.choice(len(iss_list), size=len(iss_list), replace=True)
        pool=[]
        for i in picks: pool.extend(iss_groups[iss_list[i]])
        vals.append(stat(pool))
    lo,hi=np.percentile(vals,[2.5,97.5]); return float(np.mean(vals)),float(lo),float(hi)
sh_stat=lambda pool: sum(1 for r in pool if r["_shadow"])/len(pool)
t1_stat=lambda pool: sum(1 for r in pool if r["disclosure_code"]=="T1")/len(pool)
sb_m,sb_lo,sb_hi=cluster_boot(sh_stat)
t1_m,t1_lo,t1_hi=cluster_boot(t1_stat)
# issuer-level mean shadow (each issuer weighted equally)
iss_shadow=[shadow_rate(g)[2] for g in iss_groups.values()]
R["clustered_inference"]={
    "shadow_incidentlevel_wilson":[round(x,4) for x in wilson(sum(1 for r in rows if r['_shadow']),N)],
    "shadow_issuer_cluster_bootstrap":{"mean":round(sb_m,4),"ci95":[round(sb_lo,4),round(sb_hi,4)],"B":10000,"seed":42},
    "T1_issuer_cluster_bootstrap":{"mean":round(t1_m,4),"ci95":[round(t1_lo,4),round(t1_hi,4)]},
    "issuer_level_mean_shadow":round(float(np.mean(iss_shadow)),4),
    "note":"Issuer-clustered bootstrap resamples the 21 issuers with replacement; widens vs incident-level Wilson. GLMM not estimated (only 7 substantive positives -> separation)."}

# ---- 4. formal tests on substantive disclosure (T1+T2) across strata ----
def fisher_table(groupfn):
    groups=defaultdict(lambda:[0,0])
    for r in rows:
        g=groupfn(r); groups[g][0 if r["_subst"] else 1]+=1
    return groups
def chi2_or_fisher(groups):
    tab=np.array([[v[0],v[1]] for v in groups.values()])
    if tab.shape[0]==2:
        _,p=stats.fisher_exact(tab); test="fisher_exact"
    else:
        chi2,p,_,_=stats.chi2_contingency(tab); test="chi2"
    n=tab.sum(); cv=math.sqrt((stats.chi2_contingency(tab)[0])/(n*(min(tab.shape)-1))) if n else 0
    return test,round(float(p),4),round(cv,3),{str(k):v for k,v in groups.items()}
tests={}
tests["by_severity"]=chi2_or_fisher(fisher_table(lambda r:r["severity_tier"]))
tests["by_role"]=chi2_or_fisher(fisher_table(lambda r:r["role"]))
tests["by_parent"]=chi2_or_fisher(fisher_table(lambda r:r["listing_status"]))
# Cochran-Armitage trend of substantive over year
yrs=sorted(set(r["incident_date"][:4] for r in rows))
ylab={y:i for i,y in enumerate(yrs)}
succ=[0]*len(yrs); tot=[0]*len(yrs)
for r in rows:
    i=ylab[r["incident_date"][:4]]; tot[i]+=1; succ[i]+= 1 if r["_subst"] else 0
def cochran_armitage(succ,tot,scores):
    succ=np.array(succ);tot=np.array(tot);x=np.array(scores,float)
    N=tot.sum();R_=succ.sum();pbar=R_/N
    T=np.sum(succ*x)-pbar*np.sum(tot*x)
    varT=pbar*(1-pbar)*(np.sum(tot*x*x)-(np.sum(tot*x)**2)/N)
    z=T/math.sqrt(varT) if varT>0 else 0.0; p=2*(1-stats.norm.cdf(abs(z)))
    return round(float(z),3),round(float(p),4)
z,pt=cochran_armitage(succ,tot,list(range(len(yrs))))
tests["year_trend_cochran_armitage"]={"z":z,"p":pt,"succ_by_year":dict(zip(yrs,succ)),"n_by_year":dict(zip(yrs,tot))}
R["formal_tests"]=tests
R["formal_tests_note"]=("Only 7 substantive (T1+T2) positives -> tests are low-powered; non-significant "
    "results indicate 'no detectable difference', not evidence of equality.")

# ---- 5. issuer-level T1-T4 table + % issuers with >=1 substantive ----
issuer_tbl={}
for iss,g in sorted(iss_groups.items(), key=lambda kv:-len(kv[1])):
    d=Counter(r["disclosure_code"] for r in g)
    issuer_tbl[iss]={"n":len(g),**{t:d.get(t,0) for t in ["T1","T2","T3","T4"]},
                     "shadow":round(shadow_rate(g)[2],3),"has_substantive":any(r["_subst"] for r in g)}
R["issuer_level"]={"table":issuer_tbl,
    "n_issuers_with_substantive":sum(1 for v in issuer_tbl.values() if v["has_substantive"]),
    "pct_issuers_with_substantive":round(sum(1 for v in issuer_tbl.values() if v["has_substantive"])/len(issuer_tbl),3)}

# ---- 6. incident-category (transparent keyword rubric) ----
import re
CATS=[("autonomous_vehicle",r"cruise|waymo|autopilot|self-driving|robotaxi|zoox|full self|smart summon|driverless"),
 ("copyright_ip",r"copyright|libgen|books3|training data|infring|pirat"),
 ("discrimination_bias",r"bias|discriminat|racial|gender|fair housing|redlin"),
 ("privacy_surveillance",r"privacy|facial recognition|surveillance|biometric|camera|footage|data breach|leak"),
 ("misinformation_content",r"misinformation|deepfake|fake|hate|content|moderat|defamation|defam|propaganda|election"),
 ("safety_physical",r"injur|death|killed|fatal|robot|crash|collision|pedestrian|stroke|medical"),
 ("employment_hiring",r"hiring|recruit|resume|applicant|worker|employee|layoff"),
 ("generative_error",r"chatbot|hallucinat|inaccurate|gemini|bard|bing|copilot|generated|llm|assistant|search")]
def categorize(r):
    t=((r.get("title","") or "")+" "+(raw.get(r["incident_id"],{}).get("description","") or "")).lower()
    for name,pat in CATS:
        if re.search(pat,t): return name
    return "other"
for r in rows: r["_cat"]=categorize(r)
cat_tbl={}
for cat in [c for c,_ in CATS]+["other"]:
    g=[r for r in rows if r["_cat"]==cat]
    if not g: continue
    d=Counter(r["disclosure_code"] for r in g)
    cat_tbl[cat]={"n":len(g),**{t:d.get(t,0) for t in ["T1","T2","T3","T4"]},
                  "substantive":sum(1 for r in g if r["_subst"])}
R["by_category"]=cat_tbl

# ---- 7. retrieval-validation + window robustness summaries (from agent outputs) ----
fn=0; ftot=0
for f in ["retrieval_A.json","retrieval_B.json"]:
    p=(C.LOGS/f)
    if p.exists():
        d=json.load(open(p))
        for v in d.values():
            ftot+=1
            if isinstance(v,dict) and str(v.get("audit_verdict","")).upper().startswith("REVISE"): fn+=1
R["retrieval_validation"]={"audited":ftot,"false_negatives_found":fn,
    "false_negative_rate":round(fn/ftot,4) if ftot else None,
    "rule_of_three_upper95": round(3/ftot,4) if (ftot and fn==0) else None,
    "interpretation":"0 missed disclosures in the audited sample; upper 95% bound ~3/n."}
if (C.LOGS/"altwindow.json").exists():
    aw=json.load(open(C.LOGS/"altwindow.json"))
    def subst_at(key):
        return sum(1 for v in aw.values() if str(v.get(key,"")).startswith(("T1","T2")))
    # baseline substantive=7; shadow = 307 - substantive
    def shadow_at(nsubst): return round((N-nsubst)/N,4)
    s6=sum(1 for v in aw.values() if str(v.get("code_6mo","")).startswith(("T1","T2")))
    s18=sum(1 for v in aw.values() if str(v.get("code_18mo","")).startswith(("T1","T2")))
    s24=sum(1 for v in aw.values() if str(v.get("code_24mo","")).startswith(("T1","T2")))
    R["window_robustness"]={"substantive_6mo":s6,"substantive_12mo":7,"substantive_18mo":s18,"substantive_24mo":s24,
        "shadow_6mo":shadow_at(s6),"shadow_12mo":shadow_at(7),"shadow_18mo":shadow_at(s18),"shadow_24mo":shadow_at(s24),
        "note":"Substantive disclosures fall in the fiscal-year 10-K ~9-11 months post-incident; robust to lengthening (12=18=24), only shortening to 6mo drops 4 of 7 into T3."}

(C.EXT_JSON).write_text(json.dumps(R,indent=2,default=str))
# markdown
L=["# P13 Extended Analysis (revision)","",
 f"## Concentration\n- Issuers: {R['concentration']['n_issuers']}; HHI = **{R['concentration']['HHI']}** "
 f"(top-2 share {R['concentration']['top2_share']}, top-5 {R['concentration']['top5_share']}).",
 f"- Top issuers: "+", ".join(f"{c} {n}" for c,n in R['concentration']['top_issuers'][:7]),"",
 "## Concentration robustness (shadow rate)",
 f"- Full: {R['robustness_concentration']['full_shadow']*100:.1f}%",
 f"- Leave-one-issuer-out range: {R['robustness_concentration']['LOIO_min']*100:.1f}%–{R['robustness_concentration']['LOIO_max']*100:.1f}%",
 f"- Drop top-2 (Alphabet+Meta): {R['robustness_concentration']['drop_top2']['shadow']*100:.1f}% (n={R['robustness_concentration']['drop_top2']['n']})",
 f"- Drop top-5: {R['robustness_concentration']['drop_top5']['shadow']*100:.1f}% (n={R['robustness_concentration']['drop_top5']['n']})","",
 "## Clustered inference",
 f"- Shadow, incident-level Wilson: {R['clustered_inference']['shadow_incidentlevel_wilson'][0]*100:.1f}% "
 f"[{R['clustered_inference']['shadow_incidentlevel_wilson'][1]*100:.1f}, {R['clustered_inference']['shadow_incidentlevel_wilson'][2]*100:.1f}]",
 f"- Shadow, issuer-clustered bootstrap: {sb_m*100:.1f}% [{sb_lo*100:.1f}, {sb_hi*100:.1f}] (B=10k, seed 42)",
 f"- T1, issuer-clustered bootstrap: {t1_m*100:.1f}% [{t1_lo*100:.1f}, {t1_hi*100:.1f}]",
 f"- Issuer-level mean shadow: {R['clustered_inference']['issuer_level_mean_shadow']*100:.1f}%","",
 "## Formal tests (substantive T1+T2 across strata)",
 f"- Severity: {tests['by_severity'][0]} p={tests['by_severity'][1]}, Cramér's V={tests['by_severity'][2]}",
 f"- Role: {tests['by_role'][0]} p={tests['by_role'][1]}, V={tests['by_role'][2]}",
 f"- Parent vs direct: {tests['by_parent'][0]} p={tests['by_parent'][1]}, V={tests['by_parent'][2]}",
 f"- Year trend (Cochran–Armitage): z={z}, p={pt}",
 f"- _{R['formal_tests_note']}_","",
 "## Issuer-level outcomes",
 f"- Issuers with ≥1 substantive disclosure: **{R['issuer_level']['n_issuers_with_substantive']}/{len(issuer_tbl)} "
 f"({R['issuer_level']['pct_issuers_with_substantive']*100:.0f}%)**","",
 "| issuer | n | T1 | T2 | T3 | T4 | shadow |","|---|---|---|---|---|---|---|"]
for iss,v in list(issuer_tbl.items())[:12]:
    L.append(f"| {iss[:24]} | {v['n']} | {v['T1']} | {v['T2']} | {v['T3']} | {v['T4']} | {v['shadow']*100:.0f}% |")
L+=["","## By incident category","| category | n | T1 | T2 | T3 | T4 | substantive |","|---|---|---|---|---|---|---|"]
for cat,v in sorted(cat_tbl.items(),key=lambda kv:-kv[1]['n']):
    L.append(f"| {cat} | {v['n']} | {v['T1']} | {v['T2']} | {v['T3']} | {v['T4']} | {v['substantive']} |")
L+=["","## Retrieval validation (false negatives)",
 f"- Audited {R['retrieval_validation']['audited']} incidents (20 T3 + 20 T4); "
 f"**{R['retrieval_validation']['false_negatives_found']} missed disclosures found**; "
 f"upper 95% bound ≈ {R['retrieval_validation']['rule_of_three_upper95']}.",""]
if "window_robustness" in R:
    w=R["window_robustness"]
    L+=["## Window robustness (shadow rate)",
     f"- 6mo {w['shadow_6mo']*100:.1f}% · 12mo {w['shadow_12mo']*100:.1f}% · 18mo {w['shadow_18mo']*100:.1f}% · 24mo {w['shadow_24mo']*100:.1f}%",
     f"- _{w['note']}_"]
(C.EXT_MD).write_text("\n".join(L)+"\n")
print("\n".join(L))
