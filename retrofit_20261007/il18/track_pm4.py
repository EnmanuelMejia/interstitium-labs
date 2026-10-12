# PM track, part 4: pm-case-rep, pm-mock
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["pm-interview-prep--pm-case-rep"] = {
"summary": (
"Welcome back to the PM track — I'm your instructor, and this is Module 5: Guided Product Case. "
"Reps on the canonical PM cases: teardowns, design questions, metrics drills, and prioritization — building "
"the aloud-thinking discipline the rounds score. By the end of this module you will tear down a product by "
"mechanism, design for a new user from their reality, improve an existing product with evidence, debug a "
"metric live, survive a prioritization showdown, walk a guesstimate sanely, and think aloud without rambling."
),
"concepts": """- **Product teardown** — What works, what fails users, why — by mechanism; then your first change and its expected effect.
- **New-user design** — Clarifying the user, their problem, and constraints — then the solution shaped to their reality, not yours.
- **Product improvement** — Diagnose with data, prioritize by impact/effort, propose the highest-leverage change — improvement with evidence.
- **Metrics deep-dive** — A metric moved: debug it live — instrumentation, segments, hypotheses, tests. The judgment round.
- **Prioritization showdown** — State the framework, apply it transparently, defend the tradeoff — prioritization as performance.
- **Guesstimate** — Assumptions first, round math, sanity check — the chain matters more than the number.
- **Thinking aloud** — Narrating structure without rambling: the discipline the rounds actually score.""" ,
"procedure": """Run the six-case circuit. Work each case aloud with a timer — 20 minutes each — then tighten.
1. Teardown: pick your favorite product and tear it down by mechanism — what works, what fails users, why — then name your first change and its expected effect.
2. New-user design: pick a user unlike you, clarify their problem and constraints, then shape the solution to their reality — narrate the whole chain aloud.
3. Improvement: pick an existing product, diagnose with data (real or reasoned), prioritize by impact/effort, propose the highest-leverage change with evidence.
4. Metrics deep-dive: take a moved metric and debug it live — instrumentation, segments, hypotheses, tests — narrate the judgment, not just the steps.
5. Prioritization showdown: given three competing asks, state your framework, apply it transparently, and defend the tradeoff aloud as the interviewer pushes back.
6. Guesstimate: assumptions first, round math, sanity check — narrate the chain; the number is the least important part.
7. Review each case: where did you ramble, where did the structure hold, and which case needs one more rep?""",
"brief": """Your interview prep brief: complete the six-case circuit and record the tightened versions.
The scenario. Your PM onsite runs sense, execution, and metrics rounds — the canonical cases. This circuit is the rehearsal.
Deliverables.
- Six timed (20-minute) case walkthroughs: teardown, new-user design, improvement, metrics deep-dive, prioritization showdown, guesstimate — narrated aloud.
- One tightened re-take of your weakest case, with the rambling cut.
- A one-page framework sheet: your default structure for each case type, in your own words.
Grading lens. Case rounds score aloud-thinking discipline: did you clarify before solving, apply frameworks transparently, defend tradeoffs under pushback, and show the reasoning chain — without rambling?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Case reps build the thinking discipline, not scripts — rehearse frameworks until they are automatic, then apply them to products you actually know. Recited answers fail the follow-up; structured thinking on real products survives it.""",
"quiz": [
("Teardowns critique by:", ["Taste", "Mechanism — what works, what fails, why", "Looks", "Hype"], 1, "The Concepts glossary defines the product teardown as what works, what fails users, why — by mechanism — then your first change and its expected effect."),
("New-user design starts with:", ["Features", "Clarifying the user, problem, and constraints", "Technology", "Copying competitors"], 1, "The Concepts note defines new-user design as clarifying the user, their problem, and constraints — the solution shaped to their reality, not yours."),
("The metrics deep-dive:", ["Reports numbers", "Debugs live: instrumentation, segments, hypotheses, tests", "Guesses", "Defers"], 1, "The Concepts glossary defines the metrics deep-dive as a moved metric debugged live — the judgment round."),
("The prioritization showdown:", ["Asserts", "Applies the framework transparently and defends the tradeoff", "Yields", "Votes"], 1, "The Concepts note defines the showdown as stating the framework, applying it transparently, defending the tradeoff — prioritization as performance."),
("Guesstimates:", ["Need precision", "Assumptions, round math, sanity check — the chain is graded", "Need speed", "Can be skipped"], 1, "The Concepts glossary defines the guesstimate as assumptions first, round math, sanity check — the chain matters more than the number."),
("Improvement cases require:", ["Opinions", "Diagnosis with data and the highest-leverage change with evidence", "More features", "Redesigns"], 1, "The Concepts note defines product improvement as diagnose with data, prioritize by impact/effort, propose the highest-leverage change — improvement with evidence."),
("Thinking aloud is scored on:", ["Volume", "Narrating structure without rambling", "Speed", "Confidence"], 1, "The Concepts glossary defines thinking aloud as narrating structure without rambling — the discipline the rounds actually score."),
("The tightened re-take targets:", ["The strongest case", "Your weakest case — with the rambling cut", "The easiest case", "A new case"], 1, "The Project brief requires one tightened re-take of your weakest case — iteration is where the reps pay off."),
("The framework sheet is in your own words because:", ["Plagiarism is bad", "Frameworks you can state yourself are frameworks you can apply under pressure", "It is shorter", "Interviewers like it"], 1, "The Project brief's framework sheet is in your own words — the Honesty note warns recited answers fail follow-ups; owned frameworks survive."),
("Each case is timed at 20 minutes because:", ["Arbitrary", "Case rounds run under pressure — rehearse under pressure", "Short is trendy", "Attention spans"], 1, "The Hands-on procedure times each case at 20 minutes — the aloud-thinking discipline is scored under realistic pressure."),
]}

RETRO["pm-interview-prep--pm-mock"] = {
"summary": (
"Welcome back to the PM track — I'm your instructor, and this is Module 6: PM Mock Circuit. "
"The full circuit, simulated: sense, execution, metrics, and behavioral rounds under real timing, with rubrics "
"and recording review that make each mock sharper than the last. By the end of this module you will simulate "
"the full PM loop back-to-back, hold timing discipline per round, rubric-score your product answers, review "
"your own recordings to make 'tight' measurable, and iterate between mocks."
),
"concepts": """- **PM loop** — Sense, execution, metrics, behavioral — the full circuit under real timing.
- **Full-loop simulation** — Back-to-back rounds with clocks — stamina and transitions practiced, not just content.
- **Timing discipline** — Knowing each round's shape and budget — where to spend minutes, when to land the plane.
- **Rubric scoring (product)** — Structure, user focus, tradeoff awareness, data grounding — the dimensions interviewers actually grade.
- **Recording review** — You hear the rambling you cannot feel — recordings make "tight" measurable.
- **Iteration between mocks** — Targeted fixes re-tested under pressure — each mock sharper than the last by design.""" ,
"procedure": """Run the full PM mock loop. Schedule four back-to-back rounds with a partner or record yourself; real clocks.
1. Round 1 — product sense (30 min): a design question and a teardown — structure audible, user first, assumptions stated.
2. Round 2 — execution (30 min): roadmap and prioritization under P0 pressure — ship judgment, tradeoffs explicit.
3. Round 3 — metrics (30 min): a moved metric debugged live plus a guesstimate — reasoning chains, not numbers.
4. Round 4 — behavioral (30 min): two stories in tight STAR plus your interviewer questions — preparation and honesty.
5. Rubric-score every round immediately: structure, user focus, tradeoff awareness, data grounding — score honestly.
6. Review the recordings: mark every ramble, every unstated assumption, every landed plane — make "tight" measurable.
7. Write the iteration plan: three targeted fixes for the next loop — each mock sharper than the last by design.
8. Run the loop again in one week and measure the delta on the rubric dimensions.""",
"brief": """Your interview prep brief: execute and document one full PM mock loop.
The scenario. Your PM onsite is two weeks out. The loop is your dress rehearsal across sense, execution, metrics, and behavioral.
Deliverables.
- Timed recordings (or partner notes) for all four rounds.
- Rubric scores for each round on the four dimensions: structure, user focus, tradeoff awareness, data grounding.
- A recording-review log: rambles marked, unstated assumptions flagged, planes landed or missed.
- An iteration plan: three targeted fixes, and next week's measured delta.
Grading lens. Mocks are rehearsal, not performance: the graded artifact is the iteration plan and the measured delta — did each mock change the next loop?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Recordings are honest mirrors — review them as a coach, not a critic, and score the rubric without flinching. Every story must be yours; every framework must be in your own words. Honest scoring is what makes the next loop better.""",
"quiz": [
("The PM loop is:", ["One round", "Sense, execution, metrics, behavioral — timed", "Trivia", "Case only"], 1, "The Concepts glossary defines the PM loop as sense, execution, metrics, behavioral — the full circuit under real timing."),
("Full-loop simulation builds:", ["Knowledge", "Stamina and transitions, not just content", "Fear", "Speed"], 1, "The Concepts note defines full-loop simulation as back-to-back rounds with clocks — stamina and transitions practiced, not just content."),
("Timing discipline means:", ["Rigidity", "Knowing each round's budget — where minutes go", "Looseness", "Ignoring the clock"], 1, "The Concepts glossary defines timing discipline as knowing each round's shape and budget — where to spend minutes, when to land the plane."),
("Rubric scoring grades:", ["Harshness", "Structure, user focus, tradeoff awareness, data grounding", "Optionally", "Subjectively"], 1, "The Concepts note defines product rubric scoring as structure, user focus, tradeoff awareness, data grounding — the dimensions interviewers actually grade."),
("Recordings reveal:", ["Nothing", "The rambling you cannot feel — 'tight' made measurable", "Flaws only", "Lies"], 1, "The Concepts glossary defines recording review as hearing the rambling you cannot feel — recordings make 'tight' measurable."),
("Landing the plane means:", ["Crashing", "Closing the answer on time with the conclusion stated", "Flying", "Stalling"], 1, "The Concepts glossary's timing discipline ends with 'when to land the plane' — closing on time with the conclusion stated."),
("The recording-review log marks:", ["Praise", "Rambles, unstated assumptions, landed or missed planes", "Outfits", "Backgrounds"], 1, "The procedure's step 6 marks every ramble, every unstated assumption, every landed plane — making 'tight' measurable."),
("Iteration between loops requires:", ["More loops", "Three targeted fixes, re-tested — each loop sharper by design", "Luck", "Rest"], 1, "The procedure's step 7 writes three targeted fixes, and the Concepts note defines iteration as targeted fixes re-tested under pressure."),
("The four rubric dimensions are scored:", ["Eventually", "Immediately after each round — while the memory is fresh", "Never", "By others"], 1, "The procedure's step 5 rubric-scores every round immediately — fresh memory makes honest scoring possible."),
("The mock loop's graded artifact is:", ["The performance", "The iteration plan and the measured delta", "The recordings", "The partner"], 1, "The Project brief's grading lens: mocks are rehearsal, not performance — the iteration plan and the measured delta are graded."),
]}
