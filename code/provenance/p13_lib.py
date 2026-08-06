"""p13_lib — shared helpers for the Paper 13 pilot pipeline.

Pure-stdlib where possible so the entity/EDGAR-URL logic is testable without network.
"""
from __future__ import annotations
import hashlib, json, re, urllib.parse
from datetime import date
from dateutil.relativedelta import relativedelta  # type: ignore

# ----------------------------- provenance -----------------------------
def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def append_manifest(manifest_path, filename, sha256, note=""):
    """Append-only SHA-256 manifest for data/raw."""
    line = f"{sha256}  {filename}  {note}".rstrip() + "\n"
    with open(manifest_path, "a") as f:
        f.write(line)

# ----------------------------- CIK helpers -----------------------------
def pad_cik(cik) -> str:
    """SEC EDGAR full-text search requires 10-digit zero-padded CIK."""
    return str(int(cik)).zfill(10)

# ----------------------------- EDGAR EFTS URL builder -----------------------------
EFTS = "https://efts.sec.gov/LATEST/search-index"

def efts_url(q: str, cik=None, forms="8-K,10-K,10-Q",
             startdt: str | None = None, enddt: str | None = None, frm: int = 0) -> str:
    """Deterministic EDGAR full-text search URL. Logging these URLs makes every
    disclosure-detection result reproducible."""
    params = {"q": q, "forms": forms}
    if cik is not None:
        params["ciks"] = pad_cik(cik)
    if startdt and enddt:
        params["dateRange"] = "custom"; params["startdt"] = startdt; params["enddt"] = enddt
    if frm:
        params["from"] = str(frm)
    # quote_via=quote keeps the phrase quotes (%22) and boolean operators intact
    return EFTS + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

def disclosure_window(incident_date: str, months: int = 12) -> tuple[str, str]:
    y, m, d = map(int, incident_date[:10].split("-"))
    start = date(y, m, d)
    end = start + relativedelta(months=months)
    return start.isoformat(), end.isoformat()

# ----------------------------- severity rubric -----------------------------
# Transparent 3-tier rubric (codebook §CODEBOOK). Applied to each incident from its
# AIID harm classification + report evidence. Deterministic given the coded harm fields.
SEVERITY_TIERS = {
    "T3-severe":   "Death, serious physical injury, or large-scale deprivation of a legal "
                   "right / essential service / financial harm (e.g., wrongful benefit denial "
                   "at scale, wrongful arrest, safety-critical failure).",
    "T2-moderate": "Material individual harm without death/serious injury, or documented "
                   "discrimination / privacy violation affecting an identifiable group.",
    "T1-limited":  "Reputational, service-quality, or contained harm; no documented physical "
                   "or large-scale rights/financial harm.",
}

# ----------------------------- generic AI-incident query terms -----------------------------
# Used in addition to incident-specific terms for DISCLOSED-GENERIC detection.
GENERIC_AI_TERMS = [
    '"artificial intelligence"', '"machine learning"', '"algorithm"',
    '"automated decision"', '"AI system"', '"model risk"',
]

def norm_name(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\b(inc|corp|corporation|co|company|ltd|llc|plc|holdings|group|the)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


if __name__ == "__main__":
    # self-test (no network)
    assert pad_cik(320193) == "0000320193"
    u = efts_url('"Cruise" "pedestrian"', cik=40730, forms="8-K",
                 startdt="2023-10-02", enddt="2024-10-02")
    assert "ciks=0000040730" in u and "dateRange=custom" in u and "%22Cruise%22" in u
    s, e = disclosure_window("2023-10-02", 12)
    assert s == "2023-10-02" and e == "2024-10-02"
    print("p13_lib self-test OK")
    print(u)
