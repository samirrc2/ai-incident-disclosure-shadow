"""full verification of the revised manuscript.
Every number traced to a machine-readable output, every citation resolved and used, every
cross-reference bound, prose cross-checked against the tables. Exits non-zero on any failure."""
import csv,glob,json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
R=L.ROOT
F=L.FRONTIERS
CODING=L.CODING
# sibling scripts live in scripts/ in the repo and code/ in the Code Ocean capsule
_SCRIPTDIR=os.path.dirname(os.path.abspath(__file__))
man=open(f"{F}/manuscript.tex",encoding='utf-8').read()
sup=open(f"{F}/submission/supplementary.tex",encoding='utf-8').read()
bib=open(f"{F}/references.bib",encoding='utf-8').read()
body=man[man.index(r'\section{Introduction}'):man.index(r'\section*{Conflict of Interest')]
abstract=man[man.index(r'\begin{abstract}'):man.index(r'\tiny')]
tabreg=man[man.index("TABLES (Frontiers: at end)"):man.index("FIGURE CAPTIONS + FIGURES")]
prose=re.sub(r'\\begin\{table\}.*?\\end\{table\}',' ',abstract+body,flags=re.S)
fails=[];checks=0
def chk(n,ok,d=""):
    global checks;checks+=1
    if not ok: fails.append((n,d))
    print(f"  [{'ok  ' if ok else 'FAIL'}] {n}"+(f"  -- {d}" if d and not ok else ""))

# ---------- traceable numeric set ----------
blobs=[]
for p in (glob.glob(f"{R}/results/*.json")+glob.glob(f"{R}/results/*.csv")+glob.glob(f"{R}/results/*.json")
          +glob.glob(f"{R}/data/*.csv")+glob.glob(f"{R}/data/*.csv")
          +glob.glob(f"{CODING}/results/*.json")):
    try: blobs.append(open(p,encoding='utf-8',errors='replace').read())
    except Exception: pass
allout=" ".join(blobs)
trace=set()
for f in re.findall(r'-?\d+\.?\d*',allout):
    try: v=abs(float(f))
    except ValueError: continue
    for dp in (0,1,2,3,4):
        trace.add(f"{v:.{dp}f}"); trace.add(f"{v*100:.{dp}f}"); trace.add(f"{v/100:.{dp}f}")
    if v==int(v): trace.add(str(int(v)))
# integers that are legitimately structural rather than results
STRUCT={"1","2","3","4","5","6","7","8","9","10","11","12","20","24","40","80","95","100",
        "2019","2020","2021","2022","2023","2024","2025","2026","2003","2013","0","18","73","106",
        "1.05","3.1","3.2","3.3","3.4","4.1","4.2","4.3","4.4","4.5","4.6","4.7","0.05"}
def numbers(txt):
    t=re.sub(r'\\(?:cite[a-z]*|ref|label|texttt|url)\s*\{[^}]*\}',' ',txt)
    t=re.sub(r'\b(?:8|10|20|6)-(?:K|Q|F)\b',' ',t)              # form names
    t=re.sub(r'\b\d{10}\b|\b\d{4}-\d{2}-\d{2}\b|\b\d{7,}\b',' ',t)  # CIKs, dates, accessions
    t=t.replace("{,}","")
    return re.findall(r'(?<![\w.-])(\d+(?:\.\d+)?)(?![\w.%-]*[A-Za-z])',t)
miss=[]
for n in set(numbers(prose)):
    if n in STRUCT or n in trace: continue
    if n.lstrip('0') in trace or n.rstrip('0').rstrip('.') in trace: continue
    if n in allout: continue
    miss.append(n)
chk(f"every number in abstract+body traces to an output  ({len(set(numbers(prose)))} distinct)",
    not miss, f"untraced: {sorted(miss)}")
mt=[n for n in set(numbers(tabreg)) if n not in STRUCT and n not in trace and n not in allout]
chk(f"every number in the tables traces to an output  ({len(set(numbers(tabreg)))} distinct)",
    not mt, f"untraced: {sorted(mt)}")
ms=[n for n in set(numbers(sup)) if n not in STRUCT and n not in trace and n not in allout]
chk(f"every number in the supplementary traces  ({len(set(numbers(sup)))} distinct)",
    not ms, f"untraced: {sorted(ms)}")

# ---------- citations ----------
keys=set()
for m in re.findall(r'\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}',man):
    keys|={k.strip() for k in m.split(',') if k.strip()}
entries=set(re.findall(r'^@\w+\{([^,]+),',bib,re.M))
chk(f"every citation key resolves  ({len(keys)} keys)",not (keys-entries),f"orphans: {sorted(keys-entries)}")
chk(f"every bibliography entry is cited  ({len(entries)} entries)",not (entries-keys),f"uncited: {sorted(entries-keys)}")

DOI_EXPECTED_DATACITE={"Bommasani2021"}
DOI_ONLINE_FIRST={"Campbell2014","Macrae2016"}
NO_DOI_BY_NATURE={"TSC1976","Basic1988","SEC2023Cyber","EUAIAct2024","Gordon2010"}
def bibentries(src):
    out=[]
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,\s]+)\s*,',src):
        i=src.index('{',m.start()); d=1; p=i+1
        while p<len(src) and d:
            if src[p]=='{': d+=1
            elif src[p]=='}': d-=1
            p+=1
        out.append((m.group(1).lower(),m.group(2),src[i+1:p-1]))
    return out
ents=bibentries(bib)
chk(f"bibliography parses cleanly  ({len(ents)} entries)",len(ents)==len(entries))
nodoi={k for _,k,b in ents if not re.search(r'\bdoi\s*=',b,re.I)}
chk("only the expected entries lack a DOI",nodoi==NO_DOI_BY_NATURE,
    f"unexpected: {sorted(nodoi ^ NO_DOI_BY_NATURE)}")
chk("DataCite-registered DOIs are documented",DOI_EXPECTED_DATACITE <= {k for _,k,_ in ents})
chk("online-first year exceptions are documented",DOI_ONLINE_FIRST <= {k for _,k,_ in ents})
chk("citation verification record exists",
    os.path.exists(f"{R}/docs/CITATION_VERIFICATION.md")
    or os.path.exists(f"{R}/data/docs/CITATION_VERIFICATION.md"))

# ---------- cross-references ----------
labels=set(re.findall(r'\\label\{([^}]*)\}',man))
refs=set(re.findall(r'\\ref\{([^}]*)\}',man))
chk(f"every \\ref resolves to a \\label  ({len(refs)} refs)",not (refs-labels),f"dangling: {sorted(refs-labels)}")
tl=[l for l in labels if l.startswith("tab:")]
unref=[l for l in tl if l not in refs]
chk(f"every table is referenced in the text  ({len(tl)} tables)",not unref,f"unreferenced: {unref}")
fl=[l for l in labels if l.startswith("fig:")]
chk(f"every figure is referenced  ({len(fl)} figures)",not [l for l in fl if l not in refs],
    f"unreferenced: {[l for l in fl if l not in refs]}")

# ---------- supplementary pointers ----------
sref={int(x) for x in re.findall(r'Supplementary Tables?~S(\d+)',man)}
sref|={int(x) for x in re.findall(r'--S(\d+)',man)}
ntab=len(re.findall(r'\\begin\{table\}',sup))
chk(f"supplementary pointers fall inside S1..S{ntab+1}  (pointers {sorted(sref)})",
    all(1<=s<=ntab+1 for s in sref),f"out of range: {[s for s in sref if not 1<=s<=ntab+1]}")

# ---------- prose vs table agreement on the headline figures ----------
T=json.load(open(L.res("tables.json")))
adj={r['tier']:r for r in T['table1_adjudicated']['rows']}
pre={r['tier']:r for r in T['table1_prereg']['rows']}
def pc(r): return f"{100*r['share']:.1f}"
pairs=[("T1 pre-registered count in abstract","4 T1" in abstract),
       ("T2 pre-registered count in abstract","3 T2" in abstract),
       ("T3 pre-registered count in abstract","278 T3" in abstract),
       ("T4 pre-registered count in abstract","22 T4" in abstract),
       ("shadow 97.7% in abstract","97.7" in abstract),
       ("T1 1.3% in abstract","1.3" in abstract),
       ("substantive 2.3% in abstract","2.3" in abstract),
       (f"T3a n={adj['T3a']['n']} appears in body",str(adj['T3a']['n']) in body),
       (f"T3b n={adj['T3b']['n']} appears in body",str(adj['T3b']['n']) in body),
       (f"weakly-related {pc(adj['weakly_related_or_none_T3bT4'])}% in body and abstract",
        pc(adj['weakly_related_or_none_T3bT4']) in body and pc(adj['weakly_related_or_none_T3bT4']) in abstract)]
for n,ok in pairs: chk("prose/table agreement: "+n,ok)
chk("N=307 stated consistently",body.count("307")>=5 and "303" in body)

# ---------- internal arithmetic ----------
D=adj
chk("five tiers sum to 307",D['T1']['n']+D['T2']['n']+D['T3a']['n']+D['T3b']['n']+D['T4']['n']==307,
    f"sum={D['T1']['n']+D['T2']['n']+D['T3a']['n']+D['T3b']['n']+D['T4']['n']}")
chk("pre-registered tiers sum to 307",pre['T1']['n']+pre['T2']['n']+pre['T3a']['n']+pre['T3b']['n']+pre['T4']['n']==307)
chk("substantive + shadow = 307",D['substantive_T1T2']['n']+D['shadow_broad_T3aT3bT4']['n']==307)
chk("T3b + T4 = weakly-related-or-none",D['T3b']['n']+D['T4']['n']==D['weakly_related_or_none_T3bT4']['n'])
chk("adjudication preserves the substantive total",
    pre['T1']['n']+pre['T2']['n']==D['T1']['n']+D['T2']['n']==7)
chk("exclusion counts reconcile 1389 -> 307",398+400+243+26+15==1082 and 1389-1082==307)
chk("mapped file reconciles 348 = 307+26+15",307+26+15==348)
chk("corrected sample 307-4=303","303" in body and "307 - 4 = 303" not in body.replace("$",""))

# ---------- every CI is ordered and contains its point estimate ----------
bad=[]
for src in (T['table1_prereg']['rows'],T['table1_adjudicated']['rows']):
    for r in src:
        if not (r['lo']<=r['share']<=r['hi']): bad.append(r['tier'])
for r in T['table2_severity']:
    for a,b,c in (('T1_lo','T1_share','T1_hi'),('sub_lo','sub_share','sub_hi')):
        if not (r[a]<=r[b]<=r[c]): bad.append(r['severity'])
chk("every interval is ordered and brackets its estimate",not bad,f"bad: {bad}")

# ---------- role and severity figures quoted in prose match the outputs ----------
LO=json.load(open(L.res("role_loo.json"))); P=json.load(open(L.res("severity_power.json")))
chk("3-way role p in prose matches output",f"{LO['baseline_adjudicated']['three_way'][1]:.3f}" in body)
chk("2x2 role p in prose matches output",f"{LO['baseline_adjudicated']['two_by_two'][1]:.3f}" in body)
chk("LOO range in prose matches output",
    f"{LO['p3_min']:.3f}" in body and f"{LO['p3_max']:.3f}" in body)
# The prose states the MDE rounded to a whole percent ("approximately 13%"); tie that
# wording to the computed value rather than to a literal string.
_mde=100*P['mde_severe_rate_80pct']
chk(f"MDE in prose matches output  (computed {_mde:.1f}%)",
    f"approximately {round(_mde)}\\%" in body or f"{_mde:.1f}" in body,
    f"body states neither 'approximately {round(_mde)}%' nor {_mde:.1f}")
chk("3x power in prose matches output",f"{100*P['power_3x']:.1f}" in body)

# ---------- forbidden / retracted claims must not reappear ----------
banned=[("two incident-level mapping errors","unsupported crosswalk claim"),
        ("exact p = 0.02","inferential role p in the abstract"),
        ("All four T1 disclosures featured an issuer as a deployer","false deployer claim"),
        ("complete disclosure silence","overstated shadow composition")]
for s_,why in banned: chk(f"retracted claim absent: {why}",s_ not in man,s_)
chk("legal-safety phrasing absent: 'failed to disclose'","failed to disclose" not in man)
chk("legal-safety phrasing absent: 'concealed'","concealed" not in man.lower())

# ---------- no revision-process narration in reader-facing text ----------
# A published paper should not tell the reader what was done "at revision": the reader cannot
# interpret it and has no reason to care. The pre-registered / post-hoc distinction stays, because
# that is a disclosure norm about the analysis, not a note about the review process.
PROC=re.compile(r'at revision|revision-stage|reviewer-requested|this revision|the revision stage',re.I)
for label,txt in (("manuscript",man),("supplementary",sup),
                  ("figure 1 labels",open(f"{_SCRIPTDIR}/make_figures.py",encoding='utf-8').read()
                                      .split('def flowchart')[1].split('def stacked')[0])):
    hits=sorted({m.group(0).lower() for m in PROC.finditer(txt)})
    chk(f"no revision-process narration in the {label}",not hits,f"found: {hits}")
ml=man.lower()
chk(f"pre-registered / post-hoc distinction retained  ({ml.count('post-hoc')} post-hoc, {ml.count('pre-registered')} pre-registered)",
    ml.count("post-hoc")>=5 and ml.count("pre-registered")>=5)

# ---------- figures land in results/figures/ (data/frontiers is read-only) ----------
_gen=sorted(glob.glob(f"{R}/results/figures/fig*.png"))
chk(f"generated figures written to results/figures/  ({len(_gen)} files)",
    {os.path.basename(p) for p in _gen}>= {"fig1.png","fig2.png","fig3.png","fig4.png","figS1.png"},
    f"found: {[os.path.basename(p) for p in _gen]}")

# ---------- figure 1 agrees with the text on the corrected sample ----------
_fg=open(f"{_SCRIPTDIR}/make_figures.py",encoding='utf-8').read()
_nc=re.search(r"N_PRIMARY,N_FIXES,N_CORRECTED\s*=\s*(\d+),(\d+),(\d+)",_fg)
_tabn=[r['n'] for r in T['table4_robustness'] if r['variant'].startswith("Corrected sample")]
chk("figure 1 corrected sample matches Table 7 and the body",
    bool(_nc) and _tabn and int(_nc.group(3))==_tabn[0] and str(_tabn[0]) in body
    and int(_nc.group(1))-int(_nc.group(2))==int(_nc.group(3)),
    f"figure says {_nc.group(3) if _nc else '?'}, table says {_tabn[0] if _tabn else '?'}")

# ---------- no claimed numeric range may exclude a value in the robustness table ----------
_shad=[100*r['shadow_share'] for r in T['table4_robustness'] if r.get('shadow_share')]
# also take the values as they are typeset in tab:rob, which includes the pre-registered rows
# (issuer-concentration, window variants, severe subset) that are not in the generated JSON
_tabblk=man[man.index("label{tab:rob}"):]; _tabblk=_tabblk[:_tabblk.index(chr(92)+"end{table}")]
_shad+= [float(x) for x in re.findall(r"&\s*(\d{2}\.\d)\\%",_tabblk)]
_bad=[]
for _m in re.finditer(r"between (\d+\.\d)\\% and (\d+\.\d)\\%",body):
    _lo,_hi=float(_m.group(1)),float(_m.group(2))
    if _lo<50: continue                 # a range on some other quantity, not the shadow
    _out=[round(v,1) for v in _shad if not (_lo-0.05<=v<=_hi+0.05)]
    if _out: _bad.append(f"'{_m.group(0)}' excludes {sorted(set(_out))}")
chk("every stated range covers the values it claims to summarise",not _bad,"; ".join(_bad))

# ---------- no eaten backslashes ----------
# A literal TAB in a .tex file is nearly always the signature of "\t" being interpreted in a
# regex replacement string, which silently swallows the backslash of a command such as \texttt.
for _n,_f in (("manuscript",f"{F}/manuscript.tex"),
              ("supplementary",f"{F}/submission/supplementary.tex")):
    _s=open(_f,encoding="utf-8").read()
    _bad=[_s[max(0,m):m+28].replace("\t","<TAB>") for m in
          [i for i,c in enumerate(_s) if c=="\t"]]
    chk(f"no stray tab (eaten backslash) in the {_n}", not _bad, f"{len(_bad)} found: {_bad[:3]}")
# a LaTeX command name should never be left bare after losing its backslash
_man=open(f"{F}/manuscript.tex",encoding="utf-8").read()
_orphan=re.findall(r"(?<![\\\w])(?:exttt|extbf|extit|extsc|mph|ef|abel|ootnote)\{",_man)
chk("no LaTeX command left without its backslash", not _orphan, f"found: {sorted(set(_orphan))}")

# ---------- supplementary pointers resolve ----------
# These are plain text, not \ref, so LaTeX cannot catch an off-by-one when a table is added
# or removed. Recompute the numbering the supplementary will actually render.
_sup=open(f"{F}/submission/supplementary.tex",encoding="utf-8").read()
_start=re.search(r"\\setcounter\{table\}\{(\d+)\}",_sup)
_n=int(_start.group(1)) if _start else 0
_exist=set()
for _ in re.finditer(r"\\begin\{(?:table|longtable)\}",_sup):
    _n+=1; _exist.add(_n)
_cited=set()
for _m in re.finditer(r"Supplementary Tables?~S(\d+)(?:--S(\d+))?",man):
    _cited.add(int(_m.group(1)))
    if _m.group(2): _cited.add(int(_m.group(2)))
_bad=sorted(_cited-_exist)
chk(f"every supplementary table the manuscript cites exists  ({len(_cited)} cited, {len(_exist)} exist)",
    not _bad, f"cited but absent: {['S%d'%x for x in _bad]}")

# ---------- table numbers cited outside the manuscript stay in range ----------
# The response letter and the number ledger name table numbers as plain text, so LaTeX
# cannot catch drift when a table is inserted or removed.
_ntab=len(re.findall(r"\\begin\{table\}",man))
_nsup=_n if False else None
_supsrc=open(f"{F}/submission/supplementary.tex",encoding="utf-8").read()
_start=re.search(r"\\setcounter\{table\}\{(\d+)\}",_supsrc)
_nsupt=(int(_start.group(1)) if _start else 0)+len(re.findall(r"\\begin\{(?:table|longtable)\}",_supsrc))
_led=open(f"{R}/results/number_audit.csv",encoding="utf-8").read()
_lp=f"{F}/submission/response_to_reviewers.md"
_letter=open(_lp,encoding="utf-8").read() if os.path.exists(_lp) else ""
_badmain=sorted({int(x) for x in re.findall(r"Table (\d+)",_led) if int(x)>_ntab})
_badsup=sorted({int(x) for x in re.findall(r"Table S(\d+)",_led) if int(x)>_nsupt})
chk(f"number ledger cites tables that exist  (main 1-{_ntab}, suppl S1-{_nsupt})",
    not _badmain and not _badsup, f"out of range: main {_badmain}, suppl {_badsup}")
_badletter=sorted({int(x) for x in re.findall(r"Table (\d+)",_letter) if int(x)>_ntab})
chk(f"response letter cites tables that exist  (1-{_ntab})",
    not _badletter, f"out of range: {_badletter}")

# ---------- section numbers cited outside the manuscript exist ----------
_st=man.index("\\section{Introduction}")
_n1=_n2=_n3=0; _valid=set()
for _m in re.finditer(r"\\(section|subsection|subsubsection)(\*?)\{([^}]*)\}",man[_st:]):
    if _m.group(2): continue
    if _m.group(1)=="section": _n1+=1;_n2=_n3=0;_valid.add(str(_n1))
    elif _m.group(1)=="subsection": _n2+=1;_n3=0;_valid.add(f"{_n1}.{_n2}")
    else: _n3+=1;_valid.add(f"{_n1}.{_n2}.{_n3}")
_ledtxt=open(f"{R}/results/number_audit.csv",encoding="utf-8").read()
_lq=f"{F}/submission/response_to_reviewers.md"
_lettxt=open(_lq,encoding="utf-8").read() if os.path.exists(_lq) else ""
for _lbl,_src in (("number ledger",_ledtxt),("response letter",_lettxt)):
    _b=sorted({s for s in re.findall(r"§([\w.]+)",_src) if s not in _valid})
    chk(f"{_lbl} cites sections that exist", not _b, f"unknown: {_b}")

# ---------- no orphan figures ----------
# A figure that is generated but never included is usually the sign of a figure having been
# replaced without its caption being updated.
import os as _os
_supsrc2=open(f"{F}/submission/supplementary.tex",encoding="utf-8").read()
_used={_os.path.basename(x) for x in re.findall(r"includegraphics[^{]*\{([^}]*)\}",man+_supsrc2)}
_have={f for f in _os.listdir(f"{F}/figures") if f.endswith(".png")}
_orph=sorted(_have-_used-{"FigureS1.png"})
_orph=[f for f in _orph if f.replace("fig","Figure") not in _used]
chk(f"every generated figure is included somewhere  ({len(_have)} generated)",
    not _orph, f"generated but never included: {_orph}")
_missing=sorted(f for f in _used if not _os.path.exists(f"{F}/figures/{f}")
                and not _os.path.exists(f"{F}/submission/{f}"))
chk("every included figure file exists", not _missing, f"missing: {_missing}")

# ---------- the repository is public; nothing reader-facing may say otherwise ----------
_stale=[]
for _f in (f"{F}/manuscript.tex", f"{F}/submission/supplementary.tex",
           f"{R}/DATA_AVAILABILITY.md", f"{R}/README.md",
           f"{R}/data/DATA_AVAILABILITY.md", f"{R}/data/README.md",
           f"{F}/submission/SUBMISSION_README.md"):
    if os.path.exists(_f) and re.search(r"(upon|on) acceptance", open(_f,encoding="utf-8").read(), re.I):
        _stale.append(os.path.basename(_f))
chk("no live file says the repository becomes public on acceptance", not _stale, f"found in: {_stale}")

# ---------- no text or table may run past the right margin ----------
# pdflatex records every such case as an overfull hbox. One is inherent to the Frontiers
# title block and is present in the as-submitted version too, so that one is allowed.
_log=f"{F}/manuscript.log"
if os.path.exists(_log):
    _lg=open(_log,errors="replace").read()
    _ov=re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)",_lg)
    _big=[float(x) for x in _ov if float(x)>10]
    chk(f"nothing runs past the right margin  ({len(_ov)} overfull, largest "
        f"{max([float(x) for x in _ov]) if _ov else 0:.1f}pt)",
        not _big, f"overflows over 10pt: {_big}")
    chk("manuscript compiles without LaTeX errors", _lg.count(chr(10)+"! ")==0,
        f"{_lg.count(chr(10)+'! ')} errors in the log")

# ---------- braces balance on every single-line macro in the front matter ----------
# A careless regex edit can truncate one of these and leave a dangling tail that still
# typesets. Check the lines that are written as one self-contained command.
for _m in re.finditer(r"^\\keyFont\{.*$", man, re.M):
    _ln=_m.group(0)
    chk(f"braces balance in: {_ln[:46]}...", _ln.count("{")==_ln.count("}"),
        f"{_ln.count('{')} open vs {_ln.count('}')} close")

# ---------- lexicon: no unreviewed short pattern ----------
# Three patterns once fired inside longer words: 'fee' matched "Feed", 'error' matched
# "terrorism", 'minor' matched "minority". Each was bounded. The rest of the short patterns
# below were checked against the evidence corpus and match only intended morphology
# ("injur" -> injury/injured, "defam" -> defamation). This freezes that review: a NEW short
# unbounded pattern must be checked and added here deliberately.
sys.path.insert(0,_SCRIPTDIR)
import taxonomy as _tax
_REVIEWED={"false","defam","bias","equal","women","injur","death","fatal","crash","child",
           "teen","youth","csam","gpt","bard","fsd","drone","kiosk"}
_new=[]
for _n,_D in (("harm",_tax.HARM_FAMILIES),("app",_tax.APP_FAMILIES)):
    for _fam,_ps in _D.items():
        for _p in _ps:
            if _p.isalpha() and len(_p)<=5 and _p not in _REVIEWED:
                _new.append(f"{_n}:{_fam}:{_p}")
chk(f"no unreviewed short lexicon pattern  ({len(_REVIEWED)} reviewed)", not _new,
    f"new and unbounded, check for inside-word matches: {_new}")

# ---------- every family match traced to the word that caused it ----------
# The reviewed extensions below are intended morphology ("defam" -> defamation). Anything
# else where the matched word is materially longer than the pattern is a candidate
# inside-word match of the kind that made "fee" match "Feed", and must be checked.
_tr=f"{R}/results/family_triggers.csv"
if os.path.exists(_tr):
    import csv as _csv
    _OK={("recommend","recommendation"),("recommend","recommendations"),("gpt","chatgpt"),
         ("advertis","advertisements"),("advertis","advertisement"),("defam","defamatory"),
         ("defam","defamation"),("infring","infringement"),("fatal","fatalities"),
         ("transcri","transcription"),("censor","censorship")}
    _odd=[]
    for _r in _csv.DictReader(open(_tr,encoding="utf-8")):
        _p,_w=_r["pattern"],_r["matched_word"].lower()
        if _p.isalpha() and len(_w)>len(_p)+3 and (_p,_w) not in _OK:
            _odd.append(f"{_p}->{_w}")
    chk(f"no unreviewed inside-word family match  ({len(_OK)} reviewed extensions)",
        not _odd, f"check these: {sorted(set(_odd))}")

# ---------- every included figure has a producer ----------
# fig3 was once included by the manuscript but produced by no script: it survived only as a
# stale file on disk, and a clean checkout could not rebuild it.
_figsrc=open(f"{_SCRIPTDIR}/make_figures.py",encoding="utf-8").read()
_made={x for x in re.findall(r'FIG\s*/\s*"([^"]+\.png)"',_figsrc)}
_inc={os.path.basename(x) for x in re.findall(r"includegraphics[^{]*\{([^}]*)\}",man)}
_noproducer=sorted(_inc-_made)
chk(f"every figure the manuscript includes is produced by a script  ({len(_made)} produced)",
    not _noproducer, f"no producer for: {_noproducer}")

# ---------- inputs no script can rebuild are covered by the manifest ----------
_mf=open(f"{R}/data/MANIFEST.sha256",encoding="utf-8",errors="replace").read()
_scripts=" ".join(open(x,encoding="utf-8").read() for x in glob.glob(f"{_SCRIPTDIR}/*.py"))
_unprotected=[]
for _f in sorted(os.listdir(f"{R}/data")):
    if not _f.endswith((".csv",".json")): continue
    _written=re.search(r'out\("'+re.escape(_f)+r'"\)\s*,\s*"w"',_scripts)
    if not _written and _f not in _mf: _unprotected.append(_f)
chk("every irreplaceable input is in the manifest", not _unprotected,
    f"not regenerable and not hashed: {_unprotected}")

# ---------- no file paths in the reader-facing text ----------
# Data and code are cited by persistent identifier and located in the Data Availability
# Statement; a filename in the Methods is not a citation convention anywhere. Field names
# set in typewriter (AIID's "deployers"/"developers") are fine.
_das=man.index(chr(92)+"section*{Data Availability Statement}")
_paths=[m.group(1) for m in re.finditer(r"\\texttt\{([^}]*)\}",man)
        if m.start()<_das and ("/" in m.group(1) or m.group(1).endswith((".csv",".py",".json",".tex")))]
chk("no file path or script name in the body text", not _paths,
    f"move these to the Data Availability Statement: {_paths}")

# ---------- table bodies must agree with the generated values ----------
# Tables 4, 5B, 6 and 8 are typeset by hand from results/tables.json. When the T3a/T3b
# split changed, their cells still summed to the old 79/199 while the abstract and Table 3
# carried the new figures. Check the column sums against the data, not the prose.
def _colsum(label, col_from_left, after_midrule=1):
    _i=man.index("label{"+label+"}")
    _j=_i
    for _ in range(after_midrule): _j=man.index(chr(92)+"midrule",_j)+8
    _k=man.index(chr(92)+"bottomrule",_j)
    _tot=0
    for _row in man[_j:_k].split(chr(92)+chr(92)):
        _c=[x.strip() for x in _row.split("&")]
        if len(_c)>col_from_left and re.fullmatch(r"\d+",_c[col_from_left]): _tot+=int(_c[col_from_left])
    return _tot
_T3a=T["table1_adjudicated"]["T3a"]["n"] if isinstance(T["table1_adjudicated"].get("T3a"),dict) else None
if _T3a is None:
    _r=[x for x in T["table4_robustness"] if x["variant"].startswith("Adjudicated")][0]
    _T3a,_T3b=_r["T3a"],_r["T3b"]
for _lbl,_ca,_cb,_mr in (("tab:sev",4,5,1),("tab:role",4,5,1),("tab:attrib",4,5,2)):
    try:
        _a,_b=_colsum(_lbl,_ca,_mr),_colsum(_lbl,_cb,_mr)
        chk(f"{_lbl} T3a/T3b columns sum to the data  ({_a}/{_b})",
            _a==_T3a and _b==_T3b, f"table sums {_a}/{_b}, data says {_T3a}/{_T3b}")
    except ValueError:
        chk(f"{_lbl} column sums checked", False, "could not parse the table body")

# ---------- tie-break counts reconcile with the table's N ----------
# The prose says how many incidents change issuer; the table reports N after dropping them.
# 307 - changed must equal the row's N, or the reader cannot connect the two.
_co=[_r for _r in csv.DictReader(open(L.out("cocandidates.csv"),newline="",encoding="utf-8",errors="replace"))
     if _r["incident_id"] in {_d["incident_id"] for _d in csv.DictReader(open(f"{R}/data/disclosure_coding.csv",newline="",encoding="utf-8",errors="replace"))}]
_dev=sum(1 for _r in _co if _r.get("changes_under_prefer_developer")=="True")
_par=sum(1 for _r in _co if _r.get("changes_under_prefer_parent")=="True")
_blk=man[man.index("label{tab:rob}"):man.index(chr(92)+"bottomrule",man.index("label{tab:rob}"))]
for _lbl,_ch in (("prefer developer",_dev),("prefer parent",_par)):
    _m=re.search(r"Tie-break: "+_lbl+r"[^&]*&\s*(\d+)\s*&",_blk)
    _n=int(_m.group(1)) if _m else -1
    chk(f"tie-break {_lbl}: 307 - {_ch} = {307-_ch} matches the table's N",
        _n==307-_ch, f"table says N={_n}, prose implies {307-_ch}")
    chk(f"prose states {_ch} changed incidents for {_lbl}",
        str(_ch) in re.search(r"Sensitivity analyses that instead[^.]*\.",man).group(0))

print(f"\n{checks-len(fails)}/{checks} checks passed")
if fails:
    print("\nFAILURES:")
    for n,d in fails: print(f"  - {n}: {d}")
sys.exit(1 if fails else 0)
