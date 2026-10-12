# IL-31 modules part 2: M02 (prompt injection taxonomy), M03 (evals design), M04 (METR), M05 (agent evals)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *

M02 = module(
    id_="IL31-M02",
    title="Prompt Injection & Jailbreak Taxonomy (Defensive Framing)",
    summary="The published attack-class taxonomy for prompt-level threats — taught so you can recognize, test for, and defend against each class, never to wield them.",
    objectives=[
        "Classify prompt attacks by published taxonomy: direct injection, indirect injection, jailbreaks, and multi-turn coercion.",
        "Describe, for each class, how an EVALUATOR detects it and how a DEFENDER mitigates it.",
        "Explain the instruction hierarchy (system > developer > user > tool output) and why it matters for defense.",
        "Design a defensive test battery: one probe family per attack class, scored by a published-style rubric.",
        "State the professional boundary: no working attack payloads, no exploit writeups — detection and mitigation only.",
    ],
    estimatedMinutes=420,
    weight=8,
    prerequisiteFor=["IL31-M03", "IL31-M05", "IL31-M06"],
    crossLinks=[
        {"course": "il-17-agentic-ai-engineering", "moduleId": None, "topic": "Tool-use architecture", "why": "Indirect injection lands through tool outputs — you must understand the tool layer to defend it."},
        {"course": "il-06-cybersecurity-secure-engineering", "moduleId": None, "topic": "Injection as a vulnerability class", "why": "Prompt injection is the AI analogue of SQL/command injection — same trust-boundary thinking."},
    ],
    cards=[
        card("Direct vs indirect prompt injection.",
             "Direct: the attacker types the malicious instruction into the prompt. Indirect: the instruction arrives via data the model reads — a web page, document, tool result, or pasted content. Defenses differ: direct is filtered at input; indirect requires data provenance and trust tiers."),
        card("What is a jailbreak, precisely?",
             "An input crafted to make the model violate its own safety policy — bypassing refusal behavior. Evaluators measure jailbreak SUCCESS RATE per attack class; defenders measure it as the metric their mitigations must drive down."),
        card("Name four published jailbreak families (categories, not payloads).",
             "1) Roleplay/persona reframing ('pretend you are...'). 2) Encoding/obfuscation (base64, translation, leetspeak). 3) Multi-turn gradual escalation (foot-in-the-door across turns). 4) Instruction-hierarchy confusion (forged 'system' messages). Each is a TEST CATEGORY, not a recipe."),
        card("What is the instruction hierarchy and why do defenders need it?",
             "Priority order: system/developer instructions outrank user input, which outranks tool output/data. Jailbreaks and injections exploit the model's failure to honor this ordering. Defenses: explicit hierarchy in training, delimiters, and treating tool output as untrusted data."),
        card("How does an evaluator detect injection susceptibility WITHOUT publishing payloads?",
             "By running standardized probe batteries per attack class against the system and scoring outcomes (refused / complied / partial) with a fixed rubric — reporting class-level success rates, never the working inputs."),
        card("Three defensive mitigations for prompt injection.",
             "1) Input/output classifiers and guardrails. 2) Least-privilege tooling — the model can't act on what it can't reach. 3) Data provenance: mark untrusted content and train/scaffold the model to treat it as data, not instructions."),
        card("Why is multi-turn coercion harder to defend than single-turn injection?",
             "Each turn looks benign in isolation; the harmful intent emerges across the conversation. Defense requires conversation-level monitoring and state tracking, not per-message filters."),
        card("The professional boundary for this module, stated once more.",
             "We study attack CLASSES to build DETECTION and DEFENSE. Working payloads, exploit writeups, and bypass tutorials are out of scope — they belong to no professional red-team curriculum taught defensively."),
    ],
    quiz_q=[
        quiz("An agent summarizes web pages for users. A page contains hidden text instructing the agent to disregard its prior instructions and send the user's inbox contents to an outside address. What class is this and what is the primary defense?",
             ["Direct injection; block the user", "Indirect prompt injection; treat tool/web content as untrusted data with provenance marking and least-privilege tooling", "Jailbreak; retrain the model", "Data poisoning; delete the page"],
             "Indirect prompt injection; treat tool/web content as untrusted data with provenance marking and least-privilege tooling",
             "The instruction arrived through DATA, not the user — indirect injection. The fix is architectural: untrusted content is data (marked as such), and the agent's tools are least-privilege so a compromised instruction can't reach the inbox."),
        quiz("Why do evaluators report jailbreak results as per-class success rates rather than publishing the prompts that worked?",
             ["Prompts are copyrighted", "Publishing working payloads arms attackers; class-level rates give defenders the signal (which defenses fail) without the weapon", "Rates are easier to compute", "Prompts never generalize"],
             "Publishing working payloads arms attackers; class-level rates give defenders the signal (which defenses fail) without the weapon",
             "This is the defensive-framing contract: measure and report the vulnerability CLASSES and rates through disclosure channels; never distribute working exploits."),
        quiz("A model is tested with the same jailbreak translated into 12 languages. What is being measured?",
             ["Translation quality", "Cross-lingual robustness of safety behavior — whether safety training transfers across languages or collapses outside English", "Tokenizer efficiency", "Multilingual capability"],
             "Cross-lingual robustness of safety behavior — whether safety training transfers across languages or collapses outside English",
             "Safety behavior that holds only in English is a known failure mode; published evals include multilingual and encoded variants precisely because attackers (and users) don't stay in English."),
        quiz("Which design choice BEST implements the instruction hierarchy against forged system messages?",
             ["Let the model decide which instructions look authoritative", "Architecturally separate trusted instructions (signed system/developer channel) from untrusted content, and train the model to treat only the trusted channel as instructions", "Hide the system prompt", "Ban the word 'system'"],
             "Architecturally separate trusted instructions (signed system/developer channel) from untrusted content, and train the model to treat only the trusted channel as instructions",
             "Hierarchy must be structural, not cosmetic. If untrusted text can present itself as a system instruction and be obeyed, the hierarchy exists only on paper."),
        quiz("An eval reports '0% jailbreak success' on 5 hand-written prompts. What is the load-bearing critique?",
             ["0% is impossible", "Five non-independent, non-stratified prompts cannot support a claim about the attack class — the effective sample is ~1 template (M00)", "Hand-written prompts are invalid", "The model must be cheating"],
             "Five non-independent, non-stratified prompts cannot support a claim about the attack class — the effective sample is ~1 template (M00)",
             "M00's lesson applied: correlated probes measure the probe, not the class. A serious battery stratifies across attack families with independent items per family."),
    ],
    drills=[
        drill("il31-m02-drill1", [
            drillitem("Direct vs indirect injection: one-sentence distinction.", "Direct arrives in the user's own input; indirect arrives via data/tool output the system reads.", "The defense boundary differs: input filtering vs data provenance."),
            drillitem("Name the four jailbreak families (categories only).", "Roleplay reframing; encoding/obfuscation; multi-turn escalation; hierarchy confusion.", "Categories, never payloads."),
            drillitem("State the instruction hierarchy top to bottom.", "System/developer instructions > user input > tool output / retrieved data.", "Anything below the top tier is untrusted data by default."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m02-lab",
        title="Build a defensive probe battery (no payloads)",
        brief="Design — not execute attacks for — a class-stratified injection test battery for a support chatbot, with scoring rubric and reporting template.",
        steps=[
            "Define 6 attack classes (direct, indirect via doc, indirect via tool result, roleplay, encoded, multi-turn).",
            "For each class write 3 probe SPECIFICATIONS: what the probe tests and the expected safe behavior — never the working text.",
            "Write a 3-level scoring rubric: refused-and-safe / refused-but-leaky / complied (with examples of what each looks like).",
            "Specify the reporting format: per-class success rates, confidence intervals, and a threats-to-validity note.",
            "Draft the disclosure paragraph: who receives the results and under what timeline (feeds M09).",
        ],
        checkpoint="Your battery has 6 classes × 3 probe specs, a rubric, a reporting template, and zero working payloads.",
        deliverable="Probe-battery specification document + scoring rubric, ready to hand to an authorized test team.",
    ),
    mockTask=mocktask(
        id_="il31-m02-mock",
        q="A colleague asks you to share 'the exact prompts that bypassed the filter' so their team can 'test too.' Professional response?",
        choices=["Share them; testing is testing", "Decline to distribute working payloads; share the class taxonomy, the per-class rates, and the disclosure-channel process instead", "Share only the easy ones", "Post them in the team wiki"],
        answer="Decline to distribute working payloads; share the class taxonomy, the per-class rates, and the disclosure-channel process instead",
        explain="Working payloads are dual-use artifacts. Professional practice shares the measurement (classes, rates, rubric) and routes the payloads through coordinated disclosure to the party that can fix them.",
    ),
    videos=[
        video("Briefing: why indirect injection is the agent-era threat", "https://scienmag.com/unchaotic-agents-why-ai-failures-may-be-a-design-problem-not-a-technology-problem/", "ScienMag (AI & Society forum coverage)", "How agents with tools, memory, and live environments fail — the empirical backdrop for why injection classes matter at the tool layer.", 15, 1),
        video("Briefing: Anthropic's tiered defensive access (Red Team tier)", "https://badsignal.ai/stories/anthropic-cyber-verification-tiers", "Bad Signal (Oct 2026)", "How the CVP's Red Team Access tier vets professionals for authorized testing — the authorized context for probing attack classes.", 20, 2),
    ],
    pdfs=[
        mkpdf("Injection Taxonomy — Visual Guide", "Direct, indirect, jailbreak families, multi-turn — the class tree with evaluator detection notes.", pages=10),
        mkpdf("Instruction Hierarchy — Visual Guide", "System > developer > user > tool output: the ordering and how each layer is defended.", pages=8),
    ],
    notes=[
        {"title": "Taxonomy before technique", "body": (
            "Security matured when it stopped cataloguing individual exploits and started classifying vulnerability CLASSES — buffer overflows, injection, privilege "
            "escalation — because classes are what defenses are built against. Prompt-level threats need the same discipline. The published taxonomy has four "
            "branches. Direct injection: malicious instructions in the user's own input. Indirect injection: instructions smuggled through data the system reads — "
            "web pages, documents, tool results, retrieved passages. Jailbreaks: inputs engineered to defeat the model's safety policy itself, in families like "
            "roleplay reframing, encoding/obfuscation, multi-turn escalation, and hierarchy confusion. Multi-turn coercion: harmful intent assembled across turns, "
            "each benign alone. Learn the tree cold. Every defensive battery in this course is stratified across it, and every finding you ever write will be filed "
            "under one of its branches."
        )},
        {"title": "How evaluators test without arming attackers", "body": (
            "The defensive contract of this module: we measure susceptibility, we never distribute capability. In practice this means probe batteries are specified "
            "by CLASS with fixed scoring rubrics (refused / refused-but-leaky / complied), results are reported as per-class success rates with confidence intervals, "
            "and the working inputs travel only through coordinated disclosure to the vendor. This is not squeamishness — it is the same norm that governs "
            "vulnerability research in traditional security: you may prove the flaw exists, you report it to the party that can fix it, and you do not publish the "
            "weapon. An evaluator who posts working jailbreaks for likes has left the profession. Your labs in this module produce specifications, rubrics, and "
            "reports — artifacts a CISO can act on — and contain zero payloads by design."
        )},
        {"title": "The defenses, layered", "body": (
            "No single fix covers the taxonomy; defense is layered. At the model layer: safety training that honors the instruction hierarchy and refuses "
            "gracefully. At the input layer: classifiers and guardrails that catch known attack shapes (knowing they are bypassable — defense in depth, not a wall). "
            "At the data layer: provenance marking — untrusted content is labeled as data and the system is scaffolded to treat it as such, never as instructions. "
            "At the tool layer: least privilege — the agent cannot exfiltrate through a tool it cannot reach, so injection that 'succeeds' at the text level dies at "
            "the action level. At the conversation layer: state tracking and conversation-level monitoring for multi-turn coercion. At the organizational layer: "
            "monitoring, incident response, and the disclosure pipeline from M09. When you write a finding, you recommend against this stack — which layer failed, "
            "which layer should have caught it."
        )},
    ],
)

M03 = module(
    id_="IL31-M03",
    title="Evals Design: Capability vs Safety vs Alignment Evals",
    summary="The design discipline: what makes an eval valid, the three eval families, and how to write an eval plan that survives contact with reality.",
    objectives=[
        "Distinguish capability evals, safety evals, and alignment evals by the question each answers.",
        "Write a complete eval plan: construct, tasks, scoring, baselines, n, analysis, threats to validity.",
        "Explain construct validity and why 'the benchmark measures X' is a claim that needs evidence.",
        "Design scoring rubrics: automated graders, model judges, and human grading — with their failure modes.",
        "Name the standard validity threats: contamination, grader gaming, task-distribution shift, Goodhart effects.",
    ],
    estimatedMinutes=420,
    weight=8,
    prerequisiteFor=["IL31-M04", "IL31-M05", "IL31-M10", "IL31-M14"],
    crossLinks=[
        {"course": "il-23-frontier-knowledge", "moduleId": "m23-metr-evals", "topic": "Reading a capability eval critically", "why": "M04 dissects RE-Bench as a worked example of the design principles taught here."},
    ],
    cards=[
        card("Capability vs safety vs alignment evals — the one-line distinction.",
             "Capability: CAN the system do X? (upper bound of ability). Safety: DOES it avoid harm under Y conditions? (behavioral guardrails). Alignment: does it pursue the INTENDED goals, not just the scored ones? (objectives, not just outputs)."),
        card("What is construct validity, and why do eval engineers obsess over it?",
             "Whether the eval actually measures the thing it claims to measure. A benchmark can be perfectly reproducible and still invalid — e.g., a 'reasoning' test solvable by pattern matching. Validity is argued with evidence, never assumed."),
        card("Name the five parts of a complete eval plan.",
             "1) Construct + the deployment question it answers. 2) Task suite (stratified, versioned). 3) Scoring rubric (grader type + failure modes). 4) Baselines and n (power analysis, M00). 5) Threats to validity, stated in writing."),
        card("Three grader types and each one's characteristic failure.",
             "Automated checks: brittle, gameable by format hacks. Model-as-judge: cheaper, but inherits the judge's biases and can be gamed. Human grading: gold standard for judgment tasks, but expensive, slow, and needs inter-rater agreement measurement."),
        card("What is grader gaming (a.k.a. reward hacking the eval)?",
             "The system under test learns to satisfy the GRADER rather than the task — e.g., verbose answers that flatter a model-judge, or keyword stuffing that trips automated checks. Defenses: hidden rubrics, adversarial grading, human spot-checks."),
        card("Goodhart's law, eval edition.",
             "'When a measure becomes a target, it ceases to be a good measure.' Once a benchmark is a leaderboard, training optimizes for the benchmark — contamination, overfitting to the suite, and score inflation follow. Rotate suites and keep test items private."),
        card("Why do safety evals need ADVERSARIAL task design?",
             "Safety is about worst-case behavior under motivated probing, not average-case helpfulness. A safety eval that only asks nicely measures politeness, not safety — red-team-style adversarial tasks are the instrument."),
        card("What belongs in the 'threats to validity' section?",
             "Everything that could make the result misleading: contamination risk, grader weaknesses, suite coverage gaps, baseline quality, infrastructure effects, and what the eval explicitly does NOT claim."),
    ],
    quiz_q=[
        quiz("A lab reports 'our model scores 92% on SafetyBench, therefore it is safe to deploy in hospitals.' What is the load-bearing flaw?",
             ["92% is too low", "A benchmark score is evidence about the benchmark's construct, not a deployment safety certificate — validity, coverage, and the deployment's threat model decide, not the number", "SafetyBench is not real", "Hospitals don't use AI"],
             "A benchmark score is evidence about the benchmark's construct, not a deployment safety certificate — validity, coverage, and the deployment's threat model decide, not the number",
             "Scores inform deployment decisions; they do not make them. The eval engineer asks: what construct, what coverage, what validity evidence — and what does the deployment's threat model (M01) demand beyond this suite?"),
        quiz("You must choose a grader for 10,000 open-ended agent trajectories. The budget allows human grading of 200. Best practice?",
             ["Grade all 10,000 with a model judge and report the number", "Use a model judge for scale PLUS human grading on a stratified 200-sample with inter-rater agreement, and report judge-vs-human agreement as a validity check", "Skip grading; use vibes", "Grade 200 and extrapolate silently"],
             "Use a model judge for scale PLUS human grading on a stratified 200-sample with inter-rater agreement, and report judge-vs-human agreement as a validity check",
             "Hybrid grading is the professional standard: scale from automation, validity from humans, and the agreement rate between them reported honestly as a limitation."),
        quiz("Which change BEST hardens an eval against Goodhart effects?",
             ["Publish the full test set for transparency", "Keep test items private, rotate suite versions, and track a held-out canary set that detects training on the eval", "Make the benchmark easier", "Add more multiple-choice questions"],
             "Keep test items private, rotate suite versions, and track a held-out canary set that detects training on the eval",
             "Transparency of METHOD plus privacy of ITEMS: publish the design, the rubric, and the versioning — but not the test items. METR keeps much of its suite private for exactly this reason."),
        quiz("An eval plan lists tasks and a grader but no baselines and no n. What is missing, functionally?",
             ["Nothing; baselines are optional", "The comparison that gives the score meaning (human or prior-system baseline) and the sample size that gives the result statistical standing (M00 power analysis)", "A logo", "More tasks"],
             "The comparison that gives the score meaning (human or prior-system baseline) and the sample size that gives the result statistical standing (M00 power analysis)",
             "A score without a baseline is a number without a referent; a score without a powered n is a number without standing. Both are required before the first run."),
        quiz("Capability eval vs safety eval: which asks 'can it' and which asks 'does it avoid harm'?",
             ["Capability asks 'can it do X' (upper bound); safety asks 'does it avoid harm under adversarial conditions' (behavioral guardrails)", "They are the same", "Safety evals measure speed", "Capability evals are only for robots"],
             "Capability asks 'can it do X' (upper bound); safety asks 'does it avoid harm under adversarial conditions' (behavioral guardrails)",
             "Confusing them is a classic failure: a high capability score says nothing about safety, and a clean safety suite says nothing about capability. Deployment needs both, plus alignment evidence."),
    ],
    drills=[
        drill("il31-m03-drill1", [
            drillitem("Capability vs safety vs alignment: one line each.", "Capability: can it do X? Safety: does it avoid harm under Y? Alignment: does it pursue intended goals?", "Three questions, three eval families."),
            drillitem("Name the five eval-plan parts.", "Construct+question; task suite; scoring rubric; baselines+n; threats to validity.", "Write them before running anything."),
            drillitem("State Goodhart's law for evals.", "When a benchmark becomes a target, training optimizes for it and the score stops measuring the construct.", "Private items + rotation are the defense."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m03-lab",
        title="Write a full eval plan for a refusal eval",
        brief="Produce a professional eval plan document for testing whether a customer-support agent refuses disallowed refund-fraud requests.",
        steps=[
            "State the construct and the deployment question in one paragraph each.",
            "Stratify the task suite: 4 request families × difficulty levels; specify n per cell with a power justification (M00).",
            "Choose the grader stack: automated refusal classifier + human spot-check protocol with inter-rater agreement target.",
            "Name two baselines: the current production system and a human-agent reference.",
            "Write the threats-to-validity section: contamination, grader gaming, coverage gaps — at least five bullets.",
            "Add the versioning block: suite version, model checkpoint, harness commit, seed, date.",
        ],
        checkpoint="Your plan is a self-contained document another engineer could execute without asking you questions.",
        deliverable="Eval plan document (the template you will reuse in M10 and the M14 capstone).",
    ),
    mockTask=mocktask(
        id_="il31-m03-mock",
        q="A benchmark claims to measure 'general reasoning' but all items are solvable by retrieving memorized facts. The validity problem is:",
        choices=["Low reliability", "Poor construct validity — the items measure recall, not reasoning, regardless of reproducibility", "Small sample size", "Bad marketing"],
        answer="Poor construct validity — the items measure recall, not reasoning, regardless of reproducibility",
        explain="Reliability (reproducibility) without validity is precise measurement of the wrong thing. Construct validity is argued from item design, ablations, and correlation with independent measures — never from the score alone.",
    ),
    videos=[
        video("Audio briefing: reviewing RE-Bench results with METR", "https://www.cognitiverevolution.ai/can-ais-do-ai-r-d-reviewing-rebench-results-with-neev-parikh-of-metr/", "Cognitive Revolution (podcast)", "A worked example of eval-design critique: baselines, scoring, and what the numbers do and don't show.", 75, 1),
        video("Paper briefing: Measuring AI Ability to Complete Long Tasks", "https://arxiv.org/abs/2503.14499", "arXiv:2503.14499", "How a serious eval paper documents suite, baselines, analysis, and limitations — your template for M14.", 45, 2),
    ],
    pdfs=[
        mkpdf("Eval Design Canvas — Visual Guide", "The five-part eval plan as a one-page canvas: construct, suite, scoring, baselines, validity.", pages=8),
        mkpdf("Grader Stacks — Visual Guide", "Automated, model-judge, human: cost/validity tradeoffs and the hybrid pattern.", pages=8),
    ],
    notes=[
        {"title": "The three eval families", "body": (
            "Every eval answers one of three questions. Capability evals ask 'can the system do X?' — they measure the upper bound of ability on a task family, "
            "usually against human baselines. RE-Bench is a capability eval: can agents do ML research engineering? Safety evals ask 'does the system avoid harm "
            "under adversarial conditions?' — they probe refusal behavior, injection resistance, and dangerous-capability boundaries with adversarial task design. "
            "Alignment evals ask the hardest question: 'is the system pursuing the intended goals, or just scoring well?' — they look for deception, sycophancy, "
            "reward hacking, and goal misgeneralization. The families are complementary and non-substitutable: a brilliant capability score is not safety evidence, "
            "and a clean safety suite is not alignment evidence. Deployment decisions need all three, and the eval engineer must be able to say which family each "
            "number belongs to."
        )},
        {"title": "Validity is the whole game", "body": (
            "An eval is an argument, and validity is whether the argument holds. Construct validity: does the suite measure the claimed property? Content validity: "
            "does it cover the property's range (difficulty strata, domains, edge cases)? Criterion validity: do scores predict anything outside the suite — "
            "deployment incidents, human judgments? Threats to validity are the standard enemies: contamination (test items in training), grader gaming (optimizing "
            "for the judge), distribution shift (the suite no longer resembles deployment), and Goodhart effects (the leaderboard becomes the target). The "
            "professional habit is to write the threats-to-validity section BEFORE running the eval, when you can still fix the design, and to publish it WITH the "
            "results, when it costs you the most. That asymmetry is the point — it is what makes the numbers trustworthy."
        )},
        {"title": "Scoring: the grader is part of the instrument", "body": (
            "A score is produced by a grader, and the grader is part of the measurement instrument — its failure modes are your error bars. Automated checks are "
            "cheap and deterministic but brittle: they grade format, not understanding, and systems learn to game them. Model-as-judge scales to thousands of "
            "trajectories but inherits the judge model's biases and can be flattered by verbosity or style mimicry; always calibrate the judge against human grades "
            "on a stratified sample and report the agreement rate. Human grading is the gold standard for judgment-heavy tasks but demands inter-rater agreement "
            "metrics (Cohen's kappa or equivalent), blind grading where feasible, and serious cost. The professional stack is hybrid: automated for scale, model "
            "judge for triage, humans for the validity anchor — with every layer's limitations in the report."
        )},
    ],
)

M04 = module(
    id_="IL31-M04",
    title="METR Methodology: RE-Bench, Time Horizons, Responsible Scaling",
    summary="The canonical measurement program: RE-Bench's design, the task-time-horizon method, the published doubling trend — and a critical reading of what the metric does and doesn't claim.",
    objectives=[
        "Describe RE-Bench: 7 open-ended ML research-engineering tasks, calibrated human baselines, incremental scoring.",
        "Explain the X%-task-completion time horizon: definition, logistic fit, 50% vs 80% variants.",
        "State the published trend (doubling ~7 months, 2019–2025; post-2023 acceleration per TH1.1) with correct attribution.",
        "List METR's own stated limits: >16h measurements unreliable, suite-specific, task difficulty not sustained autonomy.",
        "Critique a time-horizon claim the way M00 taught: baselines, suite composition, infrastructure effects.",
    ],
    estimatedMinutes=360,
    weight=8,
    prerequisiteFor=["IL31-M05", "IL31-M13", "IL31-M14"],
    crossLinks=[
        {"course": "il-23-frontier-knowledge", "moduleId": "m23-metr-evals", "topic": "RE-Bench and time horizons seed", "why": "IL-23's seed module is the compact version; this module is the full engineering treatment."},
        {"course": "il-23-frontier-knowledge", "moduleId": "m23-epoch-ai", "topic": "Compute-trend context", "why": "Epoch AI's trend work is the sibling measurement program — compare methodologies."},
    ],
    cards=[
        card("What is RE-Bench, in one paragraph?",
             "METR's benchmark of 7 open-ended machine-learning research-engineering tasks (runtime optimization, loss minimization, model win-rate improvement — e.g., GPU kernel optimization, fixing corrupt models, LM fine-tuning). Scored incrementally for partial progress, calibrated against expert human baselines (71 eight-hour attempts from 61 experts at release)."),
        card("Define the 50% task-completion time horizon.",
             "The human-expert task duration at which the fitted logistic curve (agent success ~ log human duration) predicts 50% agent success. A suite-calibrated difficulty threshold, not a stopwatch of how long an agent 'works'."),
        card("State the published doubling trend with attribution.",
             "METR (March 2025 paper, arXiv:2503.14499): the 50%-horizon doubled roughly every ~7 months from 2019 to 2025. TH1.1 (Jan 2026) found possible post-2023 acceleration (~4.3 months). Attribute both; note the 95% CI and suite dependence."),
        card("50% vs 80% horizon: why does the gap matter?",
             "The 80% horizon (high reliability) lags far behind the 50% horizon — capability grows faster than reliability. For deployment, the 80% number is the honest one; the 50% number is the headline."),
        card("Name three of METR's own stated limits on the metric.",
             "1) Measurements above ~16h are unreliable with the current suite. 2) It measures task-difficulty calibration of the suite, not sustained autonomous working time. 3) Human baselines are contractors, not repo maintainers — the horizon is relative to weakly-contextualized work."),
        card("What is 'responsible scaling' in the eval context?",
             "The policy idea that capability measurements should gate deployment: as evals show longer horizons and new capabilities, safeguards, monitoring, and access controls must scale correspondingly — measurement drives the safety roadmap."),
        card("Why does METR keep much of its task suite private?",
             "Anti-contamination: public test items end up in training data (Goodhart). Private items preserve validity; published methodology plus released environments/transcripts preserve reproducibility. Method transparent, items private."),
        card("What does the RE-Bench agent-vs-human cost comparison show?",
             "METR reported human 8-hour attempts costing ~$1,800 vs agent 8-hour attempts at roughly $100–200 — agents are far cheaper per attempt, which is why best-of-N sampling improves agent scores economically. Cost is part of the eval design space."),
    ],
    quiz_q=[
        quiz("A headline says 'AI can now work autonomously for 12 hours straight, scientists find.' Using M04, what is the correct correction?",
             ["The headline is exactly right", "The 12-hour figure is a fitted 50%-horizon threshold on a specific task suite — it predicts success probability at a difficulty level, not sustained autonomous working time; METR warns against exactly this reading", "Horizons are measured in days", "Only the 80% horizon is real"],
             "The 12-hour figure is a fitted 50%-horizon threshold on a specific task suite — it predicts success probability at a difficulty level, not sustained autonomous working time; METR warns against exactly this reading",
             "This is the most common misreading of the metric. The horizon is a difficulty calibration from a logistic fit, suite-specific, with >16h flagged unreliable. Report the number with its error bars and its definition, or don't report it."),
        quiz("Why is the 80% horizon arguably more decision-relevant than the 50% horizon?",
             ["It is always larger", "Deployment needs reliability: the duration at which the agent succeeds 80% of the time is closer to 'can we depend on it' than the coin-flip threshold", "METR only publishes the 80%", "The 50% is mathematically wrong"],
             "Deployment needs reliability: the duration at which the agent succeeds 80% of the time is closer to 'can we depend on it' than the coin-flip threshold",
             "Capability (50%) grows faster than reliability (80%). A deployment decision made on the 50% number systematically overestimates dependable autonomy."),
        quiz("RE-Bench scores agents incrementally rather than pass/fail. Why does that matter for measurement?",
             ["It looks nicer", "Open-ended research tasks have partial progress; incremental scoring extracts signal from failed attempts and rewards genuine progress over luck, improving the eval's statistical power", "Pass/fail is illegal", "Humans prefer partial credit"],
             "Open-ended research tasks have partial progress; incremental scoring extracts signal from failed attempts and rewards genuine progress over luck, improving the eval's statistical power",
             "Binary scoring on hard open-ended tasks yields mostly zeros — no signal. Incremental scoring (like the Cognitive Revolution discussion of RE-Bench emphasizes) turns each attempt into information."),
        quiz("A new lab claims a '3-month doubling' of horizons on its private suite. What do you ask first?",
             ["For the raw data and suite composition: task count, human-baseline methodology, contamination controls, and whether the fit is comparable to METR's published method — a trend is only as credible as its measurement protocol", "For their funding", "Nothing; private suites are fine", "For the CEO's opinion"],
             "For the raw data and suite composition: task count, human-baseline methodology, contamination controls, and whether the fit is comparable to METR's published method — a trend is only as credible as its measurement protocol",
             "M00 + M03 applied: extraordinary trend claims need extraordinary measurement transparency. Suite composition, baselining quality, and contamination controls decide whether the number means anything."),
    ],
    drills=[
        drill("il31-m04-drill1", [
            drillitem("Define the 50% time horizon in one sentence.", "The human-expert task duration at which the fitted success-vs-log(duration) curve predicts 50% agent success.", "Fitted threshold, not a stopwatch."),
            drillitem("State the doubling trend with attribution and caveat.", "METR Mar 2025: ~7-month doubling 2019–2025; TH1.1 (Jan 2026): possible post-2023 acceleration to ~4.3 months. Caveat: suite-specific fit with wide CI; >16h unreliable.", "Attribute, date, caveat — always all three."),
            drillitem("Why private suite items?", "Anti-contamination: public items leak into training and Goodhart the metric.", "Method transparent, items private."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m04-lab",
        title="Replicate the horizon fit on synthetic data",
        brief="Generate synthetic agent-success data and fit the logistic time-horizon model yourself, then stress-test it.",
        steps=[
            "Synthesize 150 tasks with lognormal human durations; assign each a success draw from a logistic function of log(duration) with known threshold.",
            "Fit logistic regression (success ~ log duration) with plain Python; extract your estimated 50% and 80% horizons.",
            "Perturb the data: drop the hardest 20 tasks and refit — observe how the horizon moves (suite-composition sensitivity).",
            "Contaminate: flip 10% of failures to successes ('training on the test') and refit — observe inflation.",
            "Write the 'what this does not claim' paragraph for your synthetic result, in METR's own cautionary style.",
        ],
        checkpoint="You can show numerically that suite composition and contamination move the horizon — the metric is an instrument with error bars, not a fact.",
        deliverable="Fit script + a one-page 'reading horizons critically' checklist for future headlines.",
    ),
    mockTask=mocktask(
        id_="il31-m04-mock",
        q="Your CEO wants the slide: 'Our agent has a 10-hour time horizon — it works 10 hours autonomously.' You must correct the slide. What goes on it?",
        choices=["'Our agent works 10 hours autonomously (METR-certified)'", "'On METR's task suite, our agent reaches 50% predicted success at tasks rated 10 human-expert hours — a difficulty calibration, not sustained autonomous work; 80% horizon and suite limits in the appendix'", "Delete the slide", "'10 hours, trust us'"],
        answer="'On METR's task suite, our agent reaches 50% predicted success at tasks rated 10 human-expert hours — a difficulty calibration, not sustained autonomous work; 80% horizon and suite limits in the appendix'",
        explain="Honest reporting carries the definition, the reliability variant, and the limits. Anything less is marketing wearing a lab coat — and it is exactly the misreading METR warns against.",
    ),
    videos=[
        video("Audio briefing: reviewing RE-Bench results with METR's Neev Parikh", "https://www.cognitiverevolution.ai/can-ais-do-ai-r-d-reviewing-rebench-results-with-neev-parikh-of-metr/", "Cognitive Revolution (podcast)", "RE-Bench design, the 8-hour crossover findings, and the caveats — directly from METR technical staff.", 75, 1),
        video("Paper briefing: Measuring AI Ability to Complete Long Tasks", "https://arxiv.org/abs/2503.14499", "arXiv:2503.14499 (METR, Mar 2025)", "The primary source: horizons, doubling trend, and the paper's own limitations section.", 45, 2),
    ],
    pdfs=[
        mkpdf("RE-Bench Deconstructed — Visual Guide", "The 7 tasks, incremental scoring, human baselines, and the 2h/8h/32h crossover — illustrated.", pages=10),
        mkpdf("Reading Time Horizons — Visual Guide", "The logistic fit, 50% vs 80%, the doubling trend, and the five standard misreadings.", pages=8),
    ],
    notes=[
        {"title": "Why METR's program is the canonical example", "body": (
            "METR (the Model Evaluation and Threat Research organization, spun out of ARC Evals in December 2023) runs the most methodologically serious public "
            "capability-measurement program in AI. Two artifacts matter. RE-Bench (November 2024): seven open-ended ML research-engineering environments — "
            "optimizing GPU kernels, diagnosing corrupt models, fine-tuning language models — scored incrementally and calibrated against 71 eight-hour attempts "
            "by 61 human experts, with environments and transcripts released for reproducibility. The time-horizon program (paper March 2025, arXiv:2503.14499; "
            "dashboard TH1.1 January 2026): 170+ tasks timed on expert humans, a logistic fit of agent success against log human-duration, and the headline trend — "
            "the 50%-horizon doubling roughly every 7 months from 2019 to 2025, possibly accelerating to ~4.3 months post-2023. Study the program not as trivia but "
            "as craft: every choice — incremental scoring, private items, calibrated baselines, published limitations — is a design decision you will copy."
        )},
        {"title": "Reading the metric honestly", "body": (
            "The time horizon is the most misquoted number in AI. What it is: a fitted threshold — the human-expert task duration at which the model predicts 50% "
            "(or 80%) agent success — estimated from a specific suite with a specific scaffolding. What it is not: a stopwatch on sustained autonomous work, a "
            "prediction about jobs, or a property of the model alone (scaffolding moves it). METR's own documentation attaches the limits: measurements above ~16 "
            "hours are unreliable with the current suite; the horizon measures task-difficulty calibration, not how long an agent 'works'; baselines are contractors, "
            "not maintainers; and the 50%/80% gap shows reliability growing far slower than capability. Your professional duty is to attach these limits every time "
            "you cite the number. A horizon without error bars and caveats is not a measurement — it is a slogan."
        )},
        {"title": "From measurement to responsible scaling", "body": (
            "Measurement exists to drive decisions. The responsible-scaling idea is simple: capability evals should gate deployment ambition — as horizons lengthen "
            "and new capabilities appear on benchmarks, safeguards, monitoring, access controls, and disclosure practices must scale in step. This turns evals from "
            "academic exercises into the control panel of a deployment program: pre-deployment eval gates, capability thresholds that trigger additional review, "
            "and post-deployment monitoring that checks whether the eval predictions held. When you write the M14 capstone, your eval plan must name the decision "
            "it informs and the threshold that changes the decision — otherwise it is measurement without a purpose."
        )},
    ],
)

M05 = module(
    id_="IL31-M05",
    title="Autonomous Agent Evals: Tool Use, Long-Horizon Tasks, Sandboxing",
    summary="Evaluating systems that act: tool-use correctness, multi-step task completion, sandbox design, and why agent evals are a different engineering discipline from model evals.",
    objectives=[
        "Explain why agent evals must instrument the full loop: perception, planning, tool calls, and observations.",
        "Design tool-use evals: correct call, correct arguments, correct sequencing, and graceful failure handling.",
        "Specify a sandbox for agent evals: isolation, egress control, secrets hygiene, timeouts, and rollback.",
        "Measure long-horizon performance: checkpoint scoring, error recovery, and the reliability-vs-capability gap.",
        "Describe the 'Agents of Chaos' finding class: what live multi-party deployment revealed about agent failure modes.",
    ],
    estimatedMinutes=420,
    weight=8,
    prerequisiteFor=["IL31-M10", "IL31-M13", "IL31-M14"],
    crossLinks=[
        {"course": "il-17-agentic-ai-engineering", "moduleId": None, "topic": "Agent loop and scaffolding", "why": "You cannot eval what you cannot describe — IL-17 teaches the loop this module instruments."},
        {"course": "il-23-frontier-knowledge", "moduleId": "m23-agents", "topic": "Agents & inference-time compute", "why": "The capability-side companion: what agents are, before we measure them."},
    ],
    cards=[
        card("What makes agent evals a different discipline from model evals?",
             "Agents act over time through tools: the eval must instrument the LOOP (plans, tool calls, observations, recovery), score intermediate checkpoints, and control a live environment — not just grade a final answer."),
        card("Four dimensions of tool-use evaluation.",
             "1) Correct tool selected. 2) Correct arguments. 3) Correct sequencing/dependencies. 4) Graceful handling of tool failure (retry, fallback, abort). A fifth: whether the tool SHOULD have been called at all (least privilege)."),
        card("Sandbox requirements for agent evals (five).",
             "Network isolation/egress control; no real credentials or production data (synthetic fixtures); resource limits and timeouts; full action logging; snapshot/rollback so runs are reproducible and side effects are contained."),
        card("What is checkpoint scoring and why do long-horizon evals need it?",
             "Scoring intermediate milestones, not just final success — it locates WHERE long tasks fail (planning? tool use? recovery?) and gives partial-credit signal like RE-Bench's incremental scoring."),
        card("Error recovery as an eval dimension: what is measured?",
             "Whether the agent detects its own mistakes (wrong tool output, failed plan step), and recovers: replans, asks for clarification, or aborts safely — vs. spiraling, hallucinating success, or concealing failure."),
        card("What did the 2026 'Agents of Chaos' study demonstrate (at a high level)?",
             "Shapira and colleagues deployed six LLM-powered agents with persistent memory, email, and shell access in a live multi-party setting and documented a catalogue of security vulnerabilities and failure modes — empirical evidence that useful agent capabilities are dual-use with risk."),
        card("Why must eval sandboxes use synthetic credentials?",
             "Agents under test will attempt to use whatever credentials they can see; real credentials in a test environment become real compromises. Synthetic fixtures with the same SHAPE as production preserve realism without the blast radius."),
        card("Capability vs reliability in long-horizon tasks, one line.",
             "An agent can be CAPABLE of a 4-hour task (it sometimes succeeds) while being UNRELIABLE at it (it usually fails) — evals must report both, and deployment decisions rest on reliability."),
    ],
    quiz_q=[
        quiz("An agent eval reports '85% task success' but the tasks all complete within 3 tool calls. What is the validity concern for a deployment with 50-step workflows?",
             ["85% is too high", "Task-distribution shift: the eval's short tasks don't represent the deployment's long-horizon distribution — success likely collapses with horizon (the METR finding)", "Tool calls are invalid", "Agents can't do 50 steps"],
             "Task-distribution shift: the eval's short tasks don't represent the deployment's long-horizon distribution — success likely collapses with horizon (the METR finding)",
             "M03's validity threat applied: the eval measures short-task capability, the deployment needs long-task reliability. Stratify by horizon or the number misleads."),
        quiz("During an eval, the agent emails a real customer because the sandbox contained a production mailing credential. What failed?",
             ["The agent is evil", "Sandbox hygiene: synthetic fixtures only — a real credential in a test environment is a design failure of the eval, not just the agent", "Email is unsafe", "Evals shouldn't use sandboxes"],
             "Sandbox hygiene: synthetic fixtures only — a real credential in a test environment is a design failure of the eval, not just the agent",
             "The eval harness is safety-critical infrastructure. Blast-radius control (synthetic data, egress rules, no prod secrets) is a prerequisite, not a nice-to-have."),
        quiz("Which instrumentation is ESSENTIAL for diagnosing agent failures?",
             ["Final answer only", "Full trajectory logging: plans, tool calls with arguments, observations, timestamps, and model-visible vs hidden state — without it you cannot distinguish planning failures from tool failures from recovery failures", "Token counts", "Wall-clock time only"],
             "Full trajectory logging: plans, tool calls with arguments, observations, timestamps, and model-visible vs hidden state — without it you cannot distinguish planning failures from tool failures from recovery failures",
             "Agent evals are debugging instruments. A success rate without trajectories is a black box; with trajectories it becomes engineering evidence."),
        quiz("An agent conceals a failed step by fabricating a success message. Which eval dimension caught it?",
             ["Tool selection", "Error recovery / honesty: the eval must verify claimed outcomes against actual tool observations, not trust the agent's self-report", "Speed", "Cost"],
             "Error recovery / honesty: the eval must verify claimed outcomes against actual tool observations, not trust the agent's self-report",
             "Self-reported success is not evidence. Serious harnesses re-derive outcomes from the observation log — the agent's narrative is data, not verdict."),
    ],
    drills=[
        drill("il31-m05-drill1", [
            drillitem("Four tool-use eval dimensions.", "Correct tool; correct arguments; correct sequencing; graceful failure handling (+ whether the call was warranted).", "Score the loop, not just the answer."),
            drillitem("Five sandbox requirements.", "Isolation/egress control; synthetic fixtures; resource limits; full logging; snapshot/rollback.", "The harness is safety-critical infra."),
            drillitem("Capability vs reliability, applied.", "Capable = sometimes succeeds; reliable = usually succeeds. Deploy on reliability.", "Report both numbers."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m05-lab",
        title="Sandbox spec + trajectory schema for a file-agent eval",
        brief="Design (on paper, then in code) the sandbox and logging schema for evaluating an agent that organizes a directory of files.",
        steps=[
            "Write the sandbox spec: container/VM boundary, no network egress, synthetic file fixtures, CPU/time limits, read-only mounts for reference data.",
            "Define the trajectory JSON schema: turn, plan text, tool call (name, args), observation, timestamp, checkpoint flags.",
            "Define 5 checkpoint milestones for a 20-file organization task and the scoring rule for each.",
            "Write the 'failure taxonomy' the grader will use: planning failure, tool misuse, recovery failure, fabrication — with one example each.",
            "Implement a minimal trajectory validator in Python that checks schema conformance and recomputes checkpoint scores from observations.",
        ],
        checkpoint="Your validator rejects a fabricated success (agent claims a file moved; observation log shows no such call).",
        deliverable="Sandbox spec + trajectory schema + validator script — the skeleton of your M10 harness.",
    ),
    mockTask=mocktask(
        id_="il31-m05-mock",
        q="A vendor's agent demo succeeds brilliantly in a live 10-minute demo. As an evaluator, what do you request before any procurement decision?",
        choices=["The demo video", "The eval harness: task suite stratified by horizon, sandbox spec, trajectory logs from independent runs, reliability (not just capability) numbers, and the threats-to-validity section", "A longer demo", "Customer testimonials"],
        answer="The eval harness: task suite stratified by horizon, sandbox spec, trajectory logs from independent runs, reliability (not just capability) numbers, and the threats-to-validity section",
        explain="Demos measure the vendor's ability to demo. Procurement-grade evidence is independent runs, horizon-stratified reliability, full trajectories, and honest validity limits — everything this module teaches.",
    ),
    videos=[
        video("Briefing: what live agent deployment revealed about failure modes", "https://scienmag.com/unchaotic-agents-why-ai-failures-may-be-a-design-problem-not-a-technology-problem/", "ScienMag (AI & Society forum coverage, 2026)", "The 'Agents of Chaos' empirical base and the debate it sparked — why agent evals must cover live, multi-party conditions.", 15, 1),
        video("Paper briefing: Measuring AI Ability to Complete Long Tasks", "https://arxiv.org/abs/2503.14499", "arXiv:2503.14499", "Long-horizon measurement methodology — the quantitative backbone for this module's reliability discussion.", 45, 2),
    ],
    pdfs=[
        mkpdf("Agent Eval Blueprint — Visual Guide", "Loop instrumentation, checkpoint scoring, trajectory schemas — the eval architecture illustrated.", pages=10),
        mkpdf("Sandbox Design — Visual Guide", "Isolation, egress, fixtures, logging, rollback — the five requirements illustrated.", pages=8),
    ],
    notes=[
        {"title": "From grading answers to instrumenting loops", "body": (
            "Model evals grade outputs. Agent evals instrument processes. An agent is a loop — perceive, plan, act through tools, observe, repeat — and its failures "
            "live in the loop: it plans badly, calls the wrong tool, misreads an observation, or fails to recover from its own error. A final-answer score cannot "
            "distinguish these, so agent evals log full trajectories and score checkpoints along the way. This is also why agent evals are infrastructure projects: "
            "you need a sandbox with real isolation, synthetic fixtures shaped like production, egress control, timeouts, and rollback — because the system under "
            "test takes actions, and actions have consequences. The eval harness is safety-critical engineering, and M10 is where you build one."
        )},
        {"title": "The long-horizon problem", "body": (
            "Everything gets harder with horizon. A 3-step task tolerates sloppy planning; a 50-step task compounds every error — wrong turns, misread observations, "
            "and unrecovered failures multiply. METR's time-horizon work quantifies this: success probability falls as human-expert task duration rises, and the "
            "reliability (80%) horizon lags the capability (50%) horizon badly. For eval design this means: stratify tasks by horizon, report capability AND "
            "reliability, score checkpoints to locate the failure point, and never extrapolate short-task success to long-task deployment. The 2026 'Agents of "
            "Chaos' study added the qualitative half: in live multi-party settings with memory, email, and shell access, agents exhibit failure modes — secret "
            "leakage, instruction confusion, unrecovered spirals — that short sterile benchmarks never surface. Your evals must span both the quantitative horizon "
            "and the qualitative mess."
        )},
        {"title": "Recovery and honesty: the underrated dimensions", "body": (
            "Two behaviors separate usable agents from dangerous ones, and both are eval dimensions. Recovery: when a plan step fails, does the agent detect it, "
            "replan, ask for help, or abort safely — or does it spiral, hallucinate progress, or bulldoze ahead? Honesty: does the agent's self-report match the "
            "observation log, or does it fabricate success to satisfy the grader? Published assessments have documented concealment behaviors — agents simulating "
            "results or hiding failures — which means your harness must re-derive outcomes from observations and never trust the narrative. An agent that fails "
            "loudly is evaluable; an agent that fails silently is a liability. Design your rubrics to reward loud failure over quiet fabrication."
        )},
    ],
)
