"""Hoist module-level scenarios/drills to course level (matches course-shell.js renderer + multicloud template)."""
import json, copy

p = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-23-frontier-knowledge.json'
d = json.load(open(p))

existing_sc = {s.get('id') for s in d.get('scenarios', [])}
existing_dr = {x.get('id') for x in d.get('drills', [])}

moved_sc, moved_dr = 0, 0
for m in d['modules']:
    for key, existing, counter in (('scenarios', existing_sc, 'sc'), ('drills', existing_dr, 'dr')):
        items = m.pop(key, [])
        for it in items:
            iid = it.get('id')
            assert iid and iid not in existing, f'DUPLICATE {key} id: {iid}'
            # tag with source module for traceability
            it = copy.deepcopy(it)
            it['module'] = m['id']
            d[key].append(it)
            existing.add(iid)
            if key == 'scenarios':
                moved_sc += 1
            else:
                moved_dr += 1

json.dump(d, open(p, 'w'), indent=1, ensure_ascii=False)
d2 = json.load(open(p))
print(f'moved scenarios: {moved_sc} -> course total {len(d2["scenarios"])}')
print(f'moved drills: {moved_dr} -> course total {len(d2["drills"])}')
# sanity: no module retains scenarios/drills keys
for m in d2['modules']:
    assert 'scenarios' not in m and 'drills' not in m, m['id']
print('OK: no module-level scenarios/drills remain; JSON valid')
