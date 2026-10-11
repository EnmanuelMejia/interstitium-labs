#!/usr/bin/env python3
"""IL-27 fast-track remediation builder. Rebuilds FT01-FT06 to IL-26 grade.
Run from anywhere: python3 build_ft.py"""
import json, copy, datetime, sys

SRC = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-27-it-infrastructure-specialist-threatlocker-mastery.json'
OUT = '/home/hatch/workspace/apex-audit/docs/university/data/courses/_il27-remediation/il-27-remediated.json'
UTC = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

FT = {}  # moduleId -> dict of rebuilt arrays

def N(title, body):
    return {"title": title, "body": body}

def C(front, back):
    return {"front": front, "back": back}

def Q(q, choices, answer, explain, index):
    return {"q": q, "choices": choices, "answer": answer, "explain": explain, "index": index}

def D(did, title, items):
    return {"id": did, "title": title, "items": [{"prompt": p, "answer": a, "explain": e} for (p, a, e) in items]}

def LAB(lid, title, brief, steps, deliverable, checkpoint):
    return {"id": lid, "title": title, "brief": brief, "steps": steps,
            "deliverable": deliverable, "checkpoint": checkpoint}

def RES(title, url, kind, status=200):
    return {"title": title, "url": url, "kind": kind, "verifiedUtc": UTC, "httpStatus": status}

def VID(title, url, source, blurb, watchBefore):
    return {"title": title, "url": url, "source": source, "blurb": blurb,
            "order": 1, "watchBefore": watchBefore, "verifiedUtc": UTC, "httpStatus": 200}

# ================================================================= FT01 ===
FT01_NOTES = [
N("Source discipline: what we know and how we know it",
"""Every company fact in this module comes from one of three public sources: ThreatLocker's public website, ThreatLocker's public job postings, or publicly visible candidate reports (Glassdoor public snippets, fetched 2026-10-07). Full Glassdoor reviews sit behind a sign-in wall — noted as a limit, not bypassed.

What that means in the interview: you can say "I've studied your public materials closely." You cannot claim insider knowledge, employment, certification, or endorsement. If an interviewer asks something you don't know, the honest answer is "I haven't seen that published — here's what I do know about your public approach..."

Grounded fact sheet (public sources only):
- ThreatLocker is a Zero Trust endpoint-security company founded in 2017 in Orlando, Florida, by Danny Jenkins, Sami Jenkins, and John Carolan.
- Public materials describe the team as "Cyber Heroes" and the mission as a world where organizations operate free from cybercriminal influence.
- Core platform components (public site): Application Allowlisting, Ringfencing, Storage Control, Elevation Control, Endpoint Network Control, Configuration Management, Operational Alerts — a default-deny approach to servers and endpoints.
- Candidate reports (Glassdoor public snippets): interview difficulty easy-to-average (~2.45/5); many interviews brief and conversational, focused on background, eagerness, and culture fit; reported questions include "Could you build a virtual machine?", "Why ThreatLocker?", "Why cybersecurity?"; ~18 days average from first interview to offer.
- ThreatLocker publicly described a three-step process for a Senior Technical Support Specialist role: (1) technical phone interview, (2) product demo presentation back to the team, (3) onsite hands-on troubleshooting session. The IT Infrastructure Specialist loop may differ — prepare for all three.
- Public postings describe a background check and drug/substance screening after a conditional offer.
- Culture signals (public snippets): ~3.3/5 overall; in-office culture emphasized, no remote work; fast-paced, high-expectation environment; leadership praised in positive reviews."""),

N("The 60-second company answer — worked example",
"""When they ask "What do you know about ThreatLocker?" they are scoring three things: did you do the work, can you explain their model in your own words, and do you sound like a believer without sounding like a fanboy. Structure: company → approach → products → mission. Sixty seconds, no notes.

Worked example — say it aloud and time it:
> "ThreatLocker is a Zero Trust endpoint security company founded in 2017 in Orlando. Their whole platform is built on default-deny: instead of trying to recognize every piece of malware, Application Allowlisting means only explicitly approved software is allowed to run — everything else is denied by default. Then Ringfencing limits what even approved applications are allowed to do, so a trusted app can't be weaponized to reach the internet or touch sensitive files. Around that core they've built Storage Control, Elevation Control, Endpoint Network Control, Configuration Management, and Operational Alerts. The mission, in their words, is a world where organizations operate free from cybercriminal influence — and honestly, default-deny is the direction I believe endpoint security has to go, which is why I'm here."

Why this works: every claim is a public fact. It shows you understand the *model*, not just the product list. It ends with conviction, not flattery. Practice until it flows in your own words — never recite it verbatim or you'll sound rehearsed."""),

N("Allowlisting: the core product, explained three ways",
"""You must be able to explain allowlisting at three altitudes. Worked examples:

**To a fellow technician (precise):** "Allowlisting inverts the endpoint security model. Instead of maintaining signatures of known-bad files — an infinite, losing list — the agent enforces a policy of known-good executables. Anything not on the approved list is denied execution by default. Updates and new software go through an approval workflow, so the environment stays in a known-good state."

**To a non-technical manager (analogy):** "Think of it as a guest list instead of a most-wanted list. A bouncer with a most-wanted list has to recognize every criminal in the world. A bouncer with a guest list just checks whether you're on it. Allowlisting is the guest list for software."

**In one sentence (the interview answer):** "Only explicitly approved applications are allowed to run — everything else is denied by default."

Common follow-up: "Doesn't that break everything when users need new software?" Strong answer: "That's what the approval workflow and learning modes are for — the platform catalogs what's in the environment and admins approve through a request process, so legitimate software gets in quickly while unknown executables stay blocked. It's a process change as much as a technology change, and that's the honest trade-off."""),

N("Ringfencing and the control suite — one-liners plus a worked scenario",
"""One-sentence briefs for each public component. Memorize these cold:
- **Ringfencing:** limits what approved applications are allowed to *do* — e.g., blocking a trusted app from reaching the internet or touching sensitive files — containing weaponized legitimate software.
- **Storage Control:** governs which applications may write to protected storage locations, blocking ransomware-style mass encryption by untrusted processes.
- **Elevation Control:** governs when applications may run with elevated privileges, so users operate as standard accounts and elevation is granted deliberately.
- **Endpoint Network Control:** controls what the endpoint itself may reach on the network.
- **Configuration Management:** keeps endpoint configuration in a desired, auditable state.
- **Operational Alerts:** surfaces blocked/attempted actions so the team sees what the controls stopped.

Worked scenario — "Walk me through how Ringfencing stops an attack":
> "Say a user opens a malicious document and the PDF reader has a zero-day. The reader is an approved application, so allowlisting lets it run. But Ringfencing policy says the reader may not launch child processes or reach the internet. The exploit fires, tries to download a payload — denied. Tries to encrypt the documents folder — Storage Control denies the write. The attempt is logged and the team gets an Operational Alert. Three layers, one incident, zero damage — and none of it required recognizing the malware."

That scenario is the *concept* of the platform as publicly described — present it as your understanding of the model, not as insider product knowledge."""),

N("What candidates report: process, culture, and the limits of what we know",
"""Public candidate reports (Glassdoor public snippets, fetched 2026-10-07) paint a consistent picture — and you must know both the picture and its limits.

**What multiple candidates report:**
- Difficulty skews easy-to-average (~2.45/5). Many describe brief, conversational interviews focused on background, eagerness, and culture fit rather than deep technical grilling.
- Frequently reported questions: "Could you build a virtual machine?", "Why ThreatLocker?", "Why cybersecurity?", "Tell me about yourself."
- One July 2026 candidate reported the hiring signal directly: they are "looking for people starting their career in cybersecurity — as long as you're eager you will be fine." Eagerness + preparation is the signal.
- Average ~18 days from first interview to offer (Glassdoor aggregate).
- Post-offer: public postings describe a background check and drug/substance screening after a conditional offer.
- Culture (public snippets): ~3.3/5 overall; in-office culture with no remote work; fast-paced, high-expectation; leadership praised in positive reviews.

**The limits — say these to yourself, not necessarily aloud:**
- These are aggregates and snippets, not a complete picture. Your loop may differ.
- The three-step process (phone → demo → onsite troubleshooting) was described for a *Senior Technical Support Specialist* role, not IT Infrastructure Specialist. Prepare for all formats anyway — that's the point of FT04.
- Never cite Glassdoor in the interview ("I read on Glassdoor that..."). Use the knowledge silently: be ready for conversational culture-fit questions, have the VM answer ready, lead with eagerness.

**Worked example — using this knowledge without citing it:**
Interviewer: "So why us?" Weak answer: "I saw the reviews are good." Strong answer: "Because your default-deny approach is the direction I believe endpoint security has to go, and I want to build my infrastructure career inside a company whose product philosophy I can defend. I enrolled in your Zero Trust bootcamp on September 30th — I'm not casually interested, I'm invested." (See FT02-B01.)"""),

N("The independent-prep line: exact phrases to use and avoid",
"""You are a knowledgeable independent candidate. Every sentence you say must keep that line. Worked pairs — the wrong version, then the right version:

❌ "As a ThreatLocker-certified engineer..." → ✅ "I've studied your public platform materials closely as an independent candidate..."
❌ "My insider contact told me your interview process is..." → ✅ "From your public postings and candidate reports, I understand the process may include... I've prepared for each format."
❌ "I completed your bootcamp." → ✅ "I enrolled in the Zero Trust bootcamp on September 30th and have been working through the material since."
❌ "I was basically promised this role." → ✅ (never say anything like this; no hiring promise exists or is implied)
❌ "I know exactly how your console works." → ✅ "My understanding of the model from your public materials is... — I'd love to learn the console itself on the job."

The principle: deep knowledge of *public* material + explicit honesty about the boundary. Interviewers at a security company are professionally paranoid about exaggeration — the candidate who says "here's what I know, here's what I don't" earns trust faster than the one who bluffs.

Drill this with FT01-D3 until the right phrasing is automatic."""),
]

FT01_CARDS_ADD = [
C("Elevation Control in one sentence (concept)",
  "Governs when applications may run with elevated privileges — users operate as standard accounts and elevation is granted deliberately, not by default."),
C("Storage Control in one sentence (concept)",
  "Governs which applications may write to protected storage locations — blocks ransomware-style mass encryption by untrusted processes."),
C("The 60-second answer skeleton",
  "Company → approach → products → mission. 'ThreatLocker is a Zero Trust endpoint security company founded in 2017 in Orlando. Their default-deny platform...'"),
]

FT01_QUIZ_ADD = [
Q("An interviewer asks: 'Doesn't allowlisting break everything when users need new software?' What is the strong answer?",
  ["Say it never breaks anything",
   "Acknowledge the trade-off: approval workflows and learning modes let legitimate software in quickly while unknown executables stay blocked — it's a process change as much as a technology change",
   "Say you don't know",
   "Blame the users"],
  1, "Honest trade-off + the mechanism that manages it. Security people respect trade-off awareness.", 3),
Q("In the Ringfencing scenario, a weaponized PDF reader tries to download a payload. What happens?",
  ["Allowlisting blocks the reader from running at all",
   "Ringfencing denies the internet access; Storage Control denies mass-encryption writes; the attempt is logged and alerted",
   "Nothing — approved apps are fully trusted",
   "The firewall handles it"],
  1, "Approved-but-constrained: ringfencing limits what it may do, storage control guards writes, alerts fire.", 4),
Q("Which interview-loop fact is correctly qualified?",
  ["'Your process is phone, demo, then onsite — I know this for my role'",
   "'You publicly described a three-step process for a Senior Technical Support Specialist role; my loop may differ, so I've prepared for all formats'",
   "'Glassdoor says your interviews are easy'",
   "'I know exactly what you'll ask me'"],
  1, "The three-step structure was described for a different role — cite it with the qualifier.", 5),
Q("What is the reported hiring signal, and how do you use it?",
  ["There is no signal; ignore it",
   "'Looking for people starting their career in cybersecurity — as long as you're eager' → lead every answer with eagerness + evidence of preparation",
   "Pretend to be senior",
   "Memorize the Glassdoor reviews"],
  1, "Eagerness + preparation is the reported signal. Never cite Glassdoor aloud.", 6),
Q("What post-offer screening do public postings describe?",
  ["None",
   "Background check and drug/substance screening after a conditional offer — keep ID and documentation ready",
   "A polygraph",
   "Immediate termination"],
  1, "Public postings describe both; expect it as standard process, not a surprise.", 7),
Q("Which phrase holds the independent-prep line?",
  ["'I know exactly how your console works'",
   "'My understanding of the model from your public materials is...'",
   "'My insider contact told me...'",
   "'I'm basically already on the team'"],
  1, "Public-materials framing + explicit honesty about the boundary.", 8),
]

FT01_DRILLS = [
D("ft01-drill-pitch", "60-second company pitch — aloud, timed", [
("Deliver the 60-second 'What does ThreatLocker do?' answer. Time it.",
 "Company → approach → products → mission, ≤60 seconds, all public facts, ends with conviction not flattery.",
 "If you ran over, cut product deep-dives; the skeleton is company, approach, products, mission."),
("Answer 'Why ThreatLocker?' in 45 seconds.",
 "Default-deny conviction + bootcamp enrollment Sept 30 as proof of initiative + infrastructure career framing.",
 "Generic praise fails; the bootcamp date is your evidence of seriousness."),
("Explain the difference between allowlisting and ringfencing in 30 seconds.",
 "Allowlisting controls WHAT may run; ringfencing controls what approved apps may DO.",
 "What-runs vs what-it-may-do — the two halves of default-deny."),
]),
D("ft01-drill-products", "Product one-liners — cold recall", [
("Allowlisting, one sentence.", "Only explicitly approved applications may run; everything else is denied by default.", "Guest list, not most-wanted list."),
("Ringfencing, one sentence.", "Limits what approved applications are allowed to do — contains weaponized legitimate software.", "Even trusted apps get boundaries."),
("Storage Control, one sentence.", "Governs which apps may write to protected storage — blocks ransomware-style mass encryption.", "Guards the writes."),
("Elevation Control, one sentence.", "Governs when apps may run elevated — standard accounts by default, deliberate elevation.", "Least privilege for processes."),
("Configuration Management + Operational Alerts, one sentence each.", "Keeps endpoints in a desired auditable state; surfaces blocked/attempted actions to the team.", "Desired state + visibility."),
]),
D("ft01-drill-guardrails", "Independent-prep phrasing — fix the violation", [
("Fix: 'As a ThreatLocker-certified engineer, I...'",
 "'I've studied your public platform materials closely as an independent candidate...'",
 "No certification exists or is claimed — ever."),
("Fix: 'I completed your bootcamp.'",
 "'I enrolled in the Zero Trust bootcamp on September 30th and have been working through the material since.'",
 "Enrolled, never completed. They can verify."),
("Fix: 'I know exactly how your console works.'",
 "'My understanding of the model from your public materials is... — I'd love to learn the console itself on the job.'",
 "Model knowledge yes; insider product knowledge no."),
]),
]

FT01_LAB = LAB(
"ft01-lab-briefing",
"Company briefing one-pager",
"Produce a one-page briefing document you could review in the parking lot: company facts with sources, product one-liners, your 60-second pitch script in your own words, and three questions to ask them.",
["Write the fact sheet: founding, founders, mission, product list — each with its public source.",
 "Write each product one-liner from memory, then check against the cards.",
 "Draft your 60-second pitch script in your own words. Time it aloud; cut to ≤60 seconds.",
 "Draft three questions to ask the interviewers (about the team, the infrastructure stack, growth).",
 "Do a final honesty pass: strike any phrase implying affiliation, certification, or insider knowledge."],
"One-page briefing: sourced facts, one-liners, timed pitch script, three questions.",
"Every fact has a public source; pitch times ≤60s; zero affiliation-claim phrases remain.")

FT01_RES = [
RES("ThreatLocker — official site", "https://www.threatlocker.com/", "vendor"),
RES("ThreatLocker platform overview", "https://www.threatlocker.com/platform", "vendor"),
RES("ThreatLocker careers", "https://www.threatlocker.com/careers", "vendor"),
]

FT01_VIDS = [
VID("Allowlisting: Secure mode and real-time threat blocking",
    "https://www.youtube.com/watch?v=iPDhck3deag", "ThreatLocker (official)",
    "Official ThreatLocker walkthrough: Secure Mode blocking unauthorized software instantly — watch how the allowlisting model behaves in practice.",
    "notes"),
VID("Scheduled application policies with CEO Danny Jenkins",
    "https://www.youtube.com/watch?v=qVokkp0iU88", "ThreatLocker (official)",
    "ThreatLocker co-founder Danny Jenkins demonstrates time-based application control — how the platform restricts powerful tools to maintenance windows.",
    "notes"),
]

FT01_NOTES.append(
N("Visual: the default-deny model as a diagram",
"""Study this until you can redraw it from memory — then do exactly that on the whiteboard if they ask "how does it all fit together?"

```
                    ┌─────────────────────────────────┐
                    │        UNTRUSTED BY DEFAULT      │
                    │   every executable, every user,  │
                    │   every network flow             │
                    └───────────────┬─────────────────┘
                                    │ policy decision
                    ┌───────────────▼─────────────────┐
                    │      ALLOWLISTING (what runs)    │
                    │  known-good hash? signed by     │
                    │  trusted publisher? → APPROVED  │
                    │  otherwise → DENIED by default  │
                    └───────────────┬─────────────────┘
                                    │ approved apps only
              ┌─────────────────────▼─────────────────────┐
              │        RINGFENCING (what it may do)        │
              │  internet access?  ──► policy decides     │
              │  sensitive files?  ──► policy decides     │
              │  child processes?  ──► policy decides     │
              │  even trusted apps get boundaries         │
              └─────────────────────┬─────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
┌───────▼────────┐       ┌──────────▼─────────┐       ┌─────────▼────────┐
│ STORAGE CTRL   │       │ ELEVATION CTRL     │       │ NETWORK CTRL     │
│ which apps may │       │ when apps may run  │       │ what endpoints   │
│ write where    │       │ elevated           │       │ may reach         │
└───────┬────────┘       └──────────┬─────────┘       └────────┬─────────┘
        │                           │                          │
        └───────────────────────────┼──────────────────────────┘
                                    ▼
                    ┌───────────────────────────────┐
                    │ CONFIG MGMT: desired state,    │
                    │ auditable                     │
                    │ OPERATIONAL ALERTS: every     │
                    │ blocked attempt is visible    │
                    └───────────────────────────────┘
```

Read it top-down in the interview: "Everything starts untrusted. Allowlisting decides what runs. Ringfencing decides what the approved apps may do. The control suite governs storage, elevation, and network. Configuration management keeps it auditable, and operational alerts make every blocked attempt visible."

The one-line version: **deny by default, approve explicitly, constrain continuously, alert on everything.** If you can say that sentence and draw this diagram, you understand their model better than 90% of candidates."""))

FT["IL27-FT01"] = {
    "notes": FT01_NOTES, "cards_add": FT01_CARDS_ADD, "quiz_add": FT01_QUIZ_ADD,
    "drills": FT01_DRILLS, "handsOnLab": FT01_LAB,
    "supplementalResources": FT01_RES, "videos": FT01_VIDS,
    "estimatedMinutes": 180,
}

# ================================================================= FT02 ===
FT02_NOTES = [
N("How to use this bank: the 6-day method",
"""Sixty questions across eight categories. Nine are publicly reported by ThreatLocker candidates (marked 'reported by candidates'); the rest are likely probes authored for this IT Infrastructure Specialist role (marked 'likely'). The model answers are starting points — rebuild each in your own words and anchor it to something you have actually done.

The method, day by day:
- **Days 1–2 (FT track day 2):** Work one category per day aloud. 90 seconds per answer, phone recording on. Behavioral first — those are the reported questions and the highest-probability asks.
- **Day 3:** Random sampling. Have someone (or a random-number generator) pick 15 questions across categories. No warm-up, no cherry-picking.
- **Day 4 (mock day):** FT04 pulls 8 from this bank under timed conditions.
- **Day 5:** Weak-question drill — only the questions you scored 0–1 on. Re-answer until every one is a 2 or 3.

Rules that never bend: never memorize model answers word-for-word — interviewers detect recitation instantly and it reads as dishonest. Every technical answer gets paired with evidence from your real history (homelab, founder work, bootcamp). If an interviewer asks where you prepared, say "public candidate reports and your public materials" — never claim insider knowledge."""),

N("The 90-second answer architecture — worked example",
"""Every technical answer follows the same skeleton: **verdict → method → evidence → close**. Ninety seconds is roughly 200 words aloud. Worked example with FT02-N01 ("A user can't reach the internet but can reach local servers"):

> **Verdict (10s):** "Local works, so the local stack is fine — this is a gateway, DNS, or upstream problem."
> **Method (45s):** "I'd isolate it in order: ping the default gateway first — if that fails, it's the gateway or the local route. Then ping 8.8.8.8: if IPs work but names don't, it's DNS — check the resolver config and try nslookup. If neither works past the gateway, it's the gateway itself or upstream — check the gateway's status and the WAN link."
> **Evidence (20s):** "I've run exactly this triage in my homelab when a VM lost external access after a virtual-switch change — turned out to be the gateway assignment on the new switch."
> **Close (10s):** "Layered, outside-in, and I verify each layer before moving up."

Why it scores: the interviewer hears a *method*, not just an answer. The evidence line is short and real. The whole thing fits in 90 seconds. Now do the same for FT02-W02 (GPO not applying): verdict "scope issue until proven otherwise" → method "gpresult, OU link, filtering, inheritance, replication" → evidence "homelab GPO for workstation baselines" → close."""),

N("Handling reported questions — worked example",
"""The nine reported questions are your highest-probability asks. They skew conversational — which means most candidates under-prepare them and ramble. Worked example with FT02-B03 ("Could you build a virtual machine?"):

Weak answer: "Yeah, I've built VMs before." (Scores 1/3 — vague, no evidence.)
Strong answer (90 seconds):
> "Yes — and I can walk you through it. Enable the Hyper-V role, create an external virtual switch for network access, then create the VM: Generation 2 for a modern OS, assign vCPUs and RAM with headroom for the workload, attach a dynamically expanding VHDX sized for it, mount the ISO, install the OS, install integration services, apply my baseline configuration, and take a checkpoint before any changes. I've done this repeatedly in my homelab — I can whiteboard the whole flow right now if you'd like."

The structure: **yes + ordered steps + specific nouns (Hyper-V, Gen2, VHDX) + offer to demonstrate**. The offer to whiteboard is the power move — it converts a verbal question into a practical demonstration, and interviewers remember it.

Do the same treatment for each reported question: FT02-B01 (why ThreatLocker → conviction + bootcamp date), FT02-B04 (endpoint security → show you studied THEIR model), FT02-B05 (hardest homelab problem → the RAID 0 migration, lesson-first)."""),

N("Anchoring to real evidence — worked example",
"""A correct answer with no evidence scores 2/3. A correct answer anchored to something you've done scores 3/3. The transformation, worked example with FT02-E03 (patching without breaking users):

Generic (2/3): "Ringed rollouts: pilot group first, then broad deployment with deadlines and notifications, maintenance windows for servers, expedited rings for zero-days, and a rollback plan."

Anchored (3/3): "Ringed rollouts: pilot group first, then broad deployment with deadlines and user notifications. I learned the discipline running my own infrastructure — when I maintain my homelab hosts, I patch one node, validate services, then roll to the rest, with a snapshot before each ring. Same principle at fleet scale: expedited ring for critical zero-days, deferrals with hard deadlines for workstations, and a rollback plan before any fleet-wide push."

The anchor doesn't have to be enterprise — it has to be *real*. Your evidence inventory: homelab builds and migrations, founder/DevSecOps production operations, bootcamp enrollment, the Oct 7 prep marathon. Map every FT02 technical question to at least one inventory item before mock day."""),

N("Recitation vs fluency: what interviewers detect",
"""Interviewers — especially at a security company — are trained to detect memorization. The tells: identical phrasing across answers, unnatural pacing, eyes defocusing mid-answer, collapse when interrupted with a follow-up. A memorized answer that gets a follow-up question dies; an *understood* answer adapts.

Worked example — the follow-up test. You deliver FT02-Z01 ("What is Zero Trust?") fluently: "Never trust, always verify — every access request authenticated, authorized, continuously re-evaluated." The interviewer follows up: "Okay, so how does that change how you'd design our office network?" The reciter freezes or repeats the definition. The fluent candidate reasons aloud: "I'd assume breach from the start — micro-segment the network so departments are isolated zones, put identity at the center with MFA and conditional access, remove implicit trust for anything inside the perimeter, and make every cross-segment connection an explicit, logged decision."

Train for follow-ups, not just questions: after every bank answer, ask yourself "why?" and "how would you apply that here?" twice. That's the FT04 branching-scenario muscle."""),

N("Provenance honesty in the room",
"""If an interviewer asks where you prepared — or if a question clearly comes from candidate reports — the honest framing is: "From your public materials and public candidate reports." Never imply insider knowledge. Never say "I heard your interviews are easy." Never reference Glassdoor by name.

Worked example — the trap and the recovery. Interviewer: "You seem well-prepared for our process. How did you know what to expect?" Weak: "I read all about it online." Strong: "I studied your public platform materials closely, and I prepared for the formats you've publicly described — technical conversation, a demo-style presentation, and hands-on troubleshooting — because I'd rather be over-prepared for your format than surprised by it."

Notice what the strong answer does: it demonstrates knowledge of the three-step structure *without* claiming it applies to this loop, and it frames preparation as respect for their time. That's the independent-prep line held under pressure."""),
]

FT02_CARDS_ADD = [
C("Behavioral slice — the 5 you must nail cold",
  "Why ThreatLocker? Why cybersecurity? Build a VM? Tell me about yourself. Hardest homelab problem? → 90s each, evidence-anchored, never recited."),
C("Windows Server/AD slice — cue words",
  "DC promo: role → promote → DNS → repadmin → SYSVOL → FSMO. GPO: gpresult → scope → filtering → inheritance → replication."),
C("Networking slice — cue words",
  "No internet but LAN works: gateway → ping 8.8.8.8 (routing vs DNS) → upstream. Single-host drops: physical first, swap-test."),
C("Virtualization slice — cue words",
  "Hyper-V VM: role → vSwitch (external/internal/private) → Gen2 → vCPU/RAM → VHDX → ISO → baselines → checkpoint. Checkpoint ≠ backup."),
C("Endpoint hardening slice — cue words",
  "Baseline image → patch → BitLocker → Defender → least privilege → firewall → enroll → document. Drift detection."),
C("PowerShell slice — cue words",
  "Get-ADUser -Filter {Enabled -eq $false}; WhatIf → lab → production; CIM sessions for fleet queries; JEA for remoting."),
C("Zero Trust slice — cue words",
  "Never trust, always verify. Identity = perimeter. Micro-segmentation = blast radius. Allowlisting = finite good vs infinite bad."),
C("Incident response slice — cue words",
  "Contain → preserve evidence → scope → eradicate → recover → after-action. Ransomware: isolate → scope → verify clean backups."),
C("The 90-second skeleton",
  "Verdict (10s) → method (45s) → evidence (20s) → close (10s). ~200 words aloud."),
C("Follow-up armor",
  "After every answer ask yourself 'why?' and 'how would you apply that here?' twice. Fluency survives follow-ups; recitation dies."),
]

FT02_QUIZ_ADD = [
Q("You answer a technical question correctly but with zero evidence from your history. What score and why?",
  ["3/3 — correctness is all that matters", "2/3 — correct but unanchored; evidence is what earns the third point",
   "0/3 — wrong format", "1/3 — too short"],
  1, "The bank's rubric: 2 = correct, 3 = correct + evidence. Map every question to your inventory.", 2),
Q("An interviewer interrupts your memorized Zero Trust answer with 'how would you apply that to our office network?' What distinguishes the fluent candidate?",
  ["Repeating the definition louder", "Reasoning aloud from the model: assume breach, micro-segment, identity-centered, explicit cross-segment decisions",
   "Saying 'great question' and stalling", "Changing the subject"],
  1, "Fluency = reasoning from the model under follow-up pressure. Train 'why?' x2 after every answer.", 3),
Q("What is the correct provenance framing if asked where you prepared?",
  ["'I have insider sources'", "'From your public materials and public candidate reports' — never claim insider knowledge",
   "'Glassdoor told me everything'", "Dodge the question"],
  1, "Public-materials framing; never name Glassdoor, never imply insider access.", 4),
Q("For FT02-B03 ('Could you build a VM?'), what is the power move after the ordered steps?",
  ["Stop talking", "'I can whiteboard the whole flow right now if you'd like' — convert verbal to demonstration",
   "Ask about salary", "List every hypervisor ever made"],
  1, "The whiteboard offer converts a question into a demo. Interviewers remember it.", 5),
Q("A 'likely' probe stumps you. What is the scored response?",
  ["Bluff confidently", "'I haven't hit that in production yet. Here's how I'd figure it out: [method].' — honesty + method",
   "Go silent", "Answer a different question"],
  1, "Honesty + method beats bluffing; bluffing is detectable and fatal at a security company.", 6),
Q("How do you convert a generic patching answer into a 3/3?",
  ["Add more jargon", "Anchor it: 'I learned the discipline maintaining my homelab hosts — patch one node, validate, roll, snapshot before each ring'",
   "Speak faster", "Cite a vendor whitepaper"],
  1, "Real + short beats generic + long. Your evidence inventory is the anchor bank.", 7),
Q("What is the Day 3 drill for this bank?",
  ["Re-read the model answers silently", "Random sampling: 15 questions across categories, no warm-up, no cherry-picking, aloud and recorded",
   "Only study reported questions", "Take the day off"],
  1, "Random sampling under mild pressure is what converts study into performance.", 8),
]

FT02_DRILLS = [
D("ft02-drill-behavioral", "Behavioral sprint — 9 reported questions, aloud", [
("Why ThreatLocker? 45 seconds.", "Default-deny conviction + bootcamp enrolled Sept 30 + infrastructure career framing.", "Conviction, not flattery."),
("Could you build a VM? 90 seconds with steps.", "Yes + Hyper-V ordered steps (role → vSwitch → Gen2 → VHDX → baselines → checkpoint) + whiteboard offer.", "Steps + offer to demo."),
("Hardest homelab problem? 90 seconds.", "RAID 0 migration: verify backups → staged batches with checksums → validate → lesson: infrastructure is change management.", "Real history, lesson-first."),
("Tell me about yourself. 90 seconds.", "Builder → founder/DevSecOps → homelab depth → bootcamp Sept 30 → goal: trusted infrastructure specialist.", "Chronological, ends with the goal."),
("Frustrated customer? 60 seconds.", "De-escalate: acknowledge impact → own next step with ETA → communicate → document.", "They feel unheard — fix that first."),
]),
D("ft02-drill-technical", "Technical sprint — one per category, 90 seconds each", [
("GPO not applying. Verdict + method.", "Verdict: scope issue. Method: gpresult → OU link → filtering → inheritance → replication → gpupdate.", "Scope before re-linking randomly."),
("User can't reach internet, LAN works.", "Gateway → ping 8.8.8.8 (routing vs DNS) → upstream. Verify each layer.", "Isolate: gateway vs DNS vs upstream."),
("Checkpoint vs backup.", "Checkpoint = short-term rollback, same storage. Backup = real recovery, off-host, tested. Checkpoint is NOT a backup.", "Say it with conviction."),
("EDR flags a workstation.", "Isolate preserving state → review alert context → escalate per IR plan → forensics before reimage.", "Speed on containment, discipline after."),
("Suspected ransomware on file server. First three.", "Isolate → scope (shares, accounts) → preserve evidence + verify clean backups. No premature recovery.", "Contain first, always."),
]),
D("ft02-drill-zerotrust", "Zero Trust fluency — follow-up armor", [
("What is Zero Trust? Then: how would you apply it to an office network?",
 "Definition: never trust, always verify. Application: assume breach, micro-segment, identity-centered MFA/CA, explicit cross-segment decisions.",
 "Reason from the model, don't repeat the definition."),
("Explain allowlisting to a skeptical sysadmin.",
 "You know signature tools miss novel threats — you've lived it. Finite good vs infinite bad; approval workflow manages the trade-off.",
 "Empathy first, then the inversion."),
("Give a concrete least-privilege example.",
 "Helpdesk: password resets yes, domain admin no. Backup service account: read volumes, no interactive logon. Quarterly reviews.",
 "Concrete + review cadence."),
]),
]

FT02_LAB = LAB(
"ft02-lab-audit",
"Recorded answer audit",
"Record yourself answering 10 bank questions (mix reported + likely), transcribe, and score each against the rubric. Convert every sub-2 into a re-take.",
["Pick 10 questions: 4 reported behavioral, 6 technical across categories.",
 "Answer each aloud in ≤90 seconds, phone recording on. No re-takes during the set.",
 "Transcribe each answer (speech-to-text or manual).",
 "Score 0–3: 0 wrong/silent, 1 vague, 2 correct, 3 correct + evidence. Note time overruns.",
 "For every score ≤1: rewrite the answer using verdict → method → evidence → close, re-record.",
 "File the scored transcripts — they're your evidence of preparation trajectory."],
"10 scored transcripts with every answer at 2+ and ≤90 seconds.",
"All 10 answers score ≥2, none exceed 90 seconds, no verbatim recitation of model answers.")

FT02_RES = [
RES("Windows Server documentation", "https://learn.microsoft.com/en-us/windows-server/", "docs"),
RES("PowerShell documentation", "https://learn.microsoft.com/en-us/powershell/", "docs"),
RES("Active Directory Domain Services overview", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview", "docs"),
RES("Windows commands reference", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands", "docs"),
]

FT["IL27-FT02"] = {
    "notes": FT02_NOTES, "cards_add": FT02_CARDS_ADD, "quiz_add": FT02_QUIZ_ADD,
    "drills": FT02_DRILLS, "handsOnLab": FT02_LAB,
    "supplementalResources": FT02_RES, "videos": [],
    "estimatedMinutes": 660,
}

# ================================================================= FT03 ===
FT03_NOTES = [
N("STAR mechanics: the 15-second version, expanded",
"""Situation → Task → Action → Result. Under two minutes. End on the lesson. That's the whole method — but each letter has a discipline:

- **Situation (20s):** One or two sentences of context. Not your life story — just enough that the action makes sense. Cut everything the interviewer doesn't need to evaluate you.
- **Task (15s):** What was *your* responsibility? Not the team's — yours. "I was responsible for..." is the sentence.
- **Action (60s):** What YOU did, specifically, in order. Verbs, not adjectives. This is 60% of the story — most candidates rush it and it's the part being scored.
- **Result (25s):** The outcome *plus the lesson or transferable skill*. "We migrated cleanly" is an outcome. "…and it's why I verify backups as a non-negotiable gate in every plan I write" is the lesson — and the lesson is what interviewers remember.

Worked micro-example (30 seconds total): "Situation: my homelab outgrew its storage layout. Task: migrate live data to a new RAID 0 array with zero loss. Action: I verified backups first, built the array, migrated in staged batches with checksum verification, and validated every service after cutover. Result: clean migration, zero data loss — and a reusable runbook. The lesson: infrastructure work is really change-management work; the plan matters more than the commands."

Record each story, listen back, cut filler. Two minutes max per story."""),

N("The honesty tripwires — what never to say",
"""Six STAR stories are already built in this module from your real, documented history (see the stories array). The honesty line for each:

- **Bootcamp:** "enrolled September 30th and working through it" — never "completed." They can verify; a security company *will* notice.
- **Founder:** your title is Founder and DevSecOps/Full Stack Developer at Interstitium Labs. The work was real. Don't inflate team size, revenue, or headcount.
- **Homelab:** state homelab scale plainly — "in my homelab" is a strength here, not a weakness. Interviewers respect honest homelab depth; they punish homelab-described-as-enterprise.
- **Numbers:** if a story needs a number you don't have, drop the number. A story without metrics beats a story with invented ones.
- **Certifications:** never claim one you don't hold. If pressed: "I don't have that yet — here's what I do have, and here's my plan to earn it."

Worked example — the pressed follow-up. Interviewer: "So you're Security+ certified?" Wrong: "Basically, I've studied the material." (Sounds evasive.) Right: "Not yet — I'm studying the Security+ domains now and it's in my 30/60/90 plan. What I can do today is walk you through the concepts — want me to explain how I'd apply least privilege to your endpoint fleet?" Honest, then pivot to demonstrated competence."""),

N("Story inventory: mining your real history",
"""Before mock day, run a full inventory pass so no experience goes unused. The worksheet method:

1. **Timeline sweep:** list every infrastructure thing you've built, broken, fixed, or migrated — homelab, founder work, bootcamp, the Oct 7 prep marathon. Aim for 15+ raw items; quantity first.
2. **Theme mapping:** the interview themes are ownership, troubleshooting depth, learning speed, honesty under pressure, customer empathy, and initiative. Tag each raw item with every theme it could serve.
3. **STAR-draft the top 8:** write Situation/Task/Action/Result for the eight best-tagged items. The six stories in this module are your core six; the extra two are spares for unexpected questions.
4. **The 'so what' test:** read each Result and ask "what does this prove about me as an infrastructure hire?" If you can't answer in one sentence, the story needs a sharper lesson.

Worked mini-inventory (yours, already done — verify it): bootcamp enrollment → initiative/learning speed; prep marathon → work ethic/pressure; founder work → ownership/breadth; homelab migration → technical depth/change discipline; platform shipping → quality bar/delivery; honest junior → ambition/honesty. Six stories, six themes, zero invention.

Do this pass on paper tonight. The physical act of writing surfaces stories that typing misses."""),
N("TEMPLATE — practice only: building a STAR story from a junior scenario",
"""**This is a TEMPLATE for practice, not your history.** Use it to rehearse the STAR *mechanics* on a scenario that isn't yours, so your real stories stay clean. Never present template content as your experience.

Template scenario: "A junior tech's first on-call weekend."
- **Situation:** "A monitoring alert fired at 2 AM on my first on-call weekend — a file server's disk was at 95%."
- **Task:** "I was the responder. Keep the server up until morning without data loss."
- **Action:** "I remoted in, confirmed it was log growth not user data, compressed and archived the oldest logs to secondary storage, verified the service was healthy, and wrote a disk-space monitor check so it wouldn't page blindly again."
- **Result:** "Server stayed up, no data lost. Lesson: the fix is half the job — the monitor I added afterward is what made it a real resolution."

Now the exercise: take this template and (1) time yourself delivering it in under two minutes, (2) identify which interview theme it serves (ownership + troubleshooting), (3) rewrite the Result's lesson in your own words. Then do the same with your real stories — the mechanics transfer, the content stays honest.

Why practice on templates: it separates *storytelling skill* from *your facts*. In the interview, the skill carries your facts."""),
N("The 2-minute delivery: pacing and the lesson close",
"""Two minutes is ~260 words aloud. The pacing that lands:

- **0:00–0:20 — Situation.** Slow, scene-setting. One breath per sentence.
- **0:20–0:35 — Task.** The pivot sentence: "My responsibility was..." Slightly faster — this is the bridge.
- **0:35–1:35 — Action.** Your natural pace. Ordered steps, specific verbs. This is where you earn the score — don't rush it.
- **1:35–2:00 — Result + lesson.** Slow down for the lesson. Make eye contact (or pause on the phone). The lesson is the last thing they hear — it's what they write down.

Worked example — the lesson close, three versions of the same story ending:
- Weak: "...so yeah, it worked out." (No lesson. Forgettable.)
- Okay: "...and we had zero data loss." (Outcome, no transfer.)
- Strong: "...zero data loss — and it's why verification is a non-negotiable gate in every plan I write now. I'd bring that same discipline here." (Outcome + lesson + forward link to the role.)

The forward link ("I'd bring that here") is the closer's move: it converts a past story into a future promise. Use it on your two strongest stories, not all six — scarcity keeps it meaningful.

Delivery drill: record all six stories back-to-back. Listen for filler ("um," "like," "you know"), hedging ("I kind of..."), and rushed actions. Cut, re-record. Two passes minimum before mock day."""),
N("Mapping stories to questions — worked example",
"""In the interview you don't get to choose the question — but you do choose which story answers it. Build the mapping now so retrieval is instant.

Worked mapping (yours):
| Question | Story | Why it fits |
|---|---|---|
| Why ThreatLocker? | S1 bootcamp enrollment | Proves conviction with a dated action |
| Hardest homelab problem? | S4 homelab migration | Technical depth + change discipline |
| Tell me about yourself? | S3 founder + S6 honest junior | Breadth, then trajectory framing |
| Failed? | S4 migration (verification lesson) | Failure → system → prevention |
| Frustrated customer? | S5 platform shipping (quality gates) | Ownership of other people's pain |
| Why hire you over experience? | S6 honest junior + S2 prep marathon | Trajectory + preparation as evidence |
| Coworker conflict? | S3 founder (disagree-and-commit) | Honest about background, principled |

The exercise: for each of the 9 reported questions in FT02, write the story ID you'd reach for. If any question has no story, that's a gap — draft a seventh story from your inventory (note 3) or prepare an honest "here's how I'd handle it" answer. No question should catch you without a mapped response.

The meta-skill: interviewers often ask the *same* competency three ways. When you hear the third variant, don't invent a new story — tell the best-fitting one again from a different angle. Consistency reads as depth."""),
]

FT03_CARDS_ADD = [
C("S2 prep marathon — themes", "Work ethic, preparation, handling pressure. 'I treated preparation like an engineering problem with a deadline.'"),
C("S3 founder — themes", "Ownership, breadth, self-direction. 'No escalation path — every decision terminates with you.'"),
C("S4 homelab migration — themes", "Technical depth, change discipline. 'Infrastructure work is change-management work.'"),
C("S5 platform shipping — themes", "Quality bar, delivery, operational discipline. 'Verify before you ship.'"),
C("S6 honest junior — themes", "Ambition, honesty. 'Sell the slope, not the intercept.'"),
C("S1 bootcamp — themes", "Initiative, continuous learning, why-ThreatLocker. 'Enrolled Sept 30, never completed.'"),
C("The 'so what' test", "Read each Result; if you can't state what it proves about you in one sentence, sharpen the lesson."),
C("Pacing map", "0:00–0:20 Situation · 0:20–0:35 Task · 0:35–1:35 Action · 1:35–2:00 Result + lesson. Slow down for the lesson."),
C("The forward link", "'I'd bring that same discipline here.' Use on your two strongest stories only."),
C("Template vs real", "Templates rehearse mechanics; real stories carry facts. Never present template content as experience."),
]

FT03_QUIZ_ADD = [
Q("Your Action section is 20 seconds and your Situation is 90 seconds. What's wrong?",
  ["Nothing — context matters most", "Inverted: Action should be ~60% of the story (the scored part); Situation needs 1–2 sentences",
   "Stories should be 5 minutes", "Skip the Action"],
  1, "Action is what's scored. Situation is scene-setting, not the story.", 1),
Q("An interviewer asks about a certification you don't hold. What is the scored response?",
  ["'Basically, I've studied the material'", "'Not yet — here's what I do have, and my plan to earn it. Want me to demonstrate the concepts?'",
   "Change the subject", "Claim it and hope"],
  1, "Honest + pivot to demonstrated competence. Evasion and invention both fail.", 2),
Q("What is the 'forward link' and when do you use it?",
  ["A networking cable", "'I'd bring that same discipline here' — converts a past story into a future promise; use on your two strongest stories only",
   "Use on every story", "Never use it"],
  1, "Scarcity keeps it meaningful. Two stories max.", 3),
Q("You hear the third variant of the same competency question. What do you do?",
  ["Invent a new story", "Tell the best-fitting story again from a different angle — consistency reads as depth",
   "Say 'you already asked that'", "Go silent"],
  1, "Re-angled consistency beats invented variety.", 4),
Q("What is the 'so what' test?",
  ["A personality quiz", "Read each Result; if you can't state what it proves about you as a hire in one sentence, sharpen the lesson",
   "A salary negotiation tactic", "Skip it"],
  1, "The lesson is what's remembered — test every story for it.", 5),
Q("Why practice STAR mechanics on a TEMPLATE scenario?",
  ["To have more stories to tell", "Separates storytelling skill from your facts — the skill transfers, your real stories stay clean and honest",
   "Templates are better stories", "To fool interviewers"],
  1, "Mechanics on templates, facts from real history. Never present template content as experience.", 6),
Q("Your story runs 3 minutes. What do you cut first?",
  ["The lesson", "Situation detail and filler — keep Action intact; the lesson close is the last thing cut",
   "The Action", "Nothing — longer is better"],
  1, "Cut context and filler first. Action and lesson are the load-bearing parts.", 7),
Q("Which bootcamp phrasing holds the honesty line?",
  ["'I completed the bootcamp'", "'I enrolled September 30th and have been working through the Zero Trust material since'",
   "'I'm basically certified'", "Don't mention it"],
  1, "Enrolled + substance. They can verify; a security company will notice.", 8),
]

FT03_DRILLS = [
D("ft03-drill-delivery", "Story delivery — all six, timed", [
("S1 bootcamp enrollment. ≤2 min, end on the lesson.", "Situation → Task → Action → Result + lesson: 'enrolled Sept 30 to prove I understood the model, not the buzzword.'", "Lesson close, forward link optional."),
("S4 homelab migration. ≤2 min.", "Verify backups → build array → staged batches with checksums → validate → lesson: change management.", "Specific verbs, ordered steps."),
("S6 honest junior. ≤2 min.", "Junior on paper → months of verifiable prep → sell trajectory: 'evaluate me on slope, not intercept.'", "Never apologize for being junior."),
("S2 prep marathon. ≤2 min.", "Blank on skills narrative → full prep marathon in one night → lesson: prepare obsessively and systematically.", "Discipline, not desperation."),
]),
D("ft03-drill-mapping", "Question → story mapping, instant recall", [
("'Why ThreatLocker?' → story?", "S1 — conviction with a dated action.", "Dated proof beats praise."),
("'Tell me about a time you failed.' → story?", "S4 — skipped verification once, now it's a non-negotiable gate.", "Failure → system → prevention."),
("'Why should we hire you over experience?' → story?", "S6 + S2 — trajectory + preparation as evidence.", "Slope, not intercept."),
("'Frustrated customer?' → story?", "S5 — quality gates as ownership of others' pain; or honest 'here's my method' if no direct story.", "Never invent a customer."),
]),
D("ft03-drill-template", "Template mechanics practice (labeled practice only)", [
("Deliver the template on-call story. ≤2 min.", "2 AM disk alert → remote in → log growth identified → archive + monitor added → lesson: the monitor made it a real resolution.", "Mechanics practice — not your history."),
("Rewrite the template's Result lesson in your own words.", "Any honest rephrasing that keeps outcome + transferable lesson.", "Your words, template facts."),
("Which theme does the template serve?", "Ownership + troubleshooting depth.", "Theme-tagging is the retrieval skill."),
]),
]

FT03_LAB = LAB(
"ft03-lab-inventory",
"STAR inventory + recorded stories",
"Complete the story inventory worksheet, record all six real stories, and drill two template scenarios for mechanics. Everything labeled: real vs template.",
["Timeline sweep: list 15+ infrastructure things you've built, broken, fixed, or migrated.",
 "Theme-tag each item (ownership, troubleshooting, learning speed, honesty, empathy, initiative).",
 "Verify the six module stories against your inventory; draft 2 spare STAR stories for gaps.",
 "Record all six stories back-to-back, ≤2 min each. Two passes: cut filler, sharpen lesson closes.",
 "Drill the template on-call scenario twice for mechanics (label recordings TEMPLATE).",
 "Build the question→story map for all 9 reported FT02 questions; confirm zero gaps."],
"Inventory worksheet + 6 recorded real stories (2 passes) + question→story map with no gaps.",
"All six stories ≤2 min, each ends on a lesson; every reported question maps to a story; templates clearly labeled.")

FT03_RES = [
RES("ThreatLocker careers — culture and values", "https://www.threatlocker.com/careers", "vendor"),
]

FT["IL27-FT03"] = {
    "notes": FT03_NOTES, "cards_add": FT03_CARDS_ADD, "quiz_add": FT03_QUIZ_ADD,
    "drills": FT03_DRILLS, "handsOnLab": FT03_LAB,
    "supplementalResources": FT03_RES, "videos": [],
    "estimatedMinutes": 240,
}

# ================================================================= FT04 ===
FT04_NOTES = [
N("How the mock works: rules, scoring, re-take protocol",
"""Four timed, scored rounds modeled on the interview structure ThreatLocker publicly described for an IT-adjacent role (technical phone screen → demo presentation → onsite troubleshooting), plus a behavioral round. Honest framing: the Infrastructure Specialist loop may differ — you prepare for all formats.

The rules:
- **Rounds 1–4 back-to-back** on mock day, in order, with only 5-minute breaks. This simulates interview fatigue — round 4 is where unprepared candidates collapse.
- **Aloud, always.** Silent "thinking" doesn't count. Record every round (phone voice memo is fine).
- **Score immediately after each round** using the rubrics below. No generosity: a 2 is "correct," a 3 is "correct + evidence." Most first attempts land 1s and 2s — that's the point.
- **Overall pass: all four rounds at or above their pass marks.** Any round below → targeted study of its weakest questions → re-take the same day. The re-take is non-negotiable; walking away from a failed round teaches your brain that failing is acceptable.
- **Question sources:** Round 1 samples 8 from the FT02 bank (mix reported + likely). Round 2 is the whiteboard talk. Round 3 uses the three scenarios below. Round 4 uses FT02 behavioral + your six STAR stories.

What you're really training: starting answers under pressure, thinking aloud, recovering from blanks, and finishing strong when tired. The content is FT02/FT03 — the mock is the *performance* layer on top."""),

N("Round 1: phone screen tactics — worked example",
"""20 minutes, 8 questions, 90 seconds each. On a phone screen there is no whiteboard and no body language — your voice is the entire signal. Tactics:

- **Number your structure aloud:** "Three things I'd check: first..." Numbering keeps you from rambling and signals organized thinking through audio alone.
- **Verdict first:** give the conclusion in the first 10 seconds, then the method. On the phone, interviewers decide early; don't bury the lead.
- **Name the nouns:** gpresult, repadmin, VHDX, Get-ADUser — specific tool names are credibility through a phone line.
- **End with an offer:** "I can go deeper on any of those" — invites the follow-up you want.

Worked example — the round 1 answer that scores 3/3. Question: "A GPO isn't applying to a user."
> "Verdict: it's a scope issue until proven otherwise. Three things I'd check, in order: first, gpresult /r on the affected machine to see what's applied and what's denied — that tells me whether it's scope or something stranger. Second, the link itself: is the user in the linked OU, link order, Enforced versus Block Inheritance, security filtering, WMI filters. Third, replication — is the DC I'm checking actually converged? Then gpupdate /force and re-check. I've hit exactly this in my homelab with a workstation baseline policy — turned out to be security filtering I'd set and forgotten. The method is: verify with gpresult, fix the scope, don't re-link randomly."

Score it: verdict (✓), ordered method with named tools (✓), real evidence (✓), 90 seconds (✓) → 3/3. Now sample 8 from FT02 and do the same for each."""),

N("Round 2: the 10-minute demo talk — full outline, worked example",
"""ThreatLocker publicly described a demo-presentation step for an IT-adjacent role: present back to the team. Your topic: "How I would harden and document a new Windows Server for a Zero Trust environment." Ten minutes, whiteboard or screen share, then 20 minutes of follow-up questions from FT02.

The outline (memorize the skeleton, not the script):
1. **Problem frame (1 min):** "A new server is an untrusted asset until proven otherwise. My job: make it known-good, least-privilege, and auditable before it touches production."
2. **Approach (2 min):** Baseline-first: patched gold image or clean install + updates; remove unneeded roles/features; local admin hygiene (LAPS-style thinking, no shared passwords).
3. **Demo (4 min):** Walk the controls: firewall profile, Defender posture, BitLocker where applicable, service minimization, audit policy, documentation of every change. *Draw* the server with its trust boundaries as you talk.
4. **Trade-offs (2 min):** "Hardening is never free — every disabled service is a potential break. My rule: disable with documentation and a rollback note, so the next admin knows why."
5. **Questions (1 min + 20 min follow-up):** "What would you challenge in this approach?" — inviting critique shows confidence.

Worked opening (the first 60 seconds, verbatim-ish — then make it yours):
> "If I unbox a Windows Server today, I treat it as hostile until I've made it otherwise. My hardening sequence is: one, get it to a known-good state — fully patched, nothing extra installed. Two, shrink the attack surface — remove unneeded roles and features, disable unneeded services, and set the firewall to deny-by-default with explicit allows. Three, identity hygiene — no shared local admin passwords, dedicated admin accounts, and audit policy on from the start. Four, document everything as I go, because an undocumented hardened server is a server nobody can maintain. Let me walk you through each layer..."

Scoring: clarity 0–6, technical accuracy 0–6, handling questions 0–6, time discipline 0–6. Pass ≥17/24. The trap: rambling past 10 minutes. Finish at 9, not 11."""),

N("Round 3: thinking aloud — worked example",
"""30 minutes, 3 scenarios, 10 minutes each. The meta-skill: narrate your methodology. Interviewers score the thinking they can *hear*, not the answer you reach silently.

The narration template: "I'm checking X first because [reason]. That gives me [information], which tells me whether to go to Y or Z."

Worked example — scenario (a): "A user can't reach the file share."
> "Okay — first I need to know the blast radius, so I'm asking: is it one user or everyone? One user — that rules out the server itself for now, so I'm looking at the client and the path. I'm checking the physical layer first because it's cheapest to rule out: cable, port, can they reach anything else? They can reach the intranet — so L1/L2 and their local stack are fine, and it's specific to the share. Next I'd check name resolution versus the share itself: can they ping the server by name? By IP? If IP works but the name doesn't, it's DNS. If both work but the share fails, I'm looking at SMB and permissions — and I'd check whether their password recently changed, because cached credentials cause exactly this. At each step I'm ruling out a layer before moving deeper, so I don't chase three hypotheses at once."

What the interviewer heard: blast-radius discipline, layered method, cheapest-test-first, a specific gotcha (cached credentials), and hypothesis control. That's 4/4 on methodology even before the diagnosis lands.

Scenario (b) GPO: narrate the gpresult-first method from FT02-W02. Scenario (c) VM lost network: narrate the virtual-switch check (external/internal/private), then the guest's network config — "the most common cause after a change is the change itself, so I'm looking at what moved." Always narrate *why this check before that one*."""),

N("Round 4: behavioral delivery — worked example",
"""15 minutes, 5 answers: 3 STAR stories + "why ThreatLocker" + "why hire you." By round 4 you're tired — that's the test. Tactics:

- **Lead with your strongest story.** Don't save it. A strong first answer sets the interviewer's pen moving in the right direction.
- **The stories are already built (FT03).** Round 4 is delivery, not invention. If you catch yourself inventing, stop — tell a real one again from a different angle.
- **"Why ThreatLocker" and "why hire you" are closers.** End each with the forward link: "...which is why I'm here" / "...evaluate me on trajectory."

Worked example — "Why should we hire you over a more experienced candidate?" (the hardest 60 seconds of the day):
> "I won't pretend to have years I don't have — so here's the honest case. What I offer is trajectory: I learn systems end-to-end instead of memorizing steps, I document everything, and I prepare obsessively — this interview is the evidence. I enrolled in your Zero Trust bootcamp on September 30th, I've spent six days in structured prep, and I can whiteboard a VM build, narrate a file-share triage, and defend the default-deny model right now, cold. You'd be hiring someone with no bad habits to unlearn and a demonstrated slope. I'm asking to be evaluated on that."

Score it: honesty without apology (✓), specific dated evidence (✓), demonstration offer (✓), forward framing (✓) → 3/3. Then stop. The biggest round-4 failure is the ramble-after-the-answer — when you're done, you're done."""),

N("Scoring yourself honestly + the re-take loop — worked example scorecard",
"""Score immediately after each round. The rubric, per question: 0 wrong/silent, 1 vague, 2 correct, 3 correct + evidence. Round pass marks: R1 ≥17/24, R2 ≥17/24, R3 ≥25/36, R4 ≥11/15.

Worked example — a filled R1 scorecard:
| # | Question | Score | Note |
|---|---|---|---|
| 1 | Build a VM? | 3 | Steps + whiteboard offer, 85s |
| 2 | GPO not applying? | 2 | Method right, no evidence anchor |
| 3 | TCP vs UDP? | 2 | Correct, rushed the examples |
| 4 | Checkpoint vs backup? | 3 | "Checkpoint is NOT a backup" landed |
| 5 | Zero Trust plain language? | 1 | Rambled, no skeleton, 2 min+ |
| 6 | EDR flag? | 2 | Missed "preserve evidence" |
| 7 | Subnetting for a manager? | 1 | Jargon dump, no analogy |
| 8 | Why ThreatLocker? | 3 | Conviction + bootcamp date |
| Total | | 17/24 | PASS — but 5 and 7 are re-take targets |

The re-take loop (same day, non-negotiable):
1. **Isolate:** only the sub-pass questions (here: #5, #7, plus #2's missing anchor, #6's missed step).
2. **Targeted study:** 30 minutes on exactly those — rewrite using verdict → method → evidence → close.
3. **Re-take:** re-answer just those four, aloud, timed. All must hit 2+.
4. **Log it:** write the date, the round, the weak questions, and what fixed them. This log is your trajectory evidence — and it kills the anxiety of "am I actually improving?" because the numbers say so.

Rule: a failed round re-taken the same day counts double in your confidence. A failed round postponed counts zero."""),
]

FT04_CARDS_ADD = [
C("R1 phone tactics", "Number structure aloud · verdict first · name the nouns (gpresult, repadmin, VHDX) · end with an offer to go deeper."),
C("R2 talk skeleton", "Problem (1) → approach (2) → demo (4) → trade-offs (2) → questions. Finish at 9 min, not 11."),
C("R3 narration template", "'I'm checking X first because [reason]. That tells me whether to go to Y or Z.' Methodology they can hear."),
C("R4 order", "Strongest story first. Stories from FT03 — delivery, not invention. Closers end with the forward link."),
C("The ramble-after-the-answer", "Round 4's biggest failure. When you're done, you're done. Stop talking."),
C("R1 pass mark", "≥17/24 across 8 questions. 0 wrong/silent · 1 vague · 2 correct · 3 correct + evidence."),
C("R2 pass mark", "≥17/24: clarity 6 + accuracy 6 + questions 6 + time 6."),
C("R3 pass mark", "≥25/36: methodology 4 + diagnosis 4 + communication 4 per scenario × 3."),
C("R4 pass mark", "≥11/15: 0–3 per answer on structure, honesty, evidence."),
C("Re-take loop", "Isolate weak questions → 30 min targeted study → re-answer aloud → log the fix. Same day."),
]

FT04_QUIZ = [
Q("In Round 1 (phone screen), why do you number your structure aloud?",
  ["It sounds smart", "No whiteboard or body language — numbering keeps you from rambling and signals organized thinking through audio alone",
   "Interviewers require it", "It fills time"],
  1, "Voice is the entire signal on a phone screen; structure must be audible.", 0),
Q("Your Round 2 talk runs 13 minutes. What is the scoring consequence?",
  ["None — more content is better", "Time discipline is 6 of 24 points; finishing at 9 beats rambling to 13. Cut to fit.",
   "They'll stop you politely", "It shows enthusiasm"],
  1, "Time discipline is scored. Finish early rather than ramble.", 1),
Q("In Round 3, you reach the right diagnosis silently, then announce it. What did you lose?",
  ["Nothing — the answer is right", "Methodology points: interviewers score the thinking they can hear. Narrate why this check before that one.",
   "Time", "Confidence"],
  1, "The meta-skill is audible methodology, not silent correctness.", 2),
Q("Round 4, you're tired and inventing details in a story. What is the correct recovery?",
  ["Keep going — they won't notice", "Stop. Tell a real story again from a different angle. Invention is detectable and fatal.",
   "Blame fatigue", "Ask for water and stall"],
  1, "Delivery, not invention. Consistency reads as depth.", 3),
Q("Your R1 scorecard totals 15/24. What happens next?",
  ["Move on — close enough", "Same-day re-take loop: isolate weak questions → 30 min targeted study → re-answer aloud → log the fix",
   "Retake the whole bank", "Blame the questions"],
  1, "Below pass mark → targeted re-take the same day. Non-negotiable.", 4),
Q("What is the single highest-leverage line in the VM-build answer?",
  ["The Hyper-V version number", "'I can whiteboard the whole flow right now if you'd like' — converts verbal to demonstration",
   "The RAM amount", "The ISO filename"],
  1, "The whiteboard offer is the power move interviewers remember.", 5),
Q("Why do rounds run back-to-back with only 5-minute breaks?",
  ["To save time", "Simulates interview fatigue — round 4 is where unprepared candidates collapse. Train tired.",
   "It's traditional", "No reason"],
  1, "Performance under fatigue is a separate skill. Train it deliberately.", 6),
Q("A follow-up question exposes a gap in your Round 2 talk. What scores best?",
  ["Bluff through it", "'Good challenge — here's how I'd think about it...' then reason aloud from the model. Honesty + method.",
   "Say 'next question'", "Repeat the talk"],
  1, "Handling questions is 6 of 24 points in R2. Reason aloud; never bluff.", 7),
Q("What does the re-take log give you beyond the scores?",
  ["Nothing", "Trajectory evidence — dated proof you're improving, which kills 'am I actually getting better?' anxiety",
   "Extra credit", "A diary"],
  1, "The log turns feelings into numbers. Numbers compound confidence.", 8),
]

FT04_DRILLS = [
D("ft04-drill-r1", "Round 1 simulation — 8 sampled, timed", [
("Sample 8 FT02 questions (mix reported + likely). 90s each, aloud, recorded.",
 "Score 0–3 each; pass ≥17/24. Number structure aloud, verdict first, name the nouns.",
 "No cherry-picking — random sample only."),
("Re-answer every 0–1 immediately with verdict → method → evidence → close.",
 "All re-answers must hit 2+.", "Same-day re-take rule."),
]),
D("ft04-drill-r3", "Round 3 think-aloud — 3 scenarios", [
("Scenario (a): user can't reach the file share. 10 min, narrate everything.",
 "Blast radius → layered method (physical → name resolution → SMB/permissions) → hypothesis control. Methodology audible.",
 "If you went silent for >30s, you failed the narration — redo."),
("Scenario (b): GPO not applying. 10 min.", "gpresult-first narration: scope → filtering → inheritance → replication.", "Say why each check comes before the next."),
("Scenario (c): VM lost network after a change. 10 min.", "'The most common cause after a change is the change itself' → vSwitch type → guest config.", "Change-aware triage."),
]),
D("ft04-drill-r2r4", "Round 2 talk + Round 4 closers", [
("Deliver the 10-min hardening talk. Time it.",
 "Problem → approach → demo → trade-offs → questions. Finish ≤10 min; target 9.", "Record and check: did you ramble?"),
("Deliver 'why hire you' in 60s. Cold, no warm-up.",
 "Honest junior + dated evidence + demonstration offer + forward link. Then STOP — no ramble-after.", "The stop is part of the drill."),
]),
]

FT04_LAB = LAB(
"ft04-lab-mockday",
"Full mock day — four rounds, scored",
"Run all four rounds back-to-back with 5-minute breaks, score each immediately, and execute the same-day re-take loop on every sub-pass round.",
["Set up: quiet room, phone recording, printed scorecards, FT02 bank + 3 R3 scenarios + R2 talk outline.",
 "Round 1 (20 min): 8 sampled FT02 questions, 90s each, aloud. Score immediately.",
 "5-min break. Round 2 (30 min): 10-min hardening talk + 20 min FT02 follow-ups. Score.",
 "5-min break. Round 3 (30 min): 3 scenarios × 10 min, thinking aloud. Score.",
 "5-min break. Round 4 (15 min): 3 STAR stories + why ThreatLocker + why hire you. Score.",
 "Tally: every round at/above pass mark? For any round below: 30-min targeted study, re-take weak questions same day.",
 "Log: date, round scores, weak questions, what fixed them."],
"Four completed scorecards + re-take log with every round at pass mark.",
"All four rounds ≥ pass marks after re-takes; recordings exist for every round; log is written.")

FT04_RES = [
RES("Windows Server documentation", "https://learn.microsoft.com/en-us/windows-server/", "docs"),
RES("PowerShell documentation", "https://learn.microsoft.com/en-us/powershell/", "docs"),
]

FT["IL27-FT04"] = {
    "notes": FT04_NOTES, "cards_add": FT04_CARDS_ADD, "quiz": FT04_QUIZ,
    "drills": FT04_DRILLS, "handsOnLab": FT04_LAB,
    "supplementalResources": FT04_RES, "videos": [],
    "estimatedMinutes": 300,
}

# ---- FT04 branching scenarios (course-level) ----
BRANCH_FT04 = [
{
 "id": "IL27-BRANCH-FT04-01",
 "moduleId": "IL27-FT04",
 "title": "The follow-up probe: when your answer is thin",
 "start": "probe1",
 "nodes": {
  "probe1": {"text": "You answered 'What is Zero Trust?' with the definition. The interviewer leans in: 'Okay — but we've heard the definition from everyone today. Tell me about a time you actually applied a Zero Trust idea, even in a homelab.'",
   "choices": [
    {"label": "Freeze and repeat the definition with different words.", "feedback": "The interviewer nods politely and moves on. You've confirmed their suspicion: recitation, not understanding. Score: 1/3 for the exchange.", "next": "end_weak"},
    {"label": "Pivot to a real example: 'In my homelab I removed standing admin rights — separate admin accounts, and I review who has what quarterly. That's least privilege, which is the identity half of Zero Trust.'", "feedback": "The interviewer's pen moves. 'Good — how did you handle the pushback when something needed admin?' They're giving you rope — take it.", "next": "probe2"},
    {"label": "Bluff: 'Oh yeah, I implemented full Zero Trust at enterprise scale.'", "feedback": "Fatal. A security company's interviewers detect invented scale instantly, and everything after is scored as untrustworthy. Never do this.", "next": "end_fatal"}]},
  "probe2": {"text": "'How did you handle the pushback when something needed admin?'",
   "choices": [
    {"label": "'I just said no — security first.'", "feedback": "Honest but rigid. Better: offer the narrow alternative. Score for the exchange: 2/3.", "next": "end_ok"},
    {"label": "'I'd grant it temporarily with a ticket, a time limit, and a review — say no to standing access, yes to just-in-time with an audit trail.'", "feedback": "That's the senior answer: least privilege with operational empathy. The interviewer writes something down. Score: 3/3 for the exchange.", "next": "end_strong"},
    {"label": "'I'd escalate to my manager.'", "feedback": "Reasonable in an enterprise, but it surrenders the judgment call. For a junior role it's acceptable; it doesn't stand out. Score: 2/3.", "next": "end_ok"}]},
  "end_weak": {"text": "Exchange over. Lesson: when probed past the definition, the only move is a real example — even a small one. Rehearse one applied-Zero-Trust story before mock day.", "choices": []},
  "end_ok": {"text": "Exchange over. Solid 2/3 — honest and reasonable. To reach 3/3, add the mechanism: just-in-time access with audit trail beats both blanket-no and escalation.", "choices": []},
  "end_strong": {"text": "Exchange over — 3/3. You turned a probe into a demonstration: real example, then a principled mechanism under follow-up. That's the fluency the bank trains.", "choices": []},
  "end_fatal": {"text": "Exchange over. The bluff poisons the whole interview. Rule restated: never invent scale, employers, or experience. Re-read FT03 note 2.", "choices": []}
 }},
{
 "id": "IL27-BRANCH-FT04-02",
 "moduleId": "IL27-FT04",
 "title": "The whiteboard VM build — follow-ups branch",
 "start": "wb1",
 "nodes": {
  "wb1": {"text": "You whiteboarded the Hyper-V VM build cleanly. The interviewer points at your virtual switch box: 'You drew an external switch. What breaks if I change it to private right now, and how would you know?'",
   "choices": [
    {"label": "'The VM would lose external network access. I'd know because the guest can't reach the gateway — I'd verify with ping tests from inside the guest.'", "feedback": "Correct and verifiable. The interviewer nods: 'And the host?'", "next": "wb2"},
    {"label": "'Nothing — the switch type doesn't matter.'", "feedback": "Wrong, and it's a core concept. The interviewer moves on, but the miss is logged. Re-study FT02-V05.", "next": "end_miss"},
    {"label": "'I'd have to look that up.'", "feedback": "Honest, but this one is core — vSwitch types are day-one virtualization knowledge. Better to reason it out: private = VM-to-VM only, so external access dies.", "next": "end_miss"}]},
  "wb2": {"text": "'And the host?'",
   "choices": [
    {"label": "'The host keeps its own physical NIC connectivity — the vSwitch change only affects the virtual network. But I'd double-check I didn't bind the management OS in a way that depended on that switch.'", "feedback": "Excellent — you separated the virtual network from the host's physical path AND flagged the management-OS binding edge case. That's senior-shaped thinking. 3/3.", "next": "end_strong2"},
    {"label": "'The host loses network too.'", "feedback": "Not quite — the host's physical NIC is independent of the virtual switch topology. Close, but the distinction matters. 2/3.", "next": "end_ok2"}]},
  "end_miss": {"text": "Branch over. vSwitch types (external/internal/private) are high-probability follow-ups after any VM question — lock in FT02-V05 before mock day.", "choices": []},
  "end_ok2": {"text": "Branch over. Good instinct to reason it out — now lock the precise distinction: host physical path vs virtual topology.", "choices": []},
  "end_strong2": {"text": "Branch over — 3/3. You demonstrated layered thinking: answer, then the edge case, unprompted. That's what 'correct + evidence' looks like under follow-up.", "choices": []}
 }}
]

# ================================================================= FT05 ===
FT05_NOTES = [
N("Why logistics win interviews before they start",
"""Interviews are scored from the first handshake. A candidate who arrives flustered, late, or digging through a bag for a resume starts at a deficit no technical answer fully erases. Logistics are the only part of the interview you control completely — so control them completely.

The psychology, briefly: interviewers are pattern-matching for "can I trust this person with my infrastructure?" Punctuality, preparation, and composure are *evidence* of operational discipline — the same discipline that prevents outages. When you arrive 20 minutes early with printed resumes and a calm demeanor, you've already answered "are you reliable?" before the first question.

The corollary: no amount of logistics saves bad answers. FT05 doesn't replace FT01–FT04 — it protects the investment you made in them. Think of it as the change-management wrapper around the technical deployment: the deployment (your knowledge) only lands if the change window (the day) is executed cleanly."""),

N("Day-before walkthrough with rationale",
"""Each day-before item exists for a reason. Walk it with the reasoning attached:

1. **Confirm the address from the invitation email.** See the location note below — there are two candidate addresses. The invitation is the authority. Map the route; drive it if possible. (Rationale: navigation failure is the #1 preventable cause of lateness.)
2. **Print 5 copies of your resume on clean paper + one-page portfolio summary** (homelab builds, bootcamp enrollment Sept 30, cert track). (Rationale: interviewers share resumes; handing a crisp copy to each person signals preparation. The portfolio summary is your evidence sheet — it does the bragging so you don't have to.)
3. **Lay out professional attire; pack the bag** (resumes, portfolio summary, notebook + pen, photo ID, references list, phone charger, water). (Rationale: every item packed tonight is one decision you don't make under morning adrenaline.)
4. **Light review only: the 9 reported questions + 6 STAR stories, once. No cramming after 8 PM.** (Rationale: cramming the night before degrades sleep, and sleep is performance. You prepared for six days; trust the work.)
5. **Two alarms. Sleep by 10:30 PM.** (Rationale: a single alarm is a single point of failure. You of all people should know better — no SPOFs.)

The theme: eliminate morning decisions, eliminate single points of failure, protect sleep. You're applying infrastructure discipline to yourself."""),

N("Day-of minute-by-minute — the reasoning",
"""```
06:30  Wake, no snooze. Protein breakfast; no excess caffeine.
         → Snooze fragments sleep inertia; protein sustains, caffeine spikes then crashes.
07:00  Final review: 60-sec "why ThreatLocker", VM-build walkthrough, one STAR story.
         Then STOP studying.
         → Three reps, not thirty. The stop is the discipline — it signals trust in prep.
07:45  Depart with 30+ minutes buffer. Orlando morning traffic is real.
         → Buffer absorbs the unexpected; arriving stressed undoes the calm you built.
08:35  Arrive. Check in calmly; breathe; review one-page cheat sheet once, then put it away.
         → Early arrival = composure. The cheat sheet goes away before you're called —
            being seen studying in the lobby reads as under-prepared.
09:00  Interview. Think aloud, anchor to real experience, hold the honesty line.
         → Everything FT01–FT04 trained. Execute the plan.
After  Thank-you note within 2 hours, referencing something specific from the conversation.
         → Specificity proves you listened; speed proves you care.
```

Worked example — the 07:00 review, exactly: stand up, phone timer, deliver "why ThreatLocker" (45s), the VM-build walkthrough (90s), S4 homelab migration (2 min). Total under 5 minutes. Then close the materials. If your brain screams "one more topic!" — that's anxiety, not a gap. The six days were the preparation; the morning is the performance."""),

N("Location verification protocol",
"""Plan anchor: **1950 W Maitland Blvd, Orlando** — per the interview invitation details provided. This is the address you navigate to.

The conflict you must resolve: ThreatLocker's public listings show its headquarters at **1950 Summit Park Drive, Orlando, FL 32810**. Two addresses, one company. The protocol:

1. **The invitation email is the authority.** Re-read it the night before. If it says Maitland Blvd, you go to Maitland Blvd.
2. **If the invitation is ambiguous**, check the Calendly confirmation (booked via Crawford Thomas / Alex Starr) — it should restate the location.
3. **If still ambiguous**, email Alex Starr the day before: "Confirming tomorrow's 9:00 AM interview location — 1950 W Maitland Blvd?" One short email beats driving to the wrong building.
4. **Have both addresses in your maps app.** If you arrive and the building looks wrong, you have the fallback ready without panic.

Worked example — the drive-by: the night before, you map 1950 W Maitland Blvd, note the parking situation on satellite view, and save 1950 Summit Park Drive as a second pin labeled "HQ fallback." Morning-of, you drive to the invitation address. Total extra effort: 4 minutes. Total risk removed: arriving at the wrong building for a 9:00 AM interview.

Never assume. Verify. This is the same discipline as verifying backups before a migration — the stakes are just more visible."""),

N("The 5-minute reset + the 'I don't know' protocol",
"""Two micro-skills for the waiting room and the hot seat.

**The 5-minute reset** (in your car or the lobby, before you're called):
1. Arrive → 2. Breathe: 4 counts in, 6 out, 3 rounds → 3. Recall one STAR story (your strongest — S4 or S1) → 4. Say to yourself: "trajectory, preparation, honesty" → 5. Walk in.

The breathing isn't mysticism — it down-regulates the adrenaline spike so your prefrontal cortex (the part that answers technical questions) stays online. The story recall puts you in "I have evidence" mode instead of "I hope they go easy" mode. The three words are your identity anchor for the day.

**The 'I don't know' protocol** — because you *will* get a question you can't answer, and how you handle it is scored:
> "I haven't hit that in production yet. Here's how I'd figure it out: [method]."

Worked example. Question: "How would you configure ThreatLocker's Network Control for a multi-site deployment?" (You don't know their console.) Weak: bluffing about console screens you've never seen — fatal at a security company. Strong: "I haven't worked in the console itself — my knowledge is from your public platform materials. Here's how I'd approach it from first principles: I'd start by mapping what each site's endpoints need to reach, default-deny everything else, and build the policy in monitor mode before enforcing, so I can see what would break before it breaks. And I'd lean on your team's console expertise for the click-path — I'm here to learn the tool, I already understand the model."

Honesty + method + forward lean. That's a 2/3 on a question you couldn't answer — which beats the 0/3 (plus trust damage) of a bluff, every time."""),

N("After: the thank-you note — worked example",
"""Send within 2 hours of leaving. Email to the interviewer(s) — via Alex Starr at Crawford Thomas if you don't have direct addresses. Three sentences, one specific reference.

Worked example:
> Subject: Thank you — IT Infrastructure Specialist interview
>
> [Name], thank you for the conversation this morning. I particularly enjoyed the discussion about [something specific — e.g., "how your team thinks about default-deny in practice" or "the troubleshooting scenario you walked me through"] — it confirmed what drew me to ThreatLocker in the first place.
>
> I'm excited about the possibility of contributing to the team. Please let me know if there's anything else I can provide.
>
> Best, Enmanuel Mejia · (617) 299-0781 · mejiaenmanueld@gmail.com

Why it works: the specific reference proves you were present and listening (most thank-yous are generic). The contact block makes follow-up frictionless. What it doesn't do: beg, grovel, or re-litigate answers you wish you'd nailed — never "by the way, what I meant to say about subnets was..."

Then: log the interview while it's fresh — who you met, what they asked, what you'd improve. That log is gold whether there's a second round or a next opportunity."""),
]

FT05_CARDS_ADD = [
C("Night-before SPOF check", "Two alarms. Bag packed. Address verified from invitation. Attire laid out. No single points of failure — you're infrastructure people."),
C("The 07:00 review — exactly", "Why ThreatLocker (45s) → VM build (90s) → one STAR story (2 min). Then STOP. The stop is the discipline."),
C("Arrival protocol", "08:35–08:40. Check in calmly. Cheat sheet once, then away — being seen studying reads as under-prepared."),
C("Location authority order", "1. Invitation email 2. Calendly confirmation 3. Ask Alex Starr. Never assume; Maitland Blvd is the plan anchor."),
C("The reset (5 min)", "Breathe 4-in/6-out ×3 → recall strongest story → 'trajectory, preparation, honesty' → walk in."),
C("'I don't know' script", "'I haven't hit that in production yet. Here's how I'd figure it out: [method].' Honesty + method > bluff."),
C("Thank-you timing", "Within 2 hours. 3 sentences. One specific reference. Contact block. Never re-litigate answers."),
C("What to bring — memory check", "5 resumes · portfolio summary · notebook+pen · photo ID · references · charger · water · calm."),
C("Phone discipline", "Silent before entering the building, not after sitting down."),
C("Blood sugar rule", "Eat before you go. Low blood sugar ruins more interviews than hard questions."),
]

FT05_QUIZ = [
Q("The invitation says 1950 W Maitland Blvd but public listings show 1950 Summit Park Drive. What do you do?",
  ["Go to Summit Park — it's the HQ", "Treat the invitation as authoritative; verify against Calendly; if ambiguous, email Alex Starr the day before; keep both addresses pinned",
   "Pick whichever is closer", "Call ThreatLocker's main line repeatedly"],
  1, "Invitation is the authority; verify, don't assume. Two pins, zero panic.", 0),
Q("It's 8 PM the night before. You feel under-prepared on subnetting. What do you do?",
  ["Cram until 1 AM", "Light review once, then stop — sleep is performance; six days of prep beats one night of panic",
   "Skip sleep entirely", "Cancel the interview"],
  1, "No cramming after 8 PM. Trust the work; protect sleep.", 1),
Q("You're seen studying your cheat sheet in the lobby when they call your name. Why is this bad?",
  ["It isn't", "Being seen studying reads as under-prepared — review once at 08:35, then put it away before you're called",
   "Cheat sheets are banned", "They'll quiz you on it"],
  1, "Composure is scored from the first handshake. The sheet goes away early.", 2),
Q("An interviewer asks about a console workflow you've never used. What scores best?",
  ["Bluff the click-path", "'I haven't worked in the console — my knowledge is from your public materials. Here's how I'd approach it from first principles...' + method + forward lean",
   "'Next question please'", "Go silent"],
  1, "Honesty + method + 'I'm here to learn the tool, I understand the model.' 2/3 on an unanswerable beats 0/3 + trust damage.", 3),
Q("What are the three non-negotiable night-before items?",
  ["New shoes, cologne, gum", "Address verified from invitation + bag packed + two alarms — eliminate morning decisions and single points of failure",
   "Memorize 60 answers", "Watch more videos"],
  1, "Infrastructure discipline applied to yourself: no SPOFs, no morning decisions.", 4),
Q("The thank-you note should include which specific element?",
  ["A re-answered technical question", "One specific reference to the conversation — proves you listened; plus contact block",
   "Your salary requirements", "A joke"],
  1, "Specificity proves presence. Never re-litigate answers in the thank-you.", 5),
Q("Why 30+ minutes of buffer for a 20-minute drive?",
  ["Paranoia", "Buffer absorbs the unexpected; arriving stressed undoes the composure you built all week",
   "To sightsee", "No reason"],
  1, "Composure is the product; buffer is how you manufacture it.", 6),
Q("Your 07:00 review runs 25 minutes and you're still studying at 07:45. What broke?",
  ["Nothing — more prep is better", "The stop discipline: 3 reps (why ThreatLocker, VM build, one story), then close the materials. The morning is performance, not preparation.",
   "You woke up late", "The material is too hard"],
  1, "'One more topic' at 07:45 is anxiety, not a gap. Execute the plan.", 7),
Q("Phone rings mid-interview. What should you have done?",
  ["Answer it — might be important", "Silent BEFORE entering the building. Not after sitting down.",
   "Apologize and continue", "Blame the carrier"],
  1, "Pre-building silence is the discipline. Mid-interview ringing is a composure hit.", 8),
]

FT05_DRILLS = [
D("ft05-drill-pack", "Pack from memory — the bag drill", [
("List everything in the interview bag from memory.",
 "5 resumes · portfolio summary · notebook + pen · photo ID · references list · phone charger · water bottle · calm preparation.",
 "Missed one? Pack it now, re-drill tomorrow."),
("Recite the day-of timeline with times.", "06:30 wake → 07:00 review (then stop) → 07:45 depart → 08:35 arrive → 09:00 interview → thank-you within 2h.", "Times are the skeleton; rationale is the muscle."),
]),
D("ft05-drill-reset", "The reset + the unknown — aloud", [
("Run the 5-minute reset aloud, real-time.", "Breathe 4-in/6-out ×3 → recall S4 → 'trajectory, preparation, honesty' → walk in.", "Do it physically, not mentally."),
("Deliver the 'I don't know' script on a hard question.", "'I haven't hit that in production yet. Here's how I'd figure it out: [method].' Then give the method.", "Method is what makes it 2/3 instead of 1/3."),
("Deliver the 60-second 'why ThreatLocker' cold. Time it.", "Conviction + bootcamp Sept 30 + infrastructure framing. ≤60s.", "Cold = no warm-up. That's the condition you'll face."),
]),
D("ft05-drill-location", "Location verification — dry run", [
("State the plan anchor address and the verification order.", "1950 W Maitland Blvd, Orlando. Invitation → Calendly → ask Alex Starr.", "Invitation is the authority."),
("What do you do if the building looks wrong on arrival?", "Check the HQ fallback pin (1950 Summit Park Drive) — saved last night, no panic.", "Two pins, zero panic."),
]),
]

FT05_LAB = LAB(
"ft05-lab-rehearsal",
"Interview-day dress rehearsal",
"Run the full day-before checklist and a timed morning routine end-to-end, the day before the interview. Timestamp everything.",
["Verify the address from the invitation email; save both addresses as map pins.",
 "Print 5 resumes + one-page portfolio summary; lay out attire; pack the bag from the memory drill.",
 "Set two alarms for 06:30.",
 "Timed dry run: deliver the 07:00 review set (why ThreatLocker, VM build, one story) — confirm ≤5 min total, then stop.",
 "Run the 5-minute reset physically. Note how it feels; adjust the breathing counts if needed.",
 "Draft the thank-you note template with blanks for the specific reference; save as a draft.",
 "Lights out by 22:30. Log completion with timestamps."],
"Timestamped checklist: every item done, bag packed, alarms set, drafts saved.",
"Zero unchecked items; 07:00 set ≤5 min; in bed by 22:30.")

FT05_RES = [
RES("Map: 1950 W Maitland Blvd, Orlando FL", "https://www.google.com/maps/search/?api=1&query=1950+W+Maitland+Blvd+Orlando+FL", "map"),
RES("ThreatLocker careers", "https://www.threatlocker.com/careers", "vendor"),
]

FT["IL27-FT05"] = {
    "notes": FT05_NOTES, "cards_add": FT05_CARDS_ADD, "quiz": FT05_QUIZ,
    "drills": FT05_DRILLS, "handsOnLab": FT05_LAB,
    "supplementalResources": FT05_RES, "videos": [],
    "estimatedMinutes": 120,
}

# ---- FT05 click sim (course-level) ----
CLICK_FT05 = {
 "id": "IL27-CLICK-FT05-01",
 "moduleId": "IL27-FT05",
 "tool": "Interview-day logistics rehearsal",
 "title": "Interview-day logistics rehearsal — step by step",
 "steps": [
  "Night before, 20:00 — Open the invitation email. Read the location line twice. Confirm: 1950 W Maitland Blvd, Orlando. If ambiguous, check the Calendly confirmation.",
  "Night before, 20:10 — Save both addresses as map pins: 'Interview — Maitland Blvd' and 'HQ fallback — Summit Park Drive'. Check parking on satellite view.",
  "Night before, 20:30 — Print 5 resumes on clean paper. Print the one-page portfolio summary (homelab builds, bootcamp enrolled Sept 30, cert track).",
  "Night before, 21:00 — Pack the bag: resumes, portfolio summary, notebook + pen, photo ID, references list, phone charger, water bottle. Lay out attire.",
  "Night before, 22:00 — Set TWO alarms for 06:30. Phone on charge. Lights out by 22:30 — no cramming after 20:00.",
  "Interview day, 06:30 — Wake, no snooze. Protein breakfast; coffee normal amount, not triple.",
  "Interview day, 07:00 — Final review, timed: 'why ThreatLocker' (45s), VM-build walkthrough (90s), one STAR story (2 min). Then CLOSE the materials.",
  "Interview day, 07:45 — Depart with 30+ minutes buffer. Phone on silent BEFORE entering the building.",
  "Interview day, 08:35 — Arrive. Check in calmly. Breathe (4-in/6-out ×3). Review cheat sheet once, then put it away.",
  "Interview day, 09:00 — Interview. Think aloud, anchor to real experience, hold the honesty line.",
  "After, within 2 hours — Send the thank-you note with one specific reference from the conversation."
 ]
}

# ================================================================= FT06 ===
FT06_NOTES = [
N("The no-promise framing — read this first",
"""No hiring promise is made or implied by this module, this course, or your preparation. You are preparing to *handle* an offer professionally if one comes — not expecting one. That distinction matters for two reasons:

1. **Desperation leaks.** Candidates who act like the offer is certain (or desperately needed) negotiate badly and interview anxiously. The mindset is: "I'm preparing for every outcome, including a no — and a no just means the next rep."
2. **The screening is real either way.** Public postings describe a background check and drug/substance screening after a conditional offer. Being ready for that step is professionalism, not presumption.

Worked mindset check — say these aloud and mean them:
- "My preparation earns me the best possible performance. The outcome is not mine to control."
- "If the answer is no, I keep the thank-you, the log, and the reps — and I go again."
- "If the answer is yes, I evaluate calmly, not euphorically."

This module is the 30/60/90 plan, the offer evaluation worksheet, and the screening prep. Professional handling of success is a skill — train it like the rest."""),

N("Evaluating an offer: total compensation — worked example",
"""Never accept on the spot from excitement. Take the full decision window. Evaluate *total* compensation, not just salary:

**Worked example — the evaluation worksheet (fill with real numbers when the offer comes):**
```
Base salary:            $______ /yr        (your stated target: $90,000)
Bonus / variable:       $______            (ask: is it guaranteed or target-based?)
Health insurance:       $______ /mo employee cost  (ask: what plan, what deductible?)
PTO / holidays:         ______ days        (ask: accrual vs lump, rollover?)
Retirement match:       ______ %           (ask: vesting schedule?)
Training/cert budget:   $______ /yr        (ask explicitly — funds your Security+/AZ path)
On-call expectations:   ________________   (ask: rotation, compensation, frequency)
Growth path:            ________________   (ask: what does year 2 look like?)
Start date flexibility: ________________
```

**The questions to ask (in writing, before deciding):**
- "Can you confirm the role scope — title, team, primary responsibilities, on-call expectations?"
- "What does the certification and training support look like?" (Signals growth culture AND funds your path.)
- "What is the decision timeline on your side?" (Gives you the window without seeming hesitant.)

**Red flags that warrant a pause:** pressure to decide same-day, scope that shifts between conversations, unwillingness to put the offer in writing, on-call described as "occasional" with no rotation defined. None of these are accusations — they're clarifications you request calmly, in writing.

Worked example — the stall, done gracefully: "Thank you — I'm excited about this. I want to give it the careful consideration it deserves; can I confirm by [date]?" Professional, unhurried, respectful of both sides."""),

N("Negotiation scripts for a junior candidate — worked examples",
"""Junior candidates can negotiate — the leverage is *competing optionality and demonstrated value*, not years. Three scripts:

**Script 1 — the number is below target:** "Thank you for the offer. Based on my research for infrastructure specialist roles in Orlando and the preparation I've invested in your stack specifically, I was targeting closer to $90,000. Is there flexibility to bridge that gap?" (Calm, researched, specific number. Then *stop talking* — silence is the negotiation tool.)

**Script 2 — the number is fine but growth matters:** "The base works for me. What I'd love to understand is the growth path — what does progression look like in the first 18 months, and is there training budget for the Security+ and AZ-800 I'm pursuing?" (Trades salary pressure for career capital — often easier for them to say yes to.)

**Script 3 — they say the number is firm:** "I understand. Two things would make this an easy yes: [training budget / start date / PTO day]. Are any of those flexible?" (When salary is fixed, negotiate the package around it.)

**Rules:**
- Everything material in writing before you accept. Verbal promises evaporate.
- Never lie about competing offers. ("I have another offer at $X" when you don't is detectable and destroys trust.)
- Your stated desired salary ($90,000/yr, from your applications) is your anchor — don't negotiate against yourself by naming a lower number first.
- One round of negotiation is normal; three rounds is adversarial. Ask once, well."""),

N("Screening prep: what the public postings describe",
"""ThreatLocker's publicly posted roles describe a **background check and drug/substance screening after a conditional offer**. This is their standard process — expect it, don't fear it. Preparation:

1. **Keep a valid photo ID ready** — the same ID you bring to the interview.
2. **Ensure your references are warned and reachable.** Call them *before* the offer: "You may get a reference check from ThreatLocker/Crawford Thomas in the next two weeks — are you still good to speak for me?" A surprised reference is a weak reference.
3. **Keep your documented history consistent** with what you stated in interviews — dates, titles, bootcamp enrollment (Sept 30, *enrolled*). Inconsistency between interview statements and screening forms is the #1 self-inflicted wound.
4. **Disclose proactively if asked.** If a form asks about anything in your history, answer truthfully and briefly. The screening verifies; it doesn't interrogate — unless you give it a reason to.

Worked example — the reference warning call (do this now, before any offer): "Hi [Name] — quick heads-up: I'm in final stages for an IT Infrastructure Specialist role at ThreatLocker in Orlando. If they call, they'd ask about [reliability / technical ability / character]. Still comfortable speaking for me? I'll send you the role description so you're not blindsided." Two minutes, massive difference in reference quality.

Timeline note: screening happens *after* a conditional offer — it is not part of the interview day. Don't bring it up unprompted in the interview; handle it when the offer letter arrives."""),

N("The 30/60/90 plan — worked example (his actual plan)",
"""Write this on one page. Bring it if a final-round conversation invites it — unprompted is fine only if the moment fits ("What would your first 90 days look like?" is the invitation; don't force it).

**Days 1–30: LEARN**
- Document the environment as you discover it — network map, AD structure, ticket queues, escalation paths. Your documentation habit is your onboarding superpower.
- Ask questions constantly; write down every answer. Nobody expects output in week one — they expect *absorption*.
- Complete compliance, security, and tooling onboarding without being chased.
- Shadow escalations. Take notes on how seniors triage — that's your real training.

**Days 31–60: CONTRIBUTE**
- Own L2 tickets end-to-end: triage → resolve → document → close. Become the person whose tickets don't bounce back.
- Propose one documentation improvement — the gap you found while learning. (Contributing docs in month two signals ownership.)
- Start Security+ study in earnest — 30 minutes a day, non-negotiable.

**Days 61–90: LEAD (something small)**
- Own a small infrastructure improvement end-to-end — a GPO cleanup, a monitoring gap closed, a runbook written.
- Present a 15-minute lunch-and-learn on something you learned (e.g., "What I learned about our ticketing patterns in 60 days").
- Have AZ-800 booked or Security+ scheduled. Certifications in flight prove the trajectory you sold in the interview.

Worked one-line version (the card): 30: learn the environment and document it. 60: contribute independently and start certifying. 90: lead something small and teach something back.

Why this plan wins: it's *specific* (not "learn the ropes"), it's *documented* (your differentiator), and every phase has a visible artifact. Interviewers don't just hear ambition — they hear execution."""),

N("First-week behaviors that earn trust — worked example",
"""The offer is signed. Now the real interview begins — the first two weeks, when everyone forms their permanent impression. Behaviors that earn trust fast:

1. **Write everything down, then share it.** Your day-3 network map draft, posted for correction, earns more trust than a month of silent competence. Seniors *love* juniors who document — it means they don't have to.
2. **Ask the question, then the follow-up.** "How do we handle this?" then "Why is it done that way?" The second question is what separates learners from ticket-closers.
3. **Close the loop visibly.** "You asked me to check X — here's what I found, here's the doc." Reliability is demonstrated in small completions, not grand promises.
4. **Learn names and roles in week one.** The fastest way to get help in month three is to have been genuinely curious in week one.
5. **Protect the honesty line forever.** "I don't know, but here's how I'd find out" works on day 5 exactly as well as it worked in the interview. The day you bluff at work is the day the interview honesty becomes a lie.

Worked example — the first-week win: On day 4, you notice the onboarding wiki's VPN setup steps are outdated (you just lived them). You update the page, note the change in the team channel, and move on. Cost: 20 minutes. Signal sent: this person improves the environment they touch, documents without being asked, and doesn't wait for permission to fix small things. That's the entire 30/60/90 plan in miniature — and it's how "junior" becomes "trusted" faster than tenure would predict."""),
]

FT06_CARDS_ADD = [
C("Mindset check (say aloud)", "'My preparation earns the best performance. The outcome isn't mine to control.' Desperation leaks; preparation doesn't."),
C("Offer worksheet — the 8 lines", "Base · bonus · health cost · PTO · 401k match + vesting · training budget · on-call terms · growth path."),
C("The graceful stall", "'Thank you — I'm excited. Can I confirm by [date]?' Never accept on the spot from excitement."),
C("Negotiation script 1 — below target", "'I was targeting closer to $90,000 based on Orlando infrastructure roles. Is there flexibility?' Then STOP TALKING."),
C("Negotiation script 2 — number's fine", "Trade salary pressure for career capital: growth path + training budget for Security+/AZ-800."),
C("Negotiation script 3 — firm number", "'Two things would make this an easy yes: [training budget/start date/PTO]. Any flexibility there?'"),
C("Everything in writing", "Verbal promises evaporate. Material terms confirmed in writing before acceptance."),
C("Reference warning — do it NOW", "Call references before any offer: role, what they'll be asked, send the description. Surprised = weak."),
C("Screening = standard process", "Background check + drug/substance screening after conditional offer, per public postings. ID ready, history consistent."),
C("30/60/90 one-liners", "30: learn + document. 60: contribute + start certifying. 90: lead something small + teach it back."),
C("First-week trust builders", "Document publicly · ask why, not just how · close loops visibly · learn names · never bluff."),
]

FT06_QUIZ = [
Q("The offer comes in below your target. What is the first move?",
  ["Accept immediately — don't risk it", "Take the full decision window; evaluate total comp on the worksheet; then negotiate once, well, with a specific number",
   "Counter with a random higher number", "Decline on the spot"],
  1, "Calm evaluation beats euphoric acceptance and panicked rejection alike.", 0),
Q("Which negotiation script fits when the base is acceptable but you want career growth?",
  ["Script 1 — demand more base", "Script 2 — trade salary pressure for growth path + training budget (Security+/AZ-800)",
   "Script 3 — walk away", "No script — accept silently"],
  1, "Career capital is often easier for them to grant than salary — and it compounds.", 1),
Q("They say the salary number is firm. What next?",
  ["Walk away", "Script 3: negotiate the package around it — training budget, start date, PTO. One round, well-aimed.",
   "Accept resentfully", "Threaten to decline"],
  1, "Fixed salary ≠ fixed package. Negotiate what moves.", 2),
Q("When do you warn your references?",
  ["After the background check starts", "NOW — before any offer: role, what they'll be asked, send the description",
   "Never — it's their problem", "Only if asked"],
  1, "A warned reference is a strong reference. Two-minute call, massive difference.", 3),
Q("What does 'everything in writing' protect you from?",
  ["Paperwork", "Verbal promises evaporating — scope, training budget, start date confirmed before acceptance",
   "Taxes", "Nothing"],
  1, "Material terms in writing. Always.", 4),
Q("Your 30/60/90 says 'lead something small' at day 61. What does that mean concretely?",
  ["Manage the team", "Own one small infrastructure improvement end-to-end — GPO cleanup, monitoring gap closed, runbook written — plus a lunch-and-learn",
   "Demand a promotion", "Work weekends"],
  1, "Specific, visible, documented. Small leadership beats big promises.", 5),
Q("Day 4: you spot outdated VPN setup docs in the onboarding wiki. What do you do?",
  ["Ignore — not your job", "Update the page, note it in the team channel, move on. 20 minutes that signals ownership.",
   "Complain about it", "Rewrite the entire wiki"],
  1, "Improve the environment you touch, document without being asked.", 6),
Q("What is the #1 self-inflicted wound in screening?",
  ["Slow email replies", "Inconsistency between interview statements and screening forms — dates, titles, bootcamp 'enrolled' vs 'completed'",
   "Asking questions", "Being employed"],
  1, "Consistency is the screening game. Enrolled Sept 30 — never completed.", 7),
Q("How many negotiation rounds is normal before it turns adversarial?",
  ["As many as it takes", "One round, well-aimed. Three rounds is adversarial.",
   "Zero — never negotiate", "Five"],
  1, "Ask once, well. Then decide like a professional.", 8),
]

FT06_DRILLS = [
D("ft06-drill-offer", "Offer evaluation — worksheet drill", [
("Fill the 8-line worksheet from memory with your targets.", "Base $90k target · bonus type · health cost · PTO · 401k+vesting · training budget · on-call terms · growth path.", "The worksheet is the decision tool — know it cold before the call comes."),
("Deliver Script 1 aloud. Then stop talking.", "'...I was targeting closer to $90,000. Is there flexibility to bridge that gap?' [silence]", "The silence after the number is the technique. Practice the silence."),
]),
D("ft06-drill-3090", "30/60/90 — one-page drill", [
("Recite the 30/60/90 one-liners.", "30: learn + document. 60: contribute + certify. 90: lead small + teach back.", "One line each — that's the version you say aloud."),
("Expand days 31–60 with two concrete artifacts.", "L2 tickets owned end-to-end + one documentation improvement proposed + Security+ study started.", "Artifacts, not adjectives."),
]),
]

FT06_LAB = LAB(
"ft06-lab-packet",
"Offer decision packet",
"Build the one-page 30/60/90 and the offer evaluation worksheet now — before any offer arrives. Decisions made calmly beat decisions made euphorically.",
["Write the 30/60/90 on one page: 3 phases, each with 2–3 concrete artifacts.",
 "Fill the 8-line offer worksheet with your targets and must-ask questions.",
 "Draft your negotiation Script 1/2/3 lines in your own words; rehearse the post-number silence.",
 "Call your references this week: warn them, send the role description.",
 "Assemble the packet: 30/60/90 + worksheet + scripts + reference list. One folder, ready.",
 "Review the honesty line once more: every date and claim in the packet matches your interview statements."],
"One folder: 30/60/90 page + filled worksheet + scripts + warned references.",
"Every claim matches interview statements; references warned; packet complete before any offer.")

FT06_RES = [
RES("ThreatLocker careers", "https://www.threatlocker.com/careers", "vendor"),
RES("ThreatLocker — official site", "https://www.threatlocker.com/", "vendor"),
]

FT["IL27-FT06"] = {
    "notes": FT06_NOTES, "cards_add": FT06_CARDS_ADD, "quiz": FT06_QUIZ,
    "drills": FT06_DRILLS, "handsOnLab": FT06_LAB,
    "supplementalResources": FT06_RES, "videos": [],
    "estimatedMinutes": 120,
}

# ---- FT01 click sim (course-level; IL-27 string-steps shape) ----
CLICK_FT01 = {
 "id": "IL27-CLICK-FT01-01",
 "moduleId": "IL27-FT01",
 "tool": "Allowlist policy review — conceptual walkthrough",
 "title": "Allowlist policy review — conceptual walkthrough",
 "steps": [
  "CONCEPTUAL DRILL — this walks the decision flow of an allowlisting model as publicly described, not any vendor's actual console screens.",
  "Step 1 — A user requests a new application. The request arrives with metadata: file hash, publisher signature, and the business justification.",
  "Step 2 — Check the hash against the known-good catalog. Known and signed by a trusted publisher? It maps to an existing policy — approve.",
  "Step 3 — Unknown hash? Check the publisher: signed by a known vendor goes to standard review; unsigned or unknown publisher goes to elevated review.",
  "Step 4 — Elevated review: run it in the ringfenced context first — no internet, no sensitive-file access — and observe behavior before any broad approval.",
  "Step 5 — Decision: approve (add hash + publisher to the allowlist policy), deny (log the rationale), or time-box (approve for the project window, then re-review).",
  "Step 6 — Every decision is logged with who approved, when, and why — the audit trail is the point. Denied executions generate an Operational Alert, not a silent block.",
  "Takeaway: allowlisting is a process discipline (request → verify → decide → audit), not just a technology switch. That's the model to describe in the interview."
 ]
}

# ---- FT01 terminal sims (course-level; IL-27 free-play shape) ----
TERM_FT01 = [
{
 "id": "IL27-TERM-FT01-01",
 "moduleId": "IL27-FT01",
 "title": "Endpoint triage one-liners",
 "brief": "A workstation is acting strangely. Triage it from PowerShell: processes, services, network. Type each command exactly.",
 "prompt": "PS C:\\>",
 "commands": [
  {"cmd": "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5",
   "out": "Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id ProcessName\n-------  ------    -----      -----     ------     -- -----------\n    812     45    182340     201120     412.55   4820 svchost\n    301     22     98300     110240     188.10   7712 MsMpEng\n    ...                                          (top 5 CPU consumers)"},
  {"cmd": "Get-Service | Where-Object {$_.Status -eq 'Running'} | Measure-Object",
   "out": "Count    : 87\n# 87 running services — compare against your hardened baseline; anything unfamiliar gets investigated."},
  {"cmd": "Test-NetConnection -ComputerName 8.8.8.8 -Port 443",
   "out": "ComputerName     : 8.8.8.8\nRemoteAddress    : 8.8.8.8\nRemotePort       : 443\nTcpTestSucceeded : True\n# Path to the internet is clean — the problem is local to this host."},
  {"cmd": "Get-NetTCPConnection -State Established | Select-Object LocalPort, RemoteAddress, RemotePort, OwningProcess | Sort-Object RemotePort",
   "out": "LocalPort RemoteAddress    RemotePort OwningProcess\n--------- -------------    ---------- ------------\n  49671   20.190.145.12         443         4820\n  49688   52.96.11.22           443         7712\n# Every established connection mapped to its owning process — the threat-hunting view."}
 ]
},
{
 "id": "IL27-TERM-FT01-02",
 "moduleId": "IL27-FT01",
 "title": "Threat-hunting one-liners: what doesn't belong",
 "brief": "Same workstation, deeper: find the process that doesn't belong. Hunt with PowerShell — no GUI, no guessing.",
 "prompt": "PS C:\\>",
 "commands": [
  {"cmd": "Get-Process | Where-Object {$_.Path -notlike 'C:\\Windows\\*'} | Select-Object Name, Path",
   "out": "Name          Path\n----          ----\nslack         C:\\Users\\emejia\\AppData\\Local\\slack\\slack.exe\ninvoice_pdf   C:\\Users\\emejia\\AppData\\Local\\Temp\\invoice_pdf.exe\n# invoice_pdf.exe running from Temp — unsigned, unexpected. That's your lead."},
  {"cmd": "Get-AuthenticodeSignature 'C:\\Users\\emejia\\AppData\\Local\\Temp\\invoice_pdf.exe' | Select-Object Status, SignerCertificate",
   "out": "Status            : NotSigned\nSignerCertificate :\n# Unsigned binary in Temp — in an allowlisted world this never executes. In triage, it's isolated first."},
  {"cmd": "Get-WinEvent -LogName Security -MaxEvents 5 | Select-Object TimeCreated, Id, Message",
   "out": "TimeCreated          Id Message\n-----------          -- -------\n10/13/2026 08:12:04  4688  A new process has been created... invoice_pdf.exe\n# 4688 = process creation. The Security log tells you WHEN it started — scope the incident from there."}
 ]
}
]

# ============================================================ ASSEMBLY ===
def main():
    with open(SRC) as f:
        course = json.load(f)

    mods = {m["id"]: m for m in course["modules"]}
    for mid, spec in FT.items():
        m = mods[mid]
        # Replace content arrays; preserve every other key (id/title/flags/objectives/
        # crossLinks/summary + module-specific: questions, stories, rounds, dayBefore, etc.)
        m["notes"] = spec["notes"]
        base_cards = m.get("cards", [])
        m["cards"] = base_cards + spec.get("cards_add", [])
        base_quiz = m.get("quiz", [])
        if "quiz" in spec:      # full replacement (was empty)
            m["quiz"] = spec["quiz"]
        else:                   # keep + add
            m["quiz"] = base_quiz + spec.get("quiz_add", [])
        for i, q in enumerate(m["quiz"]):
            q["index"] = i
        m["drills"] = spec["drills"]
        m["handsOnLab"] = spec["handsOnLab"]
        m["supplementalResources"] = spec["supplementalResources"]
        m["videos"] = spec["videos"]
        m["estimatedMinutes"] = spec["estimatedMinutes"]

    # Course-level additions
    course["terminalSims"] = course.get("terminalSims", []) + TERM_FT01
    course["clickSims"] = course.get("clickSims", []) + [CLICK_FT01, CLICK_FT05]
    course["branchingScenarios"] = course.get("branchingScenarios", []) + BRANCH_FT04

    # Hours fix: recompute AFTER rebuild
    total_min = sum(m.get("estimatedMinutes", 0) for m in course["modules"])
    course["hours"] = round(total_min / 60)
    course["updatedAt"] = UTC

    with open(OUT, "w") as f:
        json.dump(course, f, indent=1)
    # validate
    with open(OUT) as f:
        check = json.load(f)
    print("wrote", OUT, "| modules:", len(check["modules"]),
          "| minutes:", total_min, "| hours:", check["hours"])
    return check

# ============================================================ AUDIT ===
BANNED = ["palantir", "nsa ", "nsa.", "certified engineer", "insider contact"]

def audit(course):
    errs = []
    fts = [m for m in course["modules"] if m.get("fastTrack")]
    assert len(fts) == 6, "expected 6 FT modules, got %d" % len(fts)
    for m in fts:
        mid = m["id"]
        notes = m.get("notes", [])
        if not (5 <= len(notes) <= 8):
            errs.append(f"{mid}: notes count {len(notes)} not in 5-8")
        for n in notes:
            if not isinstance(n, dict):
                errs.append(f"{mid}: bare-string note found")
            elif not n.get("title") or len(n.get("body", "")) < 100:
                errs.append(f"{mid}: note incomplete: {str(n.get('title'))[:40]}")
        cards = m.get("cards", [])
        if not (10 <= len(cards) <= 14):
            errs.append(f"{mid}: cards count {len(cards)} not in 10-14")
        for c in cards:
            if not c.get("front") or not c.get("back"):
                errs.append(f"{mid}: card missing front/back")
        quiz = m.get("quiz", [])
        if not (8 <= len(quiz) <= 10):
            errs.append(f"{mid}: quiz count {len(quiz)} not in 8-10")
        for qi, q in enumerate(quiz):
            if not q.get("q") or len(q.get("choices", [])) != 4:
                errs.append(f"{mid}: quiz {qi} bad shape")
            a = q.get("answer")
            if not isinstance(a, int) or not (0 <= a <= 3):
                errs.append(f"{mid}: quiz {qi} missing/invalid answer key")
            if not q.get("explain"):
                errs.append(f"{mid}: quiz {qi} missing explain")
            if q.get("index") != qi:
                errs.append(f"{mid}: quiz {qi} index mismatch")
        drills = m.get("drills", [])
        if not (2 <= len(drills) <= 4):
            errs.append(f"{mid}: drills count {len(drills)} not in 2-4")
        for d in drills:
            for it in d.get("items", []):
                if not it.get("prompt") or not it.get("answer") or not it.get("explain"):
                    errs.append(f"{mid}: drill item missing key")
        lab = m.get("handsOnLab")
        if not lab or not all(lab.get(k) for k in ("title", "brief", "steps", "deliverable", "checkpoint")):
            errs.append(f"{mid}: handsOnLab incomplete")
        # preserved identity
        for k in ("id", "title", "fastTrack", "fastTrackDay", "objectives", "crossLinks"):
            if k not in m:
                errs.append(f"{mid}: lost key {k}")
        # banned content scan over new text — but allow intentional counter-examples:
        # phrases inside ❌ wrong-version examples, wrong quiz choices, or "Fix:" drill prompts
        import re as _re
        def clean_text(mid, m):
            parts = []
            for n in m["notes"]:
                # strip ❌ wrong-version examples (up to the ✅ correction)
                body = _re.sub(r"❌.*?(✅|\n\n)", "", n.get("body", ""), flags=_re.S)
                parts.append(n.get("title", "") + " " + body)
            for q in m["quiz"]:
                for i, ch in enumerate(q.get("choices", [])):
                    if i != q.get("answer"):
                        continue  # wrong choices are counter-examples by design
                    parts.append(ch)
                parts.append(q.get("q", "") + " " + q.get("explain", ""))
            for d in m["drills"]:
                for it in d.get("items", []):
                    p = it.get("prompt", "")
                    if p.strip().lower().startswith("fix:"):
                        continue  # correction drill by design
                    parts.append(p + " " + it.get("answer", "") + " " + it.get("explain", ""))
            lab = m.get("handsOnLab", {})
            parts.append(json.dumps(lab))
            for c in m.get("cards", []):
                parts.append(c.get("front", "") + " " + c.get("back", ""))
            return " ".join(parts).lower()
        blob = clean_text(mid, m)
        for b in BANNED:
            if b in blob:
                errs.append(f"{mid}: banned phrase '{b}' found outside correction context")
        blob2 = _re.sub(r"vs\.?\s*['\"]?completed['\"]?", "", blob)
        if _re.search(r"i completed.{0,40}bootcamp|bootcamp.{0,40}(was|has been|is)\s+completed", blob2):
            errs.append(f"{mid}: bootcamp completion claim outside correction context")
    # course-level additions
    if len([s for s in course.get("terminalSims", []) if s.get("moduleId", "").startswith("IL27-FT")]) != 2:
        errs.append("terminalSims FT additions != 2")
    for s in course.get("terminalSims", []):
        if s.get("moduleId", "").startswith("IL27-FT"):
            for c in s.get("commands", []):
                if not c.get("cmd") or "out" not in c:
                    errs.append(f"term sim {s['id']}: bad command shape")
    nclick = len([s for s in course.get("clickSims", []) if s.get("moduleId", "").startswith("IL27-FT")])
    if nclick != 2:
        errs.append(f"clickSims FT additions = {nclick}, expected 2")
    for s in course.get("clickSims", []):
        if s.get("moduleId", "").startswith("IL27-FT"):
            if not all(isinstance(st, str) and len(st) > 20 for st in s.get("steps", [])):
                errs.append(f"clicksim {s['id']}: steps must be non-trivial strings (IL-27 renderer)")
    nbranch = len([b for b in course.get("branchingScenarios", []) if b.get("moduleId", "").startswith("IL27-FT")])
    if nbranch != 2:
        errs.append(f"branching FT additions = {nbranch}, expected 2")
    for b in course.get("branchingScenarios", []):
        if b.get("moduleId", "").startswith("IL27-FT"):
            nodes = b.get("nodes", {})
            if b.get("start") not in nodes:
                errs.append(f"branch {b['id']}: start not in nodes")
            for nid, n in nodes.items():
                for ch in n.get("choices", []):
                    if ch.get("next") and ch["next"] not in nodes:
                        errs.append(f"branch {b['id']}: node {nid} bad next {ch['next']}")
    # hours
    total_min = sum(m.get("estimatedMinutes", 0) for m in course["modules"])
    if course.get("hours") != round(total_min / 60):
        errs.append(f"hours {course.get('hours')} != rounded {round(total_min/60)}")
    # non-FT modules untouched: spot check counts
    nonft = [m for m in course["modules"] if not m.get("fastTrack")]
    if len(nonft) != 48:
        errs.append(f"non-FT module count {len(nonft)} != 48")
    return errs

if __name__ == "__main__":
    course = main()
    errs = audit(course)
    if errs:
        print("AUDIT FAILURES:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print("AUDIT PASS: all 6 FT modules IL-26 grade, no banned content, hours consistent.")
    for m in [x for x in course["modules"] if x.get("fastTrack")]:
        print(f"  {m['id']}: notes={len(m['notes'])} cards={len(m['cards'])} "
              f"quiz={len(m['quiz'])} drills={len(m['drills'])} lab=1 "
              f"res={len(m['supplementalResources'])} vids={len(m['videos'])} min={m['estimatedMinutes']}")
