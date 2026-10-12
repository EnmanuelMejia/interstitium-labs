"""Shared helper for the IL-15 retrofit to the Multicloud (IL-19) course template."""
import json
import os

COURSE = os.path.expanduser(
    "~/workspace/apex-audit/docs/university/data/courses/il-15-data-engineering-analytics-interview-prep.json"
)

BANNED = ["aleks", "brilliant", "khan academy", "coursera", "udemy", "edx", "palantir"]


def load():
    with open(COURSE) as f:
        return json.load(f)


def save(course):
    tmp = COURSE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(course, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(tmp) as f:
        json.load(f)  # validate before replacing
    os.replace(tmp, COURSE)


def get_sources_body(mod):
    for n in mod.get("notes", []):
        if n.get("title") == "Sources":
            return n.get("body", "")
    return ""


def get_teach_body(mod):
    for n in mod.get("notes", []):
        if n.get("title") == "How Interstitium Labs teaches this":
            return n.get("body", "")
    return ""


def check_banned(text, where):
    low = text.lower()
    for b in BANNED:
        if b in low:
            raise ValueError("BANNED term %r found in %s" % (b, where))


def apply_module(course, mid, c):
    mod = next(m for m in course["modules"] if m["id"] == mid)
    teach = get_teach_body(mod)
    sources = get_sources_body(mod)

    mod["summary"] = c["summary"]

    concepts_body = c["concepts"].rstrip()
    if sources.strip():
        concepts_body += "\n\nSources for this module:\n" + sources.rstrip()

    proc_body = c["procedure_intro"].rstrip()
    if teach.strip():
        proc_body = teach.rstrip() + "\n\n" + proc_body
    steps = "\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(c["procedure_steps"]))
    proc_note = {
        "title": c.get("procedure_title", "Hands-on procedure"),
        "body": proc_body + "\n" + steps,
    }
    if c.get("procedure_code"):
        proc_note["code"] = c["procedure_code"]
        proc_note["lang"] = c.get("procedure_lang", "sql")

    mod["notes"] = [
        {"title": "Concepts", "body": concepts_body},
        proc_note,
        {"title": "Project brief", "body": c["project_brief"]},
        {"title": "Honesty note", "body": c["honesty"]},
    ]

    if len(mod["cards"]) != 5:
        raise ValueError("expected 5 cards in %s, got %d" % (mid, len(mod["cards"])))
    mod["cards"].append(c["new_card"])

    if len(mod["quiz"]) != 4:
        raise ValueError("expected 4 quiz in %s, got %d" % (mid, len(mod["quiz"])))
    ptr = c.get("explain_pointer", "Covered in this module's 'Concepts' note.")
    for q in mod["quiz"]:
        q["explain"] = q["explain"].rstrip() + " " + ptr
    for q in c["new_quiz"]:
        if len(q["choices"]) != 4:
            raise ValueError("quiz needs exactly 4 choices: %s" % q["q"][:60])
        if not (0 <= q["answer"] <= 3):
            raise ValueError("answer must be 0-based 0..3: %s" % q["q"][:60])
        if not q["explain"].strip():
            raise ValueError("explain must be non-empty: %s" % q["q"][:60])
    mod["quiz"].extend(c["new_quiz"])

    # banned-term sweep of everything this script wrote
    check_banned(mod["summary"], mid + " summary")
    for n in mod["notes"]:
        check_banned(n["body"], mid + " note " + n["title"])
    check_banned(c["new_card"]["front"] + " " + c["new_card"]["back"], mid + " card")
    for q in c["new_quiz"]:
        check_banned(q["q"] + " " + " ".join(q["choices"]) + " " + q["explain"], mid + " quiz")

    return mod


def apply_all(course, content):
    for mid, c in content.items():
        apply_module(course, mid, c)
    save(course)
    print("applied %d modules; file re-validated" % len(content))
