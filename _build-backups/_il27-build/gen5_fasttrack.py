"""IL-27 certs.json — part 5: fastTrack + fastTrackModules (FT01..FT06).
FT02 Q&A bank: 60 items, each marked 'reported by candidates' (publicly visible
Glassdoor interview reports, fetched 2026-10-07) or 'likely' (authored for the role).
Independent prep only — no affiliation/endorsement/hiring-promise claims about ThreatLocker.
STAR stories use ONLY his real history — no invented jobs or metrics.
"""
import json, os

PARTS = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/_il27-build/parts")
os.makedirs(PARTS, exist_ok=True)

fastTrack = {
  "title": "IL-27 Interview Fast Track — ThreatLocker IT Infrastructure Specialist",
  "framing": "Independent interview preparation. Not affiliated with, endorsed by, or sponsored by ThreatLocker. No hiring promise is implied.",
  "interviewDate": "2026-10-13T09:00:00-04:00",
  "daysTotal": 6,
  "dailyMinutes": 240,
  "plan": [
    {"day": 1, "date": "2026-10-07", "theme": "ThreatLocker deep dive + networking refresh",
     "modules": ["IL27-FT01"], "questionBank": "FT02 networking slice (8)",
     "tasks": ["Complete FT01 cards and quiz", "Answer the 8 networking questions aloud, timed", "Write your 60-second 'why ThreatLocker' answer"],
     "minutes": 240},
    {"day": 2, "date": "2026-10-08", "theme": "Windows Server / Active Directory",
     "modules": ["IL27-M15 review"], "questionBank": "FT02 Windows Server/AD slice (8)",
     "tasks": ["Whiteboard OU + GPO design from memory", "Answer the 8 AD questions aloud", "Rehearse the virtual-machine build walkthrough (reported question)"],
     "minutes": 240},
    {"day": 3, "date": "2026-10-09", "theme": "PowerShell + troubleshooting",
     "modules": ["IL27-M16/M21 review"], "questionBank": "FT02 PowerShell troubleshooting slice (7)",
     "tasks": ["Write 3 admin scripts from scratch", "Run 5 triage scenarios using the M04 methodology", "Answer the 7 PowerShell questions aloud"],
     "minutes": 240},
    {"day": 4, "date": "2026-10-10", "theme": "Zero Trust + security",
     "modules": ["IL27-M14 review"], "questionBank": "FT02 Zero Trust (6) + incident response (6)",
     "tasks": ["Map each Zero Trust principle to a concrete control", "Rehearse the endpoint-security answer (reported question)", "Walk an incident from detection to escalation aloud"],
     "minutes": 240},
    {"day": 5, "date": "2026-10-11", "theme": "Mock interviews + STAR stories",
     "modules": ["IL27-FT03", "IL27-FT04"], "questionBank": "FT02 full bank, sampled",
     "tasks": ["Build all 6 STAR stories in your own words", "Run FT04 mock rounds 1-4, scored", "Re-take any round scoring below 70%"],
     "minutes": 300},
    {"day": 6, "date": "2026-10-12", "theme": "Review + logistics",
     "modules": ["IL27-FT05"], "questionBank": "FT02 weakest slices only",
     "tasks": ["Light review: weakest 15 questions only", "Complete the FT05 day-before checklist", "Lay out clothes, print resumes, plan route; sleep early"],
     "minutes": 120}
  ],
  "interviewDayNote": "Tue 2026-10-13, 9:00 AM ET. Follow the FT05 day-of timeline; arrive 8:35-8:40 AM."
}

# ---------------- FT01 ----------------
ft01 = {
  "id": "IL27-FT01", "code": "IL-27", "weight": 1, "estimatedMinutes": 120,
  "title": "ThreatLocker company deep-dive",
  "objectives": [
    "Describe ThreatLocker's business, products, and Zero Trust approach in 60 seconds without notes.",
    "Explain each core product (Allowlisting, Ringfencing, Storage/Elevation/Network Control, Configuration Management, Operational Alerts) in one plain sentence.",
    "State what is publicly known about their interview process and culture, with sources.",
    "Hold the independent-prep line: knowledgeable candidate, zero affiliation claims."
  ],
  "summary": "Know the company cold: what ThreatLocker sells, how Zero Trust shows up in their products, and what candidates publicly report about interviewing there. Independent preparation — this course is not affiliated with or endorsed by ThreatLocker.",
  "crossLinks": ["m24-company-cold", "m24-star-operator", "m24-default-deny", "m24-approve-deny-ringfence", "m24-endpoint-posture", "IL27-M14"],
  "cards": [
    {"front": "ThreatLocker in one sentence (public facts only)", "back": "Zero Trust endpoint-security company founded 2017 in Orlando, FL by Danny Jenkins, Sami Jenkins, and John Carolan. Public materials describe the team as 'Cyber Heroes' and the mission as a world where organizations operate free from cybercriminal influence."},
    {"front": "Name the core ThreatLocker platform components.", "back": "Application Allowlisting, Ringfencing, Storage Control, Elevation Control, Endpoint Network Control, Configuration Management, and Operational Alerts — a default-deny, Zero Trust approach to servers and endpoints."},
    {"front": "What is 'default-deny' / allowlisting, in one sentence?", "back": "Instead of trying to recognize every bad file, only explicitly approved applications are allowed to run — everything else is denied by default."},
    {"front": "What does Ringfencing do, in one sentence?", "back": "It limits what approved applications are allowed to do — e.g., blocking a trusted app from reaching the internet or touching sensitive files — containing weaponized legitimate software."},
    {"front": "What do candidates publicly report about ThreatLocker interviews? (Glassdoor, 31 interviews)", "back": "Easy-to-average difficulty (~2.45/5); many report brief, conversational interviews focused on background, eagerness, and culture fit. Reported questions include 'Could you build a virtual machine?', 'Why ThreatLocker?', and 'Why cybersecurity?'. Average ~18 days from first interview to offer per Glassdoor aggregates."},
    {"front": "What interview structure did ThreatLocker publicly describe for an IT-adjacent role?", "back": "For its Senior Technical Support Specialist posting: (1) technical phone interview, (2) product demo presentation back to the team, (3) onsite hands-on troubleshooting session. The Infrastructure Specialist loop may differ — prepare for all three formats."},
    {"front": "What hiring signal did multiple candidates report?", "back": "ThreatLocker hires career-starters in cybersecurity: one July 2026 candidate reported they are 'looking for people starting their career in cybersecurity — as long as you're eager you will be fine.' Eagerness + preparation is the signal."},
    {"front": "What post-offer screening do ThreatLocker's public postings describe?", "back": "Publicly posted roles describe a background check and drug/substance screening after a conditional offer. Expect it; keep documentation ready."},
    {"front": "What does public review data say about ThreatLocker's culture?", "back": "Glassdoor aggregates (public snippets): ~3.3/5 overall; in-office culture emphasized with no remote work; fast-paced, high-expectation environment; leadership praised in positive reviews. Frame your answers for an in-office, high-ownership culture."}
  ],
  "notes": [
    "Source discipline: every company fact above comes from ThreatLocker's public site, public job postings, or publicly visible candidate reports (Glassdoor snippets, fetched 2026-10-07). Full Glassdoor reviews sit behind a sign-in wall — noted as a limit, not bypassed.",
    "Independent-prep line for the interview: 'I've studied your public materials and platform approach closely' — never imply employment, endorsement, certification, or insider knowledge.",
    "Cross-link: IL-24 modules m24-company-cold, m24-default-deny, m24-approve-deny-ringfence, and m24-endpoint-posture rebuild this material from the assessment angle."
  ],
  "quiz": [
    {"q": "A interviewer asks: 'What does ThreatLocker do?' Give the 60-second answer structure.", "choices": ["List every product with technical deep-dives", "Zero Trust endpoint security (founded 2017, Orlando) → default-deny platform: Allowlisting, Ringfencing, Storage/Elevation/Network Control → mission framing", "Talk about their stock price", "Say you are not sure"], "answer": 1, "explain": "Company → approach → products → mission, in 60 seconds, all from public facts."},
    {"q": "How do Allowlisting and Ringfencing differ?", "choices": ["They are the same", "Allowlisting controls WHAT may run; Ringfencing controls what approved apps may DO", "Ringfencing is a firewall brand", "Allowlisting blocks the internet"], "answer": 1, "explain": "What runs vs. what it is permitted to do — the two halves of default-deny."},
    {"q": "Which statement respects the independent-prep guardrail?", "choices": ["'As a ThreatLocker-certified engineer...'", "'I've studied your public platform materials closely as an independent candidate'", "'My insider contact told me...'", "'I was promised this role'"], "answer": 1, "explain": "Knowledgeable candidate, zero affiliation claims, zero hiring-promise claims."}
  ]
}

# ---------------- FT02: 60-question bank ----------------
def bank(qid, category, question, provenance, sourceNote, modelAnswer, talkingPoints):
    assert provenance in ("reported by candidates", "likely")
    return {"id": qid, "category": category, "question": question, "provenance": provenance,
            "sourceNote": sourceNote, "modelAnswer": modelAnswer, "talkingPoints": talkingPoints}

ft02_questions = [
 # ---- Behavioral: 9 reported + 3 likely = 12 ----
 bank("FT02-B01", "Behavioral", "Why do you want to work at ThreatLocker?", "reported by candidates",
      "Reported by multiple Orlando candidates on Glassdoor (publicly visible, fetched 2026-10-07).",
      "Because ThreatLocker's default-deny, Zero Trust approach is the direction I believe endpoint security has to go, and I want to build my infrastructure career inside a company whose product philosophy I can defend. I've spent the last months studying your public platform materials and enrolled in the Zero Trust bootcamp on September 30th — I'm not casually interested, I'm invested.",
      ["Default-deny conviction, not generic praise", "Bootcamp enrollment Sept 30 as proof of initiative", "Infrastructure career framing"]),
 bank("FT02-B02", "Behavioral", "Why did you choose cybersecurity / IT infrastructure?", "reported by candidates",
      "Reported by a July 2026 Orlando candidate on Glassdoor.",
      "I started as a builder — homelabs, self-hosted infrastructure, DevSecOps work at my own company — and every system I built taught me the same lesson: the infrastructure decisions ARE the security decisions. I want to do that work where it matters most, inside a security company.",
      ["Builder origin story", "Infrastructure = security thesis", "Forward-looking, not backward-apologetic"]),
 bank("FT02-B03", "Behavioral", "Could you build a virtual machine?", "reported by candidates",
      "Reported by a hired Cyber Hero in Orlando on Glassdoor. Expect a hands-on follow-up.",
      "Yes — and I can walk you through it: choose the hypervisor, size vCPU/RAM/storage for the workload, create the virtual switch, attach the ISO, install the OS, apply baselines, snapshot before changes. I've done this repeatedly in my homelab with Hyper-V.",
      ["Answer yes with the concrete steps", "Name Hyper-V specifically", "Offer to whiteboard it on the spot"]),
 bank("FT02-B04", "Behavioral", "What do you know about endpoint security?", "reported by candidates",
      "Reported for a ThreatLocker Application Technician interview on Glassdoor.",
      "Endpoint security is the last line of defense on the device itself: controlling what runs, what it can do, and what leaves the machine. The strongest model I've studied is default-deny — allowlisting plus ringfencing so even trusted apps can't be weaponized — backed by baselines, patching, and EDR telemetry for what slips through.",
      ["Shows you studied THEIR model", "Layers: prevention, control, detection", "Ties to IL-27 M14/M23"]),
 bank("FT02-B05", "Behavioral", "What is the most technically difficult problem you've run into in your homelab?", "reported by candidates",
      "Reported for a ThreatLocker Application Technician interview — asked right after the candidate described their homelab.",
      "Migrating my live data to a RAID 0 array while keeping services up. The challenge was sequencing: verify backups, build the array, migrate in stages with checksums, and validate every service after cutover. It taught me that infrastructure work is really change-management work — the plan matters more than the commands.",
      ["Real history: RAID 0 migration", "Emphasize planning and verification", "End with the lesson learned"]),
 bank("FT02-B06", "Behavioral", "How do you respond to a frustrated or angry customer?", "reported by candidates",
      "Reported for a ThreatLocker Application Technician interview on Glassdoor.",
      "First I de-escalate: acknowledge the impact, not the tone. Then I take ownership of the next step with a clear ETA, communicate proactively until it's resolved, and document what happened so it doesn't recur. Frustration usually means they feel unheard — so I make sure they feel heard and then I fix it.",
      ["De-escalation first", "Ownership + ETA + follow-through", "Documentation as prevention"]),
 bank("FT02-B07", "Behavioral", "Tell me about a time you had a problem with a coworker and how you resolved it.", "reported by candidates",
      "Reported for a ThreatLocker Application Technician interview on Glassdoor.",
      "As a founder I've mostly managed myself, so I'll answer with how I handle disagreement: I separate the technical question from the personal one, state my reasoning with evidence, listen for what I'm missing, and converge on the option with the best trade-offs — then commit fully once decided. Disagree-and-commit beats silent resentment.",
      ["Honest about founder background", "Evidence-based disagreement", "Disagree-and-commit close"]),
 bank("FT02-B08", "Behavioral", "Tell me about yourself and your goals.", "reported by candidates",
      "Reported on Glassdoor's ThreatLocker interview page (publicly visible, fetched 2026-10-07); corroborated by the source-sweep worker's interview-experience mining.",
      "I'm a DevSecOps and full-stack builder — founder of Interstitium Labs — with deep homelab infrastructure experience: Windows Server, Active Directory, Hyper-V virtualization, networking, PowerShell automation, and endpoint hardening. I enrolled in ThreatLocker's Zero Trust bootcamp on September 30th and have spent the last week in focused interview preparation. My goal: become a trusted infrastructure specialist here and earn senior-level capability fast.",
      ["60-90 seconds, chronological", "Ends with the goal, not just history", "Honest junior positioning + ambition"]),
 bank("FT02-B09", "Behavioral", "Are you comfortable with rejection?", "reported by candidates",
      "Reported on Glassdoor; context suggests a sales-track interview — included for completeness.",
      "In infrastructure, 'rejection' looks like a change request being denied or a design being challenged — and I'm comfortable with both, because a no with a reason makes the system better. I separate the decision from my ego and ask what would make it a yes.",
      ["Reframe to infrastructure context", "Ego-free, reason-seeking"]),
 bank("FT02-B10", "Behavioral", "Tell me about a time you failed.", "likely",
      "Likely behavioral probe for resilience and honesty.",
      "Early in a homelab migration I skipped the verification step on a backup and discovered mid-cutover it was incomplete. I stopped, rebuilt the backup properly, and finished the migration a day late but with zero data loss. Now verification is a non-negotiable gate in every plan I write — I even built it into my runbook template.",
      ["Real pattern from his migration work", "Failure → system → prevention", "No blame-shifting"]),
 bank("FT02-B11", "Behavioral", "Where do you see yourself in two years?", "likely",
      "Likely closing question; tests ambition vs. flight risk.",
      "A trusted infrastructure specialist here — the person the team hands the hard escalations to — with certifications to match: Security+, AZ-800, AZ-801. I want depth in this stack and this company, not a quick hop.",
      ["Loyalty signal", "Cert plan as proof", "Role-specific, not generic"]),
 bank("FT02-B12", "Behavioral", "Why should we hire you over a more experienced candidate?", "likely",
      "Likely for a junior candidate; turn inexperience into an asset.",
      "Experience I can't fake, so I won't. What I offer: I learn systems end-to-end instead of memorizing steps, I document everything, I prepare obsessively — this interview is the proof — and I have no bad habits to unlearn. You'd be hiring trajectory, not just history.",
      ["Honest, not defensive", "Preparation as evidence", "Trajectory framing"]),
 # ---- Windows Server / AD: 8 likely ----
 bank("FT02-W01", "Windows Server/AD", "Walk me through promoting a new domain controller.", "likely",
      "Core AZ-800/AD DS competency for the role.",
      "Install the AD DS role, promote with dcpromo-equivalent wizard or Install-ADDSDomainController, verify DNS integration, check replication with repadmin, confirm SYSVOL replication, and validate FSMO placement. Then monitor event logs for the first 24 hours.",
      ["Role → promote → DNS → replication → validate", "Name repadmin and dcdiag"]),
 bank("FT02-W02", "Windows Server/AD", "A GPO isn't applying to a user. How do you troubleshoot?", "likely",
      "Classic AD troubleshooting scenario.",
      "Check scope: is the user/computer in the linked OU? Run gpresult /r to see what's applied and denied. Check link order, Enforced/Block Inheritance, security filtering, WMI filters, and replication — then gpupdate /force and re-check. Fix the scope issue, don't just re-link randomly.",
      ["gpresult first", "Scope, filtering, inheritance, replication", "Methodical, not random"]),
 bank("FT02-W03", "Windows Server/AD", "Explain OU design best practices.", "likely",
      "Tests AD design thinking.",
      "Design OUs around delegation and policy needs — not the org chart alone. Keep the structure shallow, separate users from computers where policies differ, use security groups for permissions rather than stuffing OUs, and document the design rationale so the next admin understands it.",
      ["Delegation-driven design", "Shallow hierarchy", "Groups for permissions"]),
 bank("FT02-W04", "Windows Server/AD", "How would you reset a user's password securely and communicate it?", "likely",
      "Tests operational security judgment.",
      "Verify identity first — never reset on an unverified request. Reset in ADUC or PowerShell, set 'must change at next logon' where policy requires, and deliver the temporary credential through a separate verified channel, never in the same message as the request.",
      ["Identity verification first", "Separate channel delivery", "Force change at logon"]),
 bank("FT02-W05", "Windows Server/AD", "What is the difference between share and NTFS permissions?", "likely",
      "High-frequency interview question; tests layered access understanding.",
      "Share permissions gate network access to the share; NTFS permissions gate the files themselves. Effective access is the MOST restrictive combination of the two. Best practice: set share to Everyone/Full Control and manage precisely with NTFS.",
      ["Most restrictive wins", "Best practice stated confidently"]),
 bank("FT02-W06", "Windows Server/AD", "How do you handle a suspected compromised domain account?", "likely",
      "Tests incident-response judgment on AD.",
      "Contain first: disable or force-reset the account, revoke sessions, check logons in the security event log for lateral movement. Then investigate scope before re-enabling — and review how it was compromised so the gap gets closed, not just the symptom.",
      ["Contain → investigate → remediate root cause", "Check for lateral movement"]),
 bank("FT02-W07", "Windows Server/AD", "Explain DHCP failover or scope design for a branch office.", "likely",
      "Tests network-services competence.",
      "Size the scope with headroom, set appropriate lease durations — shorter for guest/BYOD, longer for stable desktops — configure reservations for printers and infrastructure, and use DHCP failover or a second server so one failure doesn't take down addressing.",
      ["Sizing, leases, reservations, redundancy"]),
 bank("FT02-W08", "Windows Server/AD", "What would you check if replication between domain controllers is failing?", "likely",
      "Tests advanced AD troubleshooting.",
      "Start with the basics: network connectivity and DNS — replication lives or dies on name resolution. Then check time sync, repadmin /showrepl for errors, event logs, and firewall ports. Most replication failures are DNS or time, not AD itself.",
      ["DNS and time first", "repadmin /showrepl", "Most failures are environmental"]),
 # ---- Networking: 8 likely ----
 bank("FT02-N01", "Networking", "A user can't reach the internet but can reach local servers. Walk me through it.", "likely",
      "Bread-and-butter connectivity triage.",
      "Local works, so L1/L2 and the local stack are fine. Check the default gateway, then DNS — ping 8.8.8.8 to separate routing from name resolution. If IPs work but names don't, it's DNS; if neither works past the gateway, it's the gateway or upstream. Verify each layer before moving up.",
      ["Isolate: gateway vs DNS vs upstream", "Layered method, stated aloud"]),
 bank("FT02-N02", "Networking", "Explain subnetting to a non-technical manager.", "likely",
      "Tests communication skill, not just knowledge.",
      "Subnetting is dividing one big network into smaller neighborhoods. Each neighborhood gets its own address range, which keeps broadcast noise contained, lets us apply different security rules per area, and makes problems easier to locate. A /24 gives about 250 usable addresses — one neighborhood.",
      ["Analogy first", "Business reasons: security, troubleshooting", "No jargon dump"]),
 bank("FT02-N03", "Networking", "What is a VLAN and why would you use one?", "likely",
      "Core switching concept.",
      "A VLAN logically segments one physical switch into multiple broadcast domains. You'd use them to separate traffic types — workstations, servers, guests, VoIP — so a broadcast storm or compromise in one area doesn't take down the others, without buying separate switches.",
      ["Broadcast-domain isolation", "Security + resilience reasons"]),
 bank("FT02-N04", "Networking", "How does DNS resolution actually work, step by step?", "likely",
      "Tests depth on a fundamental service.",
      "The client asks its configured resolver; the resolver checks cache, then walks the hierarchy — root, TLD, authoritative — caching at each level, and returns the answer with a TTL. Failures at each step have distinct signatures, which is why understanding the chain matters for troubleshooting.",
      ["Hierarchy walk", "Cache and TTL", "Ties to troubleshooting"]),
 bank("FT02-N05", "Networking", "What would you look at first for intermittent network drops affecting one workstation?", "likely",
      "Tests single-host triage discipline.",
      "Physical layer first: cable, port, NIC — swap the patch cable and try another switch port. Then check for IP conflicts, duplex mismatch, and the workstation's event logs. Single-host intermittent issues are usually physical or configuration, not infrastructure-wide.",
      ["Physical first", "Swap-test methodology"]),
 bank("FT02-N06", "Networking", "Explain the difference between TCP and UDP and when you'd choose each.", "likely",
      "Fundamental protocol knowledge.",
      "TCP is connection-oriented with delivery guarantees — file transfers, web, email. UDP is fire-and-forget with low overhead — DNS queries, streaming, VoIP. You choose TCP when correctness matters and UDP when speed matters more than perfect delivery.",
      ["Guarantees vs speed", "Real examples each"]),
 bank("FT02-N07", "Networking", "What is NAT and why does it still matter?", "likely",
      "Tests address-space fundamentals.",
      "NAT translates private internal addresses to public ones at the network edge, which conserved IPv4 space and adds a layer of obscurity — internal addresses aren't directly reachable. It matters because nearly every office network still depends on it, even as IPv6 grows.",
      ["Conservation + obscurity", "Honest about IPv6 caveat"]),
 bank("FT02-N08", "Networking", "How would you secure a small office wireless network?", "likely",
      "Tests practical security judgment.",
      "WPA3 or WPA2-Enterprise, a strong unique admin password, guest network isolated on its own VLAN, disable WPS, keep firmware updated, and place APs based on a real survey — not just plugged in where convenient. Then document the configuration.",
      ["Encryption standard named", "Guest isolation via VLAN", "Documentation close"]),
 # ---- Virtualization: 6 likely ----
 bank("FT02-V01", "Virtualization", "Walk me through creating a Hyper-V virtual machine.", "likely",
      "Directly extends the reported 'Could you build a virtual machine?' question.",
      "Enable the Hyper-V role, create a virtual switch — external for network access — then create the VM: Generation 2 for modern OS, assign vCPUs and RAM with headroom, attach a dynamically expanding VHDX sized for the workload, mount the ISO, install the OS, install integration services, apply baselines, and take a checkpoint before any changes.",
      ["Step-by-step, in order", "Gen2 + VHDX specifics", "Checkpoint discipline"]),
 bank("FT02-V02", "Virtualization", "What is the difference between a VM and a container?", "likely",
      "Tests modern infrastructure literacy.",
      "A VM virtualizes hardware and runs a full guest OS — strong isolation, heavier. A container shares the host OS kernel and isolates at the process level — lighter and faster to start, but with a shared kernel. You pick VMs for strong isolation and heterogeneous OS needs, containers for dense, portable microservices.",
      ["Isolation level is the crux", "Trade-off framing"]),
 bank("FT02-V03", "Virtualization", "When would you use a checkpoint versus a backup?", "likely",
      "Tests operational judgment — common confusion.",
      "Checkpoints are for short-term rollback before a change — patching, config edits — and live on the same storage as the VM. Backups are for real recovery: off-host, tested restores, ransomware scenarios. A checkpoint is not a backup, and I'd never let anyone treat it as one.",
      ["Checkpoint ≠ backup", "Said with conviction"]),
 bank("FT02-V04", "Virtualization", "How do you decide how much RAM and CPU to give a VM?", "likely",
      "Tests capacity-planning thinking.",
      "Start from the workload's measured needs, not guesses — monitor the physical equivalent or pilot. Allocate with modest headroom, enable Dynamic Memory where appropriate, and watch host-level contention. Overprovisioning everything is just as bad as underprovisioning: it wastes resources and hides real bottlenecks.",
      ["Measure, don't guess", "Headroom + monitoring"]),
 bank("FT02-V05", "Virtualization", "What is a virtual switch and what are the types?", "likely",
      "Core Hyper-V networking.",
      "A virtual switch connects VMs to each other and to networks in software. External binds to a physical NIC for outside access; internal allows VM-to-host communication; private is VM-to-VM only. Choosing the wrong type is a classic 'VM has no network' root cause.",
      ["Three types, one sentence each", "Ties to troubleshooting"]),
 bank("FT02-V06", "Virtualization", "How would you troubleshoot a VM that won't boot?", "likely",
      "Tests layered virtualization triage.",
      "Check the VM state and Hyper-V event logs first, then walk the boot chain: virtual hardware present, ISO/VHDX attached and valid, boot order, Generation mismatch with the OS, and integration services. If the VHDX is corrupt, that's when the backup — not the checkpoint — conversation starts.",
      ["Logs first", "Boot-chain walk", "Backup honesty"]),
 # ---- Endpoint hardening: 7 likely ----
 bank("FT02-E01", "Endpoint hardening", "How would you harden a new Windows workstation before deployment?", "likely",
      "Direct endpoint-admin competency.",
      "Start from a known-good image or baseline: patch fully, remove bloatware, enforce BitLocker, configure Defender policies, apply least-privilege local accounts, disable unneeded services, set a standard firewall profile, enroll in management, and document the baseline so drift is detectable.",
      ["Baseline-first mindset", "Drift detection close"]),
 bank("FT02-E02", "Endpoint hardening", "What is least privilege and how do you apply it day-to-day?", "likely",
      "Tests security-culture fit.",
      "Users get only the access their job requires — no local admin for daily work, separate admin accounts for elevation, and regular reviews to prune what's stale. Day-to-day it means saying no to broad access requests and offering the narrow alternative that still unblocks the work.",
      ["Definition + practice", "Shows backbone on access requests"]),
 bank("FT02-E03", "Endpoint hardening", "How do you handle patching without breaking users' work?", "likely",
      "Tests operational maturity.",
      "Ringed rollouts: pilot group first, then broad deployment with deadlines and user notifications. Maintenance windows for servers, deferrals with hard deadlines for workstations, and expedited rings for critical zero-days. And a rollback plan before any fleet-wide push.",
      ["Rings + deadlines", "Expedited path for emergencies"]),
 bank("FT02-E04", "Endpoint hardening", "What would you do if EDR flags a workstation?", "likely",
      "Tests IR instincts on endpoints.",
      "Don't ignore it and don't nuke it immediately: isolate the host from the network while preserving state, review the alert context and timeline, escalate per the IR plan with severity, and let forensics determine scope before reimaging. Speed matters, but so does evidence.",
      ["Isolate, preserve, escalate", "Evidence-aware"]),
 bank("FT02-E05", "Endpoint hardening", "Explain BitLocker and when you'd enforce it.", "likely",
      "Core device-protection knowledge.",
      "BitLocker is full-disk encryption that protects data if a device is lost or stolen. I'd enforce it on every portable device via policy, escrow recovery keys centrally so a forgotten PIN doesn't mean data loss, and verify compliance rather than assuming it.",
      ["Why + how + key escrow", "Compliance verification"]),
 bank("FT02-E06", "Endpoint hardening", "How do you keep track of which devices are compliant?", "likely",
      "Tests management-at-scale thinking.",
      "Compliance policies define the healthy state — OS version, encryption, patch level — and the management platform reports compliance continuously. I watch trends, not just individual failures: a spike in noncompliance usually means a broken ring, a bad profile, or fleet drift, and that's the real problem to fix.",
      ["Policy-defined health", "Trends over tickets"]),
 bank("FT02-E07", "Endpoint hardening", "What is application allowlisting and why does it matter here?", "likely",
      "Directly connects his prep to ThreatLocker's model.",
      "Allowlisting flips the security model: instead of trying to recognize every bad file, only explicitly approved applications may run. It's ThreatLocker's core approach, and it matters because it stops unknown threats — zero-days, novel ransomware — that signature-based tools miss by definition.",
      ["Shows he studied their model", "Unknown-threat argument"]),
 # ---- PowerShell troubleshooting: 7 likely ----
 bank("FT02-P01", "PowerShell troubleshooting", "How would you find all disabled AD user accounts with PowerShell?", "likely",
      "Tests practical AD scripting.",
      "Get-ADUser with a filter on Enabled -eq $false, selecting name, last logon, and distinguished name, exported to CSV for review. One line for the query, but I'd wrap it in a script with logging if it becomes a recurring audit.",
      ["Cmdlet named", "Audit-ready output"]),
 bank("FT02-P02", "PowerShell troubleshooting", "A script works on your machine but fails on a server. What do you check?", "likely",
      "Tests real-world scripting troubleshooting.",
      "Execution policy, PowerShell version and module availability, permissions of the running account, and WinRM configuration for remoting. 'Works on my machine' failures are almost always environmental — so I check the environment systematically instead of rewriting the script.",
      ["Environmental checklist", "Methodical framing"]),
 bank("FT02-P03", "PowerShell troubleshooting", "How do you safely test a script that modifies production systems?", "likely",
      "Tests change discipline.",
      "WhatIf first, then a lab or pilot group, then production with logging and a rollback plan. Destructive cmdlets get -Confirm behavior reviewed and explicit safeguards. No script touches production untested — that's a rule, not a preference.",
      ["WhatIf → lab → production", "Rule, not preference"]),
 bank("FT02-P04", "PowerShell troubleshooting", "How would you check disk space across all servers quickly?", "likely",
      "Tests admin-scale scripting.",
      "A loop over the server list with Get-CimInstance for Win32_LogicalDisk via CIM sessions, collecting free space and percent free into a report, alerting under threshold. Ten minutes to write, saves hours of manual checking forever.",
      ["CIM over DCOM", "Report + threshold"]),
 bank("FT02-P05", "PowerShell troubleshooting", "Explain PowerShell remoting and its security considerations.", "likely",
      "Tests remoting depth.",
      "PowerShell remoting executes commands on remote machines over WinRM — the backbone of managing Server Core and fleets. Secure it with HTTPS listeners or constrained endpoints, JEA for least-privilege delegation, and never enable unencrypted basic auth across the network.",
      ["WinRM basis", "JEA + HTTPS hardening"]),
 bank("FT02-P06", "PowerShell troubleshooting", "How do you parse a large log file for errors efficiently?", "likely",
      "Tests text-processing practicality.",
      "Select-String with patterns for the error signatures, filtering by timestamp to narrow the window, and exporting matches with context lines. For recurring hunts, I'd parameterize it into a reusable function rather than retyping the pipeline every incident.",
      ["Select-String + context", "Reusable function habit"]),
 bank("FT02-P07", "PowerShell troubleshooting", "What is the pipeline and why does it matter?", "likely",
      "Tests conceptual PowerShell understanding.",
      "The pipeline passes rich .NET objects — not just text — between cmdlets, so you filter, sort, and act on structured data without parsing strings. It matters because it makes one-liners composable: get the objects, filter to the problem set, take action, all in one auditable line.",
      ["Objects not text", "Composability argument"]),
 # ---- Zero Trust principles: 6 likely ----
 bank("FT02-Z01", "Zero Trust principles", "What is Zero Trust in plain language?", "likely",
      "Must-answer for this company.",
      "Never trust, always verify. No device or user gets implicit trust just for being inside the network — every access request is authenticated, authorized against policy, and continuously re-evaluated based on identity, device health, and context.",
      ["One-sentence core", "Continuous, not one-time"]),
 bank("FT02-Z02", "Zero Trust principles", "How does Zero Trust change traditional network security?", "likely",
      "Tests architectural understanding.",
      "Traditional security built a hard perimeter with a soft interior — once inside, you were trusted. Zero Trust assumes breach, removes that implicit trust, and pushes enforcement to identity and every resource: micro-segmentation, least privilege, and continuous verification replace the castle-and-moat.",
      ["Castle-and-moat contrast", "Assume breach"]),
 bank("FT02-Z03", "Zero Trust principles", "What role does identity play in Zero Trust?", "likely",
      "Tests the identity-as-perimeter concept.",
      "Identity becomes the control plane — the new perimeter. Every decision starts with who is requesting, from what device, in what context. That's why MFA, conditional access, and privileged identity management aren't extras; they're the foundation everything else builds on.",
      ["Identity = perimeter", "MFA/CA as foundation"]),
 bank("FT02-Z04", "Zero Trust principles", "Give a concrete example of least privilege in infrastructure work.", "likely",
      "Tests applied, not theoretical, understanding.",
      "A helpdesk tech gets rights to reset passwords and unlock accounts — not domain admin. A backup service account can read the volumes it protects but can't log on interactively. I review these quarterly, because privilege creeps and every standing privilege is a future incident.",
      ["Concrete examples", "Review cadence"]),
 bank("FT02-Z05", "Zero Trust principles", "How does micro-segmentation limit damage?", "likely",
      "Tests containment thinking.",
      "By splitting the network into small isolated zones with explicit allow rules between them, a compromise in one segment can't freely move laterally. The attacker wins one room, not the building — and every cross-segment attempt generates a detectable event.",
      ["Blast-radius framing", "Detection bonus"]),
 bank("FT02-Z06", "Zero Trust principles", "How would you explain ThreatLocker's approach to a skeptical sysadmin?", "likely",
      "Tests ability to advocate the company's model credibly.",
      "I'd say: you already know signature-based tools miss novel threats — you've lived it. Default-deny flips the problem: instead of recognizing infinite bad, you approve finite good. Ringfencing then limits what even approved apps can do. It's the strictest version of least privilege, applied to software execution itself.",
      ["Empathy with the skeptic", "Finite-good vs infinite-bad framing"]),
 # ---- Incident response: 6 likely ----
 bank("FT02-I01", "Incident response", "Walk me through your incident response process.", "likely",
      "Core IR competency.",
      "Preparation, detection and analysis, containment, eradication, recovery, lessons learned. In practice: contain first to stop the bleeding — isolate hosts, disable accounts — preserve evidence, determine scope before declaring victory, recover in the right order with identity first, then write the after-action so it doesn't repeat.",
      ["Phases named", "Contain-first instinct", "After-action close"]),
 bank("FT02-I02", "Incident response", "You suspect ransomware on a file server. First three actions?", "likely",
      "Tests prioritization under pressure.",
      "One: isolate the server from the network immediately to stop spread. Two: alert per the IR plan and begin scoping — which shares, which accounts. Three: preserve evidence and verify clean backups exist before any recovery talk. Speed on containment, discipline on everything after.",
      ["Isolate → scope → preserve", "No premature recovery"]),
 bank("FT02-I03", "Incident response", "How do you determine the scope of a compromise?", "likely",
      "Tests investigative method.",
      "Start from the initial indicator and expand: authentication logs for the affected accounts, network connections from the host, persistence mechanisms, and timeline correlation across sources. Scope is a question you answer with evidence, not assumptions — and you keep expanding until the evidence stops, not until you're tired.",
      ["Evidence-driven expansion", "Timeline correlation"]),
 bank("FT02-I04", "Incident response", "When do you escalate versus handle it yourself?", "likely",
      "Tests judgment and humility.",
      "I handle what's in my scope and escalate when: the blast radius exceeds my authority, I see signs of active adversary presence, or I'm stuck past a reasonable timebox with no progress. Escalation isn't failure — late escalation is. I'd rather escalate early with a clean handoff than heroically fail alone.",
      ["Clear escalation criteria", "Early escalation > heroic failure"]),
 bank("FT02-I05", "Incident response", "What goes into a good after-action report?", "likely",
      "Tests learning culture.",
      "Timeline of what happened, root cause, what worked and what didn't in the response, and concrete action items with owners and dates. Blameless on people, ruthless on gaps. The report isn't done until the action items are tracked somewhere they'll actually get finished.",
      ["Blameless, actionable", "Action items with owners"]),
 bank("FT02-I06", "Incident response", "How do you communicate during an active incident?", "likely",
      "Tests comms under pressure.",
      "One clear channel, regular updates even when there's nothing new — 'still investigating, next update at :30' beats silence. Technical detail for the response team, impact and ETA for stakeholders, no speculation stated as fact. And everything important written down, because memory lies during incidents.",
      ["Cadence + honesty", "Audience-appropriate detail", "Write it down"]),
]

assert len(ft02_questions) == 60, len(ft02_questions)
reported = [q for q in ft02_questions if q["provenance"] == "reported by candidates"]
assert len(reported) == 9, len(reported)

ft02 = {
  "id": "IL27-FT02", "code": "IL-27", "weight": 2, "estimatedMinutes": 600,
  "title": "60-question interview Q&A bank with model answers",
  "objectives": [
    "Answer any of the 60 questions aloud, in under 90 seconds, without notes.",
    "Distinguish publicly reported ThreatLocker interview questions from likely probes — and nail both.",
    "Deliver model answers in your own words; never recite verbatim.",
    "Pair every technical answer with evidence from your real history."
  ],
  "summary": "Sixty interview questions across eight categories. Nine are publicly reported by ThreatLocker candidates on Glassdoor (marked 'reported by candidates' with context); the rest are likely probes authored for this infrastructure role (marked 'likely'). Model answers are starting points — rebuild each in your own words and anchor it to something you have actually done.",
  "crossLinks": ["IL27-M04", "IL27-M14", "IL27-M15", "m24-star-operator"],
  "provenanceKey": {
    "reported by candidates": "Publicly reported by ThreatLocker interview candidates on Glassdoor (publicly visible content, fetched 2026-10-07; corroborated by the source-sweep worker's interview-experience mining). Full reviews sit behind a sign-in wall — noted as a limit, not bypassed. Nine bank items carry this mark and together cover ten distinct reported questions (the two 'why ThreatLocker' variants are merged into FT02-B01).",
    "likely": "Authored for this IT Infrastructure Specialist role based on the certification domains and the two real ThreatLocker IT postings mined for the JD matrix. Not reported questions."
  },
  "categories": ["Behavioral", "Windows Server/AD", "Networking", "Virtualization", "Endpoint hardening", "PowerShell troubleshooting", "Zero Trust principles", "Incident response"],
  "questions": ft02_questions,
  "cards": [
    {"front": "How to use this bank (method)", "back": "Day 1-4: work one category per day aloud, 90 seconds per answer, recorded. Day 5: random sampling under mock conditions. Never memorize model answers word-for-word — interviewers detect recitation instantly."},
    {"front": "The 9 reported questions — name them cold", "back": "Build a VM? Why ThreatLocker? Why cybersecurity? What do you know about endpoint security? Hardest homelab problem? Frustrated customer? Coworker conflict? Walk through your background? (Comfortable with rejection — sales context.)"}
  ],
  "notes": [
    "Provenance honesty: if an interviewer asks where you prepared, say 'public candidate reports and your public materials' — never claim insider knowledge.",
    "The reported questions skew conversational and culture-fit; the technical depth in this bank is your edge — most candidates under-prepare the technical half."
  ],
  "quiz": [
    {"q": "An interviewer asks a 'reported' question: 'Could you build a virtual machine?' What is the winning structure?", "choices": ["Say yes and stop", "Yes + concrete ordered steps + offer to whiteboard it", "Talk about your favorite hypervisor's history", "Ask for the job description"], "answer": 1, "explain": "Yes, then prove it with steps, then offer to demonstrate — confidence plus evidence."},
    {"q": "How should you handle the 'likely' questions differently from the 'reported' ones?", "choices": ["Ignore the likely ones", "Prepare both identically: 90-second answers anchored to real experience", "Only study reported questions", "Memorize model answers verbatim"], "answer": 1, "explain": "Provenance tells you what to expect, not what to skip — both get the same rigorous preparation."}
  ]
}

# ---------------- FT03 ----------------
ft03 = {
  "id": "IL27-FT03", "code": "IL-27", "weight": 1, "estimatedMinutes": 180,
  "title": "STAR story builder — your real history only",
  "objectives": [
    "Tell six STAR stories from your actual history, each under two minutes.",
    "Map every story to the interview themes it serves.",
    "Hold the honesty line: enrolled (not completed), founder (not employee), homelab (not enterprise) — framed as strengths."
  ],
  "summary": "Six STAR stories built only from verified real history: founder/DevSecOps work, homelab builds, ThreatLocker bootcamp enrollment (Sept 30, 2026), and the October 7 interview-prep marathon. No invented jobs, no invented metrics — the truth, structured to land.",
  "crossLinks": ["m24-star-operator", "IL27-FT02"],
  "honestyNote": "Every story below is grounded in his real, documented history. 'Enrolled Sept 30' — never 'completed'. 'Founder' — never an invented employer. Homelab scale stated as homelab. If a story needs a number you don't have, drop the number.",
  "stories": [
    {"storyId": "FT03-S1", "title": "The bootcamp enrollment",
     "basedOn": "Enrolled in ThreatLocker's Zero Trust Cybersecurity Bootcamp on September 30, 2026 (documented).",
     "situation": "I decided to pursue infrastructure work inside the cybersecurity industry and needed to prove — to myself first — that I understood the Zero Trust model, not just the buzzword.",
     "task": "Build genuine working knowledge of default-deny, allowlisting, and ringfencing on a tight timeline before interviewing.",
     "action": "I enrolled in ThreatLocker's Zero Trust bootcamp on September 30th and worked through the material alongside hands-on lab study, mapping every concept to controls I'd actually operated in my homelab.",
     "result": "I can now explain and defend the default-deny model in depth — which is why I'm sitting in this interview able to discuss your platform approach substantively, not superficially.",
     "mapsTo": ["Why ThreatLocker?", "Initiative", "Continuous learning"],
     "honestyNote": "Say 'enrolled September 30th and working through it' — never imply completion."},
    {"storyId": "FT03-S2", "title": "The all-night prep marathon",
     "basedOn": "October 7, 2026: overnight interview-prep session (skills rebuild, practice test, mock interview, cheat sheet) ahead of a morning interview.",
     "situation": "The night before a major interview, I realized my skills narrative wasn't sharp enough — I was drawing a blank on articulating what I know.",
     "task": "Rebuild my skills story, test my knowledge, and walk in prepared — in one night.",
     "action": "I ran a full prep marathon: rebuilt my skills inventory, took a scored practice test, did a mock interview, and made a drive-over cheat sheet. I treated preparation like an engineering problem with a deadline.",
     "result": "I walked in composed and ready. That night proved something about how I work: when something matters, I prepare obsessively and systematically, not anxiously.",
     "mapsTo": ["Work ethic", "Preparation", "Handling pressure"],
     "honestyNote": "Factual: the prep session happened. Frame as discipline, not desperation."},
    {"storyId": "FT03-S3", "title": "Founder and DevSecOps builder",
     "basedOn": "Founder and DevSecOps/Full Stack Developer at Interstitium Labs (his stated title and role).",
     "situation": "As a founder, there is no escalation path — every infrastructure decision, outage, and security call terminates with you.",
     "task": "Design, build, secure, and operate production systems end-to-end with no team to hide behind.",
     "action": "I built and operated the full stack: infrastructure, CI/CD pipelines, security controls, and production operations — learning each layer by owning its failures, not by reading about them.",
     "result": "I developed the exact muscle this role needs: end-to-end ownership, systematic troubleshooting, and the habit of documenting everything because future-me is the on-call engineer.",
     "mapsTo": ["Ownership", "Breadth", "Self-direction"],
     "honestyNote": "Founder is the title; the work was real. Don't inflate team size or revenue."},
    {"storyId": "FT03-S4", "title": "The homelab migration",
     "basedOn": "Homelab infrastructure work: RAID 0 (E:) data migration, Proton pipeline operations, Hyper-V/VM builds (documented across his projects).",
     "situation": "My homelab outgrew its storage layout and I needed to migrate live data to a new RAID 0 array without losing anything.",
     "task": "Plan and execute a storage migration with zero data loss and minimal service interruption.",
     "action": "I verified backups first, built the array, migrated in staged batches with checksum verification, and validated every service after cutover — treating it with production change discipline.",
     "result": "Clean migration, zero data loss, and a reusable runbook. It's also why I can whiteboard a VM build or a migration plan on demand — I've done the reps.",
     "mapsTo": ["Technical depth", "Change discipline", "Homelab question (reported)"],
     "honestyNote": "Homelab scale, stated plainly — interviewers respect honest homelab depth."},
    {"storyId": "FT03-S5", "title": "Shipping the knowledge platform",
     "basedOn": "Built and deployed interstitiumlabs.dev / learn.interstitiumlabs.dev to production (documented).",
     "situation": "I set out to build a production-grade knowledge platform — not a demo, a real deployed system.",
     "task": "Ship enterprise-grade quality: no broken links, no half-finished pages, verified before every deploy.",
     "action": "I built automated verification gates — link integrity, content validity, production readiness — into the deploy process, so nothing ships broken. Every deploy is verified, not hoped.",
     "result": "A live production platform maintained to that bar continuously. That 'verify before you ship' discipline is exactly how I'd treat infrastructure changes here.",
     "mapsTo": ["Quality bar", "Project delivery", "Operational discipline"],
     "honestyNote": "Real shipped product. The quality-gate habit is the transferable point."},
    {"storyId": "FT03-S6", "title": "The honest junior",
     "basedOn": "His stated positioning: junior candidate aiming to earn senior-level capability; ThreatLocker's reported openness to cybersecurity career-starters.",
     "situation": "I'm interviewing as a junior infrastructure candidate against people with more years on paper.",
     "task": "Make the honest case for trajectory over tenure.",
     "action": "I've spent months in focused, verifiable preparation — bootcamp enrollment, certification-track study across A+, Network+, Security+, and Windows Server, and hands-on homelab reps. I learn systems end-to-end and document everything.",
     "result": "I'm not asking anyone to pretend I'm senior. I'm asking to be evaluated on trajectory, preparation, and how fast I close gaps — and this interview itself is the evidence.",
     "mapsTo": ["Why hire you?", "Ambition", "Honesty"],
     "honestyNote": "Never apologize for being junior; sell the slope, not the intercept."}
  ],
  "cards": [
    {"front": "STAR in 15 seconds", "back": "Situation (context) → Task (your responsibility) → Action (what YOU did, specifically) → Result (outcome + lesson). Under two minutes. End on the lesson."},
    {"front": "The honesty tripwires — what never to say", "back": "Never 'completed' the bootcamp (enrolled Sept 30). Never invent employers, metrics, or team sizes. Never claim certifications you don't hold. If pressed, say 'I don't have that yet — here's what I do have.'"}
  ],
  "notes": [
    "Rehearsal method: record each story, listen back, cut filler. Two minutes max per story.",
    "Every story must end with the lesson or the transferable skill — that's what interviewers remember."
  ],
  "quiz": [
    {"q": "An interviewer asks about the bootcamp. Which answer holds the honesty line?", "choices": ["'I completed ThreatLocker's bootcamp'", "'I enrolled September 30th and have been working through the Zero Trust material since — here's what I took from the default-deny model...'", "'I'm basically certified'", "'I didn't really do it'"], "answer": 1, "explain": "Enrolled + substance beats false completion every time — and they can verify."}
  ]
}

# ---------------- FT04 ----------------
ft04 = {
  "id": "IL27-FT04", "code": "IL-27", "weight": 2, "estimatedMinutes": 180,
  "title": "Mock interview module — timed and scored",
  "objectives": [
    "Complete four timed mock rounds and score at least 70% on each.",
    "Rehearse the demo-presentation format ThreatLocker publicly described.",
    "Convert every sub-70% round into a targeted re-take the same day."
  ],
  "summary": "Four timed, scored mock rounds modeled on the interview structure ThreatLocker publicly described for an IT-adjacent role (technical phone screen → demo presentation → onsite troubleshooting), plus a behavioral round. Framing is honest: the Infrastructure Specialist loop may differ — prepare for all formats.",
  "crossLinks": ["IL27-FT02", "IL27-FT03"],
  "formatFraming": "ThreatLocker publicly described a three-step process for its Senior Technical Support Specialist role: (1) technical phone interview, (2) product demo presentation back to the team, (3) onsite hands-on troubleshooting session. This mock mirrors that structure with a behavioral round added. The IT Infrastructure Specialist loop may differ.",
  "rounds": [
    {"round": 1, "title": "Technical phone screen", "minutes": 20, "questionCount": 8,
     "source": "Sample 8 from FT02 (mix reported + likely); answer aloud, 90 seconds each.",
     "scoring": "0-3 per question: 0 wrong/silent, 1 vague, 2 correct, 3 correct + evidence. Pass: >=17/24."},
    {"round": 2, "title": "Demo presentation", "minutes": 30, "questionCount": 1,
     "source": "Prepare and deliver a 10-minute whiteboard talk: 'How I would harden and document a new Windows Server for a Zero Trust environment.' Then 20 minutes of follow-up questions from FT02.",
     "scoring": "Clarity 0-6, technical accuracy 0-6, handling questions 0-6, time discipline 0-6. Pass: >=17/24."},
    {"round": 3, "title": "Onsite troubleshooting simulation", "minutes": 30, "questionCount": 3,
     "source": "Three scenarios, 10 minutes each, thinking aloud: (a) user can't reach the file share; (b) GPO not applying; (c) VM lost network after a change. Narrate the methodology, not just the answer.",
     "scoring": "Methodology 0-4, correct diagnosis 0-4, communication 0-4 per scenario. Pass: >=25/36."},
    {"round": 4, "title": "Behavioral and fit", "minutes": 15, "questionCount": 5,
     "source": "FT02 Behavioral slice: deliver 3 STAR stories plus 'why ThreatLocker' and 'why hire you'.",
     "scoring": "0-3 per answer: structure, honesty, evidence. Pass: >=11/15."}
  ],
  "overallRule": "Overall pass: all four rounds at or above their pass marks. Any round below → targeted study of its weakest questions → re-take the same day.",
  "cards": [
    {"front": "Thinking aloud — the meta-skill of round 3", "back": "Narrate: 'I'm checking X first because...'. Interviewers score the methodology they can hear, not the answer you reach silently."},
    {"front": "The demo-presentation trap", "back": "They're scoring communication clarity as much as technical depth. Structure: problem → approach → demo → trade-offs → questions. Finish early rather than ramble."}
  ],
  "notes": [
    "Do rounds 1-4 back-to-back on Day 5 to simulate interview fatigue.",
    "Record audio of every round. The playback reveals filler, hedging, and rambling you can't hear live."
  ],
  "quiz": []
}

# ---------------- FT05 ----------------
ft05 = {
  "id": "IL27-FT05", "code": "IL-27", "weight": 1, "estimatedMinutes": 90,
  "title": "Day-before and day-of checklist",
  "objectives": [
    "Arrive composed, early, and fully prepared on Tue Oct 13, 9:00 AM ET.",
    "Verify the interview location from the invitation before traveling.",
    "Carry everything needed: documents, proof of preparation, and calm."
  ],
  "summary": "Logistics win interviews before they start. Day-before preparation and a minute-by-minute day-of timeline for the October 13, 9:00 AM ET interview.",
  "crossLinks": ["IL27-FT01"],
  "locationNote": "Plan anchor: 1950 W Maitland Blvd, Orlando (per the interview invitation details provided). VERIFY against your invitation email before traveling — ThreatLocker's public listings show its headquarters at 1950 Summit Park Drive, Orlando, FL 32810, so confirm which address your interview uses.",
  "dayBefore": [
    "Confirm the interview address from the invitation email (see location note above). Map the route and drive it if possible.",
    "Print 5 copies of your resume on clean paper; prepare a one-page portfolio summary (homelab builds, bootcamp enrollment, cert track).",
    "Lay out professional attire; pack bag: resumes, portfolio summary, notebook + pen, photo ID, references list, phone charger, water.",
    "Review the 9 reported questions and your 6 STAR stories once — lightly. No cramming after 8 PM.",
    "Set two alarms. Target sleep by 10:30 PM."
  ],
  "dayOf": [
    "6:30 AM — wake, no snooze. Protein breakfast; no excess caffeine.",
    "7:00 AM — final review: 60-second 'why ThreatLocker', VM-build walkthrough, one STAR story. Then stop studying.",
    "7:45 AM — depart with 30+ minutes buffer. Account for Orlando morning traffic.",
    "8:35-8:40 AM — arrive. Check in calmly; breathe; review your one-page cheat sheet once, then put it away.",
    "9:00 AM — interview. Think aloud, anchor answers to real experience, hold the honesty line.",
    "After — send a brief thank-you note referencing something specific from the conversation."
  ],
  "screeningNote": "ThreatLocker's publicly posted roles describe a background check and drug/substance screening after a conditional offer. Keep a valid photo ID ready and expect this step — it is their standard process, not a surprise.",
  "whatToBring": ["5 printed resumes", "One-page portfolio summary", "Notebook and pen", "Photo ID", "References list", "Phone charger", "Water bottle", "Calm preparation"],
  "cards": [
    {"front": "The 5-minute pre-interview reset", "back": "Arrive → breathe (4 counts in, 6 out, 3 rounds) → recall one STAR story → remind yourself: 'trajectory, preparation, honesty' → walk in."},
    {"front": "If you don't know an answer", "back": "'I haven't hit that in production yet. Here's how I'd figure it out: [method].' Honesty + method beats bluffing every time — bluffing is detectable and fatal."}
  ],
  "notes": [
    "Eat before you go. Low blood sugar ruins more interviews than hard questions.",
    "Phone on silent before entering the building, not after sitting down."
  ],
  "quiz": []
}

# ---------------- FT06 ----------------
ft06 = {
  "id": "IL27-FT06", "code": "IL-27", "weight": 1, "estimatedMinutes": 60,
  "title": "Offer and onboarding readiness",
  "objectives": [
    "Evaluate an offer calmly against your criteria.",
    "Complete post-offer screening steps without friction.",
    "Arrive on day one with a 30/60/90 plan."
  ],
  "summary": "No hiring promise is made or implied — this module prepares you to handle an offer professionally if one comes: evaluation, screening, and a first-90-days plan that shows you're already thinking like an owner.",
  "crossLinks": [],
  "offerEvaluation": [
    "Compare total compensation, not just salary: benefits, growth path, and the value of the experience itself.",
    "Confirm role scope in writing: title, team, primary responsibilities, on-call expectations.",
    "Ask about the certification and training support — it signals a growth culture and funds your AZ/Security+ path.",
    "Take the full decision window; never accept on the spot from excitement."
  ],
  "screeningPrep": [
    "Background check and drug/substance screening follow a conditional offer per their public postings — keep ID and documentation ready.",
    "Ensure your references are warned and reachable.",
    "Keep your documented history consistent with what you stated in interviews."
  ],
  "first90Plan": [
    "Days 1-30: learn — document the environment as you discover it; ask questions; complete compliance and tooling onboarding; shadow escalations.",
    "Days 31-60: contribute — own L2 tickets end-to-end; propose one documentation improvement; start the first certification (Security+).",
    "Days 61-90: lead — own a small infrastructure improvement; present a lunch-and-learn on something you learned; have AZ-800 booked."
  ],
  "cards": [
    {"front": "The 30/60/90 in one line each", "back": "30: learn the environment and document it. 60: contribute independently and start certifying. 90: lead something small and teach something back."}
  ],
  "notes": ["Write the 30/60/90 on one page and bring it if a final-round conversation invites it — unprompted is fine only if the moment fits."],
  "quiz": []
}

fastTrackModules = [ft01, ft02, ft03, ft04, ft05, ft06]

out = {"fastTrack": fastTrack, "fastTrackModules": fastTrackModules}
with open(os.path.join(PARTS, "fasttrack.json"), "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("part5 ok: fastTrack", fastTrack["daysTotal"], "days,", len(fastTrackModules), "modules, FT02 =", len(ft02_questions), "Q&A (", len(reported), "reported )")
