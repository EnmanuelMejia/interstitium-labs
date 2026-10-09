import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_common import merge

D1 = 'il11-zero-trust'
D2 = 'zerotrust'

SIMS = [
    {
        "id": "zt-sim-flat-network",
        "title": "Lateral movement in a flat network",
        "kind": "troubleshoot",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "One phished workstation led to 30 compromised hosts in 4 hours. The network is flat — no segmentation, no internal access controls. Find the architectural failure.",
        "steps": [
            {
                "symptom": "WS-118 phished 09:00. By 13:00: 30 hosts compromised, including two servers. No internal firewall rules, one broadcast domain, SMB open everywhere.",
                "options": [
                    "The users need more phishing training",
                    "Implicit trust architecture: once inside the perimeter, the attacker faced zero internal verification — the flat network treated every host as trusted",
                    "The antivirus failed",
                    "The firewall at the internet edge failed"
                ],
                "correct": 1,
                "evidence": [
                    ["network-map.txt", "Single VLAN. No internal segmentation. SMB/RDP permitted host-to-host without authentication beyond domain membership."],
                    ["timeline.txt", "09:00 phish -> 09:40 lateral to 5 hosts -> 11:00 18 hosts -> 13:00 30 hosts. No internal control ever challenged the movement."],
                ],
                "explain": "The perimeter held; the interior was undefended. Zero Trust's core insight: 'inside' is not a security property. Every lateral move should have faced an access decision — instead the attacker roamed a trusted interior."
            },
            {
                "symptom": "Architectural failure confirmed. What is the remediation that actually embodies 'never trust, always verify'?",
                "options": [
                    "A bigger perimeter firewall",
                    "Microsegmentation with identity-aware policy: every host-to-host flow requires authentication, authorization, and encryption — verified continuously, not once at the perimeter",
                    "More phishing training",
                    "Blocking SMB at the edge"
                ],
                "correct": 1,
                "evidence": [
                    ["zt-design.txt", "Target: identity-based microsegments; default-deny between segments; continuous verification of device posture and user risk on every connection."],
                ],
                "explain": "The fix moves the access decision from the perimeter to every connection. Microsegmentation plus identity-aware policy means the next phished workstation is an island, not a beachhead."
            }
        ],
        "debrief": "Flat networks convert one compromise into thirty. Zero Trust puts an access decision on every flow — verify explicitly, grant least privilege, assume breach — so lateral movement dies at the first hop.",
        "points": 15
    },
    {
        "id": "zt-sim-access-decision",
        "title": "The contractor and the production database",
        "kind": "decide",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "A contractor needs production database access for a 3-day migration. Their laptop is unmanaged, and they are working from a hotel network. Make the access decision.",
        "steps": [
            {
                "symptom": "Request: direct DB access, unmanaged device, untrusted network, 3-day window, production data.",
                "options": [
                    "Grant VPN access — the migration is urgent",
                    "Conditional access: managed-session via privileged access workstation or VDI, MFA with phishing-resistant factor, time-boxed just-in-time role, session recording, no direct network path from the unmanaged device to the DB",
                    "Deny outright — contractors never touch prod",
                    "Email them the credentials"
                ],
                "correct": 1,
                "evidence": [
                    ["risk.txt", "Unmanaged device + untrusted network + prod data = maximum risk combination. Direct access would violate every Zero Trust principle simultaneously."],
                    ["zt-policy.txt", "Access decisions evaluate identity + device posture + network + risk, every session. Unmanaged devices get mediated sessions (VDI/PAW), never direct paths to crown jewels."],
                ],
                "explain": "Zero Trust does not say 'no' — it says 'verify, then grant the minimum through the safest path.' The contractor gets the work done inside a recorded, time-boxed, mediated session; the unmanaged laptop never touches the database network."
            },
            {
                "symptom": "The contractor complains the VDI session is slow and asks for direct access 'just for an hour.' Your answer?",
                "options": [
                    "Grant the hour — it is only 60 minutes",
                    "Hold the line: investigate the VDI performance issue instead, and keep the mediated path — exceptions for convenience are how perimeters die",
                    "Grant direct access but watch the logs",
                    "Cancel the migration"
                ],
                "correct": 1,
                "evidence": [
                    ["perf.txt", "VDI slowness traced to hotel Wi-Fi, not the VDI stack. Workaround: async batch jobs submitted through the session. Direct access still denied."],
                ],
                "explain": "Every 'just this once' is a precedent. Fix the underlying friction (the network, the workflow) rather than the security control — convenience exceptions compound into architecture."
            }
        ],
        "debrief": "Zero Trust access decisions weigh all signals — identity, device, network, risk — and grant the minimum through the safest path. The policy bends for legitimate need via safer alternatives, never via exceptions.",
        "points": 15
    },
    {
        "id": "zt-sim-compromised-endpoint",
        "title": "EDR flags the CFO's laptop",
        "kind": "respond",
        "domain_id": D1,
        "difficulty": 3,
        "brief": "EDR: credential-dumping behavior on LAPTOP-CFO at 10:15. The CFO is in back-to-back meetings and unreachable. The device holds cached credentials for finance systems. Respond.",
        "steps": [
            {
                "symptom": "EDR high-severity: lsass access from an unsigned binary on LAPTOP-CFO. User context: cfo. Device compliance: healthy, 2 hours ago.",
                "options": [
                    "Wait for the CFO to confirm — it might be legitimate",
                    "Assume breach: isolate the device, revoke the user's sessions and tokens, force step-up re-authentication on finance systems — then investigate",
                    "Wipe the laptop immediately",
                    "Ignore — the device was compliant"
                ],
                "correct": 1,
                "evidence": [
                    ["edr.txt", "10:15 unsigned process read lsass memory. 10:16 outbound connection to unknown IP. No IT ticket for admin work on this device."],
                    ["zt-playbook.txt", "Continuous verification: a healthy attestation from 2 hours ago is stale the moment behavior contradicts it. Trust is re-evaluated on every signal."],
                ],
                "explain": "Assume breach means the alert is guilty until the investigation acquits it — especially with finance-system credentials at stake. Isolation plus session revocation contains the blast radius in minutes; the CFO's meeting is not worth the domain."
            },
            {
                "symptom": "Device isolated, sessions revoked. Investigation: the CFO's teenager installed a 'game mod' that bundled the dumper. What completes the response?",
                "options": [
                    "Unisolate and apologize",
                    "Verify no lateral movement or data access occurred during the window, rotate the exposed credentials, re-image the device, and enforce application control so unsigned binaries cannot run on privileged devices",
                    "Ban the teenager from the laptop",
                    "Buy the CFO a new laptop"
                ],
                "correct": 1,
                "evidence": [
                    ["scope.txt", "Window 10:15–10:22. No lateral movement detected; one finance share enumerated, no files opened. Cached credentials rotated."],
                ],
                "explain": "Scope the window, rotate what was exposed, rebuild trust in the device (re-image), and close the control gap (application control on high-value endpoints). The root cause is architectural: privileged users' devices must not run unsigned code."
            }
        ],
        "debrief": "Continuous verification means trust expires on evidence, not on schedule. Isolate fast, revoke sessions, scope the window, rebuild the device — and make the control that would have prevented it permanent.",
        "points": 20
    },
    {
        "id": "zt-sim-identity-gap",
        "title": "The legacy protocol bypassing MFA",
        "kind": "troubleshoot",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "MFA is enforced everywhere — yet the auth logs show successful logons with no MFA challenge from a legacy inventory system. Find the bypass.",
        "steps": [
            {
                "symptom": "200 successful logons this month with auth method 'NTLM', zero MFA challenges, all from the legacy inventory app's service account.",
                "options": [
                    "The MFA server is misconfigured",
                    "Legacy protocol bypass: the app authenticates via NTLM, which never triggers the MFA policy — the 'MFA everywhere' claim has a protocol-shaped hole",
                    "Users are sharing MFA tokens",
                    "The logs are wrong"
                ],
                "correct": 1,
                "evidence": [
                    ["auth-log.txt", "200 logons: protocol NTLMv2, MFA challenge: none (policy only applies to modern auth flows). Account: SVC-inventory, member of Domain Users, interactive logon rights."],
                    ["mfa-policy.txt", "MFA enforced on: web SSO, VPN, RDP gateway. Not covered: NTLM, legacy IMAP/SMTP auth, direct LDAP binds."],
                ],
                "explain": "MFA policies are only as complete as the protocols they cover. Legacy protocols that predate modern auth silently bypass the control — the inventory app has a permanent MFA exemption nobody approved."
            },
            {
                "symptom": "Bypass confirmed. What is the fix that honors 'verify explicitly'?",
                "options": [
                    "Disable the inventory app",
                    "Block legacy auth at the identity provider, migrate the app to modern auth (or isolate it behind an app proxy with MFA), and audit all accounts for legacy-protocol usage",
                    "Add a second password for the service account",
                    "Monitor the NTLM logons and hope"
                ],
                "correct": 1,
                "evidence": [
                    ["remediation.txt", "NTLM blocked tenant-wide; inventory app moved behind app proxy with pre-auth MFA; legacy-auth audit found 3 more service accounts, all remediated."],
                ],
                "explain": "Verify explicitly means no protocol gets a free pass. Kill legacy auth, give the app a modern path (or a proxied one), and audit for the same hole elsewhere — bypasses travel in packs."
            }
        ],
        "debrief": "Audit your MFA coverage by protocol, not by policy document. Every legacy auth path is an MFA bypass until proven otherwise — find them with the logs before the attacker does.",
        "points": 15
    },
    {
        "id": "zt-sim-microsegment",
        "title": "Segment the three-tier app",
        "kind": "decide",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "The customer portal is three tiers — web, app, DB — on one flat segment. Design the Zero Trust segmentation: which flows are allowed, and what verifies them?",
        "steps": [
            {
                "symptom": "Current: web/app/DB all on 10.2.0.0/16, any-to-any. DB holds customer PII.",
                "options": [
                    "Put a firewall between the app and the internet",
                    "Three microsegments with explicit allow edges: internet->web (443), web->app (defined API port), app->DB (DB port, app identity only); default-deny everything else; every edge requires mutual TLS with workload identity",
                    "Move the DB to the cloud",
                    "Encrypt the database"
                ],
                "correct": 1,
                "evidence": [
                    ["flow-log.txt", "Legitimate flows: 443 in, web->app:8443, app->db:5432. Everything else (all other observed flows): scanning, admin RDP, backup agents — each needs its own explicit edge or it dies."],
                    ["zt-principles.txt", "Microsegmentation + explicit allow + workload identity + encryption on every edge. The DB never sees a packet that the app tier did not cryptographically vouch for."],
                ],
                "explain": "The design follows the actual traffic: allow the three legitimate edges, deny the universe, and authenticate the workloads (not just the network location) on each edge. The DB becomes reachable only through the app's identity."
            },
            {
                "symptom": "The backup agent needs DB access but lives outside the app segment. How does it fit the model?",
                "options": [
                    "Open the DB segment to the backup VLAN",
                    "Give the backup workload its own identity and an explicit, scheduled edge: backup-identity -> DB on the backup port, only during the backup window, logged and alerted otherwise",
                    "Run backups from the app tier",
                    "Skip backups for the DB"
                ],
                "correct": 1,
                "evidence": [
                    ["edge-spec.txt", "Edge: backup-svc -> db:5432, window 02:00–03:00, mTLS workload identity, all other times: deny + alert."],
                ],
                "explain": "Zero Trust does not forbid the backup — it gives it a named, bounded, verified edge instead of a hole in the segment. Every exception becomes an explicit edge with conditions, never a flat 'allow.'"
            }
        ],
        "debrief": "Microsegmentation is allowlisting for network flows: explicit edges between verified workload identities, default-deny between them. Every 'exception' is just another explicit edge with conditions.",
        "points": 15
    }
]

CONSOLES = [
    {
        "id": "zt-console-default-deny",
        "title": "Enforce default-deny on the segment",
        "console": "firewall",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "Allow the identity provider (10.0.5.10) to reach TCP 443 on INPUT, then set the INPUT default policy to DROP.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Add a rule accepting TCP port 443 from 10.0.5.10 on INPUT.",
                "validate": {"action": "add-rule", "params": {"chain": "INPUT", "protocol": "tcp", "port": 443, "source": "10.0.5.10", "action": "ACCEPT"}},
                "hint": "Add an INPUT rule: protocol tcp, port 443, source 10.0.5.10, action ACCEPT."
            },
            {
                "id": "t2",
                "instruction": "Set the INPUT chain default policy to DROP.",
                "validate": {"action": "set-default-policy", "params": {"chain": "INPUT", "policy": "DROP"}},
                "hint": "Set the default policy of the INPUT chain to DROP."
            }
        ],
        "debrief": "Default-deny with explicit allows is the firewall expression of Zero Trust: everything not permitted is denied."
    },
    {
        "id": "zt-console-segment-db",
        "title": "Segment the database tier",
        "console": "switch-cli",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Create VLAN 30 'prod-db', assign port Gi1/0/24 to it, and save the config.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create VLAN 30 named 'prod-db'.",
                "validate": {"action": "create-vlan", "params": {"id": 30, "name": "prod-db"}},
                "hint": "In the switch CLI type: vlan 30 name prod-db"
            },
            {
                "id": "t2",
                "instruction": "Assign port Gi1/0/24 to VLAN 30.",
                "validate": {"action": "assign-port", "params": {"port": "Gi1/0/24", "vlan": 30}},
                "hint": "In the switch CLI type: interface Gi1/0/24 access vlan 30"
            },
            {
                "id": "t3",
                "instruction": "Save the switch configuration.",
                "validate": {"action": "save-config", "params": {}},
                "hint": "In the switch CLI type: write memory"
            }
        ],
        "debrief": "The database tier gets its own segment: the first physical step toward 'the DB never sees an unverified packet.'"
    },
    {
        "id": "zt-console-isolate",
        "title": "Isolate the compromised endpoint",
        "console": "siem-dashboard",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Alert ALT-7200: credential dumping on LAPTOP-CFO. Isolate the host, acknowledge the alert, and escalate to Tier 2.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Isolate host LAPTOP-CFO.",
                "validate": {"action": "isolate-host", "params": {"host": "LAPTOP-CFO"}},
                "hint": "Use isolate-host on LAPTOP-CFO."
            },
            {
                "id": "t2",
                "instruction": "Acknowledge alert ALT-7200.",
                "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-7200"}},
                "hint": "Click acknowledge on alert ALT-7200."
            },
            {
                "id": "t3",
                "instruction": "Escalate alert ALT-7200 to Tier 2.",
                "validate": {"action": "escalate", "params": {"id": "ALT-7200"}},
                "hint": "Click escalate on ALT-7200."
            }
        ],
        "debrief": "Assume breach in action: isolate first, then work the alert queue — trust is re-evaluated on evidence."
    },
    {
        "id": "zt-console-ticket",
        "title": "Ticket the legacy-auth remediation",
        "console": "ticketing",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Open a P2 ticket to remediate the NTLM bypass, assign it to identity-engineering, and move it to in-progress.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a P2 ticket titled 'Remediate NTLM MFA bypass — SVC-inventory'.",
                "validate": {"action": "create-ticket", "params": {"title": "Remediate NTLM MFA bypass — SVC-inventory", "priority": "P2"}},
                "hint": "Create a P2 ticket titled 'Remediate NTLM MFA bypass — SVC-inventory'."
            },
            {
                "id": "t2",
                "instruction": "Assign the ticket to 'identity-engineering'.",
                "validate": {"action": "assign-ticket", "params": {"id": "1", "assignee": "identity-engineering"}},
                "hint": "Assign ticket 1 to identity-engineering."
            },
            {
                "id": "t3",
                "instruction": "Move the ticket to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "1", "status": "in-progress"}},
                "hint": "Update ticket 1 status to in-progress."
            }
        ],
        "debrief": "Identity gaps are engineering work: ticketed, owned, and tracked to closure."
    }
]

MISSIONS = [
    {
        "id": "zt-mission-dns-check",
        "title": "Verify the identity provider DNS",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Confirm the identity provider resolves correctly via DNS.",
        "objectives": ["Dig the idp host record"],
        "checks": [
            {
                "command_pattern": "^dig\\s+idp\\.corp\\.local",
                "expect_contains": "idp.corp.local",
                "hint": "Type: dig idp.corp.local"
            }
        ],
        "success_message": "Identity provider DNS verified — auth traffic has a valid target."
    },
    {
        "id": "zt-mission-grep-denied",
        "title": "Find the denied access attempts",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Search the access log for denied requests — the default-deny policy in action.",
        "objectives": ["Grep access.log for 'DENIED'"],
        "checks": [
            {
                "command_pattern": "^grep\\s+DENIED\\s+access\\.log",
                "expect_contains": "DENIED",
                "hint": "Type: grep DENIED access.log"
            }
        ],
        "success_message": "Denied attempts found — verify each one was correctly refused."
    },
    {
        "id": "zt-mission-read-policy",
        "title": "Read the access policy",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Read the Zero Trust policy file to confirm the default-deny stance.",
        "objectives": ["Cat zt-policy.json and confirm the default action"],
        "checks": [
            {
                "command_pattern": "^cat\\s+zt-policy\\.json",
                "expect_contains": "deny",
                "hint": "Type: cat zt-policy.json"
            }
        ],
        "success_message": "Policy confirmed — default-deny with explicit allows."
    },
    {
        "id": "zt-mission-verify-agent",
        "title": "Verify the endpoint agent installer",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Hash the endpoint agent installer before deployment.",
        "objectives": ["Run sha256sum on zt-agent-installer.exe"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+zt-agent-installer\\.exe",
                "expect_contains": "zt-agent-installer.exe",
                "hint": "Type: sha256sum zt-agent-installer.exe"
            }
        ],
        "success_message": "Agent installer hash captured — verify against the vendor value."
    },
    {
        "id": "zt-mission-sort-denied",
        "title": "Sort the denied-source list",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Sort the denied source IPs to spot repeat offenders.",
        "objectives": ["Sort denied-ips.txt"],
        "checks": [
            {
                "command_pattern": "^sort\\s+denied-ips\\.txt",
                "expect_contains": "185.220",
                "hint": "Type: sort denied-ips.txt"
            }
        ],
        "success_message": "Denied sources sorted — repeat offenders identified."
    },
    {
        "id": "zt-mission-diff-policy",
        "title": "Diff the policy revisions",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Compare the previous Zero Trust policy against the current one.",
        "objectives": ["Diff zt-policy-v1.json against zt-policy-v2.json"],
        "checks": [
            {
                "command_pattern": "^diff\\s+zt-policy-v1\\.json\\s+zt-policy-v2\\.json",
                "expect_contains": ">",
                "hint": "Type: diff zt-policy-v1.json zt-policy-v2.json"
            }
        ],
        "success_message": "Policy changes reviewed — every new allow is explicit."
    },
    {
        "id": "zt-mission-ping-idp",
        "title": "Check identity provider reachability",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Ping the identity provider to confirm the auth path is alive.",
        "objectives": ["Ping idp.corp.local"],
        "checks": [
            {
                "command_pattern": "^ping\\s+idp\\.corp\\.local",
                "expect_contains": "idp.corp.local",
                "hint": "Type: ping idp.corp.local"
            }
        ],
        "success_message": "Identity provider reachable — the auth path is alive."
    }
]

if __name__ == '__main__':
    merge('zero-trust', sims=SIMS, consoles=CONSOLES, missions=MISSIONS)
