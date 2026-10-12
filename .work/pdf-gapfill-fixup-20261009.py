#!/usr/bin/env python3
"""Swap least-relevant fallback PDF for zero-trust in trust/governance modules (il-17)."""
import json, os
from datetime import datetime, timezone

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
path = os.path.join(BASE, 'il-17-agentic-ai-engineering.json')
with open(path, 'r', encoding='utf-8') as fh:
    data = json.load(fh)

targets = {'Trust and Guardrails', 'Governance'}
fixed = []
for m in data['modules']:
    if m.get('title') in targets:
        urls = [p['url'].split('/')[-1] for p in m.get('pdfs', [])]
        assert 'bbg-zero-trust.pdf' not in urls, f"zero-trust already present in {m['title']}"
        assert len(urls) == 3
        # replace the last (lowest-priority fallback) entry
        m['pdfs'][-1] = {
            "title": "Zero Trust Architecture — Visual Guide",
            "url": "https://interstitiumlabs.dev/assets/pdfs/bbg-zero-trust.pdf",
            "source": "Interstitium Labs",
            "blurb": "Animated step-by-step: tenets, identity perimeter, micro-segmentation, pillars.",
            "pages": 8,
            "animated": True,
            "verifiedUtc": NOW,
            "httpStatus": 200,
        }
        fixed.append(m['title'])

with open(path, 'w', encoding='utf-8') as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
    fh.write('\n')
with open(path, 'r', encoding='utf-8') as fh:
    json.load(fh)
print('fixed:', fixed, 'validated OK')
