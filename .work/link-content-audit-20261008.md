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

## Still running
- Internal link crawler: COMPLETE. 882 URLs checked across 3 sites. Result: **zero real broken internal links** (326 initial flags were all crawler artifacts: og:type meta parsing, meta-description text in URLs, POST-only /api/waitlist, auth-gated /bootcamps/, and transient timeouts — all verified clean on recheck).
- Video resource expansion worker.
- Story supplements worker.
- Final re-crawl + verification after all workers complete.
