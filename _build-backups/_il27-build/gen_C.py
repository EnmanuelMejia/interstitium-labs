"""IL-27 Track C: Windows Server & Identity (IL27-M11..M17)."""

MODULES_C = [
{
"id": "IL27-M11",
"code": "IL-27",
"title": "Windows Server Install & Core Config",
"summary": "Install it right: editions, Server Core vs Desktop Experience, initial config, roles/features, and remote management. You need this for -> every server module and the homelab.",
"objectives": [
"Choose the right edition and install option (Core vs Desktop Experience) for a workload.",
"Perform initial config: hostname, IP, domain join, updates, remote management.",
"Add roles/features via Server Manager, PowerShell, and Windows Admin Center.",
"Manage servers remotely with RSAT, WAC, and PowerShell remoting.",
"Explain licensing basics (Standard vs Datacenter, CALs) at a conversational level."
],
"notes": [
{"title": "Editions and install options",
"body": "Editions: Standard (2 VMs + host, limited virtualization rights), Datacenter (unlimited VMs - for dense Hyper-V hosts), Essentials (small business, retired in 2022+). Azure Edition adds hotpatching. For the homelab, evaluation ISOs (180 days) are legitimate learning tools.\n\nInstall options: Desktop Experience (full GUI - familiar, larger attack surface, more patching) vs Server Core (no GUI, smaller footprint, the Microsoft-recommended default for infrastructure roles). Rule: if you RDP to click, you chose wrong - Core + Windows Admin Center + PowerShell is the professional pattern. Nano Server exists for containers only.\n\nPartitioning: separate OS (C:) from data; 100GB+ for OS on modern builds. Always install with the latest cumulative update slipstreamed if you have it - a 2019 ISO without updates means hours of patching before the server is even useful."
},
{"title": "Initial configuration checklist",
"body": "The 15-minute checklist, in order: (1) hostname (naming convention: LOC-ROLE-NN, e.g., ORL-DC-01), (2) static IP + DNS (servers never use DHCP - if the DHCP server is the thing that's down, you can't reach anything to fix it), (3) time zone + NTP (domain hierarchy or external), (4) Windows Update (patch before joining anything), (5) enable Remote Desktop + firewall rule, (6) join domain (or create it - M12), (7) activate.\n\nsconfig.cmd is the Core survival tool: numbered menu for all of the above. For fleet builds, answer files (unattend.xml) automate setup; even better, build a golden image or use IaC later (M23).\n\nPost-install hardening basics: rename Administrator, disable unneeded services, enable firewall (it is on by default - leave it), install only the roles needed. A server with every role installed 'just in case' is a vulnerability museum."
},
{"title": "Roles, features, and remote management",
"body": "Roles = the server's job (AD DS, DNS, DHCP, Hyper-V, File Server). Features = supporting pieces (.NET, Failover Clustering, RSAT tools). Add via Server Manager (GUI), Install-WindowsFeature (PowerShell - scriptable, the right way), or Windows Admin Center.\n\nRemote management trio: RSAT (admin tools on your workstation - manage servers without RDP), Windows Admin Center (browser-based, modern, free - the future), PowerShell remoting (Enter-PSSession, Invoke-Command - automation). WinRM must be enabled (winrm quickconfig / Enable-PSRemoting); in domains it's Kerberos-authenticated and safe on the LAN.\n\nLicensing conversationally: Server license per core (16-core minimum per server); Standard covers 2 VMs, Datacenter unlimited; CALs (user/device) for access - Essentials had none. You don't need to be a licensing lawyer, but 'we need Datacenter for the 12-VM host' should roll off the tongue."
}
],
"cards": [
{"front": "Standard vs Datacenter virtualization rights", "back": "Standard: 2 VMs. Datacenter: unlimited VMs."},
{"front": "Server Core vs Desktop Experience", "back": "Core: no GUI, smaller, recommended. Desktop: full GUI, larger surface."},
{"front": "Why never DHCP for servers?", "back": "If DHCP is down you can't reach anything to fix it; servers need stable addresses."},
{"front": "sconfig.cmd is for?", "back": "Menu-driven initial config on Server Core (hostname, IP, updates, domain)."},
{"front": "Install-WindowsFeature vs Server Manager", "back": "PowerShell = scriptable/repeatable; GUI = one-off."},
{"front": "Three remote management tools", "back": "RSAT, Windows Admin Center, PowerShell remoting."},
{"front": "Enable-PSRemoting does what?", "back": "Configures WinRM for PowerShell remoting."},
{"front": "Hostname convention example", "back": "LOC-ROLE-NN: ORL-DC-01 (location, role, number)."}
],
"quiz": [
{"q": "Host will run 12 VMs. Which edition?", "choices": ["Datacenter (unlimited VMs)", "Standard", "Essentials", "Foundation"], "answer": 0, "index": 0, "explain": "Standard covers 2; 12 VMs needs Datacenter."},
{"q": "Microsoft-recommended install option for infrastructure roles?", "choices": ["Server Core", "Desktop Experience", "Nano for everything", "It doesn't matter"], "answer": 0, "index": 0, "explain": "Smaller footprint, less patching, managed remotely."},
{"q": "A server can't be reached and its IP changed overnight. Root cause?", "choices": ["It was on DHCP - servers need static IPs", "DNS is slow", "The switch died", "IPv6"], "answer": 0, "index": 0, "explain": "DHCP lease change moved the server."},
{"q": "You need to manage 20 servers without RDPing to each. Best?", "choices": ["RSAT + Windows Admin Center + PowerShell remoting", "20 RDP sessions", "One shared admin login via RDP", "Email the servers"], "answer": 0, "index": 0, "explain": "Remote management trio - no interactive logons needed."},
{"q": "Install-WindowsFeature AD-Domain-Services does what?", "choices": ["Installs the AD DS role binaries (promotion is separate)", "Creates the domain", "Joins the domain", "Installs DNS only"], "answer": 0, "index": 0, "explain": "Install = binaries; promotion (Install-ADDSForest) creates the domain."},
{"q": "First 3 initial-config steps in order?", "choices": ["Hostname, static IP/DNS, updates", "Join domain, install apps, rename", "Activate, RDP, browse", "Patch, join, rename"], "answer": 0, "index": 0, "explain": "Identity, network, patch - then domain and roles."},
{"q": "CALs are:", "choices": ["Licenses for users/devices accessing the server", "CPU licenses", "Free with Windows", "Only for Linux"], "answer": 0, "index": 0, "explain": "Client Access Licenses cover access to server services."},
{"q": "A server has every role installed 'just in case'. Problem?", "choices": ["Unnecessary attack surface and patching burden", "It's faster", "Better redundancy", "No problem"], "answer": 0, "index": 0, "explain": "Least privilege applies to roles too."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M12", "IL27-M14", "IL27-M15", "IL27-M18"],
"drills": [
{"id": "m11-drill-setup", "title": "Server Setup Drill",
"items": [
{"prompt": "12-VM host: edition?", "answer": "Datacenter", "explain": "Unlimited VM rights."},
{"prompt": "2-VM branch server: edition?", "answer": "Standard", "explain": "Covers 2 VMs."},
{"prompt": "Install option for a DC?", "answer": "Server Core", "explain": "Recommended; manage remotely."},
{"prompt": "Server unreachable after DHCP lease expired", "answer": "Set static IP; reserve in DHCP", "explain": "Servers never on DHCP."},
{"prompt": "Add DNS role via PowerShell", "answer": "Install-WindowsFeature DNS -IncludeManagementTools", "explain": "Scriptable role install."},
{"prompt": "Remote into server for automation (not GUI)", "answer": "Enter-PSSession / Invoke-Command (WinRM)", "explain": "PowerShell remoting."}
]}
],
"handsOnLab": {
"id": "m11-lab",
"title": "Build Day: two servers, fully configured",
"brief": "Install and configure two Windows Server VMs (one Core, one GUI) to the checklist standard.",
"steps": [
"Install Server Core VM: run sconfig - set hostname LAB-DC-01, static IP, updates, RDP.",
"Install Desktop Experience VM: LAB-FS-01, same checklist via GUI.",
"From your workstation: install RSAT, connect to both; install Windows Admin Center and add both.",
"Enable-PSRemoting; run Invoke-Command against both to get OS version and uptime.",
"Install the File Server role on LAB-FS-01 via PowerShell; verify in WAC.",
"Document the full checklist as your golden build sheet."
],
"deliverable": "Two configured servers + build sheet + remote management verification.",
"checkpoint": "You can rack, configure, and remotely manage a Windows Server blindfolded (almost)."
},
"mockTask": {"id": "m11-mock", "type": "choice",
"q": "Interview: 'How do you set up a new Windows Server?'",
"choices": ["Right edition/option, hostname convention, static IP/DNS, patch, RDP+WinRM, join domain, minimal roles, manage via RSAT/WAC/remoting", "Next-next-finish with DHCP", "Install everything just in case", "GUI on everything"],
"answer": 0, "explain": "The checklist shows method, not just clicks."},
"crossLinks": ["il04-windows"],
"videos": "VIDEOS_M11",
"estimatedMinutes": 240,
"fastTrackEligible": True
},
{
"id": "IL27-M12",
"code": "IL-27",
"title": "Active Directory DS Design & Deployment",
"summary": "The identity plane: forests, domains, OUs, replication, FSMO, and deploying a domain controller properly. Interview-critical for any Windows infrastructure role. You need this for -> M13/M17 and everything identity.",
"objectives": [
"Design forest/domain/OU structure and defend the choices.",
"Promote a domain controller and verify replication and DNS.",
"Explain the 5 FSMO roles and what happens when each fails.",
"Manage users, groups (AGDLP), computers, and OUs with GUI and PowerShell.",
"Diagnose replication (repadmin), DNS, and time-sync issues."
],
"notes": [
{"title": "Forests, domains, OUs: the design",
"body": "Forest = security boundary (one org = one forest, almost always). Domain = replication/partition boundary inside the forest. Modern guidance: single-domain forest unless legal/regulatory forces separation - multi-domain forests multiply admin cost for little security gain (forest = the real boundary).\n\nOUs are the admin structure: design by function (Workstations, Servers, Users) or geography, never by org chart (reorgs shred org-chart OUs). Keep it shallow (3-4 levels) - deep OU trees make GPO troubleshooting miserable. Special identities: use groups for permissions (AGDLP), OUs for policy and delegation.\n\nSites and subnets: AD Sites map to physical locations; clients find the nearest DC via site-aware DNS SRV records. Wrong site topology = logons crossing the WAN. Always define subnets in Sites and Services - unassigned subnets land in the default site."
},
{"title": "Deploying and feeding a domain controller",
"body": "Promotion: Install-WindowsFeature AD-Domain-Services, then Install-ADDSForest (new forest) or Install-ADDSDomainController (replica). Prerequisites that must be right FIRST: static IP, DNS pointing to itself (for the first DC), a sensible NetBIOS/name (use ad.company.com or corp.company.com internally - never a name you don't own publicly... actually use a subdomain of your public domain), and time sync.\n\nPost-promotion verification: dcdiag (the whole battery), repadmin /replsummary (replication health), nslookup of SRV records, and confirm SYSVOL/NETLOGON shares exist. DNS is AD's oxygen - the DC must host AD-integrated DNS, and every member must point at AD DNS first.\n\nFSMO roles: Schema Master, Domain Naming Master (forest-level, on the forest root PDC), RID Master, PDC Emulator, Infrastructure Master (domain-level). PDC Emulator matters most day-to-day (password changes, time source, GPO). Seize (never transfer) roles from a dead DC with ntdsutil - seizing is for corpses, transferring for planned moves."
},
{"title": "Objects, groups, and daily operations",
"body": "Users/computers/groups live in OUs; manage with ADUC or PowerShell (New-ADUser, Get-ADUser -Filter, Add-ADGroupMember). Service accounts: prefer Group Managed Service Accounts (gMSA - automatic password management) over shared passwords in scripts. Stale computer objects: disable after 90 days inactive, delete after 180 (with a tombstone grace) - attackers love forgotten machines.\n\nAGDLP: Accounts in Global groups, Global in Domain Local, Domain Local on the ACL. In single-domain forests it simplifies to 'users in role groups, role groups on resources'. Group nesting audits (M-MX05 sets) keep token bloat down.\n\nReplication triage: repadmin /showrepl (partner status), /replsummary (error overview), dcdiag /test:replications. Lingering objects from restores past tombstone lifetime = the classic replication poison; never restore a DC from a snapshot older than the tombstone lifetime (180 days default). Time: PDC Emulator syncs externally, everyone syncs down the hierarchy - 5-minute Kerberos skew tolerance is the tripwire."
}
],
"cards": [
{"front": "Forest vs domain vs OU", "back": "Forest: security boundary. Domain: replication boundary. OU: admin/policy structure."},
{"front": "Modern domain design guidance", "back": "Single-domain forest unless legal/regulatory forces more."},
{"front": "The 5 FSMO roles", "back": "Schema, Domain Naming (forest); RID, PDC Emulator, Infrastructure (domain)."},
{"front": "Most operationally critical FSMO", "back": "PDC Emulator: passwords, time, GPO."},
{"front": "Seize vs transfer FSMO", "back": "Transfer: planned. Seize: holder is dead (ntdsutil)."},
{"front": "AGDLP expansion", "back": "Accounts -> Global -> Domain Local -> Permissions."},
{"front": "Preferred service account type", "back": "gMSA - automatic password management."},
{"front": "Replication health commands", "back": "repadmin /replsummary, repadmin /showrepl, dcdiag."}
],
"quiz": [
{"q": "Two companies merge; both keep IT separate for legal reasons. AD design?", "choices": ["Separate forests with a trust", "One domain", "One forest, two domains", "Workgroups"], "answer": 0, "index": 0, "explain": "Forest = security boundary; legal separation needs forests."},
{"q": "First DC promotion prerequisite that breaks everything if wrong?", "choices": ["DNS (DC must point to itself / AD DNS)", "Wallpaper", "Hostname length", "Monitor resolution"], "answer": 0, "index": 0, "explain": "AD is DNS-dependent; wrong DNS = failed promotion and broken SRV."},
{"q": "PDC Emulator goes offline. Immediate impact?", "choices": ["Password changes and time sync degrade", "Nothing ever", "Forest deleted", "DHCP stops"], "answer": 0, "index": 0, "explain": "PDC handles password forwarding, time hierarchy, GPO."},
{"q": "Users in a branch log on across the WAN slowly. Check?", "choices": ["AD Sites: subnets defined and mapped to the branch site", "More RAM", "The firewall", "Printer drivers"], "answer": 0, "index": 0, "explain": "Missing site mapping = clients pick any DC, often far away."},
{"q": "repadmin /replsummary shows errors on one DC for days. You:", "choices": ["Investigate that DC: dcdiag, event logs, network, time - replication errors compound", "Ignore it", "Delete the DC", "Reboot everything"], "answer": 0, "index": 0, "explain": "Replication failures age into lingering objects; fix early."},
{"q": "Stale computer objects (1 year inactive) are risky because:", "choices": ["Attackers use forgotten machines; clean: disable at 90d, delete at 180d", "They use disk space", "They slow logon", "They expire passwords"], "answer": 0, "index": 0, "explain": "Dormant accounts are attacker footholds."},
{"q": "gMSA beats a shared service account password because:", "choices": ["Automatic password management, no password in scripts", "It's faster", "It's free", "It never expires"], "answer": 0, "index": 0, "explain": "No human-known password to leak or forget."},
{"q": "Restoring a DC from a 200-day-old snapshot risks:", "choices": ["Lingering objects past tombstone lifetime poisoning replication", "Nothing", "Faster logons", "Free disk space"], "answer": 0, "index": 0, "explain": "180-day tombstone lifetime; older restores reintroduce dead objects."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M13", "IL27-M17", "IL27-M26"],
"drills": [
{"id": "m12-drill-ad", "title": "AD Operations Drill",
"items": [
{"prompt": "New forest: first 3 promotion prereqs", "answer": "Static IP, DNS to self, sensible name + time sync", "explain": "Foundation before promotion."},
{"prompt": "Verify a new DC", "answer": "dcdiag, repadmin /replsummary, SRV lookup, SYSVOL share", "explain": "Full verification battery."},
{"prompt": "Password changes failing site-wide", "answer": "Check PDC Emulator health", "explain": "PDC owns password forwarding."},
{"prompt": "Add 50 users from CSV", "answer": "Import-Csv | New-ADUser", "explain": "Bulk ops in PowerShell."},
{"prompt": "Find inactive computers >90 days", "answer": "Search-ADAccount -ComputersOnly -Inactive -TimeSpan 90", "explain": "Stale-object hygiene."},
{"prompt": "DC hardware died; need its FSMO roles", "answer": "Seize with ntdsutil on a healthy DC", "explain": "Seize = holder is dead."}
]}
],
"handsOnLab": {
"id": "m12-lab",
"title": "Forest Build: two DCs, OUs, replication",
"brief": "Build a real AD forest with two DCs, proper OU design, and verified replication.",
"steps": [
"Promote LAB-DC-01 as a new forest (corp.lab.local or similar); verify with dcdiag.",
"Promote LAB-DC-02 as a replica; verify replication with repadmin /replsummary.",
"Design OUs: Workstations, Servers, Users, ServiceAccounts (3 levels max); document the rationale.",
"Create role groups (G_Laptop_Users etc.), nest per AGDLP, bulk-import 20 users from CSV.",
"Define AD Sites/subnets for your lab network; verify client site assignment (nltest /dsgetsite).",
"Seize-test in a snapshot: transfer FSMO roles to DC-02, verify, transfer back; document."
],
"deliverable": "Two-DC forest + OU design doc + replication verification + FSMO transfer log.",
"checkpoint": "You can design, deploy, and verify AD - and explain every design choice."
},
"mockTask": {"id": "m12-mock", "type": "choice",
"q": "Interview: 'How would you design AD for a 500-person single-site company?'",
"choices": ["Single-domain forest, functional OUs (Workstations/Servers/Users), AD Sites defined, 2+ DCs, gMSAs, documented FSMO placement", "Five domains for five departments", "One forest per department", "No AD - workgroups"],
"answer": 0, "explain": "Modern best practice: simple, resilient, documented."},
"crossLinks": ["il11-active-directory-defense--zt-ad-structure", "il11-active-directory-defense--zt-ad-harden"],
"videos": [],
"estimatedMinutes": 330,
"fastTrackEligible": True
},
{
"id": "IL27-M13",
"code": "IL-27",
"title": "Group Policy Mastery",
"summary": "The most powerful and most misunderstood Windows tool: GPO lifecycle, precedence, filtering, troubleshooting, and security baselines. Interview-critical. You need this for -> M24/M26/M27 and fleet control.",
"objectives": [
"Create, link, and scope GPOs with security filtering and WMI filters.",
"Predict application with LSDOU precedence, enforcement, and block inheritance.",
"Troubleshoot with gpresult, event logs, and RSOP.",
"Design GPO structure: few, well-named, documented policies.",
"Apply security baselines and back up/restore GPOs."
],
"notes": [
{"title": "Lifecycle and precedence",
"body": "GPO = Group Policy Object: a collection of settings stored in AD (GPC) + SYSVOL (GPT). Lifecycle: create (GPMC) -> configure -> link to Site/Domain/OU -> scope (security filtering/WMI) -> test on pilot OU -> deploy -> monitor -> document -> eventually retire.\n\nPrecedence LSDOU: Local, Site, Domain, OU (child OUs win over parents). Conflicts: last-applied wins = closest OU to the object. Enforced (was 'No Override') beats Block Inheritance; Block Inheritance stops parent policies unless Enforced. Loopback processing (on terminal servers/RDS): user settings follow the COMPUTER's OU - essential for kiosk/RDS scenarios.\n\nComputer vs User halves: computer settings apply at startup (needs reboot), user at logon. 'Why didn't my policy apply?' - did you gpupdate /force? Did the machine reboot (computer policy)? Is it the right half? These three answer half of all GPO tickets."
},
{"title": "Scoping: security filtering and WMI",
"body": "Security filtering: GPO applies only to principals with Read + Apply Group Policy. Default: Authenticated Users (computers + users). Scope to a group (GG_Sales_Laptops) to target precisely. Deny Apply on an exception group carves exclusions (M-MX05 set difference).\n\nWMI filters: WQL queries evaluated on the target (SELECT * FROM Win32_OperatingSystem WHERE Version LIKE '10.%'). Powerful, but each WMI evaluation costs logon time - keep them simple and few. One slow WMI filter on a domain-linked GPO = slow logons fleet-wide.\n\nDesign rules: few GPOs, single purpose each, named by intent (SEC-BitLocker-Laptops, CFG-Power-Workstations), one setting area per GPO where possible. 'Monster GPO with 200 settings' is undebuggable - split it. Document each GPO's purpose, scope, and owner in its comment field."
},
{"title": "Troubleshooting and baselines",
"body": "Troubleshooting order: (1) gpresult /r (or /h report.html) on the target - shows applied + denied GPOs with reasons; (2) Event Viewer: GroupPolicy operational log (event IDs 5312/7016 patterns); (3) replication: is SYSVOL healthy? (dfsrdiag); (4) scope check: security filtering, WMI result, link enabled, block inheritance.\n\nCommon gotchas: GPO linked but not to the right OU; computer policy needing reboot; WMI filter false; 'Authenticated Users' removed from delegation (the infamous MS16-072 gotcha - GPOs need Read for computer accounts); slow link detection skipping policies.\n\nSecurity baselines: Microsoft publishes baselines (now via Security Compliance Toolkit) - import, compare, customize, deploy. CIS Benchmarks are the industry alternative. Baseline + monitor drift = the hardening loop. Back up GPOs (GPMC backup) before every change; version in git if you're fancy. A GPO change without a backup is a resume-generating event."
}
],
"cards": [
{"front": "LSDOU order and winner", "back": "Local, Site, Domain, OU - closest OU to the object wins conflicts."},
{"front": "Enforced vs Block Inheritance", "back": "Enforced beats Block Inheritance; Block stops parents unless Enforced."},
{"front": "Loopback processing is for?", "back": "RDS/kiosk: user settings follow the computer's OU."},
{"front": "Computer policy needs what to apply?", "back": "Reboot (applies at startup); user policy needs logon."},
{"front": "First troubleshooting command", "back": "gpresult /r (or /h) on the target."},
{"front": "MS16-072 gotcha", "back": "Computer accounts need Read on the GPO or policies don't apply."},
{"front": "WMI filter cost", "back": "Evaluated per target at policy time - slow filters = slow logons fleet-wide."},
{"front": "GPO naming convention", "back": "Intent-based: SEC-BitLocker-Laptops; one purpose per GPO."}
],
"quiz": [
{"q": "Two GPOs set different wallpapers, one linked to domain, one to the user's OU. Which wins?", "choices": ["The OU-linked one (closer to the object)", "The domain one", "Neither", "Random"], "answer": 0, "index": 0, "explain": "LSDOU: later/closer wins."},
{"q": "Parent OU policy blocked by Block Inheritance, but the GPO is Enforced. Result?", "choices": ["Applies anyway - Enforced wins", "Blocked", "Applies to admins only", "Error"], "answer": 0, "index": 0, "explain": "Enforced overrides Block Inheritance."},
{"q": "User policy not applying; gpresult shows it denied. First check?", "choices": ["Security filtering / delegation (Read + Apply)", "Reinstall Windows", "The user's password", "Disk space"], "answer": 0, "index": 0, "explain": "Denied usually = scope/filter, not corruption."},
{"q": "Computer configuration policy deployed at 9 AM; users complain at 9:05 it's not applied. You:", "choices": ["Computer policy needs reboot (or wait for background refresh)", "It's broken", "Run gpupdate on the DC", "Recreate the GPO"], "answer": 0, "index": 0, "explain": "Startup policies need a reboot; background refresh is ~90 min."},
{"q": "RDS server needs locked-down user settings regardless of who logs on. Use:", "choices": ["Loopback processing (merge/replace) on the RDS OU", "A logon script", "Local policy only", "Block Inheritance"], "answer": 0, "index": 0, "explain": "Loopback makes user settings follow the computer."},
{"q": "Fleet logons suddenly slow after a GPO change. Suspect?", "choices": ["New WMI filter evaluating slowly on every logon", "The network", "Antivirus", "The moon"], "answer": 0, "index": 0, "explain": "WMI filters run per-target; slow WQL = slow logons."},
{"q": "Before editing any production GPO you:", "choices": ["Back it up (GPMC backup)", "Edit live", "Delete it first", "Email users"], "answer": 0, "index": 0, "explain": "Backup = instant rollback."},
{"q": "Security baselines come from:", "choices": ["Microsoft Security Compliance Toolkit / CIS Benchmarks", "Reddit", "Your imagination", "The event log"], "answer": 0, "index": 0, "explain": "Published, versioned, auditable starting points."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M24", "IL27-M26", "IL27-M27"],
"drills": [
{"id": "m13-drill-gpo", "title": "GPO Troubleshooting Drill",
"items": [
{"prompt": "Policy not applying: first command?", "answer": "gpresult /r on the target", "explain": "Shows applied/denied with reasons."},
{"prompt": "Computer settings not applying after gpupdate", "answer": "Reboot - computer policy applies at startup", "explain": "gpupdate alone doesn't reboot."},
{"prompt": "GPO denied: check?", "answer": "Security filtering: Read + Apply for the object", "explain": "Scope is the usual culprit."},
{"prompt": "Slow logons after new WMI filter", "answer": "Simplify/remove the filter; WMI costs per logon", "explain": "WQL evaluation is expensive fleet-wide."},
{"prompt": "Need user settings to follow RDS server", "answer": "Loopback processing on the RDS OU", "explain": "User half from computer's OU."},
{"prompt": "Undo a bad GPO change fast", "answer": "Restore from GPMC backup", "explain": "This is why you back up first."}
]}
],
"handsOnLab": {
"id": "m13-lab",
"title": "Policy Build: secure baseline via GPO",
"brief": "Build, scope, troubleshoot, and back up a mini security baseline in your lab forest.",
"steps": [
"Create GPOs: SEC-BitLocker-Workstations, CFG-Power-Workstations, SEC-LocalAdmin-LAPS; link to the Workstations OU.",
"Scope SEC-BitLocker to GG_Laptops only (security filtering); add WMI filter for Windows 11.",
"Create an exception: deny Apply for GG_NoBitLocker; verify with gpresult on a member vs non-member.",
"Break it: remove Authenticated Users from delegation; observe failure; fix (the MS16-072 lesson).",
"Back up all GPOs; document each: purpose, scope, owner.",
"Produce an HTML gpresult report for a lab client showing the applied set."
],
"deliverable": "Three scoped GPOs + break/fix note + backups + gpresult report + documentation.",
"checkpoint": "You can design, scope, troubleshoot, and safely change Group Policy."
},
"mockTask": {"id": "m13-mock", "type": "choice",
"q": "Interview: 'A GPO isn't applying to some machines. How do you troubleshoot?'",
"choices": ["gpresult on target, check link/scope/filtering/WMI, event logs, SYSVOL replication - in that order", "Delete and recreate the GPO", "Reboot the DC", "It's always DNS"],
"answer": 0, "index": 0, "explain": "Structured: result, scope, logs, replication."},
"crossLinks": ["il11-active-directory-defense--zt-ad-harden"],
"videos": [],
"estimatedMinutes": 330,
"fastTrackEligible": True
},
{
"id": "IL27-M14",
"code": "IL-27",
"title": "DNS & DHCP on Windows Server",
"summary": "Running both services on Windows: AD-integrated zones, scavenging, DHCP failover, and the option set that makes PXE/imaging work. You need this for -> M12/M23 and production Windows networks.",
"objectives": [
"Deploy AD-integrated DNS zones and explain their replication advantage.",
"Configure forwarders, conditional forwarders, and root hints appropriately.",
"Enable DNS scavenging safely (the 7-day rule) to clean stale records.",
"Build DHCP scopes with reservations, exclusions, options, and failover.",
"Set the PXE options (066/067) and IP helpers that imaging depends on."
],
"notes": [
{"title": "Windows DNS: zones and resolution design",
"body": "AD-integrated zones store records in AD and replicate with AD - no separate zone transfers, secure dynamic updates, multi-master. Standard primary/secondary still exists for non-AD or BIND interop. Forward lookup zones (name->IP) everyone knows; reverse zones (PTR) matter for mail, logging, and security tools - build them.\n\nResolution design: internal clients use AD DNS; the DNS server uses forwarders (ISP/1.1.1.1) or root hints for the internet. Conditional forwarders per partner domain. Never point AD members at external DNS first - the M06 lesson, enforced here.\n\nAging/scavenging: dynamic records go stale (laptops, DHCP churn). Enable scavenging with no-refresh + refresh intervals (7+7 days typical) - but ONLY after verifying no static records will be eaten. Scavenging without understanding deletes production records; scavenging done right keeps the zone truthful."
},
{"title": "Windows DHCP: scopes, options, failover",
"body": "Scope = pool + options + lease duration. Best practices: 80/20 or 50/50 split was the old way; now use DHCP failover (hot standby or load balance) between two servers - no more split-scope math. Exclusions for statics/printers; reservations for MAC-pinned devices.\n\nOptions that run the network: 003 router, 006 DNS, 015 domain name, 042 NTP, 066/067 boot server/filename (PXE/WDS - imaging lives here), 150 (VoIP). Server options vs scope options vs class options - scope wins over server for that scope.\n\nSuperscopes group multiple scopes on one interface (multinetting - rare now); multicast scopes for MADCAP (rarer). Policy-based assignment (by vendor class, MAC prefix) can auto-segregate phones/printers - neat when you inherit chaos."
},
{"title": "The DNS+DHCP integration points",
"body": "Dynamic DNS updates: DHCP can register client records on behalf of clients (protects against clients failing to update, and secures the updates via the DHCP server's credentials). DNSUpdateProxy group exists for exactly this - DHCP servers in it can update records owned by others. Misconfigured, you get duplicate/stale records; configured right, DNS stays truthful automatically.\n\nPXE boot chain: client DHCP discover -> server offers IP + options 066 (TFTP server) + 067 (boot file) -> client TFTP-downloads boot image. IP helpers (DHCP relay) on routers forward broadcasts to the DHCP server across subnets - without helpers, only the local subnet gets leases. WDS/MDT/SCCM imaging (M23) stands on these three: scope, options, helpers.\n\nMonitoring: DHCP scope utilization alerts at 80%; DNS query failure spikes (event log + analytical logs); scavenging logs. A scope hitting 95% on a Monday morning is a ticket you should have gotten as an alert on Friday."
}
],
"cards": [
{"front": "AD-integrated zone advantage", "back": "Replicates with AD, secure dynamic updates, multi-master - no zone transfers."},
{"front": "Scavenging intervals (typical)", "back": "No-refresh 7d + refresh 7d; enable only after protecting statics."},
{"front": "Modern DHCP redundancy", "back": "DHCP failover (hot standby/load balance) - not split scopes."},
{"front": "PXE options", "back": "066 boot server, 067 boot filename."},
{"front": "IP helper purpose", "back": "DHCP relay: forwards broadcasts across subnets to the DHCP server."},
{"front": "DNSUpdateProxy group", "back": "Lets DHCP servers update DNS records owned by others."},
{"front": "Scope alert threshold", "back": "80% utilization = warning; investigate before exhaustion."},
{"front": "Reverse zones matter for", "back": "Mail, logging, security tools - PTR lookups."}
],
"quiz": [
{"q": "Why AD-integrated zones over standard primary?", "choices": ["AD replication, secure updates, multi-master", "They're faster", "BIND requires it", "No reason"], "answer": 0, "index": 0, "explain": "Zone data rides AD replication securely."},
{"q": "Scavenging deleted static server records. Cause?", "choices": ["Aging enabled without protecting statics", "Too many forwarders", "IPv6", "DHCP"], "answer": 0, "index": 0, "explain": "Scavenging eats anything with a timestamp unless protected."},
{"q": "Two DHCP servers, no split-scope math. Use:", "choices": ["DHCP failover relationship", "Two independent scopes", "One server", "Static IPs"], "answer": 0, "index": 0, "explain": "Failover syncs leases properly."},
{"q": "PXE boot fails; client gets IP but no boot file. Check?", "choices": ["Options 066/067 on the scope", "DNS", "The client's OS", "NTP"], "answer": 0, "index": 0, "explain": "IP without boot options = DHCP ok, PXE config missing."},
{"q": "Only the local subnet gets DHCP leases. Missing?", "choices": ["IP helper-address on the router for other subnets", "More scopes", "Faster server", "DNS"], "answer": 0, "index": 0, "explain": "Broadcasts don't cross routers without a relay."},
{"q": "Duplicate DNS records for one hostname. Likely?", "choices": ["Stale records + scavenging off, or DHCP updating without proxy config", "Too many DCs", "IPv6", "Firewall"], "answer": 0, "index": 0, "explain": "Dynamic update conflicts without proper ownership."},
{"q": "Conditional forwarders are for:", "choices": ["Sending queries for specific domains to specific servers", "Blocking websites", "Faster internet", "DHCP"], "answer": 0, "index": 0, "explain": "Per-domain resolution paths (partner AD, etc.)."},
{"q": "Scope at 95% Monday 9 AM. You should have:", "choices": ["Gotten an alert at 80% on Friday", "Done nothing", "Rebooted", "Added DNS"], "answer": 0, "index": 0, "explain": "Proactive alerting beats reactive tickets."}
],
"weight": 2,
"prerequisiteFor": [],
"drills": [
{"id": "m14-drill-services", "title": "DNS/DHCP Server Drill",
"items": [
{"prompt": "Zone type for AD replication", "answer": "AD-integrated", "explain": "Rides AD replication."},
{"prompt": "PXE needs which options?", "answer": "066 + 067", "explain": "Boot server + filename."},
{"prompt": "Cross-subnet DHCP failing", "answer": "IP helper on router", "explain": "Relay broadcasts."},
{"prompt": "Stale DNS records everywhere", "answer": "Enable scavenging (7+7) after protecting statics", "explain": "Clean the zone safely."},
{"prompt": "Redundant DHCP, modern way", "answer": "Failover relationship", "explain": "Not split scopes."},
{"prompt": "Partner domain resolution", "answer": "Conditional forwarder", "explain": "Per-domain path."}
]}
],
"handsOnLab": {
"id": "m14-lab",
"title": "Services Build: AD DNS + DHCP failover + PXE-ready",
"brief": "Deploy production-pattern DNS and DHCP on your lab DCs.",
"steps": [
"Verify AD-integrated forward/reverse zones on LAB-DC-01; add records and confirm replication to DC-02.",
"Configure forwarders + a conditional forwarder for a fake partner domain.",
"Enable scavenging with 7+7 day intervals; document protected statics.",
"Build a DHCP scope with exclusions, 2 reservations, options 003/006/015/066/067.",
"Configure DHCP failover (hot standby) between DC-01 and DC-02; test by stopping one service.",
"Verify a client PXE-boots to the boot menu (or gets options in a capture)."
],
"deliverable": "DNS/DHCP config docs + failover test log + PXE verification.",
"checkpoint": "You can deploy and harden both services in production patterns."
},
"mockTask": {"id": "m14-mock", "type": "choice",
"q": "Interview: 'How do you make DHCP highly available?'",
"choices": ["DHCP failover relationship between two servers (hot standby or load balance)", "Two independent scopes", "One big server", "Static IPs for all"],
"answer": 0, "explain": "Failover syncs lease state; split scopes are legacy."},
"crossLinks": ["il04-networking"],
"videos": [],
"estimatedMinutes": 260,
"fastTrackEligible": False
},
{
"id": "IL27-M15",
"code": "IL-27",
"title": "File, Print & Patching Services",
"summary": "The daily bread: SMB shares with proper NTFS+share permissions, print management, and WSUS. You need this for -> file server administration and update infrastructure.",
"objectives": [
"Design share + NTFS permission combinations correctly (most restrictive wins).",
"Deploy shared printers via GPO and manage the print server.",
"Build WSUS: products, classifications, groups, approvals, deadlines.",
"Explain the update pipeline: sync, approve, deadline, reporting.",
"Troubleshoot access-denied and update-failure tickets."
],
"notes": [
{"title": "File shares: the two permission layers",
"body": "Share permissions (who can connect) + NTFS permissions (what they can do) - the EFFECTIVE permission is the MOST RESTRICTIVE of both. Modern practice: share = Authenticated Users Full (or Everyone Read/Change), control everything with NTFS. Fighting both layers is how 'access denied' mysteries are born.\n\nNTFS design: role groups on folders (AGDLP), never individual users; disable inheritance only where needed (break + copy, then prune); audit with Effective Access tab. DFS Namespaces: one UNC path (\\\\company\\shared) abstracting multiple servers - server moves without breaking drive mappings. DFS Replication syncs between sites (mind conflict handling).\n\nQuotas (FSRM): soft warnings then hard caps; file screens block executables/ransomware extensions in shares (an allowlisting cousin). Shadow Copies: previous versions = user self-service restore for 'I deleted the file' - enable on file servers, it's the cheapest backup."
},
{"title": "Print services without the pain",
"body": "Print server role: central drivers, queues, and permissions. Deploy via GPO (Computer or User -> Preferences -> Printers) - no more manual 'add printer' tickets. Type 4 (v4) drivers preferred; the PrintNightmare era taught us: keep print spoolers patched, restrict driver installation (Point and Print restrictions), and consider Universal Print (cloud) for the future.\n\nQueue management: pause/purge stuck jobs, set priorities (executive queue jumps the line), separators optional. 'Printer offline' triage: can the server ping it? (network) -> can you open its web page? (device) -> restart spooler on server -> check driver. Document IP, model, driver version, location per printer - the 2 AM page goes better with a map."
},
{"title": "WSUS: the update pipeline",
"body": "WSUS: Microsoft's free on-prem update server. Pipeline: synchronize (pull metadata from Microsoft on a schedule) -> classify (products: Windows 11, Office; classifications: security, critical) -> computer groups (pilot/broad/critical rings mirror WUfB) -> approve (per group) -> deadline (forced install time) -> reporting (who's missing what).\n\nClient config via GPO: intranet update location (http://wsus:8530), group membership, detection frequency. Client triage: wuauclt /detectnow (legacy) / usoclient startscan (modern), check %windir%\\WindowsUpdate.log (now via Get-WindowsUpdateLog PowerShell), verify GPO applied.\n\nThe human process matters more than the tool: monthly cadence (test pilot day 1-3, broad day 7, deadline day 14), emergency out-of-band process for zero-days, and a rollback story (uninstall update / known-issue rollback). WSUS vs Intune vs Autopatch is a strategy choice; the ring discipline is universal."
}
],
"cards": [
{"front": "Effective permission rule", "back": "Most restrictive of share + NTFS wins."},
{"front": "Modern share permission practice", "back": "Share wide open-ish; enforce with NTFS."},
{"front": "DFS Namespace value", "back": "One UNC path abstracting servers - moves without breaking mappings."},
{"front": "Deploy printers at scale", "back": "GPO Preferences -> Printers; central drivers on print server."},
{"front": "WSUS pipeline order", "back": "Sync -> classify -> groups -> approve -> deadline -> report."},
{"front": "WSUS client GPO essentials", "back": "Intranet update location, target group, detection frequency."},
{"front": "File screens (FSRM) stop what?", "back": "Blocked file types (executables, ransomware extensions) landing in shares."},
{"front": "Shadow Copies give you", "back": "Previous Versions - user self-service file restore."}
],
"quiz": [
{"q": "Share=Read, NTFS=Full. Effective?", "choices": ["Read (most restrictive wins)", "Full", "Write", "Deny"], "answer": 0, "index": 0, "explain": "Intersection of both layers."},
{"q": "User gets 'access denied' to a share they need. Check order?", "choices": ["Group membership -> share perms -> NTFS perms -> Effective Access tab", "Reboot", "Reinstall", "Give Domain Admin"], "answer": 0, "index": 0, "explain": "Membership first, then both layers, then verify."},
{"q": "Moving a file server. How to avoid breaking 200 drive mappings?", "choices": ["DFS Namespace - repoint the folder target", "Email everyone", "Keep the old server forever", "Robocopy at midnight"], "answer": 0, "index": 0, "explain": "Namespace abstraction decouples path from server."},
{"q": "50 printers need deploying. You:", "choices": ["GPO Preferences push with central drivers", "Visit 50 desks", "Email instructions", "One shared USB printer"], "answer": 0, "index": 0, "explain": "Policy-based deployment scales."},
{"q": "WSUS shows 0 updates needed but clients are unpatched. Check?", "choices": ["Sync status, product/classification selection, client GPO targeting", "The internet", "Reinstall WSUS", "More RAM"], "answer": 0, "index": 0, "explain": "Pipeline: sync -> classify -> target - find the broken stage."},
{"q": "Zero-day drops Tuesday. Your process?", "choices": ["Out-of-band: pilot immediately, broad within 24h, emergency deadline", "Wait for monthly cadence", "Ignore it", "Email users to be careful"], "answer": 0, "index": 0, "explain": "Emergency lane exists for zero-days."},
{"q": "File screen best use?", "choices": ["Block executables/malware extensions in user shares", "Speed up disk", "Compress files", "Encrypt shares"], "answer": 0, "index": 0, "explain": "Type-based blocking at the share layer."},
{"q": "'I deleted the quarterly report!' First response?", "choices": ["Check Previous Versions (Shadow Copies) on the share", "Restore from tape", "It's gone", "Blame the user"], "answer": 0, "index": 0, "explain": "Cheapest restore path first."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M24"],
"drills": [
{"id": "m15-drill-files", "title": "File & Update Drill",
"items": [
{"prompt": "Access denied: permission check order", "answer": "Groups -> share -> NTFS -> Effective Access", "explain": "Layered verification."},
{"prompt": "Deploy 30 printers", "answer": "Print server + GPO Preferences", "explain": "Central drivers, policy push."},
{"prompt": "WSUS client not reporting", "answer": "GPO applied? usoclient startscan; check WU log", "explain": "Targeting then client health."},
{"prompt": "Ransomware extension in shares", "answer": "FSRM file screen + isolate + restore", "explain": "Block type, contain, recover."},
{"prompt": "Server move without breaking mappings", "answer": "DFS Namespace retarget", "explain": "Abstract the path."},
{"prompt": "Monthly patch cadence", "answer": "Pilot 1-3d, broad 7d, deadline 14d", "explain": "Ring discipline."}
]}
],
"handsOnLab": {
"id": "m15-lab",
"title": "Services Build: file server + WSUS mini",
"brief": "Deploy a file server with proper permissions and a WSUS pipeline in the lab.",
"steps": [
"On LAB-FS-01: create shares (Departments, Projects) with role groups; set NTFS per AGDLP; verify Effective Access.",
"Create a DFS Namespace \\\\lab\\shared pointing at the shares; test failover by retargeting.",
"Enable Shadow Copies; test Previous Versions restore of a deleted file.",
"Install WSUS (or simulate with WUfB policies): define pilot/broad groups, approve a test update, set a deadline.",
"Deploy a shared printer via GPO to a lab client; verify auto-install at logon.",
"Document the permission matrix and the update cadence."
],
"deliverable": "Permission matrix + DFS test + WSUS cadence doc + printer GPO verification.",
"checkpoint": "You can run file/print/update services the enterprise way."
},
"mockTask": {"id": "m15-mock", "type": "choice",
"q": "Interview: 'A user can't access a shared folder. Walk me through it.'",
"choices": ["Verify group membership, check share then NTFS permissions, confirm with Effective Access, fix the missing grant", "Give them Full Control of everything", "Recreate their account", "It's always the firewall"],
"answer": 0, "explain": "Layered permission diagnosis, least privilege preserved."},
"crossLinks": ["il04-windows"],
"videos": [],
"estimatedMinutes": 240,
"fastTrackEligible": False
},
{
"id": "IL27-M16",
"code": "IL-27",
"title": "PowerShell 7 for Infrastructure Admins",
"summary": "From one-liners to fleet automation: the pipeline, remoting, modules, and scripts you'd actually run. Interview-critical - 'show me PowerShell' is a live skill test. You need this for -> M13/M24/M34 and everything at scale.",
"objectives": [
"Use the pipeline (Get | Where | Select | Sort | Export) fluently on real admin tasks.",
"Write functions with parameters, help, and error handling.",
"Run fleet commands with Invoke-Command and PSSessions.",
"Manage modules (PSGallery) and execution policy correctly.",
"Automate a full admin workflow: audit, report, remediate."
],
"notes": [
{"title": "The pipeline: objects, not text",
"body": "PowerShell passes OBJECTS, not text. Get-Service returns ServiceController objects with .Status, .Name properties - no parsing. The holy verbs: Get (read), Where-Object (filter - filter LEFT, early), Select-Object (shape), Sort-Object, Measure-Object, Export-Csv, ConvertTo-Json.\n\nThe admin one-liner pattern: Get-ADComputer -Filter * -Properties LastLogonDate | Where LastLogonDate -lt (Get-Date).AddDays(-90) | Select Name, LastLogonDate | Export-Csv stale.csv. Discovery trio for any cmdlet: Get-Command *service*, Get-Help Start-Service -Full, Get-Member (pipe anything to it to see properties).\n\nPowerShell 7 vs 5.1: 7 is cross-platform, faster, parallel foreach (-Parallel), ternary operators, better errors. Windows PowerShell 5.1 remains for old modules (some AD/Exchange bits). Install 7 side-by-side; default your scripts to 7 with #requires -Version 7."
},
{"title": "Remoting: one command, a thousand machines",
"body": "Enable-PSRemoting once per machine (GPO can push it). Enter-PSSession for interactive; Invoke-Command -ComputerName (or -Session) -ScriptBlock for fleet. Fan-out: Invoke-Command runs in parallel across targets - 500 machines queried in the time of the slowest one.\n\nPatterns: $s = New-PSSession -ComputerName (Get-Content servers.txt); Invoke-Command -Session $s { Get-HotFix | Sort InstalledOn -Descending | Select -First 1 } | Export-Csv patchstatus.csv. Credentials: Get-Credential once, reuse; never hardcode passwords (use secret management / vaults). Double-hop (remote session accessing a third machine) needs CredSSP or Kerberos delegation - know the term when it bites.\n\nJEA (Just Enough Administration): constrained endpoints giving juniors exactly the cmdlets they need, nothing more - least privilege for admin access itself."
},
{"title": "Scripts that survive production",
"body": "Anatomy: #requires, [CmdletBinding()] + param() with types and validation, begin/process/end, try/catch with -ErrorAction Stop for terminating errors, Write-Verbose (not Write-Host) for progress, and comment-based help (synopsis, example). Non-zero exit codes and transcript logging (Start-Transcript) for scheduled tasks.\n\nExecution policy is NOT a security boundary (it's a seatbelt): RemoteSigned for workstations, and sign your production scripts (or deploy via trusted automation). Modules: Install-Module from PSGallery (check the publisher!), RequiredModules in the manifest.\n\nThe workflow capstone: audit (collect state from fleet) -> report (HTML/CSV to a share or email) -> remediate (fix drift, with -WhatIf first). Example: audit BitLocker status fleet-wide, report unencrypted laptops, remediate by triggering encryption - the exact loop behind compliance dashboards."
}
],
"cards": [
{"front": "PowerShell passes what through the pipeline?", "back": "Objects with properties - not text."},
{"front": "Filter-left principle", "back": "Filter as early as possible (at Get-, not after) to reduce work."},
{"front": "Fleet query pattern", "back": "Invoke-Command -ComputerName (list) -ScriptBlock { ... } - runs in parallel."},
{"front": "PowerShell 7 advantages", "back": "Cross-platform, faster, -Parallel foreach, ternary, better errors."},
{"front": "Double-hop problem", "back": "Remote session can't auth to a third machine; fix with CredSSP/Kerberos delegation."},
{"front": "Execution policy is...", "back": "A seatbelt, not a security boundary. RemoteSigned typical."},
{"front": "Production script anatomy", "back": "#requires, CmdletBinding+param, try/catch, Write-Verbose, help, transcripts."},
{"front": "Audit-report-remediate loop", "back": "Collect state -> report drift -> fix with -WhatIf first."}
],
"quiz": [
{"q": "Get-ADUser -Filter * | Where-Object {$_.Enabled} vs Get-ADUser -Filter 'Enabled -eq $true'. Better?", "choices": ["The second - filter left, at the server", "The first", "Same", "Neither works"], "answer": 0, "index": 0, "explain": "Server-side filtering transfers less data."},
{"q": "You need the newest hotfix from 200 servers. Fastest?", "choices": ["Invoke-Command -ComputerName $servers { Get-HotFix | sort InstalledOn -desc | select -first 1 }", "RDP to each", "One by one in a loop", "Ask users"], "answer": 0, "index": 0, "explain": "Fan-out remoting parallelizes the fleet."},
{"q": "A script fails silently on errors. Fix?", "choices": ["-ErrorAction Stop + try/catch", "More Write-Host", "Run as admin", "Shorter script"], "answer": 0, "index": 0, "explain": "Terminating errors + catch = visible, handled failures."},
{"q": "-Parallel is a feature of:", "choices": ["PowerShell 7 ForEach-Object", "PowerShell 5.1", "cmd.exe", "VBScript"], "answer": 0, "index": 0, "explain": "7.x parallelism; 5.1 needs workflows/jobs."},
{"q": "Scheduled task script should use:", "choices": ["Start-Transcript logging + non-zero exit codes", "Write-Host only", "No logging", "Pause at the end"], "answer": 0, "index": 0, "explain": "Unattended scripts must leave evidence and signal failure."},
{"q": "CredSSP/Kerberos delegation solves:", "choices": ["Double-hop authentication", "Slow networks", "Typos", "Module loading"], "answer": 0, "index": 0, "explain": "Second-hop auth from a remote session."},
{"q": "Install-Module safety rule?", "choices": ["Check the publisher; prefer well-known modules", "Install everything", "Avoid the Gallery", "Only v1 modules"], "answer": 0, "index": 0, "explain": "Supply-chain: know what you import."},
{"q": "JEA provides:", "choices": ["Constrained admin endpoints - least privilege for admins", "Faster remoting", "GUI tools", "Free licenses"], "answer": 0, "index": 0, "explain": "Just Enough Administration: only the needed cmdlets."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M13", "IL27-M24", "IL27-M34"],
"drills": [
{"id": "m16-drill-ps", "title": "PowerShell Drill",
"items": [
{"prompt": "List stopped automatic services, export CSV", "answer": "Get-Service | ? {$_.StartType -eq 'Automatic' -and $_.Status -ne 'Running'} | Export-Csv s.csv", "explain": "Filter, shape, export."},
{"prompt": "What properties does X have?", "answer": "$x | Get-Member", "explain": "Discovery."},
{"prompt": "Run block on 50 servers", "answer": "Invoke-Command -ComputerName $s -ScriptBlock {...}", "explain": "Fan-out."},
{"prompt": "Parallel loop in PS7", "answer": "1..10 | ForEach-Object -Parallel {...}", "explain": "7.x parallelism."},
{"prompt": "Make errors terminating", "answer": "-ErrorAction Stop + try/catch", "explain": "Catchable failures."},
{"prompt": "Check a cmdlet's full help + examples", "answer": "Get-Help X -Full (-Examples)", "explain": "Built-in docs."}
]}
],
"handsOnLab": {
"id": "m16-lab",
"title": "Fleet Automation: audit-report-remediate",
"brief": "Build a production-grade script that audits, reports, and remediates across machines.",
"steps": [
"Write Get-FleetHealth: Invoke-Command across lab VMs collecting OS, uptime, disk, pending reboot.",
"Add comment-based help, CmdletBinding, -WhatIf support.",
"Report: Export-Csv + ConvertTo-Html dashboard saved to a share.",
"Remediate: detect low-disk VMs and clean temp files (with -WhatIf first, then real).",
"Schedule it via Task Scheduler with transcript logging; verify the log.",
"Publish as a module (psm1 + manifest) to a local repository path."
],
"deliverable": "Module + scheduled task + sample reports + transcript logs.",
"checkpoint": "You write fleet automation, not one-liners - with help, safety, and evidence."
},
"mockTask": {"id": "m16-mock", "type": "choice",
"q": "Interview (live): 'Show me how you'd find all servers missing last month's patch.'",
"choices": ["Invoke-Command fleet query of Get-HotFix, filter by date, export CSV - narrating filter-left and parallelism", "Check each manually", "Ask the users", "Guess"],
"answer": 0, "index": 0, "explain": "Live demo: remoting + filtering + reporting in one pipeline."},
"crossLinks": ["il04-windows"],
"videos": "VIDEOS_M16",
"estimatedMinutes": 330,
"fastTrackEligible": True
},
{
"id": "IL27-M17",
"code": "IL-27",
"title": "Hybrid Identity with Microsoft Entra ID",
"summary": "Bridge on-prem AD and the cloud: Entra Connect sync, SSO options, Conditional Access, and the identity Zero Trust story. Interview-critical for modern Windows roles. You need this for -> M25/M28 and every cloud conversation.",
"objectives": [
"Choose between PHS, PTA, and federation for authentication.",
"Deploy and monitor Entra Connect sync (including password hash sync concepts).",
"Design Conditional Access policies (who, what, where, risk).",
"Explain hybrid join vs Entra join and when each fits.",
"Troubleshoot sync and SSO issues."
],
"notes": [
{"title": "The hybrid architecture",
"body": "Entra ID (formerly Azure AD) is the cloud identity plane; AD DS remains the on-prem plane. Entra Connect (now 'Microsoft Entra Connect Sync' / cloud sync) bridges them: synchronizes users/groups (and optionally passwords) to the cloud. Source of truth stays on-prem in classic hybrid; cloud-first orgs flip it.\n\nDevice identities: Hybrid join (domain-joined + registered in Entra - the migration state), Entra join (cloud-native, no AD - the target for new fleets), Registered (BYOD). dsregcmd /status tells you exactly where a device stands - learn to read it.\n\nSSO options: Password Hash Sync (PHS - hashes synced, auth in cloud; simplest, survives on-prem outages), Pass-Through Authentication (PTA - auth validated against on-prem DCs via agents; no hash in cloud, needs HA agents), Federation (AD FS - most control, most complexity; only when PHS/PTA can't meet requirements). Default recommendation: PHS + Seamless SSO."
},
{"title": "Conditional Access: Zero Trust policy engine",
"body": "Conditional Access = if/then for identity: IF (user/group, cloud app, device state, location, risk) THEN (require MFA, require compliant device, block, require ToU). This is policy-as-code for access - the enforcement point of Zero Trust identity.\n\nDesign: start with report-only mode (what WOULD happen), then pilot, then enforce. Baseline policies everyone needs: require MFA for admins, block legacy auth, require compliant/hybrid-joined device for corporate apps, risk-based policies (sign-in risk -> require password change / block). Emergency access accounts (break-glass): two, cloud-only, MFA'd, monitored, excluded from CA - because a CA misconfiguration can lock out every admin.\n\nNamed locations (trusted IPs), device compliance (Intune), and Identity Protection risk signals feed the conditions. Test with the 'What If' tool before enforcing - CA mistakes lock people out at scale."
},
{"title": "Sync health and SSO troubleshooting",
"body": "Monitoring: Entra Connect Health agent reports sync errors, AADSTS codes, and agent status. Common sync issues: duplicate proxyAddresses/UPN (soft-match failures), OU filtering misconfig (objects vanish), password sync lag (check the sync cycle: default 30 min; force with Start-ADSyncSyncCycle -PolicyType Delta).\n\nSSO triage: Seamless SSO needs the Kerberos decryption key + intranet zone config; PTA needs healthy agents (check agent status, outbound 443/80); federation needs AD FS + WAP healthy. AADSTS error codes are specific - look them up, don't guess.\n\nDecommissioning path: the goal for most orgs is cloud-native over time (Entra join + Intune), with hybrid as the bridge. Know how to move a user from synced to cloud-only (move out of sync scope) and how to cut over auth method - migrations are where hybrid identity careers are made."
}
],
"cards": [
{"front": "PHS vs PTA vs Federation", "back": "PHS: hashes in cloud, simplest. PTA: validated on-prem via agents. Federation: AD FS, most control/complexity."},
{"front": "Default Microsoft recommendation", "back": "PHS + Seamless SSO."},
{"front": "Hybrid join vs Entra join", "back": "Hybrid: AD-joined + Entra-registered (migration). Entra join: cloud-native."},
{"front": "dsregcmd /status tells you", "back": "Device join state: domain/Entra/hybrid, SSO state."},
{"front": "Conditional Access structure", "back": "IF (who/app/device/location/risk) THEN (MFA/compliant/block)."},
{"front": "Break-glass accounts", "back": "2x cloud-only, MFA, monitored, excluded from CA - for lockout recovery."},
{"front": "Force a delta sync", "back": "Start-ADSyncSyncCycle -PolicyType Delta."},
{"front": "CA rollout safety", "back": "Report-only -> pilot -> enforce; test with What If."}
],
"quiz": [
{"q": "Org policy: no password hashes may be stored in the cloud. Choose:", "choices": ["PTA or federation (authentication stays on-prem)", "PHS", "Seamless SSO alone", "No sync at all"], "answer": 0, "index": 0, "explain": "PTA validates against on-prem DCs; federation delegates to AD FS - neither stores hashes in cloud."},
{"q": "Users synced but passwords don't work in cloud. Check?", "choices": ["Password hash sync status / sync errors in Connect Health", "Their shoes", "The firewall color", "DNS only"], "answer": 0, "index": 0, "explain": "PHS is a separate sync channel with its own errors."},
{"q": "Block legacy auth (old protocols). Where?", "choices": ["Conditional Access policy", "DHCP", "The firewall", "GPO wallpaper"], "answer": 0, "index": 0, "explain": "CA is the identity policy engine."},
{"q": "All admins locked out by a CA policy. Recovery?", "choices": ["Break-glass accounts (excluded from CA)", "Call Microsoft", "Wait 24h", "Reinstall Entra"], "answer": 0, "index": 0, "explain": "This is exactly what break-glass exists for."},
{"q": "Seamless SSO not working on domain PCs. Check?", "choices": ["Kerberos decryption key in Entra + intranet zone config", "The printer", "Wi-Fi password", "Time zone only"], "answer": 0, "index": 0, "explain": "Seamless SSO = Kerberos to Entra; both pieces required."},
{"q": "Duplicate UPN sync errors mean:", "choices": ["Two objects claim one identity - resolve the conflict/soft-match", "Network is slow", "Passwords expired", "Too many users"], "answer": 0, "index": 0, "explain": "Identity collision blocks sync for those objects."},
{"q": "Moving from hybrid to cloud-native for new laptops:", "choices": ["Entra join + Intune (Autopilot)", "Stay hybrid forever", "Workgroups", "No identity"], "answer": 0, "index": 0, "explain": "Cloud-native join is the target state for new fleets."},
{"q": "AADSTS50105 (guest/user not assigned to role/app). Fix?", "choices": ["Assign the user/group to the enterprise app", "Reset password", "Reboot", "New tenant"], "answer": 0, "index": 0, "explain": "App assignment gate - the specific, documented fix."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M25", "IL27-M28"],
"drills": [
{"id": "m17-drill-ident", "title": "Hybrid Identity Drill",
"items": [
{"prompt": "Simplest SSO for most orgs", "answer": "PHS + Seamless SSO", "explain": "Microsoft's default recommendation."},
{"prompt": "Force delta sync", "answer": "Start-ADSyncSyncCycle -PolicyType Delta", "explain": "On-demand sync."},
{"prompt": "Device join state?", "answer": "dsregcmd /status", "explain": "Reads join/SSO state."},
{"prompt": "CA policy about to enforce: safety?", "answer": "Report-only first, What If test, pilot", "explain": "Never enforce blind."},
{"prompt": "Locked out by CA", "answer": "Break-glass accounts", "explain": "Excluded emergency access."},
{"prompt": "Users vanish from cloud", "answer": "Check OU filtering scope", "explain": "Out-of-scope OUs don't sync."}
]}
],
"handsOnLab": {
"id": "m17-lab",
"title": "Hybrid Mini-Lab: sync + Conditional Access (trial tenant)",
"brief": "Stand up a trial Entra tenant, connect your lab AD, and enforce MFA via CA.",
"steps": [
"Create a Microsoft 365/Entra trial tenant; verify a test domain (or use onmicrosoft).",
"Install Entra Connect on LAB-DC-01 (staging mode first!); sync a pilot OU; verify users in Entra.",
"Configure PHS + Seamless SSO; test SSO from a domain client.",
"Create CA policy: require MFA for admins (report-only first, review, then enforce on a test admin).",
"Create 2 break-glass accounts; document and exclude them.",
"Test: sign in as test admin from an 'untrusted' context; verify MFA challenge; document the flow."
],
"deliverable": "Sync config + CA policies + break-glass doc + test evidence.",
"checkpoint": "You can bridge AD to Entra and enforce identity policy safely."
},
"mockTask": {"id": "m17-mock", "type": "choice",
"q": "Interview: 'How would you roll out MFA to 500 users without a revolt?'",
"choices": ["CA policy: report-only, pilot with IT, staged rollout by group, comms + registration campaign, break-glass ready, then enforce", "Enforce globally overnight", "MFA for no one", "Paper forms"],
"answer": 0, "explain": "Staged, communicated, with safety nets - the professional rollout."},
"crossLinks": ["il11-entra-identity--sc300-hybrid", "il11-entra-identity--sc300-zerotrust-ca"],
"videos": "VIDEOS_M17",
"estimatedMinutes": 300,
"fastTrackEligible": True
}
]
