#!/usr/bin/env python3
"""Coordinator validation for the multicloud-template retrofit.
Checks every file modified in the working tree (vs git HEAD):
1. JSON validity of all touched .json files
2. Template shape: module notes = 4 titled sections (Concepts first),
   summary present, quiz items = 4 choices / 0-based int answer / non-empty explain
3. Competitor-brand scan (case-insensitive, word-boundary) across touched files
4. Palantir/NSA scan (word-boundary; 'nsa' needs care re: substrings)
5. Protected files untouched: _headers, _redirects, _worker.js, worker.js,
   deploy configs, il-19 course, il-23 course
"""
import json, re, subprocess, sys, os

REPO = os.path.expanduser('~/workspace/apex-audit')
os.chdir(REPO)

out = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
touched = [l[3:] for l in out.stdout.splitlines() if l.strip()]
json_files = [f for f in touched if f.endswith('.json') and not f.startswith('retrofit_20261007/') and not f.startswith('hidden_build_20261007/')]
html_files = [f for f in touched if f.endswith('.html')]

errors, warnings = [], []

# 5. protected files
protected = ['docs/_headers', 'docs/_redirects', 'docs/_worker.js', 'docs/worker.js',
             'docs/university/data/courses/il-19-multicloud-devops-ai-bootcamp.json',
             'docs/university/data/courses/il-23-frontier-knowledge.json']
for p in protected:
    if p in touched:
        errors.append(f'PROTECTED FILE MODIFIED: {p}')

# 1+2. JSON validity + template shape
NOTE_TITLES = {'concepts', 'hands-on procedure', 'worked estimation', 'project brief',
               'honesty note', 'noah check-in', 'frontier honesty'}
quiz_total = quiz_bad = 0
modules_total = modules_bad_notes = 0
for f in json_files:
    try:
        d = json.load(open(f))
    except Exception as e:
        errors.append(f'JSON INVALID: {f}: {e}')
        continue
    if 'courses/' in f and isinstance(d, dict) and 'modules' in d:
        for m in d['modules']:
            mid = m.get('id', '?')
            modules_total += 1
            notes = m.get('notes', [])
            titles = [n.get('title', '').strip().lower() for n in notes if isinstance(n, dict)]
            if len(notes) != 4 or not set(titles) <= NOTE_TITLES or 'concepts' not in titles:
                modules_bad_notes += 1
                warnings.append(f'{f} :: module {mid}: notes titles = {titles}')
            if not m.get('summary'):
                warnings.append(f'{f} :: module {mid}: missing summary')
            for qi, q in enumerate(m.get('quiz', [])):
                quiz_total += 1
                ch = q.get('choices', [])
                ans = q.get('answer')
                exp = q.get('explain', '')
                if not (isinstance(ch, list) and len(ch) == 4):
                    quiz_bad += 1; errors.append(f'{f} :: {mid} quiz[{qi}]: choices != 4')
                if not (isinstance(ans, int) and 0 <= ans < 4):
                    quiz_bad += 1; errors.append(f'{f} :: {mid} quiz[{qi}]: bad answer index {ans!r}')
                if not (isinstance(exp, str) and exp.strip()):
                    quiz_bad += 1; errors.append(f'{f} :: {mid} quiz[{qi}]: empty explain')
    if 'catalog/' in f and isinstance(d, dict):
        for p in d.get('paths', []):
            pid = p.get('id', '?')
            if not isinstance(p.get('topics'), list) or not p.get('topics'):
                warnings.append(f'{f} :: path {pid}: topics missing/empty')
            srcs = p.get('sources', [])
            if not isinstance(srcs, list) or not srcs:
                warnings.append(f'{f} :: path {pid}: sources missing/empty')
            else:
                for s in srcs:
                    if not (isinstance(s, dict) and s.get('name') and s.get('url')):
                        errors.append(f'{f} :: path {pid}: malformed source {s}')
            if not p.get('il_provides'):
                warnings.append(f'{f} :: path {pid}: il_provides missing')

# 3+4. brand scans
brands = ['aleks', 'khan academy', 'coursera', 'udemy', 'edx', 'brilliant']
# 'brilliant' as adjective is common; flag only the standalone brand in learning-platform context is hard;
# use word-boundary and report hits for manual review
palantir_ns = [r'\bpalantir\b']
brand_hits = []
for f in touched:
    if f.startswith('retrofit_20261007/') or f.startswith('hidden_build_20261007/'):
        continue
    try:
        txt = open(f, encoding='utf-8', errors='replace').read()
    except Exception as e:
        errors.append(f'cannot read {f}: {e}'); continue
    low = txt.lower()
    for b in brands:
        for m_ in re.finditer(r'\b' + re.escape(b) + r'\b', low):
            # skip 'edx' inside words already handled by \b; report context
            s = max(0, m_.start()-60); ctx = txt[s:m_.end()+60].replace('\n', ' ')
            brand_hits.append((f, b, ctx))
    for pat in palantir_ns:
        for m_ in re.finditer(pat, low):
            s = max(0, m_.start()-60); ctx = txt[s:m_.end()+60].replace('\n', ' ')
            brand_hits.append((f, 'palantir/nsa-pat', ctx))
    # NSA as standalone word (avoid 'transactions' etc. via \b)
    for m_ in re.finditer(r'\bnsa\b', low):
        s = max(0, m_.start()-60); ctx = txt[s:m_.end()+60].replace('\n', ' ')
        # allow common false positives: check context for security-agency meaning is hard; report all
        brand_hits.append((f, 'nsa', ctx))

print(f'touched files: {len(touched)} (json: {len(json_files)}, html: {len(html_files)})')
print(f'course modules checked: {modules_total}, note-shape warnings: {modules_bad_notes}')
print(f'quiz items checked: {quiz_total}, quiz shape errors: {quiz_bad}')
print(f'brand/sensitive hits: {len(brand_hits)}')
for f, b, ctx in brand_hits[:40]:
    print(f'  HIT [{b}] {f}: ...{ctx}...')
print(f'errors: {len(errors)}, warnings: {len(warnings)}')
for e in errors[:30]:
    print('  ERROR:', e)
for w in warnings[:30]:
    print('  WARN:', w)
sys.exit(1 if errors else 0)
