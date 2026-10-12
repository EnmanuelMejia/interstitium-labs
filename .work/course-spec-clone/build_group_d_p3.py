# Part 3 — IL-24, IL-25 sections + build logic

IL24_BS = [
    {"id": "il24-bs-approve", "title": "Approve or deny: the unknown installer",
     "moduleId": "m24-approve-deny-ringfence", "start": "ticket",
     "nodes": {
         "ticket": {"text": "Ticket: a user requests approval for 'InvoiceViewer-Setup.exe', first seen today, unsigned, downloaded from a vendor portal. The vendor is legitimate but the binary is new. Disposition?",
                    "choices": [{"t": "Deny and investigate: unsigned, first-seen, no reputation — verify with the vendor first", "to": "deny"},
                                {"t": "Approve — the vendor is legitimate", "to": "approve"},
                                {"t": "Approve but ringfence it", "to": "ringfence"}]},
         "deny": {"text": "Correct operator instinct: default-deny means the burden of proof is on the binary. Verify the hash with the vendor, then approve the known-good version — not the unknown one.", "end": True},
         "approve": {"text": "The vendor's legitimacy doesn't transfer to an unsigned first-seen binary. Default-deny exists precisely for this ticket.", "end": True},
         "ringfence": {"text": "Ringfencing limits blast radius but still lets an unknown binary run — the wrong default for first-seen unsigned code. Deny first, verify, then approve.", "end": True}}},
    {"id": "il24-bs-ringfence", "title": "The macro that tried to escape",
     "moduleId": "m24-approve-deny-ringfence", "start": "alert",
     "nodes": {
         "alert": {"text": "Detect alert: winword.exe spawned powershell.exe with an encoded command line. The document came from an external sender. Ringfencing is on for Office. What contained it, and what do you do next?",
                   "choices": [{"t": "Ringfencing blocked the child-process spawn; isolate the host and pull the document for analysis", "to": "contain"},
                               {"t": "Allow it — the user needs the document", "to": "allow"},
                               {"t": "Delete the alert; ringfencing handled it", "to": "dismiss"}]},
         "contain": {"text": "Correct. The control did its job — now do yours: the alert is the start of the investigation, not the end. Isolate, collect, and trace how the document arrived.", "end": True},
         "allow": {"text": "An encoded PowerShell child of Word from an external document is the textbook malicious pattern. Need does not override the control.", "end": True},
         "dismiss": {"text": "The control firing is evidence of an attempt, not proof of safety. Every blocked attempt gets triaged.", "end": True}}},
    {"id": "il24-bs-elevation", "title": "The finance app wants admin",
     "moduleId": "m24-default-deny", "start": "request",
     "nodes": {
         "request": {"text": "The finance team's reporting tool requests elevation on every launch after its update. Users are blocked. The vendor says 'run as admin is required.' Least-privilege response?",
                    "choices": [{"t": "Create an elevation-control rule scoped to the exact binary hash and the specific actions it needs", "to": "scoped"},
                                {"t": "Give the finance group local admin", "to": "admin"},
                                {"t": "Tell them to wait for the vendor to fix it", "to": "wait"}]},
         "scoped": {"text": "Correct. Elevation control exists for exactly this: grant the minimum, to the verified binary, with the rule documented and reviewable. 'Vendor says admin' is not a security architecture.", "end": True},
         "admin": {"text": "Local admin for a whole group to fix one app's updater is the opposite of least privilege — and the next malware doesn't need to escalate.", "end": True},
         "wait": {"text": "The business is blocked now; the vendor's roadmap is not a control. Scope the elevation and move on.", "end": True}}},
    {"id": "il24-bs-soc", "title": "2 AM: the Detect queue",
     "moduleId": "m24-ai-aided-soc", "start": "queue",
     "nodes": {
         "queue": {"text": "Three Detect alerts in the queue: (1) known-good updater blocked by a new policy, (2) encoded PowerShell from Word, (3) a storage-control block on a USB drive. Triage order?",
                   "choices": [{"t": "(2), then (3), then (1) — malicious pattern first, exfiltration vector second, break-fix last", "to": "order"},
                               {"t": "(1) first — the user is blocked", "to": "user"},
                               {"t": "All three at once", "to": "all"}]},
         "order": {"text": "Correct triage order: active malicious pattern, then data-movement control, then the break-fix. Impact × likelihood, worked in order — that is the whole SOC discipline.", "end": True},
         "user": {"text": "The blocked updater is annoying; the encoded PowerShell may be an intrusion. Triage by risk, not by volume of complaints.", "end": True},
         "all": {"text": "You have one pair of hands. Order is the job.", "end": True}}},
]

IL24_CS = [
    {"id": "il24-cs-allowlist", "moduleId": "m24-default-deny", "tool": "ThreatLocker portal — policy workspace",
     "title": "Create an allowlist policy for a line-of-business app",
     "steps": [
         {"screen": "Portal dashboard; the Policies section lists the built-in default-deny baseline.",
          "action": "Create a new application policy scoped to the app's signed binary hash."},
         {"screen": "The policy editor shows file identity, publisher, and hash conditions.",
          "action": "Set the condition to the verified hash; add the publisher as a secondary condition."},
         {"screen": "Learning Mode data shows the app's normal child processes.",
          "action": "Review the observed behavior, then move the policy from Learning to Enforced."},
         {"screen": "The policy is live; test launches succeed and unknown binaries still block.",
          "action": "Document the approval in the change log with the ticket reference."}]},
    {"id": "il24-cs-ringfence", "moduleId": "m24-approve-deny-ringfence", "tool": "ThreatLocker portal — ringfencing",
     "title": "Ringfence a document reader",
     "steps": [
         {"screen": "The Ringfencing section lists applications with containment profiles.",
          "action": "Select the PDF reader and open its ringfence profile."},
         {"screen": "The profile shows permitted child processes, network access, and file writes.",
          "action": "Deny child-process creation and restrict writes to the user's documents folder."},
         {"screen": "Test: open a crafted PDF that tries to spawn a shell.",
          "action": "Confirm the spawn is blocked and the alert fires in Detect."}]},
    {"id": "il24-cs-elevation", "moduleId": "m24-default-deny", "tool": "ThreatLocker portal — elevation control",
     "title": "Scope an elevation rule for an updater",
     "steps": [
         {"screen": "Elevation Control lists applications requesting admin rights.",
          "action": "Find the updater binary and open its elevation request."},
         {"screen": "The request shows the binary hash and the actions it attempted.",
          "action": "Create a rule permitting elevation for that exact hash only, expiring at the next version."},
         {"screen": "The rule is active; the updater runs, and unrelated binaries still prompt.",
          "action": "Set a review date on the rule — standing elevation is not least privilege."}]},
    {"id": "il24-cs-detect", "moduleId": "m24-ai-aided-soc", "tool": "ThreatLocker portal — Detect",
     "title": "Triage a Detect alert end to end",
     "steps": [
         {"screen": "The Detect queue shows a new alert: suspicious child process.",
          "action": "Open the alert; read the process tree, command line, and file reputation."},
         {"screen": "The alert details show an unsigned binary with no publisher.",
          "action": "Pivot to the device timeline to see how the binary arrived."},
         {"screen": "The timeline shows a browser download from an ad domain.",
          "action": "Set disposition: deny and quarantine; open the follow-up ticket."}]},
]

IL24_SCRIPTLABS = [
    {"id": "il24-script-triage", "title": "PowerShell triage collector", "moduleId": "m24-endpoint-posture",
     "brief": ("Write a PowerShell script that collects the first-response artifact set from a Windows host: running "
               "processes with command lines, established network connections, and recently created executables. "
               "Original practice content for this course; run only against lab machines you own.")},
]
IL24_INSTALL = [
    {"id": "install-lab-vm", "title": "Build the Windows lab VM",
     "steps": ["Install a hypervisor (Hyper-V, VirtualBox, or VMware) on your machine.",
               "Create a Windows VM from official installation media with a trial/evaluation license.",
               "Snapshot the clean VM BEFORE installing any security tooling.", "Keep the VM host-only networked."],
     "verify": "The VM boots, snapshots exist, and it has no production data."},
    {"id": "install-test-network", "title": "Isolate the test network",
     "steps": ["Put the lab VM on a host-only network with no route to production.",
               "Verify isolation: the VM cannot reach your LAN.", "Document the lab network range."],
     "verify": "Ping from the lab VM to production addresses fails."},
]
IL24_INSTALL_ORDER = ["install-lab-vm", "install-test-network"]
IL24_XLINKS = {
    "m24-company-cold": ["IL29-M09"],
    "m24-star-operator": ["IL29-M10"],
    "m24-default-deny": ["IL29-M01", "IL29-M02"],
    "m24-approve-deny-ringfence": ["IL29-M02", "IL29-M03"],
    "m24-endpoint-posture": ["IL29-M05", "IL29-M06"],
    "m24-attack-graphs": ["IL29-M07"],
    "m24-graph-defense": ["IL29-M07"],
    "m24-ml-threat-defense": ["IL29-M07"],
    "m24-ueba": ["IL29-M07"],
    "m24-ai-agent-sec": ["IL29-M08"],
    "m24-ai-aided-soc": ["IL29-M07", "IL29-M10"],
    "m24-math-bayes": ["IL29-M01"],
    "m24-assessment-sim": ["IL29-M01"],
    "m24-capstone": ["IL29-M11"],
    "IL-24-PM-STATS": ["IL29-M01"],
    "IL-24-PM-LOGIC": ["IL29-M01"],
}

# ---------------------------------------------------------------- IL-25 sections
IL25_BS = [
    {"id": "il25-bs-phish", "title": "The invoice email",
     "moduleId": "IL25-M20", "start": "inbox",
     "nodes": {
         "inbox": {"text": "An email from 'accounts-payable@vend0r-payments.com' has an invoice PDF and urges same-day payment. The vendor is real; the domain is not quite theirs. First move?",
                   "choices": [{"t": "Check the sender domain and headers; verify the payment request through a known-good channel", "to": "verify"},
                               {"t": "Open the PDF to see if the invoice is real", "to": "open"},
                               {"t": "Forward it to the whole finance team as a warning", "to": "forward"}]},
         "verify": {"text": "Correct. Domain lookalike + urgency + attachment is the classic BEC pattern. Verify out-of-band through the vendor's known number — never the contact details in the email.", "end": True},
         "open": {"text": "Opening the attachment is exactly what the attacker wants. Verify first, open never — route it to the SOC.", "end": True},
         "forward": {"text": "Forwarding a live phish spreads it. Report it to the SOC; let them handle the warning.", "end": True}}},
    {"id": "il25-bs-ir", "title": "Ransomware: the first hour",
     "moduleId": "IL25-M12", "start": "call",
     "nodes": {
         "call": {"text": "Help desk: three machines show ransom notes. You are the responder. What is the correct first-hour order?",
                  "choices": [{"t": "Contain (isolate hosts), then identify scope, then eradicate — communicate throughout", "to": "order"},
                              {"t": "Pay the ransom quickly to limit damage", "to": "pay"},
                              {"t": "Wipe and rebuild the three machines immediately", "to": "wipe"}]},
         "order": {"text": "Correct IR order: contain first (stop the spread), scope the incident, eradicate, recover — with comms running in parallel. The plan you wrote in the module is the plan you run.", "end": True},
         "pay": {"text": "Paying funds the next attack, doesn't guarantee decryption, and may be illegal depending on the actor. Contain first.", "end": True},
         "wipe": {"text": "Wiping destroys forensic evidence and you don't yet know the scope — the fourth machine is still encrypting.", "end": True}}},
    {"id": "il25-bs-firewall", "title": "The firewall change request",
     "moduleId": "IL25-M14", "start": "ticket",
     "nodes": {
         "ticket": {"text": "A developer requests any/any outbound 'temporarily' to debug a production issue. The change window is tonight. Disposition?",
                    "choices": [{"t": "Deny any/any; offer a time-boxed rule to the specific endpoints with logging", "to": "scoped"},
                                {"t": "Approve — it's temporary", "to": "approve"},
                                {"t": "Approve but don't log it to save time", "to": "nolog"}]},
         "scoped": {"text": "Correct. 'Temporary' any/any rules become permanent. Scope it, time-box it, log it, and set the expiry you will actually enforce.", "end": True},
         "approve": {"text": "Temporary firewall rules are the most permanent objects in networking. Scope and expire.", "end": True},
         "nolog": {"text": "An unlogged rule change is an unauditable one — and the first thing the post-incident review will ask about.", "end": True}}},
    {"id": "il25-bs-vuln", "title": "Patch Tuesday: 400 vulnerabilities",
     "moduleId": "IL25-M04", "start": "scan",
     "nodes": {
         "scan": {"text": "The scanner reports 400 findings. You can patch 20 this week. How do you choose?",
                  "choices": [{"t": "Rank by exploitability × asset criticality: internet-facing + known exploit first", "to": "risk"},
                              {"t": "Patch the 20 highest CVSS scores", "to": "cvss"},
                              {"t": "Patch alphabetically by host", "to": "alpha"}]},
         "risk": {"text": "Correct. CVSS measures severity in a vacuum; risk-based prioritization multiplies by exposure and exploit availability. That is the vulnerability management the module teaches.", "end": True},
         "cvss": {"text": "A CVSS 9.8 on an isolated test VM beats a CVSS 7.5 on the internet-facing VPN? No. Severity without context misprioritizes.", "end": True},
         "alpha": {"text": "Alphabetical patching is random patching with extra steps.", "end": True}}},
]

IL25_CS = [
    {"id": "il25-cs-iam", "moduleId": "IL25-M06", "tool": "IAM console simulator",
     "title": "Build a least-privilege role",
     "steps": [
         {"screen": "A new analyst needs read access to security logs, nothing else.",
          "action": "Create a role with read-only actions on the log bucket only."},
         {"screen": "The policy simulator shows the effective permissions.",
          "action": "Test: list the bucket (allowed), delete an object (denied)."},
         {"screen": "Access analyzer flags no findings.",
          "action": "Attach the role and document the grant with a review date."}]},
    {"id": "il25-cs-firewall", "moduleId": "IL25-M14", "tool": "Firewall rule builder",
     "title": "Write a correct firewall rule",
     "steps": [
         {"screen": "A rule form: source, destination, port, protocol, action.",
          "action": "Write an allow rule for the web tier: any → web servers, TCP 443 only."},
         {"screen": "The rule preview shows it placed above the default-deny.",
          "action": "Add the matching return-traffic consideration and a log flag."},
         {"screen": "A test packet walk shows 443 allowed, 80 denied, SSH denied.",
          "action": "Save with a ticket reference and expiry review date."}]},
    {"id": "il25-cs-ticket", "moduleId": "IL25-M11", "tool": "SOC ticket queue",
     "title": "Work an incident ticket lifecycle",
     "steps": [
         {"screen": "The queue shows a new alert: impossible-travel login.",
          "action": "Open the ticket, note the source IPs and timestamps."},
         {"screen": "Enrichment shows one IP is the corporate VPN exit.",
          "action": "Reclassify: benign with explanation, and tune the rule to exclude the VPN range."},
         {"screen": "The ticket closes with the tuning note attached.",
          "action": "Record the lesson: every false positive should improve a rule."}]},
]
IL25_TOOLLABS = [
    {"id": "il25-tool-nmap", "title": "Nmap against your own lab", "moduleId": "IL25-M13",
     "brief": ("Run Nmap scans against ONLY the lab VM you built in install-lab-vm: host discovery, port scan, "
               "and service detection. Defensive framing — you are learning what an attacker sees so you can close it. "
               "Never scan networks you do not own.")},
]
IL25_INSTALL = [
    {"id": "install-lab-vm", "title": "Build the Ubuntu lab VM",
     "steps": ["Install a hypervisor on your machine.", "Create an Ubuntu VM from official installation media.",
               "Snapshot the clean VM.", "Keep it host-only networked."],
     "verify": "The VM boots and snapshots exist."},
    {"id": "install-wireshark", "title": "Install Wireshark in the lab",
     "steps": ["Install Wireshark inside the lab VM only.", "Capture traffic on the host-only interface.",
               "Save one capture showing a TCP handshake."],
     "verify": "A capture file shows SYN, SYN-ACK, ACK."},
]
IL25_INSTALL_ORDER = ["install-lab-vm", "install-wireshark"]
IL25_XLINKS = {
    "IL25-M01": ["IL29-M01"],
    "IL25-M02": ["IL29-M01"],
    "IL25-M04": ["IL29-M07"],
    "IL25-M06": ["IL29-M04"],
    "IL25-M07": ["IL29-M04"],
    "IL25-M09": ["IL29-M10"],
    "IL25-M10": ["IL29-M01"],
    "IL25-M11": ["IL29-M07"],
    "IL25-M12": ["IL29-M07"],
    "IL25-M13": ["IL29-M08"],
    "IL25-M14": ["IL29-M06"],
    "IL25-M15": ["IL29-M01"],
    "IL25-M16": ["IL29-M10"],
    "IL25-M17": ["IL29-M07"],
    "IL25-M18": ["IL29-M07"],
    "IL25-M19": ["IL29-M07"],
    "IL25-M20": ["IL29-M07"],
    "IL25-M21": ["IL29-M07"],
    "IL25-M24": ["IL29-M11"],
    "IL-25-PM-NUMTH": ["IL29-M01"],
    "IL-25-PM-STATS": ["IL29-M01"],
    "IL-25-PM-LOGIC": ["IL29-M01"],
}
