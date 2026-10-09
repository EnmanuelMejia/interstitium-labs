#!/usr/bin/env python3
"""Verify all 108 B11 files HTTP 200 via browser-UA GET-range probes."""
import sys, urllib.request
sys.path.insert(0, "/home/hatch/workspace/apex-audit/.work")
import gen_bootcamp_b11 as G

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
BASE = "https://interstitiumlabs.dev/assets/videos/"

def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-1023"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return "ERR:%r" % e

bad, total = [], 0
for v in G.VIDEOS:
    f = v["file"]
    base = f.rsplit(".", 1)[0]
    for path in (f, base + ".vtt", base + ".narration.md"):
        total += 1
        s = check(BASE + path)
        if s != 200 and s != 206:
            bad.append((path, s))
        print("%s %s" % (s, path), flush=True)
print("== verified=%d/%d bad=%d" % (total - len(bad), total, len(bad)))
for b in bad: print("BAD", b)
