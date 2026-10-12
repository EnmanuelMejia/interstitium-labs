#!/usr/bin/env python3
"""Tolerantly parse each batch file (may contain concatenated JSON values) and
rewrite as a single JSON array. Returns the merged module list."""
import json, os

BUILD = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build"

def parse_all(text):
    dec = json.JSONDecoder()
    idx, out = 0, []
    n = len(text)
    while idx < n:
        while idx < n and (text[idx] in " \t\r\n" or text[idx] == ","):
            idx += 1
        if idx >= n:
            break
        val, end = dec.raw_decode(text, idx)
        out.append(val)
        idx = end
    return out

def load_batch(letter):
    p = os.path.join(BUILD, f"batch-{letter}.json")
    text = open(p).read()
    # children sometimes wrote literal backslash-n between concatenated JSON values
    import re
    text = re.sub(r"(\}\],?)\\n(\{)", r"\1\n\2", text)
    vals = parse_all(text)
    mods = []
    for v in vals:
        if isinstance(v, list):
            mods.extend(v)
        elif isinstance(v, dict) and "id" in v:
            mods.append(v)
        else:
            raise ValueError(f"unexpected top-level value in batch-{letter}")
    with open(p, "w") as f:
        json.dump(mods, f, ensure_ascii=False)
    return mods

if __name__ == "__main__":
    total = []
    for b in ["A", "B", "C", "D", "E1", "E2", "F"]:
        mods = load_batch(b)
        print(f"batch-{b}: {len(mods)} modules")
        total.extend(mods)
    print("total:", len(total))
