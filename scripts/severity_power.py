"""detectable-effect and power calculations for the severity contrast.

Power is computed EXACTLY rather than by simulation. Fisher's exact two-sided p-value is evaluated
once for every attainable 2x2 table (x successes of n_severe, y of n_limited); power at any pair of
true rates is then the binomial-weighted mass of the rejection region:
    power(p_s) = sum_x sum_y Binom(x; n_s, p_s) Binom(y; n_l, p_l) 1[ fisher_p(x,y) < alpha ]
This avoids the normal approximation, which is unreliable at 4/215 and 2/42, and needs no seed."""
import json,sys,os
import numpy as np
from scipy.stats import fisher_exact,binom
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L
from stats_lib import load
ALPHA=0.05

D=load(); ALL=list(D.values())
sev=[r for r in ALL if r['severity_band']=='sev_severe']
lim=[r for r in ALL if r['severity_band']=='sev_limited']
mod=[r for r in ALL if r['severity_band']=='sev_moderate']
n_s,n_l=len(sev),len(lim)
k_s=sum(1 for r in sev if r['tier_adj'] in ("T1","T2"))
k_l=sum(1 for r in lim if r['tier_adj'] in ("T1","T2"))
p_l=k_l/n_l
print(f"Severe   n={n_s:3d}  substantive={k_s}  ({k_s/n_s:.2%})")
print(f"Moderate n={len(mod):3d}  substantive={sum(1 for r in mod if r['tier_adj'] in ('T1','T2'))}")
print(f"Limited  n={n_l:3d}  substantive={k_l}  ({p_l:.2%})   <- baseline for the power calculations")

XMAX=min(n_s,25); YMAX=min(n_l,40)          # mass above these is negligible at the rates considered
REJ=np.zeros((XMAX+1,YMAX+1),dtype=bool)
for x in range(XMAX+1):
    for y in range(YMAX+1):
        REJ[x,y]= fisher_exact([[x,n_s-x],[y,n_l-y]])[1] < ALPHA
def power(p_s):
    px=binom.pmf(np.arange(XMAX+1),n_s,p_s); py=binom.pmf(np.arange(YMAX+1),n_l,p_l)
    return float((np.outer(px,py)*REJ).sum())

grid=np.round(np.arange(p_l,0.601,0.005),5); mde=None; curve=[]
for p_s in grid:
    pw=power(float(p_s)); curve.append((float(p_s),round(pw,4)))
    if mde is None and pw>=0.80: mde=float(p_s)
print(f"\n(a) minimum detectable Severe-arm substantive rate at 80% power, alpha=0.05: {mde:.1%}")
print(f"    = {mde/p_l:.1f}x the Limited-arm rate, a {100*(mde-p_l):.1f} percentage-point difference")
print(f"    in counts: {round(mde*n_s)} of {n_s} Severe incidents against {k_l} of {n_l} Limited")
pw3,pw5=power(3*p_l),power(5*p_l)
print(f"(b) power to detect 3x the Limited rate ({3*p_l:.1%}): {pw3:.1%}")
print(f"    power to detect 5x the Limited rate ({5*p_l:.1%}): {pw5:.1%}")
pw_obs=power(k_s/n_s)
print(f"(c) post-hoc power at the observed Severe rate ({k_s/n_s:.1%}): {pw_obs:.1%}")
print(f"    [post-hoc, reported for orientation only; it is not evidence about the null]")
json.dump(dict(n_severe=n_s,k_severe=k_s,n_moderate=len(mod),n_limited=n_l,k_limited=k_l,
  baseline_rate=p_l,alpha=ALPHA,method="exact binomial-weighted Fisher rejection region",
  mde_severe_rate_80pct=mde,mde_multiple=mde/p_l,mde_pp_difference=mde-p_l,
  mde_counts=f"{round(mde*n_s)}/{n_s} vs {k_l}/{n_l}",
  power_3x=pw3,power_5x=pw5,power_observed_posthoc=pw_obs,power_curve=curve),
  open(L.res("severity_power.json"),"w"),indent=1)
print("\nwrote",L.res("severity_power.json"))
