# Link + Content + Brand Audit — 2026-10-08

## The 404 he hit
`/devops-superlab` → 404. The 404 page itself lists "DevOps SuperLab" as a live surface (linking to `/labs/superlab/`), but no redirect existed for the `/devops-superlab` path users would type (the GitHub repo is named devops-superlab).
**Fixed:** code-level 301 `/devops-superlab` → `/labs/superlab/` in `_worker.js` STUB_REDIRECTS + added to `run_worker_first`. Verified live: 301 → https://interstitiumlabs.dev/labs/superlab/.

## Link findings + fixes
1. **`/bootcamps/tl-interview/` → 401 for anonymous.** Portfolio presents it as "Try it live" for the "ThreatLocker Interview Test Bootcamp" which the portfolio copy describes as "**A free**, fully interactive bootcamp" — the membership gate was a misconfiguration. **Fixed:** added `/bootcamps/tl-interview/*` to the gateway's anonymous bypass (same as threatlocker-assessment-prep). Verified live: 200 anonymous. `/bootcamps/` (index) still 401 by design (members product).
2. **Portfolio link wrong target:** "ThreatLocker Assessment Prep CBT" card's "Explore the course" pointed to `/bootcamps/tl-interview/`; now points to `/bootcamps/threatlocker-assessment-prep/` (matches its description + Source repo). Deployed.
3. OG images: all 7 serve 200; crawler OG injection verified for IL-29 (LinkedInBot UA).
4. Paywall intact: IL-01/IL-26 → 402, IL-27/28/29 → 200.

## Content depth (multicloud AI template)
- All 29 courses: 0 thin modules (avg ~2000+ words/module), labs/drills/cards/quiz at 100%.
- Prereq math present in all courses (IL-20 IS the math course).
- Cert mapping: all courses mapped except IL-20/21/22/23 — re-verified no matching accredited certification exists; added honest `_noCertNote` + certifications entries (following IL-01 pattern).
- **mockTask gap fixed:** IL-16..IL-25 had 4-20% mockTask coverage → 275 mockTasks added, now 100% (IL-27's 6 FT interview-prep modules intentionally excluded — wrong archetype).
- **Video expansion (in progress):** IL-01..IL-15 had 0 videos; IL-16..IL-25 had 2-3 each. Worker adding HTTP-verified videos per module.

## Brand consistency
- **Logo:** university header/footer used `assets/sigil.svg` (different artwork) → now `/assets/chrome/sigil-glyph.svg` (canonical). Checkout header used text "IL" div → now logo image.
- **Tagline:** university header said "LEARNING UNIVERSITY" → now "SCIENTIA OMNIA VINCIT".
- **Theme tokens (direct clone of multicloud):** il-unified.css `--paper` #0a0f1d→#06080c, `--gold` #d2a53f→#c9a227, `--cyan` #7ed4e0→#62d8e9. Portfolio styles.css `--void`→#06080c, `--gold`→#c9a227, `--cyan`→#62d8e9. Verified live.
- **Hero:** EXEMPT per user — untouched (verified: hero uses --gold-rgb + hardcoded values, not the changed tokens).
- **Background:** green wavy aurora REMOVED everywhere per user (was on 58 pages; briefly extended then fully reverted). All pages consistently dark.
- Dark-mode default preserved; light remains opt-in.

## Deploys
- Main worker solitary-sound-015a: deployed (includes _worker.js redirect, brand fixes, token alignment, course JSON updates pending video/mockTask worker).
- Gateway interstitium-course-gateway: deployed (tl-interview bypass).
- Portfolio enmanuel-mejia: deployed (link fix, token alignment).
- learn.interstitiumlabs.dev: alias, inherits main.

## Completed this pass
- Link fixes: /devops-superlab 301, tl-interview free bootcamp bypass, portfolio course link.
- Brand: canonical logo + tagline sitewide.
- Theme: multicloud tokens cloned; aurora removed per user; hero animated block untouched.
- Content: mockTask backfill (275), no-cert notes for IL-20/21/22/23.
- Link audit: 882 URLs checked — zero real broken internal links.
- Committed as 059f2a1.

## Completed — video finish-up (worker done ~18:21 EDT)
- 804/804 modules now have HTTP-verified videos (was 604/804). All 200 gaps filled, zero gaps.
- Committed + deployed (solitary-sound-015a, etag db308c5dcd02, 2026-10-08T22:42:39Z).

## Final live verification (2026-10-08 ~18:43 EDT)
- /devops-superlab → 301 (both interstitiumlabs.dev and learn.interstitiumlabs.dev)
- /bootcamps/tl-interview/ → 200 anonymous
- /bootcamps/threatlocker-assessment-prep/ → 200
- /university/course?course=il-29 → 200

## New directives 2026-10-08 ~18:02–18:07 EDT (workers spawned)

### Footer blur audit (done by coordinator)
- **Finding: NO CSS blur bug exists.** Audited all stylesheets: only `filter: blur(2px)` instances are on `.il-nebula` (intentional background decoration). No blur on footers, headers, text, or logos anywhere. The blur in his photo was likely camera focus, not a code bug.
- Headers/chrome also checked — same result, no blur bugs.

### Workers running
1. **Footer standardization** — replacing all footers with canonical centered layout (logo, INTERSTITIUMLABS.DEV, SCIENTIA OMNIA VINCIT, CREATED BY INTERSTITIUM LABS, nav rows, language selector).
2. **Animations** — IntersectionObserver-gated, prefers-reduced-motion respected, performance-disciplined.
3. **Student resources** — cheat sheets, drill packs, glossaries, verified external refs, FAQ per course.
4. **Progress tracking** — canonical IL-01→IL-29 sequence, localStorage progress, "Continue where you left off", cross-course flow.

After all complete: commit → deploy → re-crawl → verify → report.

## Completed — story supplements (worker done ~17:35 EDT)
- 104 "The story behind X" narrative supplements across all 29 courses (3.6 avg/course).
- Stored: docs/university/data/courses/stories/<course>-stories.json (29 files) + _index.json.
- Integration note: .work/story-supplements-INTEGRATION.md (player wiring not yet implemented — join contract specified).
- Format: reel-style (human moment → real history → present connection → lesson bridge), 300-600 words, verifiedClaims audit trail per story. Reel text never copied.
- Historical gaps honestly hedged, not invented (Google first A/B test 2000 unverified → used 41-shades; Bezos mandate ~2002 secondhand; etc.).
