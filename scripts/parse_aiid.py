#!/usr/bin/env python3
"""parse_aiid — extract the pinned AIID mongodump snapshot and emit a flat incidents table.

Snapshot layout (mongodump): mongodump_full_snapshot/incidents.csv with columns
  _id, incident_id, date, reports, "Alleged deployer of AI system",
  "Alleged developer of AI system", "Alleged harmed or nearly harmed parties", description, title
Entity fields are JSON arrays of canonical slugs, e.g. ["cruise"], ["microsoft-research","boston-university"].
CSET v1 harm taxonomy joined where available (classifications_CSETv1.csv, keyed by Incident ID).

Output: data/inbox/aiid_incidents.csv (incident_id, date, title, deployers, developers,
        harmed_parties, cset_harm_level, cset_tangible_harm, cset_lives_lost, cset_injuries,
        cset_rights_violation, cset_minor, cset_critical_services)
Also appends the snapshot SHA-256 to data/raw/MANIFEST.sha256 (append-only).
"""
from __future__ import annotations
import sys, csv, json, tarfile, glob
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import RAW, INBOX
from shadow_lib import sha256_file, append_manifest
csv.field_size_limit(10_000_000)

def parse_slugs(s):
    s=(s or "").strip()
    if not s: return []
    try:
        v=json.loads(s); return v if isinstance(v,list) else [v]
    except json.JSONDecodeError:
        return [t.strip() for t in s.strip("[]").replace('"','').split(",") if t.strip()]

def main():
    snaps=sorted(glob.glob(str(RAW/"backup-*.tar.bz2")))
    if not snaps: sys.exit("No snapshot in data/raw/. Fetch it (recon recon.md section 5).")
    snap=snaps[-1]
    sha=sha256_file(snap); append_manifest(RAW/"MANIFEST.sha256", Path(snap).name, sha, "AIID full DB snapshot (mongodump)")
    ex=RAW/"extracted"; ex.mkdir(exist_ok=True)
    with tarfile.open(snap,"r:*") as t: t.extractall(ex)
    base=next(ex.glob("*/incidents.csv")).parent
    inc=list(csv.DictReader(open(base/"incidents.csv")))
    # CSET join
    cset={}
    cp=base/"classifications_CSETv1.csv"
    if cp.exists():
        for r in csv.DictReader(open(cp)):
            cset[str(r.get("Incident ID","")).strip()]=r
    INBOX.mkdir(parents=True,exist_ok=True)
    out=INBOX/"aiid_incidents.csv"
    cols=["incident_id","date","title","deployers","developers","harmed_parties",
          "cset_harm_level","cset_tangible_harm","cset_lives_lost","cset_injuries",
          "cset_rights_violation","cset_minor","cset_critical_services"]
    n=0
    with open(out,"w",newline="") as f:
        w=csv.writer(f); w.writerow(cols)
        for x in inc:
            iid=str(x["incident_id"]); c=cset.get(iid,{})
            w.writerow([iid,(x["date"] or "")[:10],x.get("title",""),
                json.dumps(parse_slugs(x["Alleged deployer of AI system"])),
                json.dumps(parse_slugs(x["Alleged developer of AI system"])),
                json.dumps(parse_slugs(x["Alleged harmed or nearly harmed parties"])),
                (c.get("AI Harm Level","") or "").strip(),(c.get("Tangible Harm","") or "").strip(),
                (c.get("Lives Lost","") or "").strip(),(c.get("Injuries","") or "").strip(),
                (c.get("Rights Violation","") or "").strip(),(c.get("Involving Minor","") or "").strip(),
                (c.get("Impact on Critical Services","") or "").strip()])
            n+=1
    print(f"snapshot={Path(snap).name} sha256={sha[:16]}  parsed {n} incidents ({sum(1 for _ in cset)} with CSET) -> {out}")

if __name__=="__main__": main()
