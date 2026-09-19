"""shared analysis helpers: Clopper-Pearson intervals and the sample-variant builder."""
import csv,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from scipy.stats import beta

def cp(k,n,alpha=0.05):
    """Clopper-Pearson exact two-sided interval."""
    lo = 0.0 if k==0 else beta.ppf(alpha/2,k,n-k+1)
    hi = 1.0 if k==n else beta.ppf(1-alpha/2,k+1,n-k)
    return (k/n if n else float('nan'), lo, hi)

def pct(x): return f"{100*x:.1f}"

def load():
    """Return a per-incident dict carrying every derived code alongside the original."""
    D={d['incident_id']:dict(d) for d in L.coding()}
    for r in csv.DictReader(open(L.out("t3_split.csv"),newline='',encoding='utf-8',errors='replace')):
        D[r['incident_id']]['t3_split']=r['t3_split']; D[r['incident_id']]['t3_conf']=r['confidence']
    for r in csv.DictReader(open(L.out("attribution.csv"),newline='',encoding='utf-8',errors='replace')):
        D[r['incident_id']]['attribution_basis']=r['attribution_basis']
    adj={r['incident_id']:r['adjudicated_code'] for r in
         csv.DictReader(open(L.out("t2_adjudication.csv"),newline='',encoding='utf-8',errors='replace'))}
    import json
    fix=set(json.load(open(L.res("crosswalk_review.json")))["fix_ids_in_sample"])
    logfix={"350":"T3"}   # coding log records T3; the analytical CSV carries T4 
    for iid,d in D.items():
        d['severity_band']=L.SEV.get(d['severity_tier'],d['severity_tier'])
        d['code_prereg']=d['disclosure_code']
        d['code_adj']=adj.get(iid,d['disclosure_code'])
        d['code_logfix']=logfix.get(iid,d['code_prereg'])
        d['crosswalk_fix']= iid in fix
        # five-way tier under a given base code
        d['tier_prereg']=_five(d,'code_prereg')
        d['tier_adj']=_five(d,'code_adj')
    return D

def _five(d,key):
    c=d[key]
    return d.get('t3_split','T3a') if c=='T3' else c

TIERS5=["T1","T2","T3a","T3b","T4"]

def dist(rows,tierkey="tier_adj"):
    c=collections.Counter(r[tierkey] for r in rows)
    return {t:c.get(t,0) for t in TIERS5}

def shadow_variants(rows,tierkey="tier_adj"):
    d=dist(rows,tierkey); n=len(rows)
    return {
      "n":n,
      "T1":d["T1"],"T2":d["T2"],"T3a":d["T3a"],"T3b":d["T3b"],"T4":d["T4"],
      "substantive":d["T1"]+d["T2"],
      "shadow_broad":d["T3a"]+d["T3b"]+d["T4"],
      "weakly_or_none":d["T3b"]+d["T4"],
      "none_only":d["T4"],
    }
