#!/usr/bin/env python3
"""Course-level consistency audit for IL-09 retrofit. Read-only."""
import json, os, re

BASE = os.path.expanduser("~/workspace/apex-audit")
SRC = os.path.join(BASE, "docs/university/data/courses/il-09-adaptive-certification-command.json")
c = json.load(open(SRC))

print("top keys:", list(c.keys()))
print("arc:", [(a["phase"], a["title"]) for a in c["arc"]])
print("priorities total minutes:", sum(p["minutes"] for p in c["priorities"]))
print("battlePlan:", [(b["id"], b["title"], b["minutes"]) for b in c["battlePlan"]])
print("mockTasks:", len(c["mockTasks"]), "| mockMinutes:", c["mockMinutes"])
for t in c["mockTasks"]:
    assert len(t["choices"]) == 4 and isinstance(t["answer"], int) and 0 <= t["answer"] < 4 and t["explain"], t["id"]
print("mockTasks: all 4-choice, 0-based, explained")
print("cheatSheets:", [(s["title"], len(s["blocks"])) for s in c["cheatSheets"]])
for s in c["cheatSheets"]:
    for b in s["blocks"]:
        assert "h" in b and "body" in b, s["title"]
print("answerBank:", len(c["answerBank"]))
print("sourceLinks:", [(s["name"], s["retrieved"]) for s in c["sourceLinks"]])
print("honestyNote len:", len(c["honestyNote"]))
print("trainers:", [(t["id"], t["kind"]) for t in c.get("trainers", [])])
print("terminalSims present:", "terminalSims" in c)
print("scriptLabs/drills/scenarios:", len(c.get("scriptLabs",[])), len(c.get("drills",[])), len(c.get("scenarios",[])))
print("certifications:", len(c.get("certifications",[])))
# module summary spot-check
for m in c["modules"]:
    print(m["id"], "| weight:", m.get("weight"), "| notes:", [n["title"] for n in m["notes"]],
          "| cards:", len(m["cards"]), "| quiz:", len(m["quiz"]), "| voice:", "I'm your instructor" in m["summary"])
print("AUDIT OK")
