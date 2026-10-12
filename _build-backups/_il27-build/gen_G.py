"""IL-27 Track G: Monitoring & Reliability (IL27-M34..M36)."""

MODULES_G = [
{
"id": "IL27-M34",
"code": "IL-27",
"title": "Monitoring with Zabbix, Prometheus & Grafana",
"summary": "See the infrastructure: metrics vs logs, agent monitoring, alerting that respects sleep, and dashboards people actually read. You need this for -> M35/M36 and on-call sanity.",
"objectives": [
"Compare Zabbix vs Prometheus/Grafana and choose per environment.",
"Deploy monitoring: agents, exporters, and key metrics per system.",
"Write alerts with thresholds, hysteresis, and runbook links.",
"Build Grafana dashboards for the golden signals.",
"Defeat alert fatigue with routing, silencing, and tuning."
],
"notes": [
{"title": "The stack: Zabbix vs Prometheus",
"body": "Zabbix: all-in-one (server, agents, alerting, dashboards) - great for traditional Windows/Linux fleets, auto-discovery, templates per OS/role. Install the agent, apply the template, done. The enterprise workhorse for heterogeneous infra.\n\nPrometheus: metrics pull model - exporters expose /metrics, Prometheus scrapes, PromQL queries, Grafana visualizes, Alertmanager routes. Cloud-native standard; steeper curve, unbeatable flexibility. Windows exporter covers Windows hosts; snmp_exporter covers network gear.\n\nMetrics vs logs vs traces: metrics (numbers over time - CPU, latency), logs (events - M32), traces (request flows). This module is metrics; M32 was logs; together they're observability. Monitor what matters: the USE/RED golden signals (Utilization, Saturation, Errors / Rate, Errors, Duration)."
},
{"title": "What to monitor (per system)",
"body": "Universal host: CPU, memory, disk space/inodes, disk latency, network errors, uptime, pending reboot, service states, certificate expiry (the classic outage). AD: replication status, SYSVOL health, DC response time, time skew. Network: interface errors/discards, BGP/OSPF state, DHCP scope utilization (M14's 80% alert).\n\nApplication: service port responding, synthetic transactions (log in like a user - catches what pings miss), backup job success, queue depths. Cloud: billing alerts (M21), quota usage, instance health checks.\n\nBaselines first: monitor for 2 weeks before alerting on anomalies - 'disk 80% full' alerts on a stable archive server are noise. Every metric needs: why it matters, threshold, who gets paged, and the runbook link."
},
{"title": "Alerting without the 3 AM burnout",
"body": "Alert rules: thresholds with hysteresis (alert at 90%, clear at 80% - no flapping), sustained duration (5 min, not 1 spike), severity tiers (page vs ticket vs info). Routing: PagerDuty/Opsgenie schedules, escalation chains, business-hours vs 24/7 per service tier.\n\nRunbook links in every alert: 'what this means, first 3 checks, who to call'. An alert without a runbook is a panic notification. Silencing: maintenance windows auto-silence; acknowledge stops escalation.\n\nAlert fatigue math: if >5 pages/week per person, tune or die - people start ignoring, then miss the real one. Weekly alert review: which fired, were they actionable, tune or delete. Dashboards: one NOC overview (red/green per service), per-team detail, and executive uptime. A dashboard nobody looks at is wallpaper."
}
],
"cards": [
{"front": "Zabbix vs Prometheus", "back": "Zabbix: all-in-one, templates, traditional fleets. Prometheus: pull model, PromQL, cloud-native."},
{"front": "Metrics vs logs vs traces", "back": "Metrics: numbers over time. Logs: events. Traces: request flows."},
{"front": "Golden signals (USE/RED)", "back": "Utilization, Saturation, Errors / Rate, Errors, Duration."},
{"front": "Hysteresis in alerting", "back": "Alert at 90%, clear at 80% - prevents flapping."},
{"front": "Every alert needs", "back": "Threshold, duration, severity, owner, runbook link."},
{"front": "Certificate expiry monitoring because", "back": "Expired certs are a top-5 'embarrassing outage' cause."},
{"front": "Synthetic transactions catch what pings miss", "back": "Real user flows - login, checkout, query."},
{"front": "Alert fatigue fix", "back": "Weekly review: tune, delete, or route - >5 pages/week/person is broken."}
],
"quiz": [
{"q": "Traditional Windows fleet, need monitoring fast. Choose?", "choices": ["Zabbix (agents + templates, all-in-one)", "Build custom", "No monitoring", "Spreadsheets"], "answer": 0, "index": 0, "explain": "Templates per role = fast coverage."},
{"q": "Alert fires on one CPU spike then clears, repeatedly. Fix?", "choices": ["Add duration (5 min sustained) + hysteresis", "Lower threshold", "Delete the alert", "More RAM"], "answer": 0, "index": 0, "explain": "Sustained + hysteresis kills flapping."},
{"q": "Server 'up' by ping but users can't log in. Missing?", "choices": ["Synthetic transaction (log in like a user)", "More pings", "Bigger server", "New cables"], "answer": 0, "index": 0, "explain": "Port-up != working; test the real flow."},
{"q": "On-call gets 20 pages/week, ignores them. You:", "choices": ["Weekly alert review: tune thresholds, fix root causes, delete noise", "More on-call people", "Louder pagers", "Accept it"], "answer": 0, "index": 0, "explain": "Fatigue is a tuning failure, not a staffing one."},
{"q": "New service launches. Monitoring plan?", "choices": ["Golden signals + runbook-linked alerts + dashboard, baseline 2 weeks", "Ping only", "Later", "User complaints"], "answer": 0, "index": 0, "explain": "Instrument from day one."},
{"q": "DHCP scope hits 95% Monday. Should have:", "choices": ["Alerted at 80% Friday (M14's rule)", "Nothing", "Rebooted", "More scopes Monday"], "answer": 0, "index": 0, "explain": "Capacity alerts precede outages."},
{"q": "Prometheus pull model means:", "choices": ["Prometheus scrapes exporters' /metrics endpoints", "Agents push constantly", "No network needed", "Logs only"], "answer": 0, "index": 0, "explain": "Scrape-based collection."},
{"q": "Dashboard nobody looks at is:", "choices": ["Wallpaper - design for an audience and a decision", "Fine", "Compliance", "Art"], "answer": 0, "index": 0, "explain": "Dashboards serve decisions, not decoration."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M35"],
"drills": [
{"id": "m34-drill-mon", "title": "Monitoring Drill",
"items": [
{"prompt": "Traditional fleet, fast coverage", "answer": "Zabbix + templates", "explain": "All-in-one."},
{"prompt": "Flapping alert fix", "answer": "Duration + hysteresis", "explain": "Sustained thresholds."},
{"prompt": "Ping up, app broken", "answer": "Synthetic transaction", "explain": "Test real flows."},
{"prompt": "Alert needs what?", "answer": "Threshold, owner, runbook link", "explain": "Actionable alerts."},
{"prompt": "20 pages/week", "answer": "Tune: review weekly", "explain": "Fight fatigue."},
{"prompt": "Classic missed metric", "answer": "Certificate expiry", "explain": "Top embarrassing outage."}
]}
],
"handsOnLab": {
"id": "m34-lab",
"title": "Monitor Lab: Zabbix + Grafana, alerted",
"brief": "Monitor your lab with real tooling and real alerts.",
"steps": [
"Deploy Zabbix (container per M20) + agents on lab VMs; apply OS templates.",
"Add Prometheus + Grafana; scrape the Windows exporter; build a golden-signals dashboard.",
"Configure: disk 80% warning, service-down page, cert-expiry check (self-signed test).",
"Trigger each alert deliberately; verify routing + runbook link content.",
"Create a maintenance window silence; verify suppression.",
"Run the weekly review ritual on your lab alerts; tune one."
],
"deliverable": "Working monitoring + dashboards + triggered alerts + review notes.",
"checkpoint": "You can see your infrastructure and sleep through the night."
},
"mockTask": {"id": "m34-mock", "type": "choice",
"q": "Interview: 'How do you avoid alert fatigue?'",
"choices": ["Sustained thresholds with hysteresis, severity tiers, runbook-linked alerts, weekly review tuning, <5 pages/week/person target", "More staff", "Ignore alerts", "Page on everything"],
"answer": 0, "explain": "Alerting as a designed system, not a firehose."},
"crossLinks": [],
"videos": "VIDEOS_M34",
"estimatedMinutes": 260,
"fastTrackEligible": False
},
{
"id": "IL27-M35",
"code": "IL-27",
"title": "High Availability & Clustering Concepts",
"summary": "Design for failure: redundancy at every layer, failover vs load balancing, and the math of nines. You need this for -> M31/M36 and resilient design.",
"objectives": [
"Explain HA vs fault tolerance vs disaster recovery.",
"Design redundancy: network, power, compute, storage, app.",
"Calculate availability ('nines') and set realistic SLAs.",
"Describe clustering, load balancing, and quorum.",
"Identify single points of failure in a design."
],
"notes": [
{"title": "The vocabulary: HA, FT, DR",
"body": "High Availability: survive component failure with minimal downtime (failover clusters, redundant everything). Fault Tolerance: survive with ZERO downtime (shadow/duplicate execution - expensive, rare). Disaster Recovery: survive site loss (M31 - backups, replication, second site). Different problems, different price tags.\n\nNines math: 99% = 3.65 days downtime/year; 99.9% = 8.76 hours; 99.99% = 52.6 minutes; 99.999% = 5.26 minutes. Each nine costs roughly 10x. 'We need five nines' for the file server = an expensive conversation about whether they mean it.\n\nSLA vs SLO vs SLI: SLA (contract, with penalties), SLO (internal target), SLI (the measured metric). Error budget: the allowed unreliability (100% - SLO) - spend it on changes, freeze when exhausted. This is SRE vocabulary every infra admin should speak."
},
{"title": "Redundancy at every layer",
"body": "No single points of failure: dual power (PSUs, feeds, UPS), NIC teaming, stacked switches or MLAG, RAID (not backup!), clustered compute (M18), replicated storage, load-balanced apps, redundant internet (dual ISP + BGP or SD-WAN).\n\nFailover vs load balancing: failover (active/passive - one serves, other waits; clusters), load balancing (active/active - traffic spread; needs shared-nothing or shared state design). Health checks decide: the LB must detect dead backends fast and correctly.\n\nQuorum (M18's lesson, generalized): any clustered decision needs a tiebreaker - witness disk/file/cloud. Split-brain (both sides think they're primary) corrupts data; fencing (STONITH - shoot the other node in the head) prevents it. Respect the quorum math."
},
{"title": "Finding SPOFs",
"body": "SPOF hunt method: draw the dependency chain for each critical service (user -> LB -> app -> DB -> storage -> power -> network), then ask 'what single failure breaks this?' at each link. The answers are your project list.\n\nCommon hidden SPOFs: the one DNS server everyone points to, the single UPS, the admin's laptop with the only config backup, the cloud region with no failover plan, the SSL cert only one person can renew, the 'temporary' firewall rule holding up prod.\n\nDesign review ritual: for every new service, the HA checklist - redundant at each layer? failover tested? (untested failover is decoration - M29's lesson again), monitoring covers the standby path? (dead standby discovered during failover = the worst day), documented runbook?"
}
],
"cards": [
{"front": "HA vs FT vs DR", "back": "HA: minimal downtime. FT: zero downtime. DR: survive site loss."},
{"front": "99.9% vs 99.99% downtime/year", "back": "99.9% = 8.76h. 99.99% = 52.6min. Each nine ~10x cost."},
{"front": "SLA vs SLO vs SLI", "back": "SLA: contract. SLO: internal target. SLI: measured metric."},
{"front": "Error budget", "back": "Allowed unreliability (100%-SLO); spend on changes, freeze when gone."},
{"front": "Failover vs load balancing", "back": "Failover: active/passive. LB: active/active with health checks."},
{"front": "Split-brain prevention", "back": "Quorum + fencing (STONITH)."},
{"front": "SPOF hunt method", "back": "Draw dependency chain; ask 'what single failure breaks this?' per link."},
{"front": "Untested failover is", "back": "Decoration - test the standby path."}
],
"quiz": [
{"q": "'We need five nines for the print server.' You:", "choices": ["Cost conversation: each nine ~10x; match nines to business impact", "Agree immediately", "Refuse", "Buy servers"], "answer": 0, "index": 0, "explain": "Availability has a price; spend it where it matters."},
{"q": "Active/passive SQL cluster. That's:", "choices": ["Failover (HA)", "Load balancing", "Fault tolerance", "DR"], "answer": 0, "index": 0, "explain": "One serves, other waits = failover."},
{"q": "Two-node cluster splits; both go primary and corrupt data. Missing?", "choices": ["Quorum + fencing", "More nodes", "Faster network", "Bigger disks"], "answer": 0, "index": 0, "explain": "Tiebreaker + shoot-the-other-node."},
{"q": "Hidden SPOF examples:", "choices": ["Single DNS, one UPS, one person with cert access, untested standby", "Too many servers", "Cloud", "Monitoring"], "answer": 0, "index": 0, "explain": "The unglamorous single points."},
{"q": "Load balancer health checks must be:", "choices": ["Fast and correct - dead backends removed quickly", "Slow", "Optional", "Manual"], "answer": 0, "index": 0, "explain": "Bad health checks = traffic to corpses."},
{"q": "Error budget exhausted. You:", "choices": ["Freeze changes until reliability recovers", "Ship faster", "Ignore it", "Lower the SLO"], "answer": 0, "index": 0, "explain": "The budget disciplines change velocity."},
{"q": "RAID is:", "choices": ["Uptime (survives disk failure), not backup", "Backup", "Archival", "Encryption"], "answer": 0, "index": 0, "explain": "RAID != backup - say it with conviction."},
{"q": "Standby path monitoring because:", "choices": ["Dead standby discovered during failover = worst day", "It's fun", "Compliance", "Graphs"], "answer": 0, "index": 0, "explain": "Monitor the failover target too."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M36"],
"drills": [
{"id": "m35-drill-ha", "title": "High Availability Drill",
"items": [
{"prompt": "99.99% downtime/year", "answer": "52.6 minutes", "explain": "Nines math."},
{"prompt": "Active/passive = ?", "answer": "Failover (HA)", "explain": "One waits."},
{"prompt": "Split-brain fix", "answer": "Quorum + fencing", "explain": "Tiebreaker."},
{"prompt": "SPOF hunt", "answer": "Dependency chain per link", "explain": "Single-failure question."},
{"prompt": "RAID is not", "answer": "Backup", "explain": "Uptime only."},
{"prompt": "Error budget gone", "answer": "Freeze changes", "explain": "Reliability first."}
]}
],
"handsOnLab": {
"id": "m35-lab",
"title": "Resilience Audit: SPOF hunt + nines",
"brief": "Audit your lab (or a fictional org) for single points of failure.",
"steps": [
"Draw the full dependency chain for the lab's 'critical service'.",
"Identify every SPOF; rank by likelihood x impact.",
"Calculate current nines vs target; price the gap roughly.",
"Fix the cheapest 3 SPOFs in the lab (second DC, teamed NIC, backup power strip = UPS concept).",
"Test one failover (stop a service, verify the standby takes over).",
"Write the HA checklist for new services."
],
"deliverable": "SPOF register + nines calc + fixes + failover test + checklist.",
"checkpoint": "You see fragility others miss - and fix it."
},
"mockTask": {"id": "m35-mock", "type": "choice",
"q": "Interview: 'How do you design for high availability?'",
"choices": ["No SPOFs at any layer, failover/load balancing per workload, quorum for clusters, tested standby paths, nines matched to business value, monitoring everywhere", "Two of everything", "Cloud fixes it", "Hope"],
"answer": 0, "explain": "Layered, tested, cost-aware resilience."},
"crossLinks": [],
"videos": [],
"estimatedMinutes": 240,
"fastTrackEligible": False
},
{
"id": "IL27-M36",
"code": "IL-27",
"title": "Capacity Planning & Performance Tuning",
"summary": "Stay ahead of growth: trending, headroom, bottleneck analysis, and tuning Windows/Linux systems. You need this for -> M34/M35 and budget conversations.",
"objectives": [
"Build capacity models from trending data (MX07's math applied).",
"Identify bottlenecks: CPU, memory, disk, network - in order.",
"Tune Windows Server performance (and know Linux basics).",
"Plan hardware refresh and cloud sizing with headroom.",
"Present capacity as a business case with dates."
],
"notes": [
{"title": "Trending and headroom",
"body": "Capacity planning = trending + headroom + lead time. Trending: collect utilization over months (M34's metrics are the feed); fit the growth (linear usually, step-changes at known events). Headroom: never plan to 100% - 70% sustained is the comfort line, 85% is the 'order now' line. Lead time: hardware takes weeks, cloud takes minutes - but budget takes quarters.\n\nThe math (MX07): at 5%/month growth from 60%, you hit 85% in ~7 months - order at month 4. Present as dates, not percentages: 'disk hits the order line in March' funds itself.\n\nWhat to trend: disk (the #1 surprise), memory, CPU, network, license counts, backup windows, DHCP scopes (M14 again), certificate expiries. The untrended resource is the one that pages you."
},
{"title": "Bottleneck analysis",
"body": "Method: under load, check in order - CPU (sustained >80%? queue length?), memory (paging/page faults? available <10%?), disk (queue length >2? latency >20ms?), network (errors? saturation?). The bottleneck is the resource at 100% while others wait - fix THAT, not the others.\n\nWindows tools: Performance Monitor (the deep tool - counters, Data Collector Sets for baselining), Resource Monitor (quick view), Task Manager (triage). Linux: top/htop, iostat, vmstat, sar. PAL (Performance Analysis of Logs) for report-style analysis.\n\nCommon fixes: disk latency -> move to faster tier / add spindles / fix the query; memory pressure -> add RAM / find the leak; CPU -> scale out or optimize the hot process. Measure before AND after - tuning without measurement is superstition."
},
{"title": "Tuning and the business case",
"body": "Windows tuning levers: power plan (High Performance for servers - Balanced throttles under load), pagefile sizing (system-managed usually wins), NUMA alignment (M18), antivirus exclusions for data directories (documented!), network (RSS, chimney - usually leave alone on modern), and the biggest lever: the APPLICATION (index the database, cache, fix the code).\n\nHardware refresh: 3-5 year cycles; TCO math (power, warranty, performance/watt) beats sticker price. Cloud sizing: right-size continuously (M21's Advisor) - the cloud lets you fix mistakes monthly.\n\nThe business case: 'At current growth, X exhausts in [date]. Options: [buy/expand/optimize] costing [$], risk of doing nothing: [outage/slowness on date]. Recommendation: [one].' Dates, dollars, risks, recommendation - that format gets funded."
}
],
"cards": [
{"front": "Capacity formula", "back": "Trending + headroom (70/85%) + lead time = order dates."},
{"front": "Bottleneck check order", "back": "CPU -> memory -> disk -> network; fix the saturated one."},
{"front": "Disk latency red line", "back": ">20ms sustained / queue >2 = investigate."},
{"front": "#1 capacity surprise", "back": "Disk space - trend it always."},
{"front": "Server power plan", "back": "High Performance - Balanced throttles under load."},
{"front": "Tune without measurement is", "back": "Superstition - baseline before and after."},
{"front": "Biggest tuning lever", "back": "The application itself (indexes, caching, code)."},
{"front": "Business case format", "back": "Dates, dollars, risks, recommendation."}
],
"quiz": [
{"q": "Disk at 60%, growing 5%/month. Order line 85%. When?", "choices": ["~5 months: (85-60)/5 - start procurement now", "Never", "Next year", "Yesterday"], "answer": 0, "index": 0, "explain": "Trending gives dates; dates drive orders."},
{"q": "App slow: CPU 30%, memory fine, disk queue 8, latency 45ms. Bottleneck?", "choices": ["Disk - queue and latency confirm", "CPU", "Network", "Memory"], "answer": 0, "index": 0, "explain": "Fix the saturated resource."},
{"q": "Server sluggish under load, power plan Balanced. Try?", "choices": ["High Performance plan", "More cores", "Reboot daily", "New server"], "answer": 0, "index": 0, "explain": "Balanced throttles CPUs under load."},
{"q": "SQL data directory scanned by AV in real time. Issue?", "choices": ["Latency - exclude data dirs (documented)", "Security hole", "None", "More AV"], "answer": 0, "index": 0, "explain": "AV on database files kills performance."},
{"q": "Presenting capacity needs to leadership. Format?", "choices": ["Exhaustion date, options with costs, risk of inaction, recommendation", "A graph", "Panic", "More metrics"], "answer": 0, "index": 0, "explain": "Dates, dollars, risks, recommendation."},
{"q": "Cloud VM consistently at 15% CPU. Action?", "choices": ["Right-size down (Advisor) - pay for what you use", "Keep it", "Bigger VM", "Two VMs"], "answer": 0, "index": 0, "explain": "Monthly right-sizing is the cloud advantage."},
{"q": "Baseline before tuning because:", "choices": ["You can't prove improvement without before/after", "It's fun", "Compliance", "Vendors ask"], "answer": 0, "index": 0, "explain": "Measurement separates tuning from guessing."},
{"q": "Lead time matters because:", "choices": ["Hardware takes weeks, budget takes quarters - plan ahead", "It's trivia", "Cloud is instant always", "Vendors are slow"], "answer": 0, "index": 0, "explain": "Order dates account for reality."}
],
"weight": 2,
"prerequisiteFor": [],
"drills": [
{"id": "m36-drill-cap", "title": "Capacity Drill",
"items": [
{"prompt": "Order-line rule", "answer": "85% = order now; 70% comfort", "explain": "Headroom thresholds."},
{"prompt": "Bottleneck order", "answer": "CPU, memory, disk, network", "explain": "Check saturated first."},
{"prompt": "Disk red lines", "answer": "Queue >2, latency >20ms", "explain": "Investigate."},
{"prompt": "Server power plan", "answer": "High Performance", "explain": "No throttling."},
{"prompt": "Proving a tuning win", "answer": "Before/after measurement", "explain": "Data, not vibes."},
{"prompt": "Funding format", "answer": "Dates, dollars, risks, recommendation", "explain": "Gets funded."}
]}
],
"handsOnLab": {
"id": "m36-lab",
"title": "Tune Lab: baseline, bottleneck, prove it",
"brief": "Find and fix a real bottleneck in your lab with measurement.",
"steps": [
"Set up a Data Collector Set baselining a lab VM for 24h (or 1h accelerated).",
"Generate load (disk: large copies; CPU: stress tool); capture the bottleneck signature.",
"Identify the bottleneck using the ordered method; document evidence.",
"Apply ONE fix (power plan, AV exclusion, disk move); re-measure.",
"Build the capacity model: trend lab disk growth, project the order date.",
"Write the business case one-pager for a fictional expansion."
],
"deliverable": "Baseline + bottleneck proof + fix measurement + capacity model + business case.",
"checkpoint": "You tune with data and fund with dates."
},
"mockTask": {"id": "m36-mock", "type": "choice",
"q": "Interview: 'Our file server is slow. How do you approach it?'",
"choices": ["Baseline with PerfMon, check CPU/memory/disk/network in order, identify the saturated resource, fix it, re-measure to prove the win", "Add RAM", "New server", "Reboot"],
"answer": 0, "index": 0, "explain": "Ordered, measured diagnosis - not parts-dartboard."},
"crossLinks": [],
"videos": [],
"estimatedMinutes": 240,
"fastTrackEligible": False
}
]
