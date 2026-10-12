#!/usr/bin/env python3
"""Append standard disaffiliation clause to IL-21/22/23 honestyNotes (additive, preserves existing text)."""
import json, os

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
CLAUSES = {
    'il-21-humanities.json': (" It is not affiliated with, endorsed by, or sponsored by any university, "
                              "publisher, or institution; it confers no certificate and grants no credentials."),
    'il-22-esoteric-secret-knowledge.json': (" It is not affiliated with, endorsed by, or sponsored by any religious, "
                                             "esoteric, or academic organization; it confers no certificate and grants no credentials."),
    'il-23-frontier-knowledge.json': (" It is not affiliated with, endorsed by, or sponsored by any research lab, "
                                      "company, or institution named; it confers no certificate and grants no credentials."),
}
for f, clause in CLAUSES.items():
    p = os.path.join(BASE, f)
    with open(p) as fh:
        d = json.load(fh)
    old = d['honestyNote']
    assert 'not affiliated' not in old.lower(), f
    d['honestyNote'] = old + clause
    tmp = p + '.tmp'
    with open(tmp, 'w') as fh:
        json.dump(d, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    with open(tmp) as fh:
        json.load(fh)  # validate
    os.replace(tmp, p)
    print('updated', f, '->', len(d['honestyNote']), 'chars')
