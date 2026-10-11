import re, json, subprocess, sys
from urllib.parse import urlparse

c = json.load(open('/home/hatch/workspace/apex-audit/docs/university/data/courses/il-26-data-analyst-certification-senior-mastery.json', encoding='utf-8'))
blob = json.dumps(c)
raw = set(re.findall(r'https?://[A-Za-z0-9][^\s"<>\\]*', blob))

skip_hosts = {'localhost', 'example.com', 'www.w3.org', '127.0.0.1'}
urls = []
for u in sorted(raw):
    u = u.rstrip('.,;:\'"!?)}]')
    try:
        h = urlparse(u).hostname or ''
    except Exception:
        continue
    if h in skip_hosts or not h or '.' not in h:
        continue
    urls.append(u)

print('checking', len(urls), 'URLs')
ok, fail = [], []
for u in urls:
    try:
        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
                            '-L', '--max-time', '25',
                            '-A', 'Mozilla/5.0 (compatible; IL26-linkcheck/1.0)',
                            u],
                           capture_output=True, text=True, timeout=30)
        code = r.stdout.strip()[-3:]
        if code.startswith('2') or code == '429':
            ok.append((u, code))
        else:
            fail.append((u, code))
    except Exception as e:
        fail.append((u, 'ERR ' + str(e)[:40]))

print('OK:', len(ok), 'FAIL:', len(fail))
for u, code in fail:
    print('FAIL', code, u)
json.dump({'ok': ok, 'fail': fail}, open('/tmp/il26_url_sweep.json', 'w'), indent=1)
