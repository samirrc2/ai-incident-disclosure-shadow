#!/usr/bin/env python3
"""code_shadow — compute the pilot shadow rate from the two-pass coded table.

Input : pilot/pilot_shadow_table.csv with (at least) columns:
  incident_id, matched_company, CIK, incident_date, severity_tier,
  pass1_code, pass2_code, final_code   where *_code in
  {DISCLOSED-SPECIFIC, DISCLOSED-GENERIC, NO-DISCLOSURE-LOCATED}
Output: pilot/pilot_shadow_table.md — overall + by-severity disclosure/shadow rates,
  inter-pass agreement, exact counts. All numbers computed here (seed not needed; deterministic).
"""
from __future__ import annotations
import sys, csv
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import PILOT

CODES = ["DISCLOSED-SPECIFIC", "DISCLOSED-GENERIC", "NO-DISCLOSURE-LOCATED"]

def rate(rows, pred):
    n = len(rows)
    k = sum(1 for r in rows if pred(r))
    return k, n, (k / n if n else 0.0)

def main():
    src = PILOT / "pilot_shadow_table.csv"
    if not src.exists():
        sys.exit("coded table not found.")
    rows = list(csv.DictReader(open(src)))
    for r in rows:
        r["final_code"] = r.get("final_code") or r.get("pass1_code")

    disclosed = lambda r: r["final_code"].startswith("DISCLOSED")
    specific  = lambda r: r["final_code"] == "DISCLOSED-SPECIFIC"
    noloc     = lambda r: r["final_code"] == "NO-DISCLOSURE-LOCATED"

    agree = sum(1 for r in rows if r.get("pass1_code") == r.get("pass2_code"))
    lines = []
    lines.append("# Shadow Measurement Results\n")
    lines.append(f"_n = {len(rows)} incidents; two independent coding passes; "
                 f"inter-pass agreement = {agree}/{len(rows)} "
                 f"({agree/len(rows)*100:.0f}%). Codes resolved by written rationale where they differ._\n")

    k, n, p = rate(rows, disclosed)
    lines.append(f"**Any related disclosure located (SPECIFIC or GENERIC): {k}/{n} = {p*100:.0f}%**")
    lines.append(f"**Shadow rate (no related disclosure located): {n-k}/{n} = {(1-p)*100:.0f}%**")
    ks, _, ps = rate(rows, specific)
    lines.append(f"Of which incident-SPECIFIC disclosure: {ks}/{n} = {ps*100:.0f}%\n")

    lines.append("## By severity tier\n")
    lines.append("| Tier | n | disclosed (any) | of which specific | no disclosure located | shadow rate |")
    lines.append("|---|---|---|---|---|---|")
    by = defaultdict(list)
    for r in rows: by[r.get("severity_tier","?")].append(r)
    for tier in ["T3-severe", "T2-moderate", "T1-limited"]:
        g = by.get(tier, [])
        if not g:
            lines.append(f"| {tier} | 0 | – | – | – | – |"); continue
        kd,_,pd = rate(g, disclosed); ksp,_,_ = rate(g, specific); kn,_,pn = rate(g, noloc)
        lines.append(f"| {tier} | {len(g)} | {kd} ({pd*100:.0f}%) | {ksp} | {kn} | {pn*100:.0f}% |")

    lines.append("\n## Code distribution\n")
    dist = Counter(r["final_code"] for r in rows)
    for c in CODES:
        lines.append(f"- {c}: {dist.get(c,0)}")

    out = PILOT / "pilot_shadow_table.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out}")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
