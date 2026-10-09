#!/usr/bin/env python3
"""Re-render missing B1-B4 bootcamp videos, one subprocess per video, each
guarded by a 300s timeout so a single hang cannot stall the batch.
Filenames restricted to the B1-B4 registries (bc-* only). Never touches
sibling-builder output."""
import json, os, subprocess, sys, time

WORK = os.path.expanduser("~/workspace/apex-audit/.work")
LOG = os.path.join(WORK, "b1b4-rerender.log")

diff = json.load(open(os.path.join(WORK, "b1b4-missing-diff.json")))
t0 = time.time()
results = {"ok": [], "failed": [], "timeout": []}
logf = open(LOG, "a")

def log(msg):
    print(msg, flush=True)
    logf.write(msg + "\n"); logf.flush()

for b in ["b1", "b2", "b3", "b4"]:
    script = os.path.join(WORK, "gen_bootcamp_%s.py" % b)
    for fname in diff[b]["missing_mp4"]:
        base = fname if fname.endswith(".mp4") else fname + ".mp4"
        # re-check: sibling builders only render their own bc-* names, but be safe
        out = os.path.join(WORK, "..", "docs", "assets", "videos", base)
        if os.path.exists(out) and os.path.getsize(out) > 0:
            log("SKIP (already present): %s" % base)
            continue
        log("START %s (%s)" % (base, b))
        try:
            p = subprocess.run(
                [sys.executable, script, base],
                capture_output=True, text=True, timeout=300, cwd=WORK,
            )
            tail = (p.stdout or "")[-800:]
            if p.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 0:
                results["ok"].append(base)
                log("DONE %s" % base)
            else:
                results["failed"].append(base)
                log("FAILED %s rc=%d tail=%s" % (base, p.returncode, tail[-300:]))
        except subprocess.TimeoutExpired:
            results["timeout"].append(base)
            log("TIMEOUT %s (300s)" % base)

logf.close()
dt = time.time() - t0
print("SUMMARY ok=%d failed=%d timeout=%d elapsed=%.1fs" % (
    len(results["ok"]), len(results["failed"]), len(results["timeout"]), dt))
if results["failed"]:
    print("FAILED:", " ".join(results["failed"]))
if results["timeout"]:
    print("TIMEOUT:", " ".join(results["timeout"]))
json.dump({"results": results, "elapsed_s": dt},
          open(os.path.join(WORK, "b1b4-rerender-results.json"), "w"), indent=1)
