#!/usr/bin/env python3
"""B13 full-batch runner: render each video with a 300s per-file timeout."""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["bc-bbg-sp-active-recall.mp4"]
ok, failed = [], []
for f in FILES:
    cmd = ["timeout", "300", "python3", os.path.join(HERE, "gen_bootcamp_b13.py"), f]
    try:
        p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
        tail = [l for l in (p.stdout or "").splitlines() if l.startswith("DONE")]
        status = "EXIT=%d %s :: %s" % (p.returncode, f, " | ".join(tail) if tail else "NO DONE LINE")
        print(status, flush=True)
        if p.returncode == 0 and tail:
            ok.append(f)
        else:
            failed.append(f)
            print((p.stderr or "")[-2000:], flush=True)
    except Exception as e:
        failed.append(f)
        print("EXC %s: %r" % (f, e), flush=True)
print("== SUMMARY: ok=%d failed=%d" % (len(ok), len(failed)), flush=True)
print("FAILED:", failed, flush=True)
