#!/usr/bin/env python3
"""regenerate the revision figures. Deterministic, no network, 300 dpi, Okabe-Ito.
Run scripts/make_figures.py first for fig1 (flowchart) and fig3 (issuer Pareto), which are
unchanged; this script overwrites fig2 and fig4 with five-tier stacked versions and adds the
collapsed shadow-by-severity chart as a supplementary figure.
  fig2  stacked T1/T2/T3a/T3b/T4 by severity      (replaces the collapsed shadow-rate bars)
  fig4  stacked T1/T2/T3a/T3b/T4 by incident year (five-way)
  fig1  sample-construction flowchart, with the exact count on every exclusion branch
  figS1 collapsed shadow rate by severity with Wilson intervals (moved to the supplement)
"""
import csv,math,sys,os,collections
from pathlib import Path
import json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from stats_lib import load,TIERS5,dist
FIG=Path(L.ROOT)/"frontiers"/"figures"; FIG.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,
                     "axes.spines.right":False,"figure.dpi":300})
C={"T1":"#009E73","T2":"#0072B2","T3a":"#E69F00","T3b":"#F0D58C","T4":"#999999"}
LAB={"T1":"T1 incident-specific","T2":"T2 legal-consequence only",
     "T3a":"T3a generic, both families","T3b":"T3b generic, one family","T4":"T4 none located"}
D=load(); ALL=list(D.values())

# ---------------- fig1: PRISMA-style flowchart with every exclusion count ----------------
# Reviewer 2 point 1. Two reconciliations must hold and are asserted before the figure is drawn:
#   1,597 - 208 = 1,389 ;  1,389 - 398 - 400 - 243 = 348 ;  348 - 26 - 15 = 307 ;  307 - 4 = 303
N_SNAP,N_OUTWIN,N_WIN = 1597,208,1389
EX_GENERIC,EX_UNRESOLVED,EX_PRIVATE = 398,400,243
N_MATCHED,EX_FOREIGN,EX_DELISTED = 348,26,15
N_PRIMARY,N_FIXES,N_CORRECTED = 307,4,303
assert N_SNAP-N_OUTWIN==N_WIN
assert N_WIN-EX_GENERIC-EX_UNRESOLVED-EX_PRIVATE==N_MATCHED
assert N_MATCHED-EX_FOREIGN-EX_DELISTED==N_PRIMARY
assert EX_GENERIC+EX_UNRESOLVED+EX_PRIVATE+EX_FOREIGN+EX_DELISTED==N_WIN-N_PRIMARY==1082
assert N_PRIMARY-N_FIXES==N_CORRECTED
_D=dist(ALL,"tier_prereg"); _A=dist(ALL,"tier_adj")
FIXIDS=json.load(open(L.res("crosswalk_review.json")))["fix_ids_in_sample"]

def flowchart(path):
    """PRISMA-style flow, monochrome. Geometry rules, so arrows cannot drift out of alignment:
      * every main box is the SAME width and centred on the spine x = CX
      * BOXPAD matches the boxstyle padding, so an arrow endpoint is computed from the box's
        VISUAL edge, not its nominal rectangle; GAP is then a clear space between the arrow and
        the box it touches. Without this the arrowheads sit inside the rounded border.
      * each exclusion branch leaves the spine at the midpoint of a vertical gap and runs
        horizontally to its box, which is vertically CENTRED on that same midpoint
      * the main and exclusion columns are symmetric about x = 5, so the figure is centred"""
    EN="\u2013"
    BOXPAD, GAP = 0.10, 0.14          # BOXPAD must equal the boxstyle pad below
    MAIN_L,MAIN_W = 0.30,5.20 ; CX = MAIN_L+MAIN_W/2
    EX_L,EX_W     = 6.20,3.50
    assert abs(((MAIN_L)+(EX_L+EX_W))/2 - 5.0) < 0.02, "composition is not centred on x=5"
    assert MAIN_L+MAIN_W < EX_L, "main and exclusion columns overlap"
    INK,RULE = "#000000","#444444"
    fig,ax=plt.subplots(figsize=(8.0,8.9)); ax.axis("off")
    ax.set_xlim(0,10); ax.set_ylim(2.0,15.0)
    def box(y,h,text,lw=1.0,fs=8.4,bold=False,x=None,w=None):
        x=MAIN_L if x is None else x; w=MAIN_W if w is None else w
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad={BOXPAD}",
                     fc="white",ec=INK,lw=lw))
        ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,color=INK,
                fontweight="bold" if bold else "normal",linespacing=1.5)
    def spine(y_bottom_of_a,y_top_of_b):
        """vertical arrow, clear of both boxes' visual edges"""
        y0=y_bottom_of_a-BOXPAD-GAP; y1=y_top_of_b+BOXPAD+GAP
        assert y0-y1 >= 0.30, f"connector shaft too short ({y0-y1:.2f}); increase the vertical gap"
        ax.add_patch(FancyArrowPatch((CX,y0),(CX,y1),arrowstyle="-|>",
                     mutation_scale=12,lw=1.1,color=RULE,shrinkA=0,shrinkB=0))
    _EXSPANS=[]
    def branch(y,h,text):
        # a box must be tall enough for its own text: at fontsize 7.6 with linespacing 1.5 one
        # line occupies about 0.24 axis units, so 0.28 leaves margin. Without this an added line
        # silently spills through the border.
        assert h >= 0.28*text.count("\n")+0.28, \
            f"exclusion box of height {h:.2f} cannot hold {text.count(chr(10))+1} lines"
        _EXSPANS.append((y-h/2-BOXPAD,y+h/2+BOXPAD))
        ax.add_patch(FancyArrowPatch((CX,y),(EX_L-BOXPAD-GAP,y),arrowstyle="-|>",
                     mutation_scale=12,lw=1.0,color=RULE,shrinkA=0,shrinkB=0,linestyle=(0,(4,2))))
        box(y-h/2,h,text,lw=0.8,fs=7.6,x=EX_L,w=EX_W)
    # uniform 0.95 vertical gap between every pair of boxes, so every connector is the same length
    Y1,H1 = 13.90,0.90
    Y2,H2 = 12.05,0.90
    Y3,H3 = 10.20,0.90
    Y4,H4 =  8.25,1.00
    Y5,H5 =  6.00,1.30
    Y6,H6 =  3.75,1.30
    for (ya,ha),(yb,hb) in (((Y1,H1),(Y2,H2)),((Y2,H2),(Y3,H3)),((Y3,H3),(Y4,H4)),
                            ((Y4,H4),(Y5,H5)),((Y5,H5),(Y6,H6))):
        assert abs((ya-(yb+hb))-0.95)<0.01, f"gap is {ya-(yb+hb):.2f}, expected 0.95"
    box(Y1,H1,f"AIID snapshot 2026-07-27\n{N_SNAP:,} incident records")
    spine(Y1,Y2+H2); branch((Y1+Y2+H2)/2,0.80,
        f"Excluded: incident date\noutside 2019{EN}2026   {N_OUTWIN}")
    box(Y2,H2,f"Dated 2019{EN}2026\n{N_WIN:,} incidents (study window)")
    spine(Y2,Y3+H3); branch((Y2+Y3+H3)/2,1.70,
        "Excluded at organization identification\nand resolution:\n"
        f"generic / individual actors only   {EX_GENERIC}\n"
        f"named entity not in crosswalk   {EX_UNRESOLVED}\n"
        f"privately held firm   {EX_PRIVATE}\n"
        f"subtotal   {EX_GENERIC+EX_UNRESOLVED+EX_PRIVATE:,}")
    box(Y3,H3,f"Matched to a US-listed registrant\n{N_MATCHED} incidents")
    spine(Y3,Y4+H4); branch((Y3+Y4+H4)/2,1.35,
        "Excluded after matching:\n"
        f"foreign private issuer (20-F/6-K)   {EX_FOREIGN}\n"
        f"under the delisted-issuer rule   {EX_DELISTED}\n"
        f"subtotal   {EX_FOREIGN+EX_DELISTED}")
    box(Y4,H4,f"PRIMARY SAMPLE (pre-registered)\nN = {N_PRIMARY} incidents, 21 issuers",lw=1.8,bold=True)
    spine(Y4,Y5+H5)
    box(Y5,H5,"Four-tier disclosure coding\n12-month window, Forms 8-K / 10-K / 10-Q\n"
        f"T1 = {_D['T1']}    T2 = {_D['T2']}    T3 = {_D['T3a']+_D['T3b']}    T4 = {_D['T4']}\n"
        f"T3 relatedness split:  T3a = {_A['T3a']}    T3b = {_A['T3b']}",fs=8.0)
    spine(Y5,Y6+H6); branch((Y5+Y6+H6)/2,2.30,
        "Removed for the corrected sample\n(robustness only):\n"
        f"incident {FIXIDS[0]}, listed parent did not own\nthe entity at the incident date\n"
        f"incident {FIXIDS[1]}, issuer not yet an\nSEC periodic-report filer\n"
        "incidents 1436 and 1528, issuer does\nnot hold at the incident date")
    box(Y6,H6,f"CORRECTED SAMPLE (robustness)\nN = {N_CORRECTED} incidents\n"
        f"shadow {N_CORRECTED-7}/{N_CORRECTED} = {100*(N_CORRECTED-7)/N_CORRECTED:.1f}%, against "
        f"{N_PRIMARY-7}/{N_PRIMARY} = {100*(N_PRIMARY-7)/N_PRIMARY:.1f}%\non the primary sample",lw=1.4,fs=8.0)
    ax.text(5.0,3.05,f"Reconciliation:   {N_SNAP:,} {EN} {N_OUTWIN} = {N_WIN:,}      "
        f"{N_WIN:,} {EN} {EX_GENERIC} {EN} {EX_UNRESOLVED} {EN} {EX_PRIVATE} = {N_MATCHED}      "
        f"{N_MATCHED} {EN} {EX_FOREIGN} {EN} {EX_DELISTED} = {N_PRIMARY}      "
        f"{N_PRIMARY} {EN} {N_FIXES} = {N_CORRECTED}",ha="center",va="center",fontsize=7.3,color=RULE)
    ax.text(5.0,2.55,f"Total excluded from the {N_WIN:,} window incidents:   "
        f"{EX_GENERIC} + {EX_UNRESOLVED} + {EX_PRIVATE} + {EX_FOREIGN} + {EX_DELISTED} = 1,082, "
        "as stated in Section 3.1",ha="center",va="center",fontsize=7.3,color=RULE)
    spans=sorted(_EXSPANS)
    for (a0,a1),(b0,b1) in zip(spans,spans[1:]):
        assert a1 <= b0, f"exclusion boxes overlap: {a0:.2f}-{a1:.2f} and {b0:.2f}-{b1:.2f}"
    fig.savefig(path,bbox_inches="tight",pad_inches=0.06); plt.close(fig)
flowchart(FIG/"fig1.png")

def stacked(groups,labels,ns,path,xlabel=None,rot=0):
    fig,ax=plt.subplots(figsize=(7.4,4.3))
    bottom=[0.0]*len(labels)
    for t in TIERS5:
        vals=[100*groups[i].get(t,0)/ns[i] if ns[i] else 0 for i in range(len(labels))]
        ax.bar(labels,vals,bottom=bottom,color=C[t],label=LAB[t],width=0.72,edgecolor="white",lw=0.4)
        bottom=[b+v for b,v in zip(bottom,vals)]
    for i,n in enumerate(ns): ax.text(i,101,f"n={n}",ha="center",va="bottom",fontsize=7,color="#555")
    ax.set_ylabel("Share of incidents (%)"); ax.set_ylim(0,110); ax.set_yticks([0,25,50,75,100])
    if xlabel: ax.set_xlabel(xlabel)
    if rot: plt.setp(ax.get_xticklabels(),rotation=rot,ha="right")
    ax.legend(loc="lower center",bbox_to_anchor=(0.5,-0.34),ncol=3,frameon=False,fontsize=8)
    fig.savefig(path,bbox_inches="tight"); plt.close(fig)

# fig2 — by severity
order=["sev_severe","sev_moderate","sev_limited"]; slab=["Severe","Moderate","Limited"]
g=[collections.Counter(r['tier_adj'] for r in ALL if r['severity_band']==s) for s in order]
ns=[sum(1 for r in ALL if r['severity_band']==s) for s in order]
stacked(g,slab,ns,FIG/"fig2.png")
# fig4 — by year
yrs=sorted({r['incident_date'][:4] for r in ALL})
g4=[collections.Counter(r['tier_adj'] for r in ALL if r['incident_date'][:4]==y) for y in yrs]
n4=[sum(1 for r in ALL if r['incident_date'][:4]==y) for y in yrs]
stacked(g4,yrs,n4,FIG/"fig4.png",xlabel="Incident year")
# figS1 — collapsed shadow by severity, Wilson, retained in the supplement
def wilson(k,n,z=1.96):
    if not n: return (0,0,0)
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return p,(c-h)/d,(c+h)/d
ps=[];lo=[];hi=[]
for s in order:
    sub=[r for r in ALL if r['severity_band']==s]
    k=sum(1 for r in sub if r['tier_adj'] in ("T3a","T3b","T4")); p,l,h=wilson(k,len(sub))
    ps.append(100*p); lo.append(100*(p-l)); hi.append(100*(h-p))
fig,ax=plt.subplots(figsize=(5.6,4.0))
ax.bar(slab,ps,color="#E69F00",width=0.6,yerr=[lo,hi],capsize=5,ecolor="#333",edgecolor="white")
for i,(p,n) in enumerate(zip(ps,ns)): ax.text(i,p-8,f"{p:.1f}%\n(n={n})",ha="center",color="white",fontsize=8.5,fontweight="bold")
ax.set_ylabel("Shadow rate, T3+T4 (%)"); ax.set_ylim(0,105)
fig.savefig(FIG/"figS1.png",bbox_inches="tight"); plt.close(fig)
# mirror into the submission folder: this script overwrites fig2/fig4 after make_figures.py has copied
# them, so without this the portal-upload copies go stale.
# ---------- fig3: issuer Pareto ----------
# Incidents per issuer with the cumulative share. Carried over from the original figure
# script; it has no dependency on the revision recodes, so it is rebuilt from ALL as-is.
_byi=collections.Counter(r["matched_company"] for r in ALL).most_common()
_names=[c.replace(" Inc.","").replace(" Corporation","").replace(", Inc.","")
         .replace(" Group","").replace(" Platforms","").replace(" Company","")[:14] for c,_ in _byi]
_vals=[n for _,n in _byi]; _cum=[]; _s=0
for _v in _vals: _s+=_v; _cum.append(_s/sum(_vals)*100)
fig,ax=plt.subplots(figsize=(7.6,4.0))
ax.bar(range(len(_vals)),_vals,color="#0072B2",width=0.75)
ax.set_xticks(range(len(_vals))); ax.set_xticklabels(_names,rotation=55,ha="right",fontsize=7)
ax.set_ylabel("Incidents",color="#0072B2")
_ax2=ax.twinx(); _ax2.plot(range(len(_vals)),_cum,color="#D55E00",marker="o",ms=3,lw=1.3)
_ax2.set_ylabel("Cumulative %",color="#D55E00"); _ax2.set_ylim(0,105)
_ax2.spines["top"].set_visible(False)
fig.savefig(FIG/"fig3.png",bbox_inches="tight"); plt.close(fig)

import shutil
SUB=Path(L.ROOT)/"frontiers"/"submission"; SUB.mkdir(parents=True,exist_ok=True)
for i in (1,2,3,4): shutil.copy(FIG/f"fig{i}.png",SUB/f"Figure{i}.png")
shutil.copy(FIG/"figS1.png",SUB/"FigureS1.png")
# FIG is frontiers/figures, which is where the manuscript compiles from, so no further mirror
# is needed; the numbered Figure*.png copies for the submission package are written above.
print("regenerated:",", ".join(sorted(p.name for p in FIG.glob('fig*.png'))),"(mirrored to submission/)")
for s,n,gg in zip(slab,ns,g): print(f"   {s:<9} n={n:3d}  "+"  ".join(f"{t}={gg.get(t,0)}" for t in TIERS5))
