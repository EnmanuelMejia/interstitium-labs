"""Apply the IL-21 multicloud-template retrofit. Reads content_*.py, transforms
docs/university/data/courses/il-21-humanities.json in place (atomic write).
Validates JSON before and after plus all hard rules."""
import json, os, re, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content_a import MODULES_A
from content_b import MODULES_B
from content_course import NEW_MOCK_TASKS, NEW_CHEAT_SHEETS, BATTLEPLAN_PATCH

TARGET = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/il-21-humanities.json")
EXPECTED_TITLES = ["Concepts", "Hands-on procedure", "Project brief", "Noah check-in"]
ALT_TITLES = {"Worked estimation"}  # allowed substitute for 'Hands-on procedure'
BANNED = re.compile(r"\b(aleks|brilliant|khan academy|coursera|udemy|edx)\b", re.I)

def check(cond, msg):
    if not cond:
        raise SystemExit("VALIDATION FAILED: " + msg)

def main():
    with open(TARGET, encoding="utf-8") as f:
        doc = json.load(f)  # validates BEFORE
    check(doc.get("courseId") == "il-21-humanities", "courseId mismatch")
    mods = doc["modules"]
    check(len(mods) == 14, "expected 14 modules, got %d" % len(mods))

    content = dict(MODULES_A); content.update(MODULES_B)
    check(set(content.keys()) == {m["id"] for m in mods}, "content/module id mismatch")

    for m in mods:
        c = content[m["id"]]
        # summary -> instructor voice
        m["summary"] = c["summary"]
        check("I'm your instructor" in m["summary"], m["id"] + ": summary missing instructor voice")
        # notes -> 4 titled sections
        notes = c["notes"]
        check(len(notes) == 4, m["id"] + ": notes != 4")
        for i, n in enumerate(notes):
            exp = EXPECTED_TITLES[i]
            ok = (n["title"] == exp) or (exp == "Hands-on procedure" and n["title"] in ALT_TITLES)
            check(ok, "%s: note %d title %r" % (m["id"], i, n["title"]))
            check(isinstance(n.get("body"), str) and n["body"].strip(), "%s: note %d empty body" % (m["id"], i))
        concepts = notes[0]["body"]
        check(concepts.count("- **") >= 5, m["id"] + ": Concepts missing glossary bullets")
        proc = notes[1]["body"]
        check(re.search(r"(?m)^\d+\.\s", proc), m["id"] + ": procedure missing numbered steps")
        check(len(notes[3]["body"]) > 0, m["id"] + ": honesty note empty")
        m["notes"] = [{"title": n["title"], "body": n["body"], **({"code": n["code"], "lang": n["lang"]} if "code" in n else {})} for n in notes]
        # thin-module card expansion
        if "extra_cards" in c:
            before = len(m["cards"])
            m["cards"].extend(c["extra_cards"])
            check(len(m["cards"]) == before + len(c["extra_cards"]) and len(m["cards"]) >= 6,
                  m["id"] + ": card expansion failed")
        else:
            check(len(m["cards"]) >= 5, m["id"] + ": unexpected thin cards")
        # quiz: keep q/choices/answer, replace explain
        check(len(m["quiz"]) == 4, m["id"] + ": quiz != 4")
        for qi, q in enumerate(m["quiz"]):
            check(len(q["choices"]) == 4, "%s quiz %d: choices != 4" % (m["id"], qi))
            check(isinstance(q["answer"], int) and 0 <= q["answer"] < 4, "%s quiz %d: bad answer index" % (m["id"], qi))
            q["explain"] = c["quiz_explains"][qi]
            check(q["explain"].strip(), "%s quiz %d: empty explain" % (m["id"], qi))

    # course-level: mock tasks 36 -> 56
    existing_ids = {t["id"] for t in doc["mockTasks"]}
    check(len(doc["mockTasks"]) == 36, "expected 36 mockTasks, got %d" % len(doc["mockTasks"]))
    for t in NEW_MOCK_TASKS:
        check(t["id"] not in existing_ids, "dup mock id " + t["id"])
        check(t["type"] == "choice" and len(t["choices"]) == 4, t["id"] + ": bad choices")
        check(isinstance(t["answer"], int) and 0 <= t["answer"] < 4, t["id"] + ": bad answer")
        check(t["explain"].strip(), t["id"] + ": empty explain")
    doc["mockTasks"].extend(NEW_MOCK_TASKS)
    check(len(doc["mockTasks"]) == 56, "mockTasks != 56")

    # cheat sheets 3 -> 5
    check(len(doc["cheatSheets"]) == 3, "expected 3 cheatSheets")
    for cs in NEW_CHEAT_SHEETS:
        check(cs["title"] and all(b.get("h") and b.get("body") for b in cs["blocks"]), "bad cheat sheet")
    doc["cheatSheets"].extend(NEW_CHEAT_SHEETS)
    check(len(doc["cheatSheets"]) == 5, "cheatSheets != 5")

    # battlePlan patch
    patched = False
    for b in doc["battlePlan"]:
        if b["id"] == BATTLEPLAN_PATCH["id"]:
            b["title"] = BATTLEPLAN_PATCH["title"]; b["minutes"] = BATTLEPLAN_PATCH["minutes"]
            patched = True
    check(patched, "bp21-6 not found")

    # hard rules over the whole document
    blob = json.dumps(doc)
    m_banned = BANNED.search(blob)
    check(not m_banned, "banned brand found: " + (m_banned.group(0) if m_banned else ""))
    check("Palantir" not in blob and "NSA" not in blob.replace("NASA", ""), "palantir/nsa content found")
    for k in ["arc", "priorities", "battlePlan", "mockTasks", "cheatSheets", "answerBank",
              "mockMinutes", "sourceLinks", "honestyNote"]:
        check(k in doc and doc[k] not in (None, [], ""), "course key missing/empty: " + k)
    check(isinstance(doc["mockMinutes"], int), "mockMinutes not int")
    for s in doc["sourceLinks"]:
        check(s.get("name") and s.get("url") and s.get("retrieved"), "sourceLink missing retrieved")

    # atomic write + re-validate
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(TARGET), suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
            f.write("\n")
        with open(tmp, encoding="utf-8") as f:
            reloaded = json.load(f)
        check(len(reloaded["modules"]) == 14 and len(reloaded["mockTasks"]) == 56, "post-write mismatch")
        os.replace(tmp, TARGET)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    print("OK: 14 modules retrofitted; mockTasks=56; cheatSheets=5; battlePlan bp21-6 patched.")
    print("Bytes:", os.path.getsize(TARGET))

if __name__ == "__main__":
    main()
