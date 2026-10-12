#!/usr/bin/env python3
"""Resolve extracted URLs to unique absolute URLs + anchor check list."""
import json, re
from urllib.parse import urljoin, urlsplit, urlunsplit

d = json.load(open('/tmp/link-extract.json'))

BLANK = {'', '#'}
PLACEHOLDER = re.compile(r'^(todo|#todo|\?|javascript:void)', re.I)

unique = {}   # key: abs url minus fragment -> {'url', 'frag_ok'...}
anchors = []  # (page, file, raw, target_page_url, fragment)
blanks = []   # blank/placeholder occurrences
specials = []
occ = {}      # absurl -> [occurrence dicts]

def add_occ(absurl, o):
    occ.setdefault(absurl, []).append(o)

for u in d['urls']:
    raw, page, f = u['raw'], u['page'], u['file']
    rl = raw.lower()
    if raw in BLANK or PLACEHOLDER.match(raw) or raw.strip() in BLANK:
        blanks.append(u); continue
    if rl.startswith(('javascript:', 'data:', 'mailto:', 'tel:', 'sms:')):
        specials.append(u); continue
    if raw.startswith('#'):
        anchors.append({'page': page, 'file': f, 'raw': raw, 'frag': raw[1:]})
        continue
    # resolve relative against the page URL
    absurl = urljoin(page, raw)
    sp = urlsplit(absurl)
    if sp.scheme not in ('http', 'https'):
        specials.append(u); continue
    frag = sp.fragment
    nofrag = urlunsplit((sp.scheme, sp.netloc, sp.path or '/', sp.query, ''))
    key = nofrag
    if key not in unique:
        unique[key] = {'url': nofrag, 'frag': frag or None, 'occurrences': []}
    if frag and not unique[key]['frag']:
        unique[key]['frag'] = frag
    unique[key]['occurrences'].append({'site': u['site'], 'file': f, 'page': page,
                                       'tag': u['tag'], 'attr': u['attr'], 'raw': raw,
                                       'frag': frag})
    add_occ(nofrag, {'site': u['site'], 'file': f, 'page': page, 'tag': u['tag'],
                     'attr': u['attr'], 'raw': raw, 'frag': frag})

json.dump(unique, open('/tmp/unique-urls.json', 'w'))
json.dump(anchors, open('/tmp/anchors.json', 'w'))
json.dump(blanks, open('/tmp/blanks.json', 'w'))
json.dump(specials, open('/tmp/specials.json', 'w'), indent=1)

print(f'unique checkable urls: {len(unique)}')
print(f'anchor-only: {len(anchors)}, blanks: {len(blanks)}, specials: {len(specials)}')
# domain breakdown
from collections import Counter
hosts = Counter(urlsplit(k).netloc for k in unique)
for h, c in hosts.most_common(25): print(f'  {h}: {c}')
# blanks detail
for b in blanks:
    print('BLANK:', b['file'], '|', b['tag'], b['attr'], '|', repr(b['raw']), '| page:', b['page'])
