import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_common import merge

D = 'adaptive-foundations'

SIMS = [
    {
        "id": "adapt-sim-stuck-learner",
        "title": "The learner stuck below mastery",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A learner has attempted the subnetting module 5 times, scoring 55–62% against an 80% mastery bar. The system keeps serving the same difficulty. Diagnose why the loop is not adapting.",
        "steps": [
            {
                "symptom": "5 attempts, scores flat at ~60%, same item difficulty each time, no hint usage, no prerequisite review assigned.",
                "options": [
                    "The learner is not trying hard enough — assign more attempts",
                    "The adaptation is broken: flat scores at 60% signal the items are outside the learner's zone of proximal development — the system should drop difficulty, diagnose the misconception, or route to prerequisites instead of repeating",
                    "Lower the mastery bar to 60%",
                    "The content is fine — some learners just fail"
                ],
                "correct": 1,
                "evidence": [
                    ["attempt-log.txt", "Attempts 1–5: 58, 61, 55, 62, 59. Item difficulty: constant 0.72. Hint requests: 0. Prerequisite 'binary arithmetic' status: not attempted."],
                    ["zpd-note.txt", "Zone of proximal development: learning happens just beyond current ability with support. Flat scores far below mastery indicate items too hard, a misconception, or missing prerequisites — never 'try the same thing again.'"],
                ],
                "explain": "Mastery learning requires the system to respond to evidence. Five flat attempts are five measurements saying 'this is not working' — the correct response is easier items, targeted hints, or prerequisite routing, not repetition."
            },
            {
                "symptom": "Diagnosis: missing prerequisite (binary arithmetic never attempted). What should the system have done at attempt 2?",
                "options": [
                    "Kept serving subnetting items — persistence builds character",
                    "Detected the flat pattern, administered a prerequisite probe, and routed to binary arithmetic remediation before returning to subnetting",
                    "Skipped the learner ahead to the next module",
                    "Reset the attempt counter"
                ],
                "correct": 1,
                "evidence": [
                    ["knowledge-space.txt", "Knowledge space theory: subnetting depends on binary arithmetic. A learner missing the prerequisite cannot master the dependent skill — the graph predicts the failure before it happens."],
                ],
                "explain": "Knowledge space theory turns 'stuck' into a diagnosable state: trace the prerequisite graph, find the missing node, remediate it. The system should have known at attempt 2 what the graph already said."
            }
        ],
        "debrief": "Adaptive systems earn the name by adapting: flat scores are a signal, prerequisites are a graph, and 'try again' is not a pedagogy. Diagnose the cause, route to the missing foundation, then return.",
        "points": 15
    },
    {
        "id": "adapt-sim-next-item",
        "title": "Choose the next item: the adaptive engine's decision",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The engine estimates a learner's subnetting ability at 65% (±10%). Three candidate items: easy (95% expected success), medium (70%), hard (35%). Choose the next item.",
        "steps": [
            {
                "symptom": "Ability estimate 65% ±10%. Candidates: easy (95% success), medium (70%), hard (35%). Goal: maximum information about the learner's true ability plus productive struggle.",
                "options": [
                    "The easy item — success builds confidence",
                    "The medium item — ~70% success probability sits in the zone of proximal development and maximally reduces uncertainty about the ability estimate",
                    "The hard item — challenge reveals the ceiling",
                    "Random — the engine should not play favorites"
                ],
                "correct": 1,
                "evidence": [
                    ["irt-note.txt", "Item response theory: information is maximized when item difficulty matches learner ability. A 70%-success item both teaches (productive struggle) and measures (tightens the estimate)."],
                    ["affect-note.txt", "95% items teach nothing and measure nothing; 35% items frustrate and also measure poorly (failure is uninformative about how far below)."],
                ],
                "explain": "Adaptive testing is measurement and teaching at once. The medium item is the only choice that does both: hard enough to inform, easy enough to learn from. Extremes waste the learner's time."
            },
            {
                "symptom": "The learner answers the medium item correctly but slowly (4x median time). How should the engine update its model?",
                "options": [
                    "Raise the ability estimate — correct is correct",
                    "Raise the estimate modestly but flag low fluency: correctness without fluency means the knowledge is fragile — schedule retrieval practice rather than advancing difficulty",
                    "Lower the estimate — slow means guessing",
                    "Ignore response time entirely"
                ],
                "correct": 1,
                "evidence": [
                    ["fluency.txt", "Mastery = accuracy + fluency. Slow-correct responses predict poor retention and transfer. The engine should bank the correctness but treat fluency as a separate skill dimension needing practice."],
                ],
                "explain": "A correct answer is not the whole story. Fluency — speed plus accuracy — is what survives the forgetting curve. The engine's job is to notice the fragility and prescribe practice, not just advance the difficulty."
            }
        ],
        "debrief": "Every item selection is a bet: maximize information, keep the learner in productive struggle, and read the full response — correctness, time, and hints — before updating the model.",
        "points": 15
    },
    {
        "id": "adapt-sim-test-anomaly",
        "title": "The impossible score jump",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A learner's ability estimate jumped from 40% to 95% in one 20-minute session, with median response time of 3 seconds per item. The integrity monitor flagged it. Respond.",
        "steps": [
            {
                "symptom": "Session: 30 items, 29 correct, 3s median response time (cohort median: 48s). Previous 6 sessions: 35–45% ability, 50s+ responses.",
                "options": [
                    "Celebrate — the learner had a breakthrough",
                    "Treat as a probable integrity violation: the response pattern (impossible speed + discontinuous jump) indicates answer sharing or automation — invalidate the session and investigate before the estimate poisons downstream adaptation",
                    "Average it into the estimate",
                    "Ban the learner immediately"
                ],
                "correct": 1,
                "evidence": [
                    ["integrity.txt", "Flags: response time <10th percentile on 29/30 items; ability discontinuity >4 standard deviations; IP geolocation changed mid-session. Pattern matches answer-key use, not learning (learning curves are gradual)."],
                    ["policy.txt", "Anomalous sessions are quarantined from the ability estimate pending review. Accusation requires evidence; invalidation requires only the anomaly."],
                ],
                "explain": "Learning is gradual; cheating is discontinuous. The pattern — not the score — is the evidence. Quarantine the session so it cannot corrupt the adaptive model, then investigate fairly."
            },
            {
                "symptom": "Investigation: the learner's older sibling completed the session. The learner cooperated fully. Disposition?",
                "options": [
                    "Permanent ban — zero tolerance",
                    "Invalidate the session, reset the estimate to the pre-anomaly value, require a proctored re-assessment for the affected module, and record the integrity lesson — proportionate, restorative, and protective of the model's integrity",
                    "Count the 95% — the sibling is basically a tutor",
                    "Do nothing"
                ],
                "correct": 1,
                "evidence": [
                    ["restorative.txt", "Goal: protect measurement integrity while keeping the learner in the program. Proctored re-assessment re-establishes a trustworthy estimate; the record deters repetition."],
                ],
                "explain": "The measurement must be protected (invalidate, re-assess) and the learner kept (restorative, not destructive). Integrity systems that only punish teach evasion; systems that re-measure teach honesty."
            }
        ],
        "debrief": "Adaptive systems are measurement instruments — contaminated data corrupts every downstream decision. Quarantine anomalies fast, investigate fairly, re-measure cleanly.",
        "points": 15
    },
    {
        "id": "adapt-sim-spacing",
        "title": "Schedule the retrieval practice",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A learner mastered subnetting (92%, fluent) 7 days ago. The forgetting curve predicts 60% retention today. Decide the retrieval-practice schedule.",
        "steps": [
            {
                "symptom": "Mastered 7 days ago at 92% fluent. Predicted retention today: 60%. Exam in 30 days. Options: re-study the chapter, one retrieval session today, or spaced retrieval sessions.",
                "options": [
                    "Re-study the chapter — re-reading feels productive",
                    "Spaced retrieval: a low-stakes recall session today, then expanding intervals (3 days, 7 days, 14 days) — retrieval practice beats re-study for durable retention",
                    "One big cram session the night before the exam",
                    "Nothing — 92% was mastery"
                ],
                "correct": 1,
                "evidence": [
                    ["retrieval-research.txt", "Testing effect: retrieval practice produces ~50% better long-term retention than re-study. Expanding intervals match the forgetting curve — practice arrives just as the memory fades."],
                    ["curve.txt", "Without practice: 92% -> 60% (7d) -> 35% (30d). With spaced retrieval: 92% -> 85%+ at 30d."],
                ],
                "explain": "Mastery is not permanent — it decays on a curve. Spaced retrieval re-strengthens the memory at the moment of fading, which is exactly when practice buys the most durability. Re-reading feels fluent because it is familiar, not because it is learned."
            },
            {
                "symptom": "The learner dreads the retrieval sessions ('tests are stressful'). How do you keep the schedule without the anxiety?",
                "options": [
                    "Drop the schedule — wellbeing first",
                    "Make retrieval low-stakes: no grades, immediate feedback, framed as practice — the learning benefit comes from the retrieval attempt, not the score",
                    "Make them high-stakes to motivate",
                    "Replace retrieval with videos"
                ],
                "correct": 1,
                "evidence": [
                    ["affect.txt", "Low-stakes retrieval preserves the testing effect while removing the threat response. Feedback after the attempt (not during) maximizes learning."],
                ],
                "explain": "The stress is in the stakes, not the retrieval. Keep the cognitive work (recall attempts) and remove the threat (grades, judgment) — the memory benefits stay, the anxiety goes."
            }
        ],
        "debrief": "Durable learning is scheduled forgetting-fighting: retrieval practice at expanding intervals, low stakes, with feedback. Design the schedule around the curve, not around the calendar.",
        "points": 15
    },
    {
        "id": "adapt-sim-mastery-rule",
        "title": "Set the mastery threshold",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The course team debates the mastery bar: 70%, 80%, or 90%. Too low advances fragile learners; too high traps competent ones in remediation. Set the rule.",
        "steps": [
            {
                "symptom": "Pilot data: at 70%, 22% of advancers fail the next module; at 90%, 31% of learners need 3+ remediation cycles and completion drops 18%. At 80%: 9% downstream failure, 12% need extended remediation.",
                "options": [
                    "70% — keep completion high",
                    "80% with a fluency requirement — the pilot data minimizes total harm: downstream failures and remediation burden are both near their minimum",
                    "90% — standards matter most",
                    "No threshold — let learners self-assess"
                ],
                "correct": 1,
                "evidence": [
                    ["pilot.txt", "Total-harm curve is U-shaped: 70% harms downstream (fragile advancers), 90% harms here (trapped learners). 80% + fluency (accuracy at speed) is the observed minimum of combined harm."],
                    ["fluency-note.txt", "Accuracy-only 80% still admits slow-correct fragility; adding a fluency bar (median time under threshold) cut downstream failure from 14% to 9% in the pilot."],
                ],
                "explain": "Threshold-setting is harm minimization with data, not a values debate. The pilot measured both failure modes and found the minimum — and fluency separates real mastery from slow correct."
            },
            {
                "symptom": "Threshold set at 80% + fluency. One more decision: what happens to the learner at 79%?",
                "options": [
                    "Advance them — close enough",
                    "Targeted remediation on the specific failed subskills (not the whole module), then a focused re-assessment — the system knows exactly which items were missed",
                    "Restart the entire module",
                    "Hold them until they hit 80% on the full module retest"
                ],
                "correct": 1,
                "evidence": [
                    ["diagnostic.txt", "The 79% learner missed 3 of 4 items on one subskill (CIDR notation) and passed everything else. Whole-module repetition wastes 80% of their time."],
                ],
                "explain": "The adaptive advantage is diagnosis: the system knows which subskill failed, so remediation targets exactly that. 'Close enough' advances fragility; whole-module repetition punishes precision with tedium."
            }
        ],
        "debrief": "Mastery thresholds are set by evidence, not tradition: measure both failure modes, pick the harm minimum, require fluency — and remediate the diagnosed gap, never the whole module.",
        "points": 15
    }
]

CONSOLES = [
    {
        "id": "adapt-console-mastery-table",
        "title": "Build the learner mastery table",
        "console": "sql-studio",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Create a learner_mastery table to track skills, then run a query finding mastered skills.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create table learner_mastery with columns 'learner_id, skill, attempts, mastered'.",
                "validate": {"action": "create-table", "params": {"name": "learner_mastery", "columns": "learner_id, skill, attempts, mastered"}},
                "hint": "Create table learner_mastery with columns: learner_id, skill, attempts, mastered"
            },
            {
                "id": "t2",
                "instruction": "Run a query that finds mastered skills.",
                "validate": {"action": "run-query", "params": {"match": "mastered"}},
                "hint": "Type a query containing the word 'mastered', e.g. SELECT skill FROM learner_mastery WHERE mastered = 1"
            }
        ],
        "debrief": "Adaptive engines run on data: the mastery table is the model's memory of every learner."
    },
    {
        "id": "adapt-console-support-ticket",
        "title": "Help the stuck learner",
        "console": "ticketing",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Open a P3 support ticket for the learner stuck on subnetting, assign it to the learning coach, and move it to in-progress.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a P3 ticket titled 'Learner stuck — subnetting module (5 attempts)'.",
                "validate": {"action": "create-ticket", "params": {"title": "Learner stuck — subnetting module (5 attempts)", "priority": "P3"}},
                "hint": "Create a P3 ticket titled 'Learner stuck — subnetting module (5 attempts)'."
            },
            {
                "id": "t2",
                "instruction": "Assign the ticket to 'learning-coach'.",
                "validate": {"action": "assign-ticket", "params": {"id": "1", "assignee": "learning-coach"}},
                "hint": "Assign ticket 1 to learning-coach."
            },
            {
                "id": "t3",
                "instruction": "Move the ticket to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "1", "status": "in-progress"}},
                "hint": "Update ticket 1 status to in-progress."
            }
        ],
        "debrief": "Stuck learners get human help: the ticket routes the signal the algorithm flagged to the coach who can act."
    },
    {
        "id": "adapt-console-threshold",
        "title": "Set the mastery threshold",
        "console": "generic-web",
        "domain_id": D,
        "difficulty": 1,
        "brief": "In the course settings, set the mastery threshold to 80 and submit.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set the 'mastery-threshold' field to 80.",
                "validate": {"action": "set-field", "params": {"id": "mastery-threshold", "value": "80"}},
                "hint": "Set field mastery-threshold to 80."
            },
            {
                "id": "t2",
                "instruction": "Submit the course settings form.",
                "validate": {"action": "submit-form", "params": {}},
                "hint": "Click submit on the settings form."
            }
        ],
        "debrief": "The mastery bar is a policy control: set it from pilot data, and it governs every advancement decision."
    },
    {
        "id": "adapt-console-curriculum",
        "title": "Organize the remediation module",
        "console": "linux-desktop",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Create the remediation module directory and lock its permissions.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create the directory /curriculum/remediation-binary.",
                "validate": {"action": "create-dir", "params": {"path": "/curriculum/remediation-binary"}},
                "hint": "Create directory /curriculum/remediation-binary."
            },
            {
                "id": "t2",
                "instruction": "Change /curriculum/remediation-binary permissions to 755.",
                "validate": {"action": "chmod", "params": {"path": "/curriculum/remediation-binary", "mode": "755"}},
                "hint": "Set mode 755 on /curriculum/remediation-binary."
            }
        ],
        "debrief": "Curriculum is infrastructure: organized, permissioned, and ready for the learners the engine routes to it."
    }
]

MISSIONS = [
    {
        "id": "adapt-mission-sort-scores",
        "title": "Sort the learner scores",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Sort the module scores to find the struggling learners.",
        "objectives": ["Sort scores.csv"],
        "checks": [
            {
                "command_pattern": "^sort\\s+scores\\.csv",
                "expect_contains": "58",
                "hint": "Type: sort scores.csv"
            }
        ],
        "success_message": "Scores sorted — the learners below mastery are visible."
    },
    {
        "id": "adapt-mission-grep-fail",
        "title": "Find the failed attempts",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Search the attempt log for failed mastery checks.",
        "objectives": ["Grep attempts.log for 'FAIL'"],
        "checks": [
            {
                "command_pattern": "^grep\\s+FAIL\\s+attempts\\.log",
                "expect_contains": "FAIL",
                "hint": "Type: grep FAIL attempts.log"
            }
        ],
        "success_message": "Failed attempts found — each one is a diagnosis waiting to happen."
    },
    {
        "id": "adapt-mission-head-leaderboard",
        "title": "Preview the progress board",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Preview the first lines of the learner progress file.",
        "objectives": ["Head progress.csv"],
        "checks": [
            {
                "command_pattern": "^head\\s+progress\\.csv",
                "expect_contains": "learner_id",
                "hint": "Type: head progress.csv"
            }
        ],
        "success_message": "Progress format confirmed — the engine's data is readable."
    },
    {
        "id": "adapt-mission-tail-session",
        "title": "Check the latest session entries",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Tail the session log to see the most recent learner activity.",
        "objectives": ["Tail session.log"],
        "checks": [
            {
                "command_pattern": "^tail\\s+session\\.log",
                "expect_contains": "attempt",
                "hint": "Type: tail session.log"
            }
        ],
        "success_message": "Latest sessions reviewed — activity is current."
    },
    {
        "id": "adapt-mission-count-attempts",
        "title": "Count the attempts",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Count how many mastery attempts were logged this week.",
        "objectives": ["Count lines in attempts.log with wc"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+attempts\\.log",
                "expect_contains": "attempts.log",
                "hint": "Type: wc -l attempts.log"
            }
        ],
        "success_message": "Attempt count captured — practice volume is quantified."
    },
    {
        "id": "adapt-mission-diff-test",
        "title": "Diff the test versions",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Compare the two parallel test forms to verify they are equivalent.",
        "objectives": ["Diff test-form-a.txt against test-form-b.txt"],
        "checks": [
            {
                "command_pattern": "^diff\\s+test-form-a\\.txt\\s+test-form-b\\.txt",
                "expect_contains": ">",
                "hint": "Type: diff test-form-a.txt test-form-b.txt"
            }
        ],
        "success_message": "Test forms compared — parallel forms verified."
    },
    {
        "id": "adapt-mission-read-map",
        "title": "Read the curriculum map",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Read the curriculum knowledge-space map to see prerequisite relationships.",
        "objectives": ["Cat curriculum-map.txt and confirm the prerequisite edge"],
        "checks": [
            {
                "command_pattern": "^cat\\s+curriculum-map\\.txt",
                "expect_contains": "prerequisite",
                "hint": "Type: cat curriculum-map.txt"
            }
        ],
        "success_message": "Curriculum map read — the prerequisite graph is visible."
    }
]

if __name__ == '__main__':
    merge('adaptive-foundations', sims=SIMS, consoles=CONSOLES, missions=MISSIONS)
