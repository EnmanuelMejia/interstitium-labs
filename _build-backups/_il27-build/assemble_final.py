"""ASSEMBLER for IL-27. Merges worker deliverables into the final course JSON.

Reads:  modules.json, labs.json, certs.json
Writes: ../il-27-it-infrastructure-specialist-threatlocker-mastery.json
"""
import json
import os

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/_il27-build")
OUT = os.path.expanduser(
    "~/workspace/apex-audit/docs/university/data/courses/"
    "il-27-it-infrastructure-specialist-threatlocker-mastery.json"
)

mo = json.load(open(os.path.join(BASE, "modules.json")))
la = json.load(open(os.path.join(BASE, "labs.json")))
ce = json.load(open(os.path.join(BASE, "certs.json")))

meta = mo["meta"]
modules48 = mo["modules"]
assert len(modules48) == 48, "expected 48 base modules, got %d" % len(modules48)
ft6 = ce["fastTrackModules"]
assert len(ft6) == 6, "expected 6 fast-track modules, got %d" % len(ft6)

# ---- merge modules: 48 base + 6 flagged fast-track ----
all_modules = list(modules48)
for i, ftm in enumerate(ft6, start=1):
    flagged = dict(ftm)
    flagged["fastTrack"] = True
    flagged["fastTrackDay"] = i
    all_modules.append(flagged)
assert len(all_modules) == 54

all_ids = set(x["id"] for x in all_modules)

# ---- assert every moduleId reference resolves ----
missing = []
def scan(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("moduleId",) and isinstance(v, str):
                if v not in all_ids:
                    missing.append("%s -> %s" % (path, v))
            scan(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            scan(v, path + "[%d]" % i)
    elif isinstance(o, str):
        for part in ("IL27-M", "IL27-MX", "IL27-FT"):
            idx = o.find(part)
            while idx != -1:
                cand = o[idx:idx + 8]
                if len(cand) == 8 and cand[-2:].isdigit():
                    if cand not in all_ids:
                        missing.append("%s : %s" % (path, cand))
                idx = o.find(part, idx + 1)

scan(ce["crosswalk"], "crosswalk")
scan(ce["certGates"], "certGates")
scan(ce["jdMatrix"], "jdMatrix")
scan(ce["fastTrack"], "fastTrack")
scan(la, "labs")
assert not missing, "dangling module refs: %s" % missing[:10]

# ---- interactivity audit: >=2 element types (quiz / drills / lab) ----
audit_results = []
fails = []
for x in all_modules:
    quiz = bool(x.get("quiz"))
    drills = bool(x.get("drills"))
    lab = bool(x.get("handsOnLab")) or bool(x.get("mockTask"))
    n = (1 if quiz else 0) + (1 if drills else 0) + (1 if lab else 0)
    ok = n >= 2
    audit_results.append({
        "moduleId": x["id"],
        "fastTrack": bool(x.get("fastTrack")),
        "quiz": quiz,
        "drills": drills,
        "lab": lab,
        "elementTypes": n,
        "pass": ok,
    })
    if not ok:
        fails.append(x["id"])

# ---- worth-paying-for 5-point audit ----
wp_points = ["clearObjective", "taughtFromZero", "interactiveReady", "appliedLab", "honestTimeEstimate"]
wp_results = []
wp_fails = []
for x in all_modules:
    obj = bool(x.get("objectives"))
    notes = bool(x.get("notes"))
    inter = bool(x.get("quiz")) or bool(x.get("cards")) or bool(x.get("drills"))
    lab = bool(x.get("handsOnLab")) or bool(x.get("mockTask"))
    est = bool(x.get("estimatedMinutes")) and x.get("estimatedMinutes") > 0
    pts = {
        "clearObjective": obj,
        "taughtFromZero": notes,
        "interactiveReady": inter,
        "appliedLab": lab,
        "honestTimeEstimate": est,
    }
    score = sum(1 for v in pts.values() if v)
    entry = {"moduleId": x["id"], "fastTrack": bool(x.get("fastTrack")),
             "points": pts, "score": score, "pass": score == 5}
    wp_results.append(entry)
    if score != 5:
        wp_fails.append(x["id"])

interactivity_audit = {
    "generatedAt": "2026-10-07",
    "rule": "Every module must have >=2 interactive element types (quiz, drills, lab=handsOnLab|mockTask).",
    "worthPayingFor": {
        "points": wp_points,
        "moduleCount": len(all_modules),
        "passCount": len(all_modules) - len(wp_fails),
        "failCount": len(wp_fails),
        "failedModules": wp_fails,
        "results": wp_results,
    },
    "moduleCount": len(all_modules),
    "passCount": len(all_modules) - len(fails),
    "failCount": len(fails),
    "failedModules": fails,
    "results": audit_results,
}

# ---- assemble top-level in schema order ----
course = {}
course["code"] = meta["code"]
course["courseId"] = meta["courseId"]
course["title"] = meta["title"]
course["tagline"] = meta["tagline"]
course["blurb"] = meta["blurb"]
course["hours"] = meta["hours"]
course["mockMinutes"] = meta["mockMinutes"]
course["schemaVersion"] = 4
course["updatedAt"] = "2026-10-07"
course["honestyNote"] = meta["honestyNote"]
course["objectives"] = meta["objectives"]
course["arc"] = meta["arc"]
course["priorities"] = meta["priorities"]
course["battlePlan"] = meta["battlePlan"]
course["modules"] = all_modules
course["crosswalk"] = ce["crosswalk"]
course["certGates"] = ce["certGates"]
course["readinessDashboard"] = ce["readinessDashboard"]
course["scriptLabs"] = la["scriptLabs"]
course["drills"] = mo["drills"]
course["scenarios"] = la["scenarios"]
course["trainers"] = la["trainers"]
course["terminalSims"] = la["terminalSims"]
course["mockTasks"] = la["mockTasks"]
course["cheatSheets"] = mo["cheatSheets"]
course["answerBank"] = mo["answerBank"]
course["sourceLinks"] = mo["sourceLinks"]
course["toolLabs"] = la["toolLabs"]
course["installLabs"] = la["installLabs"]
course["fastTrack"] = ce["fastTrack"]
course["jdMatrix"] = ce["jdMatrix"]
course["branchingScenarios"] = la["branchingScenarios"]
course["clickSims"] = la["clickSims"]
course["mathLab"] = la["mathLab"]
course["scriptingLab"] = la["scriptingLab"]
course["animations"] = la["animations"]
course["interactivityAudit"] = interactivity_audit
course["studyGuide"] = ce["studyGuide"]
course["dossier"] = ce["dossier"]
course["dossierUrl"] = "il-27-dossier.html"

with open(OUT, "w") as f:
    json.dump(course, f, indent=1, ensure_ascii=False)
    f.write("\n")

# ---- validate ----
back = json.load(open(OUT))
assert list(back.keys()) == list(course.keys()), "key order changed on re-read"
assert len(back["modules"]) == 54

# ---- guardrail scan: no affiliation/certification claims, no banned names ----
blob = json.dumps(back)
flags = []
for phrase in ["Palantir", "NSA", "endorsed by ThreatLocker", "affiliated with ThreatLocker",
               "partner of ThreatLocker", "ThreatLocker-certified", "official ThreatLocker"]:
    if phrase in blob:
        flags.append(phrase)
# allow honest disclaimers containing "not affiliated" etc.
allowed = []
for phrase in list(flags):
    idx = blob.find(phrase)
    ctx = blob[max(0, idx - 60):idx + len(phrase) + 40].lower()
    if "not " in ctx or "never " in ctx or "independent" in ctx or "no " in ctx:
        allowed.append(phrase)
flags = [p for p in flags if p not in allowed]

# ---- stats ----
n_quiz = sum(len(x.get("quiz") or []) for x in all_modules)
n_cards = sum(len(x.get("cards") or []) for x in all_modules)
n_drills = len(back["drills"]) + sum(len(x.get("drills") or []) for x in all_modules)
n_gate_q = sum(len(g.get("questions") or []) for g in back["certGates"])
total_min = sum(x.get("estimatedMinutes") or 0 for x in all_modules)

print("WROTE:", OUT)
print("modules:", len(back["modules"]), "(48 base + 6 fast-track)")
print("quiz questions:", n_quiz, "| flashcards:", n_cards)
print("drills (top + module):", n_drills)
print("certGate questions:", n_gate_q)
print("total estimated minutes:", total_min)
print("interactivity audit: pass %d / fail %d" % (interactivity_audit["passCount"], interactivity_audit["failCount"]))
print("  failed:", interactivity_audit["failedModules"])
print("worth-paying-for: pass %d / fail %d" % (interactivity_audit["worthPayingFor"]["passCount"], interactivity_audit["worthPayingFor"]["failCount"]))
print("  failed:", interactivity_audit["worthPayingFor"]["failedModules"])
print("guardrail flags (unresolved):", flags)
print("top-level keys:", len(list(back.keys())))
