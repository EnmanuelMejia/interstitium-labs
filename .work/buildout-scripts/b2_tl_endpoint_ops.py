import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_common import merge

D = 'tl-endpoint-ops'

SIMS = [
    {
        "id": "tl-endpoint-sim-blocked-app",
        "title": "The incident responder's tool got blocked",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "During an active intrusion, the responder's forensic tool was blocked by the allowlist policy on the compromised host. The responder is demanding the policy be disabled. Diagnose before you decide.",
        "steps": [
            {
                "symptom": "Block event: forensic-tool.exe denied on WS-301 at 14:22. Policy: default-deny. The tool hash is not in the allowlist.",
                "options": [
                    "Disable the endpoint policy so the responder can work",
                    "Verify the tool: check the hash against the vendor's published value, confirm the responder's identity and ticket, then approve the specific hash in a scoped, time-boxed policy exception",
                    "Tell the responder to work without the tool",
                    "Add *\\*.exe to the allowlist temporarily"
                ],
                "correct": 1,
                "evidence": [
                    ["block-log.txt", "14:22 deny forensic-tool.exe sha256:9f2c... on WS-301. Policy: default-deny, Learning Mode expired 90 days ago."],
                    ["vendor-hash.txt", "Published sha256 for forensic-tool v3.2: 9f2c... — matches the blocked binary. Ticket INC-4412 names this responder and host."],
                ],
                "explain": "Default-deny did its job — it blocked an unknown binary, even a legitimate one. The answer is never 'turn off the control during the incident'; it is verify the hash, scope the exception to that hash on that host, and time-box it."
            },
            {
                "symptom": "Hash verified, exception granted for 4 hours on WS-301. The responder now asks for a permanent exception 'for next time.' Your call?",
                "options": [
                    "Make it permanent — responders need their tools",
                    "Deny permanent: approve the tool through the normal change process (hash pinned in the gold image policy, change ticket, review) instead of a standing exception",
                    "Extend the exception to 30 days",
                    "Allowlist the whole tools folder"
                ],
                "correct": 1,
                "evidence": [
                    ["change-process.txt", "Permanent allowlist entries require: vendor hash verification, change ticket, security review, and inclusion in the baseline policy — not a ticket-time exception."],
                ],
                "explain": "Temporary exceptions are incident tools; permanent entries are architecture. Routing the tool through the proper change process gets the responder their tool forever, without a standing hole punched in a panic."
            }
        ],
        "debrief": "Allowlisting will block legitimate tools — that is the price of default-deny, and it is worth paying. The discipline: verify the hash, scope the exception, time-box it, and route permanence through change control.",
        "points": 15
    },
    {
        "id": "tl-endpoint-sim-elevation",
        "title": "The elevation request at 4:55 PM",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A developer requests local admin elevation to install a driver package, 5 minutes before the change freeze. The package is unsigned. Decide.",
        "steps": [
            {
                "symptom": "Request: local admin for 2 hours, unsigned driver installer, justification 'need it for tomorrow's demo.' No ticket, no manager approval.",
                "options": [
                    "Approve — the demo matters",
                    "Deny as requested; counter with just-in-time elevation for the signed version through the normal change window, with the installer hash verified and the session recorded",
                    "Approve permanently — developers need admin",
                    "Ignore the request"
                ],
                "correct": 1,
                "evidence": [
                    ["elevation-policy.txt", "JIT elevation: time-boxed, recorded, hash-verified, manager-approved, never during freeze without incident ticket. Unsigned drivers: never elevated, no exceptions."],
                    ["threat-intel.txt", "Unsigned 'driver packages' are a top initial-access vector; BYOVD (bring your own vulnerable driver) attacks abuse exactly this path."],
                ],
                "explain": "Elevation is not a favor — it is a privileged-access decision. Unsigned code plus no ticket plus freeze window is three red flags; the counter-offer (signed, verified, recorded, in-window) meets the real need without the risk."
            },
            {
                "symptom": "The developer returns with a signed installer, a manager-approved ticket, and agrees to the change window tomorrow. Final decision?",
                "options": [
                    "Still deny — developers should never have admin",
                    "Approve JIT elevation: 1 hour, recorded session, hash-pinned installer, auto-revoke — the request now meets every policy condition",
                    "Approve for the whole week to be safe",
                    "Approve without recording to save time"
                ],
                "correct": 1,
                "evidence": [
                    ["ticket.txt", "CHG-8821 approved by manager, installer hash pinned, window 09:00–10:00 tomorrow, session recording enabled."],
                ],
                "explain": "Just-in-time elevation exists precisely for this: legitimate need, bounded blast radius, full accountability. Denying a compliant request teaches people to bypass the process; approving it properly teaches them to use it."
            }
        ],
        "debrief": "Elevation decisions are risk decisions with a paper trail. Deny the non-compliant request, approve the compliant one with bounds and recording — the process must be easier to use than to bypass.",
        "points": 15
    },
    {
        "id": "tl-endpoint-sim-ringfence",
        "title": "The ringfenced browser tried to escape",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Ringfencing contained it: the browser tried to launch powershell.exe and was denied. But the attempt itself means something got into the browser. Respond.",
        "steps": [
            {
                "symptom": "Ringfence deny: chrome.exe -> powershell.exe blocked 11:47. Preceding: user opened an invoice attachment from an unknown sender at 11:42.",
                "options": [
                    "Containment held — close the ticket, the control worked",
                    "Containment held AND investigate: the block proves the control works, but the launch attempt proves malicious content reached the browser — isolate the host, analyze the attachment, hunt for what else it tried",
                    "Remove the ringfence so the browser works normally",
                    "Reinstall Chrome"
                ],
                "correct": 1,
                "evidence": [
                    ["ringfence-log.txt", "11:47 deny: chrome.exe attempted CreateProcess powershell.exe -enc <blob>. Policy: browsers may not spawn shells. Precedent: none in 90 days."],
                    ["email.txt", "11:42 invoice.doc from unknown sender, macros enabled by user. Attachment hash matches a known Qakbot loader."],
                ],
                "explain": "Ringfencing is containment, not cure. The deny event is a detection: malicious content executed far enough to try escaping. Celebrate the control, then work the intrusion it revealed."
            },
            {
                "symptom": "Attachment confirmed malicious (Qakbot loader). The browser was ringfenced, but what else must you verify?",
                "options": [
                    "Nothing — the ringfence stopped it",
                    "Verify the full kill chain was contained: check for persistence mechanisms, credential access attempts, and lateral movement from this host — ringfencing blocks categories of behavior, and you must confirm nothing else slipped a different path",
                    "Delete the email",
                    "Block the sender domain and move on"
                ],
                "correct": 1,
                "evidence": [
                    ["hunt.txt", "Host EDR: no persistence created, no lateral movement, but 3 credential-dump attempts (all denied by a second policy). The loader tried 4 techniques; 1 was attempted, 3 were pre-blocked."],
                ],
                "explain": "Assume-breach thinking: the control stopped what it saw, but the attacker tried four things. Verify each one failed — the hunt is not over until every attempted technique is accounted for."
            }
        ],
        "debrief": "Ringfencing turns 'the browser got exploited' from a disaster into a detection. The control contains; the analyst still hunts. Every blocked escape attempt is an incident until proven otherwise.",
        "points": 20
    },
    {
        "id": "tl-endpoint-sim-usb",
        "title": "The blocked USB at the finance desk",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Storage Control blocked a USB write on a finance workstation: 2.1 GB attempted to an unapproved device. The user says it was 'just a backup.' Respond.",
        "steps": [
            {
                "symptom": "Block event: 2.1 GB write to unapproved USB on FIN-04, user k.osei, 16:40. File types: .xlsx, .pdf — names match payroll directories.",
                "options": [
                    "Approve the device — the user explained it",
                    "Treat as potential exfiltration until assessed: isolate the data question first — what was being copied, is it sensitive, was there authorization — while preserving the block",
                    "Confiscate the USB immediately",
                    "Disable Storage Control for finance"
                ],
                "correct": 1,
                "evidence": [
                    ["dlp-log.txt", "File names: payroll-q3.xlsx, bonuses-2026.pdf. Classification: confidential. No approved removable-media request on file for k.osei."],
                    ["policy.txt", "Storage Control: unapproved devices blocked by default. Assessment before accusation: determine data, authorization, and intent through proper channels."],
                ],
                "explain": "The control worked — the data did not leave. Now assess like an investigator, not a prosecutor: what data, what authorization, what intent. The block gives you time to ask; use it."
            },
            {
                "symptom": "Assessment: k.osei was taking payroll files home to 'work over the weekend.' No malicious intent found, but a clear policy violation with confidential data. Disposition?",
                "options": [
                    "Fire the user",
                    "Document the violation, require secure remote-access training, provide an approved encrypted transfer method for legitimate after-hours work, and keep the block in place",
                    "Do nothing — no harm done",
                    "Approve all USB devices to avoid friction"
                ],
                "correct": 1,
                "evidence": [
                    ["hr-note.txt", "First violation, 6-year clean record, cooperative. Remediation: training + approved workflow. Repeat violations escalate per policy."],
                ],
                "explain": "Security that only punishes teaches concealment. The fix addresses the real problem — the user had no approved way to work after hours — while keeping the control and documenting the lesson."
            }
        ],
        "debrief": "Storage Control turns exfiltration attempts into teachable moments. Block first, assess fairly, fix the workflow gap — controls plus usable alternatives beat controls plus resentment.",
        "points": 15
    },
    {
        "id": "tl-endpoint-sim-change-window",
        "title": "Emergency policy change outside the window",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A critical app breaks at 8 PM due to a policy misconfiguration. The fix is a one-line allowlist change, but the change window is tomorrow at 6 AM and the app supports the night shift. Decide.",
        "steps": [
            {
                "symptom": "Broken: night-shift logistics app, 40 users idle. Fix: allowlist one verified hash. Risk of the change: minimal (single hash, tested in staging). Risk of waiting: 10 hours of downtime.",
                "options": [
                    "Wait for the window — process is process",
                    "Emergency change: apply the fix now with documented emergency approval, peer review of the hash, automatic rollback plan, and retroactive change-ticket review tomorrow",
                    "Apply the fix quietly and tell no one",
                    "Disable the endpoint policy until morning"
                ],
                "correct": 1,
                "evidence": [
                    ["emergency-process.txt", "Emergency changes permitted when: business impact is severe, the change is minimal and reversible, two-person approval is obtained, and a rollback plan exists. Full review within 24h."],
                    ["hash-verify.txt", "Hash verified against vendor + staging test passed. Reversal: single rule deletion, <2 min."],
                ],
                "explain": "Change control exists to manage risk, not to worship the calendar. The emergency path — bounded change, two-person rule, rollback plan, retroactive review — is the process working as designed under pressure."
            },
            {
                "symptom": "Emergency change applied, app restored. What happens tomorrow?",
                "options": [
                    "Nothing — it worked",
                    "Retroactive review: the change ticket is completed with evidence, the emergency justification is recorded, and the incident feeds the policy QA process so the misconfiguration does not recur",
                    "Revert the change to follow the window",
                    "Delete the emergency approval record"
                ],
                "correct": 1,
                "evidence": [
                    ["qa-note.txt", "Root cause: hash changed in vendor update, policy not refreshed. Fix: add vendor-update monitoring to policy QA checklist."],
                ],
                "explain": "The emergency path is a loan, not a gift — it gets repaid with documentation and a root-cause fix. Otherwise every change becomes an 'emergency' and change control is dead."
            }
        ],
        "debrief": "Change control must bend without breaking. Emergency paths with approval, reversibility, and retroactive review keep the business running and the audit trail intact.",
        "points": 15
    }
]

CONSOLES = [
    {
        "id": "tl-endpoint-console-ticket",
        "title": "Run the elevation request ticket",
        "console": "ticketing",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Open a P3 ticket for the developer's elevation request, assign it to endpoint-ops, and move it to in-progress.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a P3 ticket titled 'JIT elevation — driver install (CHG-8821)'.",
                "validate": {"action": "create-ticket", "params": {"title": "JIT elevation — driver install (CHG-8821)", "priority": "P3"}},
                "hint": "Create a P3 ticket titled 'JIT elevation — driver install (CHG-8821)'."
            },
            {
                "id": "t2",
                "instruction": "Assign the ticket to 'endpoint-ops'.",
                "validate": {"action": "assign-ticket", "params": {"id": "1", "assignee": "endpoint-ops"}},
                "hint": "Assign ticket 1 to endpoint-ops."
            },
            {
                "id": "t3",
                "instruction": "Move the ticket to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "1", "status": "in-progress"}},
                "hint": "Update ticket 1 status to in-progress."
            }
        ],
        "debrief": "Elevation requests are changes: ticketed, approved, bounded, and recorded."
    },
    {
        "id": "tl-endpoint-console-firewall",
        "title": "Block the exfil destination",
        "console": "firewall",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The loader tried to reach 185.220.14.9 on TCP 443. Drop it on OUTPUT, delete the stale allow rule id 12, and set OUTPUT default to DROP.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Add a rule dropping TCP port 443 to 185.220.14.9 on OUTPUT.",
                "validate": {"action": "add-rule", "params": {"chain": "OUTPUT", "protocol": "tcp", "port": 443, "source": "any", "action": "DROP"}},
                "hint": "Add an OUTPUT rule: protocol tcp, port 443, source any, action DROP."
            },
            {
                "id": "t2",
                "instruction": "Delete stale firewall rule id 12.",
                "validate": {"action": "delete-rule", "params": {"id": "12"}},
                "hint": "Delete firewall rule with id 12."
            },
            {
                "id": "t3",
                "instruction": "Set the OUTPUT chain default policy to DROP.",
                "validate": {"action": "set-default-policy", "params": {"chain": "OUTPUT", "policy": "DROP"}},
                "hint": "Set the default policy of the OUTPUT chain to DROP."
            }
        ],
        "debrief": "Network control backs up endpoint control: kill the egress, clean stale allows, default-deny."
    },
    {
        "id": "tl-endpoint-console-quarantine",
        "title": "Quarantine the malicious attachment",
        "console": "linux-desktop",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Create a quarantine directory, lock down the captured attachment, and restrict it to root.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create the directory /quarantine/inc-4412.",
                "validate": {"action": "create-dir", "params": {"path": "/quarantine/inc-4412"}},
                "hint": "Create directory /quarantine/inc-4412."
            },
            {
                "id": "t2",
                "instruction": "Change /quarantine/invoice.doc permissions to 600.",
                "validate": {"action": "chmod", "params": {"path": "/quarantine/invoice.doc", "mode": "600"}},
                "hint": "Set mode 600 on /quarantine/invoice.doc."
            },
            {
                "id": "t3",
                "instruction": "Change the owner of /quarantine/invoice.doc to root.",
                "validate": {"action": "chown", "params": {"path": "/quarantine/invoice.doc", "owner": "root"}},
                "hint": "Change owner of /quarantine/invoice.doc to root."
            }
        ],
        "debrief": "Malware samples are evidence: quarantined, access-controlled, and owned by root — never left in a downloads folder."
    },
    {
        "id": "tl-endpoint-console-jit-config",
        "title": "Configure the JIT elevation window",
        "console": "generic-web",
        "domain_id": D,
        "difficulty": 1,
        "brief": "In the endpoint platform settings, set the JIT elevation duration to 60 minutes and submit.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set the 'jit-elevation-minutes' field to 60.",
                "validate": {"action": "set-field", "params": {"id": "jit-elevation-minutes", "value": "60"}},
                "hint": "Set field jit-elevation-minutes to 60."
            },
            {
                "id": "t2",
                "instruction": "Submit the elevation configuration form.",
                "validate": {"action": "submit-form", "params": {}},
                "hint": "Click submit on the configuration form."
            }
        ],
        "debrief": "Elevation bounds belong in platform config: time-boxed by default, so no grant outlives its need."
    }
]

MISSIONS = [
    {
        "id": "tl-endpoint-mission-ps",
        "title": "List endpoint processes",
        "domain_id": D,
        "difficulty": 1,
        "brief": "List running processes and confirm the endpoint agent is present.",
        "objectives": ["Run ps and spot the endpoint agent"],
        "checks": [
            {
                "command_pattern": "^ps",
                "expect_contains": "endpoint-agent",
                "hint": "Type: ps aux"
            }
        ],
        "success_message": "Process list captured — the endpoint agent is running."
    },
    {
        "id": "tl-endpoint-mission-grep-block",
        "title": "Find the block events",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Search the agent log for block events on the forensic tool.",
        "objectives": ["Grep agent.log for 'BLOCK'"],
        "checks": [
            {
                "command_pattern": "^grep\\s+BLOCK\\s+agent\\.log",
                "expect_contains": "BLOCK",
                "hint": "Type: grep BLOCK agent.log"
            }
        ],
        "success_message": "Block events found — default-deny is enforcing."
    },
    {
        "id": "tl-endpoint-mission-verify-installer",
        "title": "Verify the installer hash",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Hash the driver installer before approving it for elevation.",
        "objectives": ["Run sha256sum on driver-installer.exe"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+driver-installer\\.exe",
                "expect_contains": "driver-installer.exe",
                "hint": "Type: sha256sum driver-installer.exe"
            }
        ],
        "success_message": "Installer hash captured — compare against the vendor value."
    },
    {
        "id": "tl-endpoint-mission-sort-hashes",
        "title": "Sort the allowlist hashes",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Sort the approved hash list to audit it efficiently.",
        "objectives": ["Sort allowed-hashes.txt"],
        "checks": [
            {
                "command_pattern": "^sort\\s+allowed-hashes\\.txt",
                "expect_contains": "9f2c",
                "hint": "Type: sort allowed-hashes.txt"
            }
        ],
        "success_message": "Hashes sorted — the allowlist is auditable."
    },
    {
        "id": "tl-endpoint-mission-find-exe",
        "title": "Find unauthorized executables",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Search the downloads folder for executables that should not be there.",
        "objectives": ["Find .exe files under /home/user/downloads"],
        "checks": [
            {
                "command_pattern": "^find\\s+/home/user/downloads.*\\.exe",
                "expect_contains": ".exe",
                "hint": "Type: find /home/user/downloads -name '*.exe'"
            }
        ],
        "success_message": "Executables found — each one gets a hash check."
    },
    {
        "id": "tl-endpoint-mission-read-policy",
        "title": "Read the ringfence policy",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Read the ringfence policy file to confirm browsers cannot spawn shells.",
        "objectives": ["Cat ringfence-policy.json and confirm the deny rule"],
        "checks": [
            {
                "command_pattern": "^cat\\s+ringfence-policy\\.json",
                "expect_contains": "deny",
                "hint": "Type: cat ringfence-policy.json"
            }
        ],
        "success_message": "Policy confirmed — the browser-to-shell path is denied."
    },
    {
        "id": "tl-endpoint-mission-diff-policy",
        "title": "Diff the policy versions",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Compare the previous policy against the current one to audit the emergency change.",
        "objectives": ["Diff policy-v1.json against policy-v2.json"],
        "checks": [
            {
                "command_pattern": "^diff\\s+policy-v1\\.json\\s+policy-v2\\.json",
                "expect_contains": ">",
                "hint": "Type: diff policy-v1.json policy-v2.json"
            }
        ],
        "success_message": "Policy diff reviewed — the emergency change is exactly one rule."
    }
]

if __name__ == '__main__':
    merge('tl-endpoint-ops', sims=SIMS, consoles=CONSOLES, missions=MISSIONS)
