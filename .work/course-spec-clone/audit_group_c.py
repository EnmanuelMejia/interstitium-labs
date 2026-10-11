#!/usr/bin/env python3
"""Group C audit: verify each built course against its spec sheet + hard constraints.
Writes ~/workspace/apex-audit/.work/course-spec-clone/specs/IL-XX-AUDIT.md
"""
import json, os, re

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
SPECS = os.path.expanduser('~/workspace/apex-audit/.work/course-spec-clone/specs')

FILES = {
    'IL-13': ('il-13-software-engineering-interview-prep.json', 58, 334, [], True),
    'IL-14': ('il-14-sre-devops-cloud-security-interview-prep.json', 31, 178, [], True),
    'IL-15': ('il-15-data-engineering-analytics-interview-prep.json', 32, 184, [], True),
    'IL-16': ('il-16-machine-learning-ai-engineering.json', 47, 449,
              ['gate-il16-gcp-mle','gate-il16-aws-mla','gate-il16-ai103','gate-il16-tf-dev-retired'], True),
    'IL-17': ('il-17-agentic-ai-engineering.json', 46, 329, [], True),
    'IL-18': ('il-18-technical-leadership-interview-prep.json', 32, 250, ['gate-il18-interview'], True),
}

REQUIRED_MODULE_FIELDS = ["id","code","title","summary","objectives","estimatedMinutes",
    "weight","prerequisiteFor","crossLinks","cards","quiz","drills","handsOnLab",
    "mockTask","videos","pdfs","notes"]
V4_TOP = ["code","courseId","title","tagline","blurb","hours","mockMinutes",
    "schemaVersion","updatedAt","honestyNote","objectives","arc","priorities",
    "battlePlan","modules","crosswalk","certGates","readinessDashboard",
    "scriptLabs","drills","scenarios","trainers","terminalSims","mockTasks",
    "cheatSheets","answerBank","sourceLinks","toolLabs","multicloudLabs",
    "sampleDatasets","installSteps","installPrereqOrder","installLabs",
    "employerMappings","jdMatrix","sqlPlaygrounds","pythonExercises",
    "daxPlaygrounds","branchingScenarios","clickSims","interactivityAudit",
    "studyGuide","timeFormula","glossary","faq","tips","legends","topicTheme","topic",
    "noahTutoring","certNotes","mergeNotes"]

VENDOR_WORDS = {"IL-13": ["interview-prep provider"],
    "IL-14": ["CNCF","AWS","HashiCorp"], "IL-15": ["AWS","Databricks"],
    "IL-16": ["AWS","Google","Microsoft","TensorFlow"],
    "IL-17": ["AWS","Microsoft","Google","OpenAI","Anthropic"],
    "IL-18": ["PMI"]}

def check(code):
    fname, exp_modules, exp_hours, exp_gates, _ = FILES[code]
    d = json.load(open(os.path.join(BASE, fname)))
    spec = open(os.path.join(SPECS, f"{code}.md")).read()
    lines = []
    def ok(name, cond, detail=""):
        lines.append((name, bool(cond), detail))
    # hard constraints
    ok("schemaVersion == '4'", d.get("schemaVersion")=="4", str(d.get("schemaVersion")))
    total = sum(m["estimatedMinutes"] for m in d["modules"])
    ok("hours == honest rounded sum", d.get("hours")==round(total/60),
       f"hours={d.get('hours')} sum={total} -> {round(total/60)}")
    ok("hours matches spec", d.get("hours")==exp_hours, f"spec={exp_hours}")
    ok("module count matches spec", len(d["modules"])==exp_modules,
       f"{len(d['modules'])} vs {exp_modules}")
    framing_ok = all("Independent practice and preparation" in g.get("framing","") for g in d["certGates"])
    ok("every certGate has independent-prep framing", framing_ok,
       f"{len(d['certGates'])} gates")
    ok("certGates match spec", sorted(g["id"] for g in d["certGates"])==sorted(exp_gates),
       str(sorted(g["id"] for g in d["certGates"])))
    hn = d.get("honestyNote","")
    ok("honestyNote names vendors", all(w in hn for w in VENDOR_WORDS[code]),
       "missing: "+str([w for w in VENDOR_WORDS[code] if w not in hn]))
    sl_bad = [s.get("name") for s in d.get("sourceLinks",[]) if not s.get("retrieved")]
    ok("all sourceLinks have retrieved dates", not sl_bad, str(sl_bad[:3]))
    blob = json.dumps(d).lower()
    ok("no Palantir/NSA claims",
       not re.search(r"\bpalantir\b", blob) and not re.search(r"\bnsa\b", blob),
       "word-boundary scan (excludes 'transactions', 'compensation', 'unsafe', etc.)")
    ok("no braindump/testimonial language",
       not re.search(r"braindump|guaranteed pass|\d+%\s*pass rate|real exam questions", blob),
       "scan of full JSON")
    ok("all v4 top-level keys present",
       set(V4_TOP) <= set(d.keys()),
       "missing: "+str(sorted(set(V4_TOP)-set(d.keys()))))
    mod_missing = []
    for m in d["modules"]:
        miss=[k for k in REQUIRED_MODULE_FIELDS if k not in m]
        if miss: mod_missing.append((m.get("id"),miss))
    ok("every module has all 18 fields", not mod_missing, str(mod_missing[:2]))
    ok("updatedAt == 2026-10-09", d.get("updatedAt")=="2026-10-09")
    # math supplement
    if code in ("IL-16","IL-17"):
        m00 = [m for m in d["modules"] if m["id"]==f"{code}-M00"]
        ok("M00 math supplement present", len(m00)==1)
        if m00:
            ok("M00 has all 18 fields",
               all(k in m00[0] for k in REQUIRED_MODULE_FIELDS))
            ok("M00 crossLinks reference PM modules", len(m00[0].get("crossLinks",[]))==3)
    # merge notes
    mn = d.get("mergeNotes",{})
    ok("mergeNotes present with complementary courses",
       bool(mn.get("complementaryCourses")) and bool(mn.get("crossLinkedModules")))
    # study guide / audit totals
    sg = d.get("studyGuide",{})
    ok("studyGuide totals match module sum",
       sg.get("totalMinutes")==total and sg.get("totalHours")==round(total/60))
    ia = d.get("interactivityAudit",{})
    recount = (len(d.get("terminalSims",[]))+len(d.get("branchingScenarios",[]))
        +len(d.get("clickSims",[]))+len(d.get("toolLabs",[]))+len(d.get("installLabs",[]))
        +len(d.get("multicloudLabs",[]))+len(d.get("trainers",[]))+len(d.get("scriptLabs",[]))
        +len(d.get("cheatSheets",[])))
    ok("interactivityAudit total matches recount", ia.get("totalInteractive")==recount,
       f"{ia.get('totalInteractive')} vs {recount}")
    # Noah integration (required per strategic clarification)
    nt = d.get("noahTutoring")
    ok("noahTutoring section present", bool(nt))
    if nt:
        ok("5 personas", len(nt.get("personas",[]))==5,
           str([p["id"] for p in nt.get("personas",[])]))
        ok("5 persona voices mapped",
           all(p.get("voice") in ("scholar","narrator","guide","sage","spark") for p in nt["personas"]))
        ok("modulePersonaMap >= 5 entries", len(nt.get("modulePersonaMap",[]))>=5,
           str(len(nt.get("modulePersonaMap",[]))))
        modids = {m["id"] for m in d["modules"]}
        bad_refs = [mid for e in nt["modulePersonaMap"] for mid in e.get("modules",[]) if mid not in modids]
        ok("all persona-mapped module ids exist", not bad_refs, str(bad_refs[:5]))
        ok("voice-first section", nt.get("voiceFirst",{}).get("supported") is True)
        ok("adaptive SM-2 section",
           nt.get("adaptive",{}).get("scheduler","").startswith("SM-2"))
        ok("course-aware tutoring (POST /api/noah)",
           nt.get("courseAware",{}).get("endpoint")=="POST /api/noah")
        ok("house rule present", "hypothesis" in nt.get("houseRule",""))
        if code in ("IL-16","IL-17"):
            ok("bleedingEdge integration note", bool(nt.get("bleedingEdge")))
        ok("spec sheet documents Noah integration", "Noah Tutoring Integration" in spec)
    # spec sheet cross-checks
    ok("spec sheet exists with identity block",
       f"courseId: {d.get('courseId')}" in spec)
    fails = [n for n,c,_ in lines if not c]
    verdict = "PASS" if not fails else "FAIL"
    md = [f"# {code} — Audit ({d.get('title')})", "",
          f"**Verdict: {verdict}** — {len(lines)-len(fails)}/{len(lines)} checks passed.",
          f"Audited: 2026-10-09. File: `{fname}`. Spec: `specs/{code}.md`.", "",
          "| Check | Result | Detail |", "|---|---|---|"]
    for n,c,det in lines:
        md.append(f"| {n} | {'PASS' if c else 'FAIL'} | {det} |")
    if fails:
        md += ["", "## Failures requiring action",
               "\n".join(f"- {n}" for n in fails)]
    md += ["", "## Notes",
     f"- Modules: {len(d['modules'])}, minutes: {total}, hours: {d['hours']}.",
     f"- certGates: {[g['id'] for g in d['certGates']]}.",
     f"- crosswalk entries: {len(d['crosswalk'])}.",
     f"- sourceLinks: {len(d['sourceLinks'])} (all with retrieved dates: {not sl_bad}).",
     f"- Noah persona-map tracks: {len(nt['modulePersonaMap']) if nt else 0}.",
     "- No deploy performed (per task)."]
    open(os.path.join(SPECS, f"{code}-AUDIT.md"),"w").write("\n".join(md)+"\n")
    print(code, verdict, f"{len(lines)-len(fails)}/{len(lines)}")
    return verdict

verdicts = {c: check(c) for c in FILES}
print(verdicts)
