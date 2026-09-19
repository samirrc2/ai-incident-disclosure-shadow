"""shared loaders. Never writes to data/; all derived outputs go to data/."""
import csv,json,glob,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(ROOT,"scripts"))
def coding():
    return list(csv.DictReader(open(f"{ROOT}/data/disclosure_coding.csv",newline='',encoding='utf-8',errors='replace')))
def firmmap():
    return {m['incident_id']:m for m in csv.DictReader(open(f"{ROOT}/data/incident_firm_map.csv",newline='',encoding='utf-8',errors='replace'))}
def aiid():
    return {r['incident_id']:r for r in csv.DictReader(open(f"{ROOT}/data/inbox/aiid_incidents.csv",newline='',encoding='utf-8',errors='replace'))}
def evidence():
    E={}
    for f in sorted(glob.glob(f"{ROOT}/coding/results/b*.json")): E.update(json.load(open(f)))
    return E
def descriptions():
    B={}
    for f in sorted(glob.glob(f"{ROOT}/coding/batches/batch_*.json")):
        for r in json.load(open(f)): B[r['incident_id']]=r.get('description','')
    return B
SEV={"T1-limited":"sev_limited","T2-moderate":"sev_moderate","T3-severe":"sev_severe"}
def out(name): 
    os.makedirs(f"{ROOT}/data",exist_ok=True); return f"{ROOT}/data/{name}"
def res(name):
    os.makedirs(f"{ROOT}/results",exist_ok=True); return f"{ROOT}/results/{name}"
