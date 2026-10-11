#!/usr/bin/env python3
"""S1+S3: Wire cinematic images into the bootcamp hub.
- site/bootcamps/index.html: add <img class="hub-thumb"> to every hub-card
  (slug from href="{slug}/" -> /assets/cinematic/bootcamps/{slug}.png)
- site/bootcamps/engine/style.css: .hub-thumb bleed-to-edges rule"""
import os, re

H = "/home/hatch/workspace/cert-bootcamps/site/bootcamps/index.html"
html = open(H, encoding="utf-8").read()

def add_img(m):
    slug = m.group(1)
    png = f"/assets/cinematic/bootcamps/{slug}.png"
    assert os.path.exists(f"/home/hatch/workspace/apex-audit/docs/assets/cinematic/bootcamps/{slug}.png"), slug
    return m.group(0) + f'<img class="hub-thumb" src="{png}" alt="" loading="lazy">'

new_html, n = re.subn(r'<a class="hub-card" href="([^"]+)/"[^>]*>', add_img, html)
print("hub cards wired:", n)
assert n == 75, f"expected 75 cards, got {n}"
assert new_html.count('class="hub-thumb"') == 75
open(H, "w", encoding="utf-8").write(new_html)

C = "/home/hatch/workspace/cert-bootcamps/site/bootcamps/engine/style.css"
css = open(C, encoding="utf-8").read()
rule = """
/* 2026-10-09 cinematic rollout (S1): bootcamp poster thumb bleeds to card edges. */
.hub-card .hub-thumb{width:calc(100% + 40px);margin:-20px -20px 14px;aspect-ratio:16/9;object-fit:cover;border-radius:var(--radius) var(--radius) 0 0;display:block;background:#060b11}
"""
assert ".hub-thumb" not in css
css = css.rstrip("\n") + "\n" + rule
open(C, "w", encoding="utf-8").write(css)
print("engine/style.css: .hub-thumb rule added")
