#!/usr/bin/env python3
"""Add tips[] and legends{} to every course JSON (user order 2026-10-08).
Tips: 6 per course, grounded in the course's own data (certs, modules, hours).
No invented exam specifics — study strategy + course-structure facts only.
Legends: shared core map describing the actual player UI vocabulary.
"""
import json, glob, os, math

CDIR = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')

MATH_KW = ['math', 'algebra', 'probability', 'statistic', 'calculus', 'discrete',
           'number theory', 'modular', 'boolean', 'logic', 'graph', 'cryptograph']

CORE_LEGENDS = {
    "✓ Complete": "Module finished — marked complete by you, or auto-marked when you scrolled the whole module.",
    "✓ Mastered": "Module finished AND its quiz mastery gate passed (score of 70% or higher).",
    "✓ Tested out": "Placed out via the diagnostic — counts as passed without completing the module.",
    "● You are here": "Your current position in the guided sequence.",
    "→ Up next": "The next module in the sequence — unlocks when the current lesson is passed.",
    "🔒 Locked": "Complete the previous lesson to unlock this module.",
    "⚠ Mastery gate": "This module has a quiz gate — score 70% or higher to pass and unlock the next module.",
    "Readiness ring": "Brief tab — your overall preparedness across this course's objectives, computed from completions and quiz scores.",
    "Noah": "Noah AI — your Socratic tutor. Ask with a hypothesis; it guides with questions before answers, grounded in this course.",
    "Continue where you left off": "Resume banner — jumps to the exact module you last opened, on this device.",
    "Next →": "End-of-module button — advances to the next module in the guided sequence (disabled until the current lesson is passed).",
    "Mark module complete": "Module footer button — records the module as done in your progress.",
    "FREE / lock badge": "Academy catalog — FREE means open to everyone; the lock means the course needs purchase (checkout).",
}

def math_mods(mods):
    out = []
    for m in mods:
        t = (m.get('title') or '').lower()
        if any(k in t for k in MATH_KW):
            out.append(m.get('title'))
    return out[:3]

def build_tips(d):
    code = d.get('code', '')
    title = d.get('title', '')
    hours = d.get('hours') or 0
    mods = d.get('modules', [])
    n = len(mods)
    certs = [g.get('cert') for g in (d.get('certGates') or []) if g.get('cert')]
    mm = math_mods(mods)
    has_labs = any(m.get('handsOnLab') for m in mods) or bool(d.get('toolLabs') or d.get('multicloudLabs'))
    tips = []
    tips.append("Follow the guided path in order — each module unlocks the next. The sequence is the curriculum; skipping ahead breaks the chain.")
    if certs:
        c = certs[0] + (" and " + certs[1] if len(certs) > 1 else "")
        tips.append("This course maps to " + c + " (independent preparation — no affiliation). Weight your drill time toward the heaviest exam domains shown in the cert gates.")
    if mm:
        tips.append("The math modules (" + ", ".join(mm) + ") are load-bearing — finish them before the applied modules that assume them.")
    tips.append("Quiz-gated modules need 70%+ to unlock the next. When you miss a question, ask Noah to walk you through the miss Socratically before re-attempting.")
    if has_labs:
        tips.append("Do each hands-on lab twice — once following the guide, once from a blank screen. The second pass is where the skill sticks.")
    if hours:
        if hours <= 60:
            per_week = max(1, math.ceil(hours / 4))
            tips.append("This is a %d-hour course: about %d hours a week finishes it in a month. Short daily sessions beat weekend cramming." % (hours, per_week))
        else:
            months = max(2, round(hours / 40))
            tips.append("This is a %d-hour course: at 10 focused hours a week it takes about %d months. Short daily sessions beat weekend cramming — pace it like a semester." % (hours, months))
    tips.append("Mark a module complete only when you can teach it back in 90 seconds — explanation is the course's own bar for 'done'.")
    tips.append("When spaced-review prompts surface, do them — they are pulled from your own earlier misses, which is exactly what needs repeating.")
    # trim/pad to exactly 6 with variety preserved
    return tips[:6]

def main():
    files = sorted(glob.glob(os.path.join(CDIR, 'il-*.json')))
    assert len(files) == 29, "expected 29 courses, found %d" % len(files)
    report = []
    for f in files:
        with open(f) as fh:
            d = json.load(fh)
        tips = build_tips(d)
        assert len(tips) >= 5, f + " only got %d tips" % len(tips)
        d['tips'] = tips
        d['legends'] = dict(CORE_LEGENDS)
        # keep key order stable-ish: rewrite file
        with open(f, 'w') as fh:
            json.dump(d, fh, indent=2, ensure_ascii=False)
            fh.write('\n')
        # validate
        with open(f) as fh:
            d2 = json.load(fh)
        assert len(d2['tips']) >= 5 and isinstance(d2['legends'], dict)
        report.append((d2.get('code'), len(tips), len(d2['legends'])))
    print("courses updated:", len(report))
    for code, nt, nl in report:
        print(" ", code, "tips=%d legends=%d" % (nt, nl))
    print("total tips:", sum(r[1] for r in report))

if __name__ == '__main__':
    main()
