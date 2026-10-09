#!/usr/bin/env python3
"""Add sections[] to the 6 cert bootcamps missing it (overview tab currently shows Labs 0/0)."""
import json, os

BC = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUGS = ['cisco-ccna', 'comptia-a-plus', 'comptia-network-plus', 'comptia-security-plus', 'isc2-cc', 'm365-endpoint-admin']

for slug in SLUGS:
    p = os.path.join(BC, slug, 'content.json')
    d = json.load(open(p))
    assert not d.get('sections'), f'{slug} already has sections'
    # lectures: c-<domain_id> per lesson, deduped, lesson order
    seen, lectures = set(), []
    for l in d.get('lessons', []):
        lid = 'c-' + l['domain_id']
        if lid not in seen:
            seen.add(lid); lectures.append(lid)
    lab_ids = [l['id'] for l in d.get('labs', []) if l.get('id')]
    drill_domain_ids = [x['id'] for x in d.get('domains', []) if x.get('id')]
    d['sections'] = [{
        "id": f"sec-{slug}",
        "title": f"{d.get('title','Core')} \u2014 core path",
        "kind": "core",
        "lectures": lectures,
        "lab_ids": lab_ids,
        "drill_domain_ids": drill_domain_ids,
    }]
    with open(p, 'w') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write('\n')
    d2 = json.load(open(p))
    assert len(d2['sections']) == 1
    print(f"{slug}: lectures={len(lectures)} labs={len(lab_ids)} drills={len(drill_domain_ids)} OK")
print('all validated')
