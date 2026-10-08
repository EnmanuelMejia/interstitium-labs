#!/usr/bin/env python3
"""Apply IL-09 module retrofit: instructor-voice summaries, weight key,
template-titled 4-section notes. Preserves cards/quiz/objectives.
Backs up the original first. Never heredocs: this file was written via the file tools."""
import json, os, re, shutil, sys

BASE = os.path.expanduser("~/workspace/apex-audit")
WORK = os.path.join(BASE, "retrofit_20261007", "il09")
SRC = os.path.join(BASE, "docs/university/data/courses/il-09-adaptive-certification-command.json")
BAK = os.path.join(WORK, "il-09-adaptive-certification-command.orig.json")

sys.path.insert(0, WORK)
from module_content_part1 import MODULES as P1
from module_content_part2 import MODULES as P2
NEW = {**P1, **P2}

def main():
    course = json.load(open(SRC))  # load BEFORE
    if not os.path.exists(BAK):
        shutil.copy2(SRC, BAK)
        print("backup written:", BAK)

    expect = {m["id"] for m in course["modules"]}
    assert set(NEW.keys()) == expect, f"module id mismatch: {set(NEW.keys()) ^ expect}"

    banned = re.compile(r"\b(ALEKS|Brilliant|Khan Academy|Coursera|Udemy|edX|Pluralsight)\b", re.I)
    pal = re.compile(r"\bPalantir\b", re.I)
    nsaword = re.compile(r"\bNSA\b")

    for m in course["modules"]:
        mid = m["id"]
        new = NEW[mid]
        m["weight"] = 1
        m["summary"] = new["summary"]
        m["notes"] = [{"title": n["title"], "body": n["body"]} for n in new["notes"]]
        # key order: match template shape
        ordered = {k: m[k] for k in ["id", "code", "title", "weight", "summary",
                                     "objectives", "notes", "cards", "quiz"] if k in m}
        for k in m:
            if k not in ordered:
                ordered[k] = m[k]
        m.clear(); m.update(ordered)

        # validations per module
        titles = [n["title"] for n in m["notes"]]
        assert titles == ["Concepts", "Hands-on procedure", "Project brief", "Noah check-in"], (mid, titles)
        concepts = m["notes"][0]["body"]
        assert concepts.startswith("- **"), (mid, "Concepts must start with glossary bullet")
        for line in concepts.splitlines():
            if line.strip():
                assert re.match(r"^- \*\*.+\*\* — .+", line) or not line.startswith("- "), (mid, line[:60])
        assert "I'm your instructor" in m["summary"], (mid, "summary not instructor voice")
        for q in m["quiz"]:
            assert len(q["choices"]) == 4, (mid, q["q"][:50])
            assert isinstance(q["answer"], int) and 0 <= q["answer"] < 4, (mid, q["q"][:50])
            assert q["explain"], (mid, q["q"][:50])
            assert "video" not in q["explain"].lower(), (mid, "video ref in explain")
        blob = json.dumps(m)
        assert not banned.search(blob), (mid, "competitor brand found")
        assert not pal.search(blob), (mid, "Palantir found")
        assert not nsaword.search(blob), (mid, "NSA found")
        for cd in m["cards"]:
            assert cd["front"] and cd["back"], (mid, "empty card")

    # course-level validation
    required = ["arc", "priorities", "battlePlan", "mockTasks", "cheatSheets",
                "answerBank", "mockMinutes", "sourceLinks", "honestyNote"]
    for k in required:
        assert k in course and course[k], f"missing course key: {k}"
    assert isinstance(course["mockMinutes"], int), "mockMinutes not int"
    assert course["honestyNote"], "empty honestyNote"
    for s in course["sourceLinks"]:
        assert s.get("name") and s.get("url") and s.get("retrieved"), ("sourceLink", s.get("name"))

    # atomic write
    tmp = SRC + ".tmp"
    with open(tmp, "w") as f:
        json.dump(course, f, indent=1, ensure_ascii=False)
        f.write("\n")
    json.load(open(tmp))  # validate AFTER
    os.replace(tmp, SRC)
    print("wrote", SRC)
    print("modules retrofitted:", len(course["modules"]))
    print("all validations passed")

if __name__ == "__main__":
    main()
