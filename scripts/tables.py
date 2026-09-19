"""regenerates every revision table from the frozen inputs plus the recodes.
Writes machine-readable JSON to results/ and LaTeX fragments to frontiers/tables/.
All analyses here are reviewer-requested post-hoc additions; the pre-registered primary estimand
(T1 = 4/307, shadow = 300/307) is reported unchanged alongside them."""
import csv,json,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from stats_lib import cp,pct,load,dist,shadow_variants,TIERS5

D=load(); ALL=list(D.values()); OUT={}
os.makedirs(f"{L.ROOT}/frontiers/tables",exist_ok=True)

# ---------- Table 1/5: five-way distribution, pre-registered and adjudicated ----------
for tag,key in (("prereg","tier_prereg"),("adjudicated","tier_adj")):
    d=dist(ALL,key); n=len(ALL); rowsout=[]
    for t in TIERS5:
        p,lo,hi=cp(d[t],n); rowsout.append(dict(tier=t,n=d[t],share=p,lo=lo,hi=hi))
    # the four-tier presentation in Table 1 quotes a COMBINED T3 row; emit it so every printed
    # figure has a machine-readable source rather than being computed only at render time
    t3n=d["T3a"]+d["T3b"]; p3,l3,h3=cp(t3n,n)
    rowsout.append(dict(tier="T3_combined",n=t3n,share=p3,lo=l3,hi=h3))
    sv=shadow_variants(ALL,key)
    for nm,k in (("substantive_T1T2","substantive"),("shadow_broad_T3aT3bT4","shadow_broad"),
                 ("weakly_related_or_none_T3bT4","weakly_or_none"),("none_only_T4","none_only")):
        p,lo,hi=cp(sv[k],n); rowsout.append(dict(tier=nm,n=sv[k],share=p,lo=lo,hi=hi))
    OUT[f"table1_{tag}"]=dict(N=n,rows=rowsout)

# ---------- Table 2: severity, exact counts ----------
sev_rows=[]
for s in ("sev_severe","sev_moderate","sev_limited"):
    sub=[r for r in ALL if r['severity_band']==s]; d=dist(sub,"tier_adj"); n=len(sub)
    t1=d["T1"]; sub_n=d["T1"]+d["T2"]
    p1,l1,h1=cp(t1,n); ps,ls,hs=cp(sub_n,n)
    sev_rows.append(dict(severity=s,n=n,**{t:d[t] for t in TIERS5},
        T1_share=p1,T1_lo=l1,T1_hi=h1,sub_share=ps,sub_lo=ls,sub_hi=hs,
        shadow=d["T3a"]+d["T3b"]+d["T4"]))
OUT["table2_severity"]=sev_rows

# ---------- Table S5: CSET-40 only ----------
cs=[r for r in ALL if r['severity_source']=='CSET']
cset=[]
for s in ("sev_severe","sev_moderate","sev_limited"):
    sub=[r for r in cs if r['severity_band']==s]
    if not sub: continue
    d=dist(sub,"tier_adj")
    cset.append(dict(severity=s,n=len(sub),**{t:d[t] for t in TIERS5}))
OUT["tableS5_cset40"]=dict(n=len(cs),rows=cset,
    n_substantive=sum(1 for r in cs if r['tier_adj'] in ("T1","T2")),
    test="none performed: fewer than 5 substantive cases in the subset")

# ---------- Table 6: attribution basis, overall and by issuer ----------
BASES=["developer","deployer-operator","both","platform-venue","mentioned-only"]
ab=collections.Counter(r['attribution_basis'] for r in ALL)
byiss=collections.Counter((r['matched_company'],r['attribution_basis']) for r in ALL)
issuers=[i for i,_ in collections.Counter(r['matched_company'] for r in ALL).most_common()]
OUT["table6_attribution"]=dict(
  overall={b:ab.get(b,0) for b in BASES},
  overall_share={b:round(ab.get(b,0)/len(ALL),4) for b in BASES},
  by_issuer=[dict(issuer=i,n=sum(byiss.get((i,b),0) for b in BASES),
                  **{b:byiss.get((i,b),0) for b in BASES}) for i in issuers],
  by_basis_tier=[dict(basis=b,**dist([r for r in ALL if r['attribution_basis']==b],"tier_adj"),
                      n=ab.get(b,0)) for b in BASES])

# ---------- Table 7: role x tier ----------
role_rows=[]
for role,lab in (("developer","developer-only"),("deployer","deployer-only"),("both","both")):
    sub=[r for r in ALL if r['role']==role]; d=dist(sub,"tier_adj")
    role_rows.append(dict(role=lab,n=len(sub),**{t:d[t] for t in TIERS5},
        substantive=d["T1"]+d["T2"]))
dev=[r for r in ALL if r['role']=='developer']; anydep=[r for r in ALL if r['role'] in ('deployer','both')]
OUT["table7_role"]=dict(three_way=role_rows,two_by_two=dict(
    developer_only=dict(n=len(dev),substantive=sum(1 for r in dev if r['tier_adj'] in ("T1","T2")),
                        T1=sum(1 for r in dev if r['tier_adj']=="T1")),
    any_deployer=dict(n=len(anydep),substantive=sum(1 for r in anydep if r['tier_adj'] in ("T1","T2")),
                      T1=sum(1 for r in anydep if r['tier_adj']=="T1"))))

# ---------- Table 4: robustness ----------
def row(label,rows,key="tier_adj",note=""):
    sv=shadow_variants(rows,key); n=sv["n"]
    p,lo,hi=cp(sv["shadow_broad"],n); ps,ls,hs=cp(sv["substantive"],n)
    return dict(variant=label,n=n,T1=sv["T1"],T2=sv["T2"],T3a=sv["T3a"],T3b=sv["T3b"],T4=sv["T4"],
        substantive=sv["substantive"],sub_share=ps,sub_lo=ls,sub_hi=hs,
        shadow=sv["shadow_broad"],shadow_share=p,shadow_lo=lo,shadow_hi=hi,
        weakly_or_none=sv["weakly_or_none"],none_only=sv["none_only"],note=note)
rob=[]
rob.append(row("Pre-registered primary (N=307)",ALL,"tier_prereg","pre-registered; unchanged"))
rob.append(row("Adjudicated T2 codes",ALL,"tier_adj","; one T2 recoded T1"))
# Incident 350 is T4 in the analytical CSV but T3 in the coding log. Under the log it needs a
# T3a/T3b value; its evidence records family-level autonomous-robot/AI risk language with no harm
# family, so it takes T3b -- the conservative side, as in 
rob.append(row("Coding-log code for incident 350",
    [dict(r,tier_adj=("T3b" if r['incident_id']=='350' else r['tier_adj'])) for r in ALL],
    "tier_adj","; coding log records T3, the analytical CSV carried T4"))
# The second-coder audit identified incidents 1436 and 1528 as Johnson & Johnson at their incident
# dates, not Integra: Integra acquired Acclarent from Ethicon on 1 April 2024, after both. J&J's
# filings were never searched for them, so they are dropped alongside the crosswalk FIX rows.
ACCLARENT={'1436','1528'}
rob.append(row("Corrected sample: crosswalk FIX and as-of-date corrections removed",
    [r for r in ALL if not r['crosswalk_fix'] and r['incident_id'] not in ACCLARENT],"tier_adj",
    " and §5B.3; 2 crosswalk corrections and 2 ownership-date corrections removed"))
rob.append(row("Excluding platform-venue",[r for r in ALL if r['attribution_basis']!='platform-venue'],"tier_adj",""))
rob.append(row("Excluding platform-venue and mentioned-only",[r for r in ALL if r['attribution_basis'] not in ('platform-venue','mentioned-only')],"tier_adj",""))
rob.append(row("T3a treated as the only related generic language",ALL,"tier_adj","see weakly_or_none column"))
# tie-break variants: issuer changes mean those incidents' filings were never searched, so they drop
CO={r['incident_id']:r for r in csv.DictReader(open(L.out("cocandidates.csv"),newline='',encoding='utf-8',errors='replace'))}
for lab,fld in (("Tie-break: prefer developer","changes_under_prefer_developer"),
                ("Tie-break: prefer parent","changes_under_prefer_parent")):
    keep=[r for r in ALL if CO.get(r['incident_id'],{}).get(fld,'False')!='True']
    rob.append(row(lab+" (issuer-changed incidents dropped)",keep,"tier_adj",
        f"{len(ALL)-len(keep)} incidents would map to a different issuer whose filings were not searched"))
ER=json.load(open(L.res("entity_reliability.json")))
_keep={p['incident_id'] for p in ER['disagreements'] if p['orig_issuer']!=p['new_issuer']}
rob.append(row("Second-coder entity mappings (disagreement incidents dropped)",
    [r for r in ALL if r['incident_id'] not in _keep],"tier_adj",
    f"; {ER['issuer_identity']['raw_agreement']*100:.1f}% agreement on issuer identity "
    f"(kappa {ER['issuer_identity']['cohens_kappa']:.2f}); the {len(_keep)} incidents the second "
    "coder maps differently are dropped because those issuers' filings were never searched"))
OUT["entity_reliability"]=ER
# the share of the T3 mass that matches both families, quoted in Section 4.2
_d=dist(ALL,"tier_adj")
OUT["t3a_share_of_t3_mass"]=round(100*_d["T3a"]/(_d["T3a"]+_d["T3b"]),1)
OUT["table4_robustness"]=rob

# ---------- supplementary five-way breakdowns ----------
def brk(field,labels=None):
    out=[]
    vals=labels or sorted({r[field] for r in ALL})
    for v in vals:
        sub=[r for r in ALL if r[field]==v]; d=dist(sub,"tier_adj")
        out.append(dict(**{field:v},n=len(sub),**{t:d[t] for t in TIERS5}))
    return out
OUT["tableS_fiveway_by_severity"]=brk("severity_band",["sev_severe","sev_moderate","sev_limited"])
OUT["tableS_fiveway_by_role"]=brk("role",["developer","deployer","both"])
for r in ALL: r['year']=r['incident_date'][:4]
OUT["tableS_fiveway_by_year"]=brk("year")

json.dump(OUT,open(L.res("tables.json"),"w"),indent=1,default=str)

# ---------- console summary ----------
t=OUT["table1_adjudicated"]
print(f"=== five-way distribution (adjudicated), N={t['N']} ===")
for r in t["rows"]:
    print(f"   {r['tier']:<30} n={r['n']:>4}  {pct(r['share'])}%  [{pct(r['lo'])}, {pct(r['hi'])}]")
p=OUT["table1_prereg"]["rows"]
print("\n=== pre-registered primary (unchanged) ===")
for r in p:
    if r['tier'] in ("T1","shadow_broad_T3aT3bT4","substantive_T1T2"):
        print(f"   {r['tier']:<30} n={r['n']:>4}  {pct(r['share'])}%  [{pct(r['lo'])}, {pct(r['hi'])}]")
print("\n=== Table 4 robustness ===")
for r in rob:
    if r['n'] is None: print(f"   {r['variant']:<58} {r['note']}"); continue
    print(f"   {r['variant']:<58} N={r['n']:>3}  T1={r['T1']} sub={r['substantive']}  shadow={pct(r['shadow_share'])}%  T3b+T4={r['weakly_or_none']}")
print("\nwrote",L.res("tables.json"))
