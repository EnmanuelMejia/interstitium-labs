#!/usr/bin/env python3
"""Retry ERR urls with curl, sequentially (no threads)."""
import json, subprocess

RES = "/home/hatch/workspace/apex-audit/.work/url-check-results.json"
OUT = "/home/hatch/workspace/apex-audit/.work/url-retry-results.json"

r = json.load(open(RES))
todo = [x for x in r if x["http"] == "ERR"]
print(len(todo), "to retry")

out = []
for i, x in enumerate(todo):
    url = x["url"]
    try:
        p = subprocess.run(
            ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code} %{url_effective}",
             "-L", "--max-time", "25", "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36", url],
            capture_output=True, text=True, timeout=40)
        code = (p.stdout.strip().split(" ")[0] if p.stdout.strip() else "000")
        final = p.stdout.strip().split(" ", 1)[1] if " " in p.stdout.strip() else url
        out.append({"url": url, "http": code, "final": final, "course": x["course"], "label": x["label"]})
    except Exception as e:
        out.append({"url": url, "http": "ERR", "final": url, "course": x["course"], "label": x["label"], "err": repr(e)[:100]})
    if (i + 1) % 10 == 0:
        print(f"  {i+1}/{len(todo)}", flush=True)

json.dump(out, open(OUT, "w"), indent=1)
from collections import Counter
print(Counter(v["http"] for v in out))
for v in out:
    if v["http"] not in ("200", "206"):
        print(f"  [{v['http']}] {v['course']} :: {v['label'][:45]} :: {v['url'][:80]}")
print("wrote", OUT)
