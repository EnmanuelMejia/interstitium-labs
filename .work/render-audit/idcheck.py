#!/usr/bin/env python3
"""Extract getElementById/querySelector(#..) targets from JS, compare with HTML ids."""
import re, sys, html.parser

js_path, html_path, label = sys.argv[1], sys.argv[2], sys.argv[3]
js = open(js_path, encoding='utf-8', errors='replace').read()

# strip line comments and string literals roughly to avoid false positives
js_nocomments = re.sub(r'//[^\n]*', '', js)
ids_ref = set()
for m in re.finditer(r'''getElementById\(\s*['"]([^'"]+)['"]''', js_nocomments):
    ids_ref.add(m.group(1))
for m in re.finditer(r'''querySelector(?:All)?\(\s*['"]#([\w\-\:]+)''', js_nocomments):
    ids_ref.add(m.group(1))
# jQuery-ish $('#x')
for m in re.finditer(r'''\$\(\s*['"]#([\w\-]+)['"]''', js_nocomments):
    ids_ref.add(m.group(1))

class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
p = P()
p.feed(open(html_path, encoding='utf-8', errors='replace').read())

missing = sorted(i for i in ids_ref if i not in p.ids)
print(f"--- {label}")
print(f"JS: {js_path}  HTML: {html_path}")
print(f"id refs in JS: {len(ids_ref)}; missing in HTML: {len(missing)}")
for m in missing:
    lines = [n for n, l in enumerate(js.splitlines(), 1) if re.search(r'getElementById\(\s*[\'"]' + re.escape(m) + r'[\'"]|#'+re.escape(m)+r'\b', l)]
    print(f"  MISSING #{m}  (JS refs at lines {lines[:4]})")
