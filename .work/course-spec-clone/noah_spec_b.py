#!/usr/bin/env python3
"""Document noahTutoring in Group B spec sheets."""
import json

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses/'
OUT = '/home/hatch/workspace/apex-audit/.work/course-spec-clone/specs/'
FILES = {
 "IL-07": "il-07-data-engineering-analytics-ai.json",
 "IL-08": "il-08-algorithms-compilers-distributed-formal.json",
 "IL-09": "il-09-adaptive-certification-command.json",
 "IL-10": "il-10-portfolio-career-professional-practice.json",
 "IL-11": "il-11-zero-trust-endpoint-defense.json",
 "IL-12": "il-12-ai-engineering.json",
}

for code, fn in FILES.items():
    d = json.load(open(BASE + fn))
    nt = d["noahTutoring"]
    L = []
    A = L.append
    A("## Noah Tutoring — the core learning driver")
    A("")
    A(nt["concept"])
    A("")
    A("**Personas → modules:**")
    A("")
    for p in nt["personas"]:
        A("- **%s** (%s): %s" % (p["name"], p["id"], p["role"]))
        A("  - Modules: %s" % ", ".join(p["modules"]))
    A("")
    A("**Voices:** %s" % nt["voices"]["description"])
    A("")
    A("**Voice-first:** %s" % nt["voices"]["voiceFirst"])
    A("")
    A("**Adaptive (%s):** %s" % (nt["adaptive"]["method"], nt["adaptive"]["description"]))
    A("")
    A("**Course-aware:** %s" % nt["courseAware"]["description"])
    A("")
    be = nt["bleedingEdge"]
    A("**Bleeding edge:** %s" % be["note"])
    A("")
    A("**Rule:** %s" % nt["rule"])
    A("")
    section = "\n".join(L)
    path = OUT + code + ".md"
    text = open(path).read()
    marker = "\n---\n"
    assert marker in text, code
    assert "Noah Tutoring" not in text, code  # idempotent
    text = text.replace(marker, "\n" + section + marker, 1)
    open(path, "w").write(text)
    print(code, "spec updated")
