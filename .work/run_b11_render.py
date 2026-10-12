#!/usr/bin/env python3
"""Batch B11 full render: one timeout-guarded single-file run per video."""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_bootcamp_b11 as G

OUT = "/home/hatch/workspace/apex-audit/docs/assets/videos"
ok, failed = [], []
for v in G.VIDEOS:
    f = v["file"]
    path = os.path.join(OUT, f)
    r = subprocess.run(
        ["timeout", "300", "python3", os.path.join(HERE, "gen_bootcamp_b11.py"), f],
        capture_output=True, text=True, timeout=320)
    tail = r.stdout.strip().splitlines()[-2:] if r.stdout.strip() else []
    print("EXIT=%d %s :: %s" % (r.returncode, f, " | ".join(tail)), flush=True)
    if r.returncode == 0 and os.path.exists(path):
        ok.append(f)
    else:
        failed.append(f)
        print("STDERR tail:", (r.stderr or "")[-400:], flush=True)
print("== SUMMARY: ok=%d failed=%d" % (len(ok), len(failed)))
print("FAILED:", failed)
