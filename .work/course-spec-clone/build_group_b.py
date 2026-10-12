#!/usr/bin/env python3
"""Group B v4 build: IL-07, IL-08, IL-09, IL-10, IL-11, IL-12.

Preserves ALL existing content. Upgrades schemaVersion to "4", adds missing
v4 top-level keys, wires merge-plan cross-links, adds certification mappings
with independent-prep framing, and recomputes honest hours.
"""
import json, copy, math, os

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses/'
FRAMING = ("Independent practice and preparation. Not affiliated with, endorsed by, "
           "or sponsored by any vendor or employer; confers no certificate.")
RETRIEVED = "2026-10-09"

REQUIRED = ['code','courseId','title','tagline','blurb','hours','mockMinutes','schemaVersion',
 'updatedAt','honestyNote','objectives','arc','priorities','battlePlan','modules','crosswalk',
 'certGates','readinessDashboard','scriptLabs','drills','scenarios','trainers','terminalSims',
 'mockTasks','cheatSheets','answerBank','sourceLinks','toolLabs','multicloudLabs','sampleDatasets',
 'installSteps','installPrereqOrder','installLabs','employerMappings','jdMatrix','sqlPlaygrounds',
 'pythonExercises','daxPlaygrounds','branchingScenarios','clickSims','interactivityAudit',
 'studyGuide','timeFormula','glossary','faq','tips','legends','topicTheme','topic']

def interactivity_audit(d):
    order = ['terminalSims','branchingScenarios','clickSims','toolLabs','installLabs',
             'multicloudLabs','trainers','scriptLabs','cheatSheets']
    out = {}
    for k in order:
        v = d.get(k)
        out[k] = len(v) if isinstance(v, list) else 0
    out['totalInteractive'] = sum(out.values())
    out['rule'] = ("Every module ships notes, flashcards, quiz, drills, a hands-on lab, "
                   "and a mock task; interactivity is counted, not claimed.")
    return out

def study_guide(code, hours, pacing, rules):
    total_min = int(round(hours * 60))
    return {
        "title": "Study guide: how to work %s" % code,
        "totalHours": hours,
        "totalMinutes": total_min,
        "note": ("totalHours/totalMinutes are filled from module estimatedMinutes; "
                 "declared hours are the honest rounded sum."),
        "pacing": pacing,
        "rules": rules,
    }

def rd_cert(title, concept_extra=""):
    return {
        "title": title,
        "framing": FRAMING,
        "concept": ("Each track has a timed practice gate. You are ready to sit when you clear "
                    "the gate threshold twice in a row, on different days." + concept_extra),
        "formula": "readiness = (gate1 >= threshold) AND (gate2 >= threshold), gates on separate days",
        "thresholds": "Per-gate thresholds are listed on each certGate.",
        "statusLabels": ["not started", "in progress", "gate 1 cleared", "ready"],
        "rule": "Book the real exam only after clearing the readiness rule twice; never book on a single good score.",
    }

def rd_foundational(title, gates_desc):
    return {
        "title": title,
        "framing": FRAMING,
        "concept": ("This course has no vendor certification tracks. Readiness is measured by "
                    "portfolio project gates: " + gates_desc),
        "formula": "readiness = (project1 complete AND reviewed) AND (project2 complete AND reviewed)",
        "thresholds": "Per-project acceptance criteria are listed on each module's hands-on lab.",
        "statusLabels": ["not started", "in progress", "project 1 complete", "ready"],
        "rule": "Finish the capstone(s) and the peer-review checklist before declaring the course complete.",
    }

# ---------------------------------------------------------------- cert gates
GATE_DBT = {
    "id": "gate-dbt-ae",
    "cert": "dbt Analytics Engineering Certification",
    "trackModule": "il07-data-schools",
    "framing": FRAMING,
    "format": ("65 questions (multiple-choice, fill-in-the-blank, matching, hotspot, "
               "build-list, discrete-option multiple choice), 120 minutes, passing score 65%; "
               "online with live proctoring. Verify the current exam version and format at dbt's "
               "official certification page before booking."),
    "minutes": 120,
    "questionCount": 65,
    "domainWeights": [
        {"domain": "Developing and optimizing dbt models", "weight": 0.45, "questions": 29},
    ],
    "readinessRule": ("Score 65%+ on two consecutive timed 65-question practice gates covering "
                      "models, tests, snapshots, seeds, sources, and CI before booking. The models "
                      "domain is ~45% of the exam; verify the remaining published domains against "
                      "dbt's current objectives before booking."),
    "modules": ["il07-data-schools", "il07-mongodb", "il-07-data-engineering-analytics-ai-math-stats"],
}

GATE_CYSA = {
    "id": "gate-cysa-plus",
    "cert": "CompTIA CySA+ CS0-003",
    "trackModule": "il11-cyber-hero-prep--zt-hero-review",
    "framing": FRAMING,
    "format": "Up to 85 questions (multiple-choice + performance-based), 165 minutes, passing score 750/900",
    "minutes": 165,
    "questionCount": 85,
    "domainWeights": [
        {"domain": "1.0 Security Operations", "weight": 0.33, "questions": 28},
        {"domain": "2.0 Vulnerability Management", "weight": 0.30, "questions": 26},
        {"domain": "3.0 Incident Response Management", "weight": 0.20, "questions": 17},
        {"domain": "4.0 Reporting and Communication", "weight": 0.17, "questions": 14},
    ],
    "readinessRule": "Score 83%+ on two consecutive timed gates including at least 5 scenario/PBQ-style items per attempt before booking.",
    "modules": [
        "il11-zero-trust-foundations--zt-default-deny",
        "il11-allowlisting-ringfencing--zt-allowlist",
        "il11-allowlisting-ringfencing--zt-ringfence",
        "il11-allowlisting-ringfencing--zt-storage-elevation",
        "il11-red-blue-operations--zt-blue-detect",
        "il11-network-crypto-foundations--zt-encryption",
        "il11-active-directory-defense--zt-ad-attacks",
        "il11-active-directory-defense--zt-ad-harden",
        "il11-red-blue-operations--zt-social-engineering",
        "il11-cyber-hero-prep--zt-hero-review",
        "il11-cyber-hero-prep--zt-hero-scenarios",
    ],
}

GATE_TF = {
    "id": "gate-tensorflow-developer",
    "cert": "TensorFlow Developer Certificate",
    "trackModule": "aieng-capstone--capstone-build",
    "framing": FRAMING,
    "format": ("5 hands-on coding tasks in PyCharm (ML/DL foundations, image classification, "
               "NLP, time-series forecasting), 300 minutes, open book. No officially published "
               "passing score — verify the current environment setup and task list at the official "
               "exam page before booking."),
    "minutes": 300,
    "questionCount": 5,
    "domainWeights": [
        {"domain": "ML/DL foundations and debugging", "weight": 0.20, "questions": 1},
        {"domain": "Image classification", "weight": 0.20, "questions": 1},
        {"domain": "Natural language processing", "weight": 0.20, "questions": 1},
        {"domain": "Time series and sequences", "weight": 0.20, "questions": 1},
        {"domain": "Model building, training, and tuning", "weight": 0.20, "questions": 1},
    ],
    "readinessRule": ("Complete all 5 task categories within a single 5-hour window, twice, with no "
                      "environment debugging stalls, using TensorFlow (tf.keras / tf.data) before booking. "
                      "This course teaches concepts framework-neutrally; do the TensorFlow-specific "
                      "practice builds against the official exam setup guide."),
    "modules": [
        "aieng-deep-learning--neural-foundations",
        "aieng-deep-learning--cnns",
        "aieng-nlp--tokenization-embeddings",
        "aieng-deep-learning--sequence-models",
        "aieng-machine-learning--evaluation-metrics",
        "aieng-production--prod-serving",
        "aieng-capstone--capstone-build",
    ],
}

# ------------------------------------------------------------ crosswalk adds
XW_DBT = {
    "cert": "dbt Analytics Engineering Certification",
    "modules": ["il07-data-schools", "il07-mongodb"],
    "note": ("Independent preparation aligned to dbt's published objectives. dbt Core modeling, "
             "tests, snapshots, seeds, sources, and CI workflows map to il07-data-schools; "
             "verify the current exam version before booking."),
}
XW_CYSA = {
    "cert": "CompTIA CySA+ CS0-003",
    "modules": GATE_CYSA["modules"],
    "note": ("Independent preparation aligned to the 4 published CS0-003 domains (33/30/20/17). "
             "Security Operations (33%) is the heaviest lift — zt-blue-detect, zt-default-deny, "
             "and the allowlisting/ringfencing modules carry it."),
}
XW_TF = {
    "cert": "TensorFlow Developer Certificate",
    "modules": GATE_TF["modules"],
    "note": ("Independent preparation aligned to the 5 published task categories. Concepts in this "
             "course are framework-neutral; do the TensorFlow-specific practice builds against the "
             "official exam setup guide and verify the current task list before booking."),
}

# ------------------------------------------------------- per-course content
IL07_SECTIONS = {
    "sampleDatasets": [
        {"id": "ds-bikeshare", "title": "Bike-share rides (streaming + batch)",
         "description": "Timestamped ride events used for window-function SQL, streaming ingestion, and late-data handling labs."},
        {"id": "ds-ecommerce", "title": "E-commerce orders (relational)",
         "description": "Orders, customers, and line items for CTEs, dbt models, tests, and snapshot (SCD2) labs."},
        {"id": "ds-weblogs", "title": "Web server logs (semi-structured)",
         "description": "JSON log lines for parsing, sessionization, and document-database loading labs."},
    ],
    "sqlPlaygrounds": [
        {"id": "sp-windows", "title": "Window functions gym",
         "prompt": "Rank, lag/lead, running totals, and dedupe with ROW_NUMBER over the bike-share rides dataset.",
         "skills": ["window functions", "CTEs", "dedupe"]},
        {"id": "sp-dbt-models", "title": "dbt model studio",
         "prompt": "Build staging/marts models over e-commerce orders with ref(), sources, and schema tests.",
         "skills": ["dbt", "ref()", "tests", "snapshots"]},
        {"id": "sp-query-tuning", "title": "Query tuning bench",
         "prompt": "Diagnose a slow aggregation with EXPLAIN, then rewrite it with a materialized incremental model.",
         "skills": ["EXPLAIN", "incremental models", "partitioning"]},
    ],
    "pythonExercises": [
        {"id": "pe-pandas-etl", "title": "pandas ETL pipeline",
         "brief": "Build an extract-transform-load pipeline with validation checks and idempotent loads."},
        {"id": "pe-api-ingest", "title": "API ingestion with backoff",
         "brief": "Ingest a paginated REST API with retries, checkpoints, and schema evolution handling."},
        {"id": "pe-data-quality", "title": "Data quality assertions",
         "brief": "Write row-count, null-rate, and distribution assertions that fail the pipeline on violation."},
    ],
    "daxPlaygrounds": [
        {"id": "dx-timeintel", "title": "DAX time intelligence",
         "prompt": "YTD/MTD measures, SAMEPERIODLASTYEAR, and a proper date table over e-commerce orders.",
         "skills": ["CALCULATE", "time intelligence"]},
        {"id": "dx-filter-context", "title": "Filter context lab",
         "prompt": "Fix a measure that ignores slicers; rewrite with correct filter propagation.",
         "skills": ["filter context", "CALCULATE"]},
    ],
    "toolLabs": [
        {"id": "tl-dbt-init", "title": "dbt Core project bootstrap",
         "description": "Initialize a dbt project, configure a profile, and run your first models + tests."},
        {"id": "tl-duckdb-lake", "title": "Local lakehouse with DuckDB",
         "description": "Stand up a local analytical store on Parquet files; query it from SQL and Python."},
        {"id": "tl-mongo-atlas", "title": "MongoDB Atlas sandbox",
         "description": "Create a free-tier Atlas cluster, load documents, and run aggregation pipelines."},
    ],
    "installSteps": [
        "Install Python 3.11+ and verify with python3 --version.",
        "Install DuckDB (pip install duckdb) for the local analytical labs.",
        "Install dbt Core for your adapter (pip install dbt-core dbt-duckdb) for the transformation labs.",
        "Create a free MongoDB Atlas account and a free-tier cluster for the document labs.",
        "Optional: install Docker Desktop to run Airflow/Postgres containers for orchestration labs.",
    ],
    "installPrereqOrder": ["python", "duckdb", "dbt-core", "atlas-account", "docker-optional"],
    "installLabs": [
        {"id": "inl-python-env", "title": "Python environment check",
         "description": "Verify python, pip, duckdb, and dbt-core install cleanly and report versions."},
        {"id": "inl-atlas-connect", "title": "Atlas connection test",
         "description": "Connect mongosh to your Atlas cluster and run a ping + sample aggregation."},
    ],
    "employerMappings": [],
    "jdMatrix": [],
    "branchingScenarios": [],
    "clickSims": [],
    "multicloudLabs": [],
}

IL08_SECTIONS = {
    "sampleDatasets": [],
    "sqlPlaygrounds": [],
    "pythonExercises": [
        {"id": "pe-sorting-proof", "title": "Sorting: proof to code",
         "brief": "Implement mergesort and quicksort; prove the recurrence and measure actual runtimes."},
        {"id": "pe-graph-traversal", "title": "Graph traversal lab",
         "brief": "Implement BFS/DFS from scratch; use BFS to compute shortest paths on an unweighted graph."},
        {"id": "pe-dp-knapsack", "title": "Dynamic programming: knapsack",
         "brief": "Write the memoized and tabulated knapsack; derive the recurrence in the notes first."},
    ],
    "daxPlaygrounds": [],
    "toolLabs": [],
    "installSteps": [
        "Install Python 3.11+ and verify with python3 --version.",
        "Install a C compiler (gcc) for the systems-adjacent labs.",
        "Install Graphviz for rendering the graph-algorithm diagrams you generate.",
    ],
    "installPrereqOrder": ["python", "gcc", "graphviz"],
    "installLabs": [
        {"id": "inl-toolchain", "title": "Toolchain verification",
         "description": "Verify python, gcc, and dot (Graphviz) report versions and compile a hello-world C file."},
    ],
    "employerMappings": [],
    "jdMatrix": [],
    "branchingScenarios": [],
    "clickSims": [],
    "multicloudLabs": [],
}

IL09_SECTIONS = {
    "sampleDatasets": [],
    "sqlPlaygrounds": [],
    "pythonExercises": [],
    "daxPlaygrounds": [],
    "toolLabs": [
        {"id": "tl-objectives-matrix", "title": "Exam objectives matrix",
         "description": "Build a domain-by-domain objectives tracker and map every course module to the domains it covers."},
        {"id": "tl-study-scheduler", "title": "Adaptive study scheduler",
         "description": "Schedule timed practice gates from your weakest domains; reschedule automatically on gate failures."},
    ],
    "installSteps": [],
    "installPrereqOrder": [],
    "installLabs": [],
    "employerMappings": [],
    "jdMatrix": [],
    "branchingScenarios": [],
    "clickSims": [],
    "multicloudLabs": [],
}

IL10_SECTIONS = {
    "sampleDatasets": [],
    "sqlPlaygrounds": [],
    "pythonExercises": [],
    "daxPlaygrounds": [],
    "toolLabs": [],
    "installSteps": [],
    "installPrereqOrder": [],
    "installLabs": [],
    "employerMappings": [],
    "jdMatrix": [],
    "branchingScenarios": [],
    "clickSims": [],
    "multicloudLabs": [],
}

IL11_SECTIONS = {
    "sampleDatasets": [],
    "sqlPlaygrounds": [],
    "pythonExercises": [],
    "daxPlaygrounds": [],
    "toolLabs": [
        {"id": "tl-allowlist-policy", "title": "Allowlist policy authoring",
         "description": "Author a default-deny application policy for a test VM; handle the first break-fix event."},
        {"id": "tl-ringfence-profile", "title": "Ringfence profile lab",
         "description": "Constrain a browser and an office app; verify exfiltration attempts are blocked."},
        {"id": "tl-entra-ca", "title": "Entra Conditional Access lab",
         "description": "Build CA policies for risky sign-ins in a trial tenant; test with a simulated risky login."},
        {"id": "tl-kql-hunt", "title": "KQL threat-hunting lab",
         "description": "Write KQL queries against sample sign-in and audit logs to find anomalous authentication patterns."},
    ],
    "installSteps": [
        "Set up a Windows 10/11 VM or Windows Sandbox for the endpoint labs.",
        "Install PowerShell 7 (pwsh) alongside Windows PowerShell.",
        "Install the Sysinternals Suite (Process Explorer, Process Monitor, Autoruns) for investigation labs.",
        "Create a Microsoft Entra ID trial tenant for the identity labs; delete it when finished.",
    ],
    "installPrereqOrder": ["windows-vm", "powershell7", "sysinternals", "entra-trial"],
    "installLabs": [
        {"id": "inl-sandbox", "title": "Sandbox verification",
         "description": "Confirm Windows Sandbox boots, pwsh runs, and Sysinternals tools launch."},
        {"id": "inl-entra-connect", "title": "Entra connection test",
         "description": "Connect to your trial tenant with Connect-MgGraph and list users."},
    ],
    "employerMappings": [],
    "jdMatrix": [],
    "branchingScenarios": [],
    "clickSims": [],
    "multicloudLabs": [],
}

IL12_SECTIONS = {
    "sampleDatasets": [
        {"id": "ds-tiny-shakespeare", "title": "tiny-shakespeare (language)",
         "description": "Character-level text corpus for the language-modeling and tokenizer labs."},
        {"id": "ds-fashion-mnist", "title": "fashion-mnist (vision)",
         "description": "70k labeled clothing images for the CNN and training-loop labs."},
        {"id": "ds-housing", "title": "Housing prices (regression)",
         "description": "Tabular regression dataset for feature engineering and evaluation-metric labs."},
    ],
    "sqlPlaygrounds": [],
    "pythonExercises": [
        {"id": "pe-numpy-vec", "title": "NumPy vectorization",
         "brief": "Vectorize a k-NN classifier; beat the loop version by 100x and prove it with timings."},
        {"id": "pe-autograd", "title": "Autograd from scratch",
         "brief": "Build a scalar autograd engine (micrograd-style) and train a tiny MLP with it."},
        {"id": "pe-rag-pipeline", "title": "RAG pipeline",
         "brief": "Chunk documents, embed, index in a vector store, and answer questions with citations."},
        {"id": "pe-lora-sketch", "title": "LoRA fine-tune sketch",
         "brief": "Fine-tune a small open-weight model with LoRA on a toy task; measure forgetting."},
    ],
    "daxPlaygrounds": [],
    "toolLabs": [
        {"id": "tl-ollama-serve", "title": "Local model serving with Ollama",
         "description": "Serve an open-weight model locally; benchmark latency and memory at two quantization levels."},
        {"id": "tl-mlflow-track", "title": "Experiment tracking with MLflow",
         "description": "Track runs, params, and metrics; register the best model and promote it through stages."},
        {"id": "tl-vllm-infer", "title": "vLLM inference lab",
         "description": "Serve a model with vLLM; compare throughput against the naive baseline."},
    ],
    "installSteps": [
        "Install Python 3.11+ and verify with python3 --version.",
        "Install PyTorch per the official selector for your platform (CPU is fine to start).",
        "Install transformers, datasets, and scikit-learn via pip for the modeling labs.",
        "Install Ollama from the official site for the local-serving labs (optional on low-RAM machines).",
    ],
    "installPrereqOrder": ["python", "pytorch", "transformers-stack", "ollama-optional"],
    "installLabs": [
        {"id": "inl-torch", "title": "PyTorch smoke test",
         "description": "Import torch, create a tensor, run a matmul, and report the device (cpu/cuda)."},
        {"id": "inl-ollama", "title": "Ollama serve test",
         "description": "Pull a small model and get a completion through the local API."},
    ],
    "employerMappings": [],
    "jdMatrix": [],
    "branchingScenarios": [],
    "clickSims": [],
    "multicloudLabs": [],
}

# ------------------------------------------------------- cross-link wiring
IL07_CROSSLINKS = {
    "il-07-data-engineering-analytics-ai-math-stats": ["il-02-mathematical-maturity-engine-math-stats"],
    "il-07-data-engineering-analytics-ai-math-linalg": ["il02-math-spine"],
    "il07-mongodb": ["IL26-M12"],
    "il07-data-schools": ["IL26-M44", "IL26-M46"],
    "il07-ai-ml": ["advanced-ml--deep-architectures-practice",
                   "advanced-genai--transformer-arch-practice",
                   "ai-enabled-software--llm-apis-practice",
                   "IL26-M10", "IL26-M47"],
    "il07-neuroai": ["advanced-ml--probabilistic-ml"],
    "il07-openweight": ["advanced-genai--inference-serving-practice"],
    "il07-agents": ["agentic-ai-foundations--agent-loops",
                    "agentic-ai-for-data--data-agents-core"],
    "il07-frontier": ["m23-agents", "m23-transformers", "m23-metr-evals"],
    "il07-aws-data": ["IL26-M13", "IL26-M14"],
    "il07-aws-ml": ["advanced-ml--advanced-ml-project",
                    "applied-ai-production--prototyping-ai"],
}
IL08_CROSSLINKS = {
    "il-08-algorithms-compilers-distributed-formal-math-discrete": ["il02-math-spine"],
    "il-08-algorithms-compilers-distributed-formal-math-logic": ["il-02-mathematical-maturity-engine-math-logic"],
}
IL09_CROSSLINKS = {
    "il-09-adaptive-certification-command-math-binmath": ["il02-tech-math"],
    "il-09-adaptive-certification-command-math-logic": ["il-02-mathematical-maturity-engine-math-logic"],
}
IL10_CROSSLINKS = {
    "il-10-portfolio-career-professional-practice-math-quantreason": ["il02-quant-math"],
}
IL11_CROSSLINKS = {
    "il-11-zero-trust-endpoint-defense-math-numtheory": ["il-06-cybersecurity-secure-engineering-math-numtheory"],
    "il-11-zero-trust-endpoint-defense-math-logic": ["il-06-cybersecurity-secure-engineering-math-logic"],
    "il11-zero-trust-foundations--zt-perimeter-fall": ["IL29-M01", "il06-hackers-arise"],
    "il11-zero-trust-foundations--zt-nist-tenets": ["IL29-M01"],
    "il11-zero-trust-foundations--zt-cisa-maturity": ["IL29-M01"],
    "il11-zero-trust-foundations--zt-default-deny": ["IL29-M02", "IL29-M03"],
    "il11-network-crypto-foundations--zt-osi-tcpip": ["il06-defensive"],
    "il11-network-crypto-foundations--zt-hashing": ["il06-hackers-arise"],
    "il11-network-crypto-foundations--zt-encryption": ["IL29-M18"],
    "il11-active-directory-defense--zt-ad-structure": ["il06-defensive"],
    "il11-active-directory-defense--zt-ad-attacks": ["il06-offensive"],
    "il11-active-directory-defense--zt-ad-harden": ["il06-defensive"],
    "il11-allowlisting-ringfencing--zt-allowlist": ["IL29-M02"],
    "il11-allowlisting-ringfencing--zt-ringfence": ["IL29-M03"],
    "il11-allowlisting-ringfencing--zt-storage-elevation": ["IL29-M04", "IL29-M05"],
    "il11-red-blue-operations--zt-social-engineering": ["il06-offensive", "IL29-M44"],
    "il11-red-blue-operations--zt-web-attacks": ["IL29-M17", "il06-offensive"],
    "il11-red-blue-operations--zt-blue-detect": ["IL29-M07", "il06-defensive", "il06-azure-soc"],
    "il11-cyber-hero-prep--zt-hero-review": ["IL29-M45"],
    "il11-cyber-hero-prep--zt-hero-scenarios": ["IL29-M45", "IL29-M47"],
    "il11-entra-identity--sc300-lifecycle": ["IL29-M01"],
    "il11-entra-identity--sc300-zerotrust-ca": ["IL29-M01"],
    "il11-entra-identity--sc300-auth": ["IL29-M20"],
    "il11-entra-identity--sc300-hybrid": ["il06-defensive"],
    "il11-entra-identity--sc300-governance": ["il06-defensive"],
    "il11-entra-identity--sc300-troubleshoot": ["IL29-M11"],
    "il11-entra-identity--sc300-exam-prep": ["IL29-M33"],
}
IL12_CROSSLINKS = {
    "il-12-ai-engineering-math-linalg": ["IL-16-PM-LINALG"],
    "il-12-ai-engineering-math-stats": ["IL-16-PM-STATS"],
    "il-12-ai-engineering-math-discrete": ["IL-16-PM-DISCRETE"],
    "aieng-python-foundations--py-syntax-core": ["python-for-ml--numpy-pandas-practice"],
    "aieng-python-foundations--py-oop-modular": ["python-for-ml--python-ml-ecosystem"],
    "aieng-python-foundations--py-concurrency": ["python-for-ml--python-ml-ecosystem"],
    "aieng-python-foundations--py-genai-workflow": ["ai-enabled-software--llm-apis-practice"],
    "aieng-data-science--numpy-foundations": ["python-for-ml--numpy-pandas-practice"],
    "aieng-data-science--pandas-wrangling": ["python-for-ml--numpy-pandas-practice"],
    "aieng-data-science--viz-matplotlib-seaborn": ["python-for-ml--visualization-practice"],
    "aieng-data-science--statistics-for-ml": ["IL-16-PM-STATS"],
    "aieng-data-science--model-dev-workflow": ["ml-in-practice--ml-workflow"],
    "aieng-data-science--sql-for-ai-engineers": ["python-for-ml--working-with-real-data"],
    "aieng-machine-learning--supervised-learning": ["ml-in-practice--ml-workflow"],
    "aieng-machine-learning--unsupervised-learning": ["advanced-ml--probabilistic-ml"],
    "aieng-machine-learning--reinforcement-intro": ["advanced-ml--optimization-advanced"],
    "aieng-machine-learning--validation-tuning": ["ml-in-practice--model-evaluation-practice"],
    "aieng-machine-learning--feature-engineering": ["ml-in-practice--feature-engineering-practice"],
    "aieng-machine-learning--evaluation-metrics": ["ml-in-practice--model-evaluation-practice"],
    "aieng-deep-learning--neural-foundations": ["advanced-ml--deep-architectures-practice"],
    "aieng-deep-learning--backprop-optimization": ["advanced-ml--optimization-advanced"],
    "aieng-deep-learning--cnns": ["advanced-ml--deep-architectures-practice"],
    "aieng-deep-learning--sequence-models": ["advanced-nlp-practice--sequence-models-practice"],
    "aieng-deep-learning--regularization-tuning": ["advanced-ml--optimization-advanced"],
    "aieng-deep-learning--pytorch-workflows": ["python-for-ml--sklearn-api-practice"],
    "aieng-generative-ai--transformers-attention": ["advanced-genai--transformer-arch-practice"],
    "aieng-generative-ai--gpt-vs-bert": ["advanced-genai--transformer-arch-practice"],
    "aieng-generative-ai--gans-vaes": ["advanced-ml--deep-architectures-practice"],
    "aieng-generative-ai--diffusion-generation": ["advanced-ml--deep-architectures-practice"],
    "aieng-generative-ai--prompt-engineering": ["ai-enabled-software--llm-apis-practice"],
    "aieng-generative-ai--llm-apis-rag": ["ai-enabled-software--rag-practice"],
    "aieng-generative-ai--vecdb-depth": ["ai-enabled-software--rag-practice"],
    "aieng-generative-ai--advanced-retrieval": ["ai-enabled-software--rag-practice"],
    "aieng-generative-ai--genai-finetuning": ["advanced-genai--pretrain-finetune-practice"],
    "aieng-generative-ai--multimodal-foundation-models": ["advanced-genai--transformer-arch-practice"],
    "aieng-generative-ai--vision-speech-apps": ["advanced-genai--inference-serving-practice"],
    "aieng-generative-ai--llm-alignment-rlhf-dpo": ["advanced-genai--alignment-practice"],
    "aieng-nlp--text-preprocessing": ["advanced-nlp-practice--nlp-pipelines-practice"],
    "aieng-nlp--tokenization-embeddings": ["advanced-nlp-practice--embeddings-practice"],
    "aieng-nlp--nltk-classics": ["advanced-nlp-practice--nlp-pipelines-practice"],
    "aieng-nlp--sequence-models-nlp": ["advanced-nlp-practice--sequence-models-practice"],
    "aieng-nlp--hf-pipelines": ["advanced-nlp-practice--llm-for-nlp"],
    "aieng-agentic-ai--agent-architectures": ["agentic-ai-foundations--agent-loops"],
    "aieng-agentic-ai--tool-use": ["agentic-ai-foundations--llm-tool-use"],
    "aieng-agentic-ai--mcp-protocol": ["agentic-ai-foundations--multi-agent-systems"],
    "aieng-agentic-ai--langchain-autogen": ["agentic-ai-foundations--multi-agent-systems"],
    "aieng-agentic-ai--context-engineering": ["agentic-ai-foundations--memory-context"],
    "aieng-agentic-ai--copilot-studio": ["agentic-ai-lowcode--lowcode-platforms"],
    "aieng-agentic-ai--azure-ai-foundry": ["agentic-ai-lowcode--lowcode-deploy"],
    "aieng-agentic-ai--agent-autonomy-ceilings": ["agentic-ai-for-iv--agentic-system-design"],
    "aieng-azure-ai-900--azure-ai-services": ["agentic-ai-lowcode--lowcode-platforms"],
    "aieng-azure-ai-900--ml-concepts-azure": ["ml-in-practice--ml-workflow"],
    "aieng-azure-ai-900--responsible-ai": ["agentic-ai-for-leaders--leader-agent-governance"],
    "aieng-azure-ai-900--cost-governance": ["agentic-ai-for-leaders--leader-agent-metrics"],
    "aieng-production--prod-mlops-framing": ["ml-in-practice--ml-pipelines-practice"],
    "aieng-production--prod-serving": ["advanced-genai--inference-serving-practice"],
    "aieng-production--prod-monitoring": ["ai-enabled-software--eval-harness-practice"],
    "aieng-production--agentops-observability": ["agentic-ai-foundations--agent-evaluation"],
    "aieng-production--prod-cost-latency": ["advanced-genai--inference-serving-practice"],
    "aieng-production--prod-red-team": ["agentic-ai-for-swe--review-agents"],
    "aieng-production--trajectory-eval-agents": ["agentic-ai-foundations--agent-evaluation"],
    "aieng-production--prod-pipelines": ["ml-in-practice--ml-pipelines-practice"],
    "aieng-production--experiment-tracking-registry": ["ml-in-practice--ml-deployment-practice"],
    "aieng-production--feature-stores": ["ml-in-practice--feature-engineering-practice"],
    "aieng-production--data-centric-ai": ["python-for-ml--working-with-real-data"],
    "aieng-production--edge-ondevice-ai": ["advanced-genai--inference-serving-practice"],
    "aieng-capstone--capstone-framing": ["applied-ai-production--problem-framing-ai"],
    "aieng-capstone--capstone-build": ["advanced-genai--genai-capstone"],
    "aieng-capstone--capstone-eval": ["advanced-genai--genai-eval-practice"],
    "aieng-capstone--capstone-deploy": ["ml-in-practice--ml-deployment-practice"],
    "aieng-capstone--capstone-rai": ["agentic-ai-for-leaders--leader-agent-governance"],
    "aieng-capstone--capstone-portfolio": ["applied-ai-production--applied-ai-capstone"],
}

# ------------------------------------------------------------ study guides
SG_PACING = {
    "IL-07": [
        "Weeks 1-2 — Data foundations: math primers, MongoDB, the data-school spine (~2 modules/week).",
        "Weeks 3-4 — Analytics + ML: AI/ML module, NeuroAI, open-weight self-hosting; run every SQL playground.",
        "Weeks 5-6 — Agents + frontier: agent harnesses, frontier AI topics, AWS data and ML engineering.",
        "Week 7 — Certification gates: clear the AWS, Databricks, CompTIA Data+, and dbt gates twice each before booking.",
    ],
    "IL-08": [
        "Weeks 1-2 — Math spine: discrete math and logic primers, then the MIT 6-3 distilled core.",
        "Weeks 3-4 — Systems and theory: the CMU spine, the Stanford cross-walk, and every proof-to-code exercise.",
    ],
    "IL-09": [
        "Weeks 1-2 — Core stack: math primers, then CompTIA A+/Network+/Security+ modules with timed gates.",
        "Weeks 3-4 — Security track: CySA+, PenTest+, SecurityX; vendor AI and Oracle modules.",
        "Weeks 5-6 — Linux Foundation blockchain, C++/Python institutes; clear every gate twice before booking any exam.",
    ],
    "IL-10": [
        "Weeks 1-2 — Career foundation: quantitative reasoning, the forward-deployed career, self-knowledge assessment.",
        "Weeks 3-4 — Build: entrepreneurship track, quantitative finance ladder, portfolio capstone.",
    ],
    "IL-11": [
        "Weeks 1-3 — Zero-trust foundations: perimeter fall, NIST tenets, CISA maturity model, default-deny architecture.",
        "Weeks 4-6 — Network/crypto and AD defense: OSI/TCP/IP under attack, hashing, encryption, AD attacks and hardening.",
        "Weeks 7-9 — Allowlisting, ringfencing, storage/elevation; red/blue operations and detection.",
        "Weeks 10-12 — Cyber Hero prep: full review, scenario capstone, SC-300 identity modules; clear Security+ and CySA+ gates twice before booking.",
    ],
    "IL-12": [
        "Weeks 1-3 — Foundations: prereq math primers, Python, NumPy/pandas, statistics for ML.",
        "Weeks 4-8 — Classical ML: supervised, unsupervised, RL first contact, validation, features, metrics.",
        "Weeks 9-13 — Deep learning: neural foundations, backprop, CNNs, sequences, regularization, PyTorch workflows.",
        "Weeks 14-19 — Generative AI and NLP: transformers, RAG, vector DBs, fine-tuning, alignment, Hugging Face.",
        "Weeks 20-24 — Agentic AI, Azure AI-900, production MLOps, and the 6-part capstone.",
        "Final — Certification gates: clear the AWS MLA, Databricks, and TensorFlow gates twice before booking.",
    ],
}
SG_RULES = {
    "IL-07": ["Do the math primers before the ML modules.", "Run every SQL playground query yourself.", "Clear each certification gate twice on separate days."],
    "IL-08": ["Write every proof by hand before reading the solution.", "Code every algorithm you prove."],
    "IL-09": ["Map each study session to a published exam domain.", "Book only after clearing the gate twice."],
    "IL-10": ["Ship the portfolio pieces, not just the plans.", "Get one outside review of the resume before the capstone."],
    "IL-11": ["Do the math primers before the crypto modules.", "Run every lab on a disposable VM, never your host.", "Clear each certification gate twice on separate days."],
    "IL-12": ["Do the math primers before neural foundations.", "Train every model yourself; never copy a trained artifact.", "Clear each certification gate twice on separate days."],
}

# ------------------------------------------------------------ honesty notes
HN_IL07_ADD = (" This is an independent preparation and practice course aligned to publicly "
    "published exam objectives. It is not affiliated with, endorsed by, or sponsored by AWS, "
    "MongoDB, Databricks, dbt Labs, CompTIA, Stanford, or any model provider; it confers no "
    "certificate and grants no credentials. Exam facts (domains, weights, question counts, "
    "durations, passing scores) reflect publicly published objectives as of October 2026 — "
    "always verify against the vendor's current published objectives before booking.")
HN_IL11_ADD = (" This is an independent preparation and practice course aligned to publicly "
    "published exam objectives. It is not affiliated with, endorsed by, or sponsored by "
    "Microsoft, CompTIA, NIST, or CISA; it confers no certificate and grants no credentials. "
    "Exam facts (domains, weights, question counts, durations, passing scores) reflect publicly "
    "published objectives as of October 2026 — always verify against the vendor's current "
    "published objectives before booking.")
HN_IL12_ADD = (" This is an independent preparation and practice course aligned to publicly "
    "published exam objectives. It is not affiliated with, endorsed by, or sponsored by AWS, "
    "Databricks, or Google/TensorFlow; it confers no certificate and grants no credentials. "
    "Exam facts (domains, weights, question counts, durations, passing scores) reflect publicly "
    "published objectives as of October 2026 — always verify against the vendor's current "
    "published objectives before booking.")

SL_DBT = {"url": "https://flashgenius.net/certification-explorer/dbt-analytics-engineering-certification",
          "name": "dbt Analytics Engineering Certification (certification catalog entry)",
          "retrieved": RETRIEVED}
SL_TF = {"url": "https://www.bomberbot.com/tensorflow/how-to-ace-the-tensorflow-developer-certificate-exam-an-experts-guide/",
         "name": "TensorFlow Developer Certificate exam guide (format reference)",
         "retrieved": RETRIEVED}

# ---------------------------------------------------------------- build loop
CONFIG = {
    "IL-07": {
        "file": "il-07-data-engineering-analytics-ai.json",
        "crosslinks": IL07_CROSSLINKS,
        "sections": IL07_SECTIONS,
        "gates": [GATE_DBT],
        "crosswalk_add": [XW_DBT],
        "source_add": [SL_DBT],
        "honesty_add": HN_IL07_ADD,
        "readiness": rd_cert("IL-07 Certification Readiness Dashboard"),
        "m00": ["il-07-data-engineering-analytics-ai-math-stats",
                "il-07-data-engineering-analytics-ai-math-linalg"],
    },
    "IL-08": {
        "file": "il-08-algorithms-compilers-distributed-formal.json",
        "crosslinks": IL08_CROSSLINKS,
        "sections": IL08_SECTIONS,
        "gates": [],
        "crosswalk_add": [],
        "source_add": [],
        "honesty_add": "",
        "readiness": rd_foundational(
            "IL-08 Foundational Readiness Dashboard",
            "two proof-to-code projects and the algorithms project gate."),
        "m00": ["il-08-algorithms-compilers-distributed-formal-math-discrete",
                "il-08-algorithms-compilers-distributed-formal-math-logic"],
    },
    "IL-09": {
        "file": "il-09-adaptive-certification-command.json",
        "crosslinks": IL09_CROSSLINKS,
        "sections": IL09_SECTIONS,
        "gates": [],
        "crosswalk_add": [],
        "source_add": [],
        "honesty_add": "",
        "readiness": None,  # already present
        "m00": [],
    },
    "IL-10": {
        "file": "il-10-portfolio-career-professional-practice.json",
        "crosslinks": IL10_CROSSLINKS,
        "sections": IL10_SECTIONS,
        "gates": [],
        "crosswalk_add": [],
        "source_add": [],
        "honesty_add": "",
        "readiness": rd_foundational(
            "IL-10 Professional Practice Readiness Dashboard",
            "the shipped portfolio, the reviewed resume, and the capstone gate."),
        "m00": [],
    },
    "IL-11": {
        "file": "il-11-zero-trust-endpoint-defense.json",
        "crosslinks": IL11_CROSSLINKS,
        "sections": IL11_SECTIONS,
        "gates": [GATE_CYSA],
        "crosswalk_add": [XW_CYSA],
        "source_add": [],
        "honesty_add": HN_IL11_ADD,
        "readiness": None,  # already present
        "m00": ["il-11-zero-trust-endpoint-defense-math-numtheory",
                "il-11-zero-trust-endpoint-defense-math-logic"],
    },
    "IL-12": {
        "file": "il-12-ai-engineering.json",
        "crosslinks": IL12_CROSSLINKS,
        "sections": IL12_SECTIONS,
        "gates": [GATE_TF],
        "crosswalk_add": [XW_TF],
        "source_add": [SL_TF],
        "honesty_add": HN_IL12_ADD,
        "readiness": None,  # already present
        "m00": ["il-12-ai-engineering-math-linalg",
                "il-12-ai-engineering-math-stats",
                "il-12-ai-engineering-math-discrete"],
    },
}

def build(code, cfg):
    d = json.load(open(BASE + cfg["file"]))
    # 1. schema
    d["schemaVersion"] = "4"
    d["updatedAt"] = RETRIEVED
    # 2. missing sections
    for k, v in cfg["sections"].items():
        if k not in d or d[k] is None:
            d[k] = v
    # 3. readiness dashboard
    if cfg["readiness"] is not None:
        d["readinessDashboard"] = cfg["readiness"]
    # 4. cross-links on modules
    by_id = {m["id"]: m for m in d["modules"]}
    for mid, links in cfg["crosslinks"].items():
        if mid in by_id:
            existing = by_id[mid].get("crossLinks") or []
            seen = list(dict.fromkeys(list(existing) + list(links)))
            by_id[mid]["crossLinks"] = seen
    # 5. cert gates + crosswalk (no dup ids)
    have = {g.get("id") for g in d.get("certGates", [])}
    for g in cfg["gates"]:
        if g["id"] not in have:
            d["certGates"].append(copy.deepcopy(g))
    have_xw = {x.get("cert") for x in d.get("crosswalk", [])}
    for x in cfg["crosswalk_add"]:
        if x["cert"] not in have_xw:
            d["crosswalk"].append(copy.deepcopy(x))
    have_sl = {s.get("url") for s in d.get("sourceLinks", []) if isinstance(s, dict)}
    for s in cfg["source_add"]:
        if s["url"] not in have_sl:
            d["sourceLinks"].append(copy.deepcopy(s))
    # 6. honesty note vendors
    if cfg["honesty_add"]:
        d["honestyNote"] = (d.get("honestyNote", "") or "").rstrip() + cfg["honesty_add"]
    # 7. interactivity audit (after sections in place)
    d["interactivityAudit"] = interactivity_audit(d)
    # 8. study guide
    hours0 = d.get("hours")
    sg = study_guide(code, hours0, SG_PACING[code], SG_RULES[code])
    d["studyGuide"] = sg
    # 9. honest hours
    total_min = sum(m.get("estimatedMinutes", 0) for m in d["modules"])
    hours = int(round(total_min / 60))
    d["hours"] = hours
    d["studyGuide"]["totalHours"] = hours
    d["studyGuide"]["totalMinutes"] = total_min
    # 10. validate
    missing = [k for k in REQUIRED if k not in d]
    assert not missing, (code, "missing", missing)
    assert d["schemaVersion"] == "4", code
    json.dumps(d)  # serializable
    # write
    out = BASE + cfg["file"]
    tmp = out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    json.load(open(tmp))  # validate before replacing
    os.replace(tmp, out)
    linked = sum(1 for m in d["modules"] if m.get("crossLinks"))
    print("%s: modules=%d linked=%d gates=%d hours=%d (was %s) minutes=%d"
          % (code, len(d["modules"]), linked, len(d.get("certGates", [])),
             hours, hours0, total_min))

if __name__ == "__main__":
    for code, cfg in CONFIG.items():
        build(code, cfg)
    print("BUILD OK")
