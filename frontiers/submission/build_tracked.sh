#!/usr/bin/env bash
# Rebuild the tracked-changes PDF: the as-submitted manuscript against the current one.
# Builds in a temp directory so nothing is left behind. Run from this directory.
set -euo pipefail
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
cd "$(dirname "$0")"

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

latexdiff --type=UNDERLINE manuscript_v1_as_submitted.tex ../manuscript.tex \
  > "$T/manuscript_tracked.tex"

# Repair two artefacts of the diff itself; see fix_tracked.py for why.
python3 fix_tracked.py "$T/manuscript_tracked.tex" ../manuscript.tex

cp ../references.bib ../FrontiersinHarvard.cls ../Frontiers-Harvard.bst "$T/"
cp ../logo1.eps ../logo1.pdf ../logo2.eps ../logos.eps ../YM-logo.eps "$T/" 2>/dev/null || true
mkdir -p "$T/figures" && cp ../figures/*.png "$T/figures/"

cd "$T"
pdflatex -interaction=nonstopmode manuscript_tracked >/dev/null
bibtex manuscript_tracked >/dev/null 2>&1 || true
pdflatex -interaction=nonstopmode manuscript_tracked >/dev/null
pdflatex -interaction=nonstopmode manuscript_tracked >/dev/null
echo "  errors:   $(grep -c '^! ' manuscript_tracked.log || true)"
echo "  overfull: $(grep -c 'Overfull .hbox' manuscript_tracked.log || true)"
cd - >/dev/null

cp "$T/manuscript_tracked.tex" "$T/manuscript_tracked.pdf" .
echo "rebuilt manuscript_tracked.pdf"
