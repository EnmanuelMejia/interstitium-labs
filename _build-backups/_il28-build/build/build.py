import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "batch-C.json")

REQUIRED = ["id", "code", "title", "summary", "objectives", "notes", "cards",
            "quiz", "weight", "prerequisiteFor", "drills", "handsOnLab",
            "mockTask", "crossLinks", "videos", "estimatedMinutes"]


def load(n):
    path = os.path.join(HERE, "m%02d.py" % n)
    name = "m%02d" % n
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.module


def round30(x):
    return int((x + 15) / 30) * 30


errors = []
modules = []
for n in range(17, 25):
    m = load(n)
    mid = m.get("id", "m%02d" % n)
    for f in REQUIRED:
        if f not in m:
            errors.append("%s: missing field %s" % (mid, f))
    # objectives
    if not (4 <= len(m["objectives"]) <= 5):
        errors.append("%s: objectives=%d (need 4-5)" % (mid, len(m["objectives"])))
    # notes
    if not (5 <= len(m["notes"]) <= 8):
        errors.append("%s: notes=%d (need 5-8)" % (mid, len(m["notes"])))
    for i, note in enumerate(m["notes"]):
        wc = len(note["body"].split())
        if not (120 <= wc <= 300):
            errors.append("%s note %d (%s): %d words (need 120-300)"
                          % (mid, i, note.get("title", "?")[:40], wc))
    # cards
    if not (10 <= len(m["cards"]) <= 14):
        errors.append("%s: cards=%d (need 10-14)" % (mid, len(m["cards"])))
    for i, c in enumerate(m["cards"]):
        if not c.get("front") or not c.get("back"):
            errors.append("%s card %d: empty front/back" % (mid, i))
    # quiz
    if not (8 <= len(m["quiz"]) <= 10):
        errors.append("%s: quiz=%d (need 8-10)" % (mid, len(m["quiz"])))
    for i, q in enumerate(m["quiz"]):
        if len(q.get("choices", [])) != 4:
            errors.append("%s quiz %d: choices=%d (need 4)" % (mid, i, len(q.get("choices", []))))
        if not (0 <= q.get("answer", -1) <= 3):
            errors.append("%s quiz %d: bad answer index" % (mid, i))
        if not q.get("explain"):
            errors.append("%s quiz %d: empty explain" % (mid, i))
    # drills
    if not (1 <= len(m["drills"]) <= 2):
        errors.append("%s: drills=%d (need 1-2)" % (mid, len(m["drills"])))
    drill_items = 0
    for d in m["drills"]:
        if not (6 <= len(d["items"]) <= 8):
            errors.append("%s drill %s: items=%d (need 6-8)" % (mid, d.get("id"), len(d["items"])))
        drill_items += len(d["items"])
        for i, it in enumerate(d["items"]):
            if not it.get("prompt") or not it.get("answer") or not it.get("explain"):
                errors.append("%s drill %s item %d: missing prompt/answer/explain"
                              % (mid, d.get("id"), i))
    # lab
    lab = m["handsOnLab"]
    if not (8 <= len(lab["steps"]) <= 14):
        errors.append("%s lab: steps=%d (need 8-14)" % (mid, len(lab["steps"])))
    for f in ("brief", "deliverable", "checkpoint"):
        if not lab.get(f):
            errors.append("%s lab: missing %s" % (mid, f))
    # mock
    mk = m["mockTask"]
    if len(mk.get("choices", [])) != 4 or not (0 <= mk.get("answer", -1) <= 3) or not mk.get("explain"):
        errors.append("%s mockTask: malformed" % mid)
    # videos
    if not (1 <= len(m["videos"]) <= 2):
        errors.append("%s: videos=%d (need 1-2)" % (mid, len(m["videos"])))
    for v in m["videos"]:
        for f in ("title", "url", "source", "durationMin", "order", "watchBefore", "blurb"):
            if f not in v:
                errors.append("%s video: missing %s" % (mid, f))
    # estimatedMinutes
    video_min = sum(v["durationMin"] for v in m["videos"])
    est = (m["weight"] * 120 + len(m["notes"]) * 12 + len(m["cards"]) * 4
           + len(m["quiz"]) * 8 + drill_items * 4 + 90
           + min(180, video_min / 2))
    m["estimatedMinutes"] = round30(est)
    print("%s: notes=%d cards=%d quiz=%d drillItems=%d labSteps=%d videoMin=%d -> %d min"
          % (mid, len(m["notes"]), len(m["cards"]), len(m["quiz"]),
             drill_items, len(lab["steps"]), video_min, m["estimatedMinutes"]))
    modules.append(m)

if errors:
    print("\nVALIDATION ERRORS:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

with open(OUT, "w") as f:
    json.dump(modules, f, indent=2)
    f.write("\n")

# re-validate the written file parses and is a bare array
data = json.load(open(OUT))
assert isinstance(data, list) and len(data) == 8
total = sum(m["estimatedMinutes"] for m in data)
print("\nOK: wrote %s — %d modules, total %d estimated minutes" % (OUT, len(data), total))
