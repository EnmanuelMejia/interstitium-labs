# Batch 7 — entrepreneurship: Entrepreneurship: The Babson-Informed Track
DOMAIN = "entrepreneurship"

SIMS = [
    {
        "id": "entrepreneurship-sim-1",
        "title": "The Leaky Funnel",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Your SaaS gets 2,000 signups a month but only 40 become paying customers. Diagnose where the venture is actually leaking.",
        "steps": [
            {
                "symptom": "2,000 signups/month, 40 paid conversions (2%). The team wants to 'fix marketing'.",
                "evidence": [
                    ["Signup source", "70% from a viral tweet — curiosity traffic, not intent traffic"],
                    ["Activation", "Only 12% of signups ever complete onboarding"],
                    ["Paid cohort", "38 of 40 paid users came from founder-led sales calls"]
                ],
                "options": [
                    "Marketing is the problem — buy more top-of-funnel traffic",
                    "The leak is activation and intent: viral curiosity traffic never onboards, while the only converting channel is founder sales — the product isn't selling itself yet",
                    "Pricing is the problem — cut the price in half and conversions will follow"
                ],
                "correct": 1,
                "explain": "Funnel math first: 2,000 × 12% activation × conversion ≈ the 40. The viral top-of-funnel is vanity; the business runs on 38 founder-led deals. Fix onboarding and qualification before spending a dollar on traffic."
            },
            {
                "symptom": "Onboarding completion is 12%. Session replays show users stall at the 'connect your data' step.",
                "evidence": [
                    ["Drop-off", "61% of started onboardings die at data connection"],
                    ["Support tickets", "'Do I need an engineer for this?' asked 44 times"],
                    ["Happy path", "Users who skip data connection and use the demo dataset convert at 9%"]
                ],
                "options": [
                    "Add more documentation to the data-connection step",
                    "Invert the onboarding: lead with the demo dataset and time-to-value, defer data connection until the user is already convinced",
                    "Remove the data-connection step entirely"
                ],
                "correct": 1,
                "explain": "Time-to-first-value wins. The demo dataset proves value in 3 minutes; the data connection is a week-one tax. Defer the tax until after the 'aha'."
            },
            {
                "symptom": "Fixes are scoped. What single metric tells you next month whether the leak is actually closing?",
                "evidence": [
                    ["Constraint", "One number, reviewed weekly, that can't be gamed by vanity traffic"],
                    ["Goal", "Measures the real bottleneck: activation of qualified signups"]
                ],
                "options": [
                    "Total signups — bigger top of funnel fixes everything",
                    "Activated-trial-to-paid conversion rate on non-viral (intent) signups",
                    "NPS score from the existing 40 customers"
                ],
                "correct": 1,
                "explain": "The metric must track the bottleneck: what fraction of intent-driven signups who activate become paid. Signups can be gamed; this can't."
            }
        ],
        "debrief": "Venture diagnostics run on funnel math, not opinions: segment by intent, find the biggest absolute leak (activation), fix time-to-value, and measure the bottleneck metric weekly.",
        "points": 15
    },
    {
        "id": "entrepreneurship-sim-2",
        "title": "Price It or Perish",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Your first enterprise prospect asks for pricing on the call. You have no pricing page. Decide in real time.",
        "steps": [
            {
                "id": "ask",
                "text": "Discovery call, minute 35. The VP asks: 'What does this cost?' You have 40 beta users, all free. Your answer?",
                "choices": [
                    {"label": "'It's free during beta — we'll figure out pricing later.'", "feedback": "You've anchored at zero and trained the prospect that the product has no price. Every future negotiation starts from free.", "points": 1, "next": "free"},
                    {"label": "'For teams your size, customers typically invest $1,500–$2,500/month. Can I ask what budget range you're working with?'", "feedback": "You anchor with a real range and flip the question to budget. Now you're negotiating from value, not apologizing from zero.", "points": 10, "next": "negotiate"},
                    {"label": "'Let me send you our pricing deck after the call.'", "feedback": "Reasonable stall — but you've lost the live moment to read their reaction. Pricing conversations die in inboxes.", "points": 5, "next": "negotiate"}
                ]
            },
            {
                "id": "free",
                "text": "You said free. The VP's team onboards 30 users in a week and loves it. Now procurement asks for the enterprise contract. What's the damage?",
                "choices": [
                    {"label": "Quote $2,000/month — the value is proven now", "feedback": "Sticker shock: they budgeted zero. Procurement stalls for months; the champion can't defend a price that appeared from nowhere.", "points": 2, "next": "END"},
                    {"label": "Grandfather them free for 6 months, then convert — with the paid terms in writing now", "feedback": "Partial rescue: the written terms set the anchor for later. But you've still burned six months of revenue to fix a 30-second mistake.", "points": 5, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "negotiate",
                "text": "The VP says budget is 'around $1,000/month' — below your anchor. The champion loves the product. Your move?",
                "choices": [
                    {"label": "Drop to $1,000 immediately to win the logo", "feedback": "You just taught them your anchor was fiction. The next renewal starts with another discount demand.", "points": 3, "next": "END"},
                    {"label": "Hold the range but reshape scope: '$1,000 covers a 10-seat pilot; full rollout is $2,000. Let's prove it in the pilot.'", "feedback": "Scope trades for price — the anchor survives, the pilot de-risks their decision, and expansion revenue is already framed.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Never anchor at zero; anchor with a range and trade scope for price, not price for nothing. The first pricing conversation sets every negotiation that follows.",
        "points": 20
    },
    {
        "id": "entrepreneurship-sim-3",
        "title": "From Idea to First Revenue",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Order the venture-building sequence from problem discovery to first revenue — the Babson-informed path.",
        "steps": {
            "context": "You have an idea and six months of runway. Put the venture-building moves in the order that de-risks the business.",
            "items": [
                "Interview 30 potential customers about the problem (no pitch, just discovery)",
                "Sell the solution before building it — letters of intent or paid pilots",
                "Build the smallest thing that delivers the promised outcome",
                "Deliver it manually if needed; learn what actually creates value",
                "Convert the pilot to a paid contract and systematize delivery"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Discovery before building, selling before scaling, manual before automated. Each step buys information cheaply; skipping steps buys the same information at full price later.",
        "points": 10
    },
    {
        "id": "entrepreneurship-sim-4",
        "title": "Cap Table Audit",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "A founder sends you their cap table before a seed round. Find the 3 errors that will kill the round.",
        "steps": {
            "config": "# cap-table.conf — pre-seed\nfounder_common = 60%          # line 2\nadvisor_shares = 15%          # line 3\nadvisor_vesting = none        # line 4\nemployee_pool = 10%           # line 5\nuncapped_note = 500k          # line 6\nfounder_vesting = 4yr/1yr     # line 7\ndead_cofounder = 20% vested   # line 8",
            "find": 3,
            "issues": [
                {"line": 3, "description": "Advisor holds 15% — roughly 10x a sane advisor grant (0.25–1%). This alone kills most seed rounds.", "fix": "advisor_shares = 0.5%, with vesting."},
                {"line": 4, "description": "Advisor shares have NO vesting — they keep everything even if they never help again.", "fix": "advisor_vesting = 2yr, no cliff or small cliff."},
                {"line": 8, "description": "Departed cofounder fully vested at 20% — dead equity that will block every future round.", "fix": "Founder vesting (line 7) should have applied to all founders; repurchase or settle the dead equity before raising."}
            ]
        },
        "debrief": "Lines 2, 5, 6, 7 are defensible (60% founder, 10% pool, a note, founder vesting). The killers: an absurd advisor grant with no vesting, and dead cofounder equity. Investors read cap tables as character references.",
        "points": 15
    },
    {
        "id": "entrepreneurship-sim-5",
        "title": "The Investor Meeting",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "Seed pitch, partner meeting, minute 20. The partner leans in: 'Your CAC payback looks too good. Walk me through it.' The numbers are... optimistic.",
        "steps": [
            {
                "id": "question",
                "text": "Your deck shows 3-month CAC payback. The honest math — including the founder's unpaid sales time — is closer to 11 months. The partner is waiting. What do you say?",
                "choices": [
                    {"label": "Walk through the 3-month math confidently — details are for diligence", "feedback": "Diligence will find the 11 months in a week. When it does, every other number in your deck becomes suspect. Trust, once spent, doesn't refill.", "points": 0, "next": "diligence"},
                    {"label": "'The deck shows 3 months on paid channels. Fully loaded with my sales time, it's 11 — here's both, and here's the plan to get paid CAC to 5.'", "feedback": "Radical honesty about unit economics is rare and memorable. You've turned a weakness into evidence of founder discipline.", "points": 10, "next": "respect"},
                    {"label": "Deflect: 'Our focus right now is growth; we'll optimize payback at scale.'", "feedback": "Every investor has heard this deflection. It signals you either don't know your numbers or won't say them.", "points": 2, "next": "diligence"}
                ]
            },
            {
                "id": "diligence",
                "text": "Two weeks later, diligence surfaces the 11-month payback. The partner emails: 'Help us understand the discrepancy.' How do you recover?",
                "choices": [
                    {"label": "Blame the model: 'our spreadsheet had an error'", "feedback": "Nobody believes the spreadsheet did it. The round is effectively dead — and your reputation in this partnership is too.", "points": 0, "next": "END"},
                    {"label": "Own it fully: corrected model, both numbers, what you learned, no excuses", "feedback": "A full, fast correction sometimes saves the relationship even when it can't save the round. Expensive tuition.", "points": 4, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "respect",
                "text": "The partner nods: 'I appreciate the honesty. Most founders wouldn't have said that.' Then: 'Why should we believe you'll get paid CAC to 5 months?' What's the evidence?",
                "choices": [
                    {"label": "'Because we're great executors and the market is huge.'", "feedback": "Adjectives aren't evidence. You had them — don't lose them with hand-waving.", "points": 3, "next": "END"},
                    {"label": "'Two data points: our last 10 paid trials closed 40% faster after the onboarding fix, and the self-serve cohort already shows 6-month payback. Here's the cohort table.'", "feedback": "Cohort data plus a causal story (onboarding fix → faster close). That's a fundable answer — specific, checkable, and already in motion.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Fundraising is a trust market: disclose the real unit economics before diligence finds them, and answer 'why will it improve' with cohort data, not adjectives. The founders who raise are the ones investors believe about the bad numbers.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "entrepreneurship-console-1",
        "title": "Query the Customer Base",
        "console": "sql-studio",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Your CRM is a database. Build the customers table and run the queries a founder runs weekly: activation, conversion, concentration.",
        "tasks": [
            {"id": "entrepreneurship-console-1-t1", "instruction": "Create the table 'customers' with columns: id INT, email TEXT, plan TEXT, mrr INT.", "validate": {"action": "create-table", "params": {"name": "customers", "columns": "id INT, email TEXT, plan TEXT, mrr INT"}}, "hint": "Tables section: create table 'customers' with columns exactly: id INT, email TEXT, plan TEXT, mrr INT."},
            {"id": "entrepreneurship-console-1-t2", "instruction": "Create an index on customers(plan) — you segment by plan constantly.", "validate": {"action": "create-index", "params": {"table": "customers", "column": "plan"}}, "hint": "Create index form: TABLE customers, COLUMN plan."},
            {"id": "entrepreneurship-console-1-t3", "instruction": "Run: total MRR by plan — the revenue concentration query.", "validate": {"action": "run-query", "params": {"match": "SUM(mrr)"}}, "hint": "Type: SELECT plan, SUM(mrr) FROM customers GROUP BY plan; — it must contain SUM(mrr)."},
            {"id": "entrepreneurship-console-1-t4", "instruction": "Run: count of customers on the paid plan.", "validate": {"action": "run-query", "params": {"match": "WHERE plan"}}, "hint": "Type: SELECT COUNT(*) FROM customers WHERE plan = 'paid'; — it must contain WHERE plan."}
        ],
        "debrief": "Founders live in three queries: revenue by segment, conversion by cohort, concentration risk. If you can't answer those from your own data, you're flying blind."
    },
    {
        "id": "entrepreneurship-console-2",
        "title": "Review the Pitch Deck",
        "console": "git-host",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "The deck is a living document under review. Branch it, open the PR, and move the review forward.",
        "tasks": [
            {"id": "entrepreneurship-console-2-t1", "instruction": "Create a branch named 'deck/seed-round-v3'.", "validate": {"action": "create-branch", "params": {"name": "deck/seed-round-v3"}}, "hint": "Branches section: create branch 'deck/seed-round-v3'."},
            {"id": "entrepreneurship-console-2-t2", "instruction": "Open a PR titled 'Seed deck v3: honest unit economics' from head 'deck/seed-round-v3' to base 'main'.", "validate": {"action": "open-pr", "params": {"title": "Seed deck v3: honest unit economics", "base": "main", "head": "deck/seed-round-v3"}}, "hint": "Open pull request form: exact title, BASE main, HEAD deck/seed-round-v3."},
            {"id": "entrepreneurship-console-2-t3", "instruction": "Add a comment to PR #1: 'Numbers verified against cohort data.'", "validate": {"action": "add-comment", "params": {"pr": 1, "text": "Numbers verified against cohort data."}}, "hint": "Add comment form: PR NUMBER 1, COMMENT exactly 'Numbers verified against cohort data.'"}
        ],
        "debrief": "Decks deserve version control and review like code: every claim traceable, every number verified, every change discussed before it faces an investor."
    },
    {
        "id": "entrepreneurship-console-3",
        "title": "Launch the Release Pipeline",
        "console": "cicd-pipeline",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Shipping is the venture's heartbeat. Trigger the release, fix the failing stage, configure the launch, and approve the deploy.",
        "tasks": [
            {"id": "entrepreneurship-console-3-t1", "instruction": "Trigger a new build for this week's release.", "validate": {"action": "trigger-build", "params": {}}, "hint": "Click 'Trigger new build' in the Pipeline section."},
            {"id": "entrepreneurship-console-3-t2", "instruction": "The 'test' stage failed — retry it.", "validate": {"action": "retry-stage", "params": {"stage": "test"}}, "hint": "Click Retry on the test stage."},
            {"id": "entrepreneurship-console-3-t3", "instruction": "Set variable LAUNCH_COHORT to 'beta-200' — this release goes to the beta cohort.", "validate": {"action": "set-variable", "params": {"key": "LAUNCH_COHORT", "value": "beta-200"}}, "hint": "Variables section: KEY LAUNCH_COHORT, VALUE beta-200."},
            {"id": "entrepreneurship-console-3-t4", "instruction": "Approve the gated 'deploy' stage — ship it.", "validate": {"action": "approve-stage", "params": {"stage": "deploy"}}, "hint": "Click Approve on the deploy stage."}
        ],
        "debrief": "Velocity with gates: trigger often, fix fast, configure per cohort, and keep a human approval on the production release. Startups die of slowness, not of process."
    },
    {
        "id": "entrepreneurship-console-4",
        "title": "Work the Support Queue",
        "console": "ticketing",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Early-stage support IS product research. Log the ticket, assign it, and resolve it with what you learned.",
        "tasks": [
            {"id": "entrepreneurship-console-4-t1", "instruction": "Create a P2 ticket titled 'Onboarding stalls at data connection step'.", "validate": {"action": "create-ticket", "params": {"title": "Onboarding stalls at data connection step", "priority": "P2"}}, "hint": "New ticket: TITLE exactly as given, PRIORITY P2."},
            {"id": "entrepreneurship-console-4-t2", "instruction": "Assign INC-9001 to 'founder'.", "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "founder"}}, "hint": "Assign form: INC-9001 → founder."},
            {"id": "entrepreneurship-console-4-t3", "instruction": "Resolve INC-9001 with resolution 'Demo-dataset-first onboarding shipped.'", "validate": {"action": "resolve-ticket", "params": {"id": "INC-9001", "resolution": "Demo-dataset-first onboarding shipped."}}, "hint": "Resolve form (or the Resolve button won't carry your text — use the form): INC-9001 with the exact resolution."}
        ],
        "debrief": "Every support ticket is a discovery interview that filed itself. Resolve the ticket AND the underlying product gap, and record which one it was."
    }
]

MISSIONS = [
    {
        "id": "entrepreneurship-term-1",
        "title": "Survey the Workspace",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Founders orient fast. List the workspace and read the notes.",
        "objectives": ["List the workspace files", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "app.py", "hint": "Type: ls — the listing includes app.py."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "Linux essentials", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Oriented. Know your assets before you plan the quarter."
    },
    {
        "id": "entrepreneurship-term-2",
        "title": "Draft the Metrics File",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Write this month's funnel numbers to metrics.txt, then read them back.",
        "objectives": ["Create metrics.txt with funnel numbers", "Verify the file contents"],
        "checks": [
            {"command_pattern": "echo.*>\\s*metrics\\.txt", "expect_contains": "", "hint": "Type: echo \"signups 2000 activation 12pct paid 40\" > metrics.txt (no output on success)."},
            {"command_pattern": "cat\\s+metrics\\.txt", "expect_contains": "signups 2000", "hint": "Type: cat metrics.txt — your funnel numbers appear."}
        ],
        "success_message": "Metrics drafted. Write the numbers down — memory edits them in your favor."
    },
    {
        "id": "entrepreneurship-term-3",
        "title": "Measure the Funnel",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Append weekly snapshots, then measure the file: line count and paid-customer mentions.",
        "objectives": ["Append two weekly snapshots", "Count lines", "Search for paid mentions"],
        "checks": [
            {"command_pattern": "echo.*>>\\s*metrics\\.txt", "expect_contains": "", "hint": "Append: echo \"week2 paid 47\" >> metrics.txt — do it twice with different numbers."},
            {"command_pattern": "wc\\s+-l\\s+metrics\\.txt", "expect_contains": "metrics.txt", "hint": "Type: wc -l metrics.txt."},
            {"command_pattern": "grep\\s+paid\\s+metrics\\.txt", "expect_contains": "paid", "hint": "Type: grep paid metrics.txt — every paid line is listed."}
        ],
        "success_message": "Funnel measured. Trends beat snapshots — that is why the file grows weekly."
    },
    {
        "id": "entrepreneurship-term-4",
        "title": "Seal the Term Sheet",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Hash your pricing anchor so the commitment is tamper-evident.",
        "objectives": ["Hash the pricing anchor string"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "1500-2500", "hint": "Type: sha256sum pilot 1500-2500 per month — the output echoes your anchor after the real hash."}
        ],
        "success_message": "Anchor sealed. Write down the price before the negotiation, not during it."
    },
    {
        "id": "entrepreneurship-term-5",
        "title": "Provision the Environment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Initialize the venture's sandbox backend and confirm your shell identity.",
        "objectives": ["Initialize the backend", "Confirm environment identity"],
        "checks": [
            {"command_pattern": "^find(\\s|$)", "expect_contains": "successfully initialized", "hint": "Type: find — in this sandbox it initializes the backend (Terraform-style)."},
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps — prints the environment including USER=candidate."}
        ],
        "success_message": "Environment provisioned. Infrastructure before features — even in a sandbox."
    },
    {
        "id": "entrepreneurship-term-6",
        "title": "Read the Customer Logs",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Support tickets live in logs. Search the application log for errors customers hit.",
        "objectives": ["Find ERROR lines in the app log", "Read the log tail for the latest failure"],
        "checks": [
            {"command_pattern": "grep\\s+ERROR\\s+logs/app\\.log", "expect_contains": "connection refused", "hint": "Type: grep ERROR logs/app.log — the error lines appear."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "timeout", "hint": "Type: tail -n 2 logs/app.log — the latest failure is shown."}
        ],
        "success_message": "Logs read. Every error line is a customer you haven't talked to yet."
    },
    {
        "id": "entrepreneurship-term-7",
        "title": "Check Market Reachability",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Before launch day, verify DNS and connectivity to your domain.",
        "objectives": ["Resolve the launch domain", "Verify zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig launch.example.com — the ANSWER SECTION shows the address."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping launch.example.com — 0% packet loss confirms the path."}
        ],
        "success_message": "Reachability confirmed. Launch day has enough surprises without DNS being one."
    }
]
