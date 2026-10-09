#!/usr/bin/env python3
"""W6 cleanup: remove all 30 W6-pattern entries from cism (test + full run), validate."""
import json, re, os
p = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps/cism/content.json")
pat = re.compile(r"^cism-[a-z0-9_.-]+-d[123](v\d+)?$")
d = json.load(open(p))
before = len(d["media"])
d["media"] = [m for m in d["media"] if not pat.match(m.get("id", ""))]
after = len(d["media"])
tmp = p + ".w6tmp"
json.dump(d, open(tmp, "w"), ensure_ascii=False, indent=2)
json.load(open(tmp))  # validate
os.replace(tmp, p)
print(f"removed {before - after}, remaining {after}")
