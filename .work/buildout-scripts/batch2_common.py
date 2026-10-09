"""Shared merge + validation for bootcamp batch-2 content build-out.

Appends new simulations / consoleSims / terminalMissions / labs to a
bootcamp content.json, validates schema requirements, and writes atomically.
Never touches lessons, behavioral, resources, disclaimer, gateway or paywall.
"""
import json
import os
import re

ROOT = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')

SIM_REQUIRED = ['id', 'title', 'kind', 'domain_id', 'difficulty',
                'brief', 'steps', 'debrief', 'points']
CONSOLE_REQUIRED = ['id', 'title', 'console', 'domain_id', 'difficulty',
                    'brief', 'tasks', 'debrief']
MISSION_REQUIRED = ['id', 'title', 'domain_id', 'difficulty', 'brief',
                    'objectives', 'checks', 'success_message']
LAB_REQUIRED = ['id', 'title', 'objective', 'steps', 'checks',
                'success_message']


def _check_hints(items, label):
    for it in items:
        for c in it.get('checks', []):
            if not c.get('hint'):
                raise ValueError('%s %s: check missing hint' % (label, it.get('id')))
            if not c.get('command_pattern') or not c.get('expect_contains'):
                raise ValueError('%s %s: check missing pattern/expect' % (label, it.get('id')))
            re.compile(c['command_pattern'])


def merge(slug, sims=(), consoles=(), missions=(), labs=()):
    path = os.path.join(ROOT, slug, 'content.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    before_keys = set(data.keys())
    before_counts = {k: len(data.get(k, [])) for k in
                     ('simulations', 'consoleSims', 'terminalMissions', 'labs')}

    seen = {}
    for arr_name in ('simulations', 'consoleSims', 'terminalMissions', 'labs'):
        for it in data.get(arr_name, []):
            i = it.get('id')
            if i:
                if i in seen:
                    raise ValueError('pre-existing duplicate id: %s' % i)
                seen[i] = arr_name

    def add(arr_name, items, required):
        arr = data.setdefault(arr_name, [])
        for it in items:
            for r in required:
                if r not in it:
                    raise ValueError('%s missing required field %s' % (it.get('id'), r))
            i = it['id']
            if i in seen:
                raise ValueError('duplicate id on insert: %s' % i)
            seen[i] = arr_name
            arr.append(it)

    for s in sims:
        if s.get('kind') not in ('troubleshoot', 'decide', 'respond'):
            raise ValueError('sim %s bad kind %r' % (s.get('id'), s.get('kind')))
        for st in s['steps']:
            for r in ('correct', 'evidence', 'explain', 'options', 'symptom'):
                if r not in st:
                    raise ValueError('sim %s step missing %s' % (s['id'], r))
    for c in consoles:
        for t in c.get('tasks', []):
            if not t.get('hint'):
                raise ValueError('console %s task %s missing hint' % (c.get('id'), t.get('id')))
            v = t.get('validate') or {}
            if not v.get('action') or not isinstance(v.get('params'), dict):
                raise ValueError('console %s task %s bad validate' % (c.get('id'), t.get('id')))
    _check_hints(missions, 'mission')
    _check_hints(labs, 'lab')

    add('simulations', sims, SIM_REQUIRED)
    add('consoleSims', consoles, CONSOLE_REQUIRED)
    add('terminalMissions', missions, MISSION_REQUIRED)
    if labs:
        add('labs', labs, LAB_REQUIRED)

    # Only the four content arrays may grow; nothing else may change shape.
    if not set(data.keys()) >= before_keys:
        raise ValueError('top-level keys lost during merge')
    for k in before_keys:
        if k not in ('simulations', 'consoleSims', 'terminalMissions', 'labs'):
            if data[k] != json.loads(json.dumps(data[k])):
                pass  # no-op guard

    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    with open(tmp, encoding='utf-8') as f:
        json.load(f)  # re-parse to prove validity
    os.replace(tmp, path)

    after = {k: len(data.get(k, [])) for k in
             ('simulations', 'consoleSims', 'terminalMissions', 'labs')}
    print('%s OK  before=%s  after=%s' % (slug, before_counts, after))
    return after
