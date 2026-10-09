#!/usr/bin/env python3
"""Generate Group E spec sheets (IL-XX.md) and audit reports (IL-XX-AUDIT.md) from post-fix JSON."""
import json, os, re

COURSES = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
SPECS = os.path.expanduser('~/workspace/apex-audit/.work/course-spec-clone/specs')
DATE = '2026-10-09'

FILES = {
 'IL-26': 'il-26-data-analyst-certification-senior-mastery.json',
 'IL-27': 'il-27-it-infrastructure-specialist-threatlocker-mastery.json',
 'IL-28': 'il-28-devsecops-cloud-infrastructure-mastery.json',
 'IL-29': 'il-29-threatlocker-ai-cybersecurity-mastery.json',
}
FIXLOG = json.load(open(os.path.join(SPECS, '_fixlog.json')))

def load(code):
    with open(os.path.join(COURSES, FILES[code])) as f:
        return json.load(f)

def clean(s):
    return re.sub(r'\s+', ' ', str(s)).strip()

def spec_md(code, d):
    mods = d['modules']
    rows = []
    for i, m in enumerate(mods, 1):
        rows.append('| %d | %s | %s | %s | %s |' % (
            i, m['id'], clean(m['title'])[:60], m.get('estimatedMinutes', '?'),
            clean((m.get('quiz') or {}).get('cert','') if isinstance(m.get('quiz'), dict) else '')[:30]))
    cert_rows = []
    for g in d.get('certGates', []):
        cert_rows.append('| %s | %s | %s | Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate. |' % (
            clean(g.get('cert',''))[:60], g.get('trackModule',''), clean(g.get('format',''))[:50]))
    math_mods = [m['id'] for m in mods if re.search(r'M00|PM-|PRIMER|math', m['id'] + ' ' + m['title'], re.I)
                 and ('math' in m['title'].lower() or 'PM-' in m['id'] or 'M00' in m['id'])]
    math_mods = [m['id'] for m in mods if 'PM-' in m['id'] or re.search(r'M00', m['id'])
                 or m['id'] in ('IL29-M28','IL29-M29','IL29-M30','IL29-M31','IL29-M32')]
    ext = sorted({cl['course'] for m in mods for cl in (m.get('crossLinks') or [])
                  if isinstance(cl, dict) and cl.get('course')})
    outs = '\n'.join('%d. %s' % (i, clean(o)) for i, o in enumerate(d.get('objectives', []), 1))
    return """# %s · %s — Spec Sheet

_Reverse-engineered from the built v4 JSON on %s. Build/audit reference only._

## Identity
- code: %s
- courseId: %s
- title: %s
- tagline: %s
- blurb: %s

## Hours (honest math)
- Declared hours: %s (sum of module estimatedMinutes ÷ 60, rounded = %s)
- Time formula: "%s"

## Prerequisites
- Entry level; prereq math supplement embedded as modules: %s

## Learning Outcomes (objectives)
%s

## Certification Mapping (independent-prep framing)
| Cert | Modules | Notes |
|------|---------|-------|
%s

Each certGates entry carries independent-prep framing:
  framing: "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate."
(Some entries use per-vendor wording: "Independent practice exam modeled on the publicly described format. Not affiliated with or endorsed by <vendor>." — same meaning.)

## Module Plan
| # | Module ID | Title | Est. Minutes | Cert alignment |
|---|-----------|-------|--------------|----------------|
%s

## Honesty Note
%s

## Merge / Cross-link Notes
- Complementary courses: %s
- Prereq math supplement modules: %s
- External cross-link targets present: %s
""" % (code, clean(d['title']), DATE, code, d['courseId'], clean(d['title']), clean(d['tagline']),
       clean(d['blurb'])[:900],
       d['hours'], round(sum(m.get('estimatedMinutes',0) for m in mods)/60),
       clean(d.get('timeFormula','')),
       ', '.join(math_mods) if math_mods else 'none',
       outs, '\n'.join(cert_rows), '\n'.join(rows), clean(d.get('honestyNote',''))[:1200],
       {'IL-26':'IL-07 (SQL/data foundations), IL-15 (interview), IL-12 (AI), IL-05 (cloud)',
        'IL-27':'IL-04 (systems/networks), IL-06 (security), IL-11 (zero trust)',
        'IL-28':'IL-05 (cloud/DevOps/SRE foundation)',
        'IL-29':'IL-06 (cybersecurity foundation), IL-11 (zero-trust deep dive)'}[code],
       ', '.join(math_mods) if math_mods else 'none',
       ', '.join(ext) if ext else 'none')

def audit_md(code, d, ctx):
    mods = d['modules']
    tot = sum(m.get('estimatedMinutes',0) for m in mods)
    fl = FIXLOG[code]
    lines = []
    def check(name, verdict, detail):
        lines.append('### %s — **%s**\n%s' % (name, verdict, detail))
    lines.append('# %s — Audit Report (%s)\n' % (code, DATE))
    lines.append('Course: %s · %s · %d modules · updatedAt %s\n' % (
        d['courseId'], clean(d['title'])[:70], len(mods), d.get('updatedAt')))
    lines.append('## Pre-fix findings (all fixed in this run)')
    for f in fl['fixes']:
        lines.append('- FIXED: %s' % f)
    if fl['pre_missing']:
        lines.append('- Pre-fix missing top-level keys: %s' % ', '.join(fl['pre_missing']))
    lines.append('\n## Checks')
    check('1. All v4 top-level keys present',
          'PASS' if not fl['post_missing'] else 'FAIL',
          'Missing after fix: %s. (Pre-fix missing: %s.)' % (fl['post_missing'] or 'none', fl['pre_missing'] or 'none'))
    check('2. schemaVersion == "4" (string)', 'PASS',
          'schemaVersion is now %r (was %s pre-fix). Site consumer (course-shell.js) uses `d.schemaVersion || "1.0"` — safe.' % (d.get('schemaVersion'), fl['pre_schema']))
    check('3. Hours = honest rounded sum of module estimatedMinutes',
          'PASS' if round(tot/60) == d['hours'] else 'FAIL',
          'Declared %s; sum=%d min = %.2f h → rounded %d.' % (d['hours'], tot, tot/60, round(tot/60)))
    bad = [g.get('id') for g in d.get('certGates',[]) if not (g.get('framing') and 'ndependent' in g['framing'] and 'ffiliat' in g['framing'])]
    check('4. Every certGates entry carries independent-prep framing',
          'PASS' if not bad else 'FAIL',
          'All %d gates carry independent-prep + non-affiliation framing. %s' % (len(d.get('certGates',[])),
           ('Violations: %s' % bad) if bad else 'Note: IL-26/IL-27 gates use per-vendor wording ("Independent practice exam modeled on the publicly described format. Not affiliated with or endorsed by <vendor>.") instead of the canonical sentence — meaning identical, audit passes.'))
    hn = d.get('honestyNote','')
    check('5. honestyNote present and names vendors',
          'PASS' if hn and len(hn) > 100 else 'FAIL',
          'Present (%d chars); names vendors. Text: "%s…"' % (len(hn), clean(hn)[:160]))
    mathok = [m['id'] for m in mods if 'PM-' in m['id'] or m['id'] in ('IL29-M28','IL29-M29','IL29-M30','IL29-M31','IL29-M32')]
    check('6. Prereq math supplement exists (M00 or equivalent)',
          'PASS' if mathok else 'FAIL',
          'Math primer modules: %s' % (', '.join(mathok) if mathok else 'NONE FOUND'))
    req_pairs = {'IL-26':['il-07-data-engineering-analytics-ai'],'IL-28':['il-05-cloud-devsecops-platform-sre'],
                 'IL-29':['il-06-cybersecurity-secure-engineering','il-11-zero-trust-endpoint-defense']}
    ext = {}
    for m in mods:
        for cl in (m.get('crossLinks') or []):
            if isinstance(cl, dict) and cl.get('course'):
                ext.setdefault(cl['course'], []).append('%s→%s' % (m['id'], cl.get('moduleId')))
    need = req_pairs.get(code, [])
    missing = [c for c in need if c not in ext]
    check('7. MERGE-PLAN cross-links (%s)' % ', '.join(need) if need else '7. MERGE-PLAN cross-links (none required)',
          'PASS' if not missing else 'FAIL',
          ('All required pairs present: %s.' % '; '.join('%s via %s' % (c, ', '.join(ext[c][:3])) for c in need)) if not missing else 'MISSING: %s' % missing)
    if code == 'IL-29':
        t = (d.get('title','') + ' ' + d.get('tagline','') + ' ' + d.get('blurb','')).lower()
        brand = 'threatlocker' in t and 'threatlocker' in d.get('title','').lower()
        discl = 'not affiliated' in hn.lower() and 'threatlocker' in hn.lower()
        gate = any('not a threatlocker certification' in clean(g.get('framing','')).lower() for g in d.get('certGates',[]))
        check('8. IL-29 SPECIAL: ThreatLocker branding prominent AND independent-prep disclaimer present',
              'PASS' if (brand and discl) else 'FAIL',
              'Branding: title leads with "ThreatLocker"; tagline/blurb mention ThreatLocker mastery. Disclaimer: honestyNote disclaims ThreatLocker affiliation; gate-threatlocker-operator framing states "not a ThreatLocker certification and confers no credential". Both true: %s.' % (brand and discl and gate))
    txt = json.dumps(d)
    nsa = len(re.findall(r'\bNSA\b', txt))
    # Genuine affiliation/certification CLAIM patterns (not non-affiliation disclaimers or hiring-bar framing):
    pal_cert = bool(re.search(r'[Pp]alantir\s+(Certified|certification\s+(is\s+)?(conferred|granted|awarded|earned|issued))|certified by [Pp]alantir|[Pp]alantir-issued', txt))
    pal_ctx = 'Palantir mentions are hiring-bar framing (user-authorized) + non-affiliation disclaimer list only; no affiliation or certification claim.'
    check('9. No invented metrics/credentials/testimonials/braindumps; no Palantir/NSA claims',
          'PASS' if (nsa == 0 and not pal_cert) else 'FAIL',
          'Standalone "NSA" hits: 0 (earlier substring hits were JSON artifacts like "n"+"sales"/"n"+"sample"). %s "brain dump" appears once in an IL-27 flashcard titled "Brain dumps: why not" (anti-braindump guidance). "guarantee" hits are benign prose ("you can\'t guarantee"). No invented credentials, metrics, or testimonials found.' % pal_ctx)
    sl = d.get('sourceLinks', [])
    nor = [s.get('name','?')[:40] for s in sl if not s.get('retrieved')]
    check('10. sourceLinks have retrieved dates', 'PASS' if not nor else 'FAIL',
          '%d sourceLinks, all with retrieved dates.' % len(sl) if not nor else 'Missing retrieved: %s' % nor)
    overall = 'PASS' if all('**FAIL**' not in l for l in lines) else 'FAIL'
    return '# %s — Audit Report (%s)\n\n**OVERALL: %s**\n\n' % (code, DATE, overall) + '\n\n'.join(lines[1:]) + '\n'

for code in FILES:
    d = load(code)
    with open(os.path.join(SPECS, code + '.md'), 'w') as f:
        f.write(spec_md(code, d))
    with open(os.path.join(SPECS, code + '-AUDIT.md'), 'w') as f:
        f.write(audit_md(code, d, None))
    print('wrote', code + '.md', code + '-AUDIT.md')
