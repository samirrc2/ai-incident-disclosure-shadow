#!/usr/bin/env python3
"""p13_03_edgar_search — build the deterministic EDGAR full-text search plan for the pilot.

Reads a pilot subsample CSV with columns:
  incident_id, CIK, incident_date, specific_terms (| -separated phrases)
For each incident, emits (to pilot/P13_edgar_query_manifest.csv):
  - one SPECIFIC query per specific_terms phrase, restricted to CIK+forms+window
  - one GENERIC query (OR of generic AI terms), restricted to CIK+forms+window
Every row carries the exact efts URL, so results are reproducible: run each URL (via WebFetch
in the locked container, or requests on a networked host) and record hits.total.value + hit ids.

On a networked host, pass --run to execute with throttling (<=8 rps, UA, backoff).
"""
from __future__ import annotations
import sys, csv, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import PILOT, DISCLOSURE_FORMS, DISCLOSURE_HORIZON_MONTHS, SEC_USER_AGENT, SEC_MAX_RPS
from p13_lib import efts_url, disclosure_window, GENERIC_AI_TERMS

def build(subsample_csv: Path):
    rows = list(csv.DictReader(open(subsample_csv)))
    plan = []
    for r in rows:
        cik = r["CIK"]; iid = r["incident_id"]; idate = r["incident_date"]
        start, end = disclosure_window(idate, DISCLOSURE_HORIZON_MONTHS)
        for phrase in [p.strip() for p in (r.get("specific_terms","" ) or "").split("|") if p.strip()]:
            q = phrase if phrase.startswith('"') else f'"{phrase}"'
            plan.append(dict(incident_id=iid, kind="SPECIFIC", query=q, cik=cik,
                             startdt=start, enddt=end,
                             url=efts_url(q, cik=cik, forms=DISCLOSURE_FORMS, startdt=start, enddt=end)))
        gq = " OR ".join(GENERIC_AI_TERMS)
        plan.append(dict(incident_id=iid, kind="GENERIC", query=gq, cik=cik,
                         startdt=start, enddt=end,
                         url=efts_url(gq, cik=cik, forms=DISCLOSURE_FORMS, startdt=start, enddt=end)))
    return plan

def main():
    args = sys.argv[1:]
    run = "--run" in args
    args = [a for a in args if a != "--run"]
    sub = Path(args[0]) if args else (PILOT / "P13_pilot_subsample.csv")
    if not sub.exists():
        sys.exit(f"subsample not found: {sub}")
    plan = build(sub)
    man = PILOT / "P13_edgar_query_manifest.csv"
    with open(man, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["incident_id","kind","cik","startdt","enddt","query","url","hits_total","hit_ids"])
        w.writeheader()
        for p in plan:
            p = dict(p); p["hits_total"]=""; p["hit_ids"]=""
            if run:
                import requests  # networked host only
                h = {"User-Agent": SEC_USER_AGENT, "Accept-Encoding": "gzip, deflate"}
                for attempt in range(5):
                    resp = requests.get(p["url"], headers=h, timeout=30)
                    if resp.status_code == 200:
                        d = resp.json()
                        p["hits_total"] = d.get("hits",{}).get("total",{}).get("value","")
                        p["hit_ids"] = "; ".join(hh.get("_id","") for hh in d.get("hits",{}).get("hits",[])[:10])
                        break
                    time.sleep(2 ** attempt)
                time.sleep(1.0 / SEC_MAX_RPS)
            w.writerow(p)
    print(f"wrote {len(plan)} queries -> {man}" + ("  [executed]" if run else "  [urls only]"))

if __name__ == "__main__":
    main()
