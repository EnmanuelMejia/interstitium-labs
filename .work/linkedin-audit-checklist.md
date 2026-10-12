# LinkedIn Audit Checklist — course & project items
Prepared: 2026-10-08 ~13:15 EDT (subagent, curl-only, no browser used)
Profile: https://www.linkedin.com/in/enmanuelmejia/ · Company page: actorCompanyId 146647725 (Interstitium Labs)

## STEP 0 — PRE-FLIGHT GATE (READ FIRST, DO NOT SKIP)

**The university subtree is DOWN on the live site right now.** Verified 2026-10-08 ~13:10–13:16 EDT via curl (multiple user agents):

| URL | Live status |
|---|---|
| `https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery` | **404** (was 200 at launch 2026-10-07 ~19:38) |
| `https://interstitiumlabs.dev/university/course?course=il-28-devsecops-cloud-infrastructure-mastery` | **404** |
| `https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery` | **404** |
| `https://interstitiumlabs.dev/university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery` | **404** |
| `https://interstitiumlabs.dev/university/course.html`, `/university/`, `/university/courses.html`, `/university/catalog` | **404** |
| `https://interstitiumlabs.dev/il29` (worker 301 → course URL) | **404** |
| All `https://interstitiumlabs.dev/university/og/*.png` (il-29, il-28, il-27, il-26, devops-superlab, lps-enrollment, sundance-ai) | **404** |
| `https://interstitiumlabs.dev/work/lps-enrollment-analysis/` | **404** |
| `https://interstitiumlabs.dev/work/sundance-ai-architecture/` | **404** |
| `https://interstitiumlabs.dev/` root | **200** (site itself is up) |
| `https://interstitiumlabs.dev/labs/superlab/` | **200** (live) |
| Same /university/* 404s on `learn.interstitiumlabs.dev` | **404** |

Diagnosis (read-only): the repo (`~/workspace/apex-audit/docs/`) contains all of these files — the 7 OG PNGs exist locally (Oct 7 timestamps) and `docs/_worker.js` contains the `/il29`→course 301s and the edge-side OG injection (`serveCourseWithOg`) — so the deployed build lost the `/university/*` subtree and the worker routing (likely an in-flight/broken redeploy from today's paywall + course-fix workstream; repo HEAD is 2026-10-07 13:56 EDT, before the break).

**DECISION FOR THE BROWSER TASK:** Do NOT delete, re-add, or reorder any LinkedIn Featured/Projects media links in this run. Deleting a link whose target is temporarily 404 and re-adding it will cache a broken preview; worse, re-adding a 404 URL can poison LinkedIn's scraper cache for that URL. Instead:
1. Complete Steps 1–3 as READ-ONLY inventory (record what LinkedIn currently shows: order, titles, whether thumbnails render).
2. Then run Step 4 (post liveness) and Step 5 (paywall OG test).
3. Report the inventory + flag the site outage to the orchestrator so the deploy is repaired FIRST; re-schedule this checklist for a second pass after `curl -sI <course URL>` returns 200.

If the orchestrator confirms the deploy was repaired before you start Step 2, proceed with remediation as written.

---

## STEP 1 — FEATURED SECTION AUDIT (read-only unless gate cleared)

Location: profile → Featured section. Record current ORDER (top→bottom) and, for each item, what thumbnail LinkedIn renders (rich card vs grey placeholder).

### F1. IL-29 — must be FIRST
- Expected link: `https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery`
- Expected LinkedIn card title (from worker OG profile): "IL-29 · ThreatLocker Zero-Trust CBT with AI — Cybersecurity Mastery Bootcamp"
- Expected OG image: `https://interstitiumlabs.dev/university/og/il-29-threatlocker-og.png` (1200×630; local file 858 KB, exists in repo)
- curl status: target 404, OG 404 (gate not cleared — verify only)
- Remediation (only after gate cleared): if not first → use Featured reorder controls to move to top. If thumbnail grey → apply grey-placeholder playbook (below).

### F2. IL-28
- Expected link: `https://interstitiumlabs.dev/university/course?course=il-28-devsecops-cloud-infrastructure-mastery`
- Expected card title: "IL-28 · DevSecOps & Cloud Infrastructure — Production Mastery Bootcamp"
- Expected OG image: `https://interstitiumlabs.dev/university/og/il-28-devsecops-og.png` (1200×630; repo file 98 KB)
- curl status: target 404, OG 404

### F3. IL-26
- Expected link: `https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery`
- Expected card title: "IL-26 · Data Analyst Certification & Senior Mastery Bootcamp"
- Expected OG image: `https://interstitiumlabs.dev/university/og/il-26-data-analyst-og.png` (1200×630; repo file 718 KB)
- curl status: target 404, OG 404

### F4. Certification Bootcamp Catalog — 68 Interactive Prep Bootcamps
- Expected link: UNKNOWN from records — inventory the actual URL shown on the profile item and report it. (Repo has `docs/university/courses.html`, but that path 404s live; catalog may be a different page. Do not guess.)
- curl status: not verifiable from records — record from profile.

### F5. AI Vision Deck
- Expected link: UNKNOWN from records — inventory the actual URL shown on the profile item and report it.

### F6. ThreatLocker item
- Expected link: UNKNOWN from records — inventory the actual URL shown on the profile item and report it. (Note: may be the IL-29 course link, the interstitiumlabs.dev homepage, or threatlocker.com — record exactly.)

Expected Featured order: F1 (IL-29) → F2 (IL-28) → F3 (IL-26) → F4 (Catalog) → F5 (Vision Deck) → F6 (ThreatLocker). Report actual vs expected.

---

## STEP 2 — PROJECTS SECTION AUDIT (read-only unless gate cleared)

Location: profile → Projects section. For each entry verify: title text, link URL, thumbnail renders.

### P1. "IL-29 · ThreatLocker Zero-Trust CBT with AI — Cybersecurity Mastery Bootcamp"
- Expected link: `https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery`
- curl status: 404 (gate)

### P2. "IL-28 · DevSecOps & Cloud Infrastructure — Production Mastery Bootcamp"
- Expected link: `https://interstitiumlabs.dev/university/course?course=il-28-devsecops-cloud-infrastructure-mastery`
- curl status: 404 (gate)

### P3. "DevOps SuperLab — Kubernetes, GitOps & CI/CD Portfolio Lab"
- Expected link: `https://interstitiumlabs.dev/labs/superlab/`
- curl status: **200 — LIVE.** This one is healthy; if its thumbnail is grey, the grey-placeholder playbook CAN be applied now (OG image `https://interstitiumlabs.dev/university/og/devops-superlab-og.png` currently 404s live, so the card may be rendering from another image or placeholder — record what renders).

### P4. "Lawrence Public Schools Enrollment Analysis"
- Expected link: `https://interstitiumlabs.dev/work/lps-enrollment-analysis/`
- curl status: 404 (gate). OG image `https://interstitiumlabs.dev/university/og/lps-enrollment-og.png` also 404 live.

### P5. Anonymized manufacturing AI case study (SunDance)
- Expected link: `https://interstitiumlabs.dev/work/sundance-ai-architecture/`
- curl status: 404 (gate). OG image `https://interstitiumlabs.dev/university/og/sundance-ai-og.png` also 404 live.

### P6. "Certification Bootcamp Catalog — 68 Interactive Prep Bootcamps"
- Expected link: UNKNOWN from records — inventory from profile, report URL.

### P7/P8. IL-27 and IL-26 projects (may or may not exist)
- IL-27 course URL: `https://interstitiumlabs.dev/university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery` (curl 404, gate)
- IL-27 OG image: `https://interstitiumlabs.dev/university/og/il-27-it-infrastructure-og.png` (repo file 801 KB; curl 404 live)
- IL-27 worker OG title: "IL-27 - IT Infrastructure Specialist: Zero Trust Infrastructure Mastery"
- **Record whether an IL-27 project entry exists. If it does not exist, DO NOT create it in this run (target URL is 404; creating now would cache a broken card). Flag it as "to create after deploy repair."**
- Record whether an IL-26 project entry exists (IL-26 has a Featured item; a duplicate project entry is optional — report, don't change).

---

## STEP 3 — GREY-PLACEHOLDER PLAYBOOK (only after pre-flight gate clears)

Known working recipe (from memory, verified 2026-10-07):
1. Append `?v=2` to the og:image URL (e.g. `.../il-29-threatlocker-og.png?v=2`) in the site's worker OG profile, redeploy the site, confirm the PNG URL returns 200 via curl.
2. On LinkedIn: delete the media link from the Featured/Projects item, save, then re-add the SAME course link URL fresh. LinkedIn's scraper caches failed scrapes — the delete + re-add forces a fresh scrape, and the `?v=2` cache-bust guarantees a new image URL.
3. Verify the rich card thumbnail renders. If still grey, re-scrape via the post inspector once (do not hammer it).

**Never run this playbook against a target URL that returns non-200.** Verify `curl -sI <course URL>` → 200 and `curl -sI <og png>` → 200 before touching LinkedIn.

---

## STEP 4 — LAUNCH POST LIVENESS (safe to run now — read-only)

These are public LinkedIn post URLs; check each opens and shows the post with its rich preview card. (curl returned 200 for both activity URLs below on 2026-10-08 ~13:14 EDT, but curl-200 on LinkedIn can be a login-wall shell — visually confirm content + thumbnail in the browser.)

- IL-29 launch — personal post: `https://www.linkedin.com/feed/update/urn:li:activity:7513702782147883009/`
- IL-29 launch — company page post: `https://www.linkedin.com/feed/update/urn:li:share:7513703135429935106?actorCompanyId=146647725`
- IL-28 launch — personal post: `https://www.linkedin.com/feed/update/urn:li:activity:7513724746358767616/`
- IL-28 launch — company page post: `https://www.linkedin.com/feed/update/urn:li:share:7513725311033761792/?actorCompanyId=146647725`

For each: confirm the post is public, the link preview card renders with the course OG image (not grey), and note any anomalies. Do NOT edit, like, comment, or share.

---

## STEP 5 — PAYWALL OG VERIFICATION (safe to run now — read-only code fact + browser check)

Code fact (verified read-only in `docs/_worker.js`, `serveCourseWithOg`): OG tags for `/university/course?course=<id>` are injected at the edge for LinkedIn/Facebook/Twitter crawlers with NO entitlement/cookie check — the paywall (IL-01–IL-26 gated; IL-27/28/29 free) does not strip crawler-visible OG tags. The injection only requires the worker route to fire (`run_worker_first` must include `/university/course`), which is currently the broken part per Step 0.

Browser step (after gate clears): pick ONE gated course (e.g. IL-26) and use LinkedIn's link-preview flow (start a draft post, paste the IL-26 course URL, do NOT publish) to confirm the rich card renders the course title + OG image even though the course is paywalled. Discard the draft. Report pass/fail.

---

## REPORT FORMAT (what the browser task must return)

1. Pre-flight: `curl -sI` results for the 4 course URLs + 7 OG PNGs (200 or not).
2. Featured inventory: actual order, per-item title shown, thumbnail state (rich/grey), actual linked URL for F4/F5/F6.
3. Projects inventory: for P1–P8, exists? title matches? link URL? thumbnail state?
4. IL-27: project entry exists? If not — flagged "create after deploy repair" (with course URL + OG title above).
5. Post liveness: 4 posts public + cards render? Any anomalies?
6. Paywall OG test: pass/fail (or "blocked by Step 0 gate").
7. Anything you changed (expected: nothing, unless gate was cleared and orchestrator approved).
