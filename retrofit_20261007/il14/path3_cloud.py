# -*- coding: utf-8 -*-
"""IL-14 retrofit content — Path 3: Cloud Engineering Interview Prep (6 modules)."""
# pylint: disable=line-too-long

P3_SUMMARY = {
"cloud-interview-prep--cloud-concepts": (
"Welcome to the Cloud Engineering Interview Prep path of the Interstitium Labs SRE, DevOps, Cloud & Security Interview Prep course. "
"I'm your instructor for this path, and we begin with the conceptual floor every cloud interview stands on: what the cloud is, who secures what, and when each compute primitive wins. Regions, AZs, edge; the shared-responsibility model; VMs, containers, serverless; CapEx vs OpEx — told honestly. "
"This is Module 1: Core Cloud Concepts. You'll leave leading with vendor-neutral concepts, because concepts transfer and click-paths don't."
),
"cloud-interview-prep--cloud-networking": (
"Welcome back. I'm your instructor for the Cloud Interview Prep path, and this is Module 2: Cloud Networking — the module that decides cloud interviews. "
"Packets, routes, and firewalls, taught until you can debug a dead connection aloud: VPCs, subnets, route tables, security groups and NACLs, load balancers, DNS, NAT, VPN, peering. "
"By the end, a 'can't reach the instance' question becomes a layer-by-layer bisection you narrate with confidence."
),
"cloud-interview-prep--cloud-data": (
"Welcome back. I'm your instructor for the Cloud Interview Prep path, and this is Module 3: Data and Storage Services. "
"Data services as design choices: which store for which workload — object storage, managed SQL, NoSQL by access pattern — plus caching with an invalidation plan, lifecycle tiering, and the backup story that proves production thinking. "
"You'll answer RPO/RTO questions with numbers and defend a storage choice by workload, not by habit."
),
"cloud-interview-prep--cloud-security-controls": (
"Welcome back. I'm your instructor for the Cloud Interview Prep path, and this is Module 4: Cloud Security Controls. "
"Security is the interview's trust test: IAM done as least privilege, encryption at rest and in transit, secrets fetched at runtime, audit trails that make forensics possible, and guardrails that make the safe path the easy path. "
"You'll leave able to explain why an open bucket is the customer's fault and what you'd have done to prevent it."
),
"cloud-interview-prep--cloud-arch-build": (
"Welcome back. I'm your instructor for the Cloud Interview Prep path, and this is Module 5: Guided Cloud Architecture. "
"One complete, costed, failure-reviewed architecture — the artifact you walk an interviewer through when they say 'design something.' Requirements and constraints, a three-tier reference design, IaC for the whole stack, an honest cost estimate, a failure-mode review, and the ADR that records why. "
"This is the portfolio piece of the cloud path. Build it like one."
),
"cloud-interview-prep--cloud-mock": (
"Welcome back. I'm your instructor for the Cloud Interview Prep path, and this is Module 6: Cloud Mock Circuit. "
"Simulated cloud loops with the Well-Architected rubric: the architecture-design round, the cloud deep-dive round, the 'Design X on AWS' patterns, and the cost questions candidates forget to prepare. "
"You'll practice narrating cost and tradeoffs — the Cadillac and the Honda, and when each wins — until it's automatic."
),
}

P3_NOTES = {
"cloud-interview-prep--cloud-concepts": [
{"title": "Concepts", "body": (
"- **Region** — a geographic area of cloud data centers: the unit of data residency and disaster recovery.\n"
"- **Availability Zone (AZ)** — isolated data center(s) within a region with independent power and networking: run across ≥2 AZs; one AZ is a single point of failure.\n"
"- **Edge** — points of presence near users for caching and termination: proximity, not resilience.\n"
"- **Shared responsibility** — the provider secures OF the cloud (physical, hypervisor, fabric); you secure what's IN it (data, IAM, OS, app config).\n"
"- **VM** — virtualized hardware with a guest OS: strongest isolation, heaviest footprint.\n"
"- **Container** — shared host kernel, packaged userland: lighter and faster than VMs, weaker isolation.\n"
"- **Serverless** — functions the provider scales to zero: no servers to manage, pay per invocation, mind the cold starts.\n"
"- **CapEx** — buy servers upfront: fixed, depreciating. **OpEx** — pay per use: variable, agile, and in need of FinOps governance.\n"
"- **Vendor-neutral knowledge** — concepts that transfer (VPCs, IAM, queues, object storage) vs vendor-specific click-paths that expire with the UI."
)},
{"title": "Worked estimation", "body": (
"Work the classic 'should we move to the cloud' estimation — the honest version, with assumptions stated.\n"
"1. **State the workload.** A sample internal tool: 4 VMs on-prem, running 24/7, refreshed every 4 years at $8,000 per server (assumed figures for the exercise).\n"
"2. **Compute the CapEx baseline.** 4 × $8,000 = $32,000 over 4 years, plus power, cooling, and your time — write the 'plus' items even without numbers.\n"
"3. **Sketch the OpEx alternative.** Equivalent cloud VMs at an assumed $0.10/hr each: 4 × $0.10 × 730 hrs ≈ $292/month ≈ $3,500/year.\n"
"4. **Add the honest costs.** Data transfer out, managed-service premiums, and the FinOps tax: untracked variable spend surprises you.\n"
"5. **Name the non-price factors.** Elasticity for spiky workloads, managed backups, and speed of provisioning — agility is what OpEx actually buys.\n"
"6. **Deliver the verdict format.** 'On pure 24/7 steady-state cost it's close; the cloud wins on elasticity and managed undifferentiated work — and loses if we lift-and-shift without rightsizing.'"
)},
{"title": "Project brief", "body": (
"Your deliverable: a one-page 'cloud concepts' briefing you'd give a skeptical CTO.\n"
"- **The primitives**: regions/AZs/edge, shared responsibility, and the VM/container/serverless decision tree — each with its 'when it wins'.\n"
"- **The worked estimation** from this module, with assumptions labeled as assumptions.\n"
"- **The honest value props**: what the cloud genuinely buys (elasticity, managed heavy lifting, speed) and what it doesn't (automatic savings, automatic security).\n"
"- **The trap answers**: 'the cloud is secure' (no — your bucket policy is your job), 'it's always cheaper' (no — FinOps or surprise).\n"
"- **Present it in 10 minutes**, then take the hardest pushback question and answer it in writing.\n"
"Reference shelf (module sources): **AWS Documentation** (https://docs.aws.amazon.com/) — compute, networking, data, and security primitives. **Google Cloud Documentation** (https://cloud.google.com/docs) — GCP-side primitives for vendor-neutral depth."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and the worked estimation uses assumed prices to teach method. "
"Real cloud prices change constantly and vary by region, commitment, and workload shape — never quote the exercise figures as facts about any real bill. "
"The transferable skill is the structure: CapEx vs OpEx with assumptions stated, shared responsibility drawn as a line, and compute primitives chosen by workload — vendor-neutral first, because concepts transfer and click-paths don't."
)},
],
"cloud-interview-prep--cloud-networking": [
{"title": "Concepts", "body": (
"- **VPC** — your isolated virtual network: the boundary everything else lives inside.\n"
"- **Subnet** — a slice of the VPC: public subnets route to an internet gateway; private subnets have no direct inbound (NAT for outbound).\n"
"- **Route table** — decides where packets go: the VPC's traffic cop.\n"
"- **Security group** — stateful, instance-level firewall: return traffic is automatically allowed.\n"
"- **NACL** — stateless, subnet-level firewall: both directions need explicit rules.\n"
"- **Load balancer** — spreads traffic, but also health-checks, terminates TLS, and routes L7 by path/host: the first reliability device in the path.\n"
"- **NAT** — lets private resources reach the internet outbound without being reachable inbound.\n"
"- **VPN** — encrypted tunnel extending your network: site-to-site or client.\n"
"- **VPC peering** — private VPC-to-VPC connectivity over the provider backbone: no internet exposure.\n"
"- **Flow logs** — allowed/rejected IP traffic metadata: the packet-level audit trail for security-group and routing diagnosis."
)},
{"title": "Hands-on procedure", "body": (
"Debug a dead connection layer by layer — the drill that decides cloud interviews. Scenario: 'I can't SSH to the instance.'\n"
"1. **DNS.** Does the name resolve? (`dig`/`nslookup`.) 'Could not resolve host' = DNS failure, not a server problem.\n"
"2. **Routing.** Is there a route to the subnet? Check the route table: public subnet needs the internet gateway route; the instance needs a public IP.\n"
"3. **Security groups.** Stateful: is inbound SSH allowed from your IP? Remember return traffic is automatic — misdiagnosing this wastes an hour.\n"
"4. **NACLs.** Stateless: is inbound SSH allowed AND outbound ephemeral-port return allowed? The classic NACL trap.\n"
"5. **The instance.** Is it running? Is the SSH daemon up? Check system logs — the network can be perfect and the service down.\n"
"6. **Narrate the bisection.** Say each layer's test and what each outcome implicates: 'I bisect the stack instead of guessing.'"
)},
{"title": "Project brief", "body": (
"Your deliverable: a network design + troubleshooting guide for a sample three-tier VPC.\n"
"- **The design**: VPC with public/private subnets across 2 AZs, route tables, NAT, security groups (stateful, least-privilege), NACLs (stateless, explicit both ways), ALB in public, app and data in private.\n"
"- **The rules table**: every security-group and NACL rule with its justification — 'each answers a how-do-these-networks-talk question.'\n"
"- **The dead-connection runbook**: the six-layer bisection from the Hands-on procedure as a checklist.\n"
"- **The DNS section**: public vs private hosted zones, TTL strategy for an upcoming migration, health-checked failover.\n"
"- **Present the design in 10 minutes**, then debug a seeded fault (wrong NACL) live.\n"
"Reference shelf (module sources): **AWS Documentation** (https://docs.aws.amazon.com/) — networking primitives. **Google Cloud Documentation** (https://cloud.google.com/docs) — GCP networking for vendor-neutral depth."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and paper networks don't drop packets. "
"Real VPC debugging involves flow logs, overlapping CIDRs from acquisitions, and security-group sprawl that no diagram captures; the module teaches the bisection method and the stateful/stateless distinction that untangles them. "
"Service names and defaults change; verify current behavior against the linked documentation as of its retrieval date."
)},
],
"cloud-interview-prep--cloud-data": [
{"title": "Concepts", "body": (
"- **Object storage** — flat, limitless blob storage (the S3 pattern): presigned URLs let clients upload directly so bytes never touch your app servers.\n"
"- **Managed SQL** — backups, patching, failover, and read replicas handled by the provider: you keep schema design and query tuning.\n"
"- **Key-value NoSQL** — single-digit-ms lookups by key: choose by access pattern, then take the managed version.\n"
"- **Document NoSQL** — flexible JSON documents: for evolving schemas and document-shaped access.\n"
"- **Caching** — what to cache (read-heavy, slow-changing), where (edge, app, DB), and the invalidation strategy: stale data is caching's permanent tax.\n"
"- **Lifecycle tiering** — hot/warm/cold-archive matched to access frequency: every byte has a cost curve.\n"
"- **RPO** — how much data loss is tolerable: bounds backup frequency. **RTO** — how fast recovery must complete: bounds downtime."
)},
{"title": "Worked estimation", "body": (
"Work the backup-and-recovery estimation — RPO/RTO as numbers, not vibes.\n"
"1. **State the business answers.** 'We can lose at most 1 hour of orders (RPO = 1h); checkout must be back within 4 hours (RTO = 4h).' Get these from the business, not engineering.\n"
"2. **Derive the backup frequency.** RPO of 1 hour → backups (or continuous replication) at least hourly. Daily backups would violate the RPO by 23 hours — say so.\n"
"3. **Derive the recovery architecture.** RTO of 4 hours → tested restore procedure that completes in under 4 hours: rehearsed restores, not documentation.\n"
"4. **Price the tiers.** Hot data (yesterday's orders) on fast storage; 7-year compliance retention on archive tier — 'rarely-accessed retention data shouldn't pay hot-storage prices.'\n"
"5. **Name the failure test.** 'When did we last restore from backup?' — an untested backup is a hope, not a plan.\n"
"6. **Close with the line.** 'RPO bounds data loss; RTO bounds downtime — and both are business decisions with engineering price tags.'"
)},
{"title": "Project brief", "body": (
"Your deliverable: a data-architecture one-pager for a sample e-commerce service.\n"
"- **Store choices**: object storage for uploads (presigned-URL flow), managed SQL for orders (with read replicas), key-value for sessions, cache layer with invalidation strategy — each chosen by access pattern.\n"
"- **The RPO/RTO table** from the Worked estimation, with the backup schedule and restore test that satisfies it.\n"
"- **Lifecycle policy**: hot → warm → archive transitions with the cost reasoning per tier.\n"
"- **The failure story**: cache outage, primary DB failure, region loss — what degrades, what the customer sees.\n"
"- **Defend it in 10 minutes**, ending with: 'I choose the store by the query pattern, then take the managed version of that choice.'\n"
"Reference shelf (module sources): **AWS Documentation** (https://docs.aws.amazon.com/) — data service primitives. **Azure Architecture Center** (https://learn.microsoft.com/en-us/azure/architecture/) — reference architectures and design guidance."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and the worked numbers are illustrative. "
"Real RPO/RTO values come from the business's risk tolerance, and real storage costs shift with tiers, regions, and access patterns — never quote exercise figures as facts. "
"What transfers is the method: choose by access pattern, tier by cost curve, back up to the RPO, restore-test to the RTO, and always have the invalidation story before the cache."
)},
],
"cloud-interview-prep--cloud-security-controls": [
{"title": "Concepts", "body": (
"- **IAM user / role / policy** — users are people, roles are assumable identities for workloads and people, policies are the permission documents: roles over users, always.\n"
"- **Least privilege** — every permission scoped to specific actions on specific resources, with a reason and an expiry conversation: no wildcards in production.\n"
"- **SCP (Service Control Policy)** — preventive guardrail: makes bad actions impossible account-wide.\n"
"- **Encryption at rest / in transit** — data encrypted on disk and on the wire: the baseline, not the differentiator.\n"
"- **Secret manager** — rotation, audit, fine-grained access for credentials: secrets are fetched at runtime, never baked into images or repos.\n"
"- **CloudTrail-style audit log** — who did what via the API, with identity and time: the forensic record.\n"
"- **Detective controls** — Config rules and audit trails that catch what happened: the complement to preventive guardrails."
)},
{"title": "Hands-on procedure", "body": (
"Audit a sample cloud account's security posture, on paper, in 30 minutes.\n"
"1. **List the identities.** Users, roles, and what each can do. Flag: any user with console access and no MFA; any `Action: *` on `Resource: *`.\n"
"2. **Apply least privilege.** Rewrite the flagged policy scoped to specific actions on specific resources. Write the one-sentence justification per permission.\n"
"3. **Check the secrets.** Hunt for credentials in repos, env files, and images — every find becomes 'move to the secret manager, fetched at runtime.'\n"
"4. **Verify encryption.** At rest and in transit for the data stores; note where the keys live and who can use them.\n"
"5. **Add the guardrails.** One preventive (SCP blocking the worst action) and one detective (Config rule + audit-trail review cadence).\n"
"6. **Write the findings like a consultant.** Risk-ranked, business impact, concrete fix with effort — criticals first, never a 200-item undifferentiated list."
)},
{"title": "Project brief", "body": (
"Your deliverable: a cloud security review document for a sample account — the trust-test artifact.\n"
"- **Identity review**: the IAM map, least-privilege rewrites, and the access-review cadence.\n"
"- **Secrets and encryption**: the secrets inventory, the runtime-fetch design, encryption verification.\n"
"- **Guardrails**: preventive SCPs + detective Config rules, each with what it stops and what it catches.\n"
"- **The headline findings**: top 5, risk-ranked, each with business impact and a concrete fix.\n"
"- **Present it in 10 minutes** as if to a CTO, ending with: 'guardrails make the safe path the easy path.'\n"
"Reference shelf (module sources): **AWS Documentation** (https://docs.aws.amazon.com/) — IAM and security primitives. **CISA Resources & Tools** (https://www.cisa.gov/resources-tools) — hardening and best-practice guidance."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and a paper audit is not a security assessment. "
"Real accounts carry years of accumulated access, exceptions, and organizational politics that no exercise captures; the module teaches the review structure — identity, secrets, encryption, guardrails — and the consultant's reporting discipline. "
"Never present a classroom audit as professional security-assessment experience. Service specifics change; verify against the linked documentation as of its retrieval date."
)},
],
"cloud-interview-prep--cloud-arch-build": [
{"title": "Concepts", "body": (
"- **Three-tier architecture** — presentation (ALB + CDN) → application (auto-scaled compute across AZs) → data (managed DB with replicas, caches): tiers as failure and scaling boundaries.\n"
"- **Reference architecture** — the standard shape you start from and justify deviations against.\n"
"- **Failure-mode review** — 'what breaks, how the system degrades, is that degradation acceptable': what separates architecture from diagramming.\n"
"- **Cost drivers** — the line items that move the bill: transfer is the classic surprise; provisioned capacity the steady burn.\n"
"- **ADR** — Architecture Decision Record: decision, context, alternatives, consequences — how architecture survives team turnover.\n"
"- **IaC for the whole stack** — reproducible, reviewable infrastructure: the architecture exists as code, not as a diagram."
)},
{"title": "Worked estimation", "body": (
"Cost the three-tier architecture honestly — assumptions stated, surprises named.\n"
"1. **List the components.** ALB, app instances across 2 AZs, managed DB with replica, cache, object storage + CDN, data transfer.\n"
"2. **Estimate each line with an assumption.** 'App: 4 instances at assumed $0.10/hr ≈ $292/mo' — every line carries its assumption.\n"
"3. **Hunt the transfer.** Cross-AZ chatter and egress: architectures that chat across AZs/regions pay per GB, compounding silently — call it out as the surprise line item.\n"
"4. **Add the reliability tax.** Multi-AZ and replicas cost more than single-AZ; write what the extra nine costs per month.\n"
"5. **Offer the Honda.** The cheaper alternative (single AZ, smaller instances, no replica) with its tradeoff stated: 'here's the Cadillac and the Honda, and when each wins.'\n"
"6. **Close with the lever.** 'Here's what drives the bill, and here's the lever that moves it' — the sentence architects are hired to say."
)},
{"title": "Project brief", "body": (
"Your deliverable: the complete architecture package — the portfolio piece.\n"
"- **Requirements and constraints** in one page: users, scale, latency, compliance, budget.\n"
"- **The reference architecture**: three-tier across 2 AZs, every component justified, every arrow labeled.\n"
"- **IaC for the whole stack**: the module layout that builds it reproducibly.\n"
"- **The cost estimate** from the Worked estimation, assumptions labeled, Cadillac and Honda both shown.\n"
"- **The failure-mode review**: per component — what breaks, how it degrades, whether that's acceptable.\n"
"- **One ADR**: the highest-stakes decision, with alternatives and consequences.\n"
"- **Walk an interviewer through it in 15 minutes**, from requirements to the cost slide.\n"
"Reference shelf (module sources): **AWS Well-Architected Framework** (https://docs.aws.amazon.com/well-architected/) — the six pillars; the architecture interview's rubric. **Terraform Documentation** (https://developer.hashicorp.com/terraform/docs) — IaC references."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and the costed architecture is a design exercise. "
"Real prices move constantly and the worked figures are illustrative — never quote them as facts about any real deployment. Real architectures also carry organizational constraints (existing contracts, team skills, compliance regimes) that the exercise simplifies away. "
"Present it as a portfolio design with stated assumptions; the graded skill is the method — requirements first, costed honestly, failure-reviewed."
)},
],
"cloud-interview-prep--cloud-mock": [
{"title": "Concepts", "body": (
"- **Architecture-design round** — requirements → reference design → costed, with tradeoffs narrated: 'I can draw it and I can explain the boxes.'\n"
"- **Cloud deep-dive round** — one service's internals: how the LB, the queue, the DB actually work — mechanism, not marketing.\n"
"- **'Design X on AWS' patterns** — the recurring shapes: three-tier web, data pipeline, event-driven serverless — each with its cost story.\n"
"- **Well-Architected rubric** — the six pillars as the interview's hidden grading sheet: reliability, security, cost, performance, operations, sustainability.\n"
"- **Cost narration** — naming cost drivers honestly and offering the cheaper alternative with its tradeoff: the architect-level signal.\n"
"- **48-hour checklist** — logistics, rest, no new topics: the loop-day performance plan from the SRE path, reused here."
)},
{"title": "Hands-on procedure", "body": (
"Run the cloud mock circuit with a partner, timed.\n"
"1. **Architecture round (45 min).** 'Design a photo-sharing service on AWS': requirements, estimation, three-tier design, failure modes, costed — Cadillac and Honda.\n"
"2. **Deep-dive round (30 min).** Partner picks one component (the LB, the queue, the DB): explain its internals — mechanism, not marketing — until they say stop.\n"
"3. **Cost cross-examination (15 min).** Partner attacks the bill: 'cut 30%'. Defend or concede each line with the tradeoff stated.\n"
"4. **Behavioral round (20 min).** Two STAR stories: a production decision you owned, a time you were wrong about a design.\n"
"5. **Score against the pillars.** Rate each Well-Architected pillar in your answers; the lowest pillar is next week's study.\n"
"6. **Write the debrief.** The two weakest moments, their categories, and the redrill plan — then the 48-hour checklist."
)},
{"title": "Project brief", "body": (
"Your deliverable: a cloud interview dossier.\n"
"- **Three architecture one-pagers**: three-tier web, event-driven serverless, data pipeline — each costed with assumptions.\n"
"- **Deep-dive sheets**: the internals of a load balancer, a managed queue, and a managed database — mechanism-level, one page each.\n"
"- **The cost-cutting drill**: your architecture with 30% removed, and what each cut costs in reliability.\n"
"- **Score sheets** against the Well-Architected pillars, with the weakest pillar's study plan.\n"
"- **Reflection**: which 'Design X' pattern still isn't automatic, and the reps that will make it so.\n"
"Reference shelf (module sources): **AWS Well-Architected Framework** (https://docs.aws.amazon.com/well-architected/). **Azure Architecture Center** (https://learn.microsoft.com/en-us/azure/architecture/)."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and mock scores don't predict real loops. "
"Partners are kinder than panels; treat scores as triage data. Cost figures in your one-pagers are illustrative estimates — label them as such and never present them as quotes. "
"The honest win of the circuit: automatic architecture shapes, cost narration as a reflex, and a debrief habit that aims every study hour at the weakest pillar."
)},
],
}

P3_NEW_CARDS = {
"cloud-interview-prep--cloud-concepts": {
"front": "How do you answer 'why not just buy servers?'",
"back": "With the honest math: steady-state 24/7 can be close on price, but the cloud buys elasticity for spiky workloads, managed undifferentiated work (backups, patching, failover), and provisioning speed. The follow-up they want: 'and without FinOps governance, variable spend surprises you.' The interview line: 'CapEx is a bet; OpEx is a meter — I choose by workload shape.'",
},
"cloud-interview-prep--cloud-networking": {
"front": "Security group vs NACL — when does the difference actually bite?",
"back": "Security groups are stateful (return traffic auto-allowed) at the instance level; NACLs are stateless (both directions need rules) at the subnet level. It bites when SSH works through the security group but the NACL blocks the ephemeral-port return — connection hangs, not refused. The interview line: 'stateful forgives; stateless makes you write both directions.'",
},
"cloud-interview-prep--cloud-data": {
"front": "How do you answer 'SQL or NoSQL?' without sounding religious?",
"back": "By access pattern: relational integrity and ad-hoc queries → managed SQL; single-digit-ms key lookups → key-value; flexible documents → document store. Then the managed caveat: 'I choose the NoSQL by the query pattern, then take the managed version of that choice.' The interview line: 'the workload picks the store; I just read its requirements.'",
},
"cloud-interview-prep--cloud-security-controls": {
"front": "What's the first thing you check in an unfamiliar cloud account?",
"back": "Identity: who has what access. Users without MFA, wildcard admin policies, and ancient access keys are the fastest wins — most breaches start at identity, not at the firewall. The interview line: 'I audit the front door before the windows.'",
},
"cloud-interview-prep--cloud-arch-build": {
"front": "How do you present architecture tradeoffs without rambling?",
"back": "Three beats per decision: the choice, what it costs (money, complexity, latency), and when you'd choose differently. Then stop and invite the follow-up. The interview line: 'every architecture is a list of paid prices — I show the receipts.'",
},
"cloud-interview-prep--cloud-mock": {
"front": "How do you handle 'design X' when you've never built X?",
"back": "Fall back to the shapes you know: requirements first, then map X onto three-tier, queue, or event-driven patterns, stating the mapping aloud. Interviewers grade method transfer, not prior exposure. The interview line: 'I haven't built this exact system; here's how I'd reason about it from patterns I have built.'",
},
}

def _q(q, choices, answer, explain):
    assert len(choices) == 4 and 0 <= answer <= 3 and explain
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}

P3_NEW_QUIZ = {
"cloud-interview-prep--cloud-concepts": [
_q("Running production in a single AZ is risky because:",
   ["It's expensive", "An AZ failure takes the whole service down — one AZ is a single point of failure", "It's slower", "Regions require it"], 1,
   "HA means ≥2 AZs; the AZ is the failure boundary — the Concepts."),
_q("The edge (CDN/points of presence) primarily buys:",
   ["Resilience", "Proximity — content served near users, not survival of AZ failures", "Encryption", "Storage"], 1,
   "Edge is about latency to users; AZs are about surviving failure — the Concepts."),
_q("Serverless fits spiky, intermittent workloads because:",
   ["It's always cheaper", "It scales to zero — you pay per invocation instead of idle servers", "It's faster", "No code needed"], 1,
   "Pay-per-invocation with scale-to-zero matches intermittent demand — the Concepts."),
_q("The honest follow-up to 'the cloud saves money' is:",
   ["It's always true", "Without FinOps governance, variable OpEx spend surprises you — savings need discipline", "Discounts are automatic", "CapEx is dead"], 1,
   "The module's honesty: agility is the real pitch; savings require governance — the Worked estimation."),
_q("Under shared responsibility, patching the guest OS on your VM is:",
   ["The provider's job", "Your job — the OS is in your layer, 'in the cloud'", "Nobody's job", "Automatic"], 1,
   "The provider secures OF the cloud; the guest OS is IN it — the Concepts."),
_q("Leading with vendor-neutral concepts is strong because:",
   ["Vendors don't matter", "Concepts transfer across providers; console click-paths expire with the UI", "It's faster", "Interviewers dislike vendors"], 1,
   "'I learn the concept once, the console twice' — the Project brief's trap answers."),
],
"cloud-interview-prep--cloud-networking": [
_q("An instance in a private subnet reaches the internet for patches via:",
   ["A public IP", "NAT — outbound internet without inbound reachability", "VPN", "Peering"], 1,
   "NAT is the private subnet's outbound path — the Concepts."),
_q("A connection that hangs (not refused) after the security group was fixed suggests:",
   ["DNS failure", "The stateless NACL blocking return traffic — both directions need explicit rules", "The instance is off", "TLS mismatch"], 1,
   "Hangs vs refused distinguish NACL drops from rejections — the new card and the Hands-on procedure step 4."),
_q("Health checks on the load balancer exist so that:",
   ["Traffic is fast", "Only passing targets receive traffic — dead instances are removed from rotation", "TLS works", "Costs drop"], 1,
   "The LB is the first reliability device in the path — the Concepts."),
_q("VPC peering beats public IPs for inter-VPC traffic because:",
   ["It's free", "Traffic stays on the private backbone — no internet exposure", "It's faster to configure", "It encrypts"], 1,
   "Private routing for both security and latency — the Concepts."),
_q("A low TTL before a migration is set because:",
   ["Caching is good", "You expect to change the target soon and need fast propagation", "It's cheaper", "DNS requires it"], 1,
   "Low TTL trades query volume for agility — the Project brief's DNS section."),
_q("Flow logs are read first when debugging a suspected security-group issue because:",
   ["They're fast", "They show allowed/rejected IP traffic — the packet-level audit trail", "They're required", "They show app errors"], 1,
   "Flow logs record who tried to reach whom — the Concepts."),
],
"cloud-interview-prep--cloud-data": [
_q("Direct-to-object-storage uploads via presigned URLs are preferred because:",
   ["They're faster", "Bytes never touch your app servers — the app never proxies upload traffic", "They're free", "They encrypt"], 1,
   "'Bytes never touch my app servers' — the upload pattern in the Project brief."),
_q("A workload needing complex ad-hoc joins across entities belongs on:",
   ["Key-value NoSQL", "Managed SQL — relational integrity and query flexibility are its strengths", "Object storage", "A cache"], 1,
   "Choose by access pattern: relational queries → SQL — the new card."),
_q("An RPO of 1 hour requires:",
   ["Daily backups", "Backups or replication at least hourly — daily backups would violate it by 23 hours", "No backups", "Weekly tapes"], 1,
   "RPO bounds data loss; the backup frequency must fit inside it — the Worked estimation."),
_q("Moving 7-year compliance archives to cold storage is justified because:",
   ["It's faster", "Rarely-accessed retention data shouldn't pay hot-storage prices", "It's required", "It's encrypted"], 1,
   "Cost follows access frequency — the lifecycle tiering in the Concepts."),
_q("The first question about any backup strategy is:",
   ["Its cost", "'When did we last restore from it?' — an untested backup is a hope, not a plan", "Its vendor", "Its speed"], 1,
   "Restore tests are what make backups real — the Worked estimation step 5."),
_q("Caching without a named invalidation strategy is dangerous because:",
   ["Caches are slow", "Stale data is caching's permanent tax — the strategy is the design", "It's expensive", "Invalidation is optional"], 1,
   "Every caching decision must name invalidation — the Concepts."),
],
"cloud-interview-prep--cloud-security-controls": [
_q("An IAM user with console access and no MFA is:",
   ["Fine for dev", "The first finding in any audit — identity is the front door", "Required", "Encrypted"], 1,
   "Identity review starts here — the Hands-on procedure step 1 and the new card."),
_q("SCPs differ from IAM policies in that SCPs:",
   ["Are longer", "Are preventive guardrails — they make bad actions impossible account-wide", "Are optional", "Replace MFA"], 1,
   "Preventive vs detective: SCPs block, Config rules catch — the Concepts."),
_q("Credentials found in a repo should be:",
   ["Deleted from history only", "Rotated immediately and moved to a secret manager, fetched at runtime", "Left alone", "Emailed around"], 1,
   "Secrets are fetched, not shipped — and exposed ones are burned, per the Hands-on procedure step 3."),
_q("A detective control for 'someone opened SSH to the world' is:",
   ["An SCP blocking it", "A Config rule flagging it plus audit-trail review — it catches what happened", "MFA", "Encryption"], 1,
   "Preventive blocks; detective catches — the Concepts' guardrail pair."),
_q("Encryption at rest for the database is best described as:",
   ["The differentiator", "The baseline — expected, not exceptional; the differentiator is key management", "Optional", "Expensive"], 1,
   "Encryption is table stakes; who holds the keys and how they rotate is the interview depth — the Concepts."),
_q("Presenting findings risk-ranked with business impact works because:",
   ["It's long", "Decision-makers need prioritization: what burns first, what it costs, how to fix it", "It's traditional", "Tools do it"], 1,
   "Lead with criticals, never a 200-item undifferentiated list — the Hands-on procedure step 6."),
],
"cloud-interview-prep--cloud-arch-build": [
_q("Putting the app tier in private subnets is primarily about:",
   ["Cost", "Minimizing internet-facing surface — only the load balancer is directly reachable", "Speed", "NAT"], 1,
   "One controlled entry point, defense in depth behind it — the Concepts' three-tier."),
_q("Data transfer is the classic cost surprise because:",
   ["It's untracked", "Chatty cross-AZ/region architectures pay per GB, compounding silently", "It's fixed", "It's the largest line"], 1,
   "Transfer compounds with architecture chatter — the Worked estimation step 3."),
_q("A failure-mode review asks, per component:",
   ["The happy path", "What breaks, how it degrades, and whether that degradation is acceptable", "The cost", "The vendor"], 1,
   "Designing for the unhappy path separates architecture from diagramming — the Concepts."),
_q("An ADR is written so that:",
   ["Meetings are shorter", "The 'why' survives team turnover — decisions, context, alternatives, consequences", "Diagrams look good", "Auditors are happy"], 1,
   "'ADRs are how architecture survives team turnover' — the Concepts."),
_q("Showing both the Cadillac and the Honda architectures proves:",
   ["Indecision", "Value judgment — you optimize for the business, not for resume-driven architecture", "Cheapness", "Speed"], 1,
   "Cost-vs-benefit judgment is the architect-level signal — the Worked estimation step 5."),
_q("IaC for the whole stack matters to the architecture review because:",
   ["It's trendy", "The architecture exists as reproducible, reviewable code — not just a diagram", "It's faster", "Diagrams are banned"], 1,
   "Reproducible and reviewable beats pictorial — the Concepts."),
],
"cloud-interview-prep--cloud-mock": [
_q("A deep-dive round on 'how does the load balancer work' is testing:",
   ["Memory", "Whether you know the mechanism under the abstraction — not the marketing page", "Speed", "Certifications"], 1,
   "Abstractions leak; interviewers probe the layer below the console — the Concepts."),
_q("When the partner says 'cut 30% from the bill', the strong move is:",
   ["Refuse", "Defend or concede each line with its reliability tradeoff stated", "Cut randomly", "Redesign everything"], 1,
   "Cost cross-examination grades value judgment — the Hands-on procedure step 3."),
_q("Scoring yourself against the Well-Architected pillars after a mock works because:",
   ["It's formal", "The pillars are the interview's hidden grading sheet — the lowest pillar aims next week's study", "It's fast", "Partners like it"], 1,
   "Visible targets beat vague feelings — the Hands-on procedure step 5."),
_q("'Design a URL shortener' is really testing:",
   ["Memorization", "ID generation, caching, and the scaling story — the lesson, not the diagram", "Databases", "DNS"], 1,
   "The classics each teach one lesson — the Concepts' 'Design X' patterns."),
_q("Saying 'I haven't built this exact system; here's how I'd reason about it' is strong because:",
   ["It's humble", "Interviewers grade method transfer — honest reasoning from known patterns", "It's short", "It ends questions"], 1,
   "Method under novelty is the actual skill — the new card."),
_q("The cost questions candidates forget to prepare are costly because:",
   ["Interviewers are cheap", "Cost narration is the architect-level signal — value judgment, not just technical design", "Bills are scary", "Math is hard"], 1,
   "'The Cadillac and the Honda, and when each wins' — the Concepts' cost narration."),
],
}
