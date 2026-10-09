# Batch 7 — deep-work: Deep Work: Attention as a Technical Skill
DOMAIN = "deep-work"

SIMS = [
    {
        "id": "deep-work-sim-1",
        "title": "The Fragmented Afternoon",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Maya logged three hours of study, but her quiz score didn't move. Diagnose what actually happened in that session.",
        "steps": [
            {
                "symptom": "Maya studied distributed systems for three hours. Her practice-quiz score is identical to yesterday's.",
                "evidence": [
                    ["Phone unlock log", "11 unlocks between 14:02 and 16:58"],
                    ["Messages answered", "4 chat threads, average reply latency 3 minutes"],
                    ["Self report", "\"I was studying the whole time, I swear.\""]
                ],
                "options": [
                    "She didn't try hard enough — the fix is more willpower",
                    "Attention residue: every switch left part of her mind on the previous task, so each fragment ran on a fraction of her attention",
                    "Distributed systems is simply too hard to learn in an afternoon"
                ],
                "correct": 1,
                "explain": "Attention residue is the mechanism: the brain doesn't instantly reallocate. Eleven switches means eleven partial minds, none of them fully on Raft consensus."
            },
            {
                "symptom": "Maya says the afternoon 'felt busy and productive' despite zero measurable progress.",
                "evidence": [
                    ["Activity trace", "23 app switches, 0 commits, 0 notes written"],
                    ["Feeling log", "\"I was juggling a lot — it felt like real work.\""]
                ],
                "options": [
                    "Busyness is a reliable proxy for depth — she probably did learn something",
                    "Shallow work feels productive because motion is visible; depth is invisible until tested",
                    "She should study longer hours to compensate"
                ],
                "correct": 1,
                "explain": "Shallow work is logistical, interruptible, and easy to replicate — and it mimics the feeling of work. The test score is the honest instrument, not the feeling."
            },
            {
                "symptom": "Maya wants tomorrow to be different. Which intervention actually changes the structure of the session?",
                "evidence": [
                    ["Constraint", "She has the same phone, same roommates, same chatty team"],
                    ["Goal", "One 90-minute block on consensus algorithms, quiz score +20%"]
                ],
                "options": [
                    "Promise herself she'll 'really focus this time'",
                    "Time-block the 90 minutes, phone in another room, single target written down, shutdown ritual at the end",
                    "Study the same material but take more detailed notes"
                ],
                "correct": 1,
                "explain": "Structure beats intention. Fixed-schedule productivity plus environment design — phone physically elsewhere, one target, a defined stop — is the system that makes depth the default."
            }
        ],
        "debrief": "Honest measurement (quiz scores, not hours logged) plus structural fixes (phone away, single target, time block) turn study time into actual skill. Attention is the bottleneck — train it like one.",
        "points": 15
    },
    {
        "id": "deep-work-sim-2",
        "title": "The Shutdown Ritual",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "It's 5:40 PM. Your deep block ended at 5:00 but the inbox is still pinging. Run the end of the day like a professional.",
        "steps": [
            {
                "id": "start",
                "text": "5:40 PM. Your planned stop time was 5:00. Three unread messages glow in the corner of your screen, and part of your brain is still chewing on the consensus bug. What do you do?",
                "choices": [
                    {"label": "Answer 'just one more email' — it'll only take five minutes", "feedback": "Forty minutes later you're still in the inbox. The shutdown never happened, and the bug follows you to dinner.", "points": 0, "next": "leak"},
                    {"label": "Run the shutdown ritual: capture open loops, review tomorrow's block, say the day is done", "feedback": "You write down the bug's current state, block 9:00–10:30 tomorrow for it, and close the laptop. The ritual tells your brain the workday is over.", "points": 10, "next": "ritual"},
                    {"label": "Close the laptop abruptly and doomscroll on the couch", "feedback": "The laptop is closed but the loops are open — you'll ruminate all evening. Shutdown is a procedure, not a lid position.", "points": 2, "next": "leak"}
                ]
            },
            {
                "id": "leak",
                "text": "8:15 PM. You're on the couch and the consensus bug pops into your head again, uninvited. Tomorrow's 9 AM block has no defined target. What's the repair?",
                "choices": [
                    {"label": "Do a 5-minute capture now: write the bug state and tomorrow's single target on paper", "feedback": "A late, partial ritual still beats none — the loop closes enough for sleep, and tomorrow has a target.", "points": 6, "next": "END"},
                    {"label": "Open the laptop 'just to jot it down' — and check the inbox while you're there", "feedback": "The inbox reopens the loops you were trying to close. Tomorrow starts already fragmented.", "points": 0, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "ritual",
                "text": "Shutdown complete: open loops captured, tomorrow's 9:00–10:30 block has one target (fix the Raft election timeout). Your phone buzzes — a teammate asking for 'a quick review tonight'. What now?",
                "choices": [
                    {"label": "Reply: 'I'll review it in my 11:00 shallow block tomorrow — send the link'", "feedback": "Fixed-schedule productivity in action: the constraint forces the work into its proper shallow slot instead of eating your evening.", "points": 10, "next": "END"},
                    {"label": "Do the review now to be a team player", "feedback": "One exception becomes the precedent. Tomorrow's deep block starts with residue from tonight.", "points": 2, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "A shutdown ritual is how you make the workday actually end: capture every open loop, assign tomorrow's deep block a single target, and let the constraint protect your evening. Recovery is part of depth.",
        "points": 20
    },
    {
        "id": "deep-work-sim-3",
        "title": "Build the Deep Block",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Put the five moves of a proper 90-minute deep-work block in the order a professional runs them.",
        "steps": {
            "context": "You have 90 unscheduled minutes and one hard problem. Order the moves that turn those minutes into a real deep block.",
            "items": [
                "Write down the single target for the block — one sentence",
                "Clear the environment: phone in another room, tabs closed, notifications off",
                "Set a visible timer for 90 minutes and start it",
                "Work the single target with no switching until the timer ends",
                "Log what you produced and where you stopped, then shut down"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Target first, environment second, timer third — the block is a container you prepare before you enter. Logging at the end makes tomorrow's start instant instead of a 20-minute warm-up.",
        "points": 10
    },
    {
        "id": "deep-work-sim-4",
        "title": "Attention Environment Audit",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A junior engineer shows you their 'focus setup'. Find the 3 attention leaks hiding in this configuration.",
        "steps": {
            "config": "# focus.conf — 'my deep work setup'\nphone_notifications = ON          # line 2\nphone_location = desk, face-up   # line 3\nchat_client = open, all channels unmuted  # line 4\ntimer = none                    # line 5\nblock_target = 'whatever feels important'  # line 6\ndoor = closed                   # line 7\nmusic = lo-fi playlist, lyrics-free       # line 8",
            "find": 3,
            "issues": [
                {"line": 2, "description": "Phone notifications are ON — every buzz is a task-switch that leaves attention residue.", "fix": "phone_notifications = OFF during deep blocks (or phone in another room)."},
                {"line": 3, "description": "Phone on the desk face-up — mere presence of the phone degrades available cognitive capacity.", "fix": "phone_location = other room."},
                {"line": 4, "description": "Chat client open with all channels unmuted — an always-on interruption firehose.", "fix": "chat_client = closed during deep blocks; check in batched shallow slots."}
            ]
        },
        "debrief": "Environment design beats willpower: notifications off, phone physically elsewhere, chat closed. Note lines 5–6 are also weak (no timer, vague target) but the three flagged lines are the active leaks.",
        "points": 15
    },
    {
        "id": "deep-work-sim-5",
        "title": "The Interruption Storm",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "You're 40 minutes into a deep block on a hard proof when your manager Slacks: 'quick call?'. Navigate the next ten minutes without losing the block.",
        "steps": [
            {
                "id": "ping",
                "text": "40 minutes into the block. The proof is finally yielding. Slack: your manager — 'quick call?'. The message preview alone has already cost you some focus. What's the move?",
                "choices": [
                    {"label": "Reply instantly and jump on the call — managers outrank blocks", "feedback": "The block is destroyed. Whatever the call was, it could have waited 50 minutes — and now the proof's state has to be rebuilt from scratch.", "points": 0, "next": "rubble"},
                    {"label": "Don't look. Finish the block, then reply in your next shallow slot", "feedback": "You protect the remaining 50 minutes. If it were truly urgent, they'd call — Slack is by design non-urgent.", "points": 10, "next": "defend"},
                    {"label": "Glance at the message to 'triage' whether it's urgent", "feedback": "Triage IS the interruption — reading it loads their context into your working memory. Attention residue begins at the preview.", "points": 3, "next": "rubble"}
                ]
            },
            {
                "id": "rubble",
                "text": "The block is gone — you're context-switched and the proof's thread is lost. Damage control: what salvages the day?",
                "choices": [
                    {"label": "Log exactly where you stopped, then handle the interruption fully", "feedback": "The log preserves the state; tomorrow's restart costs minutes instead of an hour. Partial credit for professional wreckage management.", "points": 5, "next": "END"},
                    {"label": "Try to 'quickly get back into it' between Slack replies", "feedback": "Multitasking the recovery guarantees neither the proof nor the replies get a full mind. The residue compounds.", "points": 0, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "defend",
                "text": "Block complete — proof sketched, state logged. You open Slack: the manager's 'quick call' was a question your teammate already answered in-thread. Now you reply. What does the reply teach?",
                "choices": [
                    {"label": "'Saw this after my focus block — glad it's resolved. For urgent things, call me; Slack waits until my shallow slots.'", "feedback": "You train the organization: urgent = call, everything else = batched. Each defended block makes the next one easier to defend.", "points": 10, "next": "END"},
                    {"label": "Say nothing about the delay — just answer normally", "feedback": "The block survived, but nobody learned the protocol. Next week the same ping arrives at minute 40 again.", "points": 5, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Defending a block is a skill with two halves: the in-the-moment refusal to triage (triage is the interruption), and the after-action protocol you teach others. Urgent things arrive by phone; everything else waits for shallow time.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "deep-work-console-1",
        "title": "Lock Down the Focus Environment",
        "console": "linux-desktop",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Your attention environment is a system you administer. Create the focus directory, add a blocklist file, and lock its permissions down.",
        "tasks": [
            {"id": "deep-work-console-1-t1", "instruction": "Create the directory /home/user/focus — this is where deep-block artifacts live.", "validate": {"action": "create-dir", "params": {"path": "/home/user/focus"}}, "hint": "Use the 'Create directory' form with PATH set to /home/user/focus."},
            {"id": "deep-work-console-1-t2", "instruction": "Create the file /home/user/focus/blocklist.txt — your personal list of attention thieves to keep closed during blocks.", "validate": {"action": "create-file", "params": {"path": "/home/user/focus/blocklist.txt"}}, "hint": "Use the 'Create file' form with PATH set to /home/user/focus/blocklist.txt."},
            {"id": "deep-work-console-1-t3", "instruction": "Set mode 600 on /home/user/focus/blocklist.txt — your blocklist is yours alone.", "validate": {"action": "chmod", "params": {"path": "/home/user/focus/blocklist.txt", "mode": "600"}}, "hint": "Select the blocklist.txt row, then use the chmod form with mode 600."}
        ],
        "debrief": "Environment design is administration: dedicated directories for deep work, explicit blocklists, tight permissions. You don't negotiate with distractions mid-block — you configure them out beforehand."
    },
    {
        "id": "deep-work-console-2",
        "title": "Triage the Interruption Queue",
        "console": "ticketing",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Every interruption is an incident. Run the queue like an on-call engineer: log it, assign it, move it — don't just absorb it.",
        "tasks": [
            {"id": "deep-work-console-2-t1", "instruction": "Create a P2 ticket titled 'Phone buzzed 11 times during deep block' — interruptions get logged, not suffered silently.", "validate": {"action": "create-ticket", "params": {"title": "Phone buzzed 11 times during deep block", "priority": "P2"}}, "hint": "Use the 'New ticket' section: TITLE exactly as given, PRIORITY P2."},
            {"id": "deep-work-console-2-t2", "instruction": "Assign ticket INC-9001 to 'maya' — the pre-seeded VPN ticket is hers to drive.", "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "maya"}}, "hint": "Use the Assign form with TICKET ID INC-9001 and ASSIGNEE maya."},
            {"id": "deep-work-console-2-t3", "instruction": "Move INC-9001 to 'in-progress' — batched shallow work starts now, not during the next deep block.", "validate": {"action": "update-status", "params": {"id": "INC-9001", "status": "in-progress"}}, "hint": "Use the 'Update status' form: INC-9001 → in-progress."}
        ],
        "debrief": "Logging interruptions as tickets does two things: it keeps them out of your working memory during deep blocks, and it gives you data — which interruptions recur, and which deserve a structural fix."
    },
    {
        "id": "deep-work-console-3",
        "title": "Ship the Daily Deep Block",
        "console": "cicd-pipeline",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Treat your study system like a pipeline: trigger the day's build, fix the failing stage, approve the release of your notes.",
        "tasks": [
            {"id": "deep-work-console-3-t1", "instruction": "Trigger a new build — this starts today's deep-work run with build and test green, deploy gated.", "validate": {"action": "trigger-build", "params": {}}, "hint": "Click the 'Trigger new build' button in the Pipeline section."},
            {"id": "deep-work-console-3-t2", "instruction": "The 'test' stage is failing (your recall check flopped). Retry the test stage.", "validate": {"action": "retry-stage", "params": {"stage": "test"}}, "hint": "Click Retry next to the test stage."},
            {"id": "deep-work-console-3-t3", "instruction": "Set the pipeline variable FOCUS_HOURS to 4 — declare today's depth budget explicitly.", "validate": {"action": "set-variable", "params": {"key": "FOCUS_HOURS", "value": "4"}}, "hint": "Go to the Variables section and set KEY=FOCUS_HOURS, VALUE=4."},
            {"id": "deep-work-console-3-t4", "instruction": "Approve the gated 'deploy' stage — ship today's notes and log the session.", "validate": {"action": "approve-stage", "params": {"stage": "deploy"}}, "hint": "Click Approve next to the deploy stage."}
        ],
        "debrief": "A pipeline makes the abstract concrete: trigger (start the block), retry (re-drill what failed), variables (declare the budget), approve (publish the output). Systems beat intentions."
    },
    {
        "id": "deep-work-console-4",
        "title": "Configure the Focus Dashboard",
        "console": "generic-web",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Set up the dashboard that tracks your deep-work practice: name it, set your timezone, and submit.",
        "tasks": [
            {"id": "deep-work-console-4-t1", "instruction": "Set the site_name field to 'Deep Work HQ'.", "validate": {"action": "set-field", "params": {"id": "site_name", "value": "Deep Work HQ"}}, "hint": "Use the 'Set site name' form with VALUE 'Deep Work HQ'."},
            {"id": "deep-work-console-4-t2", "instruction": "Set the timezone field to 'America/New_York' so your block schedule renders correctly.", "validate": {"action": "set-field", "params": {"id": "timezone", "value": "America/New_York"}}, "hint": "Use the 'Set timezone' form with VALUE 'America/New_York'."},
            {"id": "deep-work-console-4-t3", "instruction": "Submit the settings form to save your dashboard configuration.", "validate": {"action": "submit-form", "params": {}}, "hint": "Click the 'Submit settings' button."}
        ],
        "debrief": "What gets configured gets measured. A named dashboard in the right timezone is the home base your daily shutdown ritual reports to."
    }
]

MISSIONS = [
    {
        "id": "deep-work-term-1",
        "title": "Survey the Workspace",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Before a deep block, orient: list the workspace and read the study notes already waiting there.",
        "objectives": ["List the files in the practice workspace", "Read the study notes file to see what's already documented"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "notes.txt", "hint": "Type: ls — the workspace listing includes notes.txt."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "Linux essentials", "hint": "Type: cat notes.txt — the notes open with 'Linux essentials'."}
        ],
        "success_message": "Workspace surveyed. Orientation is the cheapest part of a deep block — never skip it."
    },
    {
        "id": "deep-work-term-2",
        "title": "Start the Attention Log",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Honest measurement starts with a log. Create attention.txt and record today's deep-block entries.",
        "objectives": ["Create attention.txt with your first deep-block entry", "Append a second entry marking a completed block"],
        "checks": [
            {"command_pattern": "echo.*>\\s*attention\\.txt", "expect_contains": "", "hint": "Type: echo \"block 1: 90 min consensus\" > attention.txt (output is empty on success — that's normal)."},
            {"command_pattern": "echo.*>>\\s*attention\\.txt", "expect_contains": "", "hint": "Type: echo \"block 2: 60 min raft log\" >> attention.txt to append a second line."},
            {"command_pattern": "cat\\s+attention\\.txt", "expect_contains": "block 1", "hint": "Type: cat attention.txt to verify both entries are logged."}
        ],
        "success_message": "Attention log started. What gets logged gets managed — this file is now your honest instrument."
    },
    {
        "id": "deep-work-term-3",
        "title": "Count the Switches",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Add three DISTRACTION lines to your attention log, then measure: how many lines, and how many were distractions?",
        "objectives": ["Append three DISTRACTION entries to attention.txt", "Count total lines in the log", "Search the log for DISTRACTION entries"],
        "checks": [
            {"command_pattern": "echo.*DISTRACTION.*>>\\s*attention\\.txt", "expect_contains": "", "hint": "Append a distraction, e.g.: echo \"DISTRACTION: checked phone\" >> attention.txt — do it three times (once is enough to tick this check)."},
            {"command_pattern": "wc\\s+.*attention\\.txt", "expect_contains": "attention.txt", "hint": "Type: wc -l attention.txt — the output ends with the filename."},
            {"command_pattern": "grep\\s+DISTRACTION\\s+attention\\.txt", "expect_contains": "DISTRACTION", "hint": "Type: grep DISTRACTION attention.txt to list every distraction line."}
        ],
        "success_message": "Measured. The ratio of deep lines to DISTRACTION lines is the score that matters — hours logged mean nothing next to it."
    },
    {
        "id": "deep-work-term-4",
        "title": "Read the Edges",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Review sessions start at the edges: the first lines set the intention, the last lines show where you stopped.",
        "objectives": ["Read the first two lines of attention.txt", "Read the last line of attention.txt"],
        "checks": [
            {"command_pattern": "head\\s+.*attention\\.txt", "expect_contains": "block 1", "hint": "Type: head -n 2 attention.txt — the first entries appear."},
            {"command_pattern": "tail\\s+.*attention\\.txt", "expect_contains": "DISTRACTION", "hint": "Type: tail -n 3 attention.txt — your latest entries (including distractions) appear."}
        ],
        "success_message": "Edges read. Every shutdown ritual ends by reading where you stopped — tomorrow's start is already written."
    },
    {
        "id": "deep-work-term-5",
        "title": "Seal the Daily Goal",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Write tomorrow's single target as a hash commitment — a tamper-evident seal on your intention.",
        "objectives": ["Hash your daily goal string with sha256sum", "Verify the goal text appears in the hash output"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "finish chapter 4", "hint": "Type: sha256sum finish chapter 4 — the output echoes your goal text after the real hash."}
        ],
        "success_message": "Goal sealed. A commitment you can verify beats a resolution you can quietly rewrite."
    },
    {
        "id": "deep-work-term-6",
        "title": "Check the Environment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "A deep block needs a clean environment. Verify who you are, where you are, and what home is set to.",
        "objectives": ["Confirm your shell identity and environment", "Print your home directory from the environment"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps — in this sandbox it prints your environment, including USER=candidate."},
            {"command_pattern": "echo\\s+\\$HOME", "expect_contains": "/home/candidate", "hint": "Type: echo $HOME — the shell expands it to /home/candidate."}
        ],
        "success_message": "Environment verified. Professionals check the runway before takeoff — even a mental one."
    },
    {
        "id": "deep-work-term-7",
        "title": "Verify Reachability",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Before a block that needs the network (docs, repos), confirm DNS resolves and the path is clean.",
        "objectives": ["Resolve a hostname with dig", "Confirm zero packet loss with ping"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig interstitiumlabs.dev — the ANSWER SECTION shows the resolved address."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping interstitium — the summary reports 0% packet loss."}
        ],
        "success_message": "Network verified. Eliminate the environment as a variable before you blame your focus."
    }
]
