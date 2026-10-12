#!/usr/bin/env python3
"""Fixup: dedupe sourceLinks with trailing-slash URL normalization. Idempotent."""
import json, os
BASE = os.path.expanduser('~/workspace/apex-audit')
P = BASE + '/docs/university/data/courses/il-17-agentic-ai-engineering.json'
with open(P) as f:
    d = json.load(f)
seen, out = set(), []
for s in d['sourceLinks']:
    k = (s.get('name'), (s.get('url') or '').rstrip('/'))
    if k in seen:
        continue
    seen.add(k)
    out.append(s)
d['sourceLinks'] = out
tmp = P + '.fixup_tmp'
with open(tmp, 'w') as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
    f.write('\n')
with open(tmp) as f:
    json.load(f)
os.replace(tmp, P)
print('sourceLinks now', len(out))
