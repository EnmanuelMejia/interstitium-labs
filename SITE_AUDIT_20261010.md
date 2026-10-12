# SITE AUDIT — interstitiumlabs.dev — 2026-10-10

**Goal:** production-ready to ship and go live. Findings only; no deploys performed.
**Method:** 5 parallel workstreams (theme categories, link integrity, nav/consistency, layout/QA, content gaps).
**Source:** `~/workspace/apex-audit/docs/` · Live: https://interstitiumlabs.dev/ · Worker: solitary-sound-015a

## EXECUTIVE SUMMARY

The site is structurally sound — heroes, headers, footers, and viewport metas are present on all key pages; zero broken asset references; no stubs; no duplicate content; course data complete (31/31 courses have title, blurb, non-empty modules/paths). However, it is NOT shippable yet:

- **85 broken links** — 84 of them are dead `/bootcamps/<slug>/` pages linked from theme pages. This is the dominant issue.
- **3 EMPTY themes, 7 THIN themes** live (Programming, Databases, Blockchain, Cybernetics get source-level relief on next deploy; Om has zero courses even in source).
- **/jobs/ carries a stale header nav** pointing at the folded `learn.` subdomain.
- **Competitor names in live course data** (Coursera ×4 courses, Pluralsight ×1 course) violate the standing rule.
- **Wrong CTA target** on the bootcamp catalog (Interview Prep card points at Assessment Prep).
- Source-vs-live drift: theme sources modified Oct 10 are not yet deployed.

## ISSUE COUNTS

| Category | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Broken links | 0 | 84 | 1 | 0 | 85 |
| Empty/thin themes | 0 | 3 | 7 | 0 | 10 |
| Nav inconsistencies | 0 | 1 | 1 | 3 | 5 |
| Layout bugs | 0 | 0 | 3 | 3 | 6 |
| Content gaps (placeholders/dupes) | 0 | 5 | 3 | 4 | 12 |
| Competitor-name violations | 0 | 6 files | 1 comment | 0 | 7 |
| **Total** | **0** | **99** | **18** | **10** | **127** |

## PRIORITIZED FIX LIST

### HIGH — must fix before ship

1. **84 dead bootcamp links** (workstream 2). Every `/bootcamps/<slug>/` page linked from theme pages returns 404; only `/bootcamps/threatlocker-assessment-prep/` survives. Slugs: acad-cloud, acad-cyber, acad-data, acad-forge, acad-math, acad-systems, ai-agent-sec, ai-lab, ai-product, alan-turing, aleks-ops-math, aws-clf, aws-cloud-practitioner-plus, aws-data, aws-dop, aws-saa, az-104, az-305, az-700, blockchain-dev, c-lang, cisco-ccna, cism, cissp, cka, ckad, comptia-a-plus, comptia-core, comptia-cyber, comptia-infra, comptia-network-plus, comptia-security-plus, cpp, data-analyst, data-analyst-to-ml, data-engineering, data-science-certs, datascience-ml, deep-learning, docker, dotnet, dp-203, dsa, embedded-interview, full-spectrum-dominance, fullstack, il12-ai-engineering, java, kubernetes-sre, linux-essentials, llm-engineering, m365, m365-endpoint-admin, math-tech, mongodb, neuroai, nlp-advanced, nlp-engineering, nvidia-ai, oracle-db, oracle-sql, pentest, platform-engineering, python, python-systems, python-web, quant-finance-ladder, quant-finance-math, react-frontend, rhce, rhcsa, sc-200, sc-300, secops-blue-team, soc-analyst, spring, sql, sre-platform, sre-practices, systems-cs, terraform, windows-admin, zero-trust, zerotrust.
   Options: (a) worker 301 stubs per consolidation plan Phase 2; (b) retarget theme links to `/bootcamp-catalog/` or surviving pages.
2. **EMPTY themes live (3):** Blockchain (hero + boilerplate only), Cybernetics (hero + boilerplate only), Om (zero courses; only generic "Adaptive Foundations" path; hero CTA points at il-23, not Om content). Source has content for Blockchain (1 course+1 bootcamp) and Cybernetics (2 courses) not yet deployed — deploy fixes 2 of 3. Om needs authored content or a "being built" decision.
3. **Competitor names in live course data (standing-rule violation):** Coursera in il-12, il-18, il-26, il-29 course JSONs + catalog shard-p; Pluralsight in il-29 (`"On Pluralsight, by Cisco"`, line 13957). All carry honest-framing disclaimers but still violate "no competitor names anywhere." Backup dirs (`.resbak-20261008/`, `*.diagbak`, `*.auditbak-20261009`, `*.groupc-bak`) inside the deployed tree duplicate the violations — remove from deploy.
4. **/jobs/ stale header nav:** custom 3-link masthead instead of canonical 6-item pillnav; one link points at folded `learn.interstitiumlabs.dev`. Replace with canonical fragment.

### MEDIUM — fix before ship if possible

5. **THIN themes live (7):** System Design (no Learning paths section), Networking (no paths), Programming (bootcamps only, no courses/paths live), Databases (bootcamps only live), Web Development (1 course), Cryptocurrency (no paths), Esoteric (no Bootcamps section). Source-vs-live drift: Programming, Databases, Blockchain, Cybernetics sources already have content sections (not yet deployed) — next deploy improves 4 themes.
6. **Wrong CTA on bootcamp catalog (medium):** "ThreatLocker Interview Prep → Start now" links to `/bootcamps/threatlocker-assessment-prep/`; the Interview Prep CBT lives at `/bootcamps/tl-interview/` (verified at `~/workspace/cert-bootcamps/site/bootcamps/tl-interview/`). Fix target in `docs/bootcamp-catalog/index.html` L35.
7. **21 MB autoplay hero video on homepage:** `docs/assets/chrome/hero-cinematic-loop.mp4` — mobile data risk; compress or add mobile variant.
8. **Course pages are JS-only shells:** crawlers/no-JS see an empty shell; OG edge injection is the only SEO/social surface (confirmed in run_worker_first).
9. **User-visible "coming soon" strings (3):** social login tooltip (`assets/il-account.js:203`), story voiceover (`university/js/il-stories.js:171`), course audio (`university/course-shell.js:3085,3150`). Replace or ship the features.
10. `/university/` header nav is JS-only (no nav with JS disabled). /bootcamp-catalog/ has no hero and no pillnav.
11. `/assets/cinematic/courses/` bare directory link on `university/index.html` → 404. Remove or retarget.

### LOW — polish

12. "1 courses" grammar ×5 on /topics/ (Networking, Databases, Linux & Systems, Web Development, Blockchain).
13. Topic tab strip inconsistency: `/topics/` shows 12 tabs (crypto, cybernetics, esoteric, om missing from strip but present as body cards); `/topics/cybersecurity/` shows all 16. Label mismatch "Mathematics (Turing)" vs "Mathematics".
14. course.html uses absolute URLs (brand, one Enroll button) vs relative everywhere else.
15. Footer label casing mixed (ABOUT/FOUNDERS/Topics/Courses/PREP) on /jobs/ and /bootcamp-catalog/ footers.
16. `docs/assets/topics/` has .bak files and unused `-new.mp4` variants (deploy bloat).
17. Udemy mention in `payment-routes.js:61` comment (in live `_worker.bundle.js:62`) — internal note, not user-visible, but lives in a served asset.

## WHAT IS HEALTHY (verified)

- All 9 key pages: hero ✓, header nav ✓ (except /jobs/), footer ✓ (identical canonical), viewport meta ✓. Zero broken/missing asset references across all pages. Zero placeholder images. No stub pages.
- Footers fully consistent sitewide (brand block + 7-link set identical on all 9 pages).
- Course page chrome consistent by construction (single `course.html` shell, `?course=` data-driven). IL-29 JSON valid with correct title; `data/courses/<cid>.json` fetch path correct.
- All 61 sampled assets (images, videos, CSS, JS) return 200 with correct content-type.
- Shortcut routes verified: /os→/topics/, /proof→/evidence/, /login /signin /member→/account/ 200, /il26 200, /il27 /il28 /il29→course pages 200, /labs/ /play/ /adapt/→/prep/drills/, /coach/→/noah/, /cinema→/topics/ (worker 301s).
- All 31 course JSONs have title, tagline, blurb, non-empty modules/paths. IL-19: 67 modules/3 paths; IL-26: 54/2; IL-28: 52/3; IL-29: 48/4.
- Known IL-07 double-description on /university/: resolved — zero duplicates.
- No duplicate hero copy across the 16 topic pages; no duplicate blurbs across 31 course JSONs.
- Zero hits for A Cloud Guru, Cloud Academy, The Cloud Bootcamp.
- No empty `<section>`s, no TODO/TBD in served HTML/JS.
- No global mobile bottom bar exists; mobile nav = canonical MENU `<details>` dropdown below 900px (zero-JS friendly). Course pages have section-tab bottom bars (Brief/Plan/Study/Labs/Mock/More) — by design.

## THEME TABLE (RICH 6 / THIN 7 / EMPTY 3)

| Theme | Slug | Status | Gaps |
|---|---|---|---|
| Cybersecurity | cybersecurity | RICH | none |
| Cloud & DevOps | cloud-devops | RICH | none |
| AI & ML | ai-ml | RICH | none |
| Data Engineering | data-eng | RICH | none |
| Linux & Systems | linux-systems | RICH | generic course title shared w/ Networking |
| Mathematics (Turing) | math | RICH | none |
| System Design | system-design | THIN | no Learning paths section |
| Networking | networking | THIN | no paths |
| Programming | programming | THIN (live) | no courses, no paths live (source has them — undeployed) |
| Databases | databases | THIN (live) | no courses, no paths live (source has them — undeployed) |
| Web Development | web-dev | THIN | 1 course |
| Cryptocurrency (XRP) | crypto | THIN | no paths |
| Esoteric (John Dee) | esoteric | THIN | no Bootcamps section |
| Blockchain | blockchain | EMPTY (live) | zero courses/bootcamps/paths live (source has 1+1 — undeployed) |
| Cybernetics | cybernetics | EMPTY (live) | zero courses/bootcamps/paths live (source has 2 courses — undeployed) |
| Om | om | EMPTY | zero courses in source; only generic "Adaptive Foundations" path; hero CTA points to il-23 |

## SOURCE-VS-LIVE DRIFT

- `_deploy_stamp.txt` says 20261007T110032Z; theme sources modified Oct 10 00:14. A single deploy of current source resolves: Blockchain and Cybernetics empties, Programming/Databases thins, most drift gaps.
- Om remains empty after deploy — needs a content decision.

## NEEDS RENDERED VERIFICATION (parent/root with live browser)

- Visual layout/overlap on all 9 pages; hero video playback; mobile breakpoints (Pixel, Legion, Philips).
- JS-rendered course page body; OG card injection on `?course=` URLs.
- `/bootcamps/` → `/bootcamp-catalog/` 301 display behavior.
- Nav text extraction omits header markup — live nav state not confirmed from fetches.

## DETAIL FILES

- Theme audit: `~/workspace/apex-audit/theme-category-audit-2026-10-10.md`
- Link sweep: `~/workspace/apex-audit/link-integrity-sweep-20261010.md`
- Layout audit scripts: `~/workspace/apex-audit/hidden_files/layout-audit-assets.py`, `layout-audit-links.py`
