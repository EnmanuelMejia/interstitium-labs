# Content retrofit: IL-13 Fullstack track (modules 22-28 of 56)

M = {
"fullstack-interview-prep--fullstack-arch": {
"summary": ("Welcome to Fullstack Architecture — the opening module of the Fullstack Engineering Interview Prep path. I'm your instructor, and we hold the whole "
"path in one head here: every hop a request takes, the rendering strategies that shape it, and the architecture vocabulary fullstack loops demand. We cover the "
"request path from DNS to render; monolith, modular monolith, and services; the BFF pattern; SSR, SSG, and ISR; and edge/CDN placement. By the end, you will draw "
"the whole path before diving deep — because the diagram is the map."),
"concepts": [
("Request path", "DNS → TCP → TLS → CDN/edge → load balancer → app server → (cache → DB) → response → parse → render — saying the full path aloud is the fullstack flex."),
("Monolith", "One deployable, simplest ops — the honest starting point until a seam proves otherwise."),
("Modular monolith", "Bounded-context modules inside one deployable — the discipline without the distributed tax."),
("Microservices", "Independent deployables — the distributed-systems cost paid only when proven seams demand it."),
("BFF", "Backend-for-Frontend: a thin service per client type aggregating downstream services into exactly the shapes each UI needs — killing over-fetching without leaking topology."),
("SSR", "Render per request: fresh, slower TTFB — personalized dashboards, authenticated content."),
("SSG", "Render at build: fastest, stale until rebuild — marketing pages, docs."),
("ISR", "Static with timed revalidation: fresh without rebuilds — the middle path for mostly-static content that changes."),
("Edge placement", "Static and cacheable dynamic content at CDN PoPs; compute at the edge only when latency demands it; origin as the source of truth."),
("Draw-before-dive", "Establishing shared context first — then both you and the interviewer know where the deep dive lives."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Draw the full request path for an app you know, hop by hop, from DNS to render — then narrate it aloud in under three minutes.",
"For one product, choose the architecture: monolith, modular monolith, or services — write the seam analysis that justifies the call and the condition that would flip it.",
"Decide the rendering strategy per page of a sample site (landing, dashboard, docs, feed): SSG, SSR, or ISR — with the freshness argument for each.",
"Place the edge: mark on your request-path diagram what lives at the CDN, what computes at the edge, and what stays at the origin — with the latency argument per placement.",
"Present the whole-path diagram in 10 minutes to a partner: map first, then one deep dive where they point — practice the draw-before-dive discipline.",
],
"project": ("Whole-path architecture brief. For a product you choose: the request-path diagram with every hop labeled, the architecture decision (monolith → services spectrum) "
"with the seam analysis, per-page rendering strategy with freshness arguments, and the edge-placement map. Deliverable: the brief — the artifact you will adapt live when a "
"fullstack loop asks you to 'design the whole thing.'"),
"honesty": ("Honest scope: 'fullstack' depth is breadth by design — no one is expert at every hop, and this course confers no certificate. Interviewers test whether you can "
"reason across the path and know where your depth ends; claiming depth everywhere is the fastest way to lose credibility."),
},
"fullstack-interview-prep--rest-graphql": {
"summary": ("Welcome to REST and GraphQL — module 2 of the Fullstack path. I'm your instructor, and we take both API styles to decision depth: when REST's cacheability "
"wins, when GraphQL's client-shaped queries win, and how to argue it. We cover REST resource modeling, GraphQL schema/queries/mutations, the honest over/under-fetching "
"comparison, why caching GraphQL is harder, and subscriptions for real-time. By the end, you will choose per surface — because client constraints differ."),
"concepts": [
("REST resource modeling", "Resources as nouns, verbs as actions, status codes as the contract — the cacheable, toolable default."),
("GraphQL schema", "Types, queries, mutations: the typed contract clients shape per request — exact fields, one round trip."),
("Over-fetching", "REST endpoints returning fields the client ignores — wasted bytes, the cost GraphQL eliminates."),
("Under-fetching", "Needing N requests for one screen — chatty on high-latency networks, the cost GraphQL eliminates."),
("GraphQL caching cost", "A single endpoint with arbitrary query shapes defeats HTTP caching and simple per-route limits — the price of client-shaped queries; query-cost analysis required."),
("N+1 resolvers", "Per-field resolvers firing per row — the GraphQL performance trap, fixed by batching (dataloaders)."),
("Subscriptions", "GraphQL's real-time primitive — server-pushed updates over a persistent connection for live data."),
("Per-surface choice", "Client constraints (bandwidth, latency, capabilities) decide the contract shape — not architectural purity."),
("Caching as a tradeoff", "What to cache, where, the invalidation strategy, the failure story — 'caching is a tradeoff with an invalidation plan, not a speedup.'"),
("Polling vs SSE vs WebSockets", "Polling: simple, wasteful. SSE: server→client stream, auto-reconnect. WebSockets: full duplex — weakest sufficient tool per direction and frequency."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Model one screen's data needs twice: as REST endpoints (count the requests and wasted fields) and as one GraphQL query — write the over/under-fetching ledger for both.",
"Write the caching plan for the REST version (HTTP cache semantics, CDN, invalidation) and then for the GraphQL version (query hashing, persisted queries, cost limits) — compare the machinery.",
"Diagnose an N+1 resolver scenario on paper: per-row field resolvers, the query count explosion, then the dataloader batching fix — state the before/after query counts.",
"Choose the real-time mechanism for three features (notifications, chat, live dashboard): direction, frequency, weakest sufficient tool — with the rejected options named.",
"Argue one per-surface decision aloud in two minutes: 'mobile feed → GraphQL because…, public API → REST because…' — verdict plus the flip condition.",
],
"project": ("API-strategy brief. For a two-client product (web + mobile): the REST surface (resources, caching plan, invalidation) and the GraphQL surface (schema sketch, "
"caching strategy, query-cost limits, dataloader plan), the per-surface decision with client-constraint arguments, and the real-time choice per live feature. Deliverable: "
"the brief — both styles at decision depth, argued not assumed."),
"honesty": ("Honest scope: the REST/GraphQL debate is context-shaped — team skill, client mix, and existing infrastructure decide more than theory, and this course confers "
"no certificate. Interviewers score the honest comparison; partisanship for either style reads as inexperience."),
},
"fullstack-interview-prep--auth-identity": {
"summary": ("Welcome to Auth and Identity — module 3 of the Fullstack path. I'm your instructor, and this is auth without hand-waving: the flows, the token lifecycle, "
"and the storage decisions — the topic where bluffing is most visible and most punished. We cover sessions versus tokens, JWT structure and validation, the OAuth 2.0 "
"authorization code flow, OpenID Connect on top, and password hashing with bcrypt and Argon2. By the end, you will answer auth with threat models, not library names."),
"concepts": [
("Sessions", "Server-side state keyed by cookie — revocable instantly, needs a shared store at scale; the stateful default."),
("Tokens (JWT)", "Stateless, self-contained — scales horizontally, but revocation needs denylists or short expiry; the stateless tradeoff."),
("JWT structure", "header.payload.signature, base64url — claims like sub, exp, iat; signed, not encrypted: never put secrets in claims."),
("JWT validation", "Signature with the right key and algorithm (never 'none'), expiry, issuer, audience — every one checked, every time."),
("OAuth 2.0 authorization code flow", "User → client redirects to auth server → approval → short-lived single-use code → code (+ secret, PKCE for public clients) exchanged for tokens; tokens never touch the browser URL."),
("PKCE", "code_verifier/code_challenge pair protecting public clients (mobile/SPA) that can't keep a secret — prevents authorization-code interception."),
("OpenID Connect", "The identity layer on top of OAuth 2.0: standardized ID tokens for 'who is this user' — SSO's building block."),
("Password hashing", "Never encrypt (reversible) — hash with a memory-hard salted function: Argon2id preferred, bcrypt acceptable; per-user salt; work factor tuned so login takes hundreds of milliseconds."),
("Refresh token storage", "httpOnly secure cookies, rotated on use — the answer to 'where do refresh tokens live.'"),
("JWT revocation", "The honest answer: short-lived access tokens plus refresh-token rotation and denylists — statelessness means bounding the exposure window, not central killing."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Draw the authorization code flow with PKCE end to end: every redirect, the code exchange, where each token lives — then narrate it aloud in three minutes.",
"Write the JWT validation checklist for a resource server: algorithm, signature key, exp, iss, aud — then list what breaks if each check is skipped.",
"Compare sessions vs tokens for two products (a bank dashboard, a content API): revocation needs, scale needs, the verdict per product with reasons.",
"Write the password-storage spec: algorithm choice, salt strategy, work-factor target, and the 'never roll your own crypto' rule — as you'd state it in an interview.",
"Answer the three senior-loop auth questions aloud: 'how do you revoke a JWT?', 'where do refresh tokens live?', 'how do you do SSO?' — threat model first, mechanism second.",
],
"project": ("Auth design brief. For a two-client product: the flow choice (sessions vs tokens, with the revocation analysis), the OAuth/OIDC integration sketch, the JWT "
"validation checklist, refresh-token storage and rotation policy, and the password-hashing spec. Include the threat model: what each decision defends against. "
"Deliverable: the brief — auth argued from threat models."),
"honesty": ("Honest scope: auth is the topic where overconfidence is dangerous — real systems add key rotation, breach response, and compliance that interviews skip, "
"and this course confers no certificate. State the threat model honestly; 'it depends on the threat model' is a senior answer, not evasion."),
},
"fullstack-interview-prep--fullstack-data": {
"summary": ("Welcome to Data Across the Stack — module 4 of the Fullstack path. I'm your instructor, and this is data end to end: validation at every boundary, the "
"ORM/SQL tradeoff, and keeping client state and the database telling the same story. We cover validation layers from form to row, ORMs versus query builders versus "
"raw SQL, migrations in a deployed app, full-text search basics, file uploads with object storage, and client-cache/DB consistency. By the end, you will trace a datum "
"from the form field to the row — and back."),
"concepts": [
("Validation layers", "Client for UX, API boundary for trust, database constraints for the last line of defense — never trust the client alone."),
("ORM tradeoff", "Speed of development with relationships as objects — watch N+1 and leaky abstractions on complex queries; 'ORM for CRUD, SQL where it earns it.'"),
("Query builders", "Composable SQL without string soup — the middle path between ORM magic and raw strings."),
("Migrations in production", "Expand-contract: backward-compatible steps, old and new code coexisting, old shape removed after readers move."),
("Inverted index", "Terms → documents: tokenization, stemming, ranking (TF-IDF/BM25) — Postgres tsvector for the simple case, dedicated engines at scale."),
("Presigned uploads", "Clients upload straight to object storage — app servers never proxy the bytes; async processing (thumbnails, scans) via queues."),
("Optimistic updates", "UI applies the mutation immediately with a rollback path for server rejection — optimism as a UX bet, the rollback as the hedge."),
("Client/DB consistency", "Server as source of truth; client cache as a performance layer with invalidation tied to mutations — allowed to be briefly wrong, never permanently."),
("Senior answer structure", "Three beats for any deep-dive: one-sentence definition, the mechanism, when it fits and its key tradeoff — then stop and invite the follow-up."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Trace one form submission end to end: client validation, API validation, DB constraints — write what each layer catches that the others can't.",
"Take an ORM query with an N+1 smell: find it, fix it with eager loading, then drop to raw SQL for the reporting query — state the layer choice each time.",
"Write the expand-contract migration for renaming a column on a live table: the steps, the dual-read period, the cleanup — with the rollback at each step.",
"Sketch full-text search for a product catalog: tsvector vs dedicated engine — the scale and faceting arguments that decide.",
"Design the upload flow: presigned URL, direct-to-storage, async processing queue, CDN reads — draw the bytes' path and name what never touches the app server.",
],
"project": ("Data-flow brief. For your capstone-shaped app: the validation map (what each layer enforces), the ORM/SQL layering with the N+1 audit, the migration plan for "
"the first three schema changes, the search approach with the scale argument, and the upload pipeline. Deliverable: the brief — data traced from form to row, every layer justified."),
"honesty": ("Honest scope: data-layer taste is workload-shaped — the ORM/SQL split, the search engine, the migration strategy all answer to scale and team, and this course "
"confers no certificate. The interview tests the reasoning chain; production adds the constraints of the system you inherited."),
},
"fullstack-interview-prep--deploy-ops-lite": {
"summary": ("Welcome to Deployment Literacy — module 5 of the Fullstack path. I'm your instructor, and this is enough operations to be dangerous in the good way: "
"pipelines, environments, containers, and rollbacks — the literacy fullstack interviews assume. We cover CI/CD (build, test, deploy), environments and feature flags, "
"what Docker actually gives you, observability (logs, metrics, traces), and rollback strategies. By the end, you will describe a deployment the way an owner does."),
"concepts": [
("CI", "Every push builds, lints, tests, scans — fast feedback on main; the definition of done, enforced mechanically."),
("CD", "Artifacts promoted through environments with automated deployments (blue-green/canary/rolling) and one-command rollback — lead time and change-failure rate as the metrics."),
("Feature flags", "Decouple deploy from release: merge dark, release to 1%, kill-switch without redeploying — with flag hygiene (owner + removal date) or flag spaghetti."),
("Environments", "Dev → staging → production with promotion discipline — staging that mirrors production is the point, not the checkbox."),
("Docker", "Portable, reproducible runtime: image bundles code + dependencies + OS userland — containers share the host kernel (lighter than VMs, weaker isolation)."),
("Blue-green rollback", "Instant: flip the router back to the still-running previous environment — rollback as a route change, rehearsed not hoped."),
("Observability trio", "Metrics alert, traces show where, logs tell why — 'metrics alert me, traces show me where, logs tell me why.'"),
("Rollback rehearsal", "Immutable artifacts, previous version one command away, backward-compatible migrations — an untested rollback plan is a hope."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Sketch the CI/CD pipeline for your capstone: triggers, parallel jobs (lint/test/build/scan), artifact promotion, environments — with the gate that blocks a bad merge.",
"Write the feature-flag plan for one risky launch: flag name, owner, rollout percentages, kill-switch procedure, removal date — the hygiene, not just the flag.",
"Containerize a toy app: write the Dockerfile, note the layer-caching order, shrink the image — then state what Docker did and didn't give you versus a VM.",
"Design the rollback for one deploy: immutable artifact, blue-green or canary, the router flip, the migration-compatibility check — then rehearse it on paper.",
"Write the observability starter set: three alerting metrics, what each log line carries, where you'd add the first trace — the owner's minimum.",
],
"project": ("Deployment runbook. For your capstone app: the CI/CD pipeline definition, environment promotion rules, the feature-flag register (with owners and removal dates), "
"the container strategy, and the rollback runbook — including the migration-compatibility rule and the rehearsal log. Deliverable: the runbook — deployment literacy written down."),
"honesty": ("Honest scope: 'deployment literacy' is literacy, not operations expertise — real on-call involves incidents, cost, and compliance this module doesn't simulate, "
"and this course confers no certificate. The interview tests whether you think like an owner; the pager teaches the rest."),
},
"fullstack-interview-prep--fullstack-capstone": {
"summary": ("Welcome to the Fullstack Capstone — module 6 of the Fullstack path. I'm your instructor, and this is the artifact that answers 'show me you can own the "
"whole path': one deployed app, contract-first, with auth and CI. We scope a shippable app, write the API contract first, build auth and the data model, deploy with "
"CI, and write the README and demo script — then present the build. By the end, you will demo value and narrate judgment."),
"concepts": [
("Shippable scope", "The thinnest slice demonstrating the skill: contract first, auth + data model, deployed with CI, README and demo script — shipped and demoable beats ambitious and half-built."),
("Contract-first", "Interface decisions early when they're cheap — frontend and backend evolve independently against the contract."),
("Auth in the capstone", "Real login with the threat model stated: what you chose (sessions vs tokens) and what it defends against."),
("CI on the capstone", "The pipeline as proof of process: every push tested, every deploy gated — the definition of done, visible."),
("README as interview", "'The README is the interview before the interview': what it does, how to run it, architecture in one diagram, decisions and tradeoffs."),
("Demo script", "The 3-minute happy path with one 'and here's the interesting part' beat — rehearsed, not improvised."),
("Presenting the build", "Live demo, then architecture (one diagram), then the two hardest decisions with alternatives, then 'what I'd do with more time.'"),
("Scope discipline", "'What I'd do with more time' proves the build was scoped deliberately, not abandoned — a senior signal."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Scope the capstone in one page: the thinnest shippable slice, the explicit non-goals, the contract-first order of work — get the scope signed off (by a peer or yourself, in writing).",
"Write the API contract before any code: endpoints, schemas, status codes, error model, auth, rate limits — the interface the build must satisfy.",
"Build vertical slices: auth + one full feature path end to end (UI → API → DB → deploy) before adding breadth — demoable at every commit.",
"Wire CI on day one: every push builds and tests, deploys gated — the pipeline grows with the app, not after it.",
"Write the README and demo script, then present: live demo, one architecture diagram, two hardest decisions, 'what I'd do with more time' — record it.",
],
"project": ("The capstone itself. Ship it: scoped app, contract-first API, auth with a stated threat model, data model with migrations, CI/CD, deployed and demoable — plus "
"the README (run instructions, one architecture diagram, decisions and tradeoffs) and the 3-minute demo script. Deliverable: the deployed app, the repo, the README, "
"and the recorded demo — the artifact that answers 'show me.'"),
"honesty": ("Honest scope: a capstone proves you can ship a scoped thing well — it doesn't prove production experience (no real users, no incidents, no legacy), and this "
"course confers no certificate. Present it as what it is: evidence of craft and judgment, sized honestly."),
},
"fullstack-interview-prep--fullstack-mock": {
"summary": ("Welcome to the Fullstack Mock Circuit — the final module of the Fullstack path. I'm your instructor, and these are mocks that cross the stack in one "
"round: API design, data model, a UI sketch, auth deep dives, live coding across the stack — debriefed into the final study plan. By the end, you will timebox visibly, "
"demo thin working slices, and convert every mock into the plan."),
"concepts": [
("Full-path design round", "Design the path first (10 min), then code the thinnest vertical slice (API + one screen) — 'a thin working slice beats a thick imaginary one.'"),
("Timed API-design round", "5 requirements, 10 resources + verbs + status codes, 10 edge cases, 5 tradeoffs — the contract a client could program against."),
("Auth deep dive", "Threat model first, mechanism second: the senior-loop auth questions answered with the storage and lifecycle reasoning."),
("Live coding across the stack", "Timeboxed visibly: design, then the thinnest slice, narrating tradeoffs — breadth demonstrated through the slice, not described."),
("Behavioral ledger", "Story bank, stories-told-where, feedback, stumping questions — every behavioral touchpoint fresh."),
("Debrief and triage", "Within the hour: leaks, holds, biggest leak by frequency × weight, 48-hour redrill — the mock is the test, the debrief is the studying."),
("Taper plan", "No new material, redrill from the log, timed mocks, rest — consolidation for the real loop."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Run a timed full-path design mock (45 min): 10 min path design, then the thinnest vertical slice — narrate tradeoffs, timebox visibly.",
"Run an API + auth deep-dive mock: defend the contract and the threat model against follow-ups — mechanism over buzzwords.",
"Run a live-coding-across-the-stack mock: one feature from UI to DB in the timebox — thin slice, working, narrated.",
"Run one behavioral round from the ledger: two-minute STAR answers, no repeated stories.",
"Debrief all four within the hour each: template, ranked leaks, 48-hour redrills, ledger update — then the taper plan.",
],
"project": ("Fullstack mock portfolio. The four-mock circuit over two weeks — full-path design, API/auth deep dive, live coding across the stack, behavioral — each "
"debriefed with the template and the ledger updated. Close with the taper schedule for your real loop. Deliverable: four debriefs, the ledger, the taper — mocks converted into the final study plan."),
"honesty": ("Honest scope: crossing the stack in a mock is still a simulation — real loops add unfamiliar interviewers, real nerves, and company-specific bars, and this "
"course confers no certificate. What the circuit buys is the timeboxing habit and the leak log — the two things that compound."),
},
}
