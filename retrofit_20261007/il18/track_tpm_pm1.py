# Technical PM track, part 1: technical-depth-pm, api-platform-thinking
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["technical-pm-interview-prep--technical-depth-pm"] = {
"summary": (
"Welcome to the Technical Product Management track — I'm your instructor, and this is Module 1: Technical "
"Depth for PMs. Enough engineering to be dangerous in the good way: how systems are built, where they break, "
"and how to reason about scale — the depth technical PM interviews actually test. By the end of this module "
"you will reason about the web at PM altitude, compare databases by access pattern, weigh caching's speed "
"against staleness, use queues for async scale, read technical docs for commitments, and estimate scale with "
"sane round-number math."
),
"concepts": """- **The web at PM altitude** — Requests and responses over HTTP; latency from network + compute + data — enough to reason about performance tradeoffs.
- **Relational versus document databases** — Relational: structured, joins, strong consistency. Document: flexible schema, nested data, scale-out — match to the access pattern.
- **Caching** — What it buys: speed — fewer origin hits, lower latency. What it risks: staleness — invalidation strategy is the real design work.
- **Queues and async processing** — Decoupling slow work from the request path — reliability and scale via buffering and retries.
- **System-design literacy (PM)** — Components, data flow, bottlenecks, failure modes — enough to connect architecture choices to user outcomes and cost.
- **Reading technical docs and RFCs** — Reading for decisions and contracts: what is promised, what is assumed, what can change — the PM reads for commitments.
- **Scale estimation** — Users → requests per second → storage → bandwidth, assumptions stated — round-number math, sanity-checked.""" ,
"procedure": """Run the technical-depth rep set. Work each rep on paper — reasoning, not trivia.
1. Trace a web request at PM altitude: browser → DNS → load balancer → app → database — and name where latency comes from at each hop.
2. Compare databases for a real product you know: write the access pattern, then choose relational or document — and justify the choice by the pattern, not by fashion.
3. Weigh a caching decision: what it buys (speed, fewer origin hits) against what it risks (staleness) — and write the invalidation strategy, which is the real design work.
4. Design an async path: pick a slow operation and decouple it with a queue — buffering, retries, and what happens when the queue backs up.
5. Read a technical doc or RFC section for commitments: what is promised, what is assumed, what can change — write the three lists.
6. Estimate scale sanely: users → requests per second → storage → bandwidth, assumptions stated, round numbers — then sanity-check the answer.
7. Present one rep aloud in five minutes: the tradeoff you weighed and the reasoning chain — the PM's technical performance.""",
"brief": """Your interview prep brief: prove technical depth on a system you can defend.
The scenario. Your technical PM loop opens with: "Walk me through how this product works technically, and where it would break at 10x scale."
Deliverables.
- A web-request trace with latency sources named per hop.
- A database choice justified by access pattern.
- A caching decision with the invalidation strategy written out.
- An async design: the queue, the retries, the backpressure plan.
- A doc/RFC commitment read: promised, assumed, changeable.
- A scale estimate: users → RPS → storage → bandwidth, sanity-checked.
Grading lens. Technical depth rounds score the reasoning chain: did you connect architecture choices to user outcomes and cost, weigh tradeoffs explicitly, and read for commitments — without bluffing?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Technical depth must be real: trace systems you actually understand, estimate with math you can defend, and never present borrowed architecture opinions as your own. "I would need to ask the engineers" is a respectable answer when it is true.""",
"quiz": [
("Caching trades:", ["Nothing", "Speed for staleness risk — invalidation is the design work", "Money for speed", "Users for data"], 1, "The Concepts glossary defines caching as speed bought with staleness risk — the invalidation strategy is the real design work."),
("Queues decouple:", ["Teams", "Slow work from the request path — reliability via buffering", "Databases", "APIs"], 1, "The Concepts note defines queues and async processing as decoupling slow work from the request path — reliability and scale via buffering and retries."),
("Estimate scale via:", ["Guessing", "Users → RPS → storage → bandwidth, assumptions stated", "Vendor quotes", "Hoping"], 1, "The Concepts glossary defines scale estimation as users → requests per second → storage → bandwidth, assumptions stated — round-number math, sanity-checked."),
("Relational versus document:", ["The same", "Relational: structured + joins; document: flexible + scale-out — match the access pattern", "Old versus new", "SQL versus nothing"], 1, "The Concepts note compares them by access pattern: relational for structured data with joins and strong consistency; document for flexible schema and scale-out."),
("PM system-design literacy:", ["Unneeded", "Connects architecture choices to user outcomes and cost", "Replaces engineers", "Is trivia"], 1, "The Concepts glossary defines PM system-design literacy as components, data flow, bottlenecks, failure modes — enough to connect architecture choices to user outcomes and cost."),
("Latency at PM altitude comes from:", ["Magic", "Network + compute + data across the request path", "The user", "The logo"], 1, "The Concepts note defines the web at PM altitude as requests and responses over HTTP, with latency from network + compute + data."),
("Reading technical docs as a PM means reading for:", ["Grammar", "Commitments: what is promised, assumed, changeable", "Length", "Authorship"], 1, "The Concepts glossary defines reading technical docs as reading for decisions and contracts — what is promised, what is assumed, what can change."),
("The database choice is justified by:", ["Fashion", "The access pattern — how the data is actually read and written", "The vendor", "The price"], 1, "The procedure's step 2 requires justifying the choice by the access pattern, not by fashion."),
("Async design must name what happens when:", ["It succeeds", "The queue backs up — the backpressure plan", "It is fast", "Nobody watches"], 1, "The procedure's step 4 requires the backpressure plan: buffering, retries, and what happens when the queue backs up."),
("Technical depth rounds score:", ["Trivia", "The reasoning chain — tradeoffs explicit, commitments read, no bluffing", "Speed", "Jargon"], 1, "The Project brief's grading lens: the reasoning chain — architecture tied to user outcomes and cost, tradeoffs explicit, no bluffing."),
]}
