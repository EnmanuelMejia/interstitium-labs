#!/usr/bin/env python3
"""Build docs/university/data/curriculum-sequence.json — canonical IL-01..IL-29 ordering.

One master sequence: each course with its module ids in intended order.
Run from ~/workspace/apex-audit/docs/university.
"""
import json, glob, os

BASE = os.path.dirname(os.path.abspath(__file__))
courses_dir = os.path.join(BASE, 'data', 'courses')

seq = []
for i in range(1, 30):
    pats = sorted(glob.glob(os.path.join(courses_dir, f'il-{i:02d}-*.json')))
    pats = [p for p in pats if not p.endswith('.bak')]
    if not pats:
        raise SystemExit(f'no course json for IL-{i:02d}')
    f = pats[0]
    d = json.load(open(f))
    cid = d.get('courseId')
    slug = os.path.basename(f)[:-5]  # matches ?course=<slug>
    mods = d.get('modules', [])
    mids = [m.get('id') for m in mods if m.get('id')]
    seq.append({
        'courseId': cid,
        'code': f'IL-{i:02d}',
        'slug': slug,
        'title': d.get('title', ''),
        'hours': d.get('hours'),
        'moduleIds': mids,
        'modules': [{'id': m.get('id'), 'title': m.get('title', '')} for m in mods if m.get('id')],
        'moduleCount': len(mids),
    })

doc = {
    'schemaVersion': 1,
    'order': 'IL-01..IL-29 curriculum order',
    'generatedAt': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
    'free': ['IL-27', 'IL-28', 'IL-29'],
    'courses': seq,
}
out = os.path.join(BASE, 'data', 'curriculum-sequence.json')
with open(out, 'w') as fh:
    json.dump(doc, fh, indent=1)
    fh.write('\n')
print('wrote', out)
print('courses:', len(seq), 'modules:', sum(c['moduleCount'] for c in seq))
# assert module id uniqueness
allids = [m for c in seq for m in c['moduleIds']]
assert len(allids) == len(set(allids)), 'duplicate module ids!'
print('module ids unique:', len(allids))
