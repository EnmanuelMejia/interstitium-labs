#!/usr/bin/env python3
"""
W5 inline-diagram generator — IL-25..IL-29, 4 diagrams per module.

Templates (all grounded in the module's own content):
  D1  flow   "Module path"   — first 4 note titles as an ordered reading path
        (alternates with layers() stack of ALL note titles for variety)
  D2  concept_box "Key vocabulary" — **bold** terms harvested from note bodies
  D3  table_schema "Module anatomy" — component inventory (notes/objectives/cards/quiz/...)
  D4  compare "Know vs Do" — objectives split by lead verb (Bloom's);
        falls back to concept_box "How mastery is checked" if one side is empty
"""
import json, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from diag_framework import Diagram

STOP = set("""the a an of and or to in on for with as by at from is are was were be been
being it its this that these those you your we our they their them he she his her not no yes
do does did will would can could should shall may might must have has had having all any each
every other some such only just over under more most less least than then so into out up down
off about between through during before after again once here there when where which who whom
whose what why how both few many same too very now your you're""".split())

KNOW_VERBS = {'define','describe','explains','explain','identify','list','recognize',
    'recall','understand','distinguish','summarize','outline','state','name',
    'differentiate','classify','discuss','interpret','compare','contrast'}
DO_VERBS = {'apply','build','configure','implement','analyze','evaluate','create',
    'design','deploy','solves','solve','write','demonstrate','perform','troubleshoot',
    'calculate','convert','translate','use','develop','construct','execute','run','set',
    'install','harden','monitor','detect','respond','investigate','plan','prepare',
    'produce','generate','measure','assess','audit','tests','test','verify','validate',
    'optimize','automate','script','code','query','model','visualize','present',
    'communicate','recommend','prioritize','rank','select','choose','complete',
    'practice','simulate','inspect','examine','explore','map','document'}


def shorten(text, n):
    t = re.sub(r'\s+', ' ', str(text)).strip()
    if len(t) <= n:
        return t
    cut = t[:n - 1].rsplit(' ', 1)[0]
    return (cut if cut else t[:n - 1]) + '…'


def extract_terms(module):
    """Harvest **bold** vocabulary terms from note bodies, in order."""
    terms, seen = [], set()
    for note in module.get('notes', []):
        for raw in re.findall(r'\*\*(.+?)\*\*', note.get('body', '')):
            t = re.sub(r'\s+', ' ', raw).strip()
            if len(t) < 2 or len(t) > 52:
                continue
            if any(c in t for c in '[](){}|`') or 'http' in t.lower():
                continue
            if t.isdigit():
                continue
            key = t.lower()
            if key not in seen:
                seen.add(key)
                terms.append(t)
            if len(terms) >= 8:
                break
        if len(terms) >= 8:
            break
    if len(terms) < 3:
        # fallback: distinctive words from note titles
        for note in module.get('notes', []):
            for w in re.findall(r"[A-Za-z][A-Za-z\-']{3,}", note.get('title', '')):
                wl = w.lower()
                if wl in STOP or len(w) > 30:
                    continue
                if wl not in seen:
                    seen.add(wl)
                    terms.append(w)
                if len(terms) >= 6:
                    break
            if len(terms) >= 6:
                break
    return terms[:6]


def split_objectives(objectives):
    know, do = [], []
    for o in objectives or []:
        words = re.findall(r"[A-Za-z']+", o)
        verb = words[0].lower() if words else ''
        (know if verb in KNOW_VERBS else do).append(o)
    return know, do


def note_index_by_keyword(notes, keywords, default):
    for i, n in enumerate(notes):
        t = n.get('title', '').lower()
        if any(k in t for k in keywords):
            return i
    return default


def build_module_diagrams(module, mod_idx):
    mid = module.get('id') or f'M{mod_idx + 1:02d}'
    title = module.get('title', 'this module')
    notes = module.get('notes', [])
    objectives = module.get('objectives', [])
    n = len(notes)
    if n == 0:
        return []

    title_short = shorten(title, 44)
    figs = []  # (note_idx, html)

    # ---- D1: module path — flow (even) or layers stack (odd) ----
    if mod_idx % 2 == 0:
        steps = [(shorten(nt.get('title', ''), 16), f"Note {i + 1}")
                 for i, nt in enumerate(notes[:4])]
        d = Diagram(fig_num=f"{mid}-D1",
                    caption=(f"Read the notes in order — {shorten(notes[0].get('title',''), 34)} "
                             f"lays the foundation and {shorten(notes[min(3, n-1)].get('title',''), 34)} "
                             f"brings it together. Each note assumes the vocabulary of the ones before it."),
                    alt=f"Flow diagram: the opening notes of {title_short}, in reading order")
        d.flow(steps, box_w=150)
        idx = 0
    else:
        layers = [(shorten(nt.get('title', ''), 52), f"Note {i + 1} of {n}")
                  for i, nt in enumerate(notes)]
        d = Diagram(fig_num=f"{mid}-D1",
                    caption=(f"The module's full stack, top to bottom: start at {shorten(notes[0].get('title',''), 34)} "
                             f"and work down to {shorten(notes[-1].get('title',''), 34)}. "
                             f"Each layer builds on the one above it — skipping ahead leaves gaps."),
                    alt=f"Layered stack diagram: all {n} notes of {title_short}, top to bottom")
        d.layers(layers)
        idx = 0
    d.animate()
    figs.append((idx, d.render_figure()))

    # ---- D2: key vocabulary ----
    terms = extract_terms(module)
    d = Diagram(fig_num=f"{mid}-D2",
                caption=(f"The vocabulary this module installs — {', '.join(terms[:3])}"
                         f"{'…' if len(terms) > 3 else ''}. If you can define each term in "
                         f"one plain sentence, the module's objectives are within reach."),
                alt=f"Key vocabulary box listing {len(terms)} core terms from {title_short}")
    d.concept_box(f"Key vocabulary · {mid}", [shorten(t, 44) for t in terms],
                  x=110, w=500)
    idx = note_index_by_keyword(notes, ['concept'], 1)
    # prefer the note containing the most extracted terms
    best, bestc = idx, -1
    for i, nt in enumerate(notes):
        body = nt.get('body', '').lower()
        c = sum(1 for t in terms if t.lower() in body)
        if c > bestc:
            best, bestc = i, c
    d.animate()
    figs.append((best, d.render_figure()))

    # ---- D3: module anatomy (table_schema) ----
    rows = []
    rows.append(("Notes", "teaching sections", str(n)))
    rows.append(("Objectives", "measurable outcomes", str(len(objectives))))
    for key, role in (("cards", "flashcard drills"), ("quiz", "knowledge checks"),
                      ("drills", "timed practice"), ("videos", "curated watch"),
                      ("pdfs", "visual guides")):
        v = module.get(key)
        if isinstance(v, list) and v:
            rows.append((key.capitalize(), role, str(len(v))))
    if module.get('handsOnLab'):
        rows.append(("Hands-on lab", "guided exercise", "1"))
    if module.get('mockTask'):
        rows.append(("Mock task", "exam rehearsal", "1"))
    rows = rows[:7]
    total_parts = sum(int(r[2]) for r in rows[2:] if r[2].isdigit())
    d = Diagram(fig_num=f"{mid}-D3",
                caption=(f"What's inside \u201c{title_short}\u201d: {n} teaching notes and "
                         f"{len(objectives)} objectives, backed by {total_parts} practice components. "
                         f"Notes carry the teaching; everything else converts reading into recall."),
                alt=f"Table listing the components of {title_short}: notes, objectives, cards, quiz and practice items")
    d.table_schema(f"{mid} · module anatomy",
                   [(nm, role, cnt) for nm, role, cnt in rows],
                   x=130, col_w=460)
    d.animate()
    figs.append((n - 1, d.render_figure()))

    # ---- D4: Know vs Do ----
    know, do = split_objectives(objectives)
    if know and do:
        d = Diagram(fig_num=f"{mid}-D4",
                    caption=("Certification exams test two things: what you can explain (left) and what you "
                             "can do (right). This module's objectives split that way — drill the left column "
                             "for recall, and practice the right column hands-on under time pressure."),
                    alt=f"Two-column comparison of {title_short} objectives: explain versus do")
        d.compare("KNOW — explain it", [shorten(o, 40) for o in know[:5]],
                  "DO — perform it", [shorten(o, 40) for o in do[:5]])
    else:
        lines = []
        q, dr, c = module.get('quiz'), module.get('drills'), module.get('cards')
        if isinstance(q, list) and q:
            lines.append(f"{len(q)} quiz questions — recall under no pressure")
        if isinstance(dr, list) and dr:
            lines.append(f"{len(dr)} drills — timed, exam-style repetition")
        if isinstance(c, list) and c:
            lines.append(f"{len(c)} flashcards — spaced recall of key terms")
        if module.get('mockTask'):
            lines.append("Mock task — full exam rehearsal")
        if module.get('handsOnLab'):
            lines.append("Hands-on lab — guided real-tool practice")
        if not lines:
            lines = ["Work every note's examples by hand", "Re-teach each concept aloud"]
        d = Diagram(fig_num=f"{mid}-D4",
                    caption=(f"How this module checks mastery: {len(lines)} practice channels. "
                             f"Reading the notes is the input — these are the outputs that prove it stuck."),
                    alt=f"Box listing how mastery of {title_short} is checked: quiz, drills, cards")
        d.concept_box(f"How mastery is checked · {mid}", [shorten(l, 52) for l in lines[:6]],
                      x=110, w=500, accent="#a371f7")
    idx = note_index_by_keyword(notes, ['procedure', 'hands-on', 'practice', 'lab', 'project'], 2)
    d.animate()
    figs.append((idx, d.render_figure()))

    # dedupe note targets (bump forward on collision)
    used, placed = set(), []
    for i, html in figs:
        while i in used:
            i = (i + 1) % n
        used.add(i)
        placed.append((i, html))
    return placed


def process_file(path):
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    data = json.loads(raw)
    trailing_nl = raw.endswith('\n')
    added = 0
    skipped = []
    for mi, module in enumerate(data.get('modules', [])):
        notes = module.get('notes', [])
        if not notes:
            skipped.append(module.get('id', f'index-{mi}'))
            continue
        for ni, html in build_module_diagrams(module, mi):
            notes[ni]['body'] = notes[ni].get('body', '') + "\n\n" + html
            added += 1
    out = json.dumps(data, indent=2, ensure_ascii=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out + ('\n' if trailing_nl else ''))
    # validate
    json.load(open(path, encoding='utf-8'))
    return added, skipped


if __name__ == '__main__':
    base = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
    files = ['il-25-cybersecurity-professional-certificate.json',
             'il-26-data-analyst-certification-senior-mastery.json',
             'il-27-it-infrastructure-specialist-threatlocker-mastery.json',
             'il-28-devsecops-cloud-infrastructure-mastery.json',
             'il-29-threatlocker-ai-cybersecurity-mastery.json']
    total = 0
    for fn in files:
        p = os.path.join(base, fn)
        added, skipped = process_file(p)
        total += added
        print(f"{fn}: +{added} diagrams, skipped={skipped}")
    print(f"TOTAL: {total}")
