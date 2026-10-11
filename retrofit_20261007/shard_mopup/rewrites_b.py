# Shard B instructor-voice rewrites. Key: (path_id, module_id) -> new il_provides blurb.
# 2-3 sentences, first-person instructor, substance grounded in title/topics/original blurb.
RW_B = {
# ---------- il05-devops-core ----------
("il05-devops-core", "devops-role-map"):
"I'm your instructor for this module, and I give you the single canonical DevOps role map for the university — seven roles, one path. In this module I study a leading platform's paths and a nonprofit bootcamp's cohort as competitive context, never duplicating either. By the end you'll have milestone projects per role, graded against production-like rubrics.",
("il05-devops-core", "linux-shell-git"):
"I'm your instructor for this module. Rather than teaching Linux twice, I cross-link you to IL-04's Linux path — one Linux discipline, referenced not repeated. By the end you'll administer Linux, script the shell, move through Git and GitHub workflows, and reach for Go or Python when you need tooling.",
("il05-devops-core", "git-github"):
"I'm your instructor for this module. In this module I put you on a simulated team repository where your branching discipline gets reviewed like production code. By the end you'll run branching strategies, pull requests, GitHub Actions basics, and the monorepo-versus-polyrepo decision the way a working team does.",
("il05-devops-core", "containers-docker"):
"I'm your instructor for this module. In this module I run image-hardening labs where your image gets scanned — and the vulnerabilities it surfaces are yours to fix. By the end you'll read images and layers, write Dockerfiles, work registries, and use multi-stage builds to ship small, hardened containers.",
("il05-devops-core", "cicd-jenkins"):
"I'm your instructor for this module. In this module I have you build a pipeline, break it, and secure it — using the CI gates from this university's own release discipline as the example. By the end you'll treat pipelines as code, run agents and stages, manage artifacts, and put security scanning gates where they can't be skipped.",
("il05-devops-core", "k8s-foundations"):
"I'm your instructor for this module, and I teach the operation half of the Kubernetes story here. In this module I give you the on-ramp to the full CNCF stack in il05-cloud-native — this module teaches operation, that path certifies it. By the end you'll run pods, services, deployments, ConfigMaps, secrets, ingress, and Helm basics with confidence.",
("il05-devops-core", "ansible-config"):
"I'm your instructor for this module. I cross-link you to IL-04's RHCE path — one Ansible discipline, two destinations — so the material is taught once and taught well. By the end you'll write playbooks for fleet state, compose roles, guard secrets in Vault, and make every operation idempotent.",
("il05-devops-core", "observability"):
"I'm your instructor for this module. In this module I hand you an instrumented demo fleet with a real incident to diagnose — your first on-call, supervised. By the end you'll query metrics in PromQL, write alerts that mean something, build dashboards, and aggregate logs with Loki.",
# ---------- il05-cloud-native ----------
("il05-cloud-native", "kcna-foundations"):
"I'm your instructor for this module. In this module I give you the readiness map for every KCNA domain — and lab verification for every claim of competence you make. By the end you'll be able to demonstrate Kubernetes architecture, cloud-native principles, GitOps concepts, and observability basics, not just describe them.",
("il05-cloud-native", "cka-prep"):
"I'm your instructor for this module. The CKA is hands-on, so in this module I prepare you hands-on: performance-style task drills under time. By the end you'll move through cluster architecture and etcd, workloads and scheduling, services and networking, storage, and troubleshooting at exam intensity — original tasks, not memorized answers.",
("il05-cloud-native", "ckad-prep"):
"I'm your instructor for this module. In this module I run developer-workflow drills where you ship, debug, and observe real workloads against the clock. By the end you'll design applications, configure deployments, build in observability, and wire services and networking the way the CKAD demands.",
("il05-cloud-native", "cks-prep"):
"I'm your instructor for this module. In this module I run adversarial labs: you harden a cluster, then attack a peer's, then write the incident report. By the end you'll handle cluster hardening, system hardening, supply-chain security, and runtime security with Falco, seccomp, and AppArmor — and you'll have the scar tissue to prove it.",
("il05-cloud-native", "kcsa-prep"):
"I'm your instructor for this module, and I position this module honestly as associate-level. In this module I give you the security-vocabulary layer that makes the CKS deep dives legible. By the end you'll read the cloud-native security overview, Kubernetes security fundamentals, and the exam's domain map fluently — the language the deep work is written in.",
# ---------- il05-zero-trust ----------
("il05-zero-trust", "sp800-207-tenets"):
"I'm your instructor for this module. In this module I run architecture-decision exercises where you place PEPs and write policy for a fictional enterprise. By the end you'll reason from the seven tenets directly — policy engine, policy administrator, policy enforcement point, control plane versus data plane, the trust algorithm — and your work is graded on tenet fidelity.",
("il05-zero-trust", "identity-pillar"):
"I'm your instructor for this module. In this module I give you a lab identity fabric where you implement step-up authentication and watch the policy engine decide in real time. By the end you'll treat identity as the perimeter: phishing-resistant MFA, device posture, continuous authentication, and privileged access done right.",
("il05-zero-trust", "microsegmentation"):
"I'm your instructor for this module. In this module I hand you a segmented lab network that you must traverse the way an attacker would — then re-architect so that path closes. By the end you'll design segmentation strategies, reason about software-defined perimeters, inspect east-west traffic, and encrypt everything that matters.",
("il05-zero-trust", "zt-deployment-models"):
"I'm your instructor for this module. In this module I set the migration-plan capstone: a brownfield enterprise, a phased zero-trust roadmap, and a review board that asks hard questions. By the end you'll compare the device-agent/gateway, enclave, and resource-portal models, plan a migration from perimeter security, and measure zero-trust maturity honestly.",
# ---------- il05-terraform ----------
("il05-terraform", "hcl-foundations"):
"I'm your instructor for this module. In this module I give you a sandbox cloud account where every plan is reviewed before apply — the workflow taught as a discipline, not a command. By the end you'll work resources and providers, variables and outputs, the plan/apply cycle, and state fundamentals without flinching.",
("il05-terraform", "state-modules"):
"I'm your instructor for this module. In this module I run state-surgery labs where you recover corrupted state the way production engineers do — in a safe copy, never in panic. By the end you'll run remote state with locking, compose modules, use workspaces, and import and refactor without losing the thread.",
("il05-terraform", "terraform-associate-prep"):
"I'm your instructor for this module. In this module I run scenario-based readiness checks per exam domain, and I tell you plainly: the exam itself is booked through HashiCorp's own portal. By the end you'll cover the Terraform Associate (003) exam domains, IaC concepts, the core workflow, and advanced features — plus honest exam-day logistics.",
# ---------- il06-hackers-arise ----------

# ---------- il06-hackers-arise ----------
("il06-hackers-arise", "linux-for-hackers"):
"I'm your instructor for this module. In this module I build the cross-map itself: every Hackers-Arise Linux topic annotated with where HTB, THM, and PEN-200 cover it — and what only I teach here. By the end you'll run the hacker-oriented Linux curriculum, Bash for operations, and text processing at speed, and you'll know exactly which platform assumed what.",
("il06-hackers-arise", "network-basics-exploitation"):
"I'm your instructor for this module. In this module I author original lab scenarios for the scanning-to-exploitation chain, built in the IL lab format rather than cloned from any vendor. By the end you'll read TCP/IP like an attacker, run network reconnaissance and vulnerability scanning, and follow the exploitation workflow end to end.",
("il06-hackers-arise", "osint-recon"):
"I'm your instructor for this module. In this module I set an original OSINT capstone on a fictional target — all technique, no real persons — with a legal and ethics gate you pass before the module opens. By the end you'll run passive and active reconnaissance with real OSINT tradecraft and documentation discipline.",
("il06-hackers-arise", "password-attacks"):
"I'm your instructor for this module. In this module I teach the time-estimation mathematics and the defender-side lessons; the cracking itself happens in the isolated lab, against your own hashes. By the end you'll identify hashes, build wordlists and rules, estimate rig time honestly, and practice credential hygiene like a defender.",
("il06-hackers-arise", "wifi-hacking"):
"I'm your instructor for this module, and I teach the legal boundary first: lab-only hardware, your own access point, and the defender's view of every attack. In this module I walk you through 802.11 fundamentals, capture and analysis, and WPA handshake attacks — always from both sides of the frame. By the end you'll know the countermeasures as well as the attacks.",
("il06-hackers-arise", "web-app-exploitation"):
"I'm your instructor for this module. In this module I make the dedupe artifact visible: what PortSwigger teaches is linked, what it doesn't is authored here. By the end you'll work the Burp Suite methodology, injection flaws, and authentication attacks — and you'll read the PortSwigger overlap map so you never study the same ground twice.",
("il06-hackers-arise", "forensics-hackers"):
"I'm your instructor for this module. In this module I teach forensics from the attacker's artifacts: you generate the evidence, then you analyze it. By the end you'll work disk and memory forensics, build timeline analyses, understand anti-forensics awareness, and cross the bridge into the IN investigation category.",
("il06-hackers-arise", "scada-ics-satellite"):
"I'm your instructor for this module, and I front-load the safety ethics — OT attacks are taught as defensive knowledge, behind a hard ethics gate. In this module I give you an original survey of OT protocols like Modbus and DNP3, the ICS attack surface, and satellite communications basics. By the end you'll understand safety-critical systems the way a defender must, and the ethics will be non-negotiable.",
("il06-hackers-arise", "nice-framework-map"):
"I'm your instructor for this module. In this module I build the career map: every IL-06 module tagged to NICE work roles by name. By the end you'll see where you fit across Oversight and Governance, Design and Development, Implementation and Operation, Protection and Defense, and Investigation — with honest notes on which roles need clearances or degrees this platform cannot grant you.",
# ---------- il06-offensive ----------
("il06-offensive", "htb-thm-labs"):
"I'm your instructor for this module. The machines belong to HTB and THM; the method is Interstitium's, and that's what I teach here. In this module I give you the methodology layer: enumeration checklists, privilege-escalation pattern catalogs, and report templates. By the end you'll work machine methodology, enumeration discipline, escalation patterns, and documentation like a professional.",
("il06-offensive", "pen200-oscp-map"):
"I'm your instructor for this module. In this module I give you an honest readiness audit — AD lab scenarios and buffer-overflow drills that tell you whether you're ready before you pay for the exam. By the end you'll have internalized the 'try harder' methodology, buffer overflows, Active Directory attacks, and the logistics and stamina the 24-hour exam demands.",
("il06-offensive", "web-app-exploitation"):
"I'm your instructor for this module. In this module I run chained-scenario labs that PortSwigger's per-vulnerability labs don't cover — the attack as a campaign, not a checklist. By the end you'll chain SQLi to RCE, abuse SSRF and cloud metadata, and work deserialization and race conditions the way real engagements unfold.",
("il06-offensive", "ad-attack-chains"):
"I'm your instructor for this module. In this module I hand you a purpose-built AD lab forest with a guided attack-chain curriculum — the single most employable offensive skill, taught end to end. By the end you'll run Kerberoasting and AS-REP roasting, BloodHound methodology, lateral movement, and domain dominance and persistence.",
("il06-offensive", "ctf-tiers"):
"I'm your instructor for this module. In this module I give you the tier architecture itself: original IL challenges at every tier, from guided warmups to research-grade problems. By the end you'll always have a next step that belongs to this platform — T0 through T3 — and you'll know exactly which tier you're ready for.",
("il06-offensive", "report-writing"):
"I'm your instructor for this module. In this module I run a report-review service with a public rubric — your findings graded the way client reports are graded. By the end you'll write finding write-ups, rate risk honestly, craft executive summaries, and verify fixes through retest.",
# ---------- il06-defensive ----------
("il06-defensive", "soc-operations"):
"I'm your instructor for this module. In this module I put you in a simulated SOC with a live alert queue — you triage, escalate, and hunt against the clock, mentored by playbooks. By the end you'll handle alert triage at L1, investigation and correlation at L2, threat hunting at L3, and the detection-engineering mindset behind it all.",
("il06-defensive", "forensics-ir"):
"I'm your instructor for this module. In this module I give you original forensic images with planted intrusions — you build the timeline that convicts the (fictional) intruder. By the end you'll work disk, memory, and network forensics, run the IR lifecycle from detection to lessons-learned, keep chain of custody, and read timelines like evidence.",
("il06-defensive", "detection-engineering"):
"I'm your instructor for this module. In this module I run a detection lab where your rules face a live adversary simulation — precision and recall scored honestly. By the end you'll write Sigma rules, normalize log sources, tune out false positives, and practice threat-informed defense the way working teams do.",
("il06-defensive", "security-plus-bridge"):
"I'm your instructor for this module. In this module I give you the readiness gate and PBQ drills for Security+; the exam itself is booked through CompTIA. By the end you'll own the defensive vocabulary across the SY0-701 domains (V7 current, V8 expected around November 2026) — cross-linked, not duplicated, with IL-09's Security+ module.",
# ---------- il06-fde-interface ----------
("il06-fde-interface", "ik-fde-spine"):
"I'm your instructor for this module. In this module I build the preparation layer: system-design reps, customer-scenario drills, and the honest note that the credential is a leading interview-prep provider's, not ours. By the end you'll understand the FDE role — engineer at the customer — across the AI Engineering spine, the FDE spine, and interview preparation.",
("il06-fde-interface", "mitxpro-cybersecurity"):
"I'm your instructor for this module. In this module I map a preparation track to the published curriculum — every week gets a readiness check, so you enter the $7,750 program ready. By the end you'll be prepared for the 24-week professional certificate, its 36 CEUs, and the 75% pass bar — and the certificate itself remains MIT xPRO's.",
("il06-fde-interface", "third-party-ai-cybersecurity"):
"I'm your instructor for this module. In this module I build the on-ramp: AI and ML literacy at the level the live course assumes. By the end you'll arrive able to contribute from week one — AI in the SOC, AI-assisted threat hunting — and you'll understand the practitioner-led format you're stepping into.",
("il06-fde-interface", "secure-engineering"):
"I'm your instructor for this module. In this module I hand you the FDE security playbook: threat models and review checklists for engineers who ship inside customer environments. By the end you'll threat-model, set secure defaults, run security reviews, and ship safely at the boundary.",

# ---------- il07-mongodb ----------
("il07-mongodb", "atlas-foundations"):
"I'm your instructor for this module. The courses are MongoDB's; the pacing is Interstitium's, and in this module I give you the study schedule with readiness checks per unit. By the end you'll get started with MongoDB Atlas, run clusters on the free tier, explore data, and connect with drivers — plus a local-versus-Atlas decision guide you'll actually use.",
("il07-mongodb", "document-model"):
"I'm your instructor for this module. In this module I run schema-design exercises graded against query patterns, so you feel why embedding versus referencing matters. By the end you'll model documents, collections, and databases, choose value types and identifiers, work flexible schema, and enforce it with schema validation.",
("il07-mongodb", "aggregation-framework"):
"I'm your instructor for this module. In this module I run a pipeline gym: real datasets, staged pipeline problems, and explain-plan reading so performance is learned early. By the end you'll compose pipeline stages — $match, $group, $project, $lookup — wield accumulators and expressions, and think about performance before it bites.",
("il07-mongodb", "data-modeling"):
"I'm your instructor for this module. In this module I convene the modeling review board: you defend a schema against a workload, the way production reviews actually run. By the end you'll model relationships, choose embedding versus referencing patterns, and index for query patterns — and you'll defend those choices out loud.",
("il07-mongodb", "python-mongodb"):
"I'm your instructor for this module. In this module I set the application capstone that connects this path to IL-03's Python modules — one database discipline, used from your own code. By the end you'll drive MongoDB from Python with PyMongo, apply ODM patterns, use transactions, and ship a working application capstone.",
# ---------- il07-data-schools ----------
("il07-data-schools", "data-analyst-track"):
"I'm your instructor for this module. In this module I run the analyst portfolio track: every module ends in a presentable artifact, because analysts are hired on evidence. By the end you'll have SQL fluency, visualization and reporting, statistics for analysts, and a portfolio that speaks for you.",
("il07-data-schools", "data-engineering-track"):
"I'm your instructor for this module. In this module I set a pipeline capstone on real-scale data with data-quality gates — the warehouse is built, loaded, and defended. By the end you'll orchestrate pipelines, model dimensional warehouses, run batch and streaming, and enforce data quality and governance.",
("il07-data-schools", "databases-deep"):
"I'm your instructor for this module. In this module I teach the internals layer — B-trees and query planners with visualizations — cross-linked to IL-03's SQL module without duplication. By the end you'll understand relational internals, indexing and query planning, and transactions and isolation in the 6.5830/6.5831 lineage.",
("il07-data-schools", "big-data-systems"):
"I'm your instructor for this module. In this module I run scale-reasoning exercises where you price and size architectures — because big data is an economic discipline first. By the end you'll reason about distributed processing, the Hadoop/Spark lineage, mining massive datasets, and cost and scale together.",
("il07-data-schools", "mit-credentials"):
"I'm your instructor for this module. In this module I give you the preparation map: which IL modules cover which credential's prerequisites, with readiness gates before you spend a dollar. By the end you'll be ready for the xPRO Data Engineering and Advanced Analytics programs and the MicroMasters SDS graduate spine — and I never imply MIT endorsement.",
("il07-data-schools", "stanford-credentials"):
"I'm your instructor for this module. In this module I give you the preparation map with the same honesty contract: preparation here, credential there, no implied partnership. By the end you'll be ready for Stanford's Data Mining & Applications, Mining Massive Data Sets, and Databases graduate certificates — the study lives here, the credential lives there.",
# ---------- il07-ai-ml ----------
("il07-ai-ml", "ml-foundations-cs229"):
"I'm your instructor for this module. In this module I work the convex-optimization appendix from CS229's own review handouts, plus debugging-ML exercises in the CS230 'Structuring ML Projects' spirit. By the end you'll handle supervised learning, kernels and SVMs, Bayesian methods, and learning theory — bias/variance, VC dimension — the mathematical ground the rest stands on.",
("il07-ai-ml", "deep-learning-cs230"):
"I'm your instructor for this module. In this module I give you GPU notebook playgrounds and the backprop-from-scratch graded exercise — the CS231N assignment-1 ethos, original problems. By the end you'll build neural network foundations, derive backprop from scratch in NumPy, run CNNs on CIFAR-10, and work PyTorch as your primary framework.",
("il07-ai-ml", "nlp-cs224n"):
"I'm your instructor for this module. In this module I open the fine-tuning laboratory: PEFT/LoRA on open models with evaluation harnesses, so you measure rather than vibe. By the end you'll move from classical NLP through transformers to instruction tuning and RLHF, with tokenization and decoding strategies under your belt.",
("il07-ai-ml", "vision-cs231n"):
"I'm your instructor for this module. In this module I run the vision project arc: from kNN through transfer learning on a real dataset, with honest compute budgets stated up front. By the end you'll work CNN architectures, detection and segmentation, vision transformers, and transfer learning — with the costs visible from day one.",
("il07-ai-ml", "rl-cs234"):
"I'm your instructor for this module. In this module I build the RLHF bridge: how the RL you learn here becomes the H in the NLP module's RLHF — taught as one story. By the end you'll handle MDPs and dynamic programming, policy gradients, and value methods, and you'll see exactly where reinforcement learning meets language models.",
("il07-ai-ml", "mlops-production"):
"I'm your instructor for this module. In this module I teach the unglamorous half of ML seriously: the production-readiness checklist and a model-deployment capstone with monitoring. By the end you'll work maturity levels 0/1/2, track experiments, deploy and monitor models, and version data and models like production demands.",
("il07-ai-ml", "llm-engineering"):
"I'm your instructor for this module. In this module I enforce the evaluation-first discipline: every LLM system you build ships with a benchmark harness, because unevaluated AI is astrology. By the end you'll design RAG architectures, build agents with tool use, evaluate with MMLU, HELM, HumanEval, and RAGAS, and run LLMOps in production.",
# ---------- il07-neuroai ----------
("il07-neuroai", "comp-neuro-foundations"):
"I'm your instructor for this module. In this module I build the mathematics bridge: every biophysical model is paired with the IL-02 differential-equations and probability nodes it assumes. By the end you'll handle neural coding — rate versus spike — leaky integrate-and-fire and Hodgkin-Huxley models, Hebbian learning and STDP, and Hopfield networks as the bridge to AI.",
("il07-neuroai", "neural-modeling-simulation"):
"I'm your instructor for this module. In this module I open the capstone laboratory: build and simulate a small spiking network, and compare rate versus spike coding against an AI baseline. By the end you'll work NEURON compartmental models, Brian2 spiking networks in Python, and STDP rules in code.",
("il07-neuroai", "neuroai-synthesis"):
"I'm your instructor for this module. In this module I deliver the synthesis itself: an original comparative framing of what brains generalize and how — with every analogy labeled for its limits. By the end you'll weigh transformer attention against biological attention honestly, work predictive coding and the Bayesian brain, understand spiking networks and neuromorphic hardware, and treat the backprop question as open research, not settled syllabus.",

# ---------- il08-mit-63 ----------
("il08-mit-63", "mit63-programming"):
"I'm your instructor for this module. In this module I cross-link you to IL-03's Python modules — one Python discipline — with the MIT sets as the advanced problem bank. By the end you'll handle Python at MIT depth, computational thinking, and the problem-set discipline of 6.100A/B.",
("il08-mit-63", "mit63-mathcs"):
"I'm your instructor for this module. In this module I route you to the single canonical discrete-math node shared with IL-02 — no duplicated courses. By the end you'll prove by induction, work number theory and graph theory, and apply probability for computing at the 6.1200 level.",
("il08-mit-63", "mit63-algorithms"):
"I'm your instructor for this module. IL-03's DSA is the applied sibling; in this module I teach the theoretical home of algorithms. By the end you'll design and analyze algorithms, prove lower bounds, and navigate NP-completeness at the 6.1210/6.1220 level.",
("il08-mit-63", "mit63-compstruct"):
"I'm your instructor for this module. In this module I run simulator labs, with the honest note on what needs real hardware versus what simulates faithfully. By the end you'll trace the path from gates to the processor and read the hardware/software contract the way 6.1910 teaches it.",
("il08-mit-63", "mit63-systems"):
"I'm your instructor for this module. In this module I give you the design-paper reading guide for systems engineering — cross-linked to IL-04's hands-on administration. By the end you'll read computer systems and operating system engineering the way 6.1800/6.1810 expect, and you'll recognize design at scale when you see it.",
("il08-mit-63", "mit63-theory"):
"I'm your instructor for this module. In this module I set proof exercises with machine-checked steps — the theory track's assessment is formal, because the subject is. By the end you'll work finite automata and Turing machines, complexity classes, and the 6.1400 lineage with real rigor.",
# ---------- il08-cmu-cs ----------
("il08-cmu-cs", "imperative-functional-core"):
"I'm your instructor for this module. In this module I build the cross-walk: where CMU's sequence overlaps IL-03/IL-08's canonical nodes, I route you to the single node. By the end you'll work 15-122's imperative computation and 15-150's functional programming with correctness as a habit.",
("il08-cmu-cs", "cmu-dsa-systems"):
"I'm your instructor for this module. In this module I reimplement the famous labs for the platform's sandbox — the shell lab and malloc lab as original exercises in their spirit. By the end you'll handle 15-210's parallel and sequential DSA and 15-213's introduction to computer systems with the labs that made them legendary.",
("il08-cmu-cs", "cmu-theory"):
"I'm your instructor for this module. In this module I integrate theory with problem solving in CMU's style — every theorem ships with a programming exercise. By the end you'll work 15-251's great ideas and 15-451's algorithm design and analysis with proofs plus programming, together.",
("il08-cmu-cs", "cmu-systems-depth"):
"I'm your instructor for this module, and I enforce the readiness gate honestly: 15-410's prerequisites — C, assembly, 2's complement fluency — are verified before the module opens. In this module I take you into systems depth across 15-445 database systems, 15-440 distributed systems, and 15-410 operating system design. By the end you'll be ready to build a kernel.",
("il08-cmu-cs", "cmu-ai-breadth"):
"I'm your instructor for this module. In this module I use CMU's integrated AI/ML intro as the on-ramp and route the deeper study to IL-07's AI spine. By the end you'll have implemented AlexNet, GPT-2, and AlphaZero-scale ideas across search, ML, RL, and probability from 07-280 — and you'll know where to go deeper.",
# ---------- il08-stanford-cs ----------
("il08-stanford-cs", "programming-abstractions"):
"I'm your instructor for this module. In this module I map Stanford's sequence onto IL-03's canonical programming nodes, with 106B's C++ depth as the differentiator. By the end you'll handle 106A's programming methodology in Python and 106B's programming abstractions in C++ — recursion and data structures at Stanford depth.",
("il08-stanford-cs", "stanford-mathcs"):
"I'm your instructor for this module. In this module I route you to the single canonical nodes in IL-02 — the cross-walk, not a second course. By the end you'll cover CS 103's proofs, logic, and graphs and CS 109's probability for computer scientists through one coherent mathematical home.",
("il08-stanford-cs", "stanford-systems"):
"I'm your instructor for this module, and I teach the current course: the modernization note matters — CS 111 replaces the retired CS 110/140 in this spine. In this module I walk you through CS 107's computer organization and systems and CS 111's operating systems principles. By the end you'll be working the course Stanford actually teaches now.",
("il08-stanford-cs", "stanford-algorithms"):
"I'm your instructor for this module. In this module I make CS 161's prerequisite chain — 106B, 103, 109 — visible as the platform's own gates, because the chain is the curriculum. By the end you'll design and analyze algorithms across divide-and-conquer, dynamic programming, graphs, and randomization.",
("il08-stanford-cs", "stanford-depth"):
"I'm your instructor for this module. In this module I give you the branch map: each Stanford depth course routed to its canonical IL home — IL-07 for AI, IL-08 for theory and systems. By the end you'll see the whole depth landscape — theory, systems, AI — with one node per concept, university-wide.",
# ---------- il07-openweight ----------
("il07-openweight", "openweight-licensing"):
"I'm your instructor for this module, and I put the hard truth up front: 'open weights' and 'open source' are not the same thing, and the difference decides what you may legally ship. In this module I give you the license taxonomy in original prose — OSI-approved versus open-weight-only, with the exact license name quoted from each card — plus the audit worksheet where you classify six real model cards. By the end you'll run the 'check the card, not the rumor' checklist as reflex.",
("il07-openweight", "openweight-llama"):
"I'm your instructor for this module. In this module I lay out the family timeline in original prose, the license-reality explainer (why 'Llama is open source' is false), and a hardware-tier mapping for the 3.x and 4.x generations. By the end you'll trace the Llama arc from research release to default open-weight reference, quote the Llama Community License correctly, and know which rig runs what — stated as planning guidance, not vendor claims.",
("il07-openweight", "openweight-mistral"):
"I'm your instructor for this module. In this module I build a release-by-release license map with the 'check each card' discipline drilled in — because the license varies by release and you never assume the lineage. By the end you'll know Mistral Large 3, Small, Ministral, and the Mixtral classics release by release, and you'll understand why quotable licensing matters for shipping.",
("il07-openweight", "openweight-qwen"):
"I'm your instructor for this module. In this module I teach the Apache-tier versus Max-tier explainer in original prose, distill the official serving recommendations, and walk you through tracing a license claim from card to LICENSE file. By the end you'll know why Qwen releases land everywhere, what's verified from the LICENSE file in the official repo, and why you read before commercializing.",
("il07-openweight", "openweight-deepseek"):
"I'm your instructor for this module. In this module I explain why the MIT grant matters for builders — distill, modify, ship, with the actual terms quoted — and I work the distill-license inheritance rule through an example, because distill variants inherit their base model's license. By the end you'll run R1 and V3 MoE flagships with official serving guidance, and that inheritance rule will be second nature.",
("il07-openweight", "openweight-gemma-phi"):
"I'm your instructor for this module. In this module I teach the Gemma license break across generations — old terms versus new grant, with the warning to never quote the old terms as current — and the small-model hardware story. By the end you'll know Gemma 4 under Apache 2.0, Gemma 1–3 under the restrictive terms, and Phi-4 under MIT — plus what edge and on-device sizes actually unlock.",
("il07-openweight", "openweight-model-cards"):
"I'm your instructor for this module. In this module I give you the teardown worksheet and a worked example on one card — every claim traced to a line on the card, because an un-cited claim is a rumor. By the end you'll read card anatomy like a contract: license, intended use, training-data notes, eval claims, hardware guidance — and you'll spot the red flags: vague licenses, missing cards, eval claims without harnesses.",
("il07-openweight", "openweight-quantization"):
"I'm your instructor for this module. In this module I give you the format comparison in original prose — algorithm versus container, stated plainly — and the measurement lab where you run one model at three quantization levels and record the quality deltas honestly. By the end you'll know GPTQ, AWQ, and GGUF for what they are, and you'll understand that the tradeoff is empirical — measured, not assumed.",
("il07-openweight", "openweight-ollama"):
"I'm your instructor for this module. In this module I give you the Modelfile authoring guide in original prose and the build-and-serve lab: author a custom Modelfile — system prompt plus parameters — serve it, and call it from your own code against the local API. By the end you'll run Ollama as what it is: a local runner with versioned model builds, not a model itself.",
("il07-openweight", "openweight-llamacpp"):
"I'm your instructor for this module. In this module I give you the build guide — backend selection for your hardware — the measurement lab where you serve a GGUF model on a CPU-only machine and record tokens/sec and the offload split, and the 'when to reach for it' decision note. By the end you'll run plain C/C++ inference on ggml with no Python stack and no framework tax, and you'll know when the Python stacks win instead.",
("il07-openweight", "openweight-vllm"):
"I'm your instructor for this module. In this module I explain the serving architecture in original prose — why PagedAttention is a memory-management idea wearing an ML costume — and I run the load-test lab where you serve a 7–8B model, hammer it with concurrent requests, and compare throughput against a naive server. By the end you'll know the throughput triad — continuous batching, chunked prefill, prefix caching — and the difference will be measured, not marketed.",
("il07-openweight", "openweight-hf-stack"):
"I'm your instructor for this module. In this module I give you the Hub workflow guide — download a gated model properly: terms accepted, token scoped — and the honest TGI status note, because teaching an archived stack as current would be a lie. By the end you'll treat the Hub as the canonical weight source, work the Transformers library as the model-definition layer, and know that TGI is history while vLLM, SGLang, and llama.cpp are the present.",
("il07-openweight", "openweight-vram"):
"I'm your instructor for this module. In this module I teach the sizing method in original prose and the three-scenario sizing worksheet — one hardware recommendation each, estimate labeling intact throughout — with the standing reminder: check the card. By the end you'll do the rule-of-thumb math honestly labeled as planning estimates, budget KV-cache for long context, and make the single-GPU versus multi-GPU decision like an engineer.",
("il07-openweight", "openweight-capstone"):
"I'm your instructor for this module. In this module I set the capstone rubric: license-justification correctness, reproducibility of your setup docs, measured throughput numbers (not vibes), and an honest limitations section. By the end you'll have picked a family and justified the license choice in writing, deployed a model behind an API on Ollama, llama.cpp, or vLLM, documented it so a stranger can reproduce it, and run an eval smoke test. The deliverable is an endpoint you operate, not a notebook you ran.",

# ---------- il07-agents ----------
("il07-agents", "agents-anatomy"):
"I'm your instructor for this module. In this module I teach the loop anatomy in original prose and set the baseline lab: a hand-rolled ReAct loop against a local Ollama model. By the end you'll see that every agent is a perceive–act loop around a model, with tool calling as the primitive — and every framework module that follows gets compared against this baseline, so you learn what the harness adds and what it costs.",
("il07-agents", "agents-langchain"):
"I'm your instructor for this module. In this module I teach the middleware pattern in original prose and run the tracing lab: a tool-using agent with guardrail middleware and a LangSmith trace you can read end to end. By the end you'll work the modern LangChain identity — create_agent and the agent-first API — so the loop is inspectable, not magic.",
("il07-agents", "agents-langgraph"):
"I'm your instructor for this module. In this module I teach the graph-pattern catalog in original prose and run the checkpointing lab: an approval-gated workflow where the agent pauses mid-run for human sign-off, then resumes from the checkpoint. By the end you'll build agents as nodes in a graph with durable execution, persistence, and human-in-the-loop steps — this is what 'production-shaped' means.",
("il07-agents", "agents-llamaindex"):
"I'm your instructor for this module. In this module I teach the data-layer-first design guide and run the corpus lab: ingest a real document corpus, index it, retrieve from it, and answer with citations. By the end you'll build data-first agents — context augmentation as the identity, ingestion and retrieval as first-class citizens — because the agent is only as good as its context pipeline.",
("il07-agents", "agents-crewai"):
"I'm your instructor for this module. In this module I teach the role-decomposition method in original prose and run the crew lab: staff a research-and-report crew of specialists and watch delegation and handoffs happen. By the end you'll know when the role metaphor helps and when it is theater — and you'll judge whether it earned its keep.",
("il07-agents", "agents-microsoft"):
"I'm your instructor for this module. In this module I give you the Microsoft lineage map with status labels in original prose — what is current, what is maintenance, what is community-continued — and the migration-note exercise where you compare a plugin-style task across the SK-era and Agent Framework docs and write the migration note yourself. By the end you'll know Semantic Kernel, the Agent Framework, AutoGen's maintenance status, and AG2's community continuation — and which is current for greenfield work.",
("il07-agents", "agents-haystack"):
"I'm your instructor for this module. In this module I teach the pipeline-audit method in original prose and run the traceable-RAG lab: a production-shaped RAG pipeline with full tracing, so every retrieval decision is visible and defensible. By the end you'll wire explicit modular pipelines — retrieval, ranking, filtering, generation — with lifecycle hooks and full step, token, and tool-call tracking.",
("il07-agents", "agents-dspy"):
"I'm your instructor for this module. In this module I teach the metric-first method in original prose and run the optimization lab: define a metric and labeled examples, then let the optimizer beat your hand-written prompt on your own data. By the end you'll program with typed Signatures and composable Modules, and let GEPA or MIPROv2 tune against your metric — the discipline is the point, not the leaderboard.",
("il07-agents", "agents-mcp"):
"I'm your instructor for this module. In this module I explain the protocol in original prose — an open standard that standardizes connection, not agent behavior — and I run the build-it-twice lab: build an MCP server exposing a local tool, then consume it from two different clients. By the end you'll know JSON-RPC's three primitives — tools, resources, prompts — and feel what 'write once' means.",
("il07-agents", "agents-openai-sdk"):
"I'm your instructor for this module. In this module I teach the thin-harness pattern in original prose and run the handoff lab: a multi-agent handoff workflow with guardrails and tracing. By the end you'll compose agents, handoffs, and agents-as-tools with sessions and built-in tracing — and you'll be able to prove how much (or how little) harness a task needs.",
("il07-agents", "agents-selection"):
"I'm your instructor for this module. In this module I give you the selection matrix, the rubric template, and the failure-mode field guide in original prose — plus the lab where you score two frameworks on one task with a written rubric, pick a winner, and defend it. By the end you'll choose harnesses on paper: task-success rubrics, cost and latency budgets per run, and the known failure modes — tool loops, context bloat, silent degradation. Judgment is the deliverable.",
("il07-agents", "agents-capstone"):
"I'm your instructor for this module. In this module I set the capstone rubric: justification quality, harness rigor, reproducibility, honest limits. By the end you'll have shipped a complete agent — framework chosen with written justification, at least one MCP tool done for real, an eval harness with a rubric, cost and latency notes, and a limitations section that states where it breaks before anyone asks.",
# ---------- il07-frontier ----------
("il07-frontier", "frontier-attention"):
"I'm your instructor for this module. In this module I explain the mechanism in original prose — the scaling factor derived, not asserted — and I set the from-scratch lab: implement scaled dot-product attention in NumPy and visualize head patterns on a real sentence. By the end you'll own scaled dot-product attention, multi-head specialization, causal masking, and the quadratic cost of sequence length that makes KV-caching and PagedAttention necessary.",
("il07-frontier", "frontier-preference"):
"I'm your instructor for this module. In this module I teach the pipeline-to-menu narrative in original prose — from RLHF's three stages to the post-DPO menu — and I set the toy DPO lab: train on a small preference dataset, then show the before and after on held-out pairs, measured. By the end you'll choose among DPO, KTO, ORPO, SimPO, and IPO by what data you have — the decision rule, not the hype ranking.",
("il07-frontier", "frontier-finetune"):
"I'm your instructor for this module. In this module I explain the economics in original prose — where the memory actually goes — and I set the fine-tune-and-measure lab: QLoRA on a small open model, with the delta on a fixed eval reported before and after. By the end you'll work full fine-tuning economics, LoRA, and QLoRA, and you'll hold the line that fine-tuning is only real if the eval moved.",
("il07-frontier", "frontier-inference"):
"I'm your instructor for this module. In this module I teach the optimization taxonomy in original prose — bandwidth versus compute, memory versus latency: know which bottleneck you're attacking — and I set the benchmark lab across quantization levels with tokens/sec, VRAM, and quality notes recorded honestly. By the end you'll work quantization, the GGUF format-versus-algorithm distinction, the KV-cache, speculative decoding, and PagedAttention as one coherent story.",
("il07-frontier", "frontier-eval"):
"I'm your instructor for this module. In this module I teach the harness anatomy in original prose and set the run-and-audit lab: run lm-evaluation-harness on a local model, then write a contamination audit of one benchmark. By the end you'll know what a harness does that a benchmark doesn't, treat contamination as the central integrity threat, and read HELM as history — maintenance mode since 2026-06-01 — not current practice.",
("il07-frontier", "frontier-prompt"):
"I'm your instructor for this module. In this module I teach the discipline framework in original prose and set the regression-suite lab: variant prompts scored by an eval, tracked across versions — so 'it feels better' becomes 'it scored better on the suite.' By the end you'll run prompt systems as persistent contracts, calibrate few-shots, use chain-of-thought deliberately, enforce structured output, and budget cost and latency. The prompt is part of the program — test it like one.",
("il07-frontier", "frontier-safety"):
"I'm your instructor for this module. In this module I teach the honest core in original prose — no hype, no invented incidents — and I set the red-team exercise: attack a local model, then write up the failure modes you found, honestly. By the end you'll understand specification gaming, interpretability's limits, dangerous-capability evaluations, and outer versus inner alignment — with the field's open questions stated as open questions.",
("il07-frontier", "frontier-papers"):
"I'm your instructor for this module. In this module I give you the reading guides and the précis template in original prose: one paper, two pages, plus a replication sketch of what you'd need to reproduce it. By the end you'll read papers the way researchers do — claims, method, ablations, limits — across the seminar's full 14-paper list in the path credits.",
("il07-frontier", "frontier-rag-deep"):
"I'm your instructor for this module. In this module I teach the deep-cut method in original prose and set the scored-pipeline lab: build a RAG pipeline and score it with RAGAS — faithfulness, answer relevancy, context metrics. By the end you'll own chunking and indexing strategy, hybrid retrieval and reranking, and context precision and recall — and your pipeline gets a report card.",
("il07-frontier", "frontier-synthesis"):
"I'm your instructor for this module. In this module I write the synthesis essay in original prose and give you the critical-reading checklist — the questions to ask of every release, benchmark claim, and leaderboard before believing any of them. By the end you'll separate hype from documented results, read a model release critically, and hold the through-line from attention to alignment as one story, told straight.",
("il07-frontier", "frontier-capstone"):
"I'm your instructor for this module. In this module I set the capstone rubric: methodological soundness, measurement rigor, reproducibility, limits stated plainly. By the end you'll have reproduced or extended one paper result at small scale — an attention variant, a preference-optimization comparison, a quantization benchmark, or an eval-harness build — written up as claims, method, ablations, limits. The deliverable is a small, honest result: not a breakthrough, a measurement.",
}
