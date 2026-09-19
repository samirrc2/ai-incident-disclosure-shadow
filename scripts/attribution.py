"""attribution-basis coding for all 307 incidents. Reviewer-requested post-hoc.

The original protocol recorded only developer / deployer / both, inherited from AIID's own
`deployers` and `developers` arrays. It had no category for an issuer that merely hosted
third-party content or was named without any development or deployment relationship. This script
adds that layer.

Bases:
  developer          issuer built the system
  deployer-operator  issuer ran the system in the context that produced the harm, or made the
                     deployment decision
  both               both of the above
  platform-venue     issuer hosted third-party content or third-party use; the system that produced
                     the harm was not the issuer's own decision
  mentioned-only     issuer named but no developer / deployer / venue relationship is evident,
                     including cases where the issuer is the harmed party or one of several vendors
                     named in a comparative study
Base comes from the AIID arrays; the two overrides are applied by documented lexical rule plus an
explicit review list for cases the rule cannot see.
"""
import csv,json,re,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L

PLATFORM_ISSUERS={"Meta Platforms, Inc.","Alphabet Inc.","Microsoft Corporation","Amazon.com, Inc.",
                  "Snap Inc.","Apple Inc.","PayPal Holdings, Inc.","Walmart Inc.","Match Group, Inc."}
THIRD_PARTY=re.compile(r"deepfake|deep fake|scam|fraudster|fraudulent|impersonat|counterfeit|"
  r"sextortion|extortion|phishing|nudif|csam|child sexual|voice clon|face swap|"
  r"fake (?:ad|account|profile|listing|review)|sold on|scammers?|spoof",re.I)
STUDY=re.compile(r"\bstudy\b|\bstudies\b|researchers?|\baudit(?:ed|ors)?\b|\btested\b|\btests\b|"
  r"benchmark|\bsurvey\b|analysis (?:found|shows)|report(?:edly)? found|experiment|"
  r"investigation found|evaluation found",re.I)
# Cases the lexical rule cannot see, found in the revision-stage review. Each carries a reason.
REVIEW_OVERRIDE={
 "881":("mentioned-only","the harm-producing system was Waymo's robotaxi (Alphabet); the Serve "
        "Robotics delivery bot was the object struck, so Serve is the harmed party rather than the "
        "developer or operator of the system that produced the harm"),
}
D=L.coding(); B=L.descriptions()
CO=({r['incident_id']:r for r in csv.DictReader(open(L.out("cocandidates.csv"),newline='',encoding='utf-8',errors='replace'))})
BASE={"developer":"developer","deployer":"deployer-operator","both":"both"}
rows=[]
for d in D:
    iid=d['incident_id']; txt=f"{d['title']} {B.get(iid,'')}"
    base=BASE.get(d['role'],d['role']); basis=base; conf="medium"; why="AIID arrays: role="+d['role']
    ncand=int(CO.get(iid,{}).get('n_distinct_issuers',1) or 1)
    if iid in REVIEW_OVERRIDE:
        basis,why=REVIEW_OVERRIDE[iid]; conf="high"
    elif THIRD_PARTY.search(txt) and d['matched_company'] in PLATFORM_ISSUERS:
        basis="platform-venue"; conf="medium"
        why=("third-party-generated content or third-party misuse distributed through the issuer's "
             "platform; the harm-producing system was not the issuer's own deployment decision")
    elif ncand>=2 and STUDY.search(txt):
        basis="mentioned-only"; conf="low"
        why=(f"comparative study or audit naming {ncand} listed vendors; no single deployment event "
             "attributable to this issuer")
    rows.append(dict(incident_id=iid,incident_date=d['incident_date'],issuer=d['matched_company'],
        aiid_role=d['role'],attribution_basis=basis,confidence=conf,rationale=why,
        n_candidate_issuers=ncand,disclosure_code=d['disclosure_code'],
        severity=L.SEV.get(d['severity_tier'],d['severity_tier']),title=d['title'][:120]))
with open(L.out("attribution.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
c=collections.Counter(r['attribution_basis'] for r in rows)
print(f"attribution coded: {len(rows)}")
for k,v in c.most_common(): print(f"   {k:<18} {v:4d}  ({v/len(rows):.1%})")
print("\n  by issuer (top):")
bi=collections.Counter((r['issuer'],r['attribution_basis']) for r in rows)
for iss in [x for x,_ in collections.Counter(r['issuer'] for r in rows).most_common(6)]:
    print(f"   {iss[:24]:<26}"+"  ".join(f"{b}={bi.get((iss,b),0)}" for b in
          ("developer","deployer-operator","both","platform-venue","mentioned-only")))
print("\n  attribution x code:")
for b in ("developer","deployer-operator","both","platform-venue","mentioned-only"):
    sub=[r for r in rows if r['attribution_basis']==b]
    if not sub: continue
    cc=collections.Counter(r['disclosure_code'] for r in sub)
    print(f"   {b:<18} n={len(sub):4d}  T1={cc['T1']} T2={cc['T2']} T3={cc['T3']} T4={cc['T4']}")
json.dump({"n":len(rows),"basis_counts":dict(c)},open(L.res("attribution.json"),"w"),indent=1)
print("wrote",L.out("attribution.csv"))
