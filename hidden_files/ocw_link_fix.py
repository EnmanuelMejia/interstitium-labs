#!/usr/bin/env python3
"""MIT OCW link audit fix: replace bare-number /courses/<num>/ URLs with /search/?q=<num>.
Only replaces when the URL is terminated by an optional slash + quote (skips slug URLs).
Validates each edited JSON with json.load.
"""
import json
import os
import re
import sys

DOCS = os.path.expanduser("~/workspace/apex-audit/docs")

def main():
    with open("/tmp/broken.txt") as f:
        urls = [l.strip() for l in f if l.strip()]
    nums = sorted((u.rstrip("/").split("/courses/")[-1] for u in urls), key=len, reverse=True)
    with open("/tmp/affected_files.txt") as f:
        files = [l.strip().lstrip("./") for l in f if l.strip()]

    pat = re.compile(
        r"https://ocw\.mit\.edu/courses/(" + "|".join(re.escape(n) for n in nums) + r")/?\""
    )

    total = 0
    per_file = {}
    for rel in files:
        path = os.path.join(DOCS, rel)
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        def repl(m):
            return "https://ocw.mit.edu/search/?q=" + m.group(1) + '"'
        new_txt, n = pat.subn(repl, txt)
        if n:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_txt)
            # validate JSON if it's a .json file
            if path.endswith(".json"):
                with open(path, "r", encoding="utf-8") as f:
                    json.load(f)
            per_file[rel] = n
            total += n
            print(f"FIXED {n:3d}  {rel}")
        else:
            print(f"SKIP    0  {rel} (no match)")

    print(f"\nTOTAL REPLACEMENTS: {total}")

    # post-check: no bare-number /courses/ URLs (terminated by quote) should remain
    check_pat = re.compile(r"https://ocw\.mit\.edu/courses/[0-9A-Za-z]+(?:-[0-9A-Za-z]+)+/?\"")
    leftovers = []
    for rel in files:
        path = os.path.join(DOCS, rel)
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        for m in check_pat.finditer(txt):
            # exclude slug URLs (segment longer than a bare course number)
            seg = m.group(0).split("/courses/")[1].rstrip('/"')
            if re.fullmatch(r"(?:[0-9]+|[a-z]+|res)-[0-9A-Za-z]+(?:-[0-9]+)?", seg):
                leftovers.append((rel, m.group(0)))
    if leftovers:
        print("LEFTOVER BARE URLS:")
        for rel, u in leftovers:
            print(f"  {rel} :: {u}")
        sys.exit(1)
    print("POST-CHECK: no bare-number /courses/ URLs remain. OK")

if __name__ == "__main__":
    main()
