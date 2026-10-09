import importlib.util, os, sys, json

VIDDIR = os.path.expanduser("~/workspace/apex-audit/.work/../docs/assets/videos")
WORK = os.path.expanduser("~/workspace/apex-audit/.work")

existing = set(os.listdir(VIDDIR))
result = {}
for b in ["b1", "b2", "b3", "b4"]:
    path = os.path.join(WORK, "gen_bootcamp_%s.py" % b)
    spec = importlib.util.spec_from_file_location("gb_%s" % b, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    files = [v["file"] for v in mod.VIDEOS]
    missing = [f for f in files if f not in existing]
    missing_vtt = [f for f in files if (os.path.splitext(f)[0] + ".vtt") not in existing]
    missing_nar = [f for f in files if (os.path.splitext(f)[0] + ".narration.md") not in existing]
    result[b] = {
        "total": len(files),
        "missing_mp4": missing,
        "missing_vtt": missing_vtt,
        "missing_narration": missing_nar,
    }
    print("=== %s: %d total, %d missing mp4, %d missing vtt, %d missing narration" % (
        b, len(files), len(missing), len(missing_vtt), len(missing_nar)))
    for f in missing:
        print("  MISSING", f)

# also list bc-* files that currently exist (to show what survived)
bc = sorted(f for f in existing if f.startswith("bc-") and f.endswith(".mp4"))
print("EXISTING bc-*.mp4 count:", len(bc))
for f in bc:
    print("  HAVE", f)

json.dump(result, open(os.path.join(WORK, "b1b4-missing-diff.json"), "w"), indent=1)
print("wrote b1b4-missing-diff.json")
