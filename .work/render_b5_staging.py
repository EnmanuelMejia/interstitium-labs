#!/usr/bin/env python3
"""Render remaining B5 videos to a staging dir (safe from the videos-dir deleter).
Skips videos already present in staging. Run: python3 render_b5_staging.py"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
STAGING = "/tmp/b5-staging"

import gen_bootcamp_b5 as B5
B5.OUT = STAGING  # redirect output away from the deleter-targeted videos dir

only = sys.argv[1:] or None
todo = []
for v in B5.VIDEOS:
    if only and v["file"] not in only and v["file"].replace(".mp4", "") not in only:
        continue
    mp4 = os.path.join(STAGING, v["file"])
    if os.path.exists(mp4) and os.path.getsize(mp4) > 1000:
        print("SKIP (staged):", v["file"], flush=True)
        continue
    todo.append(v)

print("Rendering %d videos to %s" % (len(todo), STAGING), flush=True)
for v in todo:
    print("START", v["file"], flush=True)
    try:
        B5.render_video(v)
    except Exception as e:
        print("FAILED %s: %r" % (v["file"], e), flush=True)
print("STAGING RENDER COMPLETE", flush=True)
