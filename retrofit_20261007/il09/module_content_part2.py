# IL-09 retrofit content — modules 4-7 (part 2 of 2)

MODULES = {}

MODULES["il09-vendor-ai"] = {
    "summary": "Welcome to Module 4 of IL-09, the Adaptive Certification Command. I'm your instructor, and this module maps the AI credential landscape — tiered honestly. Tier 1 is proctored exams (Pearson VUE or PSI, ID-checked, scored): these carry hiring signal. Tier 2 is academy badges (course completion, sometimes assessed): useful learning proof, weak hiring signal. Tier 3 is pilots (limited availability, evolving): interesting, unstable — don't build a career plan on one. Before studying any AI credential, classify it: who proctors it, what the passing standard is, whether employers list it in job posts. The exams move fast — objectives update with model generations — so you always pull the current skills outline from the vendor, never a third-party summary older than six months. The durable core beneath all of them is the same: ML fundamentals (train/validate/test, overfitting, evaluation metrics), LLM concepts (tokens, context, RAG, agents, evaluation), and responsible-AI vocabulary. The technical depth lives in IL-07, IL-16, and IL-17 — this module is the credential map, not the textbook.",
    "notes": [
        {
            "title": "Concepts",
            "body": """- **Tier 1 — proctored exams** — Pearson VUE or PSI delivery, ID-checked, scored with a published passing standard. These carry hiring signal because an employer can trust what "passed" means.
- **Tier 2 — academy badges** — Course completion, sometimes assessed. Useful learning proof, weak hiring signal — present them as learning evidence, not as validated skill.
- **Tier 3 — pilots** — Limited availability, evolving objectives. Interesting, unstable — never build a career plan on one.
- **Skills outline** — The vendor-published topic list for the exam. Vendor AI exams move fast — objectives update with model generations — so always pull the current outline from the vendor, never a third-party summary older than 6 months.
- **Durable core** — The layer beneath every vendor AI exam: ML fundamentals (train/validate/test splits, overfitting, evaluation metrics), LLM concepts (tokens, context windows, RAG, agents, evaluation), and responsible-AI vocabulary. If the vendor outline changes, this core is what transfers.
- **RAG** — Retrieval-Augmented Generation: retrieving relevant documents into the prompt to ground the model's answer in your data, reducing hallucination.
- **AI-900** — Azure AI Fundamentals: describe AI workloads, ML principles, and Azure AI services at concept level. The vocabulary exam — entry point to Microsoft's AI path.
- **AI-102** — Azure AI Engineer Associate: provision and manage Azure AI services; implement vision, language, speech, and search solutions; conversational AI. Hands-on with the portal and SDKs.
- **Microsoft Learn** — Microsoft's source of truth: the AI exams track its modules closely. Study the Learn path for the exam you're targeting.
- **AIF-C01** — AWS AI Practitioner: AI/ML fundamentals, generative AI, Bedrock applications, security and responsible AI on AWS.
- **MLA-C01** — AWS ML Engineer Associate: data engineering for ML, model development, deployment and MLOps on SageMaker and Bedrock.
- **Generative AI Leader** — Google Cloud's strategic, non-technical credential: the "what and why" of generative AI for decision-makers.
- **Professional Machine Learning Engineer** — Google Cloud's deep ML exam: framing, data pipelines, modeling, deployment, MLOps on Vertex AI and Model Garden. The heaviest of the three hyperscalers' ML exams.
- **NCA-GENL** — NVIDIA's Generative AI LLMs credential: LLM concepts, experiment workflows (NeMo, NIM microservices at concept level), responsible AI. The hardware vendor's software credential.
- **Databricks Generative AI Engineer Associate** — Data engineering on the lakehouse, MLflow, serving LLM apps: the credential follows the platform's own workflow.
- **Honest tiering** — These credentials validate *platform workflow fluency*, not research ability. Present them that way on a resume: signal where they genuinely signal.""",
        },
        {
            "title": "Hands-on procedure",
            "body": """The credential-vetting procedure — run it before you spend a single study hour on any AI credential.

1. **Classify the tier.** Who proctors it? Is there a published passing standard? Do employers list it in job posts? Tier 1 proctored → proceed. Tier 2 badge → learning only, no career bet. Tier 3 pilot → watch, don't plan on.
2. **Pull the current skills outline.** From the vendor's own site, today. If the outline references a model generation older than the current one, the outline is stale — find the update.
3. **Map your durable core.** Write the three core columns (ML fundamentals, LLM concepts, responsible AI) and check off what you already own from IL-07/IL-16/IL-17. Study time goes to the gaps, not the whole outline.
4. **Build one small thing per service family.** A RAG app, a Bedrock agent, a Vertex AI pipeline — the exams increasingly test applied judgment, and a built artifact beats ten hours of slide-reading.
5. **Sit a practice gate.** Domain-weighted, 80%+, twice. Fast-moving exams punish crammers: if the gate is red, the objectives moved or you didn't learn — either way, find out before paying the fee.
6. **Present honestly.** On your resume, tier-1 exams are credentials; tier-2 badges are learning proof. Never inflate one into the other.

Cross-link: the technical depth lives in IL-07 (data/AI) and IL-16/IL-17 (ML/agentic AI) — this module is the credential map, not the textbook.""",
        },
        {
            "title": "Project brief",
            "body": """Your capstone: the **AI credential investment memo** — the document you'd write before spending a dollar or an hour.

- Tier table: every AI credential you're considering, classified Tier 1/2/3 with the proctor, passing standard, and evidence of employer demand cited.
- For each Tier 1 target: the current skills outline (vendor-published, dated as-of), the durable-core gaps you need to close, and the one artifact you'll build per service family (RAG app, agent, pipeline).
- Cost and sequence: exam fees, study hours, and the order — with the 6-month freshness rule stated: never study from a third-party summary older than 6 months.
- Honesty clause: what each credential actually validates (platform workflow fluency) and does not (research ability), and how you'll present it on a resume.

Deliverable: the memo, with all as-of dates explicit. Fast-moving claims are dated; undated claims are suspect.""",
        },
        {
            "title": "Noah check-in",
            "body": """Noah probes mastery with questions like:
- Classify this credential: a vendor-published online quiz with a completion badge, no proctoring, no passing standard published. Which tier, and what do you do with it?
- Why is a third-party exam summary older than 6 months dangerous for a vendor AI exam?
- Name the three columns of the durable core, then tell me which one you'd lean on if the vendor rewrites its outline next quarter.
- AI-900 versus AI-102: who is each one actually for? What changes between them?
- RAG stands for what, and what problem does it solve?
- Why do the exams increasingly reward having built one small thing per service family?
- Honesty check: preparation only — Interstitium Labs confers no certificate and is not affiliated with Microsoft, AWS, Google Cloud, NVIDIA, or Databricks. Confirm current exam codes on the vendor sites before booking.""",
        },
    ],
}

MODULES["il09-oracle"] = {
    "summary": "Welcome to Module 5 of IL-09, the Adaptive Certification Command. I'm your instructor, and this module is Oracle's three certification families: Java SE (the language credential — streams, lambdas, modules, virtual threads), Database SQL (queries through DDL/DML), and OCI (the year-versioned cloud program from Foundations to Professional). The official objectives are the topic maps; original code practice is the preparation. Java's 1Z0-830 is 50 questions in 120 minutes at a 68% pass mark — and it loves compilation-failure questions, so you learn to read for what won't compile before evaluating what it prints. Oracle SQL's 1Z0-071 is 63 questions in 120 minutes at 63% — pure SQL fluency under time pressure. And OCI carries year versions (like 1Z0-1085-26): the Foundations exam is free, 40 questions in 60 minutes at 65%, and compartments are the identity boundary every IAM question reduces to.",
    "notes": [
        {
            "title": "Concepts",
            "body": """- **1Z0-830 (Java SE 21 Developer)** — 50 questions, 120 minutes, 68% to pass. The exam tests precise language semantics — code-reading under time pressure. Pacing: 120 ÷ 50 = 2.4 minutes per question; anything that eats more gets flagged.
- **Stream laziness** — Intermediate operations (filter, map, peek) do nothing until a terminal operation (collect, forEach, reduce) executes. Trace stream pipelines mentally, watching for laziness.
- **Collectors & Optionals** — The stream pipeline's finishers: collectors aggregate, Optionals force explicit empty-handling. Know intermediate vs terminal by sight.
- **JPMS (Java Platform Module System)** — module-info.java, requires/exports/opens: know what breaks when a package isn't exported.
- **Virtual threads (Project Loom)** — Thread-per-task becomes viable at scale for I/O-bound work; watch for synchronized blocks pinning carrier threads. Structured concurrency concepts are in scope.
- **PECS** — Producer Extends, Consumer Super: `? extends T` when reading (producer), `? super T` when writing (consumer). Know the type-erasure consequences behind it.
- **NIO.2** — Path/Files APIs, try-with-resources, serialization basics; localization: Locale, ResourceBundle, formatting.
- **Compilation-failure tactic** — The exam's favorite trap: read for what won't compile before evaluating what it prints.
- **1Z0-071 (Oracle Database SQL)** — 63 questions, 120 minutes, 63% to pass. Pure SQL fluency: queries, joins, subqueries, DDL, DML, transaction control.
- **Join-condition vs filter trap** — Filtering the nullable side of an outer join in WHERE converts it to an inner join. Put the filter in the ON clause or lose the outer semantics — a classic trap.
- **Subquery operators** — Single-row (`=`, `<`, `>`) vs multi-row (`IN`, `ANY`, `ALL`); correlated subqueries; EXISTS vs IN (EXISTS stops at the first match and handles NULL semantics cleanly).
- **Set operators** — UNION (distinct) vs UNION ALL (straight concatenation, faster), INTERSECT, MINUS: column count and type compatibility rules.
- **Constraints** — PK, FK, UNIQUE, CHECK, NOT NULL on CREATE/ALTER; INSERT/UPDATE/DELETE, MERGE; transaction control (COMMIT/ROLLBACK/SAVEPOINT).
- **1Z0-171 (Oracle 23ai SQL Associate)** — The newer SQL track. Check which your target role expects before booking 1Z0-071.
- **OCI year-versioning** — OCI certifications carry year versions (e.g., 1Z0-1085-26). Objectives refresh annually: study the current year's guide and schedule before your version retires.
- **OCI Foundations (1Z0-1085)** — 40 questions, 60 minutes, 65% to pass — and the exam itself is free. Domains: core services 50% (compute, storage, networking, databases), security 25% (IAM, compartments, encryption), governance 10%. The cheapest credential in enterprise cloud.
- **Compartments** — The OCI identity boundary: every IAM question reduces to compartment + policy syntax. Policies attach at compartment scope.
- **OCI Professional tracks** — Architect Associate (1Z0-1072): design for HA across availability/fault domains, VCN design, load balancing, data services selection; plus Developer, DevOps, Networking, Security Professional paths.""",
        },
        {
            "title": "Hands-on procedure",
            "body": """The code-tracing drill — language exams are precision instruments, so the preparation is tracing, not reading.

1. **Work the pacing math.** Java: 120 minutes ÷ 50 questions = 2.4 min/question. SQL: 120 ÷ 63 ≈ 1.9 min/question. OCI Foundations: 60 ÷ 40 = 1.5 min/question. Write your per-question budget on the runbook card; anything that eats double gets flagged.
2. **Compilation first.** For every Java snippet: decide compile-or-not before deciding output. The exam loves compilation-failure questions — read for what won't compile first.
3. **Trace by hand.** Write the output on paper before checking: stream pipelines (watch laziness), generics bounds (PECS), try-with-resources closure order. The gap between your trace and the real output is the lesson.
4. **Drill the SQL traps.** Outer-join + WHERE filter (the semantics killer), EXISTS vs IN with NULLs, UNION vs UNION ALL. Write ten of each by hand; speed comes from reps.
5. **Draw the OCI boundary.** For every IAM scenario: name the compartment, write the policy in compartment + resource + action form. If you can't state the boundary, you can't answer the question.
6. **Year-version check.** Before studying OCI: confirm the current year's guide, and schedule before your version retires. Studying a retired year's objectives is donated effort.
7. **Trap log.** Keep a personal log: mutable defaults, PECS direction mistakes, the joins you misread. Review it before every practice set.

The official objectives are the topic maps; this procedure is the preparation.""",
        },
        {
            "title": "Project brief",
            "body": """Your capstone: the **traced-code trap portfolio** and the **OCI compartment design**.

- Trap portfolio: 20 hand-traced snippets (10 Java, 10 SQL) with your predicted output, the actual output, and the rule you extracted — including at least one compilation-failure, one laziness trap, one PECS trap, and one outer-join filter trap.
- OCI compartment design: a fictional company's compartment tree (root, per-environment, per-team), three IAM policies written in compartment + resource + action form, and the year-version you're targeting with its retirement date noted.
- Exam-day runbook: per-question pacing for 1Z0-830, 1Z0-071, and 1Z0-1085, the compilation-first rule, and the 1Z0-071 vs 1Z0-171 decision for your target role.

Deliverable: the portfolio plus the compartment design. Original snippets and designs — never recalled exam content.""",
        },
        {
            "title": "Noah check-in",
            "body": """Noah probes mastery with questions like:
- This stream pipeline has filter → map → peek, and no terminal operation. What executes? Why?
- `List<? super Integer>`: can you safely read Integers from it, write Integers to it, both, or neither? Defend with PECS.
- WHERE filters the nullable side of a LEFT JOIN. What just happened to the join semantics — and where should the filter have gone?
- UNION versus UNION ALL: what does each cost you, and when is ALL the right choice?
- OCI: write the policy that lets a group manage instances in exactly one compartment. What is the authorization boundary in your answer?
- 1Z0-830 pacing: 120 minutes, 50 questions. What's your per-question budget, and what do you do when a question eats double?
- Which SQL exam does your target role expect — 1Z0-071 or 1Z0-171 — and how did you verify?
- Honesty check: preparation only — Interstitium Labs confers no certificate and is not affiliated with Oracle. Confirm current exam codes and year versions on Oracle's site before booking.""",
        },
    ],
}

MODULES["il09-lf-blockchain"] = {
    "summary": "Welcome to Module 6 of IL-09, the Adaptive Certification Command. I'm your instructor, and this module is the Linux Foundation's two live blockchain certifications: HFCP (Hyperledger Fabric Certified Practitioner) and BCP (Besu Certified Professional). Fabric is a permissioned ledger — identity and channels first, tokens never — and HFCP tests it as a system: peers, orderers, channels, the chaincode lifecycle, client applications. Besu is an Ethereum client for permissioned networks, so your Solidity and standard tooling transfer; BCP covers networking, permissioning, privacy, and consensus. Both are 90-minute online proctored multiple-choice exams, and BCP includes two attempts with 2-year validity. This module also carries the retired-exam map — CHFA/CHFD/CHSA performance exams and the Sawtooth curriculum are gone, and studying retired objectives is the most expensive mistake in certification. Taught with a blockchain engineer's lens: these are systems-operations credentials. The exam tests whether you can run the network.",
    "notes": [
        {
            "title": "Concepts",
            "body": """- **HFCP (Hyperledger Fabric Certified Practitioner)** — 90-minute online proctored multiple-choice. Domains: Fabric Networks 36%, Smart Contracts 24%, Client Applications 24%, plus fundamentals.
- **Permissioned ledger** — Fabric's identity-first model: organizations, MSPs, and channels before anything else. Identity and channels first, tokens never.
- **Peers** — Endorse transactions (execute chaincode) and commit blocks to the ledger.
- **Orderers** — Run the consensus service (Raft) and cut blocks. In Fabric, orderers order; peers endorse and commit — never mix the roles.
- **Channels** — Private subnets of the ledger: only member organizations see a channel's data.
- **Organizations / MSPs** — Membership Service Providers: the identity layer that decides who belongs to the network.
- **Transaction flow** — Propose → endorse (chaincode execution) → order → validate → commit. Know which node does what at each step.
- **Chaincode lifecycle** — Package → install → approve (per organization) → commit (channel). The governance is the point: no single org can deploy unilaterally.
- **Client applications** — Fabric SDKs, the Gateway service, submitting vs evaluating transactions; private data collections for selective privacy.
- **LFS272** — The LF's own Fabric course material: aligned prep, but study the current exam domains, not any single course's table of contents.
- **BCP (Besu Certified Professional)** — 90-minute online proctored multiple-choice; two attempts included; valid 2 years. Domains: Networking 26%, Core Concepts 24%, then permissioning, privacy, consensus.
- **Ethereum client** — Besu is an Ethereum client for permissioned networks: EVM compatibility means Solidity and standard tooling transfer.
- **Node discovery** — discv4/dns discovery, bootnodes, static nodes: how a permissioned network actually forms.
- **Permissioning** — Node and account permissioning via on-chain contracts: who may join, who may transact.
- **Tessera / privacy groups** — Private transactions: private payloads alongside public state — the enterprise privacy pattern.
- **QBFT/IBFT vs Ethash** — Proof-of-authority BFT consensus (immediate finality, no mining) vs proof-of-work. Know the finality and fault-tolerance trade-offs.
- **Two-attempt strategy** — Two attempts included changes strategy: sit the first as a calibrated diagnostic if you're borderline-ready.
- **Retired: CHFA/CHFD/CHSA** — The old performance-based exams are gone, along with the Sawtooth curriculum (LFS273/LFD272). Do not build study plans on these.
- **Verification habit** — Before starting ANY certification, confirm it exists on the issuer's site today. Programs sunset quietly.
- **Systems-operations lens** — Taught with a blockchain engineer's lens: the exam tests whether you can run the network, not whether you can hype it.""",
        },
        {
            "title": "Hands-on procedure",
            "body": """The systems-operator's study sequence — learn each network as a machine you will run, not a whitepaper you will quote.

**HFCP sequence:**
1. **Draw the network.** Three orgs, two channels, peers and an ordering service. Label every node with its role: endorse, order, commit. If you can't draw it, you don't know it.
2. **Walk a transaction.** Propose → endorse → order → validate → commit. At each step, name the node type acting and the artifact it produces.
3. **Run the chaincode lifecycle.** Package → install → approve (per org) → commit (channel). Say out loud why approval is per-organization — the governance is the point.
4. **Submit vs evaluate.** Write the difference: evaluation reads, submission writes. Private data collections: who sees what.
5. **Domain-weight the reps.** Fabric Networks 36% gets the most hours; fundamentals get the fewest. Study by weight.

**BCP sequence:**
1. **Form the network.** Bootnodes, static nodes, discovery (discv4/dns): narrate how a permissioned network bootstraps from zero.
2. **Permission it.** Node permissioning, account permissioning: who may join, who may transact — and the on-chain contracts that enforce it.
3. **Make it private.** Tessera/privacy groups: draw public state vs private payload. Know the enterprise pattern by heart.
4. **Choose consensus.** QBFT/IBFT vs Ethash: finality and fault-tolerance trade-offs, stated as engineering decisions.
5. **Use the two attempts.** Borderline-ready? Sit attempt one as a calibrated diagnostic, then close the gaps and sit attempt two. The format is part of the strategy.

**Both:** verify the exam exists on the LF site before starting. Retired objectives are the most expensive mistake in certification.""",
        },
        {
            "title": "Project brief",
            "body": """Your capstone: the **Fabric-vs-Besu evaluation dossier** — the document you'd hand a CTO choosing a permissioned platform.

- Platform profiles: Fabric (channels, chaincode lifecycle, Raft ordering, MSP identity) and Besu (EVM compatibility, privacy groups, QBFT/IBFT, permissioning) — each as a systems operator would describe it: what runs, what can break, what it costs to operate.
- Decision matrix: three fictional enterprise scenarios (multi-org supply chain, regulated financial ledger, internal audit trail) with a platform recommendation and the consensus/privacy/identity reasoning behind each.
- Certification plan: HFCP then BCP (or the reverse — defend your order), domain-weighted study maps, the two-attempt BCP strategy, and the verification habit documented (issuer-site check dated).
- Retired-exam appendix: what not to build toward (CHFA/CHFD/CHSA, Sawtooth LFS273/LFD272) and why.

Deliverable: the dossier. Systems-operations thinking throughout — the exam tests whether you can run the network.""",
        },
        {
            "title": "Noah check-in",
            "body": """Noah probes mastery with questions like:
- In Fabric, which node type orders transactions — and what would break if a peer tried to do it?
- Walk the transaction flow: propose → endorse → order → validate → commit. At each step, which node acts and what does it produce?
- Why is chaincode approval per-organization? What attack does that governance prevent?
- Channels versus private data collections: when do you use each for privacy?
- Besu: how does a permissioned network form from zero — bootnodes, discovery, then what?
- QBFT versus Ethash: what changes about finality, and why does that matter to an enterprise ledger?
- You're borderline-ready for BCP and it includes two attempts. What's your strategy — and why is it different from a single-attempt exam?
- Before you start studying, what's the one verification step — and which retired exams make it necessary?
- Honesty check: preparation only — Interstitium Labs confers no certificate and is not affiliated with the Linux Foundation. Confirm HFCP and BCP are live on the LF site before booking.""",
        },
    ],
}

MODULES["il09-cpp-python"] = {
    "summary": "Welcome to Module 7 of IL-09, the Adaptive Certification Command. I'm your instructor, and this module is the language-vendor credentials: the C++ Institute's CPE → CPA → CPP ladder (plus the C branch: CLE/CLA/CLP) and the Python Institute's PCEP → PCAP → PCPP1 → PCPP2 ladder, with OpenEDG's free aligned courses as the study backbone. Language exams test precision — one character changes the answer — so this module trains the precision habit: trace every snippet by hand, write the output before checking, and keep a trap log. CPE-20-01 is entry at 70% to pass, CPA-21-02 is the associate depth (OOP, STL, templates basics, exceptions), CPP-22-02 is professional. On the Python side, PCEP is the vocabulary, PCAP-31-03 is the associate (modules, OOP, exceptions, generators, closures, decorators), and PCPP1/PCPP2 are the professional tiers. The exam style is predict-the-output with subtle distractors — mutable default args, late-binding closures, the most vexing parse. This module is the credential map and the exam-tactic layer over IL-03's programming depth.",
    "notes": [
        {
            "title": "Concepts",
            "body": """- **CPE-20-01** — C++ Certified Entry-Level Programmer: entry rung, 70% to pass. Basics: types, operators, control flow, functions, pointers at introduction level.
- **CPA-21-02** — C++ Certified Associate Programmer: the associate depth — OOP (classes, inheritance, polymorphism, virtual), templates basics, STL containers/algorithms, exception handling.
- **CPP-22-02** — C++ Certified Professional Programmer: professional tier — advanced templates, STL mastery, concurrency basics, idioms and best practices.
- **CLE / CLA / CLP** — The C branch mirroring the ladder for C itself: entry, associate, professional. Useful for embedded/systems roles where C++ is overkill.
- **Most vexing parse** — `Widget w();` declares a FUNCTION, not an object. Use `Widget w{};` or `Widget w;`. The exam's favorite C++ declaration trap.
- **Undefined behavior** — Sequence-point and lifetime rules: UB questions punish guessers. Know the rules cold; never reason from "it worked on my machine."
- **PCEP** — Python Certified Entry-Level Programmer: the vocabulary of Python — literals, operators, control flow, functions, basic data structures.
- **PCAP-31-03** — Python Certified Associate Programmer: modules/packages, OOP, exceptions, string and file processing, generators/closures/decorators at associate depth.
- **PCPP1** — Professional tier 1: advanced OOP (metaclasses, descriptors), networking (sockets), GUI basics, design patterns in Python.
- **PCPP2** — Professional tier 2: file processing depth, database/SQLite, numerical/scientific basics, best practices and PEP conventions.
- **OpenEDG** — Publishes free courses aligned to each Python Institute and C++ Institute exam: the legitimate study backbone. Sufficient alongside the official exam syllabi.
- **Mutable default argument** — `def f(x=[]):` — the list is created ONCE at def time; mutations persist across calls. The classic Python trap.
- **Late-binding closures** — Loop variables bind late in lambdas: `[lambda: i for i in range(3)]` gives three functions that all see the final value 2. Capture with a default argument.
- **Integer caching** — CPython caches small ints (−5..256): identity comparisons on them can surprise. Know the range; never rely on `is` for value equality.
- **Trap log** — Your personal ledger of every trap that caught you: mutable defaults, except-clause ordering, most-vexing-parse, dangling references, late binding. Reviewed before every practice set.
- **Precision habit** — Language exams are precision instruments: the preparation is tracing, not reading.""",
        },
        {
            "title": "Hands-on procedure",
            "body": """The precision-tracing drill — the only procedure that works on predict-the-output exams.

1. **Read the snippet twice.** First pass: what does it claim to do. Second pass: character by character — the exam's distractors live in single characters (`[]` vs `()`, `is` vs `==`, `w()` vs `w{}`).
2. **Classify the trap family.** Is it a lifetime trap (dangling reference, mutable default)? A binding trap (late-binding closure, PECS direction)? A parse trap (most vexing parse)? Naming the family routes you to the rule.
3. **Write the output before checking.** On paper, not in your head: the exact output, or "compilation failure" / exception type with the line. The gap between your trace and reality is the lesson.
4. **Trace the machine, not the intent.** For C++: object lifetimes, sequence points, overload resolution. For Python: name resolution order, evaluation time of defaults, closure cell contents.
5. **Log every miss.** Each wrong trace goes in the trap log with the rule restated in your own words. The log is reviewed before every practice set — it is the highest-value study artifact you own.
6. **Run the OpenEDG labs.** The free aligned courses include exercises: do them from the starter, not by reading the solution. Code you typed teaches; code you read doesn't.
7. **Gate by ladder rung.** PCEP before PCAP, CPA before CPP. Each rung's practice set at 80%+ twice before the voucher is bought.

Cross-link: IL-03's Programming Backbone is the deep study behind these exams — this module is the credential map and the exam-tactic layer.""",
        },
        {
            "title": "Project brief",
            "body": """Your capstone: the **trap-log portfolio** — the precision instrument you'd carry into the exam and the interview.

- 24 hand-traced snippets (12 C++, 12 Python) at your target rung: predicted output written before checking, actual output, and the rule extracted — with at least one most-vexing-parse, one mutable-default, one late-binding closure, one PECS/lifetime, and one undefined-behavior trap.
- The trap log itself: every miss from your practice, each with the rule restated in your own words, organized by trap family.
- Ladder plan: your rung (CPE → CPA → CPP or PCEP → PCAP → PCPP1 → PCPP2), the OpenEDG courses mapped per rung, and the 80%-twice gate rule before each voucher purchase.
- One honest page: what the credential validates (language precision at the rung's depth) and what it doesn't.

Deliverable: the portfolio and the log. Original snippets — never recalled exam content.""",
        },
        {
            "title": "Noah check-in",
            "body": """Noah probes mastery with questions like:
- `def f(x=[]): x.append(1); return x` — call it twice. What prints, and why does the second call see the first call's mutation?
- In C++, `Widget w();` — object or function? Fix it two ways.
- `[lambda: i for i in range(3)]`, then call each: what do you get, and what single change captures the value at creation?
- Trace this without running it: a list comprehension with a conditional filter over a generator that raises on the third item. Where does it fail?
- CPA vs CPP: what depth separates the associate from the professional on the C++ ladder?
- PCAP-31-03: name the associate-depth topics that PCEP doesn't cover.
- What's in your trap log this week, and which family keeps catching you?
- Honesty check: preparation only — Interstitium Labs confers no certificate and is not affiliated with the C++ Institute or the Python Institute. Confirm current exam codes on the institutes' sites before booking.""",
        },
    ],
}
