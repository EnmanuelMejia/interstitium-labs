#!/usr/bin/env python3
"""W6: bootcamp batch — 3 ANIMATED SVG diagrams per lesson (607 lessons).
Every diagram calls d.animate() before d.render_svg().
Writes SVGs to <bootcamp>/assets/diagrams/, appends media[] entries.
"""
import json, os, re, sys, shutil

BASE = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")
FW = os.path.expanduser("~/workspace/apex-audit/.work/inline-diagrams")
sys.path.insert(0, FW)
from diag_framework import Diagram

def clean(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()

def trunc(s, n):
    s = clean(s)
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

def label_of(concept, max_words=6, max_chars=30):
    s = clean(concept)
    if ":" in s:
        head = s.split(":", 1)[0].strip()
        if 3 <= len(head) <= 40 and len(head.split()) <= 7:
            return trunc(head, max_chars)
    return trunc(" ".join(s.split()[:max_words]), max_chars)

def gist_of(concept, max_chars=34):
    s = clean(concept)
    if ":" in s:
        return trunc(s.split(":", 1)[1], max_chars)
    words = s.split()
    return trunc(" ".join(words[3:]) or s, max_chars)

def short_title(t):
    t = clean(t)
    t = re.sub(r"\s*[—–-]\s*Core concepts\s*$", "", t)
    return trunc(t, 46)

def slugify(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "-", clean(s)) or "topic"

# ---------- diagram builders (each animated) ----------
def b_flow(lesson):
    concepts = [c for c in lesson.get("concepts", []) if isinstance(c, str) and clean(c)][:4]
    d = Diagram()
    d.flow([(label_of(c, 3, 16), gist_of(c, 20)) for c in concepts])
    return d

def b_layers(lesson):
    concepts = [c for c in lesson.get("concepts", []) if isinstance(c, str) and clean(c)][:5]
    d = Diagram()
    d.layers([(label_of(c, 6, 34), gist_of(c, 48)) for c in concepts])
    return d

def b_compare(lesson):
    traps = [p for p in lesson.get("pitfalls", []) if isinstance(p, str) and clean(p)][:4]
    moves = [c for c in lesson.get("concepts", []) if isinstance(c, str) and clean(c)][:4]
    d = Diagram()
    d.compare("Common traps", [trunc(re.sub(r"^Common trap:\s*", "", t), 30) for t in traps],
              "Winning moves", [label_of(c, 5, 30) for c in moves])
    return d

def b_table(lesson):
    concepts = [c for c in lesson.get("concepts", []) if isinstance(c, str) and clean(c)][:6]
    cols = []
    for i, c in enumerate(concepts):
        cols.append((label_of(c, 4, 24), gist_of(c, 20), "KEY" if i < 2 else ""))
    d = Diagram()
    d.table_schema(trunc(short_title(lesson.get("title", "Lesson")), 40), cols, col_w=360)
    return d

def b_boxes(lesson):
    ideas = [c for c in lesson.get("concepts", []) if isinstance(c, str) and clean(c)][:5]
    traps = [p for p in lesson.get("pitfalls", []) if isinstance(p, str) and clean(p)][:5]
    d = Diagram()
    d.concept_box("Core ideas", [label_of(c, 6, 30) for c in ideas],
                  x=20, y=10, w=330, accent="#3fb950")
    d.concept_box("Common traps",
                  [trunc(re.sub(r"^Common trap:\s*", "", t), 30) for t in traps],
                  x=370, y=10, w=330, accent="#d29922")
    return d

def has_pitfalls(lesson):
    return any(isinstance(p, str) and clean(p) for p in lesson.get("pitfalls", []))

# rotation: vary types per lesson
ROTATIONS = [
    [("flow", b_flow, "build order"), ("layers", b_layers, "knowledge stack"), ("compare", b_compare, "traps vs moves")],
    [("compare", b_compare, "traps vs moves"), ("table", b_table, "concept contract"), ("flow", b_flow, "build order")],
    [("table", b_table, "concept contract"), ("boxes", b_boxes, "ideas at a glance"), ("layers", b_layers, "knowledge stack")],
    [("boxes", b_boxes, "ideas at a glance"), ("compare", b_compare, "traps vs moves"), ("flow", b_flow, "build order")],
]

CAPTION_OF = {
    "flow": "Watch {t} assemble stage by stage — nodes pop in sequence so the progression reads as a build order.",
    "layers": "The {t} stack builds top-down, one layer at a time — from the highest abstraction down to the ground truth.",
    "compare": "Traps on the left, winning moves on the right — watch each pair land and keep the contrast in mind.",
    "table": "The concept contract for {t} — each key idea, what it means, and where it pays off.",
    "boxes": "{t} at a glance: core ideas on the left, the traps that bite practitioners on the right.",
}

def process_bootcamp(slug, stats):
    path = os.path.join(BASE, slug, "content.json")
    if not os.path.exists(path):
        stats["errors"].append(f"{slug}: no content.json")
        return
    bak = path + ".diagbak"
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    with open(path) as f:
        data = json.load(f)
    lessons = data.get("lessons", [])
    media = data.setdefault("media", [])
    existing_ids = {m.get("id") for m in media}
    ddir = os.path.join(BASE, slug, "assets", "diagrams")
    os.makedirs(ddir, exist_ok=True)
    made = 0
    gi0 = stats["gi"]
    for li, lesson in enumerate(lessons):
        concepts = [c for c in (lesson.get("concepts") or []) if isinstance(c, str) and clean(c)]
        if not concepts:
            stats["skipped"].append(f"{slug}/{lesson.get('domain_id')}: no concepts")
            continue
        domain = lesson.get("domain_id") or f"lesson-{li}"
        rot = ROTATIONS[(gi0 + li) % len(ROTATIONS)]
        st = short_title(lesson.get("title", domain))
        for di, (kind, builder, topic) in enumerate(rot, start=1):
            if kind in ("compare", "boxes") and not has_pitfalls(lesson):
                kind, builder, topic = "flow", b_flow, "build order"
            d = builder(lesson)
            d.animate()                      # <-- animated, per user order
            svg = d.render_svg()
            assert "il-anim" in svg and "@keyframes il-pop" in svg, "animation missing!"
            fname = f"{slugify(slug)}-{slugify(domain)}-d{di}.svg"
            ctr = 2
            while fname in stats.get("files_seen", set()):
                fname = f"{slugify(slug)}-{slugify(domain)}-d{di}v{ctr}.svg"
                ctr += 1
            stats.setdefault("files_seen", set()).add(fname)
            with open(os.path.join(ddir, fname), "w") as f:
                f.write(svg)
            mid = f"{slug}-{slugify(domain)}-d{di}"
            k = 2
            while mid in existing_ids:
                mid = f"{slug}-{slugify(domain)}-d{di}v{k}"
                k += 1
            existing_ids.add(mid)
            first_c = trunc(concepts[0], 140)
            media.append({
                "id": mid,
                "kind": "diagram",
                "title": f"{st} — {topic}",
                "svg": f"assets/diagrams/{fname}",
                "lesson_ref": f"c-{domain}",
                "caption": CAPTION_OF[kind].format(t=st) + " " + first_c,
                "alt": f"Animated diagram: {st} — {topic}.",
            })
            made += 1
    # atomic-ish write + validate
    tmp = path + ".w6tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(tmp) as f:
        json.load(f)  # validate
    os.replace(tmp, path)
    stats["per_bootcamp"][slug] = made
    stats["gi"] = gi0 + len(lessons)
    stats["total"] += made

def main():
    stats = {"total": 0, "gi": 0, "per_bootcamp": {}, "errors": [], "skipped": [], "files_seen": set()}
    slugs = sorted(d for d in os.listdir(BASE)
                   if d != "_engine" and os.path.isdir(os.path.join(BASE, d)))
    only = os.environ.get("W6_ONLY")
    if only:
        slugs = [s for s in slugs if s == only]
    for slug in slugs:
        try:
            process_bootcamp(slug, stats)
        except Exception as e:
            stats["errors"].append(f"{slug}: {type(e).__name__}: {e}")
    n_files = len(stats.pop("files_seen"))
    print(json.dumps({"total_media_entries": stats["total"], "svg_files": n_files,
                      "bootcamps": len(stats["per_bootcamp"]),
                      "errors": stats["errors"], "skipped": stats["skipped"]}, indent=1))
    with open(os.path.expanduser("~/workspace/apex-audit/.work/inline-diagrams/w6-stats.json"), "w") as f:
        json.dump({"total": stats["total"], "per_bootcamp": stats["per_bootcamp"],
                   "errors": stats["errors"], "skipped": stats["skipped"]}, f, indent=1)

if __name__ == "__main__":
    main()
