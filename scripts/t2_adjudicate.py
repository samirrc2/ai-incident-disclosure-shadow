"""adjudication of the three T2 incidents.

Motivation: the stratified reliability sample gives T2 a one-vs-rest Cohen's kappa of -0.023; the
second coder agreed with none of the three pass-1 T2 codes. T2 supplies three of the seven
incidents in the substantive numerator, so each was re-read against the codebook definitions.

Codebook, as written: T1 requires that the filing identify the underlying event with sufficient
factual specificity, and explicitly does NOT require the filing to use the term "artificial
intelligence" -- "the event, system, product, or factual circumstances" may supply the connection.
T2 applies when a formal legal consequence is disclosed but the underlying event is not identified
to that standard.
"""
import csv,json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
ADJ={
 "733":dict(original="T2",adjudicated="T1",confidence="high",
   reason=("GM's Q1-2025 10-Q contingencies note names the product and the conduct: 'the collection "
     "and use of certain consumer data obtained through our former OnStar Smart Driver product', "
     "alongside the resolved FTC consent order. Under the codebook's own T1 rule the absence of "
     "AI framing is not disqualifying where the product and factual circumstances identify the "
     "event, and they do here. Recoded T1.")),
 "711":dict(original="T2",adjudicated="T2",confidence="medium",
   reason=("Tesla's FY2024 10-K discloses NHTSA Autopilot investigations, the December 2023 recall "
     "of approximately 2 million vehicles, and DOJ document requests as legal and regulatory "
     "contingencies. It identifies the system and the regulator but not the April 2024 "
     "recall-adequacy probe as a distinct event, so the legal-consequence reading stands. A "
     "reasonable coder could call this T1; the alternative is carried in the range reported in "
     "Section 4.1.")),
 "534":dict(original="T2",adjudicated="T2",confidence="high",
   reason=("Meta's FY2021 10-K discloses the September-2021 government investigations and the "
     "securities class actions collectively, without naming the Ohio Attorney General action or "
     "the underlying algorithm-and-minors allegations as an event. The consequence is disclosed, "
     "the incident is not. T2 stands.")),
}
D={d['incident_id']:d for d in L.coding()}
rows=[]
for iid,a in ADJ.items():
    d=D[iid]
    rows.append(dict(incident_id=iid,issuer=d['matched_company'],incident_date=d['incident_date'],
        original_code=a['original'],adjudicated_code=a['adjudicated'],changed=a['original']!=a['adjudicated'],
        confidence=a['confidence'],rationale=a['reason'],title=d['title'][:120]))
with open(L.out("t2_adjudication.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
ch=[r for r in rows if r['changed']]
print(f"T2 cases adjudicated: {len(rows)}; changed: {len(ch)}")
for r in rows: print(f"   id={r['incident_id']} {r['original_code']} -> {r['adjudicated_code']}  ({r['confidence']})  {r['issuer']}")
print("\nadjudicated tier counts: T1=%d  T2=%d  (substantive unchanged at 7)"%(4+len(ch),3-len(ch)))
json.dump({"n":len(rows),"n_changed":len(ch),"changed_ids":[r['incident_id'] for r in ch],
  "adjudicated_T1":4+len(ch),"adjudicated_T2":3-len(ch)},open(L.res("t2_adjudication.json"),"w"),indent=1)
print("wrote",L.out("t2_adjudication.csv"))
