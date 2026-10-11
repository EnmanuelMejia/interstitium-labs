#!/usr/bin/env python3
"""Retrofit shard-j.json: rewrite every module's il_provides as a 2-3 sentence
instructor-voice blurb, preserving the module's substance. Everything else untouched."""
import json, os, re
BASE = os.path.expanduser('~/workspace/apex-audit')
SHARD = BASE + '/docs/university/data/catalog/shard-j.json'
COURSE = BASE + '/docs/university/data/courses/il-17-agentic-ai-engineering.json'

VERB = [
    ('Understand and apply: ', 'understand and apply '),
    ('Practice: ', 'have practiced '),
    ('Build and demonstrate: ', 'have built and demonstrated '),
    ('Apply in professional practice: ', 'be applying '),
]

def lower1(s):
    if not s:
        return s
    if len(s) >= 2 and s[0].isupper() and s[1].isupper():
        return s  # acronym lead (JSON, SQL, DAG, STAR): keep as-is
    return s[0].lower() + s[1:]

def endot(s):
    s = s.rstrip()
    return s if s and s[-1] in '.!?' else s + '.'

with open(COURSE) as f:
    course = json.load(f)
# teaching blurb + objectives by short module key (from the PRE-retrofit notes is gone;
# rebuild blurb from summary: "In this module we cover X. We'll work through..." -> X)
teach = {}
for m in course['modules']:
    key = m['id'].split('--')[1]
    sm = re.search(r'In this module we cover (.+?) We\'ll work through ', m['summary'])
    blurb = sm.group(1) if sm else ''
    teach[key] = (blurb, m['objectives'])

with open(SHARD) as f:
    d = json.load(f)  # validate BEFORE

count = 0
for p in d['paths']:
    for mod in p['modules']:
        key = mod['id']
        assert key in teach, f"no course module for shard module {key}"
        blurb, objectives = teach[key]
        blurb = re.sub(r'^[Ii]n this module:\s*', '', blurb.strip())
        s1 = f"I'm your instructor for {mod['title']}."
        s2 = f"Together we cover {endot(lower1(blurb))}"
        obj = objectives[0]
        vp = None
        for prefix, verb in VERB:
            if obj.startswith(prefix):
                vp = verb + lower1(obj[len(prefix):])
                break
        assert vp, f"unmapped objective: {obj}"
        s3 = f"By the end, you'll {endot(vp)}"
        mod['il_provides'] = f"{s1} {s2} {s3}"
        # keep topics/sources intact; re-validate their shapes
        t = mod['topics']
        assert isinstance(t, list) and t and all(isinstance(x, str) for x in t), key
        for s in mod['sources']:
            assert s.get('name') and s.get('url') and s.get('note'), key
        count += 1

tmp = SHARD + '.retrofit_tmp'
with open(tmp, 'w') as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
    f.write('\n')
with open(tmp) as f:
    json.load(f)  # validate AFTER
os.replace(tmp, SHARD)
print(f"rewrote il_provides for {count} shard-j modules")
