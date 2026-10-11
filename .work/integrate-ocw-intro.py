#!/usr/bin/env python3
"""Integrate MIT OCW Introductory Programming collection into IL-03 (primary),
IL-08 and IL-20 (light touches). Original distillation, external links only.
Date: 2026-10-09"""
import json, copy, datetime

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses'
TODAY = '2026-10-09'

# Verified live URLs from MIT OCW (via search results, 2026-10-09)
OCW = {
    'collection': 'https://ocw.mit.edu/collections/introductory-programming/',
    '6001': 'https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/',
    '6002': 'https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/',
    '6100L': 'https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/',
    '6006': 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
    '6S095': 'https://ocw.mit.edu/courses/6-s095-programming-for-the-puzzled-january-iap-2018/',
    '6S096': 'https://ocw.mit.edu/courses/6-s096-introduction-to-c-and-c-january-iap-2013/',
    '6088': 'https://ocw.mit.edu/courses/6-088-introduction-to-c-memory-management-and-c-object-oriented-programming-january-iap-2010/',
    '6092': 'https://ocw.mit.edu/courses/6-092-introduction-to-programming-in-java-january-iap-2010/',
    'matlab': 'https://ocw.mit.edu/courses/res-18-002-introduction-to-matlab-spring-2008/',
    '18S191': 'https://ocw.mit.edu/courses/18-s191-introduction-to-computational-thinking-fall-2020/',
}

def load(name):
    with open(f'{BASE}/{name}') as f:
        return json.load(f)

def save(name, d):
    tmp = f'{BASE}/{name}.tmp'
    with open(tmp, 'w') as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write('\n')
    json.load(open(tmp))  # validate
    import os
    os.replace(tmp, f'{BASE}/{name}')

# ---------------------------------------------------------------- IL-03
il03 = load('il-03-programming-language-forge.json')

new_module = {
    "id": "il03-ocw-intro-programming",
    "code": "IL-03",
    "title": "MIT OCW Introductory Programming Collection — Distilled",
    "summary": (
        "MIT OpenCourseWare's Introductory Programming collection, distilled into an Interstitium Labs study path. "
        "Three lanes: (A) General introductions in Python — 6.0001, 6.0002, and the newer 6.100L — which take you from "
        "zero programming experience to computational thinking and data science; (B) Follow-up courses — 6.006 Introduction "
        "to Algorithms and 6.S095 Programming for the Puzzled — which build algorithmic maturity; (C) Language-specific "
        "introductions — Julia (18.S191), MATLAB, Java (6.092), and C/C++ (6.S096, 6.088) — short IAP-format courses that "
        "teach one language deeply. Every concept below is an original distillation; the linked OCW pages are external "
        "references (Creative Commons), never mirrored. Ask Noah to tutor any section — it knows this module."
    ),
    "estimatedMinutes": 240,
    "weight": 0.10,
    "objectives": [
        "Follow the 6.0001 → 6.0002 Python sequence: from basic syntax to computational problem-solving and data science.",
        "Build algorithmic maturity with 6.006 (algorithms) and 6.S095 (puzzle-driven programming).",
        "Add a second and third language via the IAP courses: Julia, MATLAB, Java, C/C++.",
        "Use each OCW course's lecture notes, videos, and problem sets as external practice material.",
    ],
    "notes": [
        {
            "heading": "Lane A — General introductions (Python)",
            "body": (
                "**6.0001 Introduction to Computer Science and Programming in Python** — MIT's standard starting point for "
                "students with little or no programming experience. Distilled core: what computation is and why it matters; "
                "Python syntax and semantics; branching and iteration; functions, decomposition, and abstraction; core data "
                "structures (strings, lists, tuples, dictionaries); simple numerical methods (bisection search, Newton-Raphson); "
                "a first taste of algorithmic complexity. Prerequisite: none — pre-calculus familiarity helps but is not required. "
                f"External: {OCW['6001']}"
            ),
        },
        {
            "heading": "6.0002 — Computational thinking and data science",
            "body": (
                "**6.0002 Introduction to Computational Thinking and Data Science** — the direct continuation of 6.0001. "
                "Distilled core: optimization problems and greedy algorithms; graphs and graph search; dynamic programming; "
                "stochastic thinking — random walks and Monte Carlo simulation; descriptive statistics and plotting data; "
                "a first look at machine learning (clustering, classification). The through-line: computation as a tool for "
                "answering questions about the world, not just writing code. Prerequisite: 6.0001 or equivalent. "
                f"External: {OCW['6002']}"
            ),
        },
        {
            "heading": "6.100L — the newer Python on-ramp",
            "body": (
                "**6.100L Introduction to CS and Programming using Python** — the current-generation successor to 6.0001, "
                "covering the same ground (Python fundamentals for beginners) in MIT's renumbered curriculum. If you prefer "
                "the newest materials, start here instead of 6.0001; the concept map is the same. "
                f"External: {OCW['6100L']}"
            ),
        },
        {
            "heading": "Lane B — Follow-up courses",
            "body": (
                "**6.006 Introduction to Algorithms** — the classic next step: algorithmic thinking, models of computation, "
                "sorting (insertion, merge, heap), hashing, trees (BST, AVL), graph algorithms (BFS, DFS, Dijkstra, Bellman-Ford), "
                "dynamic programming, and complexity analysis. This is the deep end — IL-08 covers this territory in full; "
                "treat 6.006 as the external companion. "
                f"External: {OCW['6006']} · Cross-link: IL-08 Algorithms, Compilers, Distributed & Formal."
            ),
        },
        {
            "heading": "6.S095 — Programming for the Puzzled",
            "body": (
                "**6.S095 Programming for the Puzzled** (IAP) — bridges recreational algorithmic puzzles and pragmatic programming. "
                "Distilled core: greedy strategies, search techniques, dynamic programming, and graph reasoning, each taught "
                "through a puzzle ('You Will All Conform', 'Keep Those Queens Apart', Sudoku, and more). Python syntax is explained "
                "as needed per puzzle — ideal second-course material after 6.0001. "
                f"External: {OCW['6S095']}"
            ),
        },
        {
            "heading": "Lane C — Language-specific IAP courses",
            "body": (
                "**Julia — 18.S191 Introduction to Computational Thinking.** Uses Julia to attack real-world problems: image analysis "
                "and convolutions, dynamic programming (seam carving), data structures and multiple dispatch, probability via "
                "computation, graphs-as-matrices, epidemic propagation, and climate modeling. Doubles as applied-math enrichment — "
                "see IL-20. "
                f"External: {OCW['18S191']}"
            ),
        },
        {
            "heading": "MATLAB — RES.18-002",
            "body": (
                "**Introduction to MATLAB** (IAP) — foundations of programming in MATLAB for students with no prior experience: "
                "variables, arrays, conditional statements, loops, functions, and plots. The gateway to numerical computing; "
                "a natural lead-in to Java, C++, or Python for scientific work. "
                f"External: {OCW['matlab']}"
            ),
        },
        {
            "heading": "Java — 6.092",
            "body": (
                "**6.092 Introduction to Programming in Java** (IAP) — software engineering through Java: language fundamentals, "
                "object-oriented design (classes, inheritance, polymorphism), and the discipline of building high-quality working "
                "software that solves real problems. One hour of lecture plus one hour of assisted lab per session. "
                f"External: {OCW['6092']}"
            ),
        },
        {
            "heading": "C and C++ — 6.S096 and 6.088",
            "body": (
                "**6.S096 Introduction to C and C++** (IAP) — fast-paced: the compilation pipeline; C memory management (pointers, "
                "manual allocation); data structures in C; debugging; then C++ classes, inheritance, templates, and the STL. "
                "**6.088 Introduction to C Memory Management and C++ Object-Oriented Programming** (IAP) — the 'empowerment' framing: "
                "why C (memory control, performance), why C++ (objects), deep C memory work, C++ classes and STL, plus interview tricks. "
                "Take 6.S096 first; 6.088 as reinforcement. "
                f"External: {OCW['6S096']} · {OCW['6088']}"
            ),
        },
        {
            "heading": "Study order (Noah's recommended path)",
            "body": (
                "1) 6.0001 (or 6.100L) → 2) 6.0002 → 3) pick ONE IAP language (Julia for math/science, Java for OOP/software roles, "
                "C/C++ for systems) → 4) 6.S095 puzzles for algorithmic fluency → 5) 6.006 alongside IL-08. "
                "Ask Noah: 'Quiz me on 6.0002 dynamic programming' or 'Explain 6.S096 pointers like I'm five, then like I'm an interviewer.'"
            ),
        },
        {
            "heading": "Honest framing",
            "body": (
                "These are MIT's materials under Creative Commons — we link and reference them; we do not copy them, mirror them, "
                "or claim any affiliation with MIT. The distillations above are original summaries written for this course. "
                "OCW problem sets assume MIT's term structure; pace yourself as a solo learner and use Noah to fill the gap "
                "that recitations would normally cover."
            ),
        },
    ],
    "cards": [
        {"front": "6.0001 → 6.0002 sequence covers what?", "back": "6.0001: Python basics, control flow, functions, data structures, simple numerical methods. 6.0002: optimization, graphs, dynamic programming, stochastic thinking, statistics, intro ML."},
        {"front": "What makes 6.S095 different from 6.006?", "back": "6.S095 teaches algorithms through recreational puzzles in Python (IAP, lighter); 6.006 is the full algorithms course (sorting, hashing, graphs, DP, complexity)."},
        {"front": "6.088's 'empowerment' framing in one line?", "back": "Why C (memory control/performance), why C++ (objects), and how to be useful in both — plus interview tricks."},
        {"front": "18.S191 teaches what, in what language?", "back": "Computational thinking in Julia: image analysis, convolutions, dynamic programming, probability, graphs-as-matrices, epidemic and climate modeling."},
        {"front": "Noah's recommended OCW study order?", "back": "6.0001 (or 6.100L) → 6.0002 → one IAP language (Julia/Java/C++) → 6.S095 puzzles → 6.006 alongside IL-08."},
        {"front": "What is the honest framing for OCW materials here?", "back": "MIT's CC-licensed materials: we link and reference, never copy/mirror, and claim no MIT affiliation. Distillations are original summaries."},
    ],
    "quiz": [
        {"q": "Which OCW course is the direct continuation of 6.0001?", "choices": ["6.006", "6.0002", "6.S096", "18.S191"], "answer": 1},
        {"q": "6.S095 teaches programming through what vehicle?", "choices": ["Video games", "Algorithmic puzzles", "Web apps", "Kernels"], "answer": 1},
        {"q": "Which language does 18.S191 use?", "choices": ["Python", "MATLAB", "Julia", "R"], "answer": 2},
        {"q": "6.S096 covers which two languages?", "choices": ["Java and Kotlin", "C and C++", "Go and Rust", "Python and Julia"], "answer": 1},
    ],
    "drills": [
        {"id": "il03-ocw-intro--drill-recall", "title": "Recall sprint: OCW Intro Programming collection", "items": [
            {"prompt": "From memory: name the three lanes of the OCW Introductory Programming collection.", "answer": "A) General introductions in Python (6.0001/6.0002/6.100L); B) Follow-ups (6.006, 6.S095); C) Language-specific IAP courses (Julia, MATLAB, Java, C/C++)."},
            {"prompt": "From memory: what does 6.0002 add on top of 6.0001?", "answer": "Optimization and greedy algorithms, graphs, dynamic programming, stochastic thinking (random walks, Monte Carlo), statistics, and intro machine learning."},
        ]},
    ],
    "videos": [
        {"title": "MIT OCW — Introductory Programming collection", "url": OCW['collection'], "source": "MIT OpenCourseWare (external link)", "blurb": "The full collection page: general Python introductions, follow-up courses, and language-specific IAP courses.", "order": 1, "watchBefore": "notes"},
        {"title": "6.0001 — Intro to CS and Programming in Python", "url": OCW['6001'], "source": "MIT OpenCourseWare (external link)", "blurb": "Lecture videos, notes, and problem sets for MIT's standard Python starting point.", "order": 2},
        {"title": "6.0002 — Intro to Computational Thinking and Data Science", "url": OCW['6002'], "source": "MIT OpenCourseWare (external link)", "blurb": "The continuation: computation for problem-solving and data science.", "order": 3},
        {"title": "6.S095 — Programming for the Puzzled", "url": OCW['6S095'], "source": "MIT OpenCourseWare (external link)", "blurb": "Algorithmic puzzles in Python — the fun bridge to serious programming.", "order": 4},
        {"title": "18.S191 — Intro to Computational Thinking (Julia)", "url": OCW['18S191'], "source": "MIT OpenCourseWare (external link)", "blurb": "Julia for real-world modeling: images, epidemics, climate.", "order": 5},
    ],
    "crossLinks": ["IL-08", "IL-02", "IL-20"],
    "prerequisiteFor": [],
    "handsOnLab": {
        "title": "OCW playlist build",
        "steps": [
            "Pick your lane-A course (6.0001 or 6.100L) and bookmark its OCW page.",
            "Do the first two problem sets; log what confused you.",
            "Ask Noah to explain each confusion two ways: intuitively, then formally.",
            "Choose one IAP language course and complete its first assignment.",
        ],
    },
    "mockTask": {"title": "Teach-back: one OCW concept", "brief": "Pick one distilled concept (e.g., Monte Carlo simulation from 6.0002) and explain it to Noah in your own words until Noah confirms the explanation is correct."},
    "pdfs": [],
}

# replace if re-run
il03['modules'] = [m for m in il03['modules'] if m.get('id') != 'il03-ocw-intro-programming']
# insert after the backbone module (index 2) for logical flow
il03['modules'].insert(3, new_module)

# sourceLinks additions
new_links = [
    {"name": "MIT OCW — Introductory Programming collection", "url": OCW['collection'],
     "note": "Curated OCW page: Python introductions, follow-up courses, and language-specific IAP courses. External reference (CC-licensed); we link, never mirror.", "retrieved": TODAY},
    {"name": "MIT 6.0001 — Intro to CS and Programming in Python", "url": OCW['6001'],
     "note": "MIT's standard Python starting point: computation, control flow, data structures.", "retrieved": TODAY},
    {"name": "MIT 6.0002 — Intro to Computational Thinking and Data Science", "url": OCW['6002'],
     "note": "Continuation of 6.0001: optimization, graphs, DP, stochastic thinking, intro ML.", "retrieved": TODAY},
    {"name": "MIT 6.S095 — Programming for the Puzzled", "url": OCW['6S095'],
     "note": "Algorithmic puzzles in Python — IAP bridge between recreation and practice.", "retrieved": TODAY},
    {"name": "MIT 18.S191 — Intro to Computational Thinking (Julia)", "url": OCW['18S191'],
     "note": "Julia for real-world modeling: images, probability, graphs, epidemics, climate.", "retrieved": TODAY},
    {"name": "MIT 6.S096 — Introduction to C and C++", "url": OCW['6S096'],
     "note": "IAP fast-paced C/C++: compilation, memory management, OOP, STL.", "retrieved": TODAY},
    {"name": "MIT 6.092 — Introduction to Programming in Java", "url": OCW['6092'],
     "note": "IAP Java: OOP fundamentals and software-engineering discipline.", "retrieved": TODAY},
    {"name": "MIT RES.18-002 — Introduction to MATLAB", "url": OCW['matlab'],
     "note": "IAP MATLAB foundations: variables, arrays, loops, functions, plots.", "retrieved": TODAY},
]
existing_urls = {s.get('url') for s in il03.get('sourceLinks', [])}
for link in new_links:
    if link['url'] not in existing_urls:
        il03.setdefault('sourceLinks', []).append(link)

# freshSignals entry
sig = {
    "id": "ocw-intro-programming-20261009",
    "date": TODAY,
    "title": "MIT OCW Introductory Programming collection folded in",
    "brief": "Distilled all 10 courses from MIT's Introductory Programming collection (6.0001, 6.0002, 6.100L, 6.006, 6.S095, Julia/18.S191, MATLAB, Java/6.092, C/C++/6.S096/6.088) into a new module with original concept summaries, flashcards, quizzes, and external links. Ask Noah to tutor any section.",
    "sources": [OCW['collection']],
    "courses": ["IL-03"],
}
il03.setdefault('freshSignals', [])
if not any(s.get('id') == sig['id'] for s in il03['freshSignals']):
    il03['freshSignals'].append(sig)

il03['updatedAt'] = TODAY
save('il-03-programming-language-forge.json', il03)
print('IL-03 updated: modules =', len(il03['modules']))

# ---------------------------------------------------------------- IL-08 (light touch)
il08 = load('il-08-algorithms-compilers-distributed-formal.json')
sig8 = {
    "id": "ocw-intro-collection-onramp-20261009",
    "date": TODAY,
    "title": "OCW Intro Programming collection: on-ramp to 6.006",
    "brief": "MIT's Introductory Programming collection (6.0001 → 6.0002 → 6.S095 puzzles) is the recommended on-ramp to 6.006-level algorithms covered in this course. Full distillation lives in IL-03's new OCW module; start there if your Python is rusty.",
    "sources": [OCW['collection']],
    "courses": ["IL-08", "IL-03"],
}
il08.setdefault('freshSignals', [])
if not any(s.get('id') == sig8['id'] for s in il08['freshSignals']):
    il08['freshSignals'].append(sig8)
il08['updatedAt'] = TODAY
save('il-08-algorithms-compilers-distributed-formal.json', il08)
print('IL-08 updated')

# ---------------------------------------------------------------- IL-20 (light touch)
il20 = load('il-20-mathematics.json')
sig20 = {
    "id": "ocw-18s191-julia-math-20261009",
    "date": TODAY,
    "title": "18.S191: computational thinking with Julia (math modeling)",
    "brief": "MIT's 18.S191 teaches probability via computation, graphs-as-matrices, and mathematical modeling (epidemics, climate) in Julia — strong applied-math enrichment for this course's probability and linear-algebra threads.",
    "sources": [OCW['18S191']],
    "courses": ["IL-20", "IL-03"],
}
il20.setdefault('freshSignals', [])
if not any(s.get('id') == sig20['id'] for s in il20['freshSignals']):
    il20['freshSignals'].append(sig20)
il20['updatedAt'] = TODAY
save('il-20-mathematics.json', il20)
print('IL-20 updated')
print('DONE')
