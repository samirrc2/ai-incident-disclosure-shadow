#!/usr/bin/env python3
"""p13_30_figures — publication figures (300 dpi, colorblind-safe Okabe-Ito). Deterministic.
Writes revision/figures/*.png. No network.
"""
import csv, math
from collections import Counter, defaultdict
from pathlib import Path
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
sys.path.insert(0, str(Path(__file__).resolve().parent))
import p13_config as _C0; _C0.ensure_out()
import p13_config as CFG
csv.field_size_limit(10_000_000)
FIG=CFG.FIGS; FIG.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,
                     "axes.spines.right":False,"figure.dpi":300})
# Okabe-Ito
C={"T1":"#009E73","T2":"#0072B2","T3":"#E69F00","T4":"#999999"}
LAB={"T1":"T1 disclosed-specific","T2":"T2 legal-proceedings-only","T3":"T3 generic-risk-language","T4":"T4 no disclosure"}

rows=list(csv.DictReader(open(CFG.CODED)))
def wilson(k,n,z=1.96):
    if n==0: return (0,0,0)
    p=k/n;d=1+z*z/n;c=p+z*z/(2*n);h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n));return p,(c-h)/d,(c+h)/d

# ---------- Fig 1: PRISMA flowchart ----------
fig,ax=plt.subplots(figsize=(7.2,6.4)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,12)
def box(x,y,w,h,text,fc="#f2f2f2",ec="#333"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08",fc=fc,ec=ec,lw=1.1))
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=8.6)
def arrow(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=12,lw=1.1,color="#333"))
box(2.5,10.7,5,1.0,"AIID snapshot 2026-07-27\n1,597 incidents",fc="#dce6f2")
arrow(5,10.7,5,10.0)
box(2.5,9.0,5,1.0,"Dated 2019–2026\n1,389 incidents")
arrow(5,9.0,5,8.3)
box(2.5,7.3,5,1.0,"Deployer/developer entity resolution\n(21,931 slug occurrences)")
arrow(5,7.3,5,6.6)
# exclusions to the right
box(6.9,5.0,3.0,1.5,"Excluded from primary:\n• generic/individual/non-corp\n• private firms (OpenAI, etc.)\n• foreign issuers (26)\n• delisted (15)",fc="#f7ecec",ec="#a55")
arrow(5,6.6,6.9,5.9)
box(2.9,5.0,3.2,1.1,"US domestic-listed issuer\n(8-K/10-K/10-Q filers)",fc="#e8f2e8")
arrow(4.5,6.6,4.5,6.1)
box(2.5,3.3,5,1.0,"PRIMARY SAMPLE\nN = 307 incidents · 21 issuers",fc="#d7ecd7",ec="#2a7")
arrow(5,3.3,5,2.6)
box(1.2,1.2,7.6,1.1,"Four-tier disclosure coding (12-mo window, 8-K/10-K/10-Q)\nT1=4 · T2=3 · T3=278 · T4=22",fc="#fdf3e0",ec="#c88")
ax.set_title("Figure 1. Sample construction",fontsize=11,loc="left")
fig.savefig(FIG/"fig1_flowchart.png",bbox_inches="tight"); plt.close(fig)

# ---------- Fig 2: tier by year (stacked, share) ----------
yrs=sorted(set(r["incident_date"][:4] for r in rows))
counts={y:Counter(r["disclosure_code"] for r in rows if r["incident_date"][:4]==y) for y in yrs}
ns={y:sum(counts[y].values()) for y in yrs}
fig,ax=plt.subplots(figsize=(7.2,4.2))
bottom=[0]*len(yrs)
for t in ["T1","T2","T3","T4"]:
    vals=[counts[y].get(t,0)/ns[y]*100 for y in yrs]
    ax.bar(yrs,vals,bottom=bottom,color=C[t],label=LAB[t],width=0.8,edgecolor="white",lw=0.4)
    bottom=[b+v for b,v in zip(bottom,vals)]
for i,y in enumerate(yrs): ax.text(i,101,f"n={ns[y]}",ha="center",va="bottom",fontsize=7,color="#555")
ax.set_ylabel("Share of incidents (%)"); ax.set_ylim(0,108); ax.set_yticks([0,25,50,75,100])
ax.legend(loc="lower center",bbox_to_anchor=(0.5,-0.32),ncol=2,frameon=False,fontsize=8.5)
ax.set_title("Figure 2. Disclosure tier by incident year",fontsize=11,loc="left")
fig.savefig(FIG/"fig2_tier_by_year.png",bbox_inches="tight"); plt.close(fig)

# ---------- Fig 3: shadow by severity with Wilson CIs ----------
order=["T3-severe","T2-moderate","T1-limited"]; slab={"T3-severe":"Severe","T2-moderate":"Moderate","T1-limited":"Limited"}
xs=[];ps=[];los=[];his=[];ns2=[]
for s in order:
    g=[r for r in rows if r["severity_tier"]==s]
    k=sum(1 for r in g if r["disclosure_code"] in ("T3","T4")); p,lo,hi=wilson(k,len(g))
    xs.append(slab[s]);ps.append(p*100);los.append((p-lo)*100);his.append((hi-p)*100);ns2.append(len(g))
fig,ax=plt.subplots(figsize=(5.6,4.0))
ax.bar(xs,ps,color="#E69F00",width=0.6,yerr=[los,his],capsize=5,ecolor="#333",edgecolor="white")
for i,(p,nn) in enumerate(zip(ps,ns2)): ax.text(i,p-8,f"{p:.1f}%\n(n={nn})",ha="center",color="white",fontsize=8.5,fontweight="bold")
ax.set_ylabel("Shadow rate T3+T4 (%)"); ax.set_ylim(0,105)
ax.set_title("Figure 3. Shadow rate by incident severity (95% Wilson CI)",fontsize=10.5,loc="left")
fig.savefig(FIG/"fig3_shadow_by_severity.png",bbox_inches="tight"); plt.close(fig)

# ---------- Fig 4: issuer Pareto ----------
byi=Counter(r["matched_company"] for r in rows).most_common()
names=[c.replace(" Inc.","").replace(" Corporation","").replace(", Inc.","").replace(" Group","").replace(" Platforms","").replace(" Company","")[:14] for c,_ in byi]
vals=[n for _,n in byi]; cum=[]; s=0
for v in vals: s+=v; cum.append(s/sum(vals)*100)
fig,ax=plt.subplots(figsize=(7.6,4.0))
ax.bar(range(len(vals)),vals,color="#0072B2",width=0.75)
ax.set_xticks(range(len(vals))); ax.set_xticklabels(names,rotation=55,ha="right",fontsize=7)
ax.set_ylabel("Incidents",color="#0072B2")
ax2=ax.twinx(); ax2.plot(range(len(vals)),cum,color="#D55E00",marker="o",ms=3,lw=1.3)
ax2.set_ylabel("Cumulative %",color="#D55E00"); ax2.set_ylim(0,105); ax2.spines["top"].set_visible(False)
ax.set_title("Figure 4. Incident concentration by issuer (Pareto)",fontsize=10.5,loc="left")
fig.savefig(FIG/"fig4_issuer_pareto.png",bbox_inches="tight"); plt.close(fig)

# ---------- Fig 5: AI-risk-language onset vs T4 share ----------
# onset years from issuer-year baseline reads during coding (documented in coding logs)
onset={"Alphabet":2018,"Meta":2019,"Tesla":2019,"Amazon":2019,"Microsoft":2023,"Apple":2023,"General Motors":2024}
fig,ax=plt.subplots(figsize=(6.8,3.6))
firms=list(onset); ys=[onset[f] for f in firms]
ax.scatter(ys,range(len(firms)),color="#009E73",s=45,zorder=3)
for i,f in enumerate(firms): ax.text(onset[f]+0.08,i,f,va="center",fontsize=8)
ax.set_yticks([]); ax.set_xlim(2017.5,2025); ax.set_xlabel("Fiscal year AI risk-factor language first appears in 10-K")
ax.set_title("Figure 5. Onset of AI risk-factor language by issuer\n(the T3/T4 boundary: incidents before onset are T4)",fontsize=10,loc="left")
ax.grid(axis="x",ls=":",alpha=0.5)
fig.savefig(FIG/"fig5_risklang_onset.png",bbox_inches="tight"); plt.close(fig)

print("wrote figures:", *[p.name for p in sorted(FIG.glob('*.png'))])
