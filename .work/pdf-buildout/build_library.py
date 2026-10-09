"""Regenerate docs/pdf-library/index.html indexing all 241 bbg PDF guides."""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_meta import PDFS, CATEGORIES, PAGES, BASE

OUT = os.path.expanduser("~/workspace/apex-audit/docs/pdf-library/index.html")

def card(fname, cat, title, desc):
    return (
        f'<div class="pdf-card"><span class="pdf-cat">{html.escape(cat)}</span>'
        f"<h3>{html.escape(title)}</h3><p>{html.escape(desc)}</p>"
        f'<a class="btn" href="/assets/pdfs/{fname}">Read the guide</a>'
        f'<div class="pdf-meta">{PAGES} pages · animated walkthrough</div></div>'
    )

by_cat = {c: [] for c in CATEGORIES}
for fname, (cat, title, desc) in sorted(PDFS.items()):
    by_cat[cat].append((fname, title, desc))

total = sum(len(v) for v in by_cat.values())
sections = []
for cat in CATEGORIES:
    items = by_cat[cat]
    if not items:
        continue
    cards = "\n".join(card(f, cat, t, d) for f, t, d in items)
    sections.append(f"<h2>{html.escape(cat)} <span class='count'>({len(items)})</span></h2>\n<div class=\"pdf-grid\">\n{cards}\n</div>")

body = "\n\n".join(sections)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Visual Guide Library — Interstitium Labs</title>
<meta name="description" content="Animated step-by-step visual guides: system design, networking, cloud, security, AI/ML, data engineering, databases, Linux, math. Original diagrams, free to read.">
<link rel="stylesheet" href="/assets/il-unified.css">
<style>
.pdf-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.25rem;margin:2rem 0}}
.pdf-card{{border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.25rem;background:rgba(255,255,255,.03)}}
.pdf-card h3{{margin:.5rem 0;font-size:1.05rem}}
.pdf-card p{{color:#9aa0b4;font-size:.9rem;margin:.5rem 0 1rem}}
.pdf-card a.btn{{display:inline-block;padding:.5rem 1rem;border-radius:8px;background:#4361ee;color:#fff;text-decoration:none;font-weight:600;font-size:.9rem}}
.pdf-cat{{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8b9cf0;background:rgba(67,97,238,.15);padding:.25rem .6rem;border-radius:20px}}
.pdf-meta{{font-size:.8rem;color:#6b7280;margin-top:.75rem}}
.count{{font-size:1rem;color:#8b9cf0;font-weight:600}}
.toc{{columns:3;max-width:640px;margin:1rem 0 2rem;font-size:.95rem}}
.toc a{{text-decoration:none}}
</style>
</head>
<body>
<main style="max-width:1100px;margin:0 auto;padding:2rem">
<p><a href="/">← Interstitium Labs</a></p>
<h1>Visual Guide Library</h1>
<p class="lede" style="max-width:640px">Animated step-by-step visual guides in the byte-byte-go tradition — original diagrams drawn for Interstitium Labs. Step through the pages to play each animation. {total} guides, free to read, no sign-in.</p>

<div class="toc">
""" + "\n".join(f'<div><a href="#{cat.lower().replace(" & ","-").replace(" / ","-").replace(" ","-")}">{cat} ({len(by_cat[cat])})</a></div>' for cat in CATEGORIES if by_cat[cat]) + f"""
</div>

{body}

<p style="margin-top:3rem"><a href="https://enmanueldmejia.com/">← Back to portfolio</a></p>
</main>
</body>
</html>
"""

# add anchor ids to section headers
import re
def anchorize(m):
    label = m.group(1)
    aid = label.lower().replace(" & ", "-").replace(" / ", "-").replace(" ", "-")
    return f'<h2 id="{aid}">{m.group(0)[4:]}'
page = re.sub(r"<h2>([^<]+) <span", anchorize, page)

with open(OUT, "w") as f:
    f.write(page)
print(f"wrote {OUT}: {total} guides in {len([c for c in CATEGORIES if by_cat[c]])} categories")
