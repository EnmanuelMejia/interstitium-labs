# -*- coding: utf-8 -*-
"""IL-14 retrofit content — Path 1: SRE Interview Prep (6 modules).

Keys per module id:
  summary  -> instructor-voice module summary
  notes    -> list of 4 note dicts {title, body}
             titles: 'Concepts' | 'Hands-on procedure' | 'Worked estimation' | 'Project brief' | 'Honesty note'
  new_card -> one extra card {front, back} (module keeps its 5, gains this 6th)
  new_quiz -> 6 extra quiz items {q, choices[4], answer (0-based), explain}
All prose is original, on the module's own topic, drawn from the module's
existing factual material. Quiz explains reference the module's own sections.
"""
# pylint: disable=line-too-long

P1_SUMMARY = {
"sre-interview-prep--sre-sli-slo": (
"Welcome to the SRE Interview Prep path of the Interstitium Labs SRE, DevOps, Cloud & Security Interview Prep course. "
"I'm your instructor for this path, and we open with the vocabulary every SRE interview runs on: what to measure, what target to promise, and what happens when the budget burns. "
"This is Module 1: SLIs, SLOs, and Error Budgets. By the end, you'll choose SLIs from the four golden signals, do error-budget arithmetic on a whiteboard, and explain burn-rate alerting the way someone who has carried a pager explains it — in terms of paging policy, not poetry."
),
"sre-interview-prep--sre-incident-command": (
"Welcome back. I'm your instructor for the SRE Interview Prep path, and this is Module 2: Incident Response and Command. "
"Reliability interviews don't just test what you know — they test how you behave when something is on fire. In this module we rehearse the incident as a discipline: the lifecycle, the command roles, the severity call, and the postmortem that fixes systems instead of blaming people. "
"You'll leave able to walk an interviewer through a sev-1 minute by minute, narrating decisions the way an incident commander makes them."
),
"sre-interview-prep--sre-monitoring": (
"Welcome back. I'm your instructor for the SRE Interview Prep path, and this is Module 3: Monitoring, Tracing, and Alerting. "
"Observability is an interview topic that separates people who have watched dashboards from people who have designed them. We cover the three pillars, the four golden signals, the USE and RED lenses, and the alerting philosophy that keeps you from paging yourself to death. "
"By the end you'll design an alerting policy aloud — what pages, what tickets, and why — which is exactly what the monitoring round is really asking."
),
"sre-interview-prep--sre-capacity": (
"Welcome back. I'm your instructor for the SRE Interview Prep path, and this is Module 4: Capacity Planning and Scaling. "
"Capacity interviews are applied arithmetic with a cost conscience: forecast the demand, prove it with load tests, provision headroom against the utilization wall, and narrate the price of every extra nine. "
"In this module you'll do the worked math — headroom, N+1, autoscaling lag — and learn to say the interview line that matters: 'I plan headroom against the wall, not against the average.'"
),
"sre-interview-prep--sre-design-reps": (
"Welcome back. I'm your instructor for the SRE Interview Prep path, and this is Module 5: SRE System Design Reps. "
"This is where reliability becomes a graded design axis: six full design reps where every choice is defended against failure, scale, and cost. Multi-region services, HA databases, queues with backpressure, caches that fail gracefully, load shedding. "
"You'll rehearse the design-interview loop until the structure is automatic — because the interview grades method under pressure, and the method is what we drill."
),
"sre-interview-prep--sre-mock": (
"Welcome back. I'm your instructor for the SRE Interview Prep path, and this is Module 6: SRE Mock Circuit. "
"Theory ends here. This module is a complete simulated SRE loop — incident round, metrics-and-SLO round, system-design round, behavioral round — scored against a rubric, with a debrief that turns your weakest round into next week's plan. "
"You'll also get the 48-hour pre-interview checklist and the two-week taper, because performance on loop day is trained, not wished for."
),
}

P1_NOTES = {
"sre-interview-prep--sre-sli-slo": [
{"title": "Concepts", "body": (
"- **SLI (Service Level Indicator)** — the measured fact: e.g. successful requests ÷ total requests, or the fraction of requests under a latency bound. SLIs are facts, not promises.\n"
"- **SLO (Service Level Objective)** — the target set on an SLI: e.g. 99.9% of requests succeed over a 30-day window. SLOs are promises the team makes.\n"
"- **SLA (Service Level Agreement)** — the contract with consequences: what happens (credits, penalties) when the SLO is missed. SLAs are contracts with customers.\n"
"- **Error budget** — 1 − SLO: the allowed failure rate, spent deliberately on releases and risk. A 99.9% SLO leaves a 0.1% budget.\n"
"- **Four golden signals** — latency, traffic, errors, saturation: the minimum dashboard for any service, and the first SLI candidates.\n"
"- **Burn rate** — how fast the error budget is being consumed relative to the SLO window. Fast burn pages now; slow burn files a ticket.\n"
"- **Multiwindow alerting** — pairing a short window (catches fast burns) with a long window (confirms slow burns) so blips don't page.\n"
"- **Counter** — a Prometheus metric that only increases: the raw material for request/error-rate SLIs via rate() over windows.\n"
"- **Histogram** — a Prometheus metric with buckets: the raw material for latency-percentile SLIs, since any percentile is computable over any window.\n"
"- **Recording rule** — a precomputed PromQL expression: how expensive SLI ratios are calculated once and queried cheaply."
)},
{"title": "Worked estimation", "body": (
"Do this estimation on paper or a whiteboard — it is the single most common SLO whiteboard exercise.\n"
"1. **State the SLO.** 99.9% successful requests over a 30-day rolling window. Write the budget: 1 − 0.999 = 0.001, i.e. 0.1%.\n"
"2. **Convert the window to minutes.** 30 days × 24 hours × 60 minutes = 43,200 minutes.\n"
"3. **Multiply.** 0.1% × 43,200 = 43.2 minutes of total allowed badness per month — downtime, errors, slow responses, all of it drawn from one account.\n"
"4. **Interpret the number.** That is roughly one 45-minute incident per month, or several small ones. Say it aloud: 'our budget is one real incident a month.'\n"
"5. **Add a burn-rate read.** If you burn 2% of that budget in one hour, you're consuming it ~14× faster than the sustainable rate — that is a fast burn, page now. If you burn 2% in a week, that is a slow burn — ticket it.\n"
"6. **Close with the policy.** Budget remaining → ship freely. Budget exhausted → freeze risky changes until reliability recovers. The arithmetic is the policy."
)},
{"title": "Project brief", "body": (
"Your deliverable: a one-page SLO proposal for a sample checkout API, written as if you will defend it in a design review.\n"
"- **Choose three SLIs** from the four golden signals (e.g. request success rate, p99 latency under 300 ms, saturation of the checkout workers), and justify each choice in one sentence.\n"
"- **Set SLO targets and a 30-day window** for each, then compute the error budget in minutes the way the Worked estimation shows.\n"
"- **Write the release policy** as a rule: budget remaining → ship; budget exhausted → freeze. Name who decides.\n"
"- **Specify two burn-rate alerts**: one fast-burn (pages) and one slow-burn (tickets), with the metric each watches.\n"
"- **Defend it aloud in 10 minutes**, then write the three hardest questions you were asked and your improved answers.\n"
"Reference shelf (module sources): **Google SRE Books** (https://sre.google/) — SLIs/SLOs, incidents, and reliability math from the source. **Prometheus Documentation** (https://prometheus.io/docs/) — metrics, PromQL, and alerting references."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and rehearsing SLO math is not the same as carrying a production error budget. "
"Real budgets are negotiated with product and customers, and real paging policies are tuned against months of alert history you don't have yet. "
"What this module does give you is the interview's language — SLIs are facts, SLOs are promises, SLAs are contracts — and the arithmetic to defend them on a whiteboard. Vendor specifics follow vendor documentation, which changes; check the linked sources as of their retrieval dates."
)},
],
"sre-interview-prep--sre-incident-command": [
{"title": "Concepts", "body": (
"- **Incident** — a declared, time-boxed response to user-impacting degradation: saying the word 'incident' is what starts the machinery.\n"
"- **Incident Commander (IC)** — decides and coordinates; owns the incident, never the keyboard. The IC does not debug.\n"
"- **Communications lead** — owns status updates to stakeholders on a fixed cadence, in impact-first language.\n"
"- **Scribe** — owns the timeline: what happened, when, who did what. The timeline is the postmortem's raw material.\n"
"- **Severity** — the impact axis: how many users, how badly degraded. Separate from priority, which is the fix-ordering business decision.\n"
"- **Mitigation** — stopping the bleeding (rollback, shed load, fail over). Comes before understanding the cause.\n"
"- **Resolution** — the service is healthy and the incident is closed; the learning continues in the postmortem.\n"
"- **Blameless postmortem** — a review of systems and process, never people: timeline, impact, plural root causes, action items with owners and dates.\n"
"- **Paging policy** — which severities wake whom, and how fast. Severity without a paging policy is just vocabulary."
)},
{"title": "Hands-on procedure", "body": (
"Run this 20-minute mock incident with a partner or a timer — the reps are the point.\n"
"1. **Declare.** Say 'I'm declaring an incident' out loud. Open a dedicated channel. Assign IC, Communications, and Scribe — one person can wear two hats in drill, never all three.\n"
"2. **State impact first.** Scribe writes: what's degraded, who's affected, when it started. Communications posts the first status: impact, what's being done, when the next update lands.\n"
"3. **Mitigate before diagnosing.** IC picks the fastest bleed-stopper available — rollback the last deploy, shed non-critical load, fail over. Narrate the choice: 'mitigate first, understand second.'\n"
"4. **Hold the cadence.** Communications updates every 15 minutes even with 'no update' — silence during an outage is a second outage.\n"
"5. **Resolve explicitly.** IC declares the incident resolved when the SLI recovers, not when the fix feels done. Scribe closes the timeline.\n"
"6. **Schedule the postmortem.** Within 24–48 hours: timeline, impact, root causes (plural, five-whys with evidence), action items with owners and dates. Blameless, always."
)},
{"title": "Project brief", "body": (
"Your deliverable: a full mock incident on a sample scenario — the checkout API is returning 500s for 20% of requests — run end to end, then written up.\n"
"- **Run the drill** using the Hands-on procedure: declare, assign roles, mitigate (choose rollback vs shed-load and defend the choice aloud), hold comms cadence.\n"
"- **Produce the timeline** as the scribe would: timestamps, decisions, who made them.\n"
"- **Write the blameless postmortem**: impact statement, five-whys down to a systemic cause, and three action items each with an owner and a date.\n"
"- **Add the severity call**: what severity you declared, why, and who got paged under your paging policy.\n"
"- **Debrief**: what broke down in your process (not the fake system), and the one change you'll make before the next drill.\n"
"Reference shelf (module sources): **Google SRE Books** (https://sre.google/) — incident response chapters from the source. **CISA Resources & Tools** (https://www.cisa.gov/resources-tools) — US government guidance on incident response and best practice."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and a rehearsed drill is not production on-call. "
"Real incidents involve tired humans, incomplete telemetry, and business pressure that no simulation reproduces. What transfers is the structure: declare, mitigate first, communicate on cadence, review blamelessly. "
"Never present drill experience as production incident command on a resume or in an interview — describe it as rehearsed process, which is exactly what interviewers want to hear practiced."
)},
],
"sre-interview-prep--sre-monitoring": [
{"title": "Concepts", "body": (
"- **Metrics** — numbers over time: the basis of alerts and trends. 'Something is wrong.'\n"
"- **Logs** — discrete events with context: the basis of diagnosis. 'Why it's wrong.'\n"
"- **Traces** — request journeys across services: the basis of localization. 'Where it's wrong.'\n"
"- **Four golden signals** — latency, traffic, errors, saturation: the minimum dashboard for any user-facing service.\n"
"- **USE method** — Utilization, Saturation, Errors: the resource lens. 'Is the box healthy?'\n"
"- **RED method** — Rate, Errors, Duration: the service lens. 'Is the service healthy?'\n"
"- **Symptom alert** — pages on user impact (latency, error rate vs SLO). The only kind that should wake you.\n"
"- **Cause metric** — a resource reading (disk 90%, CPU spike): belongs on a dashboard for diagnosis, not in a paging rule.\n"
"- **Cardinality** — the number of unique time series: unbounded label values (like user IDs) multiply series and cost.\n"
"- **Deploy annotation** — a marker on dashboards at release time: answers 'what changed?' at a glance."
)},
{"title": "Hands-on procedure", "body": (
"Design the minimum viable observability for a sample API, on paper, in 30 minutes.\n"
"1. **List the golden signals** for the service and pick the SLI behind each: success rate (errors), p99 latency (latency), requests/sec (traffic), worker queue depth (saturation).\n"
"2. **Draw the dashboard hierarchy.** Golden signals up top; one drill-down layer per signal (signal → per-endpoint → per-instance); deploy annotations on every graph.\n"
"3. **Write the alerting policy as rules.** Page only on symptoms: fast-burn alert on error budget, p99 latency vs SLO. Ticket the slow burns and the cause metrics (disk, CPU) — they inform, they don't wake.\n"
"4. **Choose the lenses per component.** API service → RED. Database host → USE. Write one sentence for each choice.\n"
"5. **Audit cardinality.** List every label you plan; strike any with unbounded values (user IDs, request IDs) — those belong in logs/traces, not metric labels.\n"
"6. **Rehearse the narration.** Explain the whole design aloud in 5 minutes, ending with: 'metrics tell me something's wrong, traces show me where, logs tell me why.'"
)},
{"title": "Project brief", "body": (
"Your deliverable: an alerting-policy document plus dashboard sketch for a sample three-tier service.\n"
"- **Dashboard sketch**: golden signals up top, drill-down paths, deploy annotations, time-range comparisons — organized by the questions on-call asks at 3am.\n"
"- **Alerting policy table**: each alert named, its signal, its threshold or burn rate, and its route (page vs ticket) with a one-sentence justification.\n"
"- **Tracing plan**: which service boundaries get instrumented first and what question the traces answer (latency attribution across services).\n"
"- **Cardinality budget**: the label set with a written rule for what may never become a label.\n"
"- **Present it as a 10-minute design review**, then record the two objections raised and your revised answers.\n"
"Reference shelf (module sources): **Prometheus Documentation** (https://prometheus.io/docs/) — metrics, PromQL, and alerting. **Grafana Documentation** (https://grafana.com/docs/) — dashboards and alerting. **OpenTelemetry Documentation** (https://opentelemetry.io/docs/) — vendor-neutral tracing, metrics, and logs."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and a paper dashboard is not a production monitoring system. "
"Real alert tuning takes weeks of paging history; your first thresholds will be wrong, and that's normal — the module teaches the structure (symptoms page, causes inform) that makes tuning converge. "
"Vendor specifics follow vendor documentation, which changes; verify current PromQL, Grafana, and OpenTelemetry syntax against the linked sources as of their retrieval dates."
)},
],
"sre-interview-prep--sre-capacity": [
{"title": "Concepts", "body": (
"- **Headroom** — spare capacity held deliberately above forecast peak: the margin that absorbs bursts and failures.\n"
"- **N+1** — provision N+1 units for a load needing N: one unit can fail or drain without user impact.\n"
"- **Utilization wall** — queueing theory's warning: latency degrades nonlinearly as utilization nears 100%; the wall is where small load increases cause large latency spikes.\n"
"- **Horizontal scaling** — more units (HPA adds pod replicas): the cloud-native default.\n"
"- **Vertical scaling** — bigger units (VPA resizes pods): for workloads that can't scale out; needs restarts.\n"
"- **Autoscaling lag** — scaling isn't instant: cold starts and metric delays mean you still need headroom.\n"
"- **Load test** — synthetic demand proving the capacity model: k6 for code-reviewed, CI-integrated tests with thresholds as gates.\n"
"- **Spot/preemptible capacity** — spare compute at deep discounts for interruption-tolerant batch work that checkpoints.\n"
"- **N+1 query problem** — the database cousin: N parents fetched, then one query per parent's children; fixed by eager loading (JOIN or batched query)."
)},
{"title": "Worked estimation", "body": (
"Work this capacity estimate with stated assumptions — the interview grades the method, not the numbers.\n"
"1. **State the forecast as a range.** 'Peak 8,000–12,000 requests/sec during the holiday week, based on last year's growth plus the marketing launch.' Ranges with assumptions, reviewed on a cadence.\n"
"2. **Measure per-unit capacity.** From a load test: one instance sustains 500 rps at p99 < 200 ms. Write it down — measured, not guessed.\n"
"3. **Divide, then add headroom.** 12,000 ÷ 500 = 24 instances at 100% — which is the wall. Target 65% utilization: 24 ÷ 0.65 ≈ 37 instances.\n"
"4. **Apply N+1.** 37 + 1 = 38 instances, so one can drain for deploy or fail outright without breaching the SLO.\n"
"5. **Price the headroom.** Those ~14 extra instances are the cost of burst absorption and failure tolerance — narrate it: 'headroom is insurance with a line item.'\n"
"6. **Name the verification.** A k6 test at 1.5× forecast peak with thresholds as CI gates, re-run before every launch — the model is a hypothesis until the test confirms it."
)},
{"title": "Project brief", "body": (
"Your deliverable: a one-page capacity plan for a sample API facing a 3× holiday traffic spike.\n"
"- **Forecast**: a demand range with stated assumptions (growth rate, events, seasonality).\n"
"- **The math**: per-unit measured capacity, utilization target (away from the wall), headroom, and the N+1 count — shown the way the Worked estimation shows it.\n"
"- **Scaling policy**: HPA vs VPA choice with the autoscaling-lag caveat, and what stays statically provisioned.\n"
"- **Load-test plan**: k6 scenarios with pass/fail thresholds as gates, and what each scenario proves.\n"
"- **Cost note**: the price of the headroom and the cheaper alternative (spot/preemptible for the batch tier) with its tradeoff.\n"
"- **Defend it in 10 minutes aloud**, ending with the line: 'I plan headroom against the wall, not against the average.'\n"
"Reference shelf (module sources): **Google SRE Books** (https://sre.google/) — capacity planning chapters from the source. **Kubernetes Documentation** (https://kubernetes.io/docs/) — HPA/VPA and workload references."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and worked estimates use assumed numbers to teach method. "
"Real capacity numbers come from your system's load tests, not from this module — never quote the example figures as facts about any real service. "
"The transferable skill is the structure: forecast as ranges, measure per-unit capacity, hold headroom off the wall, verify with tests, and narrate the cost."
)},
],
"sre-interview-prep--sre-design-reps": [
{"title": "Concepts", "body": (
"- **RPO (Recovery Point Objective)** — how much data loss is tolerable: bounds backup frequency.\n"
"- **RTO (Recovery Time Objective)** — how fast recovery must complete: bounds downtime.\n"
"- **Active-passive** — one region serves, one stands by: simpler failover, idle cost.\n"
"- **Active-active** — both regions serve: no idle cost, but needs conflict resolution for writes.\n"
"- **Backpressure** — when consumers lag producers, pressure must go somewhere: bounded queues that block or shed, so slowness propagates instead of memory growing until collapse.\n"
"- **Load shedding** — deliberately dropping low-priority work to protect the core: a choice, unlike uncontrolled collapse.\n"
"- **Cache stampede / thundering herd** — cold-start or hot-key-expiry floods that hit the origin at once; defenses include request coalescing and staggered TTLs.\n"
"- **Circuit breaker** — fails fast to a degraded path when a dependency is down, instead of piling up doomed requests.\n"
"- **Graceful degradation** — serving stale or reduced functionality during an outage: slightly old data beats no data."
)},
{"title": "Hands-on procedure", "body": (
"Run a 45-minute design rep on 'design a multi-region web service', with a timer.\n"
"1. **Requirements (5 min).** Ask: users, read/write ratio, latency target, consistency needs. Write RPO/RTO as the business answers them.\n"
"2. **Estimation (5 min).** Back-of-envelope: requests/sec, storage, bandwidth. Show the arithmetic; say the assumptions.\n"
"3. **Happy path (10 min).** Draw: DNS/anycast → regions → LB → app → cache → DB. Label every arrow with what flows.\n"
"4. **Reliability pass (10 min).** For each component: what breaks, what the blast radius is, the mitigation — active-passive vs active-active with the cost stated, queue backpressure, cache failure story, load-shedding policy.\n"
"5. **Bottlenecks (10 min).** Walk the request path asking 'what breaks first at 10×?' and apply the right lever: shard, cache, or queue.\n"
"6. **Tradeoffs summary (5 min).** Three sentences: what you optimized for, what you paid, when you'd choose differently. End by inviting the follow-up."
)},
{"title": "Project brief", "body": (
"Your deliverable: six one-page design briefs — the portfolio you walk an interviewer through.\n"
"- **Multi-region web service**, **HA database**, **queued pipeline with backpressure**, **caching layer with a failure story**, **rate limiting + load shedding**, and **one of your choosing**.\n"
"- Each brief: requirements, estimation, the 2–3 key decisions, the scaling story, the failure modes with mitigations, and the cost-vs-reliability tradeoff stated honestly.\n"
"- **Rehearse each aloud in 15 minutes**, then write the hardest follow-up question you can imagine and answer it in writing.\n"
"- Keep the briefs to one page each: the constraint forces the prioritization that interviews grade.\n"
"Reference shelf (module sources): **Google SRE Books** (https://sre.google/) — reliability design chapters. **AWS Documentation** (https://docs.aws.amazon.com/) — service primitives for the designs."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and whiteboard designs are not production architectures. "
"Real multi-region systems carry consistency, cost, and operational burdens that a 45-minute rep compresses away; never present a rep as a shipped design. "
"What the reps train is the interview's actual skill: structured reasoning under ambiguity, defended tradeoffs, and the honesty to say 'multi-region is a business decision with an engineering price.'"
)},
],
"sre-interview-prep--sre-mock": [
{"title": "Concepts", "body": (
"- **Mock circuit** — the full simulated loop: incident round, metrics/SLO round, system-design round, behavioral round, run back-to-back under time.\n"
"- **Round shape** — the fixed structure each round type follows: rehearse the shape and the method becomes automatic under pressure.\n"
"- **Interview rubric** — fixed scoring axes per round (correctness, complexity analysis, communication, time management, tradeoffs named): turns feelings into triage data.\n"
"- **Debrief log** — the written record after every mock: what leaked, its category, the redrill plan. Improvement lives here, not in doing more mocks.\n"
"- **Weakness-targeting week** — the week between simulation and the real loop, spent only on the lowest rubric scores: raise the floor, not the ceiling.\n"
"- **Taper** — the final two weeks: no new material, redrill weak patterns, full timed mocks, fix sleep, rehearse the story bank aloud.\n"
"- **48-hour checklist** — logistics, rest, rehearsed stories, no new topics: the last two days convert preparation into performance."
)},
{"title": "Hands-on procedure", "body": (
"Run one full mock circuit this week — schedule it like a real loop day.\n"
"1. **Book the day.** Four 45-minute rounds with 15-minute breaks: incident, metrics/SLO, system design, behavioral. A partner plays interviewer; trade roles next time.\n"
"2. **Set the rules.** Timed, no pausing, think aloud the whole way. The interviewer scores against the rubric during the round, not after.\n"
"3. **Run the incident round.** Declare, mitigate first, comms cadence — the shape from the incident module, narrated.\n"
"4. **Run the metrics round.** Define SLIs, do the budget math, name the burn-rate alerts — the shape from the SLO module.\n"
"5. **Run the design round.** Requirements → estimation → HA design → failure modes — the shape from the design module.\n"
"6. **Debrief in writing within the hour.** Score each axis, name the lowest two, and write the weakness-targeting plan: what you'll redrill, and how you'll verify. Then rest — the taper has started."
)},
{"title": "Project brief", "body": (
"Your deliverable: a scored mock-loop dossier.\n"
"- **The schedule**: your four-round loop day with times, roles, and the rubric each round is scored against.\n"
"- **Score sheets**: one per round, every axis scored honestly — correctness, communication, time management, tradeoffs named.\n"
"- **The debrief**: the two lowest-scoring axes, the category of each miss (not just the instance), and a one-week redrill plan with verification.\n"
"- **The 48-hour checklist**: your personal version — logistics, sleep, story bank, what you will explicitly not study.\n"
"- **Reflection**: one paragraph on which round shape still isn't automatic, and the drill that will make it so.\n"
"Reference shelf (module sources): **Google SRE Books** (https://sre.google/) — the reliability material the mocks draw on."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and mock scores are not predictions of real outcomes. "
"Partners are kinder than hiring panels, and home whiteboards lack loop-day adrenaline; treat scores as triage data for your preparation, not as forecasts. "
"The honest value of the circuit is narrower and real: automatic round shapes, a debrief habit, and a weakness-targeting plan — which is exactly what converts knowledge into interview performance."
)},
],
}

P1_NEW_CARDS = {
"sre-interview-prep--sre-sli-slo": {
"front": "How do you size an error budget on a whiteboard?",
"back": "99.9% over 30 days → 0.1% of 43,200 minutes = 43.2 minutes of total allowed badness per month. Say it as policy: 'our budget is roughly one real incident a month — while budget remains we ship, when it's spent we harden.' The interview line: 'budgets are arithmetic, not vibes.'",
},
"sre-interview-prep--sre-incident-command": {
"front": "When do you escalate an incident's severity?",
"back": "When the impact scope grows: more users affected, a longer blast radius, or the mitigation isn't working. Severity follows impact, not effort — and the paging policy decides who the escalation wakes. The interview line: 'I escalate on impact, early; downgrading is cheaper than discovering the blast radius at the postmortem.'",
},
"sre-interview-prep--sre-monitoring": {
"front": "How do you decide what belongs in logs vs metrics?",
"back": "Metrics get the countable and the alertable — rates, latencies, saturations with bounded labels. Logs get the discrete and the contextual — errors with request IDs, decisions, anomalies to investigate. Traces get the cross-service journey. The interview line: 'if I'd page on it, it's a metric; if I'd investigate with it, it's a log.'",
},
"sre-interview-prep--sre-capacity": {
"front": "What do you load-test before a launch, and what makes the test a gate?",
"back": "The forecast peak (at 1.5× for margin), a soak run for leaks, and a spike run for autoscaling lag — each with pass/fail thresholds written before the test runs. A threshold decided after the results is decoration; decided before, it's a gate. The interview line: 'the load test is a hypothesis test on my capacity model.'",
},
"sre-interview-prep--sre-design-reps": {
"front": "How do you defend a caching choice in a design round?",
"back": "Name what you cache and why, the invalidation story, and the failure story: stampede on cold start, thundering herd on hot-key expiry, and what happens when the cache itself dies (stale-while-revalidate, circuit breaker). The interview line: 'caching is a tradeoff with an invalidation plan, not a speedup.'",
},
"sre-interview-prep--sre-mock": {
"front": "What's on your 48-hour pre-interview checklist?",
"back": "Logistics confirmed, sleep protected, story bank rehearsed aloud, the two weakest round shapes redrilled once more — and explicitly: no new topics. The checklist converts preparation into performance; cramming converts it into noise. The interview line: 'the last 48 hours are about the performer, not the material.'",
},
}

def _q(q, choices, answer, explain):
    assert len(choices) == 4 and 0 <= answer <= 3 and explain
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}

P1_NEW_QUIZ = {
"sre-interview-prep--sre-sli-slo": [
_q("A 99.9% SLO over a 30-day window leaves an error budget of about:",
   ["4.3 minutes", "43.2 minutes", "7.2 hours", "3 full days"], 1,
   "30 days = 43,200 minutes; 0.1% of that is 43.2 minutes — the Worked estimation in this module."),
_q("For a nightly batch pipeline with no user requests, the right SLI is:",
   ["Request latency", "Successful job completions ÷ total jobs", "CPU utilization", "Deploy frequency"], 1,
   "SLIs must measure what the user experiences — for batch, that's jobs completing correctly and on time, per the Concepts."),
_q("SLOs are set below 100% because:",
   ["Users can't do math", "Each extra nine costs disproportionately more while users can't perceive the difference", "Monitoring can't measure 100%", "Budgets require failure"], 1,
   "Reliability has an asymptote: the last nines are the most expensive and least felt — the budget exists to spend on velocity instead."),
_q("Recording rules exist in a Prometheus SLO setup to:",
   ["Delete old data", "Precompute expensive SLI ratio queries so dashboards and alerts stay cheap", "Send pages", "Label time series"], 1,
   "SLI ratios over 30-day windows are expensive to compute live; recording rules compute them once, per the Concepts."),
_q("A slow-burn alert (budget draining over days) should route to:",
   ["The on-call pager immediately", "A ticket for business-hours investigation", "The CEO", "Nowhere — ignore it"], 1,
   "Paging is for user impact at risk now; slow burns get tickets — the alerting policy in the Project brief."),
_q("A '30-day rolling window' for an SLO means:",
   ["It resets on the 1st of each month", "It always covers the trailing 30 days from now", "It covers the next 30 days", "It equals a calendar month"], 1,
   "Rolling windows slide with time — the measurement window in this module's Concepts, not a calendar reset."),
],
"sre-interview-prep--sre-incident-command": [
_q("The first act of incident response is:",
   ["Debugging the root cause", "Declaring the incident and assigning IC, Communications, and Scribe", "Writing the postmortem", "Paging everyone"], 1,
   "Nothing starts until someone says 'incident' and the roles exist — step 1 of the Hands-on procedure."),
_q("During an outage with no new information, Communications should:",
   ["Stay silent until there's news", "Post the scheduled update anyway — 'no update, next check-in at :30'", "Speculate on the cause", "Blame the last deploy"], 1,
   "The cadence is the product: silence during an outage is a second outage, per the Concepts."),
_q("The Scribe's most important artifact is:",
   ["The chat log", "The timestamped timeline of decisions and actions", "The alert config", "The deploy history"], 1,
   "The timeline is the postmortem's raw material — the Scribe owns it from minute one."),
_q("'Mitigate first, understand second' means the IC should prefer:",
   ["A perfect diagnosis before acting", "The fastest bleed-stopper available, e.g. rollback or load shed", "Waiting for more data", "Restarting everything"], 1,
   "Mitigation stops user impact; diagnosis can follow — step 3 of the Hands-on procedure."),
_q("A good postmortem action item always has:",
   ["A blame assignment", "An owner and a date", "Management approval", "A 50-page report"], 1,
   "The postmortem's value is the action items, not the document — owner plus date makes them real."),
_q("Paging policy exists to answer:",
   ["Who writes the postmortem", "Which severities wake whom, and how fast", "What the SLO is", "When deploys happen"], 1,
   "Severity without a paging policy is vocabulary; the policy turns it into action, per the Concepts."),
],
"sre-interview-prep--sre-monitoring": [
_q("OpenTelemetry's role in an observability stack is:",
   ["Replacing Prometheus", "Vendor-neutral instrumentation for traces, metrics, and logs", "A dashboard product", "An alerting pager"], 1,
   "OpenTelemetry standardizes how telemetry is produced so backends become interchangeable — Project brief reference shelf."),
_q("A latency spike that only appears on one endpoint is best localized with:",
   ["A CPU graph", "Distributed traces showing the request's journey across services", "Log volume counts", "The deploy calendar"], 1,
   "Traces show where the time goes across service boundaries — 'traces show me where,' per the Concepts."),
_q("Putting a request ID in a Prometheus label is wrong because:",
   ["Labels can't hold strings", "It's unbounded cardinality — millions of series, like the user_id example in this module", "It's PII only", "Queries get faster"], 1,
   "Request IDs belong in logs/traces; as labels they'd explode series count — the cardinality audit in the Hands-on procedure."),
_q("The top row of an incident-ready dashboard shows:",
   ["Every metric available", "The four golden signals", "Server inventory", "Cost graphs"], 1,
   "Golden signals up top, drill-down below — organized by the questions on-call asks at 3am, per the Project brief."),
_q("A RED dashboard suits the API service while a USE dashboard suits its database host because:",
   ["RED is newer", "RED describes service behavior from the requester's view; USE describes resource internals", "USE can't do latency", "They're interchangeable"], 1,
   "Match the lens to the question: 'is the service healthy' vs 'is the box healthy' — the Hands-on procedure step 4."),
_q("Alerting on 'disk 90% full' as a page is usually wrong because:",
   ["Disks never fill", "It's a cause metric, not a user symptom — it belongs ticketed or dashboarded, not paging", "90% is too low", "Alerts can't read disks"], 1,
   "Pages mean user impact; cause metrics inform diagnosis — the alerting policy in the Project brief."),
],
"sre-interview-prep--sre-capacity": [
_q("Forecasts should be expressed as ranges because:",
   ["Precision is impossible", "Ranges carry the assumptions openly and get reviewed on a cadence; point forecasts pretend certainty", "Math is hard", "Managers like ranges"], 1,
   "The interview line from this module: 'forecasts are ranges with assumptions, reviewed on a cadence.'"),
_q("The 65% utilization target in the Worked estimation exists to:",
   ["Save money", "Stay clear of the utilization wall, where queueing makes latency spike nonlinearly", "Match the SLO", "Please finance"], 1,
   "Provisioning at 100% is provisioning at the wall — headroom is the distance from it."),
_q("VPA is chosen over HPA when the workload:",
   ["Is stateless", "Can't scale out and needs bigger pods instead, accepting restarts", "Is cheap", "Runs on spot"], 1,
   "Horizontal is the default; vertical is for workloads that can't add replicas — the Concepts."),
_q("Autoscaling alone doesn't remove the need for headroom because:",
   ["It's expensive", "Scaling lags — cold starts and metric delays mean bursts hit before new capacity arrives", "It needs Kubernetes", "It only scales down"], 1,
   "The interview caveat: autoscaling isn't instant, so bursts still need provisioned margin."),
_q("A k6 threshold written before the test run acts as:",
   ["Documentation", "A CI gate — pass/fail decided in advance, not negotiated after the results", "A comment", "A dashboard"], 1,
   "Thresholds decided after the results are decoration; decided before, they're gates — Project brief."),
_q("Running the same service on spot instances for its batch tier is justified when:",
   ["It's faster", "The work checkpoints and tolerates interruption, buying spare capacity at deep discounts", "It's more reliable", "On-demand is banned"], 1,
   "Price follows preemptibility — interruption-tolerant work is the fit, per the Concepts."),
],
"sre-interview-prep--sre-design-reps": [
_q("Stating RPO/RTO before drawing architecture is strong because:",
   ["It's traditional", "They're business answers that constrain the design — backup frequency and downtime tolerance", "Interviewers require it", "It fills time"], 1,
   "Design follows constraints; RPO/RTO turn 'be reliable' into numbers, per the Hands-on procedure."),
_q("Active-active multi-region is harder than active-passive mainly due to:",
   ["Cost", "Write conflict resolution and consistency tradeoffs across regions", "DNS", "Latency"], 1,
   "Both regions serving means reconciling divergent writes — the complexity price in the Concepts."),
_q("A circuit breaker protects a service by:",
   ["Retrying forever", "Failing fast to a degraded path instead of piling up doomed requests on a dead dependency", "Adding caches", "Shedding all traffic"], 1,
   "Fast failure bounds the blast radius of a dead dependency — the reliability pass in the Hands-on procedure."),
_q("Labeling every arrow in a design diagram matters because:",
   ["It's pretty", "Unlabeled arrows hide the data story — the labels are where the design lives", "Tools require it", "It's traditional"], 1,
   "Architecture is data in motion; the labels carry the design's meaning — Project brief standard."),
_q("The 'what breaks first at 10×' question is asked at each hop to:",
   ["Sound dramatic", "Find the first bottleneck in order, then apply the right lever — shard, cache, or queue", "Do math", "Impress the interviewer"], 1,
   "Bottlenecks are found by walking the path, not by guessing — step 5 of the Hands-on procedure."),
_q("Ending a design round with tradeoffs ('here's what I paid') is strong because:",
   ["It's humble", "It proves engineering judgment — every choice costs something, and seniors name the price", "It's short", "Interviewers are cheap"], 1,
   "The interview grades tradeoff reasoning under ambiguity — the 5-minute summary in the Hands-on procedure."),
],
"sre-interview-prep--sre-mock": [
_q("The single highest-value activity in the hour after a mock is:",
   ["Another mock immediately", "A written debrief naming what leaked and its category, plus a redrill plan", "Reading model answers", "A week off"], 1,
   "Improvement comes from the feedback loop: name the leak, target the redrill — the Concepts' debrief log."),
_q("Rotating interviewer roles with a partner helps because:",
   ["It's fun", "Playing interviewer teaches you what answers are gradable — you learn the rubric from the other side", "It's required", "It's faster"], 1,
   "Seeing answers through the rubric's eyes is the fastest way to produce gradable answers yourself."),
_q("The taper's 'no new material' rule exists because:",
   ["New material is hard", "Performance comes from consolidation and recovery, not last-minute breadth", "Books are closed", "Partners quit"], 1,
   "The final two weeks convert knowledge into performance; cramming adds noise — the Concepts."),
_q("A rubric axis like 'tradeoffs named' is scored because:",
   ["It's easy", "Interviews grade judgment under ambiguity, and named tradeoffs are its evidence", "It's traditional", "Candidates like it"], 1,
   "What gets scored gets prepared: the rubric turns the interview's hidden grading into visible targets."),
_q("Between rounds on loop day, the best use of a 15-minute break is:",
   ["Cramming notes", "Resetting: water, notes closed, one breath — each round starts clean", "Checking email", "Rehearsing answers"], 1,
   "Stamina and context-switching are trained skills; breaks protect them — the loop-day schedule in the Hands-on procedure."),
_q("The weakness-targeting week targets the floor rather than the ceiling because:",
   ["It's easier", "Offers are lost on weak rounds, not won on strong ones — the minimum decides", "Strong areas don't matter", "It's faster"], 1,
   "Loops grade the weakest link; raising the floor raises the whole loop — the Concepts."),
],
}
