#!/usr/bin/env python3
"""S1+S3: Expand docs/_worker.js OG_PROFILES to all 29 courses with cinematic
-og.png image paths. Keeps the 4 existing hand-written profiles verbatim;
generates the other 25 from course JSON (title + tagline)."""
import json, glob, re, subprocess

ROOT = "/home/hatch/workspace/apex-audit/docs"
W = f"{ROOT}/_worker.js"
src = open(W, encoding="utf-8").read()

# ---- gather course metadata ----
courses = {}  # courseId -> (code, title, tagline)
for f in sorted(glob.glob(f"{ROOT}/university/data/courses/il-*.json")):
    if f.endswith(".diagbak"):
        continue
    d = json.load(open(f, encoding="utf-8"))
    cid, code = d.get("courseId"), d.get("code")
    if cid and code:
        courses[cid] = (code, d.get("title", ""), d.get("tagline") or d.get("blurb") or "")
assert len(courses) == 29, f"expected 29 courses, got {len(courses)}"

# ---- extract the 4 existing profiles verbatim ----
m = re.search(r"var OG_PROFILES = \{(.*?)\n\};", src, re.S)
assert m, "OG_PROFILES block not found"
old_block = m.group(1)
existing = {}
for pm in re.finditer(r'"([^"]+)": \{\s*title: "((?:[^"\\]|\\.)*)",\s*description: "((?:[^"\\]|\\.)*)",\s*image: "[^"]*"\s*\}', old_block):
    existing[pm.group(1)] = (pm.group(2), pm.group(3))
assert len(existing) == 4, f"expected 4 existing profiles, got {len(existing)}"

# ---- build the new block ----
def js_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'

lines = ["var OG_PROFILES = {"]
for cid in sorted(courses.keys()):
    code, title, tagline = courses[cid]
    png = f"/assets/cinematic/courses-og/{code}-og.png"
    if cid in existing:
        t, d = existing[cid]
        title_js, desc_js = '"' + t + '"', '"' + d + '"'
    else:
        t = title if title.startswith(code) else f"{code} \u00b7 {title}"
        d = tagline.strip()
        if len(d) > 220:
            d = d[:217].rsplit(" ", 1)[0] + "..."
        title_js, desc_js = js_str(t), js_str(d)
    lines.append(f'  "{cid}": {{')
    lines.append(f"    title: {title_js},")
    lines.append(f"    description: {desc_js},")
    lines.append(f'    image: "{png}"')
    lines.append("  },")
lines.append("};")
new_profiles = "\n".join(lines)

new_src = src[:m.start()] + new_profiles + src[m.end():]
assert new_src != src
with open(W, "w", encoding="utf-8") as f:
    f.write(new_src)

r = subprocess.run(["node", "--check", W], capture_output=True, text=True)
print("profiles:", len(courses), "| node --check:", "OK" if r.returncode == 0 else f"FAILED\n{r.stderr}")
# sanity: every code maps to a deployed file
import os
missing = [c for c, _, _ in courses.values()
           if not os.path.exists(f"{ROOT}/assets/cinematic/courses-og/{c}-og.png")]
print("missing og pngs:", missing or "none")
