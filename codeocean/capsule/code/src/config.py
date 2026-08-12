"""config — single source of paths for the Code Ocean capsule.

Layout (Code Ocean mounts /code, /data, /results at root; the run script cds to the repo
root so these relative paths resolve there, and to the capsule root locally):
  data/                     frozen, read-only inputs
    raw_extracted/          extracted AIID CSVs (incidents.csv, classifications_CSETv1.csv)
    coding_logs/            per-incident EDGAR search records (pass1/, pass2/) + validation JSONs
    disclosure_coding.csv    frozen coded table (the "labels"; see archive_manifest.md)
    incident_firm_map.csv    frozen entity-resolution map
  results/                  all generated outputs (byte-identical across runs)
"""
import os
from pathlib import Path

SEED = 42

DATA    = Path(os.environ.get("DATA", "data"))
RESULTS = Path(os.environ.get("RESULTS", "results"))
RAWX    = DATA / "raw_extracted"
LOGS    = DATA / "coding_logs"
PASS2   = LOGS / "pass2"
FIGS    = RESULTS / "figures"

# frozen inputs
CODED      = DATA / "disclosure_coding.csv"
FROZEN_MAP = DATA / "incident_firm_map.csv"
INCIDENTS  = RAWX / "incidents.csv"
CSET       = RAWX / "classifications_CSETv1.csv"

# generated outputs
RESULTS_JSON = RESULTS / "results.json"
RESULTS_MD   = RESULTS / "results.md"
EXT_JSON     = RESULTS / "extended.json"
EXT_MD       = RESULTS / "extended.md"
REL_JSON     = RESULTS / "reliability_ext.json"
REL_MD       = RESULTS / "reliability_ext.md"
MAP_REGEN    = RESULTS / "incident_firm_map.regenerated.csv"
CODED_REBUILT= RESULTS / "disclosure_coding.rebuilt.csv"

def ensure_out():
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
