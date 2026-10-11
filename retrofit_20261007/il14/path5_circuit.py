# -*- coding: utf-8 -*-
"""IL-14 retrofit content — Path 5: Technical Mock Interview Circuit (5 modules)."""
# pylint: disable=line-too-long

P5_SUMMARY = {
"tech-mock-interview-circuit--mock-dsa": (
"Welcome to the Technical Mock Interview Circuit of the Interstitium Labs SRE, DevOps, Cloud & Security Interview Prep course. "
"I'm your instructor for this final path, and we start where most loops start: data structures and algorithms as a sport. Pattern recognition, timed reps, and the narration habit that turns a solved problem into a passing round. "
"This is Module 1: DSA Speed Reps. You'll drill two pointers, sliding windows, trees, graphs, heaps, and DP basics — stating complexity aloud every single rep, because the interview grades the analysis as well as the code."
),
"tech-mock-interview-circuit--mock-sysdesign": (
"Welcome back. I'm your instructor for the Mock Interview Circuit, and this is Module 2: System Design Reps. "
"Design reps with the classics: requirements first, back-of-envelope math, then architecture defended against its own bottlenecks. Functional vs non-functional requirements, API and data-model design, scaling levers — shard, cache, queue — and bottleneck analysis by walking the path. "
"You'll prep the shortener, the feed, and the chat for their lessons, not their diagrams."
),
"tech-mock-interview-circuit--mock-behavioral": (
"Welcome back. I'm your instructor for the Mock Interview Circuit, and this is Module 3: The Behavioral Story Bank. "
"Behavioral rounds are won before the interview: a bank of ten rehearsed STAR stories — conflict, failure, leadership — practiced aloud until they sound unrehearsed, plus 'why this company' answered with specifics and questions that reveal the job's reality. "
"You'll record yourself, hear what the interviewer hears, and cut 40%."
),
"tech-mock-interview-circuit--mock-domains": (
"Welcome back. I'm your instructor for the Mock Interview Circuit, and this is Module 4: Domain Deep Dives. "
"The round candidates bomb: the deep dive. Your domain — SRE, DevOps, cloud, security — one level deeper than the job post demands, until you can teach the topic back. Read the job description as an exam, prepare one story and one deep-dive per bullet. "
"You'll learn the recovery for the blank moment too: state what you know precisely, name the boundary, reason from first principles aloud."
),
"tech-mock-interview-circuit--mock-full-loop": (
"Welcome back. I'm your instructor for the Mock Interview Circuit, and this is Module 5: Full-Loop Simulation — the dress rehearsal. "
"A full simulated loop day with a partner: four timed rounds, rotating interviewer roles, rubric scoring, and a debrief that turns the weakest round into next week's plan. Then the weakness-targeting week, the final checklist, and the taper. "
"This is where the whole course converges: stamina and context-switching, trained like the skills they are."
),
}

P5_NOTES = {
"tech-mock-interview-circuit--mock-dsa": [
{"title": "Concepts", "body": (
"- **Two pointers** — ordered data and pair-finding: opposite ends for sorted two-sum; same-direction fast/slow for cycle detection or in-place dedup. O(n) time, O(1) space.\n"
"- **Sliding window** — a window that expands/contracts over arrays/strings: the shape for subarray and substring optima.\n"
"- **BFS / DFS** — level-order vs depth-first traversal: BFS for shortest path in unweighted graphs, DFS for connectivity and topological shapes.\n"
"- **Heap** — top-k and streaming medians: the 'k smallest/largest' reflex.\n"
"- **Dynamic programming** — overlapping subproblems with optimal substructure: 1D ladder shapes, knapsack shapes — state the recurrence before coding.\n"
"- **Complexity aloud** — 'this is O(n) time, O(1) space because…': stated at each step, it's your early-warning system and the interviewer's grading feed.\n"
"- **The 30-minute bar** — 5 min clarify + plan, 20 min code, 5 min test: budget it aloud.\n"
"- **Brute force first** — state it and its complexity: a working fallback that buys time and shows honesty.\n"
"- **Miss categories** — wrong pattern, implementation bug, complexity fumble, time management: fix the category, not the instance."
)},
{"title": "Hands-on procedure", "body": (
"Run a 45-minute DSA speed-rep session — the sport's training unit.\n"
"1. **Pick the pattern batch.** Today: trees/graphs/heaps (traversals, BFS/DFS, top-k). Tomorrow: DP basics (1D ladder, knapsack shapes). One batch per session.\n"
"2. **Set the timer: 30 minutes per problem.** Budget aloud before starting: 5 clarify + plan, 20 code, 5 test.\n"
"3. **Clarify first.** Restate the problem, name the edge cases, state the pattern you suspect and why.\n"
"4. **Brute force, stated.** Write it, state its complexity — the honest baseline — then optimize the bottleneck.\n"
"5. **Narrate complexity at every step.** 'This loop is O(n) because…' — said out loud, every rep. Silent reps train half the interview.\n"
"6. **Debrief by category.** For each miss: wrong pattern, bug, complexity fumble, or time — then redrill the category, not the problem."
)},
{"title": "Project brief", "body": (
"Your deliverable: a personal DSA playbook — the pattern reference you'd trust in a loop.\n"
"- **One page per pattern**: two pointers, sliding window, BFS/DFS, heaps, DP basics — the recognition triggers, the template shape, the complexity.\n"
"- **The complexity cheat**: Big-O for the common operations, written from understanding — the analysis you state aloud.\n"
"- **Your miss log**: every recent miss classified by category, with the redrill that fixed it.\n"
"- **The 30-minute bar card**: the time budget, the brute-force rule, the test checklist — on one index card.\n"
"- **Two timed sets per week**, debriefed by category, until the narration is reflex.\n"
"Reference shelf (module sources): **NeetCode** (https://neetcode.io/) — pattern-organized DSA practice for the speed reps. **Big-O Cheat Sheet** (https://www.bigocheatsheet.com/) — complexity quick-reference for the analysis-aloud drills."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and drill speed is not engineering judgment. "
"Real work rewards choosing the right approach and maintaining it; interviews reward recognizing patterns under time. Train both honestly: the reps build the reflex, and the debrief builds the skill. "
"Never present drill counts as experience; present the method — pattern recognition, complexity aloud, categorized redrills — which is what the reps actually teach."
)},
],
"tech-mock-interview-circuit--mock-sysdesign": [
{"title": "Concepts", "body": (
"- **Functional requirements** — what the system does: the features, the APIs, the behaviors.\n"
"- **Non-functional requirements** — how well: scale, latency, availability, consistency — the constraints that shape architecture.\n"
"- **Back-of-envelope estimation** — requests/sec, storage, bandwidth from stated assumptions: the arithmetic before the boxes.\n"
"- **Sharding** — splitting data across nodes: the lever for data too big or hot for one machine.\n"
"- **Caching** — skipping work for hot paths: the lever for read-heavy, slow-changing data, with an invalidation plan.\n"
"- **Queues** — deferring work in time: the lever for spikes and async processing.\n"
"- **Bottleneck analysis** — walking the request path asking 'what breaks first at 10×?' and applying the right lever per hop.\n"
"- **The classic lessons** — shortener: IDs and caching; feed: fan-out; chat: real-time. Learn the lesson, not the diagram."
)},
{"title": "Worked estimation", "body": (
"Do the back-of-envelope for a URL shortener — the estimation interviewers watch most closely.\n"
"1. **State the assumptions.** 100M URLs shortened per month; 10:1 read/write ratio. Write them — assumptions are gradable.\n"
"2. **Writes.** 100M ÷ 30 days ≈ 40 writes/sec average; plan for 10× peak: 400 writes/sec.\n"
"3. **Reads.** 10 × 100M = 1B reads/month ≈ 400 reads/sec average; 4,000/sec at peak.\n"
"4. **Storage.** 100M URLs × ~500 bytes metadata ≈ 50 GB — trivial for one database; say so, and say why that simplifies the design.\n"
"5. **Bandwidth.** 4,000 reads/sec × ~500 bytes ≈ 2 MB/sec — the network is not the bottleneck; the ID generation and cache are the design.\n"
"6. **Name the lesson.** 'The estimation says: this is a caching and ID-generation problem wearing a URL-shortener costume.'"
)},
{"title": "Project brief", "body": (
"Your deliverable: three classic design one-pagers — shortener, feed, chat.\n"
"- **Each one-pager**: requirements (functional + non-functional), the worked estimation, the 2–3 key decisions, the scaling story, the bottleneck walk.\n"
"- **The labeled diagram**: every arrow labeled with what flows — 'the labels are where the design lives.'\n"
"- **The lesson line** per classic: what this design teaches that transfers to the next question.\n"
"- **The follow-up bank**: the five hardest questions per design, answered in writing.\n"
"- **Rehearse each aloud in 30 minutes**, then have a partner attack the bottlenecks.\n"
"Reference shelf (module sources): **System Design Primer** (https://github.com/donnemartin/system-design-primer) — the classic designs and tradeoffs. **AWS Well-Architected Framework** (https://docs.aws.amazon.com/well-architected/) — the architecture interview's rubric."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and the worked numbers are illustrative estimates. "
"Real systems have messier requirements and the estimation assumptions here are stated, not factual — never quote them as real traffic figures. What transfers is the estimation method and the lesson-per-classic discipline. "
"Design reps train interview reasoning, not production architecture judgment; present them as rehearsed method, which is exactly what design rounds grade."
)},
],
"tech-mock-interview-circuit--mock-behavioral": [
{"title": "Concepts", "body": (
"- **STAR** — Situation (2 sentences of context), Task (your responsibility), Action (what YOU did — the bulk), Result (measurable outcome + lesson): the complete evidence unit.\n"
"- **Story bank** — ten rehearsed STAR stories covering conflict, failure, leadership, ownership, and learning: banked before the loop.\n"
"- **Conflict story** — a disagreement handled professionally: what each side wanted, what decided it, what you did.\n"
"- **Failure story** — owned, with the fix: what broke, your part, what changed afterward.\n"
"- **Leadership story** — influence without authority counts: the outcome you drove through others.\n"
"- **'Why this company'** — specific, researched, tied to you: their product and challenges, something you learned, how your background maps. Generic flattery fails.\n"
"- **Recording review** — aloud reveals pacing, filler, and rambling that silent rehearsal hides: 'my first recording is always 40% too long.'"
)},
{"title": "Hands-on procedure", "body": (
"Build the story bank in one focused weekend.\n"
"1. **List ten prompts.** Conflict, failure, leadership, ownership, disagreement, mistake, tight deadline, difficult stakeholder, mentoring, proudest work.\n"
"2. **Draft each in STAR.** Two sentences of situation, your task, the bulk on YOUR actions and decisions, a measurable result plus the lesson.\n"
"3. **Time each to 2 minutes.** Behavioral answers ramble past 3; the timer is the editor.\n"
"4. **Record all ten aloud.** Listen back like an interviewer: cut filler, cut throat-clearing, keep the decisions.\n"
"5. **Write 'why this company' with specifics.** Their product, a technical challenge, something from an employee or post, your mapping to it — interchangeable answers fail.\n"
"6. **Prepare your questions.** The four reality-revealing questions; practice hearing team health in the answers."
)},
{"title": "Project brief", "body": (
"Your deliverable: the behavioral dossier.\n"
"- **Ten STAR stories**, each timed to 2 minutes, recorded and trimmed — the bank.\n"
"- **The 'why this company' page**: specifics per target company, refreshed before each loop.\n"
"- **Your interviewer questions** with notes on what good vs worrying answers sound like.\n"
"- **The recording log**: date, story, length, and the one cut you made — proof of the practice.\n"
"- **One full behavioral mock** with a partner, scored on evidence completeness and concision.\n"
"Reference shelf (module sources): **Indeed Career Guide: Interviewing** (https://www.indeed.com/career-advice) — STAR format and preparation checklists."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and rehearsed stories must stay truthful. "
"Never invent employers, outcomes, or heroics: interviewers probe stories with follow-ups, and fabricated ones collapse — in behavioral rounds, credibility is the entire evaluation. Rehearse real experience until it sounds unrehearsed; that's the whole game. "
"Bank stories from your actual work; if an experience is thin, say what you learned, not what you wish had happened."
)},
],
"tech-mock-interview-circuit--mock-domains": [
{"title": "Concepts", "body": (
"- **Domain deep dive** — the round that probes one level deeper than the job post: mechanism, tradeoffs, and judgment on your claimed expertise.\n"
"- **One level deeper** — for each listed skill: the mechanism, the tradeoff, and a story. 'I prepare the layer below the buzzword.'\n"
"- **JD as exam** — every bullet a predicted question: 'led migration to K8s' → 'walk me through that migration's hardest decision.'\n"
"- **Teach-back test** — explain it as if to a junior: if you can't produce a clear, ordered explanation with an example, you don't know it deeply enough.\n"
"- **Tradeoff question** — every technique has a cost: what you gain, what you pay, when you'd choose the alternative.\n"
"- **Blank-moment recovery** — state what you know precisely, name the boundary, reason from first principles aloud: honesty plus reasoning beats confident fabrication."
)},
{"title": "Hands-on procedure", "body": (
"Run a domain deep-dive prep session for your target role.\n"
"1. **Extract the JD's bullets.** Each becomes a predicted question with a prepared story and a deep-dive — the JD is the question list in disguise.\n"
"2. **Go one level deeper per bullet.** Mechanism, tradeoff, story. For 'Kubernetes': how the scheduler places pods, what breaks at scale, your hardest K8s decision.\n"
"3. **Teach-back each.** Explain aloud as if to a junior, with an example. Gaps you feel are gaps to fill.\n"
"4. **Pre-answer the tradeoff.** For every technique: what you gain, what you pay, when you'd choose the alternative — before the interviewer asks.\n"
"5. **Drill the blank moment.** Partner asks something you don't know; practice: 'here's what I do know precisely; here's the boundary; here's how I'd reason about it.'\n"
"6. **Log the gaps.** Every teach-back stumble becomes a study card; the log aims every hour at real weakness."
)},
{"title": "Project brief", "body": (
"Your deliverable: the deep-dive dossier for your target role.\n"
"- **The JD exam**: each bullet mapped to predicted questions, with your story and deep-dive per bullet.\n"
"- **One-level-deeper sheets**: mechanism, tradeoff, and story for the top 8 skills — teach-back ready.\n"
"- **The tradeoff bank**: the cost side of every technique you claim, in your own words.\n"
"- **The gap log**: teach-back stumbles converted to study cards, worked until the explanation is clean.\n"
"- **One full deep-dive mock**: 45 minutes on your domain, follow-ups until you hit the boundary — then the honest recovery, practiced.\n"
"Reference shelf (module sources): **AWS Documentation** (https://docs.aws.amazon.com/) — service primitives for depth. **OWASP** (https://owasp.org/) — security depth for the security domain."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and depth must be honest depth. "
"The blank-moment recovery exists because fabrication is the worst strategy: interviewers score honesty plus reasoning, and a precise partial answer with clear boundaries beats a confident invention every time. "
"Claim only the depth you have; the dossier's job is to make your real depth interview-ready, not to manufacture depth you don't."
)},
],
"tech-mock-interview-circuit--mock-full-loop": [
{"title": "Concepts", "body": (
"- **Loop day** — four timed rounds back-to-back (coding, design, domain deep-dive, behavioral): the stamina and context-switching test.\n"
"- **Rotating roles** — trading interviewer and candidate with a partner: you learn the rubric from the grading side.\n"
"- **Rubric scoring** — fixed axes per round: correctness, complexity analysis, communication, time management, tradeoffs named.\n"
"- **Weakness-targeting week** — the week between simulation and the real loop, spent only on the lowest scores: raise the floor.\n"
"- **Debrief template** — what leaked, its category, the redrill plan, the verification: written within the hour.\n"
"- **Final checklist** — logistics, rest, story bank, no new topics: the last 48 hours are about the performer."
)},
{"title": "Hands-on procedure", "body": (
"Run the full-loop simulation — the dress rehearsal.\n"
"1. **Schedule it like a real loop.** Four 45-minute rounds, 15-minute breaks, same order as your target companies: coding, design, deep-dive, behavioral.\n"
"2. **Brief your partner.** They interview first: timed, no pausing, think-aloud required, scoring against the rubric during the round.\n"
"3. **Run all four.** Stamina is the skill: each round starts clean — water, notes closed, one breath.\n"
"4. **Trade roles.** You interview them next loop: grading teaches what gradable answers look like.\n"
"5. **Debrief within the hour.** Score every axis honestly; name the two lowest; write the weakness-targeting week's plan.\n"
"6. **Execute the week, then taper.** One week on the floor-raising drills, then the final checklist: no new topics, redrill, mock, rest."
)},
{"title": "Project brief", "body": (
"Your deliverable: the loop-day dossier — the convergence of the whole course.\n"
"- **The schedule**: your four-round loop with times, roles, and rubrics.\n"
"- **Score sheets**: every axis, every round, scored honestly.\n"
"- **The debrief**: the two lowest axes, miss categories, the weakness-targeting week's day-by-day plan.\n"
"- **The final checklist**: logistics, sleep, story bank, the explicit not-study list.\n"
"- **The reflection**: which round shape still isn't automatic — and the drill that makes it so. Then rest: the taper has started.\n"
"Reference shelf (module sources): **System Design Primer** (https://github.com/donnemartin/system-design-primer). **NeetCode** (https://neetcode.io/)."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and simulation scores are triage data, not predictions. "
"Home loops lack real-loop adrenaline and real-panel skepticism; treat the dossier as a preparation instrument. Rest is part of the plan: the taper exists because performance is trained, then protected. "
"You've done the work across five paths — SRE, DevOps, cloud, security, and the circuit. Trust the structure on loop day: declare, measure, narrate, decide."
)},
],
}

P5_NEW_CARDS = {
"tech-mock-interview-circuit--mock-dsa": {
"front": "How do you choose between BFS and DFS in an interview?",
"back": "BFS for shortest path in unweighted graphs and level-order needs; DFS for connectivity, cycles, topological shapes, and when recursion depth is safe. State the choice and its complexity before coding — the choice is part of the graded reasoning. The interview line: 'BFS for distance, DFS for structure.'",
},
"tech-mock-interview-circuit--mock-sysdesign": {
"front": "How do you handle 'it depends' in a design round?",
"back": "'It depends' is only a good answer when you then explain what it depends on: the workload's read/write ratio, consistency needs, and scale decide between the options — so name the deciding factors and pick for the stated case. The interview line: 'it depends on three things; here's how each would change my answer.'",
},
"tech-mock-interview-circuit--mock-behavioral": {
"front": "How do you keep a STAR story under 2 minutes?",
"back": "Two sentences of situation, one of task, the bulk on your actions — and the result in one sentence plus the lesson. Everything else is cut in rehearsal, which is why you record: the timer is the editor. The interview line: 'my first recording is always 40% too long — that's what the practice is for.'",
},
"tech-mock-interview-circuit--mock-domains": {
"front": "What's the tradeoff question you should answer before the interviewer asks it?",
"back": "For every technique you claim: what you gain, what you pay, and when you'd choose the alternative. 'It depends' only works when you then explain what it depends on. Seniors volunteer the cost; juniors wait to be asked. The interview line: 'here's what this buys me, and here's the receipt.'",
},
"tech-mock-interview-circuit--mock-full-loop": {
"front": "How do you reset between rounds on loop day?",
"back": "Fifteen minutes, same ritual: water, notes closed, one breath — the last round's mistakes don't get a vote in this one. Context-switching is a trained skill, and the reset is the training. The interview line: 'each round starts clean; I carry the rubric, not the regret.'",
},
}

def _q(q, choices, answer, explain):
    assert len(choices) == 4 and 0 <= answer <= 3 and explain
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}

P5_NEW_QUIZ = {
"tech-mock-interview-circuit--mock-dsa": [
_q("Opposite-ends two pointers fit:",
   ["Unsorted arrays", "Sorted pair-finding — e.g. sorted two-sum or container-with-most-water", "Trees", "Graphs"], 1,
   "Ordered data and pair-finding: the pattern's recognition trigger — the Concepts."),
_q("Fast/slow pointers detect a cycle because:",
   ["They're fast", "The fast pointer laps the slow one exactly when a cycle exists — O(1) space", "They're trendy", "Recursion"], 1,
   "Same-direction pointers on linked structures: the lap is the proof — the Concepts."),
_q("Stating the brute force first is strong because:",
   ["It's expected", "It shows honest complexity reasoning and gives a working fallback while you optimize", "It's faster", "It's required"], 1,
   "A correct slow solution beats a blank editor; optimization then has a baseline — the Concepts."),
_q("A heap is the right tool for 'k largest' because:",
   ["It's fast", "It maintains the top-k in O(n log k) without sorting everything", "It's simple", "Arrays can't"], 1,
   "'K smallest/largest' is the heap reflex — the Concepts."),
_q("DP's 'overlapping subproblems' means:",
   ["It's hard", "The same subproblems recur — memoize or tabulate instead of recomputing", "It's recursive", "It's slow"], 1,
   "Recognition: recomputation is the smell; the recurrence is the fix — the Concepts."),
_q("Redrilling the miss category (not the problem) works because:",
   ["It's faster", "Interviews test categories under new disguises — the instance never repeats", "Problems repeat", "It's trendy"], 1,
   "'I fix the category, not the instance' — the Hands-on procedure step 6."),
],
"tech-mock-interview-circuit--mock-sysdesign": [
_q("Asking for non-functional requirements before drawing is strong because:",
   ["It's traditional", "Scale, latency, and consistency constraints decide the architecture — drawing first designs the wrong system", "It's fast", "Diagrams are hard"], 1,
   "Scoping first proves you design the right system — the Concepts."),
_q("The estimation says storage is 50 GB for the whole dataset. The design implication is:",
   ["Shard immediately", "One database handles it — say so, and spend the complexity budget where the estimation points (IDs, cache)", "It's too big", "Use NoSQL"], 1,
   "Estimation aims complexity: trivial storage means the design's difficulty is elsewhere — the Worked estimation step 4."),
_q("Queues handle spikes while caches handle hot data because:",
   ["They're similar", "Queues defer work in time; caches skip work entirely — different bottlenecks, different tools", "It's trendy", "Both are fast"], 1,
   "Time-shifting vs work-avoidance: match the lever to the bottleneck — the Concepts."),
_q("Fan-out is the feed's core lesson because:",
   ["Feeds are popular", "Delivering one post to millions of followers is the scaling problem the design must solve", "It's trendy", "Databases"], 1,
   "Each classic teaches one lesson — the Concepts' classic lessons."),
_q("Drawing the API and data model together is correct because:",
   ["It's faster", "API shape constrains queries and data shape constrains the API — they're one decision, not two", "It's required", "Tools do it"], 1,
   "Designed together, they can't contradict each other — the Project brief's diagram standard."),
_q("The tradeoffs summary at the end of a design round should be:",
   ["Long", "Three sentences: what you optimized for, what you paid, when you'd choose differently — then invite the follow-up", "Skipped", "Apologetic"], 1,
   "Structure separates the senior answer from the recitation — the new card's three beats."),
],
"tech-mock-interview-circuit--mock-behavioral": [
_q("The STAR 'Result' should include:",
   ["Feelings", "A measurable outcome plus the lesson — evidence the behavior worked", "The team's revenue", "Praise"], 1,
   "Interviewers score evidence of behavior; the result is the evidence — the Concepts."),
_q("'Why this company?' fails when the answer:",
   ["Is short", "Could apply to any company — no specifics about them", "Mentions the product", "Is honest"], 1,
   "Interchangeable answers reveal no research; specifics prove interest — the Concepts."),
_q("Recording yourself works because:",
   ["It's trendy", "You hear what the interviewer hears — pacing and filler invisible from inside", "It's fun", "Phones exist"], 1,
   "'My first recording is always 40% too long' — the Hands-on procedure step 4."),
_q("A conflict story should emphasize:",
   ["Winning", "The disagreement handled professionally — what each side wanted, what decided it, what you did", "The other person", "Drama"], 1,
   "Disagreements are design reviews with feelings — the Concepts."),
_q("Asking the interviewer 'what does success look like in 6 months?' reveals:",
   ["Salary", "The role's reality — expectations that predict your actual experience", "Gossip", "Nothing"], 1,
   "You're interviewing them too — the Hands-on procedure step 6."),
_q("Practicing aloud (not just writing) matters because:",
   ["Writing is slow", "Aloud reveals pacing, filler, and rambling that silent rehearsal hides", "It's fun", "It's required"], 1,
   "Delivery is half the round; only aloud practice trains it — the Concepts."),
],
"tech-mock-interview-circuit--mock-domains": [
_q("Preparing 'one level deeper than the job post' works because:",
   ["It's trendy", "Interviewers probe past the bullet into mechanism and judgment — depth is where offers are won", "Posts are vague", "It's fast"], 1,
   "'I prepare the layer below the buzzword' — the Concepts."),
_q("The teach-back test exposes gaps because:",
   ["Teaching is hard", "Producing a clear explanation exposes what recognition hides — recognition ≠ recall ≠ teaching", "It's slow", "Juniors ask hard questions"], 1,
   "Each level demands deeper organization of knowledge — the Hands-on procedure step 3."),
_q("Your memory blanks on a deep-dive question. The strongest recovery is:",
   ["Bluff confidently", "State what you know precisely, name the boundary, reason from first principles aloud", "Go silent", "Change the subject"], 1,
   "Honesty + reasoning beats confident fabrication every time — the Concepts' blank-moment recovery."),
_q("Turning each JD bullet into a predicted question works because:",
   ["It's fast", "Interviewers probe what's on the JD — each requirement maps to questions you can pre-answer", "JDs are long", "It's required"], 1,
   "The JD is the interviewer's question list in disguise — the Hands-on procedure step 1."),
_q("Volunteering a technique's cost before being asked signals:",
   ["Weakness", "Senior judgment — you evaluate tradeoffs as a habit, not under interrogation", "Nervousness", "Speed"], 1,
   "Seniors volunteer the cost; juniors wait to be asked — the new card."),
_q("The gap log's purpose is to:",
   ["Feel bad", "Aim every study hour at real weakness — teach-back stumbles become study cards", "Impress", "Fill time"], 1,
   "Triage needs data; the log is the data — the Hands-on procedure step 6."),
],
"tech-mock-interview-circuit--mock-full-loop": [
_q("Running four rounds back-to-back (not spaced across days) trains:",
   ["Speed", "Stamina and context-switching — the loop day's actual athletic demands", "Memory", "Luck"], 1,
   "The simulation must reproduce the day's shape — the Concepts."),
_q("The debrief must happen within the hour because:",
   ["Schedules", "Fresh observations decay fast — what leaked is clearest right after the round", "Partners leave", "It's traditional"], 1,
   "Name the leak while you can still feel it — the Hands-on procedure step 5."),
_q("Targeting the floor (weakest round) over the ceiling is right because:",
   ["It's easier", "Offers are lost on weak rounds, not won on strong ones — the minimum decides", "Strong areas don't matter", "It's trendy"], 1,
   "Loops grade the weakest link — the Concepts' weakness-targeting week."),
_q("Between-round resets work because:",
   ["Rituals are magic", "They stop one round's mistakes from voting in the next — each round starts clean", "Water helps", "It's required"], 1,
   "'I carry the rubric, not the regret' — the new card."),
_q("The final checklist's 'explicit not-study list' exists because:",
   ["It's funny", "The taper protects performance — naming what you won't study prevents last-minute cramming noise", "Lists are fun", "Partners ask"], 1,
   "The last 48 hours are about the performer, not the material — the Concepts."),
_q("Trading interviewer roles with a partner teaches:",
   ["Patience", "What gradable answers look like from the grading side — you learn the rubric by using it", "Friendship", "Speed"], 1,
   "Grading teaches answer-craft faster than answering — the Hands-on procedure step 4."),
],
}
