"""IL-27 meta: course meta, cheatSheets, answerBank, sourceLinks, standalone drills."""

META = {
"code": "IL-27",
"courseId": "il-27-it-infrastructure-specialist-threatlocker-mastery",
"title": "IL-27 \u00b7 IT Infrastructure Specialist \u2014 Zero Trust Infrastructure Mastery",
"tagline": "From first principles to Zero Trust: the complete infrastructure skill set, interview-ready.",
"blurb": "An enterprise-grade, self-paced mastery course covering the full IT infrastructure stack through a Zero Trust lens: hardware and Windows/Linux administration, TCP/IP and subnetting math, Windows Server and Active Directory, virtualization and cloud, endpoint management and hardening, application allowlisting, Zero Trust architecture, security operations, monitoring and reliability \u2014 plus a foundational math track (binary, Boolean logic, subnetting math, modular arithmetic, set theory, probability, queuing, Big-O) and a capstone homelab. Every module pairs original readings with flashcards, quizzes, drills, hands-on labs, and mock interview tasks. Independent preparation: this course is not affiliated with, endorsed by, or a partner of any vendor named herein, and it confers no certifications \u2014 those are earned from the vendors by passing their exams.",
"hours": 208,
"mockMinutes": 480,
"honestyNote": "Independent study material. Not affiliated with, endorsed by, sponsored by, or a partner of ThreatLocker or any other vendor mentioned. No certifications are conferred by this course; certifications are earned from vendors (CompTIA, Microsoft, Cisco) by passing their exams. All practice questions are original and written for study \u2014 they are not drawn from any real exam.",
"objectives": [
"Administer Windows 10/11 and Windows Server (AD DS, GPO, DNS/DHCP, file/print) to a production standard.",
"Apply TCP/IP, subnetting math (CIDR/VLSM/supernetting), and network troubleshooting with Wireshark-level rigor.",
"Deploy and manage virtualization (Hyper-V, VMware concepts) and core Azure/AWS infrastructure services.",
"Run endpoint lifecycles: imaging/deployment, patch rings, Intune MDM, CIS-concept hardening, and application allowlisting.",
"Design and articulate Zero Trust architecture per NIST SP 800-207 and the CISA maturity model.",
"Execute the infrastructure side of incident response, backup/DR, logging/SIEM, and vulnerability management.",
"Operate monitoring, high availability, and capacity planning for reliable services.",
"Use foundational math (binary, Boolean logic, modular arithmetic, sets, probability, queuing, Big-O) in daily infrastructure work.",
"Build, document, and present a homelab capstone with a professional documentation portfolio.",
"Interview at a specialist level: STAR stories, live troubleshooting narration, and honest certification planning."
],
"arc": [
"Foundations (Tracks A, MX): hardware, OS administration, documentation, and the math substrate.",
"Connectivity (Track B): TCP/IP, subnetting, DNS/DHCP, switching, routing, wireless, troubleshooting.",
"Identity & Control (Track C): Windows Server, Active Directory, Group Policy, PowerShell, hybrid Entra identity.",
"Platforms (Track D): Hyper-V, VMware, containers, Azure, AWS.",
"Endpoints (Track E): imaging, patching, Intune, hardening, allowlisting.",
"Zero Trust & Operations (Track F): architecture, segmentation, IR, backup/DR, SIEM, vuln management.",
"Reliability (Track G): monitoring, HA, capacity.",
"Proof & Career (Track H): capstone homelab, documentation portfolio, professional excellence, certification roadmap."
],
"priorities": [
"Interview-critical fast-track modules first: identity (M12/M13/M17), Zero Trust (M28/M29), hardening and allowlisting (M26/M27), IR and backup (M30/M31), PowerShell (M16), networking math (MX03).",
"Hands-on over passive: every module ends in a lab; the capstone homelab (M37) is the portfolio centerpiece.",
"Original exposition throughout: vendor docs are anchors for further reading, never copied text.",
"Honest framing: independent prep, no vendor affiliation claims, certifications earned from vendors."
],
"battlePlan": [
"Week 1: Foundations + math substrate (Tracks A, MX01\u2013MX03) and networking core (M05\u2013M07).",
"Week 2: Windows Server & identity deep dive (M11\u2013M13, M16\u2013M17) with daily PowerShell reps.",
"Week 3: Virtualization/cloud (M18\u2013M22) and endpoint management (M23\u2013M27).",
"Week 4: Zero Trust & security operations (M28\u2013M33) plus monitoring/reliability (M34\u2013M36).",
"Week 5: Capstone build (M37), documentation portfolio (M38), career modules (M39\u2013M40), full mock interviews."
]
}

CHEAT_SHEETS = [
{"title": "Subnetting Speed Sheet",
"blocks": [
{"h": "The magic number method", "body": "Interesting octet = 256 - mask octet. /26: 256-192=64 -> subnets increment by 64 (0, 64, 128, 192). Block size gives hosts: block - 2.", "code": "/24 -> 256-256... use: /25:128 /26:64 /27:32 /28:16 /29:8 /30:4", "lang": "text"},
{"h": "Host formula", "body": "Usable hosts = 2^(host bits) - 2. /24: 2^8-2 = 254. /30: 2^2-2 = 2 (point-to-point links).", "code": "hosts = 2^(32-prefix) - 2", "lang": "text"},
{"h": "VLSM order", "body": "Allocate largest requirement first, then next. Never carve small blocks first - you fragment the space.", "code": "500 hosts -> /23, 200 -> /24, 60 -> /26, 28 -> /27, 12 -> /28, 2 -> /30", "lang": "text"},
{"h": "Supernetting", "body": "Combine contiguous same-size blocks by shortening the mask: two /24s -> one /23. CIDR aggregation shrinks routing tables.", "code": "192.168.0.0/24 + 192.168.1.0/24 = 192.168.0.0/23", "lang": "text"}
]},
{"title": "AD & Group Policy Quick Reference",
"blocks": [
{"h": "FSMO roles", "body": "Forest: Schema Master, Domain Naming Master. Domain: RID Master, PDC Emulator, Infrastructure Master. PDC Emulator is the operationally critical one (passwords, time, GPO).", "code": "netdom query fsmo", "lang": "text"},
{"h": "GPO precedence", "body": "LSDOU: Local, Site, Domain, OU - closest OU wins. Enforced beats Block Inheritance. Computer settings need reboot; user settings need logon.", "code": "gpresult /r   # what applied and why not\ngpupdate /force", "lang": "text"},
{"h": "Replication health", "body": "The three commands that answer 'is AD healthy'.", "code": "dcdiag\nrepadmin /replsummary\nrepadmin /showrepl", "lang": "text"},
{"h": "AGDLP", "body": "Accounts -> Global groups -> Domain Local groups -> Permissions on resources. Users never directly on ACLs.", "code": "Add-ADGroupMember -Identity GG_Role -Members $users", "lang": "powershell"}
]},
{"title": "PowerShell Fleet One-Liners",
"blocks": [
{"h": "Stale computers", "body": "Find machines inactive 90+ days.", "code": "Search-ADAccount -ComputersOnly -AccountInactive -TimeSpan 90 | Select Name, LastLogonDate", "lang": "powershell"},
{"h": "Fleet patch check", "body": "Newest hotfix across servers via fan-out remoting.", "code": "$s = Get-Content servers.txt\nInvoke-Command -ComputerName $s { Get-HotFix | Sort InstalledOn -Desc | Select -First 1 }", "lang": "powershell"},
{"h": "Disk space fleet", "body": "Low-disk report, filter left.", "code": "Get-CimInstance Win32_LogicalDisk -Filter \"DriveType=3\" | Where {$_.FreeSpace/$_.Size -lt 0.2} | Select PSComputerName, DeviceID, @{n='GBfree';e={[math]::Round($_.FreeSpace/1GB,1)}}", "lang": "powershell"},
{"h": "Safe remediation pattern", "body": "Always -WhatIf first on destructive actions.", "code": "Remove-ADUser -Identity $u -WhatIf  # then real", "lang": "powershell"}
]},
{"title": "Zero Trust Interview Answers",
"blocks": [
{"h": "60-second definition", "body": "'Zero Trust means never trust, always verify: every access decision checks identity, device health, and context - never network location. Practically: phishing-resistant MFA, compliant devices, microsegmentation, least privilege, measured against the CISA maturity model.'", "code": "", "lang": "text"},
{"h": "NIST SP 800-207 tenets (7)", "body": "All services are resources; all communication secured; per-session access; dynamic policy; monitor asset posture; dynamic auth before access; collect info to improve.", "code": "", "lang": "text"},
{"h": "CISA pillars", "body": "Identity, Devices, Networks, Applications, Data - plus Visibility, Automation, Governance. Stages: Traditional -> Initial -> Advanced -> Optimal.", "code": "", "lang": "text"},
{"h": "First three projects", "body": "1. Phishing-resistant MFA + Conditional Access baselines. 2. Intune compliance gating corporate apps. 3. Tiered segmentation starting with server VLANs.", "code": "", "lang": "text"}
]},
{"title": "TCP/IP Troubleshooting Commands",
"blocks": [
{"h": "Windows", "body": "The daily kit.", "code": "ipconfig /all\nping / tracert / pathping\nnslookup / Resolve-DnsName\nnetstat -ano | findstr LISTENING\nTest-NetConnection host -Port 443", "lang": "text"},
{"h": "Linux", "body": "The daily kit.", "code": "ip addr / ip route\nss -tulpn\ndig +short / getent hosts\nmtr --report host\ncurl -vI https://host", "lang": "bash"},
{"h": "Method order", "body": "Physical -> IP config -> gateway ping -> DNS resolve -> port test -> capture. Never skip layers.", "code": "", "lang": "text"}
]},
{"title": "Ports You Must Know",
"blocks": [
{"h": "Infrastructure core", "body": "DNS 53, DHCP 67/68, HTTP 80, HTTPS 443, SMB 445, RDP 3389, SSH 22, WinRM 5985/5986.", "code": "", "lang": "text"},
{"h": "Directory & mail", "body": "LDAP 389, LDAPS 636, Kerberos 88, SMTP 25, IMAP 143/993, POP3 110/995.", "code": "", "lang": "text"},
{"h": "Network services", "body": "NTP 123, SNMP 161/162, TFTP 69, Syslog 514, NetBIOS 137-139.", "code": "", "lang": "text"},
{"h": "Databases", "body": "MSSQL 1433, MySQL 3306, PostgreSQL 5432, RDP alt 3390 (non-standard).", "code": "", "lang": "text"}
]},
{"title": "Infra Math Speed Sheet",
"blocks": [
{"h": "Binary/hex", "body": "Nibble table: 0=0000 ... 9=1001, A=1010, F=1111. Hex<->binary per nibble; decimal via place values 128-64-32-16-8-4-2-1.", "code": "0xFF = 255 = 11111111\n0xC0 = 192 = 11000000", "lang": "text"},
{"h": "SLA math", "body": "Allowed downtime = (1 - SLA) x period. 99.9% monthly ~= 43.8 min. nines: 99%=3.65d/yr, 99.9%=8.76h, 99.99%=52.6m.", "code": "downtime = (1 - 0.999) * 30 * 24 * 60 = 43.8 min/month", "lang": "text"},
{"h": "MTBF/MTTR", "body": "Availability = MTBF / (MTBF + MTTR). Halving MTTR is usually cheaper than doubling MTBF.", "code": "A = 1000/(1000+1) = 99.9%", "lang": "text"},
{"h": "Little's Law", "body": "L = lambda x W: average in system = arrival rate x average time. Size queues and staff from it.", "code": "L = 50/hr * 0.1hr = 5 concurrent", "lang": "text"}
]},
{"title": "Incident First 15 Minutes",
"blocks": [
{"h": "Minutes 0-5", "body": "Isolate via NETWORK (not power - preserve memory). Photo the screen. Note the time. Start the shared timeline doc.", "code": "", "lang": "text"},
{"h": "Minutes 5-10", "body": "Escalate per call tree. Scope: one host or many? Pull relevant logs (Security 4624/4625, Sysmon, firewall).", "code": "Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 20", "lang": "powershell"},
{"h": "Minutes 10-15", "body": "Contain wider if spreading (disable accounts, block IPs). Preserve evidence (memory capture, snapshot). Do NOT log in with domain admin.", "code": "", "lang": "text"},
{"h": "Comms", "body": "Update every 15-30 min, one channel, factual. 'We don't know yet; next update at :30' beats silence.", "code": "", "lang": "text"}
]}
]

ANSWER_BANK = [
{"q": "Walk me through how you would design Active Directory for a 500-person single-site company.",
"a": "Single-domain forest unless legal separation forces otherwise - the forest is the security boundary. Functional OUs (Workstations, Servers, Users, ServiceAccounts), shallow, never org-chart-based. Two or more DCs on separate hosts, AD Sites and subnets defined, DNS AD-integrated, time hierarchy from the PDC Emulator. Groups per AGDLP, gMSAs for services, LAPS for local admins, and a documented FSMO placement. Then harden: CIS L1-concept baselines via GPO, audit policy on, stale-object lifecycle (disable 90d, delete 180d)."},
{"q": "How do you troubleshoot a machine that cannot reach the internet but the network seems fine?",
"a": "Layer by layer, never skipping: link lights and cable, ipconfig for APIPA (169.254 = no DHCP), ping the gateway (local stack), ping 8.8.8.8 (routing), resolve a name (DNS - try Resolve-DnsName against 1.1.1.1 vs internal), Test-NetConnection port 443 (filtering), then check proxy config and capture with Wireshark if needed. Narrate each result - the method is the answer."},
{"q": "What is Zero Trust, and how would you start implementing it here?",
"a": "Never trust, always verify: every access decision checks identity, device health, and context per NIST SP 800-207 - network location is not a trust signal. I'd assess current state against the CISA maturity model per pillar, then sequence: first phishing-resistant MFA plus Conditional Access baselines, then Intune compliance gating corporate apps, then tiered network segmentation. Each is valuable alone; together they climb the maturity model. Metrics from day one: MFA coverage, compliant-device percentage, segmented workloads."},
{"q": "A GPO is not applying to some machines. Walk me through it.",
"a": "gpresult /r on an affected target first - it shows applied versus denied with reasons. Then check in order: is it linked to the right OU, is security filtering granting Read plus Apply, any WMI filter evaluating false, Block Inheritance versus Enforced, computer half needing a reboot, and SYSVOL/DFSR replication health. The MS16-072 gotcha - computer accounts needing Read on the GPO - is always worth verifying."},
{"q": "How would you roll out application allowlisting without breaking the business?",
"a": "Default-deny for code: start in audit mode to map the real application catalog - enforcing blind breaks day one. Build publisher rules (they survive updates; hash rules do not), default rules first so Windows itself keeps working, then enforce on a pilot tier starting with fixed-function devices where the catalog is smallest. Maintain it as a governed request pipeline: new software becomes a ticket - vet, approve, deploy the rule. That discipline is the endpoint enforcement of Zero Trust."},
{"q": "Ransomware is spreading on the network right now. What do you do?",
"a": "Contain first: isolate affected hosts via network - EDR isolate or disable the switch port - never power off, because memory evidence dies with power. Preserve evidence: photos, timestamps, memory capture, snapshots, and start the chain-of-custody doc. Escalate per the call tree, scope whether it is one host or many, and check backups before anyone discusses ransom. Eradication means finding patient zero and the entry vector, removing persistence, rebuilding from known-good media - cleaning is not trusted. Then the blameless postmortem with action items."},
{"q": "How do you keep patching under control for hundreds of machines?",
"a": "Ring-based program: pilot in days 1-3, broad fleet days 4-10, critical servers days 11-14 with maintenance windows and deadlines. WSUS or Intune for the OS depending on whether the fleet is LAN or remote, plus explicit third-party application patching - WSUS does not cover Chrome and Adobe, and that is where fleets actually bleed. A standing zero-day lane: assess, fast pilot, broad within 24-48 hours. Measure it: percentage patched within SLA per ring, mean time to patch for criticals, and exceptions that are documented, time-bound, and reviewed quarterly."},
{"q": "Explain the difference between a checkpoint and a backup.",
"a": "A checkpoint is a short-term differencing chain on the same storage for quick rollback around a change measured in hours - it degrades performance the longer it lives and dies with the storage. A backup is an independent, ideally immutable and offsite copy for recovery. Never substitute one for the other: checkpoints left for months are a classic outage cause, and only tested restores prove recoverability."},
{"q": "How do you decide between containers and virtual machines?",
"a": "Containers for dense, fast-starting, reproducible, mostly stateless services - they share the host kernel, so the host's patching is their security boundary. Virtual machines for full OS control, strong isolation, and Windows roles like domain controllers. In practice the layers compose: containers frequently run on VMs. For state, back up volumes and image definitions - never the containers themselves."},
{"q": "Why should we hire you for this infrastructure role?",
"a": "Because I operate the full stack, not just tickets: I design identity properly, automate with PowerShell instead of clicking, measure everything - patch compliance, backup restores, alert signal - and I document so the team gets stronger. My homelab is the proof: a segmented, monitored, backed-up environment I built, broke, fixed, and can walk you through live. And I communicate: structured updates in incidents, outcomes for managers, and blameless follow-through afterwards."}
]

SOURCE_LINKS = [
{"name": "NIST SP 800-207 Zero Trust Architecture (final)", "url": "https://csrc.nist.gov/pubs/sp/800/207/final", "note": "The authoritative Zero Trust definition; basis for IL-27 Track F. Public standard, link only.", "retrieved": "2026-10-07"},
{"name": "CISA Zero Trust Maturity Model", "url": "https://www.cisa.gov/zero-trust-maturity-model", "note": "Assessment framework: 5 pillars x 4 stages; used for maturity scoring exercises. Public guidance, link only.", "retrieved": "2026-10-07"},
{"name": "Microsoft Learn: Active Directory Domain Services (learning path)", "url": "https://learn.microsoft.com/en-us/learn/paths/active-directory-domain-services/", "note": "Official AD DS curriculum; companion to IL-27 M12. No affiliation; link only.", "retrieved": "2026-10-07"},
{"name": "Microsoft Learn: Deploy and manage identity infrastructure", "url": "https://learn.microsoft.com/en-us/training/paths/deploy-manage-identity-infrastructure/", "note": "Official hybrid identity path; companion to IL-27 M17. No affiliation; link only.", "retrieved": "2026-10-07"},
{"name": "AZ-800 / AZ-801 official study guides", "url": "https://aka.ms/az-800studyguide", "note": "Microsoft's exam study guides for Windows Server Hybrid Administrator; maps to IL-27 Track C. No affiliation; link only.", "retrieved": "2026-10-07"},
{"name": "Microsoft Learn: Fundamentals of computer networking", "url": "https://learn.microsoft.com/en-us/training/modules/network-fundamentals/", "note": "Official networking foundations; companion to IL-27 Track B. No affiliation; link only.", "retrieved": "2026-10-07"},
{"name": "Microsoft Learn: Manage Microsoft 365 services with PowerShell", "url": "https://learn.microsoft.com/en-us/training/paths/manage-microsoft-365-services-use-windows-powershell/", "note": "Official PowerShell curriculum; companion to IL-27 M16. No affiliation; link only.", "retrieved": "2026-10-07"},
{"name": "Microsoft Learn: Introduction to Azure Arc", "url": "https://learn.microsoft.com/en-us/training/modules/intro-to-azure-arc/", "note": "Official Azure Arc module; hybrid management companion to IL-27 M21. No affiliation; link only.", "retrieved": "2026-10-07"},
{"name": "Professor Messer CompTIA A+ 220-1101 (free)", "url": "https://www.professormesser.com/free-a-plus-training/220-1101/220-1101-video/220-1101-training-course/", "note": "Free A+ video course; foundations companion to IL-27 Track A. Independent educator; link only.", "retrieved": "2026-10-07"},
{"name": "Professor Messer CompTIA A+ 220-1102 (free)", "url": "https://www.professormesser.com/free-a-plus-training/220-1102/220-1102-video/220-1102-training-course/", "note": "Free A+ video course; OS/admin companion to IL-27 M02/M11. Independent educator; link only.", "retrieved": "2026-10-07"},
{"name": "Cisco Networking Academy: Networking Basics", "url": "https://www.netacad.com/courses/networking-basics?courseLang=en-US", "note": "Cisco's free networking foundations; companion to IL-27 Track B. No affiliation; link only.", "retrieved": "2026-10-07"},
{"name": "Beej's Guide to Network Programming", "url": "https://beej.us/guide/bgnet/", "note": "Classic free sockets/networking reference; depth companion to IL-27 M05/M10. Link only.", "retrieved": "2026-10-07"},
{"name": "ThreatLocker: Stop ransomware before it starts (product overview)", "url": "https://threatlocker.com/stop-ransomware-before-it-starts", "note": "Vendor's public product overview; useful for understanding allowlisting productization concepts in IL-27 M27. Independent reference only - no affiliation, endorsement, or partnership.", "retrieved": "2026-10-07"},
{"name": "Stanford CS144: Introduction to Computer Networking", "url": "https://cs144.github.io/", "note": "Stanford networking course site; depth companion to IL-27 Track B. Link only.", "retrieved": "2026-10-07"}
]

DRILLS = [
{"id": "drill-zt-60s", "title": "The 60-Second Zero Trust Answer", "prompt": "Give the 60-second 'what is Zero Trust' answer out loud.", "choices": ["Never trust, always verify: identity + device + context per access; NIST SP 800-207; assess via CISA pillars; start with MFA + Conditional Access", "It is a firewall", "It means no passwords", "It is a VPN replacement"], "answer": 0, "explain": "Definition, authority, assessment, first action - in one breath."},
{"id": "drill-subnet-30s", "title": "30-Second Subnet", "prompt": "How many usable hosts in 10.20.0.0/22?", "choices": ["1022", "1024", "510", "254"], "answer": 0, "explain": "2^10 - 2 = 1022."},
{"id": "drill-fsmo", "title": "FSMO Under Pressure", "prompt": "The PDC Emulator just died. What breaks first?",
"choices": ["Password changes, time sync hierarchy, and GPO processing degrade", "Nothing at all", "The forest is deleted", "DHCP stops"], "answer": 0, "explain": "PDC Emulator is the operationally critical role."},
{"id": "drill-gpo-order", "title": "GPO Precedence Sprint", "prompt": "Domain GPO sets X=1, OU GPO sets X=2. Effective value?",
"choices": ["2 - closest OU to the object wins (LSDOU)", "1", "Both", "Neither"], "answer": 0, "explain": "LSDOU: later/closer wins."},
{"id": "drill-ir-first", "title": "IR First Move", "prompt": "Ransomware on a file server. First action?",
"choices": ["Network-isolate the host (not power off), preserve evidence, escalate", "Reboot it", "Pay the ransom", "Delete the shares"], "answer": 0, "explain": "Contain, preserve, escalate."},
{"id": "drill-perms", "title": "Permission Math", "prompt": "Share = Change, NTFS = Read. Effective?",
"choices": ["Read - most restrictive of both layers wins", "Change", "Full", "Deny"], "answer": 0, "explain": "Intersection of share and NTFS."},
{"id": "drill-backup-test", "title": "Backup Truth", "prompt": "How do you know backups work?",
"choices": ["Quarterly isolated restore tests with documented results", "The success emails", "Disk is full of backups", "Trust"], "answer": 0, "explain": "Recoverability is the only metric."},
{"id": "drill-allowlist-rollout", "title": "Allowlist Rollout", "prompt": "First step of an AppLocker rollout?",
"choices": ["Audit mode - map the real application catalog before enforcing", "Enforce immediately", "Hash rules for everything", "Disable antivirus"], "answer": 0, "explain": "Never enforce blind."},
{"id": "drill-dns-dhcp", "title": "DNS Before DHCP", "prompt": "Client gets IP but cannot resolve names. Layer?",
"choices": ["DNS: check server config, try alternate resolver, inspect traffic", "Physical cable", "Reinstall OS", "New switch"], "answer": 0, "explain": "IP works, resolution fails - it is DNS."},
{"id": "drill-patch-ring", "title": "Patch Ring Recall", "prompt": "State the ring timeline.",
"choices": ["Pilot days 1-3, broad 4-10, critical 11-14 with deadlines", "All at once", "Never", "Yearly"], "answer": 0, "explain": "Staged with enforcement."},
{"id": "drill-laps", "title": "LAPS Value", "prompt": "What attack does LAPS kill?",
"choices": ["Lateral movement via shared local admin passwords", "Phishing", "DDoS", "Insider theft"], "answer": 0, "explain": "Unique per-machine credentials."},
{"id": "drill-rpo-rto", "title": "RPO vs RTO", "prompt": "Business tolerates 4h data loss, 24h downtime. State it.",
"choices": ["RPO 4h, RTO 24h", "RPO 24h, RTO 4h", "RPO 0, RTO 0", "No objectives"], "answer": 0, "explain": "RPO = data, RTO = time."},
{"id": "drill-port-445", "title": "Port 445", "prompt": "Port 445 is?",
"choices": ["SMB - file sharing; a lateral-movement favorite, segment it", "DNS", "HTTP", "SSH"], "answer": 0, "explain": "Know it and control it."},
{"id": "drill-ca-safety", "title": "Conditional Access Safety", "prompt": "Before enforcing a new CA policy?",
"choices": ["Report-only mode, What If test, pilot group - then enforce", "Enforce globally now", "Email users", "Disable MFA"], "answer": 0, "explain": "Blast-radius control."},
{"id": "drill-nines", "title": "Nines Math", "prompt": "99.9% uptime allows per year?",
"choices": ["8.76 hours", "52.6 minutes", "3.65 days", "5.26 minutes"], "answer": 0, "explain": "0.1% of 8760 hours."},
{"id": "drill-star", "title": "STAR Spine", "prompt": "Structure any behavioral answer as?",
"choices": ["Situation, Task, Action, Result - with measured outcomes", "A joke", "A complaint", "Silence"], "answer": 0, "explain": "The interview answer spine."}
]
