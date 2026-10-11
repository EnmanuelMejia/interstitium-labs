#!/usr/bin/env python3
"""Dark-by-default implementation: add theme boot to pages missing it,
neutralize prefers-color-scheme:light in course-shell.css, fix color-scheme meta."""
import re, sys

DOCS = "/home/hatch/workspace/apex-audit/docs"

PAGES = [
    "jobs/index.html",
    "noah/index.html",
    "search/index.html",
    "university/about.html",
    "university/academy.html",
    "university/assess.html",
    "university/course.html",
    "university/courses.html",
    "university/data/courses/_il26-build/dossier.html",
    "university/enroll.html",
    "university/honesty.html",
    "university/il-26-dossier.html",
    "university/il-27-dossier.html",
    "university/index.html",
    "university/lab-generative-packing.html",
    "university/learn.html",
    "university/path.html",
    "university/paths.html",
    "university/tracks.html",
    "work/lps-enrollment-analysis/index.html",
    "work/sundance-ai-architecture/index.html",
]

BOOT = '<script src="/assets/il-theme.js"></script>'
added, skipped = 0, 0
for rel in PAGES:
    p = f"{DOCS}/{rel}"
    try:
        s = open(p, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"MISSING: {rel}")
        continue
    if "il-theme.js" in s:
        skipped += 1
        continue
    if "<head>" not in s:
        print(f"NO-HEAD: {rel}")
        continue
    s = s.replace("<head>", "<head>" + BOOT, 1)
    open(p, "w", encoding="utf-8").write(s)
    added += 1
print(f"theme boot: added={added} skipped={skipped}")

# --- course-shell.css: gate light tokens behind explicit user choice ---
css_p = f"{DOCS}/university/course-shell.css"
css = open(css_p, encoding="utf-8").read()

# 1. Convert the :root light-token override from OS media query to explicit choice
old_light_root = """@media (prefers-color-scheme:light){
  :root{
    --bg:#f4f6fa; --panel:#ffffff; --panel2:#f7f9fc; --panel3:#eef2f7;
    --ink:#10161f; --muted:#54637a; --faint:#8494a9;
    --line:rgba(16,24,40,.11); --line2:rgba(16,24,40,.2);
    --gold:#8a6d14; --gold-soft:rgba(201,162,39,.16);
    --cyan:#0e7490; --cyan-soft:rgba(14,116,144,.08);
    --shadow:0 14px 36px rgba(16,24,40,.12);
    color-scheme:light;
  }
}"""
new_light_root = """/* Light theme is OPT-IN ONLY via the theme toggle (il-theme.js sets
   html[data-theme="light"]). The OS color-scheme preference NEVER flips
   the default: first-time and anonymous visitors always get dark. */
html[data-theme="light"]{
    --bg:#f4f6fa; --panel:#ffffff; --panel2:#f7f9fc; --panel3:#eef2f7;
    --ink:#10161f; --muted:#54637a; --faint:#8494a9;
    --line:rgba(16,24,40,.11); --line2:rgba(16,24,40,.2);
    --gold:#8a6d14; --gold-soft:rgba(201,162,39,.16);
    --cyan:#0e7490; --cyan-soft:rgba(14,116,144,.08);
    --shadow:0 14px 36px rgba(16,24,40,.12);
    color-scheme:light;
}"""
if old_light_root in css:
    css = css.replace(old_light_root, new_light_root, 1)
    print("course-shell.css: light :root block -> html[data-theme=light]")
else:
    print("course-shell.css: WARNING light :root block not found verbatim")

# 2. Remove the two no-op rules (they set dark values under light OS; deleting
#    keeps identical visuals while removing OS-dependent behavior)
noop1 = "@media (prefers-color-scheme:light){ pre{background:#10161f; color:#d6f5e3} }"
noop2 = "@media (prefers-color-scheme:light){ .code-editor{background:#10161f; color:#d9ecff} }"
for i, noop in enumerate([noop1, noop2], 1):
    if noop in css:
        css = css.replace(noop, "", 1)
        print(f"course-shell.css: removed no-op light rule #{i}")
    else:
        print(f"course-shell.css: WARNING no-op rule #{i} not found")

open(css_p, "w", encoding="utf-8").write(css)

# Any remaining prefers-color-scheme:light in course-shell.css?
remaining = re.findall(r"prefers-color-scheme\s*:\s*light", css)
print(f"course-shell.css: remaining prefers-color-scheme:light occurrences = {len(remaining)}")

# --- course.html: color-scheme meta -> dark only ---
ch_p = f"{DOCS}/university/course.html"
ch = open(ch_p, encoding="utf-8").read()
if '<meta name="color-scheme" content="dark light">' in ch:
    ch = ch.replace('<meta name="color-scheme" content="dark light">',
                    '<meta name="color-scheme" content="dark">', 1)
    open(ch_p, "w", encoding="utf-8").write(ch)
    print("course.html: color-scheme meta -> dark")
else:
    print("course.html: color-scheme meta already ok or missing")
