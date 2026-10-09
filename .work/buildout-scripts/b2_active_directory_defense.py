import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_common import merge

D1 = 'active-directory-defense'
D2 = 'adfind-recon-hunting'

SIMS = [
    {
        "id": "ad-defense-sim-dcsync",
        "title": "DCSync replication attack in progress",
        "kind": "respond",
        "domain_id": D1,
        "difficulty": 3,
        "brief": "The SIEM fires at 02:14: a non-domain-controller host is issuing DRS replication requests against DC02. Credential theft is underway right now. Work the response.",
        "steps": [
            {
                "symptom": "Event 4662 audit shows Ds-Replication-Get-Changes rights exercised by SVC-backup from WS-114, which is not a domain controller.",
                "options": [
                    "DCSync attack: a compromised account with replication rights is pulling password hashes — treat as active credential theft",
                    "Normal backup traffic: the backup service legitimately replicates the directory",
                    "A misconfigured monitoring agent polling LDAP",
                    "Routine SYSVOL replication between domain controllers"
                ],
                "correct": 0,
                "evidence": [
                    ["dc02-security.evtx.txt", "02:14:03 Event 4662 — Subject: SVC-backup — Object: DC=corp,DC=local — Accesses: DS-Replication-Get-Changes, DS-Replication-Get-Changes-All — Source host: WS-114"],
                    ["inventory.txt", "WS-114: finance workstation. Domain controllers: DC01, DC02 only. SVC-backup: backup service account, member of no replication-authorized group per policy."]
                ],
                "explain": "Only domain controllers should issue DRS replication calls. A workstation exercising DS-Replication-Get-Changes is the textbook DCSync pattern — it pulls every password hash in the domain, including krbtgt."
            },
            {
                "symptom": "You must contain the attack without tipping off the intruder's persistence. What is the correct containment order?",
                "options": [
                    "Reset the krbtgt password first, then investigate",
                    "Isolate WS-114 from the network, disable SVC-backup, then hunt for additional footholds before any password resets",
                    "Delete the SVC-backup account immediately",
                    "Shut down DC02 to stop the replication"
                ],
                "correct": 1,
                "evidence": [
                    ["soc-playbook.txt", "Containment: sever attacker access first (host isolation, account disable), THEN remediate credentials. Resetting krbtgt while the attacker still holds access lets them re-establish."],
                    ["edr.txt", "WS-114: active C2 beacon to 185.220.x.x every 60s."]
                ],
                "explain": "Isolation plus account disable cuts the attacker's hands off first. Password resets come after you confirm the foothold is gone, or the attacker just re-steals the new hashes."
            },
            {
                "symptom": "WS-114 is isolated and SVC-backup disabled. The attacker held DCSync rights for ~40 minutes. What completes eradication?",
                "options": [
                    "Re-enable SVC-backup with a new password",
                    "Reset the krbtgt account password twice, force password resets for all privileged accounts, audit replication rights",
                    "Restore DC02 from last night's backup",
                    "Block port 445 on the firewall"
                ],
                "correct": 1,
                "evidence": [
                    ["forensics.txt", "Memory capture from WS-114 shows Mimikatz sekurlsa output. DCSync window: 01:34–02:14. Hashes for 1,900+ accounts exfiltrated, including krbtgt."],
                    ["ad-guidance.txt", "After krbtgt compromise: reset twice to invalidate both current and previous password (ticket lifetime overlap). Audit all principals with DS-Replication-Get-Changes."]
                ],
                "explain": "With hashes exfiltrated, every derived ticket is suspect. The double krbtgt reset invalidates old and new ticket-granting tickets; privileged resets and a replication-rights audit close the loop."
            }
        ],
        "debrief": "DCSync turns any account with replication rights into a domain-wide password dump. Respond in order: confirm the anomaly, isolate the host and disable the account, hunt for footholds, then double-reset krbtgt and audit who holds replication rights. Prevention is least privilege on the directory itself.",
        "points": 20
    },
    {
        "id": "ad-defense-sim-kerberoast",
        "title": "Kerberoasting: hunting crackable service tickets",
        "kind": "troubleshoot",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "Overnight the SIEM logged a burst of Kerberos TGS-REQ messages with RC4 encryption from a single workstation. A service account may be getting roasted. Investigate.",
        "steps": [
            {
                "symptom": "3,100 TGS requests in 20 minutes from WS-087, all requesting RC4-encrypted service tickets.",
                "options": [
                    "Likely Kerberoasting: bulk TGS requests for RC4 tickets are harvested for offline cracking",
                    "Normal service startup after a reboot",
                    "A backup job enumerating shares",
                    "DNS misconfiguration causing ticket retries"
                ],
                "correct": 0,
                "evidence": [
                    ["dc01-kerberos.log", "00:41–01:02: 3,104 TGS-REQ from 10.4.8.87 (WS-087), etype rc4-hmac. No failures — valid user context."],
                    ["baseline.txt", "Normal TGS rate per host: ~40/hour. RC4 usage fleet-wide: <1% of tickets."]
                ],
                "explain": "Kerberoasting needs no privilege: any authenticated user can request service tickets and crack them offline. The volume plus forced RC4 downgrade is the signature — legitimate clients overwhelmingly negotiate AES."
            },
            {
                "symptom": "The tickets target MSSQLSvc/sql01.corp.local. What do you check next to confirm the exposure?",
                "options": [
                    "The service account's password age, complexity, and whether it is a managed service account",
                    "The SQL server's patch level",
                    "The workstation's antivirus status",
                    "The domain functional level"
                ],
                "correct": 0,
                "evidence": [
                    ["ad-account.txt", "SVC-sql: password last set 2019-03-11 (7 years). Not a gMSA. Member of Domain Admins (legacy)."],
                    ["spn.txt", "SPN MSSQLSvc/sql01.corp.local registered to SVC-sql."]
                ],
                "explain": "Kerberoasting succeeds against weak service-account passwords. A seven-year-old password on a Domain Admin service account is the jackpot: crack the ticket, own the domain."
            },
            {
                "symptom": "Confirmed: SVC-sql is roastable and over-privileged. What is the durable fix?",
                "options": [
                    "Disable Kerberos on the SQL server",
                    "Migrate to a group Managed Service Account with a long random password, remove Domain Admin, enforce AES",
                    "Rename the service account",
                    "Block RC4 at the firewall"
                ],
                "correct": 1,
                "evidence": [
                    ["hardening-guide.txt", "gMSA: 240-char auto-rotated passwords, cannot be cracked offline practically. AES-only: removes the RC4 downgrade path. Least privilege: service accounts are never Domain Admins."],
                ],
                "explain": "gMSAs remove the crackable secret entirely through automatic rotation of very long passwords, and AES-only kills the downgrade. Renaming changes nothing about the hash."
            }
        ],
        "debrief": "Kerberoasting is a defender's audit gift: it only works where service accounts are weak. Hunt for TGS volume anomalies, then fix the root cause — managed service accounts, long random passwords, AES enforcement, and least privilege.",
        "points": 15
    },
    {
        "id": "ad-defense-sim-golden-ticket",
        "title": "Forged Kerberos tickets bypassing authentication",
        "kind": "troubleshoot",
        "domain_id": D1,
        "difficulty": 3,
        "brief": "A user account shows successful logons to servers it never touched, with ticket lifetimes of 10 years. Something is forging Kerberos tickets. Track it down.",
        "steps": [
            {
                "symptom": "TGT lifetime 10 years for user j.chen; logons to FILE03 and BACKUP01 with no corresponding interactive session.",
                "options": [
                    "Golden ticket: forged TGTs signed with the stolen krbtgt hash, valid for years and invisible to normal logon auditing",
                    "A misconfigured SSO token cache",
                    "Clock skew between the workstation and the DC",
                    "Cached credentials from an old VPN session"
                ],
                "correct": 0,
                "evidence": [
                    ["dc02-4769.log", "TGT issued for j.chen with lifetime 87600h. Domain policy max: 10h. No 4768 (TGT request) precedes the 4769 service tickets."],
                    ["edr.txt", "No logon session for j.chen on FILE03 in EDR telemetry — the tickets arrive without authentication."]
                ],
                "explain": "Golden tickets are minted offline with the krbtgt hash, so the KDC never logs a TGT request. Absurd lifetimes and logons with no authentication event are the tells."
            },
            {
                "symptom": "You suspect krbtgt compromise. How do you confirm the scope before remediating?",
                "options": [
                    "Check every host for malware",
                    "Correlate anomalous-lifetime tickets across DCs, identify when the krbtgt hash was first abused, and inventory accounts with replication rights",
                    "Force a password change for j.chen",
                    "Rebuild the affected file servers"
                ],
                "correct": 1,
                "evidence": [
                    ["hunt.txt", "Anomalous-lifetime TGTs seen on DC01 and DC02 since 2026-09-19. First abuse predates the j.chen sightings by three weeks."],
                    ["replication-rights.txt", "Principals with DS-Replication-Get-Changes: Domain Controllers, SVC-backup, SVC-oldmigrator."]
                ],
                "explain": "Scope first: the earliest forged ticket bounds the compromise window, and the replication-rights inventory shows every path the attacker could have taken to steal krbtgt."
            },
            {
                "symptom": "Scope confirmed: krbtgt hash stolen via the stale SVC-oldmigrator account. What is the remediation sequence?",
                "options": [
                    "Disable SVC-oldmigrator, reset krbtgt twice, reset all privileged passwords, remove stale replication rights",
                    "Reset krbtgt once and monitor",
                    "Demote and rebuild both DCs",
                    "Enable MFA on the VPN"
                ],
                "correct": 0,
                "evidence": [
                    ["runbook.txt", "krbtgt double-reset: two resets invalidate tickets minted under both the current and previous hash. Single reset leaves the previous-hash window open."],
                ],
                "explain": "Kill the entry path, double-reset krbtgt to burn both ticket generations, rotate everything the stolen hash could have touched, and remove the stale rights so it cannot recur."
            }
        ],
        "debrief": "Golden tickets persist because defenders reset once or never. The discipline is: scope the abuse window, kill the theft path, double-reset krbtgt, rotate privileged credentials, and audit replication rights so the theft cannot repeat.",
        "points": 20
    },
    {
        "id": "ad-defense-sim-tier-model",
        "title": "The legacy app that demands Domain Admin",
        "kind": "decide",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "A vendor's legacy inventory app requires its service account to be a Domain Admin or it will not start. The business says it is critical. Decide the identity architecture.",
        "steps": [
            {
                "symptom": "Vendor support insists: 'SVC-inventory must be Domain Admin. No workaround.' The app runs on one member server.",
                "options": [
                    "Grant Domain Admin — the business need outweighs the risk",
                    "Refuse outright and let the app stay broken",
                    "Profile the app's actual needs with auditing, grant only the specific rights it uses, isolate the server in a tier-appropriate OU with constrained delegation",
                    "Make it a local admin on the domain controller"
                ],
                "correct": 2,
                "evidence": [
                    ["vendor-contract.txt", "Vendor requires 'Domain Admin or equivalent' — undocumented which privileges are actually exercised."],
                    ["tier-model.txt", "Tier 0 (domain controllers, identity systems): only Tier 0 admin accounts. Member servers: Tier 1. Workstations: Tier 2. No account crosses tiers."]
                ],
                "explain": "Vendors ask for Domain Admin because it is easy, not because it is needed. Auditing reveals the true minimum — usually a handful of specific rights — and the tier model keeps those rights from reaching Tier 0."
            },
            {
                "symptom": "Auditing shows the app only writes to one OU and reads three attributes. The vendor still refuses to support a non-DA configuration. Your call?",
                "options": [
                    "Document the exact delegated rights, implement them, accept the support risk with business sign-off, and monitor the account as privileged",
                    "Give up and grant Domain Admin",
                    "Run the app on a domain controller so DA is 'contained'",
                    "Create a second Domain Admin as a backup"
                ],
                "correct": 0,
                "evidence": [
                    ["risk-register.txt", "Residual risk: unsupported config. Mitigations: delegated rights documented, account monitored as Tier 1 privileged, server isolated, quarterly re-audit."],
                ],
                "explain": "Security decisions are risk decisions with owners. Delegation plus monitoring plus documented business acceptance beats both blanket refusal (business harm) and surrender (domain-wide risk)."
            }
        ],
        "debrief": "Standing Domain Admin for applications is how domains fall. Profile the real need, delegate precisely, enforce the tier boundary, and make the residual risk explicit and owned — never silent.",
        "points": 15
    },
    {
        "id": "ad-defense-sim-recon-hunt",
        "title": "AdFind-style reconnaissance at 3 AM",
        "kind": "troubleshoot",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "DC01 logs show thousands of LDAP queries enumerating group memberships and trust relationships from a helpdesk workstation at 03:00. Nobody works the helpdesk at 3 AM. Hunt it.",
        "steps": [
            {
                "symptom": "4,200 LDAP queries in 35 minutes from HD-022, enumerating 'Domain Admins', trusts, and GPOs. Source user: helpdesk intern account.",
                "options": [
                    "Active Directory reconnaissance: pre-attack enumeration mapping privileged groups, trusts, and policy — likely AdFind or similar tooling",
                    "The intern doing diligent after-hours study",
                    "A vulnerability scanner's scheduled run",
                    "Replication traffic misattributed to the workstation"
                ],
                "correct": 0,
                "evidence": [
                    ["dc01-ldap.log", "03:02–03:37: 4,213 queries from 10.4.9.22. Filters: (memberOf=CN=Domain Admins*), (objectClass=trustedDomain), (objectClass=groupPolicyContainer). Base DN: whole domain."],
                    ["edr-hd022.txt", "adfind.exe executed 03:01 from C:\\Users\\intern\\Downloads. Parent: cmd.exe. No ticket for after-hours work."]
                ],
                "explain": "Bulk enumeration of privileged groups, trusts, and GPOs with a dedicated recon binary is the attack-planning phase. Legitimate admin work is targeted; this is cartography."
            },
            {
                "symptom": "Recon confirmed on HD-022. What is the right next move?",
                "options": [
                    "Confront the intern immediately",
                    "Isolate HD-022, preserve memory and disk for forensics, reset the intern account credentials, and hunt for follow-on activity (lateral movement, persistence)",
                    "Delete adfind.exe and close the ticket",
                    "Block LDAP at the firewall"
                ],
                "correct": 1,
                "evidence": [
                    ["playbook-recon.txt", "Recon is the precursor, not the payload. Assume the account is compromised until proven otherwise; hunt for what the recon was planning."],
                ],
                "explain": "Recon means an attack is being planned — possibly by the account owner, possibly by someone who stole the session. Preserve evidence, kill the access, and hunt for the next phase instead of just deleting the tool."
            }
        ],
        "debrief": "LDAP recon is the attacker's map-making. Baseline normal query volumes, alert on bulk enumeration of privileged objects, and treat recon as the start of an investigation — not the end of one.",
        "points": 15
    }
]

CONSOLES = [
    {
        "id": "ad-defense-console-siem-dcsync",
        "title": "Work the DCSync SIEM alert",
        "console": "siem-dashboard",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Alert ALT-2077: 'DCSync replication from non-DC host WS-114'. Acknowledge it, assign it to the identity analyst, and escalate it to Tier 2.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Acknowledge alert ALT-2077.",
                "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-2077"}},
                "hint": "Click acknowledge on alert ALT-2077 in the SIEM queue."
            },
            {
                "id": "t2",
                "instruction": "Assign alert ALT-2077 to analyst 'r.okafor'.",
                "validate": {"action": "assign-alert", "params": {"id": "ALT-2077", "analyst": "r.okafor"}},
                "hint": "Use the assign control on ALT-2077 and enter analyst r.okafor."
            },
            {
                "id": "t3",
                "instruction": "Escalate alert ALT-2077 to Tier 2.",
                "validate": {"action": "escalate", "params": {"id": "ALT-2077"}},
                "hint": "Click escalate on ALT-2077 to send it to Tier 2."
            }
        ],
        "debrief": "Identity-plane alerts are never low priority: acknowledge so nobody else duplicates the work, assign a named owner, escalate with the DCSync context attached."
    },
    {
        "id": "ad-defense-console-ir-ticket",
        "title": "Open the identity incident ticket",
        "console": "ticketing",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Open a P1 incident ticket for the DCSync attack, assign it to the on-call identity responder, and move it to in-progress.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a P1 ticket titled 'DCSync attack from WS-114'.",
                "validate": {"action": "create-ticket", "params": {"title": "DCSync attack from WS-114", "priority": "P1"}},
                "hint": "Create a ticket with title 'DCSync attack from WS-114' and priority P1."
            },
            {
                "id": "t2",
                "instruction": "Assign the ticket to 'oncall-identity'.",
                "validate": {"action": "assign-ticket", "params": {"id": "1", "assignee": "oncall-identity"}},
                "hint": "Assign ticket 1 to oncall-identity."
            },
            {
                "id": "t3",
                "instruction": "Move the ticket to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "1", "status": "in-progress"}},
                "hint": "Update ticket 1 status to in-progress."
            }
        ],
        "debrief": "Active credential theft gets a P1, a named owner, and a live status — the ticket is the shared picture while the response runs."
    },
    {
        "id": "ad-defense-console-firewall",
        "title": "Cut off the rogue replication host",
        "console": "firewall",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "WS-114 (10.4.8.114) is pulling directory replication traffic. Drop its SMB/replication traffic at the host firewall, then set the FORWARD chain default to DROP.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Add a rule dropping TCP port 445 from 10.4.8.114 on INPUT.",
                "validate": {"action": "add-rule", "params": {"chain": "INPUT", "protocol": "tcp", "port": 445, "source": "10.4.8.114", "action": "DROP"}},
                "hint": "Add an INPUT rule: protocol tcp, port 445, source 10.4.8.114, action DROP."
            },
            {
                "id": "t2",
                "instruction": "Set the FORWARD chain default policy to DROP.",
                "validate": {"action": "set-default-policy", "params": {"chain": "FORWARD", "policy": "DROP"}},
                "hint": "Set the default policy of the FORWARD chain to DROP."
            }
        ],
        "debrief": "Network containment buys time: drop the attacker's replication and C2 paths at the firewall while the host is isolated and credentials are rotated."
    },
    {
        "id": "ad-defense-console-backup-perms",
        "title": "Lock down the offline AD backup",
        "console": "linux-desktop",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "The offline NTDS backup at /backups/ntds.dit is world-readable. Restrict it to root-only access.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Select /backups/ntds.dit in the file manager.",
                "validate": {"action": "select", "params": {"path": "/backups/ntds.dit"}},
                "hint": "Click to select the file /backups/ntds.dit."
            },
            {
                "id": "t2",
                "instruction": "Change /backups/ntds.dit permissions to 600.",
                "validate": {"action": "chmod", "params": {"path": "/backups/ntds.dit", "mode": "600"}},
                "hint": "Set mode 600 on /backups/ntds.dit (owner read/write only)."
            },
            {
                "id": "t3",
                "instruction": "Change the owner of /backups/ntds.dit to root.",
                "validate": {"action": "chown", "params": {"path": "/backups/ntds.dit", "owner": "root"}},
                "hint": "Change owner of /backups/ntds.dit to root."
            }
        ],
        "debrief": "An offline NTDS.dit is the whole domain in a file. World-readable backups are a DCSync without the network — permissions are a control, not paperwork."
    }
]

MISSIONS = [
    {
        "id": "ad-defense-mission-recon-grep",
        "title": "Find the recon queries",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Search the LDAP query log for bulk enumeration of the Domain Admins group.",
        "objectives": ["Grep ldap-queries.log for 'Domain Admins' enumeration"],
        "checks": [
            {
                "command_pattern": "^grep.*Domain Admins.*ldap-queries\\.log",
                "expect_contains": "Domain Admins",
                "hint": "Type: grep 'Domain Admins' ldap-queries.log"
            }
        ],
        "success_message": "Recon queries located — bulk enumeration of Domain Admins confirmed."
    },
    {
        "id": "ad-defense-mission-backup-hash",
        "title": "Verify the AD backup integrity",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Before restoring anything, verify the offline NTDS backup hash matches the known-good value.",
        "objectives": ["Run sha256sum on ntds-backup.dit and confirm the filename in the output"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+ntds-backup\\.dit",
                "expect_contains": "ntds-backup.dit",
                "hint": "Type: sha256sum ntds-backup.dit"
            }
        ],
        "success_message": "Backup hash verified — the offline copy is intact."
    },
    {
        "id": "ad-defense-mission-srv-records",
        "title": "Check domain controller SRV records",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Confirm DNS still advertises the legitimate domain controllers via SRV lookup.",
        "objectives": ["Dig the _ldap._tcp SRV record for the domain"],
        "checks": [
            {
                "command_pattern": "^dig.*_ldap\\._tcp",
                "expect_contains": "_ldap._tcp",
                "hint": "Type: dig SRV _ldap._tcp.corp.local"
            }
        ],
        "success_message": "SRV records resolve to the legitimate domain controllers."
    },
    {
        "id": "ad-defense-mission-sysvol-hunt",
        "title": "Hunt SYSVOL for planted scripts",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "Attackers plant scripts in SYSVOL for GPO-based persistence. Find any PowerShell scripts there.",
        "objectives": ["Find .ps1 files under /sysvol"],
        "checks": [
            {
                "command_pattern": "^find\\s+/sysvol.*\\.ps1",
                "expect_contains": ".ps1",
                "hint": "Type: find /sysvol -name '*.ps1'"
            }
        ],
        "success_message": "SYSVOL sweep complete — planted scripts identified for review."
    },
    {
        "id": "ad-defense-mission-gpo-diff",
        "title": "Diff the Group Policy backup",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Compare the known-good GPO export against the current one to spot unauthorized changes.",
        "objectives": ["Diff gpo-baseline.txt against gpo-current.txt"],
        "checks": [
            {
                "command_pattern": "^diff\\s+gpo-baseline\\.txt\\s+gpo-current\\.txt",
                "expect_contains": ">",
                "hint": "Type: diff gpo-baseline.txt gpo-current.txt"
            }
        ],
        "success_message": "Policy drift found — unauthorized GPO changes are now visible."
    },
    {
        "id": "ad-defense-mission-sort-logons",
        "title": "Sort the failed logon list",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Sort failed-logons.txt so you can spot the accounts under password-spray attack.",
        "objectives": ["Sort failed-logons.txt alphabetically"],
        "checks": [
            {
                "command_pattern": "^sort\\s+failed-logons\\.txt",
                "expect_contains": "administrator",
                "hint": "Type: sort failed-logons.txt"
            }
        ],
        "success_message": "Logons sorted — spray targets clustered for the hunt."
    },
    {
        "id": "ad-defense-mission-count-events",
        "title": "Count the replication events",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Count how many DRS replication events fired during the attack window.",
        "objectives": ["Count lines in drs-events.log with wc"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+drs-events\\.log",
                "expect_contains": "drs-events.log",
                "hint": "Type: wc -l drs-events.log"
            }
        ],
        "success_message": "Event count captured — the replication window is now quantified."
    }
]

if __name__ == '__main__':
    merge('active-directory-defense', sims=SIMS, consoles=CONSOLES, missions=MISSIONS)
