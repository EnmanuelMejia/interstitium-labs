#!/usr/bin/env python3
"""Dump module ids/titles/summaries for PDF topic matching."""
import json, os
courses = [
    "il-21-humanities","il-22-esoteric-secret-knowledge","il-23-frontier-knowledge",
    "il-24-threatlocker-assessment-prep-cbt","il-25-cybersecurity-professional-certificate",
    "il-26-data-analyst-certification-senior-mastery","il-27-it-infrastructure-specialist-threatlocker-mastery",
    "il-28-devsecops-cloud-infrastructure-mastery","il-29-threatlocker-ai-cybersecurity-mastery",
]
base = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
for c in courses:
    d = json.load(open(os.path.join(base, c + ".json")))
    print(f"########## {c} ({len(d['modules'])} modules)")
    for m in d["modules"]:
        t = m.get("title", "")
        s = (m.get("summary") or "")[:120].replace("\n", " ")
        o = "; ".join(m.get("objectives", [])[:3])[:140]
        print(f"{m.get('id')}|{t}|{s}|{o}")
    print()
