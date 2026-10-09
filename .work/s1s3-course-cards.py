#!/usr/bin/env python3
"""S1: Wire cinematic posters into /university/ academy cards.
- academyCard() in docs/university/index.html: prepend poster <img> for IL-01..IL-29
- docs/university/css/il.css: .card-poster styles"""
import re

P = "/home/hatch/workspace/apex-audit/docs/university/index.html"
src = open(P, encoding="utf-8").read()

old = """    c.innerHTML =
      '<div class="code">' + IL.esc(a.code) + '</div>' +"""
new = """    /* 2026-10-09 cinematic rollout (S1): poster per course code. */
    var poster = (/^IL-(0[1-9]|[12][0-9])$/.test(String(a.code || '')))
      ? '<img class="card-poster" src="/assets/cinematic/courses/' + IL.esc(a.code) + '.png" alt="" loading="lazy">' : '';
    c.innerHTML = poster +
      '<div class="code">' + IL.esc(a.code) + '</div>' +"""
assert src.count(old) == 1, "academyCard anchor not found exactly once"
src = src.replace(old, new)
open(P, "w", encoding="utf-8").write(src)
print("index.html: academyCard poster wired")

C = "/home/hatch/workspace/apex-audit/docs/university/css/il.css"
css = open(C, encoding="utf-8").read()
rule = """
/* 2026-10-09 cinematic rollout (S1): course poster on academy cards. */
.card .card-poster {
  width: calc(100% + 2.8rem);
  margin: -1.35rem -1.4rem 1rem;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border-radius: var(--radius) var(--radius) 0 0;
  display: block;
  background: #06080c;
}
"""
assert ".card-poster" not in css
css = css.rstrip("\n") + "\n" + rule
open(C, "w", encoding="utf-8").write(css)
print("il.css: .card-poster rule added")
