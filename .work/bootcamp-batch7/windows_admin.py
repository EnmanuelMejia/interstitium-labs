# Batch 7 — windows-admin: Windows Systems Administration
DOMAIN = "windows-admin"

SIMS = [
    {
        "id": "windows-admin-sim-1",
        "title": "Why Isn't the GPO Applying?",
        "kind": "troubleshoot",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A security baseline GPO applies to every OU except Finance. Diagnose the Group Policy failure.",
        "steps": [
            {
                "symptom": "Baseline GPO linked at the domain level applies everywhere except the Finance OU.",
                "evidence": [
                    ["gpresult", "Finance machines show the GPO as 'Denied (Security Filtering)'"],
                    ["Delegation", "The GPO's security filter lists only 'Workstation-Admins'"],
                    ["Finance", "Finance machines are in 'Finance-Users' — nobody added them to the filter"]
                ],
                "options": [
                    "Link the GPO directly to the Finance OU as well",
                    "Security filtering is the cause: the GPO only applies to principals in its filter — add 'Finance-Computers' (or Authenticated Users, per design) to the security filter instead of duplicating links",
                    "Run gpupdate /force on every Finance machine"
                ],
                "correct": 1,
                "explain": "'Denied (Security Filtering)' names the mechanism: link order is fine, but the GPO's ACL doesn't include Finance's machines. Fix the filter once; duplicating links creates the OU-sprawl that causes the next mystery."
            },
            {
                "symptom": "Filter fixed, but one Finance laptop still doesn't apply the policy after gpupdate.",
                "evidence": [
                    ["Event log", "Event 1058: cannot access the SYSVOL share"],
                    ["Network", "Laptop is on the guest Wi-Fi, not the corporate LAN"],
                    ["Others", "Every wired Finance machine applied fine"]
                ],
                "options": [
                    "Rebuild the laptop",
                    "The laptop can't reach SYSVOL from guest Wi-Fi — move it to the corporate network (or VPN) and gpupdate again; GPO needs the domain, not just the command",
                    "Disable the firewall on the laptop"
                ],
                "correct": 1,
                "explain": "gpupdate without domain connectivity is theater. Event 1058 says the client can't read SYSVOL — fix the network path (corporate LAN/VPN), then update. Always read the event log before rebuilding anything."
            },
            {
                "symptom": "All green. What permanent practice prevents the next GPO mystery?",
                "evidence": [
                    ["Constraint", "Must catch filtering/link mistakes before users do"],
                    ["Goal", "Every GPO change verified end-to-end"]
                ],
                "options": [
                    "Email the team after every GPO change",
                    "A GPO change checklist: document link order, security filter, and WMI filters; verify with gpresult on a pilot machine in each affected OU before wide rollout",
                    "Stop using security filtering entirely"
                ],
                "correct": 1,
                "explain": "GPO changes get the same discipline as code: checklists, pilot OUs, gpresult verification. The checklist from this incident becomes the runbook for the next change."
            }
        ],
        "debrief": "Group Policy failures are almost always scope problems (links, filters, WMI) or connectivity (SYSVOL reachability). Read gpresult, read the event log, verify on pilots — in that order.",
        "points": 15
    },
    {
        "id": "windows-admin-sim-2",
        "title": "Patch Tuesday Triage",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "It's Patch Tuesday. 400 servers, a critical RCE in the print spooler, and a maintenance window Friday. Run the triage.",
        "steps": [
            {
                "id": "triage",
                "text": "Critical RCE, print spooler, exploit chatter online. 400 servers across prod, staging, and lab. Maintenance window Friday 10 PM–2 AM. First move?",
                "choices": [
                    {"label": "Push the patch to all 400 servers immediately — critical means now", "feedback": "Untested patches on 400 production servers is how you trade a vulnerability for an outage. Speed without staging is gambling.", "points": 2, "next": "blast"},
                    {"label": "Risk-rank: patch internet-facing and print servers TODAY via emergency change; lab tonight; staging tomorrow; prod in Friday's window", "feedback": "Blast-radius thinking: the exposed systems get the emergency change, everything else rides the normal ring progression. Risk reduced today, stability kept.", "points": 10, "next": "rings"},
                    {"label": "Wait for Friday's window — process is process", "feedback": "Process without judgment: the internet-facing print servers sit exploitable for 72 hours because the calendar said so.", "points": 3, "next": "blast"}
                ]
            },
            {
                "id": "blast",
                "text": "You pushed everywhere at once. 60 servers blue-screen on reboot — the patch conflicts with the EDR driver. 2 AM, phones ringing. What now?",
                "choices": [
                    {"label": "Keep pushing — the remaining 340 need the patch too", "feedback": "Pushing through a known-bad interaction is how 60 becomes 400. Stop the line.", "points": 0, "next": "END"},
                    {"label": "Halt the rollout, roll back the 60 via the recovery image, open a P1 with the EDR vendor, and re-stage with the fixed driver combo", "feedback": "Stop-the-line discipline: halt, recover, root-cause with the vendor, re-stage. The 340 wait — safely.", "points": 6, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "rings",
                "text": "Rings worked: lab clean, staging clean, Friday's prod window patched 380 servers with zero incidents. Monday's review: what becomes permanent policy?",
                "choices": [
                    {"label": "'We got lucky — same process next month'", "feedback": "It wasn't luck, it was rings. Failing to encode the win guarantees relearning it during the next critical RCE.", "points": 3, "next": "END"},
                    {"label": "Encode the ring model: emergency ring for exposed systems, lab→staging→prod progression, EDR-compat check as a mandatory gate, stop-the-line authority for the on-call", "feedback": "The incident becomes infrastructure: rings, gates, and explicit stop authority. Next Patch Tuesday runs itself.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Patching is risk management, not speed: ring the rollout by exposure, gate on compatibility, and give the on-call stop-the-line authority. The policy is the product of the incident.",
        "points": 20
    },
    {
        "id": "windows-admin-sim-3",
        "title": "Join the Domain",
        "kind": "ordering",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Order the steps to properly join a Windows machine to the domain and verify it.",
        "steps": {
            "context": "A new workstation needs to join the corp domain. Order the steps.",
            "items": [
                "Verify network: the machine reaches a domain controller (DNS points at the DC)",
                "Join the domain with a privileged account and reboot",
                "Confirm the computer object appears in the correct OU (move it if needed)",
                "Run gpupdate and verify with gpresult that baseline policies apply",
                "Hand off: document the asset in inventory and notify the user"
            ],
            "correct_order": [0, 1, 2, 3, 4]
        },
        "debrief": "DNS first (domain join is DNS-dependent), join and reboot, OU placement (policies follow the OU), verify with gpresult, then document. Skip the verification and you'll meet the machine again — as a ticket.",
        "points": 10
    },
    {
        "id": "windows-admin-sim-4",
        "title": "Audit the Server Config",
        "kind": "config-check",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "A member server's hardening checklist has 3 failures. Find them.",
        "steps": {
            "config": "# srv-hardening.conf — member server\nadmin_shares = enabled           # line 2\nrdp_nla = required              # line 3\nsmb1 = enabled                  # line 4\nlocal_admin = renamed           # line 5\nfirewall = on                   # line 6\nllmnr = enabled                 # line 7\nautoplay = disabled             # line 8",
            "find": 3,
            "issues": [
                {"line": 2, "description": "Default administrative shares (C$, ADMIN$) enabled — lateral-movement fuel; rarely needed on member servers.", "fix": "admin_shares = disabled (or restricted via GPO)."},
                {"line": 4, "description": "SMBv1 enabled — deprecated, unpatchable protocol and the WannaCry vector; no modern reason to run it.", "fix": "smb1 = disabled; verify no legacy dependency first."},
                {"line": 7, "description": "LLMNR enabled — spoofable name resolution, the classic Responder attack surface.", "fix": "llmnr = disabled via GPO; ensure DNS suffices."}
            ]
        },
        "debrief": "Lines 3, 5, 6, 8 are hardened correctly (NLA, renamed admin, firewall on, autoplay off). The failures: admin shares, SMBv1, and LLMNR — the standard lateral-movement triad. Harden by default, exception by ticket.",
        "points": 15
    },
    {
        "id": "windows-admin-sim-5",
        "title": "Ransomware at 3 AM",
        "kind": "branching",
        "domain_id": DOMAIN,
        "difficulty": 3,
        "brief": "The on-call phone rings at 3 AM: file shares are encrypting, ransom notes appearing. Run the first hour.",
        "steps": [
            {
                "id": "hour1",
                "text": "3:07 AM. Reports: finance share encrypting, ransom notes in three directories, help desk phone lighting up. Your first three actions?",
                "choices": [
                    {"label": "Start investigating which variant it is — attribution guides response", "feedback": "Attribution is hour-six work. Right now encryption is spreading per minute; every minute of analysis is terabytes lost.", "points": 1, "next": "spread"},
                    {"label": "Isolate: kill the share server's network (keep it powered for forensics), disable the affected AD accounts, page the IR team and leadership", "feedback": "Contain first: network-isolate the encrypting host, cut the compromised accounts' access, escalate. Analysis happens on a contained scene.", "points": 10, "next": "contain"},
                    {"label": "Pay the ransom quickly — it's the fastest recovery", "feedback": "Paying funds the next attack, doesn't guarantee decryption, and may be illegal depending on attribution. Never the first move.", "points": 0, "next": "spread"}
                ]
            },
            {
                "id": "spread",
                "text": "4:30 AM. The encryption reached the backup server — it was domain-joined with the same credentials. What's the brutal lesson and the immediate move?",
                "choices": [
                    {"label": "Lesson: backups must be isolated (offline/air-gapped copies). Move: assess what's recoverable from the offline tapes and rebuild the domain from known-good media.", "feedback": "The hard truth faced directly: domain-joined backups aren't backups. Recovery goes to the offline copies; the domain gets rebuilt, not cleaned.", "points": 7, "next": "END"},
                    {"label": "Try to decrypt with free tools while negotiating with the attackers", "feedback": "Negotiation without contained scope or offline backups is surrender with extra steps.", "points": 1, "next": "END"}
                ],
                "outcome": "bad"
            },
            {
                "id": "contain",
                "text": "5:00 AM. Spread contained to two servers. Forensics has memory captures. Leadership asks: 'Do we pay?' Your recommendation?",
                "choices": [
                    {"label": "'Pay — it's faster than rebuilding.'", "feedback": "Faster and wrong: no guarantee, funds crime, possible sanctions violation. Speed is not the criterion.", "points": 1, "next": "END"},
                    {"label": "'No. We restore the two servers from last night's offline backups, rebuild credentials domain-wide, and publish the timeline. Paying is off the table.'", "feedback": "The professional answer: offline backups make payment unnecessary, credential rebuild removes persistence, transparency preserves trust. This is what the 3 AM discipline bought.", "points": 10, "next": "END"}
                ],
                "outcome": "good"
            }
        ],
        "debrief": "Ransomware response is contain → escalate → recover from offline backups → rebuild trust. The 3 AM decisions are made by the runbook written at 3 PM: isolated backups, practiced isolation steps, and a no-payment policy decided in advance.",
        "points": 20
    }
]

CONSOLES = [
    {
        "id": "windows-admin-console-1",
        "title": "Work the Help Desk Queue",
        "console": "ticketing",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Windows support lives in the queue. Log the ticket, assign it, and resolve it with the actual fix.",
        "tasks": [
            {"id": "windows-admin-console-1-t1", "instruction": "Create a P2 ticket titled 'GPO not applying on Finance laptops'.", "validate": {"action": "create-ticket", "params": {"title": "GPO not applying on Finance laptops", "priority": "P2"}}, "hint": "New ticket: TITLE exactly as given, PRIORITY P2."},
            {"id": "windows-admin-console-1-t2", "instruction": "Assign INC-9001 to 'winadmin-jo'.", "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "winadmin-jo"}}, "hint": "Assign: INC-9001 → winadmin-jo."},
            {"id": "windows-admin-console-1-t3", "instruction": "Add a note to INC-9001: 'gpresult showed Denied (Security Filtering); filter corrected.'", "validate": {"action": "add-note", "params": {"id": "INC-9001", "text": "gpresult showed Denied (Security Filtering); filter corrected."}}, "hint": "Add note: INC-9001 with the exact text."},
            {"id": "windows-admin-console-1-t4", "instruction": "Resolve INC-9001 with resolution 'Security filter fixed; gpupdate verified on pilot machines.'", "validate": {"action": "resolve-ticket", "params": {"id": "INC-9001", "resolution": "Security filter fixed; gpupdate verified on pilot machines."}}, "hint": "Resolve form: INC-9001 with the exact resolution text."}
        ],
        "debrief": "Windows tickets close with evidence: what gpresult said, what was fixed, how it was verified. The note trail is the next admin's runbook."
    },
    {
        "id": "windows-admin-console-2",
        "title": "Configure the Host Firewall",
        "console": "firewall",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Windows Defender Firewall with Advanced Security, simulated: allow RDP for admins only, block everything else by default.",
        "tasks": [
            {"id": "windows-admin-console-2-t1", "instruction": "Add a rule: INPUT chain, tcp port 3389, source 10.0.0.0/8, action ACCEPT — RDP for the admin network only.", "validate": {"action": "add-rule", "params": {"chain": "INPUT", "protocol": "tcp", "port": 3389, "source": "10.0.0.0/8", "action": "ACCEPT"}}, "hint": "Rules: CHAIN INPUT, PROTOCOL tcp, PORT 3389, SOURCE 10.0.0.0/8, ACTION ACCEPT."},
            {"id": "windows-admin-console-2-t2", "instruction": "Add a rule: INPUT chain, tcp port 445, source 0.0.0.0/0, action DROP — no SMB from the internet, ever.", "validate": {"action": "add-rule", "params": {"chain": "INPUT", "protocol": "tcp", "port": 445, "source": "0.0.0.0/0", "action": "DROP"}}, "hint": "Add rule: CHAIN INPUT, PROTOCOL tcp, PORT 445, SOURCE 0.0.0.0/0, ACTION DROP."},
            {"id": "windows-admin-console-2-t3", "instruction": "Set the INPUT chain default policy to DROP — the firewall denies what no rule allows.", "validate": {"action": "set-default-policy", "params": {"chain": "INPUT", "policy": "DROP"}}, "hint": "Default policies: CHAIN INPUT, POLICY DROP."}
        ],
        "debrief": "Host firewall discipline: RDP scoped to the admin network, SMB never from the internet, default-deny underneath. Every open port is a decision with a name on it."
    },
    {
        "id": "windows-admin-console-3",
        "title": "Segment the Office Network",
        "console": "switch-cli",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "The office switch needs VLANs: Finance isolated, printers separate, then save the config.",
        "tasks": [
            {"id": "windows-admin-console-3-t1", "instruction": "Create VLAN 20 named FINANCE.", "validate": {"action": "create-vlan", "params": {"id": 20, "name": "FINANCE"}}, "hint": "In the Terminal section type: vlan 20 name FINANCE"},
            {"id": "windows-admin-console-3-t2", "instruction": "Assign interface Gi0/5 to access VLAN 20 (the Finance printer port).", "validate": {"action": "assign-port", "params": {"port": "Gi0/5", "vlan": 20}}, "hint": "Type: interface Gi0/5 access vlan 20"},
            {"id": "windows-admin-console-3-t3", "instruction": "Set interface Gi0/24 to trunk mode (the uplink to the core).", "validate": {"action": "set-trunk", "params": {"port": "Gi0/24"}}, "hint": "Type: interface Gi0/24 trunk"},
            {"id": "windows-admin-console-3-t4", "instruction": "Save the running configuration.", "validate": {"action": "save-config", "params": {}}, "hint": "Type: write memory"}
        ],
        "debrief": "Segmentation is policy in copper: Finance isolated at layer 2, uplinks trunked, config saved. Unsaved configs don't survive the next power outage."
    },
    {
        "id": "windows-admin-console-4",
        "title": "Maintain the Asset Database",
        "console": "db-admin",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "The CMDB tracks every Windows asset. Create it, add the admin, grant access, back it up.",
        "tasks": [
            {"id": "windows-admin-console-4-t1", "instruction": "Create a database named 'assets'.", "validate": {"action": "create-database", "params": {"name": "assets"}}, "hint": "Databases: create 'assets'."},
            {"id": "windows-admin-console-4-t2", "instruction": "Create a database user named 'winadmin'.", "validate": {"action": "create-user", "params": {"name": "winadmin"}}, "hint": "Users & grants: create user 'winadmin'."},
            {"id": "windows-admin-console-4-t3", "instruction": "Grant SELECT on 'assets' to 'winadmin'.", "validate": {"action": "grant-priv", "params": {"db": "assets", "user": "winadmin", "priv": "SELECT"}}, "hint": "Grants: DB assets, USER winadmin, PRIVILEGE SELECT."},
            {"id": "windows-admin-console-4-t4", "instruction": "Back up the 'assets' database.", "validate": {"action": "backup", "params": {"db": "assets"}}, "hint": "Click 'Back up' on assets."}
        ],
        "debrief": "You can't patch what you can't inventory: the asset database is the foundation of every Patch Tuesday, every audit, every incident response. Back it up like the domain depends on it."
    }
]

MISSIONS = [
    {
        "id": "windows-admin-term-1",
        "title": "Survey the Server",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Orient on the box: list the workspace and read the notes (your runbook shelf).",
        "objectives": ["List the workspace", "Read the study notes"],
        "checks": [
            {"command_pattern": "^ls(\\s|$)", "expect_contains": "logs/", "hint": "Type: ls."},
            {"command_pattern": "cat\\s+notes\\.txt", "expect_contains": "Linux essentials", "hint": "Type: cat notes.txt."}
        ],
        "success_message": "Server surveyed. Read before you touch — the first rule of administration."
    },
    {
        "id": "windows-admin-term-2",
        "title": "Log the Change",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Every change gets a log entry. Write the GPO change to change-log.txt.",
        "objectives": ["Write the change entry", "Append the verification entry", "Read the log"],
        "checks": [
            {"command_pattern": "echo.*>\\s*change-log\\.txt", "expect_contains": "", "hint": "Type: echo \"GPO baseline: security filter fixed\" > change-log.txt (no output on success)."},
            {"command_pattern": "echo.*>>\\s*change-log\\.txt", "expect_contains": "", "hint": "Type: echo \"verified: gpresult clean on 3 pilots\" >> change-log.txt."},
            {"command_pattern": "cat\\s+change-log\\.txt", "expect_contains": "GPO baseline", "hint": "Type: cat change-log.txt."}
        ],
        "success_message": "Change logged. Undocumented changes are incidents waiting for a timestamp."
    },
    {
        "id": "windows-admin-term-3",
        "title": "Audit the Change Log",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Count change entries and search for the verification marker.",
        "objectives": ["Count log lines", "Find verified entries"],
        "checks": [
            {"command_pattern": "wc\\s+-l\\s+change-log\\.txt", "expect_contains": "change-log.txt", "hint": "Type: wc -l change-log.txt."},
            {"command_pattern": "grep\\s+verified\\s+change-log\\.txt", "expect_contains": "verified", "hint": "Type: grep verified change-log.txt."}
        ],
        "success_message": "Log audited. Every change verified, every verification logged."
    },
    {
        "id": "windows-admin-term-4",
        "title": "Seal the Baseline",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Hash the baseline version string — configuration drift detection starts here.",
        "objectives": ["Hash the baseline identifier"],
        "checks": [
            {"command_pattern": "^sha256sum\\s+\\S+", "expect_contains": "baseline-v42", "hint": "Type: sha256sum baseline-v42 finance-ou — the real hash plus your baseline are echoed."}
        ],
        "success_message": "Baseline sealed. Drift is detected by comparing against the seal, not by memory."
    },
    {
        "id": "windows-admin-term-5",
        "title": "Check the Event Trail",
        "domain_id": DOMAIN,
        "difficulty": 2,
        "brief": "Windows admins live in event logs. Read this log's edges and hunt errors.",
        "objectives": ["Read the first lines", "Read the last lines", "Find errors"],
        "checks": [
            {"command_pattern": "head\\s+.*logs/app\\.log", "expect_contains": "server starting", "hint": "Type: head -n 2 logs/app.log."},
            {"command_pattern": "tail\\s+.*logs/app\\.log", "expect_contains": "timeout", "hint": "Type: tail -n 2 logs/app.log."},
            {"command_pattern": "grep\\s+ERROR\\s+logs/app\\.log", "expect_contains": "connection refused", "hint": "Type: grep ERROR logs/app.log."}
        ],
        "success_message": "Event trail read. The log told you; you just had to ask."
    },
    {
        "id": "windows-admin-term-6",
        "title": "Verify the Environment",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "Confirm the administrative environment: identity and home.",
        "objectives": ["Print the environment", "Expand HOME"],
        "checks": [
            {"command_pattern": "^ps(\\s|$)", "expect_contains": "USER=candidate", "hint": "Type: ps."},
            {"command_pattern": "echo\\s+\\$HOME", "expect_contains": "/home/candidate", "hint": "Type: echo $HOME."}
        ],
        "success_message": "Environment verified. Know which context you're administering."
    },
    {
        "id": "windows-admin-term-7",
        "title": "Check Domain Reachability",
        "domain_id": DOMAIN,
        "difficulty": 1,
        "brief": "A domain member that can't reach the DC is just a workgroup machine. Verify DNS and path.",
        "objectives": ["Resolve the DC hostname", "Confirm zero packet loss"],
        "checks": [
            {"command_pattern": "^dig\\s+\\S+", "expect_contains": "ANSWER SECTION", "hint": "Type: dig dc01.corp.example.com."},
            {"command_pattern": "^ping\\s+\\S+", "expect_contains": "0% packet loss", "hint": "Type: ping dc01.corp.example.com."}
        ],
        "success_message": "DC reachable. Domain join is DNS-dependent — verify the dependency."
    }
]
