# Content retrofit: IL-13 Backend track (modules 8-14 of 56)

M = {
"backend-interview-prep--api-design-patterns": {
"summary": ("Welcome to API Design Patterns — the opening module of the Backend Engineering Interview Prep path. I'm your instructor, and we treat APIs as the "
"product here: resource modeling, idempotent mutations, and error contracts — the design judgment backend interviews probe first. We cover REST (resources, "
"verbs, status codes), idempotency and safe retries, pagination, filtering and versioning, GraphQL's honest tradeoffs, and gRPC contract-first design. By the "
"end, you will design a contract a client team could program against — and defend every choice in it."),
"concepts": [
("REST", "Resources as nouns in URLs, HTTP verbs as actions, status codes as the contract (200/201/400/401/403/404/429/500), stateless requests — plus the judgment calls: pagination, filtering, idempotency."),
("Idempotency", "'Safe to retry': repeating the request doesn't change the outcome beyond the first application — designed with idempotency keys on writes, paired with exponential backoff + jitter."),
("Cursor pagination", "Keyset paging relative to a stable key: immune to the shifting-row problem of offset, stable under inserts — the choice for feeds; offset remains fine for admin UIs."),
("GraphQL tradeoffs", "Client-shaped queries that fix over/under-fetching — at the cost of harder caching, query-complexity limits, and N+1 resolvers needing batching (dataloaders)."),
("gRPC", "Service-to-service inside the trust boundary: binary protobufs, strict .proto contracts, streaming RPCs — poor browser support keeps it off public APIs."),
("Error contracts", "Errors clients can program against: stable codes, messages, and request IDs for correlation — the contract's unhappy-path half."),
("Versioning", "How the contract evolves without breaking clients: URL, header, or additive-only evolution — a decision, not an afterthought."),
("Safe retries", "Retries that can't corrupt: idempotent endpoints plus backoff with jitter — the client-side half of reliability."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Model a small API's resources as nouns: list the resources, assign verbs, and write the status code each endpoint returns for success and for the three most likely failures.",
"Add idempotency to one mutating endpoint: design the idempotency-key header, the server-side key store, and the replay response — then write the retry policy (backoff + jitter) a client would use.",
"Compare offset vs cursor pagination for a feed endpoint: write both, insert rows mid-page in a test, and observe which one skips or duplicates.",
"Write the GraphQL-vs-REST decision for one product surface: name the over/under-fetching cost, the caching cost, and the verdict with the condition that would flip it.",
"Sketch a .proto contract for one internal service: messages, RPCs, and one streaming RPC — then list what breaks if a field is renamed (the contract-evolution lesson).",
],
"project": ("Public API contract. Design the full contract for a rate-limited public API (the companion build in this path's design module): resources and verbs, "
"status codes, the error model with request IDs, idempotency keys on writes, cursor pagination on list endpoints, versioning strategy, and the rate-limit headers "
"(429, RateLimit-*, Retry-After). Write it as an OpenAPI-style sketch a client team could build against. Deliverable: the contract document — the interface before the implementation."),
"honesty": ("Honest scope: API design taste is argued, not certified — conventions differ across companies, and this course confers no certificate. The contract you "
"write here is practice for defending judgment calls aloud; real APIs also answer to existing clients, legacy, and org politics."),
},
"backend-interview-prep--data-layer": {
"summary": ("Welcome to Databases and the Data Layer — module 2 of the Backend path. I'm your instructor, and this is the data layer interviews actually test: "
"index design, isolation levels, and the honest SQL-versus-NoSQL decision — not trivia, judgment. We cover schema design and normalization, B-tree/covering/composite "
"indexes, transactions and isolation levels, the NoSQL families, and connection pooling with the N+1 trap. By the end, you will argue storage choices from access patterns."),
"concepts": [
("Normalization", "1NF→2NF→3NF: atomic values, no partial or transitive dependencies — normalize by default, denormalize deliberately by measurement, documenting why."),
("B-tree index", "Turns O(n) scans into O(log n) lookups on indexed columns — at the cost of write overhead and storage; the workhorse of relational access."),
("Composite index", "Multi-column index serving filters left-to-right — column order follows the query patterns, not the table definition."),
("Covering index", "An index that answers the query without touching the table — the read-path optimization that removes the heap fetch."),
("Isolation levels", "The ladder: read uncommitted → read committed → repeatable read → serializable — trading anomalies (dirty reads, non-repeatable reads, phantoms) for concurrency."),
("NoSQL families", "Document (flexible JSON), key-value (single-key lookups), wide-column (massive write scale), graph (relationship traversals) — fit follows access pattern."),
("Connection pooling", "Reusing a bounded set of DB connections — because connection setup is expensive and unbounded connections collapse the database."),
("N+1 queries", "Loading N parents then one query per parent's children: N+1 round trips — fixed by eager loading (JOIN or batched query)."),
("Expand-contract migrations", "Backward-compatible schema steps where old and new code coexist; the old shape is removed only after readers move — migrations without downtime."),
("Access-pattern-first choice", "The honest SQL-versus-NoSQL method: name the reads, writes, and consistency needs first — the storage follows."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Take a small schema you know and normalize it to 3NF on paper; then pick one read-heavy query and denormalize deliberately — write the measurement that would justify it.",
"Design indexes for three query patterns against one table: single-column filter, two-column filter, and an aggregation — state which are composite, which covering, and the write cost.",
"Walk the isolation ladder for a money-transfer workload: name the anomaly each level permits, pick the level, and justify why the workload can't tolerate the cheaper one.",
"Choose storage for three workloads (shopping-cart sessions, product catalog, time-series metrics): name the access pattern, pick the family, state the rejected alternatives.",
"Write the expand-contract steps for adding a non-nullable column to a live table: expand, migrate, contract — with the rollback story at each step.",
],
"project": ("Data-layer design brief. For the order pipeline in this path's guided build, write the data-layer section: schema with normalization notes, the index list with "
"the queries each serves, the isolation level chosen for order placement with the anomaly analysis, the session/cache store choice, and the zero-downtime migration plan "
"for the first schema change. Deliverable: the data-layer brief — the section interviewers read to judge judgment."),
"honesty": ("Honest scope: storage advice is workload-specific — the 'right' database changes with scale, team, and budget, and this course confers no certificate. "
"Interview answers are argued from access patterns; production answers also involve cost, hiring, and the systems you already run."),
},
"backend-interview-prep--caching-queues": {
"summary": ("Welcome to Caching and Message Queues — module 3 of the Backend path. I'm your instructor, and this is scale's two workhorses: caches that absorb "
"reads and queues that absorb bursts — with the failure modes (stampedes, poison messages) interviewers love to ask about. We cover cache-aside/read-through/write-through, "
"TTL and invalidation, Redis data structures in practice, delivery semantics, Kafka topics/partitions/consumer groups, and backpressure with dead-letter queues. "
"By the end, you will pair every speedup with its invalidation story."),
"concepts": [
("Cache-aside", "App checks cache, falls back to DB, populates cache — flexible, with the stale-read risk you must name."),
("Read-through / write-through", "Read-through: the cache loads from the DB itself. Write-through: writes go to cache and DB together — consistent, slower writes."),
("TTL and invalidation", "Time-to-live bounds staleness; the invalidation strategy is caching's permanent tax — every caching decision must name it."),
("Thundering herd", "A hot key expires and every request stampedes the DB — stopped by request coalescing (single-flight), probabilistic early refresh, or staggered TTLs with jitter."),
("Redis data structures", "Strings (counters, rate limits), hashes (objects), lists (queues), sets (membership), sorted sets (leaderboards, time-ordered feeds) — five tools, one store."),
("At-least-once delivery", "The practical default: retries can duplicate — made safe by idempotent consumers, which is effectively exactly-once processing."),
("Exactly-once semantics", "Needs idempotent consumers or transactions (Kafka EOS) — the honest answer names the machinery, not the wish."),
("Kafka", "Distributed commit log: topics split into partitions (the parallelism unit), consumer groups split partitions across consumers, offsets track progress — ordering guaranteed per partition only."),
("Backpressure", "Bounded queues that block or shed so the producer feels the consumer's slowness — an unbounded queue is a deferred outage."),
("Dead-letter queue", "Where poison messages go after retries exhaust: quarantine for inspection instead of blocking the stream or looping forever."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Implement cache-aside for one read path in a toy app: read, miss, load, populate — then write the invalidation rule for the corresponding write path.",
"Simulate a thundering herd: expire a hot key under synthetic load, observe the DB spike, then add single-flight coalescing and re-run — compare the curves.",
"Model three features in Redis data structures (a leaderboard, a rate limiter, a job queue): pick the structure per feature and state why the others don't fit.",
"Design a consumer for at-least-once delivery: write the idempotency check (processed-IDs set), the retry policy, and the dead-letter routing for poison messages.",
"Sketch a Kafka topic for an order pipeline: choose the partition key, state the ordering guarantee it gives, and assign consumer groups for two independent consumers.",
],
"project": ("Cache-and-queue architecture brief. For the order pipeline: the caching layer (what is cached, the strategy per path, TTLs, the invalidation plan, the herd defense), "
"and the queue topology (topics/queues, partition keys, consumer groups, retry and dead-letter policy, the backpressure story). Include the failure modes: cache outage, "
"consumer lag, poison message. Deliverable: the brief — the section that proves you design for the unhappy path."),
"honesty": ("Honest scope: caching and queue topologies are capacity-shaped — the right answers change with traffic, budget, and the managed services you actually run, "
"and this course confers no certificate. The interview rewards naming failure modes honestly; production rewards measuring them."),
},
"backend-interview-prep--concurrency-limits": {
"summary": ("Welcome to Concurrency and Rate Limiting — module 4 of the Backend path. I'm your instructor, and this is concurrency the way interviews test it: "
"the primitives, the classic bugs (races, deadlocks), and rate limiting as a designed system rather than a library call. We cover threads, processes, and event "
"loops; locks, semaphores, and deadlock; async I/O and backpressure; token-bucket and leaky-bucket limiters; and distributed locking with Redis. By the end, you "
"will answer hazards with mechanisms, not buzzwords."),
"concepts": [
("Threads vs processes vs event loops", "Processes: isolated, expensive. Threads: shared memory, need locks. Event loops: single-threaded async I/O — great for I/O-bound, terrible for CPU-bound."),
("Deadlock's four conditions", "Mutual exclusion, hold-and-wait, no preemption, circular wait — break any one; lock ordering (global acquisition order) is the classic fix."),
("Backpressure", "When consumers lag producers, pressure must go somewhere: bounded queues, demand signaling, consumer-lag alerting — never an unbounded queue."),
("Token bucket", "Tokens accumulate to capacity: sustained rate plus short bursts allowed — the limiter for APIs that should tolerate spikes."),
("Leaky bucket", "Requests queue and drain at a constant rate: smooth output, no bursts — the limiter for steady downstream capacity."),
("Distributed lock (Redis)", "SET with NX + PX expiry, fencing tokens for ordering, short critical sections — because a crashed holder without a TTL deadlocks every waiter."),
("Idempotent consumers", "Reprocessing the same input yields the same output — the concurrency-safe way to survive duplicate deliveries and retries."),
("Race condition", "Outcome depends on uncontrolled scheduling interleaving — fixed by making the critical section atomic or the operation idempotent."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Write a tiny multithreaded counter with and without a lock; run it under contention and observe the lost updates — then fix it and state which hazard you removed.",
"Draw a deadlock from two locks acquired in opposite orders; then impose a global lock ordering and show the cycle can't form — state the broken condition aloud.",
"Implement a token bucket and a leaky bucket for the same API: configure burst tolerance on one and smooth output on the other, and state which product need each serves.",
"Build the Redis distributed-lock pattern (SET NX PX + fencing token + short critical section); then kill the holder mid-section and verify the TTL bounds the damage.",
"Design the backpressure story for one pipeline: bounded queue depth, the drop-or-block policy, the alert on consumer lag — and the load-shedding rule when it fills.",
],
"project": ("Rate limiter design brief. Design the rate-limited public API from this path's build: limits per key and per IP, burst policy with the token-vs-leaky-bucket "
"decision argued, distributed state in Redis with the Lua atomicity argument, 429 + RateLimit-* + Retry-After headers, and per-endpoint tiers. Include the concurrency "
"hazards (thundering increments, clock skew across instances) and their mitigations. Deliverable: the brief — rate limiting as a designed system."),
"honesty": ("Honest scope: distributed-locking and limiter tuning are environment-shaped — clock behavior, Redis topology, and traffic shape change the answers, and this "
"course confers no certificate. The interview tests whether you name the hazards; production tests whether you measured them."),
},
"backend-interview-prep--microservices-arch": {
"summary": ("Welcome to Microservices Architecture — module 5 of the Backend path. I'm your instructor, and this is microservices without the hype: decomposition "
"judgment, the distributed-systems costs (sagas, observability), and the honest counterargument for when a monolith wins — the senior answer. We cover bounded-context "
"decomposition, sync versus async communication, service discovery and API gateways, sagas for distributed transactions, and observability (traces, metrics, logs). "
"By the end, you will argue distribution as a cost you pay deliberately."),
"concepts": [
("Bounded contexts", "DDD decomposition along business capabilities with clean ownership — split by capability, not by technical layer; each service owns its data."),
("Sync vs async", "Sync (REST/gRPC): simple, couples availability and latency. Async (queues/events): decoupled and resilient, but eventually consistent and harder to debug."),
("Service discovery", "How services find each other's current addresses as instances churn — registry or DNS-based; the answer to 'what's the URL?' in a dynamic fleet."),
("API gateway", "Single entry point: routing, auth, rate limiting, aggregation for clients — cross-cutting edge concerns in one policy point."),
("Saga", "Distributed transactions without 2PC: a sequence of local transactions, each with a compensating action — choreography (events) for simple flows, orchestration (coordinator) for complex ones."),
("Observability trio", "Metrics: 'is something wrong' (alerts). Logs: 'what happened' (events with context). Traces: 'where did the request go' (latency across services)."),
("Modular monolith", "Bounded-context discipline inside one deployable — the honest starting point until a proven seam demands distribution."),
("Distributed-systems tax", "The permanent costs of distribution: network failures, eventual consistency, observability burden, deployment complexity — paid only for proven seams."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Decompose a familiar monolith (an e-commerce app) into bounded contexts on paper: name the contexts, draw the ownership lines, and state what data each service owns.",
"For each cross-service call in your decomposition, choose sync or async and write the one-sentence justification ('sync: the user waits for this answer; async: this work can wait').",
"Design the saga for an order flow (payment → inventory → notification): list the steps, write each compensating action, and choose choreography vs orchestration with reasons.",
"Write the observability plan: which metrics alert, what the logs carry per request (correlation IDs), and where traces would have found the last incident you remember.",
"Argue the counter-case: write the modular-monolith version of your decomposition and name the exact conditions (scale seam, team seam) that would flip you to services.",
],
"project": ("Decomposition brief. Take the order pipeline and write the microservices decision document: bounded contexts with ownership, the sync/async map, the saga "
"with compensating actions, service discovery and gateway placement, and the observability plan (metrics, logs, traces with correlation). Close with the honest "
"counterargument: the modular-monolith alternative and the conditions that would change the call. Deliverable: the brief — distribution argued, not assumed."),
"honesty": ("Honest scope: microservices advice is org-shaped — team size, deployment maturity, and domain complexity change the answer, and this course confers no "
"certificate. Interviewers reward the tradeoff argument; the industry's hype cycles are not engineering evidence."),
},
"backend-interview-prep--backend-design-build": {
"summary": ("Welcome to the Guided Backend Design — module 6 of the Backend path. I'm your instructor, and here we do two backend design reps from contract to "
"failure modes, documented and presented: a rate-limited public API and an order pipeline with queues — plus the API contract sketch, a k6 load-test plan, and the "
"failure-mode writeup. By the end, you will have portfolio evidence that survives the onsite: designs with contracts, load plans, and unhappy paths written down."),
"concepts": [
("Rate-limited API design", "Limits per key/IP, burst policy, token bucket in Redis with atomic Lua, 429 + RateLimit-* headers — the limiter as part of the contract."),
("Order pipeline with queues", "API accepts and validates → order events to a queue → workers for payment/inventory/notification with retries + DLQ → saga compensation — the queue as the reliability seam."),
("OpenAPI contract sketch", "Endpoints, methods, schemas, status codes, error model, auth, rate limits, versioning — enough for a client team to build against."),
("k6 load-test plan", "JS-scripted load tests with thresholds as gates: the script, the stages, the assertions — code-reviewed load tests in the pipeline."),
("k6 vs JMeter", "k6: scripted, CI-friendly, thresholds as gates. JMeter: GUI-driven, mature, broad protocol support — pick by team context, not fashion."),
("Failure-mode writeup", "Per component: how it fails, blast radius, detection (which alert), mitigation (the responder's move), graceful degradation — the unhappy path designed like the happy one."),
("45-minute presentation", "The design-round cadence: requirements, estimation, API/data, deep-dive, tradeoffs — ending with the tradeoffs you'd revisit."),
("Contract-first", "Interface decisions made early when they're cheap — and client/server work parallelized; the habit interviewers want to see generalized."),
],
"proc_title": "Worked estimation",
"procedure": [
"Estimate the rate-limited API: 10k req/s sustained, 2× burst — size the Redis token-bucket state, compute per-key memory, and state the Lua atomicity requirement.",
"Estimate the order pipeline: 50k orders/day, peak 10× — queue depth for the peak hour, worker count from per-worker throughput, DLQ sizing for a 1% poison rate.",
"Write the k6 script plan for the API: stages (ramp, sustain, spike), thresholds (p95, error rate), and the gate assertion that fails the run.",
"Recompute the pipeline estimate with one changed assumption (orders 5×, or a new channel added) and name which design decision flips.",
"Present one design in 45 minutes on camera: timebox visibly, end with three tradeoffs you'd revisit — then score yourself against the rubric.",
],
"project": ("Two documented backend designs. Produce the full artifacts: the rate-limited public API (contract, limiter design, estimation, failure modes) and the order "
"pipeline (queue topology, workers, saga, load-test plan, failure-mode writeup) — each as a one-page design doc plus a 45-minute recorded walkthrough of one. "
"Deliverable: two design docs and one recording — the portfolio evidence that survives the onsite."),
"honesty": ("Honest scope: two guided designs are interview practice, not production systems — real APIs answer to existing clients, cost constraints, and on-call burden, "
"and this course confers no certificate. The value here is the documented reasoning habit; the numbers are estimates, stated as such."),
},
"backend-interview-prep--backend-mock": {
"summary": ("Welcome to the Backend Mock Circuit — the final module of the Backend path. I'm your instructor, and these are backend-flavored mocks: API design "
"under time, concurrency and data-layer deep dives, system design on camera, and the behavioral ledger for backend roles — each debriefed into the next week's "
"study plan. By the end, your debrief log will have converted every mock into targeted reps."),
"concepts": [
("Timed API-design round", "The budget: 5 requirements, 10 resources + verbs + status codes, 10 edge cases (pagination, idempotency, versioning), 5 tradeoffs — thinking in resources and contracts."),
("Concurrency deep dive", "Hazards named with mechanisms: races, deadlocks, N+1, isolation anomalies — each tied to a concrete scenario, never a buzzword list."),
("Data-layer deep dive", "Index choices, isolation levels, storage decisions — argued from access patterns under follow-up pressure."),
("Behavioral ledger", "Story bank, stories-told-where, feedback, stumping questions — the running record that stops repeated stories."),
("Debrief and triage", "Within the hour: what leaked, what held, biggest leak by frequency × weight, the 48-hour redrill — the mock is the test, the debrief is the studying."),
("Taper plan", "Final two weeks: no new material, redrill from the debrief log, timed mocks, rest — consolidation over cramming."),
],
"proc_title": "Hands-on procedure",
"procedure": [
"Run a timed API-design mock (30 min): budget aloud, design the contract a client could program against, close with tradeoffs.",
"Run a concurrency deep-dive mock: a partner probes races, deadlocks, and limiter design — answer every hazard with a mechanism and a scenario.",
"Run a data-layer deep-dive mock: defend an index list and an isolation choice against 'why not cheaper?' follow-ups.",
"Run one system-design round on camera (45 min): the walkthrough with estimation, ending in named tradeoffs.",
"Debrief all four within the hour each: fill the template, rank the leaks, schedule the 48-hour redrills, update the ledger.",
],
"project": ("Backend mock portfolio. Run the four-mock circuit over two weeks — API design, concurrency deep dive, data-layer deep dive, system design on camera — "
"each with a partner or recorded. Produce the debrief per mock (leaks, holds, biggest leak, redrill plan) and the updated behavioral ledger, then write the taper plan "
"for your real loop. Deliverable: four debriefs, the ledger, the taper — the paper trail from mocks to study plan."),
"honesty": ("Honest scope: mocks simulate the format, not the stakes — real loops add nerves, unfamiliar interviewers, and company-specific bars, and this course confers "
"no certificate. What the circuit honestly delivers is leak discovery while it's still cheap to fix."),
},
}
