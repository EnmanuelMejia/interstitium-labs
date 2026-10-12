import json, glob, os

build = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il29-build"
mods = []
for n in ["m25", "m26", "m27", "m28", "m29", "m30", "m31", "m32"]:
    p = os.path.join(build, f"{n}.json")
    mods.append(json.load(open(p)))
assert [m["id"] for m in mods] == [f"IL29-M{i}" for i in range(25, 33)], "id order wrong"

out = os.path.join(build, "batch-D.json")
with open(out, "w") as f:
    json.dump(mods, f, ensure_ascii=False, indent=1)
print("wrote", out, len(mods), "modules")

# ---- self-check ----
req_keys = ["id","code","title","summary","objectives","estimatedMinutes","weight",
            "notes","cards","quiz","drills","handsOnLab","videos","mockTask",
            "crossLinks","prerequisiteFor"]
ok = True
for m in mods:
    mid = m["id"]
    for k in req_keys:
        if k not in m:
            print(f"FAIL {mid}: missing key {k}"); ok = False
    nn = len(m["notes"])
    if not (6 <= nn <= 8): print(f"FAIL {mid}: notes={nn}"); ok = False
    for i, n in enumerate(m["notes"]):
        wc = len(n["body"].split())
        if not (400 <= wc <= 900): print(f"WARN {mid} note{i} words={wc}")
        if set(n.keys()) != {"title","body"}: print(f"FAIL {mid} note{i} keys"); ok = False
    if len(m["cards"]) != 12: print(f"FAIL {mid}: cards={len(m['cards'])}"); ok = False
    for c in m["cards"]:
        if set(c.keys()) != {"front","back"}: print(f"FAIL {mid} card keys"); ok = False
    nq = len(m["quiz"])
    if not (9 <= nq <= 10): print(f"FAIL {mid}: quiz={nq}"); ok = False
    for qi, q in enumerate(m["quiz"]):
        if len(q["choices"]) != 4: print(f"FAIL {mid} q{qi}: choices"); ok = False
        if not (0 <= q["answer"] <= 3): print(f"FAIL {mid} q{qi}: answer idx"); ok = False
        if not q.get("explain"): print(f"FAIL {mid} q{qi}: no explain"); ok = False
    nd = len(m["drills"])
    if not (2 <= nd <= 3): print(f"FAIL {mid}: drills={nd}"); ok = False
    for d in m["drills"]:
        ni = len(d["items"])
        if not (5 <= ni <= 8): print(f"FAIL {mid} {d['id']}: items={ni}"); ok = False
        for it in d["items"]:
            if set(it.keys()) != {"prompt","answer","explain"}: print(f"FAIL {mid} drill item keys"); ok = False
    lab = m["handsOnLab"]
    if set(lab.keys()) != {"id","title","brief","steps","deliverable","checkpoint"}:
        print(f"FAIL {mid} lab keys"); ok = False
    ns = len(lab["steps"])
    if not (8 <= ns <= 14): print(f"FAIL {mid}: lab steps={ns}"); ok = False
    if not (1 <= len(m["videos"]) <= 2): print(f"FAIL {mid}: videos={len(m['videos'])}"); ok = False
    for v in m["videos"]:
        if v.get("httpStatus") != 200: print(f"FAIL {mid} video status"); ok = False
    mt = m["mockTask"]
    if not (len(mt["choices"]) == 4 and 0 <= mt["answer"] <= 3 and mt.get("explain")):
        print(f"FAIL {mid} mockTask"); ok = False
    if not (2 <= len(m["crossLinks"]) <= 4): print(f"FAIL {mid}: crossLinks"); ok = False
    if not (4 <= len(m["objectives"]) <= 6): print(f"FAIL {mid}: objectives"); ok = False
    if not (1 <= m["weight"] <= 5): print(f"FAIL {mid}: weight"); ok = False
    if not (480 <= m["estimatedMinutes"] <= 620): print(f"WARN {mid}: minutes={m['estimatedMinutes']}")

print("ALL CHECKS PASSED" if ok else "FAILURES FOUND")
# summary table
for m in mods:
    wcs = [len(n["body"].split()) for n in m["notes"]]
    print(f"{m['id']}: notes={len(m['notes'])} words={min(wcs)}-{max(wcs)} cards={len(m['cards'])} "
          f"quiz={len(m['quiz'])} drills={len(m['drills'])}/{[len(d['items']) for d in m['drills']]} "
          f"labsteps={len(m['handsOnLab']['steps'])} videos={len(m['videos'])} min={m['estimatedMinutes']} wt={m['weight']}")
import os as _os
print("bytes:", _os.path.getsize(out))
