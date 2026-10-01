import json, glob, sys

ok = True
for f in sorted(glob.glob('/tmp/apex-audit/distill-partial/distill-*.json')):
    try:
        d = json.load(open(f))
    except Exception as e:
        print(f, 'JSON PARSE FAIL', e); ok = False; continue
    name = f.split('/')[-1]
    errs = []
    if not 6 <= len(d['modules']) <= 10:
        errs.append(f"modules={len(d['modules'])}")
    for i, m in enumerate(d['modules']):
        if not 3 <= len(m['objectives']) <= 5: errs.append(f"m{i} objectives={len(m['objectives'])}")
        if not 5 <= len(m['keyConcepts']) <= 8: errs.append(f"m{i} keyConcepts={len(m['keyConcepts'])}")
        if not 3 <= len(m['labs']) <= 5: errs.append(f"m{i} labs={len(m['labs'])}")
        if not 2 <= len(m['checkpoints']) <= 4: errs.append(f"m{i} checkpoints={len(m['checkpoints'])}")
        if not m.get('sourceRefs'): errs.append(f"m{i} no sourceRefs")
    for req in ('id', 'title', 'sourceUrl', 'disclaimer'):
        if not d.get(req): errs.append(f"missing {req}")
    status = 'OK' if not errs else 'SCHEMA FAIL: ' + '; '.join(errs)
    if errs: ok = False
    print(f"{name}: id={d['id']} modules={len(d['modules'])} unverified={len(d.get('unverifiedUrls', []))} {status}")

print('ALL_OK' if ok else 'SOME_FAILED')
