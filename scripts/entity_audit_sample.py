"""stratified blind sample of 80 incidents for the second-coder entity audit.
Strata oversample the cases where mapping error is most likely: incidents with more than one listed
candidate issuer, PARENT-linked (subsidiary) incidents, and issuers contributing <=3 incidents.
The original mapping is NOT included in the sheet."""
import csv,json,sys,os,random,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
SEED=42; N=80
D=L.coding(); A=L.aiid(); B=L.descriptions(); M=L.firmmap()
CO={r['incident_id']:r for r in csv.DictReader(open(L.out("cocandidates.csv"),newline='',encoding='utf-8',errors='replace'))}
issn=collections.Counter(d['matched_company'] for d in D)
def strat(d):
    iid=d['incident_id']
    if int(CO.get(iid,{}).get('n_distinct_issuers',1) or 1)>1: return "multi-candidate"
    if M.get(iid,{}).get('listing_status')=='PARENT': return "parent-linked"
    if issn[d['matched_company']]<=3: return "small-issuer"
    return "single-candidate-large-issuer"
bys=collections.defaultdict(list)
for d in D: bys[strat(d)].append(d)
print("stratum sizes:",{k:len(v) for k,v in bys.items()})
# take all of the three high-risk strata (capped), fill the remainder at random
rng=random.Random(SEED); picked=[]
for s in ("multi-candidate","parent-linked","small-issuer"):
    pool=sorted(bys[s],key=lambda d:d['incident_id']); rng.shuffle(pool)
    picked+= pool[:min(len(pool),30)]
seen={d['incident_id'] for d in picked}
rest=sorted([d for d in bys["single-candidate-large-issuer"] if d['incident_id'] not in seen],
            key=lambda d:d['incident_id']); rng.shuffle(rest)
picked+= rest[:max(0,N-len(picked))]
picked=picked[:N]
rows=[]
for d in sorted(picked,key=lambda x:int(x['incident_id'])):
    iid=d['incident_id']; a=A.get(iid,{})
    orgs=[]
    for fld in ("deployers","developers"):
        try: orgs+=json.loads(a.get(fld) or "[]")
        except Exception: pass
    rows.append(dict(incident_id=iid,incident_date=d['incident_date'],stratum=strat(d),
        aiid_title=d['title'],aiid_summary=(B.get(iid,'') or '')[:600],
        organizations_named_in_aiid='; '.join(dict.fromkeys(orgs)),
        second_coder_issuer="",second_coder_role="",second_coder_attribution_basis="",
        second_coder_confidence="",second_coder_notes=""))
with open(L.out("entity_audit_sample.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"sample n={len(rows)}; strata:",dict(collections.Counter(r['stratum'] for r in rows)))
print("original mapping withheld: columns are",[c for c in rows[0] if c.startswith('second_coder')])
print("wrote",L.out("entity_audit_sample.csv"))
