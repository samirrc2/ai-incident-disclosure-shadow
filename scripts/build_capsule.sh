#!/usr/bin/env bash
# Assemble the Code Ocean capsule from this repository.
#
# The capsule REGENERATES THE RESULTS of the article and verifies the manuscript's numbers
# against them. It does not typeset the paper: the manuscript and supplementary sources are
# copied in read-only, as the thing being checked.
#
# The capsule is a build product and is not tracked in git. Run this, then upload
# codeocean/capsule_v3/ to Code Ocean.
#
# Usage:  bash scripts/build_capsule.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
C="codeocean/capsule_v3"

rm -rf "$C"
mkdir -p "$C"/{code,data/inbox,results,environment,metadata,docs,pilot,recon} \
         "$C"/coding/{results,batches} \
         "$C"/frontiers/{figures,submission,tables}

# --- the pipeline ---------------------------------------------------------------------
cp scripts/*.py "$C/code/"
rm -f "$C/code/build_capsule.sh"

# --- inputs ---------------------------------------------------------------------------
# Frozen tables, the audit material no script can regenerate, and the manifest that pins
# all of it. The derived tables are deliberately NOT copied: the run must rebuild them.
for f in disclosure_coding.csv incident_firm_map.csv incidents.csv validation_sheet.csv \
         entity_audit_return.csv entity_audit_adjudication.csv \
         retrieval_A.json retrieval_B.json retrieval_validation_sample.json \
         altwindow_substantive.json MANIFEST.sha256; do
    cp "data/$f" "$C/data/"
done
cp data/inbox/aiid_incidents.csv "$C/data/inbox/"
cp coding/results/*.json  "$C/coding/results/"
cp coding/batches/*.json  "$C/coding/batches/"
cp -r coding/pass2        "$C/coding/" 2>/dev/null || true
cp pilot/*.md pilot/*.csv "$C/pilot/" 2>/dev/null || true
cp recon/*.md             "$C/recon/" 2>/dev/null || true

# --- the article, read-only, as the thing being verified -------------------------------
cp frontiers/manuscript.tex frontiers/references.bib \
   frontiers/FrontiersinHarvard.cls frontiers/Frontiers-Harvard.bst "$C/frontiers/"
cp frontiers/logo*.eps frontiers/logo1.pdf frontiers/logos.eps frontiers/YM-logo.eps \
   "$C/frontiers/" 2>/dev/null || true
cp frontiers/submission/supplementary.tex "$C/frontiers/submission/"
cp docs/CITATION_VERIFICATION.md "$C/docs/"

# --- capsule furniture ------------------------------------------------------------------
cp reproduce.sh requirements.txt LICENSE CITATION.cff "$C/"
cp environment/Dockerfile "$C/environment/"
cp codeocean/capsule_meta/metadata.yml "$C/metadata/" 2>/dev/null || \
  cp metadata/metadata.yml "$C/metadata/"
cp codeocean/capsule_meta/README.md "$C/" 2>/dev/null || true

# The capsule runs scripts from code/, not scripts/. Typesetting steps are dropped: the
# capsule regenerates results, it does not build the paper.
python3 - "$C/reproduce.sh" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read().replace("python3 scripts/", "python3 code/")
out = []
for line in s.split("\n"):
    if line.startswith(("python3 code/make_tables_tex.py", "python3 code/supplementary.py")):
        out.append("# " + line + "   # typesetting: the capsule regenerates results only")
    else:
        out.append(line)
open(p, "w", encoding="utf-8").write("\n".join(out))
PY

cat > "$C/code/run" <<'SH'
#!/usr/bin/env bash
# Code Ocean entry point. Regenerates the results, then verifies the article against them.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export MPLBACKEND=Agg PYTHONHASHSEED=0
bash reproduce.sh
mkdir -p results/figures
cp -f frontiers/figures/*.png results/figures/ 2>/dev/null || true
echo
echo "All regenerated results are under results/. Figures are in results/figures/."
SH
chmod +x "$C/code/run"

echo "built $C  ($(du -sh "$C" | cut -f1))"
echo "verify it with:  (cd $C && bash code/run)"
