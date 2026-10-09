# Bootcamp 1000% Build-Out — Progress Tracker
Started: 2026-10-08 ~21:55 EDT
Scope: 65 bootcamps, filling simulations + consoleSims + terminalMissions (+labs for ai-agent-sec)

## Batch assignments
- Batch 1 (acad, 10): acad-career, acad-cloud, acad-command, acad-cyber, acad-data, acad-forge, acad-hermetica, acad-math, acad-systems, acad-theory
- Batch 2 (cyber-full, 8): active-directory-defense, ai-agent-sec, cybernetics, secops-blue-team, security-graphs, tl-endpoint-ops, zero-trust, adaptive-foundations
- Batch 3 (con-only, 6): cisco-ccna, comptia-a-plus, comptia-network-plus, comptia-security-plus, isc2-cc, m365-endpoint-admin
- Batch 4 (cloud/devops, 8): aws-cloud-practitioner-plus, devops-zero-to-hire, devsecops-mastery, iac-terraform-gitops, k8s-cka-exceed, kubernetes-sre, platform-engineering, sre-practices
- Batch 5 (data/ai, 10): ai-lab, data-analyst-to-ml, data-science-certs, deep-learning, il12-ai-engineering, ml-defense, neuroai, nlp-advanced, nlp-engineering, quantum
- Batch 6 (dev/interview, 11): android-interview, embedded-interview, ios-interview, python-systems, alan-turing, aleks-ops-math, enochian-programming, electrician-apprentice, fde-training, humanmetrics, fullstack-desk
- Batch 7 (misc, 12): deep-work, edward-bernays, entrepreneurship, frontier-path, occult-esoteric, philosophy, quant-finance-ladder, quant-finance-math, roles-library, study-protocol, vendor-map, windows-admin

## Targets per bootcamp
- simulations: 5 (59 bootcamps)
- consoleSims: 4 (65 bootcamps)
- terminalMissions: 7 (59 bootcamps)
- labs: 5 (ai-agent-sec only)

## Progress log

### Batch 3 — consoleSims only (completed 2026-10-08 ~21:56 EDT)
24 consoleSims written, 4 per bootcamp, all original. All 6 bootcamps previously had NO `consoleSims` key — inserted as `consoleSims` (array of 4) immediately after the `simulations` key (matching tl-interview's key position). Every other key verified unchanged (JSON round-trip equality). Consoles/actions all verified against `_engine/consoles.js` action vocabulary; every task has a hint; all 24 sim ids unique globally (167 consoleSims total across site).

- cisco-ccna (4, switch-cli ×4): ccna-csim-1 "Carve out the guest VLAN" (d1: vlan 50 GUEST, assign Gi1/0/12, save), ccna-csim-2 "Trunk the uplink to the core" (d1: trunk Gi1/0/48, save), ccna-csim-3 "Voice and data on floor 2" (d2: vlan 20 VOICE, 2 port assigns, save), ccna-csim-4 "Overnight port move for Finance" (d3: vlan 40 FINANCE, assign, trunk, save)
- comptia-a-plus (4): aplus-csim-1 "Triage the morning ticket queue" (d1, ticketing: create P2 INC-9002, assign, in-progress), aplus-csim-2 "Document and lock down the cleanup" (d1, linux-desktop: create-file + chmod 600), aplus-csim-3 "Log the new workstation in the asset console" (d2, generic-web: 3 set-fields + submit), aplus-csim-4 "Close out the malware cleanup ticket" (d2, ticketing: create, add-note, resolve)
- comptia-network-plus (4): netplus-csim-1 "Open DNS for the new resolver" (d1, firewall: UDP+TCP 53 ACCEPT), netplus-csim-2 "Kill legacy Telnet at the border" (d2, firewall: OUTPUT+INPUT DROP 23), netplus-csim-3 "Stand up the management VLAN" (d2, switch-cli: vlan 99 MGMT, trunk, save), netplus-csim-4 "File the maintenance change ticket" (d1, ticketing: create, note, assign)
- comptia-security-plus (4): secplus-csim-1 "Harden the new web server" (d1, firewall: ACCEPT 443 + INPUT DROP), secplus-csim-2 "Contain the crypto-miner" (d2, siem: ack/assign ALT-102, isolate wkst-117), secplus-csim-3 "Block the RDP brute-forcer" (d2, firewall: DROP 3389 from attacker, ACCEPT from corp), secplus-csim-4 "Write the failed-login detector" (d3, siem: create-rule + escalate ALT-101)
- isc2-cc (4): cc-csim-1 "Triage the impossible-travel alert" (d1, siem: ack/assign ALT-101), cc-csim-2 "Report the lost access badge" (d1, ticketing: create, note, resolve), cc-csim-3 "Contain the exfiltrating backup server" (d2, siem: ack ALT-103, isolate, escalate), cc-csim-4 "Blocklist the SSH scanner" (d2, firewall: DROP 22 from scanner, ACCEPT 443 corp)
- m365-endpoint-admin (4): md102-csim-1 "Triage the stuck Autopilot device" (d1, ticketing), md102-csim-2 "Log the manually enrolled device" (d1, generic-web: 3 set-fields + submit), md102-csim-3 "Harden the golden image firewall" (d2, firewall: OUTPUT DROP 445, ACCEPT 443), md102-csim-4 "Close out the update-ring ticket" (d2, ticketing)

Builder/validation script: [batch3-consolems.py](sandbox://workspace/cert-bootcamps/.work/batch3-consolems.py)
