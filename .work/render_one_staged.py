#!/usr/bin/env python3
"""Render ONE bootcamp video to the staging dir (safe from the videos-dir deleter).
Usage: render_one_staged.py <b1|b2|b3|b4> <filename.mp4>"""
import importlib.util, os, sys

STAGING = "/tmp/b1b4-staging"
os.makedirs(STAGING, exist_ok=True)
WORK = os.path.expanduser("~/workspace/apex-audit/.work")

batch, fname = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location(
    "gb_%s_st" % batch, os.path.join(WORK, "gen_bootcamp_%s.py" % batch))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.OUT = STAGING  # redirect away from the deleter-targeted videos dir

vids = [v for v in mod.VIDEOS if v["file"] == fname or v["file"].replace(".mp4", "") == fname]
if not vids:
    print("NOT FOUND in registry: %s" % fname, flush=True)
    sys.exit(2)
for v in vids:
    print("START", v["file"], flush=True)
    try:
        mod.render_video(v)
    except Exception as e:
        print("FAILED %s: %r" % (v["file"], e), flush=True)
        sys.exit(1)
