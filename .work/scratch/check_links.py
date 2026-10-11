#!/usr/bin/env python3
"""Numbered parallel link checker with STREAMING output (restart-safe).
Input jsonl: url, source. Appends results to OUT as they arrive, keyed by idx.
Safe to re-run: skips indices already present in OUT.
Usage: check_links.py IN.jsonl OUT.jsonl
Env: CHECKERS (default 24), CURL_TIMEOUT (default 20)."""
import json, subprocess, sys, os

IN = sys.argv[1]
OUT = sys.argv[2]
WORKERS = int(os.environ.get("CHECKERS", "24"))
TIMEOUT = os.environ.get("CURL_TIMEOUT", "20")
SCRATCH = os.path.expanduser("~/workspace/apex-audit/.work/scratch")

entries = []
with open(IN) as fh:
    for line in fh:
        line = line.strip()
        if line:
            entries.append(json.loads(line))
dedup = {}
for e in entries:
    dedup.setdefault(e["url"], e)
entries = sorted(dedup.values(), key=lambda e: e["url"])

done_idx = set()
if os.path.exists(OUT):
    with open(OUT) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    done_idx.add(json.loads(line)["idx"])
                except Exception:
                    pass

todo = [(i, e) for i, e in enumerate(entries) if i not in done_idx]
print(f"total {len(entries)}, already done {len(done_idx)}, to check {len(todo)}", flush=True)
if not todo:
    sys.exit(0)

inp = os.path.join(SCRATCH, "chk_in_" + os.path.basename(OUT) + ".txt")
with open(inp, "w") as fh:
    for i, e in todo:
        fh.write(f"{i}\t{e['url']}\n")

sh = ("idx=${1%%$'\\t'*}; u=${1#*$'\\t'}; "
      f"r=$(curl -s -o /dev/null -L --max-time {TIMEOUT} -A 'Mozilla/5.0 (link-audit)' "
      "-w '%{http_code} %{url_effective}' \"$u\" 2>&1); "
      "printf '%s\\t%s\\n' \"$idx\" \"$r\"")

proc = subprocess.Popen(
    ["xargs", "-a", inp, "-d", "\n", "-P", str(WORKERS), "-I@",
     "bash", "-c", sh, "_", "@"],
    stdout=subprocess.PIPE, text=True, bufsize=1)

by_idx = {i: e for i, e in todo}
n = 0
with open(OUT, "a") as outfh:
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            idx_s, rest = line.split("\t", 1)
            idx = int(idx_s)
            parts = rest.split(" ", 1)
            code = parts[0]
            final = parts[1] if len(parts) > 1 else ""
        except Exception:
            continue
        e = by_idx.get(idx)
        if e is None:
            continue
        outfh.write(json.dumps({
            "idx": idx, "url": e["url"], "status": code, "final": final,
            "source": e.get("source", ""), "host": e.get("host", "")
        }) + "\n")
        outfh.flush()
        n += 1
        if n % 50 == 0:
            print(f"... {n}/{len(todo)}", flush=True)
proc.wait()
print(f"done: wrote {n} results", flush=True)
