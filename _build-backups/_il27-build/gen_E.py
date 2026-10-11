"""IL-27 Track E: Endpoint Management & Hardening (IL27-M23..M27)."""

MODULES_E = [
{
"id": "IL27-M23",
"code": "IL-27",
"title": "OS Imaging & Deployment",
"summary": "Deploy Windows at scale: golden images, MDT, Sysprep, PXE boot, and Autopilot. The skill behind every 'new hire laptop ready' story. You need this for -> M24/M25 and fleet onboarding.",
"objectives": [
"Build a sysprepped golden image and explain the generalize step.",
"Run an MDT deployment share: task sequences, drivers, applications.",
"Explain the PXE boot chain and its DHCP/DNS dependencies.",
"Compare imaging vs Autopilot/Intune provisioning.",
"Troubleshoot failed deployments via logs (BDD.log, SMSTS.log)."
],
"notes": [
{"title": "Golden images and Sysprep",
"body": "Golden image: a reference Windows install (updates, baseline apps, settings) captured to a WIM file, then deployed to fleets. The critical step: Sysprep /generalize - strips machine identity (SID, GUID, drivers) so clones don't collide. Skip it and you get duplicate SIDs, WSUS ID collisions, and KMS chaos.\n\nBuild the reference VM (never on physical hardware - driver pollution), snapshot, sysprep, capture with DISM. Thin vs thick vs hybrid images: thin (vanilla OS + apps installed at deploy - flexible, slower), thick (everything baked - fast, brittle), hybrid (OS + core apps baked, the rest at deploy - the sweet spot).\n\nModern shift: Microsoft pushes away from imaging toward cloud provisioning (Autopilot) - but imaging still rules for labs, specialized hardware, and offline builds. Know both; lead with the future."
},
{"title": "MDT: the free deployment workhorse",
"body": "Microsoft Deployment Toolkit (MDT): free, powerful, the classic. Components: Deployment Share (the repository), Task Sequences (the recipe: partition, apply image, inject drivers, install apps, join domain), boot images (WinPE - the mini-OS that starts it all), and the rules (CustomSettings.ini - ZeroTouch vs LiteTouch).\n\nDriver management: total control method (driver per model via WMI query) - import once, inject by model, never 'one driver pack for all'. Applications: silent installs (/quiet /norestart - test every installer manually first). The task sequence is code: version it, test changes on one model, then fleet.\n\nPXE chain (M14's options in action): PXE boot -> DHCP (IP + options 066/067) -> TFTP downloads WinPE boot image -> WinPE connects to deployment share -> task sequence runs. WDS (Windows Deployment Services) serves the PXE/TFTP side; MDT handles the logic."
},
{"title": "Autopilot and modern provisioning",
"body": "Windows Autopilot: cloud provisioning - the device ships from the OEM (or gets a hardware hash imported), user signs in, Intune pushes config/apps/policies. No imaging, no PXE, no on-prem infrastructure. Profiles: user-driven (employee sets up) vs self-deploying (kiosk/shared).\n\nWhen each wins: Autopilot for cloud-managed fleets and remote workers (zero-touch, anywhere); MDT/imaging for specialized hardware, labs, offline/air-gapped builds, and full OS customization. Hybrid reality: many orgs image the tricky 10% and Autopilot the rest.\n\nTroubleshooting: MDT -> BDD.log (the master log) and SMSTS.log (task sequence); PXE failures -> DHCP options/IP helpers; Autopilot -> Intune enrollment status, ESP (Enrollment Status Page) blocks, hardware hash import. 'It worked on this model but not that one' is always drivers - total control method exists for exactly this."
}
],
"cards": [
{"front": "Sysprep /generalize does what?", "back": "Strips machine identity (SID, GUID) so clones don't collide."},
{"front": "Thin vs thick vs hybrid images", "back": "Thin: vanilla+apps at deploy. Thick: all baked. Hybrid: OS+core baked (sweet spot)."},
{"front": "MDT task sequence is", "back": "The deployment recipe: partition, image, drivers, apps, domain join."},
{"front": "PXE chain order", "back": "DHCP (066/067) -> TFTP WinPE -> deployment share -> task sequence."},
{"front": "Driver method that scales", "back": "Total control: per-model injection via WMI query."},
{"front": "Autopilot vs MDT", "back": "Autopilot: cloud zero-touch provisioning. MDT: on-prem imaging."},
{"front": "MDT master log", "back": "BDD.log (overall); SMSTS.log (task sequence)."},
{"front": "'Works on model A, not B' = ?", "back": "Drivers - check per-model injection."}
],
"quiz": [
{"q": "Cloned PCs show duplicate SID issues in WSUS. Cause?", "choices": ["Image captured without Sysprep /generalize", "Too many PCs", "Network speed", "Old monitors"], "answer": 0, "index": 0, "explain": "Generalize resets identity before capture."},
{"q": "PXE boot: client gets IP but never loads WinPE. Check?", "choices": ["DHCP options 066/067 and WDS/TFTP health", "The monitor", "DNS only", "User password"], "answer": 0, "index": 0, "explain": "IP without boot info = PXE config gap."},
{"q": "200 remote workers need laptops, no on-prem infra. Choose?", "choices": ["Autopilot + Intune (cloud zero-touch)", "MDT + PXE", "USB sticks by mail", "Manual setup"], "answer": 0, "index": 0, "explain": "Cloud provisioning fits distributed fleets."},
{"q": "Specialized lab hardware with custom drivers, offline. Choose?", "choices": ["MDT imaging with total-control drivers", "Autopilot", "Hope", "Manual"], "answer": 0, "index": 0, "explain": "Imaging still wins for exotic/offline builds."},
{"q": "Task sequence fails at app install. First log?", "choices": ["BDD.log / SMSTS.log", "Event Viewer only", "The BIOS", "Email"], "answer": 0, "index": 0, "explain": "MDT's own logs narrate the failure."},
{"q": "Silent install switch testing matters because:", "choices": ["Untested installers hang task sequences waiting for input", "It's fun", "Microsoft requires it", "Faster typing"], "answer": 0, "index": 0, "explain": "Interactive prompts stall unattended deploys."},
{"q": "Hybrid image means:", "choices": ["OS + core apps baked; rest installed at deploy", "Two OSes", "Cloud only", "No drivers"], "answer": 0, "index": 0, "explain": "Balance of speed and flexibility."},
{"q": "Hardware hash import is for:", "choices": ["Registering devices for Autopilot", "Warranty", "Asset tags", "BIOS updates"], "answer": 0, "index": 0, "explain": "The hash enrolls the device identity with Autopilot."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M25"],
"drills": [
{"id": "m23-drill-image", "title": "Imaging Drill",
"items": [
{"prompt": "Before capturing a golden image", "answer": "Sysprep /generalize", "explain": "Strip machine identity."},
{"prompt": "PXE needs from DHCP", "answer": "Options 066/067", "explain": "Boot server + file."},
{"prompt": "MDT failure: read first", "answer": "BDD.log / SMSTS.log", "explain": "Deployment logs."},
{"prompt": "Model-specific drivers", "answer": "Total control via WMI query", "explain": "Per-model injection."},
{"prompt": "Zero-touch remote provisioning", "answer": "Autopilot + Intune", "explain": "Cloud-native deploy."},
{"prompt": "App hangs the task sequence", "answer": "Test silent switches manually first", "explain": "/quiet /norestart verified."}
]}
],
"handsOnLab": {
"id": "m23-lab",
"title": "Deploy Lab: MDT share + PXE + Autopilot plan",
"brief": "Build a working MDT deployment and document an Autopilot rollout plan.",
"steps": [
"Install MDT + ADK; create a deployment share; import a Windows ISO.",
"Build a task sequence (standard client); add one silent-install app.",
"Set up WDS for PXE; configure DHCP options 066/067 (or IP helper in lab).",
"PXE-boot a VM; run LiteTouch; verify domain join and app install.",
"Break it: wrong driver injected - diagnose via BDD.log, fix with total control.",
"Write the Autopilot rollout plan for 100 remote laptops (profiles, apps, ESP)."
],
"deliverable": "Working MDT deployment + break/fix log + Autopilot plan.",
"checkpoint": "You can deploy Windows at any scale, old way and new way."
},
"mockTask": {"id": "m23-mock", "type": "choice",
"q": "Interview: 'How would you deploy 500 new laptops?'",
"choices": ["Autopilot for the standard fleet (zero-touch) + MDT imaging for specialized models; drivers per-model; task sequences versioned; pilot group first", "Manual setup", "One USB stick", "Ship them blank"],
"answer": 0, "explain": "Modern primary, classic fallback, piloted - the complete answer."},
"crossLinks": ["il11-endpoint-management--autopilot-path"],
"videos": "VIDEOS_M23",
"estimatedMinutes": 260,
"fastTrackEligible": True
},
{
"id": "IL27-M24",
"code": "IL-27",
"title": "Patch Management Strategy",
"summary": "The discipline that stops most breaches: rings, cadences, WSUS/Intune mechanics, emergency lanes, and rollback. Interview-critical - 'how do you patch' reveals seniority. You need this for -> M32/M37.",
"objectives": [
"Design ring-based rollout (pilot/broad/critical) with timelines.",
"Operate the monthly cadence: Patch Tuesday through deadline.",
"Run the emergency out-of-band process for zero-days.",
"Measure compliance: reporting, SLAs, and exception handling.",
"Explain rollback options when a patch breaks something."
],
"notes": [
{"title": "Rings and cadence",
"body": "Rings: Pilot (IT + volunteers, day 1-3 - find the breakage), Broad (most of fleet, day 4-10), Critical (servers/Execs, day 11-14 with maintenance windows). Deadlines force installation; grace periods respect user work. No ring skips: even 'urgent' patches ride the emergency lane, not a shortcut.\n\nMonthly cadence: Patch Tuesday (second Tuesday) -> sync metadata -> pilot approvals -> monitor pilot 48-72h -> broad approvals -> deadline enforcement -> compliance report. Servers get their own windows (never 'reboot whenever' - cluster-aware updating for Hyper-V hosts, maintenance mode for app servers).\n\nThird-party patching (browsers, Adobe, Java, drivers) is where most fleets actually bleed - WSUS doesn't cover it; Intune/third-party tools do. A 'fully patched' Windows fleet with 2-year-old Chrome is not patched."
},
{"title": "Tooling: WSUS, Intune, and the mix",
"body": "WSUS (M15): on-prem, free, GPO-driven - approvals per group, deadlines, reporting. Great for traditional domains; weak on remote workers and third-party apps. Intune/Windows Update for Business: cloud policy - rings, deadlines, feature-update deferrals; reaches anywhere with internet; Autopatch (Microsoft-managed) for hands-off.\n\nMost real orgs: hybrid - WSUS or Intune for OS, a third-party tool (or Intune) for apps, and manual processes for firmware/network gear (switches, iDRAC, UPS - the forgotten patch surface). Document the matrix: system type -> tool -> cadence -> owner.\n\nCompliance reporting: % patched within SLA per ring, mean-time-to-patch for criticals, exception list with expirations. 'We're 98% compliant on criticals within 14 days' is the sentence leadership wants."
},
{"title": "Emergencies and rollbacks",
"body": "Zero-day lane: assess (is it exploitable in our environment?) -> pilot fast (hours, not days) -> broad within 24-48h -> emergency deadline -> verify. Pre-authorized: the emergency lane needs standing approval, or you'll debate while attackers work. Communication template ready: what, who, when, action required.\n\nRollback: Windows allows uninstalling most updates (wusa /uninstall /kb), Known Issue Rollback (KIR) via GPO for Microsoft-pushed fixes, and system restore/checkpoints for the brave. Test restores before you need them. Some updates can't roll back (servicing stack) - that's what the pilot ring is for.\n\nExceptions: documented, time-bound, risk-accepted (that legacy app that breaks on .NET updates). Review quarterly. An exception without an expiry is just negligence with paperwork."
}
],
"cards": [
{"front": "Ring order and timing", "back": "Pilot (1-3d) -> Broad (4-10d) -> Critical (11-14d) with deadlines."},
{"front": "WSUS vs Intune patching", "back": "WSUS: on-prem GPO-driven. Intune/WUfB: cloud, reaches remote, Autopatch option."},
{"front": "Most-missed patch surface", "back": "Third-party apps (browsers, Adobe) + firmware/network gear."},
{"front": "Zero-day lane steps", "back": "Assess -> fast pilot -> broad 24-48h -> emergency deadline -> verify."},
{"front": "Rollback options", "back": "wusa /uninstall, Known Issue Rollback (GPO), restore points."},
{"front": "Compliance sentence leadership wants", "back": "'X% patched on criticals within N days' per ring."},
{"front": "Exception rule", "back": "Documented, time-bound, risk-accepted, quarterly review."},
{"front": "Servers patch differently how?", "back": "Maintenance windows; cluster-aware updating; never random reboots."}
],
"quiz": [
{"q": "Pilot ring finds a patch breaking VPN. You:", "choices": ["Halt the rollout, assess scope, hold broad ring, engage vendor", "Push to broad anyway", "Uninstall everywhere", "Ignore pilot"], "answer": 0, "index": 0, "explain": "Pilot exists to catch exactly this."},
{"q": "Zero-day in the wild, exploitable remotely. Timeline?", "choices": ["Emergency lane: pilot in hours, broad within 24-48h", "Next Patch Tuesday", "Next quarter", "Never"], "answer": 0, "index": 0, "explain": "Standing emergency process, pre-authorized."},
{"q": "Fleet 'fully patched' but Chrome is 2 years old. Gap?", "choices": ["Third-party patching not covered by WSUS", "Windows Update is broken", "Users", "Antivirus"], "answer": 0, "index": 0, "explain": "OS patching != application patching."},
{"q": "Hyper-V cluster patching safely:", "choices": ["Cluster-Aware Updating (one node at a time, VMs live-migrated)", "Reboot all at once", "Never patch", "Manual one by one at noon"], "answer": 0, "index": 0, "explain": "CAU orchestrates zero-downtime host patching."},
{"q": "Patch breaks a line-of-business app fleet-wide. First?", "choices": ["Known Issue Rollback / uninstall via emergency change, then root-cause", "Blame the vendor publicly", "Reimage everything", "Wait"], "answer": 0, "index": 0, "explain": "Restore service, then investigate - in that order."},
{"q": "Exception for legacy app that can't take .NET updates:", "choices": ["Document, time-bound, risk-accepted, quarterly review", "Permanent verbal ok", "No exceptions ever", "Unplug it"], "answer": 0, "index": 0, "explain": "Exceptions are managed risk, not ignored risk."},
{"q": "Remote workers never on VPN aren't patching. Fix?", "choices": ["Intune/WUfB cloud patching (internet-reachable)", "More VPN", "Longer deadlines", "USB updates"], "answer": 0, "index": 0, "explain": "Cloud update management follows the user."},
{"q": "Patch compliance report should show:", "choices": ["% patched within SLA per ring + exceptions + MTTP for criticals", "Total patches", "Server names", "Colors"], "answer": 0, "index": 0, "explain": "SLA-based metrics drive decisions."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M32"],
"drills": [
{"id": "m24-drill-patch", "title": "Patch Strategy Drill",
"items": [
{"prompt": "Ring timeline", "answer": "Pilot 1-3d, Broad 4-10d, Critical 11-14d", "explain": "Staged with deadlines."},
{"prompt": "Zero-day in the wild", "answer": "Emergency lane, broad in 24-48h", "explain": "Pre-authorized fast track."},
{"prompt": "Patch broke the app", "answer": "KIR/uninstall, then root-cause", "explain": "Restore, then investigate."},
{"prompt": "Remote workers unpatched", "answer": "Intune/WUfB cloud patching", "explain": "Internet-reachable updates."},
{"prompt": "Cluster hosts need patching", "answer": "Cluster-Aware Updating", "explain": "Zero-downtime node cycling."},
{"prompt": "Chrome 2 years old on 'patched' fleet", "answer": "Add third-party patching", "explain": "WSUS doesn't cover apps."}
]}
],
"handsOnLab": {
"id": "m24-lab",
"title": "Patch Program: design the whole machine",
"brief": "Design a complete patch management program document for a fictional 500-seat org.",
"steps": [
"Define rings, timelines, and deadlines for workstations and servers.",
"Map tools: OS (WSUS/Intune), third-party apps, firmware/network gear - tool per surface.",
"Write the monthly cadence runbook (Patch Tuesday to compliance report).",
"Write the zero-day emergency runbook (roles, approvals, comms template).",
"Define compliance metrics and the exception process.",
"Simulate: run a tabletop where a pilot-ring patch breaks VPN - execute your runbook."
],
"deliverable": "Patch program document + two runbooks + tabletop notes.",
"checkpoint": "You can own patching for an organization, not just click approve."
},
"mockTask": {"id": "m24-mock", "type": "choice",
"q": "Interview: 'How do you handle patching for 500 machines?'",
"choices": ["Ring-based rollout with deadlines, WSUS/Intune per surface, third-party coverage, monthly cadence, emergency lane, compliance reporting, managed exceptions", "Approve all immediately", "Never patch", "Manual updates"],
"answer": 0, "explain": "Program thinking, not tool clicking."},
"crossLinks": ["il24-default-deny--patch-governance"],
"videos": [],
"estimatedMinutes": 240,
"fastTrackEligible": True
},
{
"id": "IL27-M25",
"code": "IL-27",
"title": "MDM & Intune Concepts",
"summary": "Modern device management: Intune enrollment, compliance, configuration profiles, and Autopilot's partner. You need this for -> M23/M28 and every modern endpoint conversation.",
"objectives": [
"Compare GPO vs Intune management and know when each applies.",
"Enroll devices (Autopilot, bulk, BYOD) and explain the profiles.",
"Build compliance policies and Conditional Access integration.",
"Deploy apps and updates via Intune.",
"Troubleshoot enrollment and policy failures."
],
"notes": [
{"title": "The management plane shift",
"body": "GPO: on-prem, domain-joined, LAN-centric, 20 years of power. Intune: cloud, internet-centric, MDM protocol (OMA-DM) + MAM for apps. Co-management (ConfigMgr + Intune): the bridge - workloads (compliance, apps, updates) slide from on-prem to cloud one by one.\n\nEnrollment: Autopilot (zero-touch, M23), bulk enrollment packages, BYOD (work profile / MAM without full enrollment). Enrollment IS the trust moment - device identity + compliance attestation begins here. A device that can't enroll can't be trusted, full stop.\n\nProfiles vs policies: Configuration profiles (settings - like GPO), Compliance policies (rules: encryption on, OS version, jailbreak detection), App deployment (required/available/uninstall). Assignment by Entra groups - dynamic groups (all Windows 11 laptops) do the targeting work."
},
{"title": "Compliance as the Zero Trust signal",
"body": "Compliance policy: the device health checklist - BitLocker on, Defender active, OS patched, no jailbreak, password complexity. Noncompliant -> Conditional Access blocks corporate apps (M17's engine consuming Intune's signal). This is Zero Trust in action: access decisions from live device posture, not network location.\n\nRemediation: auto-remediate where possible (require encryption -> Intune can trigger it), notify the user with grace periods, then block. The user experience matters: 'your device needs an update to access email' beats a silent block.\n\nMonitoring: per-device compliance state, policy assignment status, enrollment errors. Intune's 'what if' equivalent: test assignments on pilot groups. A compliance policy typo can block the CEO's email - pilot everything."
},
{"title": "Apps, updates, and troubleshooting",
"body": "App deployment: Win32 apps (wrapped with the prep tool), Microsoft 365 apps, Store apps, required (auto-install) vs available (company portal). Dependencies and supersedence chain versions properly. Update rings (M24's rings, cloud edition): feature update deferrals, quality update deadlines.\n\nTroubleshooting: enrollment failures -> check Entra join state, MDM authority, licenses (Intune license required!); policy not applying -> assignment, group membership, sync (manual sync from Company Portal), conflicting profiles (Intune shows conflicts explicitly); app install fail -> wrapped correctly? detection rules? logs on device.\n\nThe interview line: 'Intune is how I manage devices that never touch the LAN; GPO is how I manage the ones that live on it; co-management is the migration path.'"
}
],
"cards": [
{"front": "GPO vs Intune", "back": "GPO: on-prem domain, LAN. Intune: cloud MDM, internet. Co-management bridges."},
{"front": "Enrollment methods", "back": "Autopilot, bulk packages, BYOD (MAM/work profile)."},
{"front": "Compliance policy feeds", "back": "Conditional Access - device posture drives access decisions."},
{"front": "Required vs Available apps", "back": "Required: auto-install. Available: Company Portal self-service."},
{"front": "Win32 app packaging", "back": "IntuneWin prep tool wraps installers with detection rules."},
{"front": "Policy not applying: check?", "back": "Assignment/groups, manual sync, conflicting profiles."},
{"front": "MDM authority must be", "back": "Set to Intune in Entra (else enrollment fails)."},
{"front": "Intune license requirement", "back": "Users need Intune licenses or enrollment fails silently-ish."}
],
"quiz": [
{"q": "Remote laptops never on LAN need management. Choose?", "choices": ["Intune (cloud MDM)", "GPO only", "Manual", "Nothing"], "answer": 0, "index": 0, "explain": "Internet-reachable management plane."},
{"q": "Unencrypted laptop tries to access corporate email. With Intune+CA:", "choices": ["Blocked: noncompliant device fails Conditional Access", "Allowed", "Wiped instantly", "Ignored"], "answer": 0, "index": 0, "explain": "Compliance signal drives the access decision."},
{"q": "Enrollment fails for new users. Check?", "choices": ["Intune licenses assigned + MDM authority set", "The weather", "Printer", "DNS only"], "answer": 0, "index": 0, "explain": "The two classic enrollment blockers."},
{"q": "Migrate GPO-managed fleet to cloud gradually:", "choices": ["Co-management: slide workloads to Intune one by one", "Big bang", "Never", "Two domains"], "answer": 0, "index": 0, "explain": "Workload-by-workload migration."},
{"q": "Two profiles set conflicting values. Intune:", "choices": ["Shows the conflict explicitly per device", "Picks randomly", "Crashes", "Ignores both"], "answer": 0, "index": 0, "explain": "Conflict reporting beats GPO's silent last-writer."},
{"q": "BYOD phones need corporate email without full control:", "choices": ["MAM / app protection policies (no enrollment)", "Full wipe rights", "No email", "Personal VPN"], "answer": 0, "index": 0, "explain": "App-level management respects personal ownership."},
{"q": "Deploy an app to 500 devices automatically:", "choices": ["Required assignment to a dynamic device group", "Email the installer", "USB drives", "Hope"], "answer": 0, "index": 0, "explain": "Required + dynamic targeting = hands-free."},
{"q": "Pilot group for a new compliance policy because:", "choices": ["A typo can block everyone's email - test first", "It's fun", "Microsoft requires it", "Slower is better"], "answer": 0, "index": 0, "explain": "Blast radius control."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M28"],
"drills": [
{"id": "m25-drill-intune", "title": "Intune Drill",
"items": [
{"prompt": "Cloud device management", "answer": "Intune (MDM)", "explain": "Internet-centric plane."},
{"prompt": "Zero-touch enrollment", "answer": "Autopilot", "explain": "Hardware hash + profiles."},
{"prompt": "Device health checklist", "answer": "Compliance policy", "explain": "Feeds Conditional Access."},
{"prompt": "Enrollment failing: check?", "answer": "Licenses + MDM authority", "explain": "Classic blockers."},
{"prompt": "Auto-install app to fleet", "answer": "Required assignment", "explain": "Vs Available self-service."},
{"prompt": "Gradual GPO->cloud move", "answer": "Co-management", "explain": "Workload by workload."}
]}
],
"handsOnLab": {
"id": "m25-lab",
"title": "Intune Mini-Tenant: enroll, comply, deploy",
"brief": "Use a trial tenant to run the full Intune lifecycle on a test device.",
"steps": [
"Trial tenant: set MDM authority to Intune; assign yourself a license.",
"Enroll a test VM (or device); verify in Intune portal.",
"Create a compliance policy (encryption, OS version); verify compliance state.",
"Create a Conditional Access policy requiring compliant device for a test app.",
"Deploy an app as Required to a dynamic group; verify auto-install.",
"Break it: make the device noncompliant; verify access blocks; remediate."
],
"deliverable": "Tenant config + compliance/CA policies + app deployment + break/fix evidence.",
"checkpoint": "You can run modern device management end to end."
},
"mockTask": {"id": "m25-mock", "type": "choice",
"q": "Interview: 'GPO or Intune?'",
"choices": ["GPO for on-prem domain-joined LAN fleets; Intune for cloud-managed and remote devices; co-management to migrate between them", "Only GPO", "Only Intune", "Neither"],
"answer": 0, "explain": "Horses for courses, with a migration path."},
"crossLinks": ["il11-entra-identity--sc300-zerotrust-ca", "il11-endpoint-management--autopilot-path"],
"videos": "VIDEOS_M25",
"estimatedMinutes": 260,
"fastTrackEligible": False
},
{
"id": "IL27-M26",
"code": "IL-27",
"title": "Endpoint Hardening Checklists (CIS-Concept)",
"summary": "Harden Windows endpoints systematically: CIS Benchmark concepts, baselines, LAPS, BitLocker, Defender. Interview-critical - hardening is a core ThreatLocker-adjacent skill. You need this for -> M27/M28/M32.",
"objectives": [
"Apply CIS Benchmark concepts via baselines and GPO/Intune.",
"Deploy LAPS for local admin password management.",
"Enforce BitLocker with key escrow and verify compliance.",
"Configure Defender AV/ASR rules and interpret detections.",
"Build a hardening checklist and measure drift."
],
"notes": [
{"title": "Baselines: CIS Benchmarks in practice",
"body": "CIS Benchmarks: consensus hardening guides (Level 1 = safe for most, Level 2 = high security, some breakage risk). You don't memorize 300 settings - you apply the benchmark via GPO/Intune baseline, test on pilot, handle exceptions. Microsoft's Security Baselines (built into Intune/GPO) are the equivalent starting point.\n\nThe workflow: import baseline -> compare against current (what changes?) -> pilot -> exceptions documented -> deploy -> monitor drift (compliance policies re-check). 'We hardened to CIS L1 with 12 documented exceptions' is audit-ready language.\n\nKey settings families: password/lockout (via AD), audit policy (logon events, privilege use), user rights (who can do what), security options (guest, autorun, LLMNR - disable the legacy protocols attackers love), Defender, firewall, BitLocker."
},
{"title": "LAPS, BitLocker, and local attack surface",
"body": "LAPS (Local Administrator Password Solution / Windows LAPS now built-in): unique random local admin password per machine, rotated, stored in AD/Entra. Kills lateral movement via shared local passwords - one of the highest-ROI hardening moves that exists.\n\nBitLocker: full-disk encryption - TPM + PIN for pre-boot auth on sensitive machines; recovery keys escrowed to AD/Entra (a BitLockered laptop with the key only in the user's head is a data-loss incident). Verify with compliance policy; the M25 signal feeds access decisions.\n\nLocal attack surface: disable LLMNR/NBT-NS (poisoning attacks), SMBv1 (WannaCry's vector - gone in modern Windows), Autorun, guest account, and unnecessary services. Each disabled legacy protocol is a closed attacker door."
},
{"title": "Defender and the hardening loop",
"body": "Microsoft Defender: AV + EDR sensor in one. ASR rules (Attack Surface Reduction): block Office macros from internet, block credential stealing from LSASS, block process injection - each rule in audit mode first (what WOULD break?), then block. Controlled folder access vs ransomware.\n\nHardening loop: baseline -> deploy -> monitor (Defender Secure Score, compliance) -> drift remediation -> re-baseline. Secure Score is gamified but directionally useful. Vulnerability management (Defender) shows exposed CVEs per device - feed it into M24's patching.\n\nThe checklist (your deliverable): per device type (laptop/desktop/server/kiosk), the settings, the enforcement method (GPO/Intune), the verification (compliance), and the exception process. A hardening checklist that isn't measured is a wish list."
}
],
"cards": [
{"front": "CIS L1 vs L2", "back": "L1: safe for most. L2: high security, some breakage risk."},
{"front": "LAPS solves what?", "back": "Shared local admin passwords -> unique, rotated, escrowed per machine."},
{"front": "BitLocker key escrow", "back": "Recovery keys to AD/Entra - never only in someone's head."},
{"front": "ASR rule rollout", "back": "Audit mode first (measure breakage), then block."},
{"front": "Disable these legacy protocols", "back": "LLMNR/NBT-NS, SMBv1, Autorun, Guest."},
{"front": "Hardening loop", "back": "Baseline -> deploy -> monitor drift -> remediate -> re-baseline."},
{"front": "Secure Score is", "back": "Directionally useful gamification - not a security guarantee."},
{"front": "Checklist without measurement is", "back": "A wish list - enforce via GPO/Intune, verify via compliance."}
],
"quiz": [
{"q": "Lateral movement via shared local admin password. Fix?", "choices": ["Deploy LAPS (unique per-machine passwords)", "Longer shared password", "Disable admin", "Hope"], "answer": 0, "index": 0, "explain": "Unique credentials kill pass-the-hash lateral paths."},
{"q": "New ASR rule to block mode. Before enforcing:", "choices": ["Audit mode: measure what would break", "Enforce immediately", "Never use ASR", "Email users"], "answer": 0, "index": 0, "explain": "Audit first = known blast radius."},
{"q": "BitLockered laptop, user forgot PIN, no escrow. Result?", "choices": ["Data loss - this is why keys escrow to AD/Entra", "Call Microsoft", "Reboot fixes it", "Safe mode"], "answer": 0, "index": 0, "explain": "Encryption without key management is a lockout machine."},
{"q": "CIS L2 setting breaks a legacy app. You:", "choices": ["Documented exception + compensating control, review quarterly", "Abandon hardening", "Uninstall the app silently", "Ignore the benchmark"], "answer": 0, "index": 0, "explain": "Exceptions are managed, not forbidden."},
{"q": "Attacker tool abuses LLMNR for credential capture. Prevention?", "choices": ["Disable LLMNR/NBT-NS via GPO", "Longer passwords only", "More RAM", "New switches"], "answer": 0, "index": 0, "explain": "Remove the protocol, remove the attack."},
{"q": "How do you know hardening is still applied in 6 months?", "choices": ["Compliance policies + drift monitoring", "Trust", "Annual email", "Screenshots"], "answer": 0, "index": 0, "explain": "Continuous verification beats point-in-time."},
{"q": "Controlled folder access protects against:", "choices": ["Ransomware encrypting protected folders", "Phishing", "DDoS", "Insiders with legit access"], "answer": 0, "index": 0, "explain": "Only trusted apps modify protected folders."},
{"q": "First 3 hardening moves for a new fleet?", "choices": ["LAPS + BitLocker with escrow + Defender baseline", "Wallpaper policy", "New monitors", "Faster Wi-Fi"], "answer": 0, "index": 0, "explain": "Highest-ROI controls first."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M27", "IL27-M28"],
"drills": [
{"id": "m26-drill-harden", "title": "Hardening Drill",
"items": [
{"prompt": "Shared local admin passwords", "answer": "Deploy LAPS", "explain": "Unique per machine."},
{"prompt": "New ASR rule: first step", "answer": "Audit mode", "explain": "Measure breakage first."},
{"prompt": "Lost BitLocker PIN, no escrow", "answer": "Data loss - escrow keys!", "explain": "Key management is the control."},
{"prompt": "Legacy protocols to kill", "answer": "LLMNR, NBT-NS, SMBv1, Autorun", "explain": "Attacker favorites."},
{"prompt": "Prove hardening persists", "answer": "Compliance + drift monitoring", "explain": "Continuous verification."},
{"prompt": "Benchmark breaks legacy app", "answer": "Documented exception + compensating control", "explain": "Managed risk."}
]}
],
"handsOnLab": {
"id": "m26-lab",
"title": "Harden Lab: baseline to verified",
"brief": "Harden your lab fleet to a CIS-L1-concept baseline and prove it.",
"steps": [
"Deploy Windows LAPS via GPO/Intune on lab clients; verify unique passwords in AD.",
"Enforce BitLocker with key escrow; verify recovery keys retrievable.",
"Apply a security baseline (Intune baseline or GPO import); document deviations.",
"Disable LLMNR/NBT-NS/SMBv1 via GPO; verify with scans.",
"Enable 3 ASR rules in audit mode; review what would have blocked; enforce 1.",
"Build the hardening checklist doc: setting, enforcement, verification, exceptions."
],
"deliverable": "Hardened lab + checklist + verification evidence.",
"checkpoint": "You can harden endpoints systematically and prove it."
},
"mockTask": {"id": "m26-mock", "type": "choice",
"q": "Interview: 'How would you harden 500 Windows endpoints?'",
"choices": ["CIS L1 baseline via GPO/Intune, LAPS, BitLocker with escrow, Defender ASR (audit then block), kill legacy protocols, compliance monitoring for drift, documented exceptions", "Install antivirus", "Hope", "Reimage yearly"],
"answer": 0, "explain": "Systematic, layered, measured - the professional answer."},
"crossLinks": ["il11-active-directory-defense--zt-ad-harden", "il24-approve-deny-ringfence--m24-allowlist-ops"],
"videos": [],
"estimatedMinutes": 300,
"fastTrackEligible": True
},
{
"id": "IL27-M27",
"code": "IL-27",
"title": "Application Control & Allowlisting Concepts",
"summary": "Default-deny for executables: AppLocker, WDAC, and the allowlisting mindset behind ThreatLocker's world. Interview-critical. You need this for -> M28 and the Zero Trust story.",
"objectives": [
"Explain allowlisting vs blocklisting and why default-deny wins.",
"Design AppLocker rules (publisher/path/hash) and rollout stages.",
"Describe WDAC (Device Guard) and when it supersedes AppLocker.",
"Run the audit-then-enforce rollout without breaking the business.",
"Connect allowlisting to the Zero Trust narrative."
],
"notes": [
{"title": "The default-deny mindset",
"body": "Blocklisting (antivirus model): allow everything except known-bad. Allowlisting: deny everything except known-good. The math: malware variants are infinite; your approved app catalog is finite. Default-deny is the only model that handles unknown threats - which is why it's a Zero Trust pillar and the core of companies built on allowlisting.\n\nIndependent framing: this course teaches the CONCEPT and the built-in Windows tools. Commercial products (including ThreatLocker's) productize this with central management, but the principle and the rollout discipline are tool-agnostic - and that's what interviews test.\n\nWhere it applies: fixed-function devices first (kiosks, POS, lab machines), then servers (predictable workloads), then knowledge-worker fleets (hardest - app sprawl). Start where the app catalog is smallest."
},
{"title": "AppLocker: the built-in workhorse",
"body": "AppLocker (Enterprise/Education): rules for executables, scripts, installers, packaged apps. Rule types: Publisher (signed, version-flexible - the maintainable choice), Path (simple, bypassable by file moves), Hash (exact binary - brittle, breaks on updates). Default rules first (allow Windows + Program Files), then your allow rules.\n\nRollout: Audit mode (log what WOULD block - Event Log) -> analyze (which legit apps hit?) -> build rules -> enforce on pilot -> fleet. The audit phase is non-negotiable: enforcing blind breaks the business on day one. Exceptions via rule collections per OU/group.\n\nMaintenance: publisher rules survive updates (version ranges); new apps need rule requests (the ticketing workflow - M04's process applied). Users requesting software becomes a governed pipeline, not a hallway conversation."
},
{"title": "WDAC and the enterprise picture",
"body": "WDAC (Windows Defender Application Control, formerly Device Guard): kernel-level enforcement, stronger than AppLocker (which is user-mode and bypassable by admins). Policy in signed XML; can require HVCI (memory integrity). Use WDAC where tamper-resistance matters: servers, high-security endpoints.\n\nManaged Installer / Intelligent Security Graph: trust apps deployed by your management tool (Intune) automatically - the modern answer to 'how do we allow without whitelisting every binary'. Combined with reputation-based rules, this scales allowlisting to real fleets.\n\nThe interview narrative: 'Allowlisting is default-deny for code. I start with audit mode to map the real app catalog, roll out publisher rules by device tier, and maintain it as a governed request pipeline. It's the endpoint enforcement of Zero Trust - every execution is an access decision.'"
}
],
"cards": [
{"front": "Allowlisting vs blocklisting", "back": "Allow: deny-all-except-approved. Block: allow-all-except-known-bad. Default-deny handles unknowns."},
{"front": "AppLocker rule types (best to worst)", "back": "Publisher (maintainable) > Path (simple, bypassable) > Hash (brittle)."},
{"front": "AppLocker rollout order", "back": "Audit -> analyze -> rules -> pilot enforce -> fleet."},
{"front": "WDAC vs AppLocker", "back": "WDAC: kernel-level, tamper-resistant. AppLocker: user-mode, easier, bypassable by admins."},
{"front": "Start allowlisting where?", "back": "Fixed-function devices -> servers -> knowledge workers (easiest catalog first)."},
{"front": "Managed Installer concept", "back": "Auto-trust apps deployed by your management tool."},
{"front": "Default rules first because", "back": "Allow Windows/Program Files or you brick the OS on enforcement."},
{"front": "New app request becomes", "back": "A governed ticket pipeline, not hallway conversation."}
],
"quiz": [
{"q": "Why does allowlisting beat antivirus against novel malware?", "choices": ["Default-deny blocks unknown code; blocklists only know known-bad", "It's cheaper", "It's faster", "Antivirus is dead"], "answer": 0, "index": 0, "explain": "Unknown threats are the gap blocklists can't cover."},
{"q": "AppLocker enforced without audit mode. Likely result?", "choices": ["Business breakage day one - legit apps blocked", "Perfect security", "Faster PCs", "Nothing"], "answer": 0, "index": 0, "explain": "Audit maps the real catalog first - non-negotiable."},
{"q": "Rule for an app that updates monthly. Best type?", "choices": ["Publisher (version-flexible)", "Hash", "Path to temp", "Deny all"], "answer": 0, "index": 0, "explain": "Publisher rules survive updates; hash rules break."},
{"q": "Server needs tamper-resistant enforcement. Choose?", "choices": ["WDAC (kernel-level)", "AppLocker", "Nothing", "Antivirus only"], "answer": 0, "index": 0, "explain": "Kernel enforcement resists admin bypass."},
{"q": "First allowlisting target in a hospital?", "choices": ["Fixed-function devices (kiosks, check-in)", "Surgeon laptops", "Everything at once", "The MRI"], "answer": 0, "index": 0, "explain": "Smallest catalog, clearest win, then expand."},
{"q": "User needs a new app under allowlisting. Process?", "choices": ["Governed request -> vetting -> rule deployment", "Local admin rights", "Disable the policy", "USB install"], "answer": 0, "index": 0, "explain": "The pipeline keeps default-deny intact."},
{"q": "Managed Installer / ISG helps by:", "choices": ["Auto-trusting apps from your management tools", "Blocking everything", "Faster downloads", "Free licenses"], "answer": 0, "index": 0, "explain": "Scales allow decisions via trusted deployment."},
{"q": "Allowlisting's Zero Trust connection:", "choices": ["Every execution is an access decision - verify per binary", "They're unrelated", "Zero Trust replaces it", "Only for networks"], "answer": 0, "index": 0, "explain": "Default-deny execution = Zero Trust at the endpoint."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M28"],
"drills": [
{"id": "m27-drill-allow", "title": "Allowlisting Drill",
"items": [
{"prompt": "Default-deny in one sentence", "answer": "Deny all code except explicitly approved", "explain": "The allowlisting model."},
{"prompt": "First rollout step", "answer": "Audit mode - map the real catalog", "explain": "Never enforce blind."},
{"prompt": "App updates monthly: rule type?", "answer": "Publisher", "explain": "Version-flexible."},
{"prompt": "Tamper-resistant servers", "answer": "WDAC", "explain": "Kernel-level."},
{"prompt": "Easiest first targets", "answer": "Fixed-function devices", "explain": "Smallest catalogs."},
{"prompt": "New app under allowlisting", "answer": "Governed request pipeline", "explain": "Vet, approve, deploy rule."}
]}
],
"handsOnLab": {
"id": "m27-lab",
"title": "Allowlist Lab: AppLocker audit to enforce",
"brief": "Run the full allowlisting rollout on lab machines.",
"steps": [
"Enable AppLocker audit mode on a lab client (default rules + audit).",
"Run normal lab workflows for a 'day'; collect the audit events.",
"Analyze: list every legit executable that would have been blocked.",
"Write publisher rules for the lab app set; enforce on a pilot OU.",
"Test: attempt to run an unapproved binary - verify the block + event.",
"Document the request pipeline: how a new app gets approved."
],
"deliverable": "Audit analysis + rule set + enforcement proof + request process doc.",
"checkpoint": "You can roll out default-deny without breaking the business."
},
"mockTask": {"id": "m27-mock", "type": "choice",
"q": "Interview: 'What is application allowlisting and how would you roll it out?'",
"choices": ["Default-deny for code: audit mode to map the catalog, publisher rules by device tier starting with fixed-function devices, pilot enforce, governed request pipeline - the endpoint enforcement of Zero Trust", "Block bad apps", "Antivirus", "Disable USB"],
"answer": 0, "explain": "Concept + rollout discipline + Zero Trust framing - the complete answer."},
"crossLinks": ["il11-allowlisting-ringfencing--allowlist-foundations", "il24-approve-deny-ringfence--m24-allowlist-ops"],
"videos": [],
"estimatedMinutes": 300,
"fastTrackEligible": True
}
]
