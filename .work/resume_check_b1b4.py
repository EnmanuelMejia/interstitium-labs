#!/usr/bin/env python3
"""Resume pass: ffprobe-check every B1-B4 registry MP4; collect files that are
missing, partial (duration<29s), or lack .vtt/.narration.md companions.
Deletes only incomplete B1-B4-registry MP4s (files this recovery rendered).
Never touches sibling-builder bc-* files (they're in other registries)."""
import importlib.util, os, subprocess, json

WORK = os.path.expanduser("~/workspace/apex-audit/.work")
VIDDIR = os.path.join(WORK, "..", "docs", "assets", "videos")

def duration(path):
    try:
        p = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", path],
                           capture_output=True, text=True, timeout=20)
        return float(p.stdout.strip())
    except Exception:
        return -1.0

retry = {}
for b in ["b1", "b2", "b3", "b4"]:
    spec = importlib.util.spec_from_file_location(
        "gb_%s_res" % b, os.path.join(WORK, "gen_bootcamp_%s.py" % b))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    missing = []
    for v in mod.VIDEOS:
        f = v["file"]
        mp = os.path.join(VIDDIR, f)
        base, _ = os.path.splitext(mp)
        need = False
        reason = ""
        if not os.path.exists(mp):
            need, reason = True, "missing"
        else:
            d = duration(mp)
            if d < 29.0:
                need, reason = True, "partial dur=%.1f" % d
                os.remove(mp)  # incomplete file from this recovery; re-render
            elif not os.path.exists(base + ".vtt"):
                need, reason = True, "no vtt"
            elif not os.path.exists(base + ".narration.md"):
                need, reason = True, "no narration"
        if need:
            missing.append((f, reason))
            print("%s: %s (%s)" % (b, f, reason))
    retry[b] = missing
    print("=== %s needs %d re-renders" % (b, len(missing)))

total = sum(len(v) for v in retry.values())
print("TOTAL to re-render:", total)
json.dump({b: [f for f, _ in v] for b, v in retry.items()},
          open(os.path.join(WORK, "b1b4-resume-list.json"), "w"), indent=1)
