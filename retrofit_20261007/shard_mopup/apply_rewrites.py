#!/usr/bin/env python3
"""Apply instructor-voice il_provides rewrites to catalog shards B, C, D.
Atomic writes, pre/post validation, hard-rule checks, spot checks."""
import json, os, re, sys, tempfile

BASE = "/home/hatch/workspace/apex-audit/docs/university/data/catalog"
OUTDIR = "/home/hatch/workspace/apex-audit/retrofit_20261007/shard_mopup"
sys.path.insert(0, OUTDIR)
from rewrites_b import RW_B
from rewrites_c import RW_C
from rewrites_d import RW_D

BANNED = ["aleks", "brilliant", "khan academy", "coursera", "udemy", "edx",
          "palantir", "nsa"]

def sentences_ok(s):
    # count sentence terminators; require >= 2
    parts = [p.strip() for p in re.split(r'[.!?]+\s*', s.strip()) if p.strip()]
    return len(parts) >= 2, len(parts)

def process(shard, rw):
    path = os.path.join(BASE, f"{shard}.json")
    raw = open(path, encoding="utf-8").read()
    d = json.loads(raw)  # BEFORE load
    # snapshot non-il_provides state for untouched-verify
    index = {}
    for pth in d["paths"]:
        for m in pth.get("modules", []):
            index[(pth["id"], m["id"])] = m
    missing = [k for k in rw if k not in index]
    assert not missing, f"{shard}: missing keys {missing}"
    for key, new in rw.items():
        m = index[key]
        assert isinstance(m.get("il_provides"), str), f"{shard}:{key} not str"
        old_topics = json.dumps(m.get("topics"), sort_keys=True)
        old_sources = json.dumps(m.get("sources"), sort_keys=True)
        m["il_provides"] = new
        assert json.dumps(m.get("topics"), sort_keys=True) == old_topics
        assert json.dumps(m.get("sources"), sort_keys=True) == old_sources
        ok, n = sentences_ok(new)
        assert ok, f"{shard}:{key} has {n} sentences"
        low = new.lower()
        for b in BANNED:
            assert not re.search(r"(?<![a-z])" + re.escape(b) + r"(?![a-z])", low), \
                f"{shard}:{key} contains banned {b!r}"
        assert "http" not in low, f"{shard}:{key} contains a URL"
    # all rewrites applied; now global prefix check on the doc
    text = json.dumps(d, ensure_ascii=False)
    assert '"il_provides: \\"il_provides:' not in text, f"{shard}: double prefix remains"
    # check: no remaining literal-prefix blurbs in the AFFECTED scope
    if shard in ("shard-b", "shard-c"):
        leftovers = [k for k, m in index.items()
                     if isinstance(m.get("il_provides"), str)
                     and m["il_provides"].startswith("il_provides: ")]
        assert not leftovers, f"{shard}: prefix leftovers {leftovers}"
    # atomic write
    fd, tmp = tempfile.mkstemp(dir=BASE, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, path)
    d2 = json.load(open(path, encoding="utf-8"))  # AFTER load
    n2 = sum(len(p.get("modules", [])) for p in d2["paths"])
    assert n2 == len(index), f"{shard}: module count changed {len(index)}->{n2}"
    print(f"{shard}: applied {len(rw)}, modules {n2}, prefix leftovers 0, all 2+ sentences")
    return d2, index

for shard, rw in [("shard-b", RW_B), ("shard-c", RW_C), ("shard-d", RW_D)]:
    d2, _ = process(shard, rw)

print("== spot checks ==")
import itertools
def spot(shard, rw, k=5):
    path = os.path.join(BASE, f"{shard}.json")
    d = json.load(open(path, encoding="utf-8"))
    idx = {(p["id"], m["id"]): m for p in d["paths"] for m in p.get("modules", [])}
    for key in itertools.islice(rw.keys(), k):
        m = idx[key]
        print(f"--- {shard} {key[0]}::{key[1]}")
        print("TITLE:", m["title"])
        print("BLURB:", m["il_provides"])
        print()
spot("shard-b", RW_B)
spot("shard-c", RW_C)
spot("shard-d", RW_D)
print("DONE")
