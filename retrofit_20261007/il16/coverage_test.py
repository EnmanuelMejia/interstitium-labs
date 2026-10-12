import json, re

STOP = set("""the a an and or of to in on for with as is are be by from that this it you your we our
at vs not into over under out all any can will do does did have has had which what when where how why
who whom whose their there then than so such no nor too very just about after before between during
each other some most more then also its it's than them they than then""".split())

def words(s):
    return [w for w in re.findall(r"[a-zA-Z0-9']+", s.lower()) if w not in STOP and len(w) > 2]

def overlap(a, b):
    return len(set(words(a)) & set(words(b)))

def first_sentences(s, n=1):
    parts = re.split(r'(?<=[.!?])\s+', s.strip())
    parts = [p for p in parts if p]
    return ' '.join(parts[:n])

def cap1(s):
    s = s.strip()
    return s[:1].upper() + s[1:] if s else s

d = json.load(open('/home/hatch/workspace/apex-audit/docs/university/data/courses/il-16-machine-learning-ai-engineering.json'))

# build pool per module and test glossary + step coverage
miss_gloss = []
miss_step = []
for m in d['modules']:
    if 're-bench' in m['id']:
        continue
    pool = []  # (label, text)
    for c in m['cards']:
        pool.append(('card', c['front'] + ' ' + c['back']))
    for q in m['quiz']:
        pool.append(('quiz', q['q'] + ' ' + q['explain'] + ' ' + ' '.join(q['choices'])))
    for o in m['objectives']:
        pool.append(('obj', o))
    pool.append(('how', m['notes'][1]['body']))
    pool.append(('sum', m['summary']))
    bullets = [b.strip()[2:].strip() for b in m['notes'][0]['body'].split('\n')]
    for t in bullets:
        if ': ' in t or ' \u2014 ' in t:
            continue
        best, bs = None, 0
        for kind, text in pool:
            o = overlap(t, text)
            if o > bs:
                best, bs = (kind, text), o
        if bs < 2:
            miss_gloss.append((m['id'], t))
    for o in m['objectives']:
        best, bs = None, 0
        for kind, text in pool:
            if kind == 'obj' and text == o:
                continue
            sc = overlap(o, text)
            if sc > bs:
                best, bs = (kind, text), sc
        if bs < 2:
            miss_step.append((m['id'], o))

print('glossary misses:', len(miss_gloss))
for mid, t in miss_gloss:
    print('  G', mid, '|', t)
print('step misses:', len(miss_step))
for mid, t in miss_step:
    print('  S', mid, '|', t[:90])
