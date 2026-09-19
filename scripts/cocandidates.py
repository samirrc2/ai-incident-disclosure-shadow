"""re-derive every listed-issuer candidate that entity_resolve.py discarded.
The original map keeps one issuer per incident; the discarded co-candidates were never persisted.
Also emits the tie-break sensitivity inputs for §5C.4. Reviewer-requested post-hoc."""
import csv,json,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from crosswalk import CROSSWALK
RANK={"LISTED":0,"PARENT":1,"DELISTED":2,"FOREIGN":3}
A=L.aiid(); keep={d['incident_id'] for d in L.coding()}; M=L.firmmap()
rows=[]
for iid,r in A.items():
    if not (r["date"] and "2019-01-01"<=r["date"]<="2026-12-31"): continue
    dep=json.loads(r["deployers"] or "[]"); dev=json.loads(r["developers"] or "[]")
    cands=[]
    for s in dict.fromkeys(dep+dev):
        if s in CROSSWALK:
            co,tk,cik,st,conf=CROSSWALK[s]
            if st in RANK:
                cands.append(dict(slug=s,company=co,status=st,conf=conf,
                    in_dev=s in dev,in_dep=s in dep))
    if not cands: continue
    dom=[c for c in cands if c["status"] in ("LISTED","PARENT")]
    iss={c["company"] for c in cands}; issd={c["company"] for c in dom}
    sel=M.get(iid,{}).get('matched_company','')
    # tie-break variants
    def pick(key):
        return sorted(cands,key=key)[0]["company"] if cands else ''
    base = pick(lambda c:(RANK[c["status"]],))                       # original: rank, then order
    prefdev = pick(lambda c:(0 if c["in_dev"] else 1, RANK[c["status"]]))
    prefpar = pick(lambda c:(0 if c["status"]=="PARENT" else 1, RANK[c["status"]]))
    rows.append(dict(incident_id=iid,incident_date=r["date"],in_analytical_sample=iid in keep,
        n_candidates=len(cands),n_distinct_issuers=len(iss),n_distinct_domestic_issuers=len(issd),
        selected_issuer=sel,all_candidates='|'.join(f"{c['slug']}:{c['company']}({c['status']})" for c in cands),
        discarded_issuers='|'.join(sorted(iss-{sel})),
        tiebreak_prefer_developer=prefdev,tiebreak_prefer_parent=prefpar,
        changes_under_prefer_developer=(prefdev!=sel),changes_under_prefer_parent=(prefpar!=sel),
        title=r["title"][:110]))
with open(L.out("cocandidates.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
ins=[r for r in rows if r["in_analytical_sample"]]
m2=[r for r in ins if r["n_distinct_issuers"]>1]; m2d=[r for r in ins if r["n_distinct_domestic_issuers"]>1]
print(f"mapped incidents in window: {len(rows)}   in analytical sample: {len(ins)}")
print(f"  with >=2 distinct listed-issuer candidates:            {len(m2)}  ({len(m2)/len(ins):.1%})")
print(f"  with >=2 distinct DOMESTIC listed-issuer candidates:   {len(m2d)} ({len(m2d)/len(ins):.1%})")
print(f"  max candidates on one incident: {max(r['n_candidates'] for r in ins)}")
print(f"  issuer changes under prefer-developer tie-break: {sum(r['changes_under_prefer_developer'] for r in ins)}")
print(f"  issuer changes under prefer-parent    tie-break: {sum(r['changes_under_prefer_parent'] for r in ins)}")
json.dump(dict(n_in_sample=len(ins),n_multi_any=len(m2),n_multi_domestic=len(m2d),
  max_candidates=max(r['n_candidates'] for r in ins),
  n_change_prefer_developer=sum(r['changes_under_prefer_developer'] for r in ins),
  n_change_prefer_parent=sum(r['changes_under_prefer_parent'] for r in ins)),
  open(L.res("cocandidates.json"),"w"),indent=1)
print("wrote",L.out("cocandidates.csv"))
