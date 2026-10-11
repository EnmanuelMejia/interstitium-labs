#!/usr/bin/env python3
"""Run-9 recovery renderer: re-render missing B1-B4 bootcamp files
(mp4+vtt+narration per file), one subprocess per video, 300s guard.
Logs to .work/run9-render.log; results to .work/run9-render-results.json."""
import json, os, subprocess, sys, time

WORK = os.path.expanduser("~/workspace/apex-audit/.work")
VIDDIR = os.path.join(WORK, "..", "docs", "assets", "videos")
LOG = os.path.join(WORK, "run9-render.log")

diff = json.load(open(os.path.join(WORK, "recovery-missing-diff.json")))

# full list to render: mp4 per missing-mp4, plus b1 sidecar-only gap
jobs = []
for b in ["b1", "b2", "b3", "b4"]:
    for f in diff[b]["missing_mp4"]:
        jobs.append((b, f))
# b1 sidecar-only gap: re-render the file to regenerate sidecars
if diff["b1"]["missing_vtt"] or diff["b1"]["missing_narration"]:
    base = "bc-3b1b-theory-exponential-blowup.mp4"
    jobs.insert(0, ("b1", base))
print("jobs:", len(jobs))

t0 = time.time()
results = {"ok": [], "failed": [], "timeout": []}
logf = open(LOG, "w")

def log(msg):
    print(msg, flush=True)
    logf.write(msg + "\n"); logf.flush()

for b, base in jobs:
    out = os.path.join(VIDDIR, base)
    stem = os.path.splitext(base)[0]
    want = {base, stem + ".vtt", stem + ".narration.md"}
    script = os.path.join(WORK, "gen_bootcamp_%s.py" % b)
    log("START %s (%s)" % (base, b))
    try:
        p = subprocess.run(
            [sys.executable, script, base],
            capture_output=True, text=True, timeout=300, cwd=WORK)
        got = {f for f in want if os.path.exists(os.path.join(VIDDIR, f))
               and os.path.getsize(os.path.join(VIDDIR, f)) > 0}
        if p.returncode == 0 and got == want:
            results["ok"].append(base)
            log("DONE %s" % base)
        else:
            results["failed"].append(base)
            log("FAILED %s rc=%d have=%s tail=%s" % (
                base, p.returncode, sorted(got), ((p.stdout or "")[-300:])))
    except subprocess.TimeoutExpired:
        results["timeout"].append(base)
        log("TIMEOUT %s (300s)" % base)

dt = time.time() - t0
log("SUMMARY ok=%d failed=%d timeout=%d elapsed=%.1fs" % (
    len(results["ok"]), len(results["failed"]), len(results["timeout"]), dt))
if results["failed"]:
    log("FAILED: " + " ".join(results["failed"]))
if results["timeout"]:
    log("TIMEOUT: " + " ".join(results["timeout"]))
logf.close()
json.dump({"results": results, "elapsed_s": dt},
          open(os.path.join(WORK, "run9-render-results.json"), "w"), indent=1)
