#!/usr/bin/env python3
"""Merge part_f_*.json into batch-F.json and audit against the spec."""
import json, glob, re, sys

REQUIRED = ["id","code","title","summary","objectives","notes","cards","quiz",
            "weight","prerequisiteFor","drills","handsOnLab","mockTask",
            "crossLinks","videos","estimatedMinutes"]

files = sorted(glob.glob("/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build/part_f_m*.json"))
modules = []
for fp in files:
    with open(fp) as f:
        modules.append(json.load(f))

errors = []
ids = [m.get("id") for m in modules]
if ids != [f"IL28-M{i}" for i in range(41, 51)]:
    errors.append(f"ID sequence wrong: {ids}")

for m in modules:
    mid = m.get("id", "?")
    for field in REQUIRED:
        if field not in m:
            errors.append(f"{mid}: missing field {field}")
    if not (4 <= len(m.get("objectives", [])) <= 5):
        errors.append(f"{mid}: objectives count {len(m.get('objectives', []))}")
    notes = m.get("notes", [])
    if not (5 <= len(notes) <= 8):
        errors.append(f"{mid}: notes count {len(notes)}")
    for n in notes:
        wc = len(n.get("body", "").split())
        if not (120 <= wc <= 300):
            errors.append(f"{mid}: note '{n.get('title','?')[:40]}' word count {wc}")
        if "title" not in n or "body" not in n:
            errors.append(f"{mid}: note missing title/body")
    if not (10 <= len(m.get("cards", [])) <= 14):
        errors.append(f"{mid}: cards count {len(m.get('cards', []))}")
    quiz = m.get("quiz", [])
    if not (8 <= len(quiz) <= 10):
        errors.append(f"{mid}: quiz count {len(quiz)}")
    for qi, q in enumerate(quiz):
        if len(q.get("choices", [])) != 4:
            errors.append(f"{mid}: quiz[{qi}] choices != 4")
        if not (0 <= q.get("answer", -1) <= 3):
            errors.append(f"{mid}: quiz[{qi}] answer index bad")
        if not q.get("explain"):
            errors.append(f"{mid}: quiz[{qi}] missing explain")
    drills = m.get("drills", [])
    if not (1 <= len(drills) <= 2):
        errors.append(f"{mid}: drills count {len(drills)}")
    drill_items = 0
    for d in drills:
        items = d.get("items", [])
        drill_items += len(items)
        if not (6 <= len(items) <= 8):
            errors.append(f"{mid}: drill {d.get('id')} items {len(items)}")
        for it in items:
            if not (it.get("prompt") and it.get("answer") and it.get("explain")):
                errors.append(f"{mid}: drill item missing prompt/answer/explain")
    lab = m.get("handsOnLab", {})
    steps = lab.get("steps", [])
    if not (8 <= len(steps) <= 14):
        errors.append(f"{mid}: lab steps {len(steps)}")
    for k in ["id","title","brief","steps","deliverable","checkpoint"]:
        if k not in lab:
            errors.append(f"{mid}: lab missing {k}")
    mt = m.get("mockTask", {})
    for k in ["id","type","q","choices","answer","explain"]:
        if k not in mt:
            errors.append(f"{mid}: mockTask missing {k}")
    vids = m.get("videos", [])
    if not (1 <= len(vids) <= 2):
        errors.append(f"{mid}: videos count {len(vids)}")
    # estimatedMinutes formula check
    video_min = sum(v.get("durationMin", 0) for v in vids)
    expect = (m["weight"]*120 + len(notes)*12 + len(m["cards"])*4 +
              len(quiz)*8 + drill_items*4 + 90 + min(180, video_min/2))
    expect = round(expect/30)*30
    if m.get("estimatedMinutes") != expect:
        errors.append(f"{mid}: estimatedMinutes {m.get('estimatedMinutes')} != formula {expect}")

# write merged file ONLY if no errors
if errors:
    print("AUDIT FAILURES:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

out = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build/batch-F.json"
with open(out, "w") as f:
    json.dump(modules, f, indent=2, ensure_ascii=False)

# re-read to prove parseability
with open(out) as f:
    back = json.load(f)
total_min = sum(m["estimatedMinutes"] for m in back)
print(f"OK: {len(back)} modules, total estimated minutes = {total_min}")
for m in back:
    di = sum(len(d["items"]) for d in m["drills"])
    print(f"  {m['id']}: notes={len(m['notes'])} cards={len(m['cards'])} quiz={len(m['quiz'])} drillItems={di} labSteps={len(m['handsOnLab']['steps'])} videos={len(m['videos'])} min={m['estimatedMinutes']}")
