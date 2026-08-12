"""Shared config. No secrets here; keys (if ever needed) load from env."""
from pathlib import Path

SEED = 42
# SEC fair-access: declared UA with contact, throttle <=8 req/s, backoff on 429/403.
SEC_USER_AGENT = "Paper13 AI-Incident-Disclosure Research (samir.chincholikar@gmail.com)"
SEC_MAX_RPS = 8
EDGAR_EFTS = "https://efts.sec.gov/LATEST/search-index"
SEC_TICKERS = "https://www.sec.gov/files/company_tickers.json"
AIID_SNAPSHOT_INDEX = "https://incidentdatabase.ai/research/snapshots/"

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
INBOX = DATA / "inbox"
PILOT = ROOT / "pilot"
RECON = ROOT / "recon"

INCIDENT_WINDOW = ("2019-01-01", "2026-12-31")
DISCLOSURE_FORMS = "8-K,10-K,10-Q"
DISCLOSURE_HORIZON_MONTHS = 12
