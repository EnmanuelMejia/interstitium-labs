# IL-09 retrofit content — modules 1-3 (part 1 of 2)
# Each entry: summary (instructor voice), notes (4 template-titled sections).
# All facts preserved from the pre-existing module content.

MODULES = {}

MODULES["il09-comptia-core"] = {
    "summary": "Welcome to Module 1 of IL-09, the Adaptive Certification Command. I'm your instructor, and this is where the certification campaign begins: the CompTIA core stack — A+, Network+, Security+ — sequenced so the knowledge compounds and the stackable credentials (CIOS, then CSIS) fall out of the order automatically. We study by domain weight, not by the order the objectives are printed: A+ Core 1's Hardware (25%) and Hardware/Network Troubleshooting (28%) come first because more than half the exam lives there. Security+ SY0-701 is taught as what it is — a security-operations exam, with its 28% Operations domain at the center. Every drill here pairs official exam objectives with original practice material: PBQ-style labs, subnetting sprints, and the six-step troubleshooting methodology applied until it's reflex.",
    "notes": [
        {
            "title": "Concepts",
            "body": """- **A+ Core 1 (220-1201)** — Hardware, networking, mobile devices, virtualization/cloud concepts, and hardware/network troubleshooting. Domain weights: Hardware 25%, Hardware & Network Troubleshooting 28% — more than half the exam. Study order follows weight, not the objectives list order.
- **A+ Core 2 (220-1202)** — Operating systems, security concepts, software troubleshooting, and operational procedures. Domain weights: Operating Systems 31%, Security 25%. Windows/macOS/Linux OS features lead the study order.
- **PBQ** — Performance-Based Question. These open the CompTIA exams and test applied skill in simulated environments. Do them first while fresh; flag and return if one eats more than ~4 minutes. Never leave one blank.
- **Six-step troubleshooting methodology** — The CompTIA-prescribed sequence: 1) Identify the problem, 2) Establish a theory of probable cause, 3) Test the theory, 4) Establish a plan of action, 5) Implement the solution, 6) Verify functionality and document. Memorize it in order — CompTIA asks which step comes next.
- **Network+ N10-009** — The connective-tissue exam. Domain weights: Networking Concepts 23%, Implementation 20%, Operations 19%, Security 14%, Troubleshooting 24%. Troubleshooting is the single largest domain.
- **Subnetting** — Trainable arithmetic: given 192.168.10.0/26, produce network/broadcast/usable range in under 60 seconds. 2^(32−26) − 2 = 62 usable hosts. On the exam, always isolate by OSI layer — physical first, then data link, then up the stack.
- **DHCP DORA** — Discover, Offer, Request, Acknowledge — the four-step DHCP handshake. Know it as a behavior, not a memorized acronym.
- **DNS recursion vs iteration** — A recursive resolver walks the hierarchy on the client's behalf; iterative queries return referrals and let the client keep walking. Exam questions test which one a given server performs.
- **TCP three-way handshake** — SYN → SYN-ACK → ACK, and know what each flag means — this is the *why* behind protocol questions.
- **Security+ SY0-701** — Reorganized around security operations. Domain weights: General Security Concepts 12%, Threats/Vulnerabilities/Mitigations 22%, Security Architecture 18%, Security Operations 28%, Security Program Management 20%. The largest domain is incident response, digital forensics basics, SIEM/log analysis, and vulnerability management workflow.
- **Log reading** — Timestamps, source/destination, action: most Security Operations questions are log-reading in disguise. Practice reading firewall, IDS, and endpoint logs as narratives.
- **Threat classification** — Classify first, then match the control: malware types, social engineering vectors, attack surfaces.
- **Zero trust** — Verify explicitly, least privilege, assume breach — the design philosophy behind Security+ architecture questions, alongside segmentation and cloud models.
- **Risk vocabulary** — Risk appetite, risk tolerance, risk register: the governance vocabulary of the 20% Program Management domain.
- **CIOS** — CompTIA IT Operations Specialist stackable: earned with A+ + Network+.
- **CSIS** — CompTIA Secure Infrastructure Specialist stackable: earned with A+ + Network+ + Security+. The booking order A+ → Network+ → Security+ earns CIOS then CSIS with no wasted exams.""",
        },
        {
            "title": "Hands-on procedure",
            "body": """This is the domain-weighted study loop — the procedure you'll repeat for every exam in this campaign. It replaces reading-and-hoping with measurable readiness.

1. **Pull the official objectives.** Download the current objectives PDF from comptia.org for the exact exam series you're booking (e.g., 220-1201, N10-009, SY0-701). Third-party summaries older than the current series are study poison.
2. **Rank domains by weight.** Write each domain and its percentage on one page. Your study hours follow weight: A+ Core 1's Hardware + Troubleshooting (53%) gets the bulk; Security+'s Operations (28%) is your largest single investment.
3. **Build the heaviest-domain first.** Attack the heaviest domain before touching anything else. For A+ Core 1 that means hardware install/configure depth; for Security+ it means reading log lines and working incident-response scenarios.
4. **Run the daily drill.** Subnetting sprint (network/broadcast/usable in under 60 seconds), six-step methodology recitation, one PBQ-style lab per sitting. Reflexes are trained, not read.
5. **Do PBQs first on exam day.** Open with the performance-based questions while your working memory is fresh. If one exceeds ~4 minutes, flag it and return — a stalled PBQ can eat the time two multiple-choice questions would earn.
6. **Apply the methodology to every scenario question.** Before choosing an answer, name the step: are you identifying, theorizing, or testing? CompTIA scenario questions reward the disciplined sequence.
7. **Pass the readiness gate before booking.** A domain-weighted practice set at 80%+ across two sittings is the gate. No booking until the gate is green — exam fees are too expensive to spend on hope.

Cross-link: the Network+ preparation here is the exam-prep layer over IL-04's networking path — one networking discipline, two lenses. Study them together.""",
        },
        {
            "title": "Project brief",
            "body": """Your capstone for this module: produce the **12-week core-stack campaign plan** you'd hand a peer who asked "how do I actually do this?"

- Booking order with justification: A+ Core 1 → Core 2 → Network+ N10-009 → Security+ SY0-701, each mapped to the weeks and the hours from your priorities list, with CIOS and CSIS stackables marked at the milestones where they land.
- Domain-weighted study map per exam: the heaviest domains first, the drill schedule (subnetting sprints, PBQ-style labs, log-reading reps) per week.
- Cost ledger: exam voucher prices as published on comptia.org today, total campaign cost, and the two readiness-gate rules (80%+ on domain-weighted practice, twice) that must pass before each booking.
- Exam-day runbook: PBQ-first order, the ~4-minute flag rule, the six-step methodology as your scenario-question checklist.

Deliverable: a one-page plan plus the runbook card you'd carry into the testing center. Original work, built from the official objectives — never from recalled exam content.""",
        },
        {
            "title": "Noah check-in",
            "body": """Noah probes mastery with questions like:
- In one sentence, which two A+ Core 1 domains carry over half the exam weight, and what does that imply for your study order?
- Walk me through the six-step troubleshooting methodology on this scenario: a user's machine has no network connectivity but the link light is on. Which step are you in when you ping the default gateway?
- Why does the PBQ-first exam-day order improve your expected score — what does it cost you if a PBQ runs long?
- Give me three log lines from a firewall (allow/deny with source and destination) and ask me to read them back as a narrative: what is the attacker doing?
- Name the Security+ SY0-701 domain weights from memory, then tell me which single domain your next study hour goes to and why.
- Honesty check: Interstitium Labs confers no certificate, and all practice material here is original — never recalled exam content. Confirm your current exam series on comptia.org before booking; codes and versions change.""",
        },
    ],
}

MODULES["il09-comptia-security"] = {
    "summary": "Welcome to Module 2 of IL-09, the Adaptive Certification Command. I'm your instructor, and this module is the cybersecurity pathway: CySA+ (defend — security operations, vulnerability management, incident response), PenTest+ (attack — engagement management through post-exploitation), and SecurityX (architect — GRC, architecture, engineering at the expert tier). CySA+ thinks in workflows, not definitions: the vulnerability-management lifecycle and the incident-response phases are what get tested. PenTest+ punishes cowboys — scoping and rules of engagement come first, always, and reporting is 17% of the exam and the most under-studied domain in it. SecurityX is scenario-based and pass/fail: enterprise situations with competing constraints, where the right answer balances the constraint set rather than the ideal. Stackables CSAE/CSIE cap the track.",
    "notes": [
        {
            "title": "Concepts",
            "body": """- **CySA+ (CS0-003)** — The defender's exam: can you work a security operations shift? Domain weights: Security Operations 34%, Vulnerability Management 26%, Incident Response 24%, Reporting and Communication 16%. The exam thinks in workflows, not definitions.
- **Vulnerability management lifecycle** — Discover → prioritize → remediate/mitigate → verify → report. Prioritization is the tested skill: a critical CVE on an isolated test box loses to a high CVE on an internet-facing production server.
- **CVSS triage formula** — CVSS severity × asset criticality × threat intel (exploitability). Context beats the raw score every time.
- **SIEM correlation** — Security Information and Event Management: correlation rules, timeline building, distinguishing true positives from noise. Practice reading firewall, IDS, and endpoint logs as narratives.
- **Incident response phases** — Preparation → detection/analysis → containment → eradication → recovery → lessons learned. Know what belongs in each phase and what the *first* action is: contain, don't eradicate, when the scope is unknown.
- **AI in security operations** — Now an explicit topic: know where ML helps (anomaly detection, alert triage) and where it doesn't (final attribution, legal judgment).
- **PenTest+ (PT0-003)** — The methodical offensive cert. Domain weights: Planning/Scoping 13%, Reconnaissance & Enumeration 21%, Attacks & Exploits 35%, Post-Exploitation 14%, Reporting 17%. The largest domain is attacks — but scoping and rules of engagement gate everything.
- **Recon: passive before active** — Passive recon (OSINT, DNS, WHOIS, certificate transparency) precedes active recon (scanning, enumeration). Know which techniques and tools fit which phase and what each reveals.
- **Post-exploitation discipline** — Persistence, lateral movement, pivoting, covering tracks — and the discipline of staying in scope while doing it.
- **Pentest reporting** — 17% of PenTest+ and the most under-studied: findings need severity, evidence, business impact, and remediation. A finding without remediation guidance is an incomplete finding.
- **SecurityX (X0-007, formerly CASP+)** — Expert tier: scenario-based and pass/fail. Domain weights: GRC 20%, Security Architecture 27%, Security Engineering 31%, Security Operations 22%. Questions present enterprise situations with competing constraints — budget, compliance, legacy systems.
- **Trade-off reasoning** — Every control has a cost (money, usability, performance). The right answer balances the constraint set, not the ideal. Architecture answers must cite the governing GRC requirement.
- **CSAP** — CompTIA Security Analytics Professional stackable: Security+ + CySA+.
- **CNVP** — CompTIA Network Vulnerability Assessment Professional stackable: Security+ + PenTest+.
- **CSAE / CSIE** — The expert-tier stackables that cap the security track after SecurityX.""",
        },
        {
            "title": "Hands-on procedure",
            "body": """Two drills, one per posture — defender and attacker. Run the defender drill daily; run the attacker drill as a weekly engagement simulation.

**Defender drill — the SOC shift (CySA+):**
1. **Ingest the alert.** Take one SIEM alert (or write one: source IP, destination, port, action, timestamp). Read it as a narrative, not a data point.
2. **Correlate.** Build the timeline: what happened before and after? One alert is noise; three correlated alerts are a story.
3. **Classify and prioritize.** Apply the triage formula: CVSS severity × asset criticality × threat intel. Score three findings and rank them — defend the ranking out loud.
4. **Respond by phase.** Name the incident-response phase and the first action. Unknown scope → contain first, eradicate later. Write the containment step as an imperative sentence.
5. **Report.** Draft the finding: severity, evidence, business impact, remediation. If any of the four is missing, the finding is incomplete.

**Attacker drill — the engagement walkthrough (PenTest+):**
1. **Scope.** Write the rules of engagement for a fictional target: in-scope hosts, forbidden techniques, time window, reporting contact. Nothing proceeds without this page.
2. **Recon.** List passive sources first (DNS, WHOIS, certificate transparency, OSINT), then active techniques (scanning, enumeration) — and what each reveals.
3. **Attack.** Match the technique to the target surface: network, wireless, application, cloud. For each technique, state the *why* (e.g., why LLMNR poisoning works: legacy name resolution trusting unauthenticated responses).
4. **Post-exploit.** Enumerate persistence, lateral movement, pivoting — and recheck scope at every step.
5. **Report.** Same four-element finding as the defender drill. The attacker and defender write the same report; only the perspective differs.""",
        },
        {
            "title": "Project brief",
            "body": """Your capstone: the **incident-response tabletop** and the **engagement scoping memo**, delivered as one package.

- Tabletop scenario (original): a fictional company, one compromised workstation, an SIEM alert with three correlated events. Write the timeline, the triage ranking of three findings using the CVSS × criticality × threat-intel formula, and the first three actions with their incident-response phases named.
- Scoping memo: rules of engagement for a penetration test of the same fictional company's public web application — in-scope hosts, forbidden techniques, time window, emergency contact, reporting cadence. Then the finding template: severity, evidence, business impact, remediation.
- Stackable map: Security+ → CySA+ → CSAP; Security+ → PenTest+ → CNVP; the path to SecurityX and the expert stackables — with current domain weights cited for each.

Deliverable: the tabletop packet plus the scoping memo. Original scenarios only — nothing here is recalled exam content.""",
        },
        {
            "title": "Noah check-in",
            "body": """Noah probes mastery with questions like:
- Walk me through the vulnerability management lifecycle on this: a critical CVE on an isolated lab VM versus a high CVE on an internet-facing payment server. Which gets remediated first and why?
- During incident response with unknown scope, what is the first action — and what goes wrong if you do it in the wrong order?
- Why does PenTest+ punish cowboys? Name the domain that gates everything and the percentage of the exam it carries.
- Read this alert back as a narrative: firewall deny, internal host 10.4.2.18 → external 203.0.113.9:443 at 02:14, followed by DNS queries to a newly registered domain. What story are you telling?
- A PenTest+ report finding is missing its remediation section. Complete or incomplete — and why does the exam care?
- SecurityX gives you a scenario with a tight budget, a compliance mandate, and legacy systems that can't be replaced. Walk me through how you pick the design: what does "balancing the constraint set" actually mean here?
- Honesty check: preparation only — Interstitium Labs confers no certificate, and every scenario here is original material. Confirm current exam codes on comptia.org before booking.""",
        },
    ],
}

MODULES["il09-comptia-data-cloud"] = {
    "summary": "Welcome to Module 3 of IL-09, the Adaptive Certification Command. I'm your instructor, and this module is the infrastructure and data expansion: Cloud+ (the vendor-neutral multi-cloud operator), Linux+ (the OS that runs the world's servers), Server+ (the hardware and datacenter beneath it), Data+ and DataSys+ (the data layer), and Project+ (leading the work). Cloud+ assumes you can already think in cloud, then tests whether you can run it — and the single most-tested concept is the shared responsibility model. Linux+ rewards systemd fluency and declarative automation thinking; Server+ rewards the failure math of RAID and the two numbers every disaster-recovery question reduces to — RTO and RPO. Data+ walks the full lifecycle from concepts to governance, and this module cross-links to IL-04's Linux path, IL-05's platform work, and IL-07's data spine: one discipline per topic, examined here.",
    "notes": [
        {
            "title": "Concepts",
            "body": """- **Cloud+ (CV0-004)** — The vendor-neutral cloud operator cert. Domain weights: Cloud Architecture 23%, Deployment 19%, Operations 17%, Security 19%, DevOps Fundamentals 10%, Troubleshooting 12%. It tests whether you can *run* cloud, not whether you can recite vendor syntax.
- **Shared responsibility model** — The single most-tested cloud concept: know exactly where the provider's duty ends and yours begins. Under IaaS, the provider secures *of* the cloud (hypervisor, physical); you patch the guest OS.
- **Six R's of migration** — Rehost, Replatform, Repurchase, Refactor/Re-architect, Retain, Retire. Know when each fits: only refactor/re-architect changes the application architecture.
- **Linux+ (XK0-006)** — System Management 23%, Services/User Management 20%, Security 18%, Automation 17%, Troubleshooting 22%. The OS exam for the OS that runs the world's servers.
- **systemd fluency** — Units, targets, journalctl: `journalctl -u <service>` is the first stop when a service fails. Know permissions/ACLs, LVM/storage, package management, shell scripting basics, containers at concept level.
- **Declarative automation** — The modern 17%: Ansible-style declarative thinking, cron/systemd timers, scripted remediation. Automation 17% is where Linux+ separates from a trivia exam.
- **Server+ (SK0-005)** — The hardware and datacenter: Installation 18%, Administration 30%, Security/DR 24%, Troubleshooting 28%. Datacenter realism: power/cooling, physical security, backup types.
- **RAID failure math** — RAID 0/1/5/6/10 trade-offs: know what each survives. RAID 10 (mirror+stripe): fast, survives multi-disk failure in different mirrors, 50% capacity overhead. Know the failure math cold.
- **RTO vs RPO** — Recovery Time Objective (how fast systems return) vs Recovery Point Objective (how much data loss is tolerable). Every DR question reduces to these two numbers. RPO of 4 hours means backups at least every 4 hours.
- **Backup types** — Full, incremental, differential: differential = all changes since last full, so one differential suffices at restore time — faster restore, larger backup.
- **Data+ (DA0-002)** — Data Concepts 20%, Acquisition/Preparation 22%, Analysis 24%, Visualization 20%, Governance 14%. The full data lifecycle.
- **Data quality dimensions** — Accuracy, completeness, consistency, timeliness (validity and uniqueness often listed too).
- **ETL vs ELT** — Extract-Transform-Load vs Extract-Load-Transform: where the transformation happens changes cost, latency, and governance.
- **Chart selection** — Trend over time → line chart; composition → stacked bar; distribution → histogram. A line chart answers the 12-month trend question; a pie chart answers single-point composition.
- **Correlation vs causation** — Correlation is co-movement; causation needs mechanism plus controlled evidence. Never infer cause from a correlation coefficient.
- **DataSys+ (DS0-001)** — Database administration depth and data integration: normalization forms, indexing strategy, backup/recovery for databases, integration patterns.
- **Project+ (PK0-005)** — Formalizes running technical work: project basics, the constraints (scope/time/cost/quality), communication, change control. The vocabulary of leading without authority.""",
        },
        {
            "title": "Hands-on procedure",
            "body": """The operator's drill sequence — one procedure per layer, run until each is reflex.

1. **Shared-responsibility triage.** Take any cloud scenario and draw the line: provider duties vs your duties, for IaaS, PaaS, and SaaS. If you can't place the line, you can't answer Cloud+'s security questions.
2. **Migration-strategy matching.** For each workload in a fictional estate (legacy monolith, commodity web app, end-of-life tool), choose one of the six R's and defend it. Only refactor changes the architecture — name what changes.
3. **systemd rescue drill.** Given a failed service: `systemctl status`, then `journalctl -u <service>` to read the failure, then fix and restart. Time yourself; the first stop is always the journal.
4. **RAID failure-math drill.** State the capacity overhead and survivable failure for RAID 1, 5, 6, 10 from memory. Then: which survives two disk failures in the same array? (RAID 6; RAID 10 only if in different mirrors.)
5. **RTO/RPO worked estimation.** A business says: "We can lose at most 4 hours of data and must be back in 24 hours." Write: RPO = 4h → backup cadence ≤ 4h. RTO = 24h → restore must complete in 24h → differential beats incremental at restore time (one differential suffices). Show the arithmetic.
6. **Chart-selection drill.** Given a message (trend, composition, distribution), pick the chart and defend it. Then name what makes a dashboard honest: labeled axes, zero baselines, no cherry-picked ranges.
7. **Data lifecycle walkthrough.** Take one dataset and walk it: concepts → acquisition/preparation → analysis → visualization → governance. At each stage name the quality dimension and the governance control.

Cross-links: Linux+ is the exam-prep layer over IL-04's Linux path; DevOps fundamentals bridge to IL-05; the data depth lives in IL-07's data spine. Study them together.""",
        },
        {
            "title": "Project brief",
            "body": """Your capstone: the **disaster-recovery one-pager** and the **migration-strategy memo** for a fictional mid-size company.

- DR one-pager: state RTO and RPO for three workload tiers (customer-facing database, internal file shares, dev/test), the backup strategy per tier (full/incremental/differential with cadence justified by the RPO), and the RAID choice per tier with the failure math shown.
- Migration memo: classify six fictional workloads across the six R's with a one-line justification each, and mark the shared-responsibility boundary for the IaaS and PaaS targets.
- Data appendix: one honest dashboard mock (chart choices defended) and the governance controls (classification, retention, stewardship) for the customer-data store.
- Project+ frame: scope/time/cost/quality constraints for the migration program and the change-control procedure.

Deliverable: the one-pager, the memo, and the dashboard mock. Built from the official objectives — the numbers must be yours.""",
        },
        {
            "title": "Noah check-in",
            "body": """Noah probes mastery with questions like:
- Under IaaS, who patches the guest OS — and why is that the single most-tested concept in Cloud+?
- A workload must keep running during a rack failure and survive two disk failures. Walk me through your RAID choice and the capacity overhead you're accepting.
- RPO of 4 hours: what backup cadence does that force, and why does differential restore faster than incremental here?
- `systemctl status` shows a failed service. What is your exact next command, and what are you reading for?
- Full backup Sunday, differentials daily, failure on Wednesday: what do you restore? Defend it.
- Which chart shows a value's trend over 12 months — and what makes the dashboard it's on honest?
- Correlation 0.82 between two metrics. What do you claim, and what do you refuse to claim?
- Honesty check: preparation only — Interstitium Labs confers no certificate and is not affiliated with CompTIA. Confirm current exam codes on comptia.org before booking.""",
        },
    ],
}
