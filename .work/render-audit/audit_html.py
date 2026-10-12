#!/usr/bin/env python3
"""Render-audit HTML checks for one file. Usage: audit_html.py <label> <path>"""
import re, sys, html.parser

label, path = sys.argv[1], sys.argv[2]
src = open(path, encoding='utf-8', errors='replace').read()

class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = {}
        self.imgs = []
        self.inline_styles = 0
        self.stylesheet_links = []
        self.favicon = False
        self.viewport = False
        self.title = None
        self.scripts = []
        self._in_title = False
        self.inline_script_blocks = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.setdefault(a['id'], []).append(self.getpos()[0])
        if tag == 'img':
            self.imgs.append((self.getpos()[0], a.get('src'), a.get('alt')))
        if 'style' in a:
            self.inline_styles += 1
        if tag == 'link':
            rel = (a.get('rel') or '').lower()
            if 'stylesheet' in rel:
                self.stylesheet_links.append((self.getpos()[0], a.get('href')))
            if 'icon' in rel:
                self.favicon = True
        if tag == 'meta' and (a.get('name') or '').lower() == 'viewport':
            self.viewport = True
        if tag == 'script' and a.get('src'):
            self.scripts.append(a['src'])
        if tag == 'title':
            self._in_title = True
    def handle_data(self, d):
        if self._in_title:
            self.title = (self.title or '') + d.strip()
    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False

p = P()
p.feed(src)

print(f"===== {label} ({path}, {len(src)} bytes) =====")
print(f"title: {p.title!r}")
print(f"viewport meta: {'PRESENT' if p.viewport else 'MISSING'}")
print(f"favicon link: {'present' if p.favicon else 'MISSING'}")
print(f"stylesheet <link>s: {len(p.stylesheet_links)}")
for ln, href in p.stylesheet_links[:12]:
    print(f"   L{ln}: {href}")
print(f"script srcs: {len(p.scripts)}")
for s in p.scripts[:15]:
    print(f"   {s}")
print(f"inline style= attributes: {p.inline_styles}")
print(f"<img> tags: {len(p.imgs)}")
bad = 0
for ln, s, alt in p.imgs:
    if not s or not s.strip():
        print(f"   L{ln}: img MISSING/EMPTY src (alt={alt!r})"); bad += 1
    elif alt is None:
        print(f"   L{ln}: img missing alt (src={s[:80]})"); bad += 1
    elif alt.strip() == '':
        print(f"   L{ln}: img EMPTY alt (src={s[:80]})"); bad += 1
if not bad:
    print("   all imgs have src + non-empty alt")
dupes = {k: v for k, v in p.ids.items() if len(v) > 1}
print(f"duplicate ids: {len(dupes)}")
for k, v in list(dupes.items())[:15]:
    print(f"   id={k!r} at lines {v}")
for t in ('div', 'section', 'main', 'table'):
    o = len(re.findall(rf'<{t}[\s>]', src)); c = len(re.findall(rf'</{t}>', src))
    if o != c:
        print(f"   tag imbalance <{t}>: open={o} close={c}")
print()
