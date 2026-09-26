#!/usr/bin/env bash
# Assemble a Code Ocean capsule (code / data / environment only).
#
# Code Ocean's UI has three buckets. Extra top-level folders (coding/, frontiers/,
# reproduce.sh at the repo root) never arrive. This build nests those under data/
# and puts the run script plus reproduce.sh in code/.
#
# Usage:  bash scripts/build_capsule.sh
# Upload: unzip codeocean/capsule_v3.zip into Code Ocean (code, data, environment).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
C="codeocean/capsule_v3"

rm -rf "$C"
mkdir -p "$C"/code \
         "$C"/data/{inbox,coding/{results,batches},frontiers/{figures,submission,tables},docs,pilot} \
         "$C"/environment \
         "$C"/metadata \
         "$C"/results

# --- Code (every analysis script + the Code Ocean entry point) ----------------
cp scripts/*.py "$C/code/"
rm -f "$C/code/build_capsule.sh"
cp requirements.txt LICENSE CITATION.cff "$C/code/"
cp codeocean/capsule_meta/README.md "$C/code/README.md"

# --- Data: frozen tables + coding logs + manuscript (the thing we verify) ------
for f in disclosure_coding.csv incident_firm_map.csv incidents.csv validation_sheet.csv \
         entity_audit_return.csv entity_audit_adjudication.csv \
         retrieval_A.json retrieval_B.json retrieval_validation_sample.json \
         altwindow_substantive.json MANIFEST.sha256; do
    cp "data/$f" "$C/data/"
done
cp data/inbox/aiid_incidents.csv "$C/data/inbox/"
cp coding/results/*.json  "$C/data/coding/results/"
cp coding/batches/*.json  "$C/data/coding/batches/"
cp -r coding/pass2        "$C/data/coding/" 2>/dev/null || true
cp frontiers/manuscript.tex frontiers/references.bib \
   frontiers/FrontiersinHarvard.cls frontiers/Frontiers-Harvard.bst "$C/data/frontiers/"
cp frontiers/figures/*.png "$C/data/frontiers/figures/" 2>/dev/null || true
cp frontiers/submission/supplementary.tex "$C/data/frontiers/submission/"
cp frontiers/submission/SUBMISSION_README.md "$C/data/frontiers/submission/" 2>/dev/null || true
cp frontiers/submission/response_to_reviewers.md "$C/data/frontiers/submission/" 2>/dev/null || true
cp docs/CITATION_VERIFICATION.md "$C/data/docs/"
cp README.md DATA_AVAILABILITY.md "$C/data/"
cp -R pilot/. "$C/data/pilot/" 2>/dev/null || true

# --- Environment: Code Ocean base image (not python:3.12-slim) ----------------
cp codeocean/capsule/environment/Dockerfile "$C/environment/Dockerfile"
cp codeocean/capsule_meta/metadata.yml "$C/metadata/" 2>/dev/null || true

# reproduce.sh lives in code/ and cds to the capsule root
python3 - "$C/code/reproduce.sh" reproduce.sh <<'PY'
import sys
src, dst = sys.argv[2], sys.argv[1]
s = open(src, encoding="utf-8").read().replace("python3 scripts/", "python3 code/")
# run from capsule root even though this file sits in code/
s = s.replace('cd "$(dirname "$0")"', 'cd "$(cd "$(dirname "$0")/.." && pwd)"', 1)
out = []
for line in s.split("\n"):
    if line.startswith(("python3 code/make_tables_tex.py", "python3 code/supplementary.py")):
        out.append("# " + line + "   # typesetting: the capsule regenerates results only")
    else:
        out.append(line)
open(dst, "w", encoding="utf-8").write("\n".join(out))
PY

cat > "$C/code/run" <<'SH'
#!/usr/bin/env bash
# Code Ocean Reproducible Run entry point.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export MPLBACKEND=Agg PYTHONHASHSEED=0
export PYTHONUNBUFFERED=1
bash code/reproduce.sh
echo
echo "All regenerated results are under results/. Figures are in results/figures/."
SH
chmod +x "$C/code/run" "$C/code/reproduce.sh"

# Zip with the three Code Ocean buckets at the top level
( cd "$C" && zip -qr ../capsule_v3.zip code data environment metadata results )
echo "built $C  ($(du -sh "$C" | cut -f1))"
echo "zip    codeocean/capsule_v3.zip  ($(du -h codeocean/capsule_v3.zip | cut -f1))"
echo "verify:  (cd $C && bash code/run)"
