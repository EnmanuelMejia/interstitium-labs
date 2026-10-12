# EM track, part 4: eng-strategy-vision, em-scenario-rep, em-mock
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["em-interview-prep--eng-strategy-vision"] = {
"summary": (
"Welcome back to the EM track — I'm your instructor, and this is Module 4: Engineering Strategy. "
"Beyond the sprint: the strategy layer EM interviews probe — technical vision, debt strategy, and platform "
"decisions tied to business outcomes, not just engineering taste. By the end of this module you will write a "
"technical vision, quantify and fund tech debt as a portfolio, make deliberate build-versus-buy platform bets, "
"read engineering health metrics, align engineering strategy with product strategy, and plan long-range "
"without fiction."
),
"concepts": """- **Technical vision** — A 2–3 year picture of where the systems go and why — direction the team can build toward.
- **Tech debt (strategic)** — Quantify it, prioritize against features, fund paydown — debt as a managed portfolio, not a complaint.
- **Platform bets** — Build-versus-buy decisions: differentiating IP you build, commodity you buy — weighed with total cost of ownership and team skill, deliberately.
- **Engineering health metrics** — Deploy frequency, change failure rate, review latency, on-call burden — the system's vital signs.
- **Strategy alignment** — Every technical bet traces to a product outcome — architecture in service of the business, not taste.
- **Long-range planning without fiction** — Direction with explicit uncertainty: bets, hedges, and review points — honest about what is unknown.
- **Total cost of ownership (TCO)** — The full price of a platform decision: build cost, operate cost, migrate cost, and the attention cost — weighed deliberately, not just the sticker price.""" ,
"procedure": """Run the strategy drill. Pick a system you know — real or simulated — and produce the strategy layer.
1. Write the technical vision: a 2–3 year picture of where this system goes and why — one page, direction a team can build toward.
2. List the top five tech debts: quantify each (what it costs in velocity, incidents, or risk), prioritize against feature work, and propose the funding ask.
3. Take one platform decision and run build-versus-buy deliberately: differentiating IP versus commodity, total cost of ownership, team skill — with numbers, not vibes.
4. Define the engineering health metrics you would watch: deploy frequency, change failure rate, review latency, on-call burden — and the thresholds that would worry you.
5. Trace one technical bet to a product outcome in writing: if you cannot draw the line to the business, the bet is taste, not strategy.
6. Write the long-range plan with explicit uncertainty: the bets, the hedges, and the review points where you revisit — honest about what is unknown.
7. Present the strategy aloud in ten minutes: vision, debt portfolio, platform bet, health metrics — as you would to a VP.""" ,
"brief": """Your interview prep brief: present the engineering strategy for a system under strain.
The scenario. You inherit a payments platform: deploy frequency is monthly, change failure rate is high, on-call is burning people out, and the product team wants three big features this year. The VP asks for your strategy.
Deliverables.
- A one-page technical vision: where the systems go in 2–3 years and why.
- A tech-debt portfolio: quantified, prioritized against the features, with a funding ask.
- A build-versus-buy recommendation for the platform's weakest layer — deliberate, with TCO.
- Engineering health metrics with the thresholds that would worry you.
- A long-range plan with explicit uncertainty: bets, hedges, review points.
Grading lens. Strategy rounds score business-grounded thinking: does every technical bet trace to a product outcome, is debt a managed portfolio rather than a complaint, and is uncertainty named instead of hidden?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Strategy answers must be grounded in systems you actually understand — interviewers probe the numbers behind your TCO and the reality behind your vision. Taste disguised as strategy fails the follow-up; honest uncertainty survives it.""",
"quiz": [
("A technical vision is:", ["A roadmap", "A 2–3 year picture of where systems go and why", "A wish list", "A spec"], 1, "The Concepts glossary defines the technical vision as a 2–3 year picture of where the systems go and why — direction the team can build toward."),
("Tech debt strategy:", ["Rewrite everything", "Quantify, prioritize, fund — a managed portfolio", "Ignore it", "Complain loudly"], 1, "The Concepts note defines strategic tech debt as quantified, prioritized against features, funded paydown — a managed portfolio, not a complaint."),
("Platform bets weigh:", ["Hype", "Differentiating IP vs commodity, TCO, team skill", "Trends", "Vendor dinners"], 1, "The Concepts glossary defines platform bets as build-versus-buy weighed with total cost of ownership and team skill — deliberately."),
("Engineering health metrics:", ["Vanity numbers", "Deploy frequency, failure rate, review latency, on-call burden", "Lines of code", "Velocity only"], 1, "The Concepts note lists the vital signs: deploy frequency, change failure rate, review latency, on-call burden."),
("Align engineering strategy with product by:", ["Ignoring product", "Tracing every technical bet to a product outcome", "More meetings", "More OKRs"], 1, "The Concepts glossary defines strategy alignment as every technical bet tracing to a product outcome — architecture in service of the business, not taste."),
("TCO includes:", ["The sticker price", "Build, operate, migrate, and attention costs — the full price", "Just licenses", "Just headcount"], 1, "The Concepts note defines total cost of ownership as the full price: build, operate, migrate, and attention costs — weighed deliberately."),
("Long-range planning without fiction requires:", ["Certainty", "Explicit uncertainty: bets, hedges, and review points", "Longer documents", "Guessing"], 1, "The Concepts glossary defines honest long-range planning as direction with explicit uncertainty — bets, hedges, review points."),
("In the drill, a technical bet that cannot be traced to a product outcome is:", ["Still fine", "Taste, not strategy — redraw or drop it", "Visionary", "A secret"], 1, "The procedure's step 5: if you cannot draw the line to the business, the bet is taste, not strategy."),
("The debt portfolio must be quantified in:", ["Feelings", "Velocity, incidents, or risk cost — so it can be prioritized against features", "Pages", "Complaints"], 1, "The procedure's step 2 quantifies each debt in velocity, incident, or risk cost — a managed portfolio needs numbers."),
("The strategy presentation is ten minutes to a VP because:", ["VPs are busy", "Strategy rounds score whether you can land vision, debt, bets, and health crisply — executive communication is part of strategy", "Ten is lucky", "Arbitrary"], 1, "The procedure's step 7 and the Project brief's grading lens: strategy must be communicated crisply to leadership — that is part of the skill."),
]}

RETRO["em-interview-prep--em-scenario-rep"] = {
"summary": (
"Welcome back to the EM track — I'm your instructor, and this is Module 5: Guided Leadership Scenarios. "
"Reps on the situations EM interviews are built from: underperformance, reorgs, missed dates, and disputes — "
"practiced until your answers have structure under pressure. By the end of this module you will handle the "
"underperforming senior, lead through a reorg you did not choose, surface a deadline miss with options, "
"mediate a cross-team dispute, plan scaling from 5 to 15, lead through an incident, and debrief your own decisions."
),
"concepts": """- **Leadership scenario** — The EM interview's unit of work: a realistic situation you reason through aloud — structure under pressure.
- **Underperformer playbook** — Private, specific feedback with support offered — documented; escalation to formal process only if the pattern holds.
- **Reorg leadership** — Leading through a reorg you did not choose: translate it for the team honestly, protect what matters, execute the transition well — leadership in constraint.
- **Deadline-miss surfacing** — Surface early with options and tradeoffs — managing up beats the surprise; renegotiate scope, date, or quality explicitly.
- **Dispute mediation** — Interests over positions, shared outcome reframed, decision recorded — mediation with a paper trail.
- **Scaling 5→15** — What breaks: communication paths, onboarding, informal process — deliberately add structure before the chaos.
- **Incident leadership** — Command structure, comms cadence, blameless follow-through — calm is a leadership output.
- **Decision debrief** — Reviewing your own calls afterward: what you decided, what you missed, what you would change — the habit that compounds judgment.""" ,
"procedure": """Run the seven-scenario circuit. Work each scenario aloud with a timer — 10 minutes each — then debrief.
1. The underperforming senior: script your first move — private, specific feedback with support offered, documented — and where the line to formal process sits.
2. The reorg you did not choose: write the honest translation you would give the team, name what you will protect, and list the transition's three execution risks.
3. The deadline the team will miss: draft the early surfacing message — options and tradeoffs, scope/date/quality explicit — and rehearse delivering it.
4. The cross-team dispute: map interests versus positions for both sides, reframe the shared outcome, and write the recorded decision.
5. Scaling from 5 to 15: list what breaks — communication paths, onboarding, informal process — and the structure you would add before the chaos.
6. Leading through an incident: define the command structure, the comms cadence, and the blameless follow-through you would run.
7. Debrief each scenario aloud in two minutes: what structure did you show, where did you hesitate, what would you change?
8. Write one paragraph on your own hardest real leadership decision — the debrief habit starts with your own history.""",
"brief": """Your interview prep brief: complete the seven-scenario circuit and document the debriefs.
The scenario. Your EM onsite is approaching and the leadership scenarios are the highest-weight rounds. This circuit is your rehearsal material.
Deliverables.
- Timed (10-minute) spoken walkthroughs for all seven scenarios: underperformer, reorg, missed deadline, dispute, scaling, incident, plus the written self-debrief.
- A one-paragraph written debrief of your own hardest real leadership decision.
- A structure checklist: for each scenario, the framework you used (interests/positions, scope/date/quality, command/comms/follow-through).
Grading lens. Scenario rounds score judgment under pressure: did you move early and privately on people problems, surface bad news with options, add structure before chaos — and show the debrief habit on your own decisions?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Scenario answers land when they describe decisions you actually faced — interviewers will ask what happened next and what you would do differently. The written debrief of your own hardest decision is the most valuable page in this module: write it truthfully.""",
"quiz": [
("Underperformer first move:", ["PIP", "Private specific feedback with support, documented", "Ignore it", "Transfer"], 1, "The Concepts glossary defines the underperformer playbook as private, specific feedback with support offered — documented; formal process only if the pattern holds."),
("Missed deadline:", ["Hide it", "Surface early with options and tradeoffs", "Work weekends silently", "Blame the team"], 1, "The Concepts note defines deadline-miss surfacing as early, with options and tradeoffs — managing up beats the surprise."),
("Reorg you didn't choose:", ["Resist", "Translate honestly, protect what matters, execute well", "Quit", "Complain"], 1, "The Concepts glossary defines reorg leadership as translating honestly, protecting what matters, executing the transition well — leadership in constraint."),
("Scaling 5→15 breaks:", ["Nothing", "Communication, onboarding, informal process — add structure deliberately", "Code", "Culture only"], 1, "The Concepts note defines scaling 5→15 as communication paths, onboarding, and informal process breaking — deliberately add structure before the chaos."),
("Cross-team dispute:", ["Escalate immediately", "Interests over positions, decision recorded", "Avoid", "Win"], 1, "The Concepts glossary defines dispute mediation as interests over positions, shared outcome reframed, decision recorded — mediation with a paper trail."),
("Incident leadership outputs:", ["Heroics", "Command structure, comms cadence, blameless follow-through — calm", "Silence", "Blame"], 1, "The Concepts note defines incident leadership as command structure, comms cadence, blameless follow-through — calm is a leadership output."),
("Each scenario is timed at 10 minutes because:", ["Speed impresses", "Scenario rounds are scored under pressure — rehearse under pressure", "Short is trendy", "Arbitrary"], 1, "The Hands-on procedure times each scenario at 10 minutes — structure under pressure is the graded skill."),
("The decision debrief habit matters because:", ["Nostalgia", "Reviewing your own calls compounds judgment over time", "Paperwork", "Interviews demand it"], 1, "The Concepts glossary defines the decision debrief as reviewing your own calls — what you decided, missed, and would change — the habit that compounds judgment."),
("The reorg translation must be honest because:", ["Honesty is nice", "The team will learn the truth anyway — trust is built by hearing it from you first", "HR requires it", "It is faster"], 1, "The procedure's step 2 writes the honest translation for the team — leadership in constraint depends on the team's trust."),
("The most valuable page in this module is:", ["The checklist", "The truthful written debrief of your own hardest real leadership decision", "The timer", "The script"], 1, "The procedure's step 8 and the Honesty note agree: the written debrief of your own hardest decision is the most valuable page — write it truthfully."),
]}

RETRO["em-interview-prep--em-mock"] = {
"summary": (
"Welcome back to the EM track — I'm your instructor, and this is Module 6: EM Mock Circuit. "
"The full circuit, simulated: leadership, delivery, and technical rounds with panels, timing, and rubrics that "
"convert each mock into a measurably better next attempt. By the end of this module you will run the complete "
"EM loop under realistic conditions, tell leadership behavioral stories in tight STAR form, survive management "
"deep-dives, perform in scenario rounds, and iterate between mocks with rubric self-review."
),
"concepts": """- **EM loop** — The standard onsite circuit: leadership, delivery, and technical rounds — the full circuit with panels and timing.
- **Leadership behavioral stories** — The story bank: people, delivery, conflict, failure — told in tight STAR with your role explicit.
- **STAR (tight)** — Situation, task, action, result — two minutes, your role explicit, no rambling.
- **Management deep-dive** — Extended probing on one story: decisions, alternatives, outcomes — depth under follow-up questions.
- **Scenario round** — Structured thinking aloud: clarify, options, tradeoffs, decision — the EM's interview performance.
- **Mock panels and timing** — Multiple interviewers, realistic clocks — pressure and dynamics practiced together.
- **Rubric self-review** — Scoring yourself against the round's bar after each mock — the feedback loop that compounds.
- **Iteration between mocks** — Targeted fixes, re-tested: each mock must change the next.""" ,
"procedure": """Run the full EM mock circuit. Schedule three back-to-back sessions with partners or record yourself; panels and real clocks.
1. Mock 1 — leadership behavioral (45 min): tell four stories from the bank — people, delivery, conflict, failure — in tight STAR, two minutes each.
2. Your partner runs a management deep-dive on one story: extended follow-ups on decisions, alternatives, outcomes — answer without new facts.
3. Self-review with the rubric: tight STAR? role explicit? real learning named? Score honestly.
4. Mock 2 — delivery and scenario (45 min): the slipping-quarter scenario and the incident scenario — structured thinking aloud: clarify, options, tradeoffs, decision.
5. Self-review: did you surface early, estimate honestly, and lead calmly? Score against the bar.
6. Mock 3 — technical and strategy (30 min): read a design critically, then present a technical vision in five minutes.
7. Write the iteration plan: three targeted fixes for the next circuit — each mock must change the next.
8. Run the circuit again in one week and measure the delta against this week's rubric scores.""",
"brief": """Your interview prep brief: execute and document one full EM mock circuit.
The scenario. Your EM onsite is two weeks out. The circuit is your dress rehearsal across leadership, delivery, and technical-strategy rounds.
Deliverables.
- Timed recordings (or partner notes) for all three mocks with panels where possible.
- Rubric self-reviews for each round, scored honestly against the round's bar.
- A story-bank check: people, delivery, conflict, failure — each in tight STAR with your role explicit.
- An iteration plan: three targeted fixes for the next circuit, and next week's delta.
Grading lens. Mocks are rehearsal, not performance: the graded artifact is the iteration plan and the measured improvement — did each mock change the next attempt?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Every story must be yours — interviewers will deep-dive any story you tell, and borrowed stories collapse under follow-up. Score yourself honestly: inflated rubrics rehearse your blind spots into the onsite.""",
"quiz": [
("The EM loop:", ["One chat", "Leadership, delivery, technical — panels and timing", "Trivia", "Coding only"], 1, "The Concepts glossary defines the EM loop as leadership, delivery, and technical rounds — the full circuit with panels and timing."),
("Deep-dives probe:", ["Memory", "One story under follow-up: decisions, alternatives, outcomes", "Speed", "Trivia"], 1, "The Concepts note defines the management deep-dive as extended probing on one story: decisions, alternatives, outcomes — depth under follow-up questions."),
("Scenario rounds show:", ["Knowledge", "Structured thinking aloud under ambiguity", "Charisma", "Speed"], 1, "The Concepts glossary defines the scenario round as structured thinking aloud: clarify, options, tradeoffs, decision — the EM's interview performance."),
("Rubric self-review:", ["Is harsh by design", "Scores you against the bar — feedback that compounds", "Is optional", "Replaces mocks"], 1, "The Concepts note defines rubric self-review as scoring yourself against the round's bar after each mock — the feedback loop that compounds."),
("Iterate because:", ["Ritual", "Each mock must change the next", "Coaches demand it", "Fun"], 1, "The Concepts glossary is explicit: targeted fixes, re-tested — each mock must change the next."),
("Tight STAR means:", ["A long story", "Two minutes, your role explicit, no rambling", "A scripted answer", "Vagueness"], 1, "The Concepts note defines tight STAR as situation, task, action, result — two minutes, your role explicit, no rambling."),
("The deep-dive forbids new facts because:", ["Rules are rules", "The story must hold as told — invented details collapse under follow-up", "Time is short", "Partners dislike it"], 1, "The procedure's step 2 runs the deep-dive with 'answer without new facts' — and the Honesty note warns borrowed stories collapse under follow-up."),
("Panels are included because:", ["Intimidation", "Multiple interviewers and dynamics are part of the real loop — practice them together", "Tradition", "Efficiency"], 1, "The Concepts glossary defines mock panels and timing as multiple interviewers with realistic clocks — pressure and dynamics practiced together."),
("The iteration plan's fixes must be:", ["Vague", "Targeted — three specific fixes, re-tested next week", "Ambitious", "Secret"], 1, "The procedure's step 7 requires three targeted fixes, and step 8 measures the delta next week — targeted fixes, re-tested."),
("Mock scores are:", ["Verdicts", "Practice instruments — honest scoring makes iteration work", "Permanent records", "Public"], 1, "The Honesty note frames mocks as rehearsal and rubric scores as practice instruments — honest scoring is what makes the iteration plan work."),
]}
