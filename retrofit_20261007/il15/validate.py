"""Final validation of the IL-15 retrofit."""
import json
import os
import re
import stat

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university")
COURSE = BASE + "/data/courses/il-15-data-engineering-analytics-interview-prep.json"
SHARDH = BASE + "/data/catalog/shard-h.json"
IL19 = BASE + "/data/courses/il-19-multicloud-devops-ai-bootcamp.json"
IL23 = BASE + "/data/courses/il-23-frontier-knowledge.json"

BANNED = ["aleks", "brilliant", "khan academy", "coursera", "udemy", "edx", "palantir"]
errors = []


def err(msg):
    errors.append(msg)


with open(COURSE) as f:
    course = json.load(f)
with open(SHARDH) as f:
    shard = json.load(f)

mods = course["modules"]
assert len(mods) == 30, "expected 30 modules, got %d" % len(mods)

gloss_re = re.compile(r"^- \*\*.+?\*\* — .+", re.M)
step_re = re.compile(r"^(\d+)\. .+", re.M)

for m in mods:
    mid = m["id"]
    # summary instructor voice
    s = m.get("summary", "")
    if "Welcome to" not in s or "I'm your instructor" not in s:
        err("%s: summary missing instructor voice" % mid)
    # notes: 4 with exact titles
    notes = m.get("notes", [])
    titles = [n.get("title") for n in notes]
    if titles != ["Concepts", "Hands-on procedure", "Project brief", "Honesty note"]:
        err("%s: note titles wrong: %s" % (mid, titles))
        continue
    bodies = {n["title"]: n.get("body", "") for n in notes}
    gloss = gloss_re.findall(bodies["Concepts"])
    if len(gloss) < 4:
        err("%s: Concepts has only %d glossary bullets" % (mid, len(gloss)))
    steps = step_re.findall(bodies["Hands-on procedure"])
    if len(steps) < 3:
        err("%s: procedure has only %d numbered steps" % (mid, len(steps)))
    if len(bodies["Project brief"].strip()) < 100:
        err("%s: Project brief too short" % mid)
    if len(bodies["Honesty note"].strip()) < 50:
        err("%s: Honesty note too short" % mid)
    # cards
    if len(m.get("cards", [])) != 6:
        err("%s: cards=%d, want 6" % (mid, len(m.get("cards", []))))
    for c in m.get("cards", []):
        if not c.get("front", "").strip() or not c.get("back", "").strip():
            err("%s: empty card front/back" % mid)
    # quiz
    quiz = m.get("quiz", [])
    if len(quiz) != 10:
        err("%s: quiz=%d, want 10" % (mid, len(quiz)))
    for q in quiz:
        if len(q.get("choices", [])) != 4:
            err("%s: quiz item not 4 choices: %s" % (mid, q.get("q", "")[:50]))
        if not (0 <= q.get("answer", -1) <= 3):
            err("%s: answer not 0-based: %s" % (mid, q.get("q", "")[:50]))
        if not q.get("explain", "").strip():
            err("%s: empty explain: %s" % (mid, q.get("q", "")[:50]))
    # objectives preserved
    if len(m.get("objectives", [])) < 4:
        err("%s: objectives thinned" % mid)

# banned terms across whole course file
blob = json.dumps(course)
low = blob.lower()
for b in BANNED:
    if b in low:
        err("banned term in course file: %r" % b)

# course-level keys
for k in ["arc", "priorities", "battlePlan", "mockTasks", "cheatSheets", "answerBank",
          "mockMinutes", "sourceLinks", "honestyNote", "terminalSims", "trainers",
          "scriptLabs", "drills", "scenarios"]:
    if k not in course:
        err("missing course key: %s" % k)
if len(course.get("terminalSims", [])) != 2:
    err("terminalSims != 2")
for sim in course.get("terminalSims", []):
    for c in sim.get("commands", []):
        if "cmd" not in c or "out" not in c:
            err("terminalSim cmd/out missing in %s" % sim.get("id"))
if course.get("trainers") != []:
    err("trainers should remain [] (only cidr kind renders interactively)")
for s in course.get("sourceLinks", []):
    if not s.get("retrieved"):
        err("sourceLink missing retrieved: %s" % s.get("name"))

# shard-h
for p in shard["paths"]:
    if not (isinstance(p.get("topics"), list) and len(p["topics"]) >= 5 and all(isinstance(t, str) for t in p["topics"])):
        err("path %s topics bad" % p["id"])
    if not (isinstance(p.get("sources"), list) and len(p["sources"]) >= 1 and all(set(x) == {"name", "url", "note"} for x in p["sources"])):
        err("path %s sources bad" % p["id"])
    ip = p.get("il_provides", "")
    if not (isinstance(ip, str) and "I'm your instructor" in ip):
        err("path %s il_provides bad" % p["id"])
low2 = json.dumps(shard).lower()
for b in BANNED:
    if b in low2:
        err("banned term in shard-h: %r" % b)

# untouched files
for path, name in [(IL19, "il-19"), (IL23, "il-23")]:
    st = os.stat(path)
    print("%s mtime: %s size: %d" % (name, st.st_mtime, st.st_size))

print("modules validated: %d" % len(mods))
print("total quiz items: %d" % sum(len(m["quiz"]) for m in mods))
print("total cards: %d" % sum(len(m["cards"]) for m in mods))
if errors:
    print("ERRORS (%d):" % len(errors))
    for e in errors:
        print(" -", e)
    raise SystemExit(1)
print("ALL CHECKS PASSED")
