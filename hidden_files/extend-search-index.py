#!/usr/bin/env python3
"""Append bootcamp / IL-shortcut / drill entries to search-index.json (atomic)."""
import json, os

PATH = os.path.expanduser("~/workspace/apex-audit/docs/assets/search-index.json")

NEW = [
    {"t": "IL-26 · Data Analyst", "u": "/il26/", "type": "course",
     "d": "Flagship data-analyst certification — senior hiring bar, SQL, Python, probability, ontology thinking.",
     "k": "il26 il-26 data analyst flagship certification", "theme": "", "tn": "IL-26"},
    {"t": "IL-27 · IT Infrastructure", "u": "/il27/", "type": "course",
     "d": "Flagship IT infrastructure specialist certification — zero-trust infrastructure mastery.",
     "k": "il27 il-27 it infrastructure flagship certification", "theme": "", "tn": "IL-27"},
    {"t": "IL-28 · DevSecOps & Cloud", "u": "/il28/", "type": "course",
     "d": "Flagship DevSecOps and cloud infrastructure certification.",
     "k": "il28 il-28 devsecops cloud flagship certification", "theme": "", "tn": "IL-28"},
    {"t": "IL-29 · ThreatLocker Zero-Trust", "u": "/il29/", "type": "course",
     "d": "Flagship ThreatLocker zero-trust endpoint defense certification.",
     "k": "il29 il-29 threatlocker zero trust flagship certification", "theme": "", "tn": "IL-29"},
    {"t": "ThreatLocker Assessment Prep", "u": "/bootcamps/threatlocker-assessment-prep/", "type": "bootcamp",
     "d": "Interactive assessment-prep bootcamp in the ThreatLocker format — adaptive, comprehensive.",
     "k": "threatlocker assessment prep bootcamp", "theme": "cybersecurity", "tn": "Cybersecurity"},
    {"t": "ThreatLocker Interview Bootcamp", "u": "/bootcamps/tl-interview/", "type": "bootcamp",
     "d": "Interview-prep bootcamp — ThreatLocker interview readiness.",
     "k": "threatlocker interview bootcamp tl", "theme": "cybersecurity", "tn": "Cybersecurity"},
    {"t": "Bootcamp Catalog", "u": "/bootcamp-catalog/", "type": "bootcamp",
     "d": "Every Interstitium Labs bootcamp — interactive, adaptive, comprehensive.",
     "k": "bootcamp catalog all bootcamps", "theme": "", "tn": ""},
    {"t": "DevOps Desk Interview Q&A", "u": "/prep/drills/desk-interview/", "type": "practice",
     "d": "DevOps desk interview drill — rapid-fire Q&A practice.",
     "k": "devops desk interview drill practice", "theme": "cloud-devops", "tn": "Cloud & DevOps"},
    {"t": "Full-Stack Desk Drill", "u": "/prep/drills/fullstack-desk/", "type": "practice",
     "d": "Full-stack interview drill desk.",
     "k": "fullstack full-stack desk drill interview practice", "theme": "programming", "tn": "Programming"},
    {"t": "Instrument Desk Drill", "u": "/prep/drills/instrument-desk/", "type": "practice",
     "d": "Instrumentation interview drill desk.",
     "k": "instrument instrumentation desk drill interview practice", "theme": "programming", "tn": "Programming"},
]

with open(PATH) as f:
    doc = json.load(f)

have = {i["u"] for i in doc["items"]}
added = 0
for e in NEW:
    if e["u"] not in have:
        doc["items"].append(e)
        have.add(e["u"])
        added += 1

doc["count"] = len(doc["items"])

tmp = PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
os.replace(tmp, PATH)

# validate
with open(PATH) as f:
    check = json.load(f)
assert check["count"] == len(check["items"])
print("added:", added, "| total:", check["count"])
from collections import Counter
print(Counter(i.get("type") for i in check["items"]))
