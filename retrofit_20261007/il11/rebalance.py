"""Rebalance quiz answer indices across all IL-11 modules via deterministic choice rotation.
Preserves correctness; spreads answers evenly across 0-3. Also covers mockTasks."""
import json, os
from collections import Counter

SRC = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-11-zero-trust-endpoint-defense.json')

with open(SRC, encoding='utf-8') as f:
    course = json.load(f)

def rotate(q, target):
    ch = q['choices']
    cur = q['answer']
    shift = (cur - target) % 4  # rotate left by shift -> answer lands on target
    q['choices'] = ch[shift:] + ch[:shift]
    q['answer'] = target

g = 0
for m in course['modules']:
    for q in m['quiz']:
        rotate(q, g % 4)
        g += 1
for t in course['mockTasks']:
    rotate(t, g % 4)
    g += 1

# validate
errs = []
for m in course['modules']:
    for q in m['quiz']:
        assert len(q['choices']) == 4 and 0 <= q['answer'] <= 3 and q['explain'], 'bad quiz'
for t in course['mockTasks']:
    assert len(t['choices']) == 4 and 0 <= t['answer'] <= 3 and t['explain'], 'bad mock'

tmp = SRC + '.rebal-tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(course, f, ensure_ascii=False, indent=1)
    f.write('\n')
with open(tmp, encoding='utf-8') as f:
    json.load(f)
os.replace(tmp, SRC)

print('quiz answers:', dict(Counter(q['answer'] for m in course['modules'] for q in m['quiz'])))
print('mock answers:', dict(Counter(t['answer'] for t in course['mockTasks'])))
print('wrote OK')
