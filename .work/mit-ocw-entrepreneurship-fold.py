#!/usr/bin/env python3
"""Fold MIT OCW Entrepreneurship collection into IL-10 and IL-21 course JSONs.

Original distillations (own words, brief); external links only, never mirrored.
Independent-prep framing; Noah tutoring hooks included.
"""
import json
import os

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
IL10 = os.path.join(BASE, "il-10-portfolio-career-professional-practice.json")
IL21 = os.path.join(BASE, "il-21-humanities.json")

COLLECTION = {
    "name": "MIT OpenCourseWare — Entrepreneurship collection",
    "url": "https://ocw.mit.edu/collections/entrepreneurship/",
    "note": "MIT's full entrepreneurship course selection (core + supplemental), free under Creative Commons.",
    "retrieved": "2026-10-09",
}
COURSES = {
    "15.390": {
        "name": "MIT OCW 15.390 — New Enterprises (Bill Aulet et al., Spring 2013)",
        "url": "https://ocw.mit.edu/courses/15-390-new-enterprises-spring-2013/video_galleries/",
        "note": "Flagship intro to innovation-driven ventures: business-plan process, market analysis, technology viability, competitive positioning, team building, product life-cycle, marketing strategy, sales channels, founder-as-salesperson; aims at defining and dominating a new category.",
        "retrieved": "2026-10-09",
    },
    "15.393": {
        "name": "MIT OCW 15.393 — Nuts and Bolts of New Ventures (Joe Hadzima, Jan IAP 2025)",
        "url": "https://ocw.mit.edu/courses/15-393-nuts-and-bolts-of-new-ventures-january-iap-2025/",
        "note": "Execution fundamentals: finding your customer, business models, sales and pitching, hiring/inspiring/firing, legal pitfalls, negotiation, financial projections, raising capital. Thesis: startups die on execution basics, not idea quality.",
        "retrieved": "2026-10-09",
    },
    "15.392": {
        "name": "MIT OCW 15.392 — Scaling Entrepreneurial Ventures (Spring 2026)",
        "url": "https://ocw.mit.edu/courses/15-392-scaling-entrepreneurial-ventures-spring-2026/",
        "note": "Post-product-market-fit leadership: founder-to-CEO transition, org design for speed, boards and governance, durable go-to-market engines, strategy and category creation, scaleup fundraising (Series A vs B). Assumes 15.390's Disciplined Entrepreneurship framework.",
        "retrieved": "2026-10-09",
    },
    "15.835": {
        "name": "MIT OCW 15.835 — Entrepreneurial Marketing (Spring 2002)",
        "url": "http://ocw.mit.edu/courses/15-835-entrepreneurial-marketing-spring-2002/",
        "note": "Marketing with no budget: what/how am I selling and to whom; leveraging painfully limited resources; opportunity identification; competing against resourced incumbents. No universal playbook — teaches flexible thinking about marketing problems.",
        "retrieved": "2026-10-09",
    },
}

IL10_NOTE = {
    "title": "External resources — MIT OpenCourseWare: Entrepreneurship",
    "body": (
        "MIT OpenCourseWare publishes its entrepreneurship courses free under Creative Commons. "
        "These are external references — Interstitium Labs is not affiliated with MIT, confers no MIT credit, "
        "and this course's frameworks remain our own practice heuristics. The summaries below are our own words; the links are the originals.\n\n"
        "- **15.390 New Enterprises** — the flagship: how an innovation-driven venture gets formed. Core moves: "
        "the business-plan process as a discipline (not a document), market sizing from primary evidence, "
        "technology-viability assessment, competitive positioning, team formation, product life-cycle planning, "
        "go-to-market and sales-channel design, and the founder as the first salesperson. The bar: build a company "
        "that can define and dominate a new category, not just enter one. "
        "→ https://ocw.mit.edu/courses/15-390-new-enterprises-spring-2013/video_galleries/\n"
        "- **15.393 Nuts and Bolts of New Ventures** — the execution checklist: finding your customer before building, "
        "choosing a business model that matches the customer, sales fundamentals and pitching, hiring/inspiring/firing, "
        "the legal pitfalls that kill early companies, negotiating with cofounders, employees and partners, "
        "financial projections that survive contact with reality, and raising capital only when it is earned. "
        "Thesis: most startups die on execution basics, not idea quality. "
        "→ https://ocw.mit.edu/courses/15-393-nuts-and-bolts-of-new-ventures-january-iap-2025/\n"
        "- **15.392 Scaling Entrepreneurial Ventures** — what changes after product-market fit: the founder-to-CEO "
        "transition (building the company, not the product), organizational design for decision speed, boards and governance, "
        "constructing a durable go-to-market engine, strategy and category creation, and scaleup fundraising "
        "(how Series A and B actually differ). Read only after your unit economics clear the bar — scaling a broken unit is just faster dying. "
        "→ https://ocw.mit.edu/courses/15-392-scaling-entrepreneurial-ventures-spring-2026/\n"
        "- **15.835 Entrepreneurial Marketing** — marketing with no budget: two questions drive everything — what and how am I "
        "selling, and to whom; and how do I leverage painfully limited marketing resources. Covers opportunity identification, "
        "competing against resourced incumbents, and picking the marketing/sales tools that fit a startup's constraints. "
        "No universal playbook — flexible thinking about marketing problems. "
        "→ http://ocw.mit.edu/courses/15-835-entrepreneurial-marketing-spring-2002/\n"
        "- **The full collection** — MIT's entrepreneurship selection, core plus supplemental: "
        "https://ocw.mit.edu/collections/entrepreneurship/\n\n"
        "**How to use them here:** pair each with this module's drills. Watch 15.390's business-plan arc before writing "
        "your venture brief; run 15.393's customer-finding material before your problem interviews; apply 15.835 before "
        "your go-to-market plan; read 15.392 only after your unit economics clear the bar.\n\n"
        "**Noah tutoring hooks:** ask the Visionary to pressure-test your riskiest assumption against 15.390's framework; "
        "ask the Mentor to role-play the investor-pitch Q&A; ask the Trickster to argue why your venture is default-dead; "
        "ask the Engineer to audit your financial projections line by line."
    ),
}

IL21_NOTE = {
    "title": "External resources — MIT OpenCourseWare: ventures, markets, and scale",
    "body": (
        "Business and economics are applied humanities: the same questions — who decides, who benefits, who bears the risk — "
        "show up in markets and in moral philosophy. MIT OpenCourseWare publishes these entrepreneurship courses free under "
        "Creative Commons; Interstitium Labs is not affiliated with MIT and confers no MIT credit.\n\n"
        "- **15.390 New Enterprises** — market analysis and competitive positioning as applied industrial organization: "
        "sizing markets from evidence, assessing whether a technology can bear a business, and the ethics of defining a category "
        "rather than entering one. → https://ocw.mit.edu/courses/15-390-new-enterprises-spring-2013/video_galleries/\n"
        "- **15.835 Entrepreneurial Marketing** — applied demand theory: identifying who values what, pricing under uncertainty, "
        "and competing for attention with scarce resources. Pairs with this module's markets-and-costs material. "
        "→ http://ocw.mit.edu/courses/15-835-entrepreneurial-marketing-spring-2002/\n"
        "- **The full collection** — https://ocw.mit.edu/collections/entrepreneurship/\n\n"
        "**Noah tutoring hooks:** ask the Philosopher whether category creation is value creation or rent extraction; "
        "ask the Mentor to map a market you know onto a market structure; ask the Visionary how an incentive system "
        "you design today shapes behavior five years out."
    ),
}


def atomic_write(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    json.load(open(tmp, encoding="utf-8"))  # validate before replacing
    os.replace(tmp, path)


def add_source_links(course, new_links):
    links = course.setdefault("sourceLinks", [])
    existing = {l.get("url") for l in links}
    for link in new_links:
        if link["url"] not in existing:
            links.append(dict(link))
            existing.add(link["url"])


def main():
    with open(IL10, encoding="utf-8") as f:
        il10 = json.load(f)

    add_source_links(il10, [COLLECTION, COURSES["15.390"], COURSES["15.393"], COURSES["15.392"], COURSES["15.835"]])

    ent = next(m for m in il10["modules"] if m.get("id") == "il10-entrepreneurship")
    notes = ent.setdefault("notes", [])
    if not any(n.get("title") == IL10_NOTE["title"] for n in notes):
        notes.append(dict(IL10_NOTE))
    il10["updatedAt"] = "2026-10-09"
    atomic_write(IL10, il10)

    with open(IL21, encoding="utf-8") as f:
        il21 = json.load(f)

    add_source_links(il21, [COLLECTION, COURSES["15.390"], COURSES["15.835"]])

    econ = next(m for m in il21["modules"] if m.get("id") == "m21-economics-1")
    notes = econ.setdefault("notes", [])
    if not any(n.get("title") == IL21_NOTE["title"] for n in notes):
        notes.append(dict(IL21_NOTE))
    il21["updatedAt"] = "2026-10-09"
    atomic_write(IL21, il21)

    # final validation
    il10v = json.load(open(IL10, encoding="utf-8"))
    il21v = json.load(open(IL21, encoding="utf-8"))
    entv = next(m for m in il10v["modules"] if m.get("id") == "il10-entrepreneurship")
    econv = next(m for m in il21v["modules"] if m.get("id") == "m21-economics-1")
    print("IL-10 sourceLinks:", len(il10v["sourceLinks"]))
    print("IL-10 ent notes:", len(entv["notes"]), "| has OCW note:",
          any(n["title"] == IL10_NOTE["title"] for n in entv["notes"]))
    print("IL-21 sourceLinks:", len(il21v["sourceLinks"]))
    print("IL-21 econ notes:", len(econv["notes"]), "| has OCW note:",
          any(n["title"] == IL21_NOTE["title"] for n in econv["notes"]))
    print("OK")


if __name__ == "__main__":
    main()
