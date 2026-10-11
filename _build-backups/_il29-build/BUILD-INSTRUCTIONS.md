# IL-29 Build Instructions (shared by all batches)

## Course
IL-29 · ThreatLocker Zero-Trust CBT with AI — Cybersecurity Mastery Bootcamp
courseId: `il-29-threatlocker-ai-cybersecurity-mastery`, code: `IL-29`, schemaVersion: 4

## Module schema (EXACT)
Read `_module-template.json` in this directory — it is one complete IL-28 module. Copy its exact key shapes. Every module MUST have these keys with these value shapes:

- `id`: "IL29-MNN" (your batch's assigned numbers — use exactly these)
- `code`: short code like "TL-ZTA-01" (make sensible per-batch)
- `title`: module title
- `summary`: 2-3 sentence summary
- `objectives`: list of 4-6 strings ("By the end of this module you will be able to...")
- `estimatedMinutes`: honest integer (notes reading + videos + drills + lab; typical 480-620)
- `weight`: 1-5 integer (core modules higher)
- `notes`: array of 6-8 objects, each `{"title": "...", "body": "..."}`. Bodies must be FULL instruction: explain the concept from first principles, then a worked example with the solution shown step-by-step, then common mistakes / operator gotchas. Each body should be 400-900 words. Object-based only — never bare strings.
- `cards`: exactly 12 objects `{"front": "...", "back": "..."}` — flashcards, front is the prompt, back is the answer.
- `quiz`: 9-10 objects `{"q": "...", "choices": ["...", "...", "...", "..."], "answer": <0-based index>, "explain": "..."}`. 4 choices each. Explanations must teach, not just restate.
- `drills`: 2-3 objects `{"id": "il29-mNN-drillK", "title": "...", "items": [...]}` where each item is `{"prompt": "...", "answer": "...", "explain": "..."}`. Each drill should have 5-8 items. Drill 1 = rapid recall; drill 2 (and 3) = scenario/application.
- `handsOnLab`: `{"id": "il29-mNN-lab", "title": "...", "brief": "...", "steps": ["...", ...], "deliverable": "...", "checkpoint": "..."}`. Steps: 8-14 concrete steps doable on a Windows/Linux machine with free tools. Deliverable: a named artifact. Checkpoint: how to self-verify.
- `videos`: 1-2 objects `{"order": 1, "title": "...", "url": "...", "source": "...", "blurb": "...", "durationMin": <int minutes>, "watchBefore": "notes", "verifiedUtc": "2026-10-07T23:30:00Z", "httpStatus": 200}`. **Every URL must be verified with curl to return HTTP 200 before inclusion.** Use `curl -s -o /dev/null -w "%{http_code}" -L --max-time 20 "<url>"`. Prefer official/vendor and well-known educational sources (YouTube videos from official channels, MIT OCW, vendor docs). If a URL does not return 200, drop it. It is acceptable (not preferred) for a module to have 0 videos if nothing verifies.
- `mockTask`: one object `{"id": "il29-mNN-mock", "type": "choice", "q": "Panel-style question: ...", "choices": [...4...], "answer": <idx>, "explain": "..."}` — framed as an interview/panel question where it fits the module.
- `crossLinks`: list of 2-4 strings naming related IL-29 module ids (e.g. "IL29-M03").
- `prerequisiteFor`: list of 0-3 module id strings that build on this one.

## HARD quality rules
- NEVER invent facts, metrics, dates, credentials, certifications, exam question counts you are not sure of, salaries, or vendor claims. When in doubt, teach the concept without the number.
- No vendor affiliation, endorsement, or certification-conferral claims anywhere. Certification tracks are framed as "independent preparation for <exam>, aligned to its publicly published exam objectives."
- ThreatLocker product facts (VERIFIED): Zero Trust endpoint protection platform; core modules: Allowlisting (Application Control — deny-by-default, learns the application environment, permits what users use, denies everything else), Ringfencing (restricts what allowed apps can do: block executing other apps/processes, registry edits, file read/write, network sessions; stops weaponization of trusted apps, e.g. Word calling PowerShell), Elevation Control (removes local admin, just-in-time elevation delegated to applications via policy), Storage Control (granular policies over storage devices, file paths, shares; blocks data theft/exfiltration), Network Control (endpoint firewall, dynamic ACLs that open/close ports, blocks lateral movement and C2), ThreatLocker Detect (alerts on indicators of compromise blocked by modules), Configuration Manager (centralized Microsoft Defender configuration). Do NOT invent portal UI labels, exact policy names, pricing, or internal tooling beyond these verified descriptions.
- MIT 6.858 topics (VERIFIED from OCW): threat models, control hijacking attacks, buffer overflow exploits and defenses, privilege separation, capabilities, sandboxing native code, web security model, securing web applications, symbolic execution, network security, network protocols, SSL and HTTPS, side-channel attacks, user authentication, private browsing, anonymous communication, mobile phone security, data tracking, security economics. Teach the concepts in your own words; do not copy OCW text.
- MIT xPRO Professional Certificate in Cybersecurity (VERIFIED): 24-week online program, ~10-20 hrs/week, US$7,750, 36 CEUs, covers foundational/defensive/offensive cybersecurity, NIST frameworks, MITRE ATT&CK, CSA Cloud Controls Matrix; capstone project. Frame IL-29's track as independent preparation aligned to its publicly described topic map. URL for resources: https://xpro.mit.edu/courses/course-v1:xPRO-PCCYx/
- CompTIA Security+ SY0-701 (VERIFIED current version): 5 domains — 1.0 General Security Concepts 12%, 2.0 Threats, Vulnerabilities & Mitigations 22%, 3.0 Security Architecture 18%, 4.0 Security Operations 28%, 5.0 Security Program Management & Oversight 20%. Up to 90 questions, 90 minutes, passing 750/900.
- CompTIA CySA+ CS0-003 (VERIFIED): 4 domains — 1.0 Security Operations 33%, 2.0 Vulnerability Management 30%, 3.0 Incident Response Management 20%, 4.0 Reporting and Communication 17%. Max 85 questions (multiple-choice + performance-based), 165 minutes, passing 750/900.
- ISC2 CISSP (2024, 8 domains): 1. Security and Risk Management 16%, 2. Asset Security 10%, 3. Security Architecture and Engineering 13%, 4. Communication and Network Security 13%, 5. Identity and Access Management 13%, 6. Security Assessment and Testing 12%, 7. Security Operations 13%, 8. Software Development Security 10%. 100-150 CAT questions, 3 hours, 700/1000.
- GIAC GSEC (VERIFIED): administered by GIAC (SANS affiliate); 106 questions, 4-hour limit, 72% passing, open-book; aligned to SANS SEC401 Security Essentials.
- Google Cybersecurity Professional Certificate (VERIFIED): on Coursera, entry-level professional certificate by Google.
- IBM Cybersecurity Analyst Professional Certificate (VERIFIED): on Coursera, by IBM.
- Interview context (VERIFIED): ThreatLocker, IT Infrastructure Specialist role, via Crawford Thomas (recruiter Alex Starr). Interview: Tuesday October 13, 2026, 9:00 AM ET, 1950 W Maitland Blvd, Orlando, FL 32810. Panel simulation modules must train for THIS interview: technical depth + STAR behavioral.
- Do NOT duplicate IL-24 (assessment prep: company-cold, STAR basics, default-deny ops intro, triage decisions, attack graphs, UEBA, AI agent security, Bayes math, assessment sim) or IL-27 (Windows/Linux/networking admin, AD/GPO, PowerShell, allowlisting concepts, zero-trust principles at concept level, FT01-FT06 interview fast-track). IL-29 goes DEEPER and OPERATIONAL — assume the learner finished IL-24/IL-27 and now needs operator-grade depth.
- The learner persona: Enmanuel Mejia, junior IT infrastructure / aspiring security operator, preparing for the ThreatLocker IT Infrastructure Specialist interview on Oct 13, 2026. Write directly to him in second person where natural.

## Output
Write a single JSON array to `_il29-build/batch-X.json` (your batch letter). Validate with `python3 -c "import json; d=json.load(open('...')); print(len(d))"` before finishing. Every module must satisfy the counts above — self-check with a script and report the min counts per field.
