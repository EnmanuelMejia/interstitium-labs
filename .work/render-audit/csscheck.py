#!/usr/bin/env python3
"""Heuristic: fixed px widths > 400 in CSS outside @media blocks; tables/grids."""
import re, sys

path = sys.argv[1]
src = open(path, encoding='utf-8', errors='replace').read()

# strip comments
src_nc = re.sub(r'/\*.*?\*/', '', src, flags=re.S)

# find @media block spans
spans = []
for m in re.finditer(r'@media[^{]*\{', src_nc):
    start = m.start(); depth = 0
    for i in range(m.end()-1, len(src_nc)):
        if src_nc[i] == '{': depth += 1
        elif src_nc[i] == '}':
            depth -= 1
            if depth == 0:
                spans.append((start, i)); break

def in_media(pos):
    return any(a <= pos <= b for a, b in spans)

hits = []
for m in re.finditer(r'(?<![\w-])(width|min-width|max-width)\s*:\s*(\d+)px', src_nc):
    prop, val = m.group(1), int(m.group(2))
    if val > 400 and not in_media(m.start()):
        line = src_nc[:m.start()].count('\n') + 1
        # context: selector start = last } or ; before
        ctx = src_nc[max(0,m.start()-120):m.start()].split('}')[-1].strip().split('\n')[-1][:80]
        hits.append((line, prop, val, ctx))

print(f"===== {path} ({len(src)} bytes) =====")
print(f"fixed px widths >400 outside @media: {len(hits)}")
for line, prop, val, ctx in hits[:25]:
    print(f"  L{line}: {prop}: {val}px   ctx: {ctx}")
tables = len(re.findall(r'<table', ''))  # n/a
grids = len(re.findall(r'display\s*:\s*grid', src_nc))
flexes = len(re.findall(r'display\s*:\s*flex', src_nc))
print(f"display:grid rules: {grids}, display:flex rules: {flexes}")
# grid-template-columns with fixed repeat counts + fixed px
fixed_grids = []
for m in re.finditer(r'grid-template-columns\s*:\s*([^;{]+);', src_nc):
    v = m.group(1).strip()
    if re.search(r'\d+px', v) and 'minmax' not in v and not in_media(m.start()):
        line = src_nc[:m.start()].count('\n') + 1
        fixed_grids.append((line, v[:90]))
print(f"fixed-px grid-template-columns outside @media: {len(fixed_grids)}")
for line, v in fixed_grids[:15]:
    print(f"  L{line}: {v}")
print()
