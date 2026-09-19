"""every new number that appears in the revised manuscript or the response letter, mapped to
the script that produces it and the output file it lands in. Rule 2 of the revision brief."""
import csv, os, sys,json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
T=json.load(open(L.res("tables.json")))
P=json.load(open(L.res("severity_power.json")))
LO=json.load(open(L.res("role_loo.json")))
CO=json.load(open(L.res("cocandidates.json")))
AD=json.load(open(L.res("asofdate.json")))
CW=json.load(open(L.res("crosswalk_review.json")))
AT=json.load(open(L.res("attribution.json")))
TA=json.load(open(L.res("t2_adjudication.json")))
rows=[]
def a(claim,value,script,outfile,loc):
    rows.append(dict(claim=claim,value=value,script=script,output_file=outfile,manuscript_location=loc))
d={r['tier']:r for r in T['table1_adjudicated']['rows']}
pre={r['tier']:r for r in T['table1_prereg']['rows']}
a("T1 count and share, pre-registered",f"4/307 = 1.3% [0.4, 3.3]","scripts/tables.py","results/tables.json","Abstract; Table 2; §4.1")
a("T1 count and share, adjudicated",f"{d['T1']['n']}/307 = {100*d['T1']['share']:.1f}% [{100*d['T1']['lo']:.1f}, {100*d['T1']['hi']:.1f}]","scripts/tables.py","results/tables.json","Table 2; §4.1; §4.7")
a("T2 count, adjudicated",f"{d['T2']['n']}/307","scripts/t2_adjudicate.py","data/t2_adjudication.csv","§4.1; §4.7")
a("T3a count and share",f"{d['T3a']['n']}/307 = {100*d['T3a']['share']:.1f}% [{100*d['T3a']['lo']:.1f}, {100*d['T3a']['hi']:.1f}]","scripts/t3_split.py","data/t3_split.csv","Table 3; §4.2")
a("T3b count and share",f"{d['T3b']['n']}/307 = {100*d['T3b']['share']:.1f}% [{100*d['T3b']['lo']:.1f}, {100*d['T3b']['hi']:.1f}]","scripts/t3_split.py","data/t3_split.csv","Table 3; §4.2")
a("T3a share of the T3 mass",f"{d['T3a']['n']}/{d['T3a']['n']+d['T3b']['n']} = {100*d['T3a']['n']/(d['T3a']['n']+d['T3b']['n']):.1f}%","scripts/t3_split.py","data/t3_split.csv","§4.1; Discussion")
# The v1 (pre-completeness-pass) lexicon figure is quoted in Section 4.2 as a sensitivity.
# Recompute it here rather than carrying a literal, so it cannot fall out of date.
import subprocess as _sp, tempfile as _tf, shutil as _sh, collections as _co
_cur=L.out("t3_split.csv"); _bak=_tf.mktemp(suffix=".csv"); _sh.copy(_cur,_bak)
try:
    _env=dict(os.environ, REV1_LEXICON="v1")
    _sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),"t3_split.py")], env=_env,
            stdout=_sp.DEVNULL, stderr=_sp.DEVNULL, check=True)
    _c=_co.Counter(r["t3_split"] for r in csv.DictReader(open(_cur,newline="",encoding="utf-8",errors="replace")))
    _v1a,_v1b=_c["T3a"],_c["T3b"]
finally:
    _sh.copy(_bak,_cur); os.remove(_bak)
a("T3a share under the pre-spot-check lexicon (v1)",
  f"{_v1a}/{_v1a+_v1b} = {100*_v1a/(_v1a+_v1b):.1f}%",
  "REV1_LEXICON=v1 scripts/t3_split.py","data/t3_split.csv","§4.2 footnote; Supplementary S2")
a("Shadow, broad (T3a+T3b+T4) — unchanged primary",f"300/307 = 97.7% [95.4, 99.1]","scripts/tables.py","results/tables.json","Abstract; Table 2; §4.1")
a("Weakly-related-or-none (T3b+T4)",f"{d['weakly_related_or_none_T3bT4']['n']}/307 = {100*d['weakly_related_or_none_T3bT4']['share']:.1f}% [{100*d['weakly_related_or_none_T3bT4']['lo']:.1f}, {100*d['weakly_related_or_none_T3bT4']['hi']:.1f}]","scripts/tables.py","results/tables.json","Table 3; §4.2; Discussion")
a("None-located only (T4)",f"{d['none_only_T4']['n']}/307 = {100*d['none_only_T4']['share']:.1f}% [{100*d['none_only_T4']['lo']:.1f}, {100*d['none_only_T4']['hi']:.1f}]","scripts/tables.py","results/tables.json","Table 3")
for r in T['table2_severity']:
    a(f"severity {r['severity']}: n, T1, T1+T2 with CIs",
      f"n={r['n']}, T1={r['T1']} ({100*r['T1_share']:.1f}% [{100*r['T1_lo']:.1f},{100*r['T1_hi']:.1f}]), T1+T2 {100*r['sub_share']:.1f}% [{100*r['sub_lo']:.1f},{100*r['sub_hi']:.1f}]",
      "scripts/tables.py","results/tables.json","Table 4; §4.3")
a("MDE, Severe arm at 80% power",f"{100*P['mde_severe_rate_80pct']:.1f}% ({P['mde_multiple']:.1f}x the Limited rate; {P['mde_counts']})","scripts/severity_power.py","results/severity_power.json","§4.2")
a("power to detect a 3x relative difference",f"{100*P['power_3x']:.1f}%","scripts/severity_power.py","results/severity_power.json","§4.2")
a("power to detect a 5x relative difference",f"{100*P['power_5x']:.1f}%","scripts/severity_power.py","results/severity_power.json","§4.2")
a("post-hoc power at the observed effect",f"{100*P['power_observed_posthoc']:.1f}%","scripts/severity_power.py","results/severity_power.json","§4.2")
a("CSET-40 subset substantive count",f"{T['tableS5_cset40']['n_substantive']} of {T['tableS5_cset40']['n']}","scripts/tables.py","results/tables.json","Table S5; §4.3")
a("role 3-way contrast, chi2 and Monte-Carlo exact p",f"chi2={LO['baseline_adjudicated']['three_way'][0]}, p={LO['baseline_adjudicated']['three_way'][1]}","scripts/role_loo.py","results/role_loo.json","§4.4; Table 6")
a("role 2x2 contrast (developer-only vs any-deployer)",f"chi2={LO['baseline_adjudicated']['two_by_two'][0]}, p={LO['baseline_adjudicated']['two_by_two'][1]}","scripts/role_loo.py","results/role_loo.json","§4.4; Table 6")
a("LOO p-range, 3-way",f"{LO['p3_min']:.4f} to {LO['p3_max']:.4f}; >=0.05 in {LO['n_p3_nonsig']} of {LO['n_perturbations']}","scripts/role_loo.py","data/role_loo.csv","§4.4; Table S6")
a("LOO p-range, 2x2",f"{LO['p2_min']:.4f} to {LO['p2_max']:.4f}; >=0.05 in {LO['n_p2_nonsig']} of {LO['n_perturbations']}","scripts/role_loo.py","data/role_loo.csv","§4.4; Table S6")
a("incidents with >=2 listed-issuer candidates",f"{CO['n_multi_any']} of {CO['n_in_sample']} ({100*CO['n_multi_any']/CO['n_in_sample']:.1f}%); {CO['n_multi_domestic']} with >=2 domestic","scripts/cocandidates.py","data/cocandidates.csv","§3.2; Table S4a")
a("maximum candidate issuers on one incident",str(CO['max_candidates']),"scripts/cocandidates.py","data/cocandidates.csv","§3.2")
a("issuer changes under prefer-developer tie-break",str(CO['n_change_prefer_developer']),"scripts/cocandidates.py","data/cocandidates.csv","§3.2; Table 8")
a("issuer changes under prefer-parent tie-break",str(CO['n_change_prefer_parent']),"scripts/cocandidates.py","data/cocandidates.csv","§3.2; Table 8")
a("PARENT-linked incidents checked for as-of-date ownership",str(AD['n_parent_checked']),"scripts/asofdate.py","data/asofdate.csv","§3.2")
a("as-of-date failures",f"{len(AD['flagged_ids'])} (incident {', '.join(AD['flagged_ids'])})","scripts/asofdate.py","data/asofdate.csv","§3.2; Table 8")
a("crosswalk rows reviewed and verdict distribution",json.dumps(CW['verdicts']),"scripts/crosswalk_review.py","data/crosswalk_review.csv","§3.2; Table S4c")
a("crosswalk FIX rows inside the analytical sample",f"{len(CW['fix_ids_in_sample'])} (incidents {', '.join(CW['fix_ids_in_sample'])})","scripts/crosswalk_review.py","data/crosswalk_review.csv","§3.2; Table 8")
a("attribution-basis distribution",json.dumps(AT['basis_counts']),"scripts/attribution.py","data/attribution.csv","Table 5; §3.2")
ER=json.load(open(f"{L.ROOT}/results/entity_reliability.json"))
_ii=ER['issuer_identity']
a("entity-mapping agreement, issuer identity",
  f"{_ii['raw_agreement']*100:.1f}% ({round(_ii['raw_agreement']*_ii['n'])}/{_ii['n']}), kappa {_ii['cohens_kappa']:.2f}, AC1 {_ii['gwet_ac1']:.2f}",
  "scripts/entity_reliability.py","results/entity_reliability.json","§3.2; Limitations; Table S8")
a("entity-mapping agreement by stratum",
  "; ".join(f"{k} {v['agree']}/{v['n']}" for k,v in sorted(ER['issuer_by_stratum'].items())),
  "scripts/entity_reliability.py","results/entity_reliability.json","§3.2; Table S8")
a("entity-mapping agreement by the second coder's own confidence",
  "; ".join(f"{k} {v['agree']}/{v['n']} = {100*v['agree']/v['n']:.1f}%" for k,v in sorted(ER['issuer_by_confidence'].items())),
  "scripts/entity_reliability.py","results/entity_reliability.json","Table S8")
a("entity-mapping agreement on high-confidence rows",
  f"{ER['issuer_by_confidence']['high']['agree']}/{ER['issuer_by_confidence']['high']['n']}",
  "scripts/entity_reliability.py","results/entity_reliability.json","§3.2")
a("tiers of the issuer-identity disagreements",json.dumps(ER['disagreement_tiers']),
  "scripts/entity_reliability.py","results/entity_reliability.json","§3.2; Table S9")
for r in T['table4_robustness']:
    a(f"robustness: {r['variant']}",f"N={r['n']}, T1={r['T1']}, substantive={r['substantive']}, shadow={100*r['shadow_share']:.1f}% [{100*r['shadow_lo']:.1f},{100*r['shadow_hi']:.1f}]","scripts/tables.py","results/tables.json","Table 6")
a("T2 adjudication outcome",f"{TA['n_changed']} of {TA['n']} recoded; adjudicated T1={TA['adjudicated_T1']}, T2={TA['adjudicated_T2']}","scripts/t2_adjudicate.py","data/t2_adjudication.csv","§4.1; §4.7")
a("per-tier one-vs-rest kappa, T2","-0.023","scripts/reliability.py (existing)","results/reliability_ext.json","§4.6; Table S7")
a("Figure 1 reconciliation, stage counts","1,597 - 208 = 1,389; 1,389 - 398 - 400 - 243 = 348; 348 - 26 - 15 = 307; 307 - 2 = 305","scripts/make_figures.py","frontiers/figures/fig1.png","Figure 1; Suppl. S4")
a("Figure 1 total exclusions","398 + 400 + 243 + 26 + 15 = 1,082","scripts/make_figures.py","frontiers/figures/fig1.png","Figure 1; §3.1")
a("corrected-sample shadow shown in Figure 1","298/305 = 97.7%, against 300/307 = 97.7%","scripts/make_figures.py","frontiers/figures/fig1.png","Figure 1; Table 8")
a("severity test power quoted beside p = 0.61","23.3% power to detect a threefold difference, on seven substantive disclosures","scripts/severity_power.py","results/severity_power.json","§4.3; Discussion")
a("entity-audit sample size and strata","80; multi-candidate 27, parent-linked 30, small-issuer 13, other 10","scripts/entity_audit_sample.py","data/entity_audit_sample.csv","§3.2; §3.2")
with open(L.res("number_audit.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=["claim","value","script","output_file","manuscript_location"])
    w.writeheader(); w.writerows(rows)
print(f"number_audit.csv: {len(rows)} claims traced")
for r in rows[:6]: print(f"   {r['claim'][:52]:<54} {r['value'][:52]}")
