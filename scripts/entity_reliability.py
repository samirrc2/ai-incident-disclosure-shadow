"""reliability of issuer matching, once the blind second-coder sheet is returned.

Usage:  python3 scripts/entity_reliability.py <returned_sheet.csv>

Computes raw agreement, Cohen's kappa and Gwet's AC1 separately on issuer identity and on role,
lists every disagreement for reconciliation, and re-estimates the primary tier distribution under
the second coder's mappings. Incidents the second coder resolves to no listed issuer are dropped;
incidents reassigned to a different issuer are reported separately, because that issuer's filings
were never searched and no disclosure code exists for them."""
import csv,json,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from stats_lib import load,cp,dist,TIERS5

def agreement(a,b):
    """raw agreement, Cohen's kappa, Gwet's AC1 over paired nominal codings."""
    n=len(a); po=sum(1 for x,y in zip(a,b) if x==y)/n if n else float('nan')
    cats=sorted(set(a)|set(b)); ca=collections.Counter(a); cb=collections.Counter(b)
    pe_k=sum((ca[c]/n)*(cb[c]/n) for c in cats)
    pi=[ (ca[c]+cb[c])/(2*n) for c in cats ]
    pe_g=sum(p*(1-p) for p in pi)/(len(cats)-1) if len(cats)>1 else 0.0
    k=(po-pe_k)/(1-pe_k) if pe_k<1 else float('nan')
    ac1=(po-pe_g)/(1-pe_g) if pe_g<1 else float('nan')
    return dict(n=n,raw_agreement=round(po,4),cohens_kappa=round(k,4),gwet_ac1=round(ac1,4),
                pe_kappa=round(pe_k,4),pe_gwet=round(pe_g,4))

def main(path):
    ret=[r for r in csv.DictReader(open(path,newline='',encoding='utf-8',errors='replace'))
         if (r.get('second_coder_issuer') or '').strip()]
    if not ret: sys.exit("no completed rows in the returned sheet")
    D=load(); M=L.firmmap()
    pairs=[]
    for r in ret:
        iid=r['incident_id']; o=D.get(iid)
        if not o: continue
        pairs.append(dict(incident_id=iid,
            orig_issuer=o['matched_company'],new_issuer=r['second_coder_issuer'].strip(),
            orig_role=o['role'],new_role=(r.get('second_coder_role') or '').strip(),
            new_basis=(r.get('second_coder_attribution_basis') or '').strip(),
            conf=(r.get('second_coder_confidence') or '').strip(),
            notes=(r.get('second_coder_notes') or '').strip(),
            code=o['tier_adj']))
    strat={r['incident_id']:r.get('stratum','') for r in
           csv.DictReader(open(L.out("entity_audit_sample.csv"),newline='',encoding='utf-8',errors='replace'))}
    for p in pairs: p['stratum']=strat.get(p['incident_id'],'')
    iss=agreement([p['orig_issuer'] for p in pairs],[p['new_issuer'] for p in pairs])
    by_stratum={}
    for s in sorted({p['stratum'] for p in pairs}):
        sub=[p for p in pairs if p['stratum']==s]
        ag=sum(1 for p in sub if p['orig_issuer']==p['new_issuer'])
        by_stratum[s]=dict(n=len(sub),agree=ag,pct=round(100*ag/len(sub),1))
    by_conf={}
    for c in sorted({(p['conf'] or 'unstated').lower() for p in pairs}):
        sub=[p for p in pairs if (p['conf'] or 'unstated').lower()==c]
        ag=sum(1 for p in sub if p['orig_issuer']==p['new_issuer'])
        by_conf[c]=dict(n=len(sub),agree=ag,pct=round(100*ag/len(sub),1))
    rol=[p for p in pairs if p['new_role']]
    role=agreement([p['orig_role'] for p in rol],[p['new_role'] for p in rol]) if rol else {}
    dis=[p for p in pairs if p['orig_issuer']!=p['new_issuer'] or (p['new_role'] and p['orig_role']!=p['new_role'])]
    dropped=[p for p in pairs if p['new_issuer'].upper().startswith('NONE')]
    reassigned=[p for p in pairs if not p['new_issuer'].upper().startswith('NONE')
                and p['new_issuer']!=p['orig_issuer']]
    kept=[p for p in pairs if p['new_issuer']==p['orig_issuer']]
    ALL=list(D.values())
    audited={p['incident_id'] for p in pairs}
    reest=[r for r in ALL if r['incident_id'] not in audited] + \
          [D[p['incident_id']] for p in kept]
    d=dist(reest,"tier_adj"); n=len(reest)
    sh=cp(d['T3a']+d['T3b']+d['T4'],n); t1=cp(d['T1'],n)
    out=dict(sheet=os.path.basename(path),n_returned=len(pairs),
      issuer_identity=iss,role=role,
      issuer_by_stratum=by_stratum,issuer_by_confidence=by_conf,
      disagreement_tiers=dict(collections.Counter(
          p['code'] for p in pairs if p['orig_issuer']!=p['new_issuer'])),
      n_disagreements=len(dis),n_dropped_no_listed_issuer=len(dropped),
      n_reassigned_other_issuer=len(reassigned),
      reassigned_note=("filings for a reassigned issuer were never searched, so these incidents "
        "carry no disclosure code and are excluded from the re-estimate rather than recoded"),
      reestimate=dict(N=n,**{t:d[t] for t in TIERS5},
        T1_share=round(t1[0],4),T1_ci=[round(t1[1],4),round(t1[2],4)],
        shadow_share=round(sh[0],4),shadow_ci=[round(sh[1],4),round(sh[2],4)]),
      disagreements=[{k:p[k] for k in ('incident_id','orig_issuer','new_issuer','orig_role','new_role','conf','notes')} for p in dis])
    json.dump(out,open(L.res("entity_reliability.json"),"w"),indent=1)
    print(json.dumps({k:v for k,v in out.items() if k!='disagreements'},indent=1))
    print(f"\ndisagreements listed for reconciliation: {len(dis)}")
    for p in dis[:20]:
        print(f"   id={p['incident_id']}  {p['orig_issuer']} / {p['orig_role']}  ->  {p['new_issuer']} / {p['new_role']}")
    print("\nwrote",L.res("entity_reliability.json"))

if __name__=="__main__":
    if len(sys.argv)<2: sys.exit(__doc__)
    main(sys.argv[1])
