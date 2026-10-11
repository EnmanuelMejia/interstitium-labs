#!/usr/bin/env python3
"""Themed-content rollout (2026-10-09): regenerate 2 sample PDFs with themed covers.

- bbg-zero-trust.pdf      -> theme "mr-robot" (cybersecurity)
- bbg-etl-pipelines.pdf   -> theme "oceandeep" (data engineering)

Backs up the current outputs first. Proves the theme parameter works end to end;
full 241-PDF regeneration is future work.
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "output")
BACKUP = os.path.join(HERE, "output-backups-themes")
os.makedirs(BACKUP, exist_ok=True)

import bbg_style
import gen_batch4
import gen_batch6

def themed_title_page(theme):
    def _tp(c, title, subtitle, category, page_num_ref):
        return bbg_style.title_page(c, title, subtitle, category, page_num_ref, theme=theme)
    return _tp

jobs = [
    (gen_batch4, "pdf_zero_trust", "bbg-zero-trust.pdf", "mr-robot"),
    (gen_batch6, "pdf_etl", "bbg-etl-pipelines.pdf", "oceandeep"),
]

for mod, fn_name, fname, theme in jobs:
    path = os.path.join(OUT, fname)
    if os.path.isfile(path):
        bak = os.path.join(BACKUP, fname)
        if not os.path.isfile(bak):
            shutil.copy2(path, bak)
            print("backed up", fname)
    # inject themed title_page into the generator module
    mod.title_page = themed_title_page(theme)
    getattr(mod, fn_name)(path)
    size = os.path.getsize(path)
    print("regenerated", fname, "theme=%s size=%d bytes" % (theme, size))

print("done. backups in", BACKUP)
