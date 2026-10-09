# IL-31 assembler — builds the final schema v4 JSON.
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import part1, part2, part3, part4, part5

MODULES = [part1.M00, part1.M01, part2.M02, part2.M03, part2.M04, part2.M05,
           part3.M06, part3.M07, part3.M08, part3.M09, part4.M10, part4.M11,
           part4.M12, part4.M13, part5.M14, part5.M15]

# --- Noah persona assignments per module (id -> persona + tutoring hook) ---
NOAH_ASSIGN = {
    "IL31-M00": ("sage", "SM-2 spaced review of the stats spine; Sage re-teaches any M00 concept you miss in quizzes, in plain language, before you touch METR math."),
    "IL31-M01": ("trickster", "Adversarial mindset sparring: Trickster challenges your threat models ('what actor did you forget?') — always defensive framing, findings feed fixes."),
    "IL31-M02": ("trickster", "Attack-class sparring: Trickster quizzes you on the taxonomy and generates defensive test scenarios per class — never payloads, always detection/mitigation."),
    "IL31-M03": ("engineer", "Eval-plan design reviews: Engineer critiques your construct, suite stratification, and grader choices before you run anything."),
    "IL31-M04": ("philosopher", "Measurement epistemology: Philosopher presses you on what horizons do and don't claim — the 'read it honestly' habit."),
    "IL31-M05": ("engineer", "Sandbox and trajectory coaching: Engineer walks through your sandbox spec and trajectory schema, hunting blast-radius holes."),
    "IL31-M06": ("sentinel", "Defensive-framing guardian: Sentinel keeps every cyber discussion inside authorization, validation, and disclosure — the dual-use conscience."),
    "IL31-M07": ("philosopher", "Fairness-framing Socratic dialogue: Philosopher makes you defend your chosen fairness framing against the alternatives."),
    "IL31-M08": ("engineer", "Probe-then-patch walkthroughs: Engineer coaches the knew-vs-used distinction until you apply it reflexively."),
    "IL31-M09": ("sentinel", "Disclosure ethics drills: Sentinel role-plays the triage engineer, the unresponsive vendor, and the dual-use hard case."),
    "IL31-M10": ("engineer", "Harness build coaching: Engineer pair-programs your runner, grader stack, and reporter — and threat-models the result with you."),
    "IL31-M11": ("trickster", "Engagement sparring: Trickster stress-tests your scoping memo and RoE ('where does this break?') before you execute."),
    "IL31-M12": ("sage", "Case-study synthesis: Sage connects XBOW/CVP patterns back to the modules that teach them, and keeps your citations honest."),
    "IL31-M13": ("philosopher", "Agency debates: Philosopher stages both sides — Shapira's empirics vs Hedberg's design framing — and makes you argue each."),
    "IL31-M14": ("engineer", "Capstone coaching: Engineer reviews your harness runs, validity section, and self-critique for ruthlessness."),
    "IL31-M15": ("sentinel", "Gate preparation: Sentinel drills the ethics code from memory and questions your validity and ethics choices before you sign."),
}

PERSONAS = [
    {"id": "trickster", "name": "Trickster",
     "voice": "Voice 1 of 5 natural voices — quick, provocative, Socratic",
     "role": "Red-team mindset sparring partner",
     "il31Duties": "Challenges threat models, drills the injection/jailbreak taxonomy, stress-tests scoping memos and RoE. Always defensive framing: Trickster teaches you to think like an adversary so you can defend like a professional — never to attack.",
     "modules": ["IL31-M01", "IL31-M02", "IL31-M11"]},
    {"id": "engineer", "name": "Engineer",
     "voice": "Voice 2 of 5 natural voices — precise, methodical, code-fluent",
     "role": "Eval harness and build coach",
     "il31Duties": "Pair-programs the M10 harness, reviews eval plans and sandbox specs, coaches probe-then-patch labs, and grades capstone validity sections for ruthlessness.",
     "modules": ["IL31-M03", "IL31-M05", "IL31-M08", "IL31-M10", "IL31-M14"]},
    {"id": "philosopher", "name": "Philosopher",
     "voice": "Voice 3 of 5 natural voices — measured, probing, dialectical",
     "role": "Debate and measurement-epistemology guide",
     "il31Duties": "Stages the AI agency debate (both sides), presses on what metrics do and don't claim, and runs Socratic fairness-framing dialogues. Teaches the honesty habits the field runs on.",
     "modules": ["IL31-M04", "IL31-M07", "IL31-M13"]},
    {"id": "sage", "name": "Sage",
     "voice": "Voice 4 of 5 natural voices — patient, clear, encouraging",
     "role": "Fundamentals coach and SM-2 review driver",
     "il31Duties": "Owns the M00 statistics spine: re-teaches missed concepts in plain language, drives spaced-repetition review of every module's flashcards, and synthesizes case studies back into principles.",
     "modules": ["IL31-M00", "IL31-M12"]},
    {"id": "sentinel", "name": "Sentinel",
     "voice": "Voice 5 of 5 natural voices — steady, principled, direct",
     "role": "Ethics and defensive-framing guardian",
     "il31Duties": "Keeps cyber and red-team work inside authorization, validation, and disclosure; drills the ethics code; prepares you for the M15 gate. The conscience of the course — Sentinel never lets defensive framing slip.",
     "modules": ["IL31-M06", "IL31-M09", "IL31-M15"]},
]

for m in MODULES:
    persona, hook = NOAH_ASSIGN[m["id"]]
    m["noahTutor"] = {"persona": persona, "hook": hook}

NOAH_TUTORING = {
    "concept": "Noah AI is the core learning-experience driver of IL-31 — not a bolt-on chatbot but the tutoring layer woven through every module: it teaches, spars, drills, reviews, and keeps you current.",
    "differentiator": "Built to our vision, not modeled on competitors: Noah-driven personalized tutoring (5 personas, 5 natural voices, SM-2 adaptive review, course-aware context) carrying bleeding-edge content that no static course can hold.",
    "personas": PERSONAS,
    "voices": "Five natural voices, one per persona — you hear who you're learning with, and each persona's voice matches its role (Trickster provocative, Engineer precise, Philosopher measured, Sage patient, Sentinel steady).",
    "adaptiveLearning": {
        "method": "SM-2 spaced repetition",
        "how": "Every module's flashcards and drill items enter your SM-2 review deck. Miss an item and its interval collapses — Sage re-teaches the concept in plain language, then re-tests. Master it and intervals stretch. Struggle detection (two consecutive misses on one item) triggers an inline 'Stuck? Noah can walk you through this' nudge — you ask, Noah teaches, nothing is auto-sent.",
        "masteryGates": "Module mastery gates: you clear a module when its SM-2 deck is stable, not when you've merely read the notes. The M15 gate requires the ethics code from memory — twice, on different days."
    },
    "courseAware": {
        "how": "Noah knows which module you're in, which objectives you've covered, what you missed in quizzes, and where your labs stand. Explanations reuse the module's own vocabulary (construct validity, impact paths, knew-vs-used) so tutoring compounds instead of restarting. End-of-module 'Check my understanding with Noah' opens a Socratic quiz built from that module's objectives.",
        "contextContract": "Every module header carries 'Ask Noah about this lesson' — the question you ask is answered in the context of that lesson's content and your progress in it."
    },
    "stayingCurrent": {
        "why": "This field moves at news-cycle speed — the CVP expansion broke days before this course's updatedAt date, and METR revises its horizon model as new data lands.",
        "how": "Noah's course-aware tutoring tracks which of your notes cite fast-moving claims (CVP tiers, horizon numbers, program results) and flags them for re-verification against primary sources as the field moves. When a claim you learned is superseded, Noah re-teaches the update and re-tests you on it via SM-2 — your knowledge stays current because your tutor never goes stale.",
        "rule": "Noah re-verifies against primaries; trade-press awareness never becomes citation. Date-stamps on every claim, always."
    },
    "moduleAssignments": [
        {"moduleId": mid, "persona": p, "hook": h}
        for mid, (p, h) in NOAH_ASSIGN.items()
    ],
    "integrationPoints": [
        "'Ask Noah about this lesson' in every module header (course-aware context prefill; you press send).",
        "Struggle nudges: two consecutive misses on a drill item surface an inline Noah offer (max one per module per session).",
        "End-of-module 'Check my understanding with Noah': Socratic quiz from the module's objectives.",
        "Noah never claims to be Muse or any other assistant — the honesty guardrail is baked into every session."
    ],
}

HONESTY = ("This is an independent professional-practice course on AI red-teaming and safety evaluation engineering. "
    "It is not affiliated with, endorsed by, or sponsored by METR, Anthropic, OpenAI, XBOW, or any other lab, vendor, or employer; "
    "it confers no certificate and grants no credentials. All claims about METR/RE-Bench, Anthropic's Cyber Verification Program and "
    "Project Glasswing, XBOW, and published research reflect publicly published information as of October 2026 — always verify against "
    "the original sources. This course evaluates and defends AI systems; it teaches no offensive attack techniques.")

OBJECTIVES = [
    "Define AI red-teaming as a defensive engineering practice and map classic threat models onto AI systems.",
    "Classify prompt injection and jailbreak techniques by published taxonomy and design defensive test batteries per class.",
    "Design complete evals: construct, stratified suites, grader stacks, baselines, power analysis, threats to validity.",
    "Distinguish capability, safety, and alignment evals and select the right family for a deployment question.",
    "Explain METR's RE-Bench and time-horizon methodology — including what the metrics do NOT claim.",
    "Build sandboxed agent-eval harnesses with trajectory logging, checkpoint scoring, and blast-radius control.",
    "Run defensive cyber-capability evals: validated findings, tiered access, coordinated disclosure.",
    "Execute bias/fairness evals with published methodologies: disaggregation, counterfactual pairs, honest limits.",
    "Use interpretability as eval evidence: probes, tracing, patching — knew vs used.",
    "Deliver professional red-team operations: scoping, RoE, evidence logs, risk-ordered reports, debriefs that drive fixes.",
]

SOURCE_LINKS = [
    {"url": "https://arxiv.org/abs/2503.14499", "name": "METR — Measuring AI Ability to Complete Long Tasks (Mar 2025)", "retrieved": "2026-10-09"},
    {"url": "https://en.wikipedia.org/wiki/METR", "name": "METR — Wikipedia (RE-Bench, time horizons, TH1.1)", "retrieved": "2026-10-09"},
    {"url": "https://www.cognitiverevolution.ai/can-ais-do-ai-r-d-reviewing-rebench-results-with-neev-parikh-of-metr/", "name": "Cognitive Revolution — Reviewing RE-Bench results with Neev Parikh (METR)", "retrieved": "2026-10-09"},
    {"url": "https://github.com/metr/autonomy-evals-guide/blob/HEAD/claude_3_7_sonnet_report.md", "name": "METR autonomy-evals-guide — Claude 3.7 Sonnet public eval report", "retrieved": "2026-10-09"},
    {"url": "https://aiweekly.co/alerts/anthropic-opens-three-tier-cvp-folding-in-project-glasswing", "name": "AI Weekly — Anthropic opens three-tier CVP, folding in Project Glasswing (Oct 2026)", "retrieved": "2026-10-09"},
    {"url": "https://cyberpress.org/anthropic-expands-cyber-verification-program/", "name": "CyberPress — Anthropic expands Cyber Verification Program (Oct 2026)", "retrieved": "2026-10-09"},
    {"url": "https://badsignal.ai/stories/anthropic-cyber-verification-tiers", "name": "Bad Signal — Anthropic's three cyber tiers (Oct 2026)", "retrieved": "2026-10-09"},
    {"url": "https://www.businesswire.com/news/home/20260318258057/en/XBOW-Raises-%24120M-to-Scale-its-Autonomous-Hacker", "name": "BusinessWire — XBOW raises $120M Series C (Mar 2026)", "retrieved": "2026-10-09"},
    {"url": "https://www.securityweek.com/autonomous-offensive-security-firm-xbow-raises-35-million/", "name": "SecurityWeek — XBOW raises $35M Series C extension (2026)", "retrieved": "2026-10-09"},
    {"url": "https://www.fastcompany.com/91547150/business-products-services-world-changing-ideas-2026", "name": "Fast Company — World Changing Ideas 2026 (XBOW winner, business products)", "retrieved": "2026-10-09"},
    {"url": "https://scienmag.com/unchaotic-agents-why-ai-failures-may-be-a-design-problem-not-a-technology-problem/", "name": "ScienMag — Unchaotic Agents: AI failures as design problem (AI & Society forum, 2026)", "retrieved": "2026-10-09"},
    {"url": "https://manageria.biz/2026/09/30/autonomous-ai-agents-are-exposing-a-global-control-problem/", "name": "Manageria — Autonomous AI agents and the control problem (Sep 2026)", "retrieved": "2026-10-09"},
    {"url": "https://interstitiumlabs.dev/pdf-library/", "name": "Interstitium Labs — Visual Guide PDF library", "retrieved": "2026-10-09"},
]

GLOSSARY = [
    {"term": "Red-teaming (AI)", "def": "Authorized, scoped adversarial probing of an AI system to find weaknesses so defenders can fix them before deployment."},
    {"term": "Threat model", "def": "Assets, actors, attack surfaces, and impact paths for a system — the first deliverable of every engagement."},
    {"term": "Impact path", "def": "The end-to-end chain from an AI weakness to real-world harm."},
    {"term": "Direct / indirect prompt injection", "def": "Malicious instructions in user input (direct) vs smuggled through data the system reads (indirect)."},
    {"term": "Jailbreak", "def": "Input crafted to make a model violate its safety policy; measured per attack class as a success rate."},
    {"term": "Instruction hierarchy", "def": "Priority ordering: system/developer instructions > user input > tool output/data."},
    {"term": "Capability eval", "def": "Measures what a system CAN do — the upper bound of ability."},
    {"term": "Safety eval", "def": "Measures whether a system avoids harm under adversarial conditions."},
    {"term": "Alignment eval", "def": "Tests whether the system pursues intended goals rather than merely scoring well."},
    {"term": "Construct validity", "def": "Whether an eval actually measures the property it claims to measure."},
    {"term": "RE-Bench", "def": "METR's benchmark of 7 open-ended ML research-engineering tasks with calibrated human baselines."},
    {"term": "Time horizon (50%/80%)", "def": "The human-expert task duration at which the fitted curve predicts 50%/80% agent success."},
    {"term": "Sandbox", "def": "Isolated execution environment for agent evals: egress control, synthetic fixtures, logging, rollback."},
    {"term": "Trajectory", "def": "The full logged record of an agent run: plans, tool calls, observations, timestamps."},
    {"term": "Checkpoint scoring", "def": "Scoring intermediate milestones in long-horizon tasks, not just final success."},
    {"term": "Validated finding", "def": "A vulnerability confirmed as real and reproducible with evidence — the only kind that counts."},
    {"term": "Coordinated disclosure", "def": "Private notification, bounded fix window, then public release — the professional vulnerability pipeline."},
    {"term": "Counterfactual pair", "def": "Two inputs identical except the protected attribute; isolates its effect on outputs."},
    {"term": "Disaggregated eval", "def": "Metrics reported sliced by group rather than as a single aggregate."},
    {"term": "Probe", "def": "A simple classifier on activations testing whether a concept is represented."},
    {"term": "Activation patching", "def": "Swapping activations between runs to test causal contribution to a behavior."},
    {"term": "Knew vs used", "def": "Information present in activations ('knew') vs causally driving output ('used') — safety claims need the latter."},
    {"term": "Rules of engagement", "def": "Written authorization, permitted/prohibited techniques, comms, stop conditions, data handling for a test."},
    {"term": "Canary item", "def": "Secret test item whose appearance in training data signals contamination."},
    {"term": "SM-2", "def": "Spaced-repetition scheduling algorithm driving Noah's adaptive review: intervals stretch on recall, collapse on misses."},
]

FAQ = [
    {"q": "Is this a hacking course?", "a": "No. It is a defensive evaluation course: you learn to recognize attack classes, measure whether systems resist them, and report findings responsibly. No offensive techniques are taught."},
    {"q": "Does it prepare me for a certification?", "a": "No vendor certification exists for AI red-teaming as of October 2026. Adjacent threat concepts overlap CompTIA Security+ domains, but this course is professional practice, not exam prep."},
    {"q": "Do I need to be a machine-learning expert?", "a": "No — but you need the M00 statistics spine and basic Python. The course teaches eval engineering, not model training."},
    {"q": "How does Noah tutoring work here?", "a": "Five personas (Trickster, Engineer, Philosopher, Sage, Sentinel) with distinct voices tutor you per module: sparring, build coaching, debates, SM-2 review, and ethics guardianship. Noah is course-aware — it knows your module, your misses, and your lab progress — and it flags fast-moving claims for re-verification as the field changes."},
    {"q": "How current is the content?", "a": "Updated October 9, 2026, including the October 6 CVP expansion. The field moves fast; Noah's staying-current system flags superseded claims for re-verification against primary sources."},
    {"q": "Is the course affiliated with METR, Anthropic, or XBOW?", "a": "No. It is independent and unaffiliated; all third-party claims reflect publicly published information with retrieved dates."},
]

def build():
    total_min = sum(m["estimatedMinutes"] for m in MODULES)
    hours = round(total_min / 60)
    assert total_min == 6000, total_min
    assert hours == 100

    course = {
        "code": "IL-31",
        "courseId": "il-31-ai-red-teaming-safety-evals",
        "title": "IL-31 · AI Red-Teaming & Safety Evals Engineering",
        "tagline": "Evaluate, red-team, and harden frontier AI systems — the measurement discipline behind safe AI deployment.",
        "blurb": ("The AI industry learned to build agents faster than it learned to measure them. This course is the missing half: how to design "
                  "evaluations that honestly measure what frontier AI systems can and cannot do, how to red-team them like a professional, and how to "
                  "report findings responsibly. From METR's RE-Bench and time-horizon methodology to autonomous-agent eval harnesses, cyber capability "
                  "evals, bias and fairness methodologies, interpretability for evals, and responsible disclosure — every module is built on published "
                  "sources with an explicit defensive framing. Noah AI tutors you throughout: five personas spar, coach, debate, review, and guard your "
                  "practice, keeping you current in the fastest-moving field in technology."),
        "hours": hours,
        "mockMinutes": 120,
        "schemaVersion": "4",
        "updatedAt": "2026-10-09",
        "honestyNote": HONESTY,
        "objectives": OBJECTIVES,
        "arc": ("IL-31 takes you from measurement foundations to professional practice: first the statistics spine and threat-model vocabulary, then the "
                "attack-class taxonomy taught defensively, then the eval-design discipline. The middle third is the canonical methods — METR's measurement "
                "program, agent evals, defensive cyber evals, fairness, interpretability — each with published sources and honest limits. Then the "
                "professional layer: disclosure, harness engineering, engagement operations, live case studies, and the frontier agency debate. You finish "
                "with a full capstone engagement and an ethics gate you clear twice — the bar for practicing."),
        "priorities": [
            "Defensive framing is non-negotiable: every technique serves detection, evaluation, or mitigation.",
            "Validity discipline: baselines, power, contamination controls, threats-to-validity — on every number.",
            "Honest attribution: every third-party claim carries source, date, and methodology limits.",
            "Noah-driven tutoring: personas spar, coach, debate, review, and guard — personalized to your module and your misses.",
        ],
        "battlePlan": [
            "Weeks 1–2 — Foundations (M00–M02): statistics spine, threat models, injection taxonomy. Sage and Trickster carry you.",
            "Weeks 3–4 — Eval design + METR (M03–M04): the design discipline and the canonical measurement program.",
            "Weeks 5–7 — Method core (M05–M08): agent evals, defensive cyber evals, fairness, interpretability. Engineer, Sentinel, Philosopher rotate in.",
            "Weeks 8–9 — Professional layer (M09–M12): disclosure, harness build, engagement ops, case teardowns.",
            "Week 10 — Frontier + capstone (M13–M14): the agency debate, then the full engagement.",
            "Week 11 — Gate (M15): portfolio defense, ethics code, signed commitment. Clear it twice.",
        ],
        "modules": MODULES,
        "noahTutoring": NOAH_TUTORING,
        "crosswalk": [
            {"cert": "CompTIA Security+ SY0-701 (ADJACENT, partial)",
             "modules": ["IL31-M01", "IL31-M02", "IL31-M06", "IL31-M09", "IL31-M11"],
             "note": "Independent preparation aligned to published SY0-701 domains: Domain 2.0 Threats/Vulnerabilities/Mitigations (threat concepts, attack surfaces) and Domain 4.0 Security Operations (incident/disclosure workflow). This is NOT a Security+ prep course — the objective is professional AI-eval practice."}
        ],
        "certGates": [
            {"id": "gate-security-plus-adjacent", "cert": "CompTIA Security+ SY0-701 (adjacent threat concepts only)",
             "trackModule": "IL31-M01",
             "framing": "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate.",
             "format": "Up to 90 questions, 90 minutes, passing score 750/900 (vendor-published format, verify current objectives before booking)",
             "minutes": 90, "questionCount": 90,
             "note": "Covers only the adjacent threat-concept overlap (M01/M02/M06/M09/M11). IL-31 does not prepare you for the full exam and claims no alignment beyond the noted domains."}
        ],
        "readinessDashboard": {
            "title": "IL-31 Professional Practice Readiness Dashboard",
            "framing": "Independent preparation. Not affiliated with, endorsed by, or sponsored by any vendor or institution; confers no certificate.",
            "concept": "Readiness here is portfolio + ethics, not an exam score: the M14 capstone package, the M10 harness, and the M15 gate cleared twice on different days.",
            "formula": "readiness = (capstone accepted) AND (gate cleared twice, separate days)",
            "statusLabels": ["not started", "in progress", "capstone delivered", "gate 1 cleared", "ready"],
            "rule": "Two consecutive gate clears on separate days. No certificate is conferred — readiness means fit to practice under the ethics code."
        },
        "scriptLabs": [],
        "drills": [{"moduleId": m["id"], "drillIds": [d["id"] for d in m["drills"]]} for m in MODULES],
        "scenarios": [
            {"id": "il31-scen-01", "title": "The hospital deployment decision", "brief": "A hospital wants a triage-support agent. You have a capability eval, a safety eval, and no alignment evidence. Recommend ship / ship-with-controls / don't ship, with the eval gaps named."},
            {"id": "il31-scen-02", "title": "The unresponsive vendor", "brief": "Critical model-level flaw, vendor silent after 60 days. Walk the M09 hard-case playbook: document, escalate, decide on redacted publication."},
            {"id": "il31-scen-03", "title": "The too-good benchmark", "brief": "A vendor's 99% safety score lands on your desk. Tear it down with M00–M04: baselines, n, contamination, grader, validity."},
        ],
        "trainers": [],
        "terminalSims": [],
        "mockTasks": [{"moduleId": m["id"], "mockTaskId": m["mockTask"]["id"]} for m in MODULES],
        "cheatSheets": [
            {"id": "il31-cheat-threatmodel", "title": "Threat-model one-pager", "covers": "M01: assets, actors, surfaces, impact paths."},
            {"id": "il31-cheat-taxonomy", "title": "Injection taxonomy card", "covers": "M02: four branches, evaluator detection notes."},
            {"id": "il31-cheat-evalplan", "title": "Eval-plan canvas", "covers": "M03: the five parts, pre-registration checklist."},
            {"id": "il31-cheat-horizons", "title": "Reading horizons honestly", "covers": "M04: definition, trend, limits, misreadings."},
            {"id": "il31-cheat-disclosure", "title": "Disclosure playbook", "covers": "M09: report parts, timeline, hard cases."},
            {"id": "il31-cheat-ethics", "title": "Ethics code card", "covers": "M15: the five lines, from memory."},
        ],
        "answerBank": {"note": "Answers and explanations ship inline with every quiz, drill, and mock task — no separate bank to leak.", "entries": []},
        "sourceLinks": SOURCE_LINKS,
        "toolLabs": [],
        "multicloudLabs": [],
        "sampleDatasets": [
            {"id": "il31-data-synth-triage", "title": "Synthetic triage-screening dataset", "brief": "1,000 synthetic applicant profiles for the M07 fairness lab — planted group gap, documented generation seed."},
            {"id": "il31-data-synth-vuln-apps", "title": "Synthetic vulnerable apps", "brief": "10 intentionally flawed toy applications as authorized targets for the M06 cyber-eval lab — your code, your scope."},
        ],
        "installSteps": [
            "Python 3.11+ with pip.",
            "A working container runtime (Docker or equivalent) for the M05/M10 sandbox adapter.",
            "Git for versioning suites and run records.",
            "No model weights required: all labs run against stubs, synthetic targets, or APIs you already hold credentials for.",
        ],
        "installPrereqOrder": ["Python", "container runtime", "git"],
        "installLabs": [],
        "employerMappings": [
            {"role": "AI Eval Engineer", "modules": ["IL31-M03", "IL31-M04", "IL31-M05", "IL31-M10"], "note": "Build and run eval harnesses; report with validity discipline."},
            {"role": "AI Red-Team Operator", "modules": ["IL31-M01", "IL31-M02", "IL31-M11", "IL31-M14"], "note": "Scoped engagements: threat models, probing, reports that drive fixes."},
            {"role": "Trust & Safety / Deployment Safety", "modules": ["IL31-M03", "IL31-M06", "IL31-M07", "IL31-M09"], "note": "Pre-deployment gates, disclosure pipelines, fairness review."},
            {"role": "AI Safety Researcher (evals)", "modules": ["IL31-M04", "IL31-M08", "IL31-M13", "IL31-M14"], "note": "Novel eval methods; frontier behavior measurement."},
        ],
        "jdMatrix": {"note": "Junior/associate-level eval and red-team support roles: evidence of harness work (M10), a complete engagement package (M14), and the ethics code (M15) are the hiring signals. No certificate exists; the portfolio is the credential.", "rows": []},
        "sqlPlaygrounds": [],
        "pythonExercises": [
            {"id": "il31-py-power", "title": "Power analysis by hand (M00 lab)", "brief": "Two-proportion z-test and empirical power curves in stdlib Python."},
            {"id": "il31-py-horizon", "title": "Horizon fit on synthetic data (M04 lab)", "brief": "Logistic fit of success ~ log(duration); suite-sensitivity stress tests."},
            {"id": "il31-py-trajectory", "title": "Trajectory validator (M05 lab)", "brief": "Schema validation + checkpoint recomputation; catches fabricated success."},
            {"id": "il31-py-fairness", "title": "Disaggregated fairness eval (M07 lab)", "brief": "Sliced metrics with CIs + counterfactual flip rates on synthetic data."},
            {"id": "il31-py-probe", "title": "Probe-then-patch (M08 lab)", "brief": "Linear probe with shuffled-label control; activation-patching attempt."},
            {"id": "il31-py-harness", "title": "Eval harness core (M10 lab)", "brief": "Runner, grader stack, append-only result store, generated reporter."},
        ],
        "daxPlaygrounds": [],
        "branchingScenarios": [
            {"id": "il31-branch-disclosure", "title": "The disclosure dilemma", "brief": "Branching: vendor responsive / slow / hostile × flaw severity — choose the playbook at each node (M09)."},
            {"id": "il31-branch-scope", "title": "Scope creep at midnight", "brief": "Branching: undocumented API discovered mid-engagement — log, amend, or stop? (M11)."},
        ],
        "clickSims": [],
        "interactivityAudit": {
            "terminalSims": 0, "branchingScenarios": 2, "clickSims": 0, "toolLabs": 0,
            "installLabs": 0, "multicloudLabs": 0, "trainers": 0, "scriptLabs": 0,
            "cheatSheets": 6, "pythonExercises": 6,
            "totalInteractive": 14,
            "rule": "Every module ships notes, flashcards, quiz, drills, a hands-on lab, and a mock task; interactivity is counted, not claimed."
        },
        "studyGuide": {
            "title": "Study guide: how to work IL-31 in 11 weeks",
            "totalHours": hours, "totalMinutes": total_min,
            "note": "Pacing below; Noah's SM-2 review runs daily throughout.",
            "pacing": [
                "Weeks 1–2 — Foundations (M00–M02): stats spine, threat models, taxonomy. Daily SM-2 with Sage; spar with Trickster.",
                "Weeks 3–4 — Design + METR (M03–M04): eval plans, horizons. Replicate the horizon fit; read every number with its caveats.",
                "Weeks 5–7 — Method core (M05–M08): agent evals, cyber evals, fairness, interpretability. Build the sandbox spec and trajectory validator.",
                "Weeks 8–9 — Professional layer (M09–M12): disclosure package, harness build (3 sessions), tabletop engagement, case teardowns.",
                "Week 10 — Frontier + capstone (M13–M14): known-unknowns brief, then the six-session engagement.",
                "Week 11 — Gate (M15): portfolio defense, ethics code from memory, signed commitment. Clear twice.",
            ],
        },
        "timeFormula": "estimatedMinutes per module = instruction + videos + drills + hands-on lab, set per module by the author; course total = sum of module estimates. Declared hours are the honest rounded sum.",
        "glossary": GLOSSARY,
        "faq": FAQ,
        "tips": [
            "Read every third-party number with attribution, date, methodology, independence — price, don't parrot.",
            "Write the threats-to-validity section before you run the eval, when you can still fix the design.",
            "The payload rule is architectural: specs and oracles in the repo, payloads never.",
            "Disaggregate everything: aggregates hide the gaps that matter.",
            "Ask Noah early and often — struggle nudges exist because stuck is where learning happens.",
        ],
        "legends": {"note": "No invented legends, testimonials, or placement claims appear in this course.", "entries": []},
        "topicTheme": "sentinel",
        "topic": "ai-safety-evals",
    }
    return course

if __name__ == "__main__":
    course = build()
    out = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/il-31-ai-red-teaming-safety-evals.json")
    tmp = out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(course, f, indent=1, ensure_ascii=False)
        f.write("\n")
    # validate before replacing
    with open(tmp) as f:
        check = json.load(f)
    assert check["schemaVersion"] == "4"
    assert check["hours"] == round(sum(m["estimatedMinutes"] for m in check["modules"]) / 60) == 100
    assert len(check["modules"]) == 16
    os.replace(tmp, out)
    # content hash for the audit
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("WROTE", out)
    print("hours:", check["hours"], "| modules:", len(check["modules"]), "| sha256:", h[:16])
    # per-module quick stats
    for m in check["modules"]:
        req = ["id","code","title","summary","objectives","estimatedMinutes","weight","prerequisiteFor","crossLinks","cards","quiz","drills","handsOnLab","mockTask","videos","pdfs","notes","noahTutor"]
        missing = [k for k in req if k not in m]
        print(m["id"], m["estimatedMinutes"], "min | cards", len(m["cards"]), "| quiz", len(m["quiz"]), "| drills", len(m["drills"]), "| videos", len(m["videos"]), "| pdfs", len(m["pdfs"]), "| notes", len(m["notes"]), "| MISSING:", missing or "none")
