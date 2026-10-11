#!/usr/bin/env python3
"""Run-9: curl-verify all 126 B1-B4 files (mp4+vtt+narration.md) return 200.
Uses browser UA + GET-range (bare-Python-UA HEAD gets Cloudflare 403).
Writes .work/run9-verify-results.json."""
import importlib.util, json, os, subprocess

WORK = os.path.expanduser("~/workspace/apex-audit/.work")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")

def check(url):
    p = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-r", "0-0", "-A", UA, "--max-time", "20", url],
        capture_output=True, text=True)
    return p.stdout.strip()

results = {"ok": [], "non200": {}}
total = 0
for b in ["b1", "b2", "b3", "b4"]:
    path = os.path.join(WORK, "gen_bootcamp_%s.py" % b)
    spec = importlib.util.spec_from_file_location("gv_%s" % b, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for v in mod.VIDEOS:
        stem = os.path.splitext(v["file"])[0]
        for ext in (".mp4", ".vtt", ".narration.md"):
            fn = stem + ext
            total += 1
            url = "https://interstitiumlabs.dev/assets/videos/" + fn
            code = check(url)
            if code == "200":
                results["ok"].append(fn)
            else:
                results["non200"][fn] = code

print("checked %d urls, 200=%d, non200=%d" % (
    total, len(results["ok"]), len(results["non200"])))
for fn, code in results["non200"].items():
    print("  %s -> %s" % (fn, code))
json.dump(results, open(os.path.join(WORK, "run9-verify-results.json"), "w"), indent=1)
