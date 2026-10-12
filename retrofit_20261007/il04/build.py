#!/usr/bin/env python3
"""Retrofit IL-04 modules to the Multicloud course template shape.
Reads il-04 JSON, rewrites module summaries/notes/cards/quiz + weights,
writes atomically with json.load validation before and after."""
import json, os

REPO = os.path.expanduser('~/workspace/apex-audit')
SRC = os.path.join(REPO, 'docs/university/data/courses/il-04-systems-linux-windows-networks.json')

course = json.load(open(SRC))  # validate BEFORE

# ---------------------------------------------------------------- module 1
LINUX_SUMMARY = (
"Welcome to IL-04 — Systems, Linux, Windows & Networks. I'm your instructor for this course, "
"and this is Module 1: Linux Foundations to RHCSA. Over this module we take you from first principles "
"— the shell as an instrument, the filesystem hierarchy, permissions — through real administration "
"(users, systemd, LVM storage, firewalld, SELinux) and on to the RHCSA EX200 performance exam, with "
"LPIC-1/LPIC-2 running alongside as the vendor-neutral companion track. Performance exams are won in "
"the terminal: every concept below pairs with a hands-on lab, and you will break things and fix them "
"under time. If you can think in pipelines, administer with least privilege, and read an SELinux denial "
"without flinching, this module has done its job."
)

LINUX_NOTES = [
{
"title": "Concepts",
"body": (
"- **filesystem hierarchy** — the map of a Linux system: /etc holds configuration, /var holds variable "
"data (logs, spool), /usr holds programs and libraries, /home holds user data, /proc and /sys are "
"kernel interfaces, not real files.\n"
"- **permissions** — the law: rwx across user/group/other, expressed as octal (640 = rw-r-----), plus "
"setuid/setgid/sticky bits (4755 = setuid + rwxr-xr-x: executes with the file owner's privileges).\n"
"- **pipes** — connect a command's stdout to the next command's stdin (|): the instrument you think in, "
"as in journalctl ... | grep -i error | awk '{print $5}' | sort | uniq -c | sort -nr — filter, extract, "
"count, rank.\n"
"- **redirection** — send output to files: > overwrites, >> appends.\n"
"- **text processing** — grep, sed, awk, sort, uniq, xargs: the toolkit for turning log noise into answers.\n"
"- **set -euo pipefail** — the three lines that prevent 3 AM pages: exit on error (-e), on undefined "
"variables (-u), and on pipe failures (-o pipefail). In every script.\n"
"- **users/groups/ACLs** — useradd and groupmod manage identity; setfacl/getfacl grant fine-grained "
"access beyond owner/group/other.\n"
"- **systemd** — the init and service manager: units with [Unit]/[Service]/[Install] sections, "
"systemctl enable --now to enable and start, journalctl -u to read a service's logs, targets and timers "
"(timers are the modern cron: calendar or monotonic triggers with journal logging).\n"
"- **LVM** — the layer that makes resizing sane: physical volumes (PV, the disks) pour into a volume "
"group (VG, the pool); logical volumes (LV) are sliced out. Resize any layer independently; also "
"Stratis, Btrfs, and VDO (deduplication/compression) as the storage alternatives.\n"
"- **firewalld** — zone-based firewalling: assign interfaces to zones, open services not ports "
"(--add-service=http), rich rules for exceptions.\n"
"- **ip / nmcli / ss** — the modern networking tools: ip replaces ifconfig, nmcli manages NetworkManager, "
"ss -tlnp shows TCP listening sockets with numeric ports and the owning process.\n"
"- **SELinux** — mandatory access control by context (user:role:type:level): a file can have correct "
"Unix permissions and still be denied because its context is wrong. ls -Z shows contexts, restorecon "
"repairs them, semanage fcontext persists the rule, audit2allow generates policy (use sparingly — "
"understand the denial before allowing it).\n"
"- **podman** — daemonless, rootless container runtime: the RHEL-native tool (quadlets integrate "
"containers with systemd as services).\n"
"- **RHCSA (EX200)** — Red Hat's hands-on performance exam: broken systems and a clock, man pages "
"available; it recycles the same five root causes (service running? port listening? firewall? SELinux? "
"disk full?).\n"
"- **LPIC-1 / LPIC-2** — the vendor-neutral Linux Professional Institute track (101/102 essentials, "
"201/202 advanced): the companion proof alongside the Red Hat one."
)
},
{
"title": "Hands-on procedure",
"body": (
"Do this on a lab VM or with loop devices — never on a machine you care about. The procedure builds the "
"full LVM lifecycle and grows the filesystem online, then writes a hardening audit script.\n\n"
"1. Create a file-backed 'disk' so the lab is safe anywhere: dd if=/dev/zero of=/tmp/disk1.img bs=1M "
"count=256, then DEV=$(losetup -f --show /tmp/disk1.img).\n"
"2. Build the LVM layers in order: pvcreate \"$DEV\", then vgcreate vgdata \"$DEV\", then "
"lvcreate -n applv -L 100M vgdata.\n"
"3. Put a filesystem on it and mount it: mkfs.xfs /dev/vgdata/applv, mkdir -p /mnt/app, mount "
"/dev/vgdata/applv /mnt/app; confirm with df -h /mnt/app.\n"
"4. Extend online with zero downtime: lvextend -L +100M /dev/vgdata/applv, then xfs_growfs /mnt/app "
"(or resize2fs for ext4). Confirm the new size with df -h.\n"
"5. Clean up in reverse: umount, lvremove, vgremove, pvremove, losetup -d.\n"
"6. Write the hardening audit script starting every script with set -euo pipefail: grep -R NOPASSWD "
"/etc/sudoers /etc/sudoers.d/ for passwordless sudo, find /etc -xdev -type f -perm -0002 for "
"world-writable files, ss -tlnp for listening ports, and journalctl -u sshd --since today | grep -ci "
"'failed' for today's failed SSH logins; write all findings to a dated report file.\n"
"7. Create an SELinux trap on purpose: move a file from /home to /srv/web, confirm ls -Z shows the "
"wrong context, then restorecon -Rv /srv/web and confirm the service can read it again. This is the "
"exam's favorite trap — rehearse it until it is boring."
),
"code": (
"set -euo pipefail\n"
"dd if=/dev/zero of=/tmp/disk1.img bs=1M count=256\n"
"DEV=$(losetup -f --show /tmp/disk1.img)\n"
"pvcreate \"$DEV\" && vgcreate vgdata \"$DEV\" && lvcreate -n applv -L 100M vgdata\n"
"mkfs.xfs -f /dev/vgdata/applv && mount /dev/vgdata/applv /mnt/app\n"
"lvextend -L +100M /dev/vgdata/applv && xfs_growfs /mnt/app\n"
"ls -Z /srv/web/index.html        # check the context first\n"
"restorecon -Rv /srv/web          # fix the context\n"
"journalctl -u sshd --since today | grep -ci 'failed'"
),
"lang": "bash"
},
{
"title": "Project brief",
"body": (
"Your applied capstone for this module: deliver a hardened, documented RHEL 9 server build — the kind of "
"hand-off a senior admin would accept without rework.\n\n"
"The scenario. A small company needs one RHEL 9 application server rebuilt from a kickstart: the old "
"box failed its audit (world-writable configs, passwordless sudo entries, SELinux in permissive mode, "
"services listening that nobody can explain).\n\n"
"Your deliverables:\n"
"- A build script (bash, set -euo pipefail) that creates the application LV on LVM, mounts it, sets "
"ownership and permissions (640/750 discipline, umask 027 for the app user), and enables the services "
"via systemd units — one of them on a systemd timer.\n"
"- The hardening audit script from the Hands-on procedure, run against your own build, with its findings "
"report attached and every finding either remediated or documented with a reason.\n"
"- SELinux enforcing with correct contexts on all application paths (show ls -Z before/after for at "
"least one relabeled path); firewalld allowing only the required services.\n"
"- A one-page operations note: how to extend the application volume online, where the logs live "
"(journalctl), and the five-root-cause triage order for 'the app is down'.\n\n"
"Stretch: containerize the application with podman and manage it as a systemd service via a quadlet, "
"rootless."
)
},
{
"title": "Noah check-in",
"body": (
"Noah probes mastery with questions like:\n"
"- Walk Noah through the exact layer order you would check when a service cannot read a file it could "
"read yesterday: permissions, then context — why is that order correct?\n"
"- Give Noah the LVM layer order (PV -> VG -> LV) and explain why extending the filesystem without "
"extending the LV first cannot work.\n"
"- *Timed drill:* Noah gives you a moved file with correct Unix permissions and a denied service. Name "
"the two commands that diagnose and fix it, and say why setenforce 0 is the wrong answer.\n\n"
"Honesty note: all labs, scenarios, and questions in this module are original practice material — never "
"recalled exam content. EX200 is a hands-on performance exam; confirm the current objectives on "
"redhat.com before booking, because exam versions change. Preparation only: this course confers no "
"certificate and is not affiliated with Red Hat or LPI."
)
}
]

LINUX_ADD_CARDS = [
{"front": "umask 027 produces what defaults?", "back": "New files 640 (rw-r-----), new directories 750 (rwxr-x---)."},
{"front": "setfacl -m u:ana:rwx does what?", "back": "Grants user ana rwx on the file — fine-grained access beyond owner/group/other; verify with getfacl."},
]

LINUX_QUIZ = [
{"q": "A service fails to read /srv/data/file after a move from /home. Permissions are correct. Likely cause?",
 "choices": ["disk full", "SELinux context wrong", "wrong owner", "file locked"], "answer": 1,
 "explain": "mv preserves the source context (/home) — restorecon -Rv /srv/data fixes it. Classic RHCSA trap. Covered in the Concepts section."},
{"q": "Which grows a filesystem online after extending its LV?",
 "choices": ["reboot", "resize2fs / xfs_growfs on the mounted fs", "reinstall", "fsck only"], "answer": 1,
 "explain": "LVM + online resize: lvextend then resize2fs (ext4) or xfs_growfs (XFS) — no downtime. Covered in the Hands-on procedure section."},
{"q": "firewalld: allow HTTP persistently?",
 "choices": ["iptables -A INPUT -p tcp --dport 80 -j ACCEPT", "firewall-cmd --add-service=http --permanent && --reload", "open port 80 in the router", "systemctl open http"], "answer": 1,
 "explain": "Zone model: --add-service=http --permanent, then reload. Services, not raw ports. Covered in the Concepts section."},
{"q": "set -euo pipefail guards against?",
 "choices": ["slow scripts", "silent failures: unchecked errors, unset vars, masked pipe failures", "syntax errors only", "nothing"], "answer": 1,
 "explain": "-e exits on error, -u on unset variables, -o pipefail propagates pipe failures — the 3 AM page preventers. Covered in the Concepts section."},
{"q": "podman vs docker, RHEL exam relevance?",
 "choices": ["identical", "podman: daemonless, rootless, quadlets for systemd — the RHEL-native tool", "docker is required", "neither is tested"], "answer": 1,
 "explain": "EX200 tests podman: rootless containers managed as systemd services via quadlets. Covered in the Concepts section."},
{"q": "EX200 time strategy?",
 "choices": ["tasks in order, perfectionist", "read all, quick wins first, verify each, man pages allowed", "skip verification to save time", "memorize every command flag"], "answer": 1,
 "explain": "Triage like a workday: quick wins, flag long tasks, verify as you go, use man -k. Covered in the Noah check-in section."},
{"q": "A new deploy user needs default file permissions 640. What umask do you set in their profile?",
 "choices": ["022", "027", "077", "002"], "answer": 1,
 "explain": "umask 027 strips write for group and all for other: new files 640, directories 750. Covered in the Project brief section."},
{"q": "You need to give contractor 'ana' read-write-execute on /srv/app without changing the owner or group. Command?",
 "choices": ["chmod 777 /srv/app", "setfacl -m u:ana:rwx /srv/app", "chown ana /srv/app", "usermod -aG root ana"], "answer": 1,
 "explain": "setfacl grants per-user rights beyond owner/group/other; chmod 777 and group changes are over-broad. Covered in the Concepts section."},
]

# ---------------------------------------------------------------- module 2
WINDOWS_SUMMARY = (
"Welcome back to IL-04 — Systems, Linux, Windows & Networks. I'm your instructor, and this is "
"Module 2: Windows Systems Administration. Linux gave you the shell as an instrument; Windows gives "
"you the other half of the enterprise: NTFS permissions and the effective-access rule, services and "
"the registry, event logs and diagnostics — then identity with Active Directory (forests, domains, "
"OUs, Group Policy, Kerberos and NTLM), PowerShell automation through the object pipeline, and the "
"networking services Windows Server runs (DNS, DHCP, file and print). The discipline carries over: "
"least privilege, documented change, verified state. By the end you will read a GPO conflict, a "
"Kerberos failure, and a permission mystery the way you now read a pipeline — start to finish, with "
"evidence at every step."
)

WINDOWS_NOTES = [
{
"title": "Concepts",
"body": (
"- **NTFS permissions** — file-system rights (Full Control, Modify, Read & Execute, List Folder "
"Contents, Read, Write, plus special permissions like Traverse and Execute File): they travel with the "
"file and form the real security boundary.\n"
"- **share permissions** — the network entry point's rights: they combine with NTFS, and the effective "
"access is the *most restrictive* of the two. This single rule answers half the permissions questions.\n"
"- **effective access** — compute it, don't guess it: the Effective Access tab shows the real result; "
"guessing permissions is how outages happen.\n"
"- **services** — background processes managed via services.msc, sc.exe, or PowerShell Get-Service: "
"startup types, dependencies, and recovery actions.\n"
"- **registry** — the configuration database (e.g. HKLM\\SYSTEM\\CurrentControlSet\\Services): export "
"before editing, always.\n"
"- **event logs** — Event Viewer (System/Application/Security), wevtutil, Reliability Monitor: "
"troubleshooting starts here. Methodology: reproduce, check logs, isolate, fix, verify, document.\n"
"- **Server Core vs Desktop Experience** — Core is the smaller attack surface with fewer patches: the "
"exam's preferred answer for a new server, fully manageable remotely.\n"
"- **forest** — the Active Directory security boundary; contains domains, which contain OUs. Design OUs "
"by *administration*, not by org chart.\n"
"- **Group Policy** — GPOs link to sites, domains, and OUs; processing order is LSDOU (Local, Site, "
"Domain, OU — later wins); Enforced beats Block Inheritance. gpupdate /force applies now, gpresult /r "
"shows what applied.\n"
"- **AGDLP** — the canonical group-nesting pattern: Accounts go into Global groups, into Domain Local "
"groups, which get the Permissions.\n"
"- **Kerberos** — ticket-based authentication (AS then TGS then service): needs time sync (more than ~5 "
"minutes of skew kills auth), registered SPNs, and a reachable KDC — the troubleshooting trio.\n"
"- **NTLM** — legacy challenge-response authentication: pass-the-hash risk, avoid where Kerberos works.\n"
"- **hybrid identity** — Entra ID Connect syncs on-prem AD with Entra ID for SSO shapes across cloud "
"and on-prem.\n"
"- **PowerShell pipeline** — passes *objects*, not text: Get-Process | Where-Object CPU -gt 100 | "
"Sort-Object CPU -Descending | Select-Object -First 5. Filter left (Where-Object early), format right "
"(Format-* last — formatting destroys the objects).\n"
"- **PowerShell remoting / DSC** — Enter-PSSession and Invoke-Command run code on remote machines; DSC "
"is the declarative configuration model (desired state, LCM enforces it).\n"
"- **DNS** — zones, records, forwarders, scavenging: internal resolution working but external failing "
"points at forwarders or root hints first.\n"
"- **DHCP** — scopes, reservations, failover: the DORA dance (Discover, Offer, Request, Acknowledge); "
"the classic 80/20 scope split is legacy thinking — proper failover is the modern answer."
)
},
{
"title": "Hands-on procedure",
"body": (
"Do this on a lab Server Core VM with the AD DS role — the procedure rehearses the three skills the "
"module keeps testing: permissions reasoning, GPO scoping, and pipeline discipline.\n\n"
"1. Create a folder C:\\Share\\Finance, set NTFS Modify for the Finance group and share Read for the "
"same group; then open the Effective Access tab for a Finance user and record the result: Read — most "
"restrictive wins. Widen the share to Change and re-check.\n"
"2. Build the OU design: one OU per administration boundary (e.g. OU=Workstations,OU=Sales), never one "
"OU per org-chart box. Link a GPO at the domain level and a conflicting setting at the OU level.\n"
"3. Run gpresult /r on a test client and read which GPO won the conflict: the OU-linked one (LSDOU — "
"later wins). Then set Enforced on the domain GPO and re-check the flip.\n"
"4. Break Kerberos on purpose: skew the client clock by 8 minutes and attempt a domain logon; confirm "
"failure. Sync with w32tm, confirm logon works. You now own the most-tested Windows troubleshooting "
"fact there is.\n"
"5. Write a PowerShell audit one-liner and save it as a script (no aliases in scripts): "
"Get-Service | Where-Object {$_.Status -eq 'Running'} | Sort-Object DisplayName | Select-Object "
"Name, Status — filter left, format right.\n"
"6. Use Invoke-Command to run the audit against two lab machines at once: remoting is how one admin "
"covers a fleet.\n"
"7. Document every change you made (GPO links, share/NTFS settings, clock skew) with a rollback note — "
"documented change is the discipline, not the paperwork."
),
"code": (
"# Effective access: most restrictive of NTFS vs share wins\n"
"Get-SmbShareAccess -Name Finance\n"
"icacls C:\\Share\\Finance\n"
"# GPO scoping: what applied, and who won\n"
"gpupdate /force\n"
"gpresult /r\n"
"# Kerberos clock check\n"
"w32tm /query /status\n"
"# Pipeline discipline: filter left, format right\n"
"Get-Service | Where-Object {$_.Status -eq 'Running'} | Sort-Object DisplayName | Select-Object Name, Status\n"
"# One audit, many machines\n"
"Invoke-Command -ComputerName SRV1,SRV2 -ScriptBlock { Get-Service | Where-Object {$_.Status -eq 'Running'} }"
),
"lang": "powershell"
},
{
"title": "Project brief",
"body": (
"Your applied capstone for this module: stand up a small, defensible Windows domain lab and hand over "
"the runbook.\n\n"
"The scenario. A 25-person company has been running as a workgroup with 'everyone shares everything'. "
"They have approved a single new domain controller — Server Core, because you argued the smaller "
"attack surface — and one file server.\n\n"
"Your deliverables:\n"
"- The OU design document: forest/domain/OU layout designed by administration boundary, the AGDLP "
"group-nesting plan for Finance, Sales, and IT, and where each GPO links (with the LSDOU reasoning "
"written down, not assumed).\n"
"- Three working GPOs: a baseline security policy at the domain level, a mapped-drive/preferences GPO "
"at the OU level (preferences where reversibility matters, policies where enforcement matters), and "
"one Enforced setting with a written justification for why it overrides Block Inheritance risk.\n"
"- NTFS + share permission matrix for the company shares, each cell justified by the effective-access "
"rule, and a screenshot-equivalent transcript of the Effective Access tab check per share.\n"
"- A PowerShell runbook script (pipeline-disciplined, no aliases): audit script that reports services, "
"share permissions, and last GPO application across both servers via remoting, output as objects ready "
"for Export-Csv.\n"
"- The Kerberos triage card: time sync, SPN, KDC reachability — the three checks, in order, with the "
"commands.\n\n"
"Stretch: configure DHCP failover between the two servers and document the DORA flow you observed in a "
"packet capture."
)
},
{
"title": "Noah check-in",
"body": (
"Noah probes mastery with questions like:\n"
"- A user has NTFS Full Control and Share Read on a folder. State their effective access and the rule "
"that produces it — then explain why you would still set both deliberately instead of relying on one.\n"
"- Two GPOs conflict: one linked at the Domain, one at the OU, nothing enforced. Which wins, and what "
"single change flips the outcome?\n"
"- *Hands-on:* Noah skews your lab client's clock by 10 minutes. Diagnose the logon failure out loud: "
"which protocol broke, why, and the exact command that fixes it.\n\n"
"Honesty note: all labs, scenarios, and questions in this module are original practice material — never "
"recalled exam content. Windows Server versions and PowerShell behaviors change: confirm against "
"Microsoft Learn before treating any behavior as current. Preparation only: this course confers no "
"certificate and is not affiliated with Microsoft."
)
}
]

WINDOWS_ADD_CARDS = [
{"front": "Why set BOTH NTFS and share permissions?", "back": "NTFS is the real boundary (travels with the file); share is the network entry point. Set both deliberately; effective access is the most restrictive of the two."},
{"front": "Group Policy preferences vs policies?", "back": "Preferences tattoo lightly (reversible, user can change); policies enforce (reapply, locked). Use preferences where reversibility matters."},
]

WINDOWS_QUIZ = [
{"q": "NTFS Modify + Share Read on a folder. User's effective access?",
 "choices": ["Modify", "Read", "Full", "Deny"], "answer": 1,
 "explain": "Most restrictive of NTFS and share wins: Read. Covered in the Concepts section."},
{"q": "A GPO linked at Domain and OU conflict. Which wins (no enforcement)?",
 "choices": ["Domain", "OU", "Site", "Local"], "answer": 1,
 "explain": "LSDOU — later (closer to the object) wins; OU beats Domain. Covered in the Concepts section."},
{"q": "Kerberos fails across the domain; clocks differ by 8 minutes. Fix?",
 "choices": ["rejoin the domain", "sync time (w32tm)", "reset passwords", "rebuild KDC"], "answer": 1,
 "explain": "Kerberos tolerates ~5 min skew — 8 minutes breaks ticket validation. Sync time first. Covered in the Hands-on procedure section."},
{"q": "Pipeline best practice?",
 "choices": ["Format-Table first", "filter with Where-Object early, format last", "avoid the pipeline", "use aliases in scripts"], "answer": 1,
 "explain": "Filter left (reduce objects early), format right (formatting destroys the objects). Covered in the Concepts section."},
{"q": "DNS resolves internally but not externally. Check first?",
 "choices": ["reinstall DNS", "forwarders / root hints", "DHCP scope", "firewall on client"], "answer": 1,
 "explain": "Internal resolution works → the server is fine; external failure points at forwarders/root hints. Covered in the Concepts section."},
{"q": "Server Core vs Desktop Experience for a new DC?",
 "choices": ["Desktop — easier", "Core — smaller attack surface, fewer patches", "identical", "Core can't be a DC"], "answer": 1,
 "explain": "Core is the exam's preferred answer: less surface, fewer reboots, fully manageable remotely. Covered in the Concepts section."},
{"q": "In AGDLP, which group type receives the permission directly?",
 "choices": ["Global group", "Domain Local group", "Universal group", "the user account"], "answer": 1,
 "explain": "Accounts → Global → Domain Local → Permissions: the Domain Local group is the one stamped with the permission. Covered in the Concepts section."},
{"q": "Why prefer Kerberos over NTLM where both are available?",
 "choices": ["Kerberos is faster to type", "NTLM carries pass-the-hash risk; Kerberos is ticket-based and stronger", "NTLM requires more servers", "no difference"], "answer": 1,
 "explain": "NTLM is legacy challenge-response with pass-the-hash risk; Kerberos tickets are the modern, stronger mechanism. Covered in the Concepts section."},
]

# ---------------------------------------------------------------- module 3
NET_SUMMARY = (
"Welcome to Module 3 of IL-04 — Systems, Linux, Windows & Networks. I'm your instructor, and this "
"module is the network itself: the Network+ N10-009 core with Wireshark-level packet literacy. We "
"start with the maps — the OSI and TCP/IP models, IPv4 and IPv6 addressing — then build the reflex "
"every network engineer owns: subnetting to the point where a /27 is arithmetic, not a puzzle. From "
"there: switching and VLANs, routing protocols, wireless, the appliances that sit in the path, and "
"finally the skill that separates engineers from guessers — reading packets and applying the 6-step "
"troubleshooting methodology with evidence. The Network+ exam leans on performance-based questions; "
"this module rehearses exactly those, and the packet work you do here will serve every role you ever "
"take after it."
)

NET_NOTES = [
{
"title": "Concepts",
"body": (
"- **OSI model** — seven layers (physical → data link → network → transport → session → presentation "
"→ application): the troubleshooting map. Isolate bottom-up — cabling before configuration.\n"
"- **TCP/IP model** — the four-layer working model the Internet actually runs on; OSI is the map, "
"TCP/IP is the territory.\n"
"- **IPv4 / CIDR** — dotted-decimal addresses with prefix lengths: /24 = 254 hosts, /27 = 30 hosts, "
"hosts = 2^(32-n) − 2.\n"
"- **IPv6** — hex addresses with prefix lengths; no broadcast (multicast instead); link-local "
"fe80::/10, global unicast, and subnetting on nibble boundaries (/48 site, /64 subnet) — easier than "
"v4 once the hex clicks.\n"
"- **subnetting** — borrowing host bits to carve networks: the 60-second drill (given any /25–/28, "
"produce network/broadcast/usable range) is trainable and tested.\n"
"- **VLSM** — variable-length subnet masks: right-size each subnet (point-to-point links get /30 or "
"/31, VLANs get what they need) instead of wasting a /24 on two routers.\n"
"- **summarization** — aggregating contiguous blocks (192.168.0.0/24 through 192.168.3.0/24 → "
"192.168.0.0/22): smaller routing tables, valid when the blocks are contiguous with the same next hop.\n"
"- **VLAN** — virtual LAN: segments broadcast domains on one switch fabric.\n"
"- **802.1Q** — the VLAN tagging standard: trunk ports carry tagged frames for multiple VLANs; access "
"ports carry one untagged VLAN.\n"
"- **STP** — Spanning Tree Protocol: loop prevention. A port in blocking state is listening, not "
"forwarding — that is the protocol working, not a failure.\n"
"- **OSPF** — link-state routing inside one autonomous system: Dijkstra's algorithm, areas, fast "
"convergence.\n"
"- **BGP** — path-vector, the Internet's routing protocol: carries policy between autonomous systems "
"(AS_PATH in concept). Different job from OSPF — interior speed vs exterior policy.\n"
"- **802.11 / wireless** — a/b/g/n/ac/ax across 2.4/5/6 GHz with MIMO and channel width; on 2.4 GHz "
"only channels 1, 6, 11 don't overlap — the most-tested wireless fact in existence.\n"
"- **WPA2 vs WPA3** — WPA3's SAE handshake replaces the crackable WPA2 4-way handshake and resists "
"offline dictionary attacks.\n"
"- **firewall** — stateful vs NGFW (next-generation, application-aware): the policy enforcement point.\n"
"- **load balancer** — distributes traffic across servers (algorithms: round-robin, least-connections).\n"
"- **proxy / IDS/IPS** — proxies mediate and cache; IDS detects, IPS prevents — placement determines "
"what they can see.\n"
"- **SNMP / NetFlow/sFlow** — monitoring: SNMP polls device state, NetFlow/sFlow sample traffic. You "
"can't troubleshoot what you don't measure — baselines first, anomaly detection second.\n"
"- **Wireshark** — the packet analyzer: follow a TCP stream, read the three-way handshake (SYN, "
"SYN-ACK, ACK), spot retransmissions (congestion or loss), decode DNS and DHCP exchanges, recognize "
"the TLS ClientHello.\n"
"- **6-step troubleshooting methodology** — identify the problem, establish a theory, test the theory, "
"establish a plan, implement, verify and document. Same discipline as the scenarios: scope first (one "
"host? one VLAN? everyone?), then bottom-up.\n"
"- **PBQ** — performance-based questions: Network+ sims for subnetting, CLI-output analysis, and "
"diagram troubleshooting. The drill set rehearses exactly these; the objective weights say "
"troubleshooting (24%) comes first."
)
},
{
"title": "Hands-on procedure",
"body": (
"Two drills, daily for two weeks. This is arithmetic reflex and packet reading — both are trained, not "
"studied.\n\n"
"1. Subnetting drill: take 192.168.20.64/27. Host bits = 5, so 32 addresses: .64–.95. Network .64, "
"broadcast .95, usable .65–.94. Do one random /25–/28 per day and time yourself; under 60 seconds is "
"the target.\n"
"2. Summarization drill: take 10.1.0.0/24 through 10.1.3.0/24 — four contiguous /24s share 22 network "
"bits → 10.1.0.0/22. Say the rule out loud: contiguous blocks, same next hop.\n"
"3. Open Wireshark on your lab interface and capture while you open one web page. Stop the capture.\n"
"4. Find the TCP three-way handshake: filter tcp.flags.syn==1, confirm the SYN → SYN-ACK → ACK sequence "
"to the web server's port 443. That sequence is the most-read pattern in packet analysis.\n"
"5. Right-click one TCP packet and choose Follow → TCP Stream. Read the TLS ClientHello — the moment "
"encryption negotiation begins.\n"
"6. Run a DHCP exchange (ipconfig /release then /renew on Windows, or restart networking on Linux) "
"while capturing: identify the DORA sequence — Discover, Offer, Request, Acknowledge — four packets, "
"in order.\n"
"7. Introduce loss on purpose (unplug for two seconds mid-transfer, or throttle the lab link) and watch "
"retransmissions appear: retransmissions mean segments went unacknowledged — loss, congestion, or a "
"dead peer.\n"
"8. Apply the 6-step methodology to one real lab fault per week: identify (scope: one host? one VLAN? "
"everyone?), theory, test, plan, implement, verify/document. Write the one-paragraph postmortem."
),
"code": (
"# Subnetting reflex: /27 -> 32 addresses\n"
"# 192.168.20.64/27: network .64, broadcast .95, usable .65-.94\n"
"# Summarization: 10.1.0.0/24-10.1.3.0/24 -> 10.1.0.0/22\n"
"# Wireshark display filters for the drills:\n"
"tcp.flags.syn==1          # find handshakes\n"
"dns                      # DNS query/response pairs\n"
"bootp                    # DHCP DORA exchange\n"
"tcp.analysis.retransmission  # spot loss/congestion"
),
"lang": "bash"
},
{
"title": "Project brief",
"body": (
"Your applied capstone for this module: a network design document and a troubleshooting playbook for a "
"small company — the two artifacts that prove you can both build and fix.\n\n"
"The scenario. A 60-person company is moving into a two-floor office: wired workstations, a small "
"server room, warehouse scanners on Wi-Fi, and a guest network that must never touch the corporate "
"LAN. Their current 'network' is one flat /24 and a consumer router.\n\n"
"Your deliverables:\n"
"- The addressing plan: VLSM design with right-sized subnets per VLAN (workstations, servers, voice, "
"warehouse Wi-Fi, guest, and /30 or /31 point-to-point links), plus the summarized route you would "
"advertise upstream — every subnet justified, no wasted space.\n"
"- The switching design: VLAN assignments, which ports are access vs 802.1Q trunk, where STP is "
"protecting you, and the channel plan for the 2.4 GHz warehouse coverage (1/6/11, with the reasoning).\n"
"- The routing call: where static routes suffice and where a dynamic protocol earns its keep — OSPF "
"inside, and the one-paragraph explanation of what BGP would be for if they ever multi-home.\n"
"- The security layer: firewall placement and policy sketch, where IDS/IPS sits, WPA3 for corporate "
"wireless with the SAE rationale, and the guest segmentation that keeps visitors off the LAN.\n"
"- The troubleshooting playbook: the 6-step methodology written as a runbook ('the network is down' → "
"scope first: one host? one VLAN? everyone?), the Wireshark capture procedure with the three patterns "
"to check first (handshake, DNS, DHCP), and the monitoring baseline (what SNMP/NetFlow would collect "
"so the next fault has something to compare against).\n\n"
"Stretch: produce the summarized supernet for a second site and show the single route entry that covers "
"both."
)
},
{
"title": "Noah check-in",
"body": (
"Noah probes mastery with questions like:\n"
"- Noah hands you 172.16.8.0/21. State the broadcast address and defend it: how many addresses, which "
"octet moves, and why.\n"
"- In a capture, Noah points at a burst of TCP retransmissions. What do they indicate, and what is the "
"one thing they do NOT indicate?\n"
"- *Whiteboard:* Noah asks you to place OSPF and BGP on a two-site diagram and justify each placement "
"in one sentence per protocol.\n\n"
"Honesty note: all labs, drills, and questions in this module are original practice material — never "
"recalled exam content. N10-009 domains and weights change: confirm the current objectives on "
"comptia.org before booking. Preparation only: this course confers no certificate and is not "
"affiliated with CompTIA."
)
}
]

NET_ADD_CARDS = [
{"front": "VLSM in one sentence?", "back": "Right-size each subnet with different masks (/30 for point-to-point, larger for VLANs) instead of one mask everywhere."},
{"front": "SNMP vs NetFlow?", "back": "SNMP polls device state (up/down, counters); NetFlow/sFlow samples traffic flows. State vs traffic."},
]

NET_QUIZ = [
{"q": "192.168.20.64/27 — usable range?",
 "choices": [".65–.94", ".64–.95", ".65–.93", ".66–.94"], "answer": 0,
 "explain": "/27: 32 addresses, .64–.95; network .64, broadcast .95; usable .65–.94. Covered in the Hands-on procedure section."},
{"q": "Summarize 10.1.0.0/24 through 10.1.3.0/24.",
 "choices": ["10.1.0.0/23", "10.1.0.0/22", "10.0.0.0/16", "10.1.0.0/24"], "answer": 1,
 "explain": "Four contiguous /24s = /22 (22 network bits). Covered in the Hands-on procedure section."},
{"q": "A switch port in STP 'blocking' state means ___.",
 "choices": ["port failure", "loop prevention — not forwarding, listening", "VLAN mismatch", "duplex mismatch"], "answer": 1,
 "explain": "Blocking prevents loops; the port listens but doesn't forward user traffic. Covered in the Concepts section."},
{"q": "WPA3's key improvement over WPA2?",
 "choices": ["faster speed", "SAE handshake — resists offline dictionary attacks", "longer range", "more SSIDs"], "answer": 1,
 "explain": "Simultaneous Authentication of Equals replaces the crackable WPA2 4-way handshake. Covered in the Concepts section."},
{"q": "In a capture, many TCP retransmissions indicate ___.",
 "choices": ["normal operation", "packet loss or congestion", "encryption", "VLAN tagging"], "answer": 1,
 "explain": "Retransmissions = segments not acknowledged — loss, congestion, or a dead peer. Covered in the Concepts section."},
{"q": "First step when 'the network is down'?",
 "choices": ["reboot the router", "identify the problem: scope (one host? one VLAN? everyone?)", "replace cables", "call the ISP"], "answer": 1,
 "explain": "Scope first — one host is a local issue; everyone is infrastructure. Methodology before tools. Covered in the Concepts section."},
{"q": "You see the address fe80::1 on an interface. What kind of address is it?",
 "choices": ["global unicast", "link-local (fe80::/10)", "multicast", "loopback"], "answer": 1,
 "explain": "fe80::/10 is link-local — valid only on the local link, never routed. Covered in the Concepts section."},
{"q": "A load balancer spreads web traffic across four servers. Which algorithms does the module name?",
 "choices": ["round-robin and least-connections", "shortest-path and widest-path", "Dijkstra and Bellman-Ford", "LSDOU and AGDLP"], "answer": 0,
 "explain": "Load balancers distribute by algorithm — round-robin and least-connections are the named examples. Covered in the Concepts section."},
]

# ---------------------------------------------------------------- module 4
RHCE_SUMMARY = (
"Welcome to Module 4 of IL-04 — Systems, Linux, Windows & Networks. I'm your instructor, and this "
"final module is where administration becomes engineering: Red Hat Certified Engineer EX294, Ansible "
"automation on RHEL. This module assumes you can already administer the systems you're automating — "
"a current RHCSA is required, because the exam tests *how* you automate what you already know how to "
"configure by hand. We build the discipline from the ground up: inventory and patterns, playbooks and "
"plays, variables and facts, idempotence as the definition of correct automation — then roles and "
"Galaxy, the RHEL system roles, automation controller concepts, and timed performance scenarios under "
"the clock. If your playbook runs twice with zero changes the second time, you are thinking like an "
"automation engineer."
)

RHCE_NOTES = [
{
"title": "Concepts",
"body": (
"- **inventory** — the list of managed hosts: INI or YAML, organized into groups; the exam starts "
"here, so a wrong inventory fails everything downstream.\n"
"- **patterns** — host selection expressions: webservers:&staging intersects, webservers:!staging "
"excludes, --limit narrows a run to one host for iteration.\n"
"- **playbook / play / task / module** — a playbook is a YAML list of plays; a play maps tasks onto "
"hosts; a task calls a module. Ad-hoc first (ansible web -m ping) to prove the concept, then write "
"the playbook.\n"
"- **variables and facts** — variables parameterize playbooks (extra vars with -e win every precedence "
"fight); ansible_facts (e.g. ansible_facts['os_family']) describe the target for when: conditionals — "
"one playbook, many distributions.\n"
"- **Jinja2** — the templating language inside playbooks: when: already evaluates Jinja2, so never "
"double-wrap {{ }} inside a when: clause.\n"
"- **idempotence** — running twice changes nothing the second time: the *definition* of correct "
"automation. Every task must be safe to re-run — state: present, never shell commands that append "
"blindly.\n"
"- **handlers** — tasks that run once at the end of a play, only when notified by a changed task "
"(notify: restart nginx): restart the service only when the config changed.\n"
"- **ansible-vault** — encrypts secrets at rest in the repo; decrypt at runtime with --ask-vault-pass "
"or a vault password file. Never commit plaintext credentials.\n"
"- **roles** — reusable automation units with a conventional layout (tasks/main.yml, handlers/main.yml, "
"templates/, defaults/main.yml): learn the layout once, reuse forever.\n"
"- **Galaxy** — the community sharing hub for roles: vet what you download.\n"
"- **RHEL system roles** — Red Hat's supported roles (timesync, selinux, firewall, storage, network): "
"idempotent and tested — prefer them over hand-rolled or random Galaxy roles on the exam.\n"
"- **automation controller** — the enterprise scheduling and access layer over Ansible: know at concept "
"level what a job template bundles (project + inventory + credentials + playbook), plus workflows and "
"RBAC.\n"
"- **become** — privilege escalation done right: become: true on the play or task that needs root on "
"the remotes.\n"
"- **EX294** — the RHCE performance exam: real RHEL systems and a clock, configured with Ansible to a "
"specification. YAML indentation, Jinja2 quoting in when:, and a forgotten become: true are the "
"common traps; --check --diff is the pre-flight for every run."
)
},
{
"title": "Hands-on procedure",
"body": (
"Build the idempotent web tier from the module lab, then prove idempotence — the proof is the grade.\n\n"
"1. Write the inventory first: a [web] group with your lab hosts. Run ansible web -m ping and confirm "
"every host answers before writing a single task.\n"
"2. Skeleton the playbook before filling tasks: play name, hosts: web, become: true, empty tasks and "
"handlers blocks, variable file if you need one. Structure first, logic second — this is the exam "
"time-saver.\n"
"3. Add the package task with ansible.builtin.dnf: name=nginx, state=present. Declarative state, not "
"shell commands.\n"
"4. Add the config task with ansible.builtin.template: src=index.html.j2, dest with mode '0644', and "
"notify: restart nginx — the handler fires only when the template actually changes.\n"
"5. Add the firewall task with ansible.posix.firewalld: service=http, permanent=true, immediate=true, "
"state=enabled. Services, not raw ports — same discipline as Module 1.\n"
"6. Add the service task with ansible.builtin.service: name=nginx, state=started, enabled=true.\n"
"7. Pre-flight: ansible-playbook web.yml --check --diff --limit web1 — the dry run shows what WOULD "
"change, on one host.\n"
"8. Run for real: ansible-playbook web.yml. Then run it again immediately: the second run must report "
"0 changed. Zero changes on re-run is idempotence proven — that is the verdict you want.\n"
"9. Break it on purpose: change one line in the template, re-run, and confirm the handler fires exactly "
"once and only the config task reports changed."
),
"code": (
"---\n"
"- name: web tier\n"
"  hosts: web\n"
"  become: true\n"
"  tasks:\n"
"    - name: nginx installed\n"
"      ansible.builtin.dnf:\n"
"        name: nginx\n"
"        state: present\n"
"    - name: index deployed\n"
"      ansible.builtin.template:\n"
"        src: index.html.j2\n"
"        dest: /usr/share/nginx/html/index.html\n"
"        mode: '0644'\n"
"      notify: restart nginx\n"
"    - name: http allowed\n"
"      ansible.posix.firewalld:\n"
"        service: http\n"
"        permanent: true\n"
"        immediate: true\n"
"        state: enabled\n"
"    - name: nginx running\n"
"      ansible.builtin.service:\n"
"        name: nginx\n"
"        state: started\n"
"        enabled: true\n"
"  handlers:\n"
"    - name: restart nginx\n"
"      ansible.builtin.service:\n"
"        name: nginx\n"
"        state: restarted\n"
"# prove it:\n"
"ansible-playbook web.yml --check --diff --limit web1\n"
"ansible-playbook web.yml && ansible-playbook web.yml  # second run: 0 changed"
),
"lang": "yaml"
},
{
"title": "Project brief",
"body": (
"Your applied capstone for this module: a timed, multi-system automation engagement — the closest "
"rehearsal to EX294 short of the exam itself.\n\n"
"The scenario. A company has four RHEL systems fresh off the Module 1 build procedure and a "
"specification document: two web servers behind one load-balancer config, one database server with a "
"tuned config, and one monitoring host collecting logs — all to be brought to spec with Ansible, "
"nothing by hand.\n\n"
"Your deliverables:\n"
"- The inventory with groups (web, db, monitor) and group variables; ad-hoc proof (ansible all -m "
"ping) captured before any playbook ran.\n"
"- One playbook per tier, each starting from the skeleton-first pattern, using become: true where "
"privilege is needed, handlers for every service restart, and when: conditionals on ansible_facts "
"where the tiers diverge.\n"
"- At least one RHEL system role used where it fits (timesync across all four hosts is the natural "
"one) instead of a hand-rolled equivalent — with the written reason.\n"
"- Secrets handled with ansible-vault (the database password), with the vault password file outside "
"the repo and the encryption proven by showing the ciphertext in version control.\n"
"- The idempotence proof: two consecutive full runs with the second reporting 0 changed, plus the "
"--check --diff pre-flight output for the final run.\n"
"- A time-boxed run log: you get one 90-minute window to go from empty repo to green second run — "
"log start/end times and where the minutes went, because the exam is a workday compressed.\n\n"
"Stretch: convert the most-reused tier into a proper role (tasks/handlers/templates/defaults layout) "
"and consume it from a thin wrapper playbook."
)
},
{
"title": "Noah check-in",
"body": (
"Noah probes mastery with questions like:\n"
"- Noah shows you a task using shell: echo x >> /etc/motd. Rule it idempotent or not, and rewrite it "
"the idempotent way.\n"
"- Your playbook ran green but a re-run reports changes every time. Noah asks: what class of bug is "
"this, and what is the first thing you check?\n"
"- *Timed:* Noah hands you a three-host spec and starts a 20-minute clock. Narrate your skeleton-first "
"order of operations before you touch the keyboard.\n\n"
"Honesty note: all labs, scenarios, and questions in this module are original practice material — never "
"recalled exam content. EX294 objectives and the required RHCSA version change: confirm the current "
"spec on redhat.com before booking. Preparation only: this course confers no certificate and is not "
"affiliated with Red Hat."
)
}
]

RHCE_ADD_CARDS = [
{"front": "ansible_facts['os_family'] is used for?", "back": "Conditionals (when:) — one playbook behaving correctly across distributions."},
{"front": "A job template bundles what?", "back": "Project + inventory + credentials + playbook — the executable unit in automation controller."},
]

RHCE_QUIZ = [
{"q": "A task using shell: echo x >> /etc/motd is ___.",
 "choices": ["idempotent", "not idempotent — appends on every run", "fine", "deprecated"], "answer": 1,
 "explain": ">> appends every run — use copy/template with content: for idempotence. Covered in the Concepts section."},
{"q": "Restart nginx only when its config changed: mechanism?",
 "choices": ["always restart", "handlers + notify", "cron", "ignore"], "answer": 1,
 "explain": "notify: restart nginx on the config task; the handler runs once, only on change. Covered in the Concepts section."},
{"q": "Target webservers except staging: pattern?",
 "choices": ["webservers:!staging", "all", "webservers,staging", "*.staging"], "answer": 0,
 "explain": "! excludes — webservers:&staging would intersect instead. Covered in the Concepts section."},
{"q": "Secrets in a playbook: correct handling?",
 "choices": ["plaintext vars", "ansible-vault encrypt", "base64 in git", "environment hope"], "answer": 1,
 "explain": "ansible-vault encrypts at rest; decrypt at runtime with --ask-vault-pass or a vault password file. Covered in the Concepts section."},
{"q": "Task needs root on remotes: add?",
 "choices": ["sudo: yes", "become: true", "root: true", "admin: yes"], "answer": 1,
 "explain": "become: true (privilege escalation) — the modern, correct directive. Covered in the Concepts section."},
{"q": "Playbook ran green but changed nothing on re-run: verdict?",
 "choices": ["broken", "correctly idempotent", "needs --force", "unfinished"], "answer": 1,
 "explain": "Zero changes on re-run is the goal — that's idempotence proven. Covered in the Noah check-in section."},
{"q": "Your when: clause is when: \"{{ ansible_facts['os_family'] == 'RedHat' }}\". What happens?",
 "choices": ["works fine", "breaks — when: already evaluates Jinja2, never double-wrap {{ }}", "only fails on Tuesdays", "needs become: true"], "answer": 1,
 "explain": "when: evaluates Jinja2 natively; wrapping in {{ }} is the classic trap. Covered in the Concepts section."},
{"q": "You want to iterate a playbook against one host before the fleet. Flag?",
 "choices": ["--all", "--limit web1", "--force", "--fast"], "answer": 1,
 "explain": "--limit narrows the run to one host; combine with --check --diff for the pre-flight. Covered in the Hands-on procedure section."},
]

# ---------------------------------------------------------------- transforms
MODULE_DATA = {
    'il04-linux':     {'summary': LINUX_SUMMARY,   'weight': 3, 'notes': LINUX_NOTES,   'add_cards': LINUX_ADD_CARDS,   'quiz': LINUX_QUIZ},
    'il04-windows':   {'summary': WINDOWS_SUMMARY, 'weight': 2, 'notes': WINDOWS_NOTES, 'add_cards': WINDOWS_ADD_CARDS, 'quiz': WINDOWS_QUIZ},
    'il04-networking':{'summary': NET_SUMMARY,     'weight': 2, 'notes': NET_NOTES,     'add_cards': NET_ADD_CARDS,     'quiz': NET_QUIZ},
    'il04-rhce':      {'summary': RHCE_SUMMARY,    'weight': 1, 'notes': RHCE_NOTES,    'add_cards': RHCE_ADD_CARDS,    'quiz': RHCE_QUIZ},
}

COMPETITORS = ['aleks', 'brilliant', 'khan academy', 'coursera', 'udemy', 'edx']

for m in course['modules']:
    t = MODULE_DATA[m['id']]
    m['summary'] = t['summary']
    m['weight'] = t['weight']
    m['notes'] = t['notes']
    m['cards'] = m.get('cards', []) + t['add_cards']
    m['quiz'] = t['quiz']
    # sanity per module
    assert len(m['notes']) == 4, m['id']
    assert [n['title'] for n in m['notes']] == ['Concepts', 'Hands-on procedure', 'Project brief', 'Noah check-in'], m['id']
    assert len(m['cards']) >= 6 and len(m['quiz']) >= 6, m['id']
    for q in m['quiz']:
        assert len(q['choices']) == 4 and isinstance(q['answer'], int) and 0 <= q['answer'] < 4, q['q']
        assert q['explain'].strip(), q['q']
    blob = json.dumps(m).lower()
    for c in COMPETITORS:
        assert c not in blob, (m['id'], c)
    assert 'palantir' not in blob and 'nsa' not in blob.lower().replace('dns', ''), m['id']

# course-level: nothing to add — all keys present; keep updatedAt
course['updatedAt'] = '2026-10-07'

blob = json.dumps(course).lower()
for c in COMPETITORS:
    assert c not in blob, ('course', c)
assert 'palantir' not in blob, 'course palantir'

# atomic write + validate
TMP = SRC + '.retrofit-tmp'
with open(TMP, 'w') as f:
    json.dump(course, f, ensure_ascii=False, indent=1)
reloaded = json.load(open(TMP))  # validate AFTER
assert len(reloaded['modules']) == 4
os.replace(TMP, SRC)
print('OK: wrote', SRC)
print('modules:', [(m['id'], m['weight'], len(m['notes']), len(m['cards']), len(m['quiz'])) for m in reloaded['modules']])
print('course keys:', list(reloaded.keys()))
