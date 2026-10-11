#!/usr/bin/env python3
"""IL-27 clickSims, trainers, mockTasks, animations."""
import json

CK = []
def clicksim(id, moduleId, tool, title, steps):
    CK.append({"id": id, "moduleId": moduleId, "tool": tool, "title": title,
               "steps": [{"screen": s, "instruction": i, "hotspots": h, "feedback": f}
                         for s, i, h, f in steps]})

clicksim("IL27-CLICK-01", "IL27-M03", "Active Directory Users and Computers", "Create an AD user in ADUC",
    [("ADUC open, connected to lab.local; OU=Users selected in the left tree.",
      "Right-click OU=Users > New > User.",
      ["OU=Users", "New", "User"],
      "New Object - User dialog opens."),
     ("New Object - User dialog: name fields empty.",
      "Fill First name 'Test', Last name 'User', User logon name 'tuser' (pre-Windows 2000 name auto-fills as TUSER). Click Next.",
      ["First name field", "User logon name field", "Next"],
      "Password screen appears."),
     ("Password screen: fields empty.",
      "Type the temporary password twice, CHECK 'User must change password at next logon', UNCHECK 'Password never expires'. Click Next.",
      ["Password fields", "'User must change password at next logon'", "Next"],
      "Summary screen shows the new account details."),
     ("Summary screen: CN=Test User, OU=Users,DC=lab,DC=local.",
      "Click Finish.",
      ["Finish"],
      "Test User appears in the OU=Users results pane.")])

clicksim("IL27-CLICK-02", "IL27-M04", "Group Policy Management Console", "Create and link a GPO",
    [("GPMC open; forest lab.local expanded; Group Policy Objects container visible.",
      "Right-click 'Group Policy Objects' > New. Name it 'LAB-Screen-Lock-15min'. Click OK.",
      ["Group Policy Objects", "New", "Name field", "OK"],
      "The new GPO appears in the list, unlinked (no links yet)."),
     ("The new GPO is selected; right pane shows Scope/S ettings tabs.",
      "Right-click the GPO > Edit. This opens the Group Policy Management Editor.",
      ["Edit"],
      "Editor opens with Computer Configuration and User Configuration trees."),
     ("Editor: User Configuration tree visible.",
      "Navigate User Configuration > Policies > Administrative Templates > Control Panel > Personalization. Double-click 'Screen saver timeout'.",
      ["User Configuration", "Administrative Templates", "Personalization", "Screen saver timeout"],
      "The policy setting dialog opens."),
     ("Setting dialog: 'Not Configured' selected.",
      "Select Enabled, set seconds to 900. Click OK. Then enable 'Password protect the screen saver' the same way.",
      ["Enabled", "seconds field (900)", "OK"],
      "Both settings show as Enabled in the editor."),
     ("Back in GPMC, GPO still unlinked.",
      "Drag the GPO onto OU=Workstations (or right-click OU=Workstations > Link an Existing GPO and select it).",
      ["OU=Workstations", "Link an Existing GPO"],
      "The GPO appears under OU=Workstations with Link Enabled = Yes."),
     ("Linked GPO selected; right pane Scope tab.",
      "Confirm: Links show OU=Workstations; Security Filtering shows Authenticated Users. Close GPMC.",
      ["Scope tab", "Links", "Security Filtering"],
      "GPO is linked, filtered, and ready — verify on a client with gpresult /r.")])

clicksim("IL27-CLICK-03", "IL27-M07", "Hyper-V Manager", "Create a Hyper-V virtual machine",
    [("Hyper-V Manager open, host selected in the left pane.",
      "In the Actions pane click New > Virtual Machine. The wizard opens.",
      ["Actions pane", "New", "Virtual Machine"],
      "Before You Begin page of the New Virtual Machine Wizard."),
     ("Specify Name and Location page.",
      "Name it 'LAB-FS01'. Keep the default location (or tick 'Store the virtual machine in a different location' for your lab drive). Click Next.",
      ["Name field", "Next"],
      "Specify Generation page appears."),
     ("Specify Generation page: Generation 1 / Generation 2.",
      "Select Generation 2 (UEFI, modern OS). Click Next.",
      ["Generation 2", "Next"],
      "Assign Memory page appears."),
     ("Assign Memory: Startup memory 2048 MB; 'Use Dynamic Memory' ticked.",
      "Set 4096 MB for a server VM. Click Next.",
      ["Startup memory field", "Next"],
      "Configure Networking page appears."),
     ("Configure Networking: Connection dropdown lists your virtual switches.",
      "Select 'Lab-Internal'. Click Next.",
      ["Connection dropdown", "Lab-Internal", "Next"],
      "Connect Virtual Hard Disk page appears."),
     ("Connect Virtual Hard Disk: 'Create a virtual hard disk' selected, 127 GB default.",
      "Set 100 GB (dynamic is fine for lab). Click Next, then on the Installation Options page choose 'Install an operating system from a bootable image file' and browse to your Server 2025 ISO. Click Finish.",
      ["Size field", "bootable image file", "ISO browse", "Finish"],
      "LAB-FS01 appears in the Virtual Machines list, State: Off — ready to start and install.")])

clicksim("IL27-CLICK-04", "IL27-M05", "DHCP Console", "Configure a DHCP scope",
    [("DHCP console (dhcpmgmt.msc) open; server lab-dc01.lab.local expanded; IPv4 selected.",
      "Right-click IPv4 > New Scope. The New Scope Wizard opens.",
      ["IPv4", "New Scope"],
      "Welcome page of the New Scope Wizard."),
     ("Scope Name page: empty Name/Description.",
      "Name: 'Lab-Workstations', Description: 'DHCP for lab client VLAN'. Click Next.",
      ["Name field", "Next"],
      "IP Address Range page appears."),
     ("IP Address Range: Start/End IP, subnet mask fields.",
      "Start 192.168.10.100, End 192.168.10.200, Length 24 (mask auto-fills 255.255.255.0). Click Next.",
      ["Start IP", "End IP", "Next"],
      "Add Exclusions page appears."),
     ("Add Exclusions and Delay page.",
      "Exclude 192.168.10.150-192.168.10.160 (reserved for printers/static lab gear). Click Next.",
      ["Excluded address range", "Add", "Next"],
      "Lease Duration page appears (default 8 days)."),
     ("Lease Duration: 8 days default.",
      "Set 1 day (lab churn is high; short leases recycle faster). Click Next.",
      ["Days field (1)", "Next"],
      "Configure DHCP Options: Yes, I want to configure these options now."),
     ("Router (Default Gateway) option page.",
      "Enter 192.168.10.1, click Add. Next: DNS Servers — enter 192.168.20.10, Add. Next: WINS — skip (Next).",
      ["Router field", "Add", "DNS field", "Add"],
      "Activate Scope page: 'Yes, I want to activate this scope now'."),
     ("Activate Scope page.",
      "Keep Yes selected, click Finish.",
      ["Finish"],
      "Scope 'Lab-Workstations' appears under IPv4 with a green up-arrow — active and leasing.")])

clicksim("IL27-CLICK-05", "IL27-M11", "Zabbix Frontend", "Add a host in Zabbix",
    [("Zabbix UI: logged in as Admin; left menu visible.",
      "Go to Data collection > Hosts. Click 'Create host' (top right).",
      ["Data collection", "Hosts", "Create host"],
      "New host form opens."),
     ("Host tab: Host name, Templates, Host groups empty.",
      "Host name: 'LAB-DC01'. Click Select next to Templates, choose 'Windows by Zabbix agent'. Host groups: select 'Windows servers'.",
      ["Host name field", "Select (Templates)", "Windows by Zabbix agent"],
      "Template and group attached."),
     ("Still on Host tab: Interfaces section shows 'No interfaces'.",
      "Click Add > Agent. Enter IP 192.168.20.10, port 10050. Click Add.",
      ["Add", "Agent", "IP field", "Port"],
      "An Agent interface row appears with the IP."),
     ("Top of the form: 'Enabled' toggle.",
      "Confirm Enabled is on. Click Add (bottom) to save the host.",
      ["Add (save)"],
      "Host list shows LAB-DC01. The ZBX icon is grey — agent not yet reporting."),
     ("Hosts list: LAB-DC01 row visible.",
      "Wait ~2 minutes, then refresh. The ZBX icon turns green.",
      ["refresh", "ZBX icon"],
      "Green ZBX = Zabbix is collecting. Open Monitoring > Latest data, filter host LAB-DC01 — metrics are flowing.")])

TR = []
def trainer(id, moduleId, title, kind, description, items):
    TR.append({"id": id, "moduleId": moduleId, "title": title, "kind": kind,
               "description": description, "items": items})

trainer("IL27-TRAIN-01", "IL27-M05", "Subnetting trainer", "rapid-fire",
    "Timed rapid-fire subnetting: network/broadcast addresses, host counts, CIDR conversions. Infinite practice via parameterized templates.",
    [
        {"q": "How many usable host addresses in a /26?", "answer": "62", "explanation": "2^(32-26) - 2 = 64 - 2 = 62."},
        {"q": "Network address of 192.168.10.77/27?", "answer": "192.168.10.64", "explanation": "/27 blocks of 32: 77 falls in 64-95, network is .64."},
        {"q": "Broadcast address of 10.4.0.200/22?", "answer": "10.4.3.255", "explanation": "/22 = block of 4 in third octet: 0-3, broadcast is last address 10.4.3.255."},
        {"q": "CIDR for mask 255.255.255.240?", "answer": "/28", "explanation": "240 = 11110000, 24 + 4 = /28."},
        {"q": "Broadcast address of 172.16.4.0/23?", "answer": "172.16.5.255", "explanation": "/23 spans two /24s: 172.16.4.0 through 172.16.5.255; broadcast is the last address."},
        {"q": "Smallest subnet fitting 40 hosts?", "answer": "/26", "explanation": "/26 gives 62 usable; /27 gives only 30. Always round UP."},
        {"q": "How many /26 subnets fit in a /24?", "answer": "4", "explanation": "2^(26-24) = 4."},
        {"q": "First usable host of 192.168.99.128/25?", "answer": "192.168.99.129", "explanation": "Network .128, first usable .129."},
    ])

trainer("IL27-TRAIN-02", "IL27-M10", "PowerShell cmdlet trainer", "rapid-fire",
    "Match the task to the cmdlet — the 40 cmdlets an infrastructure specialist types weekly. Infinite practice via templates.",
    [
        {"q": "Create a new AD user account", "choices": ["New-ADUser", "Add-ADUser", "Set-ADUser", "Install-ADUser"], "answer": "New-ADUser", "explanation": "New-* creates; Set-* modifies; Add-* adds to collections."},
        {"q": "Test whether TCP port 443 is open on a host", "choices": ["Test-NetConnection", "Test-Connection", "Invoke-WebRequest", "Get-NetTCPConnection"], "answer": "Test-NetConnection", "explanation": "Test-NetConnection -Port does TCP port tests; Test-Connection is ICMP-only."},
        {"q": "List the last 24h of failed logons (event 4625)", "choices": ["Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625}", "Get-EventLog Security | Where Id -eq 4625", "Get-WinEvent -LogName Security -MaxEvents 10", "wevtutil qe Security"], "answer": "Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625}", "explanation": "FilterHashtable filters server-side — fastest and the modern cmdlet."},
        {"q": "Restart the Print Spooler service", "choices": ["Restart-Service Spooler", "Start-Service Spooler -Force", "Set-Service Spooler -Status Running", "sc.exe start Spooler"], "answer": "Restart-Service Spooler", "explanation": "Restart-Service handles stop+start; Start-Service fails if already running."},
        {"q": "Find which process is listening on port 53", "choices": ["Get-NetTCPConnection -LocalPort 53", "netstat -ano | findstr :53 then tasklist", "Get-Process -Port 53", "ss -tlnp (Linux only)"], "answer": "Get-NetTCPConnection -LocalPort 53", "explanation": "Native PowerShell object output with OwningProcess — pipe to Get-Process."},
        {"q": "Export AD users to CSV without type junk on line 1", "choices": ["Export-Csv -NoTypeInformation", "Export-Csv -NoHeader", "ConvertTo-Csv | Out-File", "Export-Clixml"], "answer": "Export-Csv -NoTypeInformation", "explanation": "-NoTypeInformation drops the #TYPE header line."},
        {"q": "Show disk usage per drive with % free", "choices": ["Get-PSDrive", "Get-Disk", "Get-Volume", "Get-Partition"], "answer": "Get-PSDrive", "explanation": "Get-PSDrive shows Used/Free per filesystem drive in one view."},
        {"q": "Run a command on 10 servers at once", "choices": ["Invoke-Command -ComputerName $s -ScriptBlock {}", "Enter-PSSession in a loop", "psexec @file", "Start-Job per server"], "answer": "Invoke-Command -ComputerName $s -ScriptBlock {}", "explanation": "Invoke-Command fans out in parallel over WinRM — the admin's force multiplier."},
    ])

trainer("IL27-TRAIN-03", "IL27-M05", "Port & protocol trainer", "rapid-fire",
    "Name the port, name the service — the ports that appear in firewall rules, incident tickets, and interviews. Infinite practice via templates.",
    [
        {"q": "Port 53", "answer": "DNS", "explanation": "UDP 53 (queries) + TCP 53 (zone transfers, large responses)."},
        {"q": "Port 88", "answer": "Kerberos", "explanation": "AD authentication. If 88 is blocked, domain logons fail."},
        {"q": "Port 389", "answer": "LDAP", "explanation": "AD directory queries; 636 = LDAPS."},
        {"q": "Port 445", "answer": "SMB", "explanation": "File shares, Group Policy, AD replication. Prime ransomware lateral-movement port."},
        {"q": "Port 3389", "answer": "RDP", "explanation": "Remote Desktop. Never expose to the internet unprotected."},
        {"q": "Port 22", "answer": "SSH", "explanation": "Linux remote admin; key auth, not passwords."},
        {"q": "Ports 80 / 443", "answer": "HTTP / HTTPS", "explanation": "Web traffic; 443 is TLS-encrypted."},
        {"q": "Port 25 / 587", "answer": "SMTP / SMTP submission", "explanation": "Mail routing (25) vs authenticated client submission (587)."},
        {"q": "Port 67 / 68", "answer": "DHCP", "explanation": "67 server, 68 client — UDP."},
        {"q": "Port 161", "answer": "SNMP", "explanation": "Monitoring queries (what Zabbix uses for network gear)."},
        {"q": "Port 10050 / 10051", "answer": "Zabbix agent / Zabbix server", "explanation": "10050 agent listener, 10051 server/trapper."},
        {"q": "Port 5985 / 5986", "answer": "WinRM HTTP / HTTPS", "explanation": "PowerShell remoting. 5986 is the encrypted one."},
    ])

MK = []
def mocktask(id, moduleId, title, kind, brief, scenario, deliverable, rubric):
    MK.append({"id": id, "moduleId": moduleId, "title": title, "kind": kind, "brief": brief,
               "scenario": scenario, "deliverable": deliverable, "rubric": rubric})

mocktask("IL27-MOCK-01", "IL27-M15", "Write an incident report", "writing",
    "Turn the ransomware drill (IL27-TL-12) into a one-page incident report a manager and an auditor can both use.",
    "At 2:14 PM Zabbix alerted on mass file renames on LAB-W11-01. You isolated the host at 2:16, preserved a snapshot, found a phishing macro as patient zero plus a scheduled-task persistence mechanism, eradicated both, and restored the user's files from the 2 AM backup by 5 PM.",
    "A one-page incident report (PDF or Markdown) with: executive summary (3 lines), timeline table (time/action/actor), root cause, impact, containment + eradication + recovery actions, and two preventive controls with owners.",
    ["Timeline is complete and timestamps are consistent", "Root cause names the actual vector (phishing macro), not 'malware'", "Recovery point (2 AM backup) and data-loss window stated", "Preventive controls are specific and owned (not 'be more careful')", "Tone is factual, no blame, no jargon without explanation"])

mocktask("IL27-MOCK-02", "IL27-M16", "Draft a change request", "writing",
    "Write the change request you'd file BEFORE aligning the VPN crypto proposals (IL27-BRANCH-04) — because in production, you don't touch crypto without paper.",
    "The branch-office VPN tunnel is down after their firmware update changed phase-2 defaults. You plan to align proposals to AES-256/GCM + SHA256 + DH14 on both firewalls during tonight's 10 PM-11 PM window.",
    "A change request with: summary, business justification, scope (exact devices + settings), risk assessment, backout plan (config backup restore, tested), test plan (tunnel up + branch traffic matrix), and approver sign-off line.",
    ["Backout plan is concrete and tested (config backup exists)", "Risk assessment names the real risks (extended outage, crypto mismatch)", "Test plan verifies business traffic, not just 'tunnel up'", "Maintenance window and rollback timebox stated", "Approver and implementer are different people (separation of duties)"])

mocktask("IL27-MOCK-03", "IL27-M06", "Build a network diagram from a description", "diagram",
    "Convert a written description into a clean network diagram — the skill every infrastructure interview tests.",
    "The lab has: an ISP handoff into pfSense WAN; pfSense LAN 192.168.10.1/24 with 3 workstations and a printer; pfSense OPT1 (DMZ) 192.168.20.1/24 with LAB-DC01 (192.168.20.10, AD/DNS/DHCP) and LAB-FS01 (192.168.20.11, files); lab-linux01 (192.168.10.20) running Zabbix + Docker. Firewall rules: LAN->DMZ limited to DNS/AD/SMB; DMZ->LAN deny by default; DMZ->WAN allowed for updates.",
    "A network diagram (any tool: draw.io, Excalidraw, even neat ASCII) showing: all segments with CIDRs, every host with IP + role, firewall rule summaries on the inter-segment arrows, and a legend.",
    ["Every IP from the description appears and matches", "Segments are visually separated with CIDR labels", "Firewall rules annotated on the correct arrows", "Legend explains all symbols/colors", "A stranger could rebuild the addressing from the diagram alone"])

AN = []
def animation(id, moduleId, title, kind, description):
    AN.append({"id": id, "moduleId": moduleId, "title": title, "kind": kind, "description": description})

animation("IL27-ANIM-01", "IL27-M06", "Network topology builder", "canvas",
    "Interactive canvas: the learner drags device icons (firewall, switch, server, workstation, printer, cloud/ISP) onto a grid and draws links between them. Each placed device gets an editable property panel (hostname, IP/CIDR, role). A 'validate' button checks the topology against the IL-27 lab spec (pfSense with WAN/LAN/DMZ, DC + file server on DMZ, workstations on LAN) and highlights mismatches. Animated packet dots flow along links when 'simulate traffic' is pressed, turning red when a link crosses a firewall rule that would deny it. Export produces the addressing table used by later labs.")

animation("IL27-ANIM-02", "IL27-M03", "AD forest / domain tree", "svg",
    "Animated SVG of the lab.local domain: the domain root node expands into the five OUs (Workstations, Servers, Users, Groups, ServiceAccounts), each OU expanding to show its member objects (users, computers, groups) with distinct icons. Clicking any object shows its key attributes (DN, SID, memberOf). A replication animation draws pulsing arrows between the DC node and a (future) second DC, with a toggle for 'what replicates' (schema, configuration, domain partitions). A time-slider shows the promotion sequence: standalone server -> AD DS installed -> forest created -> DNS integrated.")

animation("IL27-ANIM-03", "IL27-M06", "Zero Trust request flow", "svg",
    "Step-through SVG animation of a single access request under Zero Trust: (1) user/device on LAN requests the file share, (2) request hits the policy engine (identity check: who + device health + MFA), (3) explicit allow/deny decision rendered as a gate, (4) encrypted session to the resource, (5) continuous verification ticking in the background. Each step highlights with a caption explaining the principle ('never trust, always verify', 'least privilege', 'assume breach'). A toggle switches between 'flat network' (request walks straight through, red flags) and 'segmented' (request passes the gate, green) to show why the IL-27 lab segments LAN/DMZ.")

animation("IL27-ANIM-04", "IL27-M05", "DHCP DORA sequence", "svg",
    "Animated sequence diagram of DHCP DORA: client broadcasts DISCOVER (packet expands to the broadcast domain), server responds OFFER (unicast, with offered IP highlighted), client broadcasts REQUEST, server answers ACK. Each packet is drawn with its real fields (op, xid, yiaddr, options 51/54/3/6) and the learner can hover any field for a plain-English explanation. A 'lease timeline' bar below shows T1/T2 renewal and expiry; pressing 'renew' replays REQUEST/ACK. A fault-injection toggle ('rogue server') shows a second OFFER racing the legitimate one, teaching why DHCP snooping exists.")

animation("IL27-ANIM-05", "IL27-M05", "DNS resolution chain", "svg",
    "Full recursive-resolution walkthrough as an animated chain: stub resolver -> pfSense forwarder -> (root hints -> TLD -> authoritative) for an internet name, contrasted with the short path for lab.local (forwarder -> domain override -> LAB-DC01). Each hop lights up in order with the query/response packet contents shown; caching is visualized as a fading memory bar at each resolver ('TTL countdown'). The learner can type any name and watch the chain build; a toggle shows what breaks when the DC's DNS stops (lab.local goes dark while internet still resolves) — the exact IL27-BRANCH-02 incident, visualized.")

animation("IL27-ANIM-06", "IL27-M04", "GPO processing order", "svg",
    "LSDOU processing order animated: Local -> Site -> Domain -> OU, with each layer's policies stacking onto a sample setting (e.g. screen-saver timeout) and later layers visibly overriding earlier ones. Toggles for 'Block Inheritance' (red X cuts the chain at that OU) and 'Enforced' (policy punches through the block, highlighted). A conflict demo sets the same setting at Domain and OU levels with different values and shows the winner plus WHY. Links to the learner's own lab: they can input their three IL27-TL-05 GPOs and watch them apply to a test computer object moving between OUs.")

animation("IL27-ANIM-07", "IL27-M12", "Backup rotation scheme", "canvas",
    "Interactive Grandfather-Father-Son rotation visualizer on a calendar canvas: daily incrementals (sons), weekly fulls (fathers), monthly fulls (grandfathers), with retention bars showing how far back each tier reaches. The learner drags the 'today' marker and the diagram highlights exactly which backup sets would restore any given date, computing the RPO. A 'disk cost' meter totals the storage consumed by the scheme vs a naive daily-full scheme. A disaster button ('file server dies on the 17th') walks the restore: pick the recovery point, list the sets needed (last full + incrementals since), and flag the data-loss window.")

animation("IL27-ANIM-08", "IL27-M15", "Incident response lifecycle", "svg",
    "The six-phase IR lifecycle (Preparation -> Detection & Analysis -> Containment -> Eradication -> Recovery -> Lessons Learned) as a circular animated diagram. Clicking a phase expands it with the IL-27 lab's concrete actions (e.g. Containment: 'disable NIC at hypervisor'; Lessons Learned: 'write the report, add the AppLocker rule'). An animated scenario dot travels the circle using the ransomware drill timeline (2:14 PM detection -> 5 PM recovery), pausing at each phase with the actual action taken. A 'what if you skip' toggle removes a phase and shows the consequence cascade (skip Eradication -> reinfection animation). Printable as the one-page IR playbook for the interview.")

with open("/home/hatch/workspace/apex-audit/docs/university/data/courses/_il27-build/frag_click_train_mock_anim.json", "w") as f:
    json.dump({"clickSims": CK, "trainers": TR, "mockTasks": MK, "animations": AN}, f, indent=1)
print("clickSims:", len(CK), "trainers:", len(TR), "mockTasks:", len(MK), "animations:", len(AN))
