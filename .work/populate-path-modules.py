#!/usr/bin/env python3
"""Populate empty path modules in catalog shards from course JSON modules.
Maps each of the 29 empty-module paths to its course's real modules,
converted to the path-module summary format used by university/path.html.
"""
import json, glob, re, sys, shutil, os

DOCS = os.path.expanduser('~/workspace/apex-audit/docs')

def load_course(fname):
    with open(os.path.join(DOCS, 'university/data/courses', fname)) as f:
        return json.load(f)

def distill_topics(mod, n=4):
    """Derive topic phrases from objectives (first clause of each)."""
    topics = []
    for o in (mod.get('objectives') or []):
        # take text before first colon/comma/period, cap length
        t = re.split(r'[:;.]', o, 1)[0].strip()
        t = re.sub(r'^(Define|Explain|Describe|Understand|Learn|Identify|Compare|Apply|Build|Create|Analyze|Demonstrate|Explore|Master)\s+', '', t, flags=re.I)
        t = t[:70].strip()
        if t and t not in topics:
            topics.append(t)
        if len(topics) >= n:
            break
    # fallback: crossLinks
    if not topics:
        for c in (mod.get('crossLinks') or [])[:n]:
            s = c if isinstance(c, str) else c.get('title', '')
            if s: topics.append(s[:70])
    return topics

def build_sources(mod, course_links, n=2):
    srcs = []
    for v in (mod.get('videos') or [])[:n]:
        if isinstance(v, dict) and v.get('url'):
            srcs.append({'name': v.get('source') or v.get('title', 'Video')[:60],
                         'url': v['url'],
                         'note': (v.get('title') or '')[:120]})
    if not srcs:
        for s in (course_links or [])[:n]:
            if isinstance(s, dict) and s.get('url'):
                srcs.append({'name': s.get('name', 'Reference')[:60], 'url': s['url'],
                             'note': (s.get('note') or '')[:120]})
    return srcs

def build_il_provides(mod):
    s = (mod.get('summary') or '').strip()
    if s:
        return s[:400]
    t = mod.get('title', '')
    o = (mod.get('objectives') or [''])[0]
    return ("I teach %s. %s" % (t, o))[:400]

def to_path_module(mod, course_links):
    return {
        'id': mod.get('id', ''),
        'title': mod.get('title', ''),
        'kind': 'core',
        'topics': distill_topics(mod),
        'sources': build_sources(mod, course_links),
        'il_provides': build_il_provides(mod),
    }

def phase_chunks(mods, size=4):
    """Group module ids into phases with honest derived names."""
    phases = []
    for i in range(0, len(mods), size):
        chunk = mods[i:i+size]
        first = chunk[0].get('title', '')
        last = chunk[-1].get('title', '')
        name = 'Phase %d — %s' % (len(phases)+1, first[:50])
        phases.append({
            'name': name,
            'weeks': '',
            'topics': [m.get('title','')[:60] for m in chunk],
            'outcome': 'Outcome: complete %s through %s with working hands-on evidence.' % (first[:40], last[:40]),
        })
    return phases

# ---- mapping: (shard_file, path_id, course_file, [module ids or 'ALL' or prefix list]) ----
COURSES = {
    'IL-19': 'il-19-multicloud-devops-ai-bootcamp.json',
    'IL-20': 'il-20-mathematics.json',
    'IL-21': 'il-21-humanities.json',
    'IL-22': 'il-22-esoteric-secret-knowledge.json',
    'IL-23': 'il-23-frontier-knowledge.json',
    'IL-24': 'il-24-threatlocker-assessment-prep-cbt.json',
    'IL-25': 'il-25-cybersecurity-professional-certificate.json',
    'IL-26': 'il-26-data-analyst-certification-senior-mastery.json',
    'IL-27': 'il-27-it-infrastructure-specialist-threatlocker-mastery.json',
    'IL-28': 'il-28-devsecops-cloud-infrastructure-mastery.json',
    'IL-29': 'il-29-threatlocker-ai-cybersecurity-mastery.json',
    'IL-30': 'il-30-post-quantum-cryptography-quantum-safe.json',
    'IL-31': 'il-31-ai-red-teaming-safety-evals.json',
}

def prefix(ids, *pfx):
    return [i for i in ids if any(i.startswith(p) for p in pfx)]

MAPPING = {
    # IL-19
    'il19-computing-fundamentals': ('IL-19', prefix, ('CF-',)),
    'il19-aws-cloud':              ('IL-19', prefix, ('AWS-',)),
    'il19-azure-cloud':            ('IL-19', prefix, ('AZ-',)),
    'il19-google-cloud':           ('IL-19', prefix, ('GCP-',)),
    'il19-oracle-cloud':           ('IL-19', prefix, ('OCI-',)),
    'il19-devops-cloud':           ('IL-19', prefix, ('DO-',)),
    'il19-ai-cloud':               ('IL-19', prefix, ('AI-',)),
    'il19-career-strategy':        ('IL-19', prefix, ('CS-',)),
    'il19-certification-maps':     ('IL-19', prefix, ('CM-',)),
    'il19-guided-missions':        ('IL-19', prefix, ('IL-19-PM-',)),
    # IL-20
    'il20-discrete-foundations':   ('IL-20', ['IL-20-M00','m20-sets-logic','m20-proof-methods','m20-counting','m20-relations-functions']),
    'il20-algebra-calculus-core':   ('IL-20', ['m20-linear-algebra-1','m20-linear-algebra-2','m20-linear-algebra-3','m20-calculus-1','m20-calculus-2','m20-series','m20-multivariable']),
    'il20-probability-computation': ('IL-20', ['m20-probability','m20-statistics','m20-graphs-recurrence','m20-numerical-methods','m20-linear-systems-optimization','il20-ocw-togo-20261009']),
    # IL-21
    'il21-philosophy-ethics':      ('IL-21', ['m21-what-is-philosophy','m21-logic-argument','m21-ethics-1','m21-ethics-2','m21-epistemology','IL-21-PM-LOGIC']),
    'il21-history-science-tech':    ('IL-21', ['m21-history-science-1','m21-history-science-2','m21-history-tech']),
    'il21-writing-economics-law':   ('IL-21', ['m21-technical-writing','m21-rhetoric','m21-economics-1','m21-economics-2','m21-law-policy','m21-synthesis','IL-21-PM-STATS','il21-ocw-togo-20261009']),
    # IL-22
    'il22-western-mystery-traditions': ('IL-22', ['m22-approaching','m22-kabbalah','m22-hermeticism','m22-alchemy','m22-rosicrucianism','m22-theosophy','m22-golden-dawn','IL-22-PM-NUMTH']),
    'il22-divination-practices':    ('IL-22', ['m22-astrology','m22-tarot','m22-enochian','m22-divination','m22-symbolism']),
    'il22-orders-modern-occultism': ('IL-22', ['m22-grimoires','m22-gnosticism','m22-eastern-esoteric','m22-modern-revival','IL-22-PM-LOGIC']),
    # IL-23
    'il23-bio-energy-frontier':    ('IL-23', ['m23-crispr','m23-fusion','m23-synbio','m23-blockchain-finance','IL-23-PM-STATS','il23-ocw-togo-20261009']),
    'il23-compute-space-frontier':  ('IL-23', ['m23-transformers','m23-quantum','m23-bci','m23-agents','m23-semiconductors','m23-space','m23-frontier-method','m23-epoch-ai','m23-metr-evals','IL-23-PM-LINALG','IL-23-PM-LOGIC']),
    # IL-24..IL-31 core paths -> ALL modules
    'il-24-core-path': ('IL-24', 'ALL'),
    'il-25-core-path': ('IL-25', 'ALL'),
    'il-26-core-path': ('IL-26', 'ALL'),
    'il-27-core-path': ('IL-27', 'ALL'),
    'il-28-core-path': ('IL-28', 'ALL'),
    'il-29-core-path': ('IL-29', 'ALL'),
    'il-30-core-path': ('IL-30', 'ALL'),
    'il-31-core-path': ('IL-31', 'ALL'),
}

# pre-load courses
course_cache = {}
def get_course(code):
    if code not in course_cache:
        course_cache[code] = load_course(COURSES[code])
    return course_cache[code]

def resolve_modules(code, spec):
    d = get_course(code)
    mods = d['modules']
    links = d.get('sourceLinks', [])
    if spec == 'ALL':
        return [(m, links) for m in mods]
    if isinstance(spec, tuple) and spec[0] is prefix:
        ids = prefix([m['id'] for m in mods], *spec[1:])
        by_id = {m['id']: m for m in mods}
        return [(by_id[i], links) for i in ids if i in by_id]
    by_id = {m['id']: m for m in mods}
    out = []
    for i in spec:
        if i in by_id:
            out.append((by_id[i], links))
        else:
            print('  WARN: module id not found:', code, i)
    return out

def main():
    changed_files = []
    total_paths = 0
    total_modules = 0
    for f in sorted(glob.glob(os.path.join(DOCS, 'university/data/catalog/shard-*.json'))):
        with open(f) as fh:
            d = json.load(fh)
        dirty = False
        for p in d.get('paths', []):
            pid = p.get('id')
            if pid in MAPPING and not p.get('modules'):
                entry = MAPPING[pid]
                code = entry[0]
                spec = entry[1] if len(entry) == 2 else entry[1:]
                resolved = resolve_modules(code, spec)
                if not resolved:
                    print('WARN: no modules resolved for', pid)
                    continue
                p['modules'] = [to_path_module(m, links) for m, links in resolved]
                # add phases for the IL-19 cloud bootcamp paths (clean module ranges)
                if pid.startswith('il19-') and pid not in ('il19-guided-missions',):
                    p['phases'] = phase_chunks([m for m, _ in resolved], size=4)
                dirty = True
                total_paths += 1
                total_modules += len(resolved)
                print('POPULATED %s <- %s (%d modules)' % (pid, code, len(resolved)))
        if dirty:
            bak = f + '.pathmod-bak'
            shutil.copy2(f, bak)
            with open(f, 'w') as fh:
                json.dump(d, fh, indent=1, ensure_ascii=False)
                fh.write('\n')
            # validate
            json.load(open(f))
            changed_files.append(f)
    print('---')
    print('paths populated:', total_paths)
    print('modules added:', total_modules)
    print('files changed:', changed_files)

if __name__ == '__main__':
    main()
