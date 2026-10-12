# Technical PM track, part 2: api-platform-thinking, data-literacy-pm
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["technical-pm-interview-prep--api-platform-thinking"] = {
"summary": (
"Welcome back to the Technical PM track — I'm your instructor, and this is Module 2: API and Platform "
"Thinking. APIs are products with developer customers. This module covers design tradeoffs, versioning "
"discipline, and the unglamorous contract work that decides whether a platform gets adopted. By the end of "
"this module you will discuss REST tradeoffs credibly, weigh versioning as a compatibility promise, choose "
"between webhooks and polling deliberately, think in platforms versus products, and treat developer experience "
"as the product."
),
"concepts": """- **REST literacy** — Resources, methods, status codes — the vocabulary for discussing API design tradeoffs credibly.
- **API design tradeoffs** — Granularity, consistency, evolvability — each choice taxes some consumers to benefit others; name who pays.
- **Versioning** — Compatibility promises that let developers build without fear — versioning discipline decides platform adoption.
- **Webhooks versus polling** — Webhooks: push, real-time, needs receiver infra. Polling: pull, simple, wasteful — match to latency needs and consumer capability.
- **Platform versus product** — Different customers: platform customers are developers — their product is your API's developer experience. Different users, different success metrics.
- **Developer experience (DX)** — Docs, SDKs, errors, onboarding — the DX is the UI of a platform; it decides adoption.
- **Rate limits, auth, and the boring parts** — The unglamorous contract work: auth, limits, idempotency, deprecation promises — the parts that keep platforms alive.""" ,
"procedure": """Run the API-design rep. Design an API for a partner integration you know — real or simulated — on paper.
1. Start with consumers and use cases: who calls this API, what jobs are they doing — consumers before endpoints.
2. Sketch the resources and methods: name the resources, the verbs, and the status-code vocabulary — REST literacy in practice.
3. Weigh the design tradeoffs: granularity, consistency, evolvability — and write down who pays for each choice.
4. Write the versioning and compatibility promise: what can change, what cannot, how deprecation works — the contract developers build on.
5. Choose webhooks versus polling for the event story: match to latency needs and consumer capability — and justify the choice in writing.
6. Design the boring parts: auth, rate limits, error shapes, idempotency — the contract work that keeps platforms alive.
7. Audit the DX: docs, SDKs, errors, onboarding — would a developer adopt this? Write the three friction points you would fix first.
8. Present the design aloud in ten minutes: consumers, tradeoffs, contract, DX — as you would in the API design round.""",
"brief": """Your interview prep brief: design an API as a product and defend it.
The scenario. Your technical PM loop includes an API design round: "Design an API that lets partners pull order data and receive fulfillment events." No code — design and judgment.
Deliverables.
- A consumer-first design: use cases, resources, methods, status codes.
- A tradeoff memo: granularity, consistency, evolvability — who pays for each choice.
- A versioning and compatibility promise: change rules and the deprecation path.
- A webhooks-versus-polling decision with the justification.
- The boring-parts spec: auth, rate limits, error shapes, idempotency.
- A DX audit: the three friction points you would fix first for adoption.
Grading lens. API rounds score consumer thinking: did you start from developers' jobs, make tradeoffs explicit, write a contract developers could trust — and treat DX as the product?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. API judgment must be grounded in APIs you have actually used, built, or integrated — interviewers will ask about the tradeoffs you personally weighed. Borrowed API opinions read as documentation recitation; owned tradeoffs read as product judgment.""",
"quiz": [
("REST literacy covers:", ["Cooking", "Resources, methods, status codes", "GraphQL only", "SOAP"], 1, "The Concepts glossary defines REST literacy as resources, methods, status codes — the vocabulary for discussing API design tradeoffs credibly."),
("Versioning is:", ["Vanity", "A compatibility promise — the contract deciding adoption", "Optional", "Free"], 1, "The Concepts note defines versioning as compatibility promises letting developers build without fear — versioning discipline decides platform adoption."),
("Webhooks versus polling:", ["The same", "Push/real-time versus pull/simple — match to latency needs", "Old versus new", "Fast versus slow"], 1, "The Concepts glossary contrasts them: webhooks are push and real-time but need receiver infra; polling is pull, simple, wasteful — match to latency needs and consumer capability."),
("Platform customers are:", ["End users", "Developers — DX is the product", "Nobody", "Everyone"], 1, "The Concepts note defines platform versus product: platform customers are developers — different users, different success metrics."),
("DX decides:", ["Nothing", "Adoption — docs, SDKs, errors, onboarding", "Price", "Speed"], 1, "The Concepts glossary defines developer experience as docs, SDKs, errors, onboarding — the DX is the UI of a platform; it decides adoption."),
("API design tradeoffs require naming:", ["The winner", "Who pays — each choice taxes some consumers to benefit others", "The framework", "The vendor"], 1, "The Concepts note defines API design tradeoffs as granularity, consistency, evolvability — each choice taxes some consumers; name who pays."),
("API design starts with:", ["Endpoints", "Consumers and use cases", "Code", "Documentation"], 1, "The Hands-on procedure's step 1 starts with consumers and use cases — consumers before endpoints."),
("The boring parts that matter include:", ["Logos", "Auth, rate limits, error shapes, idempotency, deprecation promises", "Colors", "Fonts"], 1, "The Concepts glossary defines the boring parts as the unglamorous contract work — auth, limits, idempotency, deprecation — that keeps platforms alive."),
("The deprecation promise belongs in:", ["The marketing site", "The versioning and compatibility contract developers build on", "The footer", "Nowhere"], 1, "The procedure's step 4 writes the versioning and compatibility promise — what can change, what cannot, how deprecation works."),
("API rounds score:", ["Syntax", "Consumer thinking: contracts, versioning, DX — APIs as products", "Speed", "Trivia"], 1, "The Project brief's grading lens: consumer thinking — starting from developers' jobs, explicit tradeoffs, a trustworthy contract, DX as the product."),
]}

RETRO["technical-pm-interview-prep--data-literacy-pm"] = {
"summary": (
"Welcome back to the Technical PM track — I'm your instructor, and this is Module 3: Data Literacy for PMs. "
"Technical PMs live in data: querying it, instrumenting it, and knowing when it misleads. This module builds "
"hands-on literacy with the tools analysts actually use. By the end of this module you will write the SQL a "
"PM actually needs, design event instrumentation and taxonomies, read funnels and cohorts, build dashboards "
"that answer questions, stay data-informed rather than data-driven, spot lying data, and work with data teams "
"effectively."
),
"concepts": """- **SQL literacy (PM)** — Joins, aggregations, window functions — enough to answer your own questions without waiting in the analytics queue.
- **Event instrumentation** — Defining the events and properties the product emits — the data foundation; garbage taxonomy, garbage analysis.
- **Taxonomy** — The naming contract for events and properties: consistent, documented, versioned — the difference between analysis and archaeology.
- **Funnels and cohorts** — Funnels: where users drop. Cohorts: how behavior differs by group and over time — the PM's diagnostic pair.
- **Decision dashboards** — Designed around decisions, not data availability — every chart should imply an action.
- **Data-informed versus data-driven** — Informed: data inputs to judgment. Driven: judgment abdicated to data — know which you are doing.
- **Lying data** — Instrumentation bugs, selection bias, Simpson's paradox, vanity metrics — skepticism is a data skill.
- **Working with data teams** — Clear questions, shared definitions, realistic timelines — the partnership that keeps analysis trustworthy.""" ,
"procedure": """Run the data-literacy rep set. Use a product you know — real or simulated — and work the data by hand.
1. Write three SQL queries a PM actually needs: a join across two tables, an aggregation by day, and a window function ranking users — answer your own question.
2. Design the event taxonomy for one user flow: the events, the properties, the naming contract — garbage taxonomy means garbage analysis.
3. Sketch the funnel for that flow and a cohort comparison: where users drop, how behavior differs by group — the diagnostic pair.
4. Design a decision dashboard: three charts maximum, each implying an action — designed around decisions, not data availability.
5. Write the data-informed decision memo: the data, your judgment, and which one carried the decision — know which you are doing.
6. Play skeptic: invent three ways your own dashboard could be lying — instrumentation bug, selection bias, Simpson's paradox — and how you would check each.
7. Write the data-team request: the question, the definitions, the timeline — the partnership brief that gets good analysis back.""",
"brief": """Your interview prep brief: deliver the data-literacy portfolio page.
The scenario. Your technical PM loop tests whether you can work data without an analyst on speed-dial: "How would you measure this feature's success, and how would you know the data is lying?"
Deliverables.
- Three working SQL queries: join, aggregation, window function — answering a real product question.
- An event taxonomy for one user flow: events, properties, naming contract.
- A funnel sketch plus a cohort comparison with the diagnostic read.
- A three-chart decision dashboard where every chart implies an action.
- A skepticism audit: three ways the data could lie, and how you would check each.
Grading lens. Data rounds score independence and skepticism: can you answer your own questions, instrument before analyzing, design for decisions — and distrust your own dashboard on purpose?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. Data literacy must be practiced on data you actually understand — fabricated analyses teach fabricated judgment. In the round, show queries you have written and taxonomies you have designed; never present a borrowed dashboard as your own work.""",
"quiz": [
("PM SQL needs:", ["Nothing", "Joins, aggregations, windows — answer your own questions", "Admin rights", "DBA skills"], 1, "The Concepts glossary defines PM SQL literacy as joins, aggregations, window functions — enough to answer your own questions without the analytics queue."),
("Bad taxonomy gives:", ["Insights", "Garbage analysis — instrumentation is the foundation", "Speed", "Nothing"], 1, "The Concepts note defines event instrumentation as the data foundation: garbage taxonomy, garbage analysis."),
("Funnels diagnose:", ["Revenue directly", "Where users drop — the vital signs", "Costs", "Nothing"], 1, "The Concepts glossary defines funnels as showing where users drop — the PM's diagnostic pair with cohorts."),
("Data-informed means:", ["Obeying data", "Data inputs to judgment — humans decide", "Ignoring data", "Guessing"], 1, "The Concepts note distinguishes informed from driven: informed means data inputs to judgment; driven abdicates judgment to data."),
("Data lies via:", ["Honesty", "Instrumentation bugs, bias, Simpson's paradox, vanity metrics", "Size", "Speed"], 1, "The Concepts glossary defines lying data as instrumentation bugs, selection bias, Simpson's paradox, vanity metrics — skepticism is a data skill."),
("Decision dashboards are designed around:", ["Data availability", "Decisions — every chart should imply an action", "Beauty", "Volume"], 1, "The Concepts note defines decision dashboards as designed around decisions, not data availability — every chart implies an action."),
("Cohorts show:", ["Totals", "How behavior differs by group and over time", "Averages", "Nothing"], 1, "The Concepts glossary defines cohorts as behavior compared by group and over time — the diagnostic pair with funnels."),
("The skepticism audit exists because:", ["Distrust is fun", "Your own dashboard can lie — instrumentation bugs, bias, and paradoxes are a data skill to hunt", "Analysts err", "Tools fail"], 1, "The procedure's step 6 plays skeptic on your own dashboard — the Concepts note calls skepticism a data skill."),
("Working with data teams starts with:", ["Demands", "Clear questions, shared definitions, realistic timelines", "SQL", "Silence"], 1, "The Concepts glossary defines working with data teams as clear questions, shared definitions, realistic timelines — the partnership keeping analysis trustworthy."),
("Data rounds score:", ["Tool trivia", "Independence and skepticism: own queries, designed instrumentation, deliberate distrust", "Speed", "Chart beauty"], 1, "The Project brief's grading lens: independence and skepticism — answer your own questions, instrument before analyzing, distrust your dashboard on purpose."),
]}
