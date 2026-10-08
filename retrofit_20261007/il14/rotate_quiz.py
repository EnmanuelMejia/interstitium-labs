# -*- coding: utf-8 -*-
"""Deterministically rotate the 6 NEW quiz items' choices per module so answers
spread across 0-3. Old items (already answer=1) are left untouched."""
import json
import os

BASE = os.path.expanduser("~/workspace/apex-audit")
COURSE = os.path.join(BASE, "docs/university/data/courses/il-14-sre-devops-cloud-security-interview-prep.json")

with open(COURSE) as f:
    d = json.load(f)

for mi, m in enumerate(d["modules"]):
    assert len(m["quiz"]) == 10, m["id"]
    for j in range(6):
        q = m["quiz"][4 + j]
        assert q["answer"] == 1, (m["id"], j)
        r = (mi * 6 + j) % 4  # deterministic rotation
        if r:
            q["choices"] = q["choices"][r:] + q["choices"][:r]
            q["answer"] = (1 - r) % 4
        assert len(q["choices"]) == 4 and 0 <= q["answer"] <= 3

from collections import Counter
c = Counter(q["answer"] for m in d["modules"] for q in m["quiz"][4:])
print("new-quiz answer distribution:", dict(c))

tmp = COURSE + ".rot-tmp"
with open(tmp, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
    f.write("\n")
with open(tmp) as f:
    json.load(f)
os.replace(tmp, COURSE)
print("rotation WRITE OK")
