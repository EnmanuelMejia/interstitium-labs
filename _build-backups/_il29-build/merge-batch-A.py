#!/usr/bin/env python3
"""Merge batch-A module files into batch-A.json and validate all hard requirements."""
import json, os, sys

BASE = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il29-build"
MOD_IDS = ["IL29-M%02d" % n for n in range(1, 9)]
REQUIRED_KEYS = ["id", "code", "title", "summary", "objectives", "estimatedMinutes",
                 "weight", "notes", "cards", "quiz", "drills", "handsOnLab",
                 "videos", "mockTask", "crossLinks", "prerequisiteFor"]

modules = []
errors = []
report = []

for mid in MOD_IDS:
    path = os.path.join(BASE, "batch-A-m%02d.json" % (MOD_IDS.index(mid) + 1))
    try:
        with open(path) as f:
            m = json.load(f)
    except Exception as e:
        errors.append("%s: failed to load: %s" % (mid, e))
        continue
    modules.append(m)
    tag = mid
    # required keys
    for k in REQUIRED_KEYS:
        if k not in m:
            errors.append("%s: missing key %s" % (tag, k))
    if m.get("id") != mid:
        errors.append("%s: id mismatch: %s" % (tag, m.get("id")))
    # notes
    notes = m.get("notes", [])
    if not (6 <= len(notes) <= 8):
        errors.append("%s: notes count %d (need 6-8)" % (tag, len(notes)))
    for i, n in enumerate(notes):
        if not isinstance(n, dict) or "title" not in n or "body" not in n:
            errors.append("%s: note %d not object-based" % (tag, i))
            continue
        wc = len(n["body"].split())
        if not (400 <= wc <= 900):
            errors.append("%s: note %d word count %d (need 400-900)" % (tag, i, wc))
    # cards
    cards = m.get("cards", [])
    if len(cards) != 12:
        errors.append("%s: cards count %d (need exactly 12)" % (tag, len(cards)))
    for i, c in enumerate(cards):
        if not isinstance(c, dict) or "front" not in c or "back" not in c:
            errors.append("%s: card %d bad shape" % (tag, i))
    # quiz
    quiz = m.get("quiz", [])
    if not (9 <= len(quiz) <= 10):
        errors.append("%s: quiz count %d (need 9-10)" % (tag, len(quiz)))
    for i, q in enumerate(quiz):
        if not isinstance(q, dict) or not all(k in q for k in ("q", "choices", "answer", "explain")):
            errors.append("%s: quiz %d bad shape" % (tag, i))
            continue
        if len(q["choices"]) != 4 or not (0 <= q["answer"] <= 3):
            errors.append("%s: quiz %d choices/answer bad" % (tag, i))
    # drills
    drills = m.get("drills", [])
    if not (2 <= len(drills) <= 3):
        errors.append("%s: drills count %d (need 2-3)" % (tag, len(drills)))
    for d in drills:
        items = d.get("items", [])
        if not (5 <= len(items) <= 8):
            errors.append("%s: drill %s items %d (need 5-8)" % (tag, d.get("id"), len(items)))
        for it in items:
            if not isinstance(it, dict) or not all(k in it for k in ("prompt", "answer", "explain")):
                errors.append("%s: drill %s item bad shape" % (tag, d.get("id")))
    # lab
    lab = m.get("handsOnLab", {})
    steps = lab.get("steps", [])
    if not (8 <= len(steps) <= 14):
        errors.append("%s: lab steps %d (need 8-14)" % (tag, len(steps)))
    for k in ("id", "title", "brief", "deliverable", "checkpoint"):
        if k not in lab:
            errors.append("%s: lab missing %s" % (tag, k))
    # videos
    vids = m.get("videos", [])
    if not (0 <= len(vids) <= 2):
        errors.append("%s: videos count %d (need 0-2)" % (tag, len(vids)))
    for v in vids:
        if v.get("httpStatus") != 200 or "verifiedUtc" not in v or "watchBefore" not in v:
            errors.append("%s: video missing verification fields" % tag)
    # mockTask
    mt = m.get("mockTask", {})
    if mt.get("type") != "choice" or len(mt.get("choices", [])) != 4:
        errors.append("%s: mockTask bad shape" % tag)
    # objectives
    obj = m.get("objectives", [])
    if not (4 <= len(obj) <= 6):
        errors.append("%s: objectives %d (need 4-6)" % (tag, len(obj)))
    # crossLinks / prerequisiteFor
    cl = m.get("crossLinks", [])
    if not (2 <= len(cl) <= 4):
        errors.append("%s: crossLinks %d (need 2-4)" % (tag, len(cl)))
    pf = m.get("prerequisiteFor", [])
    if not (0 <= len(pf) <= 3):
        errors.append("%s: prerequisiteFor %d (need 0-3)" % (tag, len(pf)))

    min_wc = min(len(n["body"].split()) for n in notes) if notes else 0
    max_wc = max(len(n["body"].split()) for n in notes) if notes else 0
    report.append("%s notes=%d cards=%d quiz=%d drills=%d drillItems=[%s] labSteps=%d videos=%d noteWords=%d-%d estMin=%d weight=%d" % (
        mid, len(notes), len(cards), len(quiz), len(drills),
        ",".join(str(len(d.get("items", []))) for d in drills),
        len(steps), len(vids), min_wc, max_wc,
        m.get("estimatedMinutes"), m.get("weight")))

if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print("  -", e)
    sys.exit(1)

out = os.path.join(BASE, "batch-A.json")
tmp = out + ".tmp"
with open(tmp, "w") as f:
    json.dump(modules, f, indent=1, ensure_ascii=False)
    f.write("\n")
os.replace(tmp, out)

# re-validate final file
with open(out) as f:
    d = json.load(f)
assert isinstance(d, list) and len(d) == 8, "final file must be array of 8"
print("OK: batch-A.json written, %d modules, valid JSON" % len(d))
print()
for r in report:
    print(r)
