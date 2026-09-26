""", §5A.7, §6.3, §7B.3, §7A.1, §3B.4 — build the supplementary tables and the
T3 coding-example section (S2). Emits frontiers/submission/supplementary.tex."""
import csv,json,re,sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from stats_lib import load,TIERS5
T=json.load(open(L.res("tables.json"))); D=load(); ALL=list(D.values())
E=L.evidence(); B=L.descriptions()
SPL={r['incident_id']:r for r in csv.DictReader(open(L.out("t3_split.csv"),newline='',encoding='utf-8',errors='replace'))}
SHORT={"Meta Platforms, Inc.":"Meta","Alphabet Inc.":"Alphabet","Tesla, Inc.":"Tesla",
       "General Motors Company":"GM","Microsoft Corporation":"Microsoft","Amazon.com, Inc.":"Amazon",
       "Apple Inc.":"Apple","UnitedHealth Group Inc.":"UnitedHealth","SoundThinking, Inc.":"SoundThinking",
       "Serve Robotics Inc.":"Serve Robotics","Zillow Group, Inc.":"Zillow"}
pc=lambda x:f"{100*float(x):.1f}"
def esc(s):
    s=(s or "").replace("\\","").replace("&","\\&").replace("%","\\%").replace("$","\\$")
    s=s.replace("#","\\#").replace("_","\\_").replace("{","(").replace("}",")")
    return re.sub(r"\s+"," ",s).strip()
def frag(iid,words=40):
    """shortest verbatim quoted fragment in the evidence prose, else the leading clause"""
    ev=(E.get(iid,{}) or {}).get('evidence','') or ''
    q=re.findall(r"'([^']{25,300})'",ev)
    s=q[0] if q else ev.split('.')[0]
    return " ".join(s.split()[:words])
O=[r"""\section*{Supplementary Material}
\setcounter{table}{0}\renewcommand{\thetable}{S\arabic{table}}
\renewcommand{\thefigure}{S\arabic{figure}}
% Only tables and figures carry S numbers. Numbering the sections as well produced two
% parallel S sequences, so that section S7 contained tables S8 and S9.
\setcounter{secnumdepth}{0}

\section{CSET AI-Harm severity for the externally classified subset}
Supplementary Table~S1 lists the 40 incidents carrying an external CSET AI-Harm classification,
unchanged from the original submission. For these incidents the CSET value was preserved rather than
assigned under the study rubric, and is reproduced verbatim from the released taxonomy.

{\scriptsize\renewcommand{\arraystretch}{1.0}
\begin{longtable}{@{}r p{8.6cm} l@{}}
\caption{The 40 incidents carrying an external CSET AI Harm Taxonomy classification, unchanged from the original submission. The remaining 267 incidents were assigned Severe, Moderate or Limited under the pre-specified study rubric and are not listed here.}\\
\toprule
AIID incident ID & CSET classification (harm level; tangible harm) & Study severity \\ \midrule
\endfirsthead
\toprule
AIID incident ID & CSET classification (harm level; tangible harm) & Study severity \\ \midrule
\endhead
\midrule \multicolumn{3}{r}{\emph{continued on next page}}\\
\endfoot
\bottomrule
\endlastfoot
81 & none; no tangible harm, near-miss, or issue & Moderate \\
82 & none; no tangible harm, near-miss, or issue & Moderate \\
83 & none; no tangible harm, near-miss, or issue & Moderate \\
84 & none; no tangible harm, near-miss, or issue & Moderate \\
89 & none; tangible harm definitively occurred & Severe \\
92 & AI tangible harm event; tangible harm definitively occurred & Severe \\
97 & AI tangible harm issue; non-imminent risk of tangible harm (an issue) occurred & Moderate \\
102 & none; no tangible harm, near-miss, or issue & Moderate \\
105 & AI tangible harm event; tangible harm definitively occurred & Severe \\
113 & none; no tangible harm, near-miss, or issue & Moderate \\
116 & AI tangible harm event; tangible harm definitively occurred & Severe \\
124 & AI tangible harm event; tangible harm definitively occurred & Severe \\
125 & AI tangible harm event; tangible harm definitively occurred & Severe \\
127 & none; tangible harm definitively occurred & Severe \\
129 & none; no tangible harm, near-miss, or issue & Moderate \\
139 & none; no tangible harm, near-miss, or issue & Moderate \\
142 & AI tangible harm issue; non-imminent risk of tangible harm (an issue) occurred & Moderate \\
143 & none; no tangible harm, near-miss, or issue & Moderate \\
144 & unclear; unclear & Limited \\
145 & AI tangible harm issue; non-imminent risk of tangible harm (an issue) occurred & Moderate \\
149 & AI tangible harm event; tangible harm definitively occurred & Severe \\
153 & AI tangible harm event; tangible harm definitively occurred & Severe \\
156 & none; tangible harm definitively occurred & Severe \\
157 & unclear; tangible harm definitively occurred & Severe \\
160 & AI tangible harm issue; non-imminent risk of tangible harm (an issue) occurred & Moderate \\
220 & AI tangible harm event; tangible harm definitively occurred & Severe \\
281 & none; non-imminent risk of tangible harm (an issue) occurred & Moderate \\
313 & none; no tangible harm, near-miss, or issue & Moderate \\
354 & AI tangible harm event; tangible harm definitively occurred & Severe \\
360 & none; no tangible harm, near-miss, or issue & Moderate \\
367 & none; no tangible harm, near-miss, or issue & Moderate \\
393 & none; no tangible harm, near-miss, or issue & Moderate \\
414 & none; no tangible harm, near-miss, or issue & Moderate \\
489 & none; no tangible harm, near-miss, or issue & Moderate \\
501 & AI tangible harm event; tangible harm definitively occurred & Severe \\
554 & none; no tangible harm, near-miss, or issue & Moderate \\
574 & none; no tangible harm, near-miss, or issue & Moderate \\
576 & none; no tangible harm, near-miss, or issue & Moderate \\
583 & none; no tangible harm, near-miss, or issue & Moderate \\
614 & none; no tangible harm, near-miss, or issue & Moderate \\
\end{longtable}}

\section{T3 coding examples}
The T3 threshold requires filing language that names the \emph{class} of technology or the
\emph{class} of harm implicated in the incident. The examples below are drawn from the per-incident
filing-search records in the replication package. Positive examples qualified as T3a, where the
filing language matched both the incident's technology family and its harm family; negative examples
qualified only as T3b, where a single family matched, which is the distinction this split isolates.
Fragments are quoted verbatim from the coding record and truncated to at most forty words."""]

# --- S2 examples: 4 positive (T3a) and 4 negative (T3b), one pair per domain ---
# Domains are defined on BOTH the application and the harm family, and incidents are used at most
# once across the whole table, so the same incident cannot appear under two domain labels.
DOMAINS=[("content / misinformation",("content-moderation","recommender-ranking"),("misinformation-content",)),
         ("generative-AI error",     ("generative-llm",),                          ("service-quality","misinformation-content")),
         ("autonomous system",       ("autonomous-vehicle","robotics-automation"), ("physical-safety",)),
         ("bias / discrimination",   ("vision-biometric","ads-targeting","predictive-scoring"),("discrimination-bias",))]
# A quoted span is only usable as a worked example if it is language from a periodic
# filing. Search notes ("efts returned only..."), statements of absence ("no 10-K/10-Q")
# and coding rationale ("squarely within the same family") are not filing text, and
# showing them as the evidence for a T3 code contradicts the code.
NOT_FILING = re.compile(
    r"efts|no 10-K|no 10-Q|no 8-K|returned only|did not disclose|not named|zero hits|"
    r"0 hits|shareholder proposal|PX14A6G|DEF 14A|squarely within|same-family|"
    r"proxy|no in-window|no periodic|no filing|not the event|in any filing|"
    r"only generic|is not a|flags only|window flags|hits are|routine 10-K|"
    r"references\.|surfaced|returns", re.I)

def quoted(iid,words=34,minwords=8):
    """A verbatim passage from a periodic filing, or None if the record holds no such quote."""
    ev=(E.get(iid,{}) or {}).get('evidence','') or ''
    qs=[q for q in re.findall(r"[\u2018']([^\u2019']{30,400})[\u2019']",ev)
        if len(q.split())>=minwords and not NOT_FILING.search(q)]
    if not qs: return None
    return " ".join(qs[0].split()[:words])
_used=set()
def pick(split,apps,harms):
    """An example for one domain and one side of the split.

    A domain is defined by its harm family; the application families narrow it. If no
    incident satisfies both and still carries a quotable filing passage, fall back to the
    harm family alone rather than leaving the pair incomplete."""
    for require_app in (True,False):
        for iid,r in sorted(SPL.items(),key=lambda kv:int(kv[0])):
            if iid in _used or r['t3_split']!=split: continue
            if require_app and not any(a in r['incident_app_families'] for a in apps): continue
            if not any(h in r['incident_harm_families'] for h in harms): continue
            # The example has to demonstrate its own class. A T3a case must show both
            # families matched; a T3b case must show exactly one. An incident that matched
            # neither is still T3b by the residual rule, but it illustrates nothing.
            na=bool(r['app_family_matched']); nh=bool(r['harm_family_matched'])
            if split=="T3a" and not (na and nh): continue
            if split=="T3b" and (na+nh)!=1: continue
            frag=quoted(iid)
            if not frag: continue
            _used.add(iid); return r,frag
    return None,None
rows=[]
for lab,apps,harms in DOMAINS:
    for split in ("T3a","T3b"):
        r,frag=pick(split,apps,harms)
        if r is None: continue
        rows.append((lab,split,r['incident_id'],r['issuer'],r['app_family_matched'],r['harm_family_matched'],frag))
assert len({x[2] for x in rows})==len(rows), "an incident appears twice in the S2 example table"
O.append(r"""\begin{table}[H]
\caption{Worked T3 coding examples, one T3a and one T3b per domain, each incident used once. \emph{Qualified} reports which of the incident's two families the filing language matched: a T3a example matched both, a T3b example only one, which is why a T3b case does not support the reading that the generic language is closely related to the realized incident. Fragments are quoted verbatim from the filing-search record and truncated.}
\centering\scriptsize
\begin{center}
\begin{tabular}{@{}p{1.9cm}cr p{1.7cm} p{2.5cm} p{4.6cm}@{}}
\toprule
Domain & Split & AIID id & Issuer & Qualified (app / harm) & Verbatim fragment from the filing record \\ \midrule
"""+"".join(f"{esc(lab)} & {sp} & {iid} & {esc(SHORT.get(iss,iss))} & {esc(am.replace('|',', ')) or '---'} / {esc(hm.replace('|',', ')) or '---'} & {esc(fr)} \\\\\n"
            for lab,sp,iid,iss,am,hm,fr in rows)+r"""\bottomrule
\end{tabular}
\end{center}
\end{table}""")

# --- S4a co-candidates ---
CO=[r for r in csv.DictReader(open(L.out("cocandidates.csv"),newline='',encoding='utf-8',errors='replace'))
    if r['in_analytical_sample']=='True' and int(r['n_distinct_issuers'])>1]
O.append(r"""\section{Entity resolution detail}
\begin{table}[H]
\caption{Incidents in the analytical sample with more than one listed-issuer candidate. The original procedure retained one issuer per incident, selected by listing status with ties broken by the order of organizations in the AIID record; the discarded candidates were not persisted and are re-derived here.}
\centering\scriptsize
\begin{tabular}{@{}rlp{4.2cm}p{5.4cm}@{}}
\toprule
AIID id & Date & Issuer retained & Listed candidates discarded \\ \midrule
"""+"".join(f"{r['incident_id']} & {r['incident_date']} & {esc(r['selected_issuer'])} & {esc('; '.join(x for x in r['discarded_issuers'].split('|') if x.strip()))} \\\\\n" for r in CO)+r"""\bottomrule
\end{tabular}
\end{table}""")

# --- S4b exclusion stages ---
O.append(r"""\begin{table}[H]
\caption{Stage-by-stage exclusion accounting. Of 1{,}389 window incidents, 1{,}082 are excluded and 307 remain. Note that foreign private issuers and delisted issuers are excluded \emph{after} a successful organization-to-registrant match, which is why the mapped file contains 348 rows (307 + 26 + 15).}
\centering\small
\begin{tabular}{@{}p{3.0cm}p{4.6cm}rp{4.9cm}@{}}
\toprule
Stage & Exclusion & n & Sub-reason \\ \midrule
1. Date window & outside 2019--2026 & 208 & of 1{,}597 snapshot records \\ \midrule
2. Organization named & generic or individual actors only & 398 & scammers, users, unnamed developers, government bodies \\
3. Organization resolvable & named entity not in the crosswalk & 400 & unresolved corporate or institutional names \\
4. Listed status & privately held & 243 & dominated by private AI labs \\ \midrule
5. Post-match: domicile & foreign private issuer (20-F/6-K) & 26 & Baidu, Alibaba, Thomson Reuters and others \\
6. Post-match: listing & excluded under the study's delisted-issuer rule & 15 & Twitter/X Corp., Rite Aid \\ \midrule
\multicolumn{2}{@{}l}{\textbf{Total excluded}} & \textbf{1{,}082} & \\
\multicolumn{2}{@{}l}{\textbf{Analytical sample}} & \textbf{307} & 21 issuers \\
\bottomrule
\end{tabular}
\end{table}""")

# --- S4c crosswalk verdicts ---
# The crosswalk verdict table was removed: Section 3.2 of the main text already gives all four
# verdict counts and names both corrected incidents, so the table only restated them.

# --- S5 CSET subset ---
cs=T['tableS5_cset40']
O.append(r"""\section{Severity}
\begin{table}[H]
\caption{Tier distribution for the """+str(cs['n'])+r""" incidents carrying an external CSET AI-Harm severity classification. The subset contains """+str(cs['n_substantive'])+r""" substantive disclosure, so no inferential test is performed (fewer than 5 substantive cases).}
\centering\small
\begin{tabular}{@{}lrrrrr@{}}
\toprule
CSET severity & n & T1 & T2 & T3a & T3b \& T4 \\ \midrule
"""+"".join(f"{r['severity'].replace('sev_','')} & {r['n']} & {r['T1']} & {r['T2']} & {r['T3a']} & {r['T3b']+r['T4']} \\\\\n" for r in cs['rows'])+r"""\bottomrule
\end{tabular}
\end{table}""")

# --- S6 role LOO ---
RL=list(csv.DictReader(open(L.out("role_loo.csv"),newline='',encoding='utf-8',errors='replace')))
O.append(r"""\section{Role analysis fragility}
\begin{table}[H]
\caption{Leave-one-positive-out sensitivity of the role association. Each of the seven substantive incidents is in turn dropped, reclassified one tier down, and reclassified to T3; both contrasts are recomputed by Monte-Carlo exact permutation (20{,}000 draws, seed 42). The final row promotes one developer-only T3 incident to T1 as an upper-bound perturbation.}
\centering\small
\begin{tabular}{@{}llrrrr@{}}
\toprule
Perturbation & Incident & \multicolumn{2}{c}{3-way contrast} & \multicolumn{2}{c}{2$\times$2 contrast} \\
 & & $\chi^2$ & $p$ & $\chi^2$ & $p$ \\ \midrule
"""+"".join(f"{esc(r['perturbation'])} & {r['incident_id']} & {r['chi2_3way']} & {float(r['p_3way']):.4f} & {r['chi2_2x2']} & {float(r['p_2x2']):.4f} \\\\\n" for r in RL)+r"""\bottomrule
\end{tabular}
\end{table}""")

# --- S7 per-tier kappa ---
REL=json.load(open(f"{L.ROOT}/results/reliability_ext.json"))
pt=REL['per_tier_one_vs_rest']; cm=REL['confusion']
O.append(r"""\section{Reliability by tier}
\begin{table}[H]
\caption{One-tier-against-the-rest agreement in the stratified reliability sample (n = 68), and the full confusion matrix. The T2 coefficient is negative: the second coder assigned the three pass-one T2 incidents to T1, T3 and T4 respectively, agreeing with none. T2 therefore has no demonstrated inter-coder reliability in this sample, which is why T1 is the primary measure of incident-specific disclosure and T1+T2 is reported as an upper bound.}
\centering\small
\begin{tabular}{@{}lrrr@{}}
\toprule
Tier & n (pass 1) & Raw agreement & Cohen's $\kappa$ \\ \midrule
"""+"".join(f"{k} & {v['n_pass1']} & {v['po']:.3f} & {v['kappa']:.3f} \\\\\n" for k,v in pt.items())+r"""\midrule
\multicolumn{4}{@{}l}{Aggregate: raw """+f"{REL['observed_agreement']:.3f}"+r""", $\kappa$ """+f"{REL['cohens_kappa']:.3f}"+r""", PABAK """+f"{REL['PABAK']:.3f}"+r""", Gwet AC1 """+f"{REL['gwet_ac1']:.3f}"+r""" } \\
\bottomrule
\end{tabular}

\vspace{4pt}
\begin{tabular}{@{}lrrrr@{}}
\toprule
Pass 1 $\downarrow$ / Pass 2 $\rightarrow$ & T1 & T2 & T3 & T4 \\ \midrule
"""+"".join(f"{k} & {v['T1']} & {v['T2']} & {v['T3']} & {v['T4']} \\\\\n" for k,v in cm.items())+r"""\bottomrule
\end{tabular}
\end{table}""")

# The five-way subgroup breakdowns that used to sit here were removed: the severity and role
# versions duplicated Tables 3 and 5 of the main text column for column, and the year version
# was not requested by either reviewer.

# --- S11-S12 entity-mapping reliability: strata and adjudicated disagreements ---
ER=json.load(open(L.res("entity_reliability.json")))
STRATLAB={"multi-candidate":"More than one listed candidate",
          "parent-linked":"Mapped through a subsidiary or product",
          "single-candidate-large-issuer":"Single candidate, frequent issuer",
          "small-issuer":"Issuer contributing three or fewer incidents"}
O.append(r"""\section{Reliability of issuer matching}
\begin{table}[H]
\caption{Agreement on issuer identity between the study mapping and a blind second coder, by sampling stratum. The sample of 80 incidents (seed 42) deliberately oversamples ambiguous cases, so the overall rate is expected to be conservative relative to full-sample agreement. Overall: """+f"{ER['issuer_identity']['raw_agreement']*100:.1f}"+r"""\% raw agreement, Cohen's $\kappa$ = """+f"{ER['issuer_identity']['cohens_kappa']:.2f}"+r""", Gwet's AC1 = """+f"{ER['issuer_identity']['gwet_ac1']:.2f}"+r""". Post-hoc; not pre-specified.}
\label{tab:entrel}
\centering\small
\begin{tabular}{@{}lrrr@{}}
\toprule
Stratum & n & Agree & Agreement \\ \midrule
"""+"".join(
  f"{STRATLAB.get(k,k)} & {v['n']} & {v['agree']} & {100*v['agree']/v['n']:.1f}\\% \\\\\n"
  for k,v in sorted(ER['issuer_by_stratum'].items(),key=lambda kv:-kv[1]['n']))
+r"""\midrule
"""+"".join(
  f"\\emph{{Second coder's own confidence: {k}}} & {v['n']} & {v['agree']} & {100*v['agree']/v['n']:.1f}\\% \\\\\n"
  for k,v in sorted(ER['issuer_by_confidence'].items(),key=lambda kv:-kv[1]['n']))
+r"""\bottomrule
\end{tabular}
\end{table}""")

ADJ=[r for r in csv.DictReader(open(L.frozen("entity_audit_adjudication.csv"),newline='',encoding='utf-8',errors='replace'))]
O.append(r"""\begin{table}[H]
\caption{Every disagreement on issuer identity, with its adjudication against the attribution rules of Section~3.2. Ten resolve in favour of the study mapping, four in favour of the second coder. None involves an incident coded T1 or T2. Post-hoc; not pre-specified.}
\label{tab:entadj}
\centering\footnotesize
\begin{tabular}{@{}llll@{}}
\toprule
Incident & Study mapping & Second coder & Adjudication \\ \midrule
"""+"".join(
  f"{r['incident_id']} & {esc(SHORT.get(r['study_issuer'],r['study_issuer']))} & "
  f"{esc(SHORT.get(r['second_coder_issuer'],r['second_coder_issuer']))} & {esc(r['adjudication'])} \\\\\n"
  for r in ADJ)
+r"""\bottomrule
\end{tabular}
\end{table}""")

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[margin=2.2cm,a4paper]{geometry}
\usepackage{booktabs,longtable,array,url,hyperref,graphicx,float}
% [H] pins each table where it is written. With nine floats and [h!], LaTeX moved
% tables away from the headings that introduce them.
\usepackage[T1]{fontenc}
\renewcommand{\arraystretch}{1.12}
% With every float pinned by [H], a page that is fractionally too full would otherwise
% be stretched past the bottom margin. Let pages end short instead.
\raggedbottom
% Each supplementary section starts a fresh page, so a heading is never separated from
% its table and no page ends with a large gap where a table would not fit.
\let\oldsection\section
\newcounter{supsec}
\renewcommand{\section}[1]{\stepcounter{supsec}\ifnum\value{supsec}>1\clearpage\fi\oldsection*{#1}}
\title{Supplementary Material\\\large The AI Incident Disclosure Shadow: Tracking AI Incidents into U.S. Securities Filings}
\author{Samir Chincholikar \and Robin Chawla}
\date{}
\begin{document}
\maketitle
"""
O.append(r"""\section{Shadow rate by severity}
\begin{figure}[H]
\centering
\includegraphics[width=0.78\textwidth]{FigureS1.png}
\caption{Collapsed shadow rate (T3+T4) by incident severity, with 95\% Wilson intervals. Figure~2 of the main text gives the same strata as a five-way distribution across all tiers.}
\label{fig:supp-sev}
\end{figure}""")

open(L.res("supplementary.tex"),"w").write(
    PREAMBLE + "\n\n".join(O) + "\n\\end{document}\n")
print("wrote results/supplementary.tex; tables S2-S10; %d T3 examples"%len(rows))
