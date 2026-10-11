# TPM track, part 3: cross-functional-leadership, technical-depth-tpm
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["tpm-interview-prep--cross-functional-leadership"] = {
"summary": (
"Welcome back to the TPM track — I'm your instructor, and this is Module 3: Cross-Functional Leadership. "
"TPMs own outcomes they cannot command. This module teaches the influence toolkit: stakeholder maps, decision "
"logs, crisp escalations, and the follow-through that makes teams trust your coordination. By the end of this "
"module you will align engineering managers and PMs on shared outcomes, resolve cross-team conflict with the "
"tradeoff explicit, write executive pre-reads that respect executive time, and drive decisions in ambiguous ownership."
),
"concepts": """- **Influence without authority** — The TPM's core currency: stakeholder maps, decision logs, crisp escalations, and relentless follow-through — trust compounded over time.
- **Connective tissue** — The TPM's organizational role: carrying context across team boundaries so multi-team programs stay coherent.
- **Decision log** — The written record of who decided what, when, and why — ambiguity dies where decisions are logged.
- **Alignment** — A document before it is a feeling: shared outcomes, explicit tradeoffs, and written agreements between engineering managers and PMs.
- **Conflict resolution** — Reframing around the shared goal, surfacing the real constraint, deciding with the tradeoff explicit — then recording it.
- **Executive communication** — Pre-reads carrying the decision needed, the options, and the recommendation — respect for executive time earns executive trust.
- **Ambiguous ownership** — Resolved when someone names the decision, proposes the owner, and sets the deadline — ambiguity hates documentation.
- **Trust across organizations** — Built by follow-through on coordination promises: what you said would happen, happened.""" ,
"procedure": """Run the cross-functional influence drill. Pick a real or simulated two-team dispute or ambiguous decision — the mechanics work on any material.
1. Draw the stakeholder map: who is impacted, who decides, who needs informing — for both teams.
2. Write the decision log entry: name the decision, propose the owner, set the deadline — write it down even if it feels premature.
3. Draft a one-page alignment document: the shared outcome, the explicit tradeoffs, and the written agreement both sides will sign off on.
4. If there is conflict, reframe it in writing around the shared goal: surface the real constraint (capacity? priority? information?) and record the decision with its tradeoff.
5. Write the executive pre-read for the decision: the decision needed, the options, your recommendation — one page, respectful of executive time.
6. Follow through: send the updates you promised on the rhythm you promised — and log that you did.
7. Debrief aloud in three minutes: where did influence work, where did it stall, and which tool (map, log, pre-read, follow-through) moved it?""",
"brief": """Your interview prep brief: show influence without authority on a conflict between two teams.
The scenario. The payments team and the fraud team disagree on the checkout program's fraud-review scope: payments wants speed, fraud wants rigor, and both report to different VPs. The launch date is held by the executive sponsor, who wants a recommendation this week.
Deliverables.
- A stakeholder map and a decision log entry with the decision named, owner proposed, deadline set.
- A one-page alignment document both teams can sign: shared outcome, explicit tradeoffs, written agreements.
- An executive pre-read: decision needed, options, your recommendation — one page.
- A three-minute spoken walkthrough of how you influenced the outcome without owning either team.
Grading lens. Cross-functional rounds score process, not authority: did you reframe around the shared outcome, surface the real constraint, record the decision — and earn trust through follow-through?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Influence stories are only as strong as the outcomes behind them: anchor every answer in a real situation you actually coordinated, and name your real role. Fabricated influence reads as manipulation; earned influence reads as leadership.""",
"quiz": [
("Influence without authority is built on:", ["Titles", "Trust, decision logs, and follow-through", "Politics", "Meeting volume"], 1, "The Concepts note defines influence without authority as stakeholder maps, decision logs, crisp escalations, and relentless follow-through — trust compounded over time."),
("Ambiguous ownership resolves when:", ["It is ignored", "Someone names the decision, owner, and deadline in writing", "It is escalated", "It is voted on"], 1, "The Concepts glossary says ambiguity resolves when someone names the decision, proposes the owner, and sets the deadline — ambiguity hates documentation."),
("Executive pre-reads contain:", ["Everything", "The decision needed, options, and recommendation", "Jokes", "Full history"], 1, "Executive communication is the decision needed, the options, and the recommendation — respect for executive time earns executive trust."),
("Cross-team conflict resolves via:", ["Authority", "Reframing around the shared goal, the tradeoff explicit, the decision recorded", "Avoidance", "Escalation only"], 1, "The Concepts note defines conflict resolution as reframing around the shared goal, surfacing the real constraint, and deciding with the tradeoff explicit — then recording it."),
("The TPM as connective tissue means:", ["Attending every meeting", "Carrying context across team boundaries", "Writing documentation", "Chatting constantly"], 1, "The Concepts glossary defines the connective-tissue role as carrying context across team boundaries — the information flow keeping programs coherent."),
("In the influence drill, the alignment document comes:", ["After feelings align", "Before the feeling — alignment is a document first", "Never", "After launch"], 1, "The Concepts note states alignment is a document before it is a feeling: shared outcomes, explicit tradeoffs, written agreements."),
("The decision log entry requires all of:", ["The decision, the proposed owner, and the deadline", "Just the decision", "Just the owner", "A committee vote"], 0, "The Hands-on procedure's step 2 names the three required elements: name the decision, propose the owner, set the deadline — written down even if it feels premature."),
("Follow-through earns trust because:", ["It is polite", "Coordination promises kept on rhythm compound into trust", "It fills the calendar", "It impresses executives"], 1, "The Concepts note defines trust across organizations as built by follow-through on coordination promises: what you said would happen, happened."),
("Reframing a conflict around the shared goal requires first:", ["Picking a winner", "Surfacing the real constraint — capacity, priority, or information", "A louder voice", "More meetings"], 1, "The procedure's conflict step: surface the real constraint first, then reframe around the shared goal and record the decision with its tradeoff."),
("The Project brief's pre-read is one page because:", ["Short is trendy", "Executive time is scarce — the decision, options, and recommendation must fit it", "Formatting is easy", "Nobody reads"], 1, "The Project brief grades respect for executive time: the decision needed, the options, the recommendation — one page."),
]}

RETRO["tpm-interview-prep--technical-depth-tpm"] = {
"summary": (
"Welcome back to the TPM track — I'm your instructor, and this is Module 4: Technical Depth for TPMs. "
"TPM interviews probe technical depth without requiring you to code. This module builds the literacy to read "
"designs, question tradeoffs, and spot integration risk — and the humility to know where your depth ends. "
"By the end of this module you will read architecture documents critically, reason about API contracts and "
"integration points, speak SLOs and error budgets fluently, and ask the sharp technical questions that show "
"you understand the tradeoff space."
),
"concepts": """- **Technical depth for TPMs** — Literacy, not coding: reading designs critically, spotting integration risk, and questioning tradeoffs — plus the humility to know where your depth ends.
- **System-design literacy (non-coder)** — Reading architecture docs for components, data flow, and failure modes — enough to question tradeoffs intelligently.
- **Critical reading of architecture docs** — Asking what breaks, what scales, what was decided and why — the questions that reveal the design's real risks.
- **API contracts and integration points** — The boundaries where systems meet: schemas, versions, error handling — where integration risk lives.
- **Data pipelines** — Sources, transforms, sinks — and where data quality or latency breaks downstream promises.
- **SLO literacy** — SLIs, SLOs, and error budgets: what "reliable enough" costs — the language of production commitments.
- **Sharp technical questions** — Probes of assumptions, alternatives considered, and failure modes — questions that show you understand the tradeoff space.
- **Deferral with humility** — Knowing when to defer to engineering judgment on implementation choices within agreed constraints — humility that builds engineering trust.""" ,
"procedure": """Run the technical-depth rep on a real architecture document — from your own past work if you have one, or a public design doc you can reference.
1. Read the document once and sketch its component diagram: components, data flow, and the integration points between systems.
2. Mark every API contract and integration point with a red flag — these are where integration risk lives.
3. Trace one end-to-end data pipeline through the diagram: source, transform, sink — and write down where data quality or latency could break a downstream promise.
4. Ask the three critical questions in writing: what breaks first, what scales worst, and what was decided and why.
5. Write the SLO question: what is the production commitment here, what does "reliable enough" cost, and where is the error budget?
6. Draft three sharp technical questions you would ask the design's author — each probing an assumption, an alternative, or a failure mode.
7. Mark in writing the boundary of your own depth: which judgments you can defend, and which you would defer to engineering judgment — humility on paper.
8. Present the whole reading aloud in ten minutes: the design, its risks, your questions, and your deferral boundary.""",
"brief": """Your interview prep brief: prove technical depth without writing code.
The scenario. Your TPM technical round hands you a design doc for a notification pipeline: an API ingests events, a queue buffers them, workers render templates, and an email/SMS provider delivers. The interviewer asks you to find the risks.
Deliverables.
- A component-and-data-flow sketch with integration points flagged.
- A written critical reading: what breaks first, what scales worst, what was decided and why.
- The SLO reading: the production commitment, the error-budget implication, the "reliable enough" cost.
- Three sharp technical questions probing assumptions, alternatives, and failure modes.
- A stated deferral boundary: what you can defend, and what you would hand to engineering judgment.
Grading lens. The round scores literacy plus judgment, with humility: did you find the real integration risks, speak the reliability language, ask questions that reveal the tradeoff space — and know where your depth ends?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Technical depth cannot be borrowed: read real designs, ask real questions, and never claim fluency you do not have. The deferral boundary is a strength in the interview, not a weakness — bluffing collapses under follow-up.""",
"quiz": [
("TPM technical depth is for:", ["Coding", "Reading designs critically and spotting integration risk", "Showing off", "Replacing engineers"], 1, "The Concepts note defines TPM technical depth as literacy, not coding: reading designs critically, spotting integration risk, questioning tradeoffs."),
("Integration risk lives at:", ["The database", "API contracts and integration points between systems", "The UI", "Nowhere"], 1, "The Concepts glossary is explicit: the boundaries where systems meet — schemas, versions, error handling — are where integration risk lives."),
("SLO literacy means understanding:", ["Uptime only", "Error budgets and what 'reliable enough' costs", "Latency only", "Nothing"], 1, "The Concepts note defines SLO literacy as SLIs, SLOs, and error budgets — the language of production commitments."),
("Sharp technical questions probe:", ["Trivia", "Assumptions, alternatives, and failure modes", "Syntax", "Company history"], 1, "The Concepts glossary defines sharp questions as probes of assumptions, alternatives considered, and failure modes — revealing the tradeoff space."),
("Defer to engineering judgment on:", ["Everything", "Implementation choices within agreed constraints", "Nothing", "Strategy"], 1, "The Concepts note defines deferral with humility: defer on implementation choices within agreed constraints — humility builds engineering trust."),
("In the technical-depth rep, the first thing you mark on the diagram is:", ["The logo", "Every API contract and integration point — integration risk lives there", "The colors", "The page numbers"], 1, "The Hands-on procedure's step 2: flag every API contract and integration point, because the boundaries are where systems break."),
("Tracing the data pipeline means walking:", ["The org chart", "Source, transform, sink — and where quality or latency breaks downstream promises", "The budget", "The roadmap"], 1, "The procedure's step 3 and the Concepts glossary define pipeline tracing as sources, transforms, sinks, plus where data quality or latency breaks downstream promises."),
("The deferral boundary is written down because:", ["It looks honest", "Bluffing collapses under follow-up — knowing where your depth ends is a strength", "Interviewers like lists", "It saves time"], 1, "The procedure's step 7 and the Honesty note agree: mark which judgments you can defend and which you defer — humility is a strength, bluffing collapses."),
("The three critical reading questions are:", ["Who wrote this", "What breaks first, what scales worst, what was decided and why", "How long is this", "Is this pretty"], 1, "The procedure's step 4 lists exactly these three questions — the questions that reveal the design's real risks."),
("The technical round scores:", ["Coding speed", "Literacy plus judgment, with humility about limits", "Whiteboard art", "Jargon density"], 1, "The Project brief's grading lens: literacy plus judgment, with humility — finding real risks, speaking reliability language, knowing your boundary."),
]}
