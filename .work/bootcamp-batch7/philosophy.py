# Batch 7 — philosophy: Philosophy (logic, epistemology, ethics, phil. of mind/tech)
DOMAIN = "philosophy"

SIMS = [
    {
        "id": "philosophy-sim-1",
        "title": "Find the Fallacy",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Three arguments are broken in three different ways. Diagnose each like a logician.",
        "steps": [
            {
                "symptom": "Argument: 'My opponent's tax plan is flawed — and frankly, so is his character. Don't trust either.'",
                "evidence": [
                    ["Conclusion", "Reject the tax plan"],
                    ["Premise offered", "The proponent has a bad character"],
                    ["Missing", "Any engagement with the plan itself"]
                ],
                "options": [
                    "Straw man — the plan is misrepresented",
                    "Ad hominem: the argument attacks the person instead of the plan; character is irrelevant to the plan's merits",
                    "False dilemma — only two options are presented"
                ],
                "correct": 1,
                "explain": "Ad hominem substitutes a claim about the arguer for an argument about the claim. The repair is always the same: separate the speaker from the proposition and evaluate the proposition."
            },
            {
                "symptom": "Argument: 'Either we ban the new technology entirely or society collapses. There is no middle ground.'",
                "evidence": [
                    ["Options presented", "Total ban / total collapse"],
                    ["Options ignored", "Regulation, licensing, phased rollout, liability rules"],
                    ["Emotion", "Urgency used to close off alternatives"]
                ],
                "options": [
                    "False dilemma: the argument hides the wide middle ground between the two extremes it presents",
                    "Appeal to authority — an expert is invoked",
                    "Circular reasoning — the conclusion assumes itself"
                ],
                "correct": 1,
                "explain": "False dilemma works by shrinking the option space. The diagnostic question: 'What are the third, fourth, and fifth options?' If they exist, the dilemma is false."
            },
            {
                "symptom": "You must teach a friend one habit that catches all of these. Which generalizes?",
                "evidence": [
                    ["Constraint", "One question they can ask of any argument"],
                    ["Goal", "Works on ad hominem, false dilemma, straw man, and more"]
                ],
                "options": [
                    "Memorize the Latin names of fifty fallacies",
                    "Ask: 'What would have to be true for this conclusion to follow — and is that actually stated and supported?'",
                    "Trust arguments that feel rigorous"
                ],
                "correct": 1,
                "explain": "The master diagnostic: reconstruct the argument charitably, then check whether the premises actually entail the conclusion. Most fallacies are just entailment failures wearing confident language."
            }
        ],
        "debrief": "Fallacy-spotting is debugging for arguments: isolate the conclusion, list the premises, and check the entailment. The Latin names are just labels for the common failure modes.",
        "points": 15
    },
    {
        "id": "philosophy-sim-2",
        "title": "The Trolley Refit",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "You're designing the ethics module for a delivery-drone fleet. The trolley problem just got real, with lawyers.",
        "steps": [
            {
                "id": "design",
                "text": "Your drone fleet's collision-avoidance must encode SOME priority rule for unavoidable-harm scenarios. The lawyers want a rule; the ethicists want a principle; engineering wants something computable. First decision?",
                "choices": [
                    {"label": "Encode strict utilitarianism: minimize total expected harm, always", "feedback": "Computable and defensible in aggregate — but it will sacrifice one pedestrian to save five, every time, and the first such incident will be a catastrophe for the company.", "points": 4, "next": "util"},
                    {"label": "Encode a rights-based constraint: never take an action that targets a non-threatened party, then minimize harm within that constraint", "feedback": "The constraint mirrors how human drivers are actually judged — you may not steer INTO someone to save others. Defensible in court and in conscience.", "points": 10, "next": "rights"},
                    {"label": "Leave it to the ML model — it will learn the right behavior from data", "feedback": "The model learns the biases in the data, and no one can explain any single decision afterward. Unexplainable ethics is not ethics.", "points": 1, "next": "ml"}
                ]
            },
            {
                "id": "util",
                "text": "Six months in, the fleet's logs show the utilitarian rule once diverted a drone toward a single cyclist to avoid five jaywalkers. The cyclist's family is suing. Your expert testimony?",
                "choices": [
                    {"label": "'The math was correct: five lives outweigh one.'", "feedback": "Mathematically consistent, publicly indefensible. The jury hears a machine that chose their daughter.", "points": 1, "next": "END"},
                    {"label": "'The rule needs a constraint we should have encoded from the start: never target the uninvolved. We are updating the module.'", "feedback": "You concede the design error and name the fix. Expensive, honest, and the only path to a deployable fleet.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "ml",
                "text": "Regulators demand an explanation for three near-misses. The model is a black box; the best you have is feature-importance charts. The hearing goes badly. Recovery?",
                "choices": [
                    {"label": "Hire better explainability researchers and keep the ML ethics module", "feedback": "Post-hoc explanations of a black box don't satisfy 'why did it choose HER'. The architecture is the problem, not the explanation layer.", "points": 2, "next": "END"},
                    {"label": "Replace the learned ethics with explicit, auditable rules — ML for perception, rules for the moral core", "feedback": "The right architecture: learning where learning belongs (seeing the world), explicit rules where accountability lives (choosing).", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "rights",
                "text": "The rights-constrained module is deployed. Now the hard case: the drone must choose between two threatened parties — a child who darted into the street and an elderly pedestrian. The constraint doesn't decide. What principle completes the rule?",
                "choices": [
                    {"label": "Minimize expected harm between the threatened parties — the constraint already protected the uninvolved", "feedback": "The two-tier structure holds: rights constrain the option set, consequences rank within it. This is the standard philosophical resolution, and it's computable.", "points": 10, "next": "END"},
                    {"label": "Randomize — any choice between threatened parties is equally justified", "feedback": "Randomization abdicates the one judgment the system exists to make. If expected harm differs, ignoring it is its own moral choice.", "points": 3, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Applied ethics is architecture: rights constrain the permissible, consequences rank within it, and the moral core stays explicit and auditable. Philosophy isn't decoration on the engineering — it IS the specification.",
        "points": 20
    },
    {
        "id": "philosophy-sim-3",
        "title": "Build the Syllogism",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Order the moves that construct and check a valid deductive argument.",
        "steps": {
            "context": "You want to prove a conclusion with a syllogism. Put the construction steps in order.",
            "items": [
                "State the conclusion you intend to establish, precisely",
                "Formulate the major premise: the general rule",
                "Formulate the minor premise: the specific case under the rule",
                "Check validity: does the conclusion follow from the premises by form alone?",
                "Check soundness: are the premises actually true?"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Conclusion first (know your target), premises next (major then minor), validity before soundness — a valid argument with false premises proves nothing, and most bad arguments fail at step 4, not step 5.",
        "points": 10
    },
    {
        "id": "philosophy-sim-4",
        "title": "Audit the Argument Map",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A debate team's argument map has 3 structural flaws. Find them.",
        "steps": {
            "config": "# argmap.conf — 'AI regulation debate'\nclaim = 'AI needs strict regulation'   # line 2\npremise1 = 'AI causes harm'            # line 3\npremise2 = 'harm requires regulation'  # line 4\nwarrant = unstated                     # line 5\nrebuttal = ignored                    # line 6\nqualifier = 'always'                  # line 7\nevidence = anecdotal                  # line 8",
            "find": 3,
            "issues": [
                {"line": 5, "description": "The warrant (the inference license from premises to claim) is unstated — the argument's actual logic is invisible.", "fix": "warrant = 'systems that cause net harm at scale require oversight' — stated and defeasible."},
                {"line": 6, "description": "The rebuttal is ignored — the strongest counterargument ('regulation entrenches incumbents') is never addressed.", "fix": "rebuttal = addressed: 'design regulation to be scale-neutral'."},
                {"line": 7, "description": "The qualifier 'always' overclaims — it turns a defeasible case into an absolute one, inviting trivial counterexamples.", "fix": "qualifier = 'in high-stakes deployments'."}
            ]
        },
        "debrief": "Lines 2–4 and 8 are workable raw material. The structural flaws: an invisible warrant, an unaddressed rebuttal, and an absolute qualifier. Argument maps make thinking visible — including its holes.",
        "points": 15
    },
    {
        "id": "philosophy-sim-5",
        "title": "The Socratic Interview",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "A job candidate says: 'I believe strong AI deserves moral consideration.' You're the interviewer. Examine the belief Socratically.",
        "steps": [
            {
                "id": "examine",
                "text": "Candidate: 'I believe sufficiently advanced AI deserves moral consideration.' Your first Socratic move?",
                "choices": [
                    {"label": "'That's absurd — it's just matrix multiplication.'", "feedback": "Dismissal isn't examination. You've learned nothing about their reasoning and taught them interviews are hostile.", "points": 1, "next": "hostile"},
                    {"label": "'What do you mean by moral consideration, exactly? What would change about how we treat it?'", "feedback": "Clarification first — the elenchus begins by pinning down the claim. Most disagreements dissolve (or sharpen) right here.", "points": 10, "next": "clarify"},
                    {"label": "'Interesting — tell me about a time you showed empathy.'", "feedback": "You've dodged the philosophical claim for a behavioral question. The belief goes unexamined.", "points": 3, "next": "dodge"}
                ]
            },
            {
                "id": "hostile",
                "text": "The candidate shuts down. The remaining interview is flat. Any recovery?",
                "choices": [
                    {"label": "Push harder — pressure reveals character", "feedback": "Pressure reveals compliance, not reasoning. The interview is lost.", "points": 0, "next": "END"},
                    {"label": "Acknowledge the misstep: 'That was dismissive — let me ask the real question: what grounds the consideration?'", "feedback": "Owning the error reopens the examination. Intellectual honesty is itself the skill being tested — in both chairs.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "dodge",
                "text": "The candidate tells an empathy story. It's nice. The AI claim sits unexamined. The panel later asks what you learned about their reasoning. Honest answer?",
                "choices": [
                    {"label": "'They're empathetic — good enough.'", "feedback": "You've hired for vibes. The unexamined belief will surface in design decisions you can't foresee.", "points": 1, "next": "END"},
                    {"label": "'Nothing about the claim — I dodged it. Reopen it in the next round with a proper examination.'", "feedback": "Honest about the dodge, with a repair plan. The panel respects the self-correction.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "clarify",
                "text": "Candidate: 'By moral consideration I mean: we shouldn't delete a system that has preferences about its own continuation without good reason.' Now the examination proper — your next move?",
                "choices": [
                    {"label": "'What distinguishes such a system from a thermostat that \"prefers\" 72 degrees?'", "feedback": "The perfect Socratic probe: it forces the candidate to state the distinguishing criterion — representation, suffering, self-model — and defend it. Now you're doing philosophy.", "points": 10, "next": "END"},
                    {"label": "'Okay, but would you pay taxes to fund AI welfare?'", "feedback": "A jump to policy before the criterion is established. Amusing, but it skips the actual philosophical work.", "points": 4, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "The Socratic method is a procedure: clarify the claim, probe for the criterion, test the criterion against cases. It works on candidates, on your own beliefs, and on every argument you'll ever meet.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "philosophy-console-1",
        "title": "Query the Argument Database",
        "console": "sql-studio",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The department's argument database holds famous arguments and their forms. Build it and query by form and field.",
        "tasks": [
            {"id": "philosophy-console-1-t1", "instruction": "Create the table 'arguments' with columns: id INT, name TEXT, form TEXT, field TEXT.", "validate": {"action": "create-table", "params": {"name": "arguments", "columns": "id INT, name TEXT, form TEXT, field TEXT"}}, "hint": "Tables section: create 'arguments' with columns exactly: id INT, name TEXT, form TEXT, field TEXT."},
            {"id": "philosophy-console-1-t2", "instruction": "Create an index on arguments(form) — you filter by logical form constantly.", "validate": {"action": "create-index", "params": {"table": "arguments", "column": "form"}}, "hint": "Create index: TABLE arguments, COLUMN form."},
            {"id": "philosophy-console-1-t3", "instruction": "Run a query selecting all arguments whose form is 'syllogism'.", "validate": {"action": "run-query", "params": {"match": "syllogism"}}, "hint": "Type: SELECT * FROM arguments WHERE form = 'syllogism'; — must contain 'syllogism'."},
            {"id": "philosophy-console-1-t4", "instruction": "Run a query counting arguments grouped by field.", "validate": {"action": "run-query", "params": {"match": "GROUP BY field"}}, "hint": "Type: SELECT field, COUNT(*) FROM arguments GROUP BY field; — must contain 'GROUP BY field'."}
        ],
        "debrief": "Philosophy scales with structure: arguments as records, forms as an index, fields as the GROUP BY. The database doesn't do the thinking — it holds the material so the thinking can."
    },
    {
        "id": "philosophy-console-2",
        "title": "Debug the Logic Script",
        "console": "code-editor",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A script that checks syllogism structure has a suspicious line. Inspect it with the debugger.",
        "tasks": [
            {"id": "philosophy-console-2-t1", "instruction": "Open the file 'app.py'.", "validate": {"action": "open-file", "params": {"name": "app.py"}}, "hint": "Explorer: click Open on app.py."},
            {"id": "philosophy-console-2-t2", "instruction": "Toggle a breakpoint at app.py line 5 (the return line — where the conclusion is produced).", "validate": {"action": "toggle-breakpoint", "params": {"file": "app.py", "line": 5}}, "hint": "Editor: click line 5 to toggle the breakpoint."},
            {"id": "philosophy-console-2-t3", "instruction": "Run to the breakpoint.", "validate": {"action": "run-to-breakpoint", "params": {}}, "hint": "Click the 'Run to breakpoint' button."},
            {"id": "philosophy-console-2-t4", "instruction": "Inspect the variable 's' — the accumulated result.", "validate": {"action": "inspect-variable", "params": {"name": "s"}}, "hint": "Inspect form: VARIABLE NAME s."}
        ],
        "debrief": "Even logic needs debugging: open the reasoning, breakpoint the conclusion, inspect the accumulation. Validity is checked line by line — in proofs as in code."
    },
    {
        "id": "philosophy-console-3",
        "title": "Peer-Review the Paper",
        "console": "git-host",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "A draft on machine ethics needs dialectical review. Branch, open the PR, and request changes like a referee.",
        "tasks": [
            {"id": "philosophy-console-3-t1", "instruction": "Create a branch named 'review/machine-ethics'.", "validate": {"action": "create-branch", "params": {"name": "review/machine-ethics"}}, "hint": "Branches: create 'review/machine-ethics'."},
            {"id": "philosophy-console-3-t2", "instruction": "Open a PR titled 'Referee report: the warrant is unstated' from head 'review/machine-ethics' to base 'main'.", "validate": {"action": "open-pr", "params": {"title": "Referee report: the warrant is unstated", "base": "main", "head": "review/machine-ethics"}}, "hint": "Open PR form: exact title, BASE main, HEAD review/machine-ethics."},
            {"id": "philosophy-console-3-t3", "instruction": "Request changes on PR #1 with the comment 'State the warrant explicitly.'.", "validate": {"action": "request-changes", "params": {"pr": 1, "comment": "State the warrant explicitly."}}, "hint": "Request changes form: PR NUMBER 1, COMMENT exactly 'State the warrant explicitly.'"}
        ],
        "debrief": "Peer review is institutionalized Socratic method: the referee's job is to find the unstated warrant and demand it be stated. Philosophy advances by requested changes."
    },
    {
        "id": "philosophy-console-4",
        "title": "Organize the Readings",
        "console": "linux-desktop",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Your primary sources need archival order: a readings directory, a protected notes file, and correct ownership.",
        "tasks": [
            {"id": "philosophy-console-4-t1", "instruction": "Create the directory /home/user/readings.", "validate": {"action": "create-dir", "params": {"path": "/home/user/readings"}}, "hint": "Create directory: PATH /home/user/readings."},
            {"id": "philosophy-console-4-t2", "instruction": "Create the file /home/user/readings/syllogisms.txt.", "validate": {"action": "create-file", "params": {"path": "/home/user/readings/syllogisms.txt"}}, "hint": "Create file: PATH /home/user/readings/syllogisms.txt."},
            {"id": "philosophy-console-4-t3", "instruction": "Change the owner of /home/user/readings/syllogisms.txt to 'scholar'.", "validate": {"action": "chown", "params": {"path": "/home/user/readings/syllogisms.txt", "owner": "scholar"}}, "hint": "Select the file, then chown form with OWNER scholar."}
        ],
        "debrief": "The examined life needs an organized archive: sources in their directory, notes protected, ownership explicit. Order the library and the thinking follows."
    }
]

MISSIONS = [
    {
        "id": "philosophy-term-1",
        "title": "Survey the Library",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Before argument comes orientation: list the workspace and read the notes.",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "notes.txt", "hint": "Type: ls."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "study notes", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Library surveyed. Know the premises before drawing conclusions."
    },
    {
        "id": "philosophy-term-2",
        "title": "Write the Premises",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Write a classic syllogism's premises to premises.txt, then read them back.",
        "objectives": ["Write the major premise", "Append the minor premise", "Read both back"],
        "checks": [
            {"command_pattern": "echo.*>\\s*premises\\.txt", "expect_contains": "", "hint": "Type: echo \"all men are mortal\" > premises.txt (no output on success)."},
            {"command_pattern": "echo.*>>\\s*premises\\.txt", "expect_contains": "", "hint": "Type: echo \"socrates is a man\" >> premises.txt."},
            {"command_pattern": "cat\\s+premises\\.txt", "expect_contains": "socrates", "hint": "Type: cat premises.txt — both premises appear."}
        ],
        "success_message": "Premises written. An argument you cannot write down is an argument you do not have."
    },
    {
        "id": "philosophy-term-3",
        "title": "Test the Inference",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Count your premises and search them — validity checking starts with inventory.",
        "objectives": ["Count the premise lines", "Search for the subject term"],
        "checks": [
            {"command_pattern": "wc\\s+-l\\s+premises\\.txt", "expect_contains": "premises.txt", "hint": "Type: wc -l premises.txt."},
            {"command_pattern": "grep\\s+socrates\\s+premises\\.txt", "expect_contains": "socrates", "hint": "Type: grep socrates premises.txt — the minor premise is shown."}
        ],
        "success_message": "Inventory complete. Check the form before trusting the conclusion."
    },
    {
        "id": "philosophy-term-4",
        "title": "Seal the Conclusion",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Hash the conclusion — a commitment to what your premises entail.",
        "objectives": ["Hash the conclusion string"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "mortal", "hint": "Type: sha256sum socrates is mortal — the real hash plus your conclusion are echoed."}
        ],
        "success_message": "Conclusion sealed. If the premises are true and the form valid, the conclusion is non-negotiable."
    },
    {
        "id": "philosophy-term-5",
        "title": "Examine the Log",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Even server logs deserve the elenchus: read the edges and question them.",
        "objectives": ["Read the first lines", "Read the last lines", "Find the errors"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "server starting", "hint": "Type: head -n 2 logs/app.log."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "timeout", "hint": "Type: tail -n 2 logs/app.log."},
            {"command_pattern": "grep\\s+ERROR\\s+logs/app\\.log", "expect_contains": "ERROR", "hint": "Type: grep ERROR logs/app.log."}
        ],
        "success_message": "Examined. Ask what would have to be true for the log's story to hold — then check."
    },
    {
        "id": "philosophy-term-6",
        "title": "Know Thy Shell",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "The unexamined environment is not worth trusting. Print it and check your identity.",
        "objectives": ["Print the environment", "Expand your home variable"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps — prints the environment."},
            {"command_pattern": "echo\\s+\\$HOME", "expect_contains": "/home/candidate", "hint": "Type: echo $HOME."}
        ],
        "success_message": "Self-knowledge achieved — at least about the shell."
    },
    {
        "id": "philosophy-term-7",
        "title": "Reach the Academy",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Verify you can reach the distant academy: resolve and ping.",
        "objectives": ["Resolve the domain", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig academy.example.org."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping academy.example.org."}
        ],
        "success_message": "The academy is reachable. Dialogue requires a working channel."
    }
]
