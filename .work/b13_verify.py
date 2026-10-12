#!/usr/bin/env python3
"""B13 CDN verify: 18 files (6 mp4 + 6 vtt + 6 narration.md) via browser-UA GET-range."""
import subprocess

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
BASE = "https://interstitiumlabs.dev/assets/videos/"
NAMES = [
    "bc-bbg-rl-skill-mapping",
    "bc-fireship-rl-role-ladder",
    "bc-story-rl-pivot",
    "bc-primer-sp-spaced-repetition",
    "bc-3b1b-sp-forgetting-curve",
    "bc-bbg-sp-active-recall",
]
FILES = []
for n in NAMES:
    FILES += ["%s.mp4" % n, "%s.vtt" % n, "%s.narration.md" % n]
ok, bad = [], []
for f in FILES:
    url = BASE + f
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                        "-A", UA, "-r", "0-1023", "--max-time", "30", url],
                       capture_output=True, text=True)
    code = (r.stdout or "").strip()
    if code == "206" or code == "200":
        ok.append((f, code))
    else:
        bad.append((f, code))
    print("%s -> %s" % (f, code), flush=True)
print("== OK: %d  BAD: %d" % (len(ok), len(bad)), flush=True)
with open("/home/hatch/workspace/apex-audit/.work/b13-verify-results.txt", "w") as fh:
    fh.write("ok=%d bad=%d\n" % (len(ok), len(bad)))
    for f, c in ok:
        fh.write("OK %s %s\n" % (f, c))
    for f, c in bad:
        fh.write("BAD %s %s\n" % (f, c))
