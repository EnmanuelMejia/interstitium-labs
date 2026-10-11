"""IL-27 Track F: Zero Trust & Security Operations (IL27-M28..M33)."""

MODULES_F = [
{
"id": "IL27-M28",
"code": "IL-27",
"title": "Zero Trust Architecture Principles",
"summary": "The strategy behind the job title: NIST SP 800-207 tenets, CISA maturity model, and applying Zero Trust to real infrastructure. Interview-critical - this is the company's language. You need this for -> M29/M30 and every interview answer.",
"objectives": [
"State the NIST SP 800-207 tenets and apply each to infrastructure.",
"Place an org on the CISA Zero Trust Maturity Model (Traditional/Initial/Advanced/Optimal).",
"Design identity, device, and network controls per Zero Trust.",
"Explain what Zero Trust does NOT mean (no product, no rip-and-replace).",
"Answer 'what is Zero Trust' in 60 seconds, 5 minutes, and 30 minutes."
],
"notes": [
{"title": "NIST SP 800-207: the tenets",
"body": "Zero Trust = 'never trust, always verify' applied to every access decision. NIST SP 800-207 (the authoritative definition - read it, it's public) tenets: (1) All data sources and computing services are resources. (2) All communication is secured. (3) Access to individual resources is granted per-session. (4) Access is determined by dynamic policy (identity, device, behavior). (5) The enterprise monitors the integrity and security posture of all assets. (6) Authentication/authorization are dynamic and strictly enforced before access. (7) The enterprise collects as much information as possible to improve posture.\n\nKey shift: identity becomes the perimeter. Network location stops being a trust signal - a domain-joined laptop on the LAN gets the same verification as one at a coffee shop. For infrastructure teams this means: every service needs identity-aware access, every device needs health attestation, every flow needs policy.\n\nWhat it's NOT: not a product you buy, not 'no VPN', not rip-and-replace. It's an architecture you migrate toward - microsegmentation, strong identity, device compliance, least privilege - each a project, each valuable alone."
},
{"title": "CISA maturity model: where are we?",
"body": "CISA's Zero Trust Maturity Model: 5 pillars (Identity, Devices, Networks, Applications, Data) × 3 cross-cutting (Visibility/Analytics, Automation/Orchestration, Governance) across 4 stages: Traditional -> Initial -> Advanced -> Optimal. Use it to ASSESS, not to impress: 'our identity is Advanced (phishing-resistant MFA, Conditional Access), our networks are Initial (flat VLANs, no microsegmentation)'.\n\nTypical enterprise reality: Identity leads (MFA, CA), Devices follow (Intune compliance), Networks lag (flat networks are everywhere), Data trails (classification is hard). Your infrastructure roadmap IS the maturity climb: each M28-M33 module moves a pillar.\n\nInterview power: walking in with 'here's how I'd assess your maturity and the first three projects I'd run' turns a Q&A into a working session. Assess honestly - claiming Optimal anything invites hard questions."
},
{"title": "Applying it: the infrastructure playbook",
"body": "Identity: phishing-resistant MFA (FIDO2/Windows Hello), Conditional Access everywhere, no standing admin rights (PIM/JIT). Devices: compliance-gated access (M25), allowlisting on fixed functions (M27), EDR everywhere. Networks: microsegment (M29), private access over VPN-sprawl, DNS-layer policy. Applications: SSO everything, kill legacy auth. Data: classify, encrypt, DLP on the crown jewels.\n\nThe 60-second answer: 'Zero Trust means every access decision verifies identity, device health, and context - no implicit trust from network location. Practically: strong MFA, compliant devices, microsegmentation, and least-privilege access, measured against the CISA maturity model.'\n\nThe 30-minute version adds: your assessment of THEIR maturity, the project sequence (identity first - cheapest wins), metrics (MFA coverage %, compliant device %, segmented workloads), and honest scope ('this is a multi-year architecture, not a product install')."
}
],
"cards": [
{"front": "Zero Trust in one sentence", "back": "Never trust, always verify - every access decision checks identity, device, context."},
{"front": "NIST SP 800-207 tenet count + core idea", "back": "7 tenets; identity is the perimeter, access per-session by dynamic policy."},
{"front": "CISA ZTMM pillars", "back": "Identity, Devices, Networks, Applications, Data (+ visibility, automation, governance)."},
{"front": "Maturity stages", "back": "Traditional -> Initial -> Advanced -> Optimal."},
{"front": "Typical pillar order (leads to lags)", "back": "Identity -> Devices -> Networks -> Data."},
{"front": "Zero Trust is NOT", "back": "A product, 'no VPN', or rip-and-replace - it's an architecture you migrate toward."},
{"front": "First project in a ZT rollout", "back": "Identity: phishing-resistant MFA + Conditional Access (cheapest wins)."},
{"front": "Metrics that prove progress", "back": "MFA coverage %, compliant devices %, segmented workloads, legacy auth blocked."}
],
"quiz": [
{"q": "A vendor says 'buy our box for Zero Trust'. You:", "choices": ["Zero Trust is an architecture, not a product - assess against NIST/CISA first", "Buy two", "It's true", "Ask for a discount"], "answer": 0, "index": 0, "explain": "No product confers Zero Trust; it's designed and measured."},
{"q": "Domain laptop on LAN vs same laptop at a cafe. Zero Trust says:", "choices": ["Same verification - location is not a trust signal", "LAN = trusted", "Cafe = blocked always", "VPN fixes everything"], "answer": 0, "index": 0, "explain": "Identity and device health decide, not network location."},
{"q": "Org has MFA everywhere but flat networks. CISA assessment?", "choices": ["Identity Advanced, Networks Traditional/Initial - report per pillar", "Optimal overall", "Traditional overall", "Can't assess"], "answer": 0, "index": 0, "explain": "Pillars mature independently; assess each honestly."},
{"q": "Per-session access (tenet 3) means:", "choices": ["Each resource access is authorized individually - no broad network trust", "One login per day", "Sessions never expire", "VPN always on"], "answer": 0, "index": 0, "explain": "Granular, per-resource authorization."},
{"q": "Dynamic policy (tenet 4) uses:", "choices": ["Identity, device posture, behavior/risk signals", "IP address only", "Time of day only", "Nothing - static rules"], "answer": 0, "index": 0, "explain": "Multiple live signals drive each decision."},
{"q": "Cheapest first Zero Trust win?", "choices": ["Enforce phishing-resistant MFA + Conditional Access baselines", "Replace the network", "New firewalls", "Hire consultants"], "answer": 0, "index": 0, "explain": "Identity controls are high-ROI and fast."},
{"q": "'We have Zero Trust because we removed VPN.' Problem?", "choices": ["Removing VPN isn't Zero Trust - verification architecture is", "Correct", "VPN is required", "Nothing"], "answer": 0, "index": 0, "explain": "Zero Trust is what replaces implicit trust, not one tool removal."},
{"q": "Governance cross-cutting capability means:", "choices": ["Policies, risk management, and compliance overseeing all pillars", "More meetings", "A committee", "Paperwork"], "answer": 0, "index": 0, "explain": "Governance steers the whole program."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M29", "IL27-M30"],
"drills": [
{"id": "m28-drill-zt", "title": "Zero Trust Drill",
"items": [
{"prompt": "60-second definition", "answer": "Never trust, always verify: identity + device + context per access", "explain": "The elevator answer."},
{"prompt": "Authoritative definition doc", "answer": "NIST SP 800-207", "explain": "Read the source."},
{"prompt": "Assessment framework", "answer": "CISA Zero Trust Maturity Model", "explain": "5 pillars, 4 stages."},
{"prompt": "Identity is the new ___", "answer": "Perimeter", "explain": "Location stopped being trust."},
{"prompt": "First project", "answer": "Phishing-resistant MFA + Conditional Access", "explain": "Cheapest wins first."},
{"prompt": "Vendor sells 'Zero Trust in a box'", "answer": "Architecture, not a product - assess first", "explain": "No magic boxes."}
]}
],
"handsOnLab": {
"id": "m28-lab",
"title": "Assess & Pitch: Zero Trust maturity for a fictional org",
"brief": "Perform a CISA-model assessment and build the 90-day plan.",
"steps": [
"Read NIST SP 800-207 tenets (skim) and the CISA ZTMM one-pager.",
"Score a fictional 500-seat org per pillar (invent realistic evidence).",
"Identify the 3 highest-ROI projects with effort/impact estimates.",
"Write the 60-second, 5-minute, and 30-minute versions of 'what is Zero Trust'.",
"Define metrics for each project (MFA %, compliant %, segmented workloads).",
"Present it as a 5-slide pitch (record yourself or present to a peer)."
],
"deliverable": "Maturity assessment + 90-day plan + three versions of the pitch.",
"checkpoint": "You can assess, plan, and sell Zero Trust like a practitioner."
},
"mockTask": {"id": "m28-mock", "type": "choice",
"q": "Interview: 'What is Zero Trust?'",
"choices": ["Never trust, always verify: every access decision checks identity, device health, and context per NIST SP 800-207; I'd assess maturity per CISA pillar and start with identity wins", "It's a firewall product", "No more passwords", "It's just VPN replacement"],
"answer": 0, "explain": "Definition + framework + action - the complete answer."},
"crossLinks": ["il11-zero-trust-foundations--zt-nist-tenets", "il11-zero-trust-foundations--zt-cisa-maturity", "il11-zero-trust-foundations--zt-default-deny"],
"videos": "VIDEOS_M28",
"estimatedMinutes": 300,
"fastTrackEligible": True
},
{
"id": "IL27-M29",
"code": "IL-27",
"title": "Microsegmentation & Network Access Control",
"summary": "Shrink the blast radius: VLAN/ACL segmentation, host firewalls, 802.1X/NAC, and lateral-movement defense. Interview-critical - segmentation is where infrastructure meets Zero Trust. You need this for -> M28/M30.",
"objectives": [
"Design a segmented network (tiers, VLANs, ACLs) and justify each boundary.",
"Explain east-west vs north-south traffic and why east-west matters.",
"Deploy 802.1X concepts: supplicant, authenticator, RADIUS/NPS.",
"Use Windows Firewall with Advanced Security as a segmentation tool.",
"Detect and respond to lateral movement patterns."
],
"notes": [
{"title": "Segmentation design",
"body": "Flat network = one compromised host reaches everything (the ransomware dream). Segmentation draws boundaries: user VLANs, server VLANs, management VLAN, DMZ, IoT/printer VLAN, guest. Between them: ACLs or firewall policy - default deny, allow only required flows.\n\nEast-west (server-to-server, host-to-host) is where lateral movement lives - and where most orgs have ZERO inspection. North-south (in/out of the datacenter) gets the firewall love. Microsegmentation pushes policy to the workload/host itself (host firewall rules per role) - the network equivalent of allowlisting.\n\nDesign method: map required flows first (app->DB:1433, users->app:443, admins->mgmt:3389/22), then write allow rules for exactly those, deny the rest. Document each rule's owner and purpose - undocumented firewall rules are how 'temporary' becomes permanent."
},
{"title": "NAC and 802.1X",
"body": "NAC answers 'should this device be on my network at all?' 802.1X: port-based authentication - supplicant (device) -> authenticator (switch/AP) -> authentication server (RADIUS/NPS talking to AD). Success = VLAN assignment by policy (employees->corp VLAN, printers->printer VLAN, unknowns->quarantine).\n\nRADIUS/NPS on Windows Server: policies by group, device type, health (with NAP remnants or modern compliance checks). MAB (MAC auth bypass) for dumb devices (printers, cameras) - MAC allowlist, weak but better than open ports.\n\nReality check: full 802.1X is a project (certificates, switch config, exception handling). Start with: DHCP snooping + DAI on switches (kills basic spoofing), guest isolation, and a plan. NAC maturity climbs with the org."
},
{"title": "Host firewalls and lateral defense",
"body": "Windows Firewall with Advanced Security: per-profile (domain/private/public), per-rule (program/port/IP scope), manageable by GPO at fleet scale. The microsegmentation workhorse: servers allow only their role's ports from only their tier's subnets. 'Allow SQL 1433 from app-tier only' beats any VLAN alone.\n\nLateral movement patterns to know: SMB/PSExec hopping, RDP jumps, WMI, credential dumping (LSASS), pass-the-hash. Defenses layer: LAPS (M26 - no shared creds), Credential Guard, network segmentation (this module), EDR (M32), and log correlation (M33's SIEM feeds).\n\nTest it: from a lab workstation, try to reach a 'server' on another VLAN - verify the deny, check the firewall log, then add the allow rule and verify. Segmentation you haven't tested is decoration."
}
],
"cards": [
{"front": "East-west vs north-south", "back": "East-west: host-to-host (lateral movement). North-south: in/out of DC."},
{"front": "Microsegmentation = ?", "back": "Policy at the workload/host level - network allowlisting."},
{"front": "802.1X roles", "back": "Supplicant (device) -> authenticator (switch) -> RADIUS server."},
{"front": "MAB is for", "back": "Dumb devices (printers/cameras) - MAC-based, weak but better than open."},
{"front": "Windows Firewall profiles", "back": "Domain, Private, Public - different rule sets per network."},
{"front": "First segmentation quick wins", "back": "DHCP snooping + DAI, guest isolation, tier VLANs with ACLs."},
{"front": "Lateral movement vectors", "back": "SMB/PSExec, RDP, WMI, LSASS dumping, pass-the-hash."},
{"front": "Undocumented firewall rules become", "back": "Permanent - document owner and purpose per rule."}
],
"quiz": [
{"q": "Ransomware spreads host-to-host in minutes. Missing control?", "choices": ["East-west segmentation + host firewall policy", "Bigger firewall", "More antivirus", "Faster internet"], "answer": 0, "index": 0, "explain": "Lateral movement needs lateral controls."},
{"q": "Unknown device plugs into a wall jack. With 802.1X:", "choices": ["Quarantine VLAN or no access until authenticated", "Full access", "Internet only", "It depends on mood"], "answer": 0, "index": 0, "explain": "Port-level auth gates network entry."},
{"q": "Printer needs network but can't do 802.1X. Use:", "choices": ["MAB (MAC bypass) on a dedicated printer VLAN", "Corp VLAN open", "No network", "Wi-Fi password"], "answer": 0, "index": 0, "explain": "Weak auth + isolated VLAN = pragmatic."},
{"q": "App server should take SQL only from app tier. Implement?", "choices": ["Host firewall rule: 1433 from app-tier subnet only", "Open 1433 everywhere", "Disable firewall", "New VLAN only"], "answer": 0, "index": 0, "explain": "Workload-level policy = microsegmentation."},
{"q": "DHCP snooping + DAI prevent:", "choices": ["Rogue DHCP and ARP spoofing on the LAN", "Phishing", "Malware", "DDoS"], "answer": 0, "index": 0, "explain": "Switch-level anti-spoofing basics."},
{"q": "Design order for firewall rules:", "choices": ["Map required flows first, then allow-list them, deny rest", "Deny all first", "Allow all first", "Copy another company"], "answer": 0, "index": 0, "explain": "Flows drive rules; documentation per rule."},
{"q": "Guest Wi-Fi design must include:", "choices": ["Isolation from corp + captive portal + rate limits", "Corp VLAN access", "No password", "Full LAN"], "answer": 0, "index": 0, "explain": "Guests get internet, nothing else."},
{"q": "You haven't tested a segment boundary. It is:", "choices": ["Decoration - verify deny then allow", "Fine", "Secure by design", "Compliant"], "answer": 0, "index": 0, "explain": "Test every boundary both ways."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M28", "IL27-M30"],
"drills": [
{"id": "m29-drill-seg", "title": "Segmentation Drill",
"items": [
{"prompt": "Ransomware spreading host-to-host", "answer": "East-west segmentation + host firewalls", "explain": "Lateral controls."},
{"prompt": "Device auth at the switch port", "answer": "802.1X (supplicant/authenticator/RADIUS)", "explain": "Port-based NAC."},
{"prompt": "Printer can't do 802.1X", "answer": "MAB on isolated VLAN", "explain": "Pragmatic exception."},
{"prompt": "SQL only from app tier", "answer": "Host firewall scoped rule", "explain": "Microsegmentation."},
{"prompt": "Rogue DHCP on LAN", "answer": "DHCP snooping", "explain": "Switch security."},
{"prompt": "Untested boundary = ?", "answer": "Decoration", "explain": "Verify both ways."}
]}
],
"handsOnLab": {
"id": "m29-lab",
"title": "Segment Lab: VLANs + host firewalls + test",
"brief": "Build segmented lab networks and prove the boundaries work.",
"steps": [
"Create 3 VLANs (users/servers/mgmt) on a managed switch or virtual equivalent.",
"Place lab VMs per tier; verify inter-VLAN routing through ACLs.",
"Write allow-rules for required flows only (RDP mgmt->servers, app->DB); deny rest.",
"Configure Windows Firewall GPO: servers allow role ports from tier subnets only.",
"Attack-test: from user VLAN, attempt server access - verify deny + log.",
"Document the flow matrix: source, dest, port, rule, owner."
],
"deliverable": "Segment diagram + flow matrix + test evidence (deny and allow).",
"checkpoint": "You design, implement, and verify segmentation - not just draw it."
},
"mockTask": {"id": "m29-mock", "type": "choice",
"q": "Interview: 'How would you segment our flat network?'",
"choices": ["Map required flows first, tier VLANs (user/server/mgmt/DMZ/guest), default-deny ACLs between them, host firewalls per role, 802.1X plan, test every boundary", "More VLANs randomly", "One big firewall", "It's fine flat"],
"answer": 0, "explain": "Flows-first, layered, verified - the professional sequence."},
"crossLinks": ["il11-network-crypto-foundations--zt-osi-tcpip"],
"videos": "VIDEOS_M29",
"estimatedMinutes": 300,
"fastTrackEligible": True
},
{
"id": "IL27-M30",
"code": "IL-27",
"title": "Incident Response for Infrastructure Teams",
"summary": "When security calls at 2 AM: containment, evidence, eradication, recovery - the infrastructure role in IR. Interview-critical - IR stories are STAR gold. You need this for -> M31/M32 and on-call readiness.",
"objectives": [
"Execute the IR lifecycle: prepare, detect, contain, eradicate, recover, lessons.",
"Perform first-responder actions: isolate, preserve evidence, capture memory.",
"Explain the infrastructure admin's role vs the SOC's role.",
"Write an incident report and run a blameless postmortem.",
"Build a jump kit and call tree before you need them."
],
"notes": [
{"title": "The lifecycle and your role",
"body": "NIST 800-61 lifecycle: Preparation -> Detection & Analysis -> Containment/Eradication/Recovery -> Post-Incident. The SOC detects and analyzes; INFRASTRUCTURE contains and recovers: isolate hosts (network, not power - memory evidence dies with power), disable accounts, block at firewall, snapshot before rebuild, restore from known-good.\n\nFirst responder rules: don't log into the compromised box with domain admin (credential theft), don't 'clean and reboot' before evidence (you destroy the timeline), DO isolate (pull the network cable / disable switch port / EDR isolate), photograph the screen, note the time, escalate per the call tree.\n\nContainment choices: short-term (isolate host, block IP) vs long-term (rebuild, reimage, credential reset fleet-wide if domain compromise suspected). Ransomware: isolate first, identify variant, check backups BEFORE negotiating anything - and know your org's ransom policy in advance."
},
{"title": "Evidence and eradication",
"body": "Evidence basics for infra: memory capture (before reboot!), disk image or snapshot, firewall/proxy logs, AD logs (4624/4625/4768), EDR timeline. Chain of custody: who touched what, when - a shared doc started at minute one. You don't need to be a forensics expert; you need to PRESERVE so experts can work.\n\nEradication: find the root cause (patient zero, entry vector), remove persistence (scheduled tasks, services, WMI, registry run keys), close the vector (patch, config, phish training). Rebuilding from known-good media beats 'cleaning' - assume the box is untrustworthy until rebuilt.\n\nRecovery: restore in priority order (identity first - DCs, then core services, then users), verify clean (scan restored data), monitor for re-infection. Communicate: who needs to know what, when - the comms plan is part of preparation, not improvisation."
},
{"title": "Preparation: the jump kit",
"body": "Jump kit (have it BEFORE the incident): clean USBs with tools (memory capture, AV scanners), known-good ISOs, credential reset scripts, network diagrams, asset inventory, call tree (who, in what order, with phone numbers that work at 2 AM), runbooks for the top 5 scenarios (ransomware, BEC, data theft, insider, outage-vs-attack).\n\nTabletop exercises: walk through a scenario quarterly ('ransomware on the file server, go'). The first time you meet your IR team shouldn't be during the incident. Document decisions and gaps after each exercise.\n\nPostmortem: blameless, timeline-based, action items with owners and dates. 'Human error' is never the root cause - ask why the system allowed it. The report: executive summary (impact, duration), timeline, root cause, actions taken, lessons, improvements. This document is career capital - it proves you operate under pressure."
}
],
"cards": [
{"front": "NIST 800-61 phases", "back": "Prepare -> Detect/Analyze -> Contain/Eradicate/Recover -> Post-incident."},
{"front": "Infra vs SOC in IR", "back": "SOC: detect/analyze. Infra: contain/recover (isolate, snapshot, rebuild, restore)."},
{"front": "First responder: isolate how?", "back": "Network isolation (cable/port/EDR) - NOT power off (kills memory evidence)."},
{"front": "Never log into a compromised box with", "back": "Domain admin - credential theft risk. Use dedicated IR creds."},
{"front": "Rebuild vs clean", "back": "Rebuild from known-good beats cleaning - assume untrustworthy."},
{"front": "Jump kit contents", "back": "Clean tools USB, ISOs, reset scripts, diagrams, inventory, call tree, runbooks."},
{"front": "'Human error' as root cause", "back": "Never - ask why the system allowed it."},
{"front": "Recovery order", "back": "Identity first (DCs), then core services, then users."}
],
"quiz": [
{"q": "Ransomware on a file server, 2 AM. First 3 actions?", "choices": ["Isolate (network), preserve evidence (photo/time), escalate per call tree", "Reboot it", "Pay immediately", "Delete the files"], "answer": 0, "index": 0, "explain": "Contain, preserve, escalate - in that order."},
{"q": "Why not power off the compromised host?", "choices": ["Memory evidence (running malware, keys) dies with power", "It's faster", "Saves electricity", "No reason"], "answer": 0, "index": 0, "explain": "Volatile evidence first."},
{"q": "SOC says 'we need the host isolated'. You:", "choices": ["EDR isolate / disable switch port / pull cable - network, not power", "Shutdown", "Reimage now", "Ignore"], "answer": 0, "index": 0, "explain": "Network isolation preserves the host for forensics."},
{"q": "Domain admin creds were on the compromised box. Now?", "choices": ["Assume domain compromise: reset KRBTGT twice, reset creds, rebuild DCs if needed", "Change one password", "Nothing", "Reboot the DC"], "answer": 0, "index": 0, "explain": "Credential theft = domain-wide response."},
{"q": "Eradication means:", "choices": ["Remove persistence + close the entry vector, verified", "Delete the alert", "Reboot", "New antivirus"], "answer": 0, "index": 0, "explain": "Root cause gone, vector closed, verified clean."},
{"q": "Postmortem rule #1:", "choices": ["Blameless - fix systems, not people", "Find who to fire", "Skip it", "Blame the vendor"], "answer": 0, "index": 0, "explain": "Blame kills honesty; systems thinking fixes recurrence."},
{"q": "Tabletop exercises are for:", "choices": ["Practicing decisions before the real incident", "Compliance theater", "Fun", "Skipping runbooks"], "answer": 0, "index": 0, "explain": "Reps before game day."},
{"q": "Recovery priority order?", "choices": ["Identity (DCs) -> core services -> users", "Users first", "Email first", "Random"], "answer": 0, "index": 0, "explain": "Everything authenticates against identity."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M31"],
"drills": [
{"id": "m30-drill-ir", "title": "Incident Response Drill",
"items": [
{"prompt": "Ransomware 2 AM: first 3", "answer": "Isolate (network), preserve, escalate", "explain": "Contain, evidence, call tree."},
{"prompt": "Power off the box?", "answer": "No - kills memory evidence", "explain": "Network isolate instead."},
{"prompt": "Admin creds on compromised host", "answer": "Assume domain compromise; KRBTGT x2", "explain": "Full credential reset."},
{"prompt": "Clean or rebuild?", "answer": "Rebuild from known-good", "explain": "Assume untrustworthy."},
{"prompt": "Recovery order", "answer": "Identity -> services -> users", "explain": "DCs first."},
{"prompt": "Postmortem rule", "answer": "Blameless, systems-focused", "explain": "Fix the system."}
]}
],
"handsOnLab": {
"id": "m30-lab",
"title": "Tabletop + Jump Kit: run a simulated incident",
"brief": "Build the kit, then run a ransomware tabletop against your lab.",
"steps": [
"Build the jump kit doc: call tree, diagrams, asset list, top-5 runbooks.",
"Scenario: ransomware on LAB-FS-01. Walk the lifecycle on paper first.",
"Simulate: isolate the VM (host-only/disconnect), 'capture' memory (document steps), snapshot.",
"Practice evidence: export relevant event logs with timestamps; start chain-of-custody doc.",
"Eradicate: identify the (simulated) vector, rebuild the VM from ISO, restore data.",
"Write the postmortem: timeline, root cause, 3 action items with owners."
],
"deliverable": "Jump kit + tabletop notes + postmortem report.",
"checkpoint": "You can run the infra side of an incident without panic."
},
"mockTask": {"id": "m30-mock", "type": "choice",
"q": "Interview: 'Tell me about a time you handled a security incident.' (STAR)",
"choices": ["Situation/Task/Action/Result using the IR lifecycle: isolated via network (not power), preserved evidence, rebuilt from known-good, blameless postmortem with action items", "I rebooted it", "Never happened", "Someone else handled it"],
"answer": 0, "explain": "STAR + lifecycle vocabulary = credible IR story."},
"crossLinks": ["il06-defensive"],
"videos": [],
"estimatedMinutes": 280,
"fastTrackEligible": True
},
{
"id": "IL27-M31",
"code": "IL-27",
"title": "Backup & Disaster Recovery",
"summary": "The last line of defense: 3-2-1, RPO/RTO, backup types, restore testing, and DR planning. Untested backups are wishes. You need this for -> M30/M34 and business continuity.",
"objectives": [
"Design 3-2-1 backup architecture with RPO/RTO targets.",
"Choose full/incremental/differential and retention (GFS).",
"Protect against ransomware: immutable/air-gapped copies.",
"Test restores on a schedule and document results.",
"Write a DR plan with roles, priorities, and communication."
],
"notes": [
{"title": "3-2-1 and the objectives",
"body": "3-2-1: 3 copies of data, 2 different media, 1 offsite. Modern addendum: 1 immutable/air-gapped (ransomware encrypts your online backups too). RPO (how much data can we lose - backup frequency) and RTO (how long to restore - restore speed + process) are BUSINESS decisions you implement: 'RPO 4h, RTO 24h for file services' drives the design.\n\nBackup types: Full (everything - slow, simple restore), Incremental (changes since last backup of any type - fast backup, slow multi-step restore), Differential (changes since last full - middle ground). GFS retention: Grandfather-Father-Son (daily/weekly/monthly) - keep dailies 2 weeks, weeklies 2 months, monthlies a year (adjust to compliance).\n\nWhat people forget: system state/AD backups (authoritative restore knowledge), configs (firewall, switch, GPO backups), cloud data (M365 needs third-party backup - Microsoft's retention isn't backup), and credentials to access the backups (documented, sealed, tested)."
},
{"title": "Ransomware-proofing backups",
"body": "Ransomware hunts backups first: mapped drives, backup server creds, cloud buckets. Defenses: immutable storage (S3 Object Lock, immutable vaults - can't be deleted even by admin for the retention period), air-gapped/offline copies (tape, rotated USBs - old school, still works), separate backup credentials (backup admin accounts NOT domain admins), and network isolation of the backup server.\n\nTest the restore, not the backup: 'backup succeeded' emails mean nothing. Quarterly: full restore of a critical system to isolated network, verify boot + data + app. Annual: full DR test. Document results - auditors and insurers ask.\n\nMonitoring: backup job success/failure (alert on failure, obviously), capacity trends, and restore-test calendar. A backup admin's worst day is discovering 6 months of failed jobs during an incident."
},
{"title": "The DR plan",
"body": "DR plan structure: objectives (RPO/RTO per tier), roles (who declares disaster, who does what), inventory (what exists, where), priority order (identity -> network -> core apps -> users - M30's order), procedures (step-by-step restores), communication (who tells whom, templates), and test schedule.\n\nTiers: Tier 1 (hours - identity, core apps), Tier 2 (day - file, print, secondary), Tier 3 (week - nice-to-haves). Cloud DR: Azure Site Recovery / AWS Elastic DR replicate VMs for failover - the M21/M22 concepts applied. On-prem: second site or Hyper-V Replica (M18).\n\nDeclaring disaster: who has authority, what's the trigger, where does everyone go (alternate site / remote). Keep a printed copy offsite - the DR plan on the dead file server helps no one."
}
],
"cards": [
{"front": "3-2-1-1 rule", "back": "3 copies, 2 media, 1 offsite, 1 immutable/air-gapped."},
{"front": "RPO vs RTO", "back": "RPO: data loss tolerance (frequency). RTO: downtime tolerance (restore speed)."},
{"front": "Full vs Incremental vs Differential", "back": "Full: all. Incremental: since any backup. Differential: since last full."},
{"front": "GFS retention", "back": "Daily/weekly/monthly tiers - e.g., dailies 2wk, weeklies 2mo, monthlies 1yr."},
{"front": "Ransomware vs backups defense", "back": "Immutable storage, air-gapped copies, separate creds, isolated backup server."},
{"front": "Test what?", "back": "The RESTORE (quarterly isolated), not just backup success emails."},
{"front": "DR recovery order", "back": "Identity -> network -> core apps (tiered) -> users."},
{"front": "DR plan kept where?", "back": "Printed offsite - not only on the servers that died."}
],
"quiz": [
{"q": "Backups 'succeed' nightly but restore fails. Lesson?", "choices": ["Test restores quarterly - backup success != recoverability", "More backups", "Faster disks", "Trust the emails"], "answer": 0, "index": 0, "explain": "Recoverability is the only metric that matters."},
{"q": "Ransomware encrypted the backup server too. Missing?", "choices": ["Immutable/air-gapped copies + separate backup credentials", "More storage", "Antivirus", "Luck"], "answer": 0, "index": 0, "explain": "Backups need their own security architecture."},
{"q": "Business: 'we can lose 4h of data, be down 1 day.' That's:", "choices": ["RPO 4h, RTO 24h", "RPO 24h, RTO 4h", "RPO 0, RTO 0", "No requirements"], "answer": 0, "index": 0, "explain": "RPO=data loss window; RTO=downtime window."},
{"q": "Fast backup, slower multi-step restore:", "choices": ["Incremental", "Full", "Differential", "Mirror"], "answer": 0, "index": 0, "explain": "Incremental chains need every link to restore."},
{"q": "M365 data protection: Microsoft's retention is:", "choices": ["Not a backup - use third-party backup for M365", "Sufficient", "Automatic forever", "Free backup"], "answer": 0, "index": 0, "explain": "Shared responsibility: your data, your backup."},
{"q": "AD disaster: which backup matters?", "choices": ["System State (authoritative restore knowledge)", "File backup", "Email backup", "None"], "answer": 0, "index": 0, "explain": "AD recovery needs system state + procedure."},
{"q": "DR test frequency minimum?", "choices": ["Quarterly restore tests, annual full DR test", "Never", "Once ever", "When disaster strikes"], "answer": 0, "index": 0, "explain": "Untested plans are fiction."},
{"q": "Backup admin accounts should be:", "choices": ["Separate from domain admins, isolated", "Domain admins", "Shared", "Guest"], "answer": 0, "index": 0, "explain": "Compromised domain admin shouldn't reach backups."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M30"],
"drills": [
{"id": "m31-drill-backup", "title": "Backup & DR Drill",
"items": [
{"prompt": "3-2-1-1", "answer": "3 copies, 2 media, 1 offsite, 1 immutable", "explain": "The modern rule."},
{"prompt": "RPO 4h means", "answer": "Back up at least every 4h", "explain": "Data loss tolerance."},
{"prompt": "RTO 24h means", "answer": "Restored within 24h", "explain": "Downtime tolerance."},
{"prompt": "Ransomware-proofing", "answer": "Immutable + air-gap + separate creds", "explain": "Backup security."},
{"prompt": "What do you test?", "answer": "Restores, quarterly isolated", "explain": "Recoverability."},
{"prompt": "DR plan location", "answer": "Printed offsite too", "explain": "Not only on dead servers."}
]}
],
"handsOnLab": {
"id": "m31-lab",
"title": "Restore Proof: backup, break, recover",
"brief": "Prove your backup strategy by actually restoring.",
"steps": [
"Set up Windows Server Backup (or Veeam CE) on LAB-FS-01: full + daily incremental.",
"Document RPO/RTO targets for the lab 'business'.",
"Simulate ransomware: 'encrypt' (rename) the data volume.",
"Restore to an isolated VM: full + incrementals; verify data integrity.",
"Test an AD system-state restore in an isolated network (document steps).",
"Write the DR one-pager: tiers, order, RPO/RTO, comms."
],
"deliverable": "Backup config + restore proof + DR one-pager.",
"checkpoint": "You trust your backups because you've restored from them."
},
"mockTask": {"id": "m31-mock", "type": "choice",
"q": "Interview: 'How do you know our backups work?'",
"choices": ["3-2-1-1 with immutable copies, quarterly isolated restore tests with documented results, RPO/RTO per tier, annual DR test", "The emails say success", "We have a lot of storage", "Trust"],
"answer": 0, "explain": "Evidence-based recoverability - the only acceptable answer."},
"crossLinks": [],
"videos": "VIDEOS_M31",
"estimatedMinutes": 280,
"fastTrackEligible": True
},
{
"id": "IL27-M32",
"code": "IL-27",
"title": "Log Management & SIEM Concepts",
"summary": "See everything: Windows event logs, syslog, centralization, and SIEM/SOAR concepts for the infra admin. You need this for -> M30/M33 and detection conversations.",
"objectives": [
"Read Windows event logs (Security/System/Application) and key event IDs.",
"Centralize logs: Windows Event Forwarding, syslog, agents.",
"Explain SIEM concepts: ingestion, parsing, correlation, alerting.",
"Write a basic detection (KQL/SPL concept) for a suspicious event.",
"Manage log retention, volume, and cost."
],
"notes": [
{"title": "Windows logs: the essential IDs",
"body": "The big three: Security (4624 logon, 4625 failed logon, 4634 logoff, 4672 special privileges, 4720/4728 account/group changes, 4768/4769 Kerberos), System (1074 shutdown/restart, 6008 unexpected shutdown, service failures), Application (app crashes). Sysmon (Sysinternals): process creation with full command line, network connections, driver loads - the EDR-grade telemetry, free.\n\nAudit policy (GPO): enable logon auditing, account management, privilege use, object access for file servers. Without the audit policy, the logs you need don't exist - 'we weren't logging that' is the saddest IR sentence.\n\nPowerShell: Get-WinEvent -FilterHashtable for fast queries; wevtutil for CLI. Centralize BEFORE you need them: Windows Event Forwarding (WEF - agentless, GPO-driven subscriptions) to a collector, then to SIEM."
},
{"title": "Centralization and SIEM",
"body": "Pipeline: sources (servers, firewalls, switches via syslog, EDR) -> collectors/forwarders -> normalization/parsing -> SIEM storage -> correlation/rules -> alerts -> SOAR playbooks. Microsoft Sentinel (M17/IL-06's territory): cloud SIEM+SOAR, KQL queries, playbooks via Logic Apps.\n\nCorrelation example: 5 failed logons (4625) + 1 success (4624) + new service installed = brute-force-to-persistence story no single log tells. Rules: threshold, anomaly, watchlist, threat intel matches. Tuning: every rule needs true/false-positive review or analysts drown.\n\nInfra admin's SIEM role: ensure the logs FLOW (agents healthy, forwarders up, time synced - logs with wrong timestamps are useless), know what each system SHOULD log, and be the person who can pull the raw logs when the SOC asks."
},
{"title": "KQL basics and log hygiene",
"body": "KQL (Kusto): SecurityEvent | where EventID == 4625 | summarize count() by Account, Computer | where count_ > 10. The pattern: table -> filter -> summarize -> filter. Learn 5 queries cold: failed logons by account, logons by computer, new services, account creations, rare processes (Sysmon).\n\nLog hygiene: retention policy (hot/warm/cold - 90 days searchable, 1 year archive typical; compliance may demand more), volume control (filter noise at the source - debug logs from chatty apps), and cost (SIEM ingestion is priced per GB - the M21 cost lesson again).\n\nTime: NTP everywhere (M11's checklist) - correlation across systems with skewed clocks is fiction. One second of skew is fine; five minutes breaks Kerberos AND your timeline."
}
],
"cards": [
{"front": "4624 / 4625 / 4672", "back": "Logon success / failed logon / special privileges assigned."},
{"front": "Sysmon gives you", "back": "Process creation w/ command line, network conns, driver loads - EDR-grade, free."},
{"front": "WEF = ?", "back": "Windows Event Forwarding - agentless, GPO-driven log centralization."},
{"front": "SIEM pipeline order", "back": "Sources -> collectors -> parse -> store -> correlate -> alert -> SOAR."},
{"front": "KQL pattern", "back": "Table | where (filter) | summarize | where - learn 5 queries cold."},
{"front": "'We weren't logging that' prevention", "back": "Audit policy via GPO before you need the logs."},
{"front": "SIEM cost driver", "back": "Ingestion per GB - filter noise at the source."},
{"front": "Time sync matters for logs because", "back": "Correlation across skewed clocks is fiction."}
],
"quiz": [
{"q": "Brute force against RDP. Which events?", "choices": ["Many 4625s then a 4624 (Logon Type 10)", "1074", "1", "No events"], "answer": 0, "index": 0, "explain": "Failed logons -> success = the brute-force signature."},
{"q": "New account created at 3 AM by unknown admin. Event?", "choices": ["4720 (user created) - investigate immediately", "4624", "1074", "Normal"], "answer": 0, "index": 0, "explain": "Account creation outside change windows = red flag."},
{"q": "SOC asks for logs from a server; WEF was never configured. Lesson?", "choices": ["Centralize before incidents - agentless WEF via GPO", "Logs aren't needed", "Reboot", "Buy more storage"], "answer": 0, "index": 0, "explain": "Preparation beats scrambling."},
{"q": "KQL: failed logons per account over 10. Write conceptually:", "choices": ["SecurityEvent | where EventID==4625 | summarize count() by Account | where count_>10", "SELECT *", "DELETE", "No query needed"], "answer": 0, "index": 0, "explain": "Filter -> aggregate -> threshold."},
{"q": "SIEM bill tripled. First look?", "choices": ["Noisy sources - filter at collection, check debug/verbose logging", "Buy more", "Delete everything", "Stop logging"], "answer": 0, "index": 0, "explain": "Volume control at the source."},
{"q": "Sysmon vs default Security log:", "choices": ["Sysmon adds command lines, network, hashes - richer process telemetry", "Same", "Worse", "Only for Linux"], "answer": 0, "index": 0, "explain": "Deploy Sysmon for real detection depth."},
{"q": "Logs show timestamps 5 minutes apart for one incident. Problem?", "choices": ["Clock skew - fix NTP; timeline unreliable", "Fine", "More logs", "New SIEM"], "answer": 0, "index": 0, "explain": "Correlation needs synchronized clocks."},
{"q": "Alert fires 500 times a day, all benign. You:", "choices": ["Tune the rule (threshold/allowlist) - alert fatigue kills detection", "Ignore alerts", "Disable SIEM", "More analysts"], "answer": 0, "index": 0, "explain": "Every rule needs FP review."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M30"],
"drills": [
{"id": "m32-drill-logs", "title": "Log & SIEM Drill",
"items": [
{"prompt": "Failed logon event", "answer": "4625", "explain": "Auth failure."},
{"prompt": "Brute force signature", "answer": "Many 4625 -> one 4624", "explain": "Failures then success."},
{"prompt": "Agentless Windows log forwarding", "answer": "WEF via GPO", "explain": "Subscriptions to collector."},
{"prompt": "Richer process telemetry, free", "answer": "Sysmon", "explain": "Command lines + network."},
{"prompt": "KQL pattern", "answer": "table | where | summarize | where", "explain": "Filter, aggregate, threshold."},
{"prompt": "500 benign alerts/day", "answer": "Tune the rule", "explain": "Fight alert fatigue."}
]}
],
"handsOnLab": {
"id": "m32-lab",
"title": "Log Pipeline: WEF + Sysmon + detection",
"brief": "Build a mini log pipeline and write a real detection.",
"steps": [
"Enable enhanced auditing via GPO on lab clients; deploy Sysmon with a standard config.",
"Set up WEF: collector on LAB-DC-01, subscription GPO for Security/Sysmon logs.",
"Generate events: failed logons, new service, account creation - verify they arrive centrally.",
"Write 3 KQL-style queries (or PowerShell equivalents): brute force, new accounts, rare processes.",
"Simulate noise: tune one query to cut false positives.",
"Document retention policy and volume estimate for a 500-seat org."
],
"deliverable": "Working pipeline + 3 detections + retention/volume doc.",
"checkpoint": "You can build the visibility layer IR depends on."
},
"mockTask": {"id": "m32-mock", "type": "choice",
"q": "Interview: 'How would you detect a brute-force attack?'",
"choices": ["Centralized 4625s (WEF/Sysmon), KQL threshold per account, alert + auto-block playbook, tuned against false positives", "Check manually", "Antivirus", "Hope"],
"answer": 0, "explain": "Pipeline + query + response + tuning - the full detection story."},
"crossLinks": ["il06-azure-soc"],
"videos": [],
"estimatedMinutes": 260,
"fastTrackEligible": False
},
{
"id": "IL27-M33",
"code": "IL-27",
"title": "Vulnerability & Compliance Basics",
"summary": "Find weaknesses before attackers do: scanning, prioritization, remediation SLAs, and speaking compliance. You need this for -> M24/M32 and audit conversations.",
"objectives": [
"Run a vulnerability scan and interpret results (CVE, CVSS).",
"Prioritize by exploitability, not just CVSS score.",
"Drive remediation with SLAs per severity.",
"Explain common frameworks (NIST CSF, CIS, PCI, HIPAA) at a conversational level.",
"Prepare for an audit: evidence, not promises."
],
"notes": [
{"title": "Scanning and scoring",
"body": "Vulnerability scanners (Nessus/OpenVAS/Defender VM): authenticated scans (with creds - sees patches, configs) beat unauthenticated (sees banners). Scan regularly: weekly for servers, monthly for workstations, after major changes. Credentials for scanning: dedicated least-privilege scan account.\n\nCVE: the vulnerability's ID. CVSS: 0-10 severity score - useful but flawed (a 9.8 nobody can exploit vs a 7.5 with public exploit). EPSS (exploit prediction) + CISA KEV catalog (known exploited - patch THESE first) beat raw CVSS for prioritization.\n\nFalse positives: scanners flag generously - verify before panicking. Track: new, recurring, remediated, exception. 'We went from 400 criticals to 40' is the trend leadership funds."
},
{"title": "Remediation as a program",
"body": "SLAs by severity: critical (KEV) - days; high - 2 weeks; medium - 30 days; low - 90 days or accept. Owners per system (the M04 accountability lesson); the scanner finds, the owner fixes, you track. Exceptions: documented, compensating controls, expiry - same discipline as M24.\n\nRemediation usually = patching (M24's machine), config change (GPO), or decommission (that 2012 server). The vulnerability program and the patch program are siblings - run them together.\n\nReporting: open by severity/age, MTTR per severity, SLA compliance %, top recurring. One page, monthly, to leadership. Trends beat snapshots."
},
{"title": "Compliance conversations",
"body": "Frameworks you'll hear: NIST CSF 2.0 (Govern, Identify, Protect, Detect, Respond, Recover - the lingua franca), CIS Controls (18 prioritized safeguards), PCI DSS (card data - network segmentation + logging heavy), HIPAA (health data - access controls + audit), SOC 2 (vendor trust - auditors love evidence).\n\nAudit prep: evidence, not promises - 'show me' beats 'we do'. Evidence = configs, logs, tickets, reports with dates. Control mapping: one action satisfies many frameworks (MFA covers CIS, PCI, HIPAA, SOC 2).\n\nThe infra admin's compliance role: implement the technical controls, produce the evidence, and never lie to an auditor. 'We don't do that yet; here's our plan with dates' beats a confident fiction every time."
}
],
"cards": [
{"front": "Authenticated vs unauthenticated scan", "back": "Authenticated (with creds): sees patches/configs. Unauthenticated: banners only."},
{"front": "Prioritize by", "back": "Exploitability (KEV/EPSS), not CVSS alone."},
{"front": "CISA KEV = ?", "back": "Known Exploited Vulnerabilities catalog - patch these first."},
{"front": "Remediation SLAs (typical)", "back": "Critical/KEV: days. High: 2wk. Medium: 30d. Low: 90d/accept."},
{"front": "NIST CSF 2.0 functions", "back": "Govern, Identify, Protect, Detect, Respond, Recover."},
{"front": "Audit rule #1", "back": "Evidence, not promises - show configs, logs, tickets with dates."},
{"front": "One action, many frameworks", "back": "MFA satisfies CIS, PCI, HIPAA, SOC 2 simultaneously."},
{"front": "Never do with an auditor", "back": "Lie. 'Not yet; here's our dated plan' beats fiction."}
],
"quiz": [
{"q": "CVSS 9.8 with no exploit vs 7.5 in CISA KEV. Patch first?", "choices": ["The KEV 7.5 - exploited in the wild beats theoretical severity", "The 9.8", "Neither", "Both never"], "answer": 0, "index": 0, "explain": "Exploitability drives priority."},
{"q": "Scanner flags 400 criticals. First step?", "choices": ["Verify (FP check), prioritize by KEV/exploitability, assign owners with SLAs", "Panic", "Ignore", "Rescan"], "answer": 0, "index": 0, "explain": "Triage before action."},
{"q": "That 2012 server can't be patched. Options?", "choices": ["Isolate/segment, compensating controls, documented exception, decommission plan", "Internet-facing", "Ignore", "Hope"], "answer": 0, "index": 0, "explain": "Manage unpatchable risk explicitly."},
{"q": "Unauthenticated scan shows clean; authenticated shows 50 missing patches. Lesson?", "choices": ["Always scan authenticated - banners lie", "Scanners are broken", "Patching is fine", "Uninstall scanner"], "answer": 0, "index": 0, "explain": "Credentialed scans see reality."},
{"q": "Auditor asks 'prove MFA is enforced'. You show:", "choices": ["Conditional Access policies + sign-in logs + compliance report", "A promise", "A screenshot of one login", "The vendor brochure"], "answer": 0, "index": 0, "explain": "Policy + logs + report = evidence."},
{"q": "Vulnerability and patch programs relate how?", "choices": ["Siblings: scanner finds, patch program fixes, vuln program tracks", "Unrelated", "Enemies", "Same tool"], "answer": 0, "index": 0, "explain": "Run them as one motion."},
{"q": "SLA breach on a critical: you:", "choices": ["Escalate with risk statement and options, not just the miss", "Hide it", "Extend silently", "Blame the owner"], "answer": 0, "index": 0, "explain": "Risk-framed escalation drives decisions."},
{"q": "NIST CSF 'Govern' (new in 2.0) covers:", "choices": ["Risk strategy, oversight, and policy - the management layer", "Firewalls", "Passwords", "Backups"], "answer": 0, "index": 0, "explain": "Governance over all functions."}
],
"weight": 2,
"prerequisiteFor": [],
"drills": [
{"id": "m33-drill-vuln", "title": "Vulnerability Drill",
"items": [
{"prompt": "Patch-first list", "answer": "CISA KEV catalog", "explain": "Known exploited."},
{"prompt": "CVSS vs exploitability", "answer": "Exploitability wins", "explain": "KEV/EPSS over raw score."},
{"prompt": "Critical SLA", "answer": "Days", "explain": "KEV = fast."},
{"prompt": "Unpatchable 2012 server", "answer": "Isolate + exception + decon plan", "explain": "Managed risk."},
{"prompt": "Prove a control to auditors", "answer": "Policy + logs + reports (evidence)", "explain": "Show, don't tell."},
{"prompt": "NIST CSF 2.0 functions", "answer": "G,I,P,D,R,R + Govern", "explain": "The lingua franca."}
]}
],
"handsOnLab": {
"id": "m33-lab",
"title": "Vuln Program: scan, prioritize, remediate",
"brief": "Run a real scan-to-remediation cycle on your lab.",
"steps": [
"Install OpenVAS (or Nessus Essentials) as a container (M20); scan the lab authenticated.",
"Export results; triage: verify 5 findings (FP check), map CVEs to KEV.",
"Prioritize top 10 by exploitability; assign (yourself) with SLA dates.",
"Remediate: patch/config-fix the lab; rescan to verify closure.",
"Write the one-page leadership report: open by severity, MTTR, trend.",
"Document one exception with compensating controls and expiry."
],
"deliverable": "Scan reports + triage + remediation proof + leadership one-pager.",
"checkpoint": "You run vulnerability management as a program, not a scan."
},
"mockTask": {"id": "m33-mock", "type": "choice",
"q": "Interview: 'How do you prioritize vulnerabilities?'",
"choices": ["Verify findings, prioritize by exploitability (KEV/EPSS) over raw CVSS, SLA per severity, owners assigned, tracked to closure, exceptions documented", "Highest CVSS first", "Alphabetical", "Ignore lows"],
"answer": 0, "explain": "Risk-based prioritization with accountability."},
"crossLinks": ["il06-hackers-arise"],
"videos": "VIDEOS_M33",
"estimatedMinutes": 240,
"fastTrackEligible": False
}
]
