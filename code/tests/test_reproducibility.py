"""Reproducibility tests — assert the paper's headline numbers from the regenerated outputs.
Run after code/scripts/reproduce.sh (which generates results/). Paths resolve from the repo root.
"""
import json, csv, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results"
DATA = ROOT / "data"

def _load(p):
    return json.load(open(p))

def test_coded_table_shape():
    rows = list(csv.DictReader(open(DATA / "P13_disclosure_coding.csv")))
    assert len(rows) == 307
    codes = [r["disclosure_code"] for r in rows]
    assert set(codes) <= {"T1", "T2", "T3", "T4"}
    from collections import Counter
    d = Counter(codes)
    assert (d["T1"], d["T2"], d["T3"], d["T4"]) == (4, 3, 278, 22)

def test_headline_results():
    R = _load(RES / "P13_results.json")
    assert R["N"] == 307
    assert R["distribution"] == {"T1": 4, "T2": 3, "T3": 278, "T4": 22}
    h = R["headline"]
    assert h["T1_specific"]["k"] == 4
    assert abs(h["T1_specific"]["rate"] - 0.013) < 0.002
    assert abs(h["shadow_T3plusT4"]["rate"] - 0.977) < 0.002
    lo, hi = h["shadow_T3plusT4"]["ci95"]
    assert lo < h["shadow_T3plusT4"]["rate"] < hi          # CI brackets estimate

def test_extended_concentration_and_tests():
    E = _load(RES / "P13_extended.json")
    assert E["concentration"]["n_issuers"] == 21
    assert abs(E["concentration"]["HHI"] - 0.1813) < 0.002
    assert abs(E["robustness_concentration"]["drop_top5"]["shadow"] - 0.9245) < 0.002
    # role is the significant stratum; severity is not
    assert E["formal_tests"]["by_role"][1] < 0.05
    assert E["formal_tests"]["by_severity"][1] > 0.05
    assert E["issuer_level"]["n_issuers_with_substantive"] == 4
    # clustered CI is wider than but consistent with the point estimate
    ci = E["clustered_inference"]["shadow_issuer_cluster_bootstrap"]["ci95"]
    assert ci[0] < 0.977 < ci[1] + 1e-9

def test_extended_reliability():
    RL = _load(RES / "P13_reliability_ext.json")
    assert RL["pass2_n"] == 68
    assert abs(RL["cohens_kappa"] - 0.726) < 0.01
    assert RL["gwet_ac1"] > RL["cohens_kappa"]             # prevalence-robust higher under T3 dominance
    assert RL["gate"].startswith("PASS")

def test_retrieval_validation_zero_false_negatives():
    E = _load(RES / "P13_extended.json")
    assert E["retrieval_validation"]["audited"] == 40
    assert E["retrieval_validation"]["false_negatives_found"] == 0

def test_window_robustness_monotone():
    E = _load(RES / "P13_extended.json")
    w = E["window_robustness"]
    assert w["shadow_12mo"] == w["shadow_18mo"] == w["shadow_24mo"]
    assert w["shadow_6mo"] >= w["shadow_12mo"]             # shortening only raises the shadow

def test_resolution_regenerated():
    assert (RES / "P13_incident_firm_map.regenerated.csv").exists()
    prim = [r for r in csv.DictReader(open(RES / "P13_incident_firm_map.regenerated.csv"))
            if r["listing_status"] in ("LISTED", "PARENT")]
    assert len(prim) == 307
