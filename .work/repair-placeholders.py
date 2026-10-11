#!/usr/bin/env python3
"""Repair unformatted {topic}/{objective}/{course_code} placeholders in IL-01..IL-15."""
import json, glob, os

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")

def sub(s, topic, objective, code):
    if not isinstance(s, str):
        return s
    return s.replace("{topic}", topic).replace("{objective}", objective).replace("{course_code}", code)

def walk(o, topic, objective, code):
    if isinstance(o, dict):
        return {k: walk(v, topic, objective, code) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v, topic, objective, code) for v in o]
    return sub(o, topic, objective, code)

n_files = n_repl = 0
for f in sorted(glob.glob(os.path.join(BASE, "il-0[1-9]-*.json")) + glob.glob(os.path.join(BASE, "il-1[0-5]-*.json"))):
    d = json.load(open(f))
    code = d.get("code", "")
    changed = False
    for m in d.get("modules", []):
        topic = m.get("title", "this module")
        obj = (m.get("objectives") or ["this module's objectives"])[0]
        new_m = walk(m, topic, obj, code)
        if new_m != m:
            # count replacements
            before = json.dumps(m).count("{topic}") + json.dumps(m).count("{objective}") + json.dumps(m).count("{course_code}")
            n_repl += before
            m.clear(); m.update(new_m)
            changed = True
    if changed:
        tmp = f + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(d, fh, indent=1, ensure_ascii=False); fh.write("\n")
        json.load(open(tmp))
        os.replace(tmp, f)
        n_files += 1
print(f"repaired {n_repl} placeholders across {n_files} files")
# verify
left = 0
for f in sorted(glob.glob(os.path.join(BASE, "il-0[1-9]-*.json")) + glob.glob(os.path.join(BASE, "il-1[0-5]-*.json"))):
    c = open(f).read().count("{topic}") + open(f).read().count("{objective}") + open(f).read().count("{course_code}")
    left += c
print("remaining placeholders:", left)
