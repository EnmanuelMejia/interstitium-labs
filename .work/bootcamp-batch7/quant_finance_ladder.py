# Batch 7 — quant-finance-ladder: Quantitative Finance: The Ladder
DOMAIN = "quant-finance-ladder"

SIMS = [
    {
        "id": "quant-finance-ladder-sim-1",
        "title": "Why Did the Backtest Lie?",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Your momentum strategy shows a 2.1 Sharpe in backtest and loses money live. Diagnose the gap.",
        "steps": [
            {
                "symptom": "Backtest Sharpe 2.1 (2018–2023). Live trading: -4% in two months. Same code.",
                "evidence": [
                    ["Backtest data", "Survivorship-biased equity universe (only stocks still listed in 2023)"],
                    ["Costs", "Backtest assumed zero slippage, zero fees"],
                    ["Live fills", "Average slippage 8 bps per trade; strategy trades 400x/year"]
                ],
                "options": [
                    "The market regime changed — wait for mean reversion",
                    "Look-ahead and cost bias: survivorship bias inflated returns, and 400 trades/year × 8 bps slippage eats the entire edge — the backtest never modeled reality",
                    "Increase leverage to recover the losses"
                ],
                "correct": 1,
                "explain": "Two classic lies: survivorship bias (dead stocks don't drag the backtest) and frictionless trading (400 × 8bps ≈ 3.2%/year of phantom edge). Honest backtests use point-in-time universes and real cost models."
            },
            {
                "symptom": "You rebuild with a point-in-time universe and 10 bps all-in costs. Sharpe drops to 0.9. Is the strategy dead?",
                "evidence": [
                    ["Honest Sharpe", "0.9 over 6 years"],
                    ["Drawdown", "Max 14%, recovers within 8 months historically"],
                    ["Capacity", "Edge decays above $50M AUM"]
                ],
                "options": [
                    "Dead — 0.9 Sharpe isn't worth trading",
                    "Viable at small scale: 0.9 Sharpe with contained drawdowns is a real edge if sized honestly and kept under capacity",
                    "Add leverage until the Sharpe looks good again"
                ],
                "correct": 1,
                "explain": "0.9 honest Sharpe is a tradeable edge at appropriate size. The ladder lesson: most 'dead' strategies were never alive (biased), and most 'mediocre' honest ones are careers. Size to capacity, not to dreams."
            },
            {
                "symptom": "What's the permanent research practice this incident demands?",
                "evidence": [
                    ["Constraint", "Must prevent biased backtests from reaching production again"],
                    ["Goal", "Every future strategy gets the honest treatment by default"]
                ],
                "options": [
                    "Only trade strategies with backtest Sharpe above 2.0",
                    "A research checklist enforced in code: point-in-time data, survivorship-free universe, cost model, out-of-sample holdout, and a pre-registered hypothesis",
                    "Hire a consultant to bless each backtest"
                ],
                "correct": 1,
                "explain": "Process beats brilliance: pre-register the hypothesis (no p-hacking), enforce point-in-time data and costs in the pipeline, and keep a true holdout. The checklist is the junior quant's senior."
            }
        ],
        "debrief": "Backtests lie by bias (survivorship, look-ahead) and by omission (costs). The professional standard: honest data, honest costs, pre-registered hypotheses, and sizing to measured capacity.",
        "points": 15
    },
    {
        "id": "quant-finance-ladder-sim-2",
        "title": "Two Offers",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "You're a junior quant with two offers: a bank's prestigious rotational program, or a 12-person prop shop. Choose the ladder.",
        "steps": [
            {
                "id": "offers",
                "text": "Offer A: bulge-bracket bank, rotational program, famous name, $180k, slow promotion, heavy process. Offer B: 12-person prop shop, $150k + real P&L cut, you ship to production in month two, unknown name. Your career goal: become a genuinely good quant.",
                "choices": [
                    {"label": "Take the bank — prestige compounds and the name opens doors forever", "feedback": "Prestige is real currency, but two years of rotational PowerPoint teaches you process, not P&L. You'll know the bank's politics intimately and trading barely at all.", "points": 4, "next": "bank"},
                    {"label": "Take the prop shop — P&L responsibility early is the fastest teacher", "feedback": "Month two, your code has real money on it. Every mistake costs basis points you feel personally. Nothing teaches like P&L.", "points": 10, "next": "prop"},
                    {"label": "Negotiate the bank up and take whichever pays more", "feedback": "Optimizing year-one comp is the classic junior mistake — the learning rate, not the salary, determines year-five comp.", "points": 2, "next": "bank"}
                ]
            },
            {
                "id": "bank",
                "text": "Eighteen months at the bank: you've rotated through three desks, built exactly one model that traded (briefly), and your bonus was formulaic. A prop shop calls. What now?",
                "choices": [
                    {"label": "Stay — you're up for Associate and the pension vests", "feedback": "The golden handcuffs close one link at a time. In five years you'll be a well-paid process expert who has never owned risk.", "points": 2, "next": "END"},
                    {"label": "Leave now — the 18 months bought you just enough credibility to get the prop seat, and the learning clock is ticking", "feedback": "Correct late is better than comfortable forever. You banked the brand name; now go buy the skill.", "points": 7, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "prop",
                "text": "Year one at the prop shop: your first strategy made money, your second lost $200k in a week (a bug, not the market). The partners are watching. How do you handle the post-mortem?",
                "choices": [
                    {"label": "Blame the market regime — the strategy was sound", "feedback": "It was a bug, and everyone knows it. Denial at a prop shop is a career-ending move — trust is the only currency.", "points": 1, "next": "END"},
                    {"label": "Own the bug completely, present the fixed validation pipeline, and show the checklist that would have caught it", "feedback": "Prop shops forgive bugs; they don't forgive cover-ups. The post-mortem with a systemic fix is how juniors become seniors.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "The ladder isn't prestige — it's P&L proximity. Choose the seat closest to real risk earliest, own mistakes completely, and let the learning rate (not year-one comp) drive the decision.",
        "points": 20
    },
    {
        "id": "quant-finance-ladder-sim-3",
        "title": "Climb the Ladder",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Order the quant career climb from undergraduate preparation to senior quant readiness.",
        "steps": {
            "context": "The full climb, honestly mapped. Put the stages in order.",
            "items": [
                "Undergraduate foundation: probability, statistics, linear algebra, programming",
                "Graduate credential: financial mathematics / statistics / CS with real projects",
                "Junior seat: own a small piece of production risk, learn the cost of mistakes",
                "Mid-level: own a strategy or book end-to-end — research, risk, and P&L",
                "Senior: allocate capital and mentor — your edge is now other people's growth"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Math, credential, production scar tissue, ownership, then leverage through others. The fork is real (bank vs. prop vs. tech), but the ladder's rungs don't change.",
        "points": 10
    },
    {
        "id": "quant-finance-ladder-sim-4",
        "title": "Audit the Resume",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A junior quant's resume is one hiring-manager skim away from the bin. Find the 3 lines that kill it.",
        "steps": {
            "config": "# resume.conf — junior quant\nsharpe_claim = 3.2 (backtest)     # line 2\npnl_attribution = 'team P&L'        # line 3\nskills = python, pandas, excel       # line 4\nprojects = coursework only          # line 5\nreferences = 'available on request' # line 6\ngithub = empty                       # line 7\ncontact = professional              # line 8",
            "find": 3,
            "issues": [
                {"line": 2, "description": "Sharpe 3.2 claimed from a backtest with no mention of costs, universe, or out-of-sample — every hiring manager reads this as bias, not edge.", "fix": "sharpe_claim = '1.1 (point-in-time universe, 10bps costs, 2yr out-of-sample)' — honest numbers beat big ones."},
                {"line": 3, "description": "'Team P&L' with no personal attribution — the reader assumes your contribution was zero.", "fix": "pnl_attribution = 'owned signal X: +$180k net of costs, 2024' — name your slice."},
                {"line": 5, "description": "Coursework-only projects — every applicant has coursework; none of it traded.", "fix": "projects = 'independent backtest engine on GitHub with honest cost model' — show, don't list."}
            ]
        },
        "debrief": "Lines 4, 6, 7, 8 are neutral or fixable. The killers: an unqualified backtest Sharpe, unattributed P&L, and zero evidence of independent work. Quant hiring managers read resumes as research papers — methods section required.",
        "points": 15
    },
    {
        "id": "quant-finance-ladder-sim-5",
        "title": "The Interview Loop",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "Final round at a top fund. The interviewer slides a brainteaser across the table — then watches HOW you think.",
        "steps": [
            {
                "id": "loop",
                "text": "'You have a biased coin with unknown bias. How do you simulate a fair coin?' You know the von Neumann answer. What's the winning response structure?",
                "choices": [
                    {"label": "Blurt the answer immediately — speed impresses", "feedback": "Speed without structure looks memorized. They wanted to see reasoning, and you showed recall.", "points": 2, "next": "blurt"},
                    {"label": "Think aloud: define the goal, propose flip-pairs, derive why HT/TH are equiprobable, note the efficiency cost", "feedback": "The full performance: problem framing, derivation, AND the practical caveat (expected flips). That's a quant thinking, not reciting.", "points": 10, "next": "depth"},
                    {"label": "'I'd look it up — in practice I'd just use a library.'", "feedback": "Honest, but the interview tests reasoning under uncertainty — the actual job. Libraries don't save you when the library is wrong.", "points": 3, "next": "blurt"}
                ]
            },
            {
                "id": "blurt",
                "text": "Follow-up: 'Now the bias drifts over time. Your von Neumann trick breaks. What now?' You're off-balance. Recover how?",
                "choices": [
                    {"label": "Guess: 'Use more flips?'", "feedback": "Guessing under pressure is the opposite of the job. The interviewer notes it.", "points": 1, "next": "END"},
                    {"label": "Rebuild from first principles aloud: 'The trick needs stationarity — with drift I'd estimate the bias in windows and...'", "feedback": "Recovery by method: you named the broken assumption and rebuilt. Interviewers remember recoveries more than perfect runs.", "points": 7, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "depth",
                "text": "The interviewer leans in: 'Good. Now — when would you NOT use the fair coin even if you could build it?'",
                "choices": [
                    {"label": "'When the cost of flips exceeds the value of fairness — e.g., low-stakes decisions where bias doesn't matter.'", "feedback": "You reached for the meta-question: engineering is cost-benefit, not purity. The interviewer smiles — that's the senior answer.", "points": 10, "next": "END"},
                    {"label": "'Never — fairness is always worth it.'", "feedback": "Absolutism in a quant interview is a red flag. Everything has a price, including elegance.", "points": 3, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Quant interviews test reasoning structure, not recall: think aloud, name your assumptions, derive, then price the solution. And when you stumble, rebuild from first principles — recovery is the real test.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "quant-finance-ladder-console-1",
        "title": "Query the Trades Table",
        "console": "sql-studio",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The research database holds every fill. Build the trades table and run the attribution queries.",
        "tasks": [
            {"id": "quant-finance-ladder-console-1-t1", "instruction": "Create the table 'trades' with columns: id INT, symbol TEXT, pnl INT, strategy TEXT.", "validate": {"action": "create-table", "params": {"name": "trades", "columns": "id INT, symbol TEXT, pnl INT, strategy TEXT"}}, "hint": "Tables section: create 'trades' with columns exactly: id INT, symbol TEXT, pnl INT, strategy TEXT."},
            {"id": "quant-finance-ladder-console-1-t2", "instruction": "Create an index on trades(strategy) — attribution is always by strategy.", "validate": {"action": "create-index", "params": {"table": "trades", "column": "strategy"}}, "hint": "Create index: TABLE trades, COLUMN strategy."},
            {"id": "quant-finance-ladder-console-1-t3", "instruction": "Run: total P&L by strategy.", "validate": {"action": "run-query", "params": {"match": "SUM(pnl)"}}, "hint": "Type: SELECT strategy, SUM(pnl) FROM trades GROUP BY strategy; — must contain SUM(pnl)."},
            {"id": "quant-finance-ladder-console-1-t4", "instruction": "Run: losing trades only.", "validate": {"action": "run-query", "params": {"match": "pnl < 0"}}, "hint": "Type: SELECT * FROM trades WHERE pnl < 0; — must contain 'pnl < 0'."}
        ],
        "debrief": "Attribution is the job: P&L by strategy, losers isolated, every basis point named. If you can't query your own track record, you don't have one."
    },
    {
        "id": "quant-finance-ladder-console-2",
        "title": "Guard the Research Database",
        "console": "db-admin",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Point-in-time data is the crown jewels. Create the database, gate access, and back it up.",
        "tasks": [
            {"id": "quant-finance-ladder-console-2-t1", "instruction": "Create a database named 'marketdata'.", "validate": {"action": "create-database", "params": {"name": "marketdata"}}, "hint": "Databases section: create 'marketdata'."},
            {"id": "quant-finance-ladder-console-2-t2", "instruction": "Create a database user named 'researcher'.", "validate": {"action": "create-user", "params": {"name": "researcher"}}, "hint": "Users & grants: create user 'researcher'."},
            {"id": "quant-finance-ladder-console-2-t3", "instruction": "Grant SELECT on 'marketdata' to 'researcher' — researchers read; they don't rewrite history.", "validate": {"action": "grant-priv", "params": {"db": "marketdata", "user": "researcher", "priv": "SELECT"}}, "hint": "Grants form: DB marketdata, USER researcher, PRIVILEGE SELECT."},
            {"id": "quant-finance-ladder-console-2-t4", "instruction": "Back up 'marketdata'.", "validate": {"action": "backup", "params": {"db": "marketdata"}}, "hint": "Click 'Back up' on marketdata."}
        ],
        "debrief": "Research data gets research-grade custody: read-only for researchers (history must be immutable), backed up always. A corrupted point-in-time database corrupts every backtest built on it."
    },
    {
        "id": "quant-finance-ladder-console-3",
        "title": "Work the Trading Desk Queue",
        "console": "ticketing",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Production issues on a trading desk are P1 by default. Triage the queue.",
        "tasks": [
            {"id": "quant-finance-ladder-console-3-t1", "instruction": "Create a P1 ticket titled 'Strategy X filling 8bps wide of model'.", "validate": {"action": "create-ticket", "params": {"title": "Strategy X filling 8bps wide of model", "priority": "P1"}}, "hint": "New ticket: TITLE exactly as given, PRIORITY P1."},
            {"id": "quant-finance-ladder-console-3-t2", "instruction": "Assign INC-9001 to 'desk-quant'.", "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "desk-quant"}}, "hint": "Assign form: INC-9001 → desk-quant."},
            {"id": "quant-finance-ladder-console-3-t3", "instruction": "Move INC-9001 to 'in-progress'.", "validate": {"action": "update-status", "params": {"id": "INC-9001", "status": "in-progress"}}, "hint": "Update status: INC-9001 → in-progress."}
        ],
        "debrief": "On a trading desk, the queue IS risk management: log the deviation, assign an owner, move it now. Slippage doesn't wait for the next sprint."
    },
    {
        "id": "quant-finance-ladder-console-4",
        "title": "Ship the Research Pipeline",
        "console": "cicd-pipeline",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Research code ships through the same gates as everything else. Trigger, fix, configure, approve.",
        "tasks": [
            {"id": "quant-finance-ladder-console-4-t1", "instruction": "Trigger a new build of the research pipeline.", "validate": {"action": "trigger-build", "params": {}}, "hint": "Click 'Trigger new build'."},
            {"id": "quant-finance-ladder-console-4-t2", "instruction": "Retry the failed 'test' stage (the backtest validation suite).", "validate": {"action": "retry-stage", "params": {"stage": "test"}}, "hint": "Click Retry on test."},
            {"id": "quant-finance-ladder-console-4-t3", "instruction": "Set variable COST_MODEL_BPS to 10 — the honest cost model is now pipeline-enforced.", "validate": {"action": "set-variable", "params": {"key": "COST_MODEL_BPS", "value": "10"}}, "hint": "Variables: KEY COST_MODEL_BPS, VALUE 10."},
            {"id": "quant-finance-ladder-console-4-t4", "instruction": "Approve the gated 'deploy' stage.", "validate": {"action": "approve-stage", "params": {"stage": "deploy"}}, "hint": "Click Approve on deploy."}
        ],
        "debrief": "The research checklist from sim-1 lives here as pipeline: enforced cost models, validation suites, human approval before production. Process is the senior you don't have yet."
    }
]

MISSIONS = [
    {
        "id": "quant-finance-ladder-term-1",
        "title": "Survey the Desk",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Orient on the research workstation: list files, read the notes.",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "notes.txt", "hint": "Type: ls."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "grep", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Desk surveyed. Know your data before you trade on it."
    },
    {
        "id": "quant-finance-ladder-term-2",
        "title": "Record the Fills",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Log today's fills to fills.txt — the research journal starts here.",
        "objectives": ["Write the first fill", "Append a second fill", "Read the journal"],
        "checks": [
            {"command_pattern": "echo.*>\\s*fills\\.txt", "expect_contains": "", "hint": "Type: echo \"AAPL +120bps\" > fills.txt (no output on success)."},
            {"command_pattern": "echo.*>>\\s*fills\\.txt", "expect_contains": "", "hint": "Type: echo \"MSFT -35bps\" >> fills.txt."},
            {"command_pattern": "cat\\s+fills\\.txt", "expect_contains": "AAPL", "hint": "Type: cat fills.txt."}
        ],
        "success_message": "Fills recorded. The journal is the difference between trading and gambling."
    },
    {
        "id": "quant-finance-ladder-term-3",
        "title": "Attribute the P&L",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Count your fills and isolate the winners — attribution in the shell.",
        "objectives": ["Count fill lines", "Search for the winning ticker"],
        "checks": [
            {"command_pattern": "wc\\s+-l\\s+fills\\.txt", "expect_contains": "fills.txt", "hint": "Type: wc -l fills.txt."},
            {"command_pattern": "grep\\s+AAPL\\s+fills\\.txt", "expect_contains": "AAPL", "hint": "Type: grep AAPL fills.txt."}
        ],
        "success_message": "Attributed. Every basis point named, every fill owned."
    },
    {
        "id": "quant-finance-ladder-term-4",
        "title": "Seal the Hypothesis",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Pre-register your hypothesis with a hash — no p-hacking after the fact.",
        "objectives": ["Hash the hypothesis string"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "momentum", "hint": "Type: sha256sum momentum 12-1 formation — the real hash plus your hypothesis are echoed."}
        ],
        "success_message": "Hypothesis sealed. Pre-registration is what separates research from storytelling."
    },
    {
        "id": "quant-finance-ladder-term-5",
        "title": "Check Colocation Latency",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Verify the network path to the exchange: DNS and round-trip.",
        "objectives": ["Resolve the exchange host", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig exchange.example.com."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping exchange.example.com."}
        ],
        "success_message": "Path verified. In this business, milliseconds are money — verify the road."
    },
    {
        "id": "quant-finance-ladder-term-6",
        "title": "Audit the Research Logs",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The strategy's runtime log holds the truth. Read its edges and hunt errors.",
        "objectives": ["Read the first lines", "Read the last lines", "Find errors"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "INFO", "hint": "Type: head -n 3 logs/app.log."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "ERROR", "hint": "Type: tail -n 3 logs/app.log."},
            {"command_pattern": "grep\\s+ERROR\\s+logs/app\\.log", "expect_contains": "connection refused", "hint": "Type: grep ERROR logs/app.log."}
        ],
        "success_message": "Logs audited. The live system grades your backtest daily — read the grades."
    },
    {
        "id": "quant-finance-ladder-term-7",
        "title": "Verify the Environment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Confirm the research environment: identity and home directory.",
        "objectives": ["Print the environment", "Expand HOME"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps."},
            {"command_pattern": "echo\\s+\\$HOME", "expect_contains": "/home/candidate", "hint": "Type: echo $HOME."}
        ],
        "success_message": "Environment verified. Reproducibility starts with knowing where you stand."
    }
]
