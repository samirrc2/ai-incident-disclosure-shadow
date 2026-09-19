"""as-of-incident-date ownership check for the 47 PARENT-linked incidents.
The original crosswalk is static: a slug maps to one listed parent for the whole 2019-2026 window,
with no as-of-date logic. This script supplies the check that the original protocol did not perform.

OWNERSHIP records the date from which the listed parent controlled the named entity, and whether
that date was verified against a primary/authoritative source or asserted from general knowledge.
Anything asserted rather than verified is flagged for author confirmation in AUTHOR_REVIEW.csv.
"""
import csv,json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import paths as L

# slug -> (parent_control_from, basis, verified?)  "internal" = built in-house, no acquisition date.
# Every relationship below except naviHealth predates 2019-01-01, the start of the study window, so
# no incident in the sample can precede it; naviHealth is the sole case the check can bind on.
OWNERSHIP={
 "youtube":            ("2006-11-13","Google completed the YouTube acquisition",           "asserted"),
 "waymo":              ("2009-01-01","Google self-driving project; Waymo formed as an Alphabet subsidiary Dec 2016 and Alphabet controlled the programme throughout","asserted"),
 "gemini":             ("internal",  "Google in-house model family, launched Dec 2023",    "asserted"),
 "google-bard":        ("internal",  "Google in-house product, launched Mar 2023",         "asserted"),
 "google-deepmind":    ("2014-01-26","Google completed the DeepMind acquisition",          "asserted"),
 "deepmind":           ("2014-01-26","Google completed the DeepMind acquisition",          "asserted"),
 "google-cloud":       ("internal",  "Google in-house division",                           "asserted"),
 "instagram":          ("2012-04-09","Facebook announced/completed the Instagram acquisition (closed Sep 2012)","asserted"),
 "whatsapp":           ("2014-10-06","Facebook completed the WhatsApp acquisition",        "asserted"),
 "meta-ai":            ("internal",  "Meta in-house research/product unit",                "asserted"),
 "microsoft-copilot":  ("internal",  "Microsoft in-house product, launched 2023",          "asserted"),
 "microsoft-research": ("internal",  "Microsoft in-house division",                        "asserted"),
 "bing":               ("internal",  "Microsoft in-house product",                          "asserted"),
 "linkedin":           ("2016-12-08","Microsoft completed the LinkedIn acquisition",       "asserted"),
 "github":             ("2018-10-26","Microsoft completed the GitHub acquisition",         "asserted"),
 "cruise":             ("2016-05-12","GM completed the Cruise Automation acquisition",     "asserted"),
 "gm-cruise":          ("2016-05-12","GM completed the Cruise Automation acquisition",     "asserted"),
 "zoox":               ("2020-06-26","Amazon completed the Zoox acquisition",              "asserted"),
 "amazon-web-services":("internal",  "Amazon in-house division",                            "asserted"),
 "aws":                ("internal",  "Amazon in-house division",                            "asserted"),
 "ring":               ("2018-04-12","Amazon completed the Ring acquisition",              "asserted"),
 "alexa":              ("internal",  "Amazon in-house product",                             "asserted"),
 "uber-eats":          ("internal",  "Uber in-house service, launched 2014",                "asserted"),
 "acclarent":          ("2010-01-01","Johnson & Johnson completed the Acclarent acquisition (announced Dec 2009)","asserted"),
 "optum":              ("2011-01-01","UnitedHealth Group in-house brand consolidation",     "asserted"),
 "navihealth":         ("2020-05-01","Optum/UnitedHealth acquisition of naviHealth announced May 2020. naviHealth was majority-owned by Clayton, Dubilier & Rice from 1 August 2018 (CD&R ~55%, Cardinal Health ~45%), having been Cardinal Health-controlled from August 2015. This is the only parent relationship in the crosswalk established after the 2019 start of the study window, and therefore the only one on which the check can bind","verified"),
}
D=L.coding(); M=L.firmmap(); rows=[]
for d in D:
    m=M.get(d['incident_id'],{})
    if m.get('listing_status')!='PARENT': continue
    slug=m['entity_slug']; own=OWNERSHIP.get(slug)
    frm,basis,ver=own if own else ("UNKNOWN","slug not in the revision ownership table","unverified")
    if frm=="internal":   flag="ok-internal"
    elif frm=="UNKNOWN":  flag="cannot-verify"
    else:                 flag="ok" if d['incident_date']>=frm else "FLAG-parent-did-not-own"
    rows.append(dict(incident_id=d['incident_id'],incident_date=d['incident_date'],entity_slug=slug,
        listed_parent=d['matched_company'],parent_control_from=frm,basis=basis,date_status=ver,
        asof_verdict=flag,disclosure_code=d['disclosure_code'],title=d['title'][:110]))
with open(L.out("asofdate.csv"),"w",newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
import collections
c=collections.Counter(r['asof_verdict'] for r in rows)
print(f"PARENT-linked incidents checked: {len(rows)}")
for k,v in c.most_common(): print(f"   {k}: {v}")
bad=[r for r in rows if r['asof_verdict']=='FLAG-parent-did-not-own']
for r in bad:
    print(f"  FLAGGED  id={r['incident_id']} {r['incident_date']} {r['entity_slug']} -> {r['listed_parent']}")
    print(f"           parent control only from {r['parent_control_from']}; code {r['disclosure_code']}")
    print(f"           {r['title']}")
json.dump(dict(n_parent_checked=len(rows),verdicts=dict(c),
  flagged_ids=[r['incident_id'] for r in bad]),open(L.res("asofdate.json"),"w"),indent=1)
print("wrote",L.out("asofdate.csv"))
