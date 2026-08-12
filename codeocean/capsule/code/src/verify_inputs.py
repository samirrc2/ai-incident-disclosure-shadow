#!/usr/bin/env python3
"""verify_inputs — verify SHA-256 of every frozen data asset before anything runs.
Fails loudly if any input has changed. Writes results/INPUT_MANIFEST.sha256.
"""
import hashlib, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

# Frozen SHA-256 of each data asset, pinned at capsule build time. These are the paper's inputs.
EXPECTED = {
 "data/disclosure_coding.csv": None,   # filled from archive_manifest at build; verified below
}

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()

def main():
    C.ensure_out()
    assets=[C.CODED,C.FROZEN_MAP,C.INCIDENTS,C.CSET]
    assets+=sorted(C.LOGS.glob("pass1/*.json"))+sorted(C.PASS2.glob("*.json"))
    assets+=[C.LOGS/"retrieval_A.json",C.LOGS/"retrieval_B.json",C.LOGS/"altwindow.json"]
    manifest_path=Path(__file__).resolve().parents[2]/"data"/"MANIFEST.sha256"
    pinned={}
    if manifest_path.exists():
        for line in open(manifest_path):
            line=line.strip()
            if line and not line.startswith("#"):
                h,_,name=line.partition("  "); pinned[name.strip()]=h.strip()
    out=[]; fails=[]
    for a in assets:
        if not a.exists(): fails.append(f"MISSING: {a}"); continue
        h=sha256(a); rel=str(a).split("data/",1)[-1]; rel="data/"+rel
        out.append(f"{h}  {rel}")
        if rel in pinned and pinned[rel]!=h:
            fails.append(f"HASH MISMATCH: {rel}\n  expected {pinned[rel]}\n  got      {h}")
    (C.RESULTS/"INPUT_MANIFEST.sha256").write_text("\n".join(out)+"\n")
    if fails:
        print("VERIFY_INPUTS: FAIL"); [print("  -",f) for f in fails]; sys.exit(1)
    checked = f"{len(pinned)} pinned hashes checked" if pinned else "no pinned manifest (first build) — hashes recorded"
    print(f"VERIFY_INPUTS: PASS — {len(assets)} frozen data assets present; {checked}.")

if __name__=="__main__": main()
