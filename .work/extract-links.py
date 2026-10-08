#!/usr/bin/env python3
"""Extract href/src/action URLs + ids from site HTML for dead-link audit."""
import os, re, json, sys
from html.parser import HTMLParser
from urllib.parse import urljoin

URL_ATTRS = {'a': ('href',), 'link': ('href',), 'img': ('src', 'srcset'),
             'script': ('src',), 'source': ('src', 'srcset'), 'video': ('src', 'poster'),
             'audio': ('src',), 'iframe': ('src',), 'form': ('action',),
             'meta': ('content',),  # only og/twitter image/url recorded separately
             }

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = []   # (tag, attr, raw)
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for a, v in attrs:
            if a == 'id' or a == 'name':
                self.ids.add(v)
        if tag in URL_ATTRS:
            for attr in URL_ATTRS[tag]:
                v = d.get(attr)
                if v is None: continue
                if tag == 'meta':
                    prop = (d.get('property') or d.get('name') or '').lower()
                    if attr == 'content' and prop in ('og:image', 'twitter:image',
                                                      'og:url', 'twitter:url',
                                                      'og:video', 'twitter:player'):
                        self.urls.append((tag, attr, v.strip()))
                elif attr in ('srcset',):
                    for part in v.split(','):
                        u = part.strip().split(' ')[0]
                        if u: self.urls.append((tag, attr, u))
                else:
                    self.urls.append((tag, attr, v.strip()))

def page_url(root, domain, relpath):
    # relpath like ./about/index.html -> https://domain/about/index.html
    p = relpath[2:] if relpath.startswith('./') else relpath
    return f'https://{domain}/{p}'

def main():
    jobs = [
        ('/home/hatch/workspace/apex-audit/docs', 'interstitiumlabs.dev', '**/*.html'),
        ('/home/hatch/workspace/portfolio-site', 'enmanueldmejia.com', '**/*.html'),
    ]
    out = {'urls': [], 'ids': {}}
    for root, domain, _ in jobs:
        for dirpath, _, files in os.walk(root):
            for f in files:
                if not f.endswith('.html'): continue
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, root)
                purl = f'https://{domain}/{rel}'
                try:
                    with open(full, encoding='utf-8', errors='replace') as fh:
                        html = fh.read()
                except Exception as e:
                    print(f'READ-ERR {full}: {e}', file=sys.stderr); continue
                p = P(); p.feed(html)
                out['ids'][purl] = sorted(p.ids)
                for tag, attr, raw in p.urls:
                    out['urls'].append({'site': domain, 'file': full, 'page': purl,
                                        'tag': tag, 'attr': attr, 'raw': raw})
    json.dump(out, open('/tmp/link-extract.json', 'w'), indent=1)
    print(f"url occurrences: {len(out['urls'])}, pages: {len(out['ids'])}")

if __name__ == '__main__':
    main()
