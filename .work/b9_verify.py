#!/usr/bin/env python3
"""Verify all B9 files return HTTP 200 with a browser User-Agent (separate ok/bad lists)."""
import sys, os, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_bootcamp_b9 as G

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
ok, bad = [], []

urls = []
for v in G.VIDEOS:
    base = v["file"][:-4]
    urls += ["/assets/videos/" + v["file"], "/assets/videos/" + base + ".vtt",
             "/assets/videos/" + base + ".narration.md"]

def probe(path):
    url = "https://interstitiumlabs.dev" + path
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    req.add_header("Range", "bytes=0-0")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return "ERR:" + repr(e)

import urllib.error
for u in urls:
    s = probe(u)
    (ok if s == 200 or s == 206 else bad).append((u, s))
    if len(ok) + len(bad) in (27, 54, 81, 108):
        print("%d/%d checked..." % (len(ok) + len(bad), len(urls)), flush=True)

print("OK:", len(ok), "BAD:", len(bad))
for u, s in bad:
    print("BAD", s, u)
out = os.path.join(HERE, "b9-verify-results.txt")
with open(out, "w") as f:
    f.write("ok=%d bad=%d\n" % (len(ok), len(bad)))
    for u, s in bad:
        f.write("BAD %s %s\n" % (s, u))
print("results ->", out)
