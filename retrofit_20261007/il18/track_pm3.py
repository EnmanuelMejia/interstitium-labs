# PM track, part 3: execution-pm, pm-behavioral
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["pm-interview-prep--execution-pm"] = {
"summary": (
"Welcome back to the PM track — I'm your instructor, and this is Module 3: Execution. "
"Execution rounds test whether you can ship: scoping with engineers, prioritizing under constraints, and "
"turning launches into iteration loops instead of one-shot bets. By the end of this module you will roadmap "
"under real constraints, prioritize when everything is P0, scope tradeoffs with engineering, plan launches "
"with verified readiness, run post-launch iteration loops, say no with a rationale, and manage stakeholders "
"through delivery."
),
"concepts": """- **Roadmapping under constraints** — Sequencing bets with honest capacity, dependencies, and uncertainty — the roadmap as a communication tool, not a promise.
- **Prioritization under P0 pressure** — Impact versus effort with assumptions stated — plus the explicit tradeoff conversation with stakeholders when everything is P0.
- **Scoping with engineering** — Tradeoffs together: scope, date, quality — the PM brings the why, engineering brings the how, decisions are shared.
- **Launch readiness** — The checklist: owners, rollback, comms, support, monitoring — readiness verified before users arrive.
- **Post-launch iteration loops** — Measure, learn, iterate — launches are hypotheses with a plan, not one-shot bets.
- **Saying no (PM)** — No, because [strategy/metric tradeoff], and here is what we are doing instead — no without rationale is just obstruction.
- **Stakeholder management through delivery** — Keeping stakeholders aligned as reality moves: early flags, options, and the tradeoff made explicit.""" ,
"procedure": """Run the execution drill on a feature you know — real or simulated. Work the full ship cycle on paper.
1. Write the roadmap for the next quarter: sequence three bets with honest capacity, named dependencies, and the uncertainty stated — a communication tool, not a promise.
2. Run the everything-is-P0 triage: score the three bets on impact versus effort with assumptions stated, rank them, and write the tradeoff conversation you would have with stakeholders.
3. Scope one bet with engineering: write the scope/date/quality tradeoff as a shared decision — the PM's why, engineering's how, the decision recorded.
4. Build the launch checklist: owners, rollback, comms, support, monitoring — and mark each verified or not-yet; unverified items are launch blockers.
5. Design the post-launch iteration loop: the metrics you will watch, the hypotheses you will test, the cadence — the launch as a hypothesis with a plan.
6. Write a no with a rationale for one plausible request: the strategy or metric tradeoff, and what you are doing instead.
7. Draft the stakeholder update for a two-week slip: early, with options, the tradeoff explicit — managing stakeholders through delivery.
8. Debrief aloud in five minutes: where did constraint change a decision, and where did the loop replace a one-shot bet?""",
"brief": """Your interview prep brief: ship a feature on paper, end to end.
The scenario. You own a checkout-redesign feature with a fixed quarter, two engineers, a dependency on the payments API, and three stakeholders who each call their ask P0.
Deliverables.
- A quarterly roadmap: three sequenced bets, honest capacity, named dependencies, stated uncertainty.
- A P0 triage: impact versus effort with stated assumptions, the ranking, and the stakeholder tradeoff conversation.
- A shared scoping decision with engineering: scope/date/quality, recorded.
- A verified launch checklist and a post-launch iteration loop with metrics and hypotheses.
- A no with rationale, and a stakeholder update for a two-week slip — early, with options.
Grading lens. Execution rounds score shipping judgment: did you sequence honestly, share scoping decisions, verify readiness, and turn the launch into a loop instead of a bet?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Execution answers must describe ships you actually worked on — the constraints were real, the tradeoffs were real, the slips were real. Interviewers ask what broke and what you learned; answer from the launch you lived, not the one you wish you had.""",
"quiz": [
("Roadmaps are:", ["Promises", "Communication tools under real constraints", "Contracts", "Fiction"], 1, "The Concepts glossary defines roadmapping as sequencing bets with honest capacity, dependencies, and uncertainty — a communication tool, not a promise."),
("When everything is P0:", ["Do it all", "Impact/effort with stated assumptions plus an explicit tradeoff conversation", "Panic", "Delegate"], 1, "The Concepts note defines P0-pressure prioritization as impact versus effort with stated assumptions — plus the explicit tradeoff conversation with stakeholders."),
("Scoping with engineering is:", ["The PM deciding", "Shared: the PM brings the why, engineering brings the how", "Engineering deciding", "A fight"], 1, "The Concepts glossary defines scoping with engineering as tradeoffs together — decisions shared, the why from the PM, the how from engineering."),
("Launch readiness means:", ["Hope", "A verified checklist: owners, rollback, comms, support", "A date", "A press release"], 1, "The Concepts note defines launch readiness as the checklist — owners, rollback, comms, support, monitoring — verified before users arrive."),
("Say no with:", ["Silence", "A rationale and the alternative", "Authority", "Delay"], 1, "The Concepts glossary defines the PM's no as: no, because [strategy/metric tradeoff], and here is what we are doing instead."),
("Post-launch iteration loops treat launches as:", ["One-shot bets", "Hypotheses with a plan: measure, learn, iterate", "Victories", "Endings"], 1, "The Concepts note defines post-launch loops as measure, learn, iterate — launches are hypotheses with a plan, not one-shot bets."),
("In the drill, unverified checklist items are:", ["Fine", "Launch blockers — readiness must be verified", "Optional", "Someone else's problem"], 1, "The procedure's step 4 marks each checklist item verified or not-yet — unverified items are launch blockers."),
("The roadmap must state uncertainty because:", ["It looks honest", "The roadmap is a communication tool — stated uncertainty keeps it honest under change", "It is trendy", "Lawyers require it"], 1, "The procedure's step 1 sequences bets with the uncertainty stated — a communication tool, not a promise."),
("Stakeholder management through delivery requires:", ["Good news", "Early flags, options, and the tradeoff made explicit as reality moves", "Silence", "More meetings"], 1, "The Concepts glossary defines stakeholder management through delivery as early flags, options, and explicit tradeoffs as reality moves."),
("The ship-on-paper brief grades you on:", ["Speed", "Shipping judgment: honest sequencing, shared scoping, verified readiness, launch-as-loop", "Slide design", "Optimism"], 1, "The Project brief's grading lens: shipping judgment — honest sequencing, shared scoping decisions, verified readiness, launch as a loop."),
]}

RETRO["pm-interview-prep--pm-behavioral"] = {
"summary": (
"Welcome back to the PM track — I'm your instructor, and this is Module 4: Behavioral for PMs. "
"Behavioral rounds are won in preparation: a story bank covering leadership, conflict, failure, and ambiguity — "
"each told in tight STAR form with your actual role and learning explicit. By the end of this module you will "
"bank leadership, conflict, failure, and ambiguity stories, tell them in tight STAR, calibrate the seniority "
"your stories show, and ask your interviewers questions about their real problems."
),
"concepts": """- **Story bank** — Prepared stories covering the rounds' greatest hits: leadership, conflict, failure, ambiguity.
- **Leadership story** — Your influence on the outcome, the hard call, what you would repeat — ownership audible.
- **Conflict story** — Disagreement, your approach, resolution, relationship preserved — conflict handled, not won.
- **Failure story** — What broke, your part in it, what changed after — real learning, not humblebrag.
- **Ambiguity story** — No map, no precedent: how you created structure and moved forward — comfort with the unknown.
- **Tight STAR** — Situation, task, action, result — two minutes, your role explicit, no rambling.
- **Interviewer questions** — Ask about their hard problems and success measures — curiosity about real work, not perks.
- **Seniority calibration** — Matching your stories' scope and ownership to the level you are interviewing for.""" ,
"procedure": """Build your story bank. Write each story, then rehearse it aloud with a timer — two minutes each.
1. Write the leadership story: your influence on the outcome, the hard call you made, what you would repeat — ownership audible.
2. Write the conflict story: the disagreement, your approach, the resolution, the relationship preserved — handled, not won.
3. Write the failure story: what broke, your part in it, what changed after — real learning, not humblebrag.
4. Write the ambiguity story: no map, no precedent — how you created structure and moved forward.
5. Tighten each to STAR: situation, task, action, result — two minutes, your role explicit, no rambling.
6. Calibrate seniority: for the level you are targeting, does each story show the right scope and ownership? Adjust one story up or down.
7. Write three questions for your interviewers: their hard problems, their success measures, what a great PM does there in year one.
8. Rehearse all four stories back-to-back: 8 minutes, no notes — the bank under pressure.""",
"brief": """Your interview prep brief: produce the interview-ready story bank.
The scenario. Your PM loop's behavioral rounds will ask for leadership, conflict, failure, and ambiguity — the greatest hits. Walk in with the bank built.
Deliverables.
- Four written stories (leadership, conflict, failure, ambiguity), each in tight STAR — two minutes, your role explicit.
- A seniority calibration note: the level targeted and how each story's scope matches it.
- Three interviewer questions: their hard problems, their success measures, the year-one picture.
- A timed back-to-back rehearsal recording: all four stories, eight minutes, no notes.
Grading lens. Behavioral rounds score preparation and honesty: is the structure tight, is your role explicit, is the learning real — and are the stories yours?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Behavioral stories must be your own — your role, your decisions, your learning. Interviewers deep-dive every story; borrowed or inflated stories collapse under follow-up, and the damage is worse than a weak answer. Tell the truth, tightly.""",
"quiz": [
("The story bank covers:", ["Wins only", "Leadership, conflict, failure, ambiguity", "Jokes", "Titles"], 1, "The Concepts glossary defines the story bank as prepared stories covering the rounds' greatest hits: leadership, conflict, failure, ambiguity."),
("Tight STAR means:", ["A long story", "Two minutes, your role explicit, no rambling", "A scripted answer", "Vagueness"], 1, "The Concepts note defines tight STAR as situation, task, action, result — two minutes, your role explicit, no rambling."),
("Failure stories need:", ["Excuses", "Your part, what broke, what changed", "Blame", "Humor"], 1, "The Concepts glossary defines the failure story as what broke, your part in it, what changed after — real learning, not humblebrag."),
("Ambiguity stories show:", ["Luck", "Creating structure with no map", "Chaos", "Delegation"], 1, "The Concepts note defines the ambiguity story as no map, no precedent — how you created structure and moved forward."),
("Ask interviewers about:", ["Perks", "Their hard problems and success measures", "Salary bands", "Office hours"], 1, "The Concepts glossary defines interviewer questions as curiosity about real work: their hard problems and success measures."),
("A conflict story is scored on:", ["Winning", "Disagreement, approach, resolution, relationship preserved", "Drama", "Length"], 1, "The Concepts note defines the conflict story as conflict handled, not won — resolution with the relationship preserved."),
("Seniority calibration adjusts:", ["The font", "Each story's scope and ownership to the level targeted", "The order", "The jokes"], 1, "The Concepts glossary defines seniority calibration as matching your stories' scope and ownership to the level you are interviewing for."),
("The eight-minute rehearsal runs with no notes because:", ["Notes are banned", "Behavioral rounds happen from memory — the bank must work under pressure", "Paper is scarce", "Tradition"], 1, "The procedure's step 8 rehearses all four stories back-to-back with no notes — the bank under pressure."),
("A leadership story must make audible:", ["The team size", "Your influence on the outcome, the hard call, what you would repeat", "The office", "The timeline"], 1, "The Concepts glossary defines the leadership story as your influence on the outcome, the hard call, what you would repeat — ownership audible."),
("The behavioral rounds score:", ["Performance", "Preparation and honesty: tight structure, explicit role, real learning, your own stories", "Charisma", "Length"], 1, "The Project brief's grading lens: preparation and honesty — tight structure, explicit role, real learning, and stories that are yours."),
]}
