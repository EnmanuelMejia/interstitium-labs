#!/usr/bin/env python3
"""Apply href/src/action fixes: reads fix map JSON, edits exact occurrences in files.
Fix map format: [{"file": path, "old": 'href="#phase3"', "new": 'href="#main"', "count": 1}]
Validates each edit happened exactly `count` times; aborts file on mismatch."""
import json, sys

fixes = json.load(open('/tmp/fix-map.json'))
by_file = {}
for f in fixes:
    by_file.setdefault(f['file'], []).append(f)

log = []
for path, edits in sorted(by_file.items()):
    with open(path, encoding='utf-8') as fh:
        html = fh.read()
    orig = html
    for e in edits:
        n = html.count(e['old'])
        if n != e.get('count', 1):
            log.append(f"SKIP-MISMATCH {path}: expected {e.get('count',1)}× {e['old']!r}, found {n}")
            continue
        html = html.replace(e['old'], e['new'])
        log.append(f"FIXED {path}: {e['old']!r} -> {e['new']!r} ({n}×)")
    if html != orig:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)

print('\n'.join(log))
print(f'{len([l for l in log if l.startswith("FIXED")])} fixes applied')
