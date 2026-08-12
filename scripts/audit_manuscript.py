#!/usr/bin/env python3
"""Manuscript-wide numerical consistency audit (source of truth).

Recomputes every headline value from the frozen inputs and asserts it equals the
value stated in the manuscript. Fails loudly on any mismatch so the paper, tables,
figures, and code cannot drift apart. Run: python3 scripts/audit_manuscript.py
"""
import csv, json, sys, math
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

rows = list(csv.DictReader(open(DATA / "disclosure_coding.csv")))
inc  = list(csv.DictReader(open(DATA / "inbox" / "aiid_incidents.csv")))

def cp(k, n):  # Clopper-Pearson two-sided 95%
    from scipy import stats
    lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
    return round(100 * k / n, 1), round(100 * lo, 1), round(100 * hi, 1)

N = len(rows)
tiers = Counter(r["disclosure_code"] for r in rows)
T1, T2, T3, T4 = tiers["T1"], tiers["T2"], tiers["T3"], tiers["T4"]
issuers = len({r["CIK"] for r in rows})
shadow_k = T3 + T4
sev = Counter(r["severity_tier"] for r in rows)
srole = Counter(r["role"] for r in rows)
cset_src = Counter(r["severity_source"] for r in rows)
cset_snapshot = sum(1 for r in inc if any((r.get(k, "") or "").strip() not in ("", "NA", "None", "nan")
                                          for k in r if k.startswith("cset_")))

# ---- FACTS recomputed from frozen data ----
facts = {
    "N matched":            N,
    "issuers":              issuers,
    "T1":                   T1,
    "T2":                   T2,
    "T3":                   T3,
    "T4":                   T4,
    "T3 share% (1dp)":      round(100 * T3 / N, 1),
    "T1 rate% (CP)":        cp(T1, N),
    "substantive rate% (CP)": cp(T1 + T2, N),
    "shadow rate% (CP)":    cp(shadow_k, N),
    "severe tier n":        sev["T3-severe"],
    "moderate tier n":      sev["T2-moderate"],
    "limited tier n":       sev["T1-limited"],
    "role developer n":     srole["developer"],
    "CSET severity (matched)": cset_src["CSET"],
    "rubric severity (matched)": cset_src["rubric"],
    "CSET classified (snapshot)": cset_snapshot,
}

# ---- What the MANUSCRIPT states (single source of truth to keep in sync) ----
manuscript = {
    "N matched":            307,
    "issuers":              21,
    "T1":                   4,
    "T2":                   3,
    "T3":                   278,
    "T4":                   22,
    "T3 share% (1dp)":      90.6,
    "T1 rate% (CP)":        (1.3, 0.4, 3.3),
    "substantive rate% (CP)": (2.3, 0.9, 4.6),
    "shadow rate% (CP)":    (97.7, 95.4, 99.1),
    "severe tier n":        42,
    "moderate tier n":      50,
    "limited tier n":       215,
    "role developer n":     58,
    "CSET severity (matched)": 40,
    "rubric severity (matched)": 267,
    "CSET classified (snapshot)": 213,
}

print(f"{'FACT':30s} {'RECOMPUTED':>18s}  {'MANUSCRIPT':>18s}  OK")
print("-" * 74)
ok = True
for key, mval in manuscript.items():
    fval = facts[key]
    match = (fval == mval)
    ok &= match
    print(f"{key:30s} {str(fval):>18s}  {str(mval):>18s}  {'OK' if match else 'FAIL'}")

# cross-check against committed result JSONs
res = json.load(open(ROOT / "pilot" / "results.json"))
print("\nresults.json present and loadable:", bool(res))

print("\n" + ("AUDIT PASS — manuscript numbers match the frozen data."
              if ok else "AUDIT FAIL — mismatch(es) above."))
sys.exit(0 if ok else 1)
