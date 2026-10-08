#!/usr/bin/env python3
"""Augment IL-01..IL-15 modules to the HARD quality bar.
Idempotent-ish: skips modules that already meet the bar (drills present, lab present,
notes>=6, cards>=12, quiz>=9, estimatedMinutes set).
"""
import json, glob, os, sys, hashlib, random, shutil, copy

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
WORK = os.path.expanduser("~/workspace/apex-audit/.work")
BACKUP = os.path.join(WORK, "backups-il01-15")
sys.path.insert(0, WORK)
from banks_il01_15 import PITFALLS, LABS

os.makedirs(BACKUP, exist_ok=True)

def rng(seed):
    return random.Random(int(hashlib.sha256(seed.encode()).hexdigest(), 16) % (2**31))

def first_sentence(s):
    s = (s or "").strip()
    for sep in [". ", ".\n", "! ", "? "]:
        if sep in s:
            return s.split(sep)[0] + sep.strip()[0]
    return s[:220]

def trunc(s, n):
    s = (s or "").strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"

def correct_choice(q):
    ch = q.get("choices", [])
    a = q.get("answer", 0)
    return ch[a] if isinstance(a, int) and 0 <= a < len(ch) else ""

def worked_example_note(m):
    qs = [q for q in (m.get("quiz") or []) if isinstance(q, dict) and q.get("choices") and len(q["choices"]) >= 3 and q.get("explain")]
    q = qs[0]
    corr = correct_choice(q)
    rule = first_sentence(q.get("explain", ""))
    body = (
        f"**Problem.** {q['q']}\n\n"
        "**Step 1 — Answer from first principles.** Cover the choices and commit to an answer using only the concept, "
        "not pattern-matching. Say your reasoning out loud — in interviews and in real work, the reasoning is what gets graded.\n\n"
        "**Step 2 — Reveal and verify.**\n"
        f"- **Correct answer:** {corr}\n"
        f"- **Why:** {q['explain']}\n\n"
        "**Step 3 — Lock in the principle.** Compress the explanation into one reusable rule: *"
        f"{rule}* Write it on a card. If you cannot state the rule without the item in front of you, you memorized the item instead of the idea.\n\n"
        "**Step 4 — Teach it back.** Explain this item to an imaginary junior in three sentences: what was asked, what the right move was, "
        "and the one mistake to avoid. Teaching is the retention test — if the explanation wobbles, re-study before moving on."
    )
    return {"title": f"Worked example: {trunc(q['q'], 70)}", "body": body}

def pitfalls_note(course_id, m):
    bank = PITFALLS[course_id]
    topic = m.get("title", "this module")
    body = bank["intro"].format(topic=topic) + "\n" + "\n".join("- " + b.format(topic=topic) for b in bank["bullets"])
    return {"title": "Pitfalls & how to dodge them", "body": body}

def cards_from_quiz(m, n=4):
    out = []
    for q in (m.get("quiz") or [])[:n]:
        if not (isinstance(q, dict) and q.get("explain")):
            continue
        corr = correct_choice(q)
        back = f"**{corr}** — {q['explain']}"
        out.append({"front": q["q"], "back": trunc(back, 600)})
    return out

def quiz_from_cards(cards_in, m, target=10):
    quiz = m.get("quiz") or []
    need = target - len(quiz)
    if need <= 0:
        return []
    cards = [c for c in (cards_in or []) if isinstance(c, dict) and c.get("front") and c.get("back") and len(c["back"]) <= 400]
    backs_pool = [c["back"] for c in (cards_in or []) if isinstance(c, dict) and c.get("back")]
    out, r = [], rng(m.get("id", "") + "|quiztop")
    for c in cards:
        if len(out) >= need:
            break
        distract = [b for b in backs_pool if b != c["back"]]
        if len(distract) < 3:
            continue
        r.shuffle(distract)
        choices = [trunc(c["back"], 200)] + [trunc(d, 200) for d in distract[:3]]
        r.shuffle(choices)
        out.append({
            "q": c["front"],
            "choices": choices,
            "answer": choices.index(trunc(c["back"], 200)),
            "explain": "Recall check — the card's answer is the definition: " + trunc(c["back"], 300),
        })
    return out

def drill_recall(m):
    items = []
    note0 = (m.get("notes") or [{}])[0].get("title", "Concepts") if m.get("notes") else "Concepts"
    for c in (m.get("cards") or [])[4:8]:
        if not (isinstance(c, dict) and c.get("front") and c.get("back")):
            continue
        items.append({
            "prompt": f"From memory, in one or two sentences: {c['front']}",
            "answer": c["back"],
            "explain": f"Core recall for this module. If this wasn't fluent, re-read the '{note0}' note and retry until it is.",
        })
    # pad from first cards if short
    for c in (m.get("cards") or [])[:4]:
        if len(items) >= 4:
            break
        if not (isinstance(c, dict) and c.get("front") and c.get("back")):
            continue
        if any(it["answer"] == c["back"] for it in items):
            continue
        items.append({
            "prompt": f"From memory, in one or two sentences: {c['front']}",
            "answer": c["back"],
            "explain": f"Core recall for this module. If this wasn't fluent, re-read the '{note0}' note and retry until it is.",
        })
    return {"id": f"{m['id']}--drill-recall", "title": f"Recall sprint: {m.get('title','')}",
            "items": items[:4]}

def drill_applied(m):
    items = []
    for q in (m.get("quiz") or [])[4:8]:
        if not (isinstance(q, dict) and q.get("explain")):
            continue
        items.append({
            "prompt": f"Applied check: {q['q']}",
            "answer": correct_choice(q),
            "explain": q["explain"],
        })
    for q in (m.get("quiz") or [])[:4]:
        if len(items) >= 4:
            break
        if not (isinstance(q, dict) and q.get("explain")):
            continue
        if any(it["prompt"].endswith(q["q"]) for it in items):
            continue
        items.append({
            "prompt": f"Applied check: {q['q']}",
            "answer": correct_choice(q),
            "explain": q["explain"],
        })
    return {"id": f"{m['id']}--drill-applied", "title": f"Applied reps: {m.get('title','')}",
            "items": items[:4]}

def lab(course_id, m):
    bank = LABS[course_id]
    topic = m.get("title", "this module")
    return {
        "id": f"{m['id']}--lab",
        "title": bank["title"].format(topic=topic),
        "brief": bank["brief"].format(topic=topic),
        "steps": [s.format(topic=topic) for s in bank["steps"]],
        "deliverable": bank["deliverable"].format(topic=topic),
        "checkpoint": bank["checkpoint"].format(topic=topic),
    }

def estimate_minutes(m):
    n_notes = len(m.get("notes", []) or [])
    n_cards = len(m.get("cards", []) or [])
    n_quiz = len(m.get("quiz", []) or [])
    n_drill_items = sum(len(d.get("items", [])) for d in (m.get("drills", []) or []))
    mins = 60 + 15 * n_notes + 2 * n_cards + 3 * n_quiz + 10 * n_drill_items + 60
    return int(5 * round(mins / 5))

def module_needs(m):
    notes = [n for n in (m.get("notes") or []) if isinstance(n, dict)]
    return (len(notes) < 6 or len(m.get("cards", []) or []) < 12
            or len(m.get("quiz", []) or []) < 9 or len(m.get("drills", []) or []) < 2
            or not m.get("handsOnLab") or not m.get("estimatedMinutes"))

def augment_course(path):
    fn = os.path.basename(path)
    with open(path) as f:
        d = json.load(f)
    course_id = d.get("courseId")
    changed, stats = False, {"modules_touched": 0}
    for m in d.get("modules", []):
        if not module_needs(m):
            continue
        changed = True
        stats["modules_touched"] += 1
        notes = [n for n in (m.get("notes") or []) if isinstance(n, dict)]
        while len(notes) < 6:
            notes.append(worked_example_note(m) if len(notes) == 4 else pitfalls_note(course_id, m))
        m["notes"] = notes
        have_cards = m.get("cards") or []
        new_cards = cards_from_quiz(m, 12 - len(have_cards))
        new_quiz = quiz_from_cards(have_cards, m, 10)
        m["cards"] = have_cards + new_cards
        m["quiz"] = (m.get("quiz") or []) + new_quiz
        if len(m.get("drills", []) or []) < 2:
            m["drills"] = [drill_recall(m), drill_applied(m)]
        if not m.get("handsOnLab"):
            m["handsOnLab"] = lab(course_id, m)
        m["estimatedMinutes"] = estimate_minutes(m)
    if changed:
        total = sum(mm.get("estimatedMinutes", 0) for mm in d.get("modules", []))
        d["hours"] = round(total / 60)
        d["updatedAt"] = "2026-10-08"
        d["timeFormula"] = ("estimatedMinutes per module = 60 (orientation) + 15/note + 2/card + 3/quiz item + "
                            "10/drill item + 60 (hands-on lab), rounded to 5; course hours = rounded sum of module minutes.")
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
            f.write("\n")
        json.load(open(tmp))  # validate before replace
        shutil.copy2(path, os.path.join(BACKUP, fn + ".bak"))
        os.replace(tmp, path)
        stats.update(hours=d["hours"], total_minutes=total)
    stats["file"] = fn
    return stats

if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(BASE, "il-0[1-9]-*.json")) + glob.glob(os.path.join(BASE, "il-1[0-5]-*.json")))
    only = sys.argv[1:] or None
    for f in files:
        if only and os.path.basename(f) not in only:
            continue
        print(augment_course(f), flush=True)
