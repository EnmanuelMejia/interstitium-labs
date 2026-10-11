#!/usr/bin/env python3
"""IL-27 toolLabs (chained toward the capstone homelab) and scriptLabs."""
import json

TL = []
def toollab(id, title, chain, moduleId, requiresInstall, requiresLab, brief, steps, deliverable, checkpoint):
    TL.append({"id": id, "title": title, "chain": chain, "moduleId": moduleId,
               "requiresInstall": requiresInstall, "requiresLab": requiresLab, "brief": brief,
               "steps": steps, "deliverable": deliverable, "checkpoint": checkpoint})

toollab("IL27-TL-01", "Build the virtualization host and first VM", 1, "IL27-M07",
    ["IL27-INST-03"], None,
    "The chain starts here: pick one hypervisor (Hyper-V), create the Lab-Internal virtual switch, and boot a throwaway VM to prove the platform. Every later lab builds on this host.",
    ["Enable Hyper-V per IL27-INST-03 and create the 'Lab-Internal' internal switch plus an External switch.",
     "Create a Gen 2 VM 'lab-template-test' (2 GB RAM, 40 GB dynamic disk) on Lab-Internal; attach the Ubuntu Server ISO and install with hostname lab-test.",
     "Snapshot the VM right after first boot ('clean-install') — snapshots are your undo button for the whole course.",
     "Assign a static IP 192.168.56.50/24 on Lab-Internal and confirm the host can ping it.",
     "Delete nothing yet: keep this VM as your sandbox for risky commands in later modules."],
    "Running 'lab-test' VM on Lab-Internal with a clean-install snapshot and static IP 192.168.56.50",
    "Hyper-V Manager shows lab-test Running; Test-Connection 192.168.56.50 -Count 2 -Quiet returns True; Get-VMSnapshot -VMName lab-test lists 'clean-install'.")

toollab("IL27-TL-02", "Install Windows Server 2025 and configure core networking", 2, "IL27-M02",
    ["IL27-INST-01"], "IL27-TL-01",
    "Stand up the future domain controller: Windows Server 2025 Eval with Desktop Experience, static IP, correct hostname, and Remote Desktop enabled for admin access.",
    ["Create the Server VM per IL27-INST-01 (4 vCPU, 8 GB RAM, 100 GB disk, NIC on Lab-Internal) and complete setup; name it LAB-DC01 during install.",
     "Set a static IP: New-NetIPAddress -InterfaceAlias 'Ethernet' -IPAddress 192.168.56.10 -PrefixLength 24 -DefaultGateway 192.168.56.1; Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses 127.0.0.1 (loopback until DNS role exists).",
     "Rename if needed: Rename-Computer -NewName 'LAB-DC01' -Restart.",
     "Enable RDP: Set-ItemProperty 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server' -Name fDenyTSConnections -Value 0; Enable-NetFirewallRule -DisplayGroup 'Remote Desktop'.",
     "Take a snapshot named 'pre-dc-promo'. Install all Windows updates (sconfig > option 6, or Settings > Windows Update) and reboot."],
    "LAB-DC01 at 192.168.56.10, RDP reachable, snapshot 'pre-dc-promo' taken",
    "From the host: mstsc /v:192.168.56.10 connects; on the VM, Get-NetIPAddress shows 192.168.56.10; Get-VMSnapshot lists 'pre-dc-promo'.")

toollab("IL27-TL-03", "Promote LAB-DC01 and build the OU structure", 3, "IL27-M03",
    ["IL27-INST-05", "IL27-INST-02"], "IL27-TL-02",
    "Turn LAB-DC01 into the lab.local domain controller and lay down the OU skeleton (Workstations, Servers, Users, Groups, ServiceAccounts) that Group Policy and every later lab will target.",
    ["On LAB-DC01 run Install-WindowsFeature AD-Domain-Services -IncludeManagementTools.",
     "Promote: Install-ADDSForest -DomainName 'lab.local' -DomainNetbiosName 'LAB' -InstallDns -Force (supply a DSRM password at the prompt); the server reboots.",
     "Log on as LAB\\Administrator. Create the OUs: 'Workstations','Servers','Users','Groups','ServiceAccounts' | ForEach-Object { New-ADOrganizationalUnit -Name $_ -Path 'DC=lab,DC=local' -ProtectedFromAccidentalDeletion $true }.",
     "Create a domain admin service account for labs: New-ADUser -Name 'svc-labadmin' -SamAccountName 'svc-labadmin' -Path 'OU=ServiceAccounts,DC=lab,DC=local' -AccountPassword (Read-Host -AsSecureString) -Enabled $true; Add-ADGroupMember 'Domain Admins' 'svc-labadmin'.",
     "From your workstation with RSAT: open dsa.msc, connect to lab.local, and confirm the full OU tree renders."],
    "lab.local domain live on LAB-DC01 with the five-OU skeleton and svc-labadmin in Domain Admins",
    "Get-ADDomain shows lab.local; Get-ADOrganizationalUnit -Filter * returns the 5 OUs; dcdiag /q is silent.")

toollab("IL27-TL-04", "DHCP and DNS services for the lab network", 4, "IL27-M05",
    ["IL27-INST-05"], "IL27-TL-03",
    "Give the lab real infrastructure services: a DHCP scope handing out Lab-Internal addresses and DNS zones (forward + reverse) so every name in the course resolves.",
    ["Install roles: Install-WindowsFeature DHCP, DNS -IncludeManagementTools. Authorize the DHCP server in AD: Add-DhcpServerInDC -DnsName lab-dc01.lab.local -IPAddress 192.168.56.10.",
     "Create the scope: Add-DhcpServerv4Scope -Name 'Lab-Internal' -StartRange 192.168.56.100 -EndRange 192.168.56.200 -SubnetMask 255.255.255.0; Set-DhcpServerv4OptionValue -ScopeId 192.168.56.0 -Router 192.168.56.1 -DnsServer 192.168.56.10 -DnsDomain 'lab.local'.",
     "Create the reverse zone: Add-DnsServerPrimaryZone -NetworkId '192.168.56.0/24' -ReplicationScope Domain; enable scavenging later in the hardening module.",
     "Add a host record for the future file server: Add-DnsServerResourceRecordA -Name 'lab-fs01' -ZoneName 'lab.local' -IPv4Address 192.168.56.11.",
     "Spin up the lab-test VM on Lab-Internal with DHCP and confirm it receives 192.168.56.100+, resolves lab-dc01.lab.local, and nslookup shows the reverse PTR."],
    "Working DHCP scope (100-200) + forward/reverse DNS zones on LAB-DC01; lab-test VM gets DHCP address and resolves names",
    "Get-DhcpServerv4Scope shows the scope Active; Resolve-DnsName lab-fs01.lab.local returns 192.168.56.11; on the client ipconfig /all shows DHCP-assigned address with DNS 192.168.56.10.")

toollab("IL27-TL-05", "Group Policy: baselines that actually enforce", 5, "IL27-M04",
    ["IL27-INST-02"], "IL27-TL-03",
    "Write three linked GPOs — password baseline, workstation lock screen, and mapped drives — link them to the right OUs, and prove enforcement with gpupdate + gpresult.",
    ["Open gpmc.msc on your workstation (RSAT). Create GPO 'LAB-Password-Baseline' linked to the domain root: Computer/ User Configuration > Policies > Windows Settings > Security Settings > Account Policies > Password Policy: minimum length 12, complexity enabled, max age 60 days.",
     "Create 'LAB-Workstation-Lock': User Configuration > Policies > Administrative Templates > Control Panel > Personalization > Screen saver timeout = 600 seconds, password-protect the screen saver = Enabled. Link to OU=Workstations.",
     "Create 'LAB-Mapped-Drives': User Configuration > Preferences > Windows Settings > Drive Maps > New Mapped Drive S: to \\\\lab-fs01\\shared (create action). Link to OU=Users.",
     "On a domain-joined test client: gpupdate /force, then gpresult /r /scope:user — all three GPOs must appear under 'Applied Group Policy Objects'.",
     "Negative test: move the test computer object OUT of OU=Workstations into the default Computers container, gpupdate, and confirm LAB-Workstation-Lock no longer applies — OU targeting proven."],
    "Three linked GPOs with proven apply/not-apply behavior via gpresult",
    "gpresult /r on the test client lists LAB-Password-Baseline, LAB-Workstation-Lock, LAB-Mapped-Drives as applied; after the OU move, the lock GPO drops off.")

toollab("IL27-TL-06", "pfSense: segmented network with firewall rules", 6, "IL27-M06",
    ["IL27-INST-07"], "IL27-TL-01",
    "Put pfSense at the center of the lab: WAN + LAN + a DMZ-style OPT1 segment, with rules that isolate servers from workstations — the Zero Trust segmentation story for the interview.",
    ["Build the pfSense VM per IL27-INST-07: WAN on External, LAN 192.168.10.1/24 on Lab-Internal. Confirm web UI access.",
     "Add OPT1: attach a third NIC to a new vSwitch 'Lab-DMZ', assign in pfSense as OPT1 with IP 192.168.20.1/24, enable its DHCP (range .100-.150).",
     "Move LAB-DC01 and the future file server to Lab-DMZ addressing (192.168.20.10, 192.168.20.11); keep workstations on LAN 192.168.10.0/24.",
     "Write LAN rules: allow LAN net to DMZ net on TCP 53 (DNS), 88/389/445 (AD) only; block all other LAN->DMZ. Write DMZ rules: allow DMZ to LAN established/related only (default deny otherwise).",
     "Test from a workstation VM: nslookup and domain join still work; but Test-NetConnection 192.168.20.11 -Port 3389 FAILS (RDP blocked) while -Port 445 succeeds — segmentation proven."],
    "Three-segment lab (WAN/LAN/DMZ) with least-privilege inter-segment rules and a passing segmentation test matrix",
    "pfSense Status > Dashboard shows all three interfaces up; the workstation test matrix passes: DNS/AD ports open to DC, RDP to file server blocked, ping to WAN blocked from DMZ.")

toollab("IL27-TL-07", "Ubuntu Server: hardened SSH bastion", 7, "IL27-M08",
    ["IL27-INST-08", "IL27-INST-15"], "IL27-TL-01",
    "Stand up lab-linux01 as the lab's Linux workhorse: static IP, key-only SSH, automatic updates, and a non-root ops user with sudo — the template for every Linux box in the capstone.",
    ["Complete IL27-INST-08 (Ubuntu 24.04, hostname lab-linux01, static 192.168.10.20, key-only SSH).",
     "Harden: sudo apt install -y fail2ban ufw; sudo ufw default deny incoming; sudo ufw allow OpenSSH; sudo ufw --force enable. Confirm fail2ban jail for sshd is active: sudo fail2ban-client status sshd.",
     "Enable unattended upgrades: sudo apt install -y unattended-upgrades; sudo dpkg-reconfigure -plow unattended-upgrades (answer Yes).",
     "Create the lab service account: sudo useradd -m -s /bin/bash svc-monitor; give it passwordless sudo for systemctl only via /etc/sudoers.d/svc-monitor: 'svc-monitor ALL=(ALL) NOPASSWD: /usr/bin/systemctl'.",
     "Join it to monitoring later — for now prove: ssh -o PasswordAuthentication=no ops@192.168.10.20 works, password login is refused, and ufw blocks everything except 22."],
    "Hardened lab-linux01: key-only SSH, UFW deny-by-default, fail2ban, unattended upgrades",
    "ssh with a password fails; ssh with key succeeds; sudo ufw status shows 'Status: active' with only OpenSSH allowed; fail2ban-client status sshd shows the jail.")

toollab("IL27-TL-08", "Docker: containerize a lab utility", 8, "IL27-M09",
    ["IL27-INST-09"], "IL27-TL-07",
    "Run your first production-shaped workload: a containerized internal tool on lab-linux01 with a Dockerfile you wrote, a named volume for data, and restart policy so it survives reboots.",
    ["On lab-linux01 install Docker Engine (get.docker.com script) and add ops to the docker group.",
     "Write a tiny status page: ~/status-page/index.html showing lab hostname inventory. Write a Dockerfile: FROM nginx:alpine, COPY index.html to /usr/share/nginx/html, EXPOSE 80.",
     "Build and run: docker build -t lab-status:1.0 ~/status-page && docker run -d --name status --restart unless-stopped -p 8080:80 lab-status:1.0.",
     "Persist properly: recreate with a named volume for any writable path your app needs (docker volume create status-data) and document the run command in ~/status-page/README.md.",
     "From a workstation browse http://192.168.10.20:8080 — the page loads. Kill the container, reboot the VM, confirm it auto-restarts (unless-stopped)."],
    "Containerized status page on lab-linux01, auto-restarting, documented run command",
    "docker ps shows status Up; curl -s http://localhost:8080 returns your HTML; after reboot, docker ps still shows it Up without manual start.")

toollab("IL27-TL-09", "Zabbix: monitor the whole lab", 9, "IL27-M11",
    ["IL27-INST-10"], "IL27-TL-07",
    "Turn lab-linux01 into the monitoring server: Zabbix watching the DC, the firewall, and itself — with a trigger that pages (emails) you when a host goes down.",
    ["Install Zabbix server + frontend on lab-linux01 per IL27-INST-10 (or the Docker Compose alternative from IL27-INST-11 — pick one, document which).",
     "Install Zabbix Agent 2 on LAB-DC01 (Windows MSI) and on lab-linux01 (already there); add both hosts in the UI with the 'Windows by Zabbix agent' / 'Linux by Zabbix agent' templates.",
     "Add pfSense via SNMP: enable SNMP on pfSense (Services > SNMP), add the firewall as an SNMP host in Zabbix with the 'pfSense by SNMP' community template.",
     "Create a trigger that matters: '{LAB-DC01:agent.ping.nodata(5m)}=1' severity High — DC unreachable for 5 minutes. Configure a media type to email your lab mailbox on High triggers.",
     "Chaos test: shut down LAB-DC01 for 6 minutes. Confirm the trigger fires, the email arrives, and recovery clears when it boots. Document the alert timeline."],
    "Zabbix monitoring 3+ lab hosts with a tested DC-down alert path end to end",
    "Monitoring > Hosts shows all green; the chaos test produced a High event with email; Problems dashboard is clear after recovery.")

toollab("IL27-TL-10", "Backup rotation: 3-2-1 on the file server", 10, "IL27-M12",
    ["IL27-INST-12"], "IL27-TL-02",
    "Build lab-fs01 (file server VM), share department folders, then protect them with Windows Server Backup on a schedule — and prove the restore works before you need it.",
    ["Create VM LAB-FS01 (Server 2025, 4 GB RAM, 60 GB OS disk + 100 GB data disk), join to lab.local, place the computer object in OU=Servers, static IP 192.168.20.11.",
     "Install FS role: Install-WindowsFeature FS-FileServer; create D:\\Shares\\Departments with subfolders HR, IT, Finance; share as \\\\lab-fs01\\departments with Authenticated Users read, department groups modify (create LAB-HR, LAB-IT, LAB-Finance groups in OU=Groups).",
     "Attach a third 120 GB virtual disk as the backup target. Install Windows-Server-Backup; schedule daily 02:00 full-server backup to the dedicated disk (IL27-INST-12 steps).",
     "The 3-2-1 stretch: copy the weekly backup VHD to your host/external drive (the offsite copy) and document where it lives.",
     "Restore drill: delete D:\\Shares\\Departments\\IT\\canary.txt, recover it with wbadmin start recovery, and confirm the file returns with contents intact. Log the drill date."],
    "LAB-FS01 file server with department shares, nightly backups, documented offsite copy, and a logged successful restore drill",
    "wbadmin get versions shows recent backups; the canary restore succeeded; net share shows 'departments'; an offsite copy path is documented.")

toollab("IL27-TL-11", "Endpoint hardening baseline", 11, "IL27-M14",
    ["IL27-INST-02"], "IL27-TL-05",
    "Harden a Windows 11 lab client with a GPO-delivered baseline: Defender on, firewall on, BitLocker-ready, LAPS for local admin, unnecessary services off — then audit it.",
    ["Domain-join a Windows 11 VM (LAB-W11-01) into OU=Workstations.",
     "Create GPO 'LAB-Endpoint-Baseline' linked to OU=Workstations: Windows Defender Antivirus enabled with real-time protection + cloud-delivered protection; Windows Firewall Domain profile ON blocking inbound by default; BitLocker OS-drive encryption required (store recovery keys in AD).",
     "Deploy LAPS (Windows LAPS built into current Windows): configure via GPO — Computer Configuration > Administrative Templates > System > LAPS: enable password backup to AD, 30-day rotation. Confirm ms-LAPS-Password appears on the computer object.",
     "Disable legacy risk: GPO preference to disable the SMBv1 feature (Disable-WindowsOptionalFeature) and block Telnet client; set 'Deny log on locally' for Guests via Security Settings.",
     "Audit: run Get-MpComputerStatus on the client (RealTimeProtectionEnabled True), gpresult to confirm the GPO, and read the LAPS password back as Domain Admin. Record all three outputs as your hardening evidence."],
    "Hardened LAB-W11-01 with evidence pack: Defender status, applied GPO list, LAPS password retrievable",
    "Get-MpComputerStatus RealTimeProtectionEnabled=True; gpresult shows LAB-Endpoint-Baseline; Get-LapsADPassword returns a current password.")

toollab("IL27-TL-12", "Incident response drill: ransomware simulation", 12, "IL27-M15",
    ["IL27-INST-06"], "IL27-TL-11",
    "The capstone drill: simulate a ransomware alert on LAB-W11-01 and run the full IR lifecycle — detect, isolate, eradicate, recover, lessons learned — against your own lab.",
    ["SIMULATION ONLY — use a harmless canary: create C:\\Users\\Public\\ransom-sim\\ with 20 text files, then run a script that renames them to .encrypted (no real malware, no real encryption). Zabbix/Wireshark should show the file-rename burst if you are watching.",
     "DETECT: notice via your monitoring (Zabbix trigger on file-modification rate, or the canary tripwire you built in the scripting module). Record detection time.",
     "ISOLATE: disable the VM's NIC in Hyper-V (or pfSense: block the host IP with a firewall rule) — host stays on for forensics, network dead. Snapshot the VM BEFORE touching anything (evidence preservation).",
     "ERADICATE + RECOVER: identify the 'patient zero' script in PowerShell history / scheduled tasks, remove persistence, restore the canary folder from the LAB-FS01 backup (IL27-TL-10), re-enable the NIC.",
     "Write the incident report (feeds mockTasks): timeline, root cause, containment actions, recovery point, and two preventive controls you will add (e.g. AppLocker rule, backup immutability). Present it as your capstone debrief."],
    "Completed IR drill with timeline, preserved evidence snapshot, restored data, and a written incident report",
    "Incident report exists with detection/containment/recovery timestamps; the evidence snapshot is labeled; restored canary files verified; two new preventive controls documented.")

SL = []
def scriptlab(id, title, moduleId, level, brief, objectives, starter, walkthrough, extension):
    SL.append({"id": id, "title": title, "moduleId": moduleId, "level": level, "brief": brief,
               "objectives": objectives, "starterCode": starter, "solutionWalkthrough": walkthrough,
               "extension": extension})

scriptlab("IL27-SC-01", "User inventory report (PowerShell + Active Directory)", "IL27-M10", "guided",
    "Build a script that exports every enabled user in lab.local to CSV with manager, department, last logon, and stale-account flags — the exact report an IT Infrastructure Specialist runs before an audit.",
    ["Query AD with Get-ADUser using -Filter and -Properties for the fields you need (never pull * in production)",
     "Calculate days-since-last-logon and flag accounts stale over 45 days",
     "Export a clean CSV with Export-Csv -NoTypeInformation and a summary to the console"],
    '# Starter: fill in the three TODOs\nImport-Module ActiveDirectory\n$cutoff = (Get-Date).AddDays(-45)\n$users = Get-ADUser -Filter {Enabled -eq $true} -Properties DisplayName, Department, Manager, LastLogonDate, PasswordLastSet\n# TODO 1: select the fields and add a calculated StaleAccount property\n# TODO 2: sort stale accounts first, then by DisplayName\n# TODO 3: export to .\\UserInventory.csv and print a summary count\n',
    ["Import-Module ActiveDirectory — without it nothing below works; on the DC it autoloads, on workstations RSAT provides it.",
     "Get-ADUser -Filter {Enabled -eq $true} -Properties DisplayName,Department,Manager,LastLogonDate,PasswordLastSet — the -Properties list is deliberate: default properties do not include last logon.",
     "Pipe to Select-Object DisplayName,SamAccountName,Department,@{Name='Manager';Expression={(Get-ADUser $_.Manager).DisplayName}},LastLogonDate,@{Name='DaysSinceLogon';Expression={[int]((Get-Date)-$_.LastLogonDate).TotalDays}},@{Name='StaleAccount';Expression={$_.LastLogonDate -lt $cutoff}}.",
     "Sort: Sort-Object @{Expression='StaleAccount';Descending=$true}, DisplayName — stale accounts float to the top for the reviewer.",
     "Export: $report | Export-Csv -Path .\\UserInventory.csv -NoTypeInformation; then Write-Host \"$($report.Count) users, $($report.Where({$_.StaleAccount}).Count) stale\" — always print the summary so a scheduled run logs something useful.",
     "Run it with -WhatIf thinking first: read-only script, but schedule it later via Task Scheduler with a service account (never your Domain Admin)."],
    "Add fine-grained output: group by Department with Group-Object, and email the CSV to the IT manager with Send-MailMessage when stale count exceeds 10.")

scriptlab("IL27-SC-02", "Log parser: failed logons triage (PowerShell + Get-WinEvent)", "IL27-M10", "guided",
    "Parse the Security event log for failed logons (event 4625), aggregate by source IP and target account, and flag the top offenders — the daily triage an infrastructure specialist runs before coffee.",
    ["Query the Security log with Get-WinEvent -FilterHashtable (fast, server-side filtering)",
     "Extract IP and account from the event's Properties array (index positions are stable for 4625)",
     "Group, count, sort, and output a ranked offender table with a brute-force threshold alert"],
    '# Starter: fill in the TODOs\n$events = Get-WinEvent -FilterHashtable @{LogName="Security"; Id=4625; StartTime=(Get-Date).AddHours(-24)}\n# TODO 1: build objects with Time, TargetAccount ($e.Properties[5].Value), SourceIP ($e.Properties[19].Value)\n# TODO 2: Group-Object by SourceIP, count, sort descending\n# TODO 3: Write-Warning for any IP with count -ge 20 ("possible brute force")\n',
    ["Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddHours(-24)} — FilterHashtable filters at the log service, orders of magnitude faster than Where-Object after the fact.",
     "For each event: [pscustomobject]@{Time=$e.TimeCreated; TargetAccount=$e.Properties[5].Value; SourceIP=$e.Properties[19].Value} — for 4625, Properties[5] is TargetUserName and Properties[19] is IpAddress. (Verify once with ($e.Properties | ForEach-Object {$_.Value}) on a sample.)",
     "Group: $parsed | Group-Object SourceIP | Select-Object Name,Count | Sort-Object Count -Descending — Name is the IP, Count the attempts.",
     "Threshold: foreach ($g in $grouped) { if ($g.Count -ge 20) { Write-Warning \"Possible brute force from $($g.Name): $($g.Count) failures in 24h\" } }.",
     "Needs elevation: reading the Security log requires admin — run pwsh elevated, and note this in your runbook so the scheduled version uses a proper service account.",
     "Cross-check one offender with the firewall: match the IP against pfSense logs to see if it is internal (compromised host?) or external (internet noise)."],
    "Extend to 4740 (account locked out) correlation: join lockout events to the 4625 table to show which brute-force runs actually locked accounts.")

scriptlab("IL27-SC-03", "Backup verification script (PowerShell + wbadmin)", "IL27-M12", "guided",
    "Backups you never verify are hope, not strategy. Write a script that checks the latest wbadmin version, its age, and the existence of the offsite copy — and fails loudly when anything is stale.",
    ["Parse wbadmin output reliably (it is text, not objects — use Select-String)",
     "Compute backup age and fail if older than 26 hours",
     "Verify the offsite copy path exists and log a PASS/FAIL result suitable for monitoring ingestion"],
    '# Starter: fill in the TODOs\n$raw = wbadmin get versions\n# TODO 1: extract version identifiers (lines matching "Version identifier:")\n# TODO 2: extract the backup time of the newest version and compute its age in hours\n# TODO 3: Test-Path the offsite copy; emit PASS or FAIL with reasons; exit 1 on FAIL\n',
    ["$raw = wbadmin get versions — capture the text. If it says 'no backups', that IS the answer: FAIL immediately.",
     "$ids = $raw | Select-String 'Version identifier:\\s*(\\S+)' | ForEach-Object { $_.Matches.Groups[1].Value } — regex capture of the identifier.",
     "Newest backup time: $times = $raw | Select-String 'Backup time:\\s*(.+)' — take the last match, [datetime]$newest = $times[-1].Matches.Groups[1].Value, then $ageHours = ((Get-Date) - $newest).TotalHours.",
     "Gate: if ($ageHours -gt 26) { Write-Error \"FAIL: newest backup is $([int]$ageHours)h old\"; exit 1 }.",
     "Offsite: $offsite = '\\\\nas\\offsite\\lab-fs01' (your documented path from IL27-TL-10); if (-not (Test-Path $offsite)) { Write-Error 'FAIL: offsite copy unreachable'; exit 1 }.",
     "Success path: Write-Output \"PASS: backup $($ids[-1]) age $([int]$ageHours)h, offsite reachable\"; exit 0 — Zabbix can run this as a UserParameter and alert on nonzero exit."],
    "Add email alerting on FAIL via Send-MailMessage, and rotate the script's own log file so it does not grow forever.")

scriptlab("IL27-SC-04", "Linux health-check script (Bash)", "IL27-M08", "guided",
    "A 60-second health snapshot for lab-linux01: CPU load, memory, disk, critical services, and pending updates — output as one screen a human can read at 2 AM.",
    ["Read load, memory, and disk from /proc and df without extra packages",
     "Check named services with systemctl is-active and report DEGRADED on any failure",
     "Count pending security updates and exit nonzero when the box is unhealthy"],
    '#!/usr/bin/env bash\n# Starter: fill in the TODOs\nset -u\nHOSTN=$(hostname)\n# TODO 1: print 1/5/15-min load averages from /proc/loadavg\n# TODO 2: print MemAvailable and disk % for / from free/df\n# TODO 3: loop over services (ssh zabbix-agent2 docker fail2ban); systemctl is-active each; track failures\n# TODO 4: count upgradable security packages; exit 1 if any check failed\n',
    ["set -u (fail on unset variables) — the one safety line every bash health script needs.",
     "Load: read -r l1 l5 l15 _ < /proc/loadavg; echo \"Load: $l1 $l5 $l15\" — compare l1 against nproc to judge pressure.",
     "Memory/disk: free -m | awk '/Mem:/ {print \"Mem avail: \"$7\" MB\"}'; df -h / | awk 'NR==2 {print \"Disk /: \"$5\" used\"}'.",
     "Services: for s in ssh zabbix-agent2 docker fail2ban; do if ! systemctl is-active -q \"$s\"; then echo \"FAIL: $s\"; FAILED=1; fi; done — -q keeps it quiet, the loop keeps it readable.",
     "Updates: UP=$(apt list --upgradable 2>/dev/null | grep -c security); echo \"Security updates pending: $UP\" — needs a recent apt update to be accurate.",
     "Exit: [ \"${FAILED:-0}\" -eq 1 ] && exit 1; echo \"OK: $HOSTN healthy\" — wire this into Zabbix as an external check or cron it with output to a log.",
     "Make it executable (chmod +x healthcheck.sh) and test by stopping docker once: the script must catch it and exit 1."],
    "Convert the output to JSON (jq) so Zabbix or Grafana can ingest the metrics instead of a human reading them.")

with open("/home/hatch/workspace/apex-audit/docs/university/data/courses/_il27-build/frag_tool_script_labs.json", "w") as f:
    json.dump({"toolLabs": TL, "scriptLabs": SL}, f, indent=1)
print("toolLabs:", len(TL), "scriptLabs:", len(SL))
