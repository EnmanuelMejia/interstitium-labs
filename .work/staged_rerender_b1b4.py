#!/usr/bin/env python3
"""Staged recovery driver: render the 117 missing B1-B4 videos into
/tmp/b1b4-staging (away from the videos-dir deleter), one subprocess per
video with a 300s timeout. Skips files already staged (>1KB)."""
import json, os, subprocess, sys, time

WORK = os.path.expanduser("~/workspace/apex-audit/.work")
STAGING = "/tmp/b1b4-staging"
os.makedirs(STAGING, exist_ok=True)
LOG = os.path.join(WORK, "b1b4-staged-rerender.log")

retry = json.load(open(os.path.join(WORK, "b1b4-resume-list.json")))
logf = open(LOG, "w")

def log(msg):
    print(msg, flush=True)
    logf.write(msg + "\n"); logf.flush()

t0 = time.time()
ok, failed, timeout = [], [], []
for b in ["b1", "b2", "b3", "b4"]:
    for fname in retry[b]:
        staged = os.path.join(STAGING, fname)
        if os.path.exists(staged) and os.path.getsize(staged) > 1000:
            log("SKIP (staged): %s" % fname)
            continue
        log("START %s (%s)" % (fname, b))
        try:
            p = subprocess.run(
                [sys.executable, os.path.join(WORK, "render_one_staged.py"), b, fname],
                capture_output=True, text=True, timeout=300, cwd=WORK)
            tail = ((p.stdout or "") + (p.stderr or ""))[-400:]
            if p.returncode == 0 and os.path.exists(staged) and os.path.getsize(staged) > 1000:
                ok.append(fname); log("DONE %s" % fname)
            else:
                failed.append(fname); log("FAILED %s rc=%d tail=%s" % (fname, p.returncode, tail[-200:]))
        except subprocess.TimeoutExpired:
            timeout.append(fname); log("TIMEOUT %s" % fname)

logf.close()
dt = time.time() - t0
print("SUMMARY ok=%d failed=%d timeout=%d elapsed=%.1fs" % (len(ok), len(failed), len(timeout), dt))
for f in failed: print("FAILED:", f)
for f in timeout: print("TIMEOUT:", f)
json.dump({"ok": ok, "failed": failed, "timeout": timeout, "elapsed_s": dt},
          open(os.path.join(WORK, "b1b4-staged-results.json"), "w"), indent=1)
