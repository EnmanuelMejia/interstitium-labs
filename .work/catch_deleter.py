#!/usr/bin/env python3
"""Catch the bc-*.mp4 deleter: create bait, poll fast, dump process table on deletion."""
import os, time, subprocess, datetime

VIDDIR = "/home/hatch/workspace/apex-audit/docs/assets/videos"
BAIT = os.path.join(VIDDIR, "bc-honeypot-delete-me.mp4")

with open(BAIT, "w") as f:
    f.write("honeypot")
print("bait created at", datetime.datetime.now().strftime("%H:%M:%S"), flush=True)

def ps_dump():
    out = subprocess.run(["ps", "-eo", "pid,lstart,cmd"], capture_output=True, text=True).stdout
    return out

# baseline
before = ps_dump()
start = time.time()
deleted_at = None
while time.time() - start < 300:
    if not os.path.exists(BAIT):
        deleted_at = datetime.datetime.now().strftime("%H:%M:%S")
        break
    time.sleep(0.5)

if deleted_at:
    print("DELETED at", deleted_at, flush=True)
    after = ps_dump()
    # show processes that are new or python-related
    before_pids = set(l.split()[0] for l in before.strip().split("\n")[1:])
    print("--- processes NOT in baseline (new since bait creation):", flush=True)
    for l in after.strip().split("\n")[1:]:
        pid = l.split()[0]
        if pid not in before_pids:
            print(l[:200], flush=True)
    print("--- all python3 processes at deletion:", flush=True)
    for l in after.strip().split("\n")[1:]:
        if "python3" in l:
            print(l[:200], flush=True)
else:
    print("bait survived 300s", flush=True)
    os.remove(BAIT)
