#!/usr/bin/env python3
"""Build IL28-M46 module object -> part_f_m46.json"""
import json

notes = [
{"title": "SLIs, SLOs, and Error Budgets",
"body": "A Service Level Indicator (SLI) is what you measure — e.g. the fraction of checkout requests that succeed within 500ms. A Service Level Objective (SLO) is the target — 99.9% of checkouts succeed within 500ms over a 30-day window. The error budget is the allowed failure: 100% minus the SLO, so 99.9% leaves a 0.1% budget. Error budgets turn reliability into a currency: while budget remains, the team may ship features and take risks; when the budget burns out, all engineering effort shifts to reliability until it recovers. Worked example: checkout serves 10 million requests in 30 days with a 99.9% SLO. Error budget = 0.1% x 10M = 10,000 failed requests. After a bad deploy causes 8,000 failures in one day, the remaining budget is 2,000 — the release freeze policy triggers (say, below 25% remaining), so the next two feature releases are held and the team works on the flaky payment dependency instead. Solution logic: budgets make the ship-vs-stabilize tradeoff explicit and pre-agreed, so it is policy, not politics. The trap: SLOs without consequences are vanity metrics — an SLO nobody acts on teaches the organization to ignore all SLOs."},
{"title": "Burn Rate: How Fast Are You Spending Reliability?",
"body": "Burn rate measures how fast the error budget is being consumed relative to the SLO window. A burn rate of 1 spends budget exactly on target; 10 burns ten times too fast. Alerting on burn rate (rather than raw error counts) is the Google SRE practice because it is self-normalizing: it works for 10 requests/sec and 10,000 alike. The standard setup uses two alert speeds: a fast-burn alert (e.g. burn rate 14 over 1 hour — pages immediately, you will exhaust budget in days) and a slow-burn alert (burn rate 3 over 6 hours — tickets, you are leaking budget steadily). Worked example: SLO 99.9% over 30 days; in the last hour, errors ran at 2% against a 0.1% budget. Burn rate = 2% / 0.1% = 20. At this pace the 30-day budget dies in 1.5 days — page now. Contrast: errors at 0.3% sustained for 6 hours gives burn rate 3 — a ticket, investigated today, not a 3 AM page. Solution: configure both alerts; the fast one protects the budget, the slow one catches the bleed. The anti-pattern is alerting on absolute thresholds ('more than 100 errors') — it pages the low-traffic service for noise and sleeps through the high-traffic service's real outage. Burn rate alerts scale with the service."},
{"title": "Alert Routing and On-Call Design",
"body": "Alerts must reach the right human with the right context in minutes. The routing chain: detection (Prometheus alert rule or Azure Monitor alert) -> notification grouping (Alertmanager groups by service/severity to prevent 200 separate pages for one outage) -> on-call schedule (who is primary this week) -> escalation policy (no ack in 10 min -> secondary; 20 min -> manager). Alert quality rules: every page must be actionable (the runbook link tells you what to do), every page must be urgent (if it can wait until morning, it is a ticket, not a page), and alerts need severity tiers — critical (page), warning (ticket), info (dashboard). Worked example: design routing for the checkout service. Solution: Prometheus rule 'CheckoutHighErrorBudgetBurn' (fast-burn) -> Alertmanager route matching service=checkout, severity=critical -> PagerDuty/on-call primary with a runbook link to the checkout triage doc; slow-burn -> ticketing queue with a 4-hour SLA; deploy annotations feed the dashboard so the responder sees what shipped. The on-call health metric: pages per shift. More than 2-3 pages per on-call week means the alerts are miscalibrated or the service is genuinely unhealthy — either way, the fix is engineering, not heroics. Alert fatigue kills response quality faster than any outage."},
{"title": "Incident Roles and the First 30 Minutes",
"body": "Incidents need roles, not heroes. The three core roles: Incident Commander (coordinates, makes decisions, keeps the timeline — does NOT debug), Communications Lead (status page and stakeholder updates every 15-30 minutes), and Responders (diagnose and mitigate). The first-30-minutes protocol: (1) declare the incident and page the roles (2 min); (2) assess blast radius from dashboards — which services, which users, since when (5 min); (3) mitigate first, root-cause later — roll back the deploy, fail over, shed load, or flip the feature flag (10 min); (4) communicate the current status and next update time (ongoing). Worked example: checkout p99 triples at 14:02, deploy went out at 13:55. The Responder wants to read code; the Commander orders the rollback first. Solution: rollback at 14:08, p99 recovers by 14:12, incident downgraded — root-causing the bad query happens after, in the postmortem, with no users still bleeding. The principle: mitigation before diagnosis. Every minute of 'let me just check one thing' while users fail is a choice to keep the outage running. Declare early — a false alarm costs a page; a late declaration costs an outage."},
{"title": "Blameless Postmortems and the Five Whys",
"body": "A blameless postmortem asks what allowed the failure, never who caused it — because blame suppresses the reporting that prevention depends on. The document has a fixed shape: summary, impact (duration, affected users/requests), timeline (detection, mitigation, resolution with timestamps), root causes (usually 2-3 contributing factors, never one), and action items (each with an owner and a due date — an action item without an owner is a wish). The Five Whys drill past the proximate cause: 'Checkout failed' -> why? 'Payment service timed out' -> why? 'Its connection pool was exhausted' -> why? 'A retry storm from the bad deploy multiplied load 8x' -> why? 'No retry budget or circuit breaker on that client' -> why? 'Resilience patterns were never added to the integration checklist.' The fix lands at the fifth why, not the first. Worked example: write the action items for the retry-storm outage. Solution: (1) add circuit breaker + retry budgets to the payment client — owner: payments team, due in 2 weeks; (2) add a deploy-canary error-budget gate — owner: platform team, due in 1 month; (3) load-test retry behavior in staging — owner: QA, due in 3 weeks. Each is verifiable; each prevents recurrence rather than punishing the deployer."},
{"title": "Runbooks: The Lab You Write Before the Fire",
"body": "A runbook is the written procedure for a known failure mode — diagnosis steps, mitigation commands, escalation criteria, and rollback instructions — kept where the on-call can reach it at 3 AM. A good runbook has: symptoms (what the alert looks like), blast radius check (the two dashboard links), diagnosis (the exact kubectl/PromQL/KQL commands), mitigation (the exact commands, copy-pasteable), escalation (when to wake the secondary, when to declare a major incident), and rollback. Runbooks decay: every postmortem must update the runbook it used, and runbooks get a quarterly review owner. Worked example: the checkout error-budget runbook. Symptoms: fast-burn alert fires. Diagnosis: (1) kubectl get pods -n checkout (CrashLoopBackOff?); (2) Prometheus: 5xx ratio by pod (one pod or all?); (3) check deploy annotations (did something just ship?). Mitigation: if one bad pod — kubectl delete pod to reschedule; if post-deploy — kubectl rollout undo deployment/checkout; if downstream — flip the payment feature flag off. Escalation: no improvement in 15 min -> page secondary + declare major. Solution review: every step is a command, not prose; the responder never has to invent triage while stressed. The lab below has you write and then execute one — because a runbook you have never run is a rumor, not a procedure."},
]

cards = [
{"front": "SLI vs SLO vs error budget (with numbers)", "back": "SLI: measured (fraction of checkouts succeeding <500ms). SLO: target (99.9% over 30d). Budget: 100% - SLO = 0.1% allowed failures"},
{"front": "Error budget math: 10M requests, 99.9% SLO", "back": "Budget = 0.1% x 10M = 10,000 failed requests per 30 days; policy (e.g. freeze below 25% remaining) makes ship-vs-stabilize pre-agreed"},
{"front": "What is burn rate?", "back": "Error-budget consumption speed relative to the SLO window; 1 = on target, 10 = ten times too fast"},
{"front": "Fast-burn vs slow-burn alerts", "back": "Fast-burn (e.g. rate 14 over 1h): page now, budget dies in days. Slow-burn (e.g. rate 3 over 6h): ticket, steady leak"},
{"front": "Why alert on burn rate instead of absolute error counts?", "back": "Self-normalizing across traffic levels: absolute thresholds page low-traffic services for noise and miss real outages on high-traffic ones"},
{"front": "Alert routing chain (4 stages)", "back": "Detection -> grouping (Alertmanager) -> on-call schedule -> escalation policy (no-ack timers)"},
{"front": "Three rules of alert quality", "back": "Every page actionable (runbook link), every page urgent (else it is a ticket), severity tiers (critical/warning/info)"},
{"front": "Incident roles (3) and the Commander's job", "back": "Incident Commander (coordinates/decides, does NOT debug), Communications Lead (updates every 15-30 min), Responders (diagnose/mitigate)"},
{"front": "First-30-minutes protocol", "back": "Declare + page (2 min) -> assess blast radius (5 min) -> mitigate first: rollback/failover/shed load (10 min) -> communicate on a cadence"},
{"front": "Mitigation before diagnosis — why?", "back": "Every minute of investigating while users fail extends the outage; roll back first, root-cause in the postmortem"},
{"front": "Blameless postmortem: fixed shape", "back": "Summary, impact, timeline, root causes (contributing factors), action items — each with owner + due date"},
{"front": "What does the Fifth Why usually reveal?", "back": "The systemic gap (missing checklist, absent pattern, untested behavior) — the fix lands at the fifth why, not the first"},
{"front": "Runbook required sections", "back": "Symptoms, blast-radius check, diagnosis commands, mitigation commands, escalation criteria, rollback — all copy-pasteable"},
{"front": "On-call health metric", "back": "Pages per shift: >2-3/week means miscalibrated alerts or a genuinely unhealthy service — fix with engineering, not heroics"},
]

quiz = [
{"q": "Checkout: 10M requests/30d, SLO 99.9%. A bad deploy causes 8,000 failures in a day. What happens under a 25%-remaining freeze policy?",
"choices": ["Nothing", "Remaining budget is 2,000 of 10,000 (20%) — below 25%, so feature releases freeze and effort shifts to reliability", "The SLO is raised", "The budget resets"],
"answer": 1,
"explain": "Budget = 10,000; 8,000 spent leaves 20%, under the 25% threshold. The policy converts the tradeoff into a pre-agreed action, not a debate."},
{"q": "SLO 99.9%/30d. Last hour errors ran at 2% vs 0.1% budget. What is the burn rate and response?",
"choices": ["Burn rate 2, ticket", "Burn rate 20 — page immediately; budget dies in ~1.5 days at this pace", "Burn rate 0.2, ignore", "Cannot compute"],
"answer": 1,
"explain": "Burn rate = observed error ratio / budget ratio = 2%/0.1% = 20. Fast-burn threshold crossed: page now."},
{"q": "Errors at 0.3% sustained for 6 hours against a 0.1% budget. Response?",
"choices": ["Page immediately", "Slow-burn: ticket it for investigation today — a steady leak, not an imminent exhaustion", "Ignore", "Roll back everything"],
"answer": 1,
"explain": "Burn rate 3 over hours is the slow-burn pattern: real, worth a ticket with an SLA, but not a 3 AM page."},
{"q": "Which alert deserves to be a page?",
"choices": ["Disk at 70% with weeks of headroom", "Fast-burn error-budget alert with a runbook link and a mitigation command", "A daily report", "CPU at 50%"],
"answer": 1,
"explain": "Pages must be actionable and urgent. Disk at 70% is a ticket; the burn alert names the failure and the fix."},
{"q": "During an incident, the Responder wants to keep debugging while users fail. The Commander should:",
"choices": ["Let them continue", "Order mitigation first (rollback/failover) — diagnosis happens after users stop bleeding", "End the incident", "Blame the deployer"],
"answer": 1,
"explain": "Mitigation before diagnosis is the core protocol; root-causing belongs in the postmortem, not in the outage window."},
{"q": "Who writes the status updates during an incident?",
"choices": ["The Incident Commander", "The Communications Lead, every 15-30 minutes", "Whoever is free", "Nobody until it is over"],
"answer": 1,
"explain": "Dedicated comms role on a cadence keeps stakeholders informed and keeps responders free to mitigate."},
{"q": "A postmortem action item reads 'be more careful next time'. What is wrong?",
"choices": ["Nothing", "No owner, no due date, not verifiable — it is blame in disguise, not prevention", "It is too specific", "Postmortems should not have actions"],
"answer": 1,
"explain": "Action items need owner + due date + verifiability, and must fix the system (the fifth why), not scold the human."},
{"q": "Five Whys on a retry-storm outage ends at 'resilience patterns were never in the integration checklist'. What does this tell you?",
"choices": ["The deployer is at fault", "The systemic fix: add circuit breakers/retry budgets to the checklist — the first why (timeout) was only the proximate cause", "Retries should be banned", "Checklists do not work"],
"answer": 1,
"explain": "The fifth why reveals the process gap; fixing it prevents the whole class of outage. Stopping at the first why just restarts the timer."},
{"q": "On-call gets 8 pages a week, all actionable but exhausting. What is the correct response?",
"choices": ["Hire more on-call", "Treat it as an engineering problem: recalibrate thresholds, fix flaky alerts, and address the underlying reliability debt", "Ignore some pages", "Make pages louder"],
"answer": 1,
"explain": "Pages-per-shift is a health metric; sustained high paging means miscalibrated alerts or real unreliability — both fixed with engineering, not endurance."},
]

drills = [
{"id": "il28-m46-slo-math", "title": "Timed drill: SLO math under pressure",
"items": [
{"prompt": "Define SLI, SLO, error budget in one breath.", "answer": "SLI: what you measure. SLO: the target over a window. Budget: 100% minus SLO — the allowed failures.",
"explain": "One breath, three terms — the panel's warm-up."},
{"prompt": "10M requests, 99.9% SLO. Budget?", "answer": "10,000 failed requests per 30 days.",
"explain": "0.1% of 10M — show the arithmetic, not just the number."},
{"prompt": "8,000 failures spent, freeze policy at 25% remaining. Decision?", "answer": "20% remains — below threshold: freeze features, shift to reliability.",
"explain": "Policy makes it automatic — say 'pre-agreed, not political'."},
{"prompt": "Errors at 2%/hour vs 0.1% budget. Burn rate and action?", "answer": "Burn rate 20 — page now; budget dies in ~1.5 days.",
"explain": "Observed/budget = 20. Fast-burn = page."},
{"prompt": "Errors at 0.3% for 6 hours. Burn rate and action?", "answer": "Burn rate 3 — ticket for today; slow-burn leak.",
"explain": "Contrast with the previous item — the panel wants both speeds."},
{"prompt": "Why burn-rate alerts instead of 'more than 100 errors'?", "answer": "Self-normalizing: absolute counts page quiet services for noise and miss loud-service outages.",
"explain": "Scales with the service — the SRE-correct answer."},
{"prompt": "SLO with no consequences is what?", "answer": "A vanity metric — teaches the org to ignore all SLOs.",
"explain": "Consequences (freeze policy) are what make SLOs real."},
]},
{"id": "il28-m46-incident", "title": "Timed drill: incident command",
"items": [
{"prompt": "Name the three incident roles and the Commander's one rule.", "answer": "Commander (coordinates, never debugs), Comms Lead (updates every 15-30 min), Responders (mitigate).",
"explain": "The Commander's rule — does not debug — is what the panel listens for."},
{"prompt": "First 30 minutes: the four beats.", "answer": "Declare+page, assess blast radius, mitigate first, communicate on cadence.",
"explain": "Say the timeboxes: 2 / 5 / 10 minutes, then ongoing comms."},
{"prompt": "p99 triples 7 minutes after a deploy. First action?", "answer": "Rollback the deploy — mitigation before diagnosis.",
"explain": "Users are bleeding; root-cause later in the postmortem."},
{"prompt": "Postmortem fixed shape — the five sections.", "answer": "Summary, impact, timeline, root causes, action items (owner + due date).",
"explain": "Recite all five; stress owner+date on actions."},
{"prompt": "Run the Five Whys on: 'checkout failed because payment timed out.'", "answer": "Timeout -> pool exhausted -> retry storm 8x load -> no retry budget/circuit breaker -> never in the integration checklist.",
"explain": "End at the systemic gap — that is where the fix lives."},
{"prompt": "Write one good action item for the retry storm.", "answer": "'Add circuit breaker + retry budgets to payment client — owner: payments team, due in 2 weeks.'",
"explain": "Verifiable, owned, dated, systemic — the four tests."},
{"prompt": "A runbook section list — name all six.", "answer": "Symptoms, blast-radius check, diagnosis commands, mitigation commands, escalation criteria, rollback.",
"explain": "Copy-pasteable commands, not prose — runnable at 3 AM."},
]},
]

handsOnLab = {
"id": "il28-m46-lab",
"title": "Lab: burn-rate alerts, on-call routing, and a live incident drill",
"brief": "You will define SLIs/SLOs for a sample service, build fast-burn and slow-burn alerts, design the on-call routing chain, write a runbook, and then run a simulated incident against it — including the postmortem.",
"steps": [
"Pick the sample API from M45 (or any service) and define two SLIs: success ratio and p99 latency under 500ms; set SLOs (99.9% and 99%) over 30 days; compute the error budgets in requests.",
"Write the Prometheus alert rules: fast-burn (burn rate 14, 1h window, severity critical) and slow-burn (burn rate 3, 6h window, severity warning) for the success-ratio SLI.",
"Configure Alertmanager: group by service and severity; route critical to a simulated pager (webhook to a local endpoint or a log file); route warning to a ticket file. Test with amtool if available.",
"Induce a fast burn: run the /fail loop from M45 at high rate; confirm the critical alert fires and the 'page' is logged with the runbook link.",
"Induce a slow burn: trickle failures at ~0.3% for a sustained period (or simulate with a recording); confirm only the warning route triggers.",
"Write the runbook: symptoms, the two dashboard links, diagnosis commands (kubectl get pods, the 5xx-by-pod query, deploy annotation check), mitigation commands (delete bad pod, rollout undo, feature-flag flip), escalation criteria (15 min no improvement -> secondary + major).",
"Run the live drill: have a partner (or a script) break the service without telling you how; execute the runbook start to finish, timing each phase; record where the runbook was unclear.",
"Hold the postmortem: write summary, impact, timeline with timestamps, root causes via Five Whys, and 3 action items with owners and due dates.",
"Update the runbook with everything the drill exposed; set a quarterly review reminder and owner.",
"Compute your drill metrics: time-to-detect, time-to-mitigate, pages received; compare against your SLO policy targets.",
"Write the on-call improvement note: given your drill paging volume, are the thresholds right? What would you retune?",
"Archive the postmortem and runbook in the repo; present the 5-minute incident story as if to a panel."],
"deliverable": "SLI/SLO definitions with budgets, working fast/slow-burn alerts with routing, an executed runbook, and a complete blameless postmortem with owned action items.",
"checkpoint": "Fast-burn pages and slow-burn tickets on induced failures; the drill postmortem has timeline, Five Whys, and dated owned actions; the runbook was updated from drill findings."
}

mockTask = {"id": "il28-m46-mock", "type": "choice",
"q": "Your service has a 99.9% SLO. Errors run at 2% for the last hour. The on-call asks whether to page. What do you decide, and why?",
"choices": ["Do not page — wait for more data", "Page now: burn rate is 20x, the 30-day budget exhausts in about 1.5 days at this pace — this is the fast-burn case", "Page only if it lasts 24 hours", "Restart the service and see"],
"answer": 1,
"explain": "Burn rate = 2%/0.1% = 20. The fast-burn alert exists precisely for this: budget death in days, not weeks. Waiting converts a mitigable incident into an exhausted budget."}

module = {
"id": "IL28-M46", "code": "IL-28",
"title": "Alerting, SLOs & Incident Response",
"summary": "Run reliability as an engineering discipline: SLIs, SLOs, and error budgets with real math, burn-rate alerting, on-call routing, incident command, blameless postmortems, and runbooks you prove in a live drill.",
"objectives": [
"Define SLIs/SLOs and compute error budgets, applying freeze policies to ship-vs-stabilize decisions",
"Configure fast-burn and slow-burn alerts and explain why burn rate beats absolute thresholds",
"Design alert routing chains and on-call escalation with alert-quality rules",
"Run incidents with roles and the mitigate-first protocol, then write blameless postmortems with Five Whys",
"Write, execute, and maintain runbooks proven in live drills"],
"notes": notes, "cards": cards, "quiz": quiz, "weight": 2,
"prerequisiteFor": ["IL28-M49"],
"drills": drills, "handsOnLab": handsOnLab, "mockTask": mockTask,
"crossLinks": ["IL28-M49", "IL28-M45"],
"videos": [{"title": "Azure Monitor alerts overview", "url": "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview", "source": "Microsoft Learn", "durationMin": 30, "order": 1, "watchBefore": "notes", "blurb": "Official Azure alerting concepts: signals, alert rules, and action groups — the native counterpart to this module's Prometheus/Alertmanager routing."}],
"estimatedMinutes": 600,
}

with open("/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build/part_f_m46.json", "w") as f:
    json.dump(module, f, indent=2, ensure_ascii=False)
print("M46 written")
