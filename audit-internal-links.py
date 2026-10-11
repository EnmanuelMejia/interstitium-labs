#!/usr/bin/env python3
"""Internal link audit for interstitiumlabs.dev (docs/ source). Read-only."""
import os, re, json, posixpath
from html.parser import HTMLParser

DOCS = os.path.expanduser('~/workspace/apex-audit/docs')

# ---------- 1. Build valid-route sets from _worker.js + _redirects + deploy config ----------
worker_src = open(os.path.join(DOCS, '_worker.js')).read()

def dict_keys(varname):
    m = re.search(varname + r'\s*=\s*\{(.*?)\};', worker_src, re.S)
    keys, vals = {}, {}
    if not m:
        return keys, vals
    for km, vm in re.findall(r'"(/[^"]*)"\s*:\s*"(/[^"]*)"', m.group(1)):
        keys[km] = vm
    return keys, vals

stub_keys, _ = dict_keys('var STUB_REDIRECTS')
cons_keys, _ = dict_keys('var CONSOLIDATION_REDIRECTS')

# code-level redirects: add trailing-slash variants of each key
REDIRECT_SRC = {}
for k, v in list(stub_keys.items()) + list(cons_keys.items()):
    REDIRECT_SRC[k] = v
    if k.endswith('/'):
        REDIRECT_SRC[k.rstrip('/')] = v
    else:
        REDIRECT_SRC[k + '/'] = v

# explicit code-level route handlers (worker if-blocks)
EXPLICIT_ROUTES = {
    '/os', '/os/', '/proof', '/proof/',
    '/login', '/login/', '/signin', '/signin/', '/member', '/member/',
    '/bootcamps', '/bootcamps/',
    '/bootcamps/threatlocker-assessment-prep', '/bootcamps/threatlocker-assessment-prep/',
    '/il26', '/il26/', '/il27', '/il27/', '/il28', '/il28/', '/il29', '/il29/',
    '/university/course', '/university/course.html',
}

# _redirects file sources
_redirects_src = {}
for line in open(os.path.join(DOCS, '_redirects')):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split()
    if len(parts) >= 2 and parts[0].startswith('/'):
        _redirects_src[parts[0]] = parts[1]

# API + oauth worker routes from deploy config run_worker_first
api_routes = set()
try:
    cfg = json.load(open(os.path.expanduser('~/workspace/apex-audit/.work/flagship-deploy-config-20261008.json')))
    for p in cfg.get('assets_config', {}).get('run_worker_first', []):
        if p.startswith('/api/') or p.startswith('/auth/'):
            api_routes.add(p)
except Exception as e:
    print('WARN deploy config:', e)

# ---------- 2. Path resolution ----------
def resolve_path(p):
    """p: normalized absolute path (no query/fragment). Returns (ok, kind)."""
    if p in EXPLICIT_ROUTES:
        return True, 'worker-route'
    if p in api_routes:
        return True, 'worker-api'
    if p in REDIRECT_SRC:
        return True, 'worker-redirect'
    if p in _redirects_src:
        return True, '_redirects'
    rel = p.lstrip('/')
    cand = os.path.join(DOCS, rel)
    if os.path.isfile(cand):
        return True, 'file'
    if os.path.isfile(cand + '.html'):
        return True, 'file(.html)'
    if os.path.isdir(cand) and os.path.isfile(os.path.join(cand, 'index.html')):
        return True, 'dir-index'
    return False, 'missing'

def norm_path(raw, page_dir):
    """Normalize raw href to absolute site path. Returns (path, frag, query)."""
    # split fragment, query
    frag = ''
    if '#' in raw:
        raw, frag = raw.split('#', 1)
    query = ''
    if '?' in raw:
        raw, query = raw.split('?', 1)
    if raw.startswith('/'):
        p = raw
    else:
        p = posixpath.join(page_dir, raw)
    # collapse . and ..
    p = posixpath.normpath(p)
    if not p.startswith('/'):
        p = '/' + p
    return p, frag, query

# ---------- 3. Extract links from HTML ----------
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for attr in ('href', 'src', 'action', 'poster'):
            if d.get(attr):
                self.links.append((tag, attr, d[attr].strip()))
        if d.get('srcset'):
            for part in d['srcset'].split(','):
                url = part.strip().split(' ')[0]
                if url:
                    self.links.append((tag, 'srcset', url))
        if tag == 'meta':
            if d.get('http-equiv', '').lower() == 'refresh' and d.get('content'):
                m = re.search(r'url\s*=\s*(\S+)', d['content'], re.I)
                if m:
                    self.links.append(('meta', 'refresh', m.group(1).strip('\'"')))

def is_skippable(raw):
    r = raw.strip()
    if not r:
        return True, 'empty'
    if r.startswith('#'):
        return True, 'fragment'
    low = r.lower()
    for scheme in ('mailto:', 'tel:', 'sms:', 'javascript:', 'data:', 'blob:', 'callto:'):
        if low.startswith(scheme):
            return True, 'scheme:' + scheme[:-1]
    if low.startswith('http://') or low.startswith('https://'):
        return True, 'external'
    if r.startswith('//'):
        return True, 'external-protocol-relative'
    return False, ''

html_files = []
for root, dirs, files in os.walk(DOCS):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

total = 0
skipped = {}
broken = []   # (page, tag, attr, raw, resolved_path, reason)
valid_kinds = {}
seen_broken = set()

for hf in sorted(html_files):
    rel = os.path.relpath(hf, DOCS)
    page_dir = '/' + posixpath.dirname(rel) if posixpath.dirname(rel) != '.' else '/'
    if not page_dir.endswith('/'):
        page_dir += '/'
    try:
        html = open(hf, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    parser = LinkParser()
    try:
        parser.feed(html)
    except Exception:
        pass
    for tag, attr, raw in parser.links:
        total += 1
        skip, kind = is_skippable(raw)
        if skip:
            skipped[kind] = skipped.get(kind, 0) + 1
            continue
        p, frag, query = norm_path(raw, page_dir)
        ok, how = resolve_path(p)
        if ok:
            valid_kinds[how] = valid_kinds.get(how, 0) + 1
        else:
            key = (rel, raw)
            if key not in seen_broken:
                seen_broken.add(key)
                broken.append({
                    'page': rel, 'tag': tag, 'attr': attr, 'raw': raw,
                    'resolved': p, 'reason': 'no file/dir-index/.html, no _redirects rule, no worker route',
                })

# ---------- 4. Verify redirect TARGETS resolve ----------
redirect_target_broken = []
all_redirects = {}
for k, v in REDIRECT_SRC.items():
    all_redirects.setdefault(k, v)
for k, v in _redirects_src.items():
    all_redirects.setdefault(k, v)
seen_t = set()
for src_p, tgt in all_redirects.items():
    tgt_path = tgt.split('?')[0].split('#')[0]
    if tgt_path in seen_t:
        continue
    seen_t.add(tgt_path)
    ok, how = resolve_path(tgt_path)
    # target may itself be a redirect source (chain) -> ok
    if not ok:
        redirect_target_broken.append({'source': src_p, 'target': tgt, 'target_path': tgt_path})

report = {
    'html_files': len(html_files),
    'total_links_scanned': total,
    'skipped': skipped,
    'valid_internal_by_kind': valid_kinds,
    'broken_count': len(broken),
    'broken': broken,
    'redirect_target_broken': redirect_target_broken,
}
out = os.path.expanduser('~/workspace/apex-audit/internal-link-audit-report.json')
json.dump(report, open(out, 'w'), indent=1)
print('html files:', len(html_files))
print('total attrs scanned:', total)
print('skipped:', json.dumps(skipped, indent=1))
print('valid internal by kind:', json.dumps(valid_kinds, indent=1))
print('BROKEN:', len(broken))
print('redirect targets broken:', len(redirect_target_broken))
