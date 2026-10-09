#!/usr/bin/env python3
"""Verify all 108 Batch B8 files return HTTP 200 at the CDN (browser UA)."""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bootcamp_b8 as G

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
BASE = "https://interstitiumlabs.dev/assets/videos/"
ok_files = []
bad_files = []
for v in G.VIDEOS:
    b = os.path.splitext(v["file"])[0]
    for f in (v["file"], b + ".vtt", b + ".narration.md"):
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "-A", UA, "-r", "0-1023", "--max-time", "25", BASE + f],
            capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200":
            ok_files.append(f)
        else:
            bad_files.append((f, code))
print("OK: %d / %d" % (len(ok_files), len(ok_files) + len(bad_files)))
for f, c in bad_files:
    print("BAD", f, c)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "b8-verify-results.txt"), "w") as fh:
    fh.write("ok %d bad %d\n" % (len(ok_files), len(bad_files)))
    for f, c in bad_files:
        fh.write("BAD %s %s\n" % (f, c))
