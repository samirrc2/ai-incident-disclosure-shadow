#!/usr/bin/env bash
# Rebuild manuscript.docx from manuscript.tex.
#
# This exists because the DOCX was produced by hand and then went stale: after the Code
# Ocean DOI was updated the Word file still said the DOI "will be added at proof stage",
# with nothing to flag the drift.
#
# pandoc's LaTeX reader silently DROPS any tabular containing \multicolumn -- this
# manuscript has 26 of them -- so the command is expanded to plain cells first, exactly as
# the Paper 2 builder does. Without that step several tables arrive as raw LaTeX text.
set -euo pipefail
cd "$(dirname "$0")"
command -v pandoc >/dev/null || { echo "pandoc not installed" >&2; exit 2; }

python3 - <<'PY'
import os, re, shutil, subprocess
TMP = "/tmp/_p13_docx"
os.makedirs(TMP, exist_ok=True)
s = open("manuscript.tex", encoding="utf-8").read()

def grab(t, i):
    """Return the balanced {...} group starting at i, and the index after it."""
    d = 0; st = i + 1
    while i < len(t):
        if t[i] == "{": d += 1
        elif t[i] == "}":
            d -= 1
            if d == 0: return t[st:i], i + 1
        i += 1
    raise ValueError("unbalanced brace")

out = []; i = 0; n = 0
while True:
    j = s.find("\\multicolumn", i)
    if j < 0:
        out.append(s[i:]); break
    out.append(s[i:j])
    span, k = grab(s, s.index("{", j))     # column span
    _, k = grab(s, k)                       # alignment, discarded
    body, k = grab(s, k)                    # cell content
    out.append(body + " & " * (int(span) - 1))
    n += 1; i = k
open(f"{TMP}/manuscript.tex", "w", encoding="utf-8").write("".join(out))
for f in ("references.bib",):
    shutil.copy(f, TMP)
for d in ("figures", "tables"):
    if os.path.isdir(d):
        shutil.copytree(d, f"{TMP}/{d}", dirs_exist_ok=True)
r = subprocess.run(["pandoc", "manuscript.tex", "--bibliography=references.bib",
                    "--citeproc", "--resource-path=.:figures:tables",
                    "-o", "manuscript.docx"],
                   cwd=TMP, capture_output=True, text=True)
if r.returncode:
    raise SystemExit("pandoc failed: " + r.stderr[:400])
shutil.copy(f"{TMP}/manuscript.docx", "manuscript.docx")
print(f"   expanded {n} multicolumn cells; manuscript.docx written")
PY
