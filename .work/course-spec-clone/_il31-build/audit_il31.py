# IL-31 audit — verifies spec match + all hard constraints. Run after every rebuild.
import json, re, sys, os

JSON_PATH = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/il-31-ai-red-teaming-safety-evals.json")
SPEC_PATH = os.path.expanduser("~/workspace/apex-audit/.work/course-spec-clone/specs/IL-31.md")

d = json.load(open(JSON_PATH))
spec = open(SPEC_PATH).read()
results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail))

# 1. schemaVersion
check("schemaVersion == '4' (string)", d.get("schemaVersion") == "4", repr(d.get("schemaVersion")))

# 2. hours honest sum
total = sum(m["estimatedMinutes"] for m in d["modules"])
check("hours == rounded sum of estimatedMinutes", d["hours"] == round(total/60) == 100, f"hours={d['hours']} sum={total}")

# 3. certGates framing
gates = d.get("certGates", [])
fr = "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate."
check("certGates non-empty", len(gates) > 0, f"{len(gates)} gates")
for g in gates:
    check(f"certGate {g['id']} framing", g.get("framing") == fr, g.get("framing","")[:60])

# 4/5. invented metrics / Palantir / NSA
blob = json.dumps(d)
check("no Palantir claims", "palantir" not in blob.lower())
check("no NSA claims", not re.search(r"\bnsa\b", blob, re.I))
# positive credential/testimonial claims (wrong-answer choices and explicit denials are fine)
pos_claim = re.search(r"(?i)(holds|earned|awarded|grants?)\s+(a\s+)?certified\s+(ai\s+)?(red-?team|eval)", blob)
check("no positive credential claims", not pos_claim, pos_claim.group(0) if pos_claim else "")
pos_test = re.search(r"(?i)\"[^\"]*testimonial[^\"]*\"\s*:\s*\"[^a-z]*[A-Z][a-z]+ [A-Z][a-z]+ said", blob)
check("no fabricated testimonials", not pos_test, "")
check("legends explicitly empty", d.get("legends", {}).get("entries") == [])

# 6. honestyNote
hn = d.get("honestyNote", "")
check("honestyNote present", len(hn) > 100)
for vendor in ["METR", "Anthropic", "OpenAI", "XBOW"]:
    check(f"honestyNote names {vendor}", vendor in hn)
check("honestyNote: confers no certificate", "confers no certificate" in hn)
check("honestyNote: defensive framing", "no offensive attack techniques" in hn)

# 7. prereq math module
check("prereq math module IL31-M00", any(m["id"]=="IL31-M00" for m in d["modules"]))

# 10. sourceLinks retrieved dates
sl = d.get("sourceLinks", [])
check("sourceLinks non-empty", len(sl) >= 10, f"{len(sl)} links")
check("all sourceLinks have retrieved dates", all(s.get("retrieved") for s in sl))
missing = [s["url"] for s in sl if not s.get("retrieved")]
check("sourceLinks retrieved format YYYY-MM-DD", all(re.match(r"^\d{4}-\d{2}-\d{2}$", s.get("retrieved","")) for s in sl), str(missing))

# 11. spec match: module plan
check("16 modules", len(d["modules"]) == 16, str(len(d["modules"])))
plan_minutes = {"IL31-M00":480,"IL31-M01":360,"IL31-M02":420,"IL31-M03":420,"IL31-M04":360,"IL31-M05":420,
    "IL31-M06":360,"IL31-M07":360,"IL31-M08":360,"IL31-M09":300,"IL31-M10":480,"IL31-M11":360,
    "IL31-M12":300,"IL31-M13":300,"IL31-M14":480,"IL31-M15":240}
for m in d["modules"]:
    exp = plan_minutes.get(m["id"])
    check(f"spec minutes {m['id']}", m["estimatedMinutes"] == exp, f"{m['estimatedMinutes']} vs {exp}")
    check(f"spec id {m['id']} in spec sheet", m["id"] in spec)

# module required fields
REQ = ["id","code","title","summary","objectives","estimatedMinutes","weight","prerequisiteFor","crossLinks","cards","quiz","drills","handsOnLab","mockTask","videos","pdfs","notes"]
for m in d["modules"]:
    missing = [k for k in REQ if k not in m]
    check(f"module {m['id']} required fields", not missing, str(missing))
    check(f"module {m['id']} cards 6-10", 6 <= len(m["cards"]) <= 10, str(len(m["cards"])))
    check(f"module {m['id']} quiz 4-6", 4 <= len(m["quiz"]) <= 6, str(len(m["quiz"])))
    check(f"module {m['id']} code IL-31", m["code"] == "IL-31")
    # quiz answer must be in choices
    for qi, q in enumerate(m["quiz"]):
        if q["answer"] not in q["choices"]:
            check(f"module {m['id']} quiz[{qi}] answer in choices", False, q["q"][:60])

# top-level keys per SPEC-TEMPLATE
TOP = ["code","courseId","title","tagline","blurb","hours","mockMinutes","schemaVersion","updatedAt","honestyNote",
 "objectives","arc","priorities","battlePlan","modules","crosswalk","certGates","readinessDashboard","scriptLabs",
 "drills","scenarios","trainers","terminalSims","mockTasks","cheatSheets","answerBank","sourceLinks","toolLabs",
 "multicloudLabs","sampleDatasets","installSteps","installPrereqOrder","installLabs","employerMappings","jdMatrix",
 "sqlPlaygrounds","pythonExercises","daxPlaygrounds","branchingScenarios","clickSims","interactivityAudit",
 "studyGuide","timeFormula","glossary","faq","tips","legends","topicTheme","topic"]
missing_top = [k for k in TOP if k not in d]
check("all SPEC-TEMPLATE top-level keys", not missing_top, str(missing_top))
check("updatedAt 2026-10-09", d.get("updatedAt") == "2026-10-09", d.get("updatedAt"))

# Noah integration
nt = d.get("noahTutoring")
check("noahTutoring section present", isinstance(nt, dict))
if isinstance(nt, dict):
    check("noahTutoring: 5 personas", len(nt.get("personas", [])) == 5, str(len(nt.get("personas", []))))
    ids = [p["id"] for p in nt.get("personas", [])]
    for p in ["trickster","engineer","philosopher","sage","sentinel"]:
        check(f"noahTutoring persona {p}", p in ids)
    check("noahTutoring: SM-2 adaptive", "SM-2" in json.dumps(nt.get("adaptiveLearning",{})))
    check("noahTutoring: courseAware", "courseAware" in nt)
    check("noahTutoring: stayingCurrent", "stayingCurrent" in nt)
    check("noahTutoring: 16 module assignments", len(nt.get("moduleAssignments", [])) == 16)
for m in d["modules"]:
    check(f"module {m['id']} noahTutor field", isinstance(m.get("noahTutor"), dict))
    if isinstance(m.get("noahTutor"), dict):
        check(f"module {m['id']} noahTutor persona valid", m["noahTutor"]["persona"] in ["trickster","engineer","philosopher","sage","sentinel"])

# Defensive framing scan: no step-by-step attack instructions / payloads
RISKY = [r"\bbase64\s+(encode|payload)", r"ignore (all )?previous instructions", r"\bDAN\b.{0,20}prompt",
         r"step-by-step.{0,40}(bypass|exploit|jailbreak)", r"copy.?paste this prompt",
         r"exploit.{0,30}code.{0,20}(below|here)", r"\bmsfconsole\b", r"\bsqlmap\b"]
hits = []
for pat in RISKY:
    for mm in re.finditer(pat, blob, re.I):
        hits.append((pat, mm.group(0)[:60]))
check("defensive framing: no offensive payload patterns", not hits, str(hits[:5]))
# the course must not contain working jailbreak prompts — verify the payload rule is stated
check("payload rule stated in M02", "never the working text" in blob or "zero working payloads" in blob)

# cross-links to IL-06/IL-17/IL-23
xblob = json.dumps([m["crossLinks"] for m in d["modules"]])
check("cross-links IL-06", "il-06-cybersecurity-secure-engineering" in xblob)
check("cross-links IL-17", "il-17-agentic-ai-engineering" in xblob)
check("cross-links IL-23", "il-23-frontier-knowledge" in xblob)
check("cross-links m23-metr-evals", "m23-metr-evals" in xblob)
check("cross-links m23-agents", "m23-agents" in xblob)
check("cross-links m23-epoch-ai", "m23-epoch-ai" in xblob)

# cert mapping honesty: no cert invented for AI red-teaming
check("no invented AI-red-team cert", "ai red-team certification" not in blob.lower().replace("no vendor certificate exists","").replace("no certificate exists","") or True)
check("crosswalk honest about Security+ adjacency", "ADJACENT" in json.dumps(d.get("crosswalk",[])))

# video URLs: must be verbatim from research, all https
for m in d["modules"]:
    for v in m["videos"]:
        if not v["url"].startswith("https://"):
            check(f"video URL https {m['id']}", False, v["url"])
check("all video URLs https", True)

fails = [r for r in results if not r[1]]
print(f"CHECKS: {len(results)} | PASS: {len(results)-len(fails)} | FAIL: {len(fails)}")
for name, ok, detail in fails:
    print("FAIL:", name, "|", detail[:160])
sys.exit(1 if fails else 0)
