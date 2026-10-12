import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_common import merge

D1 = 'graph-defense'
D2 = 'sec-graphs'

SIMS = [
    {
        "id": "sec-graphs-sim-patch-priority",
        "title": "Patch the path, not the CVE score",
        "kind": "decide",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "Two critical CVEs, one maintenance window. CVE-A scores 9.8 on a print server; CVE-B scores 7.2 on a jump host one hop from the finance database. The attack graph says only one of them matters this week. Decide.",
        "steps": [
            {
                "symptom": "CVE-A (9.8): print server, no path to crown jewels (isolated VLAN, no trust edges). CVE-B (7.2): jump host with an active session edge to FIN-DB and an RDP edge from a compromised workstation.",
                "options": [
                    "Patch CVE-A first — 9.8 outranks 7.2",
                    "Patch CVE-B first — the attack graph shows a live 2-hop path from attacker foothold to the finance database; CVE-A has no path to anything valuable",
                    "Patch both simultaneously by extending the window",
                    "Patch neither and accept the risk"
                ],
                "correct": 1,
                "evidence": [
                    ["attack-graph.txt", "Path: WS-114(compromised) --RDP--> JUMP-01 --session--> FIN-DB. CVE-B enables privesc on JUMP-01. CVE-A host: degree 1, no edges toward crown jewels."],
                    ["policy.txt", "Patch prioritization: reachable paths to crown jewels outrank raw CVSS. A 9.8 on an island is less urgent than a 7.2 on the bridge."],
                ],
                "explain": "CVSS measures the vulnerability; the attack graph measures your exposure. Risk is the intersection — a critical bug with no path to value is noise, while a medium bug on the attack path is the incident waiting to happen."
            },
            {
                "symptom": "CVE-B patched. How do you prove the graph-driven choice was right, in terms leadership understands?",
                "options": [
                    "Report the CVSS scores patched",
                    "Show the before/after attack graph: the path to FIN-DB is severed, crown-jewel reachability dropped, and mean-time-to-patch on pathed vulnerabilities improved",
                    "Count the number of patches applied",
                    "Show the scanner is now green"
                ],
                "correct": 1,
                "evidence": [
                    ["graph-diff.txt", "Before: 3 distinct paths WS-114 -> FIN-DB. After: 0. Crown-jewel reachable nodes: 14 -> 6."],
                ],
                "explain": "Graph metrics translate security work into business risk: paths to the crown jewels are the unit of exposure. Fewer paths means less risk, regardless of how many CVEs the scanner counted."
            }
        ],
        "debrief": "Patch by path, not by score. The attack graph turns a 10,000-row vulnerability list into a ranked set of exposures — and every patch should visibly shrink the attacker's map.",
        "points": 15
    },
    {
        "id": "sec-graphs-sim-insider",
        "title": "The anomalous edges: insider or role change?",
        "kind": "troubleshoot",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "The user-asset graph flags m.alvarez: 14 new edges this week to finance systems she never touched before. Insider threat or legitimate change? Investigate.",
        "steps": [
            {
                "symptom": "14 new access edges: FIN-DB, payroll shares, finance file servers. All authenticated, all during business hours, all successful.",
                "options": [
                    "Insider threat — disable the account immediately",
                    "Correlate with the HR graph: check for role-change, transfer, or manager-approved access edges before judging the anomaly",
                    "Ignore — business hours means legitimate",
                    "The graph is wrong — delete the edges"
                ],
                "correct": 1,
                "evidence": [
                    ["hr-graph.txt", "m.alvarez transferred to Finance 9 days ago (HR edge: TRANSFER). Manager edge: approved access request REQ-2210 covering FIN-DB and payroll shares, 8 days ago."],
                    ["peer-graph.txt", "Her new peers average 16 finance edges; she has 14. Her edge pattern now matches the finance role cluster."],
                ],
                "explain": "Anomaly without context is just novelty. The HR graph (transfer + approved request) and the peer-group graph (matching the finance cluster) explain every edge. Graphs convict or acquit together — never read one in isolation."
            },
            {
                "symptom": "Legitimate transfer confirmed. But one edge still bothers you: a 2 AM access to the payroll archive, outside her peers' pattern. Next step?",
                "options": [
                    "Close the case — the transfer explains everything",
                    "Investigate the single unexplained edge: check the session details, source host, and whether the credentials were hers — one anomalous edge inside a legitimate pattern is exactly how real insider cases hide",
                    "Disable her account for the 2 AM access",
                    "Delete the payroll archive"
                ],
                "correct": 1,
                "evidence": [
                    ["session.txt", "2 AM session: source host WS-114 (not her laptop), authentication via cached credentials, files copied to USB. Her laptop was offline."],
                ],
                "explain": "The transfer explained 13 edges; the 14th came from a different host with her cached credentials at 2 AM. Real cases hide inside legitimate noise — the graph found the one edge that did not belong, and the session data confirmed it."
            }
        ],
        "debrief": "User-asset graphs do not detect 'bad people' — they detect edges that do not fit. Correlate across graphs (HR, peer, session) before acting, and remember: the clever insider hides one malicious edge inside a legitimate pattern.",
        "points": 20
    },
    {
        "id": "sec-graphs-sim-blast-radius",
        "title": "Map the blast radius: workstation compromised",
        "kind": "respond",
        "domain_id": D2,
        "difficulty": 3,
        "brief": "WS-207 is compromised with domain-user credentials. Before you contain, map what the attacker can reach from here. The graph is your battle map.",
        "steps": [
            {
                "symptom": "WS-207 (10.4.9.207) compromised. Compromised credential: svc-deploy (local admin on 40 hosts, per the privilege graph).",
                "options": [
                    "Isolate WS-207 immediately and figure out the rest later",
                    "Query the graph first: enumerate all nodes reachable from WS-207 via the svc-deploy credential edges, rank by crown-jewel proximity, then contain in priority order",
                    "Reset the svc-deploy password and consider it handled",
                    "Reimage WS-207"
                ],
                "correct": 1,
                "evidence": [
                    ["blast-radius.txt", "Reachable via svc-deploy: 40 hosts incl. BUILD-01 (CI), BACKUP-01, and JUMP-02 (1 hop from FIN-DB). WS-207 alone: 3 reachable nodes. With the credential: 40, including 2 crown-jewel-adjacent."],
                    ["ir-playbook.txt", "Blast-radius mapping precedes containment prioritization: you cannot defend what you have not enumerated. Containment order follows crown-jewel proximity."],
                ],
                "explain": "The compromised host is the least interesting node — the credential is the weapon. The graph shows the credential reaches 40 hosts including CI and backup infrastructure. Contain the crown-jewel-adjacent nodes first, not just the patient zero."
            },
            {
                "symptom": "Blast radius mapped: 40 hosts, JUMP-02 one hop from FIN-DB. What is the containment order?",
                "options": [
                    "Alphabetical — work through the list",
                    "JUMP-02 and BACKUP-01 first (crown-jewel-adjacent and recovery infrastructure), then BUILD-01 (CI), then the remaining hosts, with the svc-deploy credential rotated network-wide",
                    "WS-207 first since it was the entry point",
                    "Only contain the hosts showing active beacons"
                ],
                "correct": 1,
                "evidence": [
                    ["priority.txt", "Containment priority = crown-jewel proximity x infrastructure criticality. Backup infra is contained early: an attacker who owns backups owns your recovery."],
                ],
                "explain": "Graph-driven containment protects what matters most first: the paths to the crown jewels, then the infrastructure you need to recover (backups, CI), then the long tail. Entry point goes last — it is already known and watched."
            }
        ],
        "debrief": "In incident response the graph answers the only question that matters: from here, where can they go? Map the reachable set, rank by value, contain in that order — and always protect your recovery path.",
        "points": 20
    },
    {
        "id": "sec-graphs-sim-segmentation",
        "title": "Draw the microsegments from the graph",
        "kind": "decide",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "The network is flat: 600 hosts, one broadcast domain. The communication graph shows clear communities. Design the microsegmentation plan the graph is asking for.",
        "steps": [
            {
                "symptom": "Graph communities: finance cluster (38 hosts, dense internal edges), build/CI cluster (24 hosts), printers/IoT (60 hosts, chatty but isolated), user workstations (rest, sparse inter-edges).",
                "options": [
                    "One segment per host — maximum security",
                    "Segment along the graph communities: finance VLAN, CI VLAN, IoT VLAN, workstation VLAN — cutting the sparse inter-community edges and keeping the dense internal ones",
                    "Two segments: servers and everything else",
                    "Keep it flat but add a firewall"
                ],
                "correct": 1,
                "evidence": [
                    ["communities.txt", "Inter-community edges: finance<->workstations 12, ci<->workstations 8, iot<->anything 3. Cutting these edges removes 23 lateral paths while breaking zero legitimate workflows (all inter-community traffic is already proxied)."],
                    ["cost.txt", "Per-host microsegmentation: 600 policies to maintain. Community segmentation: 4 segments, 23 edge rules."],
                ],
                "explain": "The graph already drew the segments — communities are where the traffic naturally clusters. Cutting the sparse inter-community edges removes lateral paths at minimum operational cost. Per-host segmentation is theoretically perfect and practically unmaintainable."
            },
            {
                "symptom": "Segments approved. What validates the design before enforcement?",
                "options": [
                    "Enforce immediately — the graph is always right",
                    "Simulate first: run the proposed policy against 30 days of flow logs in the graph and confirm zero legitimate flows would break, then enforce in monitor mode, then block",
                    "Ask users if it will break anything",
                    "Enforce on Fridays"
                ],
                "correct": 1,
                "evidence": [
                    ["simulation.txt", "Policy simulation vs 30d flows: 0 legitimate flows denied, 23 lateral paths removed. Monitor mode 2 weeks: 0 complaints. Then enforced."],
                ],
                "explain": "Graphs model the past; simulation proves the future. Validate against real flow history, then monitor-mode before block-mode — segmentation that breaks the business gets rolled back and never tried again."
            }
        ],
        "debrief": "Microsegmentation is graph partitioning made physical. Let the communication graph draw the boundaries, validate against history, enforce gradually — and every segment should visibly shrink someone's attack paths.",
        "points": 15
    },
    {
        "id": "sec-graphs-sim-zt-policy",
        "title": "The vendor's edge to the finance database",
        "kind": "decide",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "A vendor support account requests a direct edge to FIN-DB 'for troubleshooting.' The Zero Trust policy engine asks you to approve or deny the relationship. Decide from the graph.",
        "steps": [
            {
                "symptom": "Requested edge: vendor-acct --troubleshoot--> FIN-DB (crown jewel). Vendor history: 2 sessions in 6 months, both to the app tier, never the DB. Contract: app-tier support only.",
                "options": [
                    "Approve — vendors need to troubleshoot",
                    "Deny the direct edge: no business justification, no historical pattern, crown-jewel target. Offer a time-boxed, recorded, approval-gated session through the PAM jump host instead",
                    "Approve permanently to avoid future tickets",
                    "Deny and block the vendor entirely"
                ],
                "correct": 1,
                "evidence": [
                    ["zt-policy.txt", "Relationship policies: edges to crown jewels require (1) contractual scope, (2) historical precedent or explicit approval, (3) session recording, (4) time bounds. This request meets zero of four."],
                    ["graph-history.txt", "vendor-acct edges, 6 months: app-web-01 (2 sessions). No DB edges ever."],
                ],
                "explain": "Zero Trust is a relationship decision, and the graph holds the evidence: no precedent, no contract scope, maximum-value target. Deny the standing edge; offer the gated, temporary, recorded alternative. The business need is met without the permanent risk."
            },
            {
                "symptom": "The vendor escalates: 'our SLA requires direct DB access.' Your final answer?",
                "options": [
                    "Grant it — the SLA settles it",
                    "Hold the denial and counter with the PAM-gated session plus a contract amendment process: if the SLA truly requires it, the requirement gets written, risk-accepted, and re-evaluated — not smuggled through a ticket",
                    "Grant it quietly and do not document",
                    "Escalate to the CEO"
                ],
                "correct": 1,
                "evidence": [
                    ["governance.txt", "Crown-jewel access changes require documented risk acceptance by the data owner. Verbal SLA claims do not override."],
                ],
                "explain": "Access to crown jewels is a governance decision with a named risk owner, not a support-ticket negotiation. The graph made the risk visible; the process makes the decision legitimate."
            }
        ],
        "debrief": "Zero Trust policies are graph edges with conditions. Every requested edge to a crown jewel must earn its place: precedent, contract, recording, time bounds — or it does not exist.",
        "points": 15
    }
]

CONSOLES = [
    {
        "id": "sec-graphs-console-vlan",
        "title": "Build the finance microsegment",
        "console": "switch-cli",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Create VLAN 40 'finance' for the finance community, assign port Gi1/0/12 to it, and save the config.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create VLAN 40 named 'finance'.",
                "validate": {"action": "create-vlan", "params": {"id": 40, "name": "finance"}},
                "hint": "In the switch CLI type: vlan 40 name finance"
            },
            {
                "id": "t2",
                "instruction": "Assign port Gi1/0/12 to VLAN 40.",
                "validate": {"action": "assign-port", "params": {"port": "Gi1/0/12", "vlan": 40}},
                "hint": "In the switch CLI type: interface Gi1/0/12 access vlan 40"
            },
            {
                "id": "t3",
                "instruction": "Save the switch configuration.",
                "validate": {"action": "save-config", "params": {}},
                "hint": "In the switch CLI type: write memory"
            }
        ],
        "debrief": "VLANs are microsegments made physical: the graph drew the community, the switch enforces the boundary."
    },
    {
        "id": "sec-graphs-console-firewall",
        "title": "Sever the lateral path",
        "console": "firewall",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "The graph shows a lateral path from the workstation segment (10.4.0.0/16) to the finance DB port. Drop that path on FORWARD and set the FORWARD default to DROP.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Add a rule dropping TCP port 1433 from 10.4.0.0/16 on FORWARD.",
                "validate": {"action": "add-rule", "params": {"chain": "FORWARD", "protocol": "tcp", "port": 1433, "source": "10.4.0.0/16", "action": "DROP"}},
                "hint": "Add a FORWARD rule: protocol tcp, port 1433, source 10.4.0.0/16, action DROP."
            },
            {
                "id": "t2",
                "instruction": "Set the FORWARD chain default policy to DROP.",
                "validate": {"action": "set-default-policy", "params": {"chain": "FORWARD", "policy": "DROP"}},
                "hint": "Set the default policy of the FORWARD chain to DROP."
            }
        ],
        "debrief": "Firewall rules are graph edges being deleted: each DROP removes a path the attacker could walk."
    },
    {
        "id": "sec-graphs-console-siem",
        "title": "Work the insider-threat alert",
        "console": "siem-dashboard",
        "domain_id": D1,
        "difficulty": 2,
        "brief": "Alert ALT-6100: 'Anomalous user-asset edges — m.alvarez'. Acknowledge it, assign it to the insider-threat analyst, and escalate to Tier 2.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Acknowledge alert ALT-6100.",
                "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-6100"}},
                "hint": "Click acknowledge on alert ALT-6100."
            },
            {
                "id": "t2",
                "instruction": "Assign alert ALT-6100 to analyst 'insider-threat'.",
                "validate": {"action": "assign-alert", "params": {"id": "ALT-6100", "analyst": "insider-threat"}},
                "hint": "Assign ALT-6100 to analyst insider-threat."
            },
            {
                "id": "t3",
                "instruction": "Escalate alert ALT-6100 to Tier 2.",
                "validate": {"action": "escalate", "params": {"id": "ALT-6100"}},
                "hint": "Click escalate on ALT-6100."
            }
        ],
        "debrief": "Graph-based alerts need graph-literate triage: acknowledge, assign a specialist owner, escalate with the edge context."
    },
    {
        "id": "sec-graphs-console-ticket",
        "title": "Ticket the segmentation rollout",
        "console": "ticketing",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Open a P2 change ticket for the finance microsegmentation rollout, assign it to netops, and move it to in-progress.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a P2 ticket titled 'Microsegment finance community — VLAN 40'.",
                "validate": {"action": "create-ticket", "params": {"title": "Microsegment finance community — VLAN 40", "priority": "P2"}},
                "hint": "Create a P2 ticket titled 'Microsegment finance community — VLAN 40'."
            },
            {
                "id": "t2",
                "instruction": "Assign the ticket to 'netops'.",
                "validate": {"action": "assign-ticket", "params": {"id": "1", "assignee": "netops"}},
                "hint": "Assign ticket 1 to netops."
            },
            {
                "id": "t3",
                "instruction": "Move the ticket to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "1", "status": "in-progress"}},
                "hint": "Update ticket 1 status to in-progress."
            }
        ],
        "debrief": "Segmentation is a change: ticketed, owned, and tracked like any production change."
    }
]

MISSIONS = [
    {
        "id": "sec-graphs-mission-read-edges",
        "title": "Read the edge list",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Read the attack-graph edge list to see the known relationships.",
        "objectives": ["Cat edges.csv and confirm the workstation entry"],
        "checks": [
            {
                "command_pattern": "^cat\\s+edges\\.csv",
                "expect_contains": "workstation",
                "hint": "Type: cat edges.csv"
            }
        ],
        "success_message": "Edge list read — the attacker's map is now yours."
    },
    {
        "id": "sec-graphs-mission-grep-paths",
        "title": "Find paths to the crown jewels",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "Search the path enumeration for any route reaching the finance database.",
        "objectives": ["Grep paths.txt for 'finance-db'"],
        "checks": [
            {
                "command_pattern": "^grep.*finance-db.*paths\\.txt",
                "expect_contains": "finance-db",
                "hint": "Type: grep finance-db paths.txt"
            }
        ],
        "success_message": "Crown-jewel paths found — these are the exposures to kill first."
    },
    {
        "id": "sec-graphs-mission-sort-risk",
        "title": "Sort nodes by risk score",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Sort the node risk list to see the highest-risk assets on top.",
        "objectives": ["Sort nodes-by-risk.txt"],
        "checks": [
            {
                "command_pattern": "^sort\\s+nodes-by-risk\\.txt",
                "expect_contains": "FIN-DB",
                "hint": "Type: sort nodes-by-risk.txt"
            }
        ],
        "success_message": "Nodes sorted — the riskiest assets are identified."
    },
    {
        "id": "sec-graphs-mission-head-paths",
        "title": "Preview the shortest paths",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Preview the shortest-path report to confirm its format.",
        "objectives": ["Head shortest-paths.txt"],
        "checks": [
            {
                "command_pattern": "^head\\s+shortest-paths\\.txt",
                "expect_contains": "hops",
                "hint": "Type: head shortest-paths.txt"
            }
        ],
        "success_message": "Path report confirmed — hop counts are the exposure metric."
    },
    {
        "id": "sec-graphs-mission-tail-audit",
        "title": "Check the latest graph audit entries",
        "domain_id": D1,
        "difficulty": 1,
        "brief": "Tail the graph audit log to see the most recent edge changes.",
        "objectives": ["Tail graph-audit.log"],
        "checks": [
            {
                "command_pattern": "^tail\\s+graph-audit\\.log",
                "expect_contains": "edge",
                "hint": "Type: tail graph-audit.log"
            }
        ],
        "success_message": "Latest edge changes reviewed — the graph is current."
    },
    {
        "id": "sec-graphs-mission-diff-snapshot",
        "title": "Diff the graph snapshots",
        "domain_id": D2,
        "difficulty": 2,
        "brief": "Compare yesterday's graph snapshot against today's to find new attack paths.",
        "objectives": ["Diff graph-old.txt against graph-new.txt"],
        "checks": [
            {
                "command_pattern": "^diff\\s+graph-old\\.txt\\s+graph-new\\.txt",
                "expect_contains": ">",
                "hint": "Type: diff graph-old.txt graph-new.txt"
            }
        ],
        "success_message": "New edges exposed — today's attack surface changes are visible."
    },
    {
        "id": "sec-graphs-mission-count-edges",
        "title": "Count the graph edges",
        "domain_id": D2,
        "difficulty": 1,
        "brief": "Count how many relationships the graph currently tracks.",
        "objectives": ["Count lines in edges.csv with wc"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+edges\\.csv",
                "expect_contains": "edges.csv",
                "hint": "Type: wc -l edges.csv"
            }
        ],
        "success_message": "Edge count captured — the graph's scale is quantified."
    }
]

if __name__ == '__main__':
    merge('security-graphs', sims=SIMS, consoles=CONSOLES, missions=MISSIONS)
