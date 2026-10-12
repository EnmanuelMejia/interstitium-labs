#!/usr/bin/env python3
"""Survey embed depth across IL-21..IL-29 course JSONs."""
import json, glob, os

courses = [
    "il-21-humanities",
    "il-22-esoteric-secret-knowledge",
    "il-23-frontier-knowledge",
    "il-24-threatlocker-assessment-prep-cbt",
    "il-25-cybersecurity-professional-certificate",
    "il-26-data-analyst-certification-senior-mastery",
    "il-27-it-infrastructure-specialist-threatlocker-mastery",
    "il-28-devsecops-cloud-infrastructure-mastery",
    "il-29-threatlocker-ai-cybersecurity-mastery",
]

base = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")

for c in courses:
    path = os.path.join(base, c + ".json")
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        print(f"{c}: LOAD FAIL {e}")
        continue
    mods = data.get("modules", [])
    pdfs_bad, quiz_bad, cards_bad, drills_bad = [], [], [], []
    for i, m in enumerate(mods):
        mid = m.get("id") or m.get("title", "")[:40] or f"idx{i}"
        pdfs = m.get("pdfs", []) or []
        quiz = m.get("quiz", []) or []
        cards = m.get("cards", []) or []
        drills = m.get("drills", []) or []
        if len(pdfs) < 2: pdfs_bad.append((mid, len(pdfs)))
        if len(quiz) < 3: quiz_bad.append((mid, len(quiz)))
        if len(cards) < 5: cards_bad.append((mid, len(cards)))
        if len(drills) < 1: drills_bad.append((mid, len(drills)))
    print(f"== {c}: {len(mods)} modules")
    print(f"   PDFs<2: {len(pdfs_bad)}  quiz<3: {len(quiz_bad)}  cards<5: {len(cards_bad)}  drills<1: {len(drills_bad)}")
    for name, bad in (("pdfs", pdfs_bad), ("quiz", quiz_bad), ("cards", cards_bad), ("drills", drills_bad)):
        if bad:
            print(f"   {name} gaps: {[(b[0], b[1]) for b in bad[:8]]}{'...' if len(bad) > 8 else ''}")
    # module key sample
    if mods:
        print(f"   sample module keys: {sorted(mods[0].keys())[:14]}")
        print(f"   sample quiz[0]: {json.dumps((mods[0].get('quiz') or [{}])[0])[:160]}")
        print(f"   sample cards[0]: {json.dumps((mods[0].get('cards') or [{}])[0])[:120]}")
        print(f"   sample drills[0]: {json.dumps((mods[0].get('drills') or [{}])[0])[:200]}")
