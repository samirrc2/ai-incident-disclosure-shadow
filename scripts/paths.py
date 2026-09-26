"""shared loaders. Never writes to data/; all derived outputs go to results/."""
import csv,json,glob,os,sys
_HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(_HERE)
sys.path.insert(0,_HERE)

def _pick(*cands):
    for p in cands:
        if os.path.isdir(p) or os.path.isfile(p):
            return p
    return cands[0]

CODING=_pick(f"{ROOT}/coding", f"{ROOT}/data/coding")
FRONTIERS=_pick(f"{ROOT}/frontiers", f"{ROOT}/data/frontiers")

def coding():
    return list(csv.DictReader(open(f"{ROOT}/data/disclosure_coding.csv",newline='',encoding='utf-8',errors='replace')))
def firmmap():
    return {m['incident_id']:m for m in csv.DictReader(open(f"{ROOT}/data/incident_firm_map.csv",newline='',encoding='utf-8',errors='replace'))}
def aiid():
    return {r['incident_id']:r for r in csv.DictReader(open(f"{ROOT}/data/inbox/aiid_incidents.csv",newline='',encoding='utf-8',errors='replace'))}
def evidence():
    E={}
    for f in sorted(glob.glob(f"{CODING}/results/b*.json")): E.update(json.load(open(f)))
    return E
def descriptions():
    B={}
    for f in sorted(glob.glob(f"{CODING}/batches/batch_*.json")):
        for r in json.load(open(f)): B[r['incident_id']]=r.get('description','')
    return B
SEV={"T1-limited":"sev_limited","T2-moderate":"sev_moderate","T3-severe":"sev_severe"}
def frozen(name):
    """Read-only input under data/."""
    return f"{ROOT}/data/{name}"
def out(name):
    """Derived CSV/JSON. Always results/, never data/."""
    os.makedirs(f"{ROOT}/results",exist_ok=True); return f"{ROOT}/results/{name}"
def res(name):
    os.makedirs(f"{ROOT}/results",exist_ok=True); return f"{ROOT}/results/{name}"
