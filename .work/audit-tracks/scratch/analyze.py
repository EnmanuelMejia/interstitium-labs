#!/usr/bin/env python3
"""Consistency audit analyzer: nav, footer, logo, theme, motto per page."""
import re, os, sys, hashlib, json

SCRATCH = os.path.dirname(os.path.abspath(__file__))

RETIRED = [
    "/assets/chrome/sigil-decor.webp",
    "/assets/chrome/sigil-glyph.svg",
    "/assets/chrome/canonical-lockup",
    "/favicon.svg",
    "/favicon.png",
    "/og.jpg",
    "/og-sigil.jpg",
    "/assets/il-logo.js",
]

def retired_hit(src):
    for r in RETIRED:
        if r in src:
            return r
    return None

def analyze(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    out = {"file": os.path.basename(path), "bytes": len(html)}
    low = html.lower()

    # --- NAV ---
    navs = re.findall(r'<nav\b[^>]*class="([^"]*)"[^>]*>', html)
    out["nav_classes"] = navs
    out["has_pillnav"] = any("il-pillnav" in c for c in navs)
    out["has_shell_header"] = "shell-header" in html
    # pillnav link texts
    m = re.search(r'<nav[^>]*class="[^"]*il-pillnav[^"]*"[^>]*>(.*?)</nav>', html, re.S)
    if m:
        links = re.findall(r'<a\b[^>]*>(.*?)</a>', m.group(1), re.S)
        out["pillnav_links"] = sorted(set(re.sub(r'<[^>]+>', '', l).strip() for l in links if re.sub(r'<[^>]+>', '', l).strip()))
    else:
        out["pillnav_links"] = []

    # --- MOTTO ---
    mottos = re.findall(r'[Ss][Cc][Ii][Ee][Nn][Tt][Ii][Aa]\s+[Oo][Mm][Nn][Ii][Aa]\s+[Vv][Ii][Nn][Cc][Ii][Tt]', html)
    # better: capture raw case
    mottos_raw = re.findall(r'SCIENTIA\s+OMNIA\s+VINCIT|Scientia\s+omnia\s+vincit|scientia\s+omnia\s+vincit', html)
    out["motto_occurrences"] = mottos_raw
    out["motto_cases"] = sorted(set(mottos_raw))

    # --- LOGO / icons ---
    img_srcs = re.findall(r'<img\b[^>]*src="([^"]+)"', html)
    logoish = [s for s in img_srcs if re.search(r'sigil|logo|chrome|brand', s, re.I)]
    out["logo_imgs"] = logoish
    out["retired_logo_hits"] = [ (s, retired_hit(s)) for s in logoish if retired_hit(s) ]
    icons = re.findall(r'<link\b[^>]*rel="[^"]*icon[^"]*"[^>]*href="([^"]+)"', html)
    out["icons"] = icons
    out["retired_icon_hits"] = [ (s, retired_hit(s)) for s in icons if retired_hit(s) ]
    # any other retired-path references anywhere
    all_retired = []
    for r in RETIRED:
        if r in html:
            all_retired.append(r)
    out["any_retired_refs"] = sorted(set(all_retired))

    # --- THEME ---
    out["has_il_theme_js"] = "/assets/il-theme.js" in html
    dm = re.search(r'<html\b[^>]*>', html)
    out["html_tag"] = dm.group(0) if dm else ""
    out["data_theme"] = re.findall(r'data-theme="([^"]*)"', html)[:3]
    out["prefers_light_override"] = bool(re.search(r'prefers-color-scheme\s*:\s*light', html))
    out["color_scheme_meta"] = re.findall(r'<meta[^>]*name="color-scheme"[^>]*>', html)
    out["theme_color_meta"] = re.findall(r'<meta[^>]*name="theme-color"[^>]*content="([^"]*)"', html)

    # --- FOOTER ---
    fm = re.findall(r'<footer\b[^>]*>(.*?)</footer>', html, re.S)
    out["footer_count"] = len(fm)
    if fm:
        norm = re.sub(r'\s+', ' ', fm[0])[:6000]
        out["footer_hash"] = hashlib.md5(norm.encode()).hexdigest()[:12]
        out["footer_len"] = len(fm[0])
        out["footer_classes"] = re.findall(r'<footer\b[^>]*class="([^"]*)"', html)
        # footer brand/motto text
        ftxt = re.sub(r'<[^>]+>', ' ', fm[0])
        ftxt = re.sub(r'\s+', ' ', ftxt).strip()
        out["footer_text_head"] = ftxt[:300]
    else:
        out["footer_hash"] = None

    # title
    t = re.search(r'<title>(.*?)</title>', html, re.S)
    out["title"] = t.group(1).strip()[:80] if t else ""
    # CF challenge / worker injection markers
    out["has_cf_challenge"] = "challenge-platform" in html
    return out

results = {}
for f in sorted(os.listdir(SCRATCH)):
    if f.endswith(".html"):
        results[f] = analyze(os.path.join(SCRATCH, f))

print(json.dumps(results, indent=1))
