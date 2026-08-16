# Frontiers in Artificial Intelligence — Original Research: compliance checklist

Manuscript: *The AI Incident Disclosure Shadow* (`manuscript.tex`). **Status legend:** ✅ done · ⚠️ needs your input · ➖ N/A.
Every requirement from the Frontiers author guidelines + the official LaTeX template is mapped below.

| # | Requirement (Frontiers spec) | Our status | Where / note |
|---|---|---|---|
| 1 | Use Frontiers template; LaTeX submit `.tex`+`.pdf`+`.bib`+figures | ✅ | `FrontiersinHarvard.cls`; all files delivered in `frontiers_submission/` |
| 2 | **Reference style = Harvard (author-date)** for Frontiers in AI | ✅ | Confirmed from accepted papers; `\bibliographystyle{Frontiers-Harvard}`, `\citep/\citet` |
| 3 | Title: concise, states main result, no abbreviations, includes keywords | ✅ | Title names the finding ("Disclosure Shadow"), no abbreviations |
| 4 | Running title | ✅ | `\title[The AI Incident Disclosure Shadow]{…}` |
| 5 | Author names listed; corresponding author marked `*` | ✅ | `Samir Chincholikar$^{1,*}$` |
| 6 | Affiliation format: Dept, Org, City, State (US/CA/AU), Country — no street/zip | ⚠️ | Placeholder **"Independent Researcher, New York, NY, United States"** — **replace with your real affiliation** |
| 7 | Corresponding email in correspondence block | ✅ | samir.chincholikar@gmail.com |
| 8 | Abstract: one paragraph, IMRAD-style, **no citations/figures/tables** | ✅ | Single paragraph; zero citations; policy names mentioned without author-date cites |
| 9 | Abstract SEO: keywords in first two sentences | ✅ | "artificial-intelligence", "AI Incident Database", "securities disclosure" up front |
| 10 | Keywords: **5–8** | ✅ | 8 keywords provided |
| 11 | Section structure: Introduction (no subheadings), Materials & Methods, Results, Discussion | ✅ | Introduction has no subheadings; M&M/Results/Discussion present |
| 12 | Materials & Methods placement (before/after Results) | ✅ | Before Results (permitted) |
| 13 | **Single/1.5 spacing + page numbers + line numbers** | ✅ | Template `onehalfspacing` (Frontiers LaTeX default) + `\linenumbers` + page numbers; production-adjustable to single if requested |
| 14 | American English default | ✅ | US spelling throughout |
| 15 | Abbreviations defined at first use; kept minimal | ✅ | AI, SEC, AIID, CSET defined on first use |
| 16 | References: peer-reviewed, up-to-date; citation↔list complete | ✅ | 34 refs, 7 streams; all `\citep` resolve (0 undefined at compile) |
| 17 | Reference list: first 6 authors + et al., initials, DOI when available | ✅ | `.bst` enforces; DOIs included where available |
| 18 | Only published/accepted works; preprints need DOI/URL + labeled | ✅ | Preprint (arXiv:2508.19313) labeled; legal/policy sources as `@misc` |
| 19 | **Figures + tables ≤ 15 combined** (Original Research) | ✅ | **5 figures + 4 tables = 9** |
| 20 | Figures cited in numerical order; mentioned in text | ✅ | Fig 1→5 cited in order (`\ref{fig:flow}` … `fig:onset`) |
| 21 | Figure captions at END of manuscript; panels bold `(A)` | ✅ | All figures + captions after references |
| 22 | Figures: 300 dpi, RGB, ≥8pt text, ≥2pt lines, 85/180mm width | ✅ | Generated at 300 dpi, colorblind-safe (Okabe–Ito), single/double-column widths |
| 23 | Alt text for figures | ⚠️ | Provide on the submission portal (captions are descriptive; alt-text field is portal-side) |
| 24 | Tables **built in LaTeX**, at END, caption immediately BEFORE table | ✅ | 4 `\begin{table}` in LaTeX after references; `\caption` before `\begin{tabular}` |
| 25 | Tables cited in numerical order | ✅ | Tables 1→4 cited in order |
| 26 | **Conflict of Interest** statement | ✅ | Present (none) |
| 27 | **Author Contributions** (initials) | ✅ | "SC conceived…" |
| 28 | **Funding** statement | ✅ | "no external funding" |
| 29 | **Acknowledgments** | ✅ | Present, carries the AI-assistance disclosure |
| 30 | **Data Availability Statement** naming repository + link | ⚠️ | GitHub link included; **insert Zenodo DOI on acceptance** |
| 31 | **Ethics statement** | ✅ | No human/animal subjects; public data only |
| 32 | **AI-use disclosure** in Methods AND Acknowledgments with name/version/model/source; AI not an author | ✅ | §3.3 "Use of AI assistance" + Acknowledgments: "Anthropic Claude, Opus-class model, accessed Aug 2026 via the Claude Agent SDK"; no AI author |
| 33 | Verbatim text in quotes with source | ✅ | No un-attributed verbatim text |
| 34 | Inclusive language / SAGER | ✅ | No sex/gender claims; neutral language |
| 35 | Word count + #figures/#tables on first page | ⚠️ | Optional first-page note; add on portal if required (body ≈ 5,600 words; 5 figures, 4 tables) |
| 36 | Supplementary material (optional): upload AI prompts/logs | ✅ | Coding logs + capsule available as the reproducibility artifact/Supplementary |
| 37 | Registration of submitting author on Frontiers | ⚠️ | Portal step (yours) |

## Items requiring your input before submission (3)
1. **Affiliation** — replace the "Independent Researcher, New York, NY" placeholder with your actual institution/affiliation and city/country.
2. **Zenodo DOI** — insert into the Data Availability Statement once you cut the release (the GitHub link is already there).
3. **Portal steps** — alt-text per figure, author registration, and (if the journal requests) the words/figures/tables count field.

## Verified at compile
`pdflatex → bibtex → pdflatex×2` compiles with **0 errors**, **0 undefined citations**, 34 references formatted in Harvard style, line + page numbers present, 13 pages. Files to upload: `manuscript.tex`, `references.bib`, `manuscript.pdf`, `figures/fig1–5.png`, and the class/style files (`FrontiersinHarvard.cls`, `Frontiers-Harvard.bst`) if the portal compiles.
