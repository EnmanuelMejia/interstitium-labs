# TPM track, part 4: tpm-case-rep, tpm-mock
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["tpm-interview-prep--tpm-case-rep"] = {
"summary": (
"Welcome back to the TPM track — I'm your instructor, and this is Module 5: Guided Program Case. "
"This is reps on realistic program cases: you plan the launch, rescue the red program, and write the brief — "
"building the structured thinking the case rounds score. By the end of this module you will walk through a "
"cross-team launch case live, diagnose and turn around a failing program, sequence a platform migration with "
"hard dependencies, read an incident postmortem as a TPM, and write the one-page program brief that forces clarity."
),
"concepts": """- **Program case** — The TPM case round's unit of work: a program scenario you structure aloud — scope, milestones, dependencies, risks, comms — narrated live.
- **Launch-case walkthrough** — Narrating the program design artifact live: scope, dependency map, risks, comms cadence — structured thinking, audible.
- **Turnaround case** — The failing-program scenario: diagnose first (red signals, unowned dependencies, unclear exit), then re-scope, re-plan, and re-communicate with owners named.
- **Platform-migration case** — Treated as a program, not a deploy: hard dependencies sequenced, rollback planned, consumers migrated with support.
- **Postmortem reading (TPM)** — Timeline, root causes, action items with owners — and whether the follow-through actually happened; follow-through is the signal.
- **Stakeholder-map exercise** — Who is impacted, who decides, who needs informing — mapped before the program needs them.
- **One-page program brief** — Problem, scope, milestones, risks, asks — the whole program on one page; one page exposes fuzzy thinking.""" ,
"procedure": """Run the three-case circuit. Work each case aloud with a timer — 30 minutes per case — and write the one-pager after.
1. Case 1 — cross-team launch: given a mandate and four teams, scope aloud (in/out/deferred), name five milestones, and draw the dependency map with owners.
2. Narrate your program-design artifact for the launch as the interviewer would hear it: two minutes, no rambling, structure audible.
3. Case 2 — failing program: you inherit a red program. Diagnose aloud first: name the red signals, the unowned dependencies, the unclear exit conditions — before proposing anything.
4. Re-scope the failing program: what changes, what stops, who owns the new plan — then write the re-communication you would send the stakeholders.
5. Case 3 — platform migration: sequence the hard dependencies, plan the rollback, and name the consumer-support plan — treat it as a program, not a deploy.
6. Read a real incident postmortem (public ones are fine) as a TPM: extract the timeline, the action items with owners, and judge whether the follow-through happened.
7. Write the one-page program brief for the launch case: problem, scope, milestones, risks, asks — one page, no overflow.
8. Review each case aloud in two minutes: what structure did you show, where did you ramble, what would you change?""",
"brief": """Your interview prep brief: complete the three-case circuit and produce a portfolio one-pager.
The scenario. You are preparing for a TPM onsite with a program-design round, an execution/behavioral round, and a technical round. The circuit rehearses all three against realistic material.
Deliverables.
- A timed (30-minute) cross-team launch case walkthrough, narrated aloud and recorded.
- A failing-program turnaround: written diagnosis (red signals, unowned dependencies, unclear exit) plus the re-scope and stakeholder re-communication.
- A platform-migration plan: sequenced hard dependencies, rollback, consumer support.
- A postmortem read: timeline, action items with owners, and a verdict on follow-through.
- The one-page program brief for the launch case.
Grading lens. Case rounds score structured thinking made audible: did you scope before planning, diagnose before prescribing, treat the migration as a program, and land the one-pager without overflow?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Case reps build structure, not scripts: rehearse the thinking framework until it is automatic, but answer from your own real programs when the round is real. Memorized answers fail the follow-up questions; structured thinking survives them.""",
"quiz": [
("A launch-case walkthrough shows:", ["Charisma", "Program design narrated live: scope, dependencies, risks, comms", "Luck", "Speed"], 1, "The Concepts note defines the launch-case walkthrough as narrating the program design artifact live — structured thinking, audible."),
("A turnaround case starts with:", ["A new plan", "Diagnosing red signals and unowned dependencies", "Blame", "More people"], 1, "The Concepts glossary is explicit: diagnose first — red signals, unowned dependencies, unclear exit — then re-scope, re-plan, re-communicate."),
("Migration cases hinge on:", ["Speed", "Sequenced dependencies, rollback, and consumer support", "Tools", "Budget"], 1, "The Concepts note defines the migration case as a program, not a deploy: hard dependencies sequenced, rollback planned, consumers migrated with support."),
("Reading postmortems as a TPM focuses on:", ["Blame", "Whether action items with owners actually happened", "Length", "Drama"], 1, "The Concepts glossary defines TPM postmortem reading as timeline, root causes, action items with owners — and follow-through is the signal."),
("The one-page brief forces:", ["Brevity for its own sake", "Clarity: problem, scope, milestones, risks, asks — fuzzy thinking exposed", "Approval", "Design"], 1, "The Concepts note defines the one-pager as the whole program on one page, forcing clarity — one page exposes fuzzy thinking."),
("In the turnaround case, proposing a new plan comes:", ["First", "After diagnosis — diagnose before prescribing", "Never", "After blaming"], 1, "The Hands-on procedure's steps 3–4: diagnose aloud first, then re-scope — diagnose before prescribing is the graded discipline."),
("The migration case is treated as a program because:", ["It sounds bigger", "It has sequenced dependencies, a rollback, and consumers needing support — not just a deploy button", "Deployments are scary", "Tools demand it"], 1, "The procedure's step 5 and the Concepts note agree: a migration has program-shaped work — sequencing, rollback, consumer support."),
("The postmortem read's verdict on follow-through matters because:", ["Paperwork is fun", "Action items that never happened are the signal of a weak reliability culture", "Length impresses", "Drama sells"], 1, "The Concepts glossary ends the postmortem definition with 'whether the follow-through actually happened' — follow-through is the signal."),
("Each case in the circuit is timed at 30 minutes because:", ["Speed impresses", "Case rounds are scored under pressure — rehearse under pressure", "Short is trendy", "Arbitrary"], 1, "The Hands-on procedure times each case at 30 minutes — the case rounds are scored under pressure, so rehearse under pressure."),
("The circuit's final review asks what you would change because:", ["Perfectionism", "Iteration between reps is how structure becomes automatic without becoming scripted", "Self-criticism impresses", "Forms require it"], 1, "The procedure's step 8 reviews each case for structure, rambling, and changes — and the Honesty note warns that structure, not scripts, survives follow-ups."),
]}

RETRO["tpm-interview-prep--tpm-mock"] = {
"summary": (
"Welcome back to the TPM track — I'm your instructor, and this is Module 6: TPM Mock Circuit. "
"The full circuit, simulated: timed mocks across program design, technical depth, and behavioral rounds, with "
"rubrics that turn each mock into a sharper next attempt. By the end of this module you will run the complete "
"TPM loop under realistic timing, tell program deep-dive stories with structure, prepare for the technical "
"round's design literacy, bank behavioral stories, and iterate between mocks with rubric self-review."
),
"concepts": """- **TPM loop** — The standard onsite circuit: program design, technical depth, and behavioral rounds — the full circuit, timed.
- **Program deep-dive stories** — Two or three programs told with structure: ambiguity faced, design produced, execution challenges, outcome, learning.
- **Technical round (TPM)** — Probes design literacy and tradeoff questioning — not coding, but genuine technical judgment.
- **TPM behavioral stories** — The role's greatest hits: influence without authority, conflict resolution, failed programs, stakeholder wins.
- **Mock structure and timing** — Realistic conditions per round with a clock — pressure practiced, not first felt on the day.
- **Self-review rubrics** — Scoring your own answers against the round's bar — turning each mock into a sharper next attempt.
- **Iteration between mocks** — Feedback that changes the next round; mocks without iteration are anxiety rehearsal.""" ,
"procedure": """Run the full TPM mock circuit. Schedule three back-to-back sessions with a partner or record yourself; real clocks, real conditions.
1. Mock 1 — program design (45 min): given an ambiguous mandate, scope, milestone, map, and risk aloud while the clock runs; no pausing.
2. Immediately self-review with the rubric: structure audible? dependencies owned? exit conditions real? Score yourself honestly.
3. Mock 2 — technical depth (30 min): your partner hands you a design doc or system description; read it critically, flag integration risks, and ask your sharp questions aloud.
4. Self-review: did you find the real risks, speak SLOs, ask tradeoff questions — and mark your deferral boundary honestly?
5. Mock 3 — behavioral (30 min): tell two deep-dive stories (ambiguity faced, design, execution, outcome, learning) and one influence-without-authority story; your partner asks follow-ups.
6. Self-review: tight structure? your role explicit? real learning named? Score against the bar.
7. Write the iteration plan: the three specific changes you will make before the next circuit — mocks without iteration are anxiety rehearsal.
8. Run the circuit again in one week and measure the delta against this week's rubric scores.""",
"brief": """Your interview prep brief: execute and document one full TPM mock circuit.
The scenario. Your TPM onsite is two weeks out. The circuit is your dress rehearsal: three rounds, realistic timing, honest scoring.
Deliverables.
- Timed recordings (or partner notes) for all three rounds: program design, technical depth, behavioral.
- Rubric self-reviews for each round, scored honestly against the round's bar.
- A story bank check: two or three program deep-dives and the behavioral greatest hits — each with structure and your role explicit.
- An iteration plan: three specific changes for the next circuit.
Grading lens. Mocks are rehearsal, not performance: the graded artifact is the iteration plan and the measured delta next week — did each mock change the next attempt?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Mock scores are practice instruments, not verdicts — and every story you tell must be yours. The iteration plan only works on honest scoring: inflate the rubric and you rehearse your blind spots into the onsite.""",
"quiz": [
("The TPM loop is:", ["One round", "Program, technical, behavioral — timed", "Trivia", "Whiteboard only"], 1, "The Concepts note defines the TPM loop as program design, technical depth, and behavioral rounds — the full circuit, timed."),
("Deep-dive stories need:", ["Length", "Structure: ambiguity, design, execution, outcome, learning", "Jargon", "Humor"], 1, "The Concepts glossary defines program deep-dive stories as two or three programs told with structure: ambiguity faced, design produced, execution challenges, outcome, learning."),
("Self-review rubrics:", ["Are optional", "Turn each mock into a sharper next attempt", "Are harsh by design", "Replace coaches"], 1, "The Concepts note defines self-review rubrics as scoring your own answers against the round's bar — turning each mock into a sharper next attempt."),
("Iterate between mocks because:", ["It is fun", "Mocks without iteration are anxiety rehearsal", "Coaches demand it", "It is a habit"], 1, "The Concepts glossary is blunt: feedback must change the next round — mocks without iteration are anxiety rehearsal."),
("Mock timing:", ["Is irrelevant", "Pressure practiced, not first felt on the day", "Slows you down", "Is cruel"], 1, "The Concepts note defines mock structure and timing as realistic conditions with a clock — pressure practiced, not first felt on the day."),
("The behavioral mock's follow-up questions test:", ["Memory", "Whether the story holds under probing — real depth vs memorized answers", "Speed", "Trivia"], 1, "The procedure's step 5 has the partner ask follow-ups — and the Honesty note warns memorized answers fail follow-up questions."),
("The iteration plan must name:", ["Vibes", "Three specific changes before the next circuit", "More mocks", "Better luck"], 1, "The Hands-on procedure's step 7 requires three specific changes — the Project brief grades the iteration plan, not the performance."),
("The circuit is re-run in one week to:", ["Fill time", "Measure the delta against this week's rubric scores", "Entertain partners", "Avoid work"], 1, "The procedure's step 8 re-runs the circuit and measures the delta — improvement you can score is improvement that happened."),
("Deep-dive stories must keep your role explicit because:", ["Ego", "Interviewers score your judgment — 'we' hides whose decisions they were", "Length", "Drama"], 1, "The procedure's self-review asks: your role explicit? — the graded discipline from the story-bank definition."),
("Mock scores are:", ["Verdicts", "Practice instruments — honest scoring makes the iteration plan work", "Permanent", "Shared publicly"], 1, "The Honesty note states mock scores are practice instruments, not verdicts — and honest scoring is what makes iteration work."),
]}
