#!/usr/bin/env python3
"""Add missing canonical module keys (prerequisiteFor=[], mockTask=null) where absent. No content invented."""
import json, os

COURSES = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
FILES = {
 'IL-26': 'il-26-data-analyst-certification-senior-mastery.json',
 'IL-27': 'il-27-it-infrastructure-specialist-threatlocker-mastery.json',
 'IL-28': 'il-28-devsecops-cloud-infrastructure-mastery.json',
 'IL-29': 'il-29-threatlocker-ai-cybersecurity-mastery.json',
}
log = {}
for code, f in FILES.items():
    p = os.path.join(COURSES, f)
    d = json.load(open(p))
    n_pf = n_mt = 0
    for m in d['modules']:
        if 'prerequisiteFor' not in m:
            m['prerequisiteFor'] = []
            n_pf += 1
        if 'mockTask' not in m:
            m['mockTask'] = None
            n_mt += 1
    if n_pf or n_mt:
        tmp = p + '.tmp'
        with open(tmp, 'w') as fh:
            json.dump(d, fh, indent=2, ensure_ascii=False)
            fh.write('\n')
        json.load(open(tmp))
        os.replace(tmp, p)
    log[code] = (n_pf, n_mt)
    print(code, 'added prerequisiteFor:', n_pf, '| mockTask:', n_mt)
print('done')
