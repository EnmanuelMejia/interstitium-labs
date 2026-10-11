#!/usr/bin/env python3
"""Structural audit of IL-01..IL-15 against the HARD quality bar."""
import json, glob, os, sys

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")

BAR = dict(notes=6, cards=12, quiz=9, drills_min=2, drills_max=3)

def audit_module(m):
    g = []
    notes = m.get("notes", []) or []
    obj_notes = [n for n in notes if isinstance(n, dict)]
    bare = len(notes) - len(obj_notes)
    if len(obj_notes) < BAR["notes"]:
        g.append(f"notes: {len(obj_notes)} object notes (< {BAR['notes']})")
    if bare:
        g.append(f"notes: {bare} BARE STRING notes (must be objects)")
    # worked examples: at least one note with code, or worked-* phrasing in title/body
    we = sum(1 for n in obj_notes if n.get("code") or "worked" in (n.get("title","") + " " + n.get("body","")).lower())
    if we == 0:
        g.append("notes: no worked-example note (code or worked example)")
    cards = m.get("cards", []) or []
    if len(cards) < BAR["cards"]:
        g.append(f"cards: {len(cards)} (< {BAR['cards']})")
    quiz = m.get("quiz", []) or []
    if len(quiz) < BAR["quiz"]:
        g.append(f"quiz: {len(quiz)} (< {BAR['quiz']})")
    badq = [i for i,q in enumerate(quiz) if not (isinstance(q, dict) and "answer" in q and "explain" in q and q.get("explain") and "choices" in q and len(q.get("choices",[])) >= 3)]
    if badq:
        g.append(f"quiz: {len(badq)} questions missing answer/explain/choices: idx {badq[:8]}")
    drills = m.get("drills", []) or []
    if len(drills) < BAR["drills_min"] or len(drills) > BAR["drills_max"]:
        g.append(f"drills: {len(drills)} (need {BAR['drills_min']}-{BAR['drills_max']})")
    for d in drills:
        items = d.get("items", []) if isinstance(d, dict) else []
        if not items:
            g.append(f"drill '{d.get('id') if isinstance(d,dict) else d}': no items")
        else:
            for i, it in enumerate(items):
                if not (isinstance(it, dict) and "answer" in it and it.get("explain")):
                    g.append(f"drill '{d.get('id','?')}' item {i}: missing answer/explain")
                    break
    if not m.get("handsOnLab"):
        g.append("no handsOnLab")
    else:
        lab = m["handsOnLab"]
        if not (lab.get("steps") and lab.get("deliverable") and lab.get("checkpoint")):
            g.append("handsOnLab missing steps/deliverable/checkpoint")
    if not m.get("estimatedMinutes"):
        g.append("no estimatedMinutes")
    vids = m.get("videos", []) or []
    badv = [v.get("url") for v in vids if isinstance(v, dict) and not v.get("url")]
    if badv:
        g.append(f"videos: {len(badv)} entries missing url")
    return g, dict(notes=len(obj_notes), bare=bare, cards=len(cards), quiz=len(quiz),
                   drills=len(drills), lab=bool(m.get("handsOnLab")), mins=m.get("estimatedMinutes"),
                   vids=len(vids))

def audit_course(path):
    d = json.load(open(path))
    mods = d.get("modules", [])
    mods_with_gaps = 0
    totals = dict(notes=0, bare=0, cards=0, quiz=0, drills=0, labs=0, mins=0)
    per = []
    for m in mods:
        g, c = audit_module(m)
        totals["notes"] += c["notes"]; totals["bare"] += c["bare"]; totals["cards"] += c["cards"]
        totals["quiz"] += c["quiz"]; totals["drills"] += c["drills"]; totals["labs"] += c["lab"]
        totals["mins"] += c["mins"] or 0
        if g:
            mods_with_gaps += 1
        per.append((m.get("code") or m.get("id"), g, c))
    declared = d.get("hours")
    summed_h = totals["mins"] / 60
    hour_gap = abs((declared or 0) - summed_h)
    # supplemental resource URLs
    urls = []
    for m in mods:
        for v in (m.get("videos") or []):
            if isinstance(v, dict) and v.get("url"):
                urls.append((m.get("code") or m.get("id"), v.get("url")))
    for sl in (d.get("sourceLinks") or []):
        if sl.get("url"):
            urls.append(("sourceLinks", sl["url"]))
    for jm in (d.get("jdMatrix") or []):
        if jm.get("postingUrl"):
            urls.append(("jdMatrix", jm["postingUrl"]))
    if d.get("dossierUrl"):
        urls.append(("dossier", d["dossierUrl"]))
    return dict(code=d.get("code"), title=d.get("title"), modules=len(mods),
                mods_with_gaps=mods_with_gaps, totals=totals, declared=declared,
                summed=round(summed_h,1), hour_gap=round(hour_gap,2), url_count=len(urls),
                urls=urls, per=per, top_keys=list(d.keys()))

files = sorted(glob.glob(os.path.join(BASE, "il-0[1-9]-*.json")) + glob.glob(os.path.join(BASE, "il-1[0-5]-*.json")))
res = {}
for f in files:
    try:
        res[os.path.basename(f)] = audit_course(f)
    except Exception as e:
        res[os.path.basename(f)] = {"ERROR": repr(e)}

out = []
for fn, r in res.items():
    if "ERROR" in r:
        out.append(f"### {fn}: ERROR {r['ERROR']}")
        continue
    t = r["totals"]
    out.append(f"### {fn} ({r['code']})")
    out.append(f"  modules={r['modules']} gaps_in={r['mods_with_gaps']} | notes={t['notes']} (bare={t['bare']}) cards={t['cards']} quiz={t['quiz']} drills={t['drills']} labs={t['labs']} | hours declared={r['declared']} summed={r['summed']} gap={r['hour_gap']} | urls={r['url_count']}")
    for code, g, c in r["per"]:
        if g:
            out.append(f"    - {code}: " + "; ".join(g))
print("\n".join(out))
json.dump({k: ({kk: vv for kk, vv in v.items() if kk not in ("per","urls")} if "ERROR" not in v else v) for k, v in res.items()},
          open("/tmp/audit-summary.json","w"), indent=1)
json.dump({k: (v.get("urls") if "ERROR" not in v else None) for k, v in res.items()},
          open("/tmp/audit-urls.json","w"), indent=1)
print("\nwrote /tmp/audit-summary.json and /tmp/audit-urls.json")
