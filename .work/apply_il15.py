#!/usr/bin/env python3
"""Apply IL-15 expansions: rewrites + new cards + trainers. Atomic replace + validate."""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/apex-audit/.work")
from il15_content import NEWCARDS, REWRITE, TRAINERS

SRC = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-15-data-engineering-analytics-interview-prep.json"

d = json.load(open(SRC))
by_id = {m["id"]: m for m in d["modules"]}

for mid, rewrites in REWRITE.items():
    m = by_id[mid]
    for idx, (front, back) in rewrites.items():
        assert m["cards"][idx]["front"], f"missing card {idx} in {mid}"
        m["cards"][idx] = {"front": front, "back": back}

for mid, cards in NEWCARDS.items():
    m = by_id[mid]
    for front, back in cards:
        assert front.strip() and back.strip(), f"empty card text in {mid}"
        m["cards"].append({"front": front, "back": back})

d["trainers"] = TRAINERS

# duplicate-front guard per module
for m in d["modules"]:
    fronts = [c["front"] for c in m["cards"]]
    assert len(fronts) == len(set(fronts)), f"dup front in {m['id']}"

tmp = SRC + ".tmp"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write("\n")
d2 = json.load(open(tmp))
os.replace(tmp, SRC)
d3 = json.load(open(SRC))
mods = d3["modules"]
print("IL-15 applied OK. modules:", len(mods),
      "cards:", sum(len(m["cards"]) for m in mods),
      "quiz:", sum(len(m["quiz"]) for m in mods),
      "trainers:", len(d3["trainers"]))
