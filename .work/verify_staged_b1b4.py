#!/usr/bin/env python3
"""Final verification of staged B1-B4 recovery files:
- every registry MP4 exists in staging, ffprobe: h264, 1280x720, duration 29-31s
- .vtt and .narration.md companions present
- also verify the 9 files already in the videos dir (1 B1 + 8 B2) are intact
Prints per-batch counts; exits 1 on any failure."""
import importlib.util, os, subprocess, sys, json

WORK = os.path.expanduser("~/workspace/apex-audit/.work")
STAGING = "/tmp/b1b4-staging"
VIDDIR = os.path.join(WORK, "..", "docs", "assets", "videos")

def probe(path):
    try:
        p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=codec_name,width,height",
                            "-show_entries", "format=duration",
                            "-of", "json", path],
                           capture_output=True, text=True, timeout=30)
        j = json.loads(p.stdout)
        s = j["streams"][0]; d = float(j["format"]["duration"])
        return s["codec_name"], int(s["width"]), int(s["height"]), d
    except Exception as e:
        return None

bad = []
totals = {}
for b in ["b1", "b2", "b3", "b4"]:
    spec = importlib.util.spec_from_file_location("gv_%s" % b,
        os.path.join(WORK, "gen_bootcamp_%s.py" % b))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ok = 0
    for v in mod.VIDEOS:
        f = v["file"]; base = os.path.splitext(f)[0]
        # prefer staged copy; fall back to videos-dir copy (the 9 pre-existing)
        mp = os.path.join(STAGING, f)
        if not os.path.exists(mp):
            mp = os.path.join(VIDDIR, f)
        r = probe(mp) if os.path.exists(mp) else None
        problems = []
        if r is None:
            problems.append("missing/unreadable")
        else:
            c, w, h, d = r
            if c != "h264": problems.append("codec=%s" % c)
            if (w, h) != (1280, 720): problems.append("res=%dx%d" % (w, h))
            if not (29.0 <= d <= 31.0): problems.append("dur=%.1f" % d)
        # companions: check wherever the mp4 lives
        loc = STAGING if os.path.exists(os.path.join(STAGING, f)) else VIDDIR
        if not os.path.exists(os.path.join(loc, base + ".vtt")):
            problems.append("no .vtt")
        if not os.path.exists(os.path.join(loc, base + ".narration.md")):
            problems.append("no .narration.md")
        if problems:
            bad.append((b, f, ";".join(problems)))
        else:
            ok += 1
    totals[b] = (ok, len(mod.VIDEOS))
    print("%s: %d/%d fully verified" % (b, ok, len(mod.VIDEOS)))

if bad:
    print("BAD FILES:")
    for b, f, p in bad:
        print("  %s %s: %s" % (b, f, p))
    sys.exit(1)
print("ALL %d FILES VERIFIED OK" % sum(t[0] for t in totals.values()))
