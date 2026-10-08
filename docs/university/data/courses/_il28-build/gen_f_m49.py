#!/usr/bin/env python3
"""Build IL28-M49 module object -> part_f_m49.json"""
import json

notes = [
{"title": "SRE Principles: Toil, Budgets, and Blamelessness",
"body": "Site Reliability Engineering treats operations as a software problem. Its principles, straight from the Google SRE tradition: (1) error budgets (M46) govern the feature-vs-reliability tradeoff; (2) toil — manual, repetitive operational work — is budgeted and automated away, with a standing cap on how much of a team's time it may consume; (3) monitoring is built around the four golden signals (latency, traffic, errors, saturation); (4) automation is preferred over heroics for every repeated task; (5) blameless postmortems turn incidents into system fixes. The SRE mindset shift for a panel: reliability is a feature with a price, negotiated explicitly via the SLO — not a vague aspiration. Worked example: a team spends 60% of its time on manual deploy verifications and ticket-driven restarts. SRE analysis: that is toil — automatable, repetitive, and scaling linearly with service count. Solution: cap toil work, automate the deploy verification into the pipeline (smoke tests + automatic rollback on burn-rate alerts), and convert the restart tickets into the autoscaler + health-probe fixes from M41. The interview one-liner: 'SRE replaces operational heroics with engineering: budgets decide priorities, automation absorbs toil, and postmortems fix systems.'"},
{"title": "High Availability: Multi-AZ and Multi-Region Design",
"body": "High availability is designed in layers. Within a region: deploy across at least 3 availability zones — AKS node pools spread with --zones 1 2 3, databases with zone-redundant replicas, load balancers zone-aware. A zone failure then costs capacity, not availability. Across regions: active-passive (traffic on one region, tested failover to the second) for most financial workloads, active-active only when the data layer supports conflict-free replication. The data layer decides everything: stateless services fail over trivially; databases need replication with a known RPO/RTO, and the failover must be rehearsed — an untested failover is a hope. Worked example: design the checkout service for zone failure. Solution: AKS with 3 zones, pod anti-affinity spreading replicas across zones, PodDisruptionBudgets guaranteeing quorum during drains, Azure SQL zone-redundant, Application Gateway multi-zone; chaos-test by failing one zone in staging quarterly. The panel question on 'fault tolerance for mission-critical financial apps' wants exactly this layered answer: multi-AZ for the common case, multi-region with tested failover for the disaster case, data replication as the binding constraint, and rehearsal as the proof. Availability math is honest: each added nine costs roughly an order of magnitude more engineering — 99.9% is 8.8 hours/year of budget, 99.99% is 53 minutes, and the SLO should match what the business will actually fund."},
{"title": "Circuit Breakers, Retries, and Timeouts",
"body": "Distributed systems fail partially, and naive clients turn partial failure into total failure. Three patterns contain it. Timeouts: every outbound call gets a deadline (e.g. 2s) — without one, a hung dependency parks your threads forever. Retries: retry transient failures with exponential backoff and jitter, but only idempotent operations — retrying a non-idempotent payment charge double-charges. Circuit breakers: after N consecutive failures, the breaker opens and calls fail fast for a cooldown period instead of hammering the dead dependency, then half-opens to probe recovery. The retry-storm math the panel loves: service A calls B with 3 retries; B calls C with 3 retries; one slow C means each user request fans out to 1 + 3 + 9 = up to 13 downstream calls — a 13x amplification that melts C. Worked example: payment calls take 200ms normally; the client has no timeout and 5 retries. Under a payment outage, threads pile up waiting, memory grows, and the checkout service itself OOMs — the M41 OOMKilled drill in distributed form. Solution: 2s timeout, max 2 retries with backoff + jitter on idempotent reads only, circuit breaker opening after 5 consecutive failures with 30s cooldown, and a retry budget (e.g. max 10% of requests may be retries). Resilience is arithmetic: bound every fan-out or the fan-out bounds you."},
{"title": "Case Study (Hypothetical): Strangler Fig on a Monolithic Trading Platform",
"body": "Exercise — hypothetical, no claims about any real firm: re-architect a legacy monolithic trading platform into microservices. The strangler fig pattern (Martin Fowler) migrates incrementally: new functionality is built as services around the monolith, traffic is routed to the new services piece by piece, and the monolith shrinks until it can be retired — like the fig that grows around a tree. The migration plan: (1) identify seams — order entry, market data, risk checks, settlement — and carve the first low-risk seam (say, market-data fan-out, read-only); (2) put an anti-corruption layer / facade in front of the monolith so new services never touch its schema directly; (3) route via the gateway progressively (1% -> 10% -> 100%) with the monolith as instant fallback; (4) extract state carefully — the database is the hard part, migrated with dual-write or change-data-capture, never a big-bang cutover; (5) retire the monolith's module only when traffic is zero and the data is migrated. Worked example: which seam first? Solution: the read-only market-data feed — no writes, no transactions, easy rollback; order entry (money movement) goes last, with the most testing. The panel answer: 'Strangler fig, seam by seam, gateway-routed with fallback, data migrated via dual-write — never a rewrite, never a big bang.'"},
{"title": "Chaos Engineering: Proving Resilience on Purpose",
"body": "Chaos engineering is the disciplined practice of injecting failure to prove resilience before production does it for you. Principles: start with a steady-state hypothesis ('checkout p99 stays under 500ms when one zone fails'), blast radius is minimized (staging first, one zone, business-hours, with an abort button), and every experiment is a game-day with observers and a rollback plan. The experiment ladder: kill a pod (does the ReplicaSet recover in seconds?); kill a node (do pods reschedule across zones?); fail a zone (does multi-AZ hold?); inject latency into a dependency (do timeouts and breakers engage?); expire a certificate (does rotation work?). Worked example: hypothesis — 'losing one of three zones keeps checkout under SLO.' Run it in staging: cordon and drain a zone's nodes, watch the dashboards. If p99 breaches, the postmortem writes the missing anti-affinity or PDB as the action item — the experiment paid for itself. The panel framing: chaos is not recklessness, it is the scientific method applied to reliability — hypothesis, controlled experiment, measured result, system fix. Never run chaos in production without the incident-command structure from M46 on standby; the point is learning, not outages."},
{"title": "Capacity Planning with Little's Law",
"body": "Little's Law — L = λW — relates the average number of items in a system (L) to the arrival rate (λ) and the average time each spends in the system (W). It is the back-of-the-envelope capacity tool: it needs no distributional assumptions, just consistent units. Worked example: checkout receives λ = 500 requests/second, each taking W = 0.4 seconds of server time. L = 500 × 0.4 = 200 concurrent requests in flight on average. If each pod handles 50 concurrent requests, you need 200/50 = 4 pods for steady state — then add headroom for bursts and rolling updates (the M41 autoscaler math), say min 6. Second example: a queue grows unboundedly. λ = 1000 msgs/s in, processing W-equivalent throughput 800/s — arrivals exceed service, so no steady state exists and the queue grows forever; the fix is more consumers or load shedding, not a bigger queue. The panel callback: combine with the M41 node math — Little's Law gives concurrent load, pod capacity gives pods needed, and the autoscaler min/max brackets the result. Capacity planning is not guessing: it is λ measured from dashboards, W measured from traces, and L computed — then verified by load test."},
]

cards = [
{"front": "SRE in one line", "back": "Operations as software: error budgets set priorities, automation absorbs toil, blameless postmortems fix systems — reliability as a priced feature"},
{"front": "Four golden signals", "back": "Latency, traffic, errors, saturation — the monitoring baseline for every service"},
{"front": "What is toil and how is it handled?", "back": "Manual repetitive ops work; budgeted, capped, and automated away — heroics are not a strategy"},
{"front": "Multi-AZ vs multi-region (when each)", "back": "Multi-AZ (3 zones): the common case — zone failure costs capacity. Multi-region active-passive: disaster case with tested failover; data replication is the binding constraint"},
{"front": "Availability budget math: 99.9% vs 99.99%", "back": "99.9% = ~8.8 h/year downtime budget; 99.99% = ~53 min/year; each nine costs ~10x the engineering — SLO must match funded reality"},
{"front": "Timeout / retry / circuit breaker (one line each)", "back": "Timeout: deadline on every call. Retry: transient failures only, backoff+jitter, idempotent ops only. Breaker: fail fast after N failures, half-open to probe recovery"},
{"front": "Retry-storm amplification math", "back": "A->B (3 retries) ->C (3 retries): one slow C fans one request into up to 13 downstream calls — bound with retry budgets (e.g. 10% cap)"},
{"front": "Why never retry a non-idempotent payment charge?", "back": "Retries re-execute: the charge happens twice. Retries are for idempotent operations only"},
{"front": "Strangler fig pattern in one paragraph", "back": "Build new services around the monolith, route traffic piece by piece via gateway with fallback, migrate data via dual-write/CDC, retire modules at zero traffic — never a big-bang rewrite"},
{"front": "Strangler fig: which seam first on a trading platform?", "back": "Read-only market-data feed (no writes, easy rollback); money-movement order entry goes last with the most testing"},
{"front": "Chaos experiment structure", "back": "Steady-state hypothesis -> minimized blast radius (staging, abort button) -> game-day with observers -> measured result -> system fix"},
{"front": "Little's Law + worked example", "back": "L = λW. λ=500 rps, W=0.4s -> L=200 concurrent; at 50/pod -> 4 pods steady state, plus headroom"},
{"front": "Queue growing unboundedly: Little's Law diagnosis?", "back": "λ (1000/s) > service rate (800/s): no steady state exists — add consumers or shed load; a bigger queue just delays the inevitable"},
{"front": "Untested failover is what?", "back": "A hope, not a plan — failover must be rehearsed (game-days) or it will fail when needed"},
]

quiz = [
{"q": "A team spends 60% of its time on manual deploy checks and restart tickets. SRE analysis?",
"choices": ["Hire more operators", "That is toil: cap it, automate deploy verification into the pipeline, fix restarts with autoscaling and health probes", "It is fine", "Stop deploying"],
"answer": 1,
"explain": "Toil is the SRE term for automatable repetitive ops work; the discipline budgets and eliminates it rather than staffing it."},
{"q": "Design checkout for zone failure. Which set is correct?",
"choices": ["Single zone, bigger VMs", "3 AZs, pod anti-affinity across zones, PDBs, zone-redundant database, multi-zone gateway, quarterly zone-failure game-day", "Active-active across 5 regions on day one", "No database replication"],
"answer": 1,
"explain": "Layered HA: multi-AZ for the common case with spreading and disruption budgets, rehearsed. Active-active everywhere on day one is over-engineering."},
{"q": "Payment client: no timeout, 5 retries, outage hits. What happens?",
"choices": ["Nothing", "Threads pile up on hung calls, retries multiply load, the caller OOMs — the distributed version of the M41 OOMKilled drill", "Retries fix the outage", "The breaker opens automatically"],
"answer": 1,
"explain": "No timeout parks threads; retries amplify; the caller's memory grows until it dies. Timeouts + bounded retries + breakers prevent exactly this."},
{"q": "A->B->C chain, each link retries 3 times. One slow C: worst-case downstream calls per user request?",
"choices": ["3", "Up to 13 (1 + 3 + 9 fan-out)", "1", "Infinite"],
"answer": 1,
"explain": "Retry multiplication compounds per hop. Retry budgets (e.g. 10% cap) and breakers bound the fan-out."},
{"q": "Which operation may be retried?",
"choices": ["POST /charge (creates a payment)", "GET /order-status (idempotent read)", "POST /transfer (moves money)", "Anything, retries are free"],
"answer": 1,
"explain": "Only idempotent operations survive re-execution. Retrying money movement double-executes it."},
{"q": "Strangler fig on a monolithic trading platform: what goes first?",
"choices": ["Order entry (money movement)", "Read-only market-data feed — no writes, trivial rollback; order entry goes last", "The database, all at once", "Everything in one cutover"],
"answer": 1,
"explain": "Seam-by-seam risk ordering: stateless reads first, money movement last, data via dual-write — never a big bang."},
{"q": "What is the anti-corruption layer's job in the strangler fig?",
"choices": ["Security scanning", "Shielding new services from the monolith's schema so they never couple to legacy internals", "Encrypting traffic", "Load balancing"],
"answer": 1,
"explain": "The facade translates between the new domain model and the monolith, preventing the new services from inheriting legacy coupling."},
{"q": "Chaos experiment: 'lose one zone in staging, checkout stays under SLO.' p99 breaches. What is the correct conclusion?",
"choices": ["Chaos is too dangerous", "The experiment paid for itself: write the missing anti-affinity/PDB/capacity as postmortem action items and re-run", "Hide the result", "Never test again"],
"answer": 1,
"explain": "A failed hypothesis is a found weakness — the scientific-method framing. Fix the system, re-run the experiment."},
{"q": "λ=500 rps, W=0.4s, 50 concurrent requests per pod. Pods for steady state?",
"choices": ["2", "4 (L=200 concurrent / 50), plus headroom for bursts and rolling updates", "200", "50"],
"answer": 1,
"explain": "L = 500×0.4 = 200 concurrent; 200/50 = 4 pods steady state. Headroom (min 6) covers bursts and update surge — the M41 autoscaler bracket."},
]

drills = [
{"id": "il28-m49-resilience", "title": "Timed drill: resilience patterns",
"items": [
{"prompt": "Timeout / retry / circuit breaker — one line each.", "answer": "Timeout: deadline per call. Retry: transient + idempotent only, backoff/jitter. Breaker: fail fast after N failures, half-open probe.",
"explain": "Then the arithmetic: bound every fan-out."},
{"prompt": "Retry-storm math: A->B->C, 3 retries each. Amplification?", "answer": "Up to 13x per user request (1+3+9). Bound with retry budgets.",
"explain": "Say the number — panels love the 13x."},
{"prompt": "Which calls may be retried?", "answer": "Idempotent ones only — never money movement.",
"explain": "Retrying a charge double-charges. One sentence."},
{"prompt": "Multi-AZ vs multi-region: when each?", "answer": "Multi-AZ: common case (capacity, not availability). Multi-region active-passive: disaster case, tested failover.",
"explain": "Data replication is the binding constraint — say it."},
{"prompt": "99.9% vs 99.99% in hours/year?", "answer": "~8.8 h vs ~53 min. Each nine ~10x the engineering.",
"explain": "SLO must match funded reality — the honest-SLO answer."},
{"prompt": "Zone-failure design: the five pieces?", "answer": "3 AZs, anti-affinity, PDBs, zone-redundant DB, rehearsed game-day.",
"explain": "Recite as the checklist for 'fault tolerance for financial apps'."},
{"prompt": "Untested failover is ___?", "answer": "A hope, not a plan — rehearse or it fails when needed.",
"explain": "One line, no hedging."},
]},
{"id": "il28-m49-strangler", "title": "Timed drill: strangler fig + capacity",
"items": [
{"prompt": "Strangler fig in 30 seconds.", "answer": "New services around the monolith; gateway routes traffic piece by piece with fallback; data via dual-write/CDC; retire at zero traffic.",
"explain": "Never a rewrite, never a big bang — the mantra."},
{"prompt": "Trading platform: first seam and last seam?", "answer": "First: read-only market-data feed. Last: order entry (money movement).",
"explain": "Risk ordering: stateless reads first, money last."},
{"prompt": "What does the anti-corruption layer do?", "answer": "Shields new services from the monolith's schema — no legacy coupling.",
"explain": "Facade translates; new domain model stays clean."},
{"prompt": "How is traffic migrated safely?", "answer": "Gateway-routed percentages (1%->10%->100%) with the monolith as instant fallback.",
"explain": "Progressive + reversible — the safety property."},
{"prompt": "How is the database migrated?", "answer": "Dual-write or change-data-capture — never a big-bang cutover.",
"explain": "Data is the hard part; say the two techniques."},
{"prompt": "Little's Law: λ=500, W=0.4. L and pods at 50/pod?", "answer": "L=200; 4 pods steady state, headroom to ~6.",
"explain": "Show the arithmetic — λ×W, then divide."},
{"prompt": "Queue grows forever: diagnosis and fix?", "answer": "λ > service rate: no steady state. Add consumers or shed load.",
"explain": "Bigger queue delays; it never fixes."},
]},
]

handsOnLab = {
"id": "il28-m49-lab",
"title": "Lab: resilience patterns and a strangler-fig plan",
"brief": "You will implement timeout/retry/circuit-breaker in a sample service, measure retry amplification, run a zone-failure game-day on a local cluster, and write the strangler-fig migration plan for a hypothetical monolith.",
"steps": [
"Write a Python client calling a flaky test server: add a 2s timeout, max 2 retries with exponential backoff + jitter, idempotency keys on writes.",
"Measure: with retries at 3 per hop across a 2-hop chain, count downstream calls during a 10s induced slowdown — record the amplification factor.",
"Add a circuit breaker (simple counter-based implementation): open after 5 consecutive failures, 30s cooldown, half-open probe; verify calls fail fast while open.",
"Add a retry budget: cap retries at 10% of requests; verify the budget throttles retries under sustained failure.",
"Deploy two services on a local kind cluster across 3 'zones' (labels); set pod anti-affinity and a PodDisruptionBudget; verify spread with kubectl get pods -o wide.",
"Drain one zone's nodes (kubectl drain); measure recovery time and error rate; record whether the SLO held.",
"Write the chaos report: hypothesis, blast radius, measurements, and the action items the experiment produced.",
"Draft the strangler-fig plan for a hypothetical monolithic trading app: seam list in migration order, facade design, gateway routing stages, dual-write data plan, retirement criteria.",
"Compute capacity with Little's Law for the lab services: measure λ and W from your test traffic, compute L, and compare with actual pod counts.",
"Define the SLOs for the lab checkout path (success ratio + p99) and the error-budget policy that would freeze the strangler migration.",
"Present the 5-minute panel narrative: strangler plan, resilience patterns, and the chaos result.",
"Clean up the kind cluster and archive the plan + report in the repo."],
"deliverable": "A client library with timeout/retry/breaker/budget, a zone-failure game-day report, a seam-ordered strangler-fig migration plan, and Little's Law capacity math.",
"checkpoint": "Amplification measured and bounded; zone drain recovers within the SLO; the migration plan orders seams by risk with data via dual-write."
}

mockTask = {"id": "il28-m49-mock", "type": "choice",
"q": "Panel: 'Re-architect our legacy monolithic trading platform as microservices.' What is the core of a strong answer?",
"choices": ["Full rewrite in microservices over one big-bang cutover", "Strangler fig: seam-by-seam extraction starting with read-only services, gateway-routed traffic with monolith fallback, anti-corruption layer, data via dual-write/CDC, retire at zero traffic", "Lift-and-shift the monolith to bigger VMs", "Split by team size"],
"answer": 1,
"explain": "The strong answer names the pattern, the seam ordering (reads first, money movement last), the safety properties (progressive routing, fallback), and the data strategy — proving you have done or deeply studied real migrations, not just drawn boxes."}

module = {
"id": "IL28-M49", "code": "IL-28",
"title": "SRE & Resilience: HA, Microservices & the Strangler Fig",
"summary": "Engineer reliability: SRE principles, layered high availability, timeout/retry/circuit-breaker arithmetic, the strangler-fig migration of a monolithic trading platform, chaos game-days, and Little's Law capacity planning.",
"objectives": [
"Apply SRE principles: error budgets, toil reduction, golden signals, blameless postmortems",
"Design multi-AZ and multi-region architectures with honest availability math",
"Implement timeouts, bounded retries, and circuit breakers, computing retry amplification",
"Plan a strangler-fig migration seam by seam with data migration and fallback safety",
"Run chaos experiments and capacity-plan with Little's Law"],
"notes": notes, "cards": cards, "quiz": quiz, "weight": 2,
"prerequisiteFor": ["IL28-M50"],
"drills": drills, "handsOnLab": handsOnLab, "mockTask": mockTask,
"crossLinks": ["IL28-M50", "IL28-M46"],
"videos": [
{"title": "StranglerFigApplication", "url": "https://martinfowler.com/bliki/StranglerFigApplication.html", "source": "martinfowler.com", "durationMin": 20, "order": 1, "watchBefore": "notes", "blurb": "Fowler's original strangler-fig description — the pattern behind this module's migration case study."},
{"title": "Site Reliability Engineering (book)", "url": "https://sre.google/sre-book/table-of-contents/", "source": "Google SRE", "durationMin": 600, "order": 2, "watchBefore": "notes", "blurb": "The free SRE book: error budgets, toil, and postmortems in depth — read the chapters matching each note."}],
"estimatedMinutes": 780,
}

with open("/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build/part_f_m49.json", "w") as f:
    json.dump(module, f, indent=2, ensure_ascii=False)
print("M49 written")
