# The AI Incident Disclosure Shadow — reproducibility capsule

Tracking AI Incidents into U.S. Securities Filings.
Samir Chincholikar and Robin Chawla.

## What this capsule does

It **regenerates the results** of the article from the frozen inputs, then checks the
article's reported numbers against what it regenerated. It does not typeset the paper; the
manuscript and supplementary sources ship read-only, as the thing being checked.

Press **Reproducible Run**. It runs offline and takes a few minutes.

Headline result, printed at the end of the run:

    incident-specific disclosure (T1)   4/307  = 1.3%  (Clopper-Pearson 95% CI 0.4-3.3)
    substantive disclosure (T1+T2)      7/307  = 2.3%  (0.9-4.6)
    AI incident disclosure shadow     300/307  = 97.7% (95.4-99.1)
    at most weakly related language   216/307  = 70.4% (64.9-75.4)

## Layout

    code/        the analysis pipeline, 29 steps driven by reproduce.sh
    data/        frozen inputs, hashed in data/MANIFEST.sha256
    coding/      per-incident filing-search records and coding batches
    frontiers/   the manuscript and supplementary sources, read-only, plus the figures
    results/     everything the run produces
    docs/        the citation verification record

The run begins by checking every frozen input against its SHA-256 and stops if any differs.

## What the run checks

After rebuilding, `code/verify_all.py` applies 73 standing checks: every number in the
manuscript traces to a generated output; every table's columns sum to the row-level data;
every cross-reference and citation resolves; no stale value survives anywhere. The run
fails if any check fails.

## Inputs that cannot be regenerated

Four frozen tables carry the coded data, and six further files hold material that no script
can rebuild: the second coder's returned issuer codings and their adjudication, the two
retrieval-audit samples, the alternative-window sample, and the retrieval validation
sample. All ten are hashed in the manifest.

## Relationship to the article

The article cites the public study repository. This capsule contains the same material and
has been submitted to Code Ocean; its DOI will be added to the article at proof stage.

## Licence

Code MIT, data CC0. See LICENSE.
