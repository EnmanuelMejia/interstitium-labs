#!/usr/bin/env python3
"""Verify anchor fragments against page ids (repo-local)."""
import json

d = json.load(open('/tmp/link-extract.json'))
ids = d['ids']
unique = json.load(open('/tmp/unique-urls.json'))
anchors = json.load(open('/tmp/anchors.json'))

def page_ids(purl):
    return set(ids.get(purl, []))

bad_same = []   # anchor-only with missing id
for a in anchors:
    frag = a['frag']
    if not frag:  # href="#" handled as blank
        continue
    if frag not in page_ids(a['page']):
        bad_same.append(a)

# cross-page fragments on INTERNAL urls
bad_cross = []
frag_pages = {}  # target nofrag url -> set of frags referenced
for key, v in unique.items():
    for o in v['occurrences']:
        frag = o.get('frag')
        if not frag: continue
        host = v['url'].split('/')[2]
        if host in ('interstitiumlabs.dev', 'enmanueldmejia.com'):
            frag_pages.setdefault(v['url'], set()).add(frag)

for turl, frags in frag_pages.items():
    pids = page_ids(turl)
    for frag in frags:
        if frag not in pids:
            bad_cross.append({'target': turl, 'frag': frag})

print(f'same-page anchors bad: {len(bad_same)}')
for b in bad_same[:30]:
    print('  MISS:', b['file'], '#', b['frag'])
print(f'cross-page anchors bad: {len(bad_cross)}')
for b in bad_cross:
    print('  MISS:', b['target'], '#', b['frag'])

json.dump({'bad_same': bad_same, 'bad_cross': bad_cross},
          open('/tmp/anchor-check.json', 'w'), indent=1)
