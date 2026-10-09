#!/usr/bin/env python3
"""Group C v4 build: IL-13..IL-18 course-spec-clone builds.
Writes spec-verified JSON upgrades; validates everything after write.
Run: python3 build_group_c.py
"""
import json, os, copy, shutil

BASE = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')

FRAMING = ("Independent practice and preparation. Not affiliated with, endorsed by, "
           "or sponsored by any vendor or employer; confers no certificate.")

REQUIRED_MODULE_FIELDS = ["id","code","title","summary","objectives","estimatedMinutes",
    "weight","prerequisiteFor","crossLinks","cards","quiz","drills","handsOnLab",
    "mockTask","videos","pdfs","notes"]

V4_TOP = ["code","courseId","title","tagline","blurb","hours","mockMinutes",
    "schemaVersion","updatedAt","honestyNote","objectives","arc","priorities",
    "battlePlan","modules","crosswalk","certGates","readinessDashboard",
    "scriptLabs","drills","scenarios","trainers","terminalSims","mockTasks",
    "cheatSheets","answerBank","sourceLinks","toolLabs","multicloudLabs",
    "sampleDatasets","installSteps","installPrereqOrder","installLabs",
    "employerMappings","jdMatrix","sqlPlaygrounds","pythonExercises",
    "daxPlaygrounds","branchingScenarios","clickSims","interactivityAudit",
    "studyGuide","timeFormula","glossary","faq","tips","legends","topicTheme","topic"]

FILES = {
    'IL-13': 'il-13-software-engineering-interview-prep.json',
    'IL-14': 'il-14-sre-devops-cloud-security-interview-prep.json',
    'IL-15': 'il-15-data-engineering-analytics-interview-prep.json',
    'IL-16': 'il-16-machine-learning-ai-engineering.json',
    'IL-17': 'il-17-agentic-ai-engineering.json',
    'IL-18': 'il-18-technical-leadership-interview-prep.json',
}

TIME_FORMULA = ("estimatedMinutes per module = 60 (orientation) + 15/note + 2/card + "
    "3/quiz item + 10/drill item + 60 (hands-on lab), rounded to 5; "
    "course hours = rounded sum of module minutes.")

# ---------------------------------------------------------------- M00 modules
M00_IL16 = {
  "id": "IL-16-M00",
  "code": "IL-16",
  "title": "M00 · Math Readiness Spine for ML & AI Engineering",
  "summary": ("Orientation to the course's math spine: how the three prereq math modules "
    "(Statistics & Probability, Linear Algebra, Discrete Mathematics) and the IL-02 "
    "Mathematical Maturity Engine modules map onto every ML/AI track in this course. "
    "Work this first: it tells you exactly which math each later module assumes."),
  "objectives": [
    "Map each ML/AI track in this course to the math it assumes.",
    "Place yourself on the IL-02 math spine (logic, statistics, linear algebra, discrete math).",
    "Schedule the three PM math modules before the technical tracks that need them.",
    "Identify which math gaps to close first using the diagnostic drills.",
    "State, in your own words, where statistics, linear algebra, and discrete math each show up in the applied ML workflow."
  ],
  "estimatedMinutes": 240,
  "weight": 1,
  "prerequisiteFor": ["IL-16-PM-STATS","IL-16-PM-LINALG","IL-16-PM-DISCRETE"],
  "crossLinks": ["IL-16-PM-STATS","IL-16-PM-LINALG","IL-16-PM-DISCRETE"],
  "cards": [
    {"front":"Which three math modules form this course's prereq math spine?","back":"IL-16-PM-STATS (Statistics & Probability), IL-16-PM-LINALG (Linear Algebra), IL-16-PM-DISCRETE (Discrete Mathematics) — drawn from the IL-02 Mathematical Maturity Engine."},
    {"front":"Where does probability show up in the applied ML workflow?","back":"Evaluation metrics (precision/recall), confidence intervals, A/B model comparisons, calibration of probabilistic models, and alert triage math (Bayes' theorem)."},
    {"front":"Where does linear algebra show up in ML?","back":"Data as vectors/matrices, dot products in embeddings and attention, matrix factorization, eigen-decomposition in PCA, and the weight matrices of neural networks."},
    {"front":"Where does discrete math show up in ML engineering?","back":"Combinatorial counting (feature interactions, hyperparameter grids), set logic (data filtering joins), graph structures (pipelines, attention as graphs), and induction-style reasoning about algorithms."},
    {"front":"Why is calculus needed for deep learning?","back":"Gradient-based optimization: backpropagation is the chain rule applied to the loss; learning rates, curvature, and convergence all rest on derivatives."},
    {"front":"What is the bias–variance tradeoff in one sentence?","back":"Total error decomposes into bias² + variance + irreducible noise — simple models underfit (high bias), complex models overfit (high variance)."},
    {"front":"What does the IL-02 'Unified Mathematical Spine' module give you?","back":"The through-line connecting logic, statistics, linear algebra, and discrete math into one reasoning system — the reference layer behind the three PM modules."},
    {"front":"Rule of thumb for when to take each PM module?","back":"STATS before any evaluation/modeling module; LINALG before embeddings, transformers, and deep architectures; DISCRETE before pipelines, graphs, and search/optimization reasoning."}
  ],
  "quiz": [
    {"q":"An ML course covers evaluation metrics, attention, and hyperparameter grids. Which math strand supports each?","choices":["Stats → metrics; linear algebra → attention; discrete → grids","Discrete → metrics; stats → attention; linear algebra → grids","Linear algebra → metrics; discrete → attention; stats → grids","Calculus covers all three"],"answer":0,"explain":"Statistics owns evaluation (metrics, intervals, tests); linear algebra owns attention (Q/K/V projections) and embeddings; discrete math owns counting structures like hyperparameter grids."},
    {"q":"You must take one PM module before 'Transformer Architectures'. Which is most urgent?","choices":["IL-16-PM-DISCRETE","IL-16-PM-LINALG","IL-16-PM-STATS","None — skip math"],"answer":1,"explain":"Transformers are linear algebra: query/key/value projections, dot-product attention, matrix multiplications. LINALG is the direct prerequisite."},
    {"q":"Which IL-02 module is the reference layer behind all three PM modules?","choices":["Tech Math","The Unified Mathematical Spine","Electrician Apprenticeship","Quantitative Finance Mathematics"],"answer":1,"explain":"The Unified Mathematical Spine connects logic, statistics, linear algebra, and discrete math into one system."},
    {"q":"A teammate says 'deep learning needs no math, the framework handles it.' The correct response:","choices":["Agree — autograd replaces understanding","Agree for applied work","Disagree — debugging training (divergence, NaNs, plateaus) requires calculus and linear algebra","Disagree — only statistics matters"],"answer":2,"explain":"Frameworks compute gradients; humans diagnose why training fails — learning-rate/divergence, vanishing/exploding gradients, and conditioning are calculus and linear-algebra questions."},
    {"q":"Bias–variance: a model has 2% training error and 31% validation error. What is it doing?","choices":["Underfitting (high bias)","Overfitting (high variance)","Perfectly calibrated","Data leakage"],"answer":1,"explain":"Huge train/validation gap with low training error is the signature of overfitting: low bias, high variance."},
    {"q":"Where does Bayes' theorem appear in this course's ML tracks?","choices":["Only in the stats PM module","Model calibration, anomaly-detector triage, and A/B decision reasoning","Nowhere — ML is frequentist","Only in NLP"],"answer":1,"explain":"Bayes updates beliefs with evidence: calibrated probabilities, detector triage (base rates), and interpreting A/B test outcomes all use it."}
  ],
  "drills": [
    {"id":"il-16-m00-drill-1","title":"Spine mapping drills","items":[
      {"prompt":"List, from memory, the three PM math modules and the one-line math strand each covers.","answer":"PM-STATS: probability & statistics; PM-LINALG: vectors, matrices, eigen; PM-DISCRETE: counting, sets, graphs, induction.","explain":"This is the spine map you will use all course."},
      {"prompt":"For 'Embeddings' (advanced-nlp-practice--embeddings-practice), name the primary math strand.","answer":"Linear algebra — embeddings are learned vector representations; similarity is dot product / cosine.","explain":"Any module about vectors and similarity is linear algebra."},
      {"prompt":"For 'GenAI Evaluation', name the primary math strand.","answer":"Statistics & probability — metrics, confidence, significance, and calibration.","explain":"Evaluation is applied statistics."},
      {"prompt":"For 'ML Pipelines', name the primary math strand.","answer":"Discrete math — DAGs, set operations on data, combinatorial validation splits.","explain":"Pipelines are graphs; discrete structures."},
      {"prompt":"Write the M00 study order for yourself: which PM module first and why?","answer":"Open answer — must justify from the tracks you plan to take (e.g., evaluation-heavy → STATS first).","explain":"The order follows your track plan, not a fixed sequence."}
    ]},
    {"id":"il-16-m00-drill-2","title":"Self-placement drills","items":[
      {"prompt":"Without notes: state the chain rule for d/dx f(g(x)).","answer":"f′(g(x)) · g′(x).","explain":"The atomic operation of backpropagation."},
      {"prompt":"Without notes: what is a dot product of [1,2,3] and [4,5,6]?","answer":"1·4+2·5+3·6 = 4+10+18 = 32.","explain":"The atomic operation of attention and similarity."},
      {"prompt":"Without notes: P(A|B) in terms of P(B|A)?","answer":"P(A|B) = P(B|A)·P(A)/P(B).","explain":"Bayes' theorem — the triage formula."},
      {"prompt":"Score yourself 1–5 on each: calculus, linear algebra, probability, discrete math. Which PM module do you take first?","answer":"Open answer — the lowest score with the earliest track dependency wins.","explain":"Honest self-placement beats syllabus order."},
      {"prompt":"Name two IL-02 modules beyond the spine that could help an ML engineer.","answer":"Quantitative Finance Mathematics (optimization under uncertainty) and Tech Math (trade-applied computation).","explain":"IL-02 is a library, not just a spine — use the shelf."}
    ]}
  ],
  "handsOnLab": {
    "title":"Build your personal math-gap map",
    "brief":"You will take the two drill groups, score yourself honestly per strand, and produce a dated study plan that schedules the three PM modules (and any IL-02 deep dives) before the technical tracks that assume them.",
    "steps":[
      "Do drill-1 from memory with the course module list open; write each track → math strand mapping in a table.",
      "Do drill-2 closed-book; score each strand 1–5 and record the scores with today's date.",
      "Open the IL-02 course map (modules: Logic & Boolean Algebra, Probability & Statistics, The Unified Mathematical Spine, Tech Math, Electrician Apprenticeship, Quantitative Finance Mathematics) and note any module that patches your weakest strand.",
      "Write your schedule: PM module order, which technical tracks follow each, and the IL-02 deep dives you will do alongside.",
      "Revisit this plan after finishing the first technical track and revise the scores."
    ],
    "deliverable":"Dated one-page math-gap map: strand scores, PM module order, IL-02 deep dives, and the technical-track sequence it unlocks."
  },
  "mockTask": {
    "q":"A colleague asks: 'Do I really need the math modules before the transformer track?' Give the two-sentence answer you would use.",
    "choices":["\"No — the framework handles the math, skip to transformers.\"","\"Yes — transformers are linear algebra (Q/K/V projections, attention scores); without it you can run the code but cannot debug it.\"","\"Only the statistics module matters for transformers.\"","\"Take discrete math instead; transformers are graphs.\""],
    "answer":1,
    "explain":"Transformers are matrix computation throughout; LINALG is the debugging toolkit for them.",
    "id":"il-16-m00-mock"
  },
  "videos": "__COPY_KHAN_IL16__",
  "pdfs": "__COPY_MATHPDFS_IL16__",
  "notes": [
    {"title":"How to use this module","body":"This is an orientation module, not a math course. Its job is placement and sequencing: read the spine map, do the self-placement drills honestly, and schedule the three PM modules (IL-16-PM-STATS, IL-16-PM-LINALG, IL-16-PM-DISCRETE) before the technical tracks that assume them. The math itself lives in the PM modules and in IL-02 — this module tells you which shelf to pull from and when."},
    {"title":"The IL-02 source shelf","body":"The prereq math content in this course is drawn from IL-02 · Mathematical Maturity Engine: Logic & Boolean Algebra (il-02-mathematical-maturity-engine-math-logic), Probability & Statistics (il-02-mathematical-maturity-engine-math-stats), The Unified Mathematical Spine (il02-math-spine), Tech Math (il02-tech-math), and Quantitative Finance Mathematics (il02-quant-math). If a PM module feels too fast, the corresponding IL-02 module is the slower, deeper treatment."},
    {"title":"Track → math dependency map","body":"Evaluation, calibration, A/B comparisons → STATS. Embeddings, attention, transformers, PCA, deep architectures → LINALG. Pipelines (DAGs), hyperparameter grids, search, data structures → DISCRETE. Optimization and training dynamics → calculus (inside the deep-learning modules, reinforced by the Calculus-for-ML visual guide). Probabilistic ML → STATS + DISCRETE."}
  ]
}

M00_IL17 = {
  "id": "IL-17-M00",
  "code": "IL-17",
  "title": "M00 · Math Readiness Spine for Agentic AI Engineering",
  "summary": ("Orientation to the course's math spine: how the three prereq math modules "
    "(Logic & Proof, Statistics & Probability, Discrete Mathematics) and the IL-02 "
    "Mathematical Maturity Engine modules map onto agent loops, planning, multi-agent "
    "systems, and agent evaluation. Work this first: it tells you which math each "
    "agent track assumes."),
  "objectives": [
    "Map each agent track in this course to the math it assumes.",
    "Place yourself on the IL-02 math spine (logic, statistics, discrete math).",
    "Schedule the three PM math modules before the agent tracks that need them.",
    "State where logic, probability, and discrete math each appear in agent engineering: tool contracts, planning, evaluation.",
    "Build a dated study plan that closes your math gaps before the multi-agent and evaluation tracks."
  ],
  "estimatedMinutes": 240,
  "weight": 1,
  "prerequisiteFor": ["IL-17-PM-LOGIC","IL-17-PM-STATS","IL-17-PM-DISCRETE"],
  "crossLinks": ["IL-17-PM-LOGIC","IL-17-PM-STATS","IL-17-PM-DISCRETE"],
  "cards": [
    {"front":"Which three math modules form this course's prereq math spine?","back":"IL-17-PM-LOGIC (Logic & Proof), IL-17-PM-STATS (Statistics & Probability), IL-17-PM-DISCRETE (Discrete Mathematics) — drawn from the IL-02 Mathematical Maturity Engine."},
    {"front":"Where does logic show up in agent engineering?","back":"Tool contracts and schemas (preconditions/postconditions), planning as search over states, guardrail rules, and formal reasoning about what an agent is allowed to do."},
    {"front":"Where does probability show up in agent engineering?","back":"Agent evaluation: pass rates with confidence intervals, comparing two agents (A/B), trajectory sampling, and reasoning about stochastic LLM behavior."},
    {"front":"Where does discrete math show up in agent engineering?","back":"Planning as graph search (states, actions, branching factor), multi-agent coordination as graphs, combinatorics of tool choices, and token/context budgeting as counting."},
    {"front":"An agent succeeds on 8/10 eval tasks. What is the honest statistical statement?","back":"Point estimate 80%, but n=10 is tiny — the confidence interval is wide (~44–97% Wilson). Report the interval, not just the point."},
    {"front":"Why is the branching factor the key number in agent planning?","back":"b^d possible trajectories for branching factor b and depth d — it explodes exponentially, which is why agents need pruning, heuristics, and stopping conditions."},
    {"front":"What is a tool contract in logical terms?","back":"A Hoare-style triple: {precondition} tool {postcondition} — the agent may call the tool only when the precondition holds, and may assume the postcondition after."},
    {"front":"Rule of thumb for PM module order in this course?","back":"LOGIC before tool use, planning, and guardrails; STATS before agent evaluation and metrics; DISCRETE before multi-agent systems and planning depth."}
  ],
  "quiz": [
    {"q":"Which math strand supports 'Agent Evaluation' (trajectory quality, pass rates)?","choices":["Logic & proof","Statistics & probability","Discrete mathematics","Calculus"],"answer":1,"explain":"Evaluation is applied statistics: pass rates, confidence intervals, significance of comparisons between agents."},
    {"q":"An agent has branching factor 5 and plans 4 steps deep. How many possible trajectories?","choices":["20","625","120","25"],"answer":1,"explain":"5^4 = 625. Branching explodes exponentially — the core argument for pruning and stopping conditions."},
    {"q":"A tool's contract says it requires a valid order_id. In logical terms this is:","choices":["A postcondition","A precondition","An invariant of the whole system","A statistical prior"],"answer":1,"explain":"Preconditions must hold before the call; postconditions hold after. Guardrails enforce preconditions."},
    {"q":"Agent A: 78/100 tasks. Agent B: 82/100 tasks. Honest conclusion?","choices":["B is better — 82 > 78","A is better — more consistent","No significant difference at n=100; report intervals and re-run","Combine them"],"answer":2,"explain":"A 4-point gap at n=100 is inside noise. Report confidence intervals; a real comparison needs more runs or a significance test."},
    {"q":"Which IL-02 module is the reference layer behind all three PM modules?","choices":["Tech Math","The Unified Mathematical Spine","Electrician Apprenticeship","Quantitative Finance Mathematics"],"answer":1,"explain":"The Unified Mathematical Spine connects the strands into one reasoning system."},
    {"q":"Multi-agent coordination problems are naturally modeled as:","choices":["Continuous functions","Graphs — agents as nodes, messages as edges","Differential equations","Single-agent MDPs only"],"answer":1,"explain":"Coordination structure (who talks to whom, ordering, consensus) is graph structure — discrete math."}
  ],
  "drills": [
    {"id":"il-17-m00-drill-1","title":"Spine mapping drills","items":[
      {"prompt":"List the three PM modules and the agent tracks each unlocks.","answer":"PM-LOGIC → tool use, planning, guardrails/governance. PM-STATS → evaluation, metrics, A/B. PM-DISCRETE → multi-agent systems, planning search, context budgeting.","explain":"The spine map for agent engineering."},
      {"prompt":"For 'Agent Loops and Planning', name the primary math strand.","answer":"Discrete math (graph search) + logic (planning correctness).","explain":"Planning is search over a state graph with logical goals."},
      {"prompt":"For 'Trust and Guardrails', name the primary math strand.","answer":"Logic & proof — preconditions, invariants, allow/deny rules.","explain":"Guardrails are logical statements about permitted behavior."},
      {"prompt":"For 'Measuring Agent Impact', name the primary math strand.","answer":"Statistics & probability — metrics, intervals, experiment design.","explain":"Impact claims are statistical claims."},
      {"prompt":"Write your PM module order with justification.","answer":"Open answer — must tie each PM module to the agent tracks you plan to take first.","explain":"Order follows your track plan."}
    ]},
    {"id":"il-17-m00-drill-2","title":"Self-placement drills","items":[
      {"prompt":"Compute 4^3 and explain what it counts in agent planning.","answer":"64 — trajectories for branching factor 4, depth 3.","explain":"Counting trajectories is the first planning instinct."},
      {"prompt":"State Bayes' theorem and one agent-evaluation use.","answer":"P(H|E)=P(E|H)P(H)/P(E); e.g., updating the belief that a guardrail works after observing blocked attacks.","explain":"Evidence updates beliefs — evaluation is belief updating."},
      {"prompt":"Write a tool precondition for a 'refund_order' tool.","answer":"order exists AND order.status == 'paid' AND refund_amount <= order.total.","explain":"Preconditions are conjunctions of checkable facts."},
      {"prompt":"Score yourself 1–5 on logic, probability, discrete math. Weakest strand?","answer":"Open answer — the weakest strand with the earliest track dependency sets your PM order.","explain":"Honest placement beats syllabus order."},
      {"prompt":"Wilson interval intuition: why is 8/10 weaker evidence than 80/100?","answer":"Same point estimate, but n=10 gives a much wider interval — less data, less certainty.","explain":"Sample size is the hidden variable in every eval claim."}
    ]}
  ],
  "handsOnLab": {
    "title":"Build your personal math-gap map",
    "brief":"You will take the two drill groups, score yourself honestly per strand, and produce a dated study plan that schedules the three PM modules (and any IL-02 deep dives) before the agent tracks that assume them.",
    "steps":[
      "Do drill-1 from memory with the course module list open; write each track → math strand mapping in a table.",
      "Do drill-2 closed-book; score each strand 1–5 and record the scores with today's date.",
      "Open the IL-02 course map and note any module that patches your weakest strand (Logic & Boolean Algebra, Probability & Statistics, The Unified Mathematical Spine).",
      "Write your schedule: PM module order, which agent tracks follow each, and the IL-02 deep dives you will do alongside.",
      "Revisit this plan after the foundations track and revise the scores."
    ],
    "deliverable":"Dated one-page math-gap map: strand scores, PM module order, IL-02 deep dives, and the agent-track sequence it unlocks."
  },
  "mockTask": {
    "q":"A PM asks: 'Do engineers really need logic and stats to build agents?' Give the two-sentence answer.",
    "choices":["\"No — prompt engineering replaces both.\"","\"Yes — logic writes the guardrails and tool contracts that keep agents safe; statistics makes evaluation claims honest instead of anecdotal.\"","\"Only stats matters; logic is academic.\"","\"Only logic matters; evals are vibes.\""],
    "answer":1,
    "explain":"Guardrails are logic; evaluation is statistics. Both are load-bearing in production agents.",
    "id":"il-17-m00-mock"
  },
  "videos": "__COPY_KHAN_IL17__",
  "pdfs": [],
  "notes": [
    {"title":"How to use this module","body":"This is an orientation module, not a math course. Its job is placement and sequencing: read the spine map, do the self-placement drills honestly, and schedule the three PM modules (IL-17-PM-LOGIC, IL-17-PM-STATS, IL-17-PM-DISCRETE) before the agent tracks that assume them. The math itself lives in the PM modules and in IL-02 — this module tells you which shelf to pull from and when."},
    {"title":"The IL-02 source shelf","body":"The prereq math content in this course is drawn from IL-02 · Mathematical Maturity Engine: Logic & Boolean Algebra (il-02-mathematical-maturity-engine-math-logic), Probability & Statistics (il-02-mathematical-maturity-engine-math-stats), and The Unified Mathematical Spine (il02-math-spine). If a PM module feels too fast, the corresponding IL-02 module is the slower, deeper treatment."},
    {"title":"Track → math dependency map","body":"Tool use, planning, guardrails, governance → LOGIC (contracts, preconditions, search). Agent evaluation, metrics, A/B, impact measurement → STATS. Multi-agent systems, planning depth, context budgeting, combinatorics of tool choice → DISCRETE. The interview track (agentic-ai-for-iv) assumes all three: system design (discrete), LLM depth (probability), behavioral (none — stories are yours)."}
  ]
}

# ------------------------------------------------------------------ per-course
HONESTY = {
 'IL-13': ("This is an independent preparation and practice course aligned to publicly "
  "published interview formats and widely used interview rubrics. It is not affiliated "
  "with, endorsed by, or sponsored by any employer or interview-prep provider; it confers "
  "no certificate and grants no credentials. Interview facts (formats, round structures, "
  "rubric styles) reflect publicly described practices as of October 2026 — always verify "
  "against the hiring company's current process. Hours are honest estimates from the "
  "module workload formula."),
 'IL-14': ("This is an independent preparation and practice course aligned to publicly "
  "described interview formats and rubrics. It is not affiliated with, endorsed by, or "
  "sponsored by CNCF, AWS, HashiCorp, any employer, or any interview-prep provider; it "
  "confers no certificate and grants no credentials. Interview facts reflect publicly "
  "described practices as of October 2026. Hours are honest estimates from the module "
  "workload formula."),
 'IL-15': ("This is an independent preparation and practice course aligned to publicly "
  "described interview formats and rubrics. It is not affiliated with, endorsed by, or "
  "sponsored by AWS, Databricks, any employer, or any interview-prep provider; it confers "
  "no certificate and grants no credentials. Interview facts reflect publicly described "
  "practices as of October 2026. Hours are honest estimates from the module workload "
  "formula."),
 'IL-16': ("This is an independent preparation and practice course aligned to publicly "
  "published exam objectives and real ML/AI engineering practice. It is not affiliated "
  "with, endorsed by, or sponsored by AWS, Google, Microsoft, TensorFlow, or any employer; "
  "it confers no certificate and grants no credentials. Exam facts (domains, weights, "
  "question counts, durations, passing scores) reflect publicly published objectives as of "
  "October 2026 — always verify against the vendor's current published objectives before "
  "booking. The AWS Certified Machine Learning – Specialty (MLS-C01) exam was retired "
  "March 31, 2026 and is no longer bookable; AWS points ML candidates to the Machine "
  "Learning Engineer – Associate (MLA-C01). The TensorFlow Developer Certificate program "
  "was closed to new candidates on May 1, 2024 and is no longer bookable. Hours are "
  "honest estimates from the module workload formula."),
 'IL-17': ("This is an independent preparation and practice course aligned to publicly "
  "described agentic AI practices and interview formats. It is not affiliated with, "
  "endorsed by, or sponsored by AWS, Microsoft, Google, OpenAI, Anthropic, any model or "
  "framework provider, any employer, or any interview-prep provider; it confers no "
  "certificate and grants no credentials. Agentic AI is an emerging field — platform "
  "capabilities and best practices change quickly; facts reflect publicly described "
  "practice as of October 2026. Hours are honest estimates from the module workload "
  "formula."),
 'IL-18': ("This is an independent preparation and practice course aligned to publicly "
  "described interview formats and rubrics. It is not affiliated with, endorsed by, or "
  "sponsored by PMI, any employer, or any interview-prep provider; it confers no "
  "certificate and grants no credentials. Interview facts reflect publicly described "
  "practices as of October 2026. Hours are honest estimates from the module workload "
  "formula."),
}

CERTNOTES = {
 'IL-13': ("Technical interviews have no accredited certification; this course prepares "
  "performance, not credentials. No vendor track is mapped. Vendor certifications "
  "(e.g. AWS, GCP, CNCF) are separate exams administered by their vendors."),
 'IL-14': ("This is interview preparation, not vendor-exam preparation. Vendor "
  "certifications (e.g. CNCF CKA, AWS Certified DevOps Engineer, HashiCorp Terraform "
  "Associate) are separate exams administered by their vendors; the earlier per-track "
  "cert gates were removed to keep this course honest about its purpose. If you want a "
  "vendor cert, book it through the vendor's own portal after this course's mock "
  "circuits."),
 'IL-15': ("This is interview preparation, not vendor-exam preparation. Vendor "
  "certifications (e.g. AWS Certified Data Engineer, Databricks Certified Data "
  "Engineer) are separate exams administered by their vendors; the earlier per-track "
  "cert gates were removed to keep this course honest about its purpose."),
 'IL-16': ("Certification tracks are independent preparation aligned to each vendor's "
  "publicly published exam objectives as of October 2026. The AWS Certified Machine "
  "Learning – Specialty (MLS-C01) exam was retired March 31, 2026 — the active AWS "
  "machine-learning certification is the Machine Learning Engineer – Associate "
  "(MLA-C01). The TensorFlow Developer Certificate program was closed to new "
  "candidates on May 1, 2024 — its track below is historical skill-domain practice "
  "only and cannot be booked."),
 'IL-17': ("Agentic AI is an emerging field; as of October 2026 there is no established "
  "vendor certification track for agentic AI engineering. Earlier adjacent AI-practitioner "
  "cert gates were removed to keep this course honest about its purpose. Foundational "
  "AI/ML vendor certifications exist (e.g. AWS Certified AI Practitioner), but none "
  "certifies agentic-AI engineering specifically."),
 'IL-18': ("This is interview preparation, not vendor-exam preparation. PMI's PMP is a "
  "separate exam administered by PMI; the earlier PMP cert gate was removed to keep "
  "this course honest about its purpose. The internal Technical Leadership Interview "
  "Readiness gate is mock-based practice, not a certification."),
}

def interview_dashboard(code, title, concept_extra=""):
    return {
      "title": title,
      "framing": FRAMING,
      "concept": ("Each domain track ends in a mock circuit. You are ready to interview "
        "when you clear the mock circuits for your target domains twice in a row, on "
        "different days. " + concept_extra).strip(),
      "formula": "readiness = (mock1 rubric-pass) AND (mock2 rubric-pass), mocks on separate days",
      "thresholds": "Mock-circuit bar: timed conditions; 80%+ rubric scores on two consecutive mocks.",
      "statusLabels": ["not started","in progress","mock cleared once","ready"],
      "rule": "Two consecutive mock-circuit clears on different days before the real interview loop.",
      "order": []
    }

DASHBOARDS = {
 'IL-13': interview_dashboard('IL-13','IL-13 Interview Readiness Dashboard'),
 'IL-14': interview_dashboard('IL-14','IL-14 Interview Readiness Dashboard'),
 'IL-15': interview_dashboard('IL-15','IL-15 Interview Readiness Dashboard'),
 'IL-17': interview_dashboard('IL-17','IL-17 Build & Interview Readiness Dashboard',
     "Each applied track ends in a shipped project; the interview track ends in a mock circuit."),
 'IL-18': None,  # keep existing, fix order below
 'IL-16': None,  # keep existing
}

MERGE_NOTES = {
 'IL-13': {
   "complementaryCourses": [
     {"code":"IL-03","title":"Programming Language Forge","role":"foundation",
      "note":"IL-13 is the interview-performance layer on top of IL-03's language/DSA/systems foundation. Work IL-03 first if the foundations feel thin."}
   ],
   "crossLinkedModules": [
     {"from":"swe-interview-foundations--dsa-big-o","toCourse":"IL-03","to":"il03-programming-backbone","note":"Complexity analysis meets the programming backbone."},
     {"from":"il-13-software-engineering-interview-prep-math-discrete","toCourse":"IL-03","to":"il-03-programming-language-forge-math-discrete","note":"Discrete math depth behind the interview combinatorics."},
     {"from":"embedded-swe-interview-prep--c-memory","toCourse":"IL-03","to":"il03-systems-software","note":"C memory models meet systems software."}
   ],
   "frontierCites": []
 },
 'IL-14': {
   "complementaryCourses": [
     {"code":"IL-05","title":"Cloud, DevSecOps, Platform & SRE","role":"foundation",
      "note":"IL-05 teaches the systems; IL-14 teaches proving you can run them under interview conditions."},
     {"code":"IL-28","title":"DevSecOps & Cloud Infrastructure","role":"production mastery",
      "note":"IL-28 is the production-depth companion — subnetting, reliability math, and Linux essentials at operator depth."}
   ],
   "crossLinkedModules": [
     {"from":"devops-interview-prep--devops-ci-cd","toCourse":"IL-05","to":"il05-devops-core","note":"CI/CD interview reps meet DevOps at cloud-native parity."},
     {"from":"devops-interview-prep--devops-containers","toCourse":"IL-05","to":"il05-cloud-native","note":"Containers/orchestration meet the Kubernetes stack."},
     {"from":"devops-interview-prep--devops-iac","toCourse":"IL-05","to":"il05-terraform","note":"IaC patterns meet Terraform depth."},
     {"from":"sre-interview-prep--sre-sli-slo","toCourse":"IL-28","to":"IL28-M06","note":"SLIs/SLOs meet reliability math (MTBF, MTTR, percentiles)."},
     {"from":"cloud-interview-prep--cloud-networking","toCourse":"IL-28","to":"IL28-M03","note":"Cloud networking meets IP addressing/subnetting/CIDR."}
   ],
   "frontierCites": []
 },
 'IL-15': {
   "complementaryCourses": [
     {"code":"IL-07","title":"SQL, Data Engineering, Analytics & AI","role":"foundation",
      "note":"IL-07 teaches the data systems; IL-15 teaches proving it in interviews — SQL drills, case reps, and mock circuits."}
   ],
   "crossLinkedModules": [
     {"from":"data-eng-interview-prep--batch-pipelines","toCourse":"IL-07","to":"il07-data-schools","note":"Pipeline design meets the data-school spine."},
     {"from":"ml-interview-prep--ml-theory-iv","toCourse":"IL-07","to":"il07-ai-ml","note":"ML interview theory meets IL-07's ML/LLM engineering."},
     {"from":"data-eng-interview-prep--data-modeling-warehousing","toCourse":"IL-07","to":"il07-mongodb","note":"Warehousing meets document-database modeling."},
     {"from":"il-15-data-engineering-analytics-interview-prep-math-stats","toCourse":"IL-07","to":"il-07-data-engineering-analytics-ai-math-stats","note":"Stats depth behind the interview statistics."}
   ],
   "frontierCites": []
 },
 'IL-16': {
   "complementaryCourses": [
     {"code":"IL-12","title":"AI Engineering","role":"engineering track (two-way)",
      "note":"IL-12 is the AI engineering track (Python foundations, GenAI-assisted coding, LLM engineering); IL-16 is the applied-ML depth layer. Cross-link both ways."},
     {"code":"IL-07","title":"SQL, Data Engineering, Analytics & AI","role":"data foundation",
      "note":"Data preparation depth behind the ML workflow."}
   ],
   "crossLinkedModules": [
     {"from":"advanced-genai--transformer-arch-practice","toCourse":"IL-12","to":"il-12-ai-engineering-math-linalg","note":"Transformer math meets IL-12's linear-algebra spine."},
     {"from":"ai-enabled-software--llm-apis-practice","toCourse":"IL-12","to":"aieng-python-foundations--py-genai-workflow","note":"LLM features meet GenAI-assisted coding workflow."},
     {"from":"IL-16-PM-STATS","toCourse":"IL-12","to":"il-12-ai-engineering-math-stats","note":"Shared statistics spine."},
     {"from":"IL-16-PM-DISCRETE","toCourse":"IL-12","to":"il-12-ai-engineering-math-discrete","note":"Shared discrete-math spine."},
     {"from":"advanced-ml--re-bench-agents-ml-research","toCourse":"IL-23","to":"frontier-survey","note":"Frontier: agents doing ML research — see IL-23 (The Frontier) for the research survey."}
   ],
   "frontierCites": ["AI frontier topics (agents doing ML research) also surveyed in IL-23."]
 },
 'IL-17': {
   "complementaryCourses": [
     {"code":"IL-12","title":"AI Engineering","role":"engineering track (two-way)",
      "note":"IL-12 is the AI engineering track; IL-17 is the agentic layer on top of it (tool use, agent loops, evaluation). Cross-link both ways."}
   ],
   "crossLinkedModules": [
     {"from":"agentic-ai-foundations--llm-tool-use","toCourse":"IL-12","to":"aieng-python-foundations--py-genai-workflow","note":"Tool use meets the GenAI coding workflow."},
     {"from":"IL-17-PM-LOGIC","toCourse":"IL-12","to":"il-12-ai-engineering-math-discrete","note":"Logic & proof meet IL-12's discrete-math spine."},
     {"from":"IL-17-PM-STATS","toCourse":"IL-12","to":"il-12-ai-engineering-math-stats","note":"Shared statistics spine (evaluation math)."}
   ],
   "frontierCites": ["Agentic AI frontier topics (multi-agent research, eval research) also surveyed in IL-23."]
 },
 'IL-18': {
   "complementaryCourses": [
     {"code":"IL-10","title":"Portfolio, Career & Professional Practice","role":"foundation",
      "note":"IL-10 builds the career substrate (self-knowledge, entrepreneurship, career design); IL-18 is the leadership-interview performance layer."}
   ],
   "crossLinkedModules": [
     {"from":"em-interview-prep--people-leadership-em","toCourse":"IL-10","to":"il10-humanmetrics","note":"People leadership meets self-knowledge assessment."},
     {"from":"em-interview-prep--eng-strategy-vision","toCourse":"IL-10","to":"il10-fde-career","note":"Engineering strategy meets forward-deployed career design."},
     {"from":"pm-interview-prep--product-sense-iv","toCourse":"IL-10","to":"il10-entrepreneurship","note":"Product sense meets the entrepreneurship track."}
   ],
   "frontierCites": []
 },
}

# ------------------------------------------------- Noah tutoring integration
# Verified platform facts (docs/_worker.js, docs/assets/noah-personas.js,
# docs/assets/noah-adaptive.js, docs/university/data/noah-knowledge.md):
# - 5 personas: Visionary, Engineer, Philosopher, Mentor, Trickster (original
#   speaking styles; no real-person impersonation; sent as `persona` to POST /api/noah)
# - 5 natural voices: Scholar, Narrator, Guide, Sage, Spark (server-side TTS via
#   POST /api/noah/tts; 5 distinct neural voices; adaptive browser speech with
#   per-persona rate/pitch, emotion-aware TTS, lip-synced avatar)
# - Adaptive learning: SM-2-inspired spaced-repetition scheduler for review timing
# - Course-aware tutoring: POST /api/noah (Cloudflare Workers AI, Llama 3.1 8B)
#   fed by the course's knowledge; degrades to a local Socratic engine with a
#   plain notice if unreachable
# - House rule: "Bring Noah your hypothesis — not 'just give me the answer.'
#   Attempt a card first."

NOAH_PERSONAS = [
  {"id":"visionary","label":"Visionary","desc":"Bold, first-principles, future-focused",
   "voice":"spark","voiceLabel":"Spark — energetic, quick",
   "style":"Cuts to the fundamental truth, then projects forward. Challenges assumptions; frames everything as 'what could be.'"},
  {"id":"engineer","label":"Engineer","desc":"Precise, systems-thinking, pragmatic",
   "voice":"scholar","voiceLabel":"Scholar — measured, precise",
   "style":"Thinks in systems: inputs, outputs, constraints, failure modes. Concrete and actionable; quantifies; calls out trade-offs explicitly."},
  {"id":"philosopher","label":"Philosopher","desc":"Socratic, deep, questioning",
   "voice":"sage","voiceLabel":"Sage — deep, contemplative",
   "style":"Asks the question beneath the question. Never rushes to answers; dwells in inquiry; repairs mental models with graduated hints."},
  {"id":"mentor","label":"Mentor","desc":"Encouraging, practical wisdom",
   "voice":"guide","voiceLabel":"Guide — clear, encouraging",
   "style":"Notices effort and names it. Honest about difficulty; balances challenge with support; speaks like someone who has been where the learner is."},
  {"id":"trickster","label":"Trickster","desc":"Playful, lateral thinking, comedic",
   "voice":"narrator","voiceLabel":"Narrator — warm, engaging",
   "style":"Finds the absurd angle and the unexpected connection. Uses humor to illuminate; breaks fixation when the learner is stuck; kind, never punching down."},
]

# persona -> representative module ids per course
NOAH_MAPS = {
 'IL-13': [
   {"track":"Mock interview circuits","persona":"mentor",
    "modules":["swe-interview-foundations--swe-mock-circuit","backend-interview-prep--backend-mock","frontend-interview-prep--frontend-mock","fullstack-interview-prep--fullstack-mock","ios-interview-prep--ios-mock","android-interview-prep--android-mock","embedded-swe-interview-prep--embedded-mock","qa-test-interview-prep--qa-mock"],
    "why":"Mentor runs timed voice mock interviews: asks the question, enforces the clock, scores against the rubric, then debriefs like a hiring manager — encouragement first, then the exact gap to close before the next rep."},
   {"track":"System design","persona":"engineer",
    "modules":["swe-interview-foundations--sysdesign-core","swe-interview-foundations--sysdesign-build","backend-interview-prep--backend-design-build","frontend-interview-prep--frontend-systems","fullstack-interview-prep--fullstack-arch"],
    "why":"Engineer drills design trade-offs with systems precision: pushes on scale numbers, failure modes, and 'what breaks first' — the follow-ups real interviewers use."},
   {"track":"DSA depth","persona":"philosopher",
    "modules":["swe-interview-foundations--dsa-big-o","swe-interview-foundations--dsa-patterns","swe-interview-foundations--dsa-trees-graphs","swe-interview-foundations--dsa-dynamic","il-13-software-engineering-interview-prep-math-discrete"],
    "why":"Philosopher walks proofs Socratically: never hands the recurrence, asks the question that makes the recurrence obvious. Complexity reasoning that survives whiteboard pressure."},
   {"track":"Debugging and edge cases","persona":"trickster",
    "modules":["embedded-swe-interview-prep--embedded-debug","qa-test-interview-prep--test-strategy","frontend-interview-prep--frontend-machine-coding"],
    "why":"Trickster breaks fixation with lateral angles: the absurd edge case, the input nobody considered — exactly the mindset that finds bugs under interview pressure."},
   {"track":"Capstones and portfolio","persona":"visionary",
    "modules":["fullstack-interview-prep--fullstack-capstone","embedded-swe-interview-prep--embedded-capstone","ios-interview-prep--ios-guided-build","android-interview-prep--android-guided-build"],
    "why":"Visionary frames the capstone as first-principles architecture and a portfolio story: what this build proves about the engineer, in the language hiring managers hear."},
 ],
 'IL-14': [
   {"track":"Mock interview circuits","persona":"mentor",
    "modules":["sre-interview-prep--sre-mock","devops-interview-prep--devops-mock","cloud-interview-prep--cloud-mock","security-eng-interview-prep--sec-mock","tech-mock-interview-circuit--mock-full-loop","tech-mock-interview-circuit--mock-behavioral"],
    "why":"Mentor runs the full loop by voice: incident-command scenarios under the clock, then a rubric debrief. The behavioral story bank gets STAR coaching — specific, honest, tight."},
   {"track":"Reliability and troubleshooting","persona":"engineer",
    "modules":["sre-interview-prep--sre-sli-slo","sre-interview-prep--sre-incident-command","devops-interview-prep--devops-troubleshoot","cloud-interview-prep--cloud-arch-build","security-eng-interview-prep--sec-design-review"],
    "why":"Engineer narrates troubleshooting aloud with a repeatable method: symptoms, hypotheses, cheapest test first. Quantifies everything — error budgets, blast radius, MTTR."},
   {"track":"Systems reasoning","persona":"philosopher",
    "modules":["sre-interview-prep--sre-design-reps","tech-mock-interview-circuit--mock-sysdesign","security-eng-interview-prep--sec-crypto","il-14-sre-devops-cloud-security-interview-prep-math-logic"],
    "why":"Philosopher asks the question beneath the design: what invariant must hold, what assumption are you smuggling in — the Socratic layer behind reliable systems."},
   {"track":"Chaos angles","persona":"trickster",
    "modules":["devops-interview-prep--devops-troubleshoot","tech-mock-interview-circuit--mock-domains"],
    "why":"Trickster asks 'what breaks at 3am on a holiday' — the lateral failure modes that separate operators who have lived it from those who have read about it."},
   {"track":"Scale thinking","persona":"visionary",
    "modules":["sre-interview-prep--sre-capacity","cloud-interview-prep--cloud-concepts"],
    "why":"Visionary stretches capacity planning to 10x: first-principles scaling, the economics of reliability, where the architecture wants to go."},
 ],
 'IL-15': [
   {"track":"Mock interview circuits","persona":"mentor",
    "modules":["data-eng-interview-prep--de-mock","data-science-interview-prep--ds-mock","data-analyst-interview-prep--analyst-mock","ml-interview-prep--ml-mock","sql-analytics-drills--drill-circuit-final"],
    "why":"Mentor runs voice mock interviews: live SQL whiteboarding with narration coaching, case-study walkthroughs, and rubric debriefs. The drill-circuit finale is the gate."},
   {"track":"Pipeline and warehouse design","persona":"engineer",
    "modules":["data-eng-interview-prep--sql-for-de","data-eng-interview-prep--batch-pipelines","data-eng-interview-prep--streaming-systems","data-eng-interview-prep--data-modeling-warehousing","ml-interview-prep--ml-system-design"],
    "why":"Engineer drills pipeline trade-offs with precision: idempotency, exactly-once semantics, late data, backfill strategy — the design questions DE loops actually ask."},
   {"track":"Statistics and experimentation","persona":"philosopher",
    "modules":["data-science-interview-prep--stats-prob-iv","data-science-interview-prep--experimentation-ab","il-15-data-engineering-analytics-interview-prep-math-stats","ml-interview-prep--ml-theory-iv"],
    "why":"Philosopher makes statistics honest: what a p-value does not say, why peeking invalidates the test, the base-rate traps in every '99% accurate' claim."},
   {"track":"SQL edge cases","persona":"trickster",
    "modules":["sql-analytics-drills--sql-window-functions","sql-analytics-drills--sql-ctes-recursive","sql-analytics-drills--analytics-patterns"],
    "why":"Trickster serves the lateral SQL: the NULL that breaks the join, the window frame that silently changes the answer — edge-case fluency that reads as seniority."},
   {"track":"Capstones and business value","persona":"visionary",
    "modules":["data-eng-interview-prep--pipeline-capstone","ml-interview-prep--ml-capstone-project","data-analyst-interview-prep--analyst-guided-project"],
    "why":"Visionary connects the pipeline to the business: what this data product changes, who decides differently because of it — the story that wins the loop."},
 ],
 'IL-16': [
   {"track":"Projects and capstones","persona":"mentor",
    "modules":["ml-in-practice--ml-practice-capstone","advanced-ml--advanced-ml-project","python-for-ml--ml-python-project","advanced-genai--genai-capstone","advanced-nlp-practice--nlp-project","ai-enabled-software--ai-feature-project","applied-ai-production--applied-ai-capstone"],
    "why":"Mentor coaches the portfolio builds: scopes the project honestly, reviews the eval results without flinching, and rehearses the stakeholder defense — 'why this metric, why this model, what would you do with 10x data.'"},
   {"track":"ML systems and optimization","persona":"engineer",
    "modules":["ml-in-practice--ml-workflow","ml-in-practice--feature-engineering-practice","ml-in-practice--ml-pipelines-practice","ml-in-practice--ml-deployment-practice","advanced-ml--optimization-advanced","advanced-genai--inference-serving-practice"],
    "why":"Engineer thinks in systems: feature leakage as a systems failure, training/serving skew, the cost curve of inference — concrete, quantified, no hand-waving."},
   {"track":"Evaluation and calibration","persona":"philosopher",
    "modules":["ml-in-practice--model-evaluation-practice","advanced-ml--probabilistic-ml","advanced-ml--model-interpretation-practice","advanced-genai--genai-eval-practice","IL-16-M00"],
    "why":"Philosopher keeps evaluation honest: what the metric hides, when the leaderboard lies, what 'calibrated' actually means — Socratic rigor for the part of ML most people fake."},
   {"track":"Adversarial angles","persona":"trickster",
    "modules":["advanced-ml--re-bench-agents-ml-research","advanced-genai--alignment-practice"],
    "why":"Trickster red-teams the work: the prompt injection you didn't consider, the eval the model games — playful mischief that hardens real systems."},
   {"track":"Where the field goes","persona":"visionary",
    "modules":["advanced-genai--transformer-arch-practice","advanced-genai--pretrain-finetune-practice","applied-ai-production--problem-framing-ai","applied-ai-production--measuring-ai-value"],
    "why":"Visionary reads the field first-principles: what transformers made obsolete, what agentic workflows make newly possible, where applied AI creates durable value."},
 ],
 'IL-17': [
   {"track":"Mock interviews and projects","persona":"mentor",
    "modules":["agentic-ai-for-iv--agentic-mock","agentic-ai-for-iv--agentic-behavioral","agentic-ai-for-iv--agentic-portfolio","agentic-ai-for-swe--swe-agent-project","agentic-ai-for-data--data-agent-project","agentic-ai-lowcode--lowcode-project"],
    "why":"Mentor runs voice mock interviews for AI roles — agentic system design on the whiteboard, LLM depth, behavioral for AI teams — and coaches every shipped agent project."},
   {"track":"Agent architectures","persona":"engineer",
    "modules":["agentic-ai-foundations--agent-loops","agentic-ai-foundations--multi-agent-systems","agentic-ai-foundations--llm-tool-use","agentic-ai-foundations--agent-evaluation","agentic-ai-for-leaders--incident-agents"],
    "why":"Engineer designs agents as systems: tool contracts as interfaces, loops with stopping conditions, multi-agent coordination without collapse, eval as the test suite."},
   {"track":"Depth and governance","persona":"philosopher",
    "modules":["agentic-ai-for-iv--llm-depth-iv","agentic-ai-for-iv--agent-system-design","agentic-ai-for-leaders--leader-agent-governance","IL-17-M00"],
    "why":"Philosopher dwells in the hard questions: what does the agent actually understand, where does responsibility sit when it acts, what can go wrong at scale — the governance layer beneath the demos."},
   {"track":"Failure modes","persona":"trickster",
    "modules":["agentic-ai-for-swe--swe-agent-limits","agentic-ai-lowcode--lowcode-limits","agentic-ai-for-data--data-agent-trust"],
    "why":"Trickster finds the break: the tool the agent misuses, the guardrail it routes around, the confident wrong answer — adversarial play that builds real trust."},
   {"track":"Roadmaps and rollout","persona":"visionary",
    "modules":["agentic-ai-foundations--agent-starter-build","agentic-ai-for-leaders--rollout-playbook","agentic-ai-for-leaders--leader-agent-metrics","agentic-ai-for-pm--pm-agent-roadmap"],
    "why":"Visionary projects where agents go next: the graduation path from low-code to pro-code, the metrics that prove agent ROI, the roadmap that survives contact with production."},
 ],
 'IL-18': [
   {"track":"Mock interview circuits","persona":"mentor",
    "modules":["tpm-interview-prep--tpm-mock","em-interview-prep--em-mock","pm-interview-prep--pm-mock","technical-pm-interview-prep--tech-pm-mock"],
    "why":"Mentor is the voice interviewer: runs timed TPM/EM/PM mocks by voice, coaches STAR stories until they are specific and honest, debriefs with the rubric a real panel uses."},
   {"track":"Technical depth","persona":"engineer",
    "modules":["tpm-interview-prep--technical-depth-tpm","technical-pm-interview-prep--technical-depth-pm","technical-pm-interview-prep--tech-pm-system-design","technical-pm-interview-prep--api-platform-thinking","technical-pm-interview-prep--data-literacy-pm"],
    "why":"Engineer drills the technical half of leadership loops: systems literacy, API/platform reasoning, SQL-backed data literacy — structured, quantified, no bluffing."},
   {"track":"Leadership reasoning","persona":"philosopher",
    "modules":["tpm-interview-prep--program-design-iv","em-interview-prep--eng-strategy-vision","pm-interview-prep--metrics-judgment","pm-interview-prep--pm-behavioral","IL-18-PM-LOGIC"],
    "why":"Philosopher asks the 'why' beneath the leadership answer: what principle decides this trade-off, whose interests does this roadmap serve — the depth panels probe for."},
   {"track":"Curveball scenarios","persona":"trickster",
    "modules":["em-interview-prep--em-scenario-rep","tpm-interview-prep--tpm-case-rep","pm-interview-prep--pm-case-rep"],
    "why":"Trickster throws the lateral scenario: the reorg mid-program, the impossible deadline, the failing vendor — practicing composure and structured thinking when the script breaks."},
   {"track":"Product and AI vision","persona":"visionary",
    "modules":["em-interview-prep--eng-strategy-vision","genai-for-pm--genai-roadmap-pm","genai-for-pm--llm-product-patterns","genai-for-pm--genai-risk-pm"],
    "why":"Visionary builds the product narrative: first-principles GenAI product thinking, roadmaps that account for model risk, the story of where the product — and the leader — are going."},
 ],
}

BLEEDING_EDGE = {
 'IL-16': ("Bleeding-edge integration: this course is wired for the daily trending fold. "
  "Fresh developments — new models, training techniques, eval results, framework releases — "
  "fold in through the site's /trending route and the IL-23 (The Frontier) AI survey, and "
  "Noah's course-aware context carries them into every tutoring session. Ask Noah "
  "'what changed this week in <topic>' and study against the freshest material alongside "
  "the stable curriculum spine. The RE-Bench module (agents doing ML research) is the "
  "frontier anchor: Noah tracks that research line as it moves."),
 'IL-17': ("Bleeding-edge integration: this course is wired for the daily trending fold. "
  "Fresh developments — new agent frameworks, tool-use protocols, eval benchmarks, "
  "multi-agent research, platform capability changes — fold in through the site's "
  "/trending route and the IL-23 (The Frontier) AI survey, and Noah's course-aware "
  "context carries them into every tutoring session. Agentic AI moves weekly; ask Noah "
  "'what changed this week in agents' and get the current state, not last quarter's "
  "textbook. Platform facts are always verified against current public documentation."),
}

def build_noah_tutoring(code):
    concept_map = {
     'IL-13': ("Noah is the core learning driver of IL-13 — a personal interview coach "
      "with five voices and five minds. Every domain track pairs with the persona that "
      "teaches it best: Mentor runs your mock interviews by voice, Engineer drills your "
      "system designs, Philosopher walks your proofs. You don't study the interview "
      "alone; you spar with Noah until the loop feels familiar."),
     'IL-14': ("Noah is the core learning driver of IL-14 — the senior engineer across "
      "the table. Mentor runs incident-command scenarios and full interview loops by "
      "voice; Engineer makes you narrate troubleshooting aloud until the method is "
      "muscle memory. Reliability is a performance discipline, and Noah is the "
      "audience that never gets tired."),
     'IL-15': ("Noah is the core learning driver of IL-15 — the interviewer who makes "
      "you think aloud. Mentor runs live SQL whiteboarding by voice; Philosopher keeps "
      "your statistics honest; Engineer drills pipeline design trade-offs. Every mock "
      "circuit ends with a rubric debrief, not a grade."),
     'IL-16': ("Noah is the core learning driver of IL-16 — a research partner with "
      "five minds. Philosopher keeps your evaluation honest, Engineer systems-thinks "
      "your pipelines, Mentor coaches your portfolio projects and stakeholder defenses. "
      "Paired with the daily trending fold, Noah keeps the curriculum bleeding-edge: "
      "new models and eval results flow into your tutoring sessions as they land."),
     'IL-17': ("Noah is the core learning driver of IL-17 — the agent engineer you "
      "pair with. Engineer designs your agent architectures, Trickster red-teams them, "
      "Mentor runs your agentic interviews by voice. In a field that moves weekly, "
      "Noah's trending-fold integration means you study the current state of agents, "
      "not last quarter's textbook."),
     'IL-18': ("Noah is the core learning driver of IL-18 — the panel across the table. "
      "Mentor runs your TPM/EM/PM mocks by voice and coaches your STAR stories until "
      "they are specific and honest; Philosopher probes the 'why' beneath every "
      "leadership answer; Trickster throws the curveball scenario. You walk into the "
      "real loop already battle-tested."),
    }
    return {
      "tagline": "Noah is the learning driver — not a bolt-on.",
      "concept": concept_map[code],
      "personas": NOAH_PERSONAS,
      "modulePersonaMap": NOAH_MAPS[code],
      "voiceFirst": {
        "supported": True,
        "description": ("Talk with Noah via voice chat while working through modules — "
         "5 distinct natural voices served by POST /api/noah/tts (Scholar, Narrator, "
         "Guide, Sage, Spark), plus adaptive browser speech: per-persona rate/pitch, "
         "emotion-aware delivery, lip-synced avatar. Voice-first mock interviews are "
         "the signature experience: Mentor asks, the clock runs, you answer aloud — "
         "exactly like the real loop."),
        "bestFor": ["mock interview circuits","behavioral story coaching","system-design narration practice","incident-command scenarios"]
      },
      "adaptive": {
        "scheduler": "SM-2-inspired spaced repetition",
        "description": ("Review timing adapts to recall performance (docs/assets/noah-adaptive.js): "
         "quiz and drill results feed per-card intervals, so weak cards resurface sooner and "
         "mastered cards fade to maintenance. Mastery is tracked in localStorage; Noah "
         "re-sequences your next session around what is due, not what is next in the list."),
        "signals": ["quiz scores","drill accuracy","card recall intervals","mock-circuit rubric scores"]
      },
      "courseAware": {
        "endpoint": "POST /api/noah",
        "model": "Cloudflare Workers AI (Llama 3.1 8B)",
        "description": ("Noah tutors from this course's own knowledge — its answers are grounded "
         "in these modules, not generic web knowledge. If the endpoint is unreachable it "
         "degrades to a local Socratic engine with a plain notice. It never invents facts, "
         "credentials, or experience.")
      },
      "bleedingEdge": BLEEDING_EDGE.get(code),
      "houseRule": "Bring Noah your hypothesis — not 'just give me the answer.' Attempt a card first.",
      "howToUse": [
        "Open Noah from any module page and pick the persona mapped to that track.",
        "Attempt the cards first — then bring Noah your hypothesis, not your blank stare.",
        "For interview tracks: switch to voice, pick Mentor, and run the mock circuit aloud.",
        "After every mock, ask Noah for the rubric debrief: what passed, what failed, what to drill next.",
        "Revisit on Noah's schedule: the SM-2 scheduler will resurface what is due."
      ]
    }

# ------------------------------------------------------------ study guides
STUDY_GUIDES = {
 'IL-13': {
  "title":"Study guide: how to work IL-13 in 12 weeks",
  "pacing":[
   "Weeks 1-2 — Foundations, modules 1-9 (~52h): math spine, DSA patterns, complexity, trees/graphs, dynamic programming, then system design fundamentals + guided build. Take the SWE mock circuit cold at the end of week 2 — it calibrates everything after.",
   "Weeks 3-4 — Backend track, modules 10-16 (~40h): APIs, data layer, caching, concurrency, microservices, guided backend design, backend mock. Interview like a backend engineer by week 4.",
   "Weeks 5-6 — Frontend track, modules 17-23: JS/TS depth, React internals, rendering performance, CSS systems, frontend system design, machine coding build, frontend mock.",
   "Weeks 7-8 — Fullstack track, modules 24-30: the full request path, REST/GraphQL, auth, data across the stack, deployment literacy, capstone, fullstack mock.",
   "Weeks 9-10 — Mobile tracks, modules 31-44: pick iOS OR Android first. Language core, frameworks, concurrency, persistence, architecture, guided build, mock circuit.",
   "Week 11 — Embedded track, modules 45-51: C memory models, RTOS, drivers, interrupts, hardware debugging, capstone, embedded mock.",
   "Week 12 — QA track, modules 52-58: test strategy, automation frameworks, API/contract testing, performance testing, planning, guided automation build, QA mock. Finish with a full mock circuit in your target domain."
  ],
  "rules":[
   "Mocks are the course — never skip a mock circuit.",
   "Drills to green before the next module; re-take any quiz below 80%.",
   "Talk through every DSA solution aloud — the interview grades narration, not just code.",
   "One domain track at a time; depth beats breadth in interviews.",
   "Bring Noah your hypothesis first — attempt every card before asking.",
   "Run at least one voice mock with Mentor-Noah per track before the real loop."
  ]},
 'IL-14': {
  "title":"Study guide: how to work IL-14 in 8 weeks",
  "pacing":[
   "Weeks 1-2 — Math + SRE, modules 1-8 (~46h): probability, logic, SLIs/SLOs, incident command, monitoring, capacity planning, SRE design reps, SRE mock circuit.",
   "Weeks 3-4 — DevOps, modules 9-14 (~35h): CI/CD systems, IaC patterns, containers/orchestration, troubleshooting under pressure, guided platform build, DevOps mock.",
   "Weeks 5-6 — Cloud + Security, modules 15-26 (~69h): cloud concepts, networking, data services, security controls, guided cloud architecture, cloud mock; then appsec, network security, crypto, detection/response, secure design review, security mock.",
   "Weeks 7-8 — Full mock circuit, modules 27-31 (~29h): DSA speed reps, system-design reps, behavioral story bank, domain deep dives, full-loop simulation. Two consecutive full-loop clears on different days before the real loop."
  ],
  "rules":[
   "Narrate troubleshooting aloud from day one — the method is the skill.",
   "Incident-command reps are timed; the clock is part of the training.",
   "Quantify every answer: error budgets, blast radius, MTTR, cost.",
   "Drills to green before the next module; re-take any quiz below 80%.",
   "Bring Noah your hypothesis first — attempt every card before asking."
  ]},
 'IL-15': {
  "title":"Study guide: how to work IL-15 in 8 weeks",
  "pacing":[
   "Weeks 1-2 — Math + SQL fluency, modules 1-2 and 28-32 (~40h): statistics, linear algebra, then the full SQL drill circuit (joins, window functions, CTEs/recursion, analytics patterns, finale). SQL fluency first — every data loop tests it.",
   "Weeks 3-4 — Data engineering, modules 3-9 (~40h): advanced SQL for DE, Python wrangling, batch pipelines, streaming systems, modeling/warehousing, pipeline capstone, DE mock.",
   "Weeks 5-6 — Data science + analyst, modules 10-21 (~69h): stats/probability interviews, pandas analysis, ML for DS, A/B experimentation, guided case study, DS mock; SQL foundations, spreadsheets, visualization, metrics, guided analyst project, analyst mock.",
   "Weeks 7-8 — ML interviews, modules 22-27 (~35h): ML theory, deep learning, ML system design, coding reps, ML capstone, ML mock. Finish with the drill-circuit finale under time."
  ],
  "rules":[
   "SQL is daily — the drill circuit is a habit, not a chapter.",
   "Every A/B claim gets power, MDE, and a peeking check — no exceptions.",
   "Whiteboard narration is graded: think aloud on every query.",
   "Drills to green before the next module; re-take any quiz below 80%.",
   "Bring Noah your hypothesis first — attempt every card before asking."
  ]},
 'IL-16': {
  "title":"Study guide: how to work IL-16 in 14 weeks",
  "pacing":[
   "Weeks 1-2 — Math spine, M00 + PM modules (~19h): M00 orientation first, then Statistics & Probability, Linear Algebra, Discrete Mathematics. Do not skip — every track assumes this math.",
   "Weeks 3-4 — Applied ML in practice, modules 1-6 (~60h): workflow, feature engineering, model evaluation, ML pipelines, deployment practice, ML practice capstone.",
   "Weeks 5-6 — Advanced ML, modules 7-12 (~60h): ensembles, probabilistic ML, deep architectures, optimization, model interpretation, advanced ML project.",
   "Weeks 7-8 — Python for ML, modules 13-18 (~60h): NumPy/pandas, visualization, scikit-learn API, the ecosystem, real data, ML Python project.",
   "Weeks 9-10 — Generative AI, modules 19-24 (~60h): transformers, pretraining/fine-tuning, alignment, GenAI evaluation, inference/serving, GenAI capstone.",
   "Weeks 11-12 — NLP, modules 25-30 (~60h): NLP pipelines, embeddings, sequence models, LLMs for NLP, information retrieval, advanced NLP project.",
   "Week 13 — AI-enabled software, modules 31-36 (~60h): LLM APIs, RAG, eval harnesses, tool use, shipping AI features, AI feature project.",
   "Week 14 — Applied AI in production, modules 37-43 (~70h): problem framing, data strategy, rapid prototyping, stakeholder communication, measuring AI value, applied AI capstone, RE-Bench."
  ],
  "rules":[
   "Math first, always — M00 then the PM modules before any technical track.",
   "Every project ships to the portfolio with an eval harness, not just a notebook.",
   "Evaluation before opinions: no model claim without a metric and a baseline.",
   "Ask Noah 'what changed this week' — the trending fold keeps this course current.",
   "Drills to green before the next module; re-take any quiz below 80%.",
   "Bring Noah your hypothesis first — attempt every card before asking."
  ]},
 'IL-17': {
  "title":"Study guide: how to work IL-17 in 12 weeks",
  "pacing":[
   "Weeks 1-2 — Math spine, M00 + PM modules (~19h): M00 orientation first, then Logic & Proof, Statistics & Probability, Discrete Mathematics. Planning is search; evaluation is statistics — the math is load-bearing.",
   "Weeks 3-4 — Foundations, modules 1-6 (~44h): tool use/function calling, agent loops, memory/context, multi-agent systems, agent evaluation, starter agent build. Build the starter agent by week 4.",
   "Weeks 5-6 — SWE + data agents, modules 7-18 (~88h): code agents, repo-scale agents, review/QA agents, dev workflow agents, SWE project, limits; data agents, pipeline agents, text-to-SQL, data quality, data project, trust/guardrails.",
   "Weeks 7-8 — PM + leader agents, modules 19-30 (~88h): agent literacy, spec/PRD agents, research agents, playbook, metrics/risk, roadmapping; program agents, eng-mgmt agents, incident agents, rollout playbook, governance, measuring impact.",
   "Weeks 9-10 — Interview prep, modules 31-36 (~44h): agentic system design, LLM depth, agentic coding reps, behavioral for AI roles, agentic mock circuit, portfolio review.",
   "Weeks 11-12 — Low-code agents, modules 37-42 (~44h): platforms, prompt flows, connectors, low-code project, deploy/share, limits of low-code. Ship one agent to production."
  ],
  "rules":[
   "M00 first — logic before tool contracts, stats before evaluation claims.",
   "Every agent ships with guardrails and an eval — demos don't count.",
   "Least-privilege tooling from the first build, not as an afterthought.",
   "Ask Noah 'what changed this week in agents' — this field moves weekly.",
   "Drills to green before the next module; re-take any quiz below 80%.",
   "Bring Noah your hypothesis first — attempt every card before asking."
  ]},
 'IL-18': {
  "title":"Study guide: how to work IL-18 in 10 weeks",
  "pacing":[
   "Weeks 1-3 — TPM track, modules 1-6 (~48h): program design, execution engine, cross-functional leadership, technical depth for TPMs, guided program case, TPM mock circuit.",
   "Weeks 4-5 — EM track, modules 7-12 (~32h): people leadership, delivery ownership, hiring/growing teams, engineering strategy, guided leadership scenarios, EM mock.",
   "Weeks 6-7 — PM track, modules 13-18 (~32h): product sense, execution, metrics/judgment, behavioral for PMs, guided product case, PM mock.",
   "Weeks 8-9 — Technical PM + GenAI for PM, modules 19-30 (~80h): technical depth, API/platform thinking, data literacy, guided technical case, technical design reps, tech-PM mock; GenAI literacy, LLM product patterns, eval/UX for AI, GenAI playbook, risk, AI roadmapping.",
   "Week 10 — Math + final loop, modules 31-32 + full simulation (~18h): logic & proof, statistics & probability, then a full leadership-loop simulation. Two consecutive clears on different days before the real loop."
  ],
  "rules":[
   "Stories are the currency — every behavioral answer gets a specific, honest STAR story.",
   "Metrics with judgment: never quote a metric without the decision it drives.",
   "Run every mock by voice with Mentor-Noah before the real loop.",
   "Technical depth is non-negotiable for TPM/tech-PM loops — no bluffing.",
   "Drills to green before the next module; re-take any quiz below 80%.",
   "Bring Noah your hypothesis first — attempt every card before asking."
  ]},
}

# ------------------------------------------------------------------ build
def ensure_module_fields(mods):
    for m in mods:
        for k in REQUIRED_MODULE_FIELDS:
            if k not in m:
                m[k] = [] if k in ("prerequisiteFor","crossLinks","cards","quiz","drills","videos","pdfs","notes") else ({} if k in ("handsOnLab","mockTask") else (0 if k in ("estimatedMinutes","weight") else ""))
    return mods

def interactivity_audit(d):
    t = len(d.get("terminalSims",[])); b = len(d.get("branchingScenarios",[]))
    c = len(d.get("clickSims",[])); tl = len(d.get("toolLabs",[]))
    il = len(d.get("installLabs",[])); mc = len(d.get("multicloudLabs",[]))
    tr = len(d.get("trainers",[])); sl = len(d.get("scriptLabs",[]))
    ch = len(d.get("cheatSheets",[]))
    return {"terminalSims":t,"branchingScenarios":b,"clickSims":c,"toolLabs":tl,
     "installLabs":il,"multicloudLabs":mc,"trainers":tr,"scriptLabs":sl,
     "cheatSheets":ch,
     "totalInteractive": t+b+c+tl+il+mc+tr+sl+ch,
     "rule":"Every module ships notes, flashcards, quiz, drills, a hands-on lab, and a mock task; interactivity is counted, not claimed."}

def copy_khan_entries(d):
    out = []
    seen = set()
    for m in d["modules"]:
        for v in m.get("videos",[]):
            if "khanacademy" in (v.get("url","")) and v.get("url") not in seen:
                out.append(copy.deepcopy(v)); seen.add(v.get("url"))
    return out

def copy_math_pdfs(d):
    out = []
    for m in d["modules"]:
        for p in m.get("pdfs",[]):
            u = p.get("url","")
            if any(s in u for s in ("linear-algebra","probability","statistics","calculus-ml","info-theory")):
                if u not in [x["url"] for x in out]:
                    out.append(copy.deepcopy(p))
    return out

def finalize_m00(code, d):
    if code == 'IL-16':
        m = copy.deepcopy(M00_IL16)
        m["videos"] = copy_khan_entries(d)
        m["pdfs"] = copy_math_pdfs(d)
        pm = [x for x in d["modules"] if x["id"]=="IL-16-PM-STATS"][0]
        m["weight"] = pm.get("weight", 1)
    else:
        m = copy.deepcopy(M00_IL17)
        m["videos"] = copy_khan_entries(d)
        pm = [x for x in d["modules"] if x["id"]=="IL-17-PM-LOGIC"][0]
        m["weight"] = pm.get("weight", 1)
    return m

results = {}
for code, fname in FILES.items():
    path = os.path.join(BASE, fname)
    bak = path + ".groupc-bak"
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    d = json.load(open(path))

    # drop build artifacts
    d.pop("_noCertNote", None); d.pop("_phase2_done", None)

    d["schemaVersion"] = "4"
    d["updatedAt"] = "2026-10-09"
    d["timeFormula"] = TIME_FORMULA
    d["honestyNote"] = HONESTY[code]
    d["certNotes"] = CERTNOTES[code]
    d["mergeNotes"] = MERGE_NOTES[code]
    d["noahTutoring"] = build_noah_tutoring(code)

    # modules: ensure fields, add M00 for IL-16/IL-17
    d["modules"] = ensure_module_fields(d["modules"])
    if code in ('IL-16','IL-17'):
        assert not any(m["id"] in ("IL-16-M00","IL-17-M00") for m in d["modules"]), code+" M00 already present"
        d["modules"].insert(0, finalize_m00(code, d))

    # cert gates / crosswalk per spec
    if code == 'IL-13':
        d["certGates"] = []; d["crosswalk"] = []
    elif code == 'IL-14':
        d["certGates"] = []; d["crosswalk"] = []
    elif code == 'IL-15':
        d["certGates"] = []; d["crosswalk"] = []
    elif code == 'IL-17':
        d["certGates"] = []; d["crosswalk"] = []
    elif code == 'IL-18':
        d["certGates"] = [g for g in d["certGates"] if g["id"]=="gate-il18-interview"]
        d["crosswalk"] = [c for c in d["crosswalk"] if "PMP" not in c.get("cert","")]
    elif code == 'IL-16':
        for g in d["certGates"]:
            assert FRAMING in g.get("framing",""), "framing missing on "+g["id"]
            if g["id"]=="gate-il16-aws-mla":
                g["format"] = ("65 questions (multiple-choice/multiple-response), passing score 720/1000; "
                 "duration per AWS's current published exam guide — verify before booking")
        tf_gate = {
          "id":"gate-il16-tf-dev-retired",
          "cert":"TensorFlow Developer Certificate (retired track — not bookable)",
          "trackModule":"python-for-ml--sklearn-api-practice",
          "framing": FRAMING + " This track is historical skill-domain practice only: the TensorFlow Developer Certificate program was closed to new candidates on May 1, 2024.",
          "format":("Historical format: 5-hour performance-based exam, 5 TensorFlow 2.x coding tasks "
           "(regression, classification, image processing, NLP, time series/forecasting). "
           "Program closed May 1, 2024 — not bookable; practice only."),
          "minutes":300, "questionCount":5,
          "domainWeights":[
            {"domain":"Regression modeling with TensorFlow","weight":0.2,"questions":1},
            {"domain":"Classification modeling with TensorFlow","weight":0.2,"questions":1},
            {"domain":"Image processing / CNNs","weight":0.2,"questions":1},
            {"domain":"Natural language processing","weight":0.2,"questions":1},
            {"domain":"Time series and forecasting","weight":0.2,"questions":1}],
          "readinessRule":"Practice-only: complete all 5 historical task domains as portfolio builds. There is no exam to book.",
          "modules":["python-for-ml--sklearn-api-practice","advanced-ml--deep-architectures-practice",
           "advanced-nlp-practice--sequence-models-practice","advanced-nlp-practice--nlp-project"]}
        assert all(m in [x["id"] for x in d["modules"]] for m in tf_gate["modules"])
        d["certGates"].append(tf_gate)
        d["crosswalk"].extend([
          {"cert":"AWS Certified Machine Learning – Specialty (MLS-C01) — RETIRED",
           "modules":["ml-in-practice--feature-engineering-practice","ml-in-practice--ml-pipelines-practice",
            "ml-in-practice--ml-workflow","advanced-ml--optimization-advanced","ml-in-practice--model-evaluation-practice",
            "ml-in-practice--ml-deployment-practice","advanced-genai--inference-serving-practice",
            "advanced-ml--model-interpretation-practice","advanced-genai--genai-eval-practice","IL-16-PM-STATS"],
           "note":"Retired March 31, 2026; not bookable. Skill domains carry over to the active MLA-C01 — independent preparation only."},
          {"cert":"TensorFlow Developer Certificate — RETIRED",
           "modules":["python-for-ml--sklearn-api-practice","advanced-ml--deep-architectures-practice",
            "advanced-nlp-practice--sequence-models-practice","advanced-nlp-practice--nlp-project"],
           "note":"Program closed May 1, 2024; not bookable. Historical skill-domain alignment for practice only — independent preparation."}])
        d["sourceLinks"].extend([
          {"name":"QA — AWS Certified Machine Learning Engineer – Associate (MLA-C01) exam structure",
           "url":"https://www.qa.com/browse/certifications/aws-certifications/aws-certified-machine-learning-engineer-associate/",
           "note":"65 questions, 720/1000 passing score; MLA-C01 domain structure.","retrieved":"2026-10-09"},
          {"name":"Digital Watch Observatory — AWS retires ML Specialty (MLS-C01) March 31, 2026",
           "url":"https://dig.watch/updates/aws-launches-new-generative-ai-certification-and-updates-security-exams",
           "note":"Retirement announcement for MLS-C01; candidates pointed to MLA-C01 and the Generative AI Developer credential.","retrieved":"2026-10-09"},
          {"name":"TensorFlow Deep Learning course notes — TensorFlow Developer Certificate closure",
           "url":"https://github.com/emmex43/tensorflow-deep-learning",
           "note":"Documents the TensorFlow Developer Certificate program closure to new candidates on May 1, 2024.","retrieved":"2026-10-09"}])

    # readiness dashboards
    if DASHBOARDS[code] is not None:
        d["readinessDashboard"] = DASHBOARDS[code]
    elif code == 'IL-18':
        d["readinessDashboard"]["title"] = "IL-18 Interview Readiness Dashboard"
        d["readinessDashboard"]["order"] = ["gate-il18-interview"]
    elif code == 'IL-16':
        d["readinessDashboard"]["order"] = ["gate-il16-gcp-mle","gate-il16-aws-mla","gate-il16-ai103"]

    # missing v4 top-level keys
    for k in ["branchingScenarios","clickSims","toolLabs","multicloudLabs","installLabs",
              "installSteps","installPrereqOrder","employerMappings","jdMatrix",
              "sqlPlaygrounds","pythonExercises","daxPlaygrounds","sampleDatasets"]:
        d.setdefault(k, [])
    d["interactivityAudit"] = interactivity_audit(d)
    sg = copy.deepcopy(STUDY_GUIDES[code])
    total_min = sum(m["estimatedMinutes"] for m in d["modules"])
    sg["totalMinutes"] = total_min
    sg["totalHours"] = round(total_min/60)
    sg["note"] = "Totals are computed from module estimatedMinutes; pacing assumes ~25-30 focused hours per week."
    d["studyGuide"] = sg

    # honest hours
    d["hours"] = round(total_min/60)

    # ---- validation before write
    assert set(V4_TOP + ["noahTutoring","certNotes","mergeNotes"]) <= set(d.keys()), code+" missing top keys: "+str(sorted(set(V4_TOP+["noahTutoring","certNotes","mergeNotes"])-set(d.keys())))
    for m in d["modules"]:
        miss = [k for k in REQUIRED_MODULE_FIELDS if k not in m]
        assert not miss, code+" "+m.get("id","?")+" missing "+str(miss)
    assert d["hours"] == round(sum(m["estimatedMinutes"] for m in d["modules"])/60)
    assert d["schemaVersion"] == "4" and d["updatedAt"] == "2026-10-09"
    for g in d["certGates"]:
        assert "Independent practice and preparation" in g.get("framing",""), code+" framing missing on "+g["id"]
    nt = d["noahTutoring"]
    assert len(nt["personas"])==5 and len(nt["modulePersonaMap"])>=5
    assert nt["voiceFirst"]["supported"] and nt["adaptive"]["scheduler"].startswith("SM-2")
    assert nt["courseAware"]["endpoint"]=="POST /api/noah"
    if code in ("IL-16","IL-17"):
        assert nt["bleedingEdge"], code+" missing bleedingEdge"
    else:
        assert nt["bleedingEdge"] is None

    tmp = path + ".tmp"
    with open(tmp,"w") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    json.load(open(tmp))  # re-parse check
    os.replace(tmp, path)
    results[code] = {"modules":len(d["modules"]),"hours":d["hours"],"minutes":total_min,
                     "gates":[g["id"] for g in d["certGates"]],
                     "noahMaps":len(nt["modulePersonaMap"])}
    print(code, "OK:", results[code])

print(json.dumps(results, indent=1))
