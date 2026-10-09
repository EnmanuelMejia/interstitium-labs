#!/usr/bin/env python3
"""W4: IL-19..IL-24 — 4 ANIMATED inline SVG diagrams per module.

Every diagram calls d.animate() before render (user order 2026-10-09 ~02:15 EDT:
all media animated; staggered entrances, flowing dash arrows, reduced-motion fallback).

Diagrams per module (content-derived from the module's own text):
  D1 concept_box  "The core idea"      — module objectives          -> Concepts note
  D2 table_schema "Key vocabulary"     — Concepts **term** bullets  -> Key takeaways note
  D3 compare      "Trap -> Discipline" — Common-mistakes bullets    -> Common mistakes note
  D4 flow         "Hands-on sequence"  — numbered procedure steps   -> Hands-on procedure note
Fallbacks keep 4/module when a parse yields too little.
"""
import json, re, shutil, sys, glob
sys.path.insert(0, '/home/hatch/workspace/apex-audit/.work/inline-diagrams')
from diag_framework import Diagram

FILES = [
    'il-19-multicloud-devops-ai-bootcamp.json',
    'il-20-mathematics.json',
    'il-21-humanities.json',
    'il-22-esoteric-secret-knowledge.json',
    'il-23-frontier-knowledge.json',
    'il-24-threatlocker-assessment-prep-cbt.json',
]
BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses/'

def clean(s, n=None):
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s or '')
    s = re.sub(r'__(.+?)__', r'\1', s)
    s = s.replace('`', '').replace('#', '')
    s = re.sub(r'\s+', ' ', s).strip()
    if n and len(s) > n:
        s = s[:n-1].rstrip() + '…'
    return s

def first_sentence(s, n=60):
    s = clean(s)
    for sep in ['. ', '! ', '? ', '.\n']:
        if sep in s:
            s = s.split(sep)[0] + '.'
            break
    return clean(s, n)

def find_note(notes, keywords, fallback_idx):
    for i, n in enumerate(notes):
        t = n['title'].lower()
        if any(k in t for k in keywords):
            return i
    return min(fallback_idx, len(notes)-1)

def finish(d):
    d.animate()  # REQUIRED: every diagram animates
    return d.render_figure()

# ---------- D1: core idea from objectives ----------
def d1(module, mid):
    title = clean(module['title'], 52)
    lines = [clean(o, 52) for o in (module.get('objectives') or [])[:3]]
    if not lines:
        lines = [clean(module.get('summary',''), 52)]
    d = Diagram(fig_num=f"{mid}-D1",
        caption=(f"The core idea of {title}: these are the competencies this module builds. "
                 "Every note, lab, and drill below serves them — if you can do these, you own the module."),
        alt=f"Diagram summarizing the core competencies taught in {title}")
    d.concept_box(title, lines, x=(720-380)/2, y=10, w=380)
    return finish(d), find_note(module['notes'], ['concept'], 0)

# ---------- D2: vocabulary table from Concepts bullets ----------
def d2(module, mid):
    title = clean(module['title'], 40)
    body = ''
    for n in module['notes']:
        if 'concept' in n['title'].lower():
            body = n['body']; break
    if not body and module['notes']:
        body = module['notes'][0]['body']
    rows = []
    for term, defi in re.findall(r'^-\s*\*\*(.+?)\*\*\s*[—–:\-]\s*(.+)$', body, re.M)[:6]:
        rows.append((clean(term, 22), '', clean(defi, 46)))
    if len(rows) < 3:
        # fallback: concept box of key ideas
        lines = [clean(t, 52) for t, _ in re.findall(r'^-\s*\*\*(.+?)\*\*\s*(.+)$', body, re.M)[:4]]
        if not lines:
            for n in module['notes']:
                if 'takeaway' in n['title'].lower():
                    lines = [clean(l, 52) for l in re.findall(r'^-\s*(.+)$', n['body'], re.M)[:4]]
                    break
        d = Diagram(fig_num=f"{mid}-D2",
            caption=(f"Key ideas to carry out of {title}. Read them once before the module and once after — "
                     "the second read should feel obvious; if it doesn't, revisit the Concepts note."),
            alt=f"Diagram listing the key ideas of {title}")
        d.concept_box(f"Key ideas — {title}", lines or ['Work the module top to bottom.'],
                      x=(720-380)/2, y=10, w=380)
        return finish(d), find_note(module['notes'], ['takeaway'], len(module['notes'])-1)
    d = Diagram(fig_num=f"{mid}-D2",
        caption=(f"The working vocabulary of {title} at a glance: term on the left, its working meaning on the right. "
                 "Learn these cold — every procedure and worked example in the module assumes them."),
        alt=f"Vocabulary table for {title}: key terms and their meanings")
    d.table_schema(f"Key vocabulary — {title}", rows, x=(720-460)/2, y=10, col_w=460)
    return finish(d), find_note(module['notes'], ['takeaway'], len(module['notes'])-1)

# ---------- D3: trap -> discipline compare from Common mistakes ----------
def d3(module, mid):
    title = clean(module['title'], 40)
    body = ''
    for n in module['notes']:
        if 'mistake' in n['title'].lower():
            body = n['body']; break
    pairs = []
    for bold, rest in re.findall(r'^-\s*\*\*(.+?)\*\*\s*(.+)$', body, re.M)[:4]:
        trap = clean(bold.rstrip('.:;'), 34)
        fix = first_sentence(rest.lstrip('—–:-. '), 40)
        pairs.append((trap, fix))
    if len(pairs) < 2:
        lines = [clean(b.rstrip('.:;'), 52) for b, _ in re.findall(r'^-\s*\*\*(.+?)\*\*', body, re.M)[:4]]
        d = Diagram(fig_num=f"{mid}-D3",
            caption=(f"Traps to avoid in {title}. Each is a failure mode learners actually hit — "
                     "read the Common mistakes note for the full fix behind each one."),
            alt=f"Diagram listing common traps to avoid in {title}")
        from diag_framework import RED
        d.concept_box(f"Traps to avoid — {title}", lines or ['See the Common mistakes note.'],
                      x=(720-380)/2, y=10, w=380, accent=RED)
        return finish(d), find_note(module['notes'], ['mistake'], len(module['notes'])-1)
    left = [p[0] for p in pairs]
    right = [p[1] for p in pairs]
    d = Diagram(fig_num=f"{mid}-D3",
        caption=(f"Where learners go wrong in {title} — each trap paired with the discipline that fixes it. "
                 "Red is the failure mode; green is what operators actually do."),
        alt=f"Comparison diagram for {title}: common traps versus the correct disciplines")
    d.compare("Common trap", left, "The discipline", right)
    return finish(d), find_note(module['notes'], ['mistake'], len(module['notes'])-1)

# ---------- D4: hands-on sequence flow from numbered steps ----------
def d4(module, mid):
    title = clean(module['title'], 40)
    body = ''
    for n in module['notes']:
        if 'procedure' in n['title'].lower() or 'hands-on' in n['title'].lower():
            body = n['body']; break
    steps = []
    n_steps = min(5, len(re.findall(r'^\d+\.\s*(.+)$', body, re.M)))
    gap = 24
    box_w = min(130, (680 - max(0, n_steps-1)*gap) / max(1, n_steps))
    lab_n = max(10, int(box_w / 8.6))
    sub_n = max(12, int(box_w / 6.8))
    for s in re.findall(r'^\d+\.\s*(.+)$', body, re.M)[:5]:
        s = s.strip()
        mb = re.match(r'\*\*(.+?)\*\*\s*(.*)$', s)
        if mb:
            label, sub = clean(mb.group(1), lab_n), clean(mb.group(2), sub_n)
        else:
            label, sub = clean(s, lab_n), ''
        steps.append((label or f"Step {len(steps)+1}", sub))
    if len(steps) >= 3:
        n = len(steps)
        d = Diagram(fig_num=f"{mid}-D4",
            caption=(f"The hands-on sequence for {title}: work the steps in order — "
                     "each one assumes the previous is done. Watch the flow build left to right."),
            alt=f"Flow diagram of the hands-on lab steps for {title}")
        d.flow(steps, y=60, box_w=box_w, box_h=64, gap=gap)
        return finish(d), find_note(module['notes'], ['procedure', 'hands-on'], 1)
    # fallback: module roadmap layers
    layers = []
    for n in module['notes'][:6]:
        layers.append((clean(n['title'], 46), clean(n['body'], 46)))
    d = Diagram(fig_num=f"{mid}-D4",
        caption=(f"Module roadmap for {title}: how this module is organized, top to bottom. "
                 "Start at the top layer and work down — the order is deliberate."),
        alt=f"Layered roadmap diagram showing the note structure of {title}")
    d.layers(layers, x=120, y=20, w=480, layer_h=52)
    return finish(d), find_note(module['notes'], ['procedure', 'hands-on'], 1)

def process_file(path):
    with open(path + '.diagbak', 'w') as bf, open(path) as f:
        bf.write(f.read())
    data = json.load(open(path))
    added = 0
    skipped = 0
    for m in data['modules']:
        mid = m.get('id') or m.get('code') or 'M'
        # idempotency: skip if already processed
        if any(f"Fig. {mid}-D1" in n.get('body','') for n in m.get('notes', [])):
            skipped += 1
            continue
        notes = m.get('notes', [])
        if not notes:
            skipped += 1
            continue
        for gen in (d1, d2, d3, d4):
            try:
                html, idx = gen(m, mid)
                notes[idx]['body'] = notes[idx].get('body','').rstrip() + '\n\n' + html
                added += 1
            except Exception as e:
                print(f"  WARN {mid}: {gen.__name__} failed: {e}")
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    # validate
    json.load(open(path))
    return len(data['modules']), added, skipped

def main():
    total_mods = total_added = total_skipped = 0
    for fname in FILES:
        path = BASE + fname
        before = open(path).read().count('class="il-diagram"')
        mods, added, skipped = process_file(path)
        after = open(path).read().count('class="il-diagram"')
        anim = open(path).read().count('class="il-anim"')
        print(f"{fname}: modules={mods} added={added} skipped={skipped} "
              f"figures {before}->{after} animated_svgs={anim}")
        total_mods += mods; total_added += added; total_skipped += skipped
    print(f"TOTAL: modules={total_mods} diagrams_added={total_added} skipped={total_skipped}")

if __name__ == '__main__':
    main()
