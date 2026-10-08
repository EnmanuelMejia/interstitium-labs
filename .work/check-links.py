#!/usr/bin/env python3
"""HTTP-check unique URLs, incremental JSONL results, resumable, polite."""
import json, subprocess, time, sys, os
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
BLOCKED_HOSTS = ('linkedin.com', 'www.linkedin.com', 'lnkd.in', 'facebook.com',
                 'www.facebook.com', 'instagram.com', 'www.instagram.com',
                 'x.com', 'twitter.com', 'www.tiktok.com', 'tiktok.com',
                 'chat.deepseek.com')
RES = '/tmp/check-results.jsonl'

unique = json.load(open('/tmp/unique-urls.json'))
done_keys = set()
if os.path.exists(RES):
    with open(RES) as fh:
        for line in fh:
            line = line.strip()
            if line:
                done_keys.add(json.loads(line)['key'])

targets = []
for key, v in unique.items():
    if key in done_keys: continue
    host = urlsplit(v['url']).netloc
    internal = host in ('interstitiumlabs.dev', 'enmanueldmejia.com')
    targets.append((key, v['url'], internal))

internal = [(k, u) for k, u, i in targets if i]
external = [(k, u) for k, u, i in targets if not i]
print(f'todo: {len(internal)} internal, {len(external)} external (already done: {len(done_keys)})', flush=True)

def check(key_url):
    key, url = key_url
    for attempt in (1, 2):
        try:
            r = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-L', '--max-time', '20',
                 '-A', UA, '-w', '\n%{http_code}\n%{url_effective}\n%{num_redirects}\n', url],
                capture_output=True, text=True, timeout=35)
            lines = [l for l in r.stdout.split('\n') if l.strip() != '']
            code, eff, nred = int(lines[-3]), lines[-2], lines[-1]
            if code == 0 and attempt == 1:
                time.sleep(1); continue
            host = urlsplit(url).netloc
            if code in (403, 429, 401, 999) and any(host == h or host.endswith('.' + h) for h in BLOCKED_HOSTS):
                return key, {'code': code, 'status': 'bot-blocked', 'effective': eff}
            if 200 <= code < 300:
                return key, {'code': code, 'status': 'ok', 'effective': eff, 'redirects': int(nred)}
            if code == 0:
                return key, {'code': 0, 'status': 'timeout', 'effective': url}
            return key, {'code': code, 'status': 'dead', 'effective': eff}
        except subprocess.TimeoutExpired:
            if attempt == 1: time.sleep(1); continue
            return key, {'code': 0, 'status': 'timeout', 'effective': url}
    return key, {'code': 0, 'status': 'timeout', 'effective': url}

def run(batch, workers, label):
    n = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(check, ku): ku[0] for ku in batch}
        with open(RES, 'a') as fh:
            for fut in as_completed(futs):
                key, res = fut.result()
                fh.write(json.dumps({'key': key, **res}) + '\n')
                fh.flush()
                n += 1
                if n % 25 == 0:
                    print(f'{label}: {n}/{len(batch)}', flush=True)
    print(f'{label} done: {n}', flush=True)

run(internal, 10, 'internal')
run(external, 5, 'external')

# summary
from collections import Counter
c = Counter()
with open(RES) as fh:
    for line in fh:
        line = line.strip()
        if line: c[json.loads(line)['status']] += 1
print(dict(c))
