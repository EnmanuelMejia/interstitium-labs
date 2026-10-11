import io, json

p = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-26-data-analyst-certification-senior-mastery.json'
c = json.load(io.open(p, encoding='utf-8'))

fixes = 0
def walk(o):
    global fixes
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str):
                nv = v
                if 'https://www.microsoft.com/en-us/microsoft-365/free-office-online' in nv:
                    nv = nv.replace('https://www.microsoft.com/en-us/microsoft-365/free-office-online',
                                    'https://www.office.com')
                if 'https://my-workspace.cloud.databricks.com' in nv:
                    nv = nv.replace('https://my-workspace.cloud.databricks.com',
                                    'https://<your-workspace>.cloud.databricks.com')
                if 'https://github.com/yourname/portfolio.git' in nv:
                    nv = nv.replace('https://github.com/yourname/portfolio.git',
                                    'https://github.com/<your-username>/portfolio.git')
                if nv != v:
                    o[k] = nv
                    fixes += 1
            else:
                walk(v)
    elif isinstance(o, list):
        for idx, v in enumerate(o):
            if isinstance(v, str):
                nv = v
                if 'https://www.microsoft.com/en-us/microsoft-365/free-office-online' in nv:
                    nv = nv.replace('https://www.microsoft.com/en-us/microsoft-365/free-office-online',
                                    'https://www.office.com')
                if nv != v:
                    o[idx] = nv
                    fixes += 1
            else:
                walk(v)

walk(c)
print('fixes applied:', fixes)

# re-extract URLs and confirm the three are gone/changed
import re
from urllib.parse import urlparse
blob = json.dumps(c)
raw = set(re.findall(r'https?://[A-Za-z0-9][^\s"<>\\]*', blob))
bad = [u for u in raw if 'yourname' in u or 'my-workspace' in u or 'free-office-online' in u]
print('remaining bad URLs:', bad)
assert not bad

tmp = p + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    json.dump(c, f, ensure_ascii=False, indent=2)
with io.open(tmp, encoding='utf-8') as f:
    r = json.load(f)
assert len(r['modules']) == 51
import os
os.replace(tmp, p)
print('URL fixes written atomically')
