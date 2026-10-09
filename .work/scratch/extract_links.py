#!/usr/bin/env python3
"""Extract href/src links from docs/**/*.html with source page attribution.
Outputs to a durable scratch dir."""
import os, re, json
from urllib.parse import urljoin

SCRATCH = os.path.expanduser("~/workspace/apex-audit/.work/scratch")
os.makedirs(SCRATCH, exist_ok=True)
DOCS = os.path.expanduser("~/workspace/apex-audit/docs")
BASE = "https://interstitiumlabs.dev"
HOST = "interstitiumlabs.dev"
OUT_INT = os.path.join(SCRATCH, "links-internal.jsonl")
OUT_EXT = os.path.join(SCRATCH, "links-external.jsonl")

pat = re.compile(r'''(?:href|src)\s*=\s*["']([^"'#<>]+)["']''', re.I)

internal, external = [], []

def resolve(raw, page_path):
    rel = os.path.relpath(page_path, DOCS)
    if rel.endswith("index.html"):
        page_url = BASE + "/" + os.path.dirname(rel).rstrip("/") + "/"
        page_url = page_url.replace("//", "/", 1).replace("https:/", "https://")
    else:
        page_url = BASE + "/" + rel
    return urljoin(page_url, raw)

for root, dirs, files in os.walk(DOCS):
    for f in files:
        if not f.endswith(".html"):
            continue
        p = os.path.join(root, f)
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                html = fh.read()
        except Exception:
            continue
        src = os.path.relpath(p, DOCS)
        for m in pat.finditer(html):
            raw = m.group(1).strip()
            if not raw:
                continue
            low = raw.lower()
            if low.startswith(("mailto:", "tel:", "javascript:", "data:", "blob:", "sms:")):
                continue
            if raw.startswith("#"):
                continue
            if low.startswith("http://") or low.startswith("https://"):
                host = re.sub(r"^https?://", "", low).split("/")[0].split("?")[0]
                if host == HOST or host == "www." + HOST:
                    internal.append((raw.split("#")[0], src))
                else:
                    external.append((raw.split("#")[0], src))
            else:
                full = resolve(raw, p).split("#")[0]
                internal.append((full, src))

def dump(pairs, path):
    seen = {}
    for u, s in pairs:
        if u not in seen:
            seen[u] = s
    with open(path, "w") as fh:
        for u, s in sorted(seen.items()):
            fh.write(json.dumps({"url": u, "source": s}) + "\n")
    return len(seen)

print("internal:", dump(internal, OUT_INT), "external:", dump(external, OUT_EXT))
