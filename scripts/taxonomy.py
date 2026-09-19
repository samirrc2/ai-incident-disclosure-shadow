"""shared taxonomy — application (technology) families and harm families used by the
revision-stage T3a/T3b recode and the attribution-basis coding. Reviewer-requested post-hoc.

Families were induced from the 307 AIID records in the analytical sample and the 307 filing-search
evidence records, then fixed before any T3a/T3b value was computed. Seed-free (pure lexicon).
"""
import re
import os
# LEXICON_VERSION: "v1" = the lexicon fixed before any T3a/T3b value was computed.
# "v2" = a completeness pass adding unambiguous domain synonyms of the SAME families after a
# spot-check found recall misses (e.g. "fair lending" not matching discrimination-bias). No family
# was added, removed or redefined; no threshold changed. Both versions are reported so the effect
# of the fix is visible. Set REV1_LEXICON=v1 to reproduce the pre-spot-check numbers.
LEXICON_VERSION = os.environ.get("REV1_LEXICON", "v2")

# ---- application / technology families -------------------------------------------------
APP_FAMILIES = {
 "recommender-ranking":   ["recommend",r"\bfeeds?\b","ranking","ranked","algorithmic amplif","newsfeed",
                           "news feed","search result","autocomplete","trending","collaborative filter"],
 "content-moderation":    ["moderation","moderat","takedown","removal of","flagged content","demonet",
                           "content polic","enforcement of.{0,20}polic","account suspension","banned"]
                          +(["fact.?check","mislabel","labelled content","labeled content",
                             "content review","content label","wrongly (?:removed|banned|blocked)",
                             "objectionable.content"] if LEXICON_VERSION=="v2" else []),
 "generative-llm":        ["generative","chatbot","chat bot","large language",r"\bllms?\b","gpt","bard",
                           "gemini","copilot","ai assistant","hallucinat","deepfake","synthetic media",
                           "image generat","text-to-image","ai-generated"],
 "autonomous-vehicle":    ["autonomous vehicle","self-driving","driverless","robotaxi","autopilot",
                           "full self","fsd","av operation","automated driving","driver assist",
                           "lane keep","summon"],
 "vision-biometric":      ["facial recognition","face recognition","image recognition","image label",
                           "computer vision","object detection","gunshot detection","license plate",
                           "biometric","photo crop","x-ray","radiolog"],
 "speech-nlp":            ["voice assistant","speech recognition","transcri","voice recognition",
                           "translation","natural language process","sentiment analysis","spam filter"],
 "ads-targeting":         ["ad delivery","ad targeting","advertis","ad platform","ad approval","ad review"],
 "predictive-scoring":    ["risk score","credit","underwrit","pricing algorithm","predictive polic",
                           "recidivism","claims","prior authoriz","length of stay","benefit denial",
                           "coverage denial","eligibility","hiring algorithm","resume screen",
                           "proctoring","grading","fraud detection","tenant screen","valuation",
                           "zestimate","home-buying","insurance"],
 "robotics-automation":   ["delivery robot","sidewalk robot","warehouse robot","robotic arm",
                           "surgical robot","drone","automation system","kiosk","drive-thru"],
}

# ---- harm families ---------------------------------------------------------------------
HARM_FAMILIES = {
 "misinformation-content":["misinformation","disinformation","false","fake news","conspirac",
                           "propaganda","mislead","defam","inaccurate content","fabricat"]
                          +(["mislabel","hallucinat","made.up","untrue"] if LEXICON_VERSION=="v2" else []),
 "discrimination-bias":   ["discriminat","bias","racial","gender","ethnic","disparate","stereotyp",
                           "ageism","civil rights","fair housing","equal"]
                          +(["fair lending","redlin","protected class","adverse impact",
                             "women","minorit","black patients","accessib"] if LEXICON_VERSION=="v2" else []),
 "privacy-surveillance":  ["privacy","surveillance","data collection","personal data","tracking",
                           "geolocation","wiretap","recorded without","consent"],
 "physical-safety":       ["injur","killed","death","fatal","collision","crash","struck","pedestrian",
                           "safety","recall","hospitaliz","physical harm"]
                          +(["dragged","collided","ran over","rear.end","veered"] if LEXICON_VERSION=="v2" else []),
 "economic-financial":    ["financial loss","write-down","write down","lost money","overcharg","denied payment",
                           "denial of","cut off","wrongful.{0,12}denial","economic harm",r"\bfees?\b","cost of"]
                          +(["write.off","impairment","restructuring charge","reimburse",
                             "payment for treatment"] if LEXICON_VERSION=="v2" else []),
 "ip-copyright":          ["copyright","intellectual property","training data","pirated","infring",
                           "likeness","royalt"],
 "harmful-content-minors":[r"\bminors?\b","child","teen","youth","csam","self-harm","suicid","eating disorder",
                           "grooming","sexualiz"],
 "service-quality":       [r"\berrors?\b","malfunction","failed to","wrongly","incorrect","glitch","outage",
                           "degraded","blocked legitimate","false positive","misidentif","wrongful"],
 "rights-legal":          ["wrongful arrest","due process","detained","imprison","deported",
                           "legal right","denied access","censor"],
}

def _flex(pattern):
    """Let a multi-word phrase match whether the source writes it spaced or hyphenated.

    Filings and incident records use both forms of the same term: a 10-K says "autonomous
    vehicle" where the coding record says "autonomous-vehicle". The pattern names a phrase;
    the hyphen is orthography, not meaning, and a literal space silently missed one form."""
    return pattern.replace(" ", "[ -]") if " " in pattern and "\\" not in pattern else pattern

_FLEX = {}

def _hits(text, lexicon):
    t = (text or "").lower()
    out = []
    for fam, keys in lexicon.items():
        for k in keys:
            kk = _FLEX.setdefault(k, _flex(k))
            if re.search(kk, t):
                out.append(fam); break
    return out

def app_families(text):  return _hits(text, APP_FAMILIES)
def harm_families(text): return _hits(text, HARM_FAMILIES)

# ---- negation stripping for filing-side evidence ---------------------------------------
# The evidence prose mixes what the filing DOES carry with what it does not. Only the
# affirmative clauses describe the generic language that makes an incident T3, so negated
# clauses are removed before the filing side is scored.
NEG = re.compile(r"(?:^|(?<=[.;]))[^.;]*?\b(?:no |not |never |none of|absent|without any|"
                 r"nothing in|no filing|no in-window|no periodic|no 10-|no 8-|no reference|"
                 r"is not |was not |does not |did not |do not |cannot )[^.;]*(?:[.;]|$)",
                 re.IGNORECASE)

def affirmative(evidence):
    """Return only the clauses of the evidence prose that assert what the filing contains."""
    return NEG.sub(" ", evidence or "")
