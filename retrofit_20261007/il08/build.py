#!/usr/bin/env python3
"""IL-08 retrofit to the Multicloud course template (IL-19 shape).

Reads docs/university/data/courses/il-08-algorithms-compilers-distributed-formal.json,
restructures each module into the template shape:
  summary -> instructor voice
  notes   -> Concepts / Hands-on procedure|Worked estimation / Project brief / Noah check-in
  quiz    -> expanded 6 -> 10 (template depth)
  weight  -> added
All existing factual content is preserved (reorganized, never deleted).
Course-level keys already exist and are kept consistent.
Writes minified single-line JSON + trailing newline, matching the file's current style.
Validates with json.load before AND after writing.
"""
import json, os, sys, copy

BASE = os.path.expanduser("~/workspace/apex-audit")
PATH = os.path.join(BASE, "docs/university/data/courses/il-08-algorithms-compilers-distributed-formal.json")

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def noah_checkin(questions):
    body = "Noah probes mastery with questions like:\n" + "\n".join("- " + q for q in questions)
    body += ("\n- Honesty note: these proofs, labs, and questions are original practice material "
             "authored for this course. Course numbers reference public university materials; "
             "this course confers no certificate and is not affiliated with MIT, CMU, or Stanford.")
    return {"title": "Noah check-in", "body": body}

# ---------------------------------------------------------------- module 1
m1_summary = (
    "Welcome to IL-08 — Algorithms, Compilers, Distributed & Formal — and to Module 1: "
    "MIT's EECS curriculum, distilled to prerequisite order. I'm your instructor, and over the "
    "next three modules we're going to build the deep core that never expires: proofs, "
    "algorithms, the machine, and the limits of computation. In this module we follow MIT 6-3's "
    "own sequence — 6.100A/B Python (computational thinking and problem-set discipline), 6.1200 "
    "Mathematics for Computer Science (proofs, induction, number theory, graphs, probability), "
    "6.1210/6.1220 Algorithms (design, analysis, lower bounds, NP-completeness), 6.1910 "
    "Computation Structures (gates to processor, the hardware/software contract), 6.1800/6.1810 "
    "Systems Engineering (modularity, the end-to-end argument, the xv6 kernel), and theory from "
    "automata to complexity (the 6.1400 lineage). No algorithm in this module without an "
    "induction proof of it; no system without a machine model beneath it. Let's begin with the "
    "mathematician's toolkit."
)

m1_concepts = """- **induction** — proof by base case, inductive hypothesis, and inductive step; every recursive algorithm's correctness proof uses it — the template until it's reflex
- **loop invariant** — a property true before and after each iteration; the loop invariant proves the loop — state it before writing the loop
- **contradiction** — assume the negation of the claim, derive an absurdity; the halting proof's weapon
- **number theory** — divisibility, modular arithmetic, gcd; Fermat's little theorem and Euler's theorem — RSA's prerequisites, straight from 6.1200
- **graph theory** — the universal modeling language: vertices, edges, BFS/DFS, Dijkstra, MST
- **divide-and-conquer** — split, solve recursively, combine; analyzed via recurrences like T(n) = aT(n/b) + f(n)
- **master theorem** — closed form for T(n) = aT(n/b) + f(n): compare f(n) against n^(log_b a) — smaller gives case 1, equal gives case 2 (times log n), larger (regularity) gives case 3; memorize the three cases, derive when unsure
- **amortized analysis** — cost averaged over a sequence of operations; three methods: aggregate, accounting, potential — dynamic-array append is O(1) amortized via doubling
- **exchange argument** — the proof pattern for greedy correctness: show an optimal solution can be transformed to include the greedy choice — greedy stays ahead (MST, scheduling)
- **lower bound** — a proof that no algorithm in a model can do better; comparison sorting is Ω(n log n) by the decision-tree argument: n! leaves need log(n!) depth
- **reduction** — to prove X hard, reduce a known-hard problem TO X in polynomial time; reduction direction matters (3-SAT ≤p X proves X hard)
- **NP-completeness** — the hardest problems in NP; 3-SAT is the canonical one — reductions start here
- **FSM** — finite-state machine: combinational logic plus state; the building block of the FSM-to-processor climb — every level is the previous level's abstraction, no magic
- **hardware/software contract** — the ISA, assembly, and calling conventions: the exact boundary the hardware promises the software
- **end-to-end argument** — implement correctness-critical functions at the endpoints, not in the network; the network can't guarantee what endpoints need
- **xv6** — MIT's teaching Unix-like kernel in ~10k lines; reading a real kernel demystifies scheduling, virtual memory, and filesystems
- **diagonalization** — self-referential construction used to prove the halting problem undecidable; the most beautiful proof in CS — learn it cold
- **P vs NP** — P: solvable in polynomial time; NP: verifiable in polynomial time; NP-complete problems are the hardest in NP; PSPACE sits beyond"""

m1_procedure = """Prove and analyze an algorithm, end to end — the procedure behind the Induction Proof Workshop and the recurrence drills:
1. **State the claim precisely** — the specification: what must hold, for which inputs (e.g., sum_{i=1..n}(2i-1) = n^2).
2. **Write the loop invariant before the loop** — a property true before and after each iteration (binary search: the key, if present, lies in a[lo..hi)).
3. **Induction skeleton: BASE → HYPOTHESIS → STEP** — prove the base case, assume the hypothesis for k, derive k+1 (Bernoulli step: (1+x)^(k+1) = (1+x)^k(1+x) ≥ (1+kx)(1+x) = 1+(k+1)x+kx² ≥ 1+(k+1)x).
4. **Preserve the invariant each iteration** — binary search halves [lo,hi): if key < a[mid] set hi=mid, else lo=mid+1; the key stays inside; hi−lo shrinks, so the loop terminates.
5. **Write the recurrence** — count the work per level (mergesort: T(n) = 2T(n/2) + n).
6. **Apply the master theorem** — T(n) = 2T(n/2) + n is case 2: f(n) = n = n^(log_2 2), so Θ(n log n).
7. **Check amortized cost where operations repeat** — dynamic-array append with doubling: n appends cost O(n) total, O(1) amortized each.
8. **Argue the lower bound** — is your bound tight? Comparison sorting cannot beat Ω(n log n).
9. **Classify the problem** — in P, or NP-complete? If the latter (reduce 3-SAT to it, show membership in NP), stop hunting for the perfect algorithm and start approximating."""

m1_project = """Your algorithm dossier — the capstone for the MIT distilled core. Pick one algorithm from the canon: quicksort, Dijkstra's shortest path, or the dynamic-array append.
The dossier has four artifacts, and each is graded:
1. **Implementation** — correct Python code (BFS-style clarity: the code from the BFS lab is the bar).
2. **Correctness proof** — written in the BASE/HYPOTHESIS/STEP skeleton with the loop invariant stated up front, exactly like the Induction Proof Workshop.
3. **Running-time analysis** — the recurrence plus its master-theorem solution (or amortized argument for the dynamic array), with a tightness verdict from the lower-bound side.
4. **Complexity verdict** — one paragraph: where does this algorithm's problem sit in the complexity landscape (P? NP-complete? undecidable-adjacent?), and what changes if the input grows 100×?
These four artifacts — code, proof, analysis, verdict — are what a theory-literate engineer produces for any algorithm they ship."""

m1_noah = noah_checkin([
    "In one sentence, what does the master theorem decide for a recurrence — and which case is mergesort?",
    "State the binary-search loop invariant, then prove it is preserved when you set hi = mid.",
    "You claim problem X is NP-complete. Reduce 3-SAT to X — and defend why the reduction goes in that direction.",
    "Walk me through diagonalization: why can't a halting decider exist?",
    "The end-to-end argument says reliable delivery belongs at the endpoints. Give me one more endpoint-vs-network example from real systems.",
])

m1_quiz_new = [
    {"q": "Which 6.1200 topic is RSA's prerequisite?",
     "choices": ["graph theory", "number theory (divisibility, modular arithmetic, gcd)", "probability", "induction"],
     "answer": 1,
     "explain": "Number theory: Fermat's little theorem and Euler's theorem are the crypto foundations — the Concepts glossary lists them as RSA's prerequisites."},
    {"q": "Exchange arguments prove which algorithm family correct?",
     "choices": ["divide-and-conquer", "greedy algorithms", "dynamic programming", "randomized algorithms"],
     "answer": 1,
     "explain": "Exchange argument: greedy stays ahead — the proof pattern for MST and scheduling in the algorithms notes."},
    {"q": "How big is xv6?",
     "choices": ["~1M lines", "~100k lines", "~10k lines", "~1k lines"],
     "answer": 2,
     "explain": "A real Unix-like kernel in ~10k lines — every OS concept (scheduling, VM, filesystems) made concrete."},
    {"q": "The diagonalization proof shows?",
     "choices": ["P = NP", "the halting problem is undecidable", "sorting needs Ω(n log n)", "3-SAT is in P"],
     "answer": 1,
     "explain": "Assume a halting decider, construct the self-contradicting program — the Concepts glossary's most beautiful proof in CS."},
]

# ---------------------------------------------------------------- module 2
m2_summary = (
    "Welcome to Module 2 — Carnegie Mellon's systems-and-theory spine. I'm your instructor, and "
    "this is where correctness becomes a habit and the machine stops being a mystery. We start "
    "with 15-122 imperative computation and 15-150 functional programming — contracts, "
    "invariants, and purity as daily discipline — then climb 15-210's parallel and sequential "
    "data structures (the work/span cost model), the legendary 15-213 computer systems course "
    "with its malloc and shell labs, the theory pair 15-251/15-451 where proofs always ship with "
    "code, and the systems depth trio: 15-445 databases, 15-440 distributed systems, and 15-410 "
    "where you build a working kernel. We close with 07-280's AI breadth — the rebuild-the-landmarks "
    "pedagogy of implementing AlexNet, GPT-2, and AlphaZero yourself. By the end you'll be able "
    "to say exactly why your allocator fragments, why your replicas disagree, and how to fix both."
)

m2_concepts = """- **contract** — pre- and post-conditions: the function's promise; callers rely on it, implementations honor it — write the contract before the code
- **loop invariant** — the imperative twin of the contract: true before and after each iteration; 15-122's correctness discipline
- **purity** — no side effects; pure functions evaluate in any order — no shared mutable state means safe parallel evaluation by construction, the 15-150 bridge to 15-210
- **work** — total number of operations in a parallel algorithm
- **span** — the longest dependency chain; parallelism ≈ work/span; Brent's bound: Tp ≤ W/P + S
- **malloc lab** — write a real allocator: explicit free lists, first-fit search, splitting, coalescing — memory management demystified forever
- **coalescing** — merging adjacent free blocks; the allocator's defense against fragmentation
- **fragmentation** — free memory rendered unusable because it is split into small pieces; fragmentation is the enemy
- **shell lab** — job control in C: processes, signals, reaping; the 15-213 systems rite of passage
- **15-213's thesis** — programmers who understand the machine write better programs — in any language
- **consensus** — agreement despite failures; the distributed systems atom (Paxos/Raft)
- **Raft safety** — committed log entries are never lost; agreement on log order despite minority failures; liveness needs a majority
- **CRDT** — conflict-free replicated data type; works when operations commute — counters are the canonical case: increments commute and merge is idempotent
- **B+tree** — the database index: fanout^levels ≈ capacity; fanout 100 at 3 levels holds ~1M keys — the arithmetic behind index depth
- **buffer pool** — the database's page cache between disk and execution; 15-445 builds one, plus B+trees and query execution — building a database teaches more than using ten
- **15-410's deliverable** — a working kernel: threads, virtual memory, syscalls — the deepest programming most will ever do
- **rebuild-the-landmarks pedagogy** — implement AlexNet, GPT-2, AlphaZero yourself; landmarks become understanding"""

m2_estimation = """Worked estimates — the 15-210 habit of putting numbers on parallel and storage claims before believing them:
1. **Parallelism from work and span** — parallel sum of n elements: work O(n), span O(log n). Parallelism ≈ work/span = n/log n. On 64 cores, expect speedup bounded by min(64, n/log n) — Brent's bound Tp ≤ W/P + S.
2. **B+tree capacity** — fanout 100, 3 levels: 100³ = 1,000,000 keys. Add a fourth level: 100⁴ = 100M. This is the arithmetic behind index depth — shallow trees, fast lookups.
3. **Allocator fragmentation audit** — free_list holds [(0,16),(32,16)] with a live block at (16,16): coalescing only merges ADJACENT blocks, so the two 16-byte holes cannot merge across the live block. External fragmentation quantified: 32 bytes free, largest usable block 16.
4. **Raft quorum math** — 5 nodes: majority = 3. The cluster survives 2 failures and still commits; lose a third and liveness stops (safety still holds — committed entries are never lost).
5. **CRDT counter merge** — three replicas count [5, 3, 2] during a partition: merge takes the element-wise maximum per replica, total = 10, exact, with zero coordination. No consensus needed because increments commute."""

m2_project = """The distributed counter — the capstone for the CMU spine. Build a crash-tolerant impression counter across three replica processes:
1. **CRDT implementation** — a G-Counter with merge that is commutative and idempotent; demonstrate convergence after a simulated network partition with divergent counts.
2. **Raft-flavored alternative** — every increment goes through an elected leader with a replicated log; simulate the same partition and measure the latency and availability cost (what happens to increments when the leader is cut off?).
3. **Design memo** — one page: when do you pay for consensus, and when does the CRDT suffice? Argue from failure modes, not vibes — the 15-440 habit.
Deliverables: two implementations, a partition test log showing the divergent/converged counts, and the memo. Bonus: reimplement the mini-allocator from the script lab in C, with coalescing, and report the fragmentation audit from the estimation section against it."""

m2_noah = noah_checkin([
    "Parallel sum: work O(n), span O(log n). What's the parallelism — and what does Brent's bound say on 16 cores?",
    "Your free_list is [(0,16),(48,16)] with live blocks between. Can the holes coalesce? Why not?",
    "A partition splits your three replicas 2-vs-1. Your CRDT counter keeps counting; your Raft counter stalls on the minority side. Defend both behaviors.",
    "State 15-213's thesis in one sentence — then give me one bug it would have prevented in your own code.",
    "15-410 asks for a working kernel. Name the three subsystems you'd build first and why.",
])

m2_quiz_new = [
    {"q": "15-213's two famous labs are?",
     "choices": ["malloc lab + shell lab", "lexer + parser", "web server + proxy", "cache + VM simulator"],
     "answer": 0,
     "explain": "The malloc lab (write a real allocator) and the shell lab (job control) — the course's rites of passage in the 15-210/213 notes."},
    {"q": "A function's contract is?",
     "choices": ["its type signature", "pre/post-conditions — the function's promise", "its test file", "its docstring"],
     "answer": 1,
     "explain": "Contracts: callers rely on them, implementations honor them — write the contract before the code, per the 15-122 notes."},
    {"q": "Which CMU course has you build a working kernel?",
     "choices": ["15-213", "15-445", "15-410", "15-210"],
     "answer": 2,
     "explain": "15-410: a working kernel — threads, VM, syscalls — the capstone of systems education."},
    {"q": "15-445's project is to?",
     "choices": ["use ten databases", "build a real database — buffer pool, B+trees, query execution", "write SQL queries", "tune indexes"],
     "answer": 1,
     "explain": "Building a database teaches more than using ten — storage to execution, per the theory/depth/breadth notes."},
]

# ---------------------------------------------------------------- module 3
m3_summary = (
    "Welcome to Module 3 — Stanford's core as a cross-walk. I'm your instructor, and this module "
    "is about triangulation: we walk the same ground the MIT and CMU modules covered, but in "
    "Stanford's order, so that what survives all three presentations is the concept itself. "
    "106A's methodology in Python, 106B's abstractions in C++ with recursion as the core skill, "
    "CS103's proofs, logic, and graphs, CS109's probability for computer scientists, CS107's "
    "computer organization and systems (where pointers stop being scary), CS111's operating "
    "systems principles, and CS161's famously rigorous design and analysis — with randomization "
    "as the signature move. We close with the depth branches: theory (154/254), systems "
    "(143 compilers, 144 networking, 145 databases), and the AI sequence. Same ideas, third "
    "telling — keep what's invariant."
)

m3_concepts = """- **recursion-first** — think recursively, then convert to iterative; 106B's core problem-solving strategy — recursive problem-solving before iterative
- **big-O** — asymptotic upper bound on growth; 106B's language for comparing algorithms
- **expectation** — the average over randomness; a fair die expects 3.5 — linearity of expectation starts here
- **linearity of expectation** — E[X+Y] = E[X] + E[Y] with no independence needed; the analysis workhorse for randomized algorithms
- **randomized algorithm** — uses random choices; randomized quicksort runs in expected O(n log n) — randomization defeats adversarial input
- **amplification** — repeat a randomized algorithm; failure probability drops exponentially — Karger repeated n² log n times yields the min cut with high probability
- **Karger's min-cut** — randomized edge contraction; the algorithm that's wrong sometimes and brilliant in expectation — repeat for confidence
- **compilation pipeline** — lex → parse → semantic analysis → IR → optimization → codegen: tokens to tree to checked IR to machine code
- **RAII** — resource acquisition is initialization; 106B's C++ idiom for managing lifetimes — the language where abstractions cost nothing
- **buffer overflow** — writing past a buffer's bounds; CS107's assignments make memory unsafety visceral — security from the machine up
- **CS109's probability** — expectation, variance, concentration: the subset of probability a computer scientist actually uses (randomized algorithms, ML)
- **cross-walk value** — see the same ideas (recursion, induction, layering) across MIT, CMU, and Stanford; triangulation — the idea outlives any single presentation
- **depth branch** — a specialization track: theory (154 automata/complexity, 254 advanced), systems (143 compilers, 144 networking, 145 databases), AI (221, 229, 230, 224N, 231N, 234 — the sequence IL-07's ML arc follows)"""

m3_estimation = """Worked estimates — CS109-style: put numbers on randomized claims before shipping them:
1. **Expected quicksort** — n = 1,000,000, random pivot: expected ≈ n log₂ n ≈ 20M comparisons. Worst case without randomization: ≈ n²/2 = 5×10¹¹. Randomization's payoff, quantified — this is why the pivot is random.
2. **Amplification arithmetic** — one Karger run succeeds with probability ≈ 2/n². Repeat n² log n times: failure ≈ (1 − 2/n²)^(n² log n) ≈ e^(−2 log n) = 1/n². Repetition drives the error down exponentially — high probability from a weak primitive.
3. **Linearity of expectation** — expected sum of 100 fair dice = 100 × 3.5 = 350. No distribution math, no independence assumptions — linearity always holds.
4. **Hashing load estimate** — n keys into m = n buckets, uniform hashing: expected chain length = n/m = 1. Double the keys (n = 2m): expected length 2. This is the estimate behind every hash-table sizing decision."""

m3_project = """Randomization, proven and shipped — the capstone for the Stanford cross-walk. Implement randomized quicksort and Karger's min-cut in Python:
1. **Working code** — both algorithms, clean enough to hand to a reviewer.
2. **Expectation analysis** — written in prose, no hand-waving: show the linearity-of-expectation step for quicksort's O(n log n) and the 2/n² success bound for Karger.
3. **Empirical check** — run quicksort on adversarial (sorted) input 50 times, record the comparison counts, and report the distribution (min/median/max); then run Karger's min-cut repeatedly on a small graph and record how many runs find the true min cut — does the amplification arithmetic from the estimation section match?
4. **Production verdict** — one paragraph: when would you reach for randomization in production, and when is determinism non-negotiable?
Deliverables: code, analysis, measurements, verdict. Then write the compiler-phase map for a language you know: which phase would catch a type error, which would catch a syntax error, and where does optimization live — the 143 pipeline made concrete."""

m3_noah = noah_checkin([
    "Randomized quicksort on sorted input: expected time, and why does the random pivot defeat the adversary?",
    "Karger succeeds with probability ≈ 2/n² per run. How many repeats for high probability — and show the amplification arithmetic.",
    "Walk the compiler pipeline for `x = 1 +` — which phase rejects it, and why not an earlier one?",
    "Expected sum of 100 fair dice — no calculator, just linearity. Then tell me why independence wasn't needed.",
    "You've now seen induction at MIT, CMU, and Stanford. What's invariant across all three — and what did each school add?",
])

m3_quiz_new = [
    {"q": "106A teaches which language?",
     "choices": ["C++", "Python", "Java", "C"],
     "answer": 1,
     "explain": "106A (Methodology): Python — decomposition, testing, programming as a craft."},
    {"q": "106B's language and core skill?",
     "choices": ["Java + OOP", "C++ + recursive problem-solving", "Python + scripting", "Rust + ownership"],
     "answer": 1,
     "explain": "106B (Abstractions): C++ with recursion as the core skill — the language where abstractions cost nothing."},
    {"q": "CS109 is probability for?",
     "choices": ["mathematicians", "computer scientists", "statisticians", "physicists"],
     "answer": 1,
     "explain": "CS109: probability for computer scientists — the subset you'll actually use (randomized algorithms, ML)."},
    {"q": "Which depth course is compilers?",
     "choices": ["CS154", "CS143", "CS144", "CS145"],
     "answer": 1,
     "explain": "143 (compilers): the dragon course — lexing to codegen, the full pipeline, per the depth-branches notes."},
]

def quiz_ok(q):
    assert isinstance(q.get("q"), str) and q["q"].strip(), "empty quiz q"
    assert isinstance(q.get("choices"), list) and len(q["choices"]) == 4, "quiz must have exactly 4 choices"
    assert all(isinstance(c, str) and c.strip() for c in q["choices"]), "empty choice"
    assert isinstance(q.get("answer"), int) and 0 <= q["answer"] <= 3, "answer must be 0-based index"
    assert isinstance(q.get("explain"), str) and q["explain"].strip(), "empty explain"

def glossary_ok(body):
    bullets = [l for l in body.splitlines() if l.startswith("- **")]
    assert bullets, "Concepts section needs glossary bullets"
    for l in bullets:
        assert " — " in l, f"glossary bullet missing em-dash definition: {l[:60]}"

def main():
    d = load(PATH)
    assert d["courseId"] == "il-08-algorithms-compilers-distributed-formal"
    mods = {m["id"]: m for m in d["modules"]}
    assert set(mods) == {"il08-mit-63", "il08-cmu-cs", "il08-stanford-cs"}, "unexpected modules"

    plan = {
        "il08-mit-63":       (m1_summary, m1_concepts, ("Hands-on procedure", m1_procedure), m1_project, m1_noah, m1_quiz_new, 3),
        "il08-cmu-cs":       (m2_summary, m2_concepts, ("Worked estimation", m2_estimation), m2_project, m2_noah, m2_quiz_new, 2),
        "il08-stanford-cs":  (m3_summary, m3_concepts, ("Worked estimation", m3_estimation), m3_project, m3_noah, m3_quiz_new, 2),
    }

    for mid, (summary, concepts, (mid_title, mid_body), project, noah, quiz_new, weight) in plan.items():
        m = mods[mid]
        old_notes = len(m["notes"]); old_cards = len(m["cards"]); old_quiz = len(m["quiz"])
        m["summary"] = summary
        m["weight"] = weight
        glossary_ok(concepts)
        m["notes"] = [
            {"title": "Concepts", "body": concepts},
            {"title": mid_title, "body": mid_body},
            {"title": "Project brief", "body": project},
            noah,
        ]
        # expand quiz to template depth (10), preserving existing 6
        assert len(m["quiz"]) == 6, f"{mid}: expected 6 existing quiz, found {len(m['quiz'])}"
        m["quiz"] = m["quiz"] + quiz_new
        for q in m["quiz"]:
            quiz_ok(q)
        # cards preserved (6 >= template depth 6)
        assert len(m["cards"]) == 6, f"{mid}: expected 6 cards"
        print(f"{mid}: notes {old_notes}->4, cards {old_cards}, quiz {old_quiz}->{len(m['quiz'])}, weight={weight}")

    # ---- course-level consistency checks (all keys must exist) ----
    for k in ["arc", "priorities", "battlePlan", "mockTasks", "cheatSheets",
              "answerBank", "mockMinutes", "sourceLinks", "honestyNote",
              "scriptLabs", "drills", "scenarios", "trainers"]:
        assert k in d, f"missing course key {k}"
    assert isinstance(d["mockMinutes"], int)
    for t in d["mockTasks"]:
        if t.get("type") == "choice":
            assert len(t["choices"]) == 4 and 0 <= t["answer"] <= 3 and t.get("explain"), f"bad mock task {t.get('id')}"
        elif t.get("type") == "code":
            assert t.get("prompt") and t.get("starter") and t.get("required") and t.get("answer") is not None, f"bad code task {t.get('id')}"
    for s in d["sourceLinks"]:
        assert s.get("name") and s.get("url") and s.get("retrieved"), f"sourceLink missing retrieved: {s.get('name')}"
    assert d["honestyNote"].strip()

    # ---- competitor-brand hygiene on the whole document ----
    import re
    banned = re.compile(r"\b(ALEKS|Brilliant|Khan Academy|Coursera|Udemy|edX|Palantir|NSA)\b")
    for mm in banned.finditer(json.dumps(d, ensure_ascii=False)):
        ctx = json.dumps(d, ensure_ascii=False)[max(0, mm.start()-60):mm.end()+60]
        # allow plain-English 'brilliant'; flag only platform names
        if mm.group(1).lower() != "brilliant":
            raise AssertionError(f"banned brand found: {ctx}")

    # ---- write atomically, same style as before (minified + trailing newline) ----
    out = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    tmp = PATH + ".new"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(out + "\n")
    verify = load(tmp)  # validate BEFORE replacing
    assert verify["courseId"] == d["courseId"]
    assert len(verify["modules"]) == 3
    os.replace(tmp, PATH)
    final = load(PATH)  # validate AFTER writing
    assert len(final["modules"]) == 3
    print("WRITE OK — modules:", [m["id"] for m in final["modules"]])

if __name__ == "__main__":
    main()
