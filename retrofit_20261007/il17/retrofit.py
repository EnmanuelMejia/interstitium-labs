#!/usr/bin/env python3
"""Retrofit IL-17 course file to the IL-19 Multicloud template shape.
Reads:  docs/university/data/courses/il-17-agentic-ai-engineering.json
Writes: same path (atomic), after json.load validation before AND after.
"""
import json, os, re, sys

BASE = os.path.expanduser('~/workspace/apex-audit')
COURSE = BASE + '/docs/university/data/courses/il-17-agentic-ai-engineering.json'
sys.path.insert(0, os.path.join(BASE, 'retrofit_20261007', 'il17'))
from content17 import MODULES, CONCEPTS_EXTRA

TRACK_TITLES = {
 'agentic-ai-foundations': 'Agentic AI Foundations',
 'agentic-ai-for-swe': 'Agentic AI for Software Engineers',
 'agentic-ai-for-data': 'Agentic AI for Data Engineers',
 'agentic-ai-for-pm': 'Agentic AI for Product Managers',
 'agentic-ai-for-leaders': 'Agentic AI for TPMs & Engineering Managers',
 'agentic-ai-for-iv': 'Agentic AI Interview Prep',
 'agentic-ai-lowcode': 'Low-Code Agentic AI',
}

BANNED = re.compile(r'aleks|brilliant|khan academy|coursera|udemy|\bedx\b|palantir|\bnsa\b', re.I)

def words(s):
    return set(re.findall(r'[a-z]{3,}', s.lower()))

def topics_of(m):
    return [l[2:].strip() for l in m['notes'][0]['body'].split('\n') if l.startswith('- ')]

def build_summary(m, track_title, idx, total):
    blurb = m['notes'][1]['body'].strip()
    blurb = re.sub(r'^[Ii]n this module:\s*', '', blurb)
    blurb = blurb[0].lower() + blurb[1:]
    blurb = blurb.rstrip()
    if not blurb or blurb[-1] not in '.!?':
        blurb += '.'
    topics = topics_of(m)
    tstr = topics[0] if len(topics) == 1 else '; '.join(topics[:-1]) + '; and ' + topics[-1]
    return (f"Welcome to {m['title']} — module {idx} of {total} in the {track_title} "
            f"track of IL-17 Agentic AI Engineering. I'm your instructor. "
            f"In this module we cover {blurb} We'll work through {tstr}.")

def build_concepts(m, key):
    topics = topics_of(m)
    cards = m['cards']
    out = []
    for t in topics:
        extra = CONCEPTS_EXTRA.get((key, t))
        if extra is not None:
            defn = extra
            if defn.startswith(t):
                defn = defn[len(t):].lstrip(' —-')
            out.append(f"- **{t}** — {defn}")
            continue
        tw = words(t)
        best, bs = None, -1
        for c in cards:
            o = len(tw & (words(c['front']) | words(c['back'])))
            if o > bs:
                bs, best = o, c
        assert best is not None and bs >= 0, (key, t)
        out.append(f"- **{t}** — {best['back']}")
    return '\n'.join(out)

def build_sec2(m, key, a):
    sources = m['notes'][2]['body'].strip()
    if a['sec2'] == 'Hands-on procedure':
        intro = "This is the lab sequence — work the steps in order; each one builds on the last."
        steps = '\n'.join(f"{i+1}. {s}" for i, s in enumerate(a['procedure']))
        body = f"{intro}\n{steps}\n\nReference docs for this module:\n{sources}"
        code, lang = a.get('code', ('', ''))
        return {'title': 'Hands-on procedure', 'body': body, 'code': code, 'lang': lang}
    intro = ("Before you trust the narrative, work the numbers. "
             "The example below is illustrative — every assumption is labeled so you can substitute your own.")
    body = f"{intro}\n\n{a['estimation']}\n\nReference docs for this module:\n{sources}"
    return {'title': 'Worked estimation', 'body': body, 'code': '', 'lang': ''}

def main():
    with open(COURSE) as f:
        d = json.load(f)  # validate BEFORE

    track_counts = {}
    track_totals = {}
    for m in d['modules']:
        tr = m['id'].split('--')[0]
        track_totals[tr] = track_totals.get(tr, 0) + 1

    for m in d['modules']:
        key = m['id'].split('--')[1]
        tr = m['id'].split('--')[0]
        assert key in MODULES, f"no authored content for {key}"
        a = MODULES[key]
        track_counts[tr] = track_counts.get(tr, 0) + 1
        idx = track_counts[tr]

        m['summary'] = build_summary(m, TRACK_TITLES[tr], idx, track_totals[tr])
        sec2 = build_sec2(m, key, a)
        m['notes'] = [
            {'title': 'Concepts', 'body': build_concepts(m, key)},
            sec2,
            {'title': 'Project brief', 'body': a['project']},
            {'title': 'Honesty note', 'body': a['honest']},
        ]
        sec_name = a.get('quiz_sec', 'Concepts')
        for q in m['quiz']:
            q['explain'] = q['explain'].rstrip() + f" See {sec_name}."
        # validate module shape
        assert [n['title'] for n in m['notes']] == ['Concepts', a['sec2'], 'Project brief', 'Honesty note'], key
        assert len(m['cards']) >= 5, key
        assert len(m['quiz']) >= 4, key
        for q in m['quiz']:
            assert isinstance(q['choices'], list) and len(q['choices']) == 4, (key, q['q'])
            assert isinstance(q['answer'], int) and 0 <= q['answer'] <= 3, (key, q['q'])
            assert q['explain'].strip(), (key, q['q'])
        blob = m['summary'] + ''.join(n['body'] for n in m['notes'])
        bad = BANNED.search(blob)
        assert not bad, (key, bad.group(0))

    # ---- course-level ----
    for cs in d['cheatSheets']:
        for b in cs['blocks']:
            b.setdefault('code', '')
            b.setdefault('lang', '')
    seen, deduped = set(), []
    for s in d['sourceLinks']:
        k = (s.get('name'), s.get('url'))
        if k in seen:
            continue
        seen.add(k)
        if not s.get('retrieved'):
            s['retrieved'] = '2026-10-07'
        deduped.append(s)
    d['sourceLinks'] = deduped
    for bp in d['battlePlan']:
        assert all(k in bp for k in ('id', 'title', 'minutes', 'detail')), bp
    for p in d['priorities']:
        assert all(k in p for k in ('label', 'minutes')), p
    assert isinstance(d['mockMinutes'], int)
    assert d['honestyNote'].strip()
    assert d['arc'] and d['mockTasks'] and d['cheatSheets'] and d['answerBank']

    tmp = COURSE + '.retrofit_tmp'
    with open(tmp, 'w') as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write('\n')
    with open(tmp) as f:
        json.load(f)  # validate AFTER
    os.replace(tmp, COURSE)
    print(f"retrofitted {len(d['modules'])} modules; sourceLinks now {len(d['sourceLinks'])}")

if __name__ == '__main__':
    main()
