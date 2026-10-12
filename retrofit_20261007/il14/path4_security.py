# -*- coding: utf-8 -*-
"""IL-14 retrofit content — Path 4: Security Engineering Interview Prep (6 modules)."""
# pylint: disable=line-too-long

P4_SUMMARY = {
"security-eng-interview-prep--sec-appsec": (
"Welcome to the Security Engineering Interview Prep path of the Interstitium Labs SRE, DevOps, Cloud & Security Interview Prep course. "
"I'm your instructor for this path, and we open with the interview's favorite ambush: application security. The OWASP Top 10 taught as mechanisms and fixes — injection, XSS, auth flaws, SSRF, deserialization — plus what you actually hunt in a code review. "
"This is Module 1: Application Security Fundamentals. You'll discuss the Top 10 as risk categories with examples, then pivot to your own findings — because categories frame, but stories score."
),
"security-eng-interview-prep--sec-network": (
"Welcome back. I'm your instructor for the Security Interview Prep path, and this is Module 2: Network Security in Practice. "
"Network security you can defend aloud: what TLS actually guarantees, how segmentation contains breaches, where zero trust replaces the moat, DNS security, and DDoS mitigation by layer. "
"By the end you'll walk the TLS handshake at interview depth and explain why the VPN perimeter is dead — with the reasoning, not just the slogan."
),
"security-eng-interview-prep--sec-crypto": (
"Welcome back. I'm your instructor for the Security Interview Prep path, and this is Module 3: Cryptography in Practice. "
"Just enough cryptography to be dangerous in the right direction: symmetric vs asymmetric, the password-storage answer, TLS lifecycle hygiene, key management, randomness done right — and the never-roll-your-own rule. "
"You'll give the password-storage answer cold, explain why Math.random is unfit for tokens, and name what real key management looks like."
),
"security-eng-interview-prep--sec-detection": (
"Welcome back. I'm your instructor for the Security Interview Prep path, and this is Module 4: Detection and Response. "
"The defender's half of the interview: ATT&CK as the map of adversary behavior, the logs that matter, detection engineering with tuned rules, and the incident response phases — contain before you eradicate. "
"You'll tell a breach story the way hiring panels score them: timeline, evidence, systemic fixes with owners."
),
"security-eng-interview-prep--sec-design-review": (
"Welcome back. I'm your instructor for the Security Interview Prep path, and this is Module 5: Secure Design Review. "
"A full design review on a sample system: STRIDE-lite threat modeling, reviewing architecture like an attacker, designing authentication from the threat model, secrets and key design, and the written review document. "
"This is the artifact security interviews revolve around — you'll produce one and present findings like a consultant."
),
"security-eng-interview-prep--sec-mock": (
"Welcome back. I'm your instructor for the Security Interview Prep path, and this is Module 6: Security Mock Circuit. "
"Simulated security loops, scored like a hiring panel scores them: the secure-design round, the attacker-mindset round, the incident-response round, behavioral breach stories, and the security engineer's portfolio. "
"You'll practice thinking aloud through all three — because in security rounds, the reasoning is the product."
),
}

P4_NOTES = {
"security-eng-interview-prep--sec-appsec": [
{"title": "Concepts", "body": (
"- **OWASP Top 10** — the risk categories, current edition: injection, broken access control, cryptographic failures, SSRF, and more — discussed as mechanisms with examples, never just listed.\n"
"- **Injection** — untrusted input executed as code (SQLi and friends): the fix is parameterized queries, never string-built commands.\n"
"- **XSS (Cross-Site Scripting)** — stored, reflected, DOM-based: untrusted data rendered as code in the browser. Fix: context-appropriate output encoding + CSP in depth.\n"
"- **IDOR** — Insecure Direct Object Reference: changing an object ID accesses another user's data — the missing authorization check.\n"
"- **Broken authentication** — credential stuffing without rate limits, weak sessions, JWT 'none' algorithm or missing expiry validation.\n"
"- **SSRF** — Server-Side Request Forgery: the server fetches attacker-chosen URLs; in cloud, the nightmare is the instance metadata endpoint and credential theft.\n"
"- **Deserialization** — unserializing untrusted data: treat as remote code execution; never do it.\n"
"- **CSP (Content-Security-Policy)** — defense in depth for XSS: constrains what the browser may execute.\n"
"- **Trust boundary** — where untrusted data enters: review these first in any code review."
)},
{"title": "Hands-on procedure", "body": (
"Run a 30-minute security code review on a sample web app, hunting the Top 10.\n"
"1. **Map the trust boundaries.** List every place untrusted data enters: forms, APIs, file uploads, webhooks. 'I review the trust boundaries first.'\n"
"2. **Hunt injection sinks.** Every query, command, or template built from input: is it parameterized/encoded? Flag string-built SQL immediately.\n"
"3. **Check every endpoint's auth.** Not just the login page: broken object-level authorization (IDOR) on each route — 'who can call this, and whose data can they touch?'\n"
"4. **Audit the session and token handling.** JWT algorithm validation, expiry, rate limits on login — the broken-authentication checklist.\n"
"5. **Look for SSRF and deserialization.** Any server-side fetch of user-influenced URLs (allowlist? metadata IP blocked?); any unserialize of untrusted data.\n"
"6. **Write the findings.** Risk-ranked, each with the vulnerable code pattern, the fix, and the verification — the writeup that shows method."
)},
{"title": "Project brief", "body": (
"Your deliverable: a code-review finding writeup — the portfolio piece.\n"
"- **Pick one vulnerability class** (XSS, IDOR, SSRF, or injection) and write the full finding: the code pattern, why it's exploitable, the fix, and how you'd verify the fix.\n"
"- **Add the Top 10 framing**: which risk category it belongs to and a second example of the same category.\n"
"- **Include the review checklist** you used — the trust-boundary-first procedure from this module.\n"
"- **Sanitize everything**: no real company code, no real hostnames — method transfers, specifics don't need to.\n"
"- **Present it in 10 minutes** as 'here's how I found one in code review and what the fix was.'\n"
"Reference shelf (module sources): **OWASP** (https://owasp.org/) — the Top 10 and project pages. **OWASP Cheat Sheet Series** (https://cheatsheetseries.owasp.org/) — concise defensive guidance on auth, crypto, and injection."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and classroom findings are not professional security-assessment experience. "
"Never present exercise writeups as client work or bug-bounty history you don't have; sanitized method writeups are the honest portfolio. The OWASP Top 10 evolves — verify the current edition against the linked sources as of their retrieval dates. "
"Security knowledge carries responsibility: everything here is defensive — mechanisms taught so you can find and fix them."
)},
],
"security-eng-interview-prep--sec-network": [
{"title": "Concepts", "body": (
"- **TLS handshake** — ClientHello → ServerHello + certificate → key exchange (ECDHE for forward secrecy) → encrypted session. Validates: chain to a trusted root, hostname match, expiry.\n"
"- **Forward secrecy** — compromise of long-term keys doesn't decrypt past sessions: the ECDHE property.\n"
"- **Certificate pinning** — clients accept only specific certs/keys: for high-value mobile/API clients.\n"
"- **Segmentation** — defense in depth through zones (DMZ, app tier, data tier): traffic flows only where explicitly allowed, east-west as well as north-south.\n"
"- **Zero trust** — 'never trust, always verify': identity-based access, least privilege, device posture, continuous verification, micro-segmentation.\n"
"- **DNSSEC / DoH / DoT** — integrity for responses (signed), privacy for queries (encrypted transport).\n"
"- **DNS tunneling** — data encoded in DNS queries to an attacker domain: DNS is rarely filtered, so it becomes a covert channel.\n"
"- **Volumetric vs L7 DDoS** — bandwidth floods vs expensive legitimate-looking requests: absorbed at the edge vs filtered by behavioral/WAF rules."
)},
{"title": "Hands-on procedure", "body": (
"Defend a network design aloud, in 20 minutes, against an interviewer's attacks.\n"
"1. **Draw the zones.** Public DMZ, app tier, data tier — traffic only where explicitly allowed, east-west as well as north-south.\n"
"2. **Walk the TLS.** Handshake at interview depth, then the practice layer: TLS 1.2+ and cipher hygiene, cert lifecycle via ACME automation, expiry monitoring, HSTS.\n"
"3. **Apply zero trust.** For each zone crossing: what identity authenticates, what context authorizes — 'being inside the network grants nothing.'\n"
"4. **Harden DNS.** DNSSEC for integrity, DoH/DoT for query privacy, monitoring for tunneling patterns, registrar locks + MFA.\n"
"5. **Plan the DDoS layers.** Edge absorption (CDN/anycast scrubbing), rate limiting, WAF rules for L7, capacity headroom — matched to volumetric vs application-layer.\n"
"6. **Take the attacker's turn.** Partner plays attacker for 5 minutes: for each attack, name the control that contains it and the residual risk."
)},
{"title": "Project brief", "body": (
"Your deliverable: a network security design review for a sample three-tier system.\n"
"- **The zone diagram** with explicit allow-rules per boundary — east-west included.\n"
"- **The TLS section**: handshake walkthrough, version/cipher policy, cert lifecycle (ACME + expiry monitoring), HSTS, and where pinning applies.\n"
"- **The zero-trust overlay**: identity, device posture, and continuous verification per access path.\n"
"- **DNS and DDoS sections**: the hardening checklist and the layered mitigation plan.\n"
"- **Findings, consultant-style**: risk-ranked, business impact, concrete fixes with effort estimates.\n"
"- **Present in 10 minutes**, ending with: 'the VPN perimeter is dead; every request authenticates and authorizes.'\n"
"Reference shelf (module sources): **CISA Resources & Tools** (https://www.cisa.gov/resources-tools) — hardening and best-practice guidance. **NIST Cybersecurity Framework** (https://www.nist.gov/cyberframework) — the Identify/Protect/Detect/Respond/Recover frame."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and paper networks don't get attacked. "
"Real network defense involves legacy protocols, exceptions, and organizational friction that no diagram captures; the module teaches the structure — zones, TLS lifecycle, zero-trust decisions, layered DDoS — and the aloud-defense habit. "
"Protocol and product specifics change; verify current TLS, DNS, and product guidance against the linked sources as of their retrieval dates."
)},
],
"security-eng-interview-prep--sec-crypto": [
{"title": "Concepts", "body": (
"- **Symmetric crypto (AES)** — one shared key, fast: for bulk data. **Asymmetric (RSA/ECDH)** — key pairs, slow: for key exchange and signatures. Hybrid in practice: asymmetric establishes, symmetric encrypts.\n"
"- **Hashing vs password storage** — fast hashes (MD5/SHA-256) are for integrity, never passwords: GPUs crack them. Passwords get Argon2id (or bcrypt) with unique per-user salts and a tuned work factor.\n"
"- **Salt / pepper** — unique per-user salt defeats rainbow tables; a pepper via KMS/HSM adds defense in depth.\n"
"- **Forward secrecy** — ECDHE key exchange: past sessions stay secret even if long-term keys leak.\n"
"- **KMS/HSM** — keys live in managed hardware/services, never in code or repos; envelope encryption; rotation on schedule and on incident.\n"
"- **CSPRNG** — cryptographic randomness (/dev/urandom, secrets module) for keys, tokens, nonces: predictable randomness is no randomness.\n"
"- **The never-roll-your-own rule** — subtle flaws survive testing and review; even experts get it wrong. Use vetted primitives."
)},
{"title": "Hands-on procedure", "body": (
"Give the crypto answers cold — drill them until they're reflex.\n"
"1. **State the password-storage answer verbatim.** 'Argon2id with unique per-user salts and a tuned work factor; pepper via KMS as defense in depth. Never fast hashes alone, never reversible encryption.'\n"
"2. **Draw the hybrid.** Asymmetric establishes trust (key exchange, signatures), symmetric does the bulk work — say when each runs.\n"
"3. **Audit a key-management story.** Keys in KMS/HSM, envelope encryption, rotation scheduled and on incident, separate keys per environment, every use audited — 'if I can see the key in the repo, we've already lost.'\n"
"4. **Kill the randomness bug.** Find `Math.random()` used for a token in sample code; replace with a CSPRNG and explain why predictable PRNGs fall to attackers.\n"
"5. **Check the TLS lifecycle.** Version/cipher hygiene, ACME automation, expiry monitoring — 'handshake knowledge gets you hired; lifecycle hygiene keeps you employed.'\n"
"6. **Say the rule.** 'I don't roll my own crypto — subtle flaws survive review; I use vetted primitives and put my cleverness into key management.'"
)},
{"title": "Project brief", "body": (
"Your deliverable: a crypto review one-pager for a sample service.\n"
"- **The password-storage design**: algorithm, salt, work factor, pepper — with the 'why not SHA-256' reasoning.\n"
"- **The TLS posture**: versions, ciphers, cert lifecycle, HSTS — handshake plus hygiene.\n"
"- **The key-management design**: where keys live, rotation schedule and triggers, per-environment separation, audit.\n"
"- **The randomness audit**: every token/nonce/key source checked against the CSPRNG rule.\n"
"- **The never-build list**: what this service will never implement itself, and the vetted primitive for each.\n"
"- **Present in 10 minutes**, ending with the never-roll-your-own rule and what it costs to break it.\n"
"Reference shelf (module sources): **OWASP Cheat Sheet Series** (https://cheatsheetseries.owasp.org/) — crypto and password-storage guidance. **NIST Cybersecurity Framework** (https://www.nist.gov/cyberframework) — the Protect function framing."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and crypto guidance must be verified against current standards. "
"Algorithms, recommended work factors, and TLS versions evolve; the module teaches the decision structure (vetted primitives, proper password storage, real key management), not eternal parameters — verify specifics against the linked sources as of their retrieval dates. "
"Never present yourself as a cryptographer; the interview line is knowing enough to choose correctly and defer to vetted implementations."
)},
],
"security-eng-interview-prep--sec-detection": [
{"title": "Concepts", "body": (
"- **MITRE ATT&CK** — the shared map of adversary behavior: tactics (why — initial access, persistence, exfiltration) → techniques (how).\n"
"- **Detection engineering** — detections mapped to ATT&CK techniques, built on verified log sources, tuned for precision/recall, tested with simulated adversary activity.\n"
"- **Log sources** — the telemetry that matters: auth logs, process execution, network flows, DNS, cloud audit trails — each verified to produce what the detection needs.\n"
"- **Precision vs recall** — precision: alerts that fire are real. Recall: real attacks fire alerts. Untuned rules destroy SOC trust.\n"
"- **NIST 800-61 phases** — Preparation → Detection & Analysis → Containment → Eradication → Recovery → Lessons Learned.\n"
"- **Contain before eradicate** — stop the bleeding and preserve evidence before removing the threat; eradicating first can tip off the adversary and destroy forensics."
)},
{"title": "Hands-on procedure", "body": (
"Build one detection, end to end, on paper — the detection-engineering drill.\n"
"1. **Pick the technique.** From ATT&CK: e.g. credential dumping — tactic: credential access. Write the technique ID from the framework.\n"
"2. **Verify the log source.** Which log would show it (process execution, auth logs)? A detection without a tested log source is a hope — state what you'd check first.\n"
"3. **Write the rule logic.** The event pattern in plain language: 'process X accessing LSASS memory outside approved tooling' — precise enough to test.\n"
"4. **Tune for precision.** Name the benign activity that would false-positive, and the exclusion or threshold that handles it — 'untuned rules get ignored, then the real alert dies in the noise.'\n"
"5. **Plan the test.** Simulated adversary activity that should fire the rule: the test is part of the detection.\n"
"6. **Write the response play.** On fire: contain (isolate host, preserve memory/disk), then eradicate, then recover — contain before eradicate, always."
)},
{"title": "Project brief", "body": (
"Your deliverable: a detection-engineering brief plus a breach-story rehearsal.\n"
"- **The detection brief**: ATT&CK technique, log source verification, rule logic, tuning rationale (precision/recall), and the adversary-simulation test.\n"
"- **Coverage map**: three techniques across three tactics, each mapped to its log source — coverage measured against the matrix, not vibes.\n"
"- **The breach story**: a sanitized incident told blameless — timeline as understood then, what investigation showed, action items with owners, what you personally changed.\n"
"- **The IR phase card**: the six NIST phases on one page, with the contain-before-eradicate rule highlighted.\n"
"- **Present the detection in 10 minutes**, then tell the breach story in 5 — and take the follow-up questions.\n"
"Reference shelf (module sources): **MITRE ATT&CK** (https://attack.mitre.org/) — the tactic/technique matrix. **CISA Resources & Tools** (https://www.cisa.gov/resources-tools) — incident-response guidance."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and paper detections are not SOC experience. "
"Real detection engineering is tuned against months of real telemetry and real adversary activity; the module teaches the method — map to ATT&CK, verify the source, tune, test. Never present exercise detections as production SOC work. "
"ATT&CK evolves with adversary behavior; verify technique details against the linked framework as of its retrieval date."
)},
],
"security-eng-interview-prep--sec-design-review": [
{"title": "Concepts", "body": (
"- **STRIDE** — Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege: the per-component, per-data-flow threat enumeration.\n"
"- **Trust boundary** — where untrusted data crosses: every finding lives at a boundary; map them first.\n"
"- **Threat model** — structured pessimism with a spreadsheet: enumerate threats, rank by risk, assign mitigations with owners.\n"
"- **Repudiation** — attackers denying their actions: countered with non-repudiation (tamper-evident audit logs, signatures).\n"
"- **Short-lived tokens** — stolen tokens are useful only briefly: lifetime bounds the value of theft; rotated, bound refresh tokens handle continuity.\n"
"- **Security review document** — finding → business impact → likelihood → concrete remediation with effort estimate: risk-ranked, criticals first.\n"
"- **Consultant presentation** — evidence-backed, actionable, business-termed: never a 200-item undifferentiated list."
)},
{"title": "Hands-on procedure", "body": (
"Run a STRIDE-lite review of a sample architecture in 40 minutes.\n"
"1. **Draw the data flows.** Components and the arrows between them; mark every trust boundary — 'boundaries frame everything.'\n"
"2. **Enumerate per flow.** For each arrow, ask the six STRIDE questions. Write every threat, even the unlikely ones — ranking comes next.\n"
"3. **Rank by risk.** Impact × likelihood in plain language; the top 5 are the review's headline.\n"
"4. **Assign mitigations.** Per top threat: the control, its owner, and the effort — 'structured pessimism with a spreadsheet.'\n"
"5. **Design the auth.** Threat-model first, then: phishing-resistant MFA where it matters, short-lived tokens, secure sessions, rate-limited login, secrets in a manager.\n"
"6. **Write the review doc.** Finding → business impact → likelihood → fix with effort; criticals first. Present the top 3 in 5 minutes, like a consultant."
)},
{"title": "Project brief", "body": (
"Your deliverable: the full security design review — the artifact security interviews revolve around.\n"
"- **The threat model**: STRIDE-lite table per data flow, risk-ranked, mitigations with owners.\n"
"- **The architecture review**: trust boundaries, data flows, failure modes, scaling story — findings risk-ranked with concrete fixes.\n"
"- **The auth design**: for a new service, from the threat model — MFA, token lifetimes, session handling, rate limits, secrets.\n"
"- **The review document**: consultant-style, criticals first, business impact in business terms.\n"
"- **The 5-minute presentation**: top 3 findings, defended against pushback.\n"
"Reference shelf (module sources): **OWASP** (https://owasp.org/) — Top 10 and project pages. **HashiCorp Vault Documentation** (https://developer.hashicorp.com/vault/docs) — secrets engines and dynamic credentials."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and a classroom review is not a professional security assessment. "
"Real reviews involve stakeholder negotiation, incomplete information, and liability that no exercise carries; the module teaches the review structure and the consultant's reporting discipline. Never present it as client assessment experience. "
"Threat landscapes evolve; verify current guidance against the linked sources as of their retrieval dates."
)},
],
"security-eng-interview-prep--sec-mock": [
{"title": "Concepts", "body": (
"- **Secure-design round** — threat-model aloud (STRIDE-lite), name mitigations per threat: show the thinking, not just the answer.\n"
"- **Attacker-mindset round** — think in exploit primitives from the code/architecture: where would you strike, and why there.\n"
"- **Incident-response round** — contain before eradicate, preserve evidence: the defender's discipline under time.\n"
"- **Breach story (behavioral)** — blameless framing, timeline as understood then, evidence-driven findings, systemic fixes with owners, what you personally changed.\n"
"- **Security portfolio** — writeups that show method: a threat model, a code-review finding with the fix, a detection with its tuning rationale, a post-incident review — sanitized.\n"
"- **Thinking aloud** — security judgment is the product; the reasoning is what's evaluated."
)},
{"title": "Hands-on procedure", "body": (
"Run the security mock circuit with a partner, timed.\n"
"1. **Secure-design round (40 min).** Given a sample architecture: STRIDE-lite aloud, mitigations per threat, the review doc's top 3 — narrated.\n"
"2. **Attacker-mindset round (25 min).** Given sample code: think in exploit primitives — injection, auth gaps, SSRF — and rank targets by exploitability.\n"
"3. **Incident-response round (25 min).** A seeded breach: contain (isolate, preserve evidence) before eradicate — narrate the phase discipline.\n"
"4. **Behavioral round (20 min).** The breach story: blameless, timeline, systemic fixes, personal change — then the portfolio walkthrough.\n"
"5. **Score it.** Design rigor, attacker creativity, IR discipline, story honesty, communication — name the lowest axis.\n"
"6. **Write the debrief.** The weakest round's category, the redrill plan, and one portfolio piece to write this week."
)},
{"title": "Project brief", "body": (
"Your deliverable: a security interview dossier.\n"
"- **One threat-model writeup**, **one code-review finding with fix**, **one detection with tuning rationale** — sanitized, method-forward.\n"
"- **The breach story**, written then rehearsed aloud in 5 minutes — blameless, evidence-driven.\n"
"- **Mock score sheets** for all three technical rounds plus behavioral, with the weakest axis's redrill plan.\n"
"- **The portfolio index**: what each piece demonstrates, and the story you'd tell walking through it.\n"
"- **The taper note**: no new topics in the final two weeks — redrill, mock, rest.\n"
"Reference shelf (module sources): **OWASP** (https://owasp.org/). **MITRE ATT&CK** (https://attack.mitre.org/)."
)},
{"title": "Honesty note", "body": (
"Preparation only — this course confers no certificate, and mock rounds are not real security work. "
"Portfolio pieces must be sanitized and truthful: writeups of exercises are labeled as exercises, real findings stay confidential, and breach stories never name employers' incidents without permission. Fabricated security experience collapses under follow-up questions — and in security, credibility is the whole interview. "
"Frameworks evolve; verify current OWASP and ATT&CK content against the linked sources as of their retrieval dates."
)},
],
}

P4_NEW_CARDS = {
"security-eng-interview-prep--sec-appsec": {
"front": "How do you discuss the OWASP Top 10 without reciting a list?",
"back": "As risk categories with a current example each — injection, broken access control, crypto failures, SSRF — then pivot to your experience: 'here's how I found one in code review and what the fix was.' Categories frame the knowledge; stories score the points. The interview line: 'the Top 10 is a map, not a script.'",
},
"security-eng-interview-prep--sec-network": {
"front": "What does TLS actually guarantee — and what doesn't it?",
"back": "It guarantees confidentiality and integrity in transit to the authenticated endpoint — not that the endpoint is trustworthy, not that the app behind it is safe. Phishing sites have valid certs. The interview line: 'TLS secures the pipe; it says nothing about what's drinking from it.'",
},
"security-eng-interview-prep--sec-crypto": {
"front": "How do you answer 'should we encrypt it twice for safety'?",
"back": "With the threat model: double encryption adds complexity and key-management burden for marginal gain — the risk is almost never the cipher, it's the keys, the randomness, and the implementation. Fix the key management first. The interview line: 'I don't armor the vault door while the keys hang on a hook beside it.'",
},
"security-eng-interview-prep--sec-detection": {
"front": "How do you measure detection coverage without vibes?",
"back": "Against the ATT&CK matrix: techniques mapped to log sources mapped to tested detections — the uncovered techniques are the gaps, named explicitly. Coverage is a spreadsheet, not a feeling. The interview line: 'show me the matrix with the holes highlighted.'",
},
"security-eng-interview-prep--sec-design-review": {
"front": "How do you threat-model when you only have 10 minutes?",
"back": "STRIDE-lite on the highest-risk data flow only: enumerate fast, rank by obvious impact, mitigate the top 3 with owners. A partial model of the riskiest flow beats a complete model of nothing. The interview line: 'threat modeling is triage with a threat vocabulary.'",
},
"security-eng-interview-prep--sec-mock": {
"front": "How do you answer 'have you ever been breached?' honestly?",
"back": "With the blameless story structure: what happened, the timeline as you understood it then, what the investigation actually showed, the systemic fixes with owners — and what you personally changed afterward. Never name others' failures; talk about what the incident taught the system. The interview line: 'I talk about what the incident taught the system, not who failed.'",
},
}

def _q(q, choices, answer, explain):
    assert len(choices) == 4 and 0 <= answer <= 3 and explain
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}

P4_NEW_QUIZ = {
"security-eng-interview-prep--sec-appsec": [
_q("Parameterized queries defeat SQL injection because:",
   ["They're faster", "User input is never executed as code — data stays data", "They encrypt", "They're trendy"], 1,
   "Injection is code/data confusion; parameters keep untrusted input as data — the Concepts."),
_q("A JWT accepted with algorithm 'none' is broken because:",
   ["It's slow", "The signature check is skipped — anyone can forge tokens", "It's too long", "It's encrypted"], 1,
   "Algorithm confusion voids the token's integrity guarantee — the broken-auth checklist in the Hands-on procedure."),
_q("Content-Security-Policy helps against XSS as:",
   ["The root fix", "Defense in depth — it constrains what the browser may execute even if injection occurs", "A firewall", "Encryption"], 1,
   "Encoding is the fix; CSP is the safety net — the Concepts."),
_q("The SSRF fix 'block the metadata IP' exists because:",
   ["Metadata is slow", "The instance metadata endpoint hands out temporary credentials one hop from the vulnerable server", "It's trendy", "DNS requires it"], 1,
   "169.254.169.254 is the cloud nightmare scenario — the Concepts."),
_q("Deserializing untrusted data is treated as remote code execution because:",
   ["It's slow", "Object reconstruction can invoke attacker-controlled logic — never unserialize untrusted input", "It's large", "It's encrypted"], 1,
   "The gadget chain turns data into code execution — the Concepts."),
_q("Reviewing trust boundaries first works because:",
   ["It's fast", "Every vulnerability lives where untrusted data enters — boundaries frame the whole review", "It's required", "Tools do it"], 1,
   "'I review the trust boundaries first — where untrusted data enters' — the Hands-on procedure step 1."),
],
"security-eng-interview-prep--sec-network": [
_q("ECDHE in the handshake provides forward secrecy, meaning:",
   ["It's faster", "Past sessions stay secret even if long-term keys are later compromised", "Certs last longer", "It's simpler"], 1,
   "Ephemeral key exchange decouples session secrecy from long-term keys — the Concepts."),
_q("An expired certificate in production is primarily:",
   ["A security breach", "An availability outage — entirely preventable with ACME automation and expiry monitoring", "A minor warning", "Expected"], 1,
   "Expired certs are a top preventable outage cause — the Hands-on procedure step 2."),
_q("Micro-segmentation contains breaches by:",
   ["Slowing the network", "Limiting lateral movement — a compromised host can't freely reach its neighbors", "Encrypting everything", "Adding firewalls"], 1,
   "East-west allow-rules turn one breach into a contained incident — the Concepts."),
_q("DoH/DoT protect DNS queries from:",
   ["Typos", "Passive observers on the path — queries travel encrypted, unlike plaintext DNS", "Tunneling", "Cache poisoning"], 1,
   "Query privacy is the DoH/DoT job; integrity is DNSSEC's — the Concepts."),
_q("Rate limiting at the edge mitigates L7 DDoS because:",
   ["It's cheap", "Application-layer attacks use expensive legitimate-looking requests — behavioral filtering beats bandwidth", "It's fast", "Bots give up"], 1,
   "L7 defense is semantic, not volumetric — the Concepts."),
_q("A phishing site with a valid certificate proves that TLS:",
   ["Is broken", "Authenticates the pipe, not the trustworthiness of who's behind it", "Is useless", "Needs pinning everywhere"], 1,
   "The new card: TLS secures the pipe; it says nothing about who's drinking from it."),
],
"security-eng-interview-prep--sec-crypto": [
_q("Argon2id beats SHA-256 for passwords because:",
   ["It's newer", "It's deliberately slow and memory-hard with a tuned work factor — GPUs can't brute-force it cheaply", "It's shorter", "It's standard"], 1,
   "Fast hashes are for integrity; password storage needs slowness — the Hands-on procedure step 1."),
_q("A unique salt per user defeats:",
   ["Phishing", "Rainbow tables — identical passwords hash differently", "Brute force", "Keyloggers"], 1,
   "Salts individualize every hash; precomputation dies — the Concepts."),
_q("Envelope encryption is used because:",
   ["It's trendy", "Data keys encrypt data while master keys in the KMS wrap data keys — keys stay in the manager, never in code", "It's faster", "It's required"], 1,
   "The hierarchy keeps raw keys out of applications — the Hands-on procedure step 3."),
_q("Key rotation on a schedule limits damage because:",
   ["Keys get stronger", "A leaked key has a bounded useful lifetime", "It's compliance theater", "It's faster"], 1,
   "Rotation shrinks the window where a compromised key is valuable — the Concepts."),
_q("`/dev/urandom` (or the secrets module) is required for tokens because:",
   ["It's fast", "It's a CSPRNG — designed to resist prediction, unlike Math.random()'s observable state", "It's built in", "It's random enough"], 1,
   "Predictable randomness is no randomness — the Hands-on procedure step 4."),
_q("The 'never roll your own' rule exists because:",
   ["Experts are busy", "Cryptographic flaws are silent until exploited — even experts get primitives wrong; vetted implementations are the sane choice", "It's slow", "Patents"], 1,
   "Peer-reviewed primitives or nothing — the Concepts."),
],
"security-eng-interview-prep--sec-detection": [
_q("Mapping detections to ATT&CK techniques (not just writing rules) matters because:",
   ["It's traditional", "Coverage becomes measurable — gaps are named techniques, not vibes", "It's faster", "Rules are short"], 1,
   "'Coverage measured against the matrix, not vibes' — the Project brief."),
_q("A detection firing 200 times a day on benign activity will:",
   ["Catch everything", "Get ignored — then the real alert dies in the noise; precision matters as much as recall", "Improve", "Self-tune"], 1,
   "Alert fatigue kills SOC trust — the tuning rationale in the Hands-on procedure step 4."),
_q("Isolating the host before wiping it is correct because:",
   ["It's faster", "Containment preserves evidence and stops spread before eradication removes the threat", "Wiping is hard", "It's optional"], 1,
   "Contain before eradicate — the IR phase discipline in the Concepts."),
_q("Testing a detection with simulated adversary activity proves:",
   ["The rule is long", "The log source actually produces the telemetry and the rule fires on it — a detection without a test is a hope", "Attackers are scary", "It's fast"], 1,
   "The test is part of the detection — the Hands-on procedure step 5."),
_q("In the NIST phases, 'Lessons Learned' feeds back into:",
   ["Nothing", "Preparation — the loop closes: findings become better defenses and playbooks", "Recovery", "Eradication"], 1,
   "The phases are a cycle, not a line — the Concepts."),
_q("A breach story told with blame ('Dave clicked the link') fails because:",
   ["Dave is innocent", "Blame produces cover stories instead of root causes — blameless framing gets honest timelines", "It's long", "It's rude"], 1,
   "Honest data requires psychological safety — the Concepts' breach-story structure."),
],
"security-eng-interview-prep--sec-design-review": [
_q("Running STRIDE per data flow (not per server) works because:",
   ["Servers are boring", "Threats live where data crosses trust boundaries — flows are where attacks happen", "It's faster", "It's traditional"], 1,
   "Every finding lives at a boundary; flows expose them — the Hands-on procedure step 1."),
_q("In STRIDE, a missing audit log is primarily a:",
   ["Spoofing threat", "Repudiation threat — attackers can deny their actions without tamper-evident logs", "DoS threat", "Tampering threat"], 1,
   "Repudiation is countered with non-repudiation — the Concepts."),
_q("Threat-modeling the auth design before choosing libraries is correct because:",
   ["Libraries are bad", "The threat model defines what you're protecting from whom — mechanism follows the model", "It's faster", "It's required"], 1,
   "'Auth design starts from the threat model, not the library' — the Hands-on procedure step 5."),
_q("Short-lived access tokens plus rotated refresh tokens:",
   ["Are slower", "Bound the value of token theft while preserving usability", "Are trendy", "Replace MFA"], 1,
   "Lifetime bounds exposure; rotation handles continuity — the Concepts."),
_q("A review that lists 200 undifferentiated findings fails because:",
   ["It's long", "Decision-makers can't act on it — risk-ranked criticals with fixes are the product", "Tools do better", "It's honest"], 1,
   "Never the undifferentiated list — the consultant presentation in the Concepts."),
_q("Assigning each mitigation an owner matters because:",
   ["It's polite", "Unowned mitigations don't happen — the threat model is a spreadsheet with accountability", "It's traditional", "Auditors ask"], 1,
   "'Structured pessimism with a spreadsheet' — the Hands-on procedure step 4."),
],
"security-eng-interview-prep--sec-mock": [
_q("In the attacker-mindset round, ranking targets by exploitability shows:",
   ["Paranoia", "Adversary thinking — where you'd strike first and why, not just a vulnerability list", "Speed", "Tool skill"], 1,
   "Think in exploit primitives from the code — the Concepts."),
_q("Narrating the STRIDE steps aloud in the design round is graded because:",
   ["It's loud", "Security judgment is the product — the reasoning is what's being evaluated", "It's polite", "Answers are short"], 1,
   "'I show the thinking, not just the answer' — the Concepts."),
_q("A portfolio detection writeup's most valuable part is:",
   ["The severity", "The tuning rationale — why it fires on attacks and not on benign activity", "The screenshots", "Its length"], 1,
   "Method transfers; any single rule doesn't — the Project brief."),
_q("Sanitizing portfolio writeups (no real hostnames, no client code) is required because:",
   ["It's tedious", "Real findings are confidential — method is shown, specifics are protected", "It's trendy", "It's faster"], 1,
   "Sanitized, of course — the Honesty note's rule."),
_q("The incident-response mock grades 'contain before eradicate' because:",
   ["It's traditional", "Eradicating first destroys evidence and can tip off the adversary mid-investigation", "It's faster", "It's optional"], 1,
   "The defender's discipline under time — the Hands-on procedure step 3."),
_q("After the circuit, the single most useful portfolio addition is:",
   ["A certificate", "One method-forward writeup (threat model, finding, or detection) produced this week", "A longer resume", "More tools"], 1,
   "'I show how I think, not just what I found' — the Project brief's dossier."),
],
}
