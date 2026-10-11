# GenAI for PM track, part 3: genai-pm-playbook, genai-risk-pm, genai-roadmap-pm
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["genai-for-pm--genai-pm-playbook"] = {
"summary": (
"Welcome back to the GenAI track — I'm your instructor, and this is Module 4: GenAI PM Playbook. "
"The capstone project of the path: take an AI feature from opportunity through prototype spec, eval plan, and "
"launch checklist — a portfolio artifact that proves AI product judgment. By the end of this module you will "
"size AI opportunities, write prototype specs that anticipate launch questions, design eval plans before "
"building, gate launches with evidence, track quality-cost-trust metrics, and brief stakeholders on AI risk."
),
"concepts": """- **Opportunity sizing (AI)** — Problem frequency × pain × AI suitability — the opportunity math before the prototype.
- **Prototype spec** — The job, the pattern, the eval plan, the guardrails — a spec that anticipates the launch questions.
- **Eval plan** — Golden cases, success criteria, human calibration, regression cadence — measurement before building.
- **AI launch checklist** — Evals green, guardrails live, rollback ready, monitoring on, owners named — the gate.
- **AI feature metrics** — Quality (task success, hallucination rate), cost (per task), trust (escalations, corrections) — the three dials.
- **Stakeholder pre-read (AI risk)** — The risks in business terms, mitigations, owners, and the launch gate — the document that keeps bets funded.""" ,
"procedure": """Build the playbook artifact end to end. Pick an AI feature you would actually ship and work it on paper.
1. Size the opportunity: problem frequency × pain × AI suitability — the math before the prototype.
2. Choose the pattern deliberately and write the prototype spec: the job, the pattern, the eval plan, the guardrails — anticipating the launch questions.
3. Design the eval plan before building: golden cases, success criteria, human calibration, regression cadence — measurement first.
4. Write the launch checklist: evals green, guardrails live, rollback ready, monitoring on, owners named — the gate, specified.
5. Define the three-dial metrics: quality (task success, hallucination rate), cost (per task), trust (escalations, corrections) — and the thresholds that would worry you.
6. Write the stakeholder pre-read on AI risk: the risks in business terms, the mitigations, the owners, the launch gate — the document that keeps the bet funded.
7. Present the whole playbook aloud in fifteen minutes: opportunity, spec, eval plan, gate, metrics, pre-read — the portfolio artifact, performed.""",
"brief": """Your interview prep brief: produce the complete GenAI PM playbook for one feature.
The scenario. Your AI PM loop's capstone question: "Take me from idea to launch for an AI feature — the whole thing." This artifact is your answer.
Deliverables.
- Opportunity sizing: frequency × pain × AI suitability, with the numbers.
- A prototype spec: job, pattern, eval plan, guardrails.
- An eval plan: golden cases, success criteria, calibration, regression cadence.
- A launch checklist: the gate, specified and checkable.
- Three-dial metrics with worry thresholds.
- A stakeholder pre-read on AI risk in business terms.
Grading lens. The capstone scores end-to-end judgment: did you do the math before the prototype, measure before building, gate on evidence — and keep the bet funded with honest risk communication?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. The playbook artifact must describe a feature you could actually defend — interviewers will probe the eval plan and the cost math. As of late 2026, model pricing and capabilities shift quickly: date your numbers and verify them against current provider documentation.""",
"quiz": [
("Opportunity sizing for AI is:", ["Gut feel", "Frequency × pain × AI suitability", "Hype", "Votes"], 1, "The Concepts glossary defines AI opportunity sizing as problem frequency × pain × AI suitability — the opportunity math before the prototype."),
("Prototype specs anticipate:", ["Code details", "Launch questions: evals, guardrails, gates", "Design polish", "Hype"], 1, "The Concepts note defines the prototype spec as the job, the pattern, the eval plan, the guardrails — a spec that anticipates the launch questions."),
("Eval plans come:", ["After launch", "Before building — measurement first", "Never", "Later"], 1, "The Concepts glossary defines the eval plan as golden cases, success criteria, human calibration, regression cadence — measurement before building."),
("The AI launch gate requires:", ["A date", "Evals green, guardrails live, rollback ready, owners named", "A demo", "A budget"], 1, "The Concepts note defines the AI launch checklist as evals green, guardrails live, rollback ready, monitoring on, owners named — the gate."),
("AI metrics' three dials are:", ["Clicks", "Quality, cost, trust", "Revenue", "Users"], 1, "The Concepts glossary defines AI feature metrics as quality (task success, hallucination rate), cost (per task), trust (escalations, corrections) — the three dials."),
("The stakeholder pre-read covers AI risk in:", ["Technical jargon", "Business terms: risks, mitigations, owners, the launch gate", "Legalese", "Marketing copy"], 1, "The Concepts note defines the pre-read as the risks in business terms, mitigations, owners, and the launch gate — the document that keeps bets funded."),
("The worry thresholds are set so that:", ["Alarms never fire", "You know what 'bad' looks like before launch — the dials have tripwires", "Dashboards look full", "Reports impress"], 1, "The procedure's step 5 defines the three dials with the thresholds that would worry you — tripwires set before launch."),
("Guardrails in the prototype spec cover:", ["The demo", "The boundaries the feature operates within — before launch questions arrive", "The logo", "The pricing"], 1, "The procedure's step 2 writes the spec with the guardrails — anticipating the launch questions."),
("The playbook is presented in fifteen minutes because:", ["Arbitrary", "Capstone rounds ask for the whole journey — opportunity to gate — performed crisply", "Long is impressive", "Short is trendy"], 1, "The procedure's step 7 performs the whole playbook in fifteen minutes — the capstone question is 'take me from idea to launch, the whole thing.'"),
("The capstone scores:", ["Polish", "End-to-end judgment: math before prototype, measurement before building, evidence at the gate", "Speed", "Length"], 1, "The Project brief's grading lens: math before the prototype, measure before building, gate on evidence — and honest risk communication keeping the bet funded."),
]}

RETRO["genai-for-pm--genai-risk-pm"] = {
"summary": (
"Welcome back to the GenAI track — I'm your instructor, and this is Module 5: Risk and Responsibility. "
"The risk half of shipping AI: bias, privacy, safety, and misuse — taught as product decisions with owners "
"and mitigations, not as abstract ethics. By the end of this module you will assess bias and fairness on your "
"use case, manage what the model remembers, threat-model safety and misuse, scope red-teaming, "
"operationalize responsible AI principles, run AI incident response, and document risk decisions."
),
"concepts": """- **Bias and fairness (AI)** — Model outputs that disadvantage groups — measured on your use case, mitigated as product decisions.
- **Privacy (model memory)** — Training data can leak through outputs — know what went in, control what comes out, minimize PII.
- **Safety and misuse** — Harmful outputs and adversarial use — threat-modeled like any abuse vector, with mitigations owned.
- **Red-teaming (PM)** — Adversarial testing of your AI feature before users do it — the PM scopes it, specialists run it.
- **Responsible AI principles** — Fairness, transparency, accountability, human oversight — operationalized as checklists and owners, not posters.
- **AI incident response** — Detect bad outputs, contain, fix, communicate — the runbook for probabilistic failures.
- **Risk documentation** — The written record of risk decisions: the risk, the mitigation, the owner, the accepted residual — decided, not drifted into.""" ,
"procedure": """Run the AI risk drill on a feature you would ship — real or simulated. Work it as product decisions, not essays.
1. Assess bias and fairness on your use case: who could be disadvantaged by the outputs, how you would measure it, and the mitigation as a product decision.
2. Audit model memory: what data went in, what could leak through outputs, and the PII minimization plan — control what comes out.
3. Threat-model safety and misuse: the harmful outputs, the adversarial uses — modeled like any abuse vector, with mitigations owned.
4. Scope the red-team: what the PM asks the specialists to attack, the success criteria for the exercise, and what a "pass" unlocks.
5. Operationalize the principles: fairness, transparency, accountability, human oversight — as checklists with named owners, not posters.
6. Write the AI incident runbook: detect bad outputs, contain, fix, communicate — the probabilistic-failure runbook.
7. Document the risk decisions: the risk, the mitigation, the owner, the accepted residual — decided in writing, not drifted into.
8. Present the risk picture aloud in ten minutes: the risks in business terms, the mitigations, the owners — the pre-read, performed.""",
"brief": """Your interview prep brief: produce the risk register and incident runbook for an AI feature.
The scenario. Your AI PM loop asks: "This AI feature handles customer data and makes recommendations. Walk me through the risks — and what happens when it goes wrong."
Deliverables.
- A risk register: bias, privacy, safety, misuse — each measured on the use case, each with a mitigation and an owner.
- A red-team scope: what gets attacked, by whom, what "pass" means.
- An operationalized principles checklist: fairness, transparency, accountability, oversight — with owners.
- An AI incident runbook: detect, contain, fix, communicate.
- Written risk decisions: the accepted residuals, decided — not drifted into.
Grading lens. Risk rounds score operational responsibility: did you measure on the use case, own the mitigations, scope the adversarial testing — and document what you accepted?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Risk claims must be grounded in real assessments of real features — never hand-wave bias, privacy, or safety in an interview; interviewers in this domain test whether you have actually done the work. As of late 2026, the risk landscape evolves: date your claims and verify against current guidance.""",
"quiz": [
("Bias risks are:", ["Theoretical", "Measured on your use case, mitigated as product decisions", "Solved", "Ignorable"], 1, "The Concepts glossary defines bias and fairness as model outputs that disadvantage groups — measured on your use case, mitigated as product decisions."),
("Model memory (privacy) means:", ["It is safe", "Training data can leak through outputs — minimize PII, control what comes out", "It is empty", "It is irrelevant"], 1, "The Concepts note defines model memory: training data can leak through outputs — know what went in, control what comes out, minimize PII."),
("Red-teaming is:", ["Hacking", "Adversarial testing before users do it — the PM scopes it", "Optional", "Fun"], 1, "The Concepts glossary defines red-teaming as adversarial testing of your AI feature before users do it — the PM scopes it, specialists run it."),
("Responsible AI in practice is:", ["Posters", "Checklists and owners: fairness, transparency, accountability, oversight", "Slogans", "Legal's job"], 1, "The Concepts note defines responsible AI principles as operationalized — checklists and owners, not posters."),
("AI incident response is:", ["Panic", "Detect, contain, fix, communicate — the probabilistic runbook", "Hiding", "Blame"], 1, "The Concepts glossary defines AI incident response as detect bad outputs, contain, fix, communicate — the runbook for probabilistic failures."),
("Safety and misuse are handled by:", ["Hope", "Threat-modeling like any abuse vector, with mitigations owned", "Filters alone", "Lawyers"], 1, "The Concepts note defines safety and misuse as threat-modeled like any abuse vector, with mitigations owned."),
("Risk documentation records:", ["Fears", "The risk, the mitigation, the owner, the accepted residual — decided in writing", "Disclaimers", "Nothing"], 1, "The Concepts glossary defines risk documentation as the written record: risk, mitigation, owner, accepted residual — decided, not drifted into."),
("The red-team scope is the PM's job because:", ["PMs hack", "The PM defines what gets attacked and what 'pass' unlocks — specialists run it", "It is fun", "No one else will"], 1, "The procedure's step 4 scopes the red-team: what the PM asks specialists to attack, the success criteria, what a pass unlocks."),
("Accepted residuals must be:", ["Hidden", "Decided in writing — not drifted into", "Denied", "Ignored"], 1, "The procedure's step 7 documents the accepted residuals as decided in writing — the Concepts note says decided, not drifted into."),
("Risk rounds score:", ["Caution", "Operational responsibility: measured on the use case, mitigations owned, adversarial testing scoped", "Fear", "Compliance"], 1, "The Project brief's grading lens: operational responsibility — measure on the use case, own the mitigations, scope the adversarial testing, document what you accepted."),
]}

RETRO["genai-for-pm--genai-roadmap-pm"] = {
"summary": (
"Welcome back to the GenAI track — I'm your instructor, and this is Module 6: Roadmapping AI Products. "
"AI roadmaps live with model improvement, vendor dependence, and uncertain timelines. This module teaches "
"sequencing, pricing, and the executive communication that keeps AI bets funded. By the end of this module "
"you will sequence AI bets as a portfolio, make deliberate build-versus-buy model decisions, manage platform "
"dependencies and vendor risk, price AI features with real margins, align stakeholders on AI risk and "
"timelines, and communicate uncertainty to executives honestly."
),
"concepts": """- **AI bet sequencing** — Low-risk wins first, platform dependencies mapped, uncertain timelines buffered — the roadmap as a bet portfolio.
- **Build versus buy (models)** — Commodity capability: buy or API. Differentiating: build or adapt. Vendor risk priced in — deliberately.
- **Platform dependencies** — Model behavior changes, pricing shifts, availability — dependencies managed, not assumed.
- **Vendor risk** — The exposure behind the dependency: what breaks if the model changes, reprices, or degrades — priced into the decision.
- **AI feature pricing** — Per-task cost at volume plus overhead and support — margins that survive the invoice and the scale-up.
- **Stakeholder alignment (AI)** — Pre-reads with the uncertainties named, gates defined, kill criteria set — alignment before the bet.
- **Executive uncertainty communication** — Ranges, scenarios, and what would change the outlook — honest uncertainty beats false precision.""" ,
"procedure": """Run the AI-roadmap drill. Plan one year of AI bets for a product you know — on paper, as a portfolio.
1. List three AI bets and sequence them: low-risk wins first, platform dependencies mapped, uncertain timelines buffered — the bet portfolio.
2. For each bet, decide build versus buy: commodity capability buys the API; differentiating builds or adapts — with vendor risk priced in, deliberately.
3. Map the platform dependencies: model behavior changes, pricing shifts, availability — and write the contingency for each.
4. Price one feature with real margins: per-task cost at volume plus overhead and support — margins that survive the invoice and the scale-up.
5. Write the stakeholder pre-read: the uncertainties named, the gates defined, the kill criteria set — alignment before the bet.
6. Draft the executive update: ranges, scenarios, and what would change the outlook — honest uncertainty, no false precision.
7. Present the roadmap aloud in ten minutes: the portfolio, the sourcing, the pricing, the uncertainty — the communication that keeps bets funded.""",
"brief": """Your interview prep brief: produce the one-year AI roadmap and the executive communication around it.
The scenario. Your AI PM loop asks: "We have budget for three AI bets next year. Sequence them, price one, and tell me how you would keep the exec team aligned."
Deliverables.
- A sequenced bet portfolio: three bets, low-risk wins first, dependencies mapped, timelines buffered.
- Build-versus-buy decisions for each: commodity versus differentiating, vendor risk priced in.
- A dependency-and-contingency map: behavior changes, pricing shifts, availability.
- Real-margin pricing for one feature: per-task cost at volume plus overhead.
- A stakeholder pre-read and an executive update: uncertainties named, gates defined, kill criteria set.
Grading lens. Roadmap rounds score portfolio judgment and honest communication: did you sequence by risk, price with margins that survive scale, and communicate uncertainty without false precision?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Roadmap claims must be grounded in real cost math and real vendor terms you have actually read — as of late 2026, model pricing and capabilities move fast, so date your numbers. Never present a roadmap built on assumed pricing as a committed plan.""",
"quiz": [
("Sequence AI bets by:", ["Biggest first", "Low-risk wins first, dependencies mapped, timelines buffered", "Random order", "All at once"], 1, "The Concepts glossary defines AI bet sequencing as low-risk wins first, platform dependencies mapped, uncertain timelines buffered — the roadmap as a bet portfolio."),
("Model build versus buy:", ["Always build", "Commodity: buy/API; differentiating: build — vendor risk priced in", "Always buy", "Cheapest wins"], 1, "The Concepts note defines the model decision as commodity capability buys the API, differentiating builds or adapts — vendor risk priced in, deliberately."),
("Vendor risks include:", ["None", "Behavior change, pricing shifts, availability — managed dependencies", "Theoretical only", "Ignorable"], 1, "The Concepts glossary defines platform dependencies as model behavior changes, pricing shifts, availability — dependencies managed, not assumed."),
("Price AI features with:", ["Hopes", "Per-task cost at volume plus overhead — margins surviving scale", "Guesses", "Discounts"], 1, "The Concepts note defines AI feature pricing as per-task cost at volume plus overhead and support — margins that survive the invoice and the scale-up."),
("Align stakeholders via:", ["Surprises", "Pre-reads: uncertainties named, gates defined, kill criteria set", "Decks", "Hype"], 1, "The Concepts glossary defines stakeholder alignment as pre-reads with the uncertainties named, gates defined, kill criteria set — alignment before the bet."),
("Executive uncertainty communication uses:", ["False precision", "Ranges, scenarios, and what would change the outlook", "Silence", "Optimism"], 1, "The Concepts note defines executive uncertainty communication as ranges, scenarios, and what would change the outlook — honest uncertainty beats false precision."),
("Vendor risk is priced into the decision because:", ["It sounds thorough", "Exposure to model changes, repricing, or degradation is a real cost — deliberate sourcing accounts for it", "Vendors demand it", "It is trendy"], 1, "The Concepts glossary defines vendor risk as the exposure behind the dependency — priced into the decision."),
("Kill criteria are set so that:", ["Bets never die", "The bet has a defined exit — alignment includes knowing when to stop", "Reports look decisive", "Execs feel powerful"], 1, "The procedure's step 5 sets kill criteria in the pre-read — alignment before the bet includes knowing when to stop."),
("The roadmap is a bet portfolio because:", ["Gambling is fun", "AI bets carry model, vendor, and timeline uncertainty — sequencing manages the portfolio risk", "Portfolios impress", "Tradition"], 1, "The Concepts glossary frames the roadmap as a bet portfolio — low-risk wins first, dependencies mapped, timelines buffered."),
("Roadmap rounds score:", ["Ambition", "Portfolio judgment and honest communication: risk-sequenced, real margins, no false precision", "Speed", "Slide design"], 1, "The Project brief's grading lens: portfolio judgment and honest communication — sequence by risk, price with surviving margins, communicate uncertainty honestly."),
]}
