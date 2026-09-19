"""emit the LaTeX for every revision table from results/tables.json."""
import json,csv,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
T=json.load(open(L.res("tables.json"))); P=json.load(open(L.res("severity_power.json")))
pc=lambda x: f"{100*float(x):.1f}"
O=[]
d={r['tier']:r for r in T['table1_adjudicated']['rows']}
pre={r['tier']:r for r in T['table1_prereg']['rows']}
LABEL={"T1":"Incident-specific","T2":"Legal-consequence only","T3a":"Generic, matches both families",
       "T3b":"Generic, matches one family only","T4":"No related disclosure located"}

# --- Table 1 (four tier, pre-registered) ---
O.append(r"""\begin{table}[h!]
\caption{Four-tier disclosure distribution under the pre-registered coding (N = 307). The four tiers are the primary presentation; the two aggregates below the rule are summary measures. Intervals are Clopper--Pearson exact 95\%. The shadow aggregate means only that neither incident-specific nor directly related legal-consequence disclosure could be identified in Forms 8-K, 10-K and 10-Q under the study protocol.}
\label{tab:dist}
\begin{center}
\begin{tabular}{@{}llrl@{}}
\toprule
Tier & Meaning & n & Share (95\% CI) \\ \midrule
T1 & Incident-specific        & 4   & 1.3\% (0.4--3.3) \\
T2 & Legal-consequence only   & 3   & 1.0\% (0.2--2.8) \\
T3 & Generic same-family risk language & 278 & 90.6\% (86.7--93.6) \\
T4 & No related disclosure located     & 22  & 7.2\% (4.5--10.6) \\ \midrule
\multicolumn{2}{@{}l}{Substantive (T1+T2), upper bound} & 7 & 2.3\% (0.9--4.6) \\
\multicolumn{2}{@{}l}{Shadow (T3+T4), summary measure}  & 300 & 97.7\% (95.4--99.1) \\
\bottomrule
\end{tabular}
\end{center}
\end{table}""")

# --- Table 5: five-way ---
rows=""
for k in ("T1","T2","T3a","T3b","T4"):
    r=d[k]; rows+=f"{k} & {LABEL[k]} & {r['n']} & {pc(r['share'])}\\% ({pc(r['lo'])}--{pc(r['hi'])}) \\\\\n"
agg=""
for k,lab in (("substantive_T1T2","Substantive (T1+T2), upper bound"),
              ("shadow_broad_T3aT3bT4","Shadow-broad (T3a+T3b+T4) = primary"),
              ("weakly_related_or_none_T3bT4","Weakly-related-or-none (T3b+T4)"),
              ("none_only_T4","None located only (T4)")):
    r=d[k]; agg+=f"\\multicolumn{{2}}{{@{{}}l}}{{{lab}}} & {r['n']} & {pc(r['share'])}\\% ({pc(r['lo'])}--{pc(r['hi'])}) \\\\\n"
O.append(r"""\begin{table}[h!]
\caption{Five-way distribution under the T3 relatedness split, with adjudicated T2 codes (N = 307). T3a denotes generic filing language matching both the incident's technology or application family and its harm family; T3b matches only one. The primary shadow rate is invariant to the T3a/T3b and T3/T4 boundaries by construction, because all three tiers sit outside the substantive categories: the split addresses the interpretation of the T3 mass, not the headline rate. Intervals are Clopper--Pearson exact 95\%. Post-hoc; not pre-specified.}
\label{tab:fiveway}
\begin{center}
\begin{tabular}{@{}llrl@{}}
\toprule
Tier & Meaning & n & Share (95\% CI) \\ \midrule
"""+rows+r"""\midrule
"""+agg+r"""\bottomrule
\end{tabular}
\end{center}
\end{table}""")

# --- Table 2: severity exact counts ---
sl={"sev_severe":"Severe","sev_moderate":"Moderate","sev_limited":"Limited"}
rr=""
for r in T['table2_severity']:
    rr+=(f"{sl[r['severity']]} & {r['n']} & {r['T1']} & {r['T2']} & {r['T3a']} & {r['T3b']} & {r['T4']} & "
         f"{pc(r['T1_share'])} ({pc(r['T1_lo'])}--{pc(r['T1_hi'])}) & {pc(r['sub_share'])} ({pc(r['sub_lo'])}--{pc(r['sub_hi'])}) \\\\\n")
O.append(r"""\begin{table}[h!]
\caption{Disclosure by incident severity, exact counts (adjudicated codes). Percentages with Clopper--Pearson exact 95\% intervals are given for T1 and for T1+T2 only; all intervals overlap. Monte-Carlo exact permutation test on substantive disclosure across tiers: p = 0.61. The design would require the Severe-group substantive rate to reach """+pc(P['mde_severe_rate_80pct'])+r"""\% to detect a difference from the Limited group at 80\% power, so this non-rejection carries little information. Exploratory.}
\label{tab:sev}
\small
\begin{center}
\begin{tabular}{@{}lrrrrrrll@{}}
\toprule
Severity & n & T1 & T2 & T3a & T3b & T4 & T1 \% (95\% CI) & T1+T2 \% (95\% CI) \\ \midrule
"""+rr+r"""\bottomrule
\end{tabular}
\end{center}
\end{table}""")

# --- Table 6: attribution basis ---
BASES=["developer","deployer-operator","both","platform-venue","mentioned-only"]
ov=T['table6_attribution']['overall']; N=sum(ov.values())
rr="".join(f"{b} & {ov[b]} & {pc(ov[b]/N)}\\% \\\\\n" for b in BASES)
bt="".join(f"{r['basis']} & {r['n']} & {r['T1']} & {r['T2']} & {r['T3a']} & {r['T3b']} & {r['T4']} \\\\\n"
           for r in T['table6_attribution']['by_basis_tier'])
iss="".join(f"{r['issuer']} & {r['n']} & {r['developer']} & {r['deployer-operator']} & {r['both']} & {r['platform-venue']} & {r['mentioned-only']} \\\\\n"
            for r in T['table6_attribution']['by_issuer'][:10])
O.append(r"""\begin{table}[h!]
\caption{Attribution basis of the 307 incidents. \emph{platform-venue} denotes an issuer that hosted third-party content or third-party use where the harm-producing system was not the issuer's own deployment decision; \emph{mentioned-only} denotes an issuer named without an evident development, deployment or venue relationship, including cases where the issuer is the harmed party or one of several vendors in a comparative study. No incident coded platform-venue or mentioned-only received T1 or T2 disclosure. Every case, with the rule that produced it and a confidence flag, is enumerated in \texttt{AUTHOR\_REVIEW.csv}. Post-hoc; not pre-specified.}
\label{tab:attrib}
\small
\begin{center}
\begin{tabular}{@{}lrr@{}}
\toprule
\multicolumn{3}{@{}l}{\emph{Panel A. Distribution of the 307 incidents}}\\
Attribution basis & n & Share \\ \midrule
"""+rr+r"""\bottomrule
\end{tabular}

\vspace{4pt}
\begin{tabular}{@{}lrrrrrr@{}}
\toprule
\multicolumn{7}{@{}l}{\emph{Panel B. Disclosure tier by attribution basis}}\\
Attribution basis & n & T1 & T2 & T3a & T3b & T4 \\ \midrule
"""+bt+r"""\bottomrule
\end{tabular}

\vspace{4pt}
\begin{tabular}{@{}lrrrrrr@{}}
\toprule
\multicolumn{7}{@{}l}{\emph{Panel C. Attribution basis by issuer, ten largest contributors}}\\
Issuer & n & developer & deployer-op. & both & venue & mentioned \\ \midrule
"""+iss+r"""\bottomrule
\end{tabular}
\end{center}
\end{table}""")

# --- Table 7: role ---
rr="".join(f"{r['role']} & {r['n']} & {r['T1']} & {r['T2']} & {r['T3a']} & {r['T3b']} & {r['T4']} & {r['substantive']} \\\\\n"
           for r in T['table7_role']['three_way'])
tb=T['table7_role']['two_by_two']
O.append(r"""\begin{table}[h!]
\caption{Issuer role against disclosure tier, exact counts (adjudicated codes). The lower panel gives the two-by-two contrast the text describes. The three-way contrast rejects at conventional levels and the two-by-two does not; Supplementary Table~S7 reports the leave-one-positive-out fragility of both. Descriptive; hypothesis-generating.}
\label{tab:role}
\small
\begin{center}
\begin{tabular}{@{}lrrrrrr@{}}
\toprule
Role & n & T1 & T2 & T3a & T3b & T4 \\ \midrule
"""+"".join(f"{r['role']} & {r['n']} & {r['T1']} & {r['T2']} & {r['T3a']} & {r['T3b']} & {r['T4']} \\\\\n" for r in T['table7_role']['three_way'])+r"""\midrule
\multicolumn{7}{@{}l}{\emph{Two-by-two contrast: substantive disclosure (T1 or T2) against all other tiers}} \\
Developer-only & """+str(tb['developer_only']['n'])+r""" & \multicolumn{5}{l}{"""+str(tb['developer_only']['substantive'])+r""" substantive, of which """+str(tb['developer_only']['T1'])+r""" are T1} \\
Any deployer (deployer-only or both) & """+str(tb['any_deployer']['n'])+r""" & \multicolumn{5}{l}{"""+str(tb['any_deployer']['substantive'])+r""" substantive, of which """+str(tb['any_deployer']['T1'])+r""" are T1} \\
\bottomrule
\end{tabular}
\end{center}
\end{table}""")

# --- Table: substantively disclosed incidents, with pre-registered and adjudicated tiers ---
# Regenerated at revision because the hand-written original still showed incident 733 as T2 after
# the adjudication of section 7A moved it to T1.
from stats_lib import load as _load
_D=_load()
FILING={"149":("Zillow Group","8-K Items 2.02/8.01","Yes --- $\\approx$\\$304M inventory write-down"),
        "596":("General Motors","10-K Items 1 and 1A","No incident-specific reserve"),
        "726":("General Motors","10-K Items 1 and 1A; 8-K special items","Yes --- \\$478M Cruise restructuring"),
        "997":("Meta Platforms","Legal Proceedings, named suit","No"),
        "534":("Meta Platforms","10-K Commitments and Contingencies","No"),
        "711":("Tesla","Legal Proceedings / NHTSA, DOJ matters","No"),
        "733":("General Motors","10-Q Commitments and Contingencies","No")}
_rows=""
for iid in ("149","596","726","997","534","711","733"):
    r=_D[iid]; iss,loc,imp=FILING[iid]
    pre,adj=r['tier_prereg'],r['tier_adj']
    mark=" $\\rightarrow$ "+adj if pre!=adj else ""
    _rows+=f"{iid} & {iss} & {pre}{mark} & {loc} & {imp} \\\\\n"
O.append(r"""\begin{table}[h!]
\caption{All substantively disclosed incidents and their disclosure channel, ordered T1 then T2 under the pre-registered coding. Where the adjudication of Section~\ref{sec:reliability} changed a code, both are shown as \emph{pre-registered} $\rightarrow$ \emph{adjudicated}; incident 733 is the one such case. Booked impact records whether the filing carried a quantified charge attributable to the incident.}
\label{tab:acct}
\small
\begin{center}
\begin{tabular}{@{}llllp{4.3cm}@{}}
\toprule
AIID id & Issuer & Tier & Filing location & Booked impact \\ \midrule
"""+_rows+r"""\bottomrule
\end{tabular}
\end{center}
\end{table}""")

open(f"{L.ROOT}/frontiers/tables/tables_body.tex","w").write("\n\n".join(O)+"\n")
print("wrote frontiers/tables/tables_body.tex  (%d tables)"%len(O))
