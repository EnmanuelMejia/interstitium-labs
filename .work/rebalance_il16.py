#!/usr/bin/env python3
"""Rebalance IL-16 quiz answer positions via deterministic choice rotation.
Rotation preserves correctness: correct text moves from a to (a+shift)%4.
New items (last 4 per module): shift = position -> answers spread 0,1,2,3.
Older items: shift = (module_idx*7 + item_idx) % 4 -> deterministic spread."""
import json, os

SRC = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-16-machine-learning-ai-engineering.json"
d = json.load(open(SRC))

def rotate(item, shift):
    ch = item["choices"]
    a = item["answer"]
    correct_text = ch[a]
    new_ch = [ch[(i - shift) % 4] for i in range(4)]
    new_a = (a + shift) % 4
    assert new_ch[new_a] == correct_text, "rotation broke correctness"
    item["choices"] = new_ch
    item["answer"] = new_a

for mi, m in enumerate(d["modules"]):
    q = m["quiz"]
    n_new = 4
    for i, item in enumerate(q):
        if i >= len(q) - n_new:
            pos = i - (len(q) - n_new)   # 0..3
            rotate(item, pos)
        else:
            rotate(item, (mi * 7 + i) % 4)

tmp = SRC + ".tmp"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write("\n")
json.load(open(tmp))
os.replace(tmp, SRC)

d3 = json.load(open(SRC))
from collections import Counter
print("rebalanced:", dict(Counter(q["answer"] for m in d3["modules"] for q in m["quiz"])))
