# Batch 7 — quant-finance-math: Quantitative Finance Mathematics
DOMAIN = "quant-finance-math"

SIMS = [
    {
        "id": "quant-finance-math-sim-1",
        "title": "Why Won't the Monte Carlo Converge?",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Your Monte Carlo pricer for a barrier option oscillates wildly even at 10M paths. Diagnose the variance.",
        "steps": [
            {
                "symptom": "10M paths, price estimate still swinging ±15%. Plain European options converge fine with the same engine.",
                "evidence": [
                    ["Payoff", "Knock-out barrier: payoff drops to zero if the barrier is ever touched"],
                    ["Path stats", "Only 3% of paths knock out — the payoff is discontinuous at the barrier"],
                    ["Estimator", "Naive Monte Carlo, no variance reduction"]
                ],
                "options": [
                    "Run 100M paths — brute force beats analysis",
                    "The discontinuity is the problem: naive MC converges as 1/sqrt(N) but the barrier discontinuity inflates variance enormously — use importance sampling or a Brownian-bridge correction for barrier crossings",
                    "Switch to a binomial tree"
                ],
                "correct": 1,
                "explain": "Discontinuous payoffs are variance poison for naive Monte Carlo. The fix is mathematical, not computational: importance sampling toward the barrier region, or Brownian-bridge probabilities for intra-step crossings. 100M naive paths just buys a more expensive wrong answer."
            },
            {
                "symptom": "You add a Brownian-bridge correction. Convergence improves 20x. But the price disagrees with the desk's PDE solver by 4%.",
                "evidence": [
                    ["MC price", "4.82 ± 0.03"],
                    ["PDE price", "4.63"],
                    ["Difference", "Persistent across seeds — not noise"]
                ],
                "options": [
                    "Trust the Monte Carlo — more paths can't be wrong",
                    "Suspect a modeling difference, not a numerical one: check monitoring frequency (continuous vs. discrete barrier), day-count, and rate curves — the two solvers are likely pricing different contracts",
                    "Average the two prices"
                ],
                "correct": 1,
                "explain": "Persistent cross-solver disagreement means different contracts, not bad numerics. Discrete vs. continuous barrier monitoring alone explains 4% easily. Reconcile the contract specification first — the math is only as good as the question."
            },
            {
                "symptom": "Root cause found: the PDE used discrete monitoring, MC used continuous. What's the durable practice?",
                "evidence": [
                    ["Constraint", "Every future pricer must price the same contract as the desk"],
                    ["Goal", "Specification errors caught before production, not after"]
                ],
                "options": [
                    "Always use the PDE solver — it's the desk standard",
                    "A single contract-specification artifact (monitoring dates, day count, curves) consumed by every solver, plus cross-solver reconciliation tests in CI",
                    "Document the difference in a wiki page"
                ],
                "correct": 1,
                "explain": "One contract spec, many solvers, automated reconciliation. The mathematics of pricing is downstream of the legal/economic specification — encode the spec once, test every solver against it."
            }
        ],
        "debrief": "Monte Carlo failures are usually variance-structure problems (discontinuities) or specification problems (different contracts), not path-count problems. Fix the math, then fix the spec, in that order.",
        "points": 15
    },
    {
        "id": "quant-finance-math-sim-2",
        "title": "Choose the Estimator",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "You need the delta of an exotic option for tomorrow's risk run. Three estimators, one night. Choose with theory.",
        "steps": [
            {
                "id": "estimator",
                "text": "Exotic option, discontinuous payoff, need delta by morning. Candidates: (A) bump-and-revalue finite differences, (B) pathwise differentiation, (C) likelihood-ratio (score function) method. Your call?",
                "choices": [
                    {"label": "A — bump-and-revalue: simple, always works", "feedback": "Simple and wrong here: finite differences on a discontinuous payoff give pure noise — the bump crosses the discontinuity randomly. You'll report a delta that's mostly artifact.", "points": 2, "next": "noise"},
                    {"label": "B — pathwise: differentiate inside the expectation", "feedback": "Pathwise needs payoff differentiability almost surely — the barrier discontinuity violates it. The estimator is biased and you won't know by how much.", "points": 4, "next": "biased"},
                    {"label": "C — likelihood ratio: differentiate the density, not the payoff", "feedback": "The score-function method differentiates the KNOWN density, never the discontinuous payoff. Unbiased for the true delta — the theoretically correct choice for discontinuous payoffs.", "points": 10, "next": "correct"}
                ]
            },
            {
                "id": "noise",
                "text": "The bump-and-revalue delta flips sign between runs. The risk manager asks if the book is hedged. What do you say?",
                "choices": [
                    {"label": "'The delta is approximately zero — we're hedged.'", "feedback": "Reporting noise as a number is how books blow up. The honest answer is the only one.", "points": 0, "next": "END"},
                    {"label": "'The estimator is unstable on this payoff — I'm switching to likelihood-ratio tonight and will have a real number by morning.'", "feedback": "Honest about the failure, correct about the fix, specific about the timeline. That's the recovery.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "biased",
                "text": "The pathwise delta looks stable — suspiciously stable. A colleague notes the payoff's discontinuity. How do you check for bias?",
                "choices": [
                    {"label": "Compare against likelihood-ratio on a test case — if they disagree, pathwise is biased", "feedback": "Cross-estimator validation: the unbiased method is the referee. Theory predicts the disagreement; measurement confirms it.", "points": 7, "next": "END"},
                    {"label": "Increase paths until it stabilizes further", "feedback": "Bias doesn't vanish with more paths — that's what makes it bias. You're converging to the wrong number with increasing confidence.", "points": 1, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "correct",
                "text": "Likelihood-ratio gives a stable, theoretically clean delta — but with high variance. The risk run is in 6 hours. How do you tame it?",
                "choices": [
                    {"label": "Accept the variance — unbiased is unbiased", "feedback": "An unbiased estimator with huge variance still produces unusable risk numbers. Theory chose the method; engineering must finish the job.", "points": 4, "next": "END"},
                    {"label": "Add a control variate — price the vanilla counterpart analytically and simulate only the exotic spread", "feedback": "The classic variance kill: the control variate absorbs what Black-Scholes already knows, leaving MC to price only the exotic remainder. Unbiased AND tight.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Estimator choice is theory applied: discontinuous payoff → differentiate the density (likelihood ratio), then kill variance with control variates. The mathematics tells you which tool; the deadline tells you to finish the job.",
        "points": 20
    },
    {
        "id": "quant-finance-math-sim-3",
        "title": "Derive the Hedge",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "Order the logical steps of the Black-Scholes derivation — the no-arbitrage argument that built modern finance.",
        "steps": {
            "context": "The Black-Scholes argument in logical order, from market assumption to PDE.",
            "items": [
                "Assume the underlying follows geometric Brownian motion with constant volatility",
                "Construct a hedged portfolio: long the option, short delta shares of stock",
                "Choose delta to eliminate the random (dW) term — the portfolio becomes instantaneously riskless",
                "No-arbitrage: a riskless portfolio must earn the risk-free rate",
                "Equate the portfolio's drift to r — this yields the Black-Scholes PDE"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Model, hedge, eliminate randomness, invoke no-arbitrage, read off the PDE. The derivation's moral: the option's price comes from the hedge, not from anyone's view of the future — that's why the drift vanishes.",
        "points": 10
    },
    {
        "id": "quant-finance-math-sim-4",
        "title": "Audit the Pricing Config",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "A desk's pricing config has 3 quantitative errors. Find them before they reach production.",
        "steps": {
            "config": "# pricing.conf — exotic desk\nvol_surface = flat 20%             # line 2\nrate_curve = ois                  # line 3\nbarrier_monitoring = continuous   # line 4\nmc_paths = 10000                  # line 5\nrng_seed = fixed 42               # line 6\nnumeraire = stock                 # line 7\nday_count = ACT/365               # line 8",
            "find": 3,
            "issues": [
                {"line": 2, "description": "Flat 20% vol surface for exotics — barrier and smile-sensitive products misprice badly on flat vol; the surface must be calibrated.", "fix": "vol_surface = calibrated smile surface, recalibrated daily."},
                {"line": 4, "description": "Continuous barrier monitoring while the term sheet specifies discrete (daily close) — this is the 4% mispricing from sim-1.", "fix": "barrier_monitoring = discrete daily, matching the term sheet exactly."},
                {"line": 6, "description": "Fixed RNG seed in production — every run identical, hiding Monte Carlo error and creating false confidence.", "fix": "rng_seed = random per run in production; fixed seeds only for regression tests."}
            ]
        },
        "debrief": "Lines 3, 7, 8 are legitimate choices. The killers: flat vol for exotics, monitoring mismatch vs. the term sheet, and a fixed seed in production. Pricing configs are where theory meets the P&L — audit them like money depends on it.",
        "points": 15
    },
    {
        "id": "quant-finance-math-sim-5",
        "title": "Calibrate or Interpolate?",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The volatility surface has a hole: no quotes for 9-month 80%-strike puts. The trader needs a price now.",
        "steps": [
            {
                "id": "hole",
                "text": "No market quotes at (9M, 80% strike). The trader needs a price in ten minutes for a client. Your approach?",
                "choices": [
                    {"label": "Interpolate the surface smoothly through the hole — it's just one point", "feedback": "Smooth interpolation through a hole assumes the smile behaves — at 80% strike in a stress regime, the wing is exactly where the model risk lives.", "points": 3, "next": "smooth"},
                    {"label": "Price with the full calibrated model AND quote a wide spread reflecting the model uncertainty at that point", "feedback": "Honest pricing: the model gives a mid, the missing data widens the spread. The client pays for your uncertainty, disclosed.", "points": 10, "next": "honest"},
                    {"label": "Refuse to price — no quotes, no price", "feedback": "Principled but useless: the client goes to the competitor who WILL price it. Refusal isn't risk management; it's abdication.", "points": 2, "next": "smooth"}
                ]
            },
            {
                "id": "smooth",
                "text": "You interpolated. The client trades. A month later the wing blows out and the position loses 3x your estimate. The post-mortem question: what should the surface procedure have been?",
                "choices": [
                    {"label": "Ban interpolation entirely", "feedback": "Overcorrection — interpolation is fine where data is dense. The failure was interpolating where data was ABSENT without a uncertainty charge.", "points": 3, "next": "END"},
                    {"label": "Require model-risk add-ons that scale with distance from quoted points — the hole gets priced, but expensively", "feedback": "The durable fix: uncertainty-aware pricing. Sparse regions trade, but the spread compensates the model risk. That's a real volatility desk policy.", "points": 8, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "honest",
                "text": "The client accepts the wide spread and trades. Your manager asks: 'Why did we charge so much more than the competitor?' Your answer?",
                "choices": [
                    {"label": "'Because our model is better.'", "feedback": "Unverifiable and arrogant. The real answer is about uncertainty, not superiority.", "points": 2, "next": "END"},
                    {"label": "'Because there were no quotes there — our spread prices the model risk of the hole. If they priced tighter, they're either interpolating blind or they know something we don't.'", "feedback": "You explained the economics of the quote: data sparsity → model risk → spread. The manager now understands the desk's edge is honesty about uncertainty.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Missing market data is not a math problem — it's a pricing-of-uncertainty problem. Interpolate where data is dense; charge for model risk where it's absent; never confuse the two.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "quant-finance-math-console-1",
        "title": "Query the Distributions Table",
        "console": "sql-studio",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The research database stores fitted distributions. Build the table and query by family and fit quality.",
        "tasks": [
            {"id": "quant-finance-math-console-1-t1", "instruction": "Create the table 'distributions' with columns: id INT, name TEXT, family TEXT, ks_stat INT.", "validate": {"action": "create-table", "params": {"name": "distributions", "columns": "id INT, name TEXT, family TEXT, ks_stat INT"}}, "hint": "Tables section: create 'distributions' with columns exactly: id INT, name TEXT, family TEXT, ks_stat INT."},
            {"id": "quant-finance-math-console-1-t2", "instruction": "Create an index on distributions(family).", "validate": {"action": "create-index", "params": {"table": "distributions", "column": "family"}}, "hint": "Create index: TABLE distributions, COLUMN family."},
            {"id": "quant-finance-math-console-1-t3", "instruction": "Run a query selecting all distributions in the 'normal' family.", "validate": {"action": "run-query", "params": {"match": "normal"}}, "hint": "Type: SELECT * FROM distributions WHERE family = 'normal'; — must contain 'normal'."},
            {"id": "quant-finance-math-console-1-t4", "instruction": "Run a query ordering distributions by ks_stat ascending — best fits first.", "validate": {"action": "run-query", "params": {"match": "ORDER BY ks_stat"}}, "hint": "Type: SELECT * FROM distributions ORDER BY ks_stat; — must contain 'ORDER BY ks_stat'."}
        ],
        "debrief": "Model selection is query work: fit everything, store the statistics, rank by fit quality. The KS statistic doesn't care about your favorite distribution."
    },
    {
        "id": "quant-finance-math-console-2",
        "title": "Debug the Pricer",
        "console": "code-editor",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The Monte Carlo pricer script misbehaves. Open it, breakpoint the accumulation, and inspect.",
        "tasks": [
            {"id": "quant-finance-math-console-2-t1", "instruction": "Open the file 'app.py'.", "validate": {"action": "open-file", "params": {"name": "app.py"}}, "hint": "Explorer: click Open on app.py."},
            {"id": "quant-finance-math-console-2-t2", "instruction": "Toggle a breakpoint at app.py line 4.", "validate": {"action": "toggle-breakpoint", "params": {"file": "app.py", "line": 4}}, "hint": "Editor: click line 4."},
            {"id": "quant-finance-math-console-2-t3", "instruction": "Step over once to advance the execution.", "validate": {"action": "step-over", "params": {}}, "hint": "Click the 'Step over' button."},
            {"id": "quant-finance-math-console-2-t4", "instruction": "Inspect the variable 's'.", "validate": {"action": "inspect-variable", "params": {"name": "s"}}, "hint": "Inspect form: VARIABLE NAME s."}
        ],
        "debrief": "Pricing bugs hide in accumulation loops: breakpoint the sum, step through it, inspect the running total. The math is only right if the code computes what the math says."
    },
    {
        "id": "quant-finance-math-console-3",
        "title": "Parameterize the Model Store",
        "console": "db-admin",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Calibrated parameters are production data. Store them with access control and backups.",
        "tasks": [
            {"id": "quant-finance-math-console-3-t1", "instruction": "Create a database named 'calibrations'.", "validate": {"action": "create-database", "params": {"name": "calibrations"}}, "hint": "Databases: create 'calibrations'."},
            {"id": "quant-finance-math-console-3-t2", "instruction": "Create a database user named 'quant'.", "validate": {"action": "create-user", "params": {"name": "quant"}}, "hint": "Users & grants: create user 'quant'."},
            {"id": "quant-finance-math-console-3-t3", "instruction": "Grant SELECT on 'calibrations' to 'quant'.", "validate": {"action": "grant-priv", "params": {"db": "calibrations", "user": "quant", "priv": "SELECT"}}, "hint": "Grants form: DB calibrations, USER quant, PRIVILEGE SELECT."},
            {"id": "quant-finance-math-console-3-t4", "instruction": "Set the database parameter 'max_connections' to 200.", "validate": {"action": "set-parameter", "params": {"key": "max_connections", "value": "200"}}, "hint": "Databases section: PARAMETER max_connections, VALUE 200."}
        ],
        "debrief": "Calibration outputs are as production-critical as the models: access-controlled, backed up, and performance-tuned. A lost calibration is a lost trading day."
    },
    {
        "id": "quant-finance-math-console-4",
        "title": "Run the Simulation Pipeline",
        "console": "cicd-pipeline",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Monte Carlo batches run as pipelines. Trigger the run, fix the failed stage, approve the results.",
        "tasks": [
            {"id": "quant-finance-math-console-4-t1", "instruction": "Trigger a new build (simulation batch).", "validate": {"action": "trigger-build", "params": {}}, "hint": "Click 'Trigger new build'."},
            {"id": "quant-finance-math-console-4-t2", "instruction": "Retry the failed 'test' stage (convergence checks).", "validate": {"action": "retry-stage", "params": {"stage": "test"}}, "hint": "Click Retry on test."},
            {"id": "quant-finance-math-console-4-t3", "instruction": "Set variable MC_PATHS to 1000000.", "validate": {"action": "set-variable", "params": {"key": "MC_PATHS", "value": "1000000"}}, "hint": "Variables: KEY MC_PATHS, VALUE 1000000."},
            {"id": "quant-finance-math-console-4-t4", "instruction": "Approve the gated 'deploy' stage (publish results).", "validate": {"action": "approve-stage", "params": {"stage": "deploy"}}, "hint": "Click Approve on deploy."}
        ],
        "debrief": "Simulation at scale is operations: trigger batches, gate on convergence tests, parameterize path counts, and approve publication. The math deserves the same rigor as the code."
    }
]

MISSIONS = [
    {
        "id": "quant-finance-math-term-1",
        "title": "Survey the Lab",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Orient: list the workspace and read the notes.",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "app.py", "hint": "Type: ls."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "Linux essentials", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Lab surveyed. State the problem before solving it."
    },
    {
        "id": "quant-finance-math-term-2",
        "title": "Log the Experiment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Record Monte Carlo run parameters to mc.txt.",
        "objectives": ["Write the run config", "Append a second config", "Read the log"],
        "checks": [
            {"command_pattern": "echo.*>\\s*mc\\.txt", "expect_contains": "", "hint": "Type: echo \"paths 1000000 seed random\" > mc.txt (no output on success)."},
            {"command_pattern": "echo.*>>\\s*mc\\.txt", "expect_contains": "", "hint": "Type: echo \"paths 2000000 seed random\" >> mc.txt."},
            {"command_pattern": "cat\\s+mc\\.txt", "expect_contains": "paths", "hint": "Type: cat mc.txt."}
        ],
        "success_message": "Experiment logged. A result without its parameters is an anecdote."
    },
    {
        "id": "quant-finance-math-term-3",
        "title": "Measure the Runs",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Count experiment lines and search for the seed policy.",
        "objectives": ["Count lines", "Search for seed entries"],
        "checks": [
            {"command_pattern": "wc\\s+-l\\s+mc\\.txt", "expect_contains": "mc.txt", "hint": "Type: wc -l mc.txt."},
            {"command_pattern": "grep\\s+seed\\s+mc\\.txt", "expect_contains": "seed", "hint": "Type: grep seed mc.txt."}
        ],
        "success_message": "Measured. Count what you ran — memory lies about sample sizes."
    },
    {
        "id": "quant-finance-math-term-4",
        "title": "Seal the Specification",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Hash the contract specification — the single source of truth for every solver.",
        "objectives": ["Hash the spec string"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "barrier", "hint": "Type: sha256sum barrier discrete daily monitoring — the real hash plus your spec are echoed."}
        ],
        "success_message": "Specification sealed. One contract, many solvers — and the spec is hashed."
    },
    {
        "id": "quant-finance-math-term-5",
        "title": "Provision the Compute",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Initialize the compute backend and verify the environment.",
        "objectives": ["Initialize the backend", "Print the environment"],
        "checks": [
            {"command_pattern": "^find(\\s|$)", "expect_contains": "successfully initialized", "hint": "Type: find — initializes the backend in this sandbox."},
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps."}
        ],
        "success_message": "Compute ready. Even pure math needs working infrastructure."
    },
    {
        "id": "quant-finance-math-term-6",
        "title": "Audit the Pricing Logs",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Read the pricer log edges and hunt for errors.",
        "objectives": ["Read the first lines", "Read the last lines", "Find errors"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "server starting", "hint": "Type: head -n 2 logs/app.log."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "timeout", "hint": "Type: tail -n 2 logs/app.log."},
            {"command_pattern": "grep\\s+ERROR\\s+logs/app\\.log", "expect_contains": "ERROR", "hint": "Type: grep ERROR logs/app.log."}
        ],
        "success_message": "Logs audited. The production pricer grades your theory every day."
    },
    {
        "id": "quant-finance-math-term-7",
        "title": "Check Market Data Reachability",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Verify DNS and connectivity to the market data host.",
        "objectives": ["Resolve the host", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig marketdata.example.com."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping marketdata.example.com."}
        ],
        "success_message": "Feed reachable. No data, no calibration, no edge."
    }
]
