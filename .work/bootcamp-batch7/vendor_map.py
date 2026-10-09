# Batch 7 — vendor-map: Vendor Landscape
DOMAIN = "vendor-map"

SIMS = [
    {
        "id": "vendor-map-sim-1",
        "title": "Why Did the Migration Fail?",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The 'lift and shift' to the new vendor's cloud failed at 70% with data locked in proprietary formats. Diagnose the lock-in.",
        "steps": [
            {
                "symptom": "Migration stalled at 70%. Remaining data sits in the old vendor's proprietary backup format; their export tool 'is deprecated'.",
                "evidence": [
                    ["Contract", "No data-portability clause; export API was 'best effort'"],
                    ["Format", "Backups in a proprietary format readable only by their appliance"],
                    ["Timeline", "The vendor was acquired 6 months ago; support is now a chatbot"]
                ],
                "options": [
                    "The migration team is too slow — add contractors",
                    "Lock-in by design: no portability clause, proprietary formats, and a deprecated export path mean exit was never actually possible — the failure was signed at procurement, not at migration",
                    "The new vendor's tooling is inadequate"
                ],
                "correct": 1,
                "explain": "Exit cost is set at purchase, not at exit. No portability clause + proprietary formats + deprecated exports = a roach motel. The diagnosis: procurement evaluated features and price, never the exit."
            },
            {
                "symptom": "You're stuck mid-migration with 30% of data hostage. What's the least-bad recovery?",
                "evidence": [
                    ["Leverage", "You're still paying the old vendor six figures annually"],
                    ["Options", "Pay their 'professional services' ransom / rebuild from source systems / sue"],
                    ["Constraint", "Business needs the data in 60 days"]
                ],
                "options": [
                    "Sue for the data — principle matters",
                    "Negotiate a one-time export engagement while rebuilding critical datasets from source systems in parallel — pay the ransom once, never again, and document the cost as the case study for the new procurement policy",
                    "Abandon the 30% — it was probably stale"
                ],
                "correct": 1,
                "explain": "Pragmatic exit: pay the one-time export (it's cheaper than the lawsuit and faster than rebuild alone), parallel-rebuild from sources to verify, and convert the ransom invoice into the political capital for a portability-first procurement policy."
            },
            {
                "symptom": "New procurement policy drafted. What single clause prevents the next roach motel?",
                "evidence": [
                    ["Constraint", "One contractual requirement, enforceable and testable"],
                    ["Goal", "Exit must be possible on day one, not just day 1,000"]
                ],
                "options": [
                    "A 99.99% uptime SLA",
                    "Data portability in open formats via a documented, tested export API — with a contractual exit-assistance obligation and the right to a trial export before signing",
                    "A most-favored-nation pricing clause"
                ],
                "correct": 1,
                "explain": "Test the exit before you enter: a trial export during evaluation proves portability is real, and the exit-assistance clause prices the vendor's cooperation. Uptime SLAs protect the stay; portability protects the leave."
            }
        ],
        "debrief": "Vendor failures are procurement failures: evaluate the exit with the same rigor as the features, demand open formats and tested exports, and price the ransom you never want to pay.",
        "points": 15
    },
    {
        "id": "vendor-map-sim-2",
        "title": "Build or Buy",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Your team needs a feature-flagging system. Build it in two weeks, or buy the market leader at $40k/year? Decide with TCO, not vibes.",
        "steps": [
            {
                "id": "decision",
                "text": "Feature flags needed. Build: ~2 engineer-weeks now, then maintenance forever. Buy: $40k/year, SOC 2 included, 1-day integration. Your team's roadmap is already full. Call it.",
                "choices": [
                    {"label": "Build — $40k/year is robbery for something so simple", "feedback": "Simple to build, expensive to own: percentages, targeting, audit logs, kill switches, and the on-call burden — forever. The $40k was buying you out of all of it.", "points": 3, "next": "build"},
                    {"label": "Buy — run the TCO: 2 weeks build + ~0.25 FTE maintenance forever vs. $40k/year with compliance included", "feedback": "The TCO math: 0.25 FTE at loaded cost ≈ $50k/year in maintenance alone, before the audit-log feature request arrives. Buying is cheaper AND faster.", "points": 10, "next": "buy"},
                    {"label": "Build the MVP now, evaluate buying next quarter", "feedback": "The classic hedge that becomes permanent: the MVP accrues users, migration gets scheduled 'later', and you're maintaining flags in 2029.", "points": 4, "next": "build"}
                ]
            },
            {
                "id": "build",
                "text": "You built it. Eighteen months later: the flags system needs audit logging for a compliance review, percentage rollouts are buggy, and the original author left. The 'free' system now costs real pain. What now?",
                "choices": [
                    {"label": "Assign the new hire to maintain it — that's what juniors are for", "feedback": "You've converted a $40k buy decision into a permanent junior-engineer tax plus compliance risk. The TCO keeps compounding.", "points": 1, "next": "END"},
                    {"label": "Migrate to the vendor now — the 18 months proved the maintenance cost; cut losses and buy", "feedback": "Correct late: the experiment produced data (real maintenance cost), and the data says buy. Sunk cost acknowledged, migration scheduled.", "points": 7, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "buy",
                "text": "You bought it. Year two: the vendor raises prices 40% and announces the 'enterprise tier' your features now require. The lock-in you accepted has teeth. Response?",
                "choices": [
                    {"label": "Pay it — switching costs more than the increase", "feedback": "You've now ratified the price hike as strategy. Next year's increase is already being planned.", "points": 3, "next": "END"},
                    {"label": "Invoke the contract's price-cap clause you negotiated at purchase, and start the 90-day exit evaluation the contract also guarantees", "feedback": "This is why the purchase included caps and exit rights: the cap holds this year, the credible exit threat disciplines next year's negotiation. Procurement done right.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Build vs. buy is TCO vs. TCO: loaded maintenance cost forever versus subscription plus exit rights. And every purchase negotiates the divorce (caps, portability, exit assistance) before the wedding.",
        "points": 20
    },
    {
        "id": "vendor-map-sim-3",
        "title": "Run the Evaluation",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Order the vendor evaluation process from problem definition to signed contract.",
        "steps": {
            "context": "You need a new monitoring vendor. Order the evaluation steps.",
            "items": [
                "Define the problem and success criteria in vendor-neutral terms",
                "Shortlist 3 vendors; run the same weighted scorecard on each",
                "Trial the top two with real workloads — including a trial data export",
                "Check references: ask their customers about the exit, not just the onboarding",
                "Negotiate price caps, portability, and exit assistance — then sign"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Neutral criteria first, scorecards second, trials with exit tests third, references about exits fourth, and the divorce negotiated fifth. Most teams start at step 2 and skip steps 3–5 — that's where the lock-in lives.",
        "points": 10
    },
    {
        "id": "vendor-map-sim-4",
        "title": "Audit the Contract",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "A SaaS renewal contract has 3 traps. Find them before legal signs.",
        "steps": {
            "config": "# renewal.conf — SaaS year 3\nauto_renew = true, 3yr          # line 2\nprice_cap = none               # line 3\nuplift = 15%/yr               # line 4\ndata_export = 'on request'      # line 5\nexport_format = proprietary     # line 6\nsla_credits = capped 10%        # line 7\ntermination = 90d notice        # line 8",
            "find": 3,
            "issues": [
                {"line": 2, "description": "Auto-renew locks 3 years with no action — the renewal happens by inertia, exactly as designed.", "fix": "auto_renew = false; renewals require explicit approval with a market check."},
                {"line": 3, "description": "No price cap combined with 15%/yr uplift (line 4) — year-3 pricing is whatever they want.", "fix": "price_cap = CPI+2% or 5%, whichever is lower."},
                {"line": 6, "description": "Export in proprietary format makes the 'on request' export (line 5) useless — you can leave with data you can't use.", "fix": "export_format = open formats (CSV/Parquet/JSON) via documented API."}
            ]
        },
        "debrief": "Lines 5, 7, 8 are workable (export on request, capped credits, 90-day notice). The traps: inertia auto-renewal, uncapped compounding uplift, and a proprietary-format export. Contracts are code for money — review them like code.",
        "points": 15
    },
    {
        "id": "vendor-map-sim-5",
        "title": "The Renewal Negotiation",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "Your EDR vendor wants +35% at renewal. You have 60 days, a credible alternative, and a tired team. Negotiate.",
        "steps": [
            {
                "id": "renewal",
                "text": "EDR renewal: +35%, 60 days to decide, team dreads a rip-and-replace. The vendor's rep says 'everyone's seeing adjustments.' Your opening?",
                "choices": [
                    {"label": "'We'll pay it — migration is too disruptive right now.'", "feedback": "You've negotiated against yourself. The rep just learned your threat point is zero.", "points": 1, "next": "cave"},
                    {"label": "'We've completed a trial export and a POC with your competitor. Here's our walk-away number — 5% over last year, 2-year term, price cap included.'", "feedback": "The holy trinity: demonstrated exit (trial export), named alternative (POC done), specific terms. Now it's a negotiation.", "points": 10, "next": "leverage"},
                    {"label": "Go silent for 45 days to 'create pressure'", "feedback": "Silence without a deadline is just delay. The rep waits; your 60 days shrink to 15 and the leverage inverts.", "points": 3, "next": "cave"}
                ]
            },
            {
                "id": "cave",
                "text": "You signaled you'll pay. The rep returns with '+30% — I fought for you.' Fifteen days left. Any recovery?",
                "choices": [
                    {"label": "Accept the 30% — it's better than 35%", "feedback": "Anchoring worked exactly as designed: 35→30 feels like a win while you pay 30% more for the same product.", "points": 1, "next": "END"},
                    {"label": "Restart properly: brief procurement, run the competitive POC in the remaining 15 days, come back with the walk-away", "feedback": "Late but real: even a compressed POC restores some leverage. Painful lesson in opening discipline.", "points": 5, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "leverage",
                "text": "The rep counters: '+12%, and we'll throw in the new module free.' Your walk-away was +5% with a cap. The team is tired. Close it how?",
                "choices": [
                    {"label": "Take the 12% — the free module softens it and the team needs rest", "feedback": "The 'free' module is shelfware with renewal implications. You traded 7 points for tiredness.", "points": 4, "next": "END"},
                    {"label": "'8%, 2-year, cap at 5%/yr, and the module in writing with no auto-upgrade — or we sign the competitor Friday.'", "feedback": "Specific, final, and credible — the Friday deadline is real because the POC is done. That's how renewals close at fair prices.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Renewal leverage is manufactured before the negotiation: trial exports, completed POCs, walk-away numbers, and real deadlines. The rep's 'adjustments' meet your arithmetic — and arithmetic wins.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "vendor-map-console-1",
        "title": "Compare Architectures",
        "console": "aws-vpc",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Two vendors, two reference architectures. Build the neutral comparison network: VPC, subnets, security groups.",
        "tasks": [
            {"id": "vendor-map-console-1-t1", "instruction": "Create a VPC named 'eval-vpc' with CIDR 10.30.0.0/16.", "validate": {"action": "create-vpc", "params": {"name": "eval-vpc", "cidr": "10.30.0.0/16"}}, "hint": "VPCs: NAME eval-vpc, CIDR 10.30.0.0/16."},
            {"id": "vendor-map-console-1-t2", "instruction": "Create a subnet in 'eval-vpc' with CIDR 10.30.1.0/24 in AZ us-east-1a.", "validate": {"action": "create-subnet", "params": {"vpc": "eval-vpc", "cidr": "10.30.1.0/24", "az": "us-east-1a"}}, "hint": "Subnets: VPC NAME eval-vpc, CIDR 10.30.1.0/24, AZ us-east-1a."},
            {"id": "vendor-map-console-1-t3", "instruction": "Create a security group named 'eval-sg' on 'eval-vpc'.", "validate": {"action": "create-sg", "params": {"vpc": "eval-vpc", "name": "eval-sg"}}, "hint": "Security Groups: VPC NAME eval-vpc, GROUP NAME eval-sg."},
            {"id": "vendor-map-console-1-t4", "instruction": "Add an inbound rule to 'eval-sg': tcp port 443 from 10.30.0.0/16.", "validate": {"action": "add-sg-rule", "params": {"sg": "eval-sg", "protocol": "tcp", "port": 443, "cidr": "10.30.0.0/16"}}, "hint": "Add rule: SG eval-sg, PROTOCOL tcp, PORT 443, CIDR 10.30.0.0/16."}
        ],
        "debrief": "Evaluate vendors on neutral ground: identical reference architectures, identical rules, scorecards not slideware. The network you build for the POC is the network the decision deserves."
    },
    {
        "id": "vendor-map-console-2",
        "title": "Score the Vendors",
        "console": "sql-studio",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Scorecards live in a database. Build the vendors table and query the weighted results.",
        "tasks": [
            {"id": "vendor-map-console-2-t1", "instruction": "Create the table 'vendors' with columns: id INT, name TEXT, score INT, exit_rating INT.", "validate": {"action": "create-table", "params": {"name": "vendors", "columns": "id INT, name TEXT, score INT, exit_rating INT"}}, "hint": "Tables: create 'vendors' with columns exactly: id INT, name TEXT, score INT, exit_rating INT."},
            {"id": "vendor-map-console-2-t2", "instruction": "Create an index on vendors(score).", "validate": {"action": "create-index", "params": {"table": "vendors", "column": "score"}}, "hint": "Create index: TABLE vendors, COLUMN score."},
            {"id": "vendor-map-console-2-t3", "instruction": "Run a query selecting vendors ordered by score descending.", "validate": {"action": "run-query", "params": {"match": "ORDER BY score"}}, "hint": "Type: SELECT * FROM vendors ORDER BY score DESC; — must contain 'ORDER BY score'."},
            {"id": "vendor-map-console-2-t4", "instruction": "Run a query selecting vendors with exit_rating above 7 — portability matters.", "validate": {"action": "run-query", "params": {"match": "exit_rating > 7"}}, "hint": "Type: SELECT * FROM vendors WHERE exit_rating > 7; — must contain 'exit_rating > 7'."}
        ],
        "debrief": "The scorecard is a database: every vendor scored on the same criteria, exit rating as a first-class column, queries instead of opinions. Decisions you can re-run are decisions you can defend."
    },
    {
        "id": "vendor-map-console-3",
        "title": "Work the Vendor Tickets",
        "console": "ticketing",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Vendor support runs through your queue, not their portal. Log it, assign it, track it.",
        "tasks": [
            {"id": "vendor-map-console-3-t1", "instruction": "Create a P2 ticket titled 'Vendor export API returning proprietary format'.", "validate": {"action": "create-ticket", "params": {"title": "Vendor export API returning proprietary format", "priority": "P2"}}, "hint": "New ticket: TITLE exactly as given, PRIORITY P2."},
            {"id": "vendor-map-console-3-t2", "instruction": "Assign INC-9001 to 'vendor-mgr'.", "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "vendor-mgr"}}, "hint": "Assign: INC-9001 → vendor-mgr."},
            {"id": "vendor-map-console-3-t3", "instruction": "Add a note to INC-9001: 'Escalated to vendor TAM; SLA clock running.'", "validate": {"action": "add-note", "params": {"id": "INC-9001", "text": "Escalated to vendor TAM; SLA clock running."}}, "hint": "Add note: INC-9001 with the exact text."}
        ],
        "debrief": "Vendor issues in your ticketing system means your SLA clock, your escalation path, your evidence trail. The portal is theirs; the record is yours."
    },
    {
        "id": "vendor-map-console-4",
        "title": "Lock Down Vendor Egress",
        "console": "firewall",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The new vendor's agent phones home. Control exactly what it may reach with host firewall rules.",
        "tasks": [
            {"id": "vendor-map-console-4-t1", "instruction": "Add a rule: OUTPUT chain, tcp port 443, source 10.30.0.0/16, action ACCEPT — the agent may use HTTPS.", "validate": {"action": "add-rule", "params": {"chain": "OUTPUT", "protocol": "tcp", "port": 443, "source": "10.30.0.0/16", "action": "ACCEPT"}}, "hint": "Rules section: CHAIN OUTPUT, PROTOCOL tcp, PORT 443, SOURCE 10.30.0.0/16, ACTION ACCEPT."},
            {"id": "vendor-map-console-4-t2", "instruction": "Add a rule: OUTPUT chain, tcp port 22, source 0.0.0.0/0, action DROP — the agent may not SSH anywhere.", "validate": {"action": "add-rule", "params": {"chain": "OUTPUT", "protocol": "tcp", "port": 22, "source": "0.0.0.0/0", "action": "DROP"}}, "hint": "Add rule: CHAIN OUTPUT, PROTOCOL tcp, PORT 22, SOURCE 0.0.0.0/0, ACTION DROP."},
            {"id": "vendor-map-console-4-t3", "instruction": "Set the default policy of the OUTPUT chain to DROP — deny by default, allow by exception.", "validate": {"action": "set-default-policy", "params": {"chain": "OUTPUT", "policy": "DROP"}}, "hint": "Default policies section: CHAIN OUTPUT, POLICY DROP."}
        ],
        "debrief": "Vendor agents get the same treatment as any third party: explicit allows, explicit denies, default-deny underneath. Trust is a firewall rule, not a feeling."
    }
]

MISSIONS = [
    {
        "id": "vendor-map-term-1",
        "title": "Survey the Market",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Orient: list the workspace and read the notes.",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "README.md", "hint": "Type: ls."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "Linux essentials", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Market surveyed. Define the problem before shopping for solutions."
    },
    {
        "id": "vendor-map-term-2",
        "title": "Draft the Scorecard",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Write the evaluation criteria to scorecard.txt.",
        "objectives": ["Write the criteria", "Append the exit criterion", "Read the scorecard"],
        "checks": [
            {"command_pattern": "echo.*>\\s*scorecard\\.txt", "expect_contains": "", "hint": "Type: echo \"criteria: features price support\" > scorecard.txt (no output on success)."},
            {"command_pattern": "echo.*>>\\s*scorecard\\.txt", "expect_contains": "", "hint": "Type: echo \"criteria: exit-portability\" >> scorecard.txt."},
            {"command_pattern": "cat\\s+scorecard\\.txt", "expect_contains": "exit-portability", "hint": "Type: cat scorecard.txt."}
        ],
        "success_message": "Scorecard drafted. What gets scored gets compared fairly."
    },
    {
        "id": "vendor-map-term-3",
        "title": "Weigh the Criteria",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Count criteria lines and search for the exit requirement.",
        "objectives": ["Count lines", "Find the exit criterion"],
        "checks": [
            {"command_pattern": "wc\\s+-l\\s+scorecard\\.txt", "expect_contains": "scorecard.txt", "hint": "Type: wc -l scorecard.txt."},
            {"command_pattern": "grep\\s+exit\\s+scorecard\\.txt", "expect_contains": "exit-portability", "hint": "Type: grep exit scorecard.txt."}
        ],
        "success_message": "Criteria weighed. The exit is a criterion, not an afterthought."
    },
    {
        "id": "vendor-map-term-4",
        "title": "Seal the Walk-Away",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Hash your walk-away price before the negotiation — commitment, tamper-evident.",
        "objectives": ["Hash the walk-away string"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "walkaway", "hint": "Type: sha256sum walkaway plus-5pct 2yr cap — the real hash plus your number are echoed."}
        ],
        "success_message": "Walk-away sealed. Decide the number before the room decides it for you."
    },
    {
        "id": "vendor-map-term-5",
        "title": "Test the Export",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Trial exports prove portability. Inspect the sample log's edges for export-relevant errors.",
        "objectives": ["Read the first lines", "Read the last lines", "Find errors"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "server starting", "hint": "Type: head -n 2 logs/app.log."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "timeout", "hint": "Type: tail -n 2 logs/app.log."},
            {"command_pattern": "grep\\s+ERROR\\s+logs/app\\.log", "expect_contains": "ERROR", "hint": "Type: grep ERROR logs/app.log."}
        ],
        "success_message": "Export path inspected. Test the exit before you enter."
    },
    {
        "id": "vendor-map-term-6",
        "title": "Verify the Environment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Confirm identity and home directory.",
        "objectives": ["Print the environment", "Expand HOME"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps."},
            {"command_pattern": "echo\\s+\\$HOME", "expect_contains": "/home/candidate", "hint": "Type: echo $HOME."}
        ],
        "success_message": "Environment verified. Evaluate from solid ground."
    },
    {
        "id": "vendor-map-term-7",
        "title": "Reach the Vendor",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Verify the vendor's status page resolves and responds.",
        "objectives": ["Resolve the status domain", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig status.example-vendor.com."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping status.example-vendor.com."}
        ],
        "success_message": "Vendor reachable. Verify the status page before you need it."
    }
]
