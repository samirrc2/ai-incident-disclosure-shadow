"""role contrast and leave-one-positive-out fragility.
The original test (scripts/inference.py) is the 3-way contrast: role (developer / deployer / both)
x substantive (T1+T2), chi-square statistic, Monte-Carlo permutation, B=20,000, seed 42, giving
p = 0.0234. Both that contrast and the 2x2 (developer-only vs any-deployer) are re-run here, then
every single-case perturbation of the seven substantive incidents is scored under both."""
import csv,json,sys,os,collections
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from stats_lib import load
B=20000; SEED=42

def chi2(labels,y):
    labs=sorted(set(labels)); tab=np.zeros((len(labs),2))
    idx={l:i for i,l in enumerate(labs)}
    for l,v in zip(labels,y): tab[idx[l],int(v)]+=1
    n=tab.sum(); rs=tab.sum(1,keepdims=True); cs=tab.sum(0,keepdims=True)
    exp=rs@cs/n
    with np.errstate(divide='ignore',invalid='ignore'):
        c=np.where(exp>0,(tab-exp)**2/exp,0.0)
    return float(c.sum())

def perm_p(labels,y,seed=SEED,B=B):
    obs=chi2(labels,y); rng=np.random.default_rng(seed)
    y=np.asarray(y,dtype=int); cnt=0
    for _ in range(B):
        if chi2(labels,rng.permutation(y))>=obs-1e-12: cnt+=1
    return round(obs,3),round((cnt+1)/(B+1),4)

D=load(); ALL=list(D.values())
def contrasts(rows,codekey="tier_adj"):
    y=[1 if r[codekey] in ("T1","T2") else 0 for r in rows]
    three=[r['role'] for r in rows]
    two=['developer-only' if r['role']=='developer' else 'any-deployer' for r in rows]
    return perm_p(three,y),perm_p(two,y)

base3,base2=contrasts(ALL)
print(f"baseline (adjudicated codes):  3-way chi2={base3[0]} p={base3[1]}   2x2 chi2={base2[0]} p={base2[1]}")
pre3,pre2=contrasts(ALL,"tier_prereg")
print(f"baseline (pre-registered):     3-way chi2={pre3[0]} p={pre3[1]}   2x2 chi2={pre2[0]} p={pre2[1]}")

subst=[r for r in ALL if r['tier_adj'] in ("T1","T2")]
rows=[]
rows.append(dict(perturbation="none (baseline, adjudicated)",incident_id="-",issuer="-",
    chi2_3way=base3[0],p_3way=base3[1],chi2_2x2=base2[0],p_2x2=base2[1]))
DOWN={"T1":"T2","T2":"T3b"}
for s in subst:
    iid=s['incident_id']
    for lab,fn in (("drop",None),("one tier down",lambda r:DOWN[r['tier_adj']]),("reclassify to T3",lambda r:"T3b")):
        if fn is None: sub=[r for r in ALL if r['incident_id']!=iid]
        else: sub=[dict(r,tier_adj=fn(r)) if r['incident_id']==iid else r for r in ALL]
        a,b=contrasts(sub)
        rows.append(dict(perturbation=lab,incident_id=iid,issuer=s['matched_company'],
            chi2_3way=a[0],p_3way=a[1],chi2_2x2=b[0],p_2x2=b[1]))
# upper-bound fragility: promote one developer-only T3 incident to T1
dev_t3=[r for r in ALL if r['role']=='developer' and r['tier_adj'] in ("T3a","T3b")][0]
sub=[dict(r,tier_adj="T1") if r['incident_id']==dev_t3['incident_id'] else r for r in ALL]
a,b=contrasts(sub)
rows.append(dict(perturbation="promote one developer-only T3 incident to T1",
    incident_id=dev_t3['incident_id'],issuer=dev_t3['matched_company'],
    chi2_3way=a[0],p_3way=a[1],chi2_2x2=b[0],p_2x2=b[1]))
with open(L.out("role_loo.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
p3=[r['p_3way'] for r in rows[1:]]; p2=[r['p_2x2'] for r in rows[1:]]
print(f"\nperturbations scored: {len(rows)-1}")
print(f"  3-way p range across perturbations: {min(p3):.4f} - {max(p3):.4f};  >=0.05 in {sum(1 for x in p3 if x>=0.05)}/{len(p3)}")
print(f"  2x2   p range across perturbations: {min(p2):.4f} - {max(p2):.4f};  >=0.05 in {sum(1 for x in p2 if x>=0.05)}/{len(p2)}")
for r in rows: print(f"   {r['perturbation']:<44} id={r['incident_id']:<5} p3={r['p_3way']:.4f}  p2x2={r['p_2x2']:.4f}")
json.dump(dict(baseline_adjudicated=dict(three_way=base3,two_by_two=base2),
  baseline_prereg=dict(three_way=pre3,two_by_two=pre2),
  p3_min=min(p3),p3_max=max(p3),p2_min=min(p2),p2_max=max(p2),
  n_perturbations=len(rows)-1,n_p3_nonsig=sum(1 for x in p3 if x>=0.05),
  n_p2_nonsig=sum(1 for x in p2 if x>=0.05),B=B,seed=SEED),
  open(L.res("role_loo.json"),"w"),indent=1)
print("wrote",L.out("role_loo.csv"))
