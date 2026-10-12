#!/usr/bin/env python3
"""Fill il-29: 24 mockTasks + 4 scriptLabs + 4 scenarios + 2 trainers."""
import json, os

P = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-29-threatlocker-ai-cybersecurity-mastery.json')
d = json.load(open(P))

def T(i, q, choices, answer, explain):
    return {"id": f"IL29-MOCK-{i:02d}", "type": "choice",
            "q": q, "choices": choices, "answer": answer, "explain": explain}

TASKS = [
 T(1, "A workstation runs default-deny application control. A user double-clicks an unapproved installer. What happens?",
    ["The installer runs, but is sandboxed automatically.",
     "Execution is blocked and an event is logged; nothing runs until an explicit allow rule exists.",
     "The installer runs once, then is blocked on the second launch.",
     "Windows SmartScreen decides based on reputation."],
    1, "Deny-by-default means no allow rule, no execution \u2014 the block is the safe default and the log entry is the audit trail. Reputation-based second chances belong to allow-by-default antivirus thinking."),
 T(2, "Ringfencing in a zero-trust endpoint platform primarily restricts:",
    ["Which applications may execute at all.",
     "What an already-allowed application may do \u2014 its files, registry, network, and child processes.",
     "Which users may log on to the machine.",
     "The physical network ports on the switch."],
    1, "Allowlisting answers 'may it run'; ringfencing answers 'what may it touch'. A permitted browser that cannot spawn PowerShell or reach the LAN is a contained browser \u2014 least privilege applied to application behavior."),
 T(3, "Elevation Control handles a standard user's request for admin rights by:",
    ["Granting permanent local admin \u2014 it is faster.",
     "Applying just-in-time, scoped, audited elevation for the specific approved action, then removing it.",
     "Disabling UAC so prompts stop appearing.",
     "Adding the user to Domain Admins temporarily."],
    1, "Standing admin rights are the credential-theft jackpot. Elevation Control grants the minimum privilege for the approved task, logs it, and takes it back \u2014 JIT administration instead of permanent privilege."),
 T(4, "Storage Control blocks an unauthorized USB drive. The security principle at work is:",
    ["Data-loss prevention at the removable-media boundary \u2014 unapproved devices never mount.",
     "Antivirus scanning of the drive's contents.",
     "Encrypting the drive automatically.",
     "Backing up the drive before allowing access."],
    0, "If the device never mounts, nothing exfiltrates and nothing infects via autorun-style vectors. Blocking at the mount point is prevention; scanning after mount is detection hoping to be fast enough."),
 T(5, "ThreatLocker Detect complements allowlisting by:",
    ["Replacing application control entirely.",
     "Providing EDR-style behavioral detection and response on top of the deny-by-default baseline \u2014 telemetry, alerting, and triage for what the controls observe.",
     "Scanning email attachments only.",
     "Managing firewall rules on the perimeter."],
    1, "Controls prevent; Detect observes and responds. The layered story: allowlisting stops the unknown binary, ringfencing contains the allowed one, and Detect gives the analyst the telemetry to hunt what slipped between the controls."),
 T(6, "A classic stack buffer overflow lets an attacker overwrite the saved return address. The fundamental fix class is:",
    ["Faster CPUs so the overflow cannot keep up.",
     "Memory safety \u2014 bounds checking, safe languages, or hardware enforcement (e.g., stack canaries as mitigation, not fix).",
     "Longer passwords on the affected service.",
     "Blocking the attacker's IP at the firewall."],
    1, "Control hijacking is a memory-safety failure: the attacker redirects control flow by corrupting code pointers. The fix is making the corruption impossible (bounds checks, safe languages); canaries and ASLR only raise the cost."),
 T(7, "Privilege separation (as in OpenSSH's design) means:",
    ["Running everything as root for simplicity.",
     "Splitting the program so the privileged part is tiny and the bulk of the code runs unprivileged \u2014 a compromise of the bulk cannot directly yield privilege.",
     "Requiring two passwords for every login.",
     "Encrypting all inter-process communication."],
    1, "The 6.858 lesson: shrink the trusted computing base. A small, auditable privileged monitor plus unprivileged workers means the attacker's foothold starts without the keys to the kingdom."),
 T(8, "Sandboxing an untrusted renderer process primarily defends against:",
    ["Phishing emails reaching the inbox.",
     "A compromised renderer escaping to the rest of the system \u2014 the sandbox confines the blast radius of an exploited component.",
     "Weak user passwords.",
     "DDoS against the web server."],
    1, "Assume the parser will fall: sandboxing puts the fall inside a box with no filesystem, no network, and a narrow IPC broker. Chrome's multi-process architecture is the canonical example."),
 T(9, "TLS protects data in transit against eavesdropping and tampering. It does NOT protect against:",
    ["A passive network sniffer reading the plaintext.",
     "A compromised endpoint or a malicious insider with legitimate access \u2014 TLS ends at the endpoints.",
     "An active MITM during the handshake (given valid PKI).",
     "Downgrade to plaintext by a middlebox."],
    1, "Cryptography secures the channel, not the endpoints. If the endpoint is owned \u2014 malware, malicious insider, compelled access \u2014 TLS delivers the attacker's data faithfully and confidentially."),
 T(10, "A timing side channel leaks a secret because:",
    ["The encryption algorithm is mathematically broken.",
     "The implementation's runtime varies with secret data (e.g., early-exit comparisons), letting an observer infer the secret from duration.",
     "The key is too short.",
     "The network is too slow."],
    1, "Side channels attack the implementation, not the math: secret-dependent branches, cache lines, or timing turn physical behavior into an oracle. Constant-time code and blinding are the defenses."),
 T(11, "Passkeys improve on passwords primarily because:",
    ["They are longer strings the user memorizes.",
     "The private key never leaves the device and authentication is bound to the origin \u2014 phishing a passkey means stealing the device, not tricking the user into typing a secret.",
     "They expire every 90 days.",
     "They are stored in the browser's password manager as text."],
    1, "Passwords are phishable shared secrets; passkeys are origin-bound public-key credentials. The server holds only a public key, so a breached database yields nothing reusable and a fake login page gets nothing to replay."),
 T(12, "An LLM agent with email-tool access receives a message containing hidden instructions to forward all mail to an attacker. This is:",
    ["A bug in the email client.",
     "Indirect prompt injection \u2014 untrusted data treated as instructions; the fix is a data/instruction boundary (tool-output sanitization, confirmation for sensitive actions, least-privilege tool scopes).",
     "A normal feature of email.",
     "Solved by a longer system prompt."],
    1, "The model cannot natively distinguish 'text to summarize' from 'orders to obey'. Agents must treat tool outputs as data, confirm destructive actions, and scope tools to least privilege \u2014 prompt wording alone is not a boundary."),
 T(13, "In AI supply chain security, model poisoning means:",
    ["The GPU overheating during training.",
     "An attacker corrupting training data or the model artifact so the deployed model misbehaves on trigger inputs \u2014 defend with provenance, dataset hygiene, and artifact signing.",
     "Using too small a model.",
     "Forgetting to set a random seed."],
    1, "The model is software: whoever controls its training data or its weights controls its behavior. Provenance attestation and signed artifacts move 'trust the model' from faith to verification."),
 T(14, "An adversarial evasion attack against an ML malware classifier works by:",
    ["Deleting the classifier's training data.",
     "Crafting inputs with small perturbations that cross the model's decision boundary while looking benign to humans.",
     "Unplugging the inference server.",
     "Training a better classifier."],
    0, "Evasion exploits the gap between human and model perception: imperceptible changes flip the prediction. Defenses (adversarial training, input validation, ensemble + non-ML controls) raise cost but the arms race is structural."),
 T(15, "NIST SP 800-61's incident response lifecycle order is:",
    ["Eradication, detection, recovery, lessons learned.",
     "Preparation; detection and analysis; containment, eradication, and recovery; post-incident activity.",
     "Recovery first, then figure out what happened.",
     "Detection, prosecution, preparation."],
    1, "You cannot contain what you have not detected, and you must not eradicate before you understand scope \u2014 premature cleanup destroys forensic evidence. Preparation (playbooks, contacts, tooling) is phase zero."),
 T(16, "Per the order of volatility, you collect this FIRST from a live compromised host:",
    ["The disk image \u2014 it holds everything.",
     "Memory (RAM) contents and other ephemeral state: registers, cache, process table, network connections \u2014 gone at power-off.",
     "The backup tapes.",
     "The firewall logs from last month."],
    1, "Volatile first: RAM, process state, live network connections evaporate on shutdown. Image memory before you touch the disk; every reboot is evidence destruction you chose."),
 T(17, "In MITRE ATT&CK, the difference between a tactic and a technique is:",
    ["There is none \u2014 the terms are interchangeable.",
     "A tactic is the adversary's goal (the 'why': e.g., Persistence); a technique is how they achieve it (e.g., Scheduled Task). Procedures are the specific implementations.",
     "Tactics are defensive, techniques are offensive.",
     "Techniques are only for malware."],
    1, "Tactic = objective (Initial Access, Exfiltration); technique = method (Phishing, Scheduled Task/Job); procedure = the concrete variant. Mapping detections to techniques is how you measure coverage honestly."),
 T(18, "The most effective single control against credential phishing is:",
    ["Longer password complexity rules.",
     "Phishing-resistant MFA (FIDO2/passkeys) \u2014 the stolen password alone is useless without the hardware-bound second factor.",
     "Monthly security awareness slides.",
     "Blocking all external email."],
    1, "Awareness helps; architecture decides. SMS/TOTP codes are phishable in real time \u2014 only origin-bound, hardware-backed factors (FIDO2) break the credential-replay chain that phishing depends on."),
 T(19, "The 'weakest link' insight of security economics says defenders should:",
    ["Spend equally on all controls.",
     "Find the cheapest attack path the adversary actually uses and raise its cost first \u2014 attackers, like water, take the path of least resistance.",
     "Buy the most expensive firewall.",
     "Focus only on zero-days."],
    1, "Security is a weakest-link game: the attacker picks your cheapest failure. Economics beats maximalism \u2014 measure where attacks actually land (phishing, unpatched edge, misconfig) and spend there first."),
 T(20, "In ThreatLocker portal administration, least privilege means an analyst role should:",
    ["Be a Global Admin so nothing ever blocks their work.",
     "Hold only the permissions its duties require \u2014 e.g., view policies and approve requests, not edit global defaults \u2014 with sensitive actions logged and reviewable.",
     "Share one admin account for the whole team.",
     "Have no access at all, for safety."],
    1, "Admin consoles are high-value targets: role-based access with minimum necessary permissions, individual accounts, and audit logging turn the portal from a single point of compromise into a governed control plane."),
 T(21, "A legitimate line-of-business app is blocked by the new allowlist policy on Monday morning. Your FIRST step as the Cyber Hero on shift is:",
    ["Disable application control org-wide until the complaints stop.",
     "Confirm scope and business impact, check the block event details, and route an emergency approval or targeted exception \u2014 restore the user fast without dismantling the control.",
     "Tell the user to work from home.",
     "Reinstall the application."],
    1, "Break-fix discipline: restore the user through the control (scoped exception/approval), never by deleting the control. The block event tells you exactly which rule fired \u2014 read it before you act."),
 T(22, "Detect raises a high-severity alert: a signed binary spawning PowerShell with encoded commands. Your triage priority is:",
    ["Close the alert \u2014 the binary is signed.",
     "Treat signature as one signal, not a verdict: isolate the host, capture process tree and command line, and check the binary's reputation and parent chain \u2014 signed malware and LOLBins are routine.",
     "Email the user asking if they ran something.",
     "Wait for a second alert to confirm."],
    1, "Signed does not mean benign \u2014 stolen certs and living-off-the-land binaries are standard tradecraft. Isolate first (containment beats curiosity), then investigate the process tree; the encoded command line is the tell."),
 T(23, "A user reports their files renamed with a ransom note. The FIRST containment action is:",
    ["Pay the ransom quickly to limit damage.",
     "Isolate the host from the network (keep it powered for forensics), then identify patient zero and scope before eradication.",
     "Delete the ransom note.",
     "Reboot into safe mode and keep working."],
    1, "Containment before eradication, and never pay as a first move: isolate (network, not power \u2014 memory holds evidence), scope the blast radius, preserve forensics, then eradicate and recover from known-clean backups."),
 T(24, "The panel asks: 'Sell me zero trust in 60 seconds.' The structure that scores is:",
    ["A 60-second recitation of the NIST 800-207 abstract.",
     "Problem (perimeter assumed trusted insiders) \u2192 principle (never trust, always verify; deny by default) \u2192 mechanism (identity, device, allowlisting, microsegmentation) \u2192 outcome (breach contained to one identity, one device).",
     "A story about a firewall you once configured.",
     "Listing every ThreatLocker feature alphabetically."],
    1, "Sixty seconds rewards structure, not completeness: problem, principle, mechanism, outcome. Name the nouns (identity, device, least privilege, deny-by-default) and land on the business result \u2014 smaller blast radius."),
]

LABS = [
 {"id": "lab-powershell-triage", "title": "PowerShell Triage Collector",
  "brief": "Write a PowerShell script that collects the first-response artifact set from a Windows host: running processes with command lines, established network connections with owning PIDs, autorun persistence points, and recently modified executables \u2014 all into a timestamped folder.",
  "starter": "# Triage collector \u2014 fill in each TODO section\n$outDir = \"C:\\Triage\\$(Get-Date -Format 'yyyyMMdd-HHmmss')\"\nNew-Item -ItemType Directory -Path $outDir | Out-Null\n\n# TODO 1: export Get-Process with Id, ProcessName, Path, CommandLine to processes.csv\n\n# TODO 2: export Get-NetTCPConnection (State=Established) joined to owning process names to net.csv\n\n# TODO 3: enumerate HKLM/HKCU Run keys + Startup folders to persistence.csv\n\n# TODO 4: list .exe files under C:\\Users modified in the last 7 days to newbinaries.csv\n\nWrite-Host \"Triage bundle written to $outDir\"",
  "required": "Four CSVs in the timestamped folder: processes.csv (with command lines), net.csv (established connections mapped to process names), persistence.csv (Run keys + Startup), newbinaries.csv (recent executables) \u2014 the script must run without elevation errors on missing keys."},
 {"id": "lab-python-detect-parser", "title": "Detect Alert Summarizer",
  "brief": "Given a CSV export of ThreatLocker Detect alerts (timestamp, host, severity, tactic, technique, process), write a Python script that prints: alert counts by severity, the top 5 MITRE techniques, and the hosts with the most high-severity alerts.",
  "starter": "import csv, sys\nfrom collections import Counter\n\n# TODO 1: read the CSV path from sys.argv[1] with csv.DictReader\n\n# TODO 2: count alerts by severity -> Counter\n\n# TODO 3: count MITRE techniques, print the top 5\n\n# TODO 4: for severity == 'High', count by host and print the top hosts\n\n# Expected output sections: 'BY SEVERITY', 'TOP TECHNIQUES', 'HOTTEST HOSTS'",
  "required": "Running `python summarizer.py alerts.csv` prints three labeled sections with correct counts; the script handles a missing file with a usage message instead of a traceback."},
 {"id": "lab-allowlist-policy", "title": "Allowlist Policy Generator",
  "brief": "From an application inventory CSV (path, publisher, hash, install_date), generate a deny-by-default allowlist policy JSON: allow rules for publishers with 2+ installed apps, per-hash rules for the rest, and a report of unsigned binaries needing review.",
  "starter": "import csv, json, sys\nfrom collections import Counter\n\n# TODO 1: load inventory rows; group by publisher\n\n# TODO 2: publishers with >= 2 apps -> {'type': 'publisher', 'name': ...} rules\n\n# TODO 3: remaining apps -> {'type': 'hash', 'sha256': ...} rules\n\n# TODO 4: rows with empty publisher -> review list\n\n# TODO 5: write {'default': 'deny', 'rules': [...]} to policy.json and print the review list",
  "required": "policy.json contains a default-deny policy with publisher rules and hash rules, and the script prints the unsigned-binary review list \u2014 no app from the inventory is silently dropped."},
 {"id": "lab-incident-timeline", "title": "Incident Timeline Builder",
  "brief": "Given mixed log lines (timestamps in two formats plus free text), build a normalized incident timeline: parse, sort chronologically, and print a clean time/action/source table for the incident report.",
  "starter": "import re, sys\nfrom datetime import datetime\n\nFORMATS = ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %I:%M %p']\n# TODO 1: read lines from sys.argv[1]; extract a timestamp with regex per line\n\n# TODO 2: try each FORMAT until one parses; skip lines with no timestamp (count them)\n\n# TODO 3: sort events chronologically\n\n# TODO 4: print 'YYYY-MM-DD HH:MM:SS | source | message' rows, then the skipped-line count",
  "required": "The timeline prints in chronological order across both timestamp formats, skipped lines are counted and reported, and the output is directly pastable into the incident report's timeline table."},
]

SCENARIOS = [
 {"id": "scenario-2am-triage", "title": "2 AM: The Ransomware Call",
  "context": "02:14 AM. The on-call phone rings: a 60-user site reports files renaming with a ransom note on three machines. You are the Cyber Hero on shift. This scenario tests IR discipline under pressure \u2014 containment before eradication, evidence before cleanup.",
  "steps": [
   {"prompt": "Your first three actions, in order?",
    "options": [
     {"text": "Isolate the affected hosts from the network (leave powered on), confirm the scope via Detect/EDR, and escalate per the playbook.", "correct": True, "why": "Containment first, but network-only \u2014 memory holds forensic evidence. Scope before eradication."},
     {"text": "Immediately reimage the three machines to stop the spread.", "correct": False, "why": "Eradication before scoping destroys evidence and you will miss patient zero and persistence."},
     {"text": "Pay the ransom \u2014 it is 2 AM and speed matters.", "correct": False, "why": "Payment funds the adversary, rarely restores everything, and skips the entire IR process."},
     {"text": "Shut everything down site-wide to be safe.", "correct": False, "why": "Indiscriminate shutdown destroys volatile evidence across clean machines and maximizes business damage."}]},
   {"prompt": "You find the entry vector: a phishing macro, plus a scheduled-task persistence mechanism. Before eradicating, you:",
    "options": [
     {"text": "Preserve memory and disk images of patient zero, document the persistence mechanism, then eradicate.", "correct": True, "why": "Forensics before cleanup \u2014 you need the how for the report and to be sure eradication is complete."},
     {"text": "Delete the scheduled task and move on \u2014 the vector is obvious.", "correct": False, "why": "'Obvious' is how second persistence mechanisms survive. Document, then eradicate, then verify."},
     {"text": "Email the whole company about the phishing email immediately.", "correct": False, "why": "Notification matters, but mid-incident it tips off no one useful and distracts the response."}]},
   {"prompt": "Recovery: the 2 AM backup is clean; the last user file changes were at 6 PM. You:",
    "options": [
     {"text": "Restore from the 2 AM backup, verify integrity on a sample, and declare the 2 AM\u20136 PM window as the data-loss interval in the report.", "correct": True, "why": "Honest RPO: the loss window is stated plainly so the business can re-create the work \u2014 no silent gaps."},
     {"text": "Restore and tell users nothing was lost.", "correct": False, "why": "The 2 AM\u20136 PM gap is real; hiding it guarantees the business discovers it from an angry user."}]}]},
 {"id": "scenario-blocked-lob-app", "title": "Monday 9 AM: The Blocked Line-of-Business App",
  "context": "The new allowlist policy went live overnight. Forty accountants cannot open the invoicing app \u2014 the exact scenario that gets security projects killed. This tests break-fix discipline: restore the user through the control, never by deleting it.",
  "steps": [
   {"prompt": "First, you check:",
    "options": [
     {"text": "The block event details: which rule fired, the file hash, the publisher, and how many hosts are affected.", "correct": True, "why": "The event tells you exactly what the policy saw \u2014 scope and cause in one read."},
     {"text": "Whether the policy can be disabled org-wide quickly.", "correct": False, "why": "Disabling the control 'temporarily' is how temporary becomes permanent \u2014 and unlogged."},
     {"text": "The vendor's support line.", "correct": False, "why": "The vendor did not block the app; your policy did. The answer is in your console."}]},
   {"prompt": "The app is legitimate, signed by a known publisher, missed in the inventory. You:",
    "options": [
     {"text": "Issue a scoped publisher-or-hash approval for the app, document the exception, and add the publisher to the next inventory review.", "correct": True, "why": "Restore through the control: targeted approval, documented, with a process fix so it does not recur."},
     {"text": "Tell finance to wait for the next policy review cycle.", "correct": False, "why": "Business-stopping blocks get emergency handling \u2014 the process must have a fast lane."},
     {"text": "Approve the file hash only, on every host, manually.", "correct": False, "why": "Per-host manual approvals do not scale and leave no auditable policy \u2014 use the policy engine."}]}]},
 {"id": "scenario-phishing-credential-theft", "title": "The Clicked Link: Credential Phishing Triage",
  "context": "A user reports clicking a 'password expiry' link 20 minutes ago and entering credentials. The domain is a fresh lookalike. This tests account-containment sequencing.",
  "steps": [
   {"prompt": "Order of operations:",
    "options": [
     {"text": "Force password reset + revoke sessions, check mailbox rules for forwarding, then reimage/verify the endpoint.", "correct": True, "why": "Account first (the credential is live), then mailbox persistence, then endpoint \u2014 in the order the attacker monetizes."},
     {"text": "Reimage the endpoint first, then deal with the account.", "correct": False, "why": "While you reimage, the stolen credential is being used \u2014 the account is the bleeding artery."},
     {"text": "Monitor the account for a day to gather threat intel.", "correct": False, "why": "Watching an active compromise to 'learn' is negligence with extra steps."}]},
   {"prompt": "The mailbox has a new forwarding rule to an external address. This tells you:",
    "options": [
     {"text": "The attacker established persistence for BEC-style follow-on \u2014 remove it, check sent items, and expand the scope to the user's contacts.", "correct": True, "why": "Forwarding rules are the quiet persistence of credential phishing \u2014 the inbox keeps paying out after the password changes."},
     {"text": "The user set it up themselves and forgot.", "correct": False, "why": "External forwarding appearing with a phishing click is attacker tradecraft until proven otherwise."}]}]},
 {"id": "scenario-angry-lockout-call", "title": "The Angry Caller: Elevation Control Lockout",
  "context": "A department head calls the Cyber Hero line furious: Elevation Control blocked their software install 10 minutes before a client demo. This tests support under pressure \u2014 empathy plus control integrity.",
  "steps": [
   {"prompt": "Your opening move on the call:",
    "options": [
     {"text": "Acknowledge the urgency, verify their identity and the business need, then walk the approved emergency elevation path \u2014 never a permanent grant.", "correct": True, "why": "Empathy plus process: the demo matters AND the control stands. Emergency paths exist precisely for this call."},
     {"text": "Grant them local admin \u2014 the demo is more important than policy.", "correct": False, "why": "One permanent admin grant under pressure becomes the standing privilege the next attacker harvests."},
     {"text": "Quote the policy and end the call.", "correct": False, "why": "Correct policy, failed support \u2014 the user will now route around you, which is worse than the exception."}]},
   {"prompt": "After the demo, you:",
    "options": [
     {"text": "Review the emergency elevation in the audit log, confirm it was scoped and time-limited, and suggest a standing approval if the software is legitimate and recurring.", "correct": True, "why": "Close the loop: verify the exception behaved, then convert the recurring need into proper policy \u2014 the control learns."},
     {"text": "Forget it \u2014 the emergency is over.", "correct": False, "why": "Unexamined exceptions rot into shadow policy. The review is the job."}]}]},
]

TRAINERS = [
 {"id": "trainer-attack-recall", "title": "ATT&CK Tactic \u2192 Technique Recall",
  "brief": "Rapid-fire recall: given a tactic, name two techniques; given a technique, name its tactic. Builds the mapping fluency the Detect triage workflow and the panel both reward.",
  "kind": "custom"},
 {"id": "trainer-ir-sequencing", "title": "IR Order-of-Operations Recall",
  "brief": "Rapid-fire sequencing: given a scrambled set of response actions (isolate, image memory, scope, eradicate, recover, report), put them in NIST 800-61 order and justify each position. Builds the discipline that survives 2 AM.",
  "kind": "custom"},
]

d['mockTasks'] = TASKS
d['scriptLabs'] = LABS
d['scenarios'] = SCENARIOS
d['trainers'] = TRAINERS

with open(P, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')

d2 = json.load(open(P))
assert len(d2['mockTasks']) == 24, len(d2['mockTasks'])
assert len(d2['scriptLabs']) == 4
assert len(d2['scenarios']) == 4
assert len(d2['trainers']) == 2
for t in d2['mockTasks']:
    assert len(t['choices']) == 4 and 0 <= t['answer'] < 4, t['id']
    assert t['explain'] and t['q']
for s in d2['scenarios']:
    assert len(s['steps']) >= 2
    for st in s['steps']:
        assert any(o['correct'] for o in st['options'])
print('validated OK: 24 mockTasks / 4 scriptLabs / 4 scenarios / 2 trainers')
