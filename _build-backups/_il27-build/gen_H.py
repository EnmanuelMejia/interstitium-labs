"""IL-27 Track H: Capstone & Career (IL27-M37..M40)."""

MODULES_H = [
{
"id": "IL27-M37",
"code": "IL-27",
"title": "Homelab Capstone Project",
"summary": "Prove it all: design, build, document, and present a complete homelab infrastructure. This is the portfolio centerpiece. You need this for -> M38 and interviews.",
"objectives": [
"Design a complete homelab: network, identity, virtualization, monitoring, backup.",
"Build it on real or virtual hardware within a budget.",
"Document it to professional standards (diagrams, configs, runbooks).",
"Present it as a 10-minute technical walkthrough.",
"Maintain it: patching, monitoring, and improvement log."
],
"notes": [
{"title": "The capstone architecture",
"body": "The build: a virtualized host (Hyper-V or Proxmox) running - DC with AD/DNS/DHCP, a member server (file/print), a Linux VM (monitoring/logging), a client VM, segmented virtual networks (users/servers/mgmt), pfSense/OPNsense as the firewall/router, Zabbix or Prometheus watching it all, and a backup job proving 3-2-1 thinking.\n\nTiers for budgets: Tier 0 (free - nested virtualization on your PC), Tier 1 (~$300 mini PC + switch), Tier 2 (used enterprise server, the classic homelab). All tiers complete the same learning; document which tier you built and why.\n\nDesign doc first: network diagram (addressing, VLANs), server roles, naming convention, service catalog, and the 'why' per choice. Building without the design doc is how homelabs become snowflakes."
},
{"title": "Build log and standards",
"body": "Build in the course's order: network -> virtualization -> identity (AD) -> services (DNS/DHCP/file) -> hardening (baselines, LAPS, BitLocker-concept) -> monitoring -> backup. Log every step: what you did, what broke, how you fixed it. The break/fix log is the most interview-valuable artifact - it proves troubleshooting.\n\nStandards: naming convention everywhere, documented admin credentials (in a password manager - never plaintext), configs backed up, change log. Treat it like production: patch monthly (M24's rings on a tiny fleet), review alerts weekly (M34), test a restore quarterly (M31).\n\nDeliberate breakage: schedule 'chaos days' - kill the DC (test the second), fill the disk (test alerts), restore a file (test backups). A homelab you only admire teaches half; one you break teaches all."
},
{"title": "The presentation",
"body": "10-minute walkthrough structure: (1) the design (diagram, 2 min), (2) live demo (log in, show AD/GPO/monitoring, 4 min), (3) a break/fix story (what broke, how you diagnosed it, 2 min), (4) what you'd do with $5,000 more (2 min - shows judgment). Record it; this video goes on your portfolio.\n\nWhat interviewers hear: design thinking, hands-on skill, troubleshooting method, and ambition bounded by budget. 'Here's my lab' beats 'I'm a fast learner' every time.\n\nMaintenance: the lab is never 'done' - keep an improvement backlog (next: 802.1X, second site VPN, K8s). A living lab signals a living engineer."
}
],
"cards": [
{"front": "Capstone build order", "back": "Network -> virtualization -> identity -> services -> hardening -> monitoring -> backup."},
{"front": "Most interview-valuable artifact", "back": "The break/fix log - proves troubleshooting method."},
{"front": "Design doc before building because", "back": "Prevents snowflake homelabs; forces intentional choices."},
{"front": "Chaos days", "back": "Deliberate breakage: kill DC, fill disk, restore - test everything."},
{"front": "10-min walkthrough structure", "back": "Design (2) -> demo (4) -> break/fix story (2) -> $5k more (2)."},
{"front": "Homelab tiers", "back": "T0 free nested, T1 mini PC, T2 used enterprise - same learning."},
{"front": "Treat it like production", "back": "Monthly patching, weekly alert review, quarterly restore test."},
{"front": "'Here's my lab' beats", "back": "'I'm a fast learner' - evidence over claims."}
],
"quiz": [
{"q": "Building the lab: first artifact?", "choices": ["Design doc: diagram, addressing, roles, naming, rationale", "Buy hardware", "Install Windows", "A name"], "answer": 0, "index": 0, "explain": "Design before build."},
{"q": "Most valuable interview artifact from the lab?", "choices": ["Break/fix log showing diagnosis method", "Uptime stats", "Hardware specs", "Photos"], "answer": 0, "index": 0, "explain": "Troubleshooting stories are STAR gold."},
{"q": "Proving backups work in the lab:", "choices": ["Quarterly restore test to isolated network", "Backup emails", "Full disks", "Hope"], "answer": 0, "index": 0, "explain": "Restore proof, not backup promises."},
{"q": "Chaos day: kill the primary DC. Expect?", "choices": ["Second DC serves auth; you practice seizure/transfer", "Total outage", "Nothing", "Data loss"], "answer": 0, "index": 0, "explain": "That's why you built two."},
{"q": "'What would you do with $5,000 more?' tests:", "choices": ["Judgment: priorities, trade-offs, business value", "Shopping skill", "Greed", "Nothing"], "answer": 0, "index": 0, "explain": "Prioritization under constraints."},
{"q": "Admin creds for the lab stored:", "choices": ["Password manager - never plaintext", "Sticky note", "Same password everywhere", "In the design doc"], "answer": 0, "index": 0, "explain": "Practice production hygiene always."},
{"q": "Lab maintenance cadence:", "choices": ["Monthly patch, weekly alerts, quarterly restore", "Never", "Yearly", "When broken"], "answer": 0, "index": 0, "explain": "Production habits at lab scale."},
{"q": "The lab is 'done' when?", "choices": ["Never - keep an improvement backlog", "Day one", "At 10 VMs", "When perfect"], "answer": 0, "index": 0, "explain": "Living lab, living engineer."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M38"],
"drills": [
{"id": "m37-drill-cap", "title": "Capstone Drill",
"items": [
{"prompt": "Build order", "answer": "Network, virt, identity, services, harden, monitor, backup", "explain": "Course order."},
{"prompt": "First artifact", "answer": "Design doc", "explain": "Diagram + rationale."},
{"prompt": "Best interview artifact", "answer": "Break/fix log", "explain": "Troubleshooting proof."},
{"prompt": "Prove backups", "answer": "Quarterly restore test", "explain": "Recoverability."},
{"prompt": "Cred storage", "answer": "Password manager", "explain": "Never plaintext."},
{"prompt": "10-min structure", "answer": "Design, demo, story, $5k", "explain": "2-4-2-2."}
]}
],
"handsOnLab": {
"id": "m37-lab",
"title": "THE CAPSTONE: build it all",
"brief": "Design, build, document, break, and present your complete homelab.",
"steps": [
"Write the design doc: diagram, addressing/VLANs, roles, naming, budget tier.",
"Build per the order: network, hypervisor, DC (AD/DNS/DHCP), member, Linux monitor.",
"Harden: baseline GPO, LAPS, firewall rules; verify with a checklist.",
"Monitor: Zabbix/Prometheus on the Linux VM watching everything; alerting to email.",
"Backup: backup jobs + one verified restore; document RPO/RTO.",
"Chaos day: kill DC-1, fill a disk, restore a file - log it all.",
"Record the 10-minute walkthrough; publish to your portfolio."
],
"deliverable": "Design doc + working lab + break/fix log + restore proof + recorded walkthrough.",
"checkpoint": "You have a portfolio centerpiece and the stories to defend it."
},
"mockTask": {"id": "m37-mock", "type": "choice",
"q": "Interview: 'Tell me about your homelab.'",
"choices": ["Design walkthrough: choices and why, live demo, a break/fix story with diagnosis method, and the improvement backlog", "I have a PC", "It's big", "I watch videos"],
"answer": 0, "explain": "Structure turns a hobby into evidence."},
"crossLinks": [],
"videos": [],
"estimatedMinutes": 600,
"fastTrackEligible": False
},
{
"id": "IL27-M38",
"code": "IL-27",
"title": "Infrastructure Documentation Portfolio",
"summary": "Your work is only as good as your docs: network diagrams, runbooks, and a portfolio that gets interviews. You need this for -> M39 and the job hunt.",
"objectives": [
"Produce professional network and AD diagrams.",
"Write runbooks others can actually follow.",
"Build a documentation portfolio site/repo.",
"Explain docs as a career accelerant.",
"Maintain docs: versioning and review cycles."
],
"notes": [
{"title": "Diagrams that communicate",
"body": "Diagram types: physical (racks, cables, ports), logical (VLANs, subnets, flows), AD (forest/domain/OU), and service maps (what depends on what). Tools: draw.io/diagrams.net (free, fine), NetBox (source of truth for larger), or even clean whiteboard photos for early drafts.\n\nStandards: consistent icons, labeled everything (IPs, VLAN IDs, roles), legend, date + version on every diagram. A diagram without a date is a rumor. Update on change - the 'docs are outdated' tax is paid in outage minutes.\n\nThe portfolio set: your capstone network diagram, AD design, GPO inventory, patch cadence doc, DR one-pager, and 2-3 runbooks. Redact sensitively (no real company data, ever - lab/fictional only)."
},
{"title": "Runbooks that work",
"body": "Runbook anatomy: purpose, prerequisites, steps (numbered, copy-pasteable commands), expected outputs, rollback, escalation. Test: hand it to someone (or your future self in 6 months) - if they can't follow it, rewrite.\n\nThe essential runbook library: new user onboarding, laptop deployment, patch cycle, backup restore, incident first response, offboarding. Each one turns tribal knowledge into team capability - and proves you think beyond yourself.\n\nDocs as code: version in git, review on change, templates for consistency. 'The runbook is in the repo, versioned, tested last quarter' is senior language."
},
{"title": "The portfolio",
"body": "Format: a clean site or GitHub repo - 'Infrastructure Portfolio': about, capstone walkthrough (M37's video), diagrams, runbooks (sanitized), project write-ups (problem -> action -> result), and a skills matrix mapping to this course. Link it on your resume and LinkedIn.\n\nWrite-ups use PAR: Problem (what was broken/missing), Action (what you did, technically specific), Result (measured - uptime, time saved, tickets cut). Numbers beat adjectives.\n\nMaintenance: quarterly review dates on every doc; stale docs get archived, not left to mislead. A portfolio with 2026 dates in 2028 says 'I stopped learning' - keep it alive."
}
],
"cards": [
{"front": "Diagram types", "back": "Physical, logical, AD, service maps - each answers different questions."},
{"front": "Every diagram needs", "back": "Labels, legend, date + version."},
{"front": "Runbook anatomy", "back": "Purpose, prereqs, steps, expected outputs, rollback, escalation."},
{"front": "Runbook test", "back": "Hand to someone else - if they can't follow it, rewrite."},
{"front": "PAR write-ups", "back": "Problem -> Action -> Result (measured)."},
{"front": "Never in a portfolio", "back": "Real company data - lab/fictional only, redacted."},
{"front": "Docs as code means", "back": "Versioned in git, reviewed on change, templated."},
{"front": "Stale docs get", "back": "Archived with dates - never left to mislead."}
],
"quiz": [
{"q": "Diagram has no date. It is:", "choices": ["A rumor - date and version everything", "Fine", "Art", "Complete"], "answer": 0, "index": 0, "explain": "Undated diagrams mislead during outages."},
{"q": "Runbook test method?", "choices": ["Someone else follows it cold", "Read it yourself", "Trust it", "Skip testing"], "answer": 0, "index": 0, "explain": "The user test for docs."},
{"q": "Portfolio project write-up format?", "choices": ["PAR: Problem, Action, Result (measured)", "A diary", "Specs list", "Screenshots only"], "answer": 0, "index": 0, "explain": "Measured outcomes persuade."},
{"q": "Including your employer's real network diagram:", "choices": ["Never - lab/fictional only, redacted", "Fine", "If it's impressive", "With permission maybe - but default no"], "answer": 0, "index": 0, "explain": "Protect company data; default to no."},
{"q": "Docs outdated after a change. Cost?", "choices": ["Paid in outage minutes - update on change", "None", "Aesthetic", "Storage"], "answer": 0, "index": 0, "explain": "Stale docs actively harm incidents."},
{"q": "Essential runbook library includes:", "choices": ["Onboarding, deployment, patching, restore, IR first response, offboarding", "Lunch orders", "One runbook", "None"], "answer": 0, "index": 0, "explain": "The tribal-knowledge capture set."},
{"q": "Portfolio shows dates from 2 years ago only. Signal?", "choices": ["Stopped learning - keep it alive quarterly", "Experience", "Stability", "Nothing"], "answer": 0, "index": 0, "explain": "Living docs signal a living engineer."},
{"q": "Best diagram tool to start?", "choices": ["draw.io/diagrams.net - free and sufficient", "Expensive CAD", "MS Paint", "None"], "answer": 0, "index": 0, "explain": "Clarity beats tooling."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M39"],
"drills": [
{"id": "m38-drill-docs", "title": "Documentation Drill",
"items": [
{"prompt": "Diagram needs what?", "answer": "Labels, legend, date, version", "explain": "Communicate + trust."},
{"prompt": "Runbook test", "answer": "Someone else follows it", "explain": "Cold-follow test."},
{"prompt": "Write-up format", "answer": "PAR with measured results", "explain": "Persuasive structure."},
{"prompt": "Real company data?", "answer": "Never in portfolio", "explain": "Redact always."},
{"prompt": "Stale docs", "answer": "Archive with dates", "explain": "Don't mislead."},
{"prompt": "Core runbooks", "answer": "Onboard, deploy, patch, restore, IR, offboard", "explain": "The essential six."}
]}
],
"handsOnLab": {
"id": "m38-lab",
"title": "Portfolio Build: ship your docs site",
"brief": "Build and publish your infrastructure documentation portfolio.",
"steps": [
"Diagram your capstone: physical, logical, AD - dated and versioned.",
"Write 3 runbooks (onboarding, patch cycle, restore) - cold-test one with a peer.",
"Write 2 PAR project write-ups from your labs.",
"Build the portfolio site/repo: about, walkthrough video, diagrams, runbooks, write-ups, skills matrix.",
"Redaction pass: verify zero real-company data.",
"Set quarterly review reminders for every doc."
],
"deliverable": "Published portfolio + redaction verification + review schedule.",
"checkpoint": "Your work is visible, credible, and hireable."
},
"mockTask": {"id": "m38-mock", "type": "choice",
"q": "Interview: 'How do you document your work?'",
"choices": ["Diagrams (dated/versioned), tested runbooks, versioned in git, PAR write-ups, portfolio - docs as a team capability", "I remember it", "Tickets only", "Someone else documents"],
"answer": 0, "explain": "Documentation as engineering discipline."},
"crossLinks": [],
"videos": [],
"estimatedMinutes": 300,
"fastTrackEligible": False
},
{
"id": "IL27-M39",
"code": "IL-27",
"title": "On-the-Job Excellence & Communication",
"summary": "The skills that get you promoted: ticketing mastery, stakeholder communication, incident comms, and on-call professionalism. Fast-track: this is interview behavior. You need this for -> M40 and day one.",
"objectives": [
"Run a ticket queue like a professional (M04 applied).",
"Communicate status: up/down/across with the right detail.",
"Handle incidents: comms cadence, bridges, and stakeholder updates.",
"Manage up: 1:1s, visibility, and asking for help well.",
"Navigate on-call without burning out."
],
"notes": [
{"title": "Tickets and queue craft",
"body": "M04's foundation, applied: triage by impact/urgency, timebox investigation, update before the user asks, close with root cause + prevention. Queue metrics that matter: first response time, resolution time, reopen rate, CSAT. Your ticket history is your reputation in writing.\n\nEscalation done right: what you tried (with evidence), what you need, urgency framing. 'I've tried X, Y, Z (logs attached); I need network to check the firewall; users down since 9:15' gets help fast. Escalation isn't failure - silent struggling is.\n\nKnowledge base: every solved novel ticket becomes a KB article. The KB is your leverage - and your replacement-proofing paradox: documenting makes you promotable, not expendable."
},
{"title": "Communication: up, down, across",
"body": "Up (management): outcomes and risks, not tech - 'email will be down 20 min for patching; risk of delay is X; no action needed.' Down (users): empathy + timeline + workaround - 'I know this blocks your morning; workaround is Y; I'll update by 10.' Across (peers): technical detail + asks - 'DC replication failing with event 1864; can you check the firewall?' \n\nIncident comms: cadence (every 15-30 min even if 'still working'), one channel (the bridge), one voice (the comms lead), factual not speculative. 'We don't know yet' beats a wrong ETA.\n\nWriting: subject lines that summarize, 3-bullet updates, no jargon to non-technical. Your emails are your brand - most of your 'communication skill' is judged in writing."
},
{"title": "On-call and growth",
"body": "On-call professionalism: acknowledge fast, assess (is this really paging-worthy?), work the runbook, escalate early, write the follow-up. Post-incident: blameless notes within 48h. Handoffs: written, with 'watch for X' items.\n\nBurnout guards: real off-call time (no 'just checking'), sleep protection (tune alerts - M34), exercise and boundaries. A fried admin makes mistakes that page everyone.\n\nGrowth: 1:1s with your manager (bring: wins, blockers, growth asks), visibility (share learnings, demo your lab), asking for help (early, specific, with what you tried), and feedback (request it quarterly). Promotions go to visible, reliable, growing people - be all three."
}
],
"cards": [
{"front": "Escalation done right", "back": "Tried (evidence) + need + urgency - not silent struggling."},
{"front": "Communicate up vs down vs across", "back": "Up: outcomes/risks. Down: empathy/timeline/workaround. Across: technical detail."},
{"front": "Incident comms cadence", "back": "Every 15-30 min, one channel, one voice, factual."},
{"front": "'We don't know yet' beats", "back": "A wrong ETA - never speculate on timelines."},
{"front": "KB article per novel ticket because", "back": "Leverage + promotability (documented = promotable)."},
{"front": "On-call follow-up timing", "back": "Blameless notes within 48h."},
{"front": "1:1 agenda", "back": "Wins, blockers, growth asks."},
{"front": "Burnout guard #1", "back": "Real off-call time + tuned alerts (sleep is safety)."}
],
"quiz": [
{"q": "Users down, cause unknown, ETA unknown. Update says?", "choices": ["'We're investigating; workaround is Y; next update in 20 min' - factual, no invented ETA", "'Fixed soon'", "'It's DNS'", "Nothing until fixed"], "answer": 0, "index": 0, "explain": "Cadence + honesty + workaround."},
{"q": "Stuck 2 hours, afraid to escalate. Reality?", "choices": ["Escalate with evidence of tries - silence is the failure", "Keep struggling", "Reboot randomly", "Blame the vendor"], "answer": 0, "index": 0, "explain": "Escalation is professionalism."},
{"q": "Manager asks for a status. You give:", "choices": ["Outcomes, risks, needed decisions - not config dumps", "Every log line", "'It's fine'", "A 50-slide deck"], "answer": 0, "index": 0, "explain": "Right detail for the audience."},
{"q": "Solved a weird issue at 2 AM. Next?", "choices": ["KB article + blameless notes within 48h", "Sleep forever", "Tell no one", "Delete the logs"], "answer": 0, "index": 0, "explain": "Capture the learning while fresh."},
{"q": "Paged for something that's not urgent. Fix?", "choices": ["Tune the alert threshold/severity (M34) - pages are for urgent", "Complain", "Ignore pages", "Quit"], "answer": 0, "index": 0, "explain": "Alert hygiene protects the team."},
{"q": "Peer asks for help mid-incident. You:", "choices": ["Technical detail + specific ask", "A shrug", "Take over silently", "A ticket"], "answer": 0, "index": 0, "explain": "Across-communication is precise."},
{"q": "1:1 with your manager. Bring?", "choices": ["Wins, blockers, growth asks", "Complaints only", "Nothing", "Gossip"], "answer": 0, "index": 0, "explain": "Drive your own growth visibly."},
{"q": "Documentation makes you:", "choices": ["Promotable (team capability), not expendable", "Replaceable", "Slow", "A target"], "answer": 0, "index": 0, "explain": "The paradox resolved."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M40"],
"drills": [
{"id": "m39-drill-comms", "title": "Professional Excellence Drill",
"items": [
{"prompt": "Escalation format", "answer": "Tried + need + urgency", "explain": "Evidence-based ask."},
{"prompt": "Incident update cadence", "answer": "15-30 min, one channel", "explain": "Predictable comms."},
{"prompt": "Unknown ETA: say?", "answer": "'We don't know yet' + next update time", "explain": "Honest cadence."},
{"prompt": "After the 2 AM fix", "answer": "KB + notes in 48h", "explain": "Capture learning."},
{"prompt": "Manager update style", "answer": "Outcomes, risks, decisions", "explain": "Audience-appropriate."},
{"prompt": "1:1 brings", "answer": "Wins, blockers, growth", "explain": "Visible growth."}
]}
],
"handsOnLab": {
"id": "m39-lab",
"title": "Comms Reps: write it like a pro",
"brief": "Produce the communication artifacts of a professional admin.",
"steps": [
"Write 3 ticket updates (user-facing) for a fictional outage: initial, progress, resolution.",
"Write the manager summary for the same outage (outcomes/risks).",
"Write the peer escalation request (technical + ask).",
"Draft your 1:1 agenda template; fill it for your current state.",
"Write a KB article from one of your lab break/fix stories.",
"Role-play: record a 2-minute incident bridge update."
],
"deliverable": "Ticket updates + manager summary + escalation + 1:1 template + KB + bridge recording.",
"checkpoint": "You communicate like the senior in the room."
},
"mockTask": {"id": "m39-mock", "type": "choice",
"q": "Interview: 'How do you handle pressure and communication during outages?'",
"choices": ["Structured comms: 15-min cadence, one channel, factual updates, workaround-first for users, outcomes for managers, blameless follow-up in 48h", "Panic quietly", "No updates until fixed", "Blame"],
"answer": 0, "explain": "Comms under pressure is a practiced skill."},
"crossLinks": [],
"videos": [],
"estimatedMinutes": 200,
"fastTrackEligible": True
},
{
"id": "IL27-M40",
"code": "IL-27",
"title": "Certification Roadmap",
"summary": "What's next, honestly: which certs matter for infrastructure careers, what they cost, and how this course maps to them. No certs are conferred here - they're earned from vendors. You need this for -> your career.",
"objectives": [
"Map this course to real certifications (A+, Network+, Security+, AZ-800/801, etc.).",
"Build a personal 12-month certification plan with costs.",
"Explain honest cert framing: earned from vendors, never conferred by courses.",
"Use practice exams and labs effectively (no brain dumps).",
"Plan continuing education: renewals and staying current."
],
"notes": [
{"title": "The honest certification landscape",
"body": "This course confers NO certifications - they are earned from the vendors (CompTIA, Microsoft, Cisco) by passing their exams. Any course claiming to 'certify' you is selling fiction. What this course does: teach the underlying skills so vendor exams test what you already know.\n\nThe roadmap, in order: CompTIA A+ (foundations, M01-M04), Network+ (M05-M10), Security+ (M26-M33 concepts), Microsoft AZ-800/801 (Windows Server Hybrid Administrator - M11-M17, M21), then specialty: SC-300 (identity), AZ-104 (Azure admin), or CCNA (networking depth).\n\nCosts (approximate, verify current): A+ ~$500 (two exams), Network+ ~$400, Security+ ~$400, Microsoft ~$165/exam. Total to Security+: ~$1,300 + study time. Say the numbers out loud - budgeting is part of planning."
},
{"title": "Your 12-month plan",
"body": "Template: months 1-3 (A+ core 1+2, using M01-M04 + Messer), 4-6 (Network+, M05-M10), 7-9 (Security+, M26-M33), 10-12 (AZ-800 or SC-300, M11-M17/M21). Each: study (this course + vendor docs), lab (homelab reps), practice exams (measure readiness), exam (schedule when practice scores hold).\n\nPractice exam discipline: 85%+ consistently before booking; review every wrong answer (why, not just what); never use brain dumps (stolen exam content - gets certs revoked and teaches nothing). Labs beat memorization: if you built it, you remember it.\n\nEmployer value: many infra roles list 'A+ or equivalent experience' - this course + homelab IS the equivalent experience, and the cert is the proof. Certs open doors; skills keep you in the room."
},
{"title": "Staying current",
"body": "Renewals: CompTIA CE (3 years - CertMaster CE or retake), Microsoft (annual free renewal assessments - do them). Calendar every renewal on day one.\n\nStaying current: vendor blogs/docs (Microsoft Learn updates constantly), one conference or community (local SpiceCorps/Meetup), homelab experiments quarterly, and teaching (write-ups, mentoring - teaching cements learning).\n\nThe meta-skill: learn how to learn vendor ecosystems. Today's AZ-800 is tomorrow's renamed role cert - the skill is navigating Microsoft Learn, reading docs, labbing fast, and passing exams. This course taught the substrate; the certs are the receipts."
}
],
"cards": [
{"front": "This course confers", "back": "No certifications - they're earned from vendors by passing exams."},
{"front": "Roadmap order", "back": "A+ -> Network+ -> Security+ -> AZ-800/801 or SC-300/AZ-104/CCNA."},
{"front": "Rough cost to Security+", "back": "~$1,300 in exam fees (verify current prices)."},
{"front": "Practice exam readiness rule", "back": "85%+ consistently before booking."},
{"front": "Brain dumps: why not", "back": "Stolen content - certs revoked, teaches nothing."},
{"front": "Microsoft renewal", "back": "Annual free renewal assessments."},
{"front": "CompTIA renewal", "back": "3-year CE cycle."},
{"front": "Certs vs skills", "back": "Certs open doors; skills keep you in the room."}
],
"quiz": [
{"q": "Does completing this course certify you?", "choices": ["No - certifications are earned from vendors via their exams", "Yes", "Partially", "With a fee"], "answer": 0, "index": 0, "explain": "Honest framing, always."},
{"q": "First cert for an aspiring infra admin?", "choices": ["CompTIA A+ (foundations)", "CCIE", "CISSP", "PMP"], "answer": 0, "index": 0, "explain": "Foundations first."},
{"q": "Windows Server Hybrid Admin maps to:", "choices": ["AZ-800/801", "A+", "CCNA", "CISSP"], "answer": 0, "index": 0, "explain": "Microsoft's hybrid server cert."},
{"q": "Practice scores at 70%. Book the exam?", "choices": ["No - 85%+ consistently first", "Yes", "Maybe", "Book two"], "answer": 0, "index": 0, "explain": "Readiness discipline saves retake fees."},
{"q": "Brain dumps are:", "choices": ["Stolen exam content - revoked certs, zero learning", "Study aids", "Fine", "Recommended"], "answer": 0, "index": 0, "explain": "Never."},
{"q": "Best exam prep method?", "choices": ["Labs + docs + practice exams (built it = remember it)", "Cramming", "Dumps", "Luck"], "answer": 0, "index": 0, "explain": "Hands-on cements knowledge."},
{"q": "Microsoft cert renewal cadence?", "choices": ["Annual free assessment", "Never", "Retake full exam", "$500"], "answer": 0, "index": 0, "explain": "Free yearly renewal."},
{"q": "Staying current includes:", "choices": ["Vendor docs, community, quarterly lab experiments, teaching", "Nothing after cert", "One book", "Hope"], "answer": 0, "index": 0, "explain": "Continuous learning is the job."}
],
"weight": 1,
"prerequisiteFor": [],
"drills": [
{"id": "m40-drill-certs", "title": "Certification Drill",
"items": [
{"prompt": "Course confers certs?", "answer": "No - earned from vendors", "explain": "Honest framing."},
{"prompt": "Roadmap order", "answer": "A+, Net+, Sec+, AZ-800/801", "explain": "Foundations up."},
{"prompt": "Booking threshold", "answer": "85%+ practice consistently", "explain": "Readiness rule."},
{"prompt": "Brain dumps?", "answer": "Never - stolen content", "explain": "Revoked certs."},
{"prompt": "MS renewal", "answer": "Annual free assessment", "explain": "Calendar it."},
{"prompt": "Best prep", "answer": "Labs + docs + practice", "explain": "Built = remembered."}
]}
],
"handsOnLab": {
"id": "m40-lab",
"title": "Plan Lab: your 12-month certification campaign",
"brief": "Build your personal, budgeted, scheduled certification plan.",
"steps": [
"Self-assess against each cert's objectives using this course's modules.",
"Draft the 12-month timeline with exam dates and study blocks.",
"Budget: exam fees + materials; verify current prices on vendor sites.",
"Schedule practice-exam checkpoints per cert (85% rule).",
"Calendar all renewal dates (even future ones).",
"Write your 'why' statement: what each cert unlocks for you."
],
"deliverable": "12-month plan + budget + checkpoints + renewal calendar + why statement.",
"checkpoint": "You have a funded, scheduled path - not a wish."
},
"mockTask": {"id": "m40-mock", "type": "choice",
"q": "Interview: 'What certifications do you have planned?'",
"choices": ["12-month roadmap: A+ to Security+ to AZ-800, budgeted and scheduled, backed by this course's labs and homelab - certs as proof of skills I already practice", "None planned", "All of them", "Whatever's cheapest"],
"answer": 0, "explain": "Planned, funded, skill-backed - credible ambition."},
"crossLinks": [],
"videos": [],
"estimatedMinutes": 180,
"fastTrackEligible": False
}
]
