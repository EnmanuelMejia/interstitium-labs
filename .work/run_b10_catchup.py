#!/usr/bin/env python3
"""Batch B10 catch-up: re-render only the remaining 6 files with 300s timeout guard."""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
REMAINING = [
    "bc-primer-vc-secrets.mp4",
    "bc-fireship-vc-policy.mp4",
    "bc-bbg-vc-mesh.mp4",
    "bc-story-fsd-day.mp4",
    "bc-bbg-fsd-ticket.mp4",
    "bc-primer-fsd-standup.mp4",
]
failed = []
for f in REMAINING:
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
