# Environment

The reproduction is **100% offline and deterministic** — a pure function of the frozen
inputs in `data/` and `coding/`. No API keys, network, or paid services are used.

## Pinned stack

`Dockerfile` mirrors the audited Code Ocean capsule
(https://doi.org/10.24433/CO.2340354.v1): a Python 3.12 base plus a minimal pinned
analysis stack — `numpy==2.2.6`, `scipy==1.14.1`, `matplotlib==3.9.2`, `pytest==8.3.3`.
Exact versions are also listed in `../environment.txt`.

## Reproduce with Docker

```bash
docker build -t incident-shadow -f environment/Dockerfile .
docker run --rm incident-shadow          # runs reproduce.sh
```

## Reproduce locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash reproduce.sh
```

The pipeline sets `MPLBACKEND=Agg` and a fixed seed (42); every reported statistic is
re-derived and checked by two independent verifiers
(`scripts/check_claims.py`, `scripts/check_claims_ext.py`).
