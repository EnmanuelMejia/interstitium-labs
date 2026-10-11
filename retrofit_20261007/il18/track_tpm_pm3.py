# Technical PM track, part 3: tech-pm-case, tech-pm-system-design, tech-pm-mock
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["technical-pm-interview-prep--tech-pm-case"] = {
"summary": (
"Welcome back to the Technical PM track — I'm your instructor, and this is Module 4: Guided Technical Case. "
"Reps on technical product cases: API design, build-versus-buy, and platform tradeoffs — where product "
"judgment has to survive contact with architecture. By the end of this module you will design an API from "
"consumers outward, reason through technical tradeoffs explicitly, run build-versus-buy with numbers, shape a "
"platform roadmap, decide reliability tradeoffs with SLOs, and write and defend the technical one-pager."
),
"concepts": """- **Technical case** — The technical PM's case round: product judgment under architectural constraint — API design, tradeoffs, build-versus-buy, platforms.
- **API-design case** — Consumers and use cases first — then resources, methods, versioning, auth, limits, and the deprecation promise.
- **Technical tradeoff** — Options, costs (latency, complexity, money), reversibility — decide with the tradeoff explicit and recorded.
- **Build versus buy** — Differentiating IP versus commodity, total cost of ownership, lock-in, team skill — deliberately, with numbers.
- **Platform roadmap** — Shaped by developer adoption, ecosystem leverage, and the boring reliability work — platforms compound or decay.
- **Reliability tradeoff** — Cost of downtime versus cost of reliability — SLOs make the tradeoff discussable instead of emotional.
- **Technical one-pager** — Problem, options, recommendation, tradeoffs, open questions — one page that a busy engineer respects.
- **Decision defense** — Defending a decision with data and architecture: the recommendation, the evidence, the recorded tradeoff.""" ,
"procedure": """Run the technical-case circuit. Work each case aloud with a timer — 25 minutes each — then write the one-pager.
1. API-design case: consumers and use cases first, then resources, methods, versioning, auth, limits, deprecation promise — narrate the design.
2. Technical-tradeoff case: lay out the options with costs (latency, complexity, money) and reversibility — decide with the tradeoff explicit and recorded.
3. Build-versus-buy case: differentiating IP versus commodity, total cost of ownership, lock-in, team skill — deliberately, with numbers on paper.
4. Platform-roadmap case: sequence by developer adoption, ecosystem leverage, and the boring reliability work — platforms compound or decay.
5. Reliability-tradeoff case: cost of downtime versus cost of reliability — write the SLO that makes the tradeoff discussable instead of emotional.
6. Write the technical one-pager for your hardest case: problem, options, recommendation, tradeoffs, open questions — one page a busy engineer respects.
7. Defend the one-pager aloud in five minutes: the recommendation, the data, the architecture, the recorded tradeoff — as the interviewer pushes back.""",
"brief": """Your interview prep brief: complete the technical-case circuit and produce the defended one-pager.
The scenario. Your technical PM onsite runs technical cases where product judgment meets architecture. This circuit is the rehearsal.
Deliverables.
- Five timed (25-minute) technical case walkthroughs: API design, technical tradeoff, build-versus-buy, platform roadmap, reliability tradeoff — narrated aloud.
- A technical one-pager for the hardest case: problem, options, recommendation, tradeoffs, open questions.
- A five-minute recorded defense of the one-pager under pushback.
Grading lens. Technical cases score judgment with architecture: did you start from consumers, make tradeoffs explicit and recorded, use numbers for build-versus-buy, and defend the recommendation with data — without bluffing?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Technical cases must be argued from systems you understand — interviewers will test the numbers behind your TCO and the reality behind your architecture claims. "I would need to validate this with engineering" is honest strength, not weakness.""",
"quiz": [
("API design starts with:", ["Endpoints", "Consumers and use cases", "Code", "Documentation"], 1, "The Concepts glossary defines the API-design case as consumers and use cases first — then resources, methods, versioning, auth, limits, and the deprecation promise."),
("Technical tradeoffs are decided with:", ["Avoidance", "Options, costs, reversibility — explicit and recorded", "Guessing", "Deferral"], 1, "The Concepts note defines the technical tradeoff as options, costs (latency, complexity, money), reversibility — decided with the tradeoff explicit and recorded."),
("Build versus buy:", ["Always build", "Differentiating: build; commodity: buy — TCO weighed", "Always buy", "Cheapest wins"], 1, "The Concepts glossary defines build-versus-buy as differentiating IP versus commodity, total cost of ownership, lock-in, team skill — deliberately, with numbers."),
("The reliability tradeoff:", ["Maximize always", "Cost of downtime versus cost of reliability — SLOs make it discussable", "Ignore it", "Hope"], 1, "The Concepts note defines the reliability tradeoff as cost of downtime versus cost of reliability — SLOs make it discussable instead of emotional."),
("One-pagers contain:", ["Everything", "Problem, options, recommendation, tradeoffs, open questions — one page", "Slides", "Nothing"], 1, "The Concepts glossary defines the technical one-pager as problem, options, recommendation, tradeoffs, open questions — one page a busy engineer respects."),
("Platform roadmaps are shaped by:", ["Hype", "Developer adoption, ecosystem leverage, and the boring reliability work", "Vendors", "Trends"], 1, "The Concepts note defines the platform roadmap as shaped by developer adoption, ecosystem leverage, and the boring reliability work — platforms compound or decay."),
("Defending a decision uses:", ["Volume", "Data and architecture: the recommendation, the evidence, the recorded tradeoff", "Authority", "Charm"], 1, "The Concepts glossary defines decision defense as the recommendation, the evidence, the recorded tradeoff — with data and architecture."),
("Reversibility matters in tradeoffs because:", ["It sounds smart", "Reversible decisions can be made fast and corrected; irreversible ones need care — the distinction changes the decision", "It is trendy", "Interviewers like it"], 1, "The Concepts note lists reversibility alongside options and costs — it changes how the tradeoff is decided."),
("The one-pager is defended under pushback because:", ["It is fun", "Interviewers test whether the recommendation survives challenge — defense with data is the graded skill", "It fills time", "Tradition"], 1, "The procedure's step 7 defends the one-pager as the interviewer pushes back — the Project brief grades judgment with architecture."),
("Technical cases score:", ["Coding", "Product judgment surviving contact with architecture — explicit, recorded, numbered", "Speed", "Diagrams"], 1, "The Project brief's grading lens: judgment with architecture — consumers first, tradeoffs explicit and recorded, numbers for build-versus-buy, defense with data."),
]}

RETRO["technical-pm-interview-prep--tech-pm-system-design"] = {
"summary": (
"Welcome back to the Technical PM track — I'm your instructor, and this is Module 5: Technical Design Reps. "
"Design reps calibrated for PMs: you will not out-architect the engineers, but you will connect architecture "
"choices to user outcomes, cost, and iteration speed — and record the tradeoffs. By the end of this module "
"you will perform the PM system-design interview format, reason about 10x and 100x scaling, weigh cost "
"versus latency versus complexity, hold the security basics, contribute the PM's lens in architecture "
"reviews, document decisions and tradeoffs, and know the limits of your depth."
),
"concepts": """- **System-design interview (PM format)** — Narrate architecture choices tied to user outcomes — you will not out-architect the engineers, and should not try.
- **Scaling reasoning** — 10x, 100x: what breaks first — the database, the single point of failure, the cost curve — name the bottleneck at each order of magnitude.
- **Cost versus latency versus complexity** — The eternal triangle: faster or cheaper or simpler — pick two consciously, state which you sacrificed.
- **Security basics (PM)** — Auth, data classification, least privilege, incident response — enough to ask the right questions and own the risk conversation.
- **Architecture reviews (PM's seat)** — Ask about tradeoffs, failure modes, and reversibility — the PM's contribution is the user-and-business lens.
- **Decision records** — ADRs outlive meetings — future teams need to know why, not just what.
- **Depth limits** — Knowing the limits of your depth: credible on systems, honest at the boundary — the calibration interviews reward.""" ,
"procedure": """Run the design-rep set. Work each rep aloud with a whiteboard or paper — 20 minutes each.
1. Narrate a system you know: components, data flow, and the architecture choices — tied to user outcomes at every step, as the PM format demands.
2. Scale it 10x: name what breaks first — the database, the single point of failure, the cost curve — and what you would change.
3. Scale it 100x: name the new bottleneck at this order of magnitude — the bottleneck moves; find it.
4. Weigh cost versus latency versus complexity for one decision: pick two consciously and state which you sacrificed — the eternal triangle, out loud.
5. Run the security read: auth, data classification, least privilege, incident response — write the risk questions you would own in the conversation.
6. Simulate the architecture review: ask three questions about tradeoffs, failure modes, and reversibility — contribute the user-and-business lens.
7. Write the decision record: the choice, the options, the tradeoff, why — ADRs outlive meetings.
8. Mark your depth boundary in writing: what you can defend, what you would defer — honest calibration is a strength.""",
"brief": """Your interview prep brief: deliver the design-rep portfolio.
The scenario. Your technical PM loop includes a system-design round calibrated for PMs: "Design a URL shortener — and tell me what breaks at 100x."
Deliverables.
- A narrated system design tied to user outcomes, with the 10x and 100x bottleneck analysis.
- A cost/latency/complexity tradeoff memo: the triangle, the two chosen, the sacrifice stated.
- A security read: the risk questions you own in the conversation.
- A simulated architecture-review question set: tradeoffs, failure modes, reversibility.
- A written decision record and a stated depth boundary.
Grading lens. PM design rounds score the PM's lens: did you narrate choices to outcomes, cost, and iteration speed — find the bottleneck at each order — and stay honest at your boundary?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Design reps must be performed on systems you genuinely understand — the format rewards the PM's lens, not borrowed architecture. Never out-architect the engineers in the room; narrate your own reasoning honestly and defer where your depth ends.""",
"quiz": [
("PM design interviews ask you to:", ["Out-architect engineers", "Narrate choices to user outcomes, cost, and iteration speed", "Draw boxes silently", "Stay silent"], 1, "The Concepts glossary defines the PM system-design format as narrating architecture choices tied to user outcomes — you will not out-architect the engineers, and should not try."),
("10x/100x reasoning:", ["Ignore scale", "Name what breaks first at each order of magnitude", "Hope", "Overbuild everything"], 1, "The Concepts note defines scaling reasoning as naming the bottleneck at each order — the database, the single point of failure, the cost curve."),
("Cost/latency/complexity:", ["Take all three", "Pick two consciously and state the sacrifice", "Ignore it", "Maximize all"], 1, "The Concepts glossary defines the eternal triangle: faster or cheaper or simpler — pick two consciously, state which you sacrificed."),
("PM security basics:", ["None needed", "Auth, classification, least privilege, incident response — ask and own the risk conversation", "Expert level", "Delegate everything"], 1, "The Concepts note defines PM security basics as auth, data classification, least privilege, incident response — enough to ask the right questions and own the risk conversation."),
("In architecture reviews, the PM contributes:", ["Silence", "The user-and-business lens: tradeoffs, failure modes, reversibility", "Approval stamps", "Designs"], 1, "The Concepts glossary defines the PM's seat at the table as asking about tradeoffs, failure modes, and reversibility — the user-and-business lens."),
("Decision records exist because:", ["Bureaucracy", "ADRs outlive meetings — future teams need to know why, not just what", "Compliance", "Habit"], 1, "The Concepts note defines decision records as outliving meetings — future teams need the why, not just the what."),
("The 100x bottleneck differs from the 10x one because:", ["It does not", "Bottlenecks move with scale — the exercise is finding each order's constraint", "Bigger numbers", "Magic"], 1, "The procedure's steps 2–3 scale to 10x then 100x, naming the new bottleneck at each order — the bottleneck moves; find it."),
("The depth boundary is written because:", ["It looks humble", "Honest calibration is a strength the interviews reward — bluffing fails follow-ups", "It saves time", "It is required"], 1, "The procedure's step 8 and the Concepts glossary agree: credible on systems, honest at the boundary — the calibration interviews reward."),
("The security read's output is:", ["A penetration test", "The risk questions you would own in the conversation", "A firewall", "A policy"], 1, "The procedure's step 5 writes the risk questions the PM would own — asking the right questions and owning the risk conversation."),
("PM design rounds score:", ["Diagrams", "The PM's lens: choices to outcomes, bottlenecks per order, honesty at the boundary", "Speed", "Vocabulary"], 1, "The Project brief's grading lens: narrate choices to outcomes, cost, and iteration speed — find the bottleneck at each order — stay honest at your boundary."),
]}

RETRO["technical-pm-interview-prep--tech-pm-mock"] = {
"summary": (
"Welcome back to the Technical PM track — I'm your instructor, and this is Module 6: Technical PM Mock "
"Circuit. The full circuit, simulated: technical depth, product judgment, and behavioral rounds tuned to the "
"technical PM bar — with rubrics that keep your depth honest. By the end of this module you will run the "
"hybrid technical-product-behavioral loop under timing, calibrate your depth honestly, whiteboard system "
"design as a PM, perform API design rounds, rubric-score technical answers, and iterate between mocks."
),
"concepts": """- **Technical PM loop** — Technical depth, product judgment, behavioral — tuned to the hybrid bar.
- **Depth calibration** — Knowing how deep is deep enough: credible on systems, honest at the boundary — the mock tunes this.
- **Whiteboard system design (PM)** — Narrate choices to outcomes: users, cost, iteration speed — the PM's design performance.
- **API design rounds** — Consumer thinking: resources, contracts, versioning, DX — APIs as products.
- **Rubric scoring (technical)** — Accuracy, tradeoff awareness, honesty about limits — the dimensions that separate credible from bluffing.
- **Iteration between mocks** — Depth calibration improves with reps — each mock sharpens the boundary between knowing and performing.""" ,
"procedure": """Run the full technical PM mock circuit. Three rounds with a partner or recorded; real clocks.
1. Round 1 — technical depth (40 min): trace a system, weigh a caching or queue tradeoff, estimate scale — reasoning chains aloud.
2. Your partner probes your depth boundary: answer honestly where it ends — the mock tunes calibration.
3. Self-review: accuracy, tradeoff awareness, honesty about limits — score the dimensions that separate credible from bluffing.
4. Round 2 — product judgment (40 min): an API design case and a build-versus-buy — consumers first, tradeoffs explicit, numbers on paper.
5. Self-review: did judgment survive contact with architecture? Score honestly.
6. Round 3 — behavioral (25 min): two stories in tight STAR — your role explicit, learning real.
7. Write the iteration plan: three targeted fixes, including one depth-calibration fix — each mock sharpens the boundary.
8. Run the circuit again in one week and measure the delta: where did calibration improve?""",
"brief": """Your interview prep brief: execute and document one full technical PM mock circuit.
The scenario. Your technical PM onsite is two weeks out: technical depth, product judgment, and behavioral rounds at the hybrid bar.
Deliverables.
- Timed recordings (or partner notes) for all three rounds.
- Rubric scores on accuracy, tradeoff awareness, and honesty about limits — per round.
- A depth-calibration note: where your boundary sits after the mock, and what you would defer.
- An iteration plan: three targeted fixes including one calibration fix, and next week's measured delta.
Grading lens. The hybrid bar scores credible depth with honest limits: did you reason in chains, weigh tradeoffs explicitly, defend with data — and mark your boundary truthfully?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Depth calibration only works on honest answers — bluffing in the mock rehearses bluffing in the loop. Every technical claim must be one you can defend; every deferral must be stated, not hidden. The boundary is the skill.""",
"quiz": [
("The tech-PM loop is:", ["Coding only", "Technical, product, behavioral — the hybrid bar", "Trivia", "Design only"], 1, "The Concepts glossary defines the technical PM loop as technical depth, product judgment, behavioral — tuned to the hybrid bar."),
("Depth calibration means:", ["Maximum depth", "How deep is deep enough — credible, honest at the boundary", "Shallow answers", "Bluffing"], 1, "The Concepts note defines depth calibration as knowing how deep is deep enough: credible on systems, honest at the boundary."),
("Whiteboarding as a PM means:", ["Silent drawing", "Narrating choices to outcomes throughout", "Letting others talk", "Skipping"], 1, "The Concepts glossary defines PM whiteboard design as narrating choices to outcomes: users, cost, iteration speed — the PM's design performance."),
("API rounds test:", ["Syntax", "Consumer thinking: contracts, versioning, DX", "Speed", "Trivia"], 1, "The Concepts note defines API design rounds as consumer thinking: resources, contracts, versioning, DX — APIs as products."),
("Technical answers are scored on:", ["Confidence", "Accuracy, tradeoff awareness, honesty about limits", "Length", "Jargon"], 1, "The Concepts glossary defines the technical rubric as accuracy, tradeoff awareness, honesty about limits — separating credible from bluffing."),
("The partner's boundary-probing tests:", ["Memory", "Whether you state your limits honestly under pressure", "Speed", "Trivia"], 1, "The procedure's step 2 probes the depth boundary — the mock tunes calibration, and honest limits are the graded skill."),
("The iteration plan must include:", ["More mocks", "One depth-calibration fix among the three targeted fixes", "Luck", "Rest"], 1, "The procedure's step 7 requires three targeted fixes including one depth-calibration fix — each mock sharpens the boundary."),
("Next week's delta measures:", ["Confidence", "Where calibration improved — knowing versus performing", "Speed", "Luck"], 1, "The procedure's step 8 measures where calibration improved — the Concepts note defines iteration as sharpening the boundary between knowing and performing."),
("Bluffing in the mock is dangerous because:", ["It is rude", "It rehearses bluffing in the loop — calibration only works on honest answers", "It wastes time", "Partners judge"], 1, "The Honesty note is explicit: bluffing in the mock rehearses bluffing in the loop — depth calibration only works on honest answers."),
("The hybrid bar rewards:", ["Maximum depth", "Credible depth with honest limits — the boundary is the skill", "Speed", "Volume"], 1, "The Project brief's grading lens and the Honesty note agree: credible depth with honest limits — the boundary is the skill."),
]}
