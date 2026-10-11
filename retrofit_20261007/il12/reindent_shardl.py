#!/usr/bin/env python3
"""Reformat shard-l.json to its original 2-space indent (content unchanged)."""
import json, os

path = os.path.expanduser("~/workspace/apex-audit/docs/university/data/catalog/shard-l.json")
with open(path, encoding="utf-8") as f:
    d = json.load(f)
tmp = path + ".reindent_tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
with open(tmp, encoding="utf-8") as f:
    json.load(f)
os.replace(tmp, path)
print("reindented shard-l.json to 2-space")
