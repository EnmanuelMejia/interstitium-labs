import json, re, sys

slugs = ['active-directory-defense', 'ai-agent-sec', 'cybernetics',
         'secops-blue-team', 'security-graphs', 'tl-endpoint-ops',
         'zero-trust', 'adaptive-foundations']
allowed = {'sha256sum', 'cat', 'ls', 'echo', 'grep', 'head', 'tail',
           'sort', 'find', 'ps', 'wc', 'dig', 'ping', 'diff'}

problems = []
for s in slugs:
    p = '/home/hatch/workspace/cert-bootcamps/site/bootcamps/%s/content.json' % s
    d = json.load(open(p, encoding='utf-8'))
    if len(d.get('simulations', [])) != 5:
        problems.append((s, 'simulations != 5'))
    if len(d.get('consoleSims', [])) != 4:
        problems.append((s, 'consoleSims != 4'))
    if len(d.get('terminalMissions', [])) != 7:
        problems.append((s, 'terminalMissions != 7'))
    if s == 'ai-agent-sec' and len(d.get('labs', [])) != 5:
        problems.append((s, 'labs != 5'))
    ids = []
    for arr in ('simulations', 'consoleSims', 'terminalMissions', 'labs'):
        for it in d.get(arr, []):
            if isinstance(it, dict) and it.get('id'):
                ids.append(it['id'])
    if len(ids) != len(set(ids)):
        problems.append((s, 'duplicate ids'))
    for m in d['terminalMissions']:
        for c in m['checks']:
            if not c.get('hint'):
                problems.append((s, m['id'], 'mission check missing hint'))
            try:
                re.compile(c['command_pattern'])
            except Exception as e:
                problems.append((s, m['id'], 'bad regex: %s' % e))
            m2 = re.match(r'\^?([a-z0-9]+)', c['command_pattern'])
            if not m2 or m2.group(1) not in allowed:
                problems.append((s, m['id'], 'command not in allowed set: %s' % c['command_pattern'][:40]))
    for cs in d['consoleSims']:
        for t in cs['tasks']:
            if not t.get('hint'):
                problems.append((s, cs['id'], t['id'], 'task missing hint'))
    for l in d.get('labs', []):
        if isinstance(l, dict) and 'checks' in l:
            for c in l['checks']:
                if not c.get('hint'):
                    problems.append((s, l['id'], 'lab check missing hint'))
    if not d.get('disclaimer'):
        problems.append((s, 'disclaimer missing'))
    if len(d.get('resources', [])) != 4:
        problems.append((s, 'resources changed'))
    if len(d.get('behavioral', [])) != 8:
        problems.append((s, 'behavioral changed'))
    if len(d.get('lessons', [])) < 1:
        problems.append((s, 'lessons changed'))
    print('%s: sims=%d consoles=%d missions=%d labs=%d' % (
        s, len(d['simulations']), len(d['consoleSims']),
        len(d['terminalMissions']), len(d.get('labs', []))))

if problems:
    print('PROBLEMS:')
    for pr in problems:
        print(' ', pr)
    sys.exit(1)
print('ALL VALIDATION PASSED')
