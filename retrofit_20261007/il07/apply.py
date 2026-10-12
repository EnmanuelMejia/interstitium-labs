#!/usr/bin/env python3
"""Apply the IL-07 retrofit. Imports data chunks, mutates, validates, writes."""
import json, os, re, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))

def load_chunk(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

retro = load_chunk("retrofit")
n13 = load_chunk("notes_1_3")
n46 = load_chunk("notes_4_6")
n79 = load_chunk("notes_7_9")

NOTES = {}
for m in (n13, n46, n79):
    NOTES.update(m.NOTES)
SUMMARIES = retro.SUMMARIES
PATH = retro.PATH

with open(PATH, encoding="utf-8") as f:
    course = json.load(f)

modules = course["modules"]
assert len(modules) == 9, f"expected 9 modules, got {len(modules)}"
assert set(NOTES) == {m["id"] for m in modules}, "notes/module id mismatch"

CODE_TASK_FIXTURES = {
 "il07-m13": {
  "id": "il07-m13", "type": "choice",
  "q": "MongoDB-style: which $group stage correctly computes revenue by category (revenue=sum of amount, n=count)?",
  "choices": [
   "stage = {'$project': {'_id': '$category', 'revenue': {'$sum': '$amount'}}}",
   "stage = {'$group': {'_id': '$category', 'revenue': {'$sum': '$amount'}, 'n': {'$sum': 1}}}",
   "stage = {'$group': {'revenue': {'$sum': '$amount'}, 'n': {'$sum': 1}}}",
   "stage = {'$match': {'_id': '$category', 'revenue': {'$sum': '$amount'}}}",
  ],
  "answer": 1,
  "explain": "$group with _id as the key; accumulators $sum for revenue and count. Correct stage: stage = {'$group': {'_id': '$category', 'revenue': {'$sum': '$amount'}, 'n': {'$sum': 1}}}. $project can't aggregate; _id is required as the group key; $match filters, it doesn't group.",
 },
 "il07-m14": {
  "id": "il07-m14", "type": "choice",
  "q": "Python: which implementation correctly computes cosine similarity between two dict vectors?",
  "choices": [
   "def cosine(a, b):\n    return sum(a[k]*b[k] for k in a) / (sum(a.values()) * sum(b.values()))",
   "def cosine(a, b):\n    import math\n    dot = sum(a[k]*b.get(k, 0) for k in a)\n    na = math.sqrt(sum(x*x for x in a.values()))\n    nb = math.sqrt(sum(x*x for x in b.values()))\n    return dot/(na*nb) if na and nb else 0.0",
   "def cosine(a, b):\n    return len(set(a) & set(b)) / len(set(a) | set(b))",
   "def cosine(a, b):\n    import math\n    return math.sqrt(sum((a.get(k,0)-b.get(k,0))**2 for k in set(a)|set(b)))",
  ],
  "answer": 1,
  "explain": "Dot over magnitudes, guarded against zero vectors. Correct: import math; def cosine(a, b): dot = sum(a[k]*b.get(k, 0) for k in a); na = math.sqrt(sum(x*x for x in a.values())); nb = math.sqrt(sum(x*x for x in b.values())); return dot/(na*nb) if na and nb else 0.0. The distractors are: sum-of-values normalization (wrong), Jaccard (wrong metric), Euclidean distance (wrong metric).",
 },
}

for i, mod in enumerate(modules):
    mid = mod["id"]
    # 1. weight
    mod["weight"] = i + 1
    # 2. instructor-voice summary (content preserved, voice retrofitted)
    mod["summary"] = SUMMARIES[mid]
    # 3. four titled note sections
    new_notes = []
    for title, body in NOTES[mid]:
        new_notes.append({"title": title, "body": body})
    mod["notes"] = new_notes
    # 4. drop stray non-schema keys in quiz items (e.g. "back":"x")
    for q in mod["quiz"]:
        for junk in [k for k in q if k not in ("q", "choices", "answer", "explain")]:
            del q[junk]

# 5. convert 'code' mockTasks to the template 'choice' shape, content preserved
fixed = 0
for idx, t in enumerate(course["mockTasks"]):
    if t.get("type") == "code":
        assert t["id"] in CODE_TASK_FIXTURES, f"no fixture for {t['id']}"
        course["mockTasks"][idx] = CODE_TASK_FIXTURES[t["id"]]
        fixed += 1

# ---------------- validation ----------------
errs = []
# module schema
for mod in modules:
    for k in ("id", "code", "title", "weight", "summary", "objectives", "notes", "cards", "quiz"):
        if k not in mod:
            errs.append(f"{mod.get('id')}: missing key {k}")
    if not mod["summary"].startswith("Welcome to Module"):
        errs.append(f"{mod['id']}: summary not instructor voice")
    titles = [n["title"] for n in mod["notes"]]
    if titles[0] != "Concepts":
        errs.append(f"{mod['id']}: first note not Concepts: {titles}")
    if titles[1] not in ("Hands-on procedure", "Worked estimation"):
        errs.append(f"{mod['id']}: second note not procedure/estimation: {titles[1]}")
    if titles[2] != "Project brief":
        errs.append(f"{mod['id']}: third note not Project brief: {titles}")
    if titles[3] != "Honesty note":
        errs.append(f"{mod['id']}: fourth note not Honesty note: {titles}")
    # glossary bullet shape
    for line in mod["notes"][0]["body"].split("\n"):
        s = line.strip()
        if not s:
            continue
        if not (s.startswith("- **") and " \u2014 " in s):
            errs.append(f"{mod['id']}: Concepts line breaks glossary shape: {s[:60]}")
            break
    # numbered steps in section 2
    if not re.search(r"^1\.\s", mod["notes"][1]["body"], re.M):
        errs.append(f"{mod['id']}: section 2 lacks numbered steps")
    if len(mod["cards"]) < 5:
        errs.append(f"{mod['id']}: <5 cards")
    if len(mod["quiz"]) < 4:
        errs.append(f"{mod['id']}: <4 quiz")
    for q in mod["quiz"]:
        if len(q["choices"]) != 4 or not isinstance(q["answer"], int) or not q["explain"].strip():
            errs.append(f"{mod['id']}: bad quiz item: {q['q'][:40]}")
# course-level keys
for k in ("arc", "priorities", "battlePlan", "mockTasks", "cheatSheets", "answerBank",
          "mockMinutes", "sourceLinks", "honestyNote"):
    if k not in course:
        errs.append(f"missing course key {k}")
for t in course["mockTasks"]:
    if set(t) != {"id", "type", "q", "choices", "answer", "explain"} or t["type"] != "choice":
        errs.append(f"mockTask schema drift: {t.get('id')}")
    if len(t["choices"]) != 4 or not isinstance(t["answer"], int) or not t["explain"].strip():
        errs.append(f"mockTask bad: {t.get('id')}")
for sl in course["sourceLinks"]:
    if not sl.get("retrieved"):
        errs.append(f"sourceLink missing retrieved: {sl.get('name')}")
# brand guard
text = json.dumps(course)
for b in ["aleks", "brilliant", "khan academy", "coursera", "udemy", "edx", "palantir"]:
    if re.search(r"\b" + re.escape(b) + r"\b", text, re.I):
        errs.append(f"brand hit: {b}")
if re.search(r"\bNSA\b", text):
    errs.append("NSA hit")
# battlePlan module-number consistency: modules 1..9 in order
expected = ["il07-mongodb", "il07-data-schools", "il07-ai-ml", "il07-neuroai",
            "il07-openweight", "il07-agents", "il07-frontier", "il07-aws-data", "il07-aws-ml"]
if [m["id"] for m in modules] != expected:
    errs.append("module order changed!")

if errs:
    print("VALIDATION ERRORS:")
    for e in errs:
        print(" -", e)
    sys.exit(1)

# ---------------- atomic write ----------------
tmp = PATH + ".retrofit-tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(course, f, ensure_ascii=False, indent=1)
    f.write("\n")
with open(tmp, encoding="utf-8") as f:
    json.load(f)  # re-validate
os.replace(tmp, PATH)
print(f"OK: wrote {PATH}; code mockTasks converted: {fixed}")
