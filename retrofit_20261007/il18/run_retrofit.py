"""Runner: apply template retrofit to il-18 course file. Reads course JSON,
merges RETRO content from track_*.py files, writes back atomically.
"""
import json, glob, importlib, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
COURSE = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-18-technical-leadership-interview-prep.json"

# 1. load and validate BEFORE
course = json.load(open(COURSE))
print("BEFORE:", len(course["modules"]), "modules | keys:", list(course.keys()))

RETRO = {}
for f in sorted(glob.glob(os.path.join(BASE, "track_*.py"))):
    modname = os.path.basename(f)[:-3]
    mod = importlib.import_module(modname)
    for k, v in mod.RETRO.items():
        assert k not in RETRO, "duplicate id %s" % k
        RETRO[k] = v
print("RETRO entries:", len(RETRO))

module_ids = [m["id"] for m in course["modules"]]
missing = [i for i in module_ids if i not in RETRO]
extra = [i for i in RETRO if i not in module_ids]
print("missing:", missing, "| extra:", extra)
assert not missing and not extra

# banned-brand sweep over new content
blob = json.dumps(RETRO)
for brand in ["aleks", "brilliant", "khan academy", "coursera", "udemy", "edx", "palantir"]:
    assert brand not in blob.lower(), "banned brand: %s" % brand
print("banned-brand sweep OK")

# every module-level source URL must already exist in course sourceLinks
course_urls = {s["url"] for s in course["sourceLinks"]}

for m in course["modules"]:
    r = RETRO[m["id"]]
    assert {"summary", "concepts", "procedure", "brief", "honesty", "quiz"} <= set(r.keys()), m["id"]
    assert len(r["quiz"]) == 10, (m["id"], len(r["quiz"]))

    m["summary"] = r["summary"]
    # verify old "Sources" note URLs all exist in course-level sourceLinks BEFORE dropping the note
    for n in m["notes"]:
        for url in re.findall(r"https?://[^\s\)\]]+", n.get("body", "")):
            assert url in course_urls, (m["id"], "module source URL missing at course level:", url)
    m["notes"] = [
        {"title": "Concepts", "body": r["concepts"]},
        {"title": "Hands-on procedure", "body": r["procedure"]},
        {"title": "Project brief", "body": r["brief"]},
        {"title": "Honesty note", "body": r["honesty"]},
    ]
    quiz = []
    for (q, choices, ans, explain) in r["quiz"]:
        assert len(choices) == 4, (m["id"], q)
        assert isinstance(ans, int) and 0 <= ans <= 3, (m["id"], q)
        assert explain and explain.strip(), (m["id"], q)
        assert "video" not in explain.lower(), (m["id"], q)
        quiz.append({"q": q, "choices": choices, "answer": ans, "explain": explain})
    m["quiz"] = quiz

    # module source URLs preserved at course level?
    for n in m.get("notes", []):
        pass
    # old "Sources" note is being replaced; verify its URLs live in course sourceLinks
    # (recompute from the ORIGINAL notes captured before overwrite)
    assert len(m["cards"]) == 6, m["id"]

print("per-module asserts OK")

# atomic write
tmp = COURSE + ".tmp"
with open(tmp, "w") as f:
    json.dump(course, f, ensure_ascii=False, indent=2)
    f.write("\n")
os.replace(tmp, COURSE)

# validate AFTER
after = json.load(open(COURSE))
print("AFTER:", len(after["modules"]), "modules")
for m in after["modules"]:
    assert [n["title"] for n in m["notes"]] == ["Concepts", "Hands-on procedure", "Project brief", "Honesty note"], m["id"]
    assert len(m["quiz"]) == 10 and len(m["cards"]) == 6, m["id"]
    assert m["summary"].startswith("Welcome to") or m["summary"].startswith("Welcome back to"), m["id"]
print("AFTER validation OK")
