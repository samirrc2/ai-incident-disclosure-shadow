#!/usr/bin/env python3
"""Generate Appendix A: the 40 matched incidents with CSET severity.
Three columns: AIID ID | CSET classification (harm level; tangible harm) | Study severity.
CSET values reproduced verbatim; nothing inferred. Emits markdown + LaTeX longtable rows."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
coded = [r for r in csv.DictReader(open(ROOT/"data/disclosure_coding.csv")) if r["severity_source"]=="CSET"]
inc = {r["incident_id"]: r for r in csv.DictReader(open(ROOT/"data/inbox/aiid_incidents.csv"))}
TIER = {"T3-severe":"Severe","T2-moderate":"Moderate","T1-limited":"Limited"}
rows = sorted(coded, key=lambda r: int(r["incident_id"]))
assert len(rows)==40, f"expected 40, got {len(rows)}"

# internal consistency check (not published): identical CSET composite -> identical severity
seen={}
for r in rows:
    s=inc[r["incident_id"]]
    key=(s.get("cset_harm_level","").strip(), s.get("cset_tangible_harm","").strip())
    sev=TIER[r["severity_tier"]]
    if key in seen and seen[key]!=sev:
        raise SystemExit(f"INCONSISTENT: {key} -> {seen[key]} and {sev} (incident {r['incident_id']})")
    seen[key]=sev

md=["| AIID Incident ID | CSET classification (harm level; tangible harm) | Study severity |","|---|---|---|"]
tex=[]
for r in rows:
    s=inc[r["incident_id"]]
    cset=f"{s.get('cset_harm_level','').strip()}; {s.get('cset_tangible_harm','').strip()}"
    md.append(f"| {r['incident_id']} | {cset} | {TIER[r['severity_tier']]} |")
    tex.append(f"{r['incident_id']} & {cset} & {TIER[r['severity_tier']]} \\\\")
OUT = ROOT/"frontiers"/"submission"
OUT.mkdir(parents=True, exist_ok=True)
(OUT/"cset_rows.tex").write_text("\n".join(tex)+"\n")
(OUT/"cset_rows.md").write_text("\n".join(md)+"\n")
print("\n".join(md))
print(f"\n[consistency OK] {len(rows)} rows; no identical CSET composite maps to different severity.")
