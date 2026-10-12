"""Per-module retrofit expansions for IL-11 -> IL-19 (Multicloud) course template.
Each entry is keyed by module id. Transform script (transform.py) applies these.
Original factual content from the source file is preserved and expanded, never deleted.
"""

EXPANSIONS = {

# =====================================================================
# PATH 1 — il11-zero-trust-foundations
# =====================================================================

'il11-zero-trust-foundations--zt-perimeter-fall': {
'title': 'The Fall of the Perimeter',
'summary': (
    "Welcome to IL-11, Zero Trust & Endpoint Defense. I'm your instructor, and this is Module 1: "
    "The Fall of the Perimeter. Before we touch a single control, you need to feel — in your bones — "
    "why the old model broke. We will trace the castle-and-moat assumptions, follow an attacker across "
    "lateral movement after breach, and see how cloud and remote work dissolved the network edge. "
    "By the end, the assume-breach mindset won't be a slogan to you; it will be the only premise that survives the evidence."
),
'objectives': [
    "Explain the castle-and-moat assumptions and name what each one got wrong",
    "Trace lateral movement after an initial breach across at least three internal hops",
    "Describe how cloud adoption and remote work dissolved the network edge",
    "Argue for the assume-breach mindset from first principles in a written memo",
],
'concepts': [
    "- **Castle-and-moat** — The legacy model: a hard network perimeter (firewalls, VPN concentrators) around a soft interior where everything inside is implicitly trusted.",
    "- **Implicit trust** — Access granted by network location rather than by identity, device state, and risk. Zero Trust removes exactly this.",
    "- **Lateral movement** — An attacker's hop-by-hop traversal of internal systems after the initial breach, moving toward data, credentials, and control.",
    "- **Assume breach** — The operating mindset that an attacker may already be inside: every request is verified continuously, regardless of origin.",
    "- **Dissolution of the edge** — Cloud services and remote work placed users, devices, and data outside the old perimeter, so the network edge no longer bounds the environment.",
    "- **Perimeter failure mode** — The asymmetry of castle-and-moat: one successful breach defeats the entire model, because nothing inside challenges the attacker again.",
],
'procedure_intro': (
    "Work this module like a detective, not a student. You will reconstruct the crime scene of the "
    "perimeter model — its assumptions, its failure mode, and what replaced it. Do each step on paper before moving on."
),
'procedure_steps': [
    "1. **Draw the moat.** Sketch a classic corporate network: firewall at the edge, VPN for remote users, flat internal LAN, file servers and domain controllers inside. Label every trust boundary your drawing implies.",
    "2. **Find the false assumption.** For each boundary you drew, write down what the design *assumes* about the traffic inside it. Circle every place where 'inside equals safe' appears — that is the castle-and-moat assumption made visible.",
    "3. **Land the breach.** Place a single phishing-compromised laptop inside your drawing. That is the only foothold the attacker needs.",
    "4. **Walk three lateral hops.** From the laptop, trace a plausible path: harvest credentials from memory, log into a file server, reach the domain controller. For each hop, ask: 'What in this drawing challenges the attacker?' Write the answer — it is usually 'nothing.'",
    "5. **Dissolve the edge.** Now erase the perimeter: add remote workers on home networks, SaaS apps, and cloud workloads. Mark which assets your firewall can no longer see. This is the environment you actually defend today.",
    "6. **Rebuild on assume-breach.** On a fresh page, write the access decision for one internal request — who, what device, what data, what risk — and check it *every time*, no matter where the request comes from. That check is the seed of Zero Trust.",
    "7. **Write the verdict.** In three sentences, explain why assume-breach is a conclusion from the evidence, not a fashion. Read it aloud — it is the premise of everything that follows in this academy.",
],
'project': (
    "**Harborview Freight — the case for Zero Trust.** Harborview Freight runs a regional logistics network: "
    "a headquarters office, two warehouses, roughly 250 endpoints, a mix of on-prem servers and SaaS, and drivers who work "
    "from home offices and truck cabs. The board believes the firewall and VPN are 'the security.' "
    "Deliverable: a one-page memo to the board that (a) walks through a phishing-to-domain-controller attack path in their environment, "
    "(b) names the castle-and-moat assumption at each hop, and (c) states the assume-breach principle that will anchor the Zero Trust program. "
    "No tools, no products — reasoning only. The memo must survive a skeptical CFO."
),
'checkin': [
    "In one sentence, what does the assume-breach mindset change about defense?",
    "Draw the phishing-to-domain-controller path from the Hands-on procedure and point to where the old model would have stopped the attacker — then explain why it doesn't.",
    "Name two business changes that dissolved the network edge, and explain why neither can be 'un-done' by buying a bigger firewall.",
],
'cards': [
    {"front": "What does the assume-breach mindset change about defense?",
     "back": "You operate as if an attacker is already inside, so every request is verified continuously instead of trusting the network."},
    {"front": "Why does the castle-and-moat model fail against modern attacks?",
     "back": "Once an attacker breaches the perimeter, nothing stops lateral movement inside the trusted network — the model's false assumption is that inside equals safe."},
    {"front": "What is lateral movement?",
     "back": "The attacker's hop-by-hop traversal of internal systems after the initial breach — harvesting credentials, pivoting to servers, and moving toward data and control."},
    {"front": "Why did cloud adoption and remote work dissolve the network edge?",
     "back": "Users, devices, and data moved outside the old perimeter onto home networks, SaaS, and cloud workloads — the firewall no longer bounds the environment, so network location stopped meaning trust."},
    {"front": "What is the perimeter's core failure mode, in one sentence?",
     "back": "One successful breach defeats the entire model, because nothing inside the perimeter challenges the attacker again."},
    {"front": "State the assume-breach principle as a rule for access decisions.",
     "back": "Verify every request — who, what device, what data, what risk — continuously, regardless of where it comes from."},
],
'quiz': [
    {"q": "The assume-breach mindset means defenders should:",
     "choices": ["Trust internal traffic", "Operate as if an attacker is already inside", "Skip monitoring once the perimeter holds", "Rely on VPNs alone"],
     "answer": 1,
     "explain": "Covered in Concepts: assume breach means continuous verification, because perimeters fail."},
    {"q": "A phishing email compromises one laptop inside a castle-and-moat network. What happens next, per this module's attack walkthrough?",
     "choices": ["The firewall blocks the attacker's lateral movement", "The attacker is stopped at the VPN gateway", "Nothing inside challenges the attacker; lateral movement proceeds toward credentials and servers", "The interior switches automatically verify the compromised laptop"],
     "answer": 2,
     "explain": "Covered in Hands-on procedure: the walkthrough shows nothing inside challenges the attacker after the initial breach."},
    {"q": "Which of the following is a topic covered in \"The Fall of the Perimeter\"?",
     "choices": ["SQL injection techniques", "Conditional Access policies: signals and controls", "Cloud and remote-work dissolution of the edge", "Microsoft 365 attack surface"],
     "answer": 2,
     "explain": "Covered in Concepts: the module's topics are the castle-and-moat assumptions, lateral movement, dissolution of the edge, and assume-breach; the other options belong to later modules."},
    {"q": "Why can't a bigger firewall restore the old security model?",
     "choices": ["Firewalls are too expensive", "The edge no longer bounds the environment: users and data live outside the perimeter", "Firewalls cannot filter encrypted traffic at all", "Remote workers refuse to use VPNs"],
     "answer": 1,
     "explain": "Covered in Project brief: cloud and remote work moved the environment outside the perimeter — a firewall guards a boundary that no longer contains the assets."},
],
},

'il11-zero-trust-foundations--zt-nist-tenets': {
'title': 'NIST SP 800-207 Tenets',
'summary': (
    "Welcome back. I'm your instructor, and this is Module 2: the NIST SP 800-207 tenets — the document that turned "
    "Zero Trust from a vendor slogan into an engineering discipline. We will do a guided reading of the seven tenets "
    "and the logical components — policy engine, policy administrator, policy enforcement point — so you know exactly "
    "what each tenet demands of a real deployment. When you can read a product pitch and map every claim to a tenet, "
    "you'll be harder to fool than most practitioners."
),
'objectives': [
    "Recite the Zero Trust doctrine and state all seven NIST SP 800-207 tenets from memory",
    "Distinguish the policy engine, policy administrator, and policy enforcement point and their roles in an access decision",
    "Explain continuous diagnostics and mitigation as an operational loop, not a tool",
    "Contrast enterprise-wide Zero Trust with the old enclave mindset",
],
'concepts': [
    "- **Zero Trust doctrine** — 'Never trust, always verify': no implicit trust is granted based on network location, asset ownership, or prior authentication; every access request is evaluated.",
    "- **Seven tenets** — The seven principles in NIST SP 800-207 that formalize the doctrine: all data sources and computing services are resources; all communication is secured; access is per-session; access is determined by dynamic policy; the enterprise monitors integrity and posture of assets; authentication and authorization are dynamic and strictly enforced; the enterprise collects as much information as possible to improve posture.",
    "- **Policy engine (PE)** — The logical component that makes the access decision: it evaluates policy, identity, device posture, and risk signals, and grants or denies.",
    "- **Policy administrator (PA)** — The logical component that executes the decision: it establishes or shuts down the communication path between subject and resource as the policy engine directs.",
    "- **Policy enforcement point (PEP)** — The component that actually allows, monitors, and terminates connections between subject and resource, under the administrator's direction.",
    "- **Continuous diagnostics and mitigation (CDM)** — The operational loop of monitoring asset posture, detecting deviation, and responding — the tenets demand it as a living process, not a one-time scan.",
    "- **Enclave mindset** — The old idea of carving the network into trusted zones and defending the zone boundary; Zero Trust replaces zone trust with per-session, per-resource decisions.",
    "- **Subject / resource** — SP 800-207 vocabulary: the *subject* is the user, device, or process requesting access; the *resource* is the data, service, or system being accessed.",
],
'procedure_intro': (
    "Read SP 800-207 like an engineer reviewing a specification. You will walk each tenet into a deployment decision "
    "until the logical components stop being abstract boxes and become jobs your infrastructure must do."
),
'procedure_steps': [
    "1. **Open the source.** Pull up NIST SP 800-207 at csrc.nist.gov (linked in this course's source list) and read the tenets section end to end. Highlight the verb in each tenet — the tenets are demands, not descriptions.",
    "2. **Draw the logical model.** On paper, place the subject on the left, the resource on the right, and the policy engine, policy administrator, and PEP between them. Draw the decision arrow from PE to PA, and the enforcement arrow from PA to PEP.",
    "3. **Run one request.** Walk a single access request through your drawing: a user on a personal phone requests the payroll app. At the PE, list the signals evaluated (identity, device posture, location, risk). At the PA, state the path action. At the PEP, state the enforcement.",
    "4. **Find the CDM loop.** Annotate where continuous diagnostics feed back into the PE — a device that was compliant at 9:00 and compromised at 9:05 must produce a *new* decision, not ride the old one.",
    "5. **Kill the enclave.** Take one 'trusted zone' from your Module 1 drawing and rewrite its rule in tenet language: not 'servers in VLAN 40 may talk,' but 'subject X may access resource Y under policy Z, per session.'",
    "6. **Stress-test a pitch.** Invent a vendor claim ('our firewall is Zero Trust!') and map it to the tenets: which tenet does it actually satisfy, and which does it ignore? Write the verdict in two sentences.",
    "7. **Recite.** From memory, state the doctrine and all seven tenets. Anything you can't say without the page is a gap — close it before the next module.",
],
'project': (
    "**Harborview Freight — tenet mapping.** Harborview's leadership heard a vendor pitch: 'Our next-gen firewall delivers Zero Trust.' "
    "Deliverable: a tenet-by-tenet scorecard. For each of the seven SP 800-207 tenets, write one paragraph judging whether a "
    "perimeter firewall alone can satisfy it, and name the component (PE, PA, PEP) or process (CDM) that would actually be required. "
    "Conclude with a buy / don't-buy recommendation and the reasoning. Cite the publication, not the pitch."
),
'checkin': [
    "From memory: state the Zero Trust doctrine and the seven tenets.",
    "A vendor says their VPN 'enables Zero Trust.' Which tenet does that claim misunderstand, and why?",
    "Walk Noah through one access request: what the PE decides, what the PA does, what the PEP enforces.",
],
'cards': [
    {"front": "State the Zero Trust doctrine and how many tenets NIST SP 800-207 defines.",
     "back": "Never trust, always verify — formalized in seven tenets in NIST SP 800-207."},
    {"front": "In a Zero Trust architecture, what decides access and what enforces it?",
     "back": "The policy engine makes the access decision; the policy administrator executes it through the policy enforcement point (PEP)."},
    {"front": "What is the policy enforcement point (PEP)?",
     "back": "The component that actually allows, monitors, and terminates the connection between subject and resource, under the policy administrator's direction."},
    {"front": "What does continuous diagnostics and mitigation (CDM) require of an enterprise?",
     "back": "A living loop: monitor asset integrity and posture, detect deviation, and respond — so that a device compromised after its initial check produces a new, denied decision."},
    {"front": "How does the Zero Trust model differ from the enclave mindset?",
     "back": "The enclave mindset trusts zones and defends zone boundaries; Zero Trust makes per-session, per-resource access decisions with no implicit trust from location."},
    {"front": "In SP 800-207 vocabulary, what are the subject and the resource?",
     "back": "The subject is the user, device, or process requesting access; the resource is the data, service, or system being accessed."},
],
'quiz': [
    {"q": "NIST SP 800-207 defines Zero Trust through how many tenets?",
     "choices": ["Five", "Six", "Seven", "Ten"],
     "answer": 2,
     "explain": "Covered in Concepts: SP 800-207 formalizes the doctrine in seven tenets."},
    {"q": "Which component makes the access decision in the SP 800-207 logical model?",
     "choices": ["Policy enforcement point", "Policy engine", "Data plane", "VPN gateway"],
     "answer": 1,
     "explain": "Covered in Concepts: the policy engine evaluates policy and signals and renders the grant/deny decision."},
    {"q": "A laptop is compliant at 9:00 AM and compromised at 9:05 AM. Under the tenets, what must happen to its 9:00 access grant?",
     "choices": ["It remains valid until the user's shift ends", "It is re-evaluated: continuous diagnostics feed new posture into a new per-session decision", "It is suspended only if the user reports the issue", "It transfers to the backup laptop automatically"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure and Concepts: access is per-session and dynamic — CDM feeds new posture into the policy engine, producing a new decision."},
    {"q": "A vendor claims their firewall alone 'delivers Zero Trust.' What is the strongest tenet-based rebuttal?",
     "choices": ["Firewalls are too expensive to count", "A single perimeter box cannot satisfy per-session, dynamic, per-resource decisions across PE, PA, PEP, and CDM — map the claim to the tenets and the gaps appear", "Zero Trust forbids the use of firewalls", "NIST prohibits vendor products in Zero Trust designs"],
     "answer": 1,
     "explain": "Covered in Project brief: score each tenet against what a perimeter firewall actually does — the PE/PA/PEP decision loop and CDM are not a firewall feature."},
],
},

'il11-zero-trust-foundations--zt-cisa-maturity': {
'title': 'CISA Zero Trust Maturity Model',
'summary': (
    "Welcome to Module 3. I'm your instructor, and today we turn doctrine into a roadmap: the CISA Zero Trust Maturity Model. "
    "Doctrine tells you what 'good' looks like; the maturity model tells you where you stand and what the next step costs. "
    "We will walk the five pillars — identity, devices, networks, applications, data — and the three steps from Traditional "
    "through Advanced to Optimal. Your deliverable is a self-assessment of a fictional organization and a remediation roadmap "
    "you could defend in a budget meeting."
),
'objectives': [
    "Name the five CISA Zero Trust pillars and what each one governs",
    "Distinguish the Traditional, Advanced, and Optimal maturity steps for any pillar",
    "Score a fictional organization against the model in a written self-assessment",
    "Write a prioritized remediation roadmap from the assessment gaps",
],
'concepts': [
    "- **Five pillars** — Identity, devices, networks, applications and workloads, data: the five domains CISA scores for Zero Trust maturity. Every control you deploy lives in one of them.",
    "- **Identity pillar** — Authentication strength, identity stores, risk assessment, and access management: verifying who (or what) is requesting before anything else.",
    "- **Devices pillar** — Endpoint compliance, authorization, and continuous monitoring: the health and trustworthiness of the thing making the request.",
    "- **Networks pillar** — Transport, segmentation, encryption, and resilience: how traffic moves and what it is allowed to reach.",
    "- **Applications and workloads pillar** — Application access, threat protection, and secure delivery of the software being used.",
    "- **Data pillar** — Classification, encryption, access policy, and governance of the information itself — the asset the other pillars exist to protect.",
    "- **Traditional / Advanced / Optimal** — The three maturity steps: Traditional is the starting posture (manual, perimeter-based); Advanced adds automation and broader coverage; Optimal is the target state (fully automated, continuously verified).",
    "- **Visibility and automation** — The cross-cutting theme: you cannot advance a pillar you cannot see, and you cannot sustain Optimal maturity with manual processes.",
    "- **Governance** — The management layer over the pillars: policies, risk decisions, and accountability that keep the technical controls pointed at business risk.",
],
'procedure_intro': (
    "Assess like an auditor. You will score Harborview Freight against the model, pillar by pillar, and the gaps you find "
    "become the roadmap. Be honest in the scoring — an inflated assessment is the most expensive kind of wrong."
),
'procedure_steps': [
    "1. **Learn the grid.** Read the CISA Zero Trust Maturity Model (linked in the course sources). For each of the five pillars, write one sentence describing its Traditional, Advanced, and Optimal states in your own words.",
    "2. **Build the worksheet.** Make a table: five pillars down the side, three steps across the top. Leave room for evidence and a score in each cell.",
    "3. **Inventory the org.** From the Harborview profile (headquarters, two warehouses, ~250 endpoints, on-prem plus SaaS, remote workers), list the facts that bear on each pillar: how identity is managed, what endpoints look like, how networks segment, what apps are used, where data lives.",
    "4. **Score honestly.** Place each pillar at Traditional, Advanced, or Optimal — with the evidence that justifies it. Most real organizations land at Traditional in at least three pillars; if everything scores Advanced, you are grading too generously.",
    "5. **Name the cheapest wins.** For each pillar below Optimal, identify the single advancement with the best security-per-dollar: usually identity (MFA/phishing-resistant auth) and visibility (logging you can actually query).",
    "6. **Sequence the roadmap.** Order the advancements into three horizons — 0–90 days, 3–12 months, 12–24 months — explaining why each step must precede the next (e.g., identity before fine-grained data policy).",
    "7. **Write the one-pager.** Summarize the assessment and roadmap for a non-technical executive: current state, target state, first three moves, and what each move buys. If it needs jargon to sound convincing, rewrite it.",
],
'project': (
    "**Harborview Freight — maturity self-assessment.** Deliverable: the completed five-pillar worksheet with evidence-based scores, "
    "plus the sequenced remediation roadmap in three horizons. Your roadmap must name the pillar, the step being advanced, the control, "
    "and the dependency it unlocks. The board will ask 'why this order' — your sequencing rationale is the graded artifact."
),
'checkin': [
    "Name the five pillars and, for one pillar of Noah's choosing, describe its Traditional, Advanced, and Optimal states.",
    "Why does visibility come before automation in advancing a pillar?",
    "Defend your roadmap's first move: what does it unlock that nothing else can?",
],
'cards': [
    {"front": "Name the five CISA Zero Trust pillars.",
     "back": "Identity, devices, networks, applications and workloads, data."},
    {"front": "What are the three maturity steps in the CISA model?",
     "back": "Traditional, Advanced, Optimal — from manual and perimeter-based, through automation and broader coverage, to fully automated and continuously verified."},
    {"front": "What does the identity pillar govern?",
     "back": "Authentication strength, identity stores, risk assessment, and access management — verifying the requester before anything else."},
    {"front": "What does the data pillar govern, and why is it last in the list but first in importance?",
     "back": "Classification, encryption, access policy, and governance of the information itself — the asset the other four pillars exist to protect."},
    {"front": "Why is visibility a prerequisite for advancing a pillar?",
     "back": "You cannot advance what you cannot see: maturity steps require evidence of posture, and Optimal demands continuous verification — both impossible without visibility."},
    {"front": "What role does governance play over the five pillars?",
     "back": "The management layer: policies, risk decisions, and accountability that keep the technical controls pointed at business risk."},
],
'quiz': [
    {"q": "Which of the following is one of the five CISA Zero Trust pillars?",
     "choices": ["Firewalls", "Devices", "Antivirus", "VPNs"],
     "answer": 1,
     "explain": "Covered in Concepts: the five pillars are identity, devices, networks, applications and workloads, and data."},
    {"q": "An organization has phishing-resistant MFA everywhere, automated device compliance checks, and continuous access re-evaluation. Which maturity step best describes its identity pillar?",
     "choices": ["Traditional", "Advanced", "Optimal", "Unscored"],
     "answer": 2,
     "explain": "Covered in Concepts and Hands-on procedure: fully automated, continuously verified identity controls match the Optimal step."},
    {"q": "Why must visibility come before automation when advancing a pillar?",
     "choices": ["Automation tools require a visibility license", "You cannot verify or sustain improvements you cannot see — evidence of posture is what the steps measure", "Visibility is cheaper than automation", "Auditors only inspect visibility dashboards"],
     "answer": 1,
     "explain": "Covered in Concepts: the steps are defined by evidence of posture and continuous verification, which visibility provides."},
    {"q": "Which module covers \"Visibility and automation\" as a maturity-model theme?",
     "choices": ["NIST SP 800-207 Tenets", "The Fall of the Perimeter", "CISA Zero Trust Maturity Model", "Default-Deny Architecture"],
     "answer": 2,
     "explain": "Covered in Concepts: visibility and automation is the cross-cutting theme of the CISA Zero Trust Maturity Model module."},
],
},

'il11-zero-trust-foundations--zt-default-deny': {
'title': 'Default-Deny Architecture',
'summary': (
    "Welcome to Module 4. I'm your instructor, and this is where Zero Trust gets teeth: default-deny architecture. "
    "Allow-by-default is how malware runs; deny-by-default is how you stop it without playing whack-a-mole with signatures. "
    "We will contrast allowlisting with denylisting, build least privilege by construction, run learning mode before "
    "enforcement, and face the honest operational cost of deny-by-default — because a control the business can't live with "
    "is a control that gets turned off."
),
'objectives': [
    "Contrast allowlisting and denylisting and explain why deny-by-default wins against novel malware",
    "Design least-privilege access by construction for an application set",
    "Run a learning-mode baseline before enforcement and convert it into policy",
    "Defend a business-continuity plan for a default-deny rollout",
],
'concepts': [
    "- **Allowlisting (deny by default)** — Only explicitly approved applications are permitted to run; everything else is blocked. The default answer is 'no.'",
    "- **Denylisting (allow by default)** — Everything is permitted except explicitly blocked items (e.g., known-bad hashes). The default answer is 'yes' — which is why novel malware walks through.",
    "- **Least privilege by construction** — Access and capability granted only as designed into the policy, not trimmed after the fact: every identity and process gets exactly what it needs, nothing more.",
    "- **Learning mode** — An observation phase before enforcement: the system records normal application behavior so the baseline reflects reality instead of guesses.",
    "- **Baselining** — The recorded inventory of legitimate applications, paths, publishers, and behaviors that becomes the initial allowlist.",
    "- **Approval workflow** — The human process by which new or changed applications enter the allowlist: request, review, approve, audit.",
    "- **Deny-by-default operations** — Day-two reality: handling block events, exceptions, break-glass, and policy updates without grinding the business to a halt.",
    "- **Operational cost of deny-by-default** — The honest price: baselining effort, approval latency, exception management — and the cost of *not* paying it, which is incident response.",
],
'procedure_intro': (
    "Design like a defender who has to answer the help desk on Monday morning. You will convert allow-by-default habits "
    "into deny-by-default policy — and prove the business still functions."
),
'procedure_steps': [
    "1. **Take inventory.** List every application class Harborview's office workers need in a week: browser, office suite, PDF reader, line-of-business apps, updaters, drivers. Be exhaustive — the allowlist is only as good as the inventory.",
    "2. **Classify built-in vs. custom.** Mark which are standard vendor applications and which are custom or line-of-business. Custom apps need publisher or hash rules; standard ones can ride publisher trust.",
    "3. **Simulate learning mode.** For three representative applications, write down what 'normal' looks like: install path, publisher, child processes, network destinations. This is your baseline — enforcement without it is guessing.",
    "4. **Write the deny rule.** State the default-deny policy in one sentence: 'Only applications matching an approved rule may execute; all else is blocked and logged.' Then write the first three allow rules from your baseline.",
    "5. **Design the approval workflow.** A warehouse supervisor needs a new label-printing utility by Friday. Map the request → review → approve → deploy → audit path, and set a service-level target so security doesn't become the department of 'no.'",
    "6. **Plan for breakage.** Write the business-continuity plan for day one of enforcement: how block events are triaged, who can grant emergency exceptions, and the rollback criteria. A deny-by-default rollout without this plan gets reverted by Friday.",
    "7. **Price it honestly.** List the operational costs — baselining hours, approval latency, exception reviews — and the avoided cost: one ransomware incident's downtime. Present both numbers; defenders who hide costs lose trust.",
],
'project': (
    "**Harborview Freight — allowlist deployment plan.** Deliverable: a three-phase plan (baseline in learning mode, pilot enforcement on 25 office endpoints, "
    "fleet-wide enforcement) with the application inventory, the first-draft allow rules, the approval workflow with service levels, and the "
    "business-continuity plan for enforcement day. Include the honest cost section. The operations manager must sign off — write for her, not for me."
),
'checkin': [
    "In one line each: allowlisting vs. denylisting — and why does the default answer matter?",
    "Why does learning mode come before enforcement? What breaks if you skip it?",
    "Walk Noah through your break-glass exception path: who approves, how fast, and what gets logged?",
],
'cards': [
    {"front": "Allowlisting vs denylisting, in one line each?",
     "back": "Allowlisting (deny by default): only approved applications run. Denylisting (allow by default): everything runs except known-bad items."},
    {"front": "Why run allowlisting in learning mode before enforcement?",
     "back": "To baseline normal application behavior, so enforcement blocks attacks without breaking legitimate work."},
    {"front": "What does least privilege require?",
     "back": "Every identity and process gets only the access it needs — enforced by construction in the policy, not trimmed after the fact."},
    {"front": "What is an approval workflow in an allowlisting program?",
     "back": "The human process for admitting new or changed applications: request, review, approve, deploy, audit — with service levels so security doesn't become the department of 'no.'"},
    {"front": "What is the honest operational cost of deny-by-default?",
     "back": "Baselining effort, approval latency, and exception management — weighed against the avoided cost of incident response when novel malware is blocked by default."},
    {"front": "Why does denylisting fail against novel malware?",
     "back": "Its default answer is 'yes': anything not already known-bad is permitted, so first-seen malware executes before anyone has a signature for it."},
],
'quiz': [
    {"q": "A default-deny architecture is best described as:",
     "choices": ["Everything runs except known malware", "Nothing runs unless explicitly approved — the default answer is 'no'", "Only administrators may run applications", "Applications run in a sandbox by default"],
     "answer": 1,
     "explain": "Covered in Concepts: default-deny equals allowlisting — only approved applications execute."},
    {"q": "Learning mode comes before enforcement because:",
     "choices": ["It satisfies auditors", "Baseline first, enforce second: the recorded normal behavior becomes the initial allowlist", "It reduces licensing costs", "Enforcement requires a reboot"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: enforcement without a baseline is guessing — learning mode records reality first."},
    {"q": "A warehouse supervisor needs a new label printer utility by Friday under your allowlist program. What is the correct path?",
     "choices": ["Install it immediately; security reviews later", "Route it through the approval workflow: request, review, approve, deploy, audit — within the published service level", "Add the whole vendor's catalog to the allowlist permanently", "Disable enforcement on warehouse endpoints"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: the approval workflow exists precisely for this — fast, audited admission without breaking deny-by-default."},
    {"q": "Which of the following is a topic covered in \"Default-Deny Architecture\"?",
     "choices": ["Password hash synchronization", "Operational cost of deny-by-default", "TLS handshake walkthrough", "Kerberos ticket abuse"],
     "answer": 1,
     "explain": "Covered in Concepts: the module's topics include the honest operational cost of deny-by-default; the others belong to later modules."},
],
},

# =====================================================================
# PATH 2 — il11-network-crypto-foundations
# =====================================================================

'il11-network-crypto-foundations--zt-osi-tcpip': {
'title': 'OSI and TCP/IP Under Attack',
'summary': (
    "Welcome to Module 5. I'm your instructor, and today we rebuild your mental model of the network — because every "
    "attack you'll ever defend against lives at a specific layer, and controls placed at the wrong layer fail silently. "
    "We will walk the seven OSI layers and the four TCP/IP layers, map each attack class to its home, trace the TLS "
    "handshake, and read packet anatomy the way a defender does. By the end, 'the network' will stop being one blurry "
    "thing and become seven (or four) precise places where things can go wrong."
),
'objectives': [
    "Name the seven OSI layers and the four TCP/IP layers in order",
    "Map common attack classes (phishing, injection, MITM, spoofing, DDoS) to their layers",
    "Walk through the TLS handshake and state what each phase accomplishes",
    "Read packet anatomy and identify which fields attackers abuse at each layer",
],
'concepts': [
    "- **OSI model (seven layers)** — Physical, Data Link, Network, Transport, Session, Presentation, Application: the reference framework for where network functions — and attacks — live.",
    "- **TCP/IP model (four layers)** — Link, Internet, Transport, Application: the practical model the real internet runs on; OSI's upper three layers collapse into TCP/IP's Application layer.",
    "- **Encapsulation** — Each layer wraps the layer above's data with its own header; defenders read those headers to see what each layer claims — and attackers forge them.",
    "- **Layer 2 attacks** — ARP spoofing, MAC flooding: the attacker is (or pretends to be) on the local wire.",
    "- **Layer 3/4 attacks** — IP spoofing, SYN floods, port scanning: abuse of routing and transport mechanics.",
    "- **Layer 7 attacks** — Phishing, SQL injection, session hijacking: the application layer, where user input becomes code's problem.",
    "- **TLS handshake** — The negotiation that precedes encrypted communication: client and server agree on protocol version and ciphers, authenticate the server (certificates), and establish session keys.",
    "- **Packet anatomy** — Headers (Ethernet, IP, TCP/UDP) plus payload: each header is both a control surface and an attack surface.",
    "- **Misplaced controls** — A control at the wrong layer (e.g., trying to stop phishing with a firewall rule) fails because it cannot see what the attack actually abuses.",
],
'procedure_intro': (
    "Map attacks to layers until it becomes reflex. Defenders who can place an attack in under five seconds "
    "choose the right control the first time."
),
'procedure_steps': [
    "1. **Write both stacks from memory.** OSI's seven, TCP/IP's four, in order, top to bottom. Check yourself, then do it again until it's automatic.",
    "2. **Place five attacks.** Take phishing, SQL injection, ARP spoofing, SYN flood, and session hijacking — assign each to its layer and write one sentence justifying the placement.",
    "3. **Trace a packet.** Follow one HTTPS request from browser to server, naming which layer adds which header at each step. Mark where TLS sits and what it protects (and what it doesn't).",
    "4. **Walk the TLS handshake.** Write the phases in order: hello and cipher negotiation, certificate presentation and validation, key establishment, encrypted session. For each phase, name what fails if an attacker interferes.",
    "5. **Break one layer.** Pick ARP spoofing at Layer 2: write exactly which header field is forged and what the victim's machine believes afterward. Precision here is the skill.",
    "6. **Place the controls.** For each of your five attacks, name the control that belongs at its layer — and name a control at the *wrong* layer that would fail. Write the failure reason in one line.",
    "7. **Teach it back.** Explain to an imaginary junior why 'the firewall will stop the phishing' is a layer error. If your explanation needs no jargon, you've got it.",
],
'project': (
    "**Harborview Freight — layer-mapped threat model.** Deliverable: a table of the ten attack classes most relevant to Harborview "
    "(phishing against dispatchers, ransomware over SMB, credential theft on warehouse Wi-Fi, and seven more you choose), each mapped to "
    "its OSI/TCP/IP layer, the header or protocol feature it abuses, and the correctly-placed control. One page, no filler — the CISO "
    "will use it to justify the control budget."
),
'checkin': [
    "Recite both stacks. Then place: SQL injection, ARP spoofing, SYN flood.",
    "Walk Noah through the TLS handshake — what does each phase accomplish, and what breaks if it's attacked?",
    "Give Noah one example of a control placed at the wrong layer, and explain the failure.",
],
'cards': [
    {"front": "How many layers do the OSI and TCP/IP models define?",
     "back": "Seven OSI layers, four TCP/IP layers — and defenders map each attack class to the layer where it lives."},
    {"front": "What does the TLS handshake accomplish?",
     "back": "Client and server negotiate ciphers and establish an encrypted session — the walkthrough: hello/negotiation, certificate validation, key establishment, encrypted traffic."},
    {"front": "What is encapsulation, and why do defenders care?",
     "back": "Each layer wraps the layer above's data with its own header. Defenders read those headers to verify claims — attackers forge them, so each header is both control surface and attack surface."},
    {"front": "Place these attacks: ARP spoofing, SYN flood, phishing.",
     "back": "ARP spoofing: Layer 2 (Data Link) — forged ARP replies. SYN flood: Layer 4 (Transport) — half-open TCP handshakes. Phishing: Layer 7 (Application) — social engineering delivered through apps."},
    {"front": "What is a misplaced control? Give an example.",
     "back": "A control at the wrong layer for the attack — e.g., expecting a network firewall to stop phishing, which abuses Layer 7 trust in the message, not Layer 3/4 traffic the firewall inspects."},
    {"front": "Which fields of a packet do attackers abuse at Layers 2–4?",
     "back": "MAC addresses and ARP mappings at Layer 2; source IPs at Layer 3; TCP flags and sequence numbers at Layer 4 — the mechanics of delivery, forged to misdirect or overwhelm."},
],
'quiz': [
    {"q": "The OSI model has __ layers; the TCP/IP model has __.",
     "choices": ["Four; seven", "Seven; four", "Five; five", "Seven; seven"],
     "answer": 1,
     "explain": "Covered in Concepts: seven OSI layers, four TCP/IP layers — the module's framing."},
    {"q": "An attacker forges ARP replies to intercept warehouse Wi-Fi traffic. At which layer does this attack live?",
     "choices": ["Layer 7 (Application)", "Layer 4 (Transport)", "Layer 2 (Data Link)", "Layer 3 (Network)"],
     "answer": 2,
     "explain": "Covered in Concepts and Hands-on procedure: ARP spoofing forges Layer 2 mappings on the local wire."},
    {"q": "During the TLS handshake, what is the purpose of the certificate validation phase?",
     "choices": ["Compressing the session data", "Authenticating the server's identity before keys are established", "Choosing the TCP port", "Encrypting the DNS lookup"],
     "answer": 1,
     "explain": "Covered in Concepts: the handshake's certificate phase authenticates the server so keys are established with the right party."},
    {"q": "Which module covers \"Where each attack class lives\"?",
     "choices": ["Hashing for Integrity", "NIST SP 800-207 Tenets", "OSI and TCP/IP Under Attack", "Encryption in Practice"],
     "answer": 2,
     "explain": "Covered in Concepts: layer-by-layer attack mapping is the core of the OSI and TCP/IP module; the other options are different modules' topics."},
],
},

'il11-network-crypto-foundations--zt-hashing': {
'title': 'Hashing for Integrity',
'summary': (
    "Welcome to Module 6. I'm your instructor, and today we take up the defender's favorite mathematical tool: hashing. "
    "You'll learn the SHA-2 family, why salts belong in every password store, how file-integrity monitoring catches "
    "tampering, and why MD5 is dead — killed by practical collision attacks, not by opinion. This is a hands-on module: "
    "you will verify downloads, detect tampering, and build the reflex of never trusting a file you haven't hashed."
),
'objectives': [
    "Explain what a cryptographic hash function guarantees and what it does not",
    "Verify a downloaded file's integrity against a published hash using local tools",
    "Explain salting and why unsalted password hashes fall to rainbow tables",
    "Describe file-integrity monitoring and why MD5 must not be used for it",
],
'concepts': [
    "- **Cryptographic hash function** — A one-way function mapping arbitrary input to a fixed-size digest: deterministic, fast to compute, infeasible to reverse, and avalanche-sensitive (tiny input change, totally different digest).",
    "- **SHA-2 family** — SHA-224, SHA-256, SHA-384, SHA-512: current standard practice for integrity checking; SHA-256 is the workhorse you'll meet everywhere.",
    "- **Collision** — Two different inputs producing the same digest. A practical collision attack breaks a hash for integrity use — which is exactly what happened to MD5.",
    "- **MD5 deprecation** — MD5 is dead for security purposes: practical collision attacks exist, so it proves nothing about integrity. It survives only in non-security checksums.",
    "- **Salt** — Random per-password data mixed in before hashing, so identical passwords produce different hashes — defeating rainbow-table lookups.",
    "- **Rainbow table** — A precomputed table of hash-to-password mappings; salting and slow, memory-hard password hashing are the defenses.",
    "- **File-integrity monitoring (FIM)** — Recording known-good hashes of critical files and alerting on change: the tripwire that catches tampering.",
    "- **Digest vs. encryption** — Hashing is one-way and has no key to 'decrypt' with; encryption is reversible with the key. Confusing them is a classic interview failure.",
],
'procedure_intro': (
    "Hash with your own hands. Every concept in this module is verifiable in under a minute on your own machine — "
    "do the labs, don't just read about them."
),
'procedure_steps': [
    "1. **Hash a file.** Pick any file on your machine and compute its SHA-256 with your OS's built-in tool (certutil on Windows, shasum/sha256sum on macOS/Linux). Record the digest.",
    "2. **Flip one bit.** Copy the file, change a single character, hash the copy. Compare digests — the avalanche effect, witnessed, not described.",
    "3. **Verify a real download.** Download any utility that publishes SHA-256 checksums, hash what you downloaded, and compare. This is the professional reflex: never install what you haven't verified.",
    "4. **Break MD5's reputation.** Hash the same file with MD5 and SHA-256 side by side. Then write, in your own words, why the MD5 digest proves nothing about integrity even though it 'looks like' a hash.",
    "5. **Salt on paper.** Take the password 'summer2024' and two different salts; sketch why the two stored hashes differ and why a rainbow table built for unsalted hashes is now useless.",
    "6. **Design a FIM tripwire.** Choose five critical files on a Harborview server (you pick which). Write the baseline-and-alert procedure: when baselines are taken, where they're stored (not on the monitored machine), and what an alert triggers.",
    "7. **Teach the distinction.** Explain hash-vs-encryption to an imaginary junior in three sentences. If 'decrypt the hash' appears anywhere, start over.",
],
'project': (
    "**Harborview Freight — integrity verification standard.** Deliverable: a one-page standard operating procedure for Harborview IT: "
    "which downloads must be hash-verified before installation, the approved hash family (SHA-256 or stronger — never MD5), the FIM baseline "
    "procedure for dispatch servers, and the password-storage rule (salted, slow hashes; no unsalted SHA-anything). Written so a new hire can follow it Monday morning."
),
'checkin': [
    "Why is MD5 dead for integrity — and what, exactly, does a collision attack prove?",
    "Walk Noah through verifying a download: which tool, which comparison, what decision follows a mismatch?",
    "Why do identical passwords need different stored hashes? Explain salting without saying 'rainbow table' twice.",
],
'cards': [
    {"front": "Why is MD5 dead for integrity checking?",
     "back": "Practical collision attacks: two different inputs can share an MD5 hash, so it proves nothing about integrity."},
    {"front": "Why salt passwords before hashing?",
     "back": "Salts make identical passwords hash differently, defeating rainbow-table lookups."},
    {"front": "What does a cryptographic hash function guarantee?",
     "back": "Deterministic, fast, one-way, avalanche-sensitive digests — integrity evidence, not secrecy. It does not encrypt and cannot be 'decrypted.'"},
    {"front": "What is file-integrity monitoring (FIM)?",
     "back": "Recording known-good hashes of critical files and alerting on change — the tripwire that catches tampering. Baselines must live off the monitored machine."},
    {"front": "Hash vs. encryption — the distinction that matters in an interview?",
     "back": "Hashing is one-way with no key and no decryption; encryption is reversible with the key. A digest proves integrity; ciphertext protects confidentiality."},
    {"front": "What defeats rainbow tables besides salting?",
     "back": "Slow, memory-hard password hashing functions that make precomputation infeasible — salting forces per-password work, slowness makes that work expensive."},
],
'quiz': [
    {"q": "Which hash family is current practice for integrity checking?",
     "choices": ["MD5", "SHA-1", "SHA-2 (e.g., SHA-256)", "CRC32"],
     "answer": 2,
     "explain": "Covered in Concepts: SHA-2 is current standard practice; MD5 is dead from collisions and SHA-1 is deprecated."},
    {"q": "You download a vendor installer and its published SHA-256 checksum. The computed hash does not match. What do you do?",
     "choices": ["Install it anyway; checksums are advisory", "Re-download once, and if it still mismatches, do not install — treat the file as untrusted", "Disable the antivirus and retry", "Hash it with MD5 instead"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: a mismatch means the file is not what the publisher shipped — verify, and never install the unverified."},
    {"q": "Two users choose the same password. Why must their stored hashes differ?",
     "choices": ["To save database space", "Salting makes identical passwords hash differently, defeating rainbow-table lookups", "Different hashes are required by password-complexity rules", "So users cannot share accounts"],
     "answer": 1,
     "explain": "Covered in Concepts: per-password salts ensure identical passwords produce different digests."},
    {"q": "Which module covers \"Hash collisions and deprecation\"?",
     "choices": ["Hashing for Integrity", "Encryption in Practice", "OSI and TCP/IP Under Attack", "NIST SP 800-207 Tenets"],
     "answer": 0,
     "explain": "Covered in Concepts: collision-driven deprecation (MD5's death) is the core cautionary tale of the hashing module."},
],
},

'il11-network-crypto-foundations--zt-encryption': {
'title': 'Encryption in Practice',
'summary': (
    "Welcome to Module 7. I'm your instructor, and today we make encryption a decision tool, not a buzzword. Symmetric "
    "versus asymmetric, key exchange, certificates and PKI, and the three data states — at rest, in transit, in use. "
    "You'll run scenario drills: choose the right control for each state and justify the key-management plan, because "
    "encryption with lost or stolen keys is just expensive obfuscation."
),
'objectives': [
    "Contrast symmetric and asymmetric encryption and state when each is used",
    "Explain key exchange and why it exists as a distinct problem",
    "Describe certificates and PKI: what a certificate binds, and what a trust chain proves",
    "Choose encryption controls for data at rest, in transit, and in use — with a key-management justification",
],
'concepts': [
    "- **Symmetric encryption** — One shared secret encrypts and decrypts; fast, ideal for bulk data — and useless until both sides somehow share the secret securely.",
    "- **Asymmetric encryption** — A public/private key pair: public encrypts (or verifies), private decrypts (or signs). Slow for bulk data; perfect for key exchange and identity.",
    "- **Hybrid use** — The standard pattern: asymmetric encryption exchanges a symmetric session key, then symmetric encryption carries the bulk data. TLS works this way.",
    "- **Key exchange** — The distinct problem of getting the secret to the other party without an attacker intercepting it — the reason asymmetric cryptography exists.",
    "- **Certificate** — A signed binding of an identity to a public key, issued by a certificate authority (CA).",
    "- **PKI (public key infrastructure)** — The system of CAs, certificates, revocation, and trust stores that makes 'this public key belongs to that server' a verifiable claim.",
    "- **Trust chain** — Certificates chained from the server's leaf certificate up through intermediates to a trusted root; validation walks the whole chain, checking signatures, expiry, and revocation.",
    "- **Data at rest** — Stored data: disk/volume/file encryption protects it when the device is lost or stolen.",
    "- **Data in transit** — Moving data: TLS protects it against interception and tampering on the wire.",
    "- **Data in use** — Data being processed: the hardest state — protected by memory isolation, confidential computing, and minimizing what ever sits in plaintext.",
    "- **Key management** — Generation, distribution, rotation, revocation, and destruction of keys: the plan that decides whether encryption is real or theater.",
],
'procedure_intro': (
    "Decide like an architect. For each scenario you will pick the control, name the key-management plan, and defend "
    "both — because the wrong encryption in the right place still fails."
),
'procedure_steps': [
    "1. **Draw the hybrid handshake.** Sketch how asymmetric key exchange hands off to symmetric bulk encryption. Label which key does what, and where each key lives.",
    "2. **Break the chain on paper.** Take a certificate chain — leaf, intermediate, root — and invalidate each link in turn: expired leaf, revoked intermediate, untrusted root. Write what the client must do in each case.",
    "3. **Sort the data states.** List five Harborview data flows (dispatch database backups, driver PII in transit, laptop disks, API traffic, in-memory session tokens) and assign each to at rest, in transit, or in use.",
    "4. **Choose the controls.** For each flow, name the encryption control: volume encryption, TLS, field-level encryption, tokenization — and write the one-line justification.",
    "5. **Write the key plan.** For your chosen controls, answer: who generates the keys, where they're stored, how often they rotate, how revocation works, and what happens when a key is suspected compromised.",
    "6. **Find the theater.** Invent a 'we encrypt everything' claim with no key-management plan, then write the three questions that expose it. Keep those questions — you'll use them for years.",
    "7. **State the rule.** In one sentence: when do you use asymmetric, and when symmetric? If your sentence doesn't mention key exchange vs. bulk data, refine it.",
],
'project': (
    "**Harborview Freight — encryption standard.** Deliverable: a two-page standard covering the three data states for Harborview's "
    "dispatch system: volume encryption for servers and laptops (at rest), TLS for all API and web traffic (in transit), and the in-use "
    "handling rules for driver PII in memory. Include the key-management plan — generation, storage, rotation, revocation — and the "
    "certificate lifecycle for their public-facing services. The auditor reads this first; make it airtight."
),
'checkin': [
    "When do you use asymmetric instead of symmetric — and why does the hybrid pattern exist?",
    "Walk Noah through validating a certificate chain: what is checked, in what order?",
    "Name one control for each data state and defend the key-management plan behind it.",
],
'cards': [
    {"front": "When do you use asymmetric encryption instead of symmetric?",
     "back": "For key exchange and identity (certificates) — then switch to symmetric for bulk data."},
    {"front": "What does PKI provide?",
     "back": "Certificates binding identities to public keys, chained to trusted roots — the verifiable claim that a public key belongs to a given server."},
    {"front": "Name one encryption control for data at rest, in transit, and in use.",
     "back": "At rest: disk or volume encryption. In transit: TLS. In use: memory isolation and minimizing plaintext exposure (confidential computing where available)."},
    {"front": "Why does key exchange exist as a distinct problem?",
     "back": "Symmetric encryption is useless until both sides share the secret — and sharing it over an insecure channel is exactly what an attacker wants to intercept. Asymmetric cryptography solves the sharing problem."},
    {"front": "What must a client check when validating a certificate chain?",
     "back": "The full chain from leaf to trusted root: signatures at each link, expiry dates, revocation status, and that the name matches the intended server."},
    {"front": "What is key management, and why does it decide whether encryption is real?",
     "back": "Generation, distribution, rotation, revocation, and destruction of keys. Encryption with lost, shared, or unrevocable keys is theater — the plan is the control."},
],
'quiz': [
    {"q": "Symmetric encryption uses __; asymmetric uses __.",
     "choices": ["A public/private pair; one shared secret", "One shared secret; a public/private key pair", "No keys; passwords only", "Certificates; session cookies"],
     "answer": 1,
     "explain": "Covered in Concepts: symmetric shares one secret; asymmetric splits the work across a key pair."},
    {"q": "A Harborview API carries driver PII between the mobile app and the dispatch server. Which control fits, and why?",
     "choices": ["Volume encryption on the server — it protects data in transit", "TLS — it protects data in transit against interception and tampering", "Hashing the PII — it encrypts the payload", "A firewall rule — it encrypts the traffic"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: in-transit data gets TLS; volume encryption covers at rest, hashing is not encryption."},
    {"q": "A client receives a certificate whose intermediate CA has been revoked. What must the client do?",
     "choices": ["Trust it anyway if the leaf is valid", "Reject the chain — revocation anywhere in the chain breaks trust", "Skip to the root and trust the root directly", "Cache the certificate and retry tomorrow"],
     "answer": 1,
     "explain": "Covered in Concepts: validation walks the whole chain — a revoked link invalidates the trust the chain confers."},
    {"q": "Which module covers \"Certificates and PKI\"?",
     "choices": ["Encryption in Practice", "Hashing for Integrity", "OSI and TCP/IP Under Attack", "CISA Zero Trust Maturity Model"],
     "answer": 0,
     "explain": "Covered in Concepts: certificates and PKI are core topics of the encryption module."},
],
},

# =====================================================================
# PATH 3 — il11-active-directory-defense
# =====================================================================

'il11-active-directory-defense--zt-ad-structure': {
'title': 'AD Structure and Trust',
'summary': (
    "Welcome to Module 8. I'm your instructor, and we now enter the room where most enterprise breaches are actually "
    "won or lost: Active Directory. Before you can defend it — or understand a single attack against it — you need the "
    "mental model cold: domains, trees, forests, trust relationships, FSMO roles, and Group Policy as the control plane. "
    "Think of AD as the organization's identity nervous system. Every attack in the next module and every defense in the "
    "one after hangs on what you build here."
),
'objectives': [
    "Diagram how domains nest into trees and trees into forests, and what the forest boundary means",
    "Explain trust relationships: direction, transitivity, and what a trust actually grants",
    "Name the FSMO roles and explain why each is a single-master operation",
    "Describe Group Policy as a control plane: what it pushes, where it applies, and why attackers care",
],
'concepts': [
    "- **Domain** — The core AD unit: a replicated directory database with its own security policies and authentication authority.",
    "- **Tree** — Domains sharing a contiguous DNS namespace, linked by automatic two-way transitive trusts.",
    "- **Forest** — The security boundary: one or more trees sharing a schema, configuration, and global catalog. Compromise anywhere in the forest threatens the forest.",
    "- **Trust relationship** — A logical link letting users in one domain access resources in another; trusts have direction (one-way/two-way) and transitivity properties that define how far access flows.",
    "- **Transitive trust** — A trust that extends through intermediate domains: if A trusts B and B trusts C, A trusts C. Powerful — and the reason forest-wide compromise is possible.",
    "- **FSMO roles** — Flexible Single Master Operations: five roles held by single domain controllers — schema master, domain naming master, RID master, PDC emulator, infrastructure master — because some operations cannot safely be multi-master.",
    "- **Schema master / domain naming master** — Forest-wide roles: the schema master controls schema changes; the domain naming master controls adding/removing domains.",
    "- **RID master / PDC emulator / infrastructure master** — Domain-wide roles: RID allocates identifier pools; PDC emulator handles password changes and time sync; infrastructure master tracks cross-domain references.",
    "- **Group Policy** — The centralized configuration and security-policy engine for domain-joined machines: settings, scripts, and security policy pushed from domain controllers to OUs.",
    "- **Control plane** — Why attackers care about Group Policy and domain controllers: whoever controls the plane that configures every machine controls every machine.",
],
'procedure_intro': (
    "Build the model on paper before you touch a console. AD's abstractions are precise — sloppy mental models here "
    "become missed attack paths later."
),
'procedure_steps': [
    "1. **Draw the forest.** Sketch Harborview's AD: one forest, two domains (hq.harborview.local, warehouse.harborview.local) in one tree. Mark the forest boundary in red — label it 'the security boundary.'",
    "2. **Place the trusts.** Draw the automatic two-way transitive trust between the domains. Then add a one-way trust to a partner's domain and annotate the direction: which side's users can reach which side's resources?",
    "3. **Seat the FSMO roles.** Place all five roles on your drawing's domain controllers. For each, write what breaks if its holder is offline — this is why the roles are single-master and why their placement matters.",
    "4. **Map an OU hierarchy.** Design Harborview's OU structure: workstations, servers, domain controllers, service accounts. For each OU, note which Group Policy settings belong there.",
    "5. **Trace a policy.** Pick one setting (e.g., a software restriction or a security baseline) and trace it: authored where, linked where, applied to which machines, in what precedence order. Write each hop.",
    "6. **Think like the attacker.** Circle the three objects on your drawing an attacker wants most — the forest root, the PDC emulator, the Group Policy that touches every workstation — and write one line for each explaining why.",
    "7. **Recite the stack.** From memory: domain → tree → forest; the five FSMO roles; what Group Policy is. Gaps here compound in the next two modules — close them now.",
],
'project': (
    "**Harborview Freight — AD design review.** Deliverable: a two-page design review of Harborview's planned AD: the forest/domain/tree "
    "layout, trust direction and transitivity for the partner domain, FSMO role placement with failure analysis, and the OU + Group Policy "
    "design. Flag every design choice that widens the blast radius, and recommend the narrower alternative. The infrastructure lead will "
    "implement what you write — be precise."
),
'checkin': [
    "Draw the forest from memory: domains, tree, trusts, FSMO placement. Noah will check the trust directions.",
    "Why is the forest — not the domain — the security boundary?",
    "Explain to Noah why Group Policy is called a control plane, and why that makes it an attacker's prize.",
],
'cards': [
    {"front": "How do AD domains, trees, and forests nest?",
     "back": "Domains group into trees (contiguous namespace); trees group into a forest, which is the security boundary — compromise anywhere in the forest threatens the forest."},
    {"front": "What are FSMO roles?",
     "back": "Single-master operations roles — schema master, domain naming master, RID, PDC emulator, infrastructure master — because some operations cannot safely be multi-master."},
    {"front": "Why is Group Policy described as a control plane?",
     "back": "It centrally pushes configuration and security policy to domain-joined machines — whoever controls the plane that configures every machine controls every machine."},
    {"front": "What do trust direction and transitivity determine?",
     "back": "Direction determines whose users can reach whose resources; transitivity determines whether that access flows through intermediate domains — together they define how far a compromise can travel."},
    {"front": "Which FSMO roles are forest-wide, and which are domain-wide?",
     "back": "Forest-wide: schema master and domain naming master. Domain-wide: RID master, PDC emulator, and infrastructure master."},
    {"front": "What does the PDC emulator do, and why do attackers care about it?",
     "back": "It handles password changes and time sync for the domain — making it a high-value target: password operations and authentication flow through it."},
],
'quiz': [
    {"q": "Which of the following is the AD security boundary?",
     "choices": ["The organizational unit", "The domain", "The forest", "The site"],
     "answer": 2,
     "explain": "Covered in Concepts: the forest is the security boundary — compromise anywhere in the forest threatens the forest."},
    {"q": "A one-way trust exists where Domain A trusts Domain B. What does this mean?",
     "choices": ["Users in A can access resources in B", "Users in B can access resources in A", "Both directions are allowed", "No access flows either way"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: trust direction defines whose users reach whose resources — A trusting B lets B's users into A's resources."},
    {"q": "Why are the FSMO roles single-master instead of multi-master?",
     "choices": ["To reduce licensing costs", "Some operations — schema changes, RID allocation, naming — cannot safely run concurrently on multiple controllers", "Single-master is faster for all operations", "Microsoft requires it for support contracts"],
     "answer": 1,
     "explain": "Covered in Concepts: operations like schema changes and RID pool allocation would conflict if multi-master, so one holder is authoritative."},
    {"q": "Which module covers \"Group Policy as control plane\"?",
     "choices": ["How AD Gets Hacked", "Hardening the Identity Plane", "AD Structure and Trust", "Hybrid Identity"],
     "answer": 2,
     "explain": "Covered in Concepts: Group Policy as the centralized configuration control plane is the foundation topic of the AD structure module."},
],
},

'il11-active-directory-defense--zt-ad-attacks': {
'title': 'How AD Gets Hacked',
'summary': (
    "Welcome to Module 9. I'm your instructor, and this one is taught defense-first: we study how AD gets hacked so you "
    "can recognize, detect, and stop each technique. Kerberoasting and AS-REP roasting, pass-the-hash and pass-the-ticket, "
    "DCSync and DCShadow — you'll learn what each abuses, what logs it leaves, and what stops it, in lab-safe abstraction. "
    "No exploit code, no live targets: attack-path walkthroughs that make you a better defender, because you can't defend "
    "what you can't see coming."
),
'objectives': [
    "Explain Kerberoasting and AS-REP roasting: what each abuses and what it leaves in logs",
    "Explain pass-the-hash and pass-the-ticket: the credential-theft mechanics behind each",
    "Explain DCSync and DCShadow: how each mimics or abuses domain-controller replication",
    "Map each attack to its detection signals and its primary defensive control",
],
'concepts': [
    "- **Kerberoasting** — Abusing Kerberos service tickets: requesting a ticket-granting-service (TGS) ticket for a service account and cracking its encrypted portion offline to recover the account's password.",
    "- **AS-REP roasting** — Abusing accounts with Kerberos pre-authentication disabled: requesting authentication data that can be cracked offline, without any prior foothold credentials.",
    "- **Pass-the-hash** — Reusing a stolen NTLM password hash directly to authenticate — no password cracking required; the hash *is* the credential.",
    "- **Pass-the-ticket** — Reusing a stolen Kerberos ticket (TGT or service ticket) to authenticate as the victim, riding their existing authentication.",
    "- **DCSync** — Mimicking a domain controller's replication requests to pull password hashes from AD — abusing the replication protocol with stolen replication rights.",
    "- **DCShadow** — Registering a rogue domain controller to inject malicious replication changes into AD — pushing poison into the directory rather than pulling secrets out.",
    "- **Credential theft chain** — The common thread: steal a hash or ticket from memory or disk, then reuse it — which is why credential hygiene (next module) is the master defense.",
    "- **Log evidence** — What each technique leaves: bursts of TGS requests (Kerberoasting), anomalous logon types (pass-the-hash), replication requests from non-DCs (DCSync), unexpected DC registrations (DCShadow).",
    "- **Lab-safe abstraction** — Studying attack mechanics from documentation and diagrams, never against systems you don't own: the knowledge transfers, the liability doesn't.",
],
'procedure_intro': (
    "Walk each attack as a defender would reconstruct it: the abused mechanism, the log evidence, the control that stops it. "
    "For every technique, you will fill the same three-column table — abuse, evidence, defense."
),
'procedure_steps': [
    "1. **Build the attack table.** Make four rows — Kerberoasting/AS-REP roasting, pass-the-hash/pass-the-ticket, DCSync, DCShadow — and three columns: what it abuses, what logs it leaves, what stops it.",
    "2. **Trace Kerberoasting.** Write the ticket flow: attacker requests a TGS ticket for a service account, receives the encrypted portion, cracks it offline. Mark the log signal: a burst of TGS requests. Fill the defense column: strong, managed service-account passwords and AES Kerberos.",
    "3. **Trace AS-REP roasting.** Note the precondition that makes it possible — pre-authentication disabled — and the fix: enable pre-auth, audit for accounts lacking it.",
    "4. **Trace the pass-the-* pair.** For pass-the-hash: stolen NTLM hash reused directly. For pass-the-ticket: stolen Kerberos ticket replayed. Both share one defense family: keep credentials out of memory (Credential Guard) and limit where admins log on (tiering).",
    "5. **Trace the replication pair.** DCSync: attacker *pulls* hashes by mimicking a DC's replication. DCShadow: attacker *pushes* changes via a rogue DC. Defenses: restrict replication rights, monitor for replication from non-DCs and unexpected DC registrations.",
    "6. **Rank by blast radius.** Order the four techniques by worst-case impact on Harborview's forest, and write the one control you'd deploy first against each. Justify the ordering in two sentences.",
    "7. **Write the detection one-pager.** For Harborview's SOC: the log source, the query idea, and the expected signal for each technique. No product names — log sources and logic only.",
],
'project': (
    "**Harborview Freight — AD attack-path assessment.** Deliverable: a written assessment covering the four technique families against "
    "Harborview's AD design from Module 8. For each: the abused mechanism in Harborview's context, the log evidence their SOC should watch for, "
    "and the primary defensive control — mapped to the hardening module that follows. Conclude with the three highest-priority detections to "
    "deploy first. Defense-first framing throughout: this document teaches detection, not exploitation."
),
'checkin': [
    "Explain Kerberoasting vs. AS-REP roasting: what does each abuse, and what precondition enables AS-REP roasting?",
    "An analyst sees replication requests from a machine that isn't a domain controller. Which technique is suspected, and what's the first containment step?",
    "Why do pass-the-hash and pass-the-ticket share a defense family? Name the two defenses.",
],
'cards': [
    {"front": "What log evidence does Kerberoasting leave?",
     "back": "A burst of Kerberos service-ticket (TGS) requests — the detection angle: unusual volume of TGS requests, especially for service accounts."},
    {"front": "What does pass-the-hash abuse?",
     "back": "A stolen NTLM hash used directly to authenticate — no password cracking needed; the hash itself is the credential."},
    {"front": "What does DCSync mimic?",
     "back": "A domain controller's replication requests — the attacker pulls password hashes by abusing replication rights."},
    {"front": "What does DCShadow abuse?",
     "back": "Rogue DC replication: the attacker registers a fake domain controller to inject malicious changes into the directory."},
    {"front": "What enables AS-REP roasting, and what is the fix?",
     "back": "Accounts with Kerberos pre-authentication disabled let attackers request crackable authentication data; the fix is enabling pre-auth and auditing for accounts lacking it."},
    {"front": "What is the common thread across all four AD attack families?",
     "back": "Credential theft and reuse: steal a hash, ticket, or replication right, then reuse it — which is why credential hygiene is the master defense."},
],
'quiz': [
    {"q": "Kerberoasting abuses:",
     "choices": ["Weak Group Policy passwords", "Kerberos service tickets: requesting a TGS ticket and cracking its encrypted portion offline", "Unpatched domain controllers only", "Physical access to the server room"],
     "answer": 1,
     "explain": "Covered in Concepts: the attacker requests service tickets, then cracks the service account's secret offline."},
    {"q": "A SOC analyst sees DRS replication requests originating from a workstation that is not a domain controller. Which technique is most likely in play?",
     "choices": ["Phishing", "DCSync — mimicking DC replication to pull hashes", "SQL injection", "ARP spoofing"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: replication requests from non-DCs are the DCSync signal."},
    {"q": "Why do pass-the-hash and Credential Guard belong in the same sentence?",
     "choices": ["Credential Guard generates NTLM hashes", "Pass-the-hash reuses hashes from memory; Credential Guard isolates credentials so they can't be harvested", "They are both Group Policy settings for printers", "Credential Guard logs pass-the-hash attempts to the firewall"],
     "answer": 1,
     "explain": "Covered in Concepts: the theft-and-reuse chain is broken by keeping credentials out of attacker-reachable memory."},
    {"q": "Which module covers \"DCSync and DCShadow\"?",
     "choices": ["AD Structure and Trust", "Hardening the Identity Plane", "How AD Gets Hacked", "Hybrid Identity"],
     "answer": 2,
     "explain": "Covered in Concepts: the replication-abuse pair is the core of the AD attacks module."},
],
},

'il11-active-directory-defense--zt-ad-harden': {
'title': 'Hardening the Identity Plane',
'summary': (
    "Welcome to Module 10. I'm your instructor, and this is the payoff for the last two modules: the hardening runbook. "
    "You know the structure, you know the attacks — now you build the defenses. Tiered administration, LAPS and credential "
    "hygiene, Credential Guard and Protected Users, MFA and phishing-resistant authentication: each control mapped to the "
    "attack it kills from Module 9. By the end you'll hold a runbook, not a wish list."
),
'objectives': [
    "Design a tiered administration model: Tier 0, Tier 1, Tier 2 with credential-separation rules",
    "Explain LAPS and the credential-hygiene problem it solves",
    "Describe Credential Guard and Protected Users and which theft techniques each defeats",
    "Specify MFA and phishing-resistant authentication for privileged access",
],
'concepts': [
    "- **Tiered administration model** — Tier 0: the identity plane (domain controllers, AD itself). Tier 1: servers and their admins. Tier 2: workstations and their users. Credentials never flow downward: a Tier 0 credential never logs on to a Tier 1 or 2 machine.",
    "- **Privileged Access Workstation (PAW)** — A hardened, dedicated machine for Tier 0 administration: the admin's daily driver never touches the identity plane.",
    "- **LAPS (Local Administrator Password Solution)** — Gives each domain-joined machine a unique, randomized, automatically rotated local administrator password stored in AD — killing the shared-local-admin-password problem.",
    "- **Credential hygiene** — The discipline of minimizing where credentials exist: no domain-admin logons to workstations, no plaintext passwords in scripts, no cached credentials on compromised-prone hosts.",
    "- **Credential Guard** — Virtualization-based isolation of credentials in memory, defeating hash-dumping tools that feed pass-the-hash.",
    "- **Protected Users** — An AD security group imposing restrictions (no NTLM, no DES/RC4, no delegation, Kerberos ticket lifetime limits) on its members — hardening high-value accounts by policy.",
    "- **MFA (multi-factor authentication)** — Requiring two or more verification factors; for privileged access, only phishing-resistant forms count.",
    "- **Phishing-resistant authentication** — FIDO2 security keys, Windows Hello for Business, number-matching authenticator: methods a phishing page cannot relay or replay.",
    "- **Attack-to-control mapping** — The runbook discipline: every attack from Module 9 gets the control that kills it — Kerberoasting meets managed service accounts, pass-the-hash meets Credential Guard and tiering, DCSync meets replication-right restriction.",
],
'procedure_intro': (
    "Write the runbook Harborview will actually execute. Each control gets an owner, a rollout order, and the attack it kills — "
    "a hardening plan without those three is a suggestion."
),
'procedure_steps': [
    "1. **Draw the tiers.** On Harborview's AD drawing, color Tier 0 (DCs, AD), Tier 1 (member servers), Tier 2 (workstations). Write the iron rule across the top: credentials never flow downward.",
    "2. **Find the violations.** List every current practice that breaks the rule: domain admins on workstations, shared local admin passwords, service accounts with domain-admin rights. Each violation is a finding.",
    "3. **Deploy LAPS on paper.** Write the rollout: enable LAPS, verify unique rotated passwords per machine, define who may read them (Tier 0/1 admins only) and the audit trail. State the killed risk: lateral movement via shared local admin.",
    "4. **Isolate the credentials.** Specify Credential Guard enablement for privileged machines and Protected Users membership for Tier 0 accounts. Map each to its kill: Credential Guard vs. hash dumping, Protected Users vs. NTLM relay and ticket theft.",
    "5. **Harden authentication.** Write the MFA standard: phishing-resistant methods required for all privileged access; SMS and voice codes explicitly excluded for Tier 0. Justify the exclusion in one sentence each.",
    "6. **Build the attack-to-control map.** Take your Module 9 attack table and add the fourth column: the control from this module that kills each technique. Every attack must have an owner and a control — no orphans.",
    "7. **Sequence the runbook.** Order the rollout by risk reduction per effort: credential hygiene and LAPS first (cheap, high yield), tiering and PAWs next, then the long tail. Write the 30/60/90-day plan.",
],
'project': (
    "**Harborview Freight — identity-plane hardening runbook.** Deliverable: the executable runbook — tier model with credential-flow rules, "
    "LAPS rollout plan, Credential Guard and Protected Users specifications, the MFA/phishing-resistant authentication standard, and the "
    "attack-to-control map tying every Module 9 technique to its killer. Include owners and the 30/60/90-day sequence. The CISO approves "
    "funding off this document."
),
'checkin': [
    "State the tier rule in one sentence, then name three real-world violations of it.",
    "Which Module 9 attack does LAPS kill, and which does Credential Guard kill? Explain the mechanism in each case.",
    "Why are SMS codes excluded from the Tier 0 MFA standard? Defend the exclusion to Noah.",
],
'cards': [
    {"front": "What problem does LAPS solve?",
     "back": "Shared local administrator passwords: LAPS gives each machine a unique, rotated local admin password stored in AD — one compromised machine no longer yields the keys to all of them."},
    {"front": "What do the administrative tiers separate?",
     "back": "Tier 0: the identity plane (domain controllers). Tier 1: servers. Tier 2: workstations. Credentials never flow downward — a Tier 0 credential never logs on below its tier."},
    {"front": "What does Credential Guard protect?",
     "back": "Credentials stored in memory, using virtualization-based isolation — defeating the hash-dumping tools that feed pass-the-hash."},
    {"front": "What restrictions does the Protected Users group impose?",
     "back": "No NTLM authentication, no DES/RC4 Kerberos encryption, no unconstrained delegation, and limited Kerberos ticket lifetimes — hardening high-value accounts by policy."},
    {"front": "Name phishing-resistant authentication methods.",
     "back": "FIDO2 security keys, Windows Hello for Business, Authenticator with number matching — methods a phishing page cannot relay or replay."},
    {"front": "What is a Privileged Access Workstation (PAW) and which tier does it serve?",
     "back": "A hardened, dedicated machine used only for Tier 0 administration — so the admin's daily-driver workstation never touches the identity plane."},
],
'quiz': [
    {"q": "A help-desk tech routinely logs on to user workstations with a Domain Admin account. Which rule does this violate?",
     "choices": ["The password-complexity rule", "Tier separation: Tier 0 credentials must never log on to Tier 2 machines", "The backup-retention rule", "The software-approval workflow"],
     "answer": 1,
     "explain": "Covered in Concepts: credentials never flow downward — a Tier 0 credential on a workstation exposes the identity plane to any compromise of that workstation."},
    {"q": "Which control directly defeats pass-the-hash by protecting credentials in memory?",
     "choices": ["LAPS", "Group Policy software installation", "Credential Guard", "Longer password expiry"],
     "answer": 2,
     "explain": "Covered in Concepts: Credential Guard's virtualization-based isolation keeps hashes out of attacker-reachable memory."},
    {"q": "Why does the runbook exclude SMS codes for Tier 0 MFA?",
     "choices": ["SMS is too expensive", "SMS codes can be phished, SIM-swapped, and intercepted — they are not phishing-resistant", "Tier 0 admins don't carry phones", "SMS violates Kerberos policy"],
     "answer": 1,
     "explain": "Covered in Concepts: only phishing-resistant methods qualify for privileged access — SMS fails that bar."},
    {"q": "Which module covers \"Credential Guard / Protected Users\"?",
     "choices": ["AD Structure and Trust", "How AD Gets Hacked", "Hardening the Identity Plane", "Authentication and Authorization"],
     "answer": 2,
     "explain": "Covered in Concepts: both are hardening controls in the identity-plane runbook module."},
],
},

# =====================================================================
# PATH 4 — il11-allowlisting-ringfencing
# =====================================================================

'il11-allowlisting-ringfencing--zt-allowlist': {
'title': 'Application Allowlisting',
'summary': (
    "Welcome to Module 11. I'm your instructor, and we now put Module 4's default-deny doctrine into operational practice: "
    "application allowlisting. You'll learn the deployment playbook end to end — built-in versus custom applications, "
    "learning-mode baselining, approval workflows, and the day-two reality of deny-by-default operations. The human "
    "workflow matters as much as the technology: an allowlist the business can't live with gets turned off, and then you "
    "have nothing."
),
'objectives': [
    "Distinguish built-in and custom applications and the rule types each requires",
    "Design a learning-mode baselining plan that captures true normal behavior",
    "Write an approval workflow with service levels for new-application requests",
    "Operate deny-by-default: triage block events, manage exceptions, and keep the business running",
],
'concepts': [
    "- **Built-in applications** — Standard vendor software (OS components, common productivity suites): identifiable by publisher certificates, suitable for publisher-based rules.",
    "- **Custom applications** — Line-of-business and bespoke software: no widely-trusted publisher, so rules must use hashes, paths, or certificates you manage yourself.",
    "- **Publisher rule** — Trust based on the software publisher's signing certificate: any binary signed by that publisher is permitted — convenient, but only as trustworthy as the publisher's signing hygiene.",
    "- **Hash rule** — Trust based on the file's cryptographic hash: precise, but breaks on every update — best for stable, rarely-changing binaries.",
    "- **Path rule** — Trust based on file location: the weakest rule type, since any writer to that path can plant an executable — use only where nothing else fits, and lock the path down.",
    "- **Learning mode** — The observation phase that records which applications actually run in the environment, producing the evidence-based initial allowlist.",
    "- **Baselining** — The recorded inventory of legitimate applications, publishers, paths, and behaviors captured during learning mode.",
    "- **Approval workflow** — Request → review → approve → deploy → audit: the human pipeline admitting new software without breaking deny-by-default.",
    "- **Deny-by-default operations** — The ongoing practice: block-event triage, exception handling, policy updates on software release cycles, and periodic baseline re-validation.",
],
'procedure_intro': (
    "Deploy like you'll own the help-desk queue on Monday. Every rule you write will be lived with — "
    "make them livable."
),
'procedure_steps': [
    "1. **Inventory by class.** List Harborview's application classes: OS and drivers, browser, office suite, PDF tools, dispatch LOB app, label printers, updaters. Mark each built-in or custom.",
    "2. **Choose rule types.** Assign each class its rule: publisher rules for standard vendors, hash or managed-certificate rules for the custom LOB app, and — only where unavoidable — locked-down path rules. Justify each choice in one line.",
    "3. **Plan learning mode.** Define the baseline window (long enough to catch month-end and patch cycles — never just a quiet week), which endpoints participate, and what 'normal' evidence you require before a rule is written.",
    "4. **Write the first ten rules.** From your inventory, draft the initial allowlist: the ten rules covering 90% of legitimate executions. Everything else hits the default-deny wall — by design.",
    "5. **Design the request path.** A dispatcher needs a new PDF tool by Thursday. Map the workflow: who requests, who reviews for risk, who approves, how it deploys, and where the audit entry lands. Set the service level: e.g., standard requests within two business days.",
    "6. **Triage a block event.** Simulate: the dispatch LOB app updates overnight and its hash changes — Monday morning it won't launch. Write the triage: verify the update's legitimacy, update the hash rule, document, and restore service. Time-box each step.",
    "7. **Schedule the hygiene.** Write the recurring calendar: baseline re-validation after patch cycles, quarterly rule review, and the exception-expiry policy so temporary allowances don't become permanent holes.",
],
'project': (
    "**Harborview Freight — allowlist deployment playbook.** Deliverable: the complete playbook — application inventory with rule-type assignments, "
    "the learning-mode baselining plan, the first-draft allowlist, the approval workflow with service levels, the block-event triage procedure, "
    "and the recurring hygiene calendar. Pilot scope: 25 office endpoints, then fleet-wide. The operations manager co-signs — write it for her."
),
'checkin': [
    "When do you use a publisher rule vs. a hash rule vs. a path rule — and what is each one's weakness?",
    "Why must the learning-mode window cover a full business cycle, not just a quiet week?",
    "Walk Noah through Monday's triage: the LOB app updated overnight and won't launch. What do you do, in order?",
],
'cards': [
    {"front": "Why run allowlisting in learning mode before enforcement?",
     "back": "To baseline normal application behavior, so enforcement blocks attacks without breaking legitimate work."},
    {"front": "Publisher rule vs. hash rule vs. path rule — when is each appropriate?",
     "back": "Publisher: standard vendor software with trustworthy signing. Hash: stable custom binaries that rarely change. Path: last resort only, with the path locked down — any writer to the path can plant an executable."},
    {"front": "What makes a custom application harder to allowlist than a built-in one?",
     "back": "No widely-trusted publisher to anchor rules on — you must manage hashes, paths, or your own signing certificates, and every update breaks hash rules."},
    {"front": "What are the five stages of the approval workflow?",
     "back": "Request → review → approve → deploy → audit — with service levels so legitimate needs don't wait on security."},
    {"front": "What does deny-by-default operations cover on day two?",
     "back": "Block-event triage, exception handling with expiries, policy updates tracking software release cycles, and periodic baseline re-validation."},
    {"front": "Why is the human workflow as important as the technology in allowlisting?",
     "back": "An allowlist the business can't live with gets disabled — then there is no control at all. Service levels, triage speed, and honest exception handling keep deny-by-default alive."},
],
'quiz': [
    {"q": "Learning mode comes before enforcement because:",
     "choices": ["It satisfies auditors", "Baseline first, enforce second — the recorded normal behavior becomes the initial allowlist", "It reduces licensing costs", "Enforcement requires a reboot"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: enforcement without a baseline is guessing."},
    {"q": "Harborview's custom dispatch application updates monthly. Which rule type fits best, and why?",
     "choices": ["Hash rule — it never changes", "Publisher rule on Harborview's own signing certificate, or a managed hash updated with each release — because monthly updates break static hashes", "Path rule on the user's Downloads folder", "No rule; custom apps can't be allowlisted"],
     "answer": 1,
     "explain": "Covered in Concepts: hash rules break on every update, so a self-managed publisher certificate (or disciplined hash updates per release) fits a monthly-release custom app."},
    {"q": "A path rule is the weakest allowlist rule type because:",
     "choices": ["Paths are too long to type", "Any process that can write to that path can plant an executable that the rule then trusts", "Path rules expire after 30 days", "Paths change on every reboot"],
     "answer": 1,
     "explain": "Covered in Concepts: path rules trust location, not identity — a writer to the path defeats them."},
    {"q": "Which module covers \"Approval workflows\" for application admission?",
     "choices": ["Ringfencing Applications", "Application Allowlisting", "Storage & Elevation Control", "Detection & Response"],
     "answer": 1,
     "explain": "Covered in Concepts: the request-to-audit human pipeline is the allowlisting module's operational core."},
],
},

'il11-allowlisting-ringfencing--zt-ringfence': {
'title': 'Ringfencing Applications',
'summary': (
    "Welcome to Module 12. I'm your instructor. Allowlisting decides *what may run* — ringfencing decides *what a running "
    "application may do*. Even trusted applications get weaponized: browsers, Office, and scripting hosts are the exact "
    "boundary modern attacks cross. You'll design containment policies that limit app-to-app communication, file and "
    "registry interaction, and network egress per application — and you'll learn why blocking weaponized LOLBins is one of "
    "the highest-leverage defenses in endpoint security."
),
'objectives': [
    "Explain ringfencing: what it contains and how it differs from allowlisting",
    "Design ringfence policies for browsers, Office applications, and scripting hosts",
    "Identify LOLBins and explain why restricting them breaks common attack chains",
    "Specify per-application network egress controls",
],
'concepts': [
    "- **Ringfencing** — Containment around a running application: limiting what it may touch — other processes, files, registry keys, network destinations — even though it is allowed to run.",
    "- **Allowlisting vs. ringfencing** — Allowlisting answers 'may it execute?'; ringfencing answers 'once executing, what may it do?' Both are needed: trusted apps get exploited too.",
    "- **LOLBins (living-off-the-land binaries)** — Legitimate system tools — PowerShell, wmic, mshta, rundll32, certutil — weaponized by attackers because they're already present, signed, and trusted.",
    "- **App-to-app communication limits** — Restricting which processes an application may launch or inject into: the boundary that stops a compromised browser from spawning PowerShell.",
    "- **File and registry interaction limits** — Restricting which files, folders, and registry keys an application may read or write: the boundary that stops macro malware from dropping payloads.",
    "- **Network egress control per app** — Restricting which destinations an application may reach: the boundary that stops a compromised app from phoning home to attacker infrastructure.",
    "- **Weaponized scripting hosts** — PowerShell, WSH, and macro engines: the highest-value LOLBins, because they turn a document or a browser exploit into arbitrary code execution.",
    "- **Containment boundary** — Each ringfence rule is a boundary drawn exactly where modern attacks cross: the moment a benign app tries to do something no benign app should do.",
],
'procedure_intro': (
    "Draw the boundaries where attacks actually cross. You'll ringfence the three most-abused application classes — "
    "and prove each boundary against a real attack pattern."
),
'procedure_steps': [
    "1. **List the abused.** Write Harborview's top abused applications: the browser, the Office suite, the PDF reader, PowerShell. For each, name one real attack pattern that starts there (macro malware, browser exploit, script download).",
    "2. **Ringfence the browser.** Define its containment: which child processes may it launch (ideally: none beyond its own helpers), which files may it write (downloads folder only), which network destinations (any — it's a browser, but log it).",
    "3. **Ringfence Office.** Define: Office apps may not launch PowerShell, cmd, wscript, or mshta. They may write documents to user folders but not executables anywhere. Write each rule as 'app X may/may not do Y.'",
    "4. **Contain the scripting hosts.** PowerShell may run only signed scripts from the IT scripts share; wscript/cscript are blocked for standard users entirely. Justify each restriction against the attack patterns from step 1.",
    "5. **Set egress per app.** The dispatch LOB app may reach only the dispatch server and the update service. The PDF reader may reach nothing. Write the egress list as an explicit allowlist — default deny, like everything else here.",
    "6. **Test against the kill chain.** Take a macro-malware scenario end to end: malicious document → macro → PowerShell download → payload → egress. Mark which ringfence rule breaks each link. Every link should have a breaker.",
    "7. **Plan the exceptions.** The IT team legitimately scripts with PowerShell. Write the exception: who gets unrestricted scripting, on which machines, approved how, reviewed when. Exceptions are policy too — undocumented ones are holes.",
],
'project': (
    "**Harborview Freight — application containment standard.** Deliverable: the ringfence policy set for browsers, Office, PDF readers, "
    "and scripting hosts — app-to-app limits, file/registry limits, and per-app egress rules — plus the documented IT scripting exception. "
    "Include the kill-chain test from the Hands-on procedure showing each macro-malware link broken by a rule. The SOC uses this as its "
    "containment reference."
),
'checkin': [
    "In one sentence each: what does allowlisting decide, and what does ringfencing decide?",
    "Name three LOLBins and the attack pattern each enables.",
    "Walk Noah through the macro-malware kill chain and point to the ringfence rule that breaks each link.",
],
'cards': [
    {"front": "What does ringfencing restrict for an application?",
     "back": "What the app may touch: app-to-app communication, file and registry access, network destinations — containment around execution, not just permission to execute."},
    {"front": "How does ringfencing differ from allowlisting?",
     "back": "Allowlisting decides what may run; ringfencing decides what a running application may do. Trusted applications get exploited, so both layers are needed."},
    {"front": "What are LOLBins? Name three.",
     "back": "Living-off-the-land binaries: legitimate signed system tools weaponized by attackers — e.g., PowerShell, wmic, mshta (also rundll32, certutil)."},
    {"front": "Why is PowerShell the highest-value LOLBin to contain?",
     "back": "It turns a document or browser exploit into arbitrary code execution — full scripting power, already present and trusted on every Windows machine."},
    {"front": "What does per-application network egress control stop?",
     "back": "A compromised application phoning home: even if malware executes, it cannot reach attacker infrastructure if its app is egress-restricted to legitimate destinations."},
    {"front": "What belongs in a documented scripting exception for IT staff?",
     "back": "Who gets unrestricted scripting, on which machines, approved by whom, and reviewed when — exceptions are policy too; undocumented ones are holes."},
],
'quiz': [
    {"q": "Ringfencing an application primarily limits:",
     "choices": ["Which users may install it", "What the running application may touch: processes, files, registry, network", "The application's license count", "Which monitor displays it"],
     "answer": 1,
     "explain": "Covered in Concepts: ringfencing is containment around execution — the app-to-app, file, registry, and egress boundaries."},
    {"q": "LOLBins are:",
     "choices": ["A type of ransomware", "Living-off-the-land binaries — legitimate system tools like PowerShell weaponized by attackers", "USB attack devices", "Phishing email templates"],
     "answer": 1,
     "explain": "Covered in Concepts: LOLBins are already-present, signed, trusted tools turned to malicious use."},
    {"q": "A malicious Word document runs a macro that launches PowerShell to download a payload. Which ringfence rule breaks this chain earliest?",
     "choices": ["Blocking the browser's network egress", "Prohibiting Office applications from launching scripting hosts like PowerShell", "Hash-blocking the Word document", "Disabling the printer spooler"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: the Office-may-not-launch-PowerShell boundary breaks the macro-to-script link — the exact boundary this attack crosses."},
    {"q": "Which module covers \"Network egress control per app\"?",
     "choices": ["Application Allowlisting", "Storage & Elevation Control", "Ringfencing Applications", "Detection & Response"],
     "answer": 2,
     "explain": "Covered in Concepts: per-application egress is one of the ringfencing boundaries."},
],
},

'il11-allowlisting-ringfencing--zt-storage-elevation': {
'title': 'Storage & Elevation Control',
'summary': (
    "Welcome to Module 13. I'm your instructor. Applications need data and privilege to do their jobs — and both are "
    "exactly what ransomware and insider misuse need too. Today: storage control (which application may touch which "
    "share), elevation control (who gets admin rights, for how long), and removable-media control. You'll run scenario "
    "labs deciding each grant — and you'll see how these three controls together blunt ransomware's encryption paths."
),
'objectives': [
    "Design per-application network-share access: which app may touch which share",
    "Explain ransomware encryption paths and how storage control interrupts them",
    "Specify just-in-time elevation: who gets admin rights, for what task, for how long",
    "Write a USB and removable-media control policy balancing security and operations",
],
'concepts': [
    "- **Per-application share access** — Storage control at the application layer: not just 'which user may open the share' but 'which application, running as that user, may write to it.'",
    "- **Ransomware encryption paths** — The routes ransomware takes to data: mapped drives, network shares, and any writable path the executing process can reach. Every reachable writable share is an encryption target.",
    "- **Blast-radius reduction** — Limiting which applications can write where, so a compromised endpoint encrypts only what its allowed apps could touch — not the whole file server.",
    "- **Just-in-time (JIT) elevation** — Administrator rights granted temporarily for a bounded task and duration, then automatically revoked — replacing always-on admin rights.",
    "- **Standing privilege** — The opposite of JIT: admin rights that persist 24/7, waiting to be stolen. Every standing admin account is a standing target.",
    "- **Elevation workflow** — Request, approve, elevate for a bounded window, audit: the human pipeline that makes JIT livable.",
    "- **Removable-media control** — Policy over USB and external drives: block, read-only, or allow-by-exception — because removable media is both an exfiltration path and a malware ingress path.",
    "- **Data staging** — The attacker technique of collecting files in one place before exfiltration; media and egress controls aim to break this step.",
],
'procedure_intro': (
    "Decide each grant like the ransomware is already on the endpoint — because in the scenario that matters, it is. "
    "Every 'yes' you give must survive that assumption."
),
'procedure_steps': [
    "1. **Map the shares.** List Harborview's network shares: dispatch data, HR records, finance, warehouse scans. For each, note who uses it and which applications legitimately write to it.",
    "2. **Restrict by application.** For each share, write the allowed-writer list as applications, not just users: the dispatch share accepts writes from the dispatch LOB app only — not from the browser, not from Office, not from PowerShell.",
    "3. **Trace the encryption path.** Simulate ransomware executing as a dispatcher: which shares can it reach through allowed applications? Write the encryption path — then apply your step-2 restrictions and re-trace. The difference is the blast radius you removed.",
    "4. **Design JIT elevation.** The warehouse lead needs local admin twice a month for label-printer driver installs. Write the workflow: request, approval, time-bounded elevation (e.g., a two-hour window), automatic revocation, and the audit entry.",
    "5. **Kill standing privilege.** Inventory Harborview's always-on admin accounts. For each, decide: convert to JIT, scope down, or document the business justification for keeping it. 'Convenience' is not a justification — write that down.",
    "6. **Write the media policy.** Three tiers: blocked by default for standard users, read-only for warehouse scanners that need it, allow-by-exception with approval for IT. Include the malicious-USB-drop scenario from the red-team modules as the rationale.",
    "7. **Combine the three.** Write the one-paragraph story of a ransomware attempt against your hardened Harborview: where storage control stops the encryption path, where JIT denies the privilege escalation, where media control blocks the ingress. That paragraph is your executive summary.",
],
'project': (
    "**Harborview Freight — storage & elevation standard.** Deliverable: the three-part standard — per-application share-access matrix, "
    "the JIT elevation workflow with the standing-privilege inventory and dispositions, and the removable-media policy. Include the "
    "ransomware blast-radius analysis (before/after) from the Hands-on procedure. Finance signs off on the JIT workflow's approval chain — "
    "write it for them."
),
'checkin': [
    "Why is 'which application may write' a stronger question than 'which user may write' against ransomware?",
    "Walk Noah through your JIT elevation workflow: request to revocation, with the audit trail.",
    "Defend the media policy's middle tier: why read-only for warehouse scanners instead of full block or full allow?",
],
'cards': [
    {"front": "What is just-in-time elevation?",
     "back": "Administrator rights granted temporarily for a bounded task and duration, then automatically revoked — replacing always-on admin rights."},
    {"front": "How does storage control blunt ransomware?",
     "back": "By restricting which applications may write to network shares — the encryption paths. A compromised endpoint can then encrypt only what its allowed apps could touch."},
    {"front": "Why control USB and removable media?",
     "back": "They are both an exfiltration path and a malware ingress path (malicious USB drops) — control must cover data leaving and malware arriving."},
    {"front": "What is standing privilege, and why is it a target?",
     "back": "Admin rights that persist 24/7: always available to be stolen, phished, or misused. Every standing admin account is a standing target — JIT exists to eliminate it."},
    {"front": "What is a ransomware encryption path?",
     "back": "The route ransomware takes to data: mapped drives, network shares, any writable path the executing process can reach. Every reachable writable share is an encryption target."},
    {"front": "What must a JIT elevation workflow include to be livable?",
     "back": "Request, approval, a bounded time window, automatic revocation, and an audit entry — fast enough that users don't bypass it, strict enough that it means something."},
],
'quiz': [
    {"q": "Ransomware executes on a dispatcher's workstation as the dispatcher. Which control most limits what it can encrypt?",
     "choices": ["A stronger workstation password", "Per-application share access: only the dispatch LOB app — not the compromised browser or Office — may write to the dispatch share", "A bigger firewall", "More frequent reboots"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: storage control at the application layer shrinks the reachable encryption paths."},
    {"q": "Just-in-time elevation is preferable to standing admin rights because:",
     "choices": ["It is cheaper to license", "It shrinks the window in which stolen credentials grant privilege — rights exist only for the bounded task, then vanish", "Users prefer requesting access", "It eliminates the need for passwords"],
     "answer": 1,
     "explain": "Covered in Concepts: JIT replaces always-on targets with time-bounded grants."},
    {"q": "A warehouse scanner needs USB access to import delivery manifests, but USB drops are a known attack vector. What is the proportionate policy?",
     "choices": ["Full USB access for everyone — convenience wins", "Block USB entirely, including the scanners", "Read-only or allow-by-exception for the scanner role, blocked by default for everyone else", "Allow USB only on Fridays"],
     "answer": 2,
     "explain": "Covered in Hands-on procedure: tiered media policy — the operational need is met narrowly while the ingress/exfiltration path stays closed by default."},
    {"q": "Which module covers \"Just-in-time elevation\"?",
     "choices": ["Application Allowlisting", "Storage & Elevation Control", "Ringfencing Applications", "Identity Governance"],
     "answer": 1,
     "explain": "Covered in Concepts: JIT elevation is the privilege half of the storage-and-elevation module."},
],
},

# =====================================================================
# PATH 5 — il11-red-blue-operations
# =====================================================================

'il11-red-blue-operations--zt-social-engineering': {
'title': 'Social Engineering & Phishing',
'summary': (
    "Welcome to Module 14. I'm your instructor, and we now study the attack vector that bypasses nearly every technical "
    "control ever built: the human. Phishing, smishing, vishing, quishing — plus AI-assisted lures that removed the "
    "telltale broken English, and malicious USB drops for the physical angle. We do defensive teardowns: you'll dissect "
    "lure patterns for indicators, design reporting workflows, and layer the technical controls that catch what training "
    "misses — because training alone never will."
),
'objectives': [
    "Distinguish phishing, smishing, vishing, and quishing and the indicators of each",
    "Explain how AI assistance changed lure quality and what still gives lures away",
    "Describe malicious USB-drop attacks and the controls that defeat them",
    "Design a user-reporting workflow and the technical controls behind it",
],
'concepts': [
    "- **Phishing** — Fraudulent messages (email) impersonating trusted senders to steal credentials or deliver malware: still the dominant initial-access vector.",
    "- **Smishing** — Phishing via SMS: short, urgent, link-driven — exploiting the trust people place in text messages.",
    "- **Vishing** — Voice phishing: calls impersonating IT, banks, or executives — exploiting authority and urgency in real time.",
    "- **Quishing** — Phishing via QR codes: the code bypasses email link-scanning and moves the victim to the attacker's page on their phone.",
    "- **AI-assisted lures** — Generative AI removed the classic tells (broken grammar, wrong logos): modern lures are fluent, personalized, and correctly branded — defenders must pivot from 'spot the typo' to verifying through independent channels.",
    "- **Malicious USB drops** — Attack devices (Rubber Ducky class) that emulate keyboards and type malicious commands at machine speed when plugged in: the physical complement to phishing.",
    "- **Pretexting** — The invented scenario ('IT needs your password to fix the outage') that gives the lure its authority; every social-engineering attack has one.",
    "- **User-reporting culture** — The organizational norm that reporting a suspicious message is fast, easy, blame-free, and visibly acted on: the human sensor network.",
    "- **Defense in depth for humans** — Training plus reporting plus technical controls (email authentication, link detonation, MFA, allowlisting): no single layer is expected to hold alone.",
],
'procedure_intro': (
    "Dissect lures like a forensic analyst. For each pattern you will extract the pretext, the indicators, the reporting "
    "path, and the technical control that catches it when the human doesn't."
),
'procedure_steps': [
    "1. **Collect four lures.** Write (do not send) one realistic example each of phishing, smishing, vishing, and quishing targeting a Harborview dispatcher. Keep them plausible — the exercise is recognition, not creativity.",
    "2. **Extract the pretext.** For each lure, name the invented scenario and the authority it borrows. Write the one question that collapses it: 'Why would IT ask for this over text?'",
    "3. **List the indicators.** For each channel, write what a trained user can still check: sender domain vs. display name, URL preview, unexpected QR context, caller verification via callback. Note which indicators AI assistance erased (grammar tells) and which survive (out-of-band verification).",
    "4. **Design the report path.** A dispatcher gets the smishing text at 6:40 AM. Map the reporting workflow: one-tap report button, where the report goes, the SLA for triage, and the feedback the reporter receives. Blame-free and fast — or nobody reports.",
    "5. **Layer the technical controls.** For each lure, name the control that catches what training misses: email authentication and link detonation for phishing, phishing-resistant MFA so stolen passwords aren't enough, allowlisting so the payload can't run, media control for the USB drop.",
    "6. **Run the USB scenario.** A 'lost' USB drive appears in the Harborview parking lot. Walk the attack (keyboard-emulation payload at machine speed) and the defenses (media control policy from Module 13, endpoint containment). Write the two-line policy reminder for the break room.",
    "7. **Measure, don't moralize.** Write the metrics that prove the program works: report rate, mean time to triage, credential-reuse rate after simulations. Training shames people; metrics improve systems.",
],
'project': (
    "**Harborview Freight — social-engineering defense program.** Deliverable: the program document — the four-channel lure reference with "
    "indicators, the user-reporting workflow with SLAs, the layered technical controls mapped per channel, and the metrics dashboard definition. "
    "Include the break-room USB reminder. HR co-owns the reporting culture piece — write the culture section for them."
),
'checkin': [
    "Distinguish the four channels for Noah: what makes each one work, and what indicator survives AI-assisted lures?",
    "Walk Noah through the 6:40 AM smishing report: what happens, how fast, and what does the reporter hear back?",
    "A user clicked and entered credentials. Which technical controls limit the damage — and why is each one needed?",
],
'cards': [
    {"front": "Distinguish phishing, smishing, vishing, quishing in one line each.",
     "back": "Phishing: fraudulent email. Smishing: phishing via SMS. Vishing: voice-call phishing exploiting authority live. Quishing: phishing via QR codes that move victims to attacker pages on their phones."},
    {"front": "How did AI assistance change phishing defense?",
     "back": "It erased the classic tells — fluent, personalized, correctly branded lures. Defense pivots from 'spot the typo' to out-of-band verification and technical controls that don't depend on user detection."},
    {"front": "What is a malicious USB drop (Rubber Ducky class)?",
     "back": "An attack device emulating a keyboard: plugged in, it 'types' malicious commands at machine speed — the physical complement to phishing, defeated by media control and endpoint containment."},
    {"front": "What makes a user-reporting culture work?",
     "back": "Reporting is fast (one tap), easy, blame-free, and visibly acted on with feedback — turning users into a sensor network instead of a liability."},
    {"front": "A user entered credentials into a phishing page. Which controls limit the damage?",
     "back": "Phishing-resistant MFA (stolen password alone isn't enough), allowlisting (the payload can't run), and rapid reporting + credential reset workflow."},
    {"front": "What is pretexting, and why does every social-engineering attack need one?",
     "back": "The invented scenario that lends the lure authority ('IT needs your password for the outage fix') — without a believable pretext, the request looks absurd and fails."},
],
'quiz': [
    {"q": "Quishing is phishing delivered via:",
     "choices": ["QR codes", "Phone calls", "USB drives", "Fake login portals on the corporate intranet"],
     "answer": 0,
     "explain": "Covered in Concepts: quishing uses QR codes to move victims to attacker-controlled pages, bypassing email link inspection."},
    {"q": "AI-assisted lures defeated 'spot the typo' training. What is the correct defensive pivot?",
     "choices": ["Abandon all user training", "Verify through independent, out-of-band channels and rely on technical controls (phishing-resistant MFA, allowlisting) that don't depend on user detection", "Block all email attachments", "Require users to memorize attacker domains"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: when lures are flawless, defense moves to verification channels and controls that hold even when the human is fooled."},
    {"q": "A dispatcher finds an unfamiliar USB drive in the parking lot and considers plugging it in to identify the owner. What should happen?",
     "choices": ["Plug it into the dispatch workstation to check", "Hand it to IT unplugged — USB drops can emulate keyboards and execute payloads at machine speed; media-control policy governs handling", "Plug it into a personal phone instead", "Throw it in the trash unreported"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: Rubber Ducky-class devices attack on insertion — the policy is hand-to-IT, never plug in."},
    {"q": "Which module covers \"User-reporting culture\"?",
     "choices": ["Detection & Response", "Social Engineering & Phishing", "Web & Application Attacks", "Scenario Capstone"],
     "answer": 1,
     "explain": "Covered in Concepts: the blame-free, fast reporting workflow is the human-sensor core of the social-engineering module."},
],
},

'il11-red-blue-operations--zt-web-attacks': {
'title': 'Web & Application Attacks',
'summary': (
    "Welcome to Module 15. I'm your instructor. Attackers don't only phish humans — they attack the applications "
    "themselves: SQL injection, broken access control, session and token abuse, and the sprawling Microsoft 365 attack "
    "surface. You'll get lab-safe walkthroughs of the OWASP Top 10 against intentionally vulnerable targets you own, "
    "then build the fixes: parameterized queries, authorization checks, and the monitoring that catches what code misses. "
    "Every attack here is studied to build a defense."
),
'objectives': [
    "Explain SQL injection: the mechanism, and why parameterized queries fix it",
    "Explain broken access control: the missing-check patterns and their fixes",
    "Describe session and token abuse and the defenses (rotation, binding, expiry)",
    "Map the Microsoft 365 attack surface: consent phishing, legacy auth, token theft",
],
'concepts': [
    "- **SQL injection** — Untrusted input concatenated into database queries and executed as code: the classic Layer-7 attack, fixed by parameterized queries (never string-building SQL) and least-privilege database accounts.",
    "- **Broken access control** — Missing or flawed authorization checks: insecure direct object references, missing function-level checks, privilege escalation via parameter tampering. The OWASP perennial #1 for a reason.",
    "- **Insecure direct object reference (IDOR)** — Accessing another user's data by changing an identifier in the request (e.g., invoice/1024 → invoice/1025) because the server never checked ownership.",
    "- **Session hijacking** — Stealing a victim's session cookie or token to ride their authenticated session: defeated by secure cookie flags, rotation on privilege change, and short lifetimes.",
    "- **Token abuse** — Theft or misuse of OAuth/OIDC tokens and API keys: over-scoped tokens and tokens in URLs or logs are the usual failures.",
    "- **Consent phishing (illicit consent grant)** — Tricking a user into granting a malicious app OAuth permissions to their mailbox or files: the Microsoft 365-native phishing variant.",
    "- **Microsoft 365 attack surface** — Mail, SharePoint, Teams, Entra-integrated apps: legacy authentication protocols, overly-permissive app consent, and token theft are the recurring weaknesses.",
    "- **Parameterized queries** — The SQL injection fix: queries with bound parameters, so input is always data, never code.",
    "- **Lab-safe targets** — Intentionally vulnerable applications you own and run locally: the only ethical place to practice exploitation mechanics.",
],
'procedure_intro': (
    "Attack the lab, then fix it. Every technique gets the same treatment: reproduce against your own vulnerable target, "
    "understand the mechanism, then implement and verify the fix."
),
'procedure_steps': [
    "1. **Stand up the lab.** Deploy an intentionally vulnerable web app you own (local VM or container). Confirm: it runs locally, it is yours, nothing else is in scope. Write the scope statement down.",
    "2. **Inject.** Against your lab login form, attempt classic SQL injection. Observe what the database returns. Then fix it with parameterized queries and re-test: the same input is now inert data.",
    "3. **Break access control.** In the lab, change an object identifier in a request (invoice/1024 → invoice/1025) and observe the missing ownership check. Then implement the server-side authorization check and verify the bypass fails.",
    "4. **Steal the session.** In the lab, capture a session cookie and replay it from a second browser profile. Then apply the defenses: HttpOnly/Secure/SameSite flags, rotation on login, and short absolute lifetimes. Re-test each.",
    "5. **Map the M365 surface.** For Harborview's Microsoft 365: list the consent-grant workflow, audit which third-party apps hold OAuth permissions, check for legacy authentication, and write the policy: admin consent required, least-privilege scopes, periodic re-certification.",
    "6. **Write the code rules.** Produce the developer checklist: parameterized queries always, authorization checks on every object access, tokens never in URLs, secrets in the vault not the code. Four rules, each with the 'why' in one line.",
    "7. **Monitor what code misses.** For each attack class, write the detection: WAF or code-level logging for injection attempts, anomaly alerts for IDOR probing, impossible-travel and token-reuse alerts for session abuse. Defense is code plus monitoring.",
],
'project': (
    "**Harborview Freight — web application defense review.** Deliverable: the review of Harborview's dispatch web portal — the "
    "attack walkthroughs reproduced against a lab clone (never production), the code fixes (parameterization, authorization checks, "
    "session handling), the Microsoft 365 hardening checklist (consent workflow, legacy auth, token policies), and the monitoring rules. "
    "The development lead implements from this document."
),
'checkin': [
    "Explain SQL injection's mechanism and the fix — then tell Noah why input validation alone is insufficient.",
    "Walk Noah through an IDOR: the request, the missing check, and the server-side fix.",
    "What is consent phishing, and which Microsoft 365 policy stops it?",
],
'cards': [
    {"front": "What is SQL injection?",
     "back": "Untrusted input executed as database commands — an OWASP Top 10 web attack, fixed by parameterized queries and least-privilege database accounts."},
    {"front": "What is broken access control?",
     "back": "Missing or flawed authorization checks that let users act on data or functions they shouldn't reach — e.g., IDOR, missing function-level checks."},
    {"front": "How are sessions and tokens abused?",
     "back": "Stolen session cookies or tokens let attackers ride an authenticated session — countered by secure flags, rotation, short lifetimes, and least-privilege token scopes."},
    {"front": "What is consent phishing (illicit consent grant)?",
     "back": "Tricking a user into granting a malicious OAuth app permissions to their mailbox or files — the Microsoft 365-native phishing variant, stopped by admin-consent workflows and least-privilege scopes."},
    {"front": "Why is input validation alone insufficient against SQL injection?",
     "back": "Validation is a denylist that attackers bypass with encoding tricks; parameterized queries make input structurally incapable of becoming code — the fix is architectural, not filter-based."},
    {"front": "What are the recurring weaknesses in the Microsoft 365 attack surface?",
     "back": "Legacy authentication protocols, overly-permissive third-party app consent grants, and OAuth token theft — addressed by modern auth, admin consent, and token hygiene."},
],
'quiz': [
    {"q": "A Harborview dispatch portal builds SQL with string concatenation of the tracking-number field. What is the correct fix?",
     "choices": ["Block special characters with a denylist", "Rewrite with parameterized queries so input is always data, never code — plus a least-privilege database account", "Hide the login form", "Rename the database tables"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: parameterization is the architectural fix; denylists are bypassable."},
    {"q": "A user changes invoice/1024 to invoice/1025 in a URL and sees another customer's invoice. This is:",
     "choices": ["SQL injection", "An insecure direct object reference — broken access control: the server never verified ownership", "Session hijacking", "A TLS failure"],
     "answer": 1,
     "explain": "Covered in Concepts: IDOR is the textbook broken-access-control pattern — missing server-side authorization check."},
    {"q": "Which combination best defends against session hijacking?",
     "choices": ["Longer session lifetimes for convenience", "Secure cookie flags (HttpOnly, Secure, SameSite), rotation on privilege change, and short absolute lifetimes", "Storing sessions in the URL for visibility", "Disabling logout buttons"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: layered session defenses shrink the theft-and-reuse window."},
    {"q": "Which module covers the \"Microsoft 365 attack surface\"?",
     "choices": ["Web & Application Attacks", "Social Engineering & Phishing", "Hybrid Identity", "AD Structure and Trust"],
     "answer": 0,
     "explain": "Covered in Concepts: consent phishing, legacy auth, and token theft in M365 are core topics of the web-attacks module."},
],
},

'il11-red-blue-operations--zt-blue-detect': {
'title': 'Detection & Response',
'summary': (
    "Welcome to Module 16. I'm your instructor. Red team shows you how attacks work; blue team is the job: detection and "
    "response. You'll learn which EDR telemetry actually matters in triage, the discipline of rapid containment, the "
    "playbooks that turn chaos into procedure, and the post-incident learning loops that convert each incident into a "
    "control. Speed matters, but discipline matters more — a fast wrong containment is worse than a measured right one."
),
'objectives': [
    "Name the EDR telemetry that matters in triage and what each signal reveals",
    "Apply triage discipline: severity assessment, scoping, and escalation criteria",
    "Execute a containment playbook: isolate, preserve evidence, eradicate, recover",
    "Run a post-incident learning loop that produces a new or improved control",
],
'concepts': [
    "- **EDR telemetry** — Endpoint detection and response data: process trees, network connections, file/registry writes, script executions — the signals that reconstruct what actually happened.",
    "- **Process tree** — The parent-child lineage of processes: the single most revealing triage artifact — malware's ancestry is written here (e.g., winword.exe spawning powershell.exe).",
    "- **Triage discipline** — Severity assessment, scoping ('one host or ten?'), and escalation criteria applied the same way every time — the difference between response and panic.",
    "- **Rapid triage** — The module's operating standard: minutes, not days, from alert to scoped severity decision. Speed comes from practiced procedure, not heroics.",
    "- **Containment** — Isolating the affected host from the network (while preserving its state for forensics): stop the bleeding before the surgery.",
    "- **Containment playbook** — The pre-written procedure: who declares, who isolates, who preserves evidence, who communicates — decided before the incident, not during it.",
    "- **Eradication and recovery** — Removing the attacker's foothold and restoring clean operations: reimaging from known-good media, credential resets, control gaps closed.",
    "- **Post-incident learning loop** — The blameless review that converts the incident into a control: what was detected, what was missed, which detection or policy changes ship as a result.",
    "- **Mean time to detect/respond (MTTD/MTTR)** — The metrics that measure the program: how fast you see it, how fast you stop it.",
],
'procedure_intro': (
    "Respond on paper before you ever respond for real. You'll triage a simulated alert, run the containment playbook, "
    "and close the learning loop — building the muscle memory incidents demand."
),
'procedure_steps': [
    "1. **Take the alert.** Simulated: EDR flags winword.exe spawning powershell.exe on a dispatch workstation, which then reached an external IP. Write your first three actions and the clock time each must complete by.",
    "2. **Read the process tree.** Sketch the ancestry: winword → powershell → network connection. Annotate what each hop tells you: the lure (document), the execution (script), the objective (egress). This is triage's core skill.",
    "3. **Scope it.** Answer before containing: one host or ten? Which shares did the host touch? Which credentials were on it? Write the scoping checklist — containment without scoping either misses hosts or nukes the business.",
    "4. **Contain.** Execute the playbook: isolate the host from the network, preserve memory/disk state for forensics, revoke the user's sessions, and force credential resets for accounts on the host. In that order — write why the order matters.",
    "5. **Eradicate and recover.** Reimage from known-good media (never 'clean' a compromised host in place), restore data from verified backups, and close the entry vector — the malicious document's delivery path gets a control, not just a deletion.",
    "6. **Communicate.** Draft the three messages: internal (IT + leadership: what happened, what's contained, what's next), users (what to watch for), and the record (timeline for the file). Calm, factual, no speculation.",
    "7. **Close the loop.** Run the blameless review: what detected it, what was missed, and the shipped improvements — a new detection rule, a ringfence policy for Office spawning PowerShell (Module 12!), an email control. The incident must leave the environment stronger.",
],
'project': (
    "**Harborview Freight — incident response playbook.** Deliverable: the executable IR playbook — triage procedure with severity levels and "
    "escalation criteria, the containment runbook (isolate, preserve, revoke, reset), communication templates, and the post-incident review "
    "format that mandates a shipped control improvement. Include the worked example from the Hands-on procedure as the reference incident. "
    "The on-call engineer follows this at 3 AM — write it for 3 AM."
),
'checkin': [
    "An EDR alert fires: winword.exe → powershell.exe → external IP. Walk Noah through your first three actions and the scoping questions.",
    "Why contain before eradicating — and why reimage rather than 'clean' the host?",
    "What must the post-incident review produce, and why is 'blameless' a requirement rather than a nicety?",
],
'cards': [
    {"front": "Which EDR telemetry matters most in triage?",
     "back": "Process trees, network connections, and file/registry writes — the signals that reconstruct what actually happened on the host."},
    {"front": "What does the blue-team module demand of triage?",
     "back": "Discipline and speed: severity assessment, scoping, and escalation criteria applied the same way every time — minutes from alert to scoped decision."},
    {"front": "Why is the process tree the most revealing triage artifact?",
     "back": "It shows malware's ancestry: winword.exe spawning powershell.exe tells you the lure, the execution, and the technique in one view."},
    {"front": "What is the correct containment order, and why?",
     "back": "Isolate the host, preserve forensic state, revoke sessions, reset credentials — stop the bleeding first, preserve evidence second, kill the attacker's access third."},
    {"front": "Why reimage a compromised host instead of 'cleaning' it?",
     "back": "You can never prove a compromised host is clean — persistence mechanisms hide. Known-good media is the only trustworthy foundation."},
    {"front": "What must a post-incident learning loop produce?",
     "back": "A shipped control improvement — a new detection, a policy change, a closed gap — plus the timeline record. The incident must leave the environment stronger."},
],
'quiz': [
    {"q": "EDR alerts: winword.exe spawned powershell.exe, which connected to an unknown external IP. What is your first move?",
     "choices": ["Delete the Word document", "Scope and contain: verify the process tree, determine blast radius, isolate the host per the playbook", "Reboot the workstation and monitor", "Email the user asking what they clicked"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: triage discipline — read the tree, scope, then contain in playbook order. Deleting evidence or rebooting destroys forensics."},
    {"q": "Why must scoping precede containment?",
     "choices": ["It saves electricity", "Containment without scoping either misses additional compromised hosts or needlessly disrupts clean ones", "Scoping is required by insurance", "Containment tools require a scope file"],
     "answer": 1,
     "explain": "Covered in Concepts: 'one host or ten?' determines the response — blind containment is either incomplete or destructive."},
    {"q": "After containment, the team wants to 'clean' the host with antivirus and return it to service. What is the correct call?",
     "choices": ["Agree — antivirus cleaning is sufficient", "Reimage from known-good media: a compromised host can never be proven clean", "Leave the host offline permanently", "Reinstall only the browser"],
     "answer": 1,
     "explain": "Covered in Concepts: persistence mechanisms hide from cleaning — known-good media is the only trustworthy recovery."},
    {"q": "Which module covers \"Post-incident learning loops\"?",
     "choices": ["Social Engineering & Phishing", "Detection & Response", "Scenario Capstone", "Web & Application Attacks"],
     "answer": 1,
     "explain": "Covered in Concepts: the blameless review that converts incidents into shipped controls is the blue-team module's closing discipline."},
],
},

# =====================================================================
# PATH 6 — il11-cyber-hero-prep
# =====================================================================

'il11-cyber-hero-prep--zt-hero-review': {
'title': 'Full-Spectrum Review',
'summary': (
    "Welcome to Module 17. I'm your instructor, and this is the synthesis checkpoint: full-spectrum review across "
    "everything you've built. Zero Trust tenets drill, AD defense drill, allowlisting policy drill, red/blue scenario "
    "drill — spaced repetition with scenario prompts in the hands-on style of the bootcamp this academy accompanies. "
    "You won't learn new controls here. You'll prove the old ones stuck — and find the gaps while there's still time "
    "to close them."
),
'objectives': [
    "Recite the Zero Trust doctrine, tenets, and CISA pillars from memory under time pressure",
    "Walk AD attack-to-defense mappings for all four technique families without notes",
    "Design allowlist and ringfence rules for a novel application on first principles",
    "Triage a red/blue scenario end to end: detect, scope, contain, improve",
],
'concepts': [
    "- **Spaced repetition** — Reviewing material at increasing intervals: the evidence-backed method this module uses — retrieval, not re-reading, is what builds durable memory.",
    "- **Zero Trust tenets drill** — Rapid-fire recall: doctrine, seven tenets, PE/PA/PEP, CDM — the Module 2 material, now at reflex speed.",
    "- **AD defense drill** — Attack-to-control mapping from memory: Kerberoasting, AS-REP roasting, pass-the-*, DCSync, DCShadow — each paired with its killer control.",
    "- **Allowlisting policy drill** — Rule-type selection (publisher/hash/path), learning-mode design, and approval workflows applied to unfamiliar applications.",
    "- **Red/blue scenario drill** — End-to-end: a lure arrives, a host is compromised, you detect, scope, contain, and ship the improvement — the whole academy in one exercise.",
    "- **Retrieval practice** — Answering from memory before checking: the mechanism that makes review work. Peeking first converts the drill into reading.",
    "- **Gap log** — The running list of what you couldn't retrieve: the most valuable document you own right now — it is your study plan for the capstone.",
],
'procedure_intro': (
    "Test yourself like the exam will test you: closed notes first, then open notes to close the gaps. "
    "Keep the gap log ruthlessly honest."
),
'procedure_steps': [
    "1. **Tenets, timed.** Set a five-minute timer: write the doctrine, all seven tenets, and PE/PA/PEP roles from memory. Grade against Module 2. Log every gap.",
    "2. **Pillars and steps.** From memory: the five CISA pillars and the Traditional/Advanced/Optimal distinction. Then place Harborview's identity pillar from your Module 3 worksheet — does your memory match your earlier work?",
    "3. **AD lightning round.** For each of the four attack families, write the abused mechanism, the log signal, and the killing control — no notes. Time yourself; hesitation is a gap.",
    "4. **Novel app drill.** Invent an application Harborview just bought (you choose the type). Write its allowlist rule, its ringfence boundaries, and its share-access grants from first principles. Check against Modules 11–13.",
    "5. **Scenario sprint.** Take the Module 16 reference incident and re-run it: triage actions, scoping questions, containment order, the shipped improvement. Faster this time, same discipline.",
    "6. **Teach the hardest one.** Pick your weakest topic from the gap log and explain it aloud as if to a junior — the Feynman check. If you stumble, that's tomorrow's first hour.",
    "7. **Prioritize the capstone.** Convert the gap log into a ranked punch list for Module 18: which gaps threaten the rollout design, which threaten the breach response, which threaten the interview. Attack in that order.",
],
'project': (
    "**Personal readiness dossier.** Deliverable: your gap log with the ranked punch list, plus one page per path (six paths) summarizing "
    "the three facts you'd stake your interview on. This dossier is the input to the capstone — and the honest measure of where you stand. "
    "No one grades it but you, which is exactly why it has to be honest."
),
'checkin': [
    "Noah picks any tenet, any AD attack, any rule type — defend your answer from memory, then show the gap log entry if you missed.",
    "Walk Noah through the novel-app drill: allowlist rule, ringfence, share grants — and the principle behind each choice.",
    "What are your top three capstone risks from the gap log, and what's the plan for each?",
],
'cards': [
    {"front": "Why does this module use retrieval practice instead of re-reading?",
     "back": "Retrieval — answering from memory before checking — builds durable memory; re-reading feels productive but doesn't. Peeking first converts the drill into reading."},
    {"front": "What goes in the gap log, and why is it your study plan?",
     "back": "Everything you couldn't retrieve under drill conditions: it's the honest inventory of weak points, ranked into the punch list for the capstone."},
    {"front": "AD lightning round: Kerberoasting — mechanism, signal, killer control?",
     "back": "Mechanism: requesting TGS tickets and cracking them offline. Signal: burst of TGS requests. Killer: strong managed service-account passwords (plus AES Kerberos)."},
    {"front": "AD lightning round: pass-the-hash — mechanism, signal, killer control?",
     "back": "Mechanism: stolen NTLM hash reused directly. Signal: anomalous logon types. Killers: Credential Guard plus tiered administration."},
    {"front": "AD lightning round: DCSync vs. DCShadow — the one-line distinction?",
     "back": "DCSync pulls secrets by mimicking DC replication; DCShadow pushes poison by registering a rogue DC. Both die to replication-right restriction and monitoring."},
    {"front": "What are the four drills in the full-spectrum review?",
     "back": "Zero Trust tenets drill, AD defense drill, allowlisting policy drill, red/blue scenario drill — the whole academy at reflex speed."},
],
'quiz': [
    {"q": "During the tenets drill you blank on two of the seven tenets. What is the correct response per this module's method?",
     "choices": ["Skip them; five is enough", "Log them in the gap log, re-study the source material, and re-drill until retrieval is clean", "Guess and move on", "Re-read the whole module passively"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: the gap log plus retrieval re-drills is the method — passive re-reading doesn't build memory."},
    {"q": "Why must drills be done closed-notes first?",
     "choices": ["To save paper", "Retrieval practice only works if you attempt recall before checking — peeking converts the drill into reading", "Open notes are prohibited by policy", "Closed notes are faster"],
     "answer": 1,
     "explain": "Covered in Concepts: the memory benefit comes from the retrieval attempt itself."},
    {"q": "Your gap log shows allowlisting rule-type selection as the weakest area. What does the module prescribe?",
     "choices": ["Ignore it; the capstone won't need it", "Rank it in the punch list and drill novel-app rule selection (Module 11) first — it threatens the rollout design", "Memorize the definitions word for word", "Ask someone else to do that part"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: gaps are ranked by capstone risk and attacked in that order — rule selection threatens the rollout design directly."},
    {"q": "Which module covers the \"Red/blue scenario drill\"?",
     "choices": ["Detection & Response", "Full-Spectrum Review", "Scenario Capstone", "Social Engineering & Phishing"],
     "answer": 1,
     "explain": "Covered in Concepts: the end-to-end scenario drill is one of the four full-spectrum review drills."},
],
},

'il11-cyber-hero-prep--zt-hero-scenarios': {
'title': 'Scenario Capstone',
'summary': (
    "Welcome to Module 18, the capstone. I'm your instructor, and everything you've built converges here: you will design "
    "a Zero Trust rollout, respond to a simulated breach, write the executive justification, and forge interview-ready "
    "articulation of it all. These are portfolio artifacts — the written deployment plan and the mock incident response "
    "that prove you can do the work, not just describe it. This is the module future-you will thank you for."
),
'objectives': [
    "Design a phased Zero Trust rollout for a mid-size organization with sequencing rationale",
    "Respond to a simulated breach in writing: triage, containment, communication, improvement",
    "Write an executive justification that survives a skeptical CFO",
    "Articulate any academy topic in interview-ready form: precise, jargon-free, confident",
],
'concepts': [
    "- **Rollout phasing** — Identity first (MFA, phishing-resistant auth), then visibility (logging you can query), then endpoints (allowlisting, ringfencing), then data policy: each phase unlocks the next.",
    "- **Sequencing rationale** — The 'why this order' argument: identity before fine-grained policy because every later decision consumes identity signals; visibility before automation because you can't automate what you can't see.",
    "- **Simulated breach response** — The written artifact: timeline, triage decisions, scoping, containment actions, communications, and the shipped improvement — graded on discipline, not heroics.",
    "- **Executive justification** — Risk in business terms: what the program costs, what a breach costs, what each phase buys, and the residual risk honestly stated.",
    "- **Residual risk** — What remains after the controls: honest security writing names it. 'Zero Trust reduces X; it does not eliminate Y.'",
    "- **Interview-ready articulation** — The ability to explain any topic in two minutes, precisely, without jargon or hand-waving: the skill the bootcamp's hiring promise actually tests.",
    "- **Portfolio artifact** — A written work product that demonstrates capability to an employer: the rollout plan and the breach response are yours to show.",
],
'procedure_intro': (
    "Produce like a professional, not a student. These artifacts carry your name — write them to the standard "
    "you'd want a hiring manager to see."
),
'procedure_steps': [
    "1. **Frame the rollout.** Write Harborview's Zero Trust program charter in one page: objective, scope (250 endpoints, HQ + two warehouses, hybrid SaaS), constraints (operations can't stop), and success criteria.",
    "2. **Phase it.** Design four phases — identity, visibility, endpoints, data — with the controls from Modules 4 and 10–13 placed in phases. For each phase: entry criteria, exit criteria, and the dependency it unlocks.",
    "3. **Write the sequencing rationale.** For each phase boundary, write the 'why this order' paragraph. If a phase could move earlier without breaking dependencies, your phasing is wrong — fix it.",
    "4. **Respond to the breach.** Simulated: ransomware detonates on a warehouse workstation at 2 PM Friday. Write the full response: triage, scoping, containment order, communications (internal, users, record), eradication, recovery, and the post-incident improvement. Use your Module 16 playbook.",
    "5. **Justify to the executive.** Write the one-page business case: program cost, breach cost avoided (use honest ranges, not invented precision), what each phase buys, and residual risk stated plainly. The CFO asks 'why not just buy X?' — answer her.",
    "6. **Rehearse the interview.** Pick five academy topics and record yourself explaining each in two minutes. Listen back: cut every jargon sentence, tighten every vague claim. Repeat until it's crisp.",
    "7. **Assemble the portfolio.** Bind the charter, phased plan, breach response, and business case into one dossier with a table of contents. This is the artifact set — treat it like the product it is.",
],
'project': (
    "**Harborview Freight — Zero Trust program dossier.** Deliverable: the complete portfolio — program charter, phased rollout plan with "
    "sequencing rationale, written simulated-breach response, and executive business case with honest residual risk. Four documents, one dossier, "
    "table of contents, your name on the cover. This is what 'interview-ready' looks like in writing."
),
'checkin': [
    "Defend your phase order to Noah: why does identity come first, and what breaks if endpoints go first?",
    "Walk Noah through the Friday 2 PM ransomware response: first three actions, scoping, containment order.",
    "Explain any academy topic Noah names in two minutes, jargon-free. Then state the residual risk honestly.",
],
'cards': [
    {"front": "What is the standard Zero Trust rollout phase order, and why?",
     "back": "Identity, visibility, endpoints, data: identity signals feed every later decision; visibility must precede automation; endpoints before data policy because the enforcement point must exist first."},
    {"front": "What makes a sequencing rationale valid?",
     "back": "Each phase's exit criteria unlock the next phase's entry criteria — dependencies, not preferences, determine the order. If a phase can move earlier safely, the phasing is wrong."},
    {"front": "What must a written breach response contain?",
     "back": "Timeline, triage decisions, scoping, containment actions in order, communications, eradication and recovery, and the shipped post-incident improvement."},
    {"front": "What is residual risk, and why must the business case state it?",
     "back": "The risk that remains after controls: honest security writing names it ('reduces X; does not eliminate Y') — hiding it destroys credibility when the residual event occurs."},
    {"front": "What is interview-ready articulation?",
     "back": "Explaining any topic in two minutes: precise, jargon-free, confident — the skill the hiring promise actually tests."},
    {"front": "Why is the capstone dossier a portfolio artifact?",
     "back": "It's a written work product demonstrating capability to an employer — the rollout plan and breach response prove you can do the work, not just describe it."},
],
'quiz': [
    {"q": "Your rollout plan puts endpoint allowlisting in Phase 1, before identity hardening. What is wrong with this sequencing?",
     "choices": ["Nothing — endpoints are the priority", "Identity signals feed every later access decision; without hardened identity first, endpoint policies rest on compromised credentials", "Allowlisting requires no identity", "Phase numbers don't matter"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: sequencing follows dependencies — identity first because later decisions consume identity signals."},
    {"q": "The CFO asks: 'After this program, are we unhackable?' What is the correct answer?",
     "choices": ["Yes — Zero Trust eliminates all risk", "No: state the residual risk honestly — the program reduces specific risks dramatically but no program eliminates risk", "Only if we buy the premium tier", "That's a technical question for IT"],
     "answer": 1,
     "explain": "Covered in Concepts: honest security writing names residual risk — credibility depends on it."},
    {"q": "Which artifact proves interview-ready capability to an employer?",
     "choices": ["A certificate of completion", "The portfolio dossier: phased rollout plan, written breach response, and business case — work products demonstrating you can do the work", "A list of tools you've heard of", "A screenshot of the course"],
     "answer": 1,
     "explain": "Covered in Concepts: portfolio artifacts demonstrate capability; this academy confers preparation, not certification (see Honesty note)."},
    {"q": "Which module covers \"Write the executive justification\"?",
     "choices": ["Full-Spectrum Review", "Scenario Capstone", "CISA Zero Trust Maturity Model", "Default-Deny Architecture"],
     "answer": 1,
     "explain": "Covered in Concepts: the executive business case with honest residual risk is the capstone's justification artifact."},
],
},

# =====================================================================
# PATH 7 — il11-entra-identity
# =====================================================================

'il11-entra-identity--sc300-lifecycle': {
'title': 'Entra ID Identity Lifecycle',
'summary': (
    "Welcome to Module 19. I'm your instructor, and we now cross into the cloud identity plane: Microsoft Entra ID, the "
    "SC-300 track. Everything you learned about AD has a cloud counterpart — and the identity lifecycle is where security "
    "is won or lost before anyone logs in. Joiner-mover-leaver automation, provisioning, B2B collaboration, access "
    "packages: you'll build the lifecycle as a security boundary, where the audit trail writes itself because every "
    "grant and revocation flows through the process."
),
'objectives': [
    "Name the identity objects Entra ID governs: users, groups, devices, applications, resources",
    "Design joiner-mover-leaver automation: provision on join, adjust on move, revoke on leave",
    "Explain HR-driven vs. API-driven provisioning and when each fits",
    "Design B2B collaboration with access packages: scoped, approved, expiring guest access",
],
'concepts': [
    "- **Identity lifecycle** — Joiner → mover → leaver: the sequence of provisioning access when someone arrives, adjusting it when their role changes, and revoking it when they depart. Stale access is a breach waiting for a date.",
    "- **Joiner-mover-leaver (JML)** — The automation pattern: HR events drive access changes — day-one provisioning, role-change adjustment, same-day deprovisioning on departure.",
    "- **HR-driven provisioning** — Identity data flows from the HR system: hires, transfers, and terminations automatically create, update, or disable accounts — the source of truth is employment status.",
    "- **API-driven provisioning** — Identity data flows from any authoritative source via API (not only HR): contractors, vendors, and non-employee populations whose lifecycle lives outside HR.",
    "- **Access package** — A bundle of resources (groups, apps, SharePoint sites) with policy: who may request, who approves, and when access expires — B2B collaboration made governable.",
    "- **B2B collaboration** — Guest access for partner users: external identities invited into your directory with scoped, time-bounded access — never a full internal account for a visitor.",
    "- **Entitlement management** — The discipline of defining, granting, and reviewing who is entitled to what: access packages are its mechanism in Entra ID.",
    "- **The lifecycle as a security boundary** — Every join, move, and leave that flows through automation is an access decision made correctly by default; every one handled manually is a chance for stale privilege.",
    "- **Orphaned accounts** — Accounts that outlive their owner's need: the leaver step exists to kill them the day employment ends, not during the next audit.",
],
'procedure_intro': (
    "Automate the lifecycle on paper before you touch the portal. Every manual access decision in this module "
    "is a future incident — design the automation that removes it."
),
'procedure_steps': [
    "1. **Map Harborview's populations.** List employees (HQ, warehouses, drivers), contractors (seasonal warehouse staff), and partners (the freight broker). Each population needs a lifecycle source — HR, a vendor list, or the partner agreement.",
    "2. **Design the joiner flow.** A dispatcher is hired Monday. Write the automation: HR record → account created → group memberships by role → access package assigned → manager notified. Day-one access, zero manual grants.",
    "3. **Design the mover flow.** The dispatcher becomes a warehouse lead. Write what changes automatically: old role's access revoked, new role's granted, and the time bound (same day, not 'whenever IT gets to it').",
    "4. " + "**Design the leaver flow.** A driver resigns Friday at 5 PM. Write the deprovisioning: account disabled, sessions revoked, access packages expired — that evening, automatically. State what happens to their data per policy.",
    "5. **Choose the provisioning source.** For each population from step 1, choose HR-driven or API-driven provisioning and justify: employees → HR; seasonal contractors → the staffing vendor's API feed; the broker's staff → B2B invitation with access packages.",
    "6. **Build the partner access package.** The freight broker needs the dispatch portal for 90 days. Define the package: resources, approver (the dispatch manager), expiry (90 days, renewable), and the audit trail. No standing broker accounts.",
    "7. **Write the leaver audit.** Quarterly, the automation's work is verified: sample ten departures, confirm same-day deprovisioning, and report the orphaned-account count (target: zero). The audit trail writes itself — your job is to read it.",
],
'project': (
    "**Harborview Freight — identity lifecycle design.** Deliverable: the lifecycle design document — population map with provisioning sources, "
    "the JML automation flows (joiner, mover, leaver) with timing SLAs, the partner access-package catalog, and the quarterly leaver-audit procedure. "
    "HR owns the source data, IT owns the automation — the RACI is part of the deliverable."
),
'checkin': [
    "A contractor's engagement ends Friday. Walk Noah through what happens to their access, hour by hour, under your design.",
    "When is API-driven provisioning the right choice over HR-driven? Give Noah two Harborview examples.",
    "Why is the lifecycle called a security boundary? Defend the phrase.",
],
'cards': [
    {"front": "What do access packages manage?",
     "back": "B2B guest lifecycle: bundles of resources with policy, approvals, and automatic expiry — scoped, governable partner access."},
    {"front": "What is joiner-mover-leaver automation?",
     "back": "Provisioning access when someone joins, adjusting on role moves, revoking on departure — driven by authoritative sources so stale access never accumulates."},
    {"front": "HR-driven vs. API-driven provisioning — when is each right?",
     "back": "HR-driven: employees, where employment status is the source of truth. API-driven: contractors, vendors, and non-employee populations whose lifecycle lives outside HR."},
    {"front": "What is an orphaned account, and which lifecycle step kills it?",
     "back": "An account outliving its owner's need — the leaver step kills it the day employment ends, automatically, not at the next audit."},
    {"front": "Why must partner access use B2B with access packages instead of full internal accounts?",
     "back": "Scoped, approved, expiring access: partners get exactly the resources they need for exactly the engagement — never a standing internal identity for a visitor."},
    {"front": "What does 'the lifecycle as a security boundary' mean in practice?",
     "back": "Every join/move/leave flowing through automation is an access decision made correctly by default; manual handling is where stale privilege is born."},
],
'quiz': [
    {"q": "A seasonal warehouse contractor's engagement ends Friday at 5 PM. Under proper lifecycle automation, what happens to their access?",
     "choices": ["It remains until the next quarterly audit", "It is automatically disabled and revoked that evening — the leaver flow fires on the engagement end date", "Their manager must remember to email IT", "It converts to a guest account permanently"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: the leaver flow deprovisions automatically on the authoritative end date — no manual memory required."},
    {"q": "Harborview onboards drivers through a staffing vendor whose system is authoritative for contractor status. Which provisioning is correct?",
     "choices": ["HR-driven — all provisioning must come from HR", "API-driven — the vendor's system is the authoritative source for this population", "Manual — contractors are too complex to automate", "None — contractors don't need accounts"],
     "answer": 1,
     "explain": "Covered in Concepts: API-driven provisioning fits populations whose lifecycle lives outside HR."},
    {"q": "A freight broker needs dispatch-portal access for a 90-day engagement. What is the correct design?",
     "choices": ["A full internal account with no expiry", "B2B invitation plus an access package: scoped resources, named approver, 90-day expiry with renewal", "Shared credentials for the broker team", "VPN credentials emailed to the broker"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: access packages make partner access scoped, approved, and expiring."},
    {"q": "Which module covers \"The lifecycle as a security boundary\"?",
     "choices": ["Identity Governance", "Entra ID Identity Lifecycle", "Hybrid Identity", "Hardening the Identity Plane"],
     "answer": 1,
     "explain": "Covered in Concepts: the lifecycle-as-boundary framing is the core thesis of the identity lifecycle module."},
],
},

'il11-entra-identity--sc300-zerotrust-ca': {
'title': 'Zero Trust and Conditional Access',
'summary': (
    "Welcome to Module 20. I'm your instructor. In Module 2 you learned the policy engine in theory — today you operate "
    "one: Conditional Access, the Zero Trust policy engine of the Microsoft identity plane. Signals in, decisions out: "
    "named locations, device compliance, user and sign-in risk. You'll build a policy set for a real organization, then "
    "attack it from a non-compliant device and watch it hold. And you'll learn what breaks when CA is misconfigured — "
    "because the most powerful policy engine in the world is a liability in careless hands."
),
'objectives': [
    "Explain Conditional Access as the cloud policy engine: signals, conditions, grant controls",
    "Design CA policies using named locations, device compliance, and risk signals",
    "Predict what breaks when CA policies are misconfigured: lockout, bypass, and silent failure modes",
    "Test a policy set against adversarial sign-in attempts and verify it holds",
],
'concepts': [
    "- **Conditional Access (CA)** — The Zero Trust policy engine for cloud identity: if-then policies evaluated at sign-in (and continuously) — if the signals match the conditions, apply the grant controls.",
    "- **Signals** — The inputs: user and group, device state, location, client app, sign-in risk, user risk. Signals in, decision out.",
    "- **Named locations** — Administrator-defined trusted network and IP definitions (office egress IPs, VPN ranges) that policies reference — 'require MFA everywhere except the trusted office' starts here.",
    "- **Device compliance** — The device pillar's verdict consumed by CA: compliant/managed vs. non-compliant — the signal that separates corporate laptops from random phones.",
    "- **Grant controls** — What the policy requires: require MFA, require compliant device, require hybrid-joined device, block access entirely.",
    "- **Sign-in risk / user risk** — Identity Protection's risk assessments: anonymous IPs, leaked credentials, unfamiliar locations feeding real-time decisions.",
    "- **Report-only mode** — Policies evaluated without enforcing: the mandatory dry-run — what *would* have happened, before you break Monday morning logins.",
    "- **Misconfiguration failure modes** — Overly broad exclusions (the 'break-glass that became a highway'), conflicting policies, and emergency-access accounts without CA coverage: each is a documented breach path.",
    "- **What-if tool** — The policy simulator: evaluate a sign-in against the policy set before it happens — the professional's pre-flight check.",
],
'procedure_intro': (
    "Build the policy set like you'll be on call for it. Every policy gets report-only first, adversarial testing second, "
    "enforcement last — no exceptions."
),
'procedure_steps': [
    "1. **Define the signals.** List Harborview's available signals: Entra groups (dispatchers, warehouse, finance, admins), named locations (HQ egress IP, warehouse IPs), device compliance states, and risk levels. No signal, no policy — inventory first.",
    "2. **Write the baseline policies.** Draft five: (a) require MFA for all users; (b) require compliant device for finance apps; (c) block legacy authentication; (d) block high sign-in risk; (e) require phishing-resistant MFA for admins. One paragraph each: who, what conditions, what grant control.",
    "3. **Protect the break-glass.** Design the two emergency-access accounts: excluded from CA, 32+ character passwords in the safe, monitored with alerts on any use. Write the rule: break-glass is for CA outages, not convenience.",
    "4. **Run report-only.** Before enforcement, run every policy in report-only mode for two weeks. Write the review procedure: which sign-ins would have been blocked, which are false positives, what gets tuned.",
    "5. **Attack your own policies.** Simulate: stolen dispatcher password from an unknown device in another country; a non-compliant phone hitting the finance app; an admin signing in from a Tor exit node. For each, trace which policy fires and what the user experiences.",
    "6. **Document the failure modes.** For each baseline policy, write what breaks if it's misconfigured: the MFA policy with an over-broad exclusion (bypass), conflicting grant controls (unpredictable behavior), no emergency access (self-inflicted lockout). This section is the on-call runbook.",
    "7. **Write the change control.** CA changes go through review: what-if evaluation, report-only soak, approval, enforcement, rollback plan. A policy engine without change control is a loaded weapon on the table.",
],
'project': (
    "**Harborview Freight — Conditional Access policy set.** Deliverable: the five baseline policies with signal definitions, named locations, "
    "and grant controls; the break-glass design; the report-only review procedure; the adversarial test results; and the change-control runbook. "
    "Include the misconfiguration failure-mode appendix. The identity admin implements from this document."
),
'checkin': [
    "Walk Noah through one sign-in: a dispatcher on a non-compliant phone from home. Which policies evaluate, in what order, and what's the outcome?",
    "What breaks when a CA policy excludes 'all trusted locations' too broadly? Trace the bypass.",
    "Why report-only before enforcement — what did your two-week soak catch?",
],
'cards': [
    {"front": "What breaks when Conditional Access is misconfigured?",
     "back": "The Zero Trust promise at the identity layer — overly broad exclusions become bypasses, conflicting policies behave unpredictably, and missing emergency access means self-inflicted lockout."},
    {"front": "What are named locations used for in Conditional Access?",
     "back": "Trusted network and IP definitions that policies reference — e.g., require MFA everywhere except the office egress IPs."},
    {"front": "Conditional Access policies combine __ to reach an access decision.",
     "back": "Signals (user, device, location, risk) evaluated against conditions, producing grant controls: require MFA, require compliant device, or block."},
    {"front": "Why is report-only mode mandatory before enforcing a CA policy?",
     "back": "It shows what would have been blocked without breaking logins — the dry run that catches false positives before Monday morning."},
    {"front": "What is the break-glass account design, and what is it for?",
     "back": "Emergency-access accounts excluded from CA, with long random passwords stored offline and alerting on any use — for CA outages, never convenience."},
    {"front": "How do sign-in risk and user risk feed Conditional Access?",
     "back": "Identity Protection assesses risk (anonymous IPs, leaked credentials, unfamiliar locations); CA policies consume those signals to step up or block access in real time."},
],
'quiz': [
    {"q": "Conditional Access policies combine __ to reach an access decision.",
     "choices": ["Signals in, policy decision out: user, device, location, and risk evaluated against conditions to apply grant controls", "Firewall rules and antivirus status", "Usernames and static passwords", "VPN tunnels and proxy settings"],
     "answer": 0,
     "explain": "Covered in Concepts: CA is the cloud policy engine — signals evaluated against conditions, grant controls applied."},
    {"q": "A new CA policy requires compliant devices for the finance app. What is the correct rollout?",
     "choices": ["Enforce immediately on Friday afternoon", "Report-only soak first: review what would break, tune, then enforce with a rollback plan", "Enforce for admins only, forever", "Skip testing; the policy is obviously correct"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: report-only before enforcement is mandatory — the dry run catches false positives."},
    {"q": "An attacker has a dispatcher's password but signs in from a non-compliant device in another country. Which policy elements combine to stop this?",
     "choices": ["Named locations only", "Device compliance requirement plus sign-in risk policy: the unknown device fails compliance and the foreign sign-in trips risk — access blocked or stepped up", "The password-expiry policy", "Email forwarding rules"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: layered signals — compliance and risk — is what makes the stolen password insufficient."},
    {"q": "Which module covers \"What breaks when CA is misconfigured\"?",
     "choices": ["Entra ID Identity Lifecycle", "Zero Trust and Conditional Access", "Hybrid Identity", "Authentication and Authorization"],
     "answer": 1,
     "explain": "Covered in Concepts: misconfiguration failure modes — bypasses, conflicts, lockouts — are the CA module's cautionary core."},
],
},

'il11-entra-identity--sc300-auth': {
'title': 'Authentication and Authorization',
'summary': (
    "Welcome to Module 21. I'm your instructor. Identity is the new perimeter — so today we master its two halves: "
    "authentication (proving who you are) and authorization (deciding what you may do). MFA methods and phishing-resistant "
    "auth, passwordless with FIDO2 and Windows Hello, the protocols underneath it all — OAuth2, OIDC, SAML — and app "
    "registrations. You'll register an app, configure OIDC, and trace the token flow yourself: protocols demystified by doing."
),
'objectives': [
    "Compare MFA methods and identify which resist phishing",
    "Explain passwordless options: FIDO2, Windows Hello for Business, Authenticator",
    "Distinguish OAuth2, OIDC, and SAML: what each protocol does",
    "Register an application, configure OIDC, and trace the token flow end to end",
],
'concepts': [
    "- **Authentication** — Proving identity: 'you are who you claim.' MFA and passwordless are authentication technologies.",
    "- **Authorization** — Deciding permitted actions after identity is proven: 'you may do what the policy allows.' OAuth2 scopes and app roles are authorization.",
    "- **MFA methods** — Something you know, have, or are — combined. Strength varies: SMS/voice (phishable), push (fatigue-able), number-matching (better), FIDO2/Windows Hello (phishing-resistant).",
    "- **Phishing-resistant MFA** — FIDO2 security keys, Windows Hello for Business, certificate-based auth: bound to the origin, so a fake login page can't relay them.",
    "- **Passwordless** — FIDO2 security keys, Windows Hello for Business, Microsoft Authenticator (phone sign-in): no password to phish, steal, or reuse — the password is removed, not just supplemented.",
    "- **OAuth2** — Delegated authorization: access tokens grant scoped API access without sharing passwords ('let this app read my calendar').",
    "- **OIDC (OpenID Connect)** — The identity layer on OAuth2: ID tokens assert *who* the user is — authentication built on the authorization framework.",
    "- **SAML** — The enterprise federation protocol: XML assertions carrying authentication and attribute statements between identity provider and service provider — the SSO workhorse.",
    "- **App registration** — Defining your application in Entra ID: its identity, redirect URIs, API permissions, and secrets/certificates — the trust anchor for the token flows.",
    "- **Enterprise app / service principal** — The local instance of an app in your tenant: where Conditional Access, consent, and assignments actually apply.",
    "- **Token flow** — The choreography: user authenticates → identity provider issues tokens (ID, access, refresh) → app validates and consumes them. Trace it once and protocols stop being magic.",
],
'procedure_intro': (
    "Learn protocols by doing. You'll register a real app, configure OIDC, and watch tokens move — "
    "the trace makes the abstractions permanent."
),
'procedure_steps': [
    "1. **Rank the MFA methods.** List SMS, voice, push, number-matching, FIDO2, Windows Hello. For each, write the attack that defeats it (SIM-swap, fatigue, relay, none practical). The ranking writes Harborview's MFA standard by itself.",
    "2. **Design the passwordless rollout.** Choose the method per population: FIDO2 keys for admins and finance, Windows Hello for office laptops, Authenticator for drivers' phones. Write the enrollment and recovery procedure — recovery is where passwordless rollouts die.",
    "3. **Register the lab app.** In a test Entra tenant, register an application: name it, set the redirect URI to your local lab, and note the application (client) ID. This is the trust anchor — everything references it.",
    "4. **Configure OIDC.** Add the platform config, request the standard scopes (openid, profile), and initiate a sign-in. Capture the authorization code, exchange it for tokens, and decode the ID token: read the claims — sub, iss, aud, exp — and state what each proves.",
    "5. **Trace the full flow.** Write the numbered choreography: user → app → identity provider → authorization code → token endpoint → ID/access tokens → app validates signature, audience, expiry → access granted. Ten steps, no gaps.",
    "6. **Contrast the protocols.** One paragraph each: when you'd choose OIDC (modern apps, JSON tokens), SAML (enterprise federation, existing SSO), and pure OAuth2 (API delegation without identity). Justify with the token/assertion each carries.",
    "7. **Write the app-governance rule.** Every Harborview app registration gets: an owner, least-privilege API permissions, certificate (not secret) credentials, and an expiry review. Unowned apps get disabled — write the quarterly review procedure.",
],
'project': (
    "**Harborview Freight — authentication standard + lab trace.** Deliverable: two parts. (1) The authentication standard: MFA method per population, "
    "the passwordless rollout with enrollment and recovery, and the app-registration governance rule. (2) The lab document: your registered app's "
    "configuration and the annotated ten-step OIDC token trace with decoded claims. The identity admin and the dev lead each own half."
),
'checkin': [
    "Rank the MFA methods for Noah and name the attack that defeats each — then defend the passwordless choices per population.",
    "Walk Noah through your OIDC trace: what does the 'aud' claim prove, and what happens if validation is skipped?",
    "When would you choose SAML over OIDC? Give Noah the one-paragraph justification.",
],
'cards': [
    {"front": "Name phishing-resistant authentication methods.",
     "back": "FIDO2 security keys, Windows Hello for Business, Authenticator with number matching — bound to the origin so phishing pages can't relay them."},
    {"front": "Name the passwordless options in Entra ID.",
     "back": "FIDO2 security keys, Windows Hello for Business, and the Microsoft Authenticator (phone sign-in) — the password is removed, not just supplemented."},
    {"front": "OAuth2 vs OIDC vs SAML, one line each?",
     "back": "OAuth2: delegated authorization via access tokens. OIDC: identity layer on OAuth2 via ID tokens. SAML: enterprise federation via XML assertions."},
    {"front": "Which MFA methods resist phishing?",
     "back": "FIDO2, Windows Hello, and number-matching Authenticator — not SMS or voice codes, which can be phished, SIM-swapped, or intercepted."},
    {"front": "What is an app registration, and what is its service principal?",
     "back": "The app's identity definition in Entra ID (ID, redirect URIs, permissions, credentials); the service principal is the tenant-local instance where CA, consent, and assignments apply."},
    {"front": "What does the 'aud' (audience) claim prove in an ID token?",
     "back": "That the token was issued for your application specifically — accepting tokens meant for someone else is a classic validation failure."},
],
'quiz': [
    {"q": "An admin's credentials are phished, including their SMS MFA code via SIM-swap. Which MFA method would have resisted this?",
     "choices": ["SMS codes", "Voice call codes", "FIDO2 security key — phishing-resistant, bound to the origin", "Longer passwords"],
     "answer": 2,
     "explain": "Covered in Concepts: only phishing-resistant methods (FIDO2, Windows Hello) resist relay and SIM-swap; SMS and voice do not."},
    {"q": "Your lab app receives an ID token. Before trusting it, what must you validate?",
     "choices": ["Nothing — tokens are always trustworthy", "Signature, issuer, audience (that it's for your app), and expiry", "Only the user's display name", "The token's length"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: the trace includes validation of signature, iss, aud, and exp — skipping validation is the classic failure."},
    {"q": "Harborview needs SSO with a legacy enterprise vendor that only speaks XML assertions. Which protocol fits?",
     "choices": ["OIDC", "SAML — the enterprise federation protocol built on XML assertions", "Pure OAuth2", "LDAP bind"],
     "answer": 1,
     "explain": "Covered in Concepts: SAML is the SSO workhorse for enterprise federation with XML assertions."},
    {"q": "Which module covers \"App registrations and enterprise apps\"?",
     "choices": ["Entra ID Identity Lifecycle", "Authentication and Authorization", "Hybrid Identity", "Zero Trust and Conditional Access"],
     "answer": 1,
     "explain": "Covered in Concepts: app registration, service principals, and the OIDC trace are the auth module's applied core."},
],
},

'il11-entra-identity--sc300-hybrid': {
'title': 'Hybrid Identity',
'summary': (
    "Welcome to Module 22. I'm your instructor. Most enterprises don't get to start in the cloud — they bridge to it. "
    "Today: hybrid identity, the span between the on-prem AD you hardened in Modules 8–10 and the Entra ID you've built "
    "since Module 19. Entra Connect Sync versus Cloud Sync, the three authentication options, seamless SSO, and writeback. "
    "You'll extend Harborview's on-prem AD to Entra in the lab — and learn where the bridge itself becomes the attack surface."
),
'objectives': [
    "Contrast Entra Connect Sync and Cloud Sync and choose between them",
    "Compare the three hybrid authentication options: password hash sync, pass-through, federation",
    "Explain seamless SSO and writeback: what each does and what each requires",
    "Identify the hybrid bridge's attack surface and its defenses",
],
'concepts': [
    "- **Hybrid identity** — One identity spanning on-prem AD and Entra ID: users sign in once, access both worlds — the bridge most enterprises actually live on.",
    "- **Entra Connect Sync** — The full-featured synchronization engine: on-prem AD to Entra ID, with filtering, writeback options, and the most configuration surface — for complex directories.",
    "- **Cloud Sync (Entra Cloud Sync)** — The lightweight provisioning agent: simpler, multi-agent, high-availability-friendly — for straightforward sync without Connect's full feature set.",
    "- **Password hash sync (PHS)** — Synchronized password hashes enable cloud authentication: sign-in works even if the on-prem link is down; leaked-credential detection runs in the cloud.",
    "- **Pass-through authentication (PTA)** — Passwords validated against on-prem AD in real time via lightweight agents: no hash in the cloud, but on-prem must be reachable.",
    "- **Federation (AD FS)** — Authentication redirected to on-prem federation servers: maximum control, maximum infrastructure — and the federation servers become the crown jewels.",
    "- **Seamless SSO** — Domain-joined machines get silent sign-in to cloud resources: Kerberos does the work, users feel nothing — the experience goal of the bridge.",
    "- **Writeback** — Cloud changes flowing back on-prem: password writeback (S SPR resets land in AD), group writeback — the bridge is two-way by design.",
    "- **The bridge as attack surface** — Sync accounts with replication-level rights, federation servers holding the keys to cloud auth: the hybrid components inherit Tier 0 status — harden them like domain controllers.",
],
'procedure_intro': (
    "Bridge the two worlds you now know. You'll extend Harborview's AD to Entra, choose the auth option deliberately, "
    "and harden the bridge itself — because attackers cross bridges too."
),
'procedure_steps': [
    "1. **Inventory the on-prem side.** From your Module 8 design: Harborview's forest, domains, and OUs. Mark which OUs sync to the cloud and which stay on-prem only (service accounts, Tier 0 admin accounts — justify each exclusion).",
    "2. **Choose the sync engine.** Connect Sync vs. Cloud Sync for Harborview: single forest, moderate complexity → justify your pick in writing, including the high-availability story (staging mode server vs. multiple agents).",
    "3. " + "**Choose the auth option.** Password hash sync vs. pass-through vs. federation: weigh resilience (PHS survives a WAN outage), control (federation keeps auth on-prem), and infrastructure cost. Write the decision and its trade-offs — there is no free choice here.",
    "4. **Design seamless SSO.** For domain-joined HQ machines: the Kerberos decryption key, the intranet-zone configuration, the expected silent sign-in. Write the user-experience test: what 'working' looks like.",
    "5. **Scope writeback.** Enable password writeback (cloud SSPR must land in AD) and decide on group writeback. For each, write the security implication: a two-way bridge means cloud compromise can flow downhill — scope it deliberately.",
    "6. **Harden the bridge.** The sync server and its service account get Tier 0 treatment: hardened host, no interactive logons, monitored like a domain controller. Write the hardening checklist — the sync account's replication rights make it a target.",
    "7. **Plan the failure modes.** WAN link down (PHS vs. PTA behavior), sync server offline (staging-mode failover), federation server compromised (the nightmare scenario — write the containment). Each failure gets a runbook paragraph.",
],
'project': (
    "**Harborview Freight — hybrid identity design.** Deliverable: the bridge design — OU sync scope with exclusions justified, the sync-engine "
    "choice, the authentication-option decision with trade-offs, seamless SSO design, writeback scope, the Tier 0 hardening checklist for sync "
    "infrastructure, and the failure-mode runbook. The infrastructure lead builds from this document."
),
'checkin': [
    "Defend your auth-option choice to Noah: what did you trade away, and why was it worth it?",
    "Why does the sync server get Tier 0 treatment? Walk Noah through what its compromise yields.",
    "The WAN link drops at 2 AM. Under your design, who can still sign in to cloud apps — and why?",
],
'cards': [
    {"front": "Entra Connect Sync vs Cloud Sync?",
     "back": "Connect Sync: full-featured synchronization from on-prem AD to Entra ID, for complex directories. Cloud Sync: lightweight provisioning agents, simpler and HA-friendly, for straightforward sync."},
    {"front": "Name the three Entra hybrid authentication options.",
     "back": "Password hash sync, pass-through authentication, and federation."},
    {"front": "Password hash sync vs. pass-through — the resilience trade-off?",
     "back": "PHS: cloud authentication survives an on-prem/WAN outage (hashes are in the cloud). PTA: passwords validated on-prem in real time — no hash in the cloud, but on-prem must be reachable."},
    {"front": "What is seamless SSO, and what powers it?",
     "back": "Silent sign-in to cloud resources from domain-joined machines — Kerberos does the work; users feel nothing."},
    {"front": "What is writeback, and why must it be scoped deliberately?",
     "back": "Cloud changes flowing back on-prem (password and group writeback). A two-way bridge means cloud compromise can flow downhill — scope it on purpose."},
    {"front": "Why is the hybrid bridge itself an attack surface?",
     "back": "Sync accounts hold replication-level rights and federation servers hold the keys to cloud authentication — compromise there bypasses both worlds' defenses. Tier 0 treatment required."},
],
'quiz': [
    {"q": "Harborview's warehouses lose WAN connectivity regularly. Which hybrid auth option keeps cloud sign-in working during an outage?",
     "choices": ["Pass-through authentication", "Password hash sync — authentication happens in the cloud against synchronized hashes", "Federation with on-prem AD FS only", "Seamless SSO alone"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: PHS authenticates in the cloud, surviving on-prem/WAN outages; PTA and federation need on-prem reachability."},
    {"q": "Why must the Entra Connect server be hardened to Tier 0 standards?",
     "choices": ["It runs the email server", "Its sync account holds replication-level rights over the directory — compromise yields the keys to both identity worlds", "Tier 0 is the default for all servers", "It stores user passwords in plaintext"],
     "answer": 1,
     "explain": "Covered in Concepts: the bridge inherits Tier 0 status — sync-account compromise is forest-level compromise."},
    {"q": "A simple single-forest directory needs sync with minimal infrastructure. Which engine fits?",
     "choices": ["Entra Connect Sync with full customization", "Cloud Sync — lightweight agents, simpler, high-availability-friendly for straightforward scenarios", "Manual CSV import", "Federation only"],
     "answer": 1,
     "explain": "Covered in Concepts: Cloud Sync is the lightweight choice for straightforward directories; Connect Sync is for complex ones."},
    {"q": "Which module covers \"Seamless SSO and writeback\"?",
     "choices": ["Hybrid Identity", "Entra ID Identity Lifecycle", "Authentication and Authorization", "AD Structure and Trust"],
     "answer": 0,
     "explain": "Covered in Concepts: seamless SSO and writeback are hybrid-bridge topics."},
],
},

'il11-entra-identity--sc300-governance': {
'title': 'Identity Governance',
'summary': (
    "Welcome to Module 23. I'm your instructor. Access granted is a decision; access *reviewed* is a discipline. Today: "
    "identity governance — access reviews that actually revoke, entitlement management, Privileged Identity Management "
    "for just-in-time admin roles, terms of use, and identity protection. Governance is continuous hygiene: the unglamorous "
    "work that keeps every grant you've made from quietly becoming tomorrow's breach."
),
'objectives': [
    "Design access reviews that revoke: scope, reviewers, cadence, and the revocation SLA",
    "Explain entitlement management: catalogs, policies, and lifecycle of entitlements",
    "Activate a PIM role with justification, approval, and time bounds — and explain why standing admin must die",
    "Describe terms of use and identity protection as governance guardrails",
],
'concepts': [
    "- **Identity governance** — The continuous discipline of ensuring the right identities have the right access for the right reasons — and nothing more, for no longer than needed.",
    "- **Access review (recertification)** — Periodic owner attestation: 'does this person still need this access?' — with a revocation SLA so 'no' means removed, not noted.",
    "- **Entitlement management** — Defining access as a catalog (packages, roles, groups) with request policy, approval, and expiry — governance by design instead of by spreadsheet.",
    "- **Privileged Identity Management (PIM)** — Just-in-time privileged role activation: eligible, not active — admins activate with justification and approval, for a bounded window, with full audit.",
    "- **Standing admin vs. eligible admin** — Standing: always-on privilege, always a target. Eligible: privilege that doesn't exist until activated — the identity-plane equivalent of JIT elevation.",
    "- **Terms of use** — Policy acceptance gates: users acknowledge acceptable-use terms before access is granted — the compliance paper trail, enforced by the platform.",
    "- **Identity Protection** — Risk-based policies: sign-in risk and user risk driving automatic remediation (require password change, block) — governance that acts without waiting for a human.",
    "- **Governance as continuous hygiene** — Reviews, recertification, and PIM aren't projects with end dates; they're the brushing-and-flossing of identity security.",
    "- **Reviewer accountability** — The review is only as honest as the reviewer: owners attest their own teams' access, and rubber-stamping is itself a finding.",
],
'procedure_intro': (
    "Govern like an auditor with a revoke button. You'll run a review that actually removes access, activate a PIM role "
    "properly, and write the cadence that keeps it all honest."
),
'procedure_steps': [
    "1. **Scope the review.** Choose Harborview's highest-risk surface: finance app access and the dispatch admin group. Define the population, the reviewer (the data/group owner — not IT), and the cadence (quarterly for privileged, semi-annual for standard).",
    "2. **Run the review on paper.** List ten members of the dispatch admin group. For each, write: still needs it / adjust / revoke — with the evidence (role, last used, manager). Be brutal: 'probably still needs it' is a revoke.",
    "3. **Set the revocation SLA.** Denied or unreviewed access is removed within 5 business days — automatically where possible. Write the escalation: what happens when a reviewer doesn't respond (hint: the access is revoked, not extended).",
    "4. **Build the entitlement catalog.** Convert Harborview's ad-hoc grants into packages: 'Dispatcher,' 'Warehouse Lead,' 'Finance Viewer' — each with resources, approver, and default expiry. New grants come from the catalog; exceptions require written justification.",
    "5. **Activate a PIM role.** Walk the flow: the IT lead is *eligible* for Global Administrator, not active. They request activation with a ticket number as justification, the CISO approves, the role is active for 4 hours, and every action is logged. Write each step and the audit entry it produces.",
    "6. **Kill a standing admin.** Find Harborview's always-on Global Admin (there is one — there always is). Write the conversion plan: eligible via PIM, break-glass excluded and monitored, and the 30-day verification that nobody 'needed' the standing grant.",
    "7. **Write the governance calendar.** Annual: terms-of-use refresh. Quarterly: privileged access reviews. Semi-annual: standard reviews. Continuous: Identity Protection risk policies. One page, owners named, dates set.",
],
'project': (
    "**Harborview Freight — identity governance program.** Deliverable: the program document — review scopes with reviewer assignments and "
    "revocation SLAs, the entitlement catalog, the PIM design (eligible roles, activation workflow, approval chain), the standing-admin conversion "
    "plan, and the governance calendar. The compliance officer co-signs — write the accountability sections for her."
),
'checkin': [
    "Run Noah through a PIM activation: eligible to active, justification to audit trail — what makes it 'just-in-time'?",
    "A reviewer ignores the quarterly review. Under your SLA, what happens to the unreviewed access — and why is that the right default?",
    "Defend the catalog: why is 'request from the catalog' more governable than ad-hoc grants?",
],
'cards': [
    {"front": "What does Privileged Identity Management provide?",
     "back": "Just-in-time privileged role activation with approval and justification — eligible, not active: privilege that exists only for the bounded window, fully audited."},
    {"front": "What is an Entra access review?",
     "back": "Periodic recertification: owners confirm who still needs access, and unjustified access is revoked within the SLA — 'no' means removed, not noted."},
    {"front": "Standing admin vs. eligible admin — the difference that matters?",
     "back": "Standing privilege is always-on and always a target; eligible privilege doesn't exist until activated with justification and approval — the identity equivalent of JIT elevation."},
    {"front": "What is entitlement management?",
     "back": "Defining access as a governed catalog — packages and roles with request policy, approval, and expiry — instead of ad-hoc grants tracked in spreadsheets."},
    {"front": "What do terms of use enforce in the governance picture?",
     "back": "Policy-acceptance gates: users acknowledge acceptable-use terms before access is granted — the compliance paper trail, enforced by the platform itself."},
    {"front": "What does Identity Protection contribute to governance?",
     "back": "Risk-based automatic remediation: sign-in and user risk driving actions (require password change, block) without waiting for a human reviewer."},
],
'quiz': [
    {"q": "An IT lead needs Global Administrator rights for a 4-hour migration window. What is the correct design?",
     "choices": ["Grant permanent Global Admin — it's easier", "PIM: eligible assignment, activation with ticket-number justification and approval, 4-hour window, full audit — then it expires", "Share the break-glass credentials", "Grant it and set a calendar reminder to remove it"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: PIM makes privilege just-in-time — eligible, justified, approved, bounded, audited."},
    {"q": "A quarterly access review ends with three owners not responding. Under a proper revocation SLA, what happens?",
     "choices": ["Extend their access until they respond", "The unreviewed access is revoked — non-response defaults to removal, not extension", "Escalate to the CEO for a decision", "Skip those users this quarter"],
     "answer": 1,
     "explain": "Covered in Concepts: the SLA's teeth — unreviewed access is removed, because silence is not attestation."},
    {"q": "Why is an entitlement catalog more governable than ad-hoc access grants?",
     "choices": ["Catalogs are cheaper", "Every grant comes from a defined package with approver and expiry — requestable, reviewable, revocable by design", "Catalogs eliminate the need for reviewers", "Ad-hoc grants are illegal"],
     "answer": 1,
     "explain": "Covered in Concepts: governance by design — the catalog makes every grant's policy, approver, and lifetime explicit."},
    {"q": "Which module covers \"Privileged Identity Management (PIM)\"?",
     "choices": ["Entra ID Identity Lifecycle", "Authentication and Authorization", "Identity Governance", "Zero Trust and Conditional Access"],
     "answer": 2,
     "explain": "Covered in Concepts: PIM is the just-in-time privilege core of the governance module."},
],
},

'il11-entra-identity--sc300-troubleshoot': {
'title': 'Troubleshooting with PowerShell and KQL',
'summary': (
    "Welcome to Module 24. I'm your instructor. Everything breaks — the professional difference is *how you find out why*. "
    "Today: troubleshooting methodology for the identity plane. Reading Entra sign-in logs like a detective, wielding "
    "PowerShell and Microsoft Graph for identity operations, and querying sign-in data with KQL. You'll diagnose broken "
    "sign-ins from real log shapes — evidence, not guesses — and build the runbook you'll reach for at 2 AM."
),
'objectives': [
    "Read an Entra sign-in log entry: identify the failure, the policy involved, and the next step",
    "Use PowerShell/Microsoft Graph for identity operations: query users, groups, assignments, audit logs",
    "Write KQL queries against sign-in data: filter failures, correlate by user, app, and location",
    "Apply the troubleshooting methodology: reproduce, isolate, hypothesize, verify, document",
],
'concepts': [
    "- **Sign-in logs** — The per-attempt record: who, from where, on what device and client, which CA policies evaluated, and the result code. The first place every identity investigation starts.",
    "- **Result codes** — The log's verdict: success vs. specific failure (bad password, blocked by CA, MFA not completed, risky sign-in). Reading the code beats guessing the cause.",
    "- **Correlation ID** — The thread tying a user's attempt across log entries and systems: follow it and the scattered events become one story.",
    "- **PowerShell for identity** — Scripted administration: querying and managing users, groups, licenses, and PIM assignments — repeatable, auditable, faster than clicking at 2 AM.",
    "- **Microsoft Graph** — The API behind the portal: every identity operation the portal does, your scripts can do — the automation surface for the lifecycle and governance modules.",
    "- **KQL (Kusto Query Language)** — The query language for log analytics: filter, summarize, and correlate sign-in data at scale — `SigninLogs | where ResultType != 0` is the starting incantation.",
    "- **Troubleshooting methodology** — Reproduce the failure, isolate the layer (credential? policy? device? risk?), hypothesize from evidence, verify with a targeted test, document the fix.",
    "- **Audit logs vs. sign-in logs** — Sign-in logs: authentication attempts. Audit logs: *changes* — who granted what to whom, when. Different questions, different logs.",
],
'procedure_intro': (
    "Diagnose from evidence. Each drill hands you a broken sign-in and the logs — your job is the methodology, "
    "not the answer key."
),
'procedure_steps': [
    "1. **Learn the methodology.** Write it on an index card: reproduce → isolate the layer → hypothesize from evidence → verify with a targeted test → document. This card lives on your monitor.",
    "2. **Read a failure.** Drill: a dispatcher's sign-in fails with a CA-related result code. From the log entry, identify: which policy evaluated, which condition failed (non-compliant device), and the fix (enroll the device / adjust the policy scope). Write the three-line diagnosis.",
    "3. **Query with KQL.** Against the lab's sign-in data: list all failed sign-ins in the last 24 hours by user; then narrow to one user and correlate by IP and app. Write both queries and state what each answers.",
    "4. **Hunt the anomaly.** KQL drill: find sign-ins from an unusual location for a finance user, and check whether a CA risk policy fired. Write the query, the finding, and the verdict: benign travel or incident?",
    "5. **Script the check.** With PowerShell/Graph: pull the dispatch admin group's membership, list each member's PIM eligibility, and export the audit log's last 50 role assignments. Save the script — it's now your quarterly review tool.",
    "6. **Isolate the layer.** Drill: MFA push never arrives. Walk the methodology: is it the device (no signal), the policy (MFA required but method unavailable), or the service? Write the isolation questions in order — each eliminates a layer.",
    "7. **Write the 2 AM runbook.** One page: the five most common identity failures, the log query or command that diagnoses each, and the fix. Laminate it mentally — this is the document from the capstone's breach response.",
],
'project': (
    "**Harborview Freight — identity troubleshooting runbook.** Deliverable: the runbook — the methodology card, the five common failures with "
    "diagnostic queries/commands and fixes, the KQL query library (failures by user, anomaly hunts, CA evaluation traces), and the PowerShell/Graph "
    "script pack for membership and audit checks. The on-call engineer uses this before escalating."
),
'checkin': [
    "A sign-in fails with a CA result code. Walk Noah through the diagnosis: which log, which fields, what conclusion?",
    "Write the KQL for Noah: all failed sign-ins for one user in 24 hours, correlated by IP. Explain each clause.",
    "MFA push never arrives for a warehouse lead. Isolate the layer for Noah: device, policy, or service — in what order do you check?",
],
'cards': [
    {"front": "What is KQL used for in identity troubleshooting?",
     "back": "Querying Entra sign-in logs — e.g., filtering failed sign-ins by user, application, location, and correlating anomalies at scale."},
    {"front": "What do Entra sign-in logs tell a troubleshooter?",
     "back": "Who tried to sign in, from where, on what device, which CA policies evaluated, and the result code — the first stop of every identity investigation."},
    {"front": "In KQL, what does `SigninLogs | where ResultType != 0` return?",
     "back": "Failed sign-ins: ResultType 0 means success, so anything else is a failure worth investigating."},
    {"front": "What is the troubleshooting methodology, in order?",
     "back": "Reproduce the failure → isolate the layer → hypothesize from evidence → verify with a targeted test → document the fix."},
    {"front": "Sign-in logs vs. audit logs — which answers which question?",
     "back": "Sign-in logs: authentication attempts (who tried, what happened). Audit logs: changes (who granted what to whom, when)."},
    {"front": "Why script identity operations with PowerShell/Graph instead of using the portal?",
     "back": "Repeatable, auditable, and fast: the same check runs identically every time, produces evidence, and works at 2 AM without clicking through blades."},
],
'quiz': [
    {"q": "In KQL, `SigninLogs | where ResultType != 0` returns:",
     "choices": ["Successful sign-ins", "Failed sign-ins — ResultType 0 is success, anything else is a failure", "All sign-ins from mobile devices", "Password-reset events"],
     "answer": 1,
     "explain": "Covered in Concepts: the result-code semantics make this the starting incantation for failure hunts."},
    {"q": "A dispatcher's sign-in fails; the log shows a CA policy requiring a compliant device, and the device is non-compliant. What is the correct diagnosis and fix?",
     "choices": ["Reset the user's password", "The device-compliance condition failed: enroll/remediate the device, or adjust the policy scope deliberately — the log names the exact policy and condition", "Disable Conditional Access", "Delete and recreate the user"],
     "answer": 1,
     "explain": "Covered in Hands-on procedure: read the log's policy evaluation — the fix addresses the failed condition, not random resets."},
    {"q": "Per the methodology, what comes immediately after isolating the failing layer?",
     "choices": ["Document the fix", "Hypothesize from evidence, then verify with a targeted test", "Escalate to Microsoft support", "Reboot everything"],
     "answer": 1,
     "explain": "Covered in Concepts: reproduce → isolate → hypothesize from evidence → verify → document. Guessing before evidence is the failure mode."},
    {"q": "Which module covers \"KQL against Entra sign-in data\"?",
     "choices": ["Identity Governance", "Troubleshooting with PowerShell and KQL", "Hybrid Identity", "SC-300 Exam Prep"],
     "answer": 1,
     "explain": "Covered in Concepts: KQL failure-hunts and correlation are the troubleshooting module's query core."},
],
},

'il11-entra-identity--sc300-exam-prep': {
'title': 'SC-300 Exam Prep',
'summary': (
    "Welcome to Module 25, the final module. I'm your instructor. You've built the identity plane from lifecycle to "
    "governance to troubleshooting — now we convert that competence into exam readiness for the SC-300, Microsoft's "
    "Identity and Access Administrator Associate. Scenario-question drills keyed to the identity lifecycle, Conditional "
    "Access policy-reading drills, PowerShell versus portal fluency, and the logistics of booking and exam day. "
    "Readiness is demonstrated, not declared — you'll prove it here before you pay for the exam."
),
'objectives': [
    "Answer scenario questions by identifying the identity-lifecycle cue in the stem",
    "Read a Conditional Access policy and predict its effect on a given sign-in",
    "Choose between PowerShell/Graph and portal approaches for administrative tasks",
    "Plan booking and exam-day logistics without surprises",
],
'concepts': [
    "- **Scenario questions** — The SC-300's dominant format: a business situation with constraints — the correct answer is the option satisfying all constraints, usually revealed by the lifecycle or governance cue in the stem.",
    "- **The lifecycle cue** — Stems mentioning joiners, movers, leavers, or partners point at lifecycle/governance answers (access packages, PIM, access reviews) — train yourself to spot the cue word.",
    "- **Policy-reading** — Given a CA policy's users, conditions, and grant controls, predicting the outcome for a described sign-in: the exam's favorite applied skill.",
    "- **PowerShell vs. portal** — Knowing both paths: the exam tests *which* tool fits (bulk/repeatable → PowerShell/Graph; one-off with guidance → portal) and the portal tests *where* (which blade, which setting).",
    "- **Least-privilege answers** — When options differ only in scope, the exam rewards the least-privilege choice that still meets the stated requirement: read the requirement, not your habits.",
    "- **Booking logistics** — Scheduling through the vendor's certification portal, ID requirements, environment rules for online proctoring vs. test centers — handled weeks ahead, never the night before.",
    "- **Exam-day discipline** — Time budget per question, flag-and-return strategy, reading every option before choosing: the meta-skills that convert knowledge into score.",
    "- **Readiness bar** — Consistently scoring above your target on full timed practice sets covering all domains — one good section isn't readiness.",
],
'procedure_intro': (
    "Practice like it's the exam: timed, scenario-first, every option read. You'll drill the question types until "
    "the cue words trigger the right domain automatically."
),
'procedure_steps': [
    "1. **Learn the cue words.** Make flashcards: 'contractor ends Friday' → lifecycle/leaver; 'partner needs portal' → access packages; 'admin needs rights for a window' → PIM; 'who still needs access' → access review. Drill until the mapping is instant.",
    "2. **Drill scenario questions.** Take ten scenario stems from your module notes (lifecycle, CA, governance). For each: underline the constraints, name the cue, eliminate options that violate a constraint, then choose. Write the elimination reasoning — that's the skill.",
    "3. **Read policies cold.** Take your Module 20 policy set. For five adversarial sign-ins, predict the outcome purely from the written policy — no portal. Check with the what-if logic. Every miss is a policy-reading gap; log it.",
    "4. **Choose the tool.** Twenty admin tasks: for each, choose PowerShell/Graph or portal and justify in one line (bulk/repeatable/scripted → PowerShell; guided one-off → portal). The exam punishes 'always portal' and 'always script' equally.",
    "5. **Run a timed set.** Assemble 40 questions across all domains, 60 minutes, no notes. Score by domain. Any domain below your bar gets a targeted re-drill week — the readiness bar is per-domain, not overall.",
    "6. **Handle the logistics.** Walk the booking flow on the vendor's certification portal: account, exam selection, scheduling, ID requirements, proctoring environment rules. Write your personal checklist with dates — logistics failures are the silliest way to lose.",
    "7. **Do the exam-day rehearsal.** The night before: documents ready, environment checked, sleep protected. Exam day: time budget per question, flag-and-return, read every option. Write your one-page exam-day plan and follow it exactly.",
],
'project': (
    "**Personal SC-300 readiness file.** Deliverable: your readiness file — the cue-word flashcard set, the policy-reading drill results, "
    "the timed-set scores by domain with the re-drill plan for weak domains, and the booking + exam-day checklist with dates. When every domain "
    "clears your bar on timed sets, you're ready to book. Not before."
),
'checkin': [
    "Noah gives you a scenario stem: find the cue word, name the domain, and eliminate two options by constraint.",
    "Read Noah a CA policy cold: predict the outcome for a non-compliant device hitting the finance app.",
    "Show Noah your timed-set scores by domain — which domain gets the re-drill week, and why?",
],
'cards': [
    {"front": "What is the identity-lifecycle cue in SC-300 scenario questions?",
     "back": "Stems mentioning joiners, movers, leavers, or partners point at lifecycle/governance answers — access packages, PIM, access reviews. Spot the cue word, find the domain."},
    {"front": "How do you answer a Conditional Access policy-reading question?",
     "back": "Map the policy's users, conditions, and grant controls to the described sign-in, and predict the outcome — signals in, decision out, exactly like the real engine."},
    {"front": "PowerShell/Graph vs. portal — how do you choose on the exam?",
     "back": "Bulk, repeatable, or scripted tasks → PowerShell/Graph; guided one-off tasks → portal. The exam rewards matching the tool to the task, not a favorite."},
    {"front": "When options differ only in scope, which does the SC-300 reward?",
     "back": "The least-privilege option that still meets the stated requirement — read the requirement, not your habits."},
    {"front": "What is the readiness bar for booking the exam?",
     "back": "Consistently clearing your target on full timed practice sets, per domain — one good section isn't readiness."},
    {"front": "What is the flag-and-return strategy?",
     "back": "Answer what you know, flag the uncertain, return with remaining time — it converts knowledge into score instead of letting one hard question eat the clock."},
],
'quiz': [
    {"q": "Scenario: 'A partner organization needs access to the dispatch portal for 90 days. Access must expire automatically.' Which answer fits?",
     "choices": ["Create permanent guest accounts", "B2B invitation with an access package: scoped resources, approval, automatic expiry — the lifecycle cue points here", "Share an admin account", "Email the portal link publicly"],
     "answer": 1,
     "explain": "Covered in Concepts: the partner/90-day/expiry cue words point to access packages — the lifecycle domain."},
    {"q": "Scenario: 'An administrator needs elevated rights every Tuesday for maintenance.' Which design is correct?",
     "choices": ["Permanent elevated rights", "PIM eligible assignment with weekly activation, justification, and expiry — just-in-time privilege", "A shared admin password", "No rights; do maintenance without them"],
     "answer": 1,
     "explain": "Covered in Concepts: recurring bounded need → PIM activation, not standing privilege."},
    {"q": "A CA policy requires MFA for all users but excludes the finance app. A finance user signs in from an unmanaged device. What happens?",
     "choices": ["MFA is required", "No MFA is required for the finance app — the exclusion removes it from the policy's scope", "Access is blocked", "The user is prompted for a password change"],
     "answer": 1,
     "explain": "Covered in Concepts and Hands-on procedure: policy-reading — exclusions define scope; the finance app sits outside this policy."},
    {"q": "Which module covers \"Booking and exam-day logistics\"?",
     "choices": ["Troubleshooting with PowerShell and KQL", "Identity Governance", "SC-300 Exam Prep", "Hybrid Identity"],
     "answer": 2,
     "explain": "Covered in Concepts: booking flow, ID requirements, and exam-day discipline are the exam-prep module's logistics core."},
],
},
}
