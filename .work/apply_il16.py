#!/usr/bin/env python3
"""Apply IL-16 expansions: cards + quiz + note-title fixes + trainers + terminalSims."""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/apex-audit/.work")
from il16_content import NEWCARDS, TRAINERS, TERMINALSIMS, NOTEFIX
from il16_quiz1 import NEWQUIZ

SRC = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-16-machine-learning-ai-engineering.json"

d = json.load(open(SRC))
by_id = {m["id"]: m for m in d["modules"]}

missing_c = [mid for mid in NEWCARDS if mid not in by_id]
missing_q = [mid for mid in NEWQUIZ if mid not in by_id]
assert not missing_c and not missing_q, (missing_c, missing_q)

for mid, cards in NEWCARDS.items():
    m = by_id[mid]
    for front, back in cards:
        assert front.strip() and back.strip(), f"empty card in {mid}"
        m["cards"].append({"front": front, "back": back})

for mid, items in NEWQUIZ.items():
    m = by_id[mid]
    for it in items:
        assert len(it["choices"]) == 4, f"choices!=4 in {mid}"
        assert isinstance(it["answer"], int) and 0 <= it["answer"] <= 3, f"bad answer in {mid}"
        assert it["q"].strip() and it["explain"].strip(), f"empty q/explain in {mid}"
        m["quiz"].append({"q": it["q"], "choices": it["choices"],
                          "answer": it["answer"], "explain": it["explain"]})

for mid, mapping in NOTEFIX.items():
    m = by_id[mid]
    for n in m["notes"]:
        if n["title"] in mapping:
            n["title"] = mapping[n["title"]]

d["trainers"] = TRAINERS
d["terminalSims"] = TERMINALSIMS

for m in d["modules"]:
    fronts = [c["front"] for c in m["cards"]]
    assert len(fronts) == len(set(fronts)), f"dup front in {m['id']}"
    assert len(m["cards"]) >= 8, f"thin cards {m['id']}"
    assert len(m["quiz"]) >= 8, f"thin quiz {m['id']}"
    assert len(m["notes"]) == 4, f"notes!=4 {m['id']}"

tmp = SRC + ".tmp"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write("\n")
json.load(open(tmp))
os.replace(tmp, SRC)
d3 = json.load(open(SRC))
mods = d3["modules"]
print("IL-16 applied OK. modules:", len(mods),
      "cards:", sum(len(m["cards"]) for m in mods),
      "quiz:", sum(len(m["quiz"]) for m in mods),
      "trainers:", len(d3["trainers"]),
      "terminalSims:", len(d3["terminalSims"]))
