#!/usr/bin/env python3
"""W3 inline-diagram worker: 4 diagrams per module for IL-13..IL-18.
Derives diagram content from the module's own notes (concept terms,
numbered procedure steps, worked-example moves, pitfalls, objectives).
Embeds each figure HTML at the end of the most topical note body.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from diag_framework import Diagram

COURSES = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
FILES = [
    "il-13-software-engineering-interview-prep",
    "il-14-sre-devops-cloud-security-interview-prep",
    "il-15-data-engineering-analytics-interview-prep",
    "il-16-machine-learning-ai-engineering",
    "il-17-agentic-ai-engineering",
    "il-18-technical-leadership-interview-prep",
]

# ---------- text helpers ----------
def trunc(s, n):
    s = " ".join(str(s).split())
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0] if " " in s[:n] else s[:n]
    return cut.rstrip(" ,;:") + "\u2026"

def bold_term(line):
    """Return (term, rest) for lines like '- **Term** \u2014 definition' or None."""
    s = line.strip()
    if not (s.startswith("- **") or s.startswith("* **")):
        return None
    inner = s[4:]  # "- **" and "* **" are both 4 chars
    parts = inner.split("**", 1)
    if len(parts) < 2:
        return None
    term = parts[0].strip()
    rest = parts[1].strip().lstrip("\u2014\u2013-: ").strip()
    if not term or len(term) > 60:
        return None
    return term, rest

def numbered_step(line):
    """Return step title for lines like '1. **Step title** ...' or '1. Step title ...'."""
    s = line.strip()
    if not s or not s[0].isdigit():
        return None
    parts = s.split(" ", 1)
    if len(parts) != 2:
        return None
    if not parts[0].rstrip(".):").isdigit():
        return None
    title = parts[1].strip()
    if title.startswith("**"):
        title = title[2:].split("**", 1)[0].strip()
    return title or None

def concept_terms(body, n):
    out = []
    for ln in body.splitlines():
        bt = bold_term(ln)
        if bt:
            out.append(bt)
        if len(out) >= n:
            break
    return out

def steps_of(body, n):
    out = []
    for ln in body.splitlines():
        st = numbered_step(ln)
        if st:
            out.append(st)
        if len(out) >= n:
            break
    return out

def short_slug(mid, title):
    seg = mid
    for sep in ("--",):
        if sep in seg:
            seg = seg.split(sep)[-1]
    if not seg or len(seg) > 40:
        words = "".join(c if c.isalnum() or c == " " else "" for c in title).split()[:3]
        seg = "-".join(words).lower() or "module"
    return seg

def note_by_title(notes, *keys):
    for n in notes:
        t = (n.get("title") or "").lower()
        for k in keys:
            if k in t:
                return n
    return None

# ---------- diagram builders ----------
def d1_layers(module, slug, concepts_body):
    terms = concept_terms(concepts_body, 6)
    if len(terms) < 2:
        objs = [o for o in (module.get("objectives") or [])]
        terms = [(trunc(o.split(":", 1)[-1], 40), "") for o in objs[:6]]
    layers = []
    for term, rest in terms[:6]:
        layers.append((trunc(term, 52), trunc(rest, 60) if rest else ""))
    d = Diagram(fig_num=slug + "-D1",
                caption=("The concept stack of %s: master these ideas in order, "
                         "each layer building on the ones below it."
                         % module.get("title", "")),
                alt=("Layered stack diagram of the core concepts in %s, ordered from foundation to application."
                     % module.get("title", "")))
    d.layers(layers, accent="#58a6ff")
    d.animate()
    return d.render_figure()

def d2_flow(module, slug, proc_body):
    steps = steps_of(proc_body, 5)
    if len(steps) < 2:
        objs = module.get("objectives") or []
        steps = [trunc(o.split(":", 1)[-1], 34) for o in objs[:5]]
    labels = [(trunc(s, 18), "") for s in steps[:5]]
    d = Diagram(fig_num=slug + "-D2",
                caption=("The hands-on procedure for %s. Follow the sequence left to right; "
                         "each step builds on the previous one, and skipping steps is where points are lost."
                         % module.get("title", "")),
                alt=("Horizontal flow diagram of the step-by-step procedure for %s."
                     % module.get("title", "")))
    d.flow(labels, accent="#39c5cf")
    d.animate()
    return d.render_figure()

def d3_compare(module, slug, example_body, pitfalls_body):
    good_steps = steps_of(example_body, 5)
    good = [(s, "") for s in good_steps] if good_steps else concept_terms(example_body, 5)
    bad = concept_terms(pitfalls_body, 5)
    if not good:
        good = [(trunc(ln.strip().lstrip("-* ").strip(), 34), "")
                for ln in example_body.splitlines() if ln.strip().startswith(("- ", "* "))][:5]
    if not bad:
        bad = [(trunc(ln.strip().lstrip("-* ").strip(), 34), "")
               for ln in pitfalls_body.splitlines() if ln.strip().startswith(("- ", "* "))][:5]
    left = [trunc(t, 34) for t, _ in bad[:5]] or ["(see pitfalls note)"]
    right = [trunc(t, 34) for t, _ in good[:5]] or ["(see worked example note)"]
    d = Diagram(fig_num=slug + "-D3",
                caption=("What loses points versus what earns them in %s. "
                         "The left column is the interview anti-pattern; the right column is the strong answer."
                         % module.get("title", "")),
                alt=("Two-column comparison for %s: pitfalls that lose points on the left, strong habits on the right."
                     % module.get("title", "")))
    d.compare("Pitfalls that lose points", left,
              "Strong moves that earn them", right,
              left_accent="#f85149", right_accent="#3fb950")
    d.animate()
    return d.render_figure()

def d4_checklist(module, slug):
    objs = module.get("objectives") or []
    lines = []
    for o in objs[:6]:
        meat = o.split(":", 1)[-1].strip()
        lines.append("\u2713 " + trunc(meat, 56))
    if not lines:
        lines = ["\u2713 " + trunc(module.get("summary", ""), 56)]
    d = Diagram(fig_num=slug + "-D4",
                caption=("The mastery checklist for %s: you are interview-ready when you can do every line "
                         "above cold, timed, and aloud." % module.get("title", "")),
                alt=("Checklist diagram of the %s learning objectives." % module.get("title", "")))
    d.concept_box("Mastery checklist", lines, x=80, w=560, accent="#a371f7")
    d.animate()
    return d.render_figure()

# ---------- main ----------
def process_file(fname):
    path = os.path.join(COURSES, fname + ".json")
    bak = path + ".diagbak"
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    doc = json.load(open(path))
    mods = doc.get("modules", [])
    count = 0
    for mi, m in enumerate(mods):
        notes = m.get("notes", [])
        if not notes:
            continue
        slug = short_slug(m.get("id", ""), m.get("title", ""))
        concepts = note_by_title(notes, "concept")
        proc = note_by_title(notes, "procedure", "hands-on")
        example = note_by_title(notes, "worked example")
        pitfalls = note_by_title(notes, "pitfall", "mistake")
        brief = note_by_title(notes, "project brief")
        f1 = d1_layers(m, slug, (concepts or notes[0]).get("body", ""))
        f2 = d2_flow(m, slug, (proc or notes[min(1, len(notes)-1)]).get("body", ""))
        f3 = d3_compare(m, slug,
                        (example or notes[min(4, len(notes)-1)]).get("body", ""),
                        (pitfalls or notes[-1]).get("body", ""))
        f4 = d4_checklist(m, slug)
        plan = [
            ((concepts or notes[0]), f1),
            ((proc or notes[min(1, len(notes)-1)]), f2),
            ((pitfalls or notes[-1]), f3),
            ((brief or notes[-1]), f4),
        ]
        for note, fig in plan:
            body = note.get("body") or ""
            note["body"] = body.rstrip() + "\n\n" + fig
            count += 1
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)  # files use 1-space indent
    json.load(open(tmp))  # validate before replace
    os.replace(tmp, path)
    return len(mods), count

def main():
    total_mods = 0
    total_figs = 0
    per_file = {}
    for f in FILES:
        nmods, nfigs = process_file(f)
        per_file[f] = (nmods, nfigs)
        total_mods += nmods
        total_figs += nfigs
        print("%s: modules=%d figures=%d" % (f, nmods, nfigs))
    print("TOTAL modules=%d figures=%d" % (total_mods, total_figs))
    with open(os.path.join(HERE, "w3-counts.json"), "w") as fh:
        json.dump({"per_file": per_file, "total_modules": total_mods,
                   "total_figures": total_figs}, fh, indent=2)

if __name__ == "__main__":
    main()
