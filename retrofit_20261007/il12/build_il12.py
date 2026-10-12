#!/usr/bin/env python3
"""IL-12 retrofit build script — applies prepared content to the course file.

Safety: fresh json.load immediately before edits; atomic write (temp + os.replace);
validates with json.load after writing; asserts template shape per module.
Sibling module aieng-agentic-ai--agent-autonomy-ceilings is PRESERVED — only
objectives_add / cards_add / quiz_add are applied to it.
"""
import json, os, sys, importlib.util

BASE = os.path.expanduser("~/workspace/apex-audit")
RETRO = os.path.join(BASE, "retrofit_20261007", "il12")
COURSE = os.path.join(BASE, "docs/university/data/courses/il-12-ai-engineering.json")
SIBLING_ID = "aieng-agentic-ai--agent-autonomy-ceilings"

def load_mod(name):
    path = os.path.join(RETRO, name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    # FRESH load immediately before edits (sibling-safe)
    with open(COURSE, encoding="utf-8") as f:
        course = json.load(f)

    content_files = ["c_python", "c_datascience", "c_ml", "c_dl", "c_genai1",
                     "c_genai2", "c_nlp", "c_agents", "c_azure", "c_prod1",
                     "c_prod2", "c_capstone"]
    content = {}
    for cf in content_files:
        content.update(load_mod(cf).CONTENT)

    cl = load_mod("c_courselevel")

    by_id = {m["id"]: m for m in course["modules"]}
    applied, skipped_sibling_notes = 0, 0

    for mid, c in content.items():
        if mid not in by_id:
            raise SystemExit(f"CONTENT module id not in course file: {mid}")
        m = by_id[mid]

        if mid == SIBLING_ID:
            # PRESERVE sibling: only additive top-ups
            if "objectives_add" in c:
                m["objectives"] = list(m.get("objectives", [])) + list(c["objectives_add"])
            if c.get("cards_add"):
                m["cards"] = list(m.get("cards", [])) + list(c["cards_add"])
            if c.get("quiz_add"):
                m["quiz"] = list(m.get("quiz", [])) + list(c["quiz_add"])
            skipped_sibling_notes += 1
            applied += 1
            continue

        # --- full retrofit (preserve id/code/title/weight; replace the rest) ---
        m["summary"] = c["summary"]
        m["objectives"] = list(c["objectives"])

        notes = [
            {"title": "Concepts",
             "body": c["concepts_intro"] + "\n" + "\n".join(c["concepts"])},
            {"title": "Hands-on procedure",
             "body": c["proc_intro"] + "\n" + "\n".join(
                 f"{i+1}. {s}" for i, s in enumerate(c["proc"]))},
            {"title": "Project brief", "body": c["project"]},
            {"title": "Honesty note", "body": c["honesty"]},
        ]
        if c.get("proc_code"):
            notes[1]["code"] = c["proc_code"]
            notes[1]["lang"] = c.get("proc_lang", "python")
        m["notes"] = notes

        if c.get("cards_add"):
            m["cards"] = list(m.get("cards", [])) + list(c["cards_add"])
        if c.get("quiz_add"):
            # preserve all existing quiz first, then fill with added up to 10
            existing_q = list(m.get("quiz", []))
            room = 10 - len(existing_q)
            if room < 0:
                raise SystemExit(f"{mid}: already has {len(existing_q)} quiz, cannot fit")
            m["quiz"] = existing_q + list(c["quiz_add"])[:room]
            if len(m["quiz"]) < 10:
                raise SystemExit(f"{mid}: quiz shortfall ({len(m['quiz'])}/10) — add content")
        applied += 1

    # --- course-level ---
    course["mockMinutes"] = 180
    existing_mock = {t["id"] for t in course.get("mockTasks", [])}
    for t in cl.MOCK_TASKS_ADD:
        if t["id"] not in existing_mock:
            course["mockTasks"].append(t)
    existing_cs = {c["title"] for c in course.get("cheatSheets", [])}
    for cs in cl.CHEATSHEETS_ADD:
        if cs["title"] not in existing_cs:
            course["cheatSheets"].append(cs)
    existing_ab = {a["q"] for a in course.get("answerBank", [])}
    for a in cl.ANSWERBANK_ADD:
        if a["q"] not in existing_ab:
            course["answerBank"].append(a)

    # --- assertions: template shape ---
    problems = []
    for m in course["modules"]:
        mid = m["id"]
        titles = [n.get("title") for n in m.get("notes", [])]
        if mid == SIBLING_ID:
            exp = ["Concepts", "Worked estimation", "Project brief", "Frontier honesty"]
        else:
            exp = ["Concepts", "Hands-on procedure", "Project brief", "Honesty note"]
        if titles != exp:
            problems.append(f"{mid}: note titles {titles}")
        if len(m.get("cards", [])) < 6:
            problems.append(f"{mid}: only {len(m.get('cards', []))} cards")
        if len(m.get("quiz", [])) != 10:
            problems.append(f"{mid}: {len(m.get('quiz', []))} quiz (want 10)")
        if len(m.get("objectives", [])) < 5:
            problems.append(f"{mid}: only {len(m.get('objectives', []))} objectives")
        if not (m.get("summary") or "").strip():
            problems.append(f"{mid}: empty summary")
        for qi, q in enumerate(m.get("quiz", [])):
            if len(q.get("choices", [])) != 4:
                problems.append(f"{mid} q{qi}: {len(q.get('choices', []))} choices")
            if not isinstance(q.get("answer"), int) or not (0 <= q["answer"] <= 3):
                problems.append(f"{mid} q{qi}: bad answer index {q.get('answer')}")
            if not (q.get("explain") or "").strip():
                problems.append(f"{mid} q{qi}: empty explain")
        for ci, card in enumerate(m.get("cards", [])):
            if not (card.get("front") or "").strip() or not (card.get("back") or "").strip():
                problems.append(f"{mid} card{ci}: empty front/back")
    # concept glossary bullet format check
    for m in course["modules"]:
        if m["id"] == SIBLING_ID:
            continue
        body = m["notes"][0]["body"]
        bullets = [ln for ln in body.split("\n") if ln.startswith("- **")]
        if len(bullets) < 6:
            problems.append(f"{m['id']}: only {len(bullets)} glossary bullets")
    # course-level checks
    if course.get("mockMinutes") != 180:
        problems.append("mockMinutes != 180")
    for key in ["arc", "priorities", "battlePlan", "mockTasks", "cheatSheets",
                "answerBank", "sourceLinks"]:
        if not course.get(key):
            problems.append(f"course-level {key} missing/empty")
    if course.get("honestyNote", "") == "":
        problems.append("honestyNote empty")

    if problems:
        print("ASSERTION FAILURES:")
        for p in problems:
            print("  -", p)
        sys.exit(1)

    # --- atomic write + re-validate ---
    tmp = COURSE + ".retrofit_tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(course, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(tmp, encoding="utf-8") as f:
        json.load(f)  # validate
    os.replace(tmp, COURSE)

    n_mods = len(course["modules"])
    print(f"OK: applied content to {applied}/{n_mods} modules "
          f"(sibling preserved: {skipped_sibling_notes})")
    print(f"course-level: mockMinutes=180, mockTasks={len(course['mockTasks'])}, "
          f"cheatSheets={len(course['cheatSheets'])}, answerBank={len(course['answerBank'])}")

if __name__ == "__main__":
    main()
