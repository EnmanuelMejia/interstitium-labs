# GenAI for PM track, part 2: llm-product-patterns, eval-ux-ai
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["genai-for-pm--llm-product-patterns"] = {
"summary": (
"Welcome back to the GenAI track — I'm your instructor, and this is Module 2: LLM Product Patterns. "
"The recurring shapes of LLM products — chat, copilots, agents, RAG — with guidance on matching the pattern "
"to the problem instead of defaulting to a chatbot. By the end of this module you will name the chat pattern's "
"traps, design copilots inside existing workflows, judge when agents fit, apply RAG for grounded knowledge "
"tasks, use summarization and transformation patterns, choose patterns deliberately, and iterate with "
"eval-driven prompt and system design."
),
"concepts": """- **Chat pattern** — The default pattern — and its trap: defaulting to chat for everything, where many tasks need structured UI, not conversation.
- **Copilots** — AI inside existing workflows: suggest, complete, accelerate — the user stays in control.
- **Agents** — When the model takes actions: multi-step tasks with tool use where autonomy pays — and where the failure modes are acceptable.
- **RAG (retrieval-augmented generation)** — Grounding answers in your data with citations — for knowledge tasks where freshness and verifiability matter.
- **Summarization and transformation** — Compress, convert, reformat — the reliable workhorses where outputs are verifiable.
- **Pattern matching** — Choosing by verifiability needs, latency, cost, and user control — matched to the job, not defaulted to a chatbot.
- **Eval-driven iteration** — Improving prompts and systems against evals: measure, change, re-measure — iteration with a scoreboard.""" ,
"procedure": """Run the pattern-matching drill. Take three product jobs and match each to a pattern — on paper, with reasons.
1. Job 1 — a knowledge task ("answer questions about our docs"): design the RAG pattern — retrieval, grounding, citations — and name where freshness and verifiability matter.
2. Job 2 — a workflow task ("help analysts write reports"): design the copilot — suggest, complete, accelerate — with the user staying in control.
3. Job 3 — a multi-step task ("triage and route incoming tickets"): judge whether agents fit — where autonomy pays, and whether the failure modes are acceptable.
4. For each job, write why chat is the wrong default: what structured UI or pattern serves the job better.
5. Weigh each pattern on the four axes: verifiability needs, latency, cost, user control — the deliberate-matching scorecard.
6. Design the eval-driven iteration loop for one pattern: the evals you would run, what you would change, how you would know it worked.
7. Present one pattern choice aloud in five minutes: the job, the pattern, the scorecard, the iteration plan.""",
"brief": """Your interview prep brief: match patterns to jobs and defend the choices.
The scenario. Your AI PM loop asks: "We have three AI ideas — a support chatbot, an in-editor writing assistant, and an autonomous ticket resolver. Which patterns, and why?"
Deliverables.
- A pattern match for each idea: the chosen pattern (chat/copilot/agent/RAG/transformation), with the four-axis scorecard: verifiability, latency, cost, user control.
- A written argument for why chat is the wrong default for at least one of them.
- An eval-driven iteration plan for the riskiest pattern choice.
- A five-minute recorded defense of the three choices.
Grading lens. AI product rounds score deliberate matching: did you choose by the job's needs rather than the default, name the failure modes, and plan iteration with a scoreboard?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Pattern judgment must be grounded in products you have actually used or built — as of late 2026, agentic capabilities and RAG tooling evolve quickly, so date your claims. Never recommend a pattern you have not seen survive real users.""",
"quiz": [
("Chat's trap is:", ["It is bad", "Defaulting to chat where structured UI fits better", "Its cost", "Its speed"], 1, "The Concepts glossary defines the chat pattern's trap as defaulting to chat for everything — many tasks need structured UI, not conversation."),
("Copilots are:", ["User replacements", "AI inside workflows — the user stays in control", "Chatbots", "Agents"], 1, "The Concepts note defines copilots as AI inside existing workflows: suggest, complete, accelerate — the user stays in control."),
("Agents fit when:", ["Always", "Multi-step tool use where autonomy pays and failure modes are acceptable", "Never", "It is cheap"], 1, "The Concepts glossary defines the agent fit as multi-step tasks with tool use where autonomy pays — and where the failure modes are acceptable."),
("RAG as a product pattern:", ["Is fine-tuning", "Grounds answers in your data with citations", "Is chat", "Is agents"], 1, "The Concepts note defines RAG as grounding answers in your data with citations — for knowledge tasks where freshness and verifiability matter."),
("Choose patterns by:", ["Hype", "Verifiability, latency, cost, user control — matched to the job", "Trends", "Ease"], 1, "The Concepts glossary defines pattern matching as choosing by verifiability needs, latency, cost, and user control — matched to the job."),
("Summarization and transformation are:", ["Unreliable", "The reliable workhorses where outputs are verifiable", "Boring", "Obsolete"], 1, "The Concepts note defines them as compress, convert, reformat — the reliable workhorses where outputs are verifiable."),
("Eval-driven iteration means:", ["Guessing", "Measure, change, re-measure against evals — iteration with a scoreboard", "Hoping", "Shipping"], 1, "The Concepts glossary defines eval-driven iteration as improving prompts and systems against evals: measure, change, re-measure."),
("In the drill, chat must be argued against for:", ["Every job", "At least one job — naming what structured UI serves better", "No job", "The easy job"], 1, "The Hands-on procedure's step 4 requires writing why chat is the wrong default — what structured UI or pattern serves the job better."),
("The four-axis scorecard covers:", ["Hype, trends, ease, cost", "Verifiability needs, latency, cost, user control", "Speed only", "Price only"], 1, "The procedure's step 5 weighs each pattern on verifiability needs, latency, cost, and user control — the deliberate-matching scorecard."),
("AI product rounds score:", ["Enthusiasm", "Deliberate matching: the job's needs, named failure modes, iteration with a scoreboard", "Speed", "Jargon"], 1, "The Project brief's grading lens: deliberate matching — choose by the job's needs, name failure modes, plan iteration with a scoreboard."),
]}

RETRO["genai-for-pm--eval-ux-ai"] = {
"summary": (
"Welcome back to the GenAI track — I'm your instructor, and this is Module 3: Evaluation and UX for AI. "
"AI products are probabilistic, so their UX and evaluation must be designed for uncertainty: evals that catch "
"regressions, interfaces that communicate confidence, and the discipline to not ship AI where determinism is "
"required. By the end of this module you will design evals with golden datasets and calibrated judges, build "
"human feedback loops, design UX for uncertainty, build trust through transparency, mitigate failure modes in "
"the interface, run the eval-ship-measure loop, and know when not to use AI at all."
),
"concepts": """- **AI evals** — Golden datasets from real usage, judges calibrated to humans, regression on change — the quality gate.
- **Golden dataset** — Representative real cases with known-good answers — the ground truth your evals measure against.
- **Human feedback loops** — Corrections and ratings that improve the system over time — usage funding evaluation.
- **UX for uncertainty** — Confidence display, sources, undo, corrections — honest interfaces for probabilistic outputs.
- **Trust and transparency** — Show what the AI did and why, cite sources, admit limits — trust is designed, not assumed.
- **Failure-mode UX mitigations** — Each known failure gets an interface answer: fallback, escalation, or graceful refusal — designed, not discovered.
- **Iteration loop** — Eval, ship, measure — the cadence that keeps AI features improving after launch.
- **The no-AI decision** — The discipline to not ship AI where determinism is required or errors are catastrophic.""" ,
"procedure": """Run the eval-and-UX drill on an AI feature you would ship — real or simulated.
1. Build the golden dataset on paper: ten representative real cases with the known-good answers — the ground truth.
2. Design the eval: the metrics, the judge (human or calibrated model), and the regression cadence — the quality gate, specified.
3. Design the human feedback loop: what corrections and ratings the product collects, and how they flow back into the system — usage funding evaluation.
4. Sketch the UX for uncertainty: confidence display, sources, undo, corrections — the honest interface for probabilistic outputs.
5. List the feature's three most likely failure modes and write the interface answer for each: fallback, escalation, or graceful refusal — designed, not discovered.
6. Write the transparency spec: what the AI did, why, its sources, its admitted limits — trust designed, not assumed.
7. Run the no-AI test: is determinism required here, or are errors catastrophic? If yes, write the non-AI alternative — the discipline to say no.
8. Present the eval-and-UX plan aloud in ten minutes: the gate, the interface, the mitigations, the no-AI verdict.""",
"brief": """Your interview prep brief: design the eval and UX for an AI feature end to end.
The scenario. Your AI PM loop asks: "Design the evals and the user experience for an AI email-drafting feature — including what happens when it is wrong."
Deliverables.
- A golden dataset spec: ten representative cases with known-good answers.
- An eval design: metrics, judges, regression cadence — the quality gate.
- A UX sketch for uncertainty: confidence, sources, undo, corrections.
- Failure-mode mitigations: the three likeliest failures with their interface answers.
- A transparency spec and the no-AI verdict: would you ship AI here at all?
Grading lens. AI UX rounds score honesty about uncertainty: did you design the gate before the launch, the interface for the failure, and the discipline to refuse AI where it does not belong?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Eval and UX claims must be grounded in systems you have actually measured — fabricated eval scores are the fastest way to lose an interviewer's trust. As of late 2026, eval tooling moves fast: date your tooling claims and verify them.""",
"quiz": [
("AI evals need:", ["Vibes", "Golden datasets, calibrated judges, regression cadence", "Benchmarks only", "Hopes"], 1, "The Concepts glossary defines AI evals as golden datasets from real usage, judges calibrated to humans, regression on change — the quality gate."),
("UX for uncertainty includes:", ["Hiding it", "Confidence, sources, undo, corrections", "More AI", "Less UI"], 1, "The Concepts note defines UX for uncertainty as confidence display, sources, undo, corrections — honest interfaces for probabilistic outputs."),
("Trust is:", ["Assumed", "Designed: show work, cite sources, admit limits", "Earned slowly only", "Irrelevant"], 1, "The Concepts glossary defines trust and transparency as showing what the AI did and why, citing sources, admitting limits — trust is designed, not assumed."),
("Failure modes need:", ["Silence", "Interface answers: fallback, escalation, refusal — designed", "Luck", "Hiding"], 1, "The Concepts note defines failure-mode mitigations as each known failure getting an interface answer — designed, not discovered."),
("Do not use AI where:", ["It is hard", "Determinism is required or errors are catastrophic", "It is easy", "Ever"], 1, "The Concepts glossary defines the no-AI decision as the discipline to not ship AI where determinism is required or errors are catastrophic."),
("A golden dataset is:", ["A benchmark", "Representative real cases with known-good answers — your ground truth", "A demo", "A dream"], 1, "The Concepts note defines the golden dataset as representative real cases with known-good answers — the ground truth evals measure against."),
("Human feedback loops:", ["Are optional", "Turn usage into evaluation: corrections and ratings improving the system", "Replace evals", "Annoy users"], 1, "The Concepts glossary defines human feedback loops as corrections and ratings that improve the system over time — usage funding evaluation."),
("The iteration loop is:", ["Ship and pray", "Eval, ship, measure — the cadence keeping AI features improving", "Eval once", "Ship once"], 1, "The Concepts note defines the iteration loop as eval, ship, measure — the cadence that keeps AI features improving after launch."),
("The no-AI test asks:", ["Is AI cool here", "Is determinism required, or are errors catastrophic — and what is the non-AI alternative", "Is it cheap", "Is it fast"], 1, "The procedure's step 7 runs the no-AI test: determinism required or errors catastrophic means writing the non-AI alternative."),
("AI UX rounds score:", ["Polish", "Honesty about uncertainty: the gate, the interface for failure, the discipline to refuse AI", "Speed", "Features"], 1, "The Project brief's grading lens: honesty about uncertainty — the gate before the launch, the interface for the failure, the discipline to refuse AI."),
]}
