# Batch 7 — study-protocol: The Deep Work Study Protocol
DOMAIN = "study-protocol"

SIMS = [
    {
        "id": "study-protocol-sim-1",
        "title": "Why Did the Study Week Fail?",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "You 'studied' 25 hours this week and failed the practice exam. Diagnose the protocol failure.",
        "steps": [
            {
                "symptom": "25 logged hours, practice exam score 52% (passing is 70%).",
                "evidence": [
                    ["Activity log", "18 hours re-reading notes, 5 hours highlighting, 2 hours practice questions"],
                    ["Recall test", "Can define terms, cannot apply them to new problems"],
                    ["Schedule", "No spaced intervals — everything crammed in 3 days"]
                ],
                "options": [
                    "Not enough hours — push to 35 next week",
                    "Fluency illusion: re-reading and highlighting build recognition, not recall — the protocol optimized for the feeling of learning, and massed cramming guaranteed forgetting",
                    "The exam was unfair"
                ],
                "correct": 1,
                "explain": "Re-reading produces fluency (it feels known) without retrievability. The evidence: definitions without application. The protocol must swap recognition activities for retrieval activities and distribute them over time."
            },
            {
                "symptom": "You switch to practice questions. Scores rise to 64% but plateau. What's the missing mechanism?",
                "evidence": [
                    ["Method", "100 practice questions, answers checked immediately"],
                    ["Errors", "Same 6 misconceptions repeating across weeks"],
                    ["Review", "Wrong answers re-read once, never re-tested"]
                ],
                "options": [
                    "Do 200 questions instead of 100",
                    "Error-driven spaced repetition: each misconception becomes a flashcard scheduled at expanding intervals until it's answered correctly three times cold",
                    "Find harder questions"
                ],
                "correct": 1,
                "explain": "Plateaus come from uncorrected misconceptions. The fix is a system: errors → cards → spaced schedule → cold-correct ×3. Volume without an error loop just rehearses the same mistakes faster."
            },
            {
                "symptom": "New protocol designed. What single weekly metric proves it's working before the next exam?",
                "evidence": [
                    ["Constraint", "Must be measurable weekly, game-resistant"],
                    ["Goal", "Predicts exam performance, not just effort"]
                ],
                "options": [
                    "Hours studied per week",
                    "Cold recall rate: percentage of due flashcards answered correctly with no hints, tracked weekly",
                    "Pages of notes written"
                ],
                "correct": 1,
                "explain": "Cold recall rate measures the actual asset (retrievable knowledge), not the input (hours) or the exhaust (notes). If it climbs 5% a week, the exam takes care of itself."
            }
        ],
        "debrief": "Study protocols fail on fluency (recognition ≠ recall), massing (cramming ≠ learning), and missing error loops. The fix: retrieval practice, spaced intervals, error cards, and one honest metric.",
        "points": 15
    },
    {
        "id": "study-protocol-sim-2",
        "title": "Choose the Method",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A brutal certification exam in 8 weeks. Four study methods compete for your 15 hours/week. Allocate like an engineer.",
        "steps": [
            {
                "id": "allocate",
                "text": "15 hrs/week, 8 weeks. Options: (A) video course end-to-end, (B) textbook cover-to-cover, (C) practice-exam-driven with targeted remediation, (D) study group discussions. Your allocation?",
                "choices": [
                    {"label": "A — videos feel productive and cover everything", "feedback": "Videos are the re-reading of the digital age: high fluency, low retrieval. Eight weeks later you'll recognize everything and recall nothing under pressure.", "points": 2, "next": "passive"},
                    {"label": "C — practice exams first, then remediate exactly what fails", "feedback": "The exam is the specification: test early, let failures aim your studying, remediate with focused retrieval. Every hour targets a measured gap.", "points": 10, "next": "targeted"},
                    {"label": "B — the textbook is the complete source of truth", "feedback": "Complete and unfinishable: 900 pages in 8 weeks at 15 hrs/week means skimming, and skimming means fluency without recall.", "points": 3, "next": "passive"}
                ]
            },
            {
                "id": "passive",
                "text": "Week 5: you've 'covered' 70% of the material but your first practice exam scores 58%. Panic is setting in. Repair?",
                "choices": [
                    {"label": "Speed up — finish the remaining 30% then do practice exams", "feedback": "More coverage of the same passive method. The 58% isn't a coverage problem; it's a retrieval problem.", "points": 1, "next": "END"},
                    {"label": "Stop covering; switch to exam-driven remediation now — 3 weeks of targeted retrieval beats 3 weeks of finishing videos", "feedback": "The correct late-stage pivot: abandon coverage, attack measured gaps. Triage beats completion.", "points": 7, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "targeted",
                "text": "Week 5: practice scores 76% and climbing. But networking questions sit at 40% while everything else is 80%+. Your move?",
                "choices": [
                    {"label": "Keep the balanced rotation — it'll come up naturally", "feedback": "The data names the gap; ignoring it is choosing to fail networking. Balanced feels fair; targeted wins.", "points": 3, "next": "END"},
                    {"label": "Reallocate: 60% of hours to networking until it hits 70%, maintenance reps for the rest", "feedback": "Data-driven reallocation: attack the weakest link, maintain the rest with spaced reps. This is what the protocol is FOR.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Study like an engineer: the exam is the spec, practice tests are the test suite, failures are the bug reports, and your hours are the sprint capacity. Allocate to the red tests.",
        "points": 20
    },
    {
        "id": "study-protocol-sim-3",
        "title": "Build the Study Session",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Order the five moves of a 90-minute protocol study session.",
        "steps": {
            "context": "One 90-minute session, one topic. Order the moves for maximum durable learning.",
            "items": [
                "Warm up with 10 minutes of cold recall on yesterday's material (no notes)",
                "Attempt new problems BEFORE consulting references — struggle first",
                "Check answers and convert every error into a spaced-repetition card",
                "Do a 5-minute free-recall brain dump of the session's key ideas",
                "Log the session: what was learned, what's still shaky, tomorrow's target"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Recall before reference (warm-up), struggle before help (desirable difficulty), errors into cards (the loop), brain dump (consolidation), log (tomorrow's start). The session is a pipeline, not a vibe.",
        "points": 10
    },
    {
        "id": "study-protocol-sim-4",
        "title": "Audit the Study Plan",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A study plan for a certification exam has 3 protocol violations. Find them.",
        "steps": {
            "config": "# study-plan.conf — 8 week cert prep\nmethod = reread_notes            # line 2\nschedule = cram_weekends          # line 3\nretrieval = none                  # line 4\nerror_cards = 0                   # line 5\npractice_exams = 1                # line 6\nsleep = 5h                        # line 7\nreview = weekly                   # line 8",
            "find": 3,
            "issues": [
                {"line": 2, "description": "Method is re-reading notes — pure fluency, zero retrieval. The plan optimizes for feeling prepared.", "fix": "method = retrieval_practice (cold recall, practice questions, brain dumps)."},
                {"line": 3, "description": "Crammed weekends — massed practice guarantees maximum forgetting between sessions.", "fix": "schedule = distributed daily blocks with spaced intervals."},
                {"line": 4, "description": "No retrieval practice at all — the single highest-evidence study technique is entirely absent.", "fix": "retrieval = every session starts with cold recall."}
            ]
        },
        "debrief": "Lines 5–8 are also weak (no error cards, one practice exam, 5h sleep) but the three flagged lines are the structural violations: no retrieval, massed schedule, fluency-based method. Fix the method first.",
        "points": 15
    },
    {
        "id": "study-protocol-sim-5",
        "title": "Exam Week Triage",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "The exam is in 72 hours. Your cold-recall rate is 68%; passing needs ~75%. Triage the final three days.",
        "steps": [
            {
                "id": "triage",
                "text": "72 hours left. Cold recall 68%, need 75%. Your error cards cluster in two domains: subnetting (55%) and IAM policies (61%). Everything else is 75%+. The plan?",
                "choices": [
                    {"label": "Re-read all the notes once more for confidence", "feedback": "Confidence without recall is how you walk in at 68% and walk out at 68%. The data is begging you to target.", "points": 1, "next": "panic"},
                    {"label": "All retrieval, all gaps: drill subnetting and IAM cards at tight intervals, one full practice exam at hour 48, sleep 8h nightly", "feedback": "The triage protocol: attack the measured gaps, verify with a full exam, protect sleep — the highest-ROI 72 hours available.", "points": 10, "next": "discipline"},
                    {"label": "Pull two all-nighters — more hours is more learning", "feedback": "Sleep deprivation destroys exactly what the exam tests: recall under pressure. You'd trade 5 points of knowledge for 10 points of impairment.", "points": 2, "next": "panic"}
                ]
            },
            {
                "id": "panic",
                "text": "24 hours left and you're exhausted, scoring 66% on drills — worse than three days ago. Emergency move?",
                "choices": [
                    {"label": "Caffeine and one more all-nighter — push through", "feedback": "Pushing through impairment is how 68% becomes 60%. The exam punishes exactly this.", "points": 0, "next": "END"},
                    {"label": "Stop. Sleep 8 hours, light review only, trust the base — damage control beats more damage", "feedback": "The least-bad move: sleep restores recall more than any cramming recovers. You sit the exam at your true 68% instead of an impaired 60%.", "points": 5, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "discipline",
                "text": "Hour 48 practice exam: 77%. The gaps closed. Last 24 hours — what now?",
                "choices": [
                    {"label": "Learn a brand-new topic to 'maximize coverage'", "feedback": "New topics at hour 48 create interference and anxiety. The exam rewards depth on the spec, not breadth beyond it.", "points": 3, "next": "END"},
                    {"label": "Light maintenance reps, review error cards once, pack your bag, sleep early — arrive at 100% of your 77%", "feedback": "The professional finish: protect the gains, arrive rested. Exams are won in the 8 weeks before, and lost in the 24 hours before.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Exam-week triage: drill the measured gaps, verify with a full practice exam, protect sleep absolutely. The protocol's final lesson — performance is retrieval plus rest, and rest is not negotiable.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "study-protocol-console-1",
        "title": "Organize the Study Archive",
        "console": "linux-desktop",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Your study materials need archival order: a subjects directory, a protected error-log file, and locked permissions.",
        "tasks": [
            {"id": "study-protocol-console-1-t1", "instruction": "Create the directory /home/user/study.", "validate": {"action": "create-dir", "params": {"path": "/home/user/study"}}, "hint": "Create directory: PATH /home/user/study."},
            {"id": "study-protocol-console-1-t2", "instruction": "Create the file /home/user/study/error-log.txt — every misconception gets logged here.", "validate": {"action": "create-file", "params": {"path": "/home/user/study/error-log.txt"}}, "hint": "Create file: PATH /home/user/study/error-log.txt."},
            {"id": "study-protocol-console-1-t3", "instruction": "Set mode 600 on /home/user/study/error-log.txt — your error log is private.", "validate": {"action": "chmod", "params": {"path": "/home/user/study/error-log.txt", "mode": "600"}}, "hint": "Select the file, then chmod with mode 600."}
        ],
        "debrief": "The protocol needs infrastructure: a study directory, an error log with a name that reminds you what it's for, and permissions that keep it yours."
    },
    {
        "id": "study-protocol-console-2",
        "title": "Run the Study Pipeline",
        "console": "cicd-pipeline",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Treat your study week like a pipeline: trigger the week's run, retry the failed recall stage, configure the target, ship the review.",
        "tasks": [
            {"id": "study-protocol-console-2-t1", "instruction": "Trigger a new build — this week's study run.", "validate": {"action": "trigger-build", "params": {}}, "hint": "Click 'Trigger new build'."},
            {"id": "study-protocol-console-2-t2", "instruction": "The 'test' stage (Friday's cold-recall check) failed — retry it.", "validate": {"action": "retry-stage", "params": {"stage": "test"}}, "hint": "Click Retry on test."},
            {"id": "study-protocol-console-2-t3", "instruction": "Set variable TARGET_RECALL_PCT to 75.", "validate": {"action": "set-variable", "params": {"key": "TARGET_RECALL_PCT", "value": "75"}}, "hint": "Variables: KEY TARGET_RECALL_PCT, VALUE 75."},
            {"id": "study-protocol-console-2-t4", "instruction": "Approve the gated 'deploy' stage — publish the week's review notes.", "validate": {"action": "approve-stage", "params": {"stage": "deploy"}}, "hint": "Click Approve on deploy."}
        ],
        "debrief": "The study week as CI: trigger (start), retry (re-drill failures), variables (declare targets), approve (publish the review). Green builds compound."
    },
    {
        "id": "study-protocol-console-3",
        "title": "Triage the Blocker Queue",
        "console": "ticketing",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Study blockers are incidents. Log them, assign them, move them — don't ruminate on them.",
        "tasks": [
            {"id": "study-protocol-console-3-t1", "instruction": "Create a P2 ticket titled 'Subnetting cold recall stuck at 55%'.", "validate": {"action": "create-ticket", "params": {"title": "Subnetting cold recall stuck at 55%", "priority": "P2"}}, "hint": "New ticket: TITLE exactly as given, PRIORITY P2."},
            {"id": "study-protocol-console-3-t2", "instruction": "Assign INC-9001 to 'study-buddy'.", "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "study-buddy"}}, "hint": "Assign: INC-9001 → study-buddy."},
            {"id": "study-protocol-console-3-t3", "instruction": "Move INC-9001 to 'in-progress'.", "validate": {"action": "update-status", "params": {"id": "INC-9001", "status": "in-progress"}}, "hint": "Update status: INC-9001 → in-progress."}
        ],
        "debrief": "Externalize the blockers: a ticketed gap gets a plan; a ruminated gap gets anxiety. The queue is where stuck becomes scheduled."
    },
    {
        "id": "study-protocol-console-4",
        "title": "Review the Notes Repo",
        "console": "git-host",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Your study notes live under version control. Branch the week's review, open the PR, and merge the corrections.",
        "tasks": [
            {"id": "study-protocol-console-4-t1", "instruction": "Create a branch named 'review/week-5-corrections'.", "validate": {"action": "create-branch", "params": {"name": "review/week-5-corrections"}}, "hint": "Branches: create 'review/week-5-corrections'."},
            {"id": "study-protocol-console-4-t2", "instruction": "Open a PR titled 'Week 5: fix 6 misconception notes' from head 'review/week-5-corrections' to base 'main'.", "validate": {"action": "open-pr", "params": {"title": "Week 5: fix 6 misconception notes", "base": "main", "head": "review/week-5-corrections"}}, "hint": "Open PR: exact title, BASE main, HEAD review/week-5-corrections."},
            {"id": "study-protocol-console-4-t3", "instruction": "Merge PR #1 (the pre-seeded one) — clear the queue before your review lands.", "validate": {"action": "merge-pr", "params": {"pr": 1}}, "hint": "In Pull requests, click Merge on PR #1."}
        ],
        "debrief": "Notes under version control: corrections are PRs, misconceptions get fixed with history, and the log shows exactly when each idea became correct."
    }
]

MISSIONS = [
    {
        "id": "study-protocol-term-1",
        "title": "Survey the Desk",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Orient: list the workspace and read the notes.",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "notes.txt", "hint": "Type: ls."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "study notes", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Desk surveyed. The protocol starts with knowing the material."
    },
    {
        "id": "study-protocol-term-2",
        "title": "Start the Recall Log",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Log cold-recall sessions to recall.txt — the protocol's honest instrument.",
        "objectives": ["Log the first session", "Append a second session", "Read the log"],
        "checks": [
            {"command_pattern": "echo.*>\\s*recall\\.txt", "expect_contains": "", "hint": "Type: echo \"session1 recall 62pct\" > recall.txt (no output on success)."},
            {"command_pattern": "echo.*>>\\s*recall\\.txt", "expect_contains": "", "hint": "Type: echo \"session2 recall 68pct\" >> recall.txt."},
            {"command_pattern": "cat\\s+recall\\.txt", "expect_contains": "session1", "hint": "Type: cat recall.txt."}
        ],
        "success_message": "Recall log started. What gets measured gets learned."
    },
    {
        "id": "study-protocol-term-3",
        "title": "Measure the Trend",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Count sessions and search the log — is recall climbing?",
        "objectives": ["Count log lines", "Search for session entries"],
        "checks": [
            {"command_pattern": "wc\\s+-l\\s+recall\\.txt", "expect_contains": "recall.txt", "hint": "Type: wc -l recall.txt."},
            {"command_pattern": "grep\\s+recall\\s+recall\\.txt", "expect_contains": "recall", "hint": "Type: grep recall recall.txt."}
        ],
        "success_message": "Trend measured. Climbing cold-recall is the only progress that counts."
    },
    {
        "id": "study-protocol-term-4",
        "title": "Seal the Target",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Hash your exam-date target — commitment, tamper-evident.",
        "objectives": ["Hash the target string"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "recall-75", "hint": "Type: sha256sum recall-75 by exam day — the real hash plus your target are echoed."}
        ],
        "success_message": "Target sealed. The protocol commits before the pressure arrives."
    },
    {
        "id": "study-protocol-term-5",
        "title": "Check the Session Edges",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Review any log from its edges: first lines, last lines.",
        "objectives": ["Read the first lines", "Read the last lines"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "INFO", "hint": "Type: head -n 2 logs/app.log."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "ERROR", "hint": "Type: tail -n 2 logs/app.log."}
        ],
        "success_message": "Edges checked. Every review starts at the boundaries."
    },
    {
        "id": "study-protocol-term-6",
        "title": "Verify the Environment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Confirm the study environment: identity and home.",
        "objectives": ["Print the environment", "Expand HOME"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps."},
            {"command_pattern": "echo\\s+\\$HOME", "expect_contains": "/home/candidate", "hint": "Type: echo $HOME."}
        ],
        "success_message": "Environment verified. Control the controllables."
    },
    {
        "id": "study-protocol-term-7",
        "title": "Reach the Library",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Verify the digital library resolves and responds.",
        "objectives": ["Resolve the library domain", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig library.example.org."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping library.example.org."}
        ],
        "success_message": "Library reachable. The protocol's supply line is open."
    }
]
