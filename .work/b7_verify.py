#!/usr/bin/env python3
"""Verify all 108 Batch B7 files return HTTP 200 at the CDN with a browser UA.
Avoids the B6 list-aliasing bug: ok_list and bad_list are separate lists."""
import sys, subprocess
sys.path.insert(0, '/home/hatch/workspace/apex-audit/.work')
import gen_bootcamp_b7 as G

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
BASE = "https://interstitiumlabs.dev/assets/videos/"

urls = []
for v in G.VIDEOS:
    base = "/assets/videos/" + v["file"].replace(".mp4", "")
    urls.append(BASE + v["file"])
    urls.append("https://interstitiumlabs.dev" + base + ".vtt")
    urls.append("https://interstitiumlabs.dev" + base + ".narration.md")

ok_list = []
bad_list = []
for u in urls:
    p = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-A", UA, "-r", "0-1023", "--max-time", "30", u],
        capture_output=True, text=True)
    code = p.stdout.strip()
    if code == "200":
        ok_list.append(u)
    else:
        bad_list.append((u, code))

print("ok=%d bad=%d total=%d" % (len(ok_list), len(bad_list), len(urls)))
for u, c in bad_list:
    print("BAD", c, u)
with open("/home/hatch/workspace/apex-audit/.work/b7-verify-results.txt", "w") as f:
    f.write("ok=%d bad=%d total=%d\n" % (len(ok_list), len(bad_list), len(urls)))
    for u, c in bad_list:
        f.write("BAD %s %s\n" % (c, u))
