# Batch 7 — frontier-path: The Frontier Path
DOMAIN = "frontier-path"

SIMS = [
    {
        "id": "frontier-path-sim-1",
        "title": "The Wedged Pipeline",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A hybrid system — symbolic reasoner feeding a neural ranker — has silently degraded. Diagnose across the boundary.",
        "steps": [
            {
                "symptom": "End-to-end accuracy fell from 91% to 74% over two weeks. Neither component's unit tests fail.",
                "evidence": [
                    ["Symbolic reasoner", "Output schema unchanged, latency normal"],
                    ["Neural ranker", "Input distribution drift: 18% of fields now arrive null"],
                    ["Contract", "No schema validation between the two components"]
                ],
                "options": [
                    "Retrain the ranker — the model is obviously stale",
                    "The interface failed, not either component: the reasoner started emitting nulls the ranker never saw in training, and nothing validates the handoff",
                    "Add more training data to the ranker"
                ],
                "correct": 1,
                "explain": "Frontier systems fail at boundaries. Each side passes its own tests; the contract between them was never specified or validated. Fix the interface (schema + validation), then decide if retraining is needed."
            },
            {
                "symptom": "You add contract validation. Accuracy recovers to 89% but 6% of requests now hard-fail.",
                "evidence": [
                    ["Failures", "All from the reasoner emitting a new field the contract rejects"],
                    ["Source", "A knowledge-base update added the field last Tuesday"],
                    ["Blast radius", "Failures cluster in one customer segment"]
                ],
                "options": [
                    "Roll back the knowledge-base update",
                    "Version the contract: accept the new field, validate its shape, and let the ranker declare which contract version it was trained against",
                    "Disable validation — 89% with failures is worse than 74% silent"
                ],
                "correct": 1,
                "explain": "Interfaces evolve; version them. The contract becomes a declared, tested artifact with versions, and each consumer pins the version it understands. Silent degradation becomes explicit negotiation."
            },
            {
                "symptom": "Fixed and versioned. What permanent practice prevents the next cross-boundary silent failure?",
                "evidence": [
                    ["Constraint", "Must catch interface drift before it reaches production"],
                    ["Goal", "Neither team can break the other silently again"]
                ],
                "options": [
                    "Merge both teams into one so there's no boundary",
                    "Contract tests in CI on both sides plus production monitoring on the interface's input distribution",
                    "Weekly meetings between the teams"
                ],
                "correct": 1,
                "explain": "Consumer-driven contract tests in CI catch drift at build time; distribution monitoring catches it at runtime. The boundary is permanent — make it explicit and guarded instead of pretending it away."
            }
        ],
        "debrief": "Synthesis systems are boundary systems: computability meets control theory at an interface, and interfaces need contracts, versions, tests, and monitoring. Debug the boundary first.",
        "points": 15
    },
    {
        "id": "frontier-path-sim-2",
        "title": "Choose the Research Bet",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "You have one year and a small team. Three frontier directions compete. Place the bet like a researcher, not a gambler.",
        "steps": [
            {
                "id": "bet",
                "text": "Three proposals: (A) neuro-symbolic theorem proving, (B) LLM agents for infrastructure automation, (C) formal verification of smart contracts. Your team: two strong engineers, one mathematician. Which do you fund?",
                "choices": [
                    {"label": "B — agents are hot, hiring and hype follow heat", "feedback": "Heat is not edge. Your team has no infra-ops depth, and the space is crowded with better-funded labs. You'd be the tenth team doing the obvious thing.", "points": 2, "next": "crowded"},
                    {"label": "A — it matches the team's rare combination (math + engineering) and few teams sit at that intersection", "feedback": "Edge comes from the intersection: the mathematician formalizes, the engineers build, and almost nobody else has both in one small team. Asymmetric bet.", "points": 10, "next": "edge"},
                    {"label": "C — smart contracts are lucrative and verification is rigorous", "feedback": "Respectable, but your team's mathematician does analysis, not formal methods — a six-month ramp before real output. The edge is thinner than it looks.", "points": 5, "next": "ramp"}
                ]
            },
            {
                "id": "crowded",
                "text": "Six months in: a frontier lab ships an open agent framework that does 80% of your roadmap. Your runway is half gone. Pivot or persist?",
                "choices": [
                    {"label": "Persist — our implementation will be better", "feedback": "'Better' against a frontier lab's distribution is not a strategy. The remaining runway buys a graceful pivot, not a heroic last stand.", "points": 1, "next": "END"},
                    {"label": "Pivot to the evaluation layer: everyone needs to measure these agents, nobody does it well", "feedback": "The heat created a new adjacent gap — measurement. Your engineering strength transfers; the crowded lane is abandoned for the empty one next to it.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "ramp",
                "text": "The mathematician is ramping on formal methods but progress is slow. A DeFi protocol offers a paid audit that would fund 4 more months. Take it?",
                "choices": [
                    {"label": "Take it — runway is runway", "feedback": "The audit consumes the mathematician for two months and teaches the team nothing about the research bet. You've traded the mission for money.", "points": 2, "next": "END"},
                    {"label": "Decline — protect the research calendar; the bet was the bet", "feedback": "Discipline: the audit pays cash but costs the compounding that was the whole point. Saying no to revenue is the researcher's hardest skill.", "points": 7, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "edge",
                "text": "Month eight: the neuro-symbolic prover beats the baseline on 60% of benchmarks but fails weirdly on the rest — the neural guesser and symbolic checker disagree in ways nobody predicted. What's the move?",
                "choices": [
                    {"label": "Tune the neural guesser harder — the failures are noise", "feedback": "The disagreements aren't noise; they're the discovery. Tuning past them buries the actual finding.", "points": 3, "next": "END"},
                    {"label": "Study the disagreements as the research object — characterize exactly when symbolic checking rejects neural guesses", "feedback": "That's the contribution: a taxonomy of neuro-symbolic disagreement modes. The failure analysis IS the paper. Frontier work is found at the boundary, again.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Research bets are placed on team-shape fit and empty intersections, not heat. And the finding is usually hiding in the disagreement between your components — study the boundary.",
        "points": 20
    },
    {
        "id": "frontier-path-sim-3",
        "title": "Assemble the Frontier Stack",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Order the build sequence for a frontier synthesis system — from foundations to the question-keeping layer.",
        "steps": {
            "context": "You're building a system where computability theory, control theory, and AI engineering meet. Order the layers bottom-up.",
            "items": [
                "Formalize the problem: what is computable here, and what are the control objectives",
                "Build the symbolic core: the rules, invariants, and verifiable kernel",
                "Add the learning layer: models that guess, constrained by the symbolic core",
                "Instrument the boundaries: contracts, monitoring, and disagreement logging",
                "Add the philosophy layer: the open questions the system must keep asking, not answer"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Formalize first (know what's computable), symbolize second (the verifiable kernel), learn third (guesses inside constraints), instrument fourth (boundaries are where truth lives), and keep the philosophical questions open last — they steer the next iteration.",
        "points": 10
    },
    {
        "id": "frontier-path-sim-4",
        "title": "Audit the Agent Config",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "An AI agent's production config is one incident away from autonomy it shouldn't have. Find the 3 dangerous settings.",
        "steps": {
            "config": "# agent.conf — production\nmax_tool_calls = 50            # line 2\nhuman_approval = none          # line 3\nallowed_tools = read-only      # line 4\nmemory_retention = 90d        # line 5\nprompt_source = user_input     # line 6\nrate_limit = 100/min          # line 7\naction_scope = production-db   # line 8",
            "find": 3,
            "issues": [
                {"line": 3, "description": "No human approval required — the agent can act autonomously in production with 50 tool calls.", "fix": "human_approval = required for all write/destructive actions."},
                {"line": 6, "description": "Prompt sourced directly from user input with no sanitization — prompt injection goes straight to the agent.", "fix": "prompt_source = sanitized template; treat user input as data, never as instructions."},
                {"line": 8, "description": "Action scope includes the production database paired with no approval — the blast radius is the crown jewels.", "fix": "action_scope = staging; production requires approval + break-glass procedure."}
            ]
        },
        "debrief": "Lines 2, 4, 5, 7 are bounded and defensible. The lethal combination is autonomy (line 3) + unsanitized input (line 6) + production scope (line 8). Frontier engineering is largely the discipline of refusing dangerous defaults.",
        "points": 15
    },
    {
        "id": "frontier-path-sim-5",
        "title": "The Dual-Use Review",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "Your persuasion-detection research could defend elections — or optimize manipulation. The review board is waiting.",
        "steps": [
            {
                "id": "review",
                "text": "Your paper: a model that predicts which messages persuade which demographics. Defensive use: inoculation campaigns. Offensive use: micro-targeted manipulation. A defense contractor wants to license it. Your call?",
                "choices": [
                    {"label": "License it — research wants to be used, and the funding is real", "feedback": "The capability diffuses to whoever pays most. You've built the targeting engine for the next influence operation and called it research.", "points": 1, "next": "diffuse"},
                    {"label": "Publish the defense half openly; withhold the targeting optimization", "feedback": "Differential publication: the inoculation methods go public, the persuasion optimizer stays in the lab notebook. Defense diffuses faster than offense.", "points": 10, "next": "differential"},
                    {"label": "Bury the whole project — too dangerous to exist", "feedback": "Someone else will build it within two years, and without your defensive insights. Burial doesn't prevent the capability; it only prevents the defense.", "points": 4, "next": "buried"}
                ]
            },
            {
                "id": "diffuse",
                "text": "A year later, your licensee's tooling appears in a documented election-interference campaign. Journalists call you for comment. What do you say?",
                "choices": [
                    {"label": "'We couldn't have known.'", "feedback": "You could have — the dual use was obvious at the review. The honest statement is harder and the only one available.", "points": 0, "next": "END"},
                    {"label": "'We licensed it; the misuse is real; here's the defensive toolkit we should have led with.'", "feedback": "Accountability plus the defense you should have published first. Late, but it's the only move that helps anyone now.", "points": 5, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "buried",
                "text": "Two years later a lab publishes exactly your targeting result — without any defensive counterpart. Your buried notebook could have inoculated the public. Regrets?",
                "choices": [
                    {"label": "Publish the defensive work now, with the full story of why it was buried", "feedback": "Late defense beats no defense, and the story teaches the field that burial is not a safety strategy.", "points": 7, "next": "END"},
                    {"label": "Stay buried — reopening it only draws attention", "feedback": "The capability exists in the world without your counterweight. Silence is now complicity with the gap you left.", "points": 2, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "differential",
                "text": "The defensive paper is cited by election-integrity teams in three countries. A journalist asks: 'Did you hold back the offensive half?' How do you answer?",
                "choices": [
                    {"label": "Deny it — admit nothing about the withheld work", "feedback": "The lab notebook exists; denial has a half-life. When it surfaces, the defensive work gets tainted by the lie.", "points": 3, "next": "END"},
                    {"label": "'Yes — we published the defense and kept the targeting method restricted, and here's the review-board reasoning.'", "feedback": "Transparent differential publication: the reasoning is public, the defense is public, the weapon isn't. That's the frontier ethos stated plainly.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Frontier capability is dual-use by default. The ethos: publish the defense, restrict the offense, document the reasoning, and never pretend burial is safety. Philosophy keeps the questions honest — including this one.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "frontier-path-console-1",
        "title": "Stand Up the Research Cluster",
        "console": "k8s-dashboard",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The synthesis lab needs an isolated namespace, the prover deployment, and an internal service. Build it.",
        "tasks": [
            {"id": "frontier-path-console-1-t1", "instruction": "Create the namespace 'frontier-lab'.", "validate": {"action": "create-namespace", "params": {"name": "frontier-lab"}}, "hint": "Namespaces section: create namespace 'frontier-lab'."},
            {"id": "frontier-path-console-1-t2", "instruction": "Deploy 'prover' in namespace 'frontier-lab' with image 'prover:0.9' and 2 replicas.", "validate": {"action": "deploy", "params": {"name": "prover", "namespace": "frontier-lab", "image": "prover:0.9", "replicas": 2}}, "hint": "Deployments section: DEPLOYMENT NAME prover, NAMESPACE frontier-lab, IMAGE prover:0.9, REPLICAS 2."},
            {"id": "frontier-path-console-1-t3", "instruction": "Expose the 'prover' deployment on port 8080 as type ClusterIP (internal only — the prover is not public).", "validate": {"action": "expose-service", "params": {"deployment": "prover", "port": 8080, "type": "ClusterIP"}}, "hint": "Services section: DEPLOYMENT prover, PORT 8080, TYPE ClusterIP."},
            {"id": "frontier-path-console-1-t4", "instruction": "Create a ConfigMap named 'prover-config' in namespace 'frontier-lab' for the contract versions.", "validate": {"action": "create-configmap", "params": {"name": "prover-config", "namespace": "frontier-lab"}}, "hint": "ConfigMaps section: NAME prover-config, NAMESPACE frontier-lab."}
        ],
        "debrief": "Frontier systems get the same discipline as production: isolated namespaces, pinned images, internal-by-default networking, and configuration as a versioned artifact."
    },
    {
        "id": "frontier-path-console-2",
        "title": "Isolate the Lab Network",
        "console": "aws-vpc",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The lab's experiment network must be isolated from everything else. Build the VPC, subnets, and security groups.",
        "tasks": [
            {"id": "frontier-path-console-2-t1", "instruction": "Create a VPC named 'frontier-vpc' with CIDR 10.20.0.0/16.", "validate": {"action": "create-vpc", "params": {"name": "frontier-vpc", "cidr": "10.20.0.0/16"}}, "hint": "VPCs section: NAME frontier-vpc, CIDR 10.20.0.0/16."},
            {"id": "frontier-path-console-2-t2", "instruction": "Create a subnet in 'frontier-vpc' with CIDR 10.20.1.0/24 in AZ us-east-1a.", "validate": {"action": "create-subnet", "params": {"vpc": "frontier-vpc", "cidr": "10.20.1.0/24", "az": "us-east-1a"}}, "hint": "Subnets section: VPC NAME frontier-vpc, CIDR 10.20.1.0/24, AZ us-east-1a."},
            {"id": "frontier-path-console-2-t3", "instruction": "Create a security group named 'prover-sg' on 'frontier-vpc'.", "validate": {"action": "create-sg", "params": {"vpc": "frontier-vpc", "name": "prover-sg"}}, "hint": "Security Groups section: VPC NAME frontier-vpc, GROUP NAME prover-sg."},
            {"id": "frontier-path-console-2-t4", "instruction": "Add an inbound rule to 'prover-sg': tcp port 8080 from 10.20.0.0/16 (lab-internal only).", "validate": {"action": "add-sg-rule", "params": {"sg": "prover-sg", "protocol": "tcp", "port": 8080, "cidr": "10.20.0.0/16"}}, "hint": "Add inbound rule form: SG prover-sg (name works), PROTOCOL tcp, PORT 8080, SOURCE CIDR 10.20.0.0/16."}
        ],
        "debrief": "Isolation is architecture: dedicated VPC, declared subnets, and security groups that default to lab-internal. The experiment network touches the outside world through exactly the doors you name."
    },
    {
        "id": "frontier-path-console-3",
        "title": "Debug the Boundary Contract",
        "console": "code-editor",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The handoff script between the symbolic core and the learning layer has a bug. Inspect, breakpoint, and fix it.",
        "tasks": [
            {"id": "frontier-path-console-3-t1", "instruction": "Open the file 'app.py' in the editor.", "validate": {"action": "open-file", "params": {"name": "app.py"}}, "hint": "Explorer section: click Open on app.py."},
            {"id": "frontier-path-console-3-t2", "instruction": "Set a breakpoint at app.py line 4 (the accumulation line — where the boundary value builds).", "validate": {"action": "toggle-breakpoint", "params": {"file": "app.py", "line": 4}}, "hint": "Editor section: click line 4 of app.py to toggle the breakpoint."},
            {"id": "frontier-path-console-3-t3", "instruction": "Inspect the variable 's' to see the accumulator's simulated value.", "validate": {"action": "inspect-variable", "params": {"name": "s"}}, "hint": "Use the Inspect form with VARIABLE NAME s."}
        ],
        "debrief": "Cross-boundary bugs are found the same way as any other: open the code, breakpoint the handoff, inspect the actual values. The boundary is just another line of code — until you skip it."
    },
    {
        "id": "frontier-path-console-4",
        "title": "Watch the Disagreement Feed",
        "console": "siem-dashboard",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "The monitor flags component disagreements like security alerts. Triage the queue.",
        "tasks": [
            {"id": "frontier-path-console-4-t1", "instruction": "Acknowledge alert ALT-101.", "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-101"}}, "hint": "Click Ack on ALT-101 in the Alerts section."},
            {"id": "frontier-path-console-4-t2", "instruction": "Assign ALT-102 to analyst 'chen'.", "validate": {"action": "assign-alert", "params": {"id": "ALT-102", "analyst": "chen"}}, "hint": "Assign alert form: ALT-102 → chen."},
            {"id": "frontier-path-console-4-t3", "instruction": "Create a detection rule named 'neuro-symbolic-disagreement' with your own query text.", "validate": {"action": "create-rule", "params": {"name": "neuro-symbolic-disagreement"}}, "hint": "Detection rules section: create rule 'neuro-symbolic-disagreement'."}
        ],
        "debrief": "Disagreements between components are the research signal — treat them like detections: acknowledge, assign, and encode the pattern as a rule so the next one is caught automatically."
    }
]

MISSIONS = [
    {
        "id": "frontier-path-term-1",
        "title": "Survey the Lab",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Orient in the lab workspace: list files and read the notes.",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "logs/", "hint": "Type: ls — the listing includes the logs/ directory."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "chmod", "hint": "Type: cat notes.txt — the notes mention chmod."}
        ],
        "success_message": "Lab surveyed. Every frontier starts with knowing the terrain."
    },
    {
        "id": "frontier-path-term-2",
        "title": "Log the Interface Contract",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Write the v1 interface contract between the symbolic core and the learning layer to contract.txt.",
        "objectives": ["Write the contract file", "Read it back to verify"],
        "checks": [
            {"command_pattern": "echo.*>\\s*contract\\.txt", "expect_contains": "", "hint": "Type: echo \"contract v1: fields name,score,provenance\" > contract.txt (no output on success)."},
            {"command_pattern": "cat\\s+contract\\.txt", "expect_contains": "contract v1", "hint": "Type: cat contract.txt — the contract text appears."}
        ],
        "success_message": "Contract logged. Boundaries that aren't written down aren't boundaries."
    },
    {
        "id": "frontier-path-term-3",
        "title": "Version the Contract",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Append a v2 contract line, then measure and search the contract file.",
        "objectives": ["Append the v2 line", "Count contract lines", "Find version markers"],
        "checks": [
            {"command_pattern": "echo.*>>\\s*contract\\.txt", "expect_contains": "", "hint": "Type: echo \"contract v2: adds confidence field\" >> contract.txt."},
            {"command_pattern": "wc\\s+-l\\s+contract\\.txt", "expect_contains": "contract.txt", "hint": "Type: wc -l contract.txt."},
            {"command_pattern": "grep\\s+v2\\s+contract\\.txt", "expect_contains": "v2", "hint": "Type: grep v2 contract.txt — the version line is shown."}
        ],
        "success_message": "Contract versioned. Interfaces evolve — versioning is how evolution stays safe."
    },
    {
        "id": "frontier-path-term-4",
        "title": "Seal the Experiment",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Hash the experiment ID so results are tamper-evident.",
        "objectives": ["Hash the experiment identifier"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "exp-042", "hint": "Type: sha256sum exp-042 neuro-symbolic run — the real hash plus your ID are echoed."}
        ],
        "success_message": "Experiment sealed. Reproducibility starts with knowing exactly what ran."
    },
    {
        "id": "frontier-path-term-5",
        "title": "Initialize the Backend",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Provision the lab backend and verify your environment.",
        "objectives": ["Initialize the backend", "Print the environment"],
        "checks": [
            {"command_pattern": "^find(\\s|$)", "expect_contains": "successfully initialized", "hint": "Type: find — initializes the backend in this sandbox."},
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "PWD=/home/candidate", "hint": "Type: ps — prints the environment including PWD."}
        ],
        "success_message": "Backend ready. Frontier work still starts with working infrastructure."
    },
    {
        "id": "frontier-path-term-6",
        "title": "Inspect the Log Boundaries",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "System logs show boundary behavior. Read the head and tail of the app log.",
        "objectives": ["Read the first lines", "Read the last lines"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "INFO", "hint": "Type: head -n 3 logs/app.log — the opening INFO lines appear."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "ERROR", "hint": "Type: tail -n 3 logs/app.log — the closing ERROR lines appear."}
        ],
        "success_message": "Boundaries inspected. The interesting behavior is always at the edges."
    },
    {
        "id": "frontier-path-term-7",
        "title": "Verify the Uplink",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Confirm the lab can reach the outside world: DNS and packet loss check.",
        "objectives": ["Resolve a hostname", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig lab.example.org — the ANSWER SECTION appears."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping lab.example.org — 0% packet loss."}
        ],
        "success_message": "Uplink verified. Even frontier labs need working DNS."
    }
]
