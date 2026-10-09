#!/usr/bin/env python3
"""Run gen_bootcamp_b10.py per-video with a 300s timeout guard (Batch B10 full batch).
Logs DONE/FAILED/TIMEOUT per file; exit nonzero if any failed."""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_bootcamp_b10 as G

failed = []
for v in G.VIDEOS:
    f = v["file"]
    print("BATCH-START", f, flush=True)
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, "gen_bootcamp_b10.py"), f],
                           timeout=300, cwd=HERE, capture_output=True, text=True)
        done = [l for l in r.stdout.splitlines() if l.startswith("DONE ")]
        failed_flag = [l for l in r.stdout.splitlines() if l.startswith("FAILED ")]
        if r.returncode == 0 and done and not failed_flag:
            print("BATCH-OK", done[0], flush=True)
        else:
            print("BATCH-FAIL %s rc=%s tail=%s" % (f, r.returncode,
                  (r.stdout + r.stderr)[-300:]), flush=True)
            failed.append(f)
    except subprocess.TimeoutExpired:
        print("BATCH-TIMEOUT", f, flush=True)
        failed.append(f)
print("BATCH-SUMMARY failed=%d: %s" % (len(failed), failed), flush=True)
sys.exit(1 if failed else 0)
