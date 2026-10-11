#!/usr/bin/env python3
"""Part 5: course-level final validation for IL-22 retrofit. Read-only except
fixing anything actually broken."""
import json, re

PATH = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-22-esoteric-secret-knowledge.json'
d = json.load(open(PATH))

print('== course-level key check ==')
for k in ['schemaVersion','courseId','code','title','tagline','blurb','hours','updatedAt',
          'objectives','arc','priorities','battlePlan','modules','mockMinutes','mockTasks',
          'cheatSheets','answerBank','sourceLinks','honestyNote']:
    v = d.get(k, '<MISSING>')
    print(' ', k, '->', ('MISSING' if v == '<MISSING>' else ('list[%d]' % len(v) if isinstance(v, list) else repr(v)[:60])))

print()
print('mockMinutes type:', type(d['mockMinutes']).__name__, '=', d['mockMinutes'])
assert isinstance(d['mockMinutes'], int)

print()
print('== sourceLinks retrieved dates ==')
for s in d['sourceLinks']:
    assert s.get('retrieved'), s
    print(' ', s['retrieved'], s['name'][:60])

print()
print('== glossary bullet shape check (first Concepts body per module) ==')
bad_gl = 0
for m in d['modules']:
    body = m['notes'][0]['body']
    bullets = [l for l in body.split('\n') if l.startswith('- **')]
    for b in bullets:
        if not re.match(r'^- \*\*[^*]+\*\* \u2014 .+', b):
            print('  BAD:', m['id'], b[:80]); bad_gl += 1
    if len(bullets) < 6:
        print('  FEW:', m['id'], len(bullets)); bad_gl += 1
print('glossary issues:', bad_gl)

print()
print('== hands-on procedure numbered steps check ==')
for m in d['modules']:
    body = m['notes'][1]['body']
    steps = [l for l in body.split('\n') if re.match(r'^\d+\. ', l)]
    if len(steps) < 4:
        print('  FEW STEPS:', m['id'], len(steps))

print()
print('== honesty-note section non-empty ==')
for m in d['modules']:
    assert m['notes'][3]['title'] == 'Honesty note' and len(m['notes'][3]['body']) > 100, m['id']

print()
print('== brand / forbidden-content scan ==')
text = json.dumps(d, ensure_ascii=False)
brands = ['ALEKS', 'Brilliant', 'Khan Academy', 'Coursera', 'Udemy', 'edX', 'edX.org',
          'Palantir', 'NSA', 'National Security Agency']
hits = [(b, text.count(b)) for b in brands if b in text]
print('forbidden hits:', hits if hits else 'none')

print()
print('== video references in quiz explains (course has no videos) ==')
vhits = []
for m in d['modules']:
    for q in m['quiz']:
        if re.search(r'\bvideo\b', q['explain'], re.I):
            vhits.append((m['id'], q['q'][:60]))
print('video refs:', vhits if vhits else 'none')

print()
print('== preserved-content spot checks ==')
spots = [
    "Casaubon's philology (1614)",
    'Keter (crown), Chokhmah (wisdom)',
    'The Kybalion',
    'solve et coagula',
    "Ptolemy's *Tetrabiblos*",
    'Pamela Colman Smith',
    'Mysteriorum Libri',
    'Fama Fraternitatis',
    'Hodgson Report',
    'Cipher Manuscripts',
    'Ars Goetia',
    'Nag Hammadi',
    'Edward Said',
    'geomancy',
    'vesica piscis',
    'Do what thou wilt',
]
missing = [s for s in spots if s not in text]
print('missing preserved phrases:', missing if missing else 'none \u2014 all present')

print()
print('== quiz answer distribution ==')
from collections import Counter
c = Counter()
for m in d['modules']:
    for q in m['quiz']:
        c[q['answer']] += 1
print(dict(c))
