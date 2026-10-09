#!/usr/bin/env python3
"""Verify all 108 B10 files return HTTP 200 on the CDN (browser-UA GET-range probes).
Writes results to b10-verify-results.txt."""
import os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_bootcamp_b10 as G

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
BASE = "https://interstitiumlabs.dev/assets/videos/"

files = []
for v in G.VIDEOS:
    f = v["file"]
    base = f[:-4]
    files += [f, base + ".vtt", base + ".narration.md"]

results = []
for f in files:
    try:
        req = urllib.request.Request(BASE + f,
                                     headers={"User-Agent": UA, "Range": "bytes=0-1023"})
        resp = urllib.request.urlopen(req, timeout=30)
        code = resp.getcode()
        n = len(resp.read())
        ok = code in (200, 206) and n > 0
        results.append((f, code, "OK" if ok else "EMPTY"))
    except Exception as e:
        results.append((f, "ERR", repr(e)[:80]))

bad = [r for r in results if r[2] != "OK"]
out = os.path.join(HERE, "b10-verify-results.txt")
with open(out, "w") as fh:
    for f, code, st in results:
        fh.write("%s %s %s\n" % (st, code, f))
    fh.write("SUMMARY: %d/%d OK\n" % (len(results) - len(bad), len(results)))
print("SUMMARY: %d/%d OK" % (len(results) - len(bad), len(results)))
for r in bad[:10]:
    print("BAD:", r)
sys.exit(1 if bad else 0)
