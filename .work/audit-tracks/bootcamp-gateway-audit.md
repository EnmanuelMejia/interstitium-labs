# Track 8 — Bootcamp Gateway Audit
Date: 2026-10-08 ~21:30 EDT. Anonymous curl checks only (no cookies, no auth). Target: interstitium-course-gateway anonymous bypass for free bootcamps + the 2026-10-08 /bootcamps/_engine/* bypass and the /assets/il-brand.css + /assets/chrome/interstitium-logo.png fixes.

## Status table (all anonymous)

| # | URL | Status | Expect | Result |
|---|-----|--------|--------|--------|
| 1 | https://interstitiumlabs.dev/bootcamps/tl-interview/ | 200 | 200 | PASS |
| 2 | https://interstitiumlabs.dev/bootcamps/_engine/style.css (what the page's `../_engine/style.css` actually resolves to) | 200 | 200 | PASS |
| 3 | https://interstitiumlabs.dev/bootcamps/_engine/bootcamp.js | 200 | 200 | PASS |
| 4 | https://interstitiumlabs.dev/bootcamps/_engine/consoles.js | 200 | 200 | PASS |
| 5 | https://interstitiumlabs.dev/bootcamps/_engine/labs.js | 200 | 200 | PASS |
| 6 | https://interstitiumlabs.dev/bootcamps/_engine/learn.js | 200 | 200 | PASS |
| 7 | https://interstitiumlabs.dev/bootcamps/_engine/missions.js | 200 | 200 | PASS |
| 8 | https://interstitiumlabs.dev/bootcamps/_engine/simulations.js | 200 | 200 | PASS |
| 9 | https://interstitiumlabs.dev/bootcamps/_engine/terminal.js | 200 | 200 | PASS |
| 10 | https://interstitiumlabs.dev/assets/il-brand.css | 200 | 200 | PASS |
| 11 | https://interstitiumlabs.dev/assets/chrome/interstitium-logo.png | 200 | 200 | PASS |
| 12 | https://interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/ | 200 | 200 | PASS |
| 13 | https://interstitiumlabs.dev/bootcamps/ (index) | 401 | 401/303 gated | PASS — still gated by design |
| 14 | https://interstitiumlabs.dev/bootcamps/il-26/ | 401 | 401/303 gated | PASS — not over-opened |
| 15 | https://interstitiumlabs.dev/bootcamps/il-01/ | 401 | 401/303 gated | PASS — not over-opened |
| 16 | https://learn.interstitiumlabs.dev/bootcamps/tl-interview/ | 308 → https://interstitiumlabs.dev/bootcamps/tl-interview/ → 200 | 200 | PASS (redirect resolves to the live page) |
| 17 | https://interstitiumlabs.dev/bootcamps/tl-interview/_engine/style.css | 404 | n/a (page does not reference this path) | info — see note |
| 18 | https://interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/_engine/style.css | 404 | n/a (page does not reference this path) | info — see note |
| 19 | https://interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/engine/style.css | FLAKY: 000 (timeout) on 3 of 4 attempts; one attempt returned a 27,620-byte body | 200 | FLAG — intermittent reachability |
| 20 | https://interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/engine/bootcamp.js | 200 (single successful probe) | 200 | PASS (provisional) |

Notes on 17/18: both free pages reference engine assets RELATIVE to the page URL, not at `/bootcamps/<name>/_engine/*`. tl-interview uses `../_engine/*` → `/bootcamps/_engine/*` (all 200, rows 2–9). threatlocker-assessment-prep uses bare `engine/*` → `/bootcamps/threatlocker-assessment-prep/engine/*` (rows 19–20).

## Bypass verification
- Both free paths (/bootcamps/tl-interview/, /bootcamps/threatlocker-assessment-prep/) return 200 anonymously. PASS.
- The 2026-10-08 /bootcamps/_engine/* anonymous bypass is live: all 8 engine assets (style.css + 7 JS) return 200 anonymously. PASS.
- Previously-404 brand assets now 200: /assets/il-brand.css, /assets/chrome/interstitium-logo.png. PASS.

## Over-open check
- /bootcamps/ → 401 (empty body), /bootcamps/il-26/ → 401, /bootcamps/il-01/ → 401. The bypass did NOT over-open: paid/gated bootcamp paths still require auth. PASS.

## Injected masthead (styled-render check)
- tl-interview HTML contains the gateway-injected `<header class="il-site-masthead il-brand-masthead">` (brand link, logo img `/assets/chrome/interstitium-logo.png`, nav: Courses / Noah / Member sign-in / Membership) AND links `/assets/il-brand.css` in the head — that stylesheet returns 200, so the page will not render unstyled. PASS.
- threatlocker-assessment-prep HTML contains the same injected masthead (`il-site-masthead` found) and links `/assets/il-brand.css`. PASS.

## Findings / follow-ups
1. **INTERMITTENT**: `/bootcamps/threatlocker-assessment-prep/engine/style.css` (the relative engine path that page actually uses) timed out (curl exit 28, status 000) on 3 of 4 probes between ~21:24 and ~21:33 EDT; one probe returned a 27,620-byte body. Sibling `/bootcamps/threatlocker-assessment-prep/engine/bootcamp.js` returned 200 once. Later both this path AND the previously-200 `/bootcamps/_engine/style.css` timed out from this environment's egress, so part of the flakiness may be network-side. Re-verify from a different vantage; if it persists, the threatlocker page could load without its own engine CSS (its masthead CSS /assets/il-brand.css is unaffected).
2. Both pages' bootcamp-specific engine CSS resolves differently (tl-interview → shared /bootcamps/_engine/*; threatlocker page → per-bootcamp /bootcamps/threatlocker-assessment-prep/engine/*). Works as designed for now, but the shared-vs-per-page split is fragile — if one path's assets move, the pages silently degrade.

## 5-line summary
1. Both free bootcamps (tl-interview, threatlocker-assessment-prep) load anonymously at 200 — the anonymous bypass works.
2. The 2026-10-08 /bootcamps/_engine/* bypass is live: all 8 engine assets (style.css + 7 JS) return 200 anonymously.
3. The previously-404 brand assets now resolve: /assets/il-brand.css → 200, /assets/chrome/interstitium-logo.png → 200.
4. No over-opening: /bootcamps/ index → 401 and spot-checked /bootcamps/il-26/, /bootcamps/il-01/ → 401; gated paths remain gated.
5. Gateway-injected masthead is present and styled on both free pages; one caution — threatlocker page's own engine CSS (/bootcamps/threatlocker-assessment-prep/engine/style.css) was intermittently unreachable (timeouts on 3 of 4 probes) and needs re-verification.
