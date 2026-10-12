#!/usr/bin/env python3
"""Fix IL-29 gate-threatlocker-operator framing to carry explicit independent-prep wording."""
import json, os, shutil

p = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-29-threatlocker-ai-cybersecurity-mastery.json')
d = json.load(open(p))
old = ("Internal operator-readiness assessment for the IT Infrastructure Specialist / Cyber Hero support role. "
 "This is not a ThreatLocker certification and confers no credential; it measures whether you can do the job's core tasks. "
 "Not affiliated with, endorsed by, or sponsored by ThreatLocker.")
new = ("Independent operator-readiness preparation and assessment for the IT Infrastructure Specialist / Cyber Hero support role. "
 "This is not a ThreatLocker certification and confers no credential; it measures whether you can do the job's core tasks. "
 "Not affiliated with, endorsed by, or sponsored by ThreatLocker.")
found = False
for g in d['certGates']:
    if g['id'] == 'gate-threatlocker-operator':
        assert g['framing'] == old, 'framing text mismatch: %r' % g['framing'][:80]
        g['framing'] = new
        found = True
assert found, 'gate not found'
tmp = p + '.tmp'
with open(tmp, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')
json.load(open(tmp))
os.replace(tmp, p)
print('framing fixed; updatedAt stays', d['updatedAt'])
