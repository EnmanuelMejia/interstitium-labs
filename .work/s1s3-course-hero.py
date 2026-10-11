#!/usr/bin/env python3
"""S1: Wire cinematic poster into the course-shell hero (heroHTML).
Poster only — no autoplay video (not forced per task).
- docs/university/course-shell.js: heroHTML() gains a banner <img> for IL-01..IL-29
- docs/university/course-shell.css: .hero-poster styles"""
import subprocess

J = "/home/hatch/workspace/apex-audit/docs/university/course-shell.js"
src = open(J, encoding="utf-8").read()

old = """function heroHTML() {
  var dl = COURSE.updatedAt ? esc(COURSE.updatedAt) + ' · ' : '';
  var hours = COURSE.hours ? ' · ' + COURSE.hours + ' hours' : '';
  return '<div class="hero">' +
    '<div class="dateline">' + dl + esc(COURSE.code) + ' · SCIENTIA OMNIA VINCIT' + hours + '</div>' +"""
new = """function heroHTML() {
  var dl = COURSE.updatedAt ? esc(COURSE.updatedAt) + ' · ' : '';
  var hours = COURSE.hours ? ' · ' + COURSE.hours + ' hours' : '';
  /* 2026-10-09 cinematic rollout (S1): course poster banner. */
  var poster = (/^IL-(0[1-9]|[12][0-9])$/.test(String(COURSE.code || '')))
    ? '<div class="hero-poster"><img src="/assets/cinematic/courses/' + esc(COURSE.code) + '.png" alt="" loading="lazy"></div>' : '';
  return '<div class="hero">' + poster +
    '<div class="dateline">' + dl + esc(COURSE.code) + ' · SCIENTIA OMNIA VINCIT' + hours + '</div>' +"""
assert src.count(old) == 1, "heroHTML anchor not found exactly once"
src = src.replace(old, new)
open(J, "w", encoding="utf-8").write(src)
r = subprocess.run(["node", "--check", J], capture_output=True, text=True)
print("course-shell.js: hero poster wired | node --check:", "OK" if r.returncode == 0 else f"FAILED\n{r.stderr}")
assert r.returncode == 0

C = "/home/hatch/workspace/apex-audit/docs/university/course-shell.css"
css = open(C, encoding="utf-8").read()
rule = """
/* 2026-10-09 cinematic rollout (S1): cinematic poster banner in course hero. */
.hero-poster{margin:0 0 14px}
.hero-poster img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:10px;display:block;background:#06080c;border:1px solid var(--line)}
"""
assert ".hero-poster" not in css
css = css.rstrip("\n") + "\n" + rule
open(C, "w", encoding="utf-8").write(css)
print("course-shell.css: .hero-poster rule added")
