#!/usr/bin/env python3
"""Point IL shortcut index entries at final canonical course URLs (no 301 hop)."""
import json, os

PATH = os.path.expanduser("~/workspace/apex-audit/docs/assets/search-index.json")
FINALS = {
    "/il26/": "/university/course?course=il-26-data-analyst-certification-senior-mastery",
    "/il27/": "/university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery",
    "/il28/": "/university/course?course=il-28-devsecops-cloud-infrastructure-mastery",
    "/il29/": "/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery",
}

with open(PATH) as f:
    doc = json.load(f)

changed = 0
for i in doc["items"]:
    if i["u"] in FINALS:
        i["u"] = FINALS[i["u"]]
        # keep shortcut codes searchable
        i["k"] = i.get("k", "") + " il26 il27 il28 il29 shortcut"
        changed += 1

tmp = PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
os.replace(tmp, PATH)

with open(PATH) as f:
    check = json.load(f)
print("changed:", changed, "| valid JSON, count:", check["count"])
for i in check["items"]:
    if i["u"].startswith("/university/course?course=il-2"):
        print(" ", i["t"], "->", i["u"])
