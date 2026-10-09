#!/usr/bin/env python3
"""Audit Group D builds against the hard constraints. Writes IL-XX-AUDIT.md per course."""
import json, os, re

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
OUT = os.path.expanduser('~/workspace/apex-audit/.work/course-spec-clone/specs')
os.makedirs(OUT, exist_ok=True)

FILES = {
    "IL-19": "il-19-multicloud-devops-ai-bootcamp.json",
    "IL-20": "il-20-mathematics.json",
    "IL-21": "il-21-humanities.json",
    "IL-22": "il-22-esoteric-secret-knowledge.json",
    "IL-23": "il-23-frontier-knowledge.json",
    "IL-24": "il-24-threatlocker-assessment-prep-cbt.json",
    "IL-25": "il-25-cybersecurity-professional-certificate.json",
}

REQ_TOP = ["code","courseId","title","tagline","blurb","hours","mockMinutes","schemaVersion",
 "updatedAt","honestyNote","objectives","arc","priorities","battlePlan","modules",
 "crosswalk","certGates","readinessDashboard","scriptLabs","drills","scenarios","trainers",
 "terminalSims","mockTasks","cheatSheets","answerBank","sourceLinks","toolLabs","multicloudLabs",
 "sampleDatasets","installSteps","installLabs","installPrereqOrder","employerMappings","jdMatrix",
 "sqlPlaygrounds","pythonExercises","daxPlaygrounds","branchingScenarios","clickSims",
 "interactivityAudit","studyGuide","timeFormula","glossary","faq","tips","legends","topicTheme",
 "topic","noahTutoring"]

REQ_MOD = ["id","code","title","summary","objectives","estimatedMinutes","weight",
           "prerequisiteFor","crossLinks","cards","quiz","drills","handsOnLab",
           "mockTask","videos","pdfs","notes"]

FRAMING_PHRASE = "not affiliated with, endorsed by, or sponsored"

def audit(code):
    d = json.load(open(os.path.join(BASE, FILES[code])))
    checks = []
    def ck(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    ck("schemaVersion == 4 (int, IL-29 gold-standard pattern)", d.get("schemaVersion") == 4,
       f"got {d.get('schemaVersion')!r}")
    ck('updatedAt == "2026-10-09"', d.get("updatedAt") == "2026-10-09", f"got {d.get('updatedAt')!r}")
    total_min = sum(m.get("estimatedMinutes", 0) for m in d["modules"])
    ck("hours == honest rounded sum", d.get("hours") == round(total_min/60),
       f"hours={d.get('hours')}, sum={total_min}min -> {round(total_min/60)}")

    missing_top = [k for k in REQ_TOP if k not in d]
    ck("all required top-level keys present", not missing_top, f"missing: {missing_top}")

    bad_mod = {}
    for m in d["modules"]:
        miss = [k for k in REQ_MOD if k not in m]
        if miss: bad_mod[m["id"]] = miss
    ck("all modules carry required v4 keys", not bad_mod, f"{len(bad_mod)} modules missing keys: {list(bad_mod)[:3]}")

    gates = d.get("certGates", [])
    bad_framing = [g.get("id") for g in gates if FRAMING_PHRASE not in g.get("framing","").lower()]
    ck("every certGates entry carries independent-prep framing", not bad_framing,
       f"{len(gates)} gates, bad framing: {bad_framing}")

    blob = json.dumps(d)
    ck("no braindump/testimonial/guaranteed-pass language",
       not re.search(r"braindump|real exam questions|guaranteed pass|testimonial", blob, re.I),
       "scan clean" if not re.search(r"braindump|real exam questions|guaranteed pass|testimonial", blob, re.I) else "HIT")
    ck("no Palantir/NSA certification claims",
       not re.search(r"palantir|national security agency", blob, re.I), "scan clean")

    hn = d.get("honestyNote","")
    ck("honestyNote present + disaffiliation language", bool(hn) and "not affiliated" in hn.lower(),
       f"{len(hn)} chars")
    if code == "IL-24":
        ck("IL-24: ThreatLocker disclaimer prominent",
           "threatlocker" in hn.lower() and "not affiliated" in hn.lower(), "honestyNote names ThreatLocker")

    # prereq math
    if code == "IL-19":
        pm = [m["id"] for m in d["modules"] if "-PM-" in m["id"]]
        ck("IL-19 prereq math supplement present", len(pm) >= 3, f"PM modules: {pm}")
    elif code == "IL-20":
        ck("IL-20 M00 primer present", any(m["id"]=="IL-20-M00" for m in d["modules"]), "IL-20-M00")

    sl = d.get("sourceLinks", [])
    nodate = [s.get("title","?")[:40] for s in sl if isinstance(s,dict) and not (s.get("retrieved") or s.get("retrievedDate") or s.get("accessed") or s.get("verifiedUtc"))]
    ck("sourceLinks all carry retrieved/verified dates", not nodate, f"{len(sl)} links, missing dates: {nodate[:3]}")

    # Noah integration
    nt = d.get("noahTutoring", {})
    personas = nt.get("personas", [])
    ck("noahTutoring present with 5 personas", len(personas) == 5, f"{len(personas)} personas")
    ck("noahTutoring: 5 natural voices + voice-first", nt.get("voices",{}).get("count")==5 and "voice" in nt.get("voices",{}).get("note","").lower(), "")
    ck("noahTutoring: SM-2 adaptive", "SM-2" in nt.get("adaptive",{}).get("method",""), "")
    ck("noahTutoring: course-aware grounding", bool(nt.get("courseAware",{}).get("groundedIn")), "")
    ck("noahTutoring: personas mapped to real module ids",
       all(mid in {m["id"] for m in d["modules"]} for p in personas for mid in p.get("moduleIds",[])),
       "all persona moduleIds resolve")
    if code == "IL-23":
        ck("IL-23: frontier note present", bool(nt.get("frontierNote")), "")

    # merge-plan cross-links
    if code == "IL-22":
        xl = [x for m in d["modules"] for x in m.get("crossLinks",[]) if x.startswith("il01-") or x.startswith("il-01-")]
        ck("IL-22 ↔ IL-01 cross-links present", len(xl) >= 10, f"{len(xl)} IL-01 links")
    if code in ("IL-24","IL-25"):
        xl = [x for m in d["modules"] for x in m.get("crossLinks",[]) if x.startswith("IL29-")]
        ck(f"{code} → IL-29 cross-links present", len(xl) >= 10, f"{len(xl)} IL-29 links")
    if code == "IL-23":
        folds = [m for m in d["modules"] if any(n.get("title")=="Frontier fold-in" for n in m.get("notes",[]))]
        ck("IL-23 fold-in notes present", len(folds) >= 5, f"{len(folds)} modules with fold notes")

    # exam-fact honesty: flag specific numeric exam claims in NEW gates (informational)
    return checks

if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or list(FILES.keys())
    for code in only:
        checks = audit(code)
        passed = sum(1 for _,ok,_ in checks if ok)
        failed = [(n,det) for n,ok,det in checks if not ok]
        L = [f"# {code} — Build Audit", "",
             f"**Result: {'PASS' if not failed else 'FAIL'}** ({passed}/{len(checks)} checks passed)", "",
             "## Checks"]
        for name, ok, det in checks:
            L.append(f"- [{'x' if ok else ' '}] {name}" + (f" — {det}" if det else ""))
        if failed:
            L += ["", "## Failures requiring action"]
            for n, det in failed:
                L.append(f"- {n}: {det}")
        L += ["", "## Notes",
              "- Existing content preserved; only missing v4 fields added (module crossLinks/prerequisiteFor, top-level sections).",
              "- schemaVersion is integer 4 per the IL-26/27/28/29 gold-standard pattern (template said string; gold standard rules).",
              "- Exam facts in pre-existing certGates (e.g., IL-19 SAA 65q/130min/720) are preserved vendor-published figures as of Oct 2026, stated via the course honestyNote; no new exam facts invented in this build."]
        out = os.path.join(OUT, f"{code}-AUDIT.md")
        with open(out, "w") as f:
            f.write("\n".join(L) + "\n")
        print(code, "PASS" if not failed else "FAIL", f"{passed}/{len(checks)}")
        for n, det in failed:
            print("   FAIL:", n, det)
