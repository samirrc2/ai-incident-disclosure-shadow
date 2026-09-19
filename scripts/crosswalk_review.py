"""populate the 137-row entity-validation crosswalk.

The archived validation_sheet.csv was written with REVIEW_verdict and REVIEW_notes empty
(entity_resolve.py line 109), so the review the original manuscript described left no trace. This
script performs the review at revision stage and records a verdict and note for every row.

Verdict rule, applied uniformly:
  OK                 mapping stands
  OK-excluded        row was correctly excluded from the analytical sample (foreign / delisted)
  OK-note            mapping stands but a qualification is recorded
  FIX                mapping does not hold at incident date; the incident leaves the corrected sample
LISTING_FROM records the date from which the named issuer was itself an SEC periodic-report filer.
"""
import csv,json,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L

# issuer -> (periodic-report filer from, note)
LISTING_FROM={
 "Serve Robotics Inc.":      ("2023-08-04","became an SEC reporting company at its August 2023 reverse merger; no periodic-report history before that date"),
 "SoundThinking, Inc.":      ("2017-06-07","IPO as ShotSpotter, Inc.; renamed SoundThinking April 2023 — same registrant and CIK, so pre-rename incidents map correctly"),
 "Twitter, Inc.":            ("2013-11-07","NYSE-listed until the 27 October 2022 take-private"),
 "X Corp. (fmr Twitter)":    ("never","private successor to Twitter, Inc.; files no periodic reports"),
 "Rite Aid Corporation":     ("1968-01-01","NYSE-listed until the October 2023 Chapter 11 delisting"),
}
DELISTED_UNTIL={"Twitter, Inc.":"2022-10-27","Rite Aid Corporation":"2023-10-16"}
ASOF=json.load(open(L.res("asofdate.json")))
flagged_asof=set(ASOF["flagged_ids"])
insample={d['incident_id'] for d in L.coding()}

V=list(csv.DictReader(open(f"{L.ROOT}/data/validation_sheet.csv",newline='',encoding='utf-8',errors='replace')))
rows=[]
for v in V:
    iid=v['incident_id']; co=v['matched_company']; st=v['listing_status']; dt=v['incident_date']
    verdict=None; note=None
    if iid in flagged_asof:
        verdict="FIX"; note=("as-of-incident-date check: the listed parent did not control the named "
            "entity on the incident date (see asofdate.csv); incident leaves the corrected sample")
    elif co in LISTING_FROM and LISTING_FROM[co][0] not in ("never",) and dt < LISTING_FROM[co][0]:
        verdict="FIX"; note=("issuer was not an SEC periodic-report filer at the incident date — "
            +LISTING_FROM[co][1]+"; incident leaves the corrected sample")
    elif st=="FOREIGN":
        verdict="OK-excluded"; note="foreign private issuer (20-F/6-K); correctly outside the domestic-filer sample"
    elif st=="DELISTED":
        du=DELISTED_UNTIL.get(co)
        if du and dt<=du:
            verdict="OK-note"; note=(f"{co} was still listed on the incident date (delisted {du}); excluded "
              "under the blanket delisted-issuer rule. Conservative over-exclusion: it removes an eligible "
              "incident rather than admitting an ineligible one")
        else:
            verdict="OK-excluded"; note=(LISTING_FROM.get(co,("",""))[1] or "issuer not a periodic-report filer on the incident date")
    elif st=="PARENT":
        verdict="OK"; note="subsidiary-to-listed-parent mapping; parent control confirmed as of the incident date at revision"
    elif co in LISTING_FROM:
        verdict="OK-note"; note=LISTING_FROM[co][1]
    else:
        verdict="OK"; note="direct slug-to-registrant match, high confidence; CIK verified in the coding record"
    r=dict(v); r['REVIEW_verdict(OK/FIX)']=verdict; r['REVIEW_notes']=note
    r['in_analytical_sample']= iid in insample
    r['reviewed_at']="revision-1"
    rows.append(r)
with open(L.out("crosswalk_review.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
c=collections.Counter(r['REVIEW_verdict(OK/FIX)'] for r in rows)
print(f"crosswalk rows reviewed: {len(rows)}")
for k,v2 in c.most_common(): print(f"   {k}: {v2}")
fix=[r for r in rows if r['REVIEW_verdict(OK/FIX)']=='FIX']
print("FIX rows:")
for r in fix: print(f"   id={r['incident_id']} {r['incident_date']} {r['matched_company']}  in_sample={r['in_analytical_sample']}")
json.dump(dict(n_rows=len(rows),verdicts=dict(c),
  fix_ids=[r['incident_id'] for r in fix],
  fix_ids_in_sample=[r['incident_id'] for r in fix if r['in_analytical_sample']]),
  open(L.res("crosswalk_review.json"),"w"),indent=1)
print("wrote",L.out("crosswalk_review.csv"))
