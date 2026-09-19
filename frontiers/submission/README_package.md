# Revision package

| File | What it is |
|---|---|
| `../manuscript.pdf` | **The revised manuscript.** 25 pp. This is the paper. |
| `manuscript_v1_as_submitted.pdf` | The manuscript exactly as first submitted, 18 pp, taken from the commit that was sent to the journal. |
| `manuscript_tracked.pdf` | v1 against the current manuscript, latexdiff. 28 pp. |
| `supplementary.pdf` | Supplementary Tables S1-S9. |
| `response_to_reviewers.md` | Point-by-point response to both referees. |
| `cover_letter.pdf` | Cover letter. |

`manuscript_v1_as_submitted.tex` and `references_v1_as_submitted.bib` are the frozen v1
sources, kept so the tracked-changes PDF stays reproducible after the revision was
promoted over `frontiers/manuscript.tex`.

Run `./build_tracked.sh` to regenerate `manuscript_tracked.pdf` after any edit to the
manuscript. It builds in a temp directory and leaves nothing behind.
