"""Build il-27-dossier.html from the IL-26 dossier pattern + certs.json dossier data."""
import html
import json
import os

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/_il27-build")
UNI = os.path.expanduser("~/workspace/apex-audit/docs/university")

dossier = json.load(open(os.path.join(BASE, "certs.json")))["dossier"]
src = open(os.path.join(UNI, "il-26-dossier.html")).read()

# reuse the IL-26 <style> block verbatim (print-ready pattern)
style = src.split("<style>", 1)[1].split("</style>", 1)[0]


def esc(x):
    return html.escape(str(x), quote=True)


def render_table(t):
    cols = t.get("columns", [])
    rows = t.get("rows", [])
    out = ["<table>", "<thead><tr>"]
    for c in cols:
        out.append("<th>" + esc(c) + "</th>")
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>")
        for c in cols:
            v = r.get(c, "") if isinstance(r, dict) else ""
            out.append('<td class="write">' + esc(v) + "</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


sections = []
for i, s in enumerate(dossier.get("sections", []), start=1):
    body = ["<section>", "<h2>" + str(i) + " &middot; " + esc(s.get("heading", "")) + "</h2>",
            "<p>" + esc(s.get("intro", "")) + "</p>"]
    if s.get("bullets"):
        body.append("<ul>")
        for b in s["bullets"]:
            body.append("<li>" + esc(b) + "</li>")
        body.append("</ul>")
    if s.get("table"):
        body.append(render_table(s["table"]))
    body.append("</section>")
    sections.append("\n".join(body))

page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IL-27 Graduate Evidence Map &mdash; IT Infrastructure Specialist: Zero Trust Infrastructure Mastery</title>
<style>""" + style + """</style>
</head>
<body>
<header>
  <h1>IL-27 Graduate Evidence Map</h1>
  <p style="margin:0;font-size:12px;">IT Infrastructure Specialist: Zero Trust Infrastructure Mastery &mdash; coursework completion &amp; portfolio evidence record. <strong>This template records completed coursework and practice scores only.</strong> It does not confer any certification and makes no claim of vendor affiliation or employer endorsement.</p>
</header>

<section>
  <h2>0 &middot; Learner</h2>
  <div class="meta">
    <div><label>Name</label><div class="field"></div></div>
    <div><label>Completion date</label><div class="field"></div></div>
    <div><label>Portfolio URL</label><div class="field"></div></div>
  </div>
</section>

""" + "\n\n".join(sections) + """

<div class="disclaimer">
  <strong>Factual framing only.</strong> """ + esc(dossier.get("framing", "")) + """
</div>

<footer>IL-27 &middot; IT Infrastructure Specialist: Zero Trust Infrastructure Mastery &middot; Graduate Evidence Map (2026-10-07)</footer>
</body>
</html>
"""

out = os.path.join(UNI, "il-27-dossier.html")
with open(out, "w") as f:
    f.write(page)
print("WROTE:", out, len(page), "bytes")
