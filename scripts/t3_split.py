"""T3a / T3b recode of all 278 T3 incidents. Reviewer-requested post-hoc.

Rule, fixed before any value was computed:
  incident side  — application and harm families detected in the AIID title + description
  filing side    — families detected in the AFFIRMATIVE clauses of the filing-search evidence
                   prose (negated clauses stripped: they describe what the filing does NOT contain)
  T3a  both the incident's application family AND its harm family are matched by filing language
  T3b  only one of the two is matched
Ties / thin evidence resolve to T3b, which is the conservative direction: it moves mass away from
the "generic coverage is genuinely related" reading rather than toward it.
"""
import csv,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from taxonomy import app_families,harm_families,affirmative

D=L.coding(); E=L.evidence(); B=L.descriptions(); A=L.aiid()
rows=[]
for d in D:
    if d['disclosure_code']!='T3': continue
    iid=d['incident_id']
    inc_txt=f"{d['title']} {B.get(iid,'')}"
    ev=(E.get(iid,{}) or {}).get('evidence','') or ''
    rat=(E.get(iid,{}) or {}).get('rationale','') or ''
    aff=affirmative(ev+" "+rat)
    i_app,i_harm=set(app_families(inc_txt)),set(harm_families(inc_txt))
    f_app,f_harm=set(app_families(aff)),set(harm_families(aff))
    app_match=sorted(i_app&f_app); harm_match=sorted(i_harm&f_harm)
    both=bool(app_match) and bool(harm_match)
    code='T3a' if both else 'T3b'
    thin=len(ev)<150
    if both:                       conf='high' if not thin else 'medium'
    elif app_match or harm_match:  conf='medium' if not thin else 'low'
    else:                          conf='low'
    frag=' '.join(aff.split())[:180]
    rows.append(dict(incident_id=iid,issuer=d['matched_company'],incident_date=d['incident_date'],
        severity=L.SEV.get(d['severity_tier'],d['severity_tier']),role=d['role'],
        incident_app_families='|'.join(sorted(i_app)),incident_harm_families='|'.join(sorted(i_harm)),
        filing_app_families='|'.join(sorted(f_app)),filing_harm_families='|'.join(sorted(f_harm)),
        app_family_matched='|'.join(app_match),harm_family_matched='|'.join(harm_match),
        t3_split=code,confidence=conf,evidence_chars=len(ev),supporting_fragment=frag,
        title=d['title'][:120]))
flds=list(rows[0].keys())
with open(L.out("t3_split.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=flds); w.writeheader(); w.writerows(rows)
import collections
c=collections.Counter(r['t3_split'] for r in rows)
cc=collections.Counter((r['t3_split'],r['confidence']) for r in rows)
print(f"T3 recoded: {len(rows)}  T3a={c['T3a']}  T3b={c['T3b']}   T3a share of T3 = {c['T3a']/len(rows):.1%}")
for k in sorted(cc): print("   ",k,cc[k])
print("wrote",L.out("t3_split.csv"))
