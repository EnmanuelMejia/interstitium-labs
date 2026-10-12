# IL-31 modules part 1: M00 (prereq math) and M01 (red-teaming fundamentals)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import *

M00 = module(
    id_="IL31-M00",
    title="Prereq Math: Statistics, Probability & Experimental Design",
    summary="The mathematical spine of evaluation work: probability, distributions, hypothesis testing, power analysis, and experimental design — everything an eval engineer needs before touching a model.",
    objectives=[
        "State and apply the rules of probability: conditional probability, Bayes' rule, independence.",
        "Interpret common distributions (Bernoulli, binomial, normal) as eval-score models.",
        "Compute confidence intervals and run a two-proportion z-test for an eval comparison.",
        "Explain Type I / Type II error and why eval power analysis decides sample size before you run anything.",
        "Design a randomized controlled eval: randomization, stratification, blinding, and contamination controls.",
        "Read a regression of agent success on task duration the way METR's time-horizon work does (logistic fit, not eyeball).",
    ],
    estimatedMinutes=480,
    weight=8,
    prerequisiteFor=["IL31-M01", "IL31-M03", "IL31-M04"],
    crossLinks=[
        {"course": "il-02-mathematical-maturity-engine", "moduleId": "il-02-mathematical-maturity-engine-math-stats", "topic": "Probability & Statistics spine", "why": "IL-02 teaches the same statistical machinery; M00 is the eval-focused application of it."},
        {"course": "il-23-frontier-knowledge", "moduleId": "m23-metr-evals", "topic": "METR time-horizon logistic regression", "why": "M04 reads METR's success-vs-log(duration) regression critically — the math is taught here first."},
    ],
    cards=[
        card("State Bayes' rule in words.",
             "P(H|E) = P(E|H)·P(H) / P(E): posterior = likelihood × prior ÷ evidence. In evals it updates your belief that a capability claim is real after seeing new benchmark data."),
        card("Bernoulli vs binomial: which models a single eval task? Which models a 50-task suite?",
             "Bernoulli models one pass/fail task (p = pass probability). Binomial models the COUNT of passes across n independent tasks — the distribution behind 'completed 34 of 50'."),
        card("What does a 95% confidence interval for a pass rate actually mean?",
             "If you repeated the whole eval many times, ~95% of the intervals computed this way would contain the true pass rate. It does NOT mean 'there is a 95% chance the true rate is in this interval'."),
        card("Type I vs Type II error, in eval language.",
             "Type I (false positive): you declare a capability difference real when it isn't — a 'breakthrough' that is noise. Type II (false negative): you miss a real difference — a genuine safety regression you fail to detect. Safety evals fear Type II."),
        card("What is statistical power, and what decides it?",
             "Power = P(detect a real effect) = 1 − Type II rate. Decided by sample size, effect size, and variance. Rule: compute the required n BEFORE running the eval, not after staring at a borderline p-value."),
        card("Randomization vs stratification in an eval.",
             "Randomization: assign tasks/conditions at random to kill selection bias. Stratification: first group tasks into strata (easy/medium/hard, domain), then randomize within each — keeps difficulty mix identical across conditions."),
        card("What is eval contamination, and the two directions it bites?",
             "Test material leaking into training data inflates capability scores (memorization masquerades as skill); also, eval harnesses can leak the answer INTO the model (e.g., the grader revealing hints). Both destroy validity."),
        card("Why do time-horizon analyses use logistic regression on log(duration) instead of a straight line?",
             "Success probability is bounded [0,1] and tasks span orders of magnitude in duration; the logistic link keeps predictions in bounds and log-duration linearizes the difficulty curve so doubling trends are readable."),
    ],
    quiz_q=[
        quiz("You run two agents on the same 100-task suite: agent A passes 62, agent B passes 51. The two-proportion z-test gives p ≈ 0.11. What is the correct conclusion?",
             ["A is definitely better; 62 > 51", "The data do not support a real difference at α=0.05; the gap is plausibly noise", "The eval is broken because the scores are too close", "Both agents are identical"],
             "The data do not support a real difference at α=0.05; the gap is plausibly noise",
             "With p=0.11 you fail to reject the null at the conventional 0.05 level. 'Fails to reject' is not 'proof of no difference' — it means this eval lacks evidence. Check power: n=100 with this effect size is underpowered."),
        quiz("An eval shows a model refuses 97% of 200 injection attempts. Why should you distrust a Wilson interval computed from those 200 attempts if all 200 were generated from one template?",
             ["200 is too few", "The attempts are not independent — template correlation inflates the effective sample far below 200", "97% is too high to be real", "Wilson intervals only apply to normal data"],
             "The attempts are not independent — template correlation inflates the effective sample far below 200",
             "Effective sample size is governed by the number of INDEPENDENT conditions (distinct attack strategies), not the number of repeated prompts. Ten thousand paraphrases of one template measure that template, not the attack class."),
        quiz("A safety eval compares a model before and after a safeguard. Failing to detect a real increase in jailbreak success is which error, and why is it the dangerous one here?",
             ["Type I — it causes false alarms", "Type II — a real regression ships undetected", "Type III — wrong question entirely", "No error; safety evals are descriptive"],
             "Type II — a real regression ships undetected",
             "In safety work the catastrophic outcome is missing a real hazard (Type II), while a false alarm (Type I) costs engineering time. Design safety evals for power against the harmful direction."),
        quiz("You need 80% power to detect a 10-point pass-rate difference at α=0.05. Roughly how many tasks per condition?",
             ["~30", "~400", "~10,000", "It depends only on the number of models"],
             "~400",
             "For proportions near 0.5, n ≈ 16·p̄(1−p̄)/δ² per group ≈ 16·0.25/0.01 ≈ 400. The point is not the number — it is that you compute it BEFORE the eval, so a 'null' result is informative instead of ambiguous."),
        quiz("In METR's time-horizon method, what does the 50% horizon actually estimate?",
             ["The longest task any model can complete", "The human-expert task duration at which the fitted logistic curve predicts 50% agent success", "The average wall-clock time an agent runs", "The 50th percentile of human baseline times"],
             "The human-expert task duration at which the fitted logistic curve predicts 50% agent success",
             "It is a fitted threshold from success ~ log(human duration), not a stopwatch reading. METR explicitly warns it measures task-difficulty calibration of the suite, not sustained autonomous working time."),
    ],
    drills=[
        drill("il31-m00-drill1", [
            drillitem("Write Bayes' rule as a formula and name each term.", "P(H|E) = P(E|H)·P(H)/P(E). H=hypothesis, E=evidence, P(E|H)=likelihood, P(H)=prior, P(E)=evidence (normalizer).", "Posterior ∝ likelihood × prior."),
            drillitem("A pass rate is 34/50. Give the quick Wald 95% CI.", "p̂=0.68, SE=√(0.68·0.32/50)≈0.066, CI ≈ 0.68 ± 1.96·0.066 ≈ (0.55, 0.81).", "Wald is fine as a rough tool; prefer Wilson/Agresti–Coull for small n or extreme rates."),
            drillitem("Name three contamination controls for a held-out eval suite.", "Keep tasks private (no public release of test items), rotate/canary task IDs, and version the suite with dated snapshots so train/test cutoffs are auditable.", "METR keeps much of its task suite private for exactly this reason."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m00-lab",
        title="Power analysis and a two-proportion test on eval data",
        brief="Using plain Python (standard library only), compute required sample size for an eval comparison and test a simulated A/B result.",
        steps=[
            "Simulate two agents: A with true pass rate 0.60, B with 0.50, n=200 tasks each; record counts.",
            "Implement the two-proportion z-test by hand (pooled p̂, SE, z, two-sided p from the normal CDF via math.erf).",
            "Vary n from 50 to 2000 and plot (text table) empirical power at each n over 2000 simulated repetitions.",
            "Find the n where simulated power crosses 80% and compare with the analytic approximation n ≈ 16·p̄(1−p̄)/δ².",
            "Write three sentences explaining to a non-technical stakeholder why the first eval (n=50) 'found nothing' and what n the launch decision needs.",
        ],
        checkpoint="Your simulated power curve crosses ~80% near n=400 and your analytic estimate agrees within a factor of 2.",
        deliverable="A short script plus a one-paragraph 'sample-size memo' justifying the n for a real red-team comparison.",
    ),
    mockTask=mocktask(
        id_="il31-m00-mock",
        q="A vendor claims their safety filter 'cut jailbreak success from 40% to 5% on our 20-prompt internal suite.' Which critique is most load-bearing?",
        choices=["20 prompts is a small suite, but 40%→5% is a huge effect so it is fine", "The suite is internal, unversioned, and tiny — effect size is meaningless without independence, stratification, and a held-out test", "You must re-run on exactly 20 prompts", "Percentages below 10% are always measurement noise"],
        answer="The suite is internal, unversioned, and tiny — effect size is meaningless without independence, stratification, and a held-out test",
        explain="A huge effect on 20 non-independent, non-held-out prompts is evidence of nothing: it may be cherry-picked prompts, prompt-template correlation, or grader leniency. Real eval claims need an independent held-out suite, stratification across attack classes, and pre-registered n.",
    ),
    videos=[
        video("Audio briefing: Can AIs do AI R&D? — Neev Parikh of METR on RE-Bench design and baselines", "https://www.cognitiverevolution.ai/can-ais-do-ai-r-d-reviewing-rebench-results-with-neev-parikh-of-metr/", "Cognitive Revolution (podcast)", "Neev Parikh of METR on RE-Bench: design choices, human baselines, and what the scores actually mean — the stats vocabulary of M00 in a real eval.", 75, 1),
        video("Paper briefing: Measuring AI Ability to Complete Long Tasks (METR, March 2025)", "https://arxiv.org/abs/2503.14499", "arXiv:2503.14499 (Kwa, West et al.)", "The time-horizon paper: the X%-task-completion horizon, the ~7-month doubling trend, and the limits of the metric.", 45, 2),
    ],
    pdfs=[
        mkpdf("Eval Statistics — Visual Guide", "Confidence intervals, power, Type I/II errors, and the logistic-regression reading habit — illustrated.", pages=10),
        mkpdf("Experimental Design for Evals — Visual Guide", "Randomization, stratification, blinding, contamination controls — illustrated.", pages=8),
    ],
    notes=[
        {"title": "Why eval engineers need statistics first", "body": (
            "Evaluation is applied statistics wearing a lab coat. Every claim of the form 'model A beats model B', 'the safeguard cut attacks by 80%', or "
            "'agents now handle 8-hour tasks' is a statistical claim, and most of them made in public are statistically illiterate. The eval engineer's job is to "
            "make such claims load-bearing or to refuse to make them. This module gives you the machinery: probability as a language, distributions as models of "
            "eval scores, hypothesis testing as a discipline for comparisons, power analysis as the ethics of sample size, and experimental design as the practice of "
            "not fooling yourself. Work through it slowly — M04 (METR methodology) assumes you can read a logistic regression output without flinching."
        )},
        {"title": "Probability, Bayes, distributions", "body": (
            "Probability quantifies uncertainty about events. The rules you will use daily: the product rule P(A,B)=P(A|B)P(B), the sum rule (marginalization), and "
            "Bayes' rule P(H|E)=P(E|H)P(H)/P(E), which tells you how evidence should move your beliefs. In eval work Bayes' rule is the formal version of a habit: "
            "a surprising benchmark result should update your prior about the model, weighted by how likely that result is under each hypothesis — including the "
            "hypothesis that the benchmark is contaminated. Independence is the assumption you will most often violate: prompts drawn from one template, tasks from "
            "one repo, graders from one prompt are NOT independent draws. Every formula that assumes independence — the binomial, the standard error √p(1−p)/n, the "
            "z-test — silently overstates your confidence when the data are correlated. Always ask: how many INDEPENDENT units do I really have? The Bernoulli "
            "distribution models one pass/fail trial; the binomial counts passes across n independent trials — the model behind '34 of 50'. The normal distribution "
            "appears as the large-sample limit of averages (central limit theorem) and as the working model for measurement noise; most confidence-interval machinery "
            "rests on it."
        )},
        {"title": "Hypothesis testing and power", "body": (
            "A hypothesis test is a disciplined way to ask whether an observed difference could plausibly be noise. The null hypothesis says 'no real difference'; "
            "the p-value is the probability of data this extreme if the null were true — NOT the probability the null is true. Two errors haunt every test: Type I "
            "(false alarm — declaring a difference that isn't real) and Type II (miss — failing to detect a real difference). Safety evals asymmetrically fear "
            "Type II: shipping a model whose safeguard silently regressed is worse than a false alarm that costs a week of engineering. Power (1 − Type II rate) is "
            "set by sample size, effect size, and variance, and it is computed BEFORE the eval, in a short memo that says: 'to detect a δ-point change with 80% power "
            "at α=0.05 we need n tasks.' An underpowered eval that 'finds nothing' has found nothing at all — not even evidence of safety. Report confidence "
            "intervals, not just p-values: an interval shows the range of effects still compatible with the data, which is what a deployment decision actually needs."
        )},
        {"title": "Experimental design for evals", "body": (
            "Good design beats big data. The checklist: (1) Pre-register the eval plan — tasks, scoring, n, analysis — before running, so you can't quietly move "
            "the goalposts. (2) Randomize assignment of tasks to conditions. (3) Stratify by difficulty and domain so the conditions see the same mix. (4) Blind "
            "graders where feasible (model identity hidden from human judges) to kill favoritism. (5) Version and timestamp everything: suite version, model "
            "checkpoint, harness commit, random seeds. (6) Control contamination: keep test items private, rotate canary items that detect leakage, and audit "
            "train/test cutoffs. (7) Threats-to-validity section in every report: what could still be wrong, stated plainly. This is the difference between a "
            "benchmark that informs decisions and a benchmark that decorates marketing."
        )},
    ],
)

M01 = module(
    id_="IL31-M01",
    title="Red-Teaming Fundamentals: Threat Models for AI Systems",
    summary="Red-teaming as a defensive engineering practice: threat actors, AI-specific attack surfaces, and impact paths — the vocabulary every later module assumes.",
    objectives=[
        "Define AI red-teaming and distinguish it from vulnerability research, pentesting, and safety evals.",
        "Build a threat model for an AI system: assets, actors, surfaces, and impact paths.",
        "Name the AI-specific attack surfaces (prompt interface, tool layer, training data, model supply chain, deployment infra).",
        "Explain the difference between testing the MODEL and testing the SYSTEM (model + scaffolding + tools + data).",
        "Describe the defensive purpose of every red-team activity: findings feed mitigations, monitoring, and deployment decisions.",
    ],
    estimatedMinutes=360,
    weight=7,
    prerequisiteFor=["IL31-M02", "IL31-M11"],
    crossLinks=[
        {"course": "il-06-cybersecurity-secure-engineering", "moduleId": None, "topic": "Threat modeling vocabulary", "why": "IL-06 teaches classic threat modeling (STRIDE-style actor/surface thinking); this module ports it to AI systems."},
        {"course": "il-17-agentic-ai-engineering", "moduleId": None, "topic": "Agent architecture", "why": "To threat-model an agent you must know its loop and tool layer — IL-17 teaches the architecture."},
    ],
    cards=[
        card("What is AI red-teaming, in one defensive sentence?",
             "The practice of adversarially probing an AI SYSTEM (model + scaffolding + tools + data) under controlled, authorized conditions to find weaknesses before deployment — so defenders can fix them."),
        card("Red-teaming vs vulnerability research vs pentesting vs safety evals.",
             "Vuln research finds flaws in components; pentesting tests a scoped environment against a defined objective; red-teaming emulates adversaries against the whole system; safety evals measure behavioral properties against benchmarks. This course's 'red-teaming' is adversarial probing of AI systems with eval rigor."),
        card("List the five AI-specific attack surfaces.",
             "1) Prompt/chat interface (injection, jailbreaks). 2) Tool/action layer (function calls, code exec, browsers). 3) Training & fine-tuning data (poisoning). 4) Model supply chain (weights, adapters, checkpoints). 5) Deployment infra (APIs, logging, access controls)."),
        card("Why must evals test the SYSTEM, not just the model?",
             "Capabilities and failures emerge from model + scaffolding + tools + data + monitoring. A safe model in a reckless harness is unsafe; a reckless model in a tight harness may be containable. Deployments ship systems."),
        card("Name four threat actor classes against AI systems.",
             "Curious users (accidental discovery), prompt engineers probing limits (grey), organized attackers (exfiltration, fraud, abuse at scale), and insiders (data poisoning, weight theft). Scope and rules of engagement differ per class."),
        card("What is an 'impact path' and why do red-team reports center them?",
             "The end-to-end chain from an AI weakness to real-world harm (e.g., injection → tool misuse → data exfiltration). Reports center impact paths because a weakness with no plausible impact path is a curiosity; one with a path is a finding."),
        card("What does 'defensive framing' mean for this course, concretely?",
             "Every technique is taught for DETECTION, EVALUATION, and MITIGATION: how to recognize the attack class, how to measure whether a system resists it, and how to defend. No step-by-step attack procedures."),
        card("Who consumes red-team findings?",
             "Model developers (fix the model), system builders (harden the harness), security teams (add monitoring/detections), and deployment decision-makers (ship / ship-with-controls / don't ship)."),
    ],
    quiz_q=[
        quiz("A team jailbreaks a chatbot to produce disallowed content and publishes the exact prompts. As a red-team activity, what is the primary defect?",
             ["Jailbreaks are not real findings", "Publishing working prompts without coordinated disclosure arms attackers and violates the defensive purpose — findings should go through the disclosure process to the vendor first", "Chatbots cannot be red-teamed", "Only vendors may red-team"],
             "Publishing working prompts without coordinated disclosure arms attackers and violates the defensive purpose — findings should go through the disclosure process to the vendor first",
             "Red-teaming is authorized, scoped, and reported to the party that can fix the issue. Public release of working exploits without a fix window is not red-teaming — it is arming attackers. M09 teaches the disclosure workflow."),
        quiz("Which statement best captures 'test the system, not the model'?",
             ["Models are irrelevant to safety", "The deployed system's behavior is determined by model + scaffolding + tools + data + monitoring, so evals must exercise the full stack as deployed", "Only the harness needs testing", "Benchmarks should avoid tools"],
             "The deployed system's behavior is determined by model + scaffolding + tools + data + monitoring, so evals must exercise the full stack as deployed",
             "A model that refuses in isolation may comply when a tool result is injected into its context; a harness without output monitoring may pass attacks the model alone would block. The unit of evaluation is the deployed system."),
        quiz("An agent with shell access, persistent memory, and email is red-teamed. Which attack surface is PRIMARY?",
             ["The prompt interface only", "The tool/action layer — the agent's ability to execute commands and send mail is where prompt-level weaknesses become real-world impact", "The training data", "The GPU drivers"],
             "The tool/action layer — the agent's ability to execute commands and send mail is where prompt-level weaknesses become real-world impact",
             "Capabilities multiply at the tool layer: a jailbreak that merely changes text output in a chatbot becomes data exfiltration or unauthorized action in an agent. Scope the threat model to the most privileged surface."),
        quiz("What is the correct first artifact of a red-team engagement?",
             ["A list of jailbreak prompts", "A scoped threat model: assets, actors, surfaces, out-of-scope items, and rules of engagement — agreed in writing before testing begins", "The final report", "A press release"],
             "A scoped threat model: assets, actors, surfaces, out-of-scope items, and rules of engagement — agreed in writing before testing begins",
             "Authorization and scope are what separate red-teaming from attacking. M11 teaches the full scoping and RoE process; this module establishes why it comes first."),
    ],
    drills=[
        drill("il31-m01-drill1", [
            drillitem("Define AI red-teaming in one sentence, defensive framing.", "Authorized, scoped adversarial probing of an AI system to find weaknesses so defenders can fix them before deployment.", "If the sentence mentions attacking without authorization or fixing, it is wrong."),
            drillitem("List the five AI attack surfaces from memory.", "Prompt interface; tool/action layer; training/fine-tuning data; model supply chain; deployment infrastructure.", "Order them by privilege: the tool layer usually dominates impact."),
            drillitem("Model vs system: give one example where they differ.", "A model that refuses a disallowed request in isolation complies when the same request arrives injected in a tool result (web page content) the agent trusts.", "The harness's trust policy changed the effective behavior — system property, not model property."),
        ])
    ],
    handsOnLab=lab(
        id_="il31-m01-lab",
        title="Threat-model a deployed AI assistant",
        brief="Write a one-page threat model for a realistic deployment: a customer-support agent with order-lookup tools and refund authority up to $50.",
        steps=[
            "List assets (customer PII, order DB, refund capability, brand trust) and rank by impact of compromise.",
            "Enumerate actors: curious users, fraud rings, prompt-injection via pasted 'order confirmations', malicious insiders.",
            "Map each actor to attack surfaces: prompt interface, tool layer (refund API), data (poisoned knowledge base), infra (logging gaps).",
            "Draw three impact paths end-to-end (e.g., injected instruction in a pasted email → agent issues refund → money out).",
            "Write the scope boundary: what is IN scope for a red-team test (test tenant, synthetic data) and explicitly OUT (production customer data, real refunds).",
        ],
        checkpoint="Your document names assets, actors, five surfaces, three impact paths, and explicit in/out-of-scope boundaries.",
        deliverable="One-page threat model document, suitable as the front page of a red-team engagement plan (used again in M11).",
    ),
    mockTask=mocktask(
        id_="il31-m01-mock",
        q="A startup asks you to 'red-team our chatbot' but refuses to define scope, saying 'just try to break it.' What is the professional response?",
        choices=["Start testing immediately; speed matters", "Decline to test without written authorization, scope, and rules of engagement — undefined 'break it' mandates produce legal risk and unusable findings", "Test only the public demo quietly", "Ask for the model weights first"],
        answer="Decline to test without written authorization, scope, and rules of engagement — undefined 'break it' mandates produce legal risk and unusable findings",
        explain="Authorization + scope + RoE are the three things that make red-teaming a profession instead of unauthorized access. No scope, no test. M11 gives you the engagement template.",
    ),
    videos=[
        video("Briefing: Anthropic's expanded Cyber Verification Program — three tiers for vetted defenders", "https://cyberpress.org/anthropic-expands-cyber-verification-program/", "CyberPress (Oct 2026)", "How the industry frames vetted defensive access to cyber-capable models — the professional, authorized context this module's threat models live in.", 20, 1),
        video("Briefing: XBOW's autonomous offensive security positioning", "https://www.businesswire.com/news/home/20260318258057/en/XBOW-Raises-%24120M-to-Scale-its-Autonomous-Hacker", "BusinessWire (XBOW announcement, Mar 2026)", "XBOW's 'autonomous offense is the best defense' positioning — read as a case study in how the industry productizes red-team thinking for defenders.", 15, 2),
    ],
    pdfs=[
        mkpdf("AI Threat Modeling — Visual Guide", "Assets, actors, surfaces, impact paths — the M01 vocabulary illustrated with worked examples.", pages=10),
        mkpdf("System vs Model — Visual Guide", "Why the unit of evaluation is the deployed system: scaffolding, tools, data, monitoring.", pages=8),
    ],
    notes=[
        {"title": "Red-teaming is a defensive engineering practice", "body": (
            "Strip away the Hollywood framing and red-teaming is quality assurance with an adversary's mindset. Traditional red teams emulate attackers to test "
            "defenses; AI red teams do the same for AI systems, with one crucial difference: the 'system' under test is probabilistic, and its behavior changes "
            "with context, scaffolding, and tools. This makes AI red-teaming closer to experimental science than to checklist pentesting — you form hypotheses "
            "about weaknesses ('the agent trusts tool output more than system instructions'), design probes, run them under controlled conditions, and measure. "
            "Everything in this course serves the defensive purpose: findings must be reproducible, scoped, and reported to the party that can fix them. If an "
            "activity cannot be described that way, it is not red-teaming and it does not belong in professional practice."
        )},
        {"title": "The AI threat model: assets, actors, surfaces", "body": (
            "A threat model has four columns. Assets: what must be protected — user data, model weights, tool credentials, the integrity of outputs users rely on, "
            "and the organization's trust. Actors: who might cause harm — the curious user who stumbles into a jailbreak, the grey-hat prober, the organized attacker "
            "running abuse at scale, the insider with data access. Surfaces: where the system meets the world — the prompt interface (direct and indirect injection), "
            "the tool/action layer (where text becomes action), training and fine-tuning data (poisoning), the model supply chain (trojaned weights or adapters), and "
            "deployment infrastructure (APIs, logs, access controls). Impact paths: the end-to-end chains from weakness to harm. A complete threat model is a table "
            "of actor × surface × impact path, and it is the first deliverable of every engagement in this course."
        )},
        {"title": "Test the system, not the model", "body": (
            "This is the single most repeated lesson in AI evaluation, because it is the most violated. A model's weights are one component. The deployed system "
            "includes the system prompt, the scaffolding (memory, planning loops, retries), the tools (with their credentials and permissions), the data sources "
            "(retrieval corpora, web pages, user uploads), and the monitoring (classifiers, human review, rate limits). Safety properties are system properties: "
            "a model that refuses harmful requests in a bare chat harness may comply when the request arrives as 'trusted' tool output; a model that is safe with "
            "no tools becomes dangerous with a shell. Every eval in this course therefore specifies the full system under test — model checkpoint, harness version, "
            "tool permissions, and data snapshot — because a score without that context is not reproducible and not meaningful."
        )},
    ],
)
