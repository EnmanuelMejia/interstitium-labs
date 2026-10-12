#!/usr/bin/env python3
"""Retry pages whose normal-UA fetch timed out (http==0)."""
import json, sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_audit_run import audit_page, save, RESULTS_PATH  # noqa

import seo_audit_run as mod

PAGES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "seo_pages.json")))
data = json.load(open(mod.RESULTS_PATH))
for p in PAGES:
    url = p["url"]
    v = data.get(url, {})
    needs = ("error" in v) or (v.get("normal", {}).get("http", 0) == 0)
    if needs:
        print("retry:", url, flush=True)
        try:
            data[url] = audit_page(url, crawl_ua_too=p.get("crawler", False))
        except Exception as e:
            data[url] = {"error": str(e)}
        save(data)
        time.sleep(1)
print("done")
