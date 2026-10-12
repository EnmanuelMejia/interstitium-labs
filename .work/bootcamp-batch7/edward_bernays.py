# Batch 7 — edward-bernays: Bernays & Public Relations
DOMAIN = "edward-bernays"

SIMS = [
    {
        "id": "edward-bernays-sim-1",
        "title": "Name the Technique",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "A 1929 soap advertisement is doing several things at once. Diagnose which persuasion technique is doing the heavy lifting.",
        "steps": [
            {
                "symptom": "An ad shows a famous surgeon holding a bar of soap. No medical claim is made — just the surgeon's face, the soap, and the word 'Purity'.",
                "evidence": [
                    ["Copy", "\"Purity — the choice of those who know.\""],
                    ["Imagery", "Surgeon in white coat, hospital corridor backdrop"],
                    ["Disclosure", "None — the surgeon is a paid endorser, unstated"]
                ],
                "options": [
                    "Plain-folks appeal — the ad is positioning soap as ordinary",
                    "Transfer / prestige association: the surgeon's authority is transferred to the soap without any logical connection",
                    "Bandwagon — the ad claims everyone already buys it"
                ],
                "correct": 1,
                "explain": "Transfer moves prestige from one symbol (the surgeon) to an unrelated product. The defense is the same every time: ask what the authority actually knows about the product."
            },
            {
                "symptom": "A campaign leaflet repeats one phrase — 'the people's choice' — on every page, in every speech, for six months.",
                "evidence": [
                    ["Frequency", "Phrase appears 40+ times across materials"],
                    ["Evidence offered", "None — repetition stands in for proof"],
                    ["Effect noted", "Voters begin repeating it unprompted"]
                ],
                "options": [
                    "Card stacking — selective facts are being arranged",
                    "The illusory truth effect via relentless repetition: repeated statements feel truer regardless of evidence",
                    "Glittering generality — vague virtue words are doing the work"
                ],
                "correct": 1,
                "explain": "Repetition manufactures familiarity, and familiarity is misread as truth. Bernays understood this as engineering: say it everywhere, and the public finishes the argument for you."
            },
            {
                "symptom": "You must brief a community group on defending themselves. Which defense generalizes across all these techniques?",
                "evidence": [
                    ["Constraint", "One habit they can actually practice daily"],
                    ["Goal", "Works against transfer, repetition, and card stacking alike"]
                ],
                "options": [
                    "Memorize a list of every known propaganda technique",
                    "Source-checking habit: who benefits, what evidence is shown vs. implied, and what the authority actually knows",
                    "Avoid all advertising and political messaging entirely"
                ],
                "correct": 1,
                "explain": "Media literacy is a procedure, not a blacklist: who benefits, what's evidenced versus implied, and whether the invoked authority has relevant knowledge. That one habit answers every technique."
            }
        ],
        "debrief": "Propaganda analysis is diagnostic work: name the technique, trace what it substitutes for evidence, then install the counter-habit. Bernays engineered consent; the defense is engineered skepticism.",
        "points": 15
    },
    {
        "id": "edward-bernays-sim-2",
        "title": "The Press Agent's Dilemma",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "It's 1924. A tobacco client wants you to make smoking fashionable for women. Your press-agent skills are in demand — your conscience is not consulted. Decide.",
        "steps": [
            {
                "id": "brief",
                "text": "1924. The client: 'Make cigarettes respectable for women. Budget is unlimited.' You know the health evidence is thin but the paycheck is enormous. Your first move?",
                "choices": [
                    {"label": "Take the account and plan the 'Torches of Freedom' style stunt — emotion over evidence", "feedback": "You stage a parade where debutantes light up as symbols of emancipation. It works brilliantly — and you have engineered consent for a product you privately doubt.", "points": 2, "next": "success"},
                    {"label": "Take the account but insist on factual, non-manipulative copy", "feedback": "The client smiles and hires someone else who won't insist. The campaign happens anyway, without you.", "points": 5, "next": "sidelines"},
                    {"label": "Decline the account and document why — then study the techniques from the outside", "feedback": "You lose the fee but keep the clear view. From the sidelines you can see the whole machine: third-party authorities, staged events, manufactured news.", "points": 10, "next": "analyst"}
                ]
            },
            {
                "id": "success",
                "text": "The stunt makes front pages nationwide. Sales surge. A journalist asks you point-blank: 'Was this news, or advertising?' How do you answer?",
                "choices": [
                    {"label": "'It was a genuine expression of women's liberation.'", "feedback": "The lie compounds. You have now manufactured both the event and its meaning — the full Bernays playbook, and its full moral cost.", "points": 0, "next": "END"},
                    {"label": "'It was a publicity event we organized.'", "feedback": "Honesty after the fact doesn't unring the bell, but it stops the next deception. Rare — and noted.", "points": 4, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "sidelines",
                "text": "From the sidelines you watch the campaign roll out: planted experts, staged 'news', repetition. A newspaper editor asks you to explain how it works — on the record. What do you do?",
                "choices": [
                    {"label": "Explain the machinery publicly — third-party technique, event staging, repetition", "feedback": "You convert inside knowledge into public defense. The editor runs the exposé; readers learn to ask who staged the 'news'.", "points": 10, "next": "END"},
                    {"label": "Stay quiet — the industry is small and you may want back in", "feedback": "Silence is a choice with a price: the machine runs unopposed, and you watched it happen.", "points": 2, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "analyst",
                "text": "As an outside analyst you catalog the campaign's anatomy: the third-party authorities, the staged event, the repetition cycle. A university asks you to teach media literacy. What's the core lesson?",
                "choices": [
                    {"label": "'Every message is manipulation — trust nothing.'", "feedback": "Cynicism is not literacy; it leaves students defenseless against the next well-made lie, because they've stopped evaluating.", "points": 4, "next": "END"},
                    {"label": "'Ask who staged it, who benefits, and what evidence would change your mind.'", "feedback": "You teach the procedure, not the paranoia. Students leave able to dissect any campaign — including the ones they'll meet tomorrow.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "The historical record is the textbook: third-party authorities, staged events, repetition. Studying the engineering of consent from the analyst's chair — and teaching the counter-procedure — is the independent-study payoff.",
        "points": 20
    },
    {
        "id": "edward-bernays-sim-3",
        "title": "Anatomy of a Campaign",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Order the five stages of a classic Bernays-style public relations campaign, from research to reinforcement.",
        "steps": {
            "context": "A 1920s-style campaign to shift public opinion. Put the stages in the order the engineering actually runs.",
            "items": [
                "Research the public's existing desires, fears, and group leaders",
                "Recruit third-party authorities to carry the message credibly",
                "Stage a newsworthy event that dramatizes the message",
                "Amplify coverage through repetition across every channel",
                "Reinforce: fold the new attitude into identity ('people like us do this')"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "Research first (find the latent desire), authority second (borrow credibility), event third (manufacture news), repetition fourth (make it feel true), identity last (make it feel like self). Recognizing the sequence is the first step to interrupting it.",
        "points": 10
    },
    {
        "id": "edward-bernays-sim-4",
        "title": "Feed Audit: Find the Manipulation",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A 'neutral' news aggregator's ranking config is doing persuasion work. Find the 3 manipulative settings.",
        "steps": {
            "config": "# ranker.conf — 'neutral news aggregator'\nboost_paid_placement = 3.0        # line 2\nlabel_sponsored = false         # line 3\noutrage_weight = 2.5            # line 4\nrecency_decay = normal          # line 5\ndiversity_penalty = 1.8         # line 6\nfact_check_badge = enabled      # line 7\nengagement_loop = infinite      # line 8",
            "find": 3,
            "issues": [
                {"line": 2, "description": "Paid placement boosted 3x — advertisers buy the top of your 'neutral' feed.", "fix": "boost_paid_placement = 1.0, or remove paid content from the news ranking entirely."},
                {"line": 3, "description": "Sponsored labels disabled — paid persuasion is presented as organic news.", "fix": "label_sponsored = true, always."},
                {"line": 4, "description": "Outrage weighted 2.5x — the algorithm amplifies whatever angers you most, the oldest manipulation trick in the book, now automated.", "fix": "outrage_weight = 1.0; rank by relevance and recency, not anger."}
            ]
        },
        "debrief": "Bernays needed press agents; the modern machine needs only a config file. Lines 5–7 are defensible (recency, diversity, fact-check badges); the three flagged lines are consent engineering running as code.",
        "points": 15
    },
    {
        "id": "edward-bernays-sim-5",
        "title": "Amplify or Expose",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "A viral video is moving markets. Your 200k-follower account can amplify it — or dissect it. The video's claims are unverified.",
        "steps": [
            {
                "id": "viral",
                "text": "A slick 90-second video claims a household product causes illness. 2M views in 6 hours. The 'expert' is unnamed, the study uncited. Your followers are asking what you think. First move?",
                "choices": [
                    {"label": "Share it with 'THIS IS HUGE' — engagement will be massive", "feedback": "You become a node in the amplification network. If the claims are false, you've laundered them with your credibility.", "points": 0, "next": "amplified"},
                    {"label": "Post a thread dissecting it: unnamed expert, uncited study, emotional editing", "feedback": "You apply the procedure publicly — who benefits, what's evidenced vs. implied. Some followers call you a shill; most learn the method.", "points": 10, "next": "dissect"},
                    {"label": "Wait 24 hours before saying anything", "feedback": "Patience is a legitimate tactic — but silence while it spreads is also a position. The window for inoculation narrows hourly.", "points": 5, "next": "dissect"}
                ]
            },
            {
                "id": "amplified",
                "text": "Your share added 400k views. A fact-checker now confirms the video's core claim is false — and traces its funding to a competitor of the product. Damage control?",
                "choices": [
                    {"label": "Delete quietly and move on", "feedback": "The correction never reaches the 400k. Quiet deletion protects you, not the people you misled.", "points": 1, "next": "END"},
                    {"label": "Post a full correction: what you shared, why it was wrong, who funded it — with the same energy as the original share", "feedback": "Corrections rarely travel as far, but a loud, honest one is the only ethical move. You've learned the amplifier's responsibility the hard way.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "dissect",
                "text": "Your thread goes modestly viral itself. A PR firm emails: 'We represent the video's creators. We'd like to discuss a partnership.' What's behind the curtain?",
                "choices": [
                    {"label": "Take the meeting — hear them out", "feedback": "The meeting is the recruitment attempt: today's third-party technique is the 'independent creator partnership'. You walk in knowing exactly what it is.", "points": 6, "next": "END"},
                    {"label": "Publish the email with analysis: this is how modern third-party recruitment works", "feedback": "You turn the recruitment attempt into the lesson. Your followers watch a Bernays technique arrive in real time — and recognize it.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "The machinery Bernays built now runs at internet speed: virality replaces the parade, creators replace the debutantes. The defense hasn't changed — evidence, sources, beneficiaries — but it has to run just as fast.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "edward-bernays-console-1",
        "title": "Query the Media Archive",
        "console": "sql-studio",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The archive holds a century of campaigns. Build the table, then query it the way an analyst would: who ran what, and who benefited?",
        "tasks": [
            {"id": "edward-bernays-console-1-t1", "instruction": "Create the table 'campaigns' with columns: id INT, year INT, sponsor TEXT, technique TEXT.", "validate": {"action": "create-table", "params": {"name": "campaigns", "columns": "id INT, year INT, sponsor TEXT, technique TEXT"}}, "hint": "In the Tables section, create table 'campaigns' with columns exactly: id INT, year INT, sponsor TEXT, technique TEXT."},
            {"id": "edward-bernays-console-1-t2", "instruction": "Create an index on campaigns(year) — analysts always filter by era.", "validate": {"action": "create-index", "params": {"table": "campaigns", "column": "year"}}, "hint": "Use the 'Create index' form: TABLE campaigns, COLUMN year."},
            {"id": "edward-bernays-console-1-t3", "instruction": "Run a query that selects everything from campaigns where the technique is 'third-party'.", "validate": {"action": "run-query", "params": {"match": "third-party"}}, "hint": "In the Query editor type e.g.: SELECT * FROM campaigns WHERE technique = 'third-party'; — it must contain the text third-party."},
            {"id": "edward-bernays-console-1-t4", "instruction": "Run a query counting campaigns grouped by sponsor — follow the money.", "validate": {"action": "run-query", "params": {"match": "GROUP BY sponsor"}}, "hint": "Type: SELECT sponsor, COUNT(*) FROM campaigns GROUP BY sponsor; — it must contain 'GROUP BY sponsor'."}
        ],
        "debrief": "Archive work is database work: structure the campaigns, index by era, then query by technique and sponsor. 'Who benefits?' is a GROUP BY question."
    },
    {
        "id": "edward-bernays-console-2",
        "title": "Review the History Draft",
        "console": "git-host",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "A colleague's draft on the 1929 campaign needs peer review. Run the editorial workflow: branch, PR, review, merge.",
        "tasks": [
            {"id": "edward-bernays-console-2-t1", "instruction": "Create a branch named 'factcheck/1929-sources' for your review work.", "validate": {"action": "create-branch", "params": {"name": "factcheck/1929-sources"}}, "hint": "In the Branches section, create branch 'factcheck/1929-sources'."},
            {"id": "edward-bernays-console-2-t2", "instruction": "Open a pull request titled 'Verify 1929 parade sources' from head 'factcheck/1929-sources' to base 'main'.", "validate": {"action": "open-pr", "params": {"title": "Verify 1929 parade sources", "base": "main", "head": "factcheck/1929-sources"}}, "hint": "Use the 'Open pull request' form with the exact title, BASE main, HEAD factcheck/1929-sources."},
            {"id": "edward-bernays-console-2-t3", "instruction": "Approve PR #1 — the pre-seeded health-check PR is unrelated to your review, but the queue needs clearing.", "validate": {"action": "approve-pr", "params": {"pr": 1}}, "hint": "Click Approve on PR #1, or use the review buttons in the Pull requests section."}
        ],
        "debrief": "Historical claims deserve the same review rigor as code: branch the inquiry, document it as a PR, get a second pair of eyes. Propaganda analysis that can't survive review is just another narrative."
    },
    {
        "id": "edward-bernays-console-3",
        "title": "Monitor the Influence Operation",
        "console": "siem-dashboard",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Treat the influence-monitoring feed like a SOC analyst: acknowledge, assign, and escalate coordinated inauthentic behavior.",
        "tasks": [
            {"id": "edward-bernays-console-3-t1", "instruction": "Acknowledge alert ALT-101 (impossible travel login) — start working the queue.", "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-101"}}, "hint": "In the Alerts section, click Ack on ALT-101."},
            {"id": "edward-bernays-console-3-t2", "instruction": "Assign ALT-102 (malware hash match) to analyst 'rivera'.", "validate": {"action": "assign-alert", "params": {"id": "ALT-102", "analyst": "rivera"}}, "hint": "Use the 'Assign alert' form: ALERT ID ALT-102, ANALYST rivera."},
            {"id": "edward-bernays-console-3-t3", "instruction": "Escalate ALT-103 (unusual outbound volume) to incident response.", "validate": {"action": "escalate", "params": {"id": "ALT-103"}}, "hint": "Click Escalate on ALT-103."},
            {"id": "edward-bernays-console-3-t4", "instruction": "Create a detection rule named 'coordinated-posting-burst' with any query text.", "validate": {"action": "create-rule", "params": {"name": "coordinated-posting-burst"}}, "hint": "In Detection rules, create rule 'coordinated-posting-burst' (query text is your choice)."}
        ],
        "debrief": "Influence operations are detected like intrusions: triage the alerts, assign ownership, escalate the real ones, and encode what you learned as a detection rule for next time."
    },
    {
        "id": "edward-bernays-console-4",
        "title": "Run the Fact-Check Queue",
        "console": "ticketing",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "The newsroom's verification desk runs on tickets. Log a claim, assign it, and resolve it with a verdict.",
        "tasks": [
            {"id": "edward-bernays-console-4-t1", "instruction": "Create a P1 ticket titled 'Viral video health claim needs verification'.", "validate": {"action": "create-ticket", "params": {"title": "Viral video health claim needs verification", "priority": "P1"}}, "hint": "New ticket section: TITLE exactly as given, PRIORITY P1."},
            {"id": "edward-bernays-console-4-t2", "instruction": "Assign INC-9001 to 'factdesk'.", "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "factdesk"}}, "hint": "Assign form: TICKET ID INC-9001, ASSIGNEE factdesk."},
            {"id": "edward-bernays-console-4-t3", "instruction": "Add a note to INC-9001: 'Sources checked: claim unsupported.'", "validate": {"action": "add-note", "params": {"id": "INC-9001", "text": "Sources checked: claim unsupported."}}, "hint": "Add note form: INC-9001 with the exact verdict text."}
        ],
        "debrief": "Verification is a workflow: intake the claim, assign an owner, record the verdict. Speed matters, but the written verdict is what the public can check later."
    }
]

MISSIONS = [
    {
        "id": "edward-bernays-term-1",
        "title": "Open the Archive",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Every investigation starts by surveying the sources. List the workspace and read the study notes.",
        "objectives": ["List the practice workspace", "Read the archived study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "notes.txt", "hint": "Type: ls — the archive listing includes notes.txt."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "grep", "hint": "Type: cat notes.txt — the notes mention grep among the essentials."}
        ],
        "success_message": "Archive surveyed. Know what sources you hold before you make claims about them."
    },
    {
        "id": "edward-bernays-term-2",
        "title": "Transcribe the Leaflet",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Transcribe a 1929 leaflet slogan into leaflet.txt, then read it back to verify the transcription.",
        "objectives": ["Write the slogan to leaflet.txt", "Read the transcription back"],
        "checks": [
            {"command_pattern": "echo.*>\\s*leaflet\\.txt", "expect_contains": "", "hint": "Type: echo \"the people's choice\" > leaflet.txt (no output on success)."},
            {"command_pattern": "cat\\s+leaflet\\.txt", "expect_contains": "people's choice", "hint": "Type: cat leaflet.txt — your transcribed slogan appears."}
        ],
        "success_message": "Transcribed and verified. Primary sources first — commentary later."
    },
    {
        "id": "edward-bernays-term-3",
        "title": "Count the Repetition",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Repetition is the technique. Append the slogan three times, then measure how repetition accumulates.",
        "objectives": ["Repeat the slogan into the file", "Count the lines", "Search for the repeated phrase"],
        "checks": [
            {"command_pattern": "echo.*>>\\s*leaflet\\.txt", "expect_contains": "", "hint": "Append again: echo \"the people's choice\" >> leaflet.txt — repeat it a few times."},
            {"command_pattern": "wc\\s+.*leaflet\\.txt", "expect_contains": "leaflet.txt", "hint": "Type: wc -l leaflet.txt — the count shows how repetition stacks."},
            {"command_pattern": "grep\\s+choice\\s+leaflet\\.txt", "expect_contains": "people's choice", "hint": "Type: grep choice leaflet.txt — every repeated line is listed."}
        ],
        "success_message": "Repetition quantified. Familiarity is not evidence — but now you can measure exactly how much familiarity was manufactured."
    },
    {
        "id": "edward-bernays-term-4",
        "title": "Verify Document Integrity",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Archives get tampered with. Seal your transcription with a real SHA-256 hash so any later alteration is detectable.",
        "objectives": ["Hash the transcription file's key phrase"],
        "checks": [
            {"command_pattern": '^sha256sum\\s+["\']', "expect_contains": "people's choice", "hint": "Type: sha256sum \"people's choice\" — the real hash is computed and the quoted phrase echoed back."},
        ],
        "success_message": "Sealed. A hash is a commitment: alter one character of the source and the seal breaks."
    },
    {
        "id": "edward-bernays-term-5",
        "title": "Read the Server Logs",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A 'news' site's traffic spiked during the campaign. Read its access log edges for anomalies.",
        "objectives": ["Read the first log lines", "Read the last log lines"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "server starting", "hint": "Type: head -n 2 logs/app.log — the log opens with the server starting."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "timeout", "hint": "Type: tail -n 2 logs/app.log — the tail shows the timeout error."}
        ],
        "success_message": "Edges read. Anomalies live at the boundaries — what started normally and what ended badly."
    },
    {
        "id": "edward-bernays-term-6",
        "title": "Trace the Source Domain",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Before citing a site, check it resolves and the path to it is clean — basic source hygiene.",
        "objectives": ["Resolve the domain", "Confirm connectivity"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "93.184.216.34", "hint": "Type: dig example-news.org — the ANSWER SECTION returns its address."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping example-news.org — zero packet loss confirms the path."}
        ],
        "success_message": "Source traced. 'Who published this and can I reach them' precedes 'do I believe them'."
    },
    {
        "id": "edward-bernays-term-7",
        "title": "Audit the Environment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Analysts verify their own tools first. Confirm your shell environment is what you expect.",
        "objectives": ["Print the environment", "Confirm the working directory via variable expansion"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "HOME=/home/candidate", "hint": "Type: ps — this sandbox prints the environment; find HOME=/home/candidate."},
            {"command_pattern": "echo\\s+\\$USER", "expect_contains": "candidate", "hint": "Type: echo $USER — expands to candidate."}
        ],
        "success_message": "Environment audited. Verify the instrument before trusting the measurement — in archives as in shells."
    }
]
