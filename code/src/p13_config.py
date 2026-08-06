"""p13_config — single source of paths for the Code Ocean capsule.

Layout (Code Ocean mounts /code, /data, /results at root; the run script cds to the repo
root so these relative paths resolve there, and to the capsule root locally):
  data/                     frozen, read-only inputs
    raw_extracted/          extracted AIID CSVs (incidents.csv, classifications_CSETv1.csv)
    coding_logs/            per-incident EDGAR search records (pass1/, pass2/) + validation JSONs
    P13_disclosure_coding.csv    frozen coded table (the "labels"; see archive_manifest.md)
    P13_incident_firm_map.csv    frozen entity-resolution map
  results/                  all generated outputs (byte-identical across runs)
"""
import os
from pathlib import Path

SEED = 42

DATA    = Path(os.environ.get("P13_DATA", "data"))
RESULTS = Path(os.environ.get("P13_RESULTS", "results"))
RAWX    = DATA / "raw_extracted"
LOGS    = DATA / "coding_logs"
PASS2   = LOGS / "pass2"
FIGS    = RESULTS / "figures"

# frozen inputs
CODED      = DATA / "P13_disclosure_coding.csv"
FROZEN_MAP = DATA / "P13_incident_firm_map.csv"
INCIDENTS  = RAWX / "incidents.csv"
CSET       = RAWX / "classifications_CSETv1.csv"

# generated outputs
RESULTS_JSON = RESULTS / "P13_results.json"
RESULTS_MD   = RESULTS / "P13_results.md"
EXT_JSON     = RESULTS / "P13_extended.json"
EXT_MD       = RESULTS / "P13_extended.md"
REL_JSON     = RESULTS / "P13_reliability_ext.json"
REL_MD       = RESULTS / "P13_reliability_ext.md"
MAP_REGEN    = RESULTS / "P13_incident_firm_map.regenerated.csv"
CODED_REBUILT= RESULTS / "P13_disclosure_coding.rebuilt.csv"

def ensure_out():
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
