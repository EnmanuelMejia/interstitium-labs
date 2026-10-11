#!/usr/bin/env python3
"""IL-06 retrofit to the il-19 Multicloud course template.
Reads il-06 JSON, restructures modules into template shape, validates, writes atomically.
NEVER touches il-23 or il-19.
"""
import json, os, re, sys

BASE = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
PATH = os.path.join(BASE, "il-06-cybersecurity-secure-engineering.json")

BANNED = ["aleks", "brilliant", "khan academy", "coursera", "udemy", "edx"]
FORBIDDEN = ["palantir", "nsa"]

# ---------------------------------------------------------------- M1 summary
M1_SUMMARY = (
    "Welcome to IL-06 \u2014 Cybersecurity & Secure Engineering. I\u2019m your instructor, and we begin "
    "the way every serious security operator begins: by learning how systems break. This is Module 1, "
    "the Hackers-Arise spine \u2014 Linux for hackers, TCP/IP for attackers, OSINT tradecraft, password "
    "cracking, Wi-Fi hacking, web application exploitation, forensics, and SCADA/ICS plus satellite "
    "systems \u2014 cross-mapped to labs and the NICE Framework, with safety-critical ethics in every "
    "lesson. Everything offensive you practice here is for legal targets only, with documented "
    "authorization. Know the attack to earn the defense \u2014 that contract runs through the whole course."
)

M1_CONCEPTS = """- **bash for operations** \u2014 the shell as an operations platform: looping over targets, parsing command output at speed.
- **text processing pipeline** \u2014 grep, sed, awk, cut, sort, and uniq chained over scan output; the attacker\u2019s spreadsheet.
- **SUID** \u2014 the set-user-ID permission bit: a binary that runs as its owner; the classic Linux privilege-escalation surface.
- **persistence mechanism** \u2014 cron jobs and services, the footholds that survive reboots; you learn them to recognize them.
- **TCP/IP for attackers** \u2014 reading what each header field leaks: TTL and window sizes hint the OS, sequence numbers hint the stack.
- **host discovery** \u2014 finding which hosts are alive before you scan a single port; recon\u2019s first question.
- **connect scan** \u2014 a full TCP handshake per port; loud, reliable, and logged everywhere.
- **SYN scan** \u2014 the half-open scan; quieter than a connect scan, and the attacker\u2019s default.
- **UDP scan** \u2014 slow and unreliable, but UDP services hide some of the best vulnerabilities.
- **vulnerability scanning** \u2014 service detection plus version fingerprinting: identify the software, pin the exact version, match the known weakness.
- **exploitation workflow** \u2014 recon \u2192 scan \u2192 exploit \u2192 post-exploitation; the grammar every attack in this course follows.
- **passive reconnaissance** \u2014 DNS, WHOIS, certificate transparency, breach data, social media; zero contact with the target.
- **active reconnaissance** \u2014 anything that touches the target; it announces you and requires authorization.
- **OSINT tradecraft** \u2014 sock puppets and compartmentation; operational security for the investigator.
- **documentation discipline** \u2014 every finding sourced and timestamped; the lab report starts at recon, not at the shell.
- **hash identification** \u2014 recognizing the hash format first (hash-identifier thinking) so the attack matches the algorithm.
- **rule-based cracking** \u2014 a wordlist plus mangling rules \u2014 leetspeak substitutions, ?d?d?d?d appends \u2014 multiplies a list roughly 100x; attackers think in rules, not bigger lists.
- **keyspace** \u2014 the total number of candidate passwords; time-to-crack is keyspace divided by hashrate.
- **credential hygiene** \u2014 the defender\u2019s lesson from cracking: length, uniqueness, and MFA beat every clever password.
- **802.11 fundamentals** \u2014 how Wi-Fi frames, beacons, and authentication actually work; the prerequisite to attacking or defending wireless.
- **4-way handshake** \u2014 the WPA2 key exchange; capture it and the crack happens offline, at your speed.
- **deauthentication attack** \u2014 forcing a client to reconnect so you can capture its handshake; on your own lab network only.
- **WPA3** \u2014 the current Wi-Fi standard; resists the offline dictionary attacks that fell WPA2.
- **PMF** \u2014 Protected Management Frames; the defense that defeats deauthentication attacks.
- **rogue-AP detection** \u2014 finding evil-twin access points impersonating your network.
- **Burp methodology** \u2014 proxy to observe, repeater to manipulate by hand, intruder to automate, decoder to transform; methodology before automation.
- **injection flaw** \u2014 SQL injection, command injection, cross-site scripting; untrusted input reaching an interpreter is the vulnerability.
- **attack surface** \u2014 in web exploitation, every input field, header, and parameter is the attack surface.
- **authentication attack** \u2014 brute force, session-handling abuse, MFA bypass shapes; identity is the perimeter now.
- **disk forensics** \u2014 file carving, deleted-file recovery, registry and USN analysis; the artifacts your attack leaves behind.
- **memory forensics** \u2014 process lists, injected code, network connections; memory is where malware lives.
- **super-timeline** \u2014 filesystem, registry, and log events merged into one chronological view of the intrusion.
- **anti-forensics** \u2014 timestomping, log wiping; you learn it so you can detect it.
- **Modbus** \u2014 the OT protocol with no authentication by design; you don\u2019t patch it, you segment around it.
- **DNP3** \u2014 the utility-sector control protocol; the same unauthenticated heritage as Modbus.
- **air-gapped lab** \u2014 the only acceptable OT practice environment: no route to production, ever.
- **safety-critical ethics** \u2014 OT attacks can kill people; that fact outranks every technique in this module.
- **NICE Framework** \u2014 the workforce taxonomy this spine maps to: OG (Oversight/Governance), DD (Design/Development), IO (Implementation/Operation), PD (Protection/Defense), IN (Investigation)."""

M1_HANDS_ON = """Before you touch an offensive tool, you build the lab and the habits. This is the exact sequence I\u2019d run with a new operator, and it\u2019s your Milestone 1.1. Everything here runs against systems you own.
1. **Build the lab first.** Two virtual machines on an isolated host-only network: an attacker Linux box and a target you own. No lab, no techniques \u2014 that\u2019s the rule.
2. **Bash warm-up: pipeline a scan.** Run a scan of your lab target, then chain grep, cut, sort, and uniq to extract just the open ports and service banners. Text processing at speed is the skill; the scan is the excuse.
3. **Passive recon drill.** Against a domain you own: pull certificate-transparency names, DNS records, and WHOIS. Zero packets to the target\u2019s ports \u2014 passive before active is ethics AND tradecraft.
4. **Scan with discipline.** One host deeply before ten hosts shallowly. Compare a connect scan against a SYN scan of the same lab host and note what each reveals \u2014 and what each would log.
5. **Identify, then crack, a lab hash.** Practice hash-identifier thinking on a hash you generated yourself, then attack it with a wordlist plus rules. Estimate the time first: keyspace divided by hashrate.
6. **Wi-Fi on your own access point.** Capture your own 4-way handshake, crack it offline, then enable WPA3 with PMF and confirm the attack no longer works. Every attack module ends in the defense \u2014 that\u2019s the spine\u2019s contract.
7. **Burp walkthrough.** Proxy a lab web application: observe in the proxy, manipulate one request by hand in the repeater, then automate one input with the intruder. Methodology before automation.
8. **Timeline your own attack.** Build a super-timeline covering steps 2 through 7 and note every artifact you left. If you can\u2019t find your own footprints, you can\u2019t find an attacker\u2019s."""

M1_PROJECT = """**Capstone: the spine field manual.** Produce your personal operator\u2019s field manual \u2014 one page per spine domain (Linux, networks, OSINT, passwords, Wi-Fi, web, forensics, OT/satellite). Each page holds: the five commands or concepts you\u2019d reach for first, one lab you actually ran with its key output, and the defensive countermeasure that defeats the attack. Append your command log from the Hands-on procedure and a one-page NICE self-map (OG/DD/IO/PD/IN) showing where your skills sit today. The manual is graded on accuracy and on the defense column \u2014 an attack page without its countermeasure is incomplete."""

M1_NOAH = """Noah probes mastery with questions like:
- In one sentence, what is the deliverable I\u2019m producing by the end of this module?
- Walk Noah through your recon order on a new lab target \u2014 and name the exact point where passive becomes active, and why that line matters.
- *Hands-on:* \u201cShow Noah your text-processing pipeline over real scan output: open ports and banners only, no noise.\u201d
- *Ethics \u2014 Noah\u2019s rule:* name the authorization for every technique you practiced this module. No authorization, no technique. Say it out loud."""

M1_QUIZ_EXTRA = [
    {"q": "A lab binary has the SUID bit set and is owned by root. Why does an attacker care?",
     "choices": ["it runs faster", "it executes with the owner\u2019s privileges \u2014 root \u2014 so an exploitable SUID binary is a privilege-escalation path", "it is hidden from ls", "it cannot be deleted"],
     "answer": 1,
     "explain": "SUID runs the binary as its owner; root-owned plus exploitable equals privesc. Covered in the Concepts section."},
    {"q": "Why is the SYN scan the attacker\u2019s default rather than the connect scan?",
     "choices": ["it is faster on UDP", "the half-open handshake is quieter and less likely to be logged than a full connect scan", "it works without a network", "it finds more ports"],
     "answer": 1,
     "explain": "SYN scans never complete the handshake, so they\u2019re stealthier than full connects. Covered in the Concepts section."},
    {"q": "Time-to-crack a password is estimated as\u2026",
     "choices": ["wordlist size times luck", "keyspace divided by hashrate", "hash length minus salt", "CPU cores plus RAM"],
     "answer": 1,
     "explain": "Total candidates divided by guesses per second gives the time estimate \u2014 the rig/time math from the Concepts section."},
    {"q": "You enable WPA3 with PMF on your lab access point. What did you just defeat?",
     "choices": ["nothing \u2014 wireless is insecure", "the offline handshake-cracking chain and deauthentication attacks", "all malware", "Bluetooth attacks"],
     "answer": 1,
     "explain": "WPA3 resists offline dictionary attacks; PMF defeats deauth. Every attack ends in the defense \u2014 the Project brief\u2019s rule."},
]

# ---------------------------------------------------------------- M2 summary
M2_SUMMARY = (
    "Welcome back \u2014 I\u2019m your instructor, and this is Module 2: offensive operations. In Module 1 you "
    "learned how systems break; now you learn to break them methodically, the way a professional "
    "penetration tester does: lab operations methodology with enumeration discipline, the PEN-200/OSCP map "
    "including buffer overflows and the 24-hour exam logistics, advanced web exploitation chains, Active "
    "Directory attack chains with BloodHound thinking, the T0\u2013T3 CTF architecture, and professional "
    "reporting \u2014 because the report is the product. Legal targets only, documented authorization, "
    "stay in scope. The exploit is the receipt; enumeration is the purchase."
)

M2_CONCEPTS = """- **machine methodology** \u2014 recon \u2192 enumerate \u2192 exploit \u2192 privilege-escalate \u2192 loot \u2192 report; the loop you run on every lab box.
- **enumeration discipline** \u2014 every port, every service, every version; the vulnerability hides in the boring service you skipped.
- **Linux privesc patterns** \u2014 SUID binaries, cron jobs, writable PATH and service files, kernel version, sudo rights; the checklist you run on every shell.
- **Windows privesc patterns** \u2014 unquoted service paths, weak service permissions, AlwaysInstallElevated, token privileges; the Windows twin of the Linux checklist.
- **\u2018try harder\u2019, correctly understood** \u2014 enumerate more, not guess more; the PEN-200 methodology in three words.
- **buffer overflow** \u2014 the rite of passage: fuzz to crash, find the offset, control EIP, deliver shellcode; it teaches the stack disguised as an exploit.
- **EIP control** \u2014 overwriting the instruction pointer; the moment a crash becomes an exploit.
- **DEP/ASLR** \u2014 Data Execution Prevention and Address Space Layout Randomization; the mitigations that make classic overflows a fundamentals lesson.
- **SQLi\u2192RCE** \u2014 turning SQL injection into remote code execution: xp_cmdshell, writing web shells; the web chain that ends in a shell.
- **SSRF** \u2014 server-side request forgery: making the server fetch a URL you chose; the pivot from web bug to infrastructure access.
- **cloud metadata service** \u2014 169.254.169.254: instance credentials over HTTP; the SSRF crown jewel and the keys to the kingdom.
- **IMDSv2 defense** \u2014 hop limits and token requirements that blunt SSRF-to-metadata attacks; know the defense with the attack.
- **deserialization** \u2014 untrusted object graphs decoded into live objects; gadget chains turn it into remote code execution.
- **race condition (TOCTOU)** \u2014 time-of-check to time-of-use: the timing attack that wins when two operations interleave wrong.
- **Kerberoasting** \u2014 requesting crackable (RC4) service tickets as any domain user, then cracking them offline; the service account\u2019s password, no privileges required.
- **AS-REP roasting** \u2014 accounts with Kerberos pre-authentication disabled let you request the AS-REP directly and crack it offline.
- **BloodHound thinking** \u2014 attack the graph, not the host: find the shortest path to Domain Admin through misconfigurations first, exploit second.
- **lateral movement** \u2014 PSExec, WMI, WinRM, pass-the-hash; moving through the network with captured credentials.
- **pass-the-hash** \u2014 authenticating with the hash itself, no cracking required; why hashes are password-equivalent.
- **Golden Ticket** \u2014 a forged Kerberos ticket-granting ticket; domain dominance that betrays itself in ticket metadata.
- **DCSync** \u2014 replicating directory secrets like a domain controller; detected in event 4662 replication anomalies.
- **event 4769** \u2014 the Kerberos service-ticket request log; anomalies here are the Kerberoasting detection.
- **T0\u2013T3 CTF architecture** \u2014 T0 guided warmups, T1 single-technique, T2 chained scenarios, T3 research-grade original problems.
- **finding write-up** \u2014 title, severity, CVSS, evidence, business impact, remediation, retest; the anatomy of a finding that gets fixed.
- **risk rating** \u2014 likelihood times impact, stated honestly; inflating severity burns credibility at retest.
- **executive summary** \u2014 the one page the board actually reads; findings are for engineers, summaries are for decisions.
- **retest verification** \u2014 proving the fix worked; the step where client trust compounds."""

M2_HANDS_ON = """This module is a discipline module: the methodology matters more than any single exploit. Run this exact loop on every lab machine, and document from minute one \u2014 screenshots and commands, because the report starts at recon.
1. **Enumerate like it\u2019s 70% of the work \u2014 because it is.** Scan every port, identify every service, pin every version. The unexamined UDP service is where the vulnerability lives; check it before you touch the web app.
2. **Run the privesc checklists.** On a Linux shell: SUID binaries, cron jobs, writable paths, kernel version, sudo rights. On a Windows shell: unquoted paths, service permissions, AlwaysInstallElevated, tokens. Checklists beat inspiration.
3. **Walk the buffer-overflow rite of passage.** In the lab: fuzz to crash, find the offset, control EIP, build the exploit. You\u2019re here to learn the stack \u2014 registers, memory layout, DEP/ASLR \u2014 disguised as an exploit.
4. **Chain a web vulnerability.** Take SQL injection to code execution in the lab (xp_cmdshell or a written shell), then pivot an SSRF to the metadata service at 169.254.169.254 \u2014 and then configure the IMDSv2 defense and confirm the chain breaks.
5. **Map Active Directory as a graph.** Ingest lab AD data into BloodHound-style thinking: find the shortest path to Domain Admin before you exploit anything. Then walk it: Kerberoasting or AS-REP roasting for the first credential, lateral movement for the next hop.
6. **Pair every attack with its detection.** Kerberoasting \u2192 event 4769 anomalies. DCSync \u2192 4662. Golden Ticket \u2192 ticket metadata. Red teaches blue \u2014 log the detection alongside the exploit in your notes.
7. **Climb one CTF tier.** Solve at your current tier (T0 guided through T3 research) and write the solve up as a finding: title, evidence, impact, remediation \u2014 even for a game box. The report is the product.
8. **Exam logistics rehearsal.** If OSCP is on your roadmap: plan a 24-hour practice block \u2014 sleep strategy, meal breaks, and starting the report early. The report has its own 48-hour clock; logistics are part of the methodology."""

M2_PROJECT = """**Capstone: the engagement report.** Run a full authorized penetration test against your lab network \u2014 minimum one Linux host, one Windows host, one web application, and an Active Directory lab \u2014 and deliver the professional report: executive summary (the page the board reads), methodology, findings with severity, CVSS, evidence, business impact, and remediation for each, plus a retest plan. Grade yourself on the honesty rules from the Concepts section: risk ratings at likelihood-times-impact with no inflation, every finding carrying its fix, and scope discipline documented. A finding without remediation is a complaint; access without a report is a story."""

M2_NOAH = """Noah probes mastery with questions like:
- In one sentence, what is the deliverable I\u2019m producing by the end of this module?
- *Enumeration drill:* \u201cNoah hands you a scan with one unexamined UDP service. Talk Noah through your next three commands and why.\u201d
- Draw the AD attack chain from the Hands-on procedure as a graph: where does BloodHound thinking save you the most time, and which hop has the clearest detection?
- *Honesty check:* you found a critical but the evidence is thin. Do you inflate, downgrade, or qualify \u2014 and what does the retest do to each choice?"""

M2_QUIZ_EXTRA = [
    {"q": "In the classic buffer-overflow workflow, what comes right after finding the crash offset?",
     "choices": ["write the report", "gain EIP control and build toward shellcode delivery", "run Nmap again", "reboot the target"],
     "answer": 1,
     "explain": "Offset \u2192 EIP control \u2192 shellcode \u2192 exploit; the rite-of-passage order from the Concepts section."},
    {"q": "SQL injection gives you stacked-query execution on a MSSQL lab host. The classic path to code execution is\u2026",
     "choices": ["reading the users table", "xp_cmdshell or writing a web shell \u2014 SQLi\u2192RCE", "changing the sa password only", "there is no path"],
     "answer": 1,
     "explain": "SQLi\u2192RCE via xp_cmdshell or a written shell is the web chain from the Concepts section."},
    {"q": "Pass-the-hash works because\u2026",
     "choices": ["hashes are encrypted passwords", "the hash itself authenticates \u2014 no cracking required \u2014 so hashes are password-equivalent", "it bypasses the network", "it only works offline"],
     "answer": 1,
     "explain": "Captured hashes authenticate directly; that\u2019s why credential hygiene matters. Covered in the Concepts section."},
    {"q": "A T2 CTF challenge differs from T1 in that it\u2026",
     "choices": ["is easier", "chains multiple techniques into a scenario rather than testing one technique", "has no solution", "is multiple choice"],
     "answer": 1,
     "explain": "T1 masters one technique; T2 combines them \u2014 the CTF architecture from the Concepts section."},
]

# ---------------------------------------------------------------- M3 summary
M3_SUMMARY = (
    "Welcome back \u2014 I\u2019m your instructor, and this is Module 3: defensive operations. Red team "
    "taught you how the break-in works; now you learn the other half of the skill: SOC operations across "
    "the three tiers, forensics and incident response at SANS depth, detection engineering with Sigma, "
    "and the Security+ bridge with its readiness gate. Red and blue are two halves of one skill \u2014 "
    "every attack you learned in Module 2 has a detection, and this module teaches you to build it. "
    "Contain before you eradicate, memory before disk, and blameless always."
)

M3_CONCEPTS = """- **L1 triage** \u2014 alert to quick classification: true or false positive, severity, escalate or close; speed with accuracy, measured by time-to-triage.
- **L2 investigation** \u2014 pulling the logs, building the timeline, correlating across EDR, firewall, proxy, and identity; depth after the L1 handoff.
- **L3 threat hunting** \u2014 hypothesis-driven searches (\u2018what would this adversary do here?\u2019); hunts that find things become detections.
- **detection engineering** \u2014 the discipline of turning hunts into deployed, tuned detections; the bridge between red knowledge and blue operations.
- **Sigma** \u2014 the open detection format: title, logsource, detection (selection plus filter plus condition), level; write once, convert to Splunk, Elastic, or Sentinel.
- **logsource** \u2014 the Sigma field naming what the rule watches; a rule is only as good as its log source\u2019s coverage.
- **false positive tuning** \u2014 baseline, threshold, allowlist; false positives are the tax on detection, budgeted and tuned \u2014 never silently tolerated.
- **blind spot** \u2014 what a log source cannot tell you; blind spots drive the logging roadmap, because you can\u2019t detect what you don\u2019t log.
- **disk forensics** \u2014 file carving, deleted-file recovery, registry and USN analysis; the persistent record of the intrusion.
- **memory forensics** \u2014 process lists, injected code, network connections; memory is where malware lives \u2014 and it evaporates.
- **network forensics** \u2014 PCAP timelines and C2 beacons: regular intervals plus consistent sizes are the beacon pattern.
- **order of volatility** \u2014 memory before disk, always; collect the ephemeral first in live response.
- **IR lifecycle** \u2014 preparation \u2192 detection and analysis \u2192 containment \u2192 eradication \u2192 recovery \u2192 lessons learned; the exam and the job agree on this order.
- **short-term containment** \u2014 isolate the host now; stop the bleeding before you diagnose.
- **long-term containment** \u2014 rebuild and harden; the fix that survives the attacker\u2019s return.
- **chain of custody** \u2014 hash everything (SHA-256) and document every hand; evidence that survives challenge.
- **super-timeline** \u2014 log2timeline-style merged timelines; the story of the intrusion in one view.
- **threat-informed defense** \u2014 mapping detections to MITRE ATT&CK; coverage gaps become the hunting backlog, and vague \u2018better detection\u2019 becomes a shopping list.
- **impossible travel** \u2014 same identity, two distant locations, minutes apart; paired with a fresh MFA enrollment it\u2019s the account-takeover pattern.
- **JA3** \u2014 the TLS client fingerprint; odd JA3 plus beaconing intervals confirms C2 in PCAP.
- **blameless postmortem** \u2014 fix the system, not the person; blame hides the next incident.
- **lessons learned** \u2014 the IR report that prevents recurrence; an incident response without it is just firefighting.
- **Security+ bridge** \u2014 the SY0-701 defensive vocabulary and readiness gate in this module; full preparation lives in IL-09."""

M3_HANDS_ON = """Blue-team skill is built in the lab exactly like red-team skill: repetition against realistic data. You\u2019ll work the full SOC motion \u2014 triage, investigate, hunt, detect \u2014 and finish by running an incident end to end.
1. **Triage drill: the 5-minute queue.** Take a set of lab alerts and classify each: true/false positive, severity, escalate or close. Time yourself \u2014 time-to-triage is the L1 metric. The impossible-travel plus new-MFA-enrollment alert escalates immediately; say why out loud.
2. **Investigate one escalation.** Pull the logs for your escalated alert and correlate across at least three sources (endpoint, identity, network). Build the timeline before you conclude \u2014 correlation beats collection.
3. **Hunt from a hypothesis.** Write one hypothesis (\u2018if the attacker used encoded PowerShell here, we\u2019d see it in process-creation logs\u2019), then search for it. Document the hypothesis even if the hunt finds nothing \u2014 failed hunts still teach the environment.
4. **Turn the hunt into a Sigma rule.** Write the detection: title, logsource, selection plus filter plus condition, level. Then write the tuning note from the Concepts section: what will false-positive, and how you\u2019d filter it.
5. **Map it to ATT&CK.** Tag your rule to its technique and check your coverage: the gap you find becomes your next hunt. Threat-informed defense turns \u2018we need better detection\u2019 into a backlog.
6. **Run the IR lifecycle tabletop.** Take the phishing-wave scenario: preparation, detection, short-term containment (isolate, revoke sessions), eradication, recovery \u2014 then write the lessons-learned. Contain before eradicating while scope is unknown.
7. **Practice the order of volatility.** In a live-response lab: memory first (process lists, connections), disk second. Narrate what evaporates if you reverse the order.
8. **Close the loop blamelessly.** Write the postmortem for your tabletop incident with zero blame on any analyst \u2014 every action item targets the system. That\u2019s the deliverable culture."""

M3_PROJECT = """**Capstone: the SOC shift simulation.** You are the entire SOC for a shift. Ingest a prepared alert bundle (benign noise, two true positives, one account-takeover pattern, one C2 beacon): triage the queue inside a timebox, escalate with written rationale, investigate the top escalation across three log sources, run one hypothesis-driven hunt, author the Sigma rule your hunt justifies with its tuning note, and close with a blameless lessons-learned memo. Deliverables: triage log with times, investigation timeline, the Sigma rule, the ATT&CK coverage note, and the memo. Graded on the Concepts-section disciplines: containment before eradication, memory before disk, tuned \u2014 not tolerated \u2014 false positives."""

M3_NOAH = """Noah probes mastery with questions like:
- In one sentence, what is the deliverable I\u2019m producing by the end of this module?
- *Triage drill:* \u201cNoah shows you an alert: impossible travel plus a new MFA enrollment. You have thirty seconds \u2014 escalate or close, and state the pattern.\u201d
- Your Sigma rule fires 500 times a day, all benign. Walk Noah through your tuning plan from the Hands-on procedure \u2014 and explain why silently disabling it is the wrong move.
- *Honesty check:* the lessons-learned draft blames the L1 analyst. Rewrite the finding the blameless way, out loud."""

M3_QUIZ_EXTRA = [
    {"q": "In live response, why does memory come before disk?",
     "choices": ["memory is bigger", "the order of volatility: memory evaporates, disk persists \u2014 collect the ephemeral first", "disk is slower", "policy says so"],
     "answer": 1,
     "explain": "Volatile evidence first is the forensics rule from the Concepts section."},
    {"q": "Event 4769 anomalies indicate\u2026",
     "choices": ["failed logons", "Kerberos service-ticket request anomalies \u2014 the Kerberoasting detection", "USB insertions", "patch installs"],
     "answer": 1,
     "explain": "4769 logs service-ticket requests; spikes and odd patterns betray Kerberoasting. Covered in the Concepts section."},
    {"q": "A super-timeline is built with\u2026",
     "choices": ["a spreadsheet only", "merged filesystem, registry, and log events (log2timeline-style) into one chronological view", "a firewall", "an antivirus scan"],
     "answer": 1,
     "explain": "Super-timelines merge every event source into the intrusion\u2019s story \u2014 the Concepts section\u2019s timeline analysis."},
    {"q": "Mapping your detections to MITRE ATT&CK gives you\u2026",
     "choices": ["a compliance certificate", "a coverage map whose gaps become the hunting backlog \u2014 threat-informed defense", "faster internet", "fewer alerts automatically"],
     "answer": 1,
     "explain": "ATT&CK mapping turns vague \u2018better detection\u2019 into a concrete backlog. Covered in the Concepts section."},
]

# ---------------------------------------------------------------- M4 summary
M4_SUMMARY = (
    "Welcome back \u2014 I\u2019m your instructor, and this is Module 4: the forward-deployed interface. "
    "This is where security engineering meets the customer: the forward-deployed engineer embedded in "
    "their network, under their compliance, on their timeline \u2014 diagnosing fast in unfamiliar estates, "
    "building to their constraints, and transferring everything so they can operate it after you leave. "
    "You\u2019ll also practice AI-aided security work with verification discipline, threat modeling with "
    "STRIDE and DREAD as working tools, and shipping secure defaults through reviews that unblock instead "
    "of blocking. The deliverable is never just access \u2014 it\u2019s the hardened system, the handoff, "
    "and the customer left stronger."
)

M4_CONCEPTS = """- **forward-deployed engineer** \u2014 the operator embedded with the customer: their network, their compliance, their timeline; diagnose fast, build to constraints, transfer everything.
- **transfer** \u2014 the FDE\u2019s real deliverable: documentation and handoff so the customer operates the system after you leave.
- **unfamiliar estate** \u2014 a customer environment you\u2019ve never seen; rapid diagnosis there is the FDE\u2019s core skill.
- **AI triage summarization** \u2014 models drafting incident summaries from alert context; the analyst verifies before acting.
- **KQL from English** \u2014 AI-generated hunt queries; useful drafts that get a human check before they touch production data.
- **verification discipline** \u2014 the model drafts, the analyst decides; every AI output gets a human check before action.
- **AI-assisted hunting** \u2014 hypothesis generation from threat intel and anomaly narration; the amplifier, not the analyst.
- **practitioner-led learning** \u2014 war stories over lectures; operators carry the tacit knowledge slides can\u2019t.
- **threat modeling** \u2014 enumerating what you\u2019re defending, from whom, and where it breaks \u2014 early, at design time.
- **STRIDE** \u2014 Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege; applied per component.
- **DREAD** \u2014 Damage, Reproducibility, Exploitability, Affected users, Discoverability; the ranking scale for what STRIDE finds.
- **mitigations with owners** \u2014 the only acceptable threat-model output: each finding paired with a fix and a name.
- **model rot** \u2014 threat models decay on change like milk, not wine; a new data flow triggers a new session.
- **secure defaults** \u2014 deny-by-default, least privilege out of the box, APIs that are hard to misuse; defaults decide outcomes.
- **deny-by-default** \u2014 nothing is allowed until explicitly permitted; the default posture that defeats most breaches.
- **least privilege** \u2014 every component gets the minimum access it needs; the principle behind the default.
- **security review as a service** \u2014 findings delivered with fixes and SLAs by severity; the review that unblocks instead of blocking.
- **review SLA** \u2014 critical findings in hours, highs in days; predictability is what turns security from gate to partner.
- **shipping at the boundary** \u2014 the customer\u2019s auditors, change windows, and rollback needs; security that ships beats perfect security that doesn\u2019t.
- **auditor-ready documentation** \u2014 writing like an auditor reads it, because at the boundary one will."""

M4_HANDS_ON = """Security engineering at the boundary is a practice discipline: model, decide, ship, hand off. Run this sequence against a sample system \u2014 a small web service with a database and an admin panel is plenty.
1. **Scope the model.** List what you\u2019re defending, from whom, and the trust boundaries. One whiteboard, one hour \u2014 a whiteboard hour now saves a sprint of rework later.
2. **STRIDE per component.** Walk each component through Spoofing, Tampering, Repudiation, Information disclosure, DoS, and Elevation. Write each finding as a concrete abuse case, not a vague worry.
3. **Rank with DREAD.** Score Damage, Reproducibility, Exploitability, Affected users, and Discoverability for each finding. The ranking is what turns a list into a plan.
4. **Assign mitigations with owners.** Every finding gets a fix and a name. A model without mitigations is a diagram \u2014 say that out loud before you close the session.
5. **Harden the defaults.** Apply deny-by-default and least privilege to the sample service: remove the permissive default config, scope the service account, choose the safe API. Defaults decide outcomes \u2014 most breaches exploit the default, not the exotic.
6. **Run the review as a service.** Write up your findings the way a review should land: each with its fix, each with an SLA (critical in hours, highs in days). Predictability builds trust.
7. **AI-amplify one step.** Have an AI tool draft the incident summary or a KQL hunt for your sample system \u2014 then verify every line before you\u2019d act on it. The model drafts, you decide.
8. **Write the handoff.** Produce the transfer document: architecture, credentials handling, runbooks, rollback plan. The customer operates it after you leave \u2014 that\u2019s the deliverable."""

M4_PROJECT = """**Capstone: the boundary engagement.** Take a sample customer scenario \u2014 regulated, change-window constrained, with an auditor in the loop \u2014 and deliver the full forward-deployed package: a STRIDE/DREAD threat model with mitigations and owners, the hardened-defaults configuration, a security review written as a service (findings with fixes and SLAs), and the transfer document with runbooks and rollback plan. Then write the one-page retrospective: where did the model rot risk live, and what triggers a re-model? Graded on the Concepts-section contract: every finding has an owner, every default is deny-first, and the handoff would survive the auditor."""

M4_NOAH = """Noah probes mastery with questions like:
- In one sentence, what is the deliverable I\u2019m producing by the end of this module?
- *Scenario:* \u201cNoah is the customer: air-gapped, regulated, and your timeline just halved. Walk Noah through what you ship, what you cut, and what the transfer looks like.\u201d
- An AI draft says to isolate the domain controller. Talk Noah through your verification steps before you\u2019d click \u2014 what\u2019s blast-radius-critical here?
- *Honesty check:* your threat model found nothing above medium. Do you ship it as-is, or does \u2018nothing found\u2019 deserve a second session? Defend your call."""

M4_QUIZ_EXTRA = [
    {"q": "STRIDE\u2019s \u2018S\u2019 \u2014 spoofing \u2014 is best countered by\u2026",
     "choices": ["backups", "strong authentication: proving the entity is who it claims to be", "encryption at rest", "rate limiting"],
     "answer": 1,
     "explain": "Spoofing is identity impersonation; authentication is the counter. Covered in the Concepts section."},
    {"q": "In DREAD, the second \u2018D\u2019 \u2014 discoverability \u2014 measures\u2026",
     "choices": ["data size", "how easily an attacker can discover the vulnerability", "disk usage", "documentation quality"],
     "answer": 1,
     "explain": "Discoverability ranks how findable the flaw is \u2014 part of the DREAD scale in the Concepts section."},
    {"q": "Deny-by-default means\u2026",
     "choices": ["deny all users", "nothing is permitted until explicitly allowed", "no passwords", "offline only"],
     "answer": 1,
     "explain": "Deny-first is the secure-default posture: allowlisting over blocklisting. Covered in the Concepts section."},
    {"q": "Least privilege applied to a new service account means\u2026",
     "choices": ["admin rights for convenience", "only the minimum permissions the service needs to function", "no password", "shared credentials"],
     "answer": 1,
     "explain": "Minimum-necessary access is the principle behind secure defaults \u2014 the Concepts section."},
    {"q": "A security review SLA of \u2018critical findings in hours, highs in days\u2019 exists because\u2026",
     "choices": ["auditors demand it", "predictability turns security from a blocking gate into an engineering partner", "it looks good", "it reduces headcount"],
     "answer": 1,
     "explain": "SLA predictability is what makes reviews unblock instead of block \u2014 the Hands-on procedure\u2019s review step."},
]

# ---------------------------------------------------------------- M5 summary
M5_SUMMARY = (
    "Welcome to the final module \u2014 I\u2019m your instructor, and this is where everything converges: "
    "security operations on Microsoft Sentinel at SC-200 depth. You\u2019ll manage the security operations "
    "environment (Defender XDR, Sentinel workspaces, data connectors, analytics rules, automation "
    "playbooks, MITRE ATT&CK mapping), respond to incidents across Defender, M365, and Purview with "
    "Graph enrichment, and hunt in KQL \u2014 hypotheses first, queries second, notebooks for "
    "repeatability \u2014 capped by a live-hunt capstone. Hunt in KQL, respond in minutes. Confirm "
    "current exam details on Microsoft Learn before you book \u2014 exam specifics change."
)

M5_CONCEPTS = """- **Defender XDR** \u2014 the unified portal: incidents queue plus advanced hunting across the Microsoft security stack.
- **Sentinel workspace** \u2014 the data boundary: connectors ingest here, rules query here, costs accrue here.
- **data connector** \u2014 the ingestion on-ramp: Defender, Entra, firewalls, CEF/Syslog; connector first, rule second \u2014 detections need data.
- **ingestion planning** \u2014 cost follows volume; high-volume noise gets filtered or sampled at the source, never blindly ingested.
- **scheduled analytics rule** \u2014 KQL run on a cadence; the workhorse detection.
- **NRT rule** \u2014 near-real-time analytics for the urgent detections that can\u2019t wait for the schedule.
- **automation playbook** \u2014 Logic Apps workflows: enrich the incident, then act \u2014 isolate the device, revoke the session; SOAR without the buzzword.
- **MITRE ATT&CK mapping** \u2014 every rule mapped to technique; coverage gaps become the hunting and detection backlog.
- **incident queue triage** \u2014 true positive? severity? blast radius? \u2014 the L1/L2 motion inside Sentinel.
- **Defender for Endpoint** \u2014 device timelines and live response; contain the endpoint from the portal without touching the desk.
- **M365 and Purview** \u2014 the email, Teams, SharePoint, DLP, and insider-risk surfaces an incident crosses.
- **Microsoft Graph enrichment** \u2014 querying identity, device, and risk state programmatically; the API behind the portal.
- **Security Copilot** \u2014 the assistant that drafts summaries and queries; the analyst verifies \u2014 the AI discipline, again.
- **KQL pipe** \u2014 table | where | summarize: the hunting query shape; filter, aggregate, rank.
- **summarize by bin()** \u2014 time-bucketing (bin(TimeGenerated, 1h)) for spotting beaconing and bursts on a timeline.
- **KQL join** \u2014 correlating two tables (or a table with itself, as in impossible-travel hunts) on a shared key.
- **hypothesis-first hunting** \u2014 \u2018if the attacker used X, we\u2019d see Y in table Z\u2019 \u2014 then the query; never the query first.
- **Sentinel notebooks** \u2014 Jupyter inside Sentinel: repeatable hunts and shared tradecraft the team can re-run.
- **live-hunt capstone** \u2014 the multi-stage attack scenario: detect, investigate, contain, report; synthesis only, no new tools.
- **SC-200 skills outline** \u2014 the exam\u2019s published domains; confirm current details on Microsoft Learn before booking."""

M5_HANDS_ON = """You learn Sentinel by hunting in it. Every step below runs against lab or sample data \u2014 the motions are the skill, and the motions transfer to any workspace.
1. **Stand up the environment on paper first.** Sketch your workspace boundary, list the data connectors you\u2019d enable (Defender, Entra, firewall/CEF-Syslog), and mark what you\u2019d filter at the source. Connector first, rule second \u2014 and ingestion is metered, so the sketch includes a cost note.
2. **Write your first scheduled rule.** A KQL detection on a schedule: filter with where, aggregate with summarize, rank the results. Read the KQL before you\u2019d trust any answer about it \u2014 the exam tests query comprehension exactly this way.
3. **Add the NRT twin.** Decide which of your detections is urgent enough for near-real-time, and justify the choice in one sentence. Not everything deserves NRT.
4. **Build the playbook.** A Logic Apps flow: enrich the incident (Graph: identity, device, risk state), then act (isolate device, revoke session) \u2014 then notify. Automation amplifies signal and noise alike, so the playbook only fires on a tuned rule.
5. **Triage the queue.** Take a set of lab incidents: true positive? severity? blast radius? Practice the ransomware-on-three-hosts versus phishing-click-with-no-payload prioritization until it\u2019s reflex.
6. **Run a hypothesis-first hunt.** State the hypothesis (\u2018if the attacker used X, we\u2019d see Y in table Z\u2019), write the KQL \u2014 joins for correlation, bin() for timelines \u2014 and save it as a notebook so the team can re-run it.
7. **Map to ATT&CK.** Tag every rule you wrote to its technique; the uncovered techniques are your hunting backlog. Threat-informed defense, in the workspace.
8. **Execute the live-hunt capstone.** A multi-stage attack scenario, end to end: detect, investigate, contain, report. No new tools \u2014 synthesis only. The incident report is the deliverable."""

M5_PROJECT = """**Capstone: the live-hunt operation.** You are the on-shift analyst when the multi-stage scenario begins: a phishing wave into M365, a clicked link with no immediate payload, then lateral movement toward the lab domain controller. Detect each stage with analytics rules you wrote, investigate across Defender XDR timelines and Purview surfaces, enrich with Graph, contain via playbook actions (verify before the DC isolation \u2014 the AI discipline applies to your own runbooks too), and deliver the incident report: timeline, blast radius, root cause, ATT&CK mapping, and remediation with owners. Then write the exam-readiness note: which SC-200 domain each capstone step exercised. Confirm current exam details on Microsoft Learn \u2014 the outline moves."""

M5_NOAH = """Noah probes mastery with questions like:
- In one sentence, what is the deliverable I\u2019m producing by the end of this module?
- *Query drill:* \u201cNoah gives you a hunting goal \u2014 top processes spawning cmd.exe. Talk Noah through the KQL shape before you write it: which table, which filter, which aggregation.\u201d
- Your playbook fires on every benign admin logon. Walk Noah through the tuning fix from the Hands-on procedure \u2014 rule-side, not playbook-side \u2014 and explain why.
- *Honesty check:* Copilot suggests isolating the domain controller mid-incident. What do you verify first, and what happens if you click without verifying?"""

M5_QUIZ_EXTRA = [
    {"q": "CEF and Syslog connectors exist so Sentinel can ingest\u2026",
     "choices": ["only Microsoft logs", "firewall, proxy, and third-party appliance logs into the workspace", "emails", "nothing \u2014 they\u2019re deprecated"],
     "answer": 1,
     "explain": "CEF/Syslog are the on-ramps for non-Microsoft security appliances \u2014 the data-connector concept from the Concepts section."},
    {"q": "An NRT analytics rule differs from a scheduled rule in that it\u2026",
     "choices": ["runs monthly", "evaluates near-real-time for urgent detections that can\u2019t wait for the schedule", "needs no KQL", "is free"],
     "answer": 1,
     "explain": "NRT is for the urgent tier; scheduled KQL is the workhorse. Covered in the Concepts section."},
    {"q": "A Logic Apps playbook in Sentinel typically runs which sequence?",
     "choices": ["notify, then investigate", "enrich the incident, then act (isolate, revoke), then notify", "delete the workspace", "email everyone first"],
     "answer": 1,
     "explain": "Enrich \u2192 act \u2192 notify is the SOAR-without-the-buzzword flow from the Concepts section."},
    {"q": "In KQL, summarize ... by bin(TimeGenerated, 1h) is used to\u2026",
     "choices": ["delete old data", "bucket events into hourly windows to spot beaconing and bursts on a timeline", "rename tables", "export to CSV"],
     "answer": 1,
     "explain": "Time-bucketing reveals periodicity \u2014 the hunting query shape from the Hands-on procedure."},
]

# ------------------------------------------------- polished quiz explains
# keyed by module id -> list index -> new explain (references module's own sections)
EXPLAINS = {
    "il06-hackers-arise": [
        "Passive reconnaissance comes first: silent, authorized-safe, and it often reveals the attack path. The Hands-on procedure runs passive before active.",
        "Rule-based cracking multiplies the wordlist; target-aware rules beat raw size. The Concepts section\u2019s hash-identification entry.",
        "Crack offline against your own lab handshake \u2014 the authorized workflow from the Hands-on procedure. Then enable WPA3 and PMF, per the Project brief\u2019s defense column.",
        "Prove impact minimally, document, report \u2014 scope is the law. The Concepts section\u2019s documentation discipline.",
        "Modbus is unauthenticated by design \u2014 defense is segmentation and monitoring, never patching the protocol. The Concepts section, with the air-gapped-lab rule.",
        "PD is Protection and Defense \u2014 the blue-team workforce roles in the NICE Framework. The Concepts section.",
    ],
    "il06-offensive": [
        "Enumeration discipline from the Hands-on procedure: the unexamined service is where the vulnerability lives \u2014 one host deeply before ten shallowly.",
        "Accounts with Kerberos pre-authentication disabled \u2014 request the AS-REP, crack offline, harden by enabling pre-auth. The Concepts section.",
        "Long random service passwords plus AES, with 4769 anomaly monitoring \u2014 every attack paired with its detection, the Hands-on procedure\u2019s rule.",
        "Potential code execution via gadget chains \u2014 never deserialize untrusted input. The Concepts section.",
        "Anomalous ticket lifetimes and encryption types betray forged tickets \u2014 every AD attack has a detection. The Concepts section.",
        "Burned credibility at retest \u2014 risk rating is likelihood \u00d7 impact, stated honestly. The Project brief\u2019s honesty rules.",
    ],
    "il06-defensive": [
        "The account-takeover pattern \u2014 escalate immediately; speed is the L1 metric. The Hands-on procedure\u2019s triage drill.",
        "Contain first while scope is unknown \u2014 eradication before containment lets attackers re-seed. The IR lifecycle in the Concepts section.",
        "Tune with baseline, threshold, and allowlist \u2014 document the change. The Hands-on procedure\u2019s tuning step.",
        "Regular intervals plus consistent sizes (and odd JA3) confirm the beacon pattern \u2014 network forensics in the Concepts section.",
        "Close the blind spot: you can\u2019t detect what you don\u2019t log \u2014 the logging roadmap in the Concepts section.",
        "Blameless culture violated \u2014 fix the system, not the person, or the next incident hides. The Concepts section.",
    ],
    "il06-fde-interface": [
        "Their constraints rule: build offline, auditable, and transferable \u2014 the FDE role in the Concepts section.",
        "The model drafts, the analyst decides \u2014 verify every AI output before action. The Concepts section\u2019s verification discipline.",
        "New data flow, new model session \u2014 models rot like milk, not wine. The Hands-on procedure\u2019s scoping step.",
        "Repudiation \u2014 counter disputed actions with signed logs and audit trails. The Concepts section\u2019s STRIDE entry.",
        "Findings with fixes plus SLAs by severity \u2014 the review that unblocks. The Hands-on procedure\u2019s review step.",
    ],
    "il06-azure-soc": [
        "Connector \u2192 analytics rule \u2192 playbook: the Sentinel pipeline from the Concepts section \u2014 connector first, rule second.",
        "Filter, aggregate, rank \u2014 the KQL pipe shape from the Hands-on procedure. Read the KQL before the answers.",
        "Triage by blast radius and stage \u2014 the queue-triage motion in the Concepts section.",
        "Verify the hypothesis first \u2014 the AI discipline from the Concepts section applies to infrastructure-critical actions.",
        "Hunt and write detections for the gap techniques \u2014 the ATT&CK mapping step in the Hands-on procedure.",
        "Tune the analytics rule \u2014 automation amplifies signal and noise alike. The Hands-on procedure\u2019s playbook step.",
    ],
}

# ------------------------------------------------- terminal sims
# Shape mirrors the template (id/title/brief/prompt/commands[{cmd,out}]); the
# renderer (course-shell.js buildTermPane) consumes these generically.
TERMINAL_SIMS = [
    {
        "id": "il06-recon-cli",
        "title": "Attacker Linux & Recon CLI simulator",
        "brief": "Practice the Module 1 command set \u2014 bash pipelines, scanning, passive recon \u2014 against the fictional lab target target.lab. All outputs are simulated practice data.",
        "prompt": "attacker@il:~$",
        "commands": [
            {"cmd": "pwd", "out": "/home/attacker"},
            {"cmd": "ls", "out": "findings.md  recon/  scans/  wordlists/"},
            {"cmd": "cat findings.md", "out": "target: target.lab (lab-owned)\npassive done: crt.sh names, DNS, WHOIS\nnext: SYN scan, then service detection"},
            {"cmd": "nmap -sS target.lab", "out": "Starting Nmap (simulated)\nPORT    STATE SERVICE\n22/tcp  open  ssh\n80/tcp  open  http\n443/tcp open  https\n445/tcp open  smb\nDone: 4 open ports (SYN scan, half-open)"},
            {"cmd": "nmap -sV target.lab", "out": "PORT    STATE SERVICE VERSION\n22/tcp  open  ssh     OpenSSH (lab build)\n80/tcp  open  http    nginx (lab build)\n443/tcp open  https   nginx (lab build)\n445/tcp open  smb     Samba (lab build)\nService detection performed. Report to findings.md."},
            {"cmd": "nmap -sU target.lab", "out": "PORT    STATE SERVICE\n53/udp  open  dns\n161/udp open  snmp\nUDP scan complete: slow, but UDP hides real vulnerabilities."},
            {"cmd": "dig target.lab +short", "out": "10.10.10.5"},
            {"cmd": "dig target.lab MX +short", "out": "10 mail.target.lab."},
            {"cmd": "whois target.lab", "out": "Domain: target.lab (LAB FIXTURE \u2014 simulated output)\nRegistrar: Example Lab Registrar\nCreated: 2026-01-01"},
            {"cmd": "nmap -sV target.lab | grep open", "out": "22/tcp  open  ssh     OpenSSH (lab build)\n80/tcp  open  http    nginx (lab build)\n443/tcp open  https   nginx (lab build)\n445/tcp open  smb     Samba (lab build)"},
            {"cmd": "nmap -sV target.lab | grep open | cut -d' ' -f1 | sort -u", "out": "22/tcp\n443/tcp\n445/tcp\n80/tcp"},
            {"cmd": "airodump-ng wlan0mon", "out": "BSSID              CH  ENC   ESSID\nAA:BB:CC:11:22:33  6   WPA2  LAB-AP (your own access point)\nCapturing handshakes on your own AP only."},
            {"cmd": "echo $SHELL", "out": "/bin/bash"},
            {"cmd": "sha256sum findings.md", "out": "9f2c...a41b  findings.md   (hash everything: chain of custody starts here)"},
        ],
    },
    {
        "id": "il06-kql-hunt",
        "title": "KQL Hunting simulator",
        "brief": "Practice Module 5 KQL hunt patterns \u2014 filter, aggregate, rank, time-bucket \u2014 against the fictional Sentinel workspace contoso-sec. All results are simulated practice data.",
        "prompt": "analyst@il:~$",
        "commands": [
            {"cmd": "SecurityEvent | where EventID == 4688 | summarize count() by Process | top 5 by count_", "out": "Process            count_\nconhost.exe        18412\nsvchost.exe        12004\npowershell.exe       312\ncmd.exe              188\nwmiprvse.exe          96"},
            {"cmd": "SecurityEvent | where Process has \"cmd.exe\" | summarize count() by ParentProcessName | top 10 by count_", "out": "ParentProcessName  count_\nexplorer.exe        141\npowershell.exe        32\nwinword.exe            3   <-- investigate: Office spawning shells\nwmiprvse.exe           2"},
            {"cmd": "SigninLogs | where ResultType == 0 | summarize count() by UserPrincipalName | top 5 by count_", "out": "UserPrincipalName        count_\nana@contoso-sec.lab      412\nben@contoso-sec.lab      388\nsvc-backup               96\nana@contoso-sec.lab ... impossible-travel candidate flagged in next hunt"},
            {"cmd": "SecurityEvent | where EventID == 4688 | summarize count() by bin(TimeGenerated, 1h)", "out": "TimeGenerated        count_\n2026-10-07T06:00Z    2104\n2026-10-07T07:00Z    2211\n2026-10-07T08:00Z    8931  <-- burst: investigate\n2026-10-07T09:00Z    2187"},
            {"cmd": "DeviceProcessEvents | where FileName == \"powershell.exe\" | where ProcessCommandLine contains \"-EncodedCommand\" | project TimeGenerated, DeviceName, AccountName", "out": "TimeGenerated        DeviceName   AccountName\n2026-10-07T08:14Z  WS-1142      TEMP\\jdoe\n2026-10-07T08:31Z  WS-1142      TEMP\\jdoe\nHypothesis confirmed: encoded PowerShell on WS-1142. Escalate to incident."},
        ],
    },
]

MODULE_ORDER = ["il06-hackers-arise", "il06-offensive", "il06-defensive", "il06-fde-interface", "il06-azure-soc"]
CONTENT = {
    "il06-hackers-arise":   {"summary": M1_SUMMARY, "concepts": M1_CONCEPTS, "hands_on": M1_HANDS_ON, "project": M1_PROJECT, "noah": M1_NOAH, "quiz_extra": M1_QUIZ_EXTRA, "weight": 1},
    "il06-offensive":       {"summary": M2_SUMMARY, "concepts": M2_CONCEPTS, "hands_on": M2_HANDS_ON, "project": M2_PROJECT, "noah": M2_NOAH, "quiz_extra": M2_QUIZ_EXTRA, "weight": 2},
    "il06-defensive":       {"summary": M3_SUMMARY, "concepts": M3_CONCEPTS, "hands_on": M3_HANDS_ON, "project": M3_PROJECT, "noah": M3_NOAH, "quiz_extra": M3_QUIZ_EXTRA, "weight": 2},
    "il06-fde-interface":   {"summary": M4_SUMMARY, "concepts": M4_CONCEPTS, "hands_on": M4_HANDS_ON, "project": M4_PROJECT, "noah": M4_NOAH, "quiz_extra": M4_QUIZ_EXTRA, "weight": 1},
    "il06-azure-soc":       {"summary": M5_SUMMARY, "concepts": M5_CONCEPTS, "hands_on": M5_HANDS_ON, "project": M5_PROJECT, "noah": M5_NOAH, "quiz_extra": M5_QUIZ_EXTRA, "weight": 1},
}

def main():
    with open(PATH, encoding="utf-8") as f:
        doc = json.load(f)  # BEFORE
    assert [m["id"] for m in doc["modules"]] == MODULE_ORDER, "module order changed!"

    for m in doc["modules"]:
        c = CONTENT[m["id"]]
        m["weight"] = c["weight"]
        m["summary"] = c["summary"]
        m["notes"] = [
            {"title": "Concepts", "body": c["concepts"]},
            {"title": "Hands-on procedure", "body": c["hands_on"]},
            {"title": "Project brief", "body": c["project"]},
            {"title": "Noah check-in", "body": c["noah"]},
        ]
        # objectives/cards preserved as-is
        new_explains = EXPLAINS[m["id"]]
        assert len(new_explains) == len(m["quiz"]), f"explain count mismatch for {m['id']}"
        for i, q in enumerate(m["quiz"]):
            q["explain"] = new_explains[i]
        m["quiz"] = m["quiz"] + c["quiz_extra"]

    # insert terminalSims right after trainers (mirrors template key order)
    assert "terminalSims" not in doc
    keys = list(doc.keys())
    out = {}
    for k in keys:
        out[k] = doc[k]
        if k == "trainers":
            out["terminalSims"] = TERMINAL_SIMS
    doc = out

    # ---------------- validation ----------------
    assert set(doc.keys()) >= {"schemaVersion","courseId","code","title","tagline","blurb","hours","updatedAt",
        "objectives","arc","priorities","battlePlan","modules","scriptLabs","drills","scenarios","trainers",
        "terminalSims","mockMinutes","mockTasks","cheatSheets","answerBank","sourceLinks","honestyNote"}
    assert isinstance(doc["mockMinutes"], int)
    gloss_re = re.compile("^- \\*\\*.+?\\*\\* — .+", re.M)
    whole = json.dumps(doc)
    for b in BANNED:
        assert not re.search(r"\b" + re.escape(b) + r"\b", whole, re.I), f"banned brand: {b}"
    for b in FORBIDDEN:
        assert not re.search(r"\b" + re.escape(b) + r"\b", whole, re.I), f"forbidden term: {b}"
    for m in doc["modules"]:
        assert set(m.keys()) >= {"id","code","title","weight","summary","objectives","notes","cards","quiz"}, m["id"]
        assert isinstance(m["weight"], int)
        assert m["summary"].startswith("Welcome") and "instructor" in m["summary"], m["id"]
        assert [n["title"] for n in m["notes"]] == ["Concepts","Hands-on procedure","Project brief","Noah check-in"], m["id"]
        lines = [l for l in m["notes"][0]["body"].split("\n") if l.strip()]
        assert lines and all(gloss_re.match(l) for l in lines), f"glossary shape broken in {m['id']}"
        assert re.search(r"^\d+\. \*\*.+\*\*", m["notes"][1]["body"], re.M), f"numbered steps missing in {m['id']}"
        assert len(m["cards"]) == 6 and all(c["front"].strip() and c["back"].strip() for c in m["cards"]), m["id"]
        assert len(m["quiz"]) == 10, f"{m['id']}: quiz={len(m['quiz'])}"
        for q in m["quiz"]:
            assert len(q["choices"]) == 4, m["id"]
            assert isinstance(q["answer"], int) and 0 <= q["answer"] < 4, m["id"]
            assert q["explain"].strip(), m["id"]
        assert len(m["objectives"]) >= 4, m["id"]
    for s in doc["terminalSims"]:
        assert set(s.keys()) == {"id","title","brief","prompt","commands"}, s["id"]
        assert all(set(c.keys()) == {"cmd","out"} and c["cmd"].strip() and c["out"].strip() for c in s["commands"])
    for t in doc["mockTasks"]:
        assert t["id"] and t["type"], t
        if t["type"] == "choice":
            assert len(t["choices"]) == 4 and 0 <= t["answer"] < 4 and t["explain"].strip()
        else:  # code: renderer-supported shape (prompt/starter), kept from original
            assert t.get("prompt","").strip() and t.get("starter","").strip()
    for sl in doc["sourceLinks"]:
        assert sl.get("retrieved","").strip(), sl["name"]

    # ---------------- atomic write ----------------
    tmp = PATH + ".new"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(tmp, encoding="utf-8") as f:
        json.load(f)  # AFTER
    os.replace(tmp, PATH)
    print("OK: wrote", PATH, f"({os.path.getsize(PATH)} bytes)")
    for m in doc["modules"]:
        print(f"  {m['id']}: weight={m['weight']} notes=4 cards={len(m['cards'])} quiz={len(m['quiz'])}")

if __name__ == "__main__":
    main()
