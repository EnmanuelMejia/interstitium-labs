"""Shuffle quiz choices deterministically so correct answers spread across
indices 0-3. Keeps q/explain intact; rotates answer index with the shuffle.
"""
import json, os, random

COURSE = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-18-technical-leadership-interview-prep.json"

course = json.load(open(COURSE))
rng = random.Random(20261007)

from collections import Counter
before = Counter()
for m in course["modules"]:
    for qi, q in enumerate(m["quiz"]):
        before[q["answer"]] += 1
print("before:", dict(before))

for m in course["modules"]:
    for qi, q in enumerate(m["quiz"]):
        correct_text = q["choices"][q["answer"]]
        # deterministic shuffle seeded by module+question index
        idx = list(range(len(q["choices"])))
        r = random.Random(20261007 + hash(m["id"] + "|" + str(qi)) % 100000)
        r.shuffle(idx)
        new_choices = [q["choices"][i] for i in idx]
        q["choices"] = new_choices
        q["answer"] = new_choices.index(correct_text)

after = Counter()
for m in course["modules"]:
    for q in m["quiz"]:
        assert len(q["choices"]) == 4 and 0 <= q["answer"] <= 3 and q["explain"].strip()
        after[q["answer"]] += 1
print("after:", dict(after))

tmp = COURSE + ".tmp"
with open(tmp, "w") as f:
    json.dump(course, f, ensure_ascii=False, indent=2)
    f.write("\n")
os.replace(tmp, COURSE)

json.load(open(COURSE))
print("shuffled + validated OK")
