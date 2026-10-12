#!/usr/bin/env python3
"""Retrofit IL-03 (Programming Language Forge) to the Multicloud course template.
Builds new module summaries/notes/quiz explains in code; preserves all facts.
"""
import json, os

SRC = "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-03-programming-language-forge.json"

with open(SRC) as f:
    doc = json.load(f)
mods = {m["id"]: m for m in doc["modules"]}
assert len(mods) == 4, len(mods)

# ---------------------------------------------------------------- module 1/4
m0 = mods["il03-programming-backbone"]
m0["weight"] = 2
m0["summary"] = (
    "Welcome to IL-03: Programming Language Forge. I'm your instructor, and over four modules "
    "we're going to forge the programming backbone every serious engineer stands on — languages as "
    "instruments, data structures and algorithms as the canonical craft, and debugging as a discipline. "
    "This is Module 1: The Programming Backbone — Python, Java, C++, and DSA. We take the three "
    "languages in sequence because each teaches what it's best at: Python for fluency and the standard "
    "library, Java for OOP discipline and the type system, C++ for the memory model and zero-cost "
    "abstraction. DSA grows alongside — every structure you implement in the language of the week, "
    "analyzed from first principles. And throughout it all, Noah is your Socratic debugging coach: "
    "hypothesis first, hints second."
)
m0["notes"] = [
    {
        "title": "Concepts",
        "body": (
            "- **instrument, not identity** — Python, Java, and C++ are tools with strengths; the lesson is choosing the right one for the job, not pledging allegiance to one.\n"
            "- **generator** — A Python iterator produced lazily with `yield`; items are computed on demand with O(1) memory, so pipelines can handle inputs that never fit in RAM.\n"
            "- **context manager** — The `with`-block protocol (`__enter__`/`__exit__`); guarantees cleanup — files closed, locks released — even when exceptions fly.\n"
            "- **duck typing** — Python's protocol-oriented OOP: if it quacks (`__len__`, `__iter__`), treat it as a duck. Dunder methods are the protocols; ABCs (abstract base classes) are the explicit interfaces.\n"
            "- **PECS** — Producer Extends, Consumer Super: `? extends T` when reading from a generic (producer), `? super T` when writing into it (consumer). If you can't explain PECS, you don't know Java generics yet.\n"
            "- **lazy stream** — Java's intermediate stream ops (filter, map, peek) do nothing until a terminal op (collect, forEach) runs; they fuse and execute per element.\n"
            "- **virtual thread** — Java 21's lightweight thread: thread-per-task at massive scale for I/O-bound work. Caveat: `synchronized` blocks pin carriers — prefer `ReentrantLock`.\n"
            "- **RAII** — Resource Acquisition Is Initialization: constructors acquire, destructors release; smart pointers (`unique_ptr`, `shared_ptr`) make ownership explicit, so leaks are impossible by construction.\n"
            "- **rule of five** — If you define any of destructor, copy/move constructor, copy/move assignment, define (or delete) all five. (Or follow the rule of zero: let the compiler do it.)\n"
            "- **move semantics** — `std::move` plus rvalue references eliminate copies; the transfer of ownership instead of duplication is the core of modern C++ performance.\n"
            "- **undefined behavior (UB)** — Code the standard doesn't define: use-after-free, data races, signed overflow, uninitialized reads. The compiler owes you nothing afterwards — learn to predict UB from reading code.\n"
            "- **Big-O** — A comparative tool, not a prophecy: n log n vs n² at n=10⁶ is the difference between a second and a lifetime. Always ask best/average/worst, and the space-time trade-off.\n"
            "- **dynamic programming** — Optimal substructure plus overlapping subproblems: memoize first, tabulate second. Recognize the pattern before reaching for it.\n"
            "- **race condition** — Two threads interleaving read-modify-write (`counter += 1` is three bytecodes: LOAD, ADD, STORE) so updates get lost. Reproduce the race first — a fix for a bug you can't reproduce is a guess.\n"
            "- **SOLID** — Five design principles for maintainable OOP; the D (Dependency Inversion: depend on abstractions, not concretions) is the seam that makes testing possible.\n"
            "- **canonical node** — This module's DSA material is the single canonical algorithms node for the whole university; IL-08 deepens the theory, nothing is duplicated."
        ),
    },
    {
        "title": "Hands-on procedure",
        "body": (
            "The forge runs on a weekly rhythm: one language, one structure, one race, one pattern. "
            "Python week: every script lab from scratch, and you write a failing test *first* — the bug zoo below "
            "assumes test-first discipline. Java week: PECS drills until reflexive, then trace one stream pipeline "
            "by hand each day, annotating each op LAZY or TERMINAL. C++ week: UB drills — predict the nasal demons "
            "before the compiler shows them to you.\n\n"
            "1. **Generator pipeline lab** — Build the data pipeline two ways: list-based and generator-based, "
            "and measure peak memory with `tracemalloc` on a large input (see scriptLab il03-lab-generators). "
            "The required fragments force the laziness comparison.\n"
            "2. **PECS exercise** — Write a method taking `List<? extends Number>` (producer: read-only) and one "
            "taking `List<? super Integer>` (consumer: safe to add Integer). Get the bounds backwards once on "
            "purpose, read the compiler error, fix it.\n"
            "3. **Race laboratory** — Write the threaded counter from scriptLab il03-lab-race, run it, and observe "
            "the shortfall (expected 400000, got less). Only then fix it with a `Lock`. Show the bug BEFORE the fix.\n"
            "4. **BST degeneration** — Implement the binary search tree in scriptLab il03-lab-bst: insert "
            "[5,3,7,1,9], verify inorder is sorted (the invariant). Then insert range(1000) sorted and measure the "
            "height — 1000, a linked list. That's why AVL and red-black exist.\n"
            "5. **Build toolchain** — Compile a two-translation-unit C++ program by hand: compile each to an object "
            "file, then link. Watch a header-guard mistake produce a link error, and learn what the linker is telling you.\n"
            "6. **Before/after refactoring** — Take one of your own week-one scripts and refactor it against a SOLID "
            "checklist (single responsibility first). Keep both versions; the diff is the lesson."
        ),
    },
    {
        "title": "Project brief",
        "body": (
            "Your deliverable is a **cross-language kata portfolio**: one problem, solved in all three languages, "
            "with analysis. Pick any three of the following — (a) a seeded word-frequency counter over a large text "
            "file, (b) an LRU cache with O(1) get/put, (c) Dijkstra over a generated graph, (d) a thread-safe "
            "bounded queue, (e) a JSON pretty-printer.\n\n"
            "For each kata you ship four artifacts: the Python solution (idiomatic: comprehensions, generators, "
            "context managers), the Java solution (typed: PECS-correct generics, a stream pipeline where it fits), "
            "the C++ solution (memory-honest: RAII, no raw `new`/`delete`, move where it pays), and a one-page "
            "analysis — Big-O of time and space, where each language helped or hurt, and which solution you'd ship "
            "and why. Include the test suite you wrote first and a bug-zoo entry: one bug you hit, the hypothesis "
            "you stated to Noah before the fix, and the fix.\n\n"
            "This is the university's canonical DSA node, so the bar is the implementation being *yours*: every "
            "structure hand-written once, every analysis done from first principles. Noah grades the reasoning, "
            "not just the green tests."
        ),
    },
    {
        "title": "Noah check-in",
        "body": (
            "Noah is your Socratic debugging coach for this module — hypothesis first, hints second. "
            "Noah probes mastery with questions like:\n"
            "- Show Noah your threaded counter shortfall. What's your hypothesis for *where* the interleaving happens — which of the three bytecodes? Don't reach for the lock until you can narrate the race.\n"
            "- Trace this stream pipeline by hand, annotating each operation LAZY or TERMINAL, and tell Noah exactly when `filter` first executes: `list.stream().filter(...).map(...).collect(toList())`.\n"
            "- Read this C++ snippet and predict: is it UB, and which kind? `int a[2]; a[2] = 5;` — then argue *why* the compiler is allowed to do anything at all.\n"
            "- Explain PECS to Noah as if Noah were a junior: why is `List<? super Integer>` safe to *add* Integer to, but not safe to *read* Integer from?\n"
            "- *Bug zoo ritual:* before any fix, state your hypothesis out loud. If the hypothesis is wrong, the zoo gets an entry — wrong hypotheses are the tuition you pay for right ones."
        ),
    },
]
for q in m0["quiz"]:
    pass  # explains patched below
m0["quiz"][0]["explain"] = "Generators are lazy — the expression evaluates when consumed, seeing the appended 4 (see the generator entry in the Concepts section)."
m0["quiz"][1]["explain"] = "Consumer super: safe to add Integer; the list holds Integer or a supertype (PECS, from the Concepts section)."
m0["quiz"][2]["explain"] = "Out-of-bounds write — classic undefined behavior; the compiler owes you nothing afterwards (see UB in the Concepts section)."
m0["quiz"][3]["explain"] = "Heapsort is O(n log n) worst-case in-place; quicksort degrades to O(n²) without randomization (Big-O, from the Concepts section)."
m0["quiz"][4]["explain"] = "BFS explores in increasing distance — first visit is via the fewest edges (covered in the Project brief's Dijkstra kata)."
m0["quiz"][5]["explain"] = "Dependency Inversion: high-level modules depend on abstractions — the seam that makes testing possible (SOLID, from the Concepts section)."

# ---------------------------------------------------------------- module 2/4
m1 = mods["il03-systems-software"]
m1["weight"] = 2
m1["summary"] = (
    "Welcome back to the Forge. I'm your instructor, and this is Module 2: Systems Software — from computer "
    "organization to software engineering. Module 1 gave you instruments; this module gives you the substrate "
    "every program runs on: how bits become data, how the OS juggles processes, how packets cross the network, "
    "how databases keep their promises, and how software gets built by teams. Concepts here become commands in "
    "IL-04's Linux path and designs in IL-08's theory track — learn the idea here, type it there. We close with "
    "the full-stack capstone: scoped, built, deployed, and presented against a public rubric — the artifact "
    "IL-10's career path will present as evidence."
)
m1["notes"] = [
    {
        "title": "Concepts",
        "body": (
            "- **two's complement** — The signed-integer representation where addition 'just works' and there is a single zero; the reason your CPU doesn't need separate add/subtract circuits.\n"
            "- **fetch-decode-execute** — The CPU's heartbeat: fetch the instruction, decode it, execute it — on registers, billions of times per second.\n"
            "- **memory hierarchy** — Registers → L1/L2/L3 cache → RAM → SSD: each level bigger and slower. Performance lives or dies here, not in the ALU.\n"
            "- **locality** — Temporal (reuse the same data soon) and spatial (use nearby data soon). Caches exploit both; the row-major vs column-major matrix exercise makes a ~10x difference you can measure.\n"
            "- **process vs thread** — A process owns an isolated address space; a thread shares its process's address space. Shared memory is the power and the peril.\n"
            "- **virtual memory** — The OS's great illusion: every process gets its own address space, and the MMU plus page tables maintain it. A page fault means the MMU found no mapping — the OS pages it in, or kills the process.\n"
            "- **starvation** — What happens when a scheduler (FCFS, round-robin, priorities) never gets around to a waiting task; priorities without aging are the classic cause.\n"
            "- **inode** — The filesystem's metadata record: permissions, ownership, block pointers — everything about a file except its name.\n"
            "- **OSI model** — Seven layers used as a troubleshooting map: when the app fails, work bottom-up (physical → link → network → transport → ...) and find the first broken layer.\n"
            "- **TCP vs UDP** — TCP: reliability plus ordering at a latency cost. UDP: speed with app-managed reliability. Chat wants ordering (TCP); games and voice often take UDP with custom recovery.\n"
            "- **ACID** — Atomicity, Consistency, Isolation, Durability: the transaction contract a database makes with you.\n"
            "- **3NF** — Third normal form: every non-key attribute depends on the key, the whole key, and nothing but the key — the rule that eliminates transitive dependencies.\n"
            "- **index trade-off** — Indexes speed WHERE/JOIN/ORDER BY on their columns (B-trees underneath) and cost on every write. Design is trade-off; EXPLAIN is the truth serum.\n"
            "- **test pyramid** — Many fast unit tests at the base, fewer integration tests, fewest slow end-to-end tests at the top. Invert it and your suite becomes a boat anchor.\n"
            "- **REST contract** — Resources modeled as URLs, verbs with semantics (PUT is idempotent — repeating it converges; POST typically creates anew), versioned and documented so a client you didn't write can conform to it."
        ),
    },
    {
        "title": "Hands-on procedure",
        "body": (
            "This module is a laboratory arc: measure first, then believe. The cache exercise, the sockets series, "
            "and the query gym all follow the same ritual — predict, measure, explain.\n\n"
            "1. **Cache locality measurement** — Write the matrix traversal twice (row-major and column-major) over "
            "a large matrix and time both. The ~10x gap is spatial locality made physical; write down which layout "
            "C uses and why it wins.\n"
            "2. **Sockets project series** — Build the TCP echo server (blocking), then add `select`, then a threaded "
            "version, then the chat server. Feel the C10k problem in your own code before learning its solutions.\n"
            "3. **Packet-level debugging** — With the chat server running, debug a deliberately broken client using "
            "ping, traceroute, dig, curl, and a packet capture. Read the capture: SYN, SYN-ACK, ACK — the handshake, "
            "in the wild.\n"
            "4. **Schema design** — Model a small domain (orders, customers, products) to 3NF on paper, then "
            "deliberately denormalize one table for read performance and document *why* — denormalize deliberately, "
            "never by accident.\n"
            "5. **Query gym** — Against a real database, write the graded queries (joins, aggregation, subqueries), "
            "run EXPLAIN on each, and add the composite index that kills the full table scan. Record the before/after "
            "plans — the decision record is the deliverable, not just the fast query.\n"
            "6. **Contract-first API** — Write the API contract first (resources, verbs, auth shape: sessions vs "
            "tokens vs OAuth), then implement to it. Your API is graded by a client you didn't write — conformance "
            "tests are the specification."
        ),
    },
    {
        "title": "Project brief",
        "body": (
            "Your deliverable is the **full-stack capstone**, staged like a real engagement: scoping, "
            "implementation, deployment, presentation.\n\n"
            "**Scope ruthlessly.** One page: the problem, the user, the three features that matter, and the five "
            "you're cutting. The cut list is graded — restraint is the skill.\n\n"
            "**Build it end to end.** Frontend (HTML/CSS, JavaScript: DOM, events, fetch), backend API "
            "(contract-first: REST resource modeling, auth, versioning, documentation), relational database "
            "(3NF schema, indexes justified with EXPLAIN output). The test pyramid governs: unit-heavy, "
            "integration in the middle, a thin e2e cap.\n\n"
            "**Deploy and present.** Ship it somewhere real, then present against the public rubric: does it run, "
            "is the schema sane, is the API contract honored, is the scope honest? This artifact travels with you — "
            "IL-10's career path presents it as portfolio evidence, so the README must explain the system to a "
            "stranger in five minutes.\n\n"
            "Agile practice runs underneath the whole build: a backlog with hygiene, standups with yourself (or "
            "your team), and a retro at each stage gate. The SDLC model you pick — waterfall, agile, spiral — must "
            "be justified in the scope document: when each fits is part of what you're proving you know."
        ),
    },
    {
        "title": "Noah check-in",
        "body": (
            "Noah probes mastery with questions like:\n"
            "- Explain your cache-exercise numbers to Noah: why did row-major win, which cache level did the win "
            "come from, and what would change the result?\n"
            "- Your chat server uses TCP. Argue the UDP case to Noah anyway — what would you have to build "
            "yourself to make UDP chat acceptable, and when would it be worth it?\n"
            "- Show Noah your EXPLAIN before and after the composite index. What did the planner do differently, "
            "and what does the index cost you on every INSERT?\n"
            "- Walk Noah through one scheduling scenario: round-robin with a CPU-hog and an interactive task — "
            "who starves, and what fixes it?\n"
            "- Defend your capstone cut list: which five features died, and what would have broken if you'd kept them?"
        ),
    },
]
m1["quiz"][0]["explain"] = "Spatial locality: row-major matches C's layout — the cache-line effect is measurable and huge (see locality in the Concepts section, measured in the Hands-on procedure)."
m1["quiz"][1]["explain"] = "Page fault = address not currently mapped; the OS pages it in (or kills the process if invalid) — virtual memory, from the Concepts section."
m1["quiz"][2]["explain"] = "Choose by requirements: chat wants ordering (TCP); games/voice often take UDP + custom recovery (TCP vs UDP, from the Concepts section)."
m1["quiz"][3]["explain"] = "3NF: non-key attributes depend only on the key — no transitive chains (see 3NF in the Concepts section)."
m1["quiz"][4]["explain"] = "Indexes serve lookups/sorts on their columns; they cost on writes and don't help unindexed scans (index trade-off, from the Concepts section)."
m1["quiz"][5]["explain"] = "Conformance tests from an independent client — the contract is the specification (from the Hands-on procedure's contract-first exercise)."

# ---------------------------------------------------------------- module 3/4
m2 = mods["il03-mit-ocw"]
m2["weight"] = 1
m2["summary"] = (
    "Welcome to Module 3: the MIT 6-3 Reference Layer. I'm your instructor, and this module is a map, not a "
    "territory. MIT's Electrical Engineering & Computer Science curriculum — 6.100A/B Python, 6.1200 discrete "
    "math, 6.1210/6.1220 algorithms, 6.1910 computation structures, 6.1800/6.1810 systems, 6.3900 machine "
    "learning — distilled into prerequisite order as a study layer over MIT OpenCourseWare's public materials. "
    "The platform's rules govern this layer: no duplicated courses (overlap routes to the single canonical node), "
    "prerequisite gates before the algorithms and ML nodes, and honest pacing adapted for solo learners. "
    "Use it as a reading and problem-set guide; the deep study lives in the IL modules it points to."
)
m2["notes"] = [
    {
        "title": "Concepts",
        "body": (
            "- **6.100A/B** — Introduction to Computer Science Programming in Python. Its problem sets are the practice spine of this layer: done in order, with Noah for Socratic help when stuck.\n"
            "- **6.1200** — Mathematics for Computer Science: proofs and induction, number theory for CS, graph theory, probability for computing. The discrete-math bridge into IL-02's canonical discrete node.\n"
            "- **induction template** — Base case, inductive hypothesis, inductive step — until it's muscle memory. This is the proof technique the algorithms courses assume you already own.\n"
            "- **number theory for CS** — Modular arithmetic, gcd, Fermat's little theorem: the RSA prerequisites, and the reason 6.1200 matters to security engineers.\n"
            "- **6.1210 / 6.1220** — Introduction to / Design and Analysis of Algorithms: sorting, hashing, divide-and-conquer, dynamic programming — gated on discrete-math fluency, because algorithm analysis is applied discrete math.\n"
            "- **6.1910** — Computation Structures: the climb from digital logic to the processor, assembly and the machine, caches and virtual memory — the hardware/software interface.\n"
            "- **6.1800 / 6.1810** — Computer Systems Engineering / Operating System Engineering: design principles at scale, taught through the classic design papers.\n"
            "- **end-to-end argument** — A 6.1800 design-paper staple: place function at the endpoints of the system unless there's a compelling reason not to. Read every design paper asking what problem, what insight, what trade-off.\n"
            "- **6.3900** — Introduction to Machine Learning: the on-ramp map, not the territory. The platform runs a prerequisite audit (IL-02 linear algebra + probability) before opening it; the territory is IL-07 and IL-16.\n"
            "- **canonical-node rule** — The global rule: where OCW overlaps an IL module (6.1200 vs IL-02's discrete module, 6.1210 vs Module 1's DSA), the platform routes to the single canonical node. No duplicated courses, ever.\n"
            "- **term-structure honesty** — OCW problem sets assume MIT's term structure: recitations, office hours, a cohort. Solo learners get adapted pacing — one problem set per week per course is a full-time pace."
        ),
    },
    {
        "title": "Hands-on procedure",
        "body": (
            "This layer is walked, not watched. The procedure turns six course catalogs into one personal curriculum.\n\n"
            "1. **Build the sequence** — Lay out the six courses in prerequisite order (6.100A/B → 6.1200 → "
            "6.1210/1220 → 6.1910 → 6.1800/1810 → 6.3900) and mark every canonical-node overlap: wherever OCW "
            "duplicates an IL module, write down the IL node you'll use instead.\n"
            "2. **Set the cadence** — One problem set per week per course is full-time pace. Be honest about your "
            "hours and pick one course at a time; the schedule is a contract with yourself.\n"
            "3. **Run the prerequisite audit** — Before opening 6.1210: can you do an induction proof cold? Before "
            "6.3900: have IL-02's linear-algebra and probability nodes verified? Gates are there to save you from "
            "opaque proofs, not to slow you down.\n"
            "4. **Work the 6.100A/B problem sets** — In order, with Noah: hypothesis first, hints second. The "
            "problem sets are the Python practice spine of Module 1's language work.\n"
            "5. **Simulator labs for 6.1910** — Build the ALU in the digital-logic simulator *before* reading about "
            "pipelining. The gates-first arc only works if your hands go first.\n"
            "6. **Active paper reading** — For each 6.1800/6.1810 design paper, write one paragraph: the problem, "
            "the insight, the trade-off. A paper you can't summarize in a paragraph is a paper you haven't read."
        ),
    },
    {
        "title": "Project brief",
        "body": (
            "Your deliverable is a **personal 6-3 study plan**: a document that could hand to a stranger and have "
            "them walk the layer.\n\n"
            "It contains: the six courses in your chosen order with the canonical-node substitutions marked (which "
            "IL modules replace which OCW overlaps, and why); your weekly cadence with the honesty math (hours "
            "available, problem sets per week, finish dates); the prerequisite gates you'll clear and how you'll "
            "verify each one; and a reading list of five 6.1800/6.1810 design papers with your one-paragraph "
            "problem/insight/trade-off summaries for two of them as samples.\n\n"
            "The plan is graded on honesty, not ambition: a sustainable twelve-month plan beats a heroic "
            "three-month plan that dies in week four. Include the failure protocol — what you do when you fall "
            "two problem sets behind (answer: re-pace, don't cram; the term-structure honesty note applies to "
            "your plan too). Revisit the plan monthly; a study plan is a living document or it's fiction."
        ),
    },
    {
        "title": "Noah check-in",
        "body": (
            "Noah probes mastery with questions like:\n"
            "- State your study order for the six courses and justify each prerequisite edge — why can't 6.1210 "
            "come before 6.1200?\n"
            "- Do an induction proof cold for Noah (Noah picks the claim). The template should be muscle memory by now.\n"
            "- Show Noah your canonical-node substitution map: where does OCW overlap IL-02 and Module 1's DSA, and "
            "which node wins each overlap?\n"
            "- Summarize one design paper in a single paragraph — problem, insight, trade-off — then defend why "
            "the trade-off was the right call.\n"
            "- What's your failure protocol? Walk Noah through exactly what happens to the plan when life costs you "
            "two weeks."
        ),
    },
]
m2["quiz"][0]["explain"] = "Algorithm analysis is applied discrete math — without induction and Big-O fluency, the proofs are opaque (see the prerequisite-audit step in the Hands-on procedure)."
m2["quiz"][1]["explain"] = "Computation Structures climbs from gates to the hardware/software interface (6.1910, from the Concepts section)."
m2["quiz"][2]["explain"] = "Recitations and office hours don't exist for solo learners — the study guide re-paces accordingly (term-structure honesty, from the Concepts section)."
m2["quiz"][3]["explain"] = "6.3900 maps the territory; IL-07 (data/AI) and IL-16 (ML engineering) are the territory (6.3900, from the Concepts section)."

# ---------------------------------------------------------------- module 4/4
m3 = mods["il03-generative-packing"]
m3["weight"] = 1
m3["summary"] = (
    "Welcome to the studio — Module 4: Generative Art: Circle Packing. I'm your instructor, and this is where "
    "precision becomes aesthetics. We build a circle packer from first principles: rejection sampling with a "
    "seeded RNG, then Poisson-disc sampling, then front-chain packing, all accelerated by spatial grids. Then "
    "parameters become a design language — Span, Factor, NC, Alpha, AngleX/AngleY, blend modes — each value a "
    "deliberate decision. And because we work from inspiration, we close with the ethics: attribution, "
    "inspired-by vs copied, and the lab notebook as experimental method. Three studies, one packer, your voice."
)
m3["notes"] = [
    {
        "title": "Concepts",
        "body": (
            "- **rejection sampling** — Propose a random candidate circle; reject it if it collides; repeat. Honest, simple, and slow enough to *feel* the algorithm.\n"
            "- **seeded RNG** — The same seed produces the same piece. Reproducibility is the difference between art and accident — and between a debuggable program and a mystery.\n"
            "- **Poisson-disc sampling** — Minimum-distance guarantees between samples via the grid-accelerated dart-throwing algorithm: even coverage without clumping.\n"
            "- **front-chain packing** — Grow from the boundary inward, placing each new circle tangent to the existing front. Denser, more deliberate compositions than pure rejection.\n"
            "- **spatial grid** — Uniform-grid hashing that makes collision checks O(1) amortized: the difference between a sketch and a system.\n"
            "- **Span** — The spacing parameter: breathing room vs density. Read it as the piece's lung capacity.\n"
            "- **Factor** — The size-falloff parameter: visual hierarchy, large to small.\n"
            "- **NC** — Hue layers: palette depth, how many color voices the piece speaks in.\n"
            "- **Alpha** — Opacity: the atmosphere and layering depth of the piece.\n"
            "- **AngleX / AngleY** — Field tilt: implied light or gravity, the direction the composition leans.\n"
            "- **blend mode** — Compositing math (multiply, screen, overlay): how layers converse. Know what the pixels do, not just what looks good.\n"
            "- **seeded variation** — Controlled surprise: the seed varies, the design language stays. Same instrument, different performance.\n"
            "- **lab notebook** — Seed, parameters, intent, result, next experiment — every study gets an entry. Experimental method applied to aesthetics.\n"
            "- **inspired-by vs copied** — Same idea plus your parameters plus your notebook = inspired. Same parameters with no transformation = copied. Lineage is a feature; name it."
        ),
    },
    {
        "title": "Hands-on procedure",
        "body": (
            "Build the packer in layers, and watch the composition quality jump at each one. Keep the lab notebook "
            "open from step one — every study gets an entry.\n\n"
            "1. **Rejection sampler** — Implement the honest version: seeded RNG, propose a random (x, y, r), "
            "reject on collision with any placed circle, repeat until N placed or attempts exhausted. Render it. "
            "It will be slow and sparse — that's the baseline.\n"
            "2. **Spatial grid** — Add uniform-grid hashing for collision checks (O(1) amortized). Measure the "
            "speedup at N=2000; the grid is what turns the sketch into a system.\n"
            "3. **Poisson-disc upgrade** — Replace pure rejection with grid-accelerated dart throwing enforcing a "
            "minimum distance. Compare the coverage: no more clumping, no more voids.\n"
            "4. **Front-chain packing** — Implement boundary-inward growth, each circle tangent to the front. "
            "Compare density against Poisson-disc on the same seed.\n"
            "5. **Parameter block** — Expose Span, Factor, NC, Alpha, AngleX/AngleY, and blend mode as one block. "
            "Read it like a score: each value is a choice about the piece's physics.\n"
            "6. **One-parameter experiments** — Change exactly one parameter at a time; record the effect in the "
            "notebook (seed, parameters, intent, result, next experiment). Ten experiments minimum before the "
            "three studies."
        ),
    },
    {
        "title": "Project brief",
        "body": (
            "Your deliverable is **three studies from one packer**: same instrument, three distinct parameter "
            "voices — breadth proves the instrument, not the accident.\n\n"
            "Study 1 — *Density*: push Span low and Factor steep; document where the composition breaks (overlap "
            "artifacts, muddy blends) and where it sings. Study 2 — *Atmosphere*: Alpha low, blend modes doing "
            "the work; the piece should feel like weather. Study 3 — *Tilt*: AngleX/AngleY carrying the composition; "
            "implied light or gravity must read at a glance.\n\n"
            "Each study ships with its lab-notebook entry (seed, parameters, intent, result, next experiment) and "
            "an attribution line: name what inspired it — the Pattlas piece, a parameter block you read, a paper "
            "on sampling — explicitly. Inspired-by means your parameters plus your notebook plus your "
            "transformation; the lineage section of each entry states what you took and what you changed. "
            "Honest attribution is graded alongside the pixels: a beautiful study with a missing lineage fails "
            "the ethics bar."
        ),
    },
    {
        "title": "Noah check-in",
        "body": (
            "Noah probes mastery with questions like:\n"
            "- Show Noah your rejection sampler's collision check. Where's the O(n²) hiding, and exactly how does "
            "the spatial grid kill it?\n"
            "- Read your own parameter block back to Noah like a score: defend each value as a design decision. "
            "Which one would you change first, and what would you expect?\n"
            "- Compare your Poisson-disc and front-chain renders on the same seed: which is denser, which is more "
            "even, and which would you choose for a poster vs a texture?\n"
            "- State the inspired-by vs copied test for your Study 2: what did you take, what did you transform, "
            "and where's the lineage recorded?\n"
            "- Your notebook's 'next experiment' column: pick the most interesting one and argue why it's the "
            "right next move."
        ),
    },
]
m3["quiz"][0]["explain"] = "Each new circle sits tangent to the existing front — denser, deliberate compositions (front-chain packing, from the Concepts section)."
m3["quiz"][1]["explain"] = "Alpha is opacity: the atmosphere and layering depth of the piece (see Alpha in the Concepts section)."
m3["quiz"][2]["explain"] = "Seed + parameters + intent + result + next experiment — experimental method for aesthetics (lab notebook, from the Concepts section)."
m3["quiz"][3]["explain"] = "No transformation, no voice — that's copying. Attribute and transform (inspired-by vs copied, from the Concepts section)."

# ---------------------------------------------------------------- write back
with open(SRC, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write("\n")
with open(SRC) as f:
    doc2 = json.load(f)
print("OK: modules =", len(doc2["modules"]))
for m in doc2["modules"]:
    assert set(["id","code","title","weight","summary","objectives","notes","cards","quiz"]) <= set(m.keys()), m["id"]
    assert [n["title"] for n in m["notes"]] == ["Concepts","Hands-on procedure","Project brief","Noah check-in"], m["id"]
    assert len(m["notes"]) == 4 and len(m["cards"]) >= 5 and len(m["quiz"]) >= 4, m["id"]
    for q in m["quiz"]:
        assert len(q["choices"]) == 4 and 0 <= q["answer"] < 4 and q["explain"], (m["id"], q["q"][:40])
    assert "I'm your instructor" in m["summary"], m["id"]
    assert all(n["body"] for n in m["notes"]), m["id"]
print("ALL ASSERTIONS PASS")
