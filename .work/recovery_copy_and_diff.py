#!/usr/bin/env python3
"""Run-9 recovery: copy /tmp/b1b4-staging/* into docs/assets/videos/,
then cross-check the 126 B1-B4 files (from gen script VIDEOS registries)
for mp4 + vtt + narration.md. Writes recovery-missing-diff.json."""
import importlib.util, json, os, shutil

WORK = os.path.expanduser("~/workspace/apex-audit/.work")
VIDDIR = os.path.expanduser("~/workspace/apex-audit/docs/assets/videos")
STAGE = "/tmp/b1b4-staging"

# 1. copy staged files
copied = 0
for f in sorted(os.listdir(STAGE)):
    src = os.path.join(STAGE, f)
    dst = os.path.join(VIDDIR, f)
    if os.path.isfile(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        copied += 1
print("copied from staging: %d" % copied)

# 2. build 126-file list from gen registries
existing = set(os.listdir(VIDDIR))
result = {}
total_files = []
for b in ["b1", "b2", "b3", "b4"]:
    path = os.path.join(WORK, "gen_bootcamp_%s.py" % b)
    spec = importlib.util.spec_from_file_location("gb_%s" % b, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    files = [v["file"] for v in mod.VIDEOS]
    total_files += [(b, f) for f in files]
    missing_mp4, missing_vtt, missing_nar = [], [], []
    for f in files:
        base = os.path.splitext(f)[0]
        if f not in existing:
            missing_mp4.append(f)
        if base + ".vtt" not in existing:
            missing_vtt.append(base + ".vtt")
        if base + ".narration.md" not in existing:
            missing_nar.append(base + ".narration.md")
    result[b] = {
        "total": len(files),
        "missing_mp4": missing_mp4,
        "missing_vtt": missing_vtt,
        "missing_narration": missing_nar,
    }
    print("== %s: %d total | missing mp4=%d vtt=%d narration=%d" % (
        b, len(files), len(missing_mp4), len(missing_vtt), len(missing_nar)))
    for f in missing_mp4:
        print("  MISSING mp4", f)

print("TOTAL B1-B4 files:", len(total_files))
assert len(total_files) == 126, "expected 126, got %d" % len(total_files)
json.dump(result, open(os.path.join(WORK, "recovery-missing-diff.json"), "w"), indent=1)
print("wrote recovery-missing-diff.json")
