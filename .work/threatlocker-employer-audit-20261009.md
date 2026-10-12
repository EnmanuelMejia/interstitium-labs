# ThreatLocker Employer Audit — 2026-10-09

**Context:** Third interview Tue Oct 13, 2026, 9:00–11:00 AM ET — IT Infrastructure Specialist (via Crawford Thomas / Alex Starr). User stated desired salary $90,000/yr on ADP applications. User self-identifies as a JUNIOR candidate.

**Method:** Direct review of master resume (r4), tailored ThreatLocker resume, applications tracker, live site fetches, memory records; plus delegated subagent audits of site claims, GitHub, and social media (results appended below).

---

## CRITICAL (fix before Oct 13)

### 1. GPA misrepresentation on master resume
- **Where:** `~/workspace/job-hunt/Enmanuel_Mejia_Resume_2026_r4.pdf` (and .docx), EDUCATION & CERTIFICATIONS section
- **What it says:** "B.S., Business Management & Finance - University of Phoenix (GPA 3.67)"
- **Reality:** Verified transcript (memory 2026-09-28) shows B.S. Business/Management finished 7/2/2006, Finance second major, **GPA 3.01**
- **Why flagged:** GPA inflation of 0.66 points is a classic background-check failure. Education verification is standard.
- **Fix:** Change to 3.01 or remove GPA entirely.

### 2. Fabricated credential in cover letter template
- **Where:** `~/workspace/job-hunt/Cover_Letter_Master_Template.txt`
- **What it says:** "I hold a B.S. in Business Management & Finance, CompTIA A+, and the **Google IT Support Professional Certificate** (Security+ and AWS Solutions Architect in progress)."
- **Reality:** Memory explicitly records "Google IT Support certificate not found — stays off resumes" (2026-09-28, MEMORY.md). The certificate was never found/earned.
- **Why flagged:** Claiming an unearned credential is resume fraud. If any sent cover letter used this template verbatim, the claim is already in employers' hands.
- **Fix:** Remove the Google IT Support claim from the template immediately. Audit sent cover letters for whether it went out.

### 3. Five ThreatLocker applications for different roles
- **Where:** `~/workspace/job-hunt/applications-tracker.csv`
- **What:** ADP applications submitted: Special Projects IT Engineer (Req 1004, 9/30), Solutions Engineer (10/2), Detection Engineer (10/2), Junior DevOps Engineer (10/2), plus Jr. Cyber Hero Intern application (10/5, memory). Now interviewing for **IT Infrastructure Specialist** — a sixth distinct role/title.
- **Why flagged:** Six applications across wildly different functions (sales engineering, detection, DevOps, intern, IT infra) signals lack of focus. A hiring manager seeing this may question genuine interest in the specific role.
- **Fix:** Prepare a clear narrative: "I applied broadly because I want to work at ThreatLocker specifically; IT Infrastructure is where my experience fits." Do not hide it — they can see their own ATS.

### 4. "Production-grade" Kubernetes/Terraform claims without production evidence
- **Where:** Master resume r4 — "DevOps SuperLab - Active GitHub portfolio demonstrating **production-grade** Kubernetes configuration, GitOps workflows, CI/CD automation, Infrastructure as Code with Terraform"; also cover letter template ("demonstrates **production-grade** DevOps work")
- **Reality:** These are homelab/portfolio projects. No production employer, no on-call, no SLAs. Memory already flagged Terraform/K8s as potentially unsupported (2026-10-02).
- **Why flagged:** ThreatLocker's interview is a live troubleshooting round. "Production-grade" invites questions he may not be able to answer at depth ("tell me about your production incident response").
- **Fix:** Downgrade to "homelab/portfolio-grade" or "hands-on lab environment." Keep the projects — they're real — but don't call them production.

### 5. Management-scope claims on an IC title at Data Vimenca
- **Where:** Master resume r4 + cover letter template
- **What it says:** Title: "IT Operations Engineer II / IT Support Engineer II" — but claims "leading a 22-person IT organization supporting 1,700+ users" and "Managed a $550,000 annual IT budget"
- **Why flagged:** An Engineer II leading 22 people and owning a $550K budget is unusual. Reference/background checks with Data Vimenca may not corroborate the scope. If true, the title undersells it; if inflated, it's a credibility hit.
- **Fix:** Verify against what Data Vimenca HR would confirm (title, reports, budget authority). Align the bullet scope with the verifiable title, or clarify "technical lead" vs "people manager."

---

## MAJOR

### 6. ThreatLocker-branded interview-prep products (optics)
- **Where:** Live sites — `https://interstitiumlabs.dev/bootcamps/tl-interview/`, resume project entries ("ThreatLocker Interview Test Bootcamp," "ThreatLocker Assessment Prep CBT")
- **Status:** Disclaimers are proper ("Not affiliated with, endorsed by, or sponsored by ThreatLocker... Confers no certificate"). Verified live 2026-10-09.
- **Why flagged anyway:** Building and marketing a "ThreatLocker Interview Test Bootcamp" while interviewing at ThreatLocker is awkward optics. A hiring manager could read it as presumptuous or as monetizing their interview process.
- **Fix (optional):** Consider temporarily unlisting or renaming these pages until after the interview loop closes. At minimum, be ready to frame it positively: "I learn by building; I built prep material to master the domain."

### 7. SOC Analyst headline on ThreatLocker-tailored resume vs IT Infrastructure role
- **Where:** `~/workspace/job-hunt/tailored-apprenticeship-20261005/Enmanuel_D_Mejia_jb-threatlocker_resume.docx`
- **What it says:** Headline: "SOC Analyst | Cybersecurity Operations | Threat Detection & Triage | CompTIA A+ CE"
- **Why flagged:** He's interviewing for IT Infrastructure Specialist, not SOC. A security-operations headline on an infra application looks mis-targeted. (Note: this resume was built for a different ThreatLocker posting; the exact resume submitted Sep 30/Oct 2 could not be located — memory 2026-10-06.)
- **Fix:** Confirm which resume version is on file with Crawford Thomas/Alex Starr for the Oct 13 interview; bring a correctly targeted copy.

### 8. Salary expectation trail
- **Where:** applications-tracker.csv — "desired salary $90,000" on all four ADP applications
- **Why flagged:** Not a public post (good — no public salary claims found on sites), but it's in ThreatLocker's ATS. If the Oct 13 conversation goes to comp, he must be consistent.
- **Fix:** None needed unless his number changed — just be consistent at $90k.

### 9. Social media blitz volume (Oct 9)
- **Where:** Instagram/Threads/Facebook/LinkedIn — ~10+ AI-promotional posts in a single day (Noah AI, IL-29, IL-28, etc.)
- **Why flagged:** A hiring manager checking LinkedIn sees a feed dominated by self-promotional AI content posted within hours. Can read as inauthentic/spammy rather than professional.
- **Fix:** Space future posts out (already planned via daily cron). Consider whether the LinkedIn feed needs curation before Oct 13.

---

## VERIFIED CLEAN (no action)

- **CompTIA A+ CE** — verified legitimate (certified 04/30/2024, expires 04/30/2027). Correctly listed.
- **"Founder" title** — his own company (Interstitium Labs); legitimate at his direction.
- **No public salary posts** on any site (only third-party job-feed JSON mentions $90k–$150/hr ranges, not his claims).
- **No exposed secrets** found in grepped public assets (spot check).
- **ThreatLocker prep disclaimers** — proper non-affiliation language on all pages.
- **`/bootcamps/` 401** — fixed 2026-10-09 (301 to catalog).

---

## DELEGATED SUBAGENT FINDINGS (appended on delivery)

### A. Site claims audit — DELIVERED 2026-10-09 ~06:47 EDT (see Section W below)
### B. GitHub claims audit — DELIVERED 2026-10-09 ~06:53 EDT (see Section G below)
### C. Social media audit — DELIVERED 2026-10-09 ~06:46 EDT (see Section S below)

---

## LINKEDIN PROFILE — NOT YET AUDITED
LinkedIn experience/skills/posts require a live-browser session (subagents cannot operate the browser). Recommend parent delegate: compare LinkedIn experience entries against resume (titles, dates, Data Vimenca scope), review recent post tone, check skills endorsements for inflated claims.

---

## G. GITHUB CLAIMS AUDIT (subagent, delivered 2026-10-09 ~06:53 EDT)
**Bottom line: GitHub is clean and unusually well-disclaimed.** None of the memory-flagged resume risks appear as GitHub claims. No critical or major findings. Profile README self-identifies as "Junior cloud / DevOps candidate" with explicit evidence boundaries ("do not represent paid production DevOps employment... CompTIA A+ is my confirmed credential"). devops-superlab explicitly disclaims production ("Terraform, HA, autoscaling... remain learning goals"). All ThreatLocker prep repos carry non-affiliation disclaimers at README, meta.json, repo description, and inside content. No profanity in commits; no live secrets (one dummy fixture in a redaction test only).

### G1. MINOR: Unverified ThreatLocker marketing figures in tl.json
- **Where:** `threatlocker-assessment-prep-cbt/source/tl.json` — "70,000+ organizations" (public sources cite ~50,000 companies as of 2025); "Cyber Hero MDR ~60-second average response" (unverified)
- **Why flagged:** If he recites these in the Oct 13 interview and they're wrong, it weakens his pitch.
- **Fix:** Verify against current ThreatLocker sources or soften to ranges.

### G2. MINOR: "Enterprise-grade" product puffery
- **Where:** `interstitium-certification-bootcamps/README.md`, `full-spectrum-dominance-cbt/README.md`
- **Why flagged:** Puffery about his own software; mitigated by explicit disclaimers.
- **Fix:** Optional tone-down.

### GitHub note for parent
Repo descriptions already carry non-affiliation language (search-result snippets covered). The trademark-bearing repo name is nominative fair use with disclaimers everywhere; do NOT rename without user's say-so (breaks live deployment routes).

---

## W. SITE CLAIMS AUDIT (subagent, delivered 2026-10-09 ~06:47 EDT)
**Scope:** interstitiumlabs.dev, enmanueldmejia.com, docs source. Overall: well-defended on highest-risk claims; disclaimers present on all ThreatLocker-named products.

### W1. MAJOR: RHEL fabric presented as deployed, but install is pending
- **Where:** https://interstitiumlabs.dev/rhel-fabric/ (linked from portfolio as "View project")
- **What it says:** Present-tense architecture: "A bare-metal RHEL 10 architecture for virtualization, containers, AI workloads, security labs..." (KVM/QEMU, SELinux enforcing, etc.)
- **Reality:** Memory records RHEL install as pending/blocked — ISO not downloaded, P920-HOST unreachable. Nothing on the page says "planned" or "in progress."
- **Why flagged:** IT Infrastructure Specialist interviewer will ask "show me the fabric."
- **Fix:** Reframe as architecture blueprint / in-progress build, or temporarily remove until deployed.

### W2. MINOR: "a decade of semiconductor operations" rounds up
- **Where:** enmanueldmejia.com hero — "I bring a decade of semiconductor operations and analytics discipline into cloud-native engineering."
- **Reality:** Intel semiconductor roles ≈ 8.7 years (Oct 2000–Jul 2009); Materion was aerospace/materials, not semiconductor.
- **Fix:** "nearly a decade of semiconductor operations."

### W3. MINOR: "supervising 22" — number unverified in available records
- **Where:** interstitiumlabs.dev/founders/ and resume
- **Why flagged:** Specific headcount invites verification; no record confirms the number 22.
- **Fix:** Confirm against employment records; if unsubstantiable, soften to "led a support team."

### W4. MINOR: IL-29 portfolio card lacks disclaimer
- **Where:** enmanueldmejia.com IL-29 project card — "ThreatLocker platform operations... ThreatLocker IT Infrastructure Specialist panel interview simulation" with no one-line disclaimer (the underlying pages disclaim properly).
- **Fix:** Add "Independent prep companion — not affiliated with ThreatLocker" to the card.

### W5. MINOR: LPS analysis wording (prepare-an-answer, not remove)
- **Where:** Portfolio claims recommendations "delivered to district leadership" vs evidence page noting the role never commenced.
- **Status:** Facts compatible (delivered at interview presentation); honest framing already in place. Just prepare the answer.

### Site positives (verified clean)
- CompTIA A+ CE claim legitimate. No salary expectations published. No MITRE/Sigma/YARA/EDR personal claims (MITRE appears only as course content). No Terraform/K8s production claims about him (SuperLab labeled "Not paid production," "designed for hands-on demonstrations"). No RHEL cert claim (RHCSA only as prep track). No title inflation ("Junior Cloud/DevOps trajectory — ambitious prep without title inflation"). No employer complaints. No exposed secrets.

---

## S. SOCIAL MEDIA AUDIT (subagent, delivered 2026-10-09 ~06:46 EDT)
**Reviewed:** Instagram (public, 80 most recent of 3,409 posts), Threads (private account — hiring manager can't see), Facebook personal (20 most recent) + IL page, TikTok @enmanuelmejia (public, stats only). X NOT reviewed (x.com blocked in subagent environment) — biggest gap since X stays public.

### S1. MAJOR: Anti-feminist political satire reel on public Instagram
- **Where:** https://www.instagram.com/reel/DdRgSzYKcDe/ (2026-09-14, his own AI-generated production, captioned #feminism)
- **What:** Satirizes "Believe All Women" movement; Amber Heard likeness confesses, crowd chants "THE HUSBAND DID IT!"
- **Why flagged:** Culture-war content = bias/harassment-risk signal to any employer screener.
- **Fix:** Delete outright. (Mitigated somewhat by planned IG privatization, but delete anyway.)

### S2. MAJOR: Possible execution-content share on Facebook (posted TODAY)
- **Where:** https://facebook.com/764083326/posts/10168127668008327/ (2026-10-09 04:35 EDT)
- **What:** Shared post with garbled OCR reading "...public execution"
- **Why flagged:** If violent/execution content, catastrophic 4 days before a third interview.
- **Fix:** Verify content immediately; delete if violent.

### S3. MAJOR: Partisan political shares on Facebook
- **Where:** Two MAGNO.NEWS shares (2026-10-08): Rubio/USAID testimony, JD Vance anti-visa-fraud task force ("AMERICAN JOBS FIGHT VISA FRAUD")
- **Why flagged:** Partisan Trump-administration content; visa-fraud framing is tone-deaf for a job seeker.
- **Fix:** Delete/unshare both.

### S4. MAJOR: Second anti-feminist data point (Facebook)
- **Where:** Daily Wire share (2026-10-08): "Feminists wanted to be the provider, now they don't."
- **Why flagged:** Two data points = pattern, worse than one.
- **Fix:** Delete.

### S5. MAJOR: "ThreatLocker Zero-Trust CBT" course branding during interview cycle
- **Where:** Instagram/Threads/Facebook posts 2026-10-07–09; IL-29 course page
- **Why flagged:** Trading on their trademark while applying; invites awkward questions.
- **Fix:** User decision — temporarily rename to "Zero-Trust CBT" or unlist during interview cycle.

### S6. MINOR: Profanity meme (Facebook, 2026-10-08)
- **Where:** Boston meme: "Go f**k yourself" as term of endearment
- **Fix:** Delete.

### S7. MINOR–MAJOR: AI-fabricated lifestyle imagery (Instagram)
- **Where:** Reel DeMumyBir7u (2026-10-07) — AI-generated photo posing with women between luxury cars at Universal Studios
- **Why flagged:** Fabricated wealth-signaling reads as deceptive under scrutiny.
- **Fix:** Delete.

### S8. MINOR: Oct 7–9 content blitz looks spammy
- **Where:** ~17 IG posts, 20 FB posts, 5 Threads in ~3 days; near-zero engagement
- **Why flagged:** Inauthentic AI-content flood undercuts the founder brand.
- **Fix:** Slow cadence going forward (already planned via daily cron).

### S9. MINOR: about.me/e.mejia title optics
- **Where:** Headline: "Data Scientist, Full Stack Software Developer, and Cloud Engineer"
- **Why flagged:** Reads senior/multi-role vs his stated JUNIOR positioning.
- **Fix:** Optional reframe with his approval.

### S10. TikTok — unreviewed videos
- **Where:** @enmanuelmejia (public, 13 videos); bio emoji-only; 2,888 following / 133 followers ratio looks follow-for-follow
- **Gap:** Video contents not retrievable; needs app or live-browser review.

### Social positives (checked, clean)
No employer complaints, no job-hunt desperation posts, no leaked employer confidential info, no drug/partying content, no negative ThreatLocker mentions.

### Social gaps
1. **X @enmanuelmejia — NOT REVIEWED** (blocked in this environment). Needs live-browser review before Oct 13 — it's the guaranteed-public professional account.
2. TikTok 13 video contents unreviewed.
3. Only last 20 FB posts and 80 most recent IG posts reviewed (of 3,409).
