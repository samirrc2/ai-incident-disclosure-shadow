# Environment (Code Ocean–compatible)

`Dockerfile` matches the capsule environment that runs the fully-offline reproduction:
a Python 3.12 base from Code Ocean's registry plus a minimal pinned analysis stack
(`numpy==2.2.6`, `scipy==1.14.1`, `matplotlib==3.9.2`, `pytest==8.3.3`). No pandas,
statsmodels, or network libraries are needed.

Capsule mounts:

| Mount | Contents |
|-------|----------|
| `/code` | `src/` (analysis + verifiers), `scripts/reproduce.sh`, `provenance/`, `tests/`, `requirements.txt`, `run` |
| `/data` | frozen inputs: `raw_extracted/`, `coding_logs/`, `P13_disclosure_coding.csv`, map, validation, `MANIFEST.sha256` |
| `/results` | all generated outputs (tables, figures, verification logs) |

**Reproducible Run:** `/code/run` → `bash code/scripts/reproduce.sh`.

## Local development
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r code/requirements.txt
bash reproduce.sh
```
The run sets `PYTHONPATH=code/src`, `MPLBACKEND=Agg`, and fixed hash/seed env vars; it is 100% offline.
