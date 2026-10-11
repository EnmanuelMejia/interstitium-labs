# Batch 7 — roles-library: IT Roles Library
DOMAIN = "roles-library"

SIMS = [
    {
        "id": "roles-library-sim-1",
        "title": "Who Owns This Outage?",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The VPN is down for 200 users. Three teams are pointing at each other. Diagnose the ownership failure.",
        "steps": [
            {
                "symptom": "VPN down 90 minutes. Network team: 'The servers are fine.' Systems team: 'The network is fine.' Help desk: 200 tickets and no updates.",
                "evidence": [
                    ["RACI chart", "VPN service has no named owner — it predates the chart"],
                    ["Monitoring", "Nobody was alerted; users reported it"],
                    ["Last change", "A firewall rule push Friday night — change ticket has no service owner listed"]
                ],
                "options": [
                    "The firewall change caused it — roll it back and move on",
                    "The ownership gap caused the 90 minutes: no service owner means no monitoring, no change accountability, and no communication — the outage is a roles failure wearing a technical mask",
                    "Hire more help desk staff to handle the ticket volume"
                ],
                "correct": 1,
                "explain": "The technical trigger (firewall rule) is secondary. Ninety minutes of silence comes from the missing role: no service owner, no monitoring ownership, no comms owner. Fix the RACI and the next outage gets a 5-minute response."
            },
            {
                "symptom": "VPN restored. The post-mortem needs exactly one roles change that prevents recurrence. Which?",
                "evidence": [
                    ["Options", "Name a service owner / buy a new VPN / add headcount"],
                    ["Constraint", "One change, structural, not headcount"]
                ],
                "options": [
                    "Buy an enterprise VPN appliance",
                    "Name a service owner for the VPN with explicit accountability: monitoring, change approval, and user communication",
                    "Add two network engineers"
                ],
                "correct": 1,
                "explain": "A named service owner with the three accountabilities (monitor, approve changes, communicate) converts every future incident from chaos to procedure. Tools don't own services; people do."
            },
            {
                "symptom": "The CIO asks how to find the OTHER unowned services before they fail. What's the method?",
                "evidence": [
                    ["Inventory", "400+ services, most grown organically"],
                    ["Goal", "Every production service gets an owner without boiling the ocean"]
                ],
                "options": [
                    "Audit all 400 services immediately in one big project",
                    "Require an owner field on every change ticket and incident: unowned services reveal themselves at the exact moments they matter, then backfill systematically",
                    "Assume the critical ones are already owned"
                ],
                "correct": 1,
                "explain": "Let incidents and changes surface the gaps: mandatory owner fields turn every ticket into a coverage audit. Backfill the revealed gaps quarterly. Coverage emerges from process, not from a heroic one-time audit."
            }
        ],
        "debrief": "Most 'technical' outages are roles failures: unowned services, unassigned monitoring, unnamed communicators. The roles library exists so the next outage meets an owner, not a pointing contest.",
        "points": 15
    },
    {
        "id": "roles-library-sim-2",
        "title": "The Career Fork",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "You're a tier-2 support engineer with three years in. Two paths open: deep specialist or people-leading manager. Choose with a skills matrix, not vibes.",
        "steps": [
            {
                "id": "fork",
                "text": "Your skills matrix: troubleshooting 9/10, scripting 7/10, mentoring juniors 8/10, architecture 4/10, stakeholder politics 3/10. The specialist track (SRE) needs architecture 8+; the manager track needs stakeholder skills 7+. Your move?",
                "choices": [
                    {"label": "Push for the SRE role now — specialists earn more", "feedback": "You'd enter senior interviews with architecture at 4/10. The rejections will be polite and unanimous.", "points": 2, "next": "sre"},
                    {"label": "Map the gaps honestly: 6 months building architecture depth (homelab, certs, project work), then apply", "feedback": "The matrix becomes a plan: architecture 4→7 via deliberate projects, scripting 7→8 via automation wins. You apply when the matrix says so.", "points": 10, "next": "plan"},
                    {"label": "Take the team-lead opening — management is the only real promotion", "feedback": "With stakeholder skills at 3/10, you'd be a lead who can't shield the team or negotiate scope. The team suffers and so do you.", "points": 3, "next": "lead"}
                ]
            },
            {
                "id": "sre",
                "text": "Two SRE interviews, two rejections: 'strong troubleshooting, not enough systems design.' What's the repair?",
                "choices": [
                    {"label": "Blame the interviewers — leetcode-style system design is broken", "feedback": "Maybe, but the market doesn't care about your critique. The gap is real regardless of the interview format.", "points": 1, "next": "END"},
                    {"label": "Treat the rejections as a free skills audit: build the missing architecture depth in public (blog, homelab, open source) and re-apply in 6 months", "feedback": "Rejections are data. Six months of visible building converts 'not enough' into a portfolio.", "points": 7, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "lead",
                "text": "Three months as team lead: you're drowning in stakeholder meetings, the team's velocity dropped, and your best engineer just quit citing 'no technical direction'. Diagnose.",
                "choices": [
                    {"label": "Work longer hours — leads are supposed to absorb pain", "feedback": "Hours don't fix a skills gap. The team needs technical direction and stakeholder shielding you can't yet provide.", "points": 1, "next": "END"},
                    {"label": "Step back to senior IC, keep mentoring (your 8/10), and deliberately train stakeholder skills before trying leadership again", "feedback": "The mature move: retreat to strength, train the weakness deliberately. Leadership will still be there when the matrix is ready.", "points": 7, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "plan",
                "text": "Six months later: architecture 7/10, two automation projects in production, a blog with real readers. The SRE loop invites you back. Final interview question: 'Why should we hire a support engineer as an SRE?'",
                "choices": [
                    {"label": "'Because I learn fast and work hard.'", "feedback": "Everyone says this. You have something better — say it.", "points": 3, "next": "END"},
                    {"label": "'Because I've spent three years debugging production from the user side — I know how systems fail in ways dashboards miss. Here's the matrix, the projects, and the post-mortems to prove it.'", "feedback": "You turned the 'support' background into the differentiator: failure-mode intuition that pure-infra hires lack. Hired.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Career moves are skills-matrix operations: measure honestly, train the specific gaps, apply when the matrix — not your impatience — says ready. And your history is an asset when you frame it as one.",
        "points": 20
    },
    {
        "id": "roles-library-sim-3",
        "title": "Escalate the Incident",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Order the incident escalation ladder from first responder to executive — who gets involved when.",
        "steps": {
            "context": "A P2 incident is degrading checkout. Order the escalation path.",
            "items": [
                "Tier 1 support: acknowledge, run the runbook, contain what you can",
                "Tier 2 / on-call engineer: deeper diagnosis, first code-level fixes",
                "Service owner: authorize risky mitigations, own customer communication",
                "Incident commander: coordinate multiple teams, manage the war room",
                "Executive sponsor: engaged only if customer impact crosses the business threshold"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Escalation is about matching authority to impact: runbooks first, engineers second, owners for risky calls, commanders for coordination, executives for business thresholds. Skipping levels wastes everyone's time.",
        "points": 10
    },
    {
        "id": "roles-library-sim-4",
        "title": "Audit the Access Review",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The quarterly access review has 3 violations hiding in plain sight. Find them.",
        "steps": {
            "config": "# access-review.conf — Q3\nceo_admin = true                # line 2\nintern_prod_db = write          # line 3\nmfa_required = all_users        # line 4\ntermd_employee = active         # line 5\nbreak_glass = logged            # line 6\nvendor_support = standing_admin # line 7\nreviews = quarterly             # line 8",
            "find": 3,
            "issues": [
                {"line": 3, "description": "Intern has WRITE on the production database — violates least privilege catastrophically.", "fix": "intern_prod_db = none; interns get anonymized staging data."},
                {"line": 5, "description": "Terminated employee still active — the offboarding process failed and nobody noticed for a quarter.", "fix": "termd_employee = disabled immediately; tie deprovisioning to HR termination events."},
                {"line": 7, "description": "Vendor holds standing admin — persistent third-party privileged access with no expiry.", "fix": "vendor_support = just-in-time elevation with ticket linkage and auto-expiry."}
            ]
        },
        "debrief": "Lines 2, 4, 6, 8 are defensible (CEO admin with MFA, logged break-glass, quarterly reviews). The violations: intern write on prod, a ghost account, and standing vendor admin. Access reviews exist to catch exactly these.",
        "points": 15
    },
    {
        "id": "roles-library-sim-5",
        "title": "The Hiring Panel",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "You're hiring a junior SOC analyst. Two finalists, one headcount. The panel is split. Break the tie correctly.",
        "steps": [
            {
                "id": "panel",
                "text": "Finalist A: CS degree, 3.9 GPA, polished, aced the trivia questions, no homelab. Finalist B: no degree, works help desk, maintains a detection-rules GitHub with 200 stars, fumbled one trivia question but debugged a live log sample brilliantly. The panel is split 2-2. Your vote?",
                "choices": [
                    {"label": "A — the degree and polish predict reliability", "feedback": "You've hired a credential. In six months A knows the playbook; B would have WRITTEN a better one.", "points": 3, "next": "credential"},
                    {"label": "B — demonstrated skill (detection rules, live debugging) beats credentials for this role", "feedback": "The GitHub is a work sample; the live debug was a job trial. B has already done the job in public.", "points": 10, "next": "skill"},
                    {"label": "Abstain — let the panel majority decide", "feedback": "Abstention is a decision to let noise decide. The hiring manager's job is judgment.", "points": 1, "next": "credential"}
                ]
            },
            {
                "id": "credential",
                "text": "A is hired. Month four: A escalates everything, writes no detections, and the senior analysts are quietly carrying the queue. The hiring manager asks what went wrong in the loop. Your honest answer?",
                "choices": [
                    {"label": "'A needs more time — juniors take a year.'", "feedback": "Time doesn't fix a hiring-criteria error. The loop selected for trivia, and trivia is what you got.", "points": 2, "next": "END"},
                    {"label": "'We hired the credential instead of the work sample. Next loop: paid work-sample exercise weighted above trivia.'", "feedback": "The fix is structural: work samples predict job performance; trivia predicts interview performance. Change the loop.", "points": 7, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "skill",
                "text": "B is hired. Month two: B's detection rule catches a real intrusion the commercial feed missed. But B's ticket hygiene is sloppy and documentation thin. How do you develop the hire?",
                "choices": [
                    {"label": "Put B on a PIP for the documentation gaps", "feedback": "A PIP for a two-month junior who just caught an intrusion is how you lose exactly the people you fought to hire.", "points": 2, "next": "END"},
                    {"label": "Pair B with a senior for ticket hygiene, make documentation part of the detection-ship checklist, and keep B writing rules", "feedback": "Develop the weakness without punishing the strength: checklists and pairing for hygiene, full runway for detections. That's what good leads do.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Hire for demonstrated work, develop the gaps structurally. The roles library's hiring lesson: work samples predict performance, credentials predict interviews — and juniors with spikes need scaffolding, not PIPs.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "roles-library-console-1",
        "title": "Provision the Team",
        "console": "aws-iam",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "New SOC analysts start Monday. Build their identities: users, groups, least-privilege policies, and MFA.",
        "tasks": [
            {"id": "roles-library-console-1-t1", "instruction": "Create an IAM user named 'soc-analyst-01'.", "validate": {"action": "create-user", "params": {"name": "soc-analyst-01"}}, "hint": "Users section: create user 'soc-analyst-01'."},
            {"id": "roles-library-console-1-t2", "instruction": "Create a group named 'soc-tier1'.", "validate": {"action": "create-group", "params": {"name": "soc-tier1"}}, "hint": "Groups section: create group 'soc-tier1'."},
            {"id": "roles-library-console-1-t3", "instruction": "Add 'soc-analyst-01' to the 'soc-tier1' group.", "validate": {"action": "add-user-to-group", "params": {"user": "soc-analyst-01", "group": "soc-tier1"}}, "hint": "Users section: add user to group form — USER soc-analyst-01, GROUP soc-tier1."},
            {"id": "roles-library-console-1-t4", "instruction": "Enable MFA for 'soc-analyst-01'.", "validate": {"action": "enable-mfa", "params": {"user": "soc-analyst-01"}}, "hint": "Users section: enable MFA form with USER soc-analyst-01."}
        ],
        "debrief": "Onboarding is identity work: named users, role-based groups, least-privilege membership, MFA from day one. The access review in sim-4 is what happens when this step is skipped."
    },
    {
        "id": "roles-library-console-2",
        "title": "Work the Help Desk Queue",
        "console": "ticketing",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Tier 1 lives in the queue. Create, assign, and advance tickets by the book.",
        "tasks": [
            {"id": "roles-library-console-2-t1", "instruction": "Create a P3 ticket titled 'New hire needs laptop imaged'.", "validate": {"action": "create-ticket", "params": {"title": "New hire needs laptop imaged", "priority": "P3"}}, "hint": "New ticket: TITLE exactly as given, PRIORITY P3."},
            {"id": "roles-library-console-2-t2", "instruction": "Assign INC-9001 to 'tier1-amy'.", "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "tier1-amy"}}, "hint": "Assign form: INC-9001 → tier1-amy."},
            {"id": "roles-library-console-2-t3", "instruction": "Add a note to INC-9001: 'User confirmed VPN stable after reimage.'", "validate": {"action": "add-note", "params": {"id": "INC-9001", "text": "User confirmed VPN stable after reimage."}}, "hint": "Add note form: INC-9001 with the exact text."},
            {"id": "roles-library-console-2-t4", "instruction": "Resolve INC-9001 with resolution 'Reimaged; VPN stable.'", "validate": {"action": "resolve-ticket", "params": {"id": "INC-9001", "resolution": "Reimaged; VPN stable."}}, "hint": "Resolve form: INC-9001, resolution exactly 'Reimaged; VPN stable.'"}
        ],
        "debrief": "Tier 1 is the profession's foundation: every ticket gets an owner, a note trail, and a real resolution. The escalation ladder in sim-3 only works if tier 1 does this part right."
    },
    {
        "id": "roles-library-console-3",
        "title": "Assign Cloud RBAC",
        "console": "azure-portal",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Map the new data analyst to their role: resource group, and a least-privilege RBAC assignment.",
        "tasks": [
            {"id": "roles-library-console-3-t1", "instruction": "Create a resource group named 'rg-analytics' in location 'eastus'.", "validate": {"action": "create-rg", "params": {"name": "rg-analytics", "location": "eastus"}}, "hint": "Resource Groups: NAME rg-analytics, LOCATION eastus."},
            {"id": "roles-library-console-3-t2", "instruction": "Create a virtual network in 'rg-analytics' with CIDR 10.5.0.0/16.", "validate": {"action": "create-vnet", "params": {"rg": "rg-analytics", "cidr": "10.5.0.0/16"}}, "hint": "Virtual Networks: RESOURCE GROUP rg-analytics, CIDR 10.5.0.0/16."},
            {"id": "roles-library-console-3-t3", "instruction": "Assign the 'Reader' role to principal 'data-analyst-02' on scope 'rg-analytics'.", "validate": {"action": "assign-rbac", "params": {"scope": "rg-analytics", "principal": "data-analyst-02", "role": "Reader"}}, "hint": "Use the RBAC assignment (assign-rbac): SCOPE rg-analytics, PRINCIPAL data-analyst-02, ROLE Reader."}
        ],
        "debrief": "Cloud roles are the roles library made concrete: scopes, principals, and named roles instead of shared admin passwords. Reader first — elevate only with a ticket."
    },
    {
        "id": "roles-library-console-4",
        "title": "Set File Permissions by Role",
        "console": "linux-desktop",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Translate role boundaries into file permissions: restrict the app config to its service account.",
        "tasks": [
            {"id": "roles-library-console-4-t1", "instruction": "Select the file /etc/app.conf.", "validate": {"action": "select", "params": {"path": "/etc/app.conf"}}, "hint": "Click Select on the /etc/app.conf row."},
            {"id": "roles-library-console-4-t2", "instruction": "Set mode 640 on /etc/app.conf — owner and group read, nothing for others.", "validate": {"action": "chmod", "params": {"path": "/etc/app.conf", "mode": "640"}}, "hint": "chmod form: PATH /etc/app.conf, MODE 640."},
            {"id": "roles-library-console-4-t3", "instruction": "Change the owner of /etc/app.conf to 'svc-app'.", "validate": {"action": "chown", "params": {"path": "/etc/app.conf", "owner": "svc-app"}}, "hint": "chown form: PATH /etc/app.conf, OWNER svc-app."}
        ],
        "debrief": "Least privilege starts at the filesystem: every file has an owning role, and permissions encode exactly what that role needs. The access review catches what this step prevents."
    }
]

MISSIONS = [
    {
        "id": "roles-library-term-1",
        "title": "Survey the Directory",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Orient: list the workspace and read the notes.",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "logs/", "hint": "Type: ls."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "Linux essentials", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Directory surveyed. Know the org chart before the incident."
    },
    {
        "id": "roles-library-term-2",
        "title": "Draft the RACI",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Write the VPN service's RACI line to raci.txt.",
        "objectives": ["Write the owner line", "Append the support line", "Read the RACI back"],
        "checks": [
            {"command_pattern": "echo.*>\\s*raci\\.txt", "expect_contains": "", "hint": "Type: echo \"vpn owner: netops-lead\" > raci.txt (no output on success)."},
            {"command_pattern": "echo.*>>\\s*raci\\.txt", "expect_contains": "", "hint": "Type: echo \"vpn support: tier1-queue\" >> raci.txt."},
            {"command_pattern": "cat\\s+raci\\.txt", "expect_contains": "netops-lead", "hint": "Type: cat raci.txt."}
        ],
        "success_message": "RACI drafted. Unowned services are outages waiting for a date."
    },
    {
        "id": "roles-library-term-3",
        "title": "Audit the Roster",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Count RACI lines and search for the owner entry.",
        "objectives": ["Count lines", "Find the owner line"],
        "checks": [
            {"command_pattern": "wc\\s+-l\\s+raci\\.txt", "expect_contains": "raci.txt", "hint": "Type: wc -l raci.txt."},
            {"command_pattern": "grep\\s+owner\\s+raci\\.txt", "expect_contains": "owner", "hint": "Type: grep owner raci.txt."}
        ],
        "success_message": "Roster audited. Every service, an owner. Every owner, named."
    },
    {
        "id": "roles-library-term-4",
        "title": "Seal the Skills Matrix",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Hash your skills-matrix snapshot — the honest baseline, tamper-evident.",
        "objectives": ["Hash the matrix string"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "troubleshooting-9", "hint": "Type: sha256sum troubleshooting-9 architecture-4 — the real hash plus your scores are echoed."}
        ],
        "success_message": "Matrix sealed. Measure honestly — the matrix is a plan, not a verdict."
    },
    {
        "id": "roles-library-term-5",
        "title": "Verify the Environment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Confirm identity and home directory.",
        "objectives": ["Print the environment", "Expand HOME"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps."},
            {"command_pattern": "echo\\s+\\$HOME", "expect_contains": "/home/candidate", "hint": "Type: echo $HOME."}
        ],
        "success_message": "Identity verified. Know your role before you play it."
    },
    {
        "id": "roles-library-term-6",
        "title": "Read the Incident Log",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The outage left a log trail. Read its edges and find the errors.",
        "objectives": ["Read the first lines", "Read the last lines", "Find errors"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "INFO", "hint": "Type: head -n 3 logs/app.log."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "ERROR", "hint": "Type: tail -n 3 logs/app.log."},
            {"command_pattern": "grep\\s+ERROR\\s+logs/app\\.log", "expect_contains": "timeout", "hint": "Type: grep ERROR logs/app.log — the timeout error appears."}
        ],
        "success_message": "Log read. Post-mortems start with the timeline."
    },
    {
        "id": "roles-library-term-7",
        "title": "Check Directory Reachability",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Verify the identity provider is reachable: DNS and ping.",
        "objectives": ["Resolve the IdP host", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig idp.example.org."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping idp.example.org."}
        ],
        "success_message": "IdP reachable. Identity is the perimeter — verify the road to it."
    }
]
