# Assemble tool-labs.json from parts + comprehensive validation
import json, re
from collections import Counter

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/'
modules = []
for pf in ['part1_modules.json', 'part2_modules.json', 'part3_modules.json', 'part4_modules.json']:
    modules.extend(json.load(open(BASE + pf)))
labs5 = json.load(open(BASE + 'part5_labs.json'))
cloud6 = json.load(open(BASE + 'part6_cloud.json'))

fragment = {
    "fragment": "C",
    "description": "Progressive tool labs + bleeding-edge modules + multicloud labs for IL-26 Data Analyst Certification: Senior Mastery. Expansion fragment: merges alongside the existing 40 modules (not a replacement).",
    "modules": modules,
    "datasets": labs5['datasets'],
    "toolLabs": labs5['toolLabs'],
    "multicloudLabs": cloud6['multicloudLabs'],
    "installSteps": cloud6['installSteps']
}

# ---------- validation ----------
errs = []
def err(m): errs.append(m)

# 1. module count + ids
ids = [m['id'] for m in modules]
exp_ids = [f'IL26-M{i}' for i in range(41, 52)]
if ids != exp_ids: err(f'module ids mismatch: {ids}')
if len(set(ids)) != 11: err('duplicate module ids')

schema_keys = {"id","code","title","summary","objectives","notes","cards","quiz","weight","prerequisiteFor"}
for m in modules:
    if set(m.keys()) != schema_keys: err(f"{m['id']} keys: {set(m.keys()) ^ schema_keys}")
    if m['code'] != 'IL-26': err(f"{m['id']} code")
    if len(m['objectives']) < 4: err(f"{m['id']} objectives <4")
    if len(m['notes']) < 4: err(f"{m['id']} notes <4")
    for n in m['notes']:
        if set(n.keys()) != {"title","body"}: err(f"{m['id']} note keys")
        if n['body'].count('```') < 2: err(f"{m['id']} note missing fenced code: {n['title'][:40]}")
    if len(m['cards']) != 8: err(f"{m['id']} cards != 8")
    for c in m['cards']:
        if set(c.keys()) != {"front","back"}: err(f"{m['id']} card keys")
    if len(m['quiz']) != 8: err(f"{m['id']} quiz != 8")
    dist = [Counter(q['answer'] for q in m['quiz'])[i] for i in range(4)]
    if dist != [2,2,2,2]: err(f"{m['id']} quiz dist {dist}")
    for q in m['quiz']:
        if set(q.keys()) != {"q","choices","answer","explain"}: err(f"{m['id']} quiz keys: {set(q.keys())}")
        if len(q['choices']) != 4 or not (0 <= q['answer'] <= 3): err(f"{m['id']} quiz choice/answer")
    if not isinstance(m['weight'], int): err(f"{m['id']} weight")
    if not isinstance(m['prerequisiteFor'], list) or not m['prerequisiteFor']: err(f"{m['id']} prerequisiteFor")

# 2. prerequisiteFor targets reference known ids (existing 40 + new 11 + tool lab ids)
known = {f'IL26-M{i:02d}' for i in list(range(1, 26)) + list(range(26, 41))} | set(ids) | \
        {f'IL26-TL-0{i}' for i in range(1, 9)}
for m in modules:
    for t in m['prerequisiteFor']:
        if t not in known: err(f"{m['id']} prerequisiteFor unknown target {t}")

# 3. toolLabs chain
labs = fragment['toolLabs']
if [l['chain'] for l in labs] != list(range(1, 9)): err('chain order')
lab_ids = [l['id'] for l in labs]
for l in labs:
    for k in ["id","title","chain","moduleId","requiresInstall","requiresLab","brief","steps","deliverable","checkpoint","datasetRef"]:
        if k not in l: err(f"{l['id']} missing {k}")
    if l['moduleId'] not in known: err(f"{l['id']} moduleId {l['moduleId']}")
    if l['requiresLab'] is not None and l['requiresLab'] not in lab_ids: err(f"{l['id']} requiresLab")
    if l['datasetRef'] not in ('inline', None): err(f"{l['id']} datasetRef")
# chain linkage: each lab's requiresLab == previous lab (except first null)
for i, l in enumerate(labs):
    want = None if i == 0 else labs[i-1]['id']
    if l['requiresLab'] != want: err(f"{l['id']} requiresLab should be {want}")

# 4. datasets
for ds in fragment['datasets']:
    if len(ds['rows']) > 15: err(f"{ds['name']} >15 rows")
    if not all(len(r) == len(ds['columns']) for r in ds['rows']): err(f"{ds['name']} ragged rows")
    if 'fictional' not in ds['note']: err(f"{ds['name']} note")

# 5. multicloud labs
for lab in fragment['multicloudLabs']:
    for k in ["id","title","cloud","brief","steps","workload","costGuardrails","cleanup","checkpoint"]:
        if k not in lab: err(f"{lab['id']} missing {k}")
    if not any('delet' in s.lower() for s in lab['cleanup']): err(f"{lab['id']} cleanup lacks deletion")

# 6. installSteps resolve
have_inst = {s['id'] for s in fragment['installSteps']}
for l in labs:
    for r in l['requiresInstall']:
        if r not in have_inst: err(f"{l['id']} install ref {r}")

# 7. external URLs: only curl-verified (200) URLs allowed; namespace URIs that
#    fail verification were replaced with URNs. Verified 2026-10-07:
VERIFIED_URLS = {"http://www.w3.org/1999/XSL/Transform"}  # curl -> 200 (standard XSLT namespace)
blob = json.dumps(fragment)
urls = set(re.findall(r'https?://[^\s"\\\]}]+', blob))
# template placeholders (containing <...>) are not real destinations
urls = {u for u in urls if '<' not in u and '>' not in u}
unverified = urls - VERIFIED_URLS
if unverified: err(f'unverified external URLs: {sorted(unverified)[:5]}')

# 8. no vendor affiliation / certification-conferral claims in prose or correct answers
#    (quiz distractors are exempt: they test that learners REJECT the claim)
banned = ['certified by', 'certification from', 'endorsed by microsoft', 'microsoft endorses',
          'confers a certification', 'official certification', 'accredited']
prose_bits = []
for m in modules:
    prose_bits += [m['summary'], m['title']]
    prose_bits += [n['title'] + ' ' + n['body'] for n in m['notes']]
    prose_bits += [c['back'] for c in m['cards']]
    for q in m['quiz']:
        prose_bits.append(q['choices'][q['answer']])  # correct choice only
        prose_bits.append(q['explain'])
for l in labs:
    prose_bits += [l['title'], l['brief'], l['deliverable'], ' '.join(l['steps'])]
for lab in fragment['multicloudLabs']:
    prose_bits += [lab['title'], lab['brief'], lab['workload']]
low = ' '.join(prose_bits).lower()
hits = [b for b in banned if b in low]
if hits: err(f'claim phrases in prose/correct answers: {hits}')

if errs:
    print('VALIDATION FAILED:')
    for e in errs: print(' -', e)
    raise SystemExit(1)

with open(BASE + 'tool-labs.json', 'w') as f:
    json.dump(fragment, f, indent=2)
print('tool-labs.json written OK')
print('modules:', len(modules), '| toolLabs:', len(labs), '| datasets:', len(fragment['datasets']),
      '| multicloudLabs:', len(fragment['multicloudLabs']), '| installSteps:', len(fragment['installSteps']))
import os
print('bytes:', os.path.getsize(BASE + 'tool-labs.json'))
# final json.load roundtrip
json.load(open(BASE + 'tool-labs.json'))
print('json.load roundtrip: valid')
