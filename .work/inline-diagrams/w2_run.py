#!/usr/bin/env python3
"""W2 driver: embed 4 ANIMATED diagrams per module into IL-07..IL-12 course JSONs."""
import sys, os, json, shutil, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w2_kits import KITS, ROUTES, build, S

COURSES = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
FILES = [
    "il-07-data-engineering-analytics-ai.json",
    "il-08-algorithms-compilers-distributed-formal.json",
    "il-09-adaptive-certification-command.json",
    "il-10-portfolio-career-professional-practice.json",
    "il-11-zero-trust-endpoint-defense.json",
    "il-12-ai-engineering.json",
]

PREFIXES = [
    ("il-07-data-engineering-analytics-ai-", "il07-"),
    ("il-08-algorithms-compilers-distributed-formal-", "il08-"),
    ("il-09-adaptive-certification-command-", "il09-"),
    ("il-10-portfolio-career-professional-practice-", "il10-"),
    ("il-11-zero-trust-endpoint-defense-", "il11-"),
    ("il-12-ai-engineering-", "il12-"),
]

def short_id(mid):
    if "--" in mid:
        return mid.rsplit("--", 1)[-1]
    for pre, rep in PREFIXES:
        if mid.startswith(pre):
            return rep + mid[len(pre):]
    return mid

def fallback_specs(module):
    """Last-resort kit built from the module's own content. Returns 4 specs."""
    title = module.get("title", "module")
    objs = [o for o in module.get("objectives", [])][:4]
    notes = [n.get("title", "") for n in module.get("notes", [])]
    steps = [((o[:30] + "…") if len(o) > 30 else o, f"objective {i+1}")
             for i, o in enumerate(objs)] or [(title, "module")]
    while len(steps) < 2:
        steps.append((notes[len(steps)] if len(notes) > len(steps) else "review", "step"))
    return [
        S("flow", {"steps": steps[:5]},
          f"Learning path for {title}: work the objectives in order, each building on the last.",
          f"Flow of learning objectives for {title}", ["concepts"]),
        S("concept", {"title": title, "lines": [(t[:44] + "…") if len(t) > 44 else t for t in notes[:4]] or ["see notes"]},
          f"Module map for {title}: the notes below cover these topics in sequence.",
          f"Concept box mapping {title} topics", ["project", "hands-on"]),
        S("compare", {"lt": "Core ideas", "li": [(t[:30]) for t in notes[:3]] or ["concepts"],
                      "rt": "Applied checks", "ri": ["Worked example", "Pitfalls", "Hands-on lab"]},
          f"Study {title} in two passes: core ideas first, then applied checks against worked examples and pitfalls.",
          f"Study strategy comparison for {title}", ["pitfalls", "worked example"]),
        S("table", {"name": title[:40], "cols": [((t[:22] + "…") if len(t) > 22 else t, "NOTE", f"{i+1}/{len(notes)}")
                                                  for i, t in enumerate(notes[:5])] or [("overview", "NOTE", "1/1")]},
          f"Note index for {title}: use this map to navigate the module's notes.",
          f"Table of notes in {title}", ["concepts"]),
    ]

def pick_note(notes, keywords, used):
    titles = [n.get("title", "").lower() for n in notes]
    cands = []
    for kw in keywords:
        kl = kw.lower()
        for i, t in enumerate(titles):
            if kl in t and i not in cands:
                cands.append(i)
    for i in cands:
        if i not in used:
            return i
    for i in range(len(notes)):
        if i not in used:
            return i
    return cands[0] if cands else 0

def process(path):
    bak = path + ".diagbak"
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
        backed = True
    else:
        backed = False
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    modules = data.get("modules", [])
    total = 0
    fallback_used = []
    unmapped = []
    for m in modules:
        mid = m.get("id", "")
        kit_key = ROUTES.get(mid)
        if kit_key is None:
            unmapped.append(mid)
            specs = fallback_specs(m)
            fallback_used.append(mid)
        else:
            specs = KITS[kit_key]
        assert len(specs) == 4, f"kit {kit_key} has {len(specs)} specs"
        notes = m.get("notes", [])
        if not notes:
            continue
        short = short_id(mid)
        used = set()
        for i, spec in enumerate(specs):
            fig_num = f"{short}-D{i+1}"
            html = build(spec, fig_num)
            # sanity: must be animated
            assert "il-anim" in html and "il-pop" in html, f"{fig_num} not animated"
            assert html.startswith('<figure class="il-diagram"'), f"{fig_num} bad figure"
            ni = pick_note(notes, spec[4], used)
            used.add(ni)
            body = notes[ni].get("body", "")
            notes[ni]["body"] = body + "\n\n" + html
            total += 1
    tmp = path + ".w2tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)
    # validate
    with open(path, encoding="utf-8") as f:
        json.load(f)
    return total, len(modules), backed, fallback_used, unmapped

def main():
    # sanity: every ROUTES value exists in KITS
    missing = {v for v in ROUTES.values() if v not in KITS}
    assert not missing, f"missing kits: {missing}"
    print(f"kits defined: {len(KITS)}, routes: {len(ROUTES)}")
    grand = 0
    per_file = []
    for fn in FILES:
        p = os.path.join(COURSES, fn)
        total, nmod, backed, fb, unmapped = process(p)
        grand += total
        per_file.append((fn, nmod, total, backed, fb, unmapped))
        print(f"{fn}: {nmod} modules -> {total} diagrams (backup: {'created' if backed else 'existed'})")
        for u in unmapped:
            print(f"  FALLBACK used for unmapped module: {u}")
    print(f"GRAND TOTAL: {grand} diagrams")
    return per_file, grand

if __name__ == "__main__":
    main()
