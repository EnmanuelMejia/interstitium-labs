"""IL-27 Track A: Foundations (IL27-M01..M04)."""

MODULES_A = [
{
"id": "IL27-M01",
"code": "IL-27",
"title": "Hardware & PC Building Blocks",
"summary": "Every component in the box, what it does, how it fails, and how to spec a business workstation vs a server. You need this for -> imaging, troubleshooting, and sounding credible when hardware is the problem.",
"objectives": [
"Name every major PC/server component and state its function in one sentence.",
"Read a spec sheet (CPU, RAM, storage, PSU) and judge fitness for office, CAD, and server roles.",
"Diagnose the four classic hardware failure patterns: no POST, random reboots, overheating, and storage death.",
"Explain UEFI vs legacy BIOS, Secure Boot, TPM 2.0, and why Windows 11 requires them.",
"Perform safe ESD-aware handling, reseating, and minimal-boot isolation."
],
"notes": [
{"title": "The component map: what each part actually does",
"body": "CPU: executes instructions; the motherboard's chipset and socket dictate compatibility, not just the brand. Cores/threads set multitasking ceiling; clock speed sets single-thread pace; cache reduces memory waits. For office fleets, a modern i5/Ryzen 5 with 16GB RAM is the sweet spot - overspending on CPU while starving RAM is the classic waste.\n\nRAM: volatile workspace. DDR4 vs DDR5 (not interchangeable - different slots), speed (MT/s) matters less than capacity for office work, and dual-channel (matched pairs) gives real bandwidth gains. 8GB is the floor for Windows 11; 16GB the business standard.\n\nStorage: NVMe SSD (PCIe lanes, fastest), SATA SSD, then HDD (spinning, for bulk/archive). For endpoints, SSD is non-negotiable - it is the single biggest perceived-speed upgrade. Check TBW (terabytes written) endurance for write-heavy roles.\n\nMotherboard: the interconnect - chipset determines CPU/RAM/storage support. PSU: the most underrated part; a failing PSU mimics every other failure. 80 Plus rating measures efficiency, not quality - buy reputable brands with proper protections. GPU: integrated graphics suffice for office; discrete GPUs serve CAD/AI/VDI."
},
{"title": "UEFI, Secure Boot, TPM: the trust chain at power-on",
"body": "Legacy BIOS booted from the MBR with 16-bit code and no verification. UEFI is a mini-OS: GPT partitioning, >2TB boot disks, mouse-driven setup, and - critically - a verifiable boot chain. Secure Boot checks each bootloader's signature against keys in firmware; an unsigned or tampered bootloader refuses to load. This is default-deny at the hardware level, the same philosophy as application allowlisting.\n\nTPM 2.0 is a cryptographic coprocessor: it stores keys, seals BitLocker encryption to the boot state (change the bootloader and the disk won't unlock), and provides measured boot. Windows 11 requires TPM 2.0 + Secure Boot + UEFI precisely because the OS assumes this hardware root of trust.\n\nPOST (power-on self-test) runs before all of it: beep codes or diagnostic LEDs identify dead CPU/RAM/GPU. No POST + no beeps + fans spin = suspect PSU or motherboard. POST then stops at RAM = reseat/replace memory. Learn your vendor's beep/LED language; it turns a dead box into a 5-minute diagnosis."
},
{"title": "The four failure patterns and minimal-boot isolation",
"body": "Pattern 1 - No POST, no beeps, fans spin or don't: power path. Check outlet, PSU switch, 24-pin + CPU power cables, then PSU tester or known-good PSU. Pattern 2 - Random reboots/shutdowns: heat or power. Check CPU temps (90C+ under load is trouble), dust-clogged heatsinks, failing PSU under load, or bad RAM (run MemTest86). Pattern 3 - Slow grind to unusable: storage dying (check SMART: reallocated sectors, CRC errors) or thermal throttling. Pattern 4 - Intermittent weirdness (BSODs with different stop codes): RAM or motherboard; different codes each crash screams memory.\n\nMinimal-boot isolation: strip to PSU + motherboard + CPU + ONE RAM stick + integrated graphics. If it POSTs, add parts back one at a time until it fails - the last part added is guilty. Document each step; 'I swapped the RAM and it worked' is not a root cause, it's luck. ESD discipline throughout: grounded wrist strap or constant contact with bare chassis metal, components handled by edges, boards on anti-static surfaces."
}
],
"cards": [
{"front": "DDR4 vs DDR5 compatibility", "back": "Not interchangeable - different physical slots/notch positions; board and CPU must match the generation."},
{"front": "What does Secure Boot verify?", "back": "Each bootloader's cryptographic signature against firmware keys; unsigned/tampered bootloaders won't load."},
{"front": "Why does Windows 11 require TPM 2.0?", "back": "Hardware root of trust: key storage, BitLocker sealing to boot state, measured boot."},
{"front": "No POST, no beeps, fans spin: suspect?", "back": "Power path - outlet, PSU switch, cables, then PSU/motherboard."},
{"front": "Different BSOD stop code on every crash suggests?", "back": "Bad RAM (or motherboard) - inconsistent errors point at memory."},
{"front": "SMART attributes that condemn a drive", "back": "Growing reallocated sector count, CRC/interface errors, failing self-tests."},
{"front": "Minimal-boot component set", "back": "PSU + motherboard + CPU + one RAM stick + integrated graphics; add back one part at a time."},
{"front": "Business workstation sweet spot spec", "back": "Modern i5/Ryzen 5, 16GB dual-channel RAM, NVMe SSD; integrated graphics unless CAD/AI."}
],
"quiz": [
{"q": "A PC powers on (fans spin) but never POSTs and emits no beeps. First checks?", "choices": ["Outlet, PSU switch, 24-pin and CPU power cables, then PSU", "Reinstall Windows", "Replace the GPU", "Update the BIOS"], "answer": 0, "index": 0, "explain": "No POST + no beeps = power path before anything else."},
{"q": "Why can't you install DDR5 in a DDR4 slot?", "choices": ["Different physical notch/slot and electrical spec", "DDR5 is slower", "BIOS blocks it", "It fits but overheats"], "answer": 0, "index": 0, "explain": "Physically keyed differently; board/chipset must support the generation."},
{"q": "Secure Boot is best described as:", "choices": ["Signature verification of bootloaders against firmware keys", "Antivirus for the OS", "Disk encryption", "A faster boot mode"], "answer": 0, "index": 0, "explain": "It enforces a signed boot chain - default-deny at power-on."},
{"q": "Random shutdowns under load, CPU at 98C. Most likely?", "choices": ["Overheating - clean/repaste heatsink, check fans", "Failing SSD", "Bad network driver", "Corrupt user profile"], "answer": 0, "index": 0, "explain": "Thermal shutdown under load is the textbook heat pattern."},
{"q": "SMART shows reallocated sector count climbing weekly. Action?", "choices": ["Replace the drive immediately; backup now", "Defragment the drive", "Ignore until failure", "Reinstall the OS"], "answer": 0, "index": 0, "explain": "Growing reallocations = dying media; replace proactively."},
{"q": "TPM sealing for BitLocker means:", "choices": ["The disk only unlocks if the boot chain is unmodified", "The TPM stores your password", "BitLocker runs faster", "The disk is hidden from the OS"], "answer": 0, "index": 0, "explain": "Keys are sealed to PCR measurements; tampered boot = no unlock."},
{"q": "Minimal-boot still fails with known-good PSU and one RAM stick. Next suspect?", "choices": ["Motherboard or CPU (try the RAM stick in another slot first)", "The case fans", "The OS", "The monitor cable"], "answer": 0, "index": 0, "explain": "After PSU/RAM elimination, board or CPU remains; reseat CPU/check socket."},
{"q": "For 200 office workstations, the best value spec is:", "choices": ["i5/Ryzen 5, 16GB dual-channel, NVMe SSD, integrated graphics", "i9, 64GB, dual RTX GPUs", "Celeron, 4GB, HDD", "Server Xeons in tower cases"], "answer": 0, "index": 0, "explain": "Matches the workload; SSD + 16GB dominate perceived speed for office use."}
],
"weight": 1,
"prerequisiteFor": ["IL27-M02", "IL27-M18"],
"drills": [
{"id": "m01-drill-diagnose", "title": "Failure Pattern Drill",
"items": [
{"prompt": "No POST, no beeps, fans spin", "answer": "Power path: outlet, PSU switch/cables, PSU, board", "explain": "Nothing initialized; power delivery suspect."},
{"prompt": "POST stops with beep code pointing at RAM", "answer": "Reseat/replace memory; test one stick at a time", "explain": "Beep codes identify the failing subsystem."},
{"prompt": "Random reboots only under load", "answer": "Heat or PSU: check temps, clean heatsink, load-test PSU", "explain": "Load-triggered = thermal or power delivery."},
{"prompt": "Different BSOD code every crash", "answer": "Bad RAM - run MemTest86", "explain": "Inconsistent codes scream memory corruption."},
{"prompt": "System progressively slower over months", "answer": "Check SMART + thermals; suspect dying drive or throttling", "explain": "Gradual degradation = media or heat."},
{"prompt": "New build: DDR5 won't fit in the board's slots", "answer": "Board is DDR4 - generations are physically incompatible", "explain": "Notch positions differ by generation."}
]}
],
"handsOnLab": {
"id": "m01-lab",
"title": "Spec & Diagnose: build a workstation quote and a failure runbook",
"brief": "Produce a real procurement spec for 25 office workstations and a one-page hardware triage runbook.",
"steps": [
"Pick a current-gen CPU, board, 16GB DDR4/DDR5 kit, 500GB NVMe SSD, case+PSU for an office fleet; record model numbers and why each fits.",
"Price it from two vendors; note warranty length (business standard: 3yr NBD on-site).",
"Write the triage runbook: symptom -> first 3 checks, for the four failure patterns in the notes.",
"Define your minimal-boot kit list (what lives in your go-bag).",
"Document ESD procedure in 5 steps.",
"Peer-review: swap runbooks with a partner (or self-review next day) and find one missing step."
],
"deliverable": "Workstation spec sheet with pricing + one-page triage runbook + go-bag list.",
"checkpoint": "You can spec a fleet machine and talk a user through hardware triage without guessing."
},
"mockTask": {"id": "m01-mock", "type": "choice",
"q": "A user's PC shuts off 10 minutes into video calls, restarts fine, then repeats. Best first action?",
"choices": ["Check CPU/GPU temperatures and clean the heatsink/fans", "Reinstall Windows", "Replace the SSD", "Order a new PC"],
"answer": 0, "explain": "Load-dependent shutdown after minutes = thermal trip; video calls load CPU/GPU."},
"crossLinks": ["il04-windows"],
"videos": [],
"estimatedMinutes": 210,
"fastTrackEligible": False
},
{
"id": "IL27-M02",
"code": "IL-27",
"title": "Windows 10/11 Deep Administration",
"summary": "Beyond the GUI: registry, services, Task Scheduler, Event Viewer, DISM/SFC, WinRE, and the admin tools that fix what Settings cannot. You need this for -> every endpoint ticket and the interview's 'how do you troubleshoot Windows' question.",
"objectives": [
"Navigate the registry safely: hives, backup/restore, and common admin keys.",
"Manage services (startup types, dependencies, recovery actions) and scheduled tasks from CLI and GUI.",
"Use Event Viewer custom views and PowerShell to find root causes in System/Application logs.",
"Repair a damaged Windows install with SFC, DISM, WinRE, and System Restore points.",
"Configure BitLocker, Windows Update for Business rings, and local security policy."
],
"notes": [
{"title": "Registry, services, and scheduled tasks: the control layer",
"body": "The registry is Windows' configuration database: five hives (HKLM for machine, HKCU for current user, plus Classes, Users, Config). Almost every 'setting' is a value under a key. Rules: export the key before editing, change one thing, document the path. regedit's Favorites and .reg files make changes repeatable; Group Policy Preferences beats manual registry edits at fleet scale.\n\nServices (services.msc): each has a startup type (Automatic, Automatic Delayed, Manual, Disabled), a logon account, dependencies, and recovery actions (restart service, run a program, restart computer). A service stuck in 'Starting' usually means a dependency failed - check the Dependencies tab before reinstalling anything. sc.exe and PowerShell (Get-Service, Set-Service, Restart-Service) do all of this remotely.\n\nTask Scheduler is the forgotten automation engine: triggers (schedule, logon, event, idle), actions, conditions (only on AC power), and history. 'Run whether user is logged on' + stored credentials = a poor man's service. Always check the History tab - a task that 'doesn't run' usually has a failed condition or an expired credential."
},
{"title": "Event Viewer and the troubleshooting loop",
"body": "The professional loop: reproduce or identify the symptom -> Event Viewer (System for drivers/services, Application for apps, Security for logons) -> filter by time window around the incident -> read the FIRST error in the cascade, not the last. Cascades lie: ten errors at 09:14 usually trace to one root at 09:13:58.\n\nCustom Views turn repeated hunts into one click: filter System log for Event IDs 41 (unexpected shutdown), 1001 (bugcheck), 6008 (dirty shutdown) to build a crash timeline. Get-WinEvent with -FilterHashtable does the same in scripts: pull the last 24h of errors from 50 machines in one pipeline.\n\nReliability Monitor (perfmon /rel) is the underused gem: a 1-10 stability index timeline with every failure and install plotted. For 'it worked last week' cases, the timeline shows exactly what changed. Pair with Task Manager Startup impact and Autoruns (Sysinternals) for 'slow boot' tickets."
},
{"title": "Repair toolkit: SFC, DISM, WinRE, and update control",
"body": "Corruption ladder, in order: sfc /scannow (repairs protected system files from the component store), then DISM /Online /Cleanup-Image /RestoreHealth (repairs the component store itself from Windows Update), then WinRE (boot to recovery: Startup Repair, System Restore, command prompt with offline SFC/DISM). Never jump to reinstall before trying the ladder - and never run the ladder without a backup of user data first.\n\nWinRE access: Settings > Recovery > Advanced startup, or interrupt boot 3 times, or boot from install media > Repair. From WinRE command prompt, offline commands target the Windows drive (often D: in RE): sfc /scannow /offbootdir=D:\\ /offwindir=D:\\Windows.\n\nUpdates: Windows Update for Business (via Intune/GPO) uses rings - pilot (IT), broad, critical - with deferral policies, NOT 'everyone on Patch Tuesday'. WSUS is the on-prem equivalent. For a stuck update: stop wuauserv + bits, rename SoftwareDistribution, restart services. BitLocker: enable with TPM+PIN for high-risk laptops, escrow recovery keys to AD/Entra - an encrypted laptop with the key in a drawer is a brick with extra steps."
}
],
"cards": [
{"front": "The five registry hives", "back": "HKLM, HKCU, HKCR, HKU, HKCC. Machine vs user vs classes."},
{"front": "Service stuck in 'Starting' - check what first?", "back": "Dependencies tab - a dependency likely failed."},
{"front": "Event IDs for a crash timeline", "back": "41 (unexpected shutdown), 1001 (bugcheck), 6008 (dirty shutdown)."},
{"front": "In a cascade of 10 errors, which do you read?", "back": "The FIRST error - cascades propagate from one root cause."},
{"front": "Repair ladder order", "back": "SFC -> DISM -> WinRE (Startup Repair/System Restore) -> reinstall."},
{"front": "What does DISM /RestoreHealth fix that SFC cannot?", "back": "The component store itself, which SFC draws from."},
{"front": "WUfB rings", "back": "Pilot (IT) -> broad -> critical, with deferrals; not everyone on day one."},
{"front": "Stuck Windows Update fix", "back": "Stop wuauserv+bits, rename SoftwareDistribution, restart services."}
],
"quiz": [
{"q": "Before editing the registry you must:", "choices": ["Export the key and document the path", "Disable antivirus", "Boot to Safe Mode", "Take ownership of HKLM"], "answer": 0, "index": 0, "explain": "Export = instant rollback; one change at a time."},
{"q": "A service fails to start with a dependency error. You:", "choices": ["Check the Dependencies tab and start the dependency", "Reinstall the application", "Set it to Disabled", "Reboot into Safe Mode"], "answer": 0, "index": 0, "explain": "Dependencies fail first; fix the root service."},
{"q": "Ten errors at 09:14, one error at 09:13:58. Root cause is likely:", "choices": ["The 09:13:58 error - first in the cascade", "The last error at 09:14", "All ten equally", "None - check the network"], "answer": 0, "index": 0, "explain": "Cascades propagate forward; the earliest error is usually the trigger."},
{"q": "sfc /scannow reports unfixable corruption. Next step?", "choices": ["DISM /Online /Cleanup-Image /RestoreHealth, then re-run SFC", "Reinstall Windows immediately", "Run chkdsk", "Ignore it"], "answer": 0, "index": 0, "explain": "DISM repairs the component store SFC depends on."},
{"q": "Reliability Monitor is best for:", "choices": ["'It worked last week' - timeline of failures and installs", "Real-time CPU graphs", "Network packet capture", "Disk defragmentation"], "answer": 0, "index": 0, "explain": "perfmon /rel plots stability index with change history."},
{"q": "A scheduled task 'doesn't run'. Check first:", "choices": ["History tab: failed conditions or expired credentials", "The task's icon", "Windows version", "Disk space"], "answer": 0, "index": 0, "explain": "Conditions (AC power, idle) and stored credentials are the usual killers."},
{"q": "WUfB pilot ring exists to:", "choices": ["Catch bad updates on IT machines before broad deployment", "Speed up downloads", "Bypass WSUS", "Encrypt updates"], "answer": 0, "index": 0, "explain": "Rings limit blast radius of a bad patch."},
{"q": "BitLocker recovery keys must be:", "choices": ["Escrowed to AD/Entra - a lost key bricks the data", "Emailed to the user", "Stored in a drawer", "Memorized"], "answer": 0, "index": 0, "explain": "No escrow = unrecoverable; central escrow is the policy."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M11", "IL27-M23", "IL27-M26", "IL27-M27"],
"drills": [
{"id": "m02-drill-repair", "title": "Windows Repair Drill",
"items": [
{"prompt": "sfc /scannow finds corruption it cannot fix", "answer": "DISM /Online /Cleanup-Image /RestoreHealth, then SFC again", "explain": "Repair the store, then the files."},
{"prompt": "Windows won't boot at all", "answer": "WinRE: Startup Repair, System Restore, or offline SFC/DISM", "explain": "Boot to recovery environment."},
{"prompt": "Event ID 41 with no bugcheck", "answer": "Unexpected power loss - check PSU/thermals/outlet, not software", "explain": "41 = dirty shutdown without clean stop."},
{"prompt": "App crashes daily at 02:00", "answer": "Task Scheduler: inspect the 02:00 task's history and conditions", "explain": "Scheduled trigger aligns with the crash."},
{"prompt": "'Worked last week' complaint", "answer": "Reliability Monitor timeline + installed updates", "explain": "Find what changed."},
{"prompt": "Update stuck at 0% for hours", "answer": "Stop wuauserv/bits, rename SoftwareDistribution, restart", "explain": "Clears the corrupt download cache."}
]}
],
"handsOnLab": {
"id": "m02-lab",
"title": "Break & Fix: corrupt, diagnose, repair a Windows VM",
"brief": "Intentionally damage a Windows VM, then walk the full diagnostic and repair ladder and document every step.",
"steps": [
"Snapshot a Windows 10/11 VM. Delete/rename a non-critical system file copy (in a test folder mirror) OR stop a dependency service to simulate failure.",
"Use Event Viewer custom views to build the incident timeline; export it.",
"Run the repair ladder: SFC, then DISM; record outputs.",
"Boot to WinRE and practice offline commands (identify the correct drive letter in RE).",
"Configure a WUfB-style deferral via local Group Policy (Computer Config > Admin Templates > Windows Components > Windows Update).",
"Enable BitLocker on a data VHD and verify key escrow location; then revert via snapshot."
],
"deliverable": "Incident timeline export + repair log with command outputs + deferral policy screenshot + BitLocker verification.",
"checkpoint": "You can take any 'Windows is broken' ticket from symptom to root cause to repair without reinstalling."
},
"mockTask": {"id": "m02-mock", "type": "choice",
"q": "Interview: 'A user reports daily 9 AM crashes. Walk me through your troubleshooting.'",
"choices": ["Check Reliability Monitor/Event Viewer around 9 AM, find the first error in the cascade, check Task Scheduler for 9 AM triggers, then repair root cause", "Reimage immediately", "Replace the PC", "Tell them to come in at 10"],
"answer": 0, "explain": "Timeline first, first-error analysis, scheduled-trigger check - the professional loop."},
"crossLinks": ["il04-windows"],
"videos": "VIDEOS_M02",
"estimatedMinutes": 300,
"fastTrackEligible": True
},
{
"id": "IL27-M03",
"code": "IL-27",
"title": "Linux Administration Fundamentals",
"summary": "The 20% of Linux that covers 80% of infrastructure work: filesystem, permissions, systemd, packages, logs, networking, and SSH. You need this for -> Docker, monitoring servers, and any cloud VM.",
"objectives": [
"Navigate the filesystem, manage files, and explain the FHS layout (/etc, /var, /opt, /home).",
"Set ownership and permissions (chmod/chown, octal and symbolic) and explain sudo vs root.",
"Manage services with systemd (status, enable, logs via journalctl) and packages (apt/dnf).",
"Read logs effectively (journalctl, /var/log) and check disk/memory/process health.",
"Configure networking (ip addr, nmcli), SSH key auth, and the firewall basics."
],
"notes": [
{"title": "Filesystem, permissions, and the root mindset",
"body": "FHS layout: /etc (config), /var/log (logs), /var/lib (service data), /opt (third-party), /home (users), /tmp (scratch). 'Everything is a file': hardware appears in /dev, process info in /proc. When lost, which(1) finds binaries, man pages explain flags.\n\nPermissions: rwx for user/group/other, set with chmod 755 (octal) or chmod u+x (symbolic). Directories need x to enter, r to list. Ownership via chown user:group. The permission model is simple but absolute: a service running as the wrong user with 777 permissions is how breaches start - least privilege applies to files too.\n\nRoot mindset: never log in as root over SSH (PermitRootLogin no); use sudo for elevation, with full paths and reviewed commands. sudo !! re-runs the last command as root - convenient and dangerous in equal measure. For fleet work, SSH keys (ssh-keygen, authorized_keys) replace passwords: disable PasswordAuthentication once keys work."
},
{"title": "systemd, packages, and logs",
"body": "systemd owns boot and services: systemctl status/start/stop/restart/enable/disable servicename. enable = start at boot (the #1 'it worked until reboot' fix). journalctl -u servicename -f tails a service's logs; journalctl --since '1 hour ago' scopes incidents; journalctl -p err surfaces errors. /var/log still holds traditional files (syslog/auth.log) on many distros.\n\nPackages: apt (Debian/Ubuntu) / dnf (RHEL/Fedora): update (refresh lists), upgrade (apply), install, remove --purge. Pin versions for servers; unattended-upgrades for security patches with a maintenance window. Never curl|bash in production without verifying the source - and even then, prefer distro packages.\n\nHealth triage: uptime/load (load > core count = saturated), free -h (memory/swap), df -h (disk - full disks kill services silently), top/htop or ps aux (runaway processes), ss -tulpn (who's listening on which port - the first question for 'can't connect')."
},
{"title": "Networking, SSH, and firewall basics",
"body": "Modern networking: ip addr (addresses), ip route (default gateway), nmcli or netplan configs (persistent), /etc/resolv.conf or systemd-resolved (DNS), ping/traceroute/mtr for path, ss -tulpn for listeners. Predictable interface names (enp0s3, ens160) replaced eth0 - don't hardcode eth0 in scripts.\n\nSSH hardening: key-only auth, non-standard port optional (obscurity, not security), fail2ban or firewall rate-limiting, Match blocks for jump hosts. scp/rsync move files; rsync -avz --delete is the sync workhorse (test with --dry-run first).\n\nFirewall: firewalld (RHEL: zones, --add-service=http --permanent) or ufw (Ubuntu: ufw allow 22/tcp, ufw enable). Default-deny inbound, allow established/related - the host-level mirror of Zero Trust. Check both the host firewall AND cloud security groups when 'can't connect' - the packet must pass every layer."
}
],
"cards": [
{"front": "What lives in /etc, /var/log, /opt?", "back": "/etc: config files. /var/log: logs. /opt: third-party software."},
{"front": "chmod 755 as rwx triplets", "back": "rwxr-xr-x."},
{"front": "Service works until reboot, then dead. Fix?", "back": "systemctl enable servicename - it wasn't enabled at boot."},
{"front": "Follow a service's logs live", "back": "journalctl -u servicename -f."},
{"front": "Full disk, service down. First commands?", "back": "df -h (find full fs), du -sh /* (find the hog), then rotate/truncate logs."},
{"front": "Who is listening on port 443?", "back": "ss -tulpn | grep 443."},
{"front": "Safest file copy/sync with dry-run", "back": "rsync -avz --dry-run first, then without it."},
{"front": "SSH hardening top 3", "back": "Key-only auth (disable passwords), PermitRootLogin no, firewall/fail2ban rate limiting."}
],
"quiz": [
{"q": "A web service fails after every reboot but runs fine when started manually. Cause?", "choices": ["Not enabled: systemctl enable the service", "Wrong port", "DNS failure", "Corrupt binary"], "answer": 0, "index": 0, "explain": "Manual start works = unit is fine; enable = start at boot."},
{"q": "You need owner rwx, group rx, other nothing. chmod?", "choices": ["750", "755", "700", "740"], "answer": 0, "index": 0, "explain": "7=rwx, 5=r-x, 0=---."},
{"q": "Which shows failed SSH logins on most distros?", "choices": ["journalctl -u sshd or /var/log/auth.log", "/etc/passwd", "dmesg", "lastlog"], "answer": 0, "index": 0, "explain": "sshd logs auth failures to the auth facility."},
{"q": "Load average 12 on a 4-core box means:", "choices": ["Saturated - 3x more runnable work than cores", "Normal", "12% CPU used", "Memory leak"], "answer": 0, "index": 0, "explain": "Load > core count = queuing for CPU."},
{"q": "ss -tulpn shows nothing on 5432 but the app 'is running'. Likely?", "choices": ["App bound to localhost only or failed to bind - check its logs", "Firewall", "DNS", "Wrong time zone"], "answer": 0, "index": 0, "explain": "Not listening = bind failure or localhost-only; logs tell which."},
{"q": "Persistent network config on Ubuntu Server uses:", "choices": ["netplan YAML in /etc/netplan", "/etc/hosts", "ifconfig", "route -n"], "answer": 0, "index": 0, "explain": "netplan is the persistent config layer; ip commands are runtime-only."},
{"q": "Before rsync --delete to production you:", "choices": ["Run with --dry-run and review", "Just run it", "Delete the target first", "Disable SSH"], "answer": 0, "index": 0, "explain": "--delete mirrors deletions; dry-run prevents surprises."},
{"q": "'Connection refused' on SSH but ping works. Check?", "choices": ["sshd running + listening (ss -tulpn), host firewall, cloud SG", "Reinstall the OS", "Change the hostname", "Add more RAM"], "answer": 0, "index": 0, "explain": "Ping = L3 ok; refused = nothing listening or firewall - check each layer."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M20", "IL27-M34"],
"drills": [
{"id": "m03-drill-triage", "title": "Linux Triage Drill",
"items": [
{"prompt": "Service dead after reboot", "answer": "systemctl enable + status; check journalctl -u", "explain": "Enable at boot; logs show why."},
{"prompt": "Disk full alert", "answer": "df -h, du -sh, rotate/truncate logs", "explain": "Find the filesystem, then the hog."},
{"prompt": "Can't connect to app port", "answer": "ss -tulpn (listening?), firewall, cloud SG", "explain": "Each layer must pass the packet."},
{"prompt": "Who's eating CPU?", "answer": "top/htop, ps aux --sort=-%cpu", "explain": "Find the runaway process."},
{"prompt": "Need to see last hour of errors", "answer": "journalctl --since '1 hour ago' -p err", "explain": "Scoped, severity-filtered logs."},
{"prompt": "Copy /data to backup server safely", "answer": "rsync -avz --dry-run, review, then run", "explain": "Verify before syncing."}
]}
],
"handsOnLab": {
"id": "m03-lab",
"title": "Harden & Serve: deploy a Linux VM as a real server",
"brief": "Build an Ubuntu Server VM, harden SSH, deploy nginx, and document the triage commands.",
"steps": [
"Install Ubuntu Server in a VM (or cloud); snapshot.",
"Create a deploy user, add SSH key, disable password auth and root login; verify you can still get in.",
"Install nginx; enable at boot; open port 80 in ufw; verify from host.",
"Break it: stop nginx and fill /tmp to trigger an alert; practice the triage loop (systemctl status, journalctl, df -h).",
"Write a 10-line health-check script (load, disk, memory, nginx status) that exits non-zero on problems.",
"Document every command in a runbook; revert the breakage."
],
"deliverable": "Hardened VM + health-check script + triage runbook with outputs.",
"checkpoint": "You can deploy, harden, and triage a Linux server from the CLI without a GUI."
},
"mockTask": {"id": "m03-mock", "type": "choice",
"q": "Interview: 'Our Linux web server stopped responding after a reboot. Walk me through it.'",
"choices": ["Check if the service is enabled (systemctl is-enabled), start it, read journalctl for the failure, fix root cause, verify after another reboot", "Reinstall nginx", "Reboot again harder", "Blame the network"],
"answer": 0, "explain": "Enable-at-boot is the classic; verify the fix survives a reboot."},
"crossLinks": ["il04-linux"],
"videos": [],
"estimatedMinutes": 260,
"fastTrackEligible": False
},
{
"id": "IL27-M04",
"code": "IL-27",
"title": "IT Documentation & Ticketing Excellence",
"summary": "Write tickets, runbooks, and KB articles that make you the person everyone wants on their incidents. You need this for -> the interview (communication is graded), M38/M39, and every job after.",
"objectives": [
"Write tickets with repro steps, impact, timeline, and attempted fixes - no 'it's broken' tickets.",
"Produce runbooks a junior can follow at 3 AM (prereqs, steps, verification, rollback).",
"Maintain a KB: problem/symptom, cause, fix, prevention - searchable and current.",
"Communicate status updates with the right detail for users vs engineers vs management.",
"Document changes with before/after, risk, backout plan, and test results."
],
"notes": [
{"title": "The anatomy of a ticket that gets solved",
"body": "Bad ticket: 'Printer broken, please help.' Good ticket: summary, impact (who/how many), repro steps (numbered, starting from a known state), expected vs actual, timeline (when it started, what changed), attempted fixes with results, environment (hostname, OS, app version), and urgency justification. The template does the thinking: if every ticket has these fields, reporters fill them.\n\nTriage discipline: acknowledge fast (users forgive slowness, not silence), reproduce before theorizing, timebox rabbit holes (30 minutes, then escalate with notes), and never close without confirming with the reporter. 'Resolved' without verification is how tickets reopen on Friday at 4:59 PM.\n\nPrioritization is impact x urgency, not loudness: a VP's cosmetic issue loses to a broken checkout for 200 users. Say it plainly and kindly: 'I'm prioritizing the outage affecting the sales floor; yours is next in queue, ETA 2 hours.' People accept queues; they don't accept being ignored."
},
{"title": "Runbooks and KB articles that survive contact with 3 AM",
"body": "A runbook has: purpose (one line), prerequisites (access, tools, backup state), steps (numbered, each with the exact command and EXPECTED OUTPUT), verification (how you know it worked), rollback (how to undo), and escalation (when to stop and call). Test every runbook by having someone else follow it blind - the gaps you find are the pages you'll thank yourself for at 3 AM.\n\nKB article structure: symptom keywords (write what users actually type), cause, fix (steps), prevention, related articles, last-verified date. Review cadence: every article gets a 90-day freshness check; stale KBs are worse than none because they teach wrong fixes. Version your docs; 'the wiki said' should always resolve to a dated revision.\n\nDiagrams earn their keep: a one-page network diagram, a login flow, a backup topology. Keep them in version control (draw.io/diagrams.net files in git), not as screenshots in chat history."
},
{"title": "Status updates for three audiences",
"body": "Users need: what's broken, who's affected, what you're doing, when you'll update next, and a workaround. No jargon, no blame, no ETA you can't keep ('next update in 30 minutes' beats 'soon').\n\nEngineers need: symptoms, timeline, what you've ruled out, current hypothesis, logs/data attached, and what you need from them. 'DB latency spiked at 14:02, correlates with deploy #4821, rolled back at 14:20, watching' - facts, not adjectives.\n\nManagement needs: business impact, customer impact, ETA or next update time, and whether they need to do anything. One paragraph. If it needs two paragraphs, it needs a call.\n\nChange documentation: what changed (before/after), why, risk level, backout plan with tested steps, test results, and who approved. 'We changed the firewall rule' is a confession; 'Changed rule X to allow Y, tested from Z, backout is re-apply rule X-bak, approved by...' is professionalism. Post-incident: blameless timeline, root cause, action items with owners and dates - the document that prevents the next outage."
}
],
"cards": [
{"front": "Fields of a ticket that gets solved", "back": "Summary, impact, repro steps, expected vs actual, timeline, attempted fixes, environment, urgency."},
{"front": "Triage rule for rabbit holes", "back": "Timebox 30 min, then escalate WITH notes - never go dark."},
{"front": "Runbook required sections", "back": "Purpose, prereqs, steps with expected output, verification, rollback, escalation."},
{"front": "How do you test a runbook?", "back": "Someone else follows it blind; fix every gap they hit."},
{"front": "KB article freshness rule", "back": "90-day review cadence; stale KBs teach wrong fixes."},
{"front": "Status update for users: the 5 elements", "back": "What's broken, who's affected, what you're doing, next update time, workaround."},
{"front": "Change doc must include", "back": "Before/after, why, risk, tested backout plan, test results, approver."},
{"front": "Post-incident doc: the point", "back": "Blameless timeline + root cause + action items with owners/dates = prevention."}
],
"quiz": [
{"q": "Best ticket title/summary?", "choices": ["'Payroll app crashes on submit for 12 users since 9 AM; repro steps attached'", "'App broken'", "'URGENT!!!'", "'Payroll'"], "answer": 0, "index": 0, "explain": "Impact + scope + timeline + repro in one line."},
{"q": "You've spent 45 minutes on a weird driver issue with no progress. You:", "choices": ["Escalate with full notes of what you tried and ruled out", "Keep going silently for 3 more hours", "Close the ticket", "Reimage without asking"], "answer": 0, "index": 0, "explain": "Timebox + escalate with notes respects the user's time."},
{"q": "A runbook step says 'restart the service'. What's missing?", "choices": ["Expected output and verification step", "Nothing, it's fine", "A joke", "The author's name"], "answer": 0, "index": 0, "explain": "Every step needs expected output + how to verify success."},
{"q": "User asks for an ETA during an outage. You don't know. You say:", "choices": ["'Next update in 30 minutes' and keep it", "'Soon'", "'It's complicated'", "Nothing until it's fixed"], "answer": 0, "index": 0, "explain": "Commit to update cadence, not to a fix time you can't guarantee."},
{"q": "VP's cosmetic issue vs broken checkout for 200 users. Priority?", "choices": ["Checkout - impact x urgency, communicated kindly", "VP - rank decides", "Whichever came first", "Both at once"], "answer": 0, "index": 0, "explain": "Impact-driven triage, with honest communication to the VP."},
{"q": "KB article from 2022 says to edit a registry key that no longer exists. Lesson?", "choices": ["90-day freshness reviews; version and date every article", "Delete all KBs", "Wikis are useless", "Registry never changes"], "answer": 0, "index": 0, "explain": "Stale docs actively harm; freshness is a process."},
{"q": "Change doc is missing a backout plan. You:", "choices": ["Block the change until a tested backout exists", "Approve - it'll be fine", "Write the backout during the change", "Skip docs for small changes"], "answer": 0, "index": 0, "explain": "No tested backout = no change. Small changes cause big outages too."},
{"q": "Post-incident review should be:", "choices": ["Blameless, with action items owned and dated", "A search for who to blame", "Optional", "Done only for major outages"], "answer": 0, "index": 0, "explain": "Blameless + owned actions = the outage doesn't repeat."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M38", "IL27-M39"],
"drills": [
{"id": "m04-drill-comms", "title": "Communication Drill",
"items": [
{"prompt": "Rewrite: 'Printer broken, please help'", "answer": "Who/where/when/repro/impact: '3rd-floor MFP paper jam error 49 since 8 AM; 20 users affected; power-cycled twice'", "explain": "Specifics replace vagueness."},
{"prompt": "User demands ETA you can't give", "answer": "'Next update in 30 minutes' + workaround", "explain": "Cadence commitment, not fix promise."},
{"prompt": "Engineer handoff needs", "answer": "Symptoms, timeline, ruled-out items, hypothesis, logs, ask", "explain": "Facts and the specific need."},
{"prompt": "Manager update format", "answer": "Impact, customer effect, ETA/next update, any action needed - one paragraph", "explain": "Business lens, brevity."},
{"prompt": "Runbook step quality test", "answer": "Exact command + expected output + verification", "explain": "Blind-follower test."},
{"prompt": "Ticket about to auto-close; user never confirmed", "answer": "Confirm with reporter before closing", "explain": "Unverified closes reopen at the worst time."}
]}
],
"handsOnLab": {
"id": "m04-lab",
"title": "Docs Sprint: ticket, runbook, KB, post-incident",
"brief": "Produce the four documents from a simulated incident and get them reviewed.",
"steps": [
"Scenario: Monday 9 AM, 30 users can't print; MFP shows error 49; you resolve it by reseating the formatter board.",
"Write the ticket as the reporter should have (all fields), then the engineer's resolution notes.",
"Write the runbook: 'MFP error 49 triage' with expected outputs and rollback (revert = reseat original).",
"Write the KB article with symptom keywords, cause, fix, prevention (firmware update), review date.",
"Write the three-audience status updates issued during the incident (user/engineer/manager).",
"Write the post-incident: timeline, root cause, 3 action items with owners and dates."
],
"deliverable": "Ticket + runbook + KB + 3 status updates + post-incident doc.",
"checkpoint": "A stranger could resolve the incident from your docs alone."
},
"mockTask": {"id": "m04-mock", "type": "choice",
"q": "Interview: 'How do you handle a frustrated user whose issue you can't fix immediately?'",
"choices": ["Acknowledge quickly, set a 30-min update cadence, give a workaround, timebox and escalate with notes", "Avoid them until it's fixed", "Promise it will be fixed in an hour", "Tell them it's low priority"],
"answer": 0, "explain": "Fast acknowledgment + cadence + workaround + honest escalation."},
"crossLinks": [],
"videos": [],
"estimatedMinutes": 200,
"fastTrackEligible": True
}
]
