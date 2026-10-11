# Codebase findings in sibling-owned files — DO NOT EDIT (audit 2026-10-08)

These files are owned by sibling workstreams this pass:
`docs/university/data/courses/*.json`, `docs/payment-routes.js`,
`docs/_worker.js`, `docs/university/academy.html`.
Issues found during review are recorded here with suggested fixes.

## 1. docs/_redirects — missing /il29 short slug (cosmetic)
- **File:** `docs/_redirects`, tail (after the `/il28` line)
- **Issue:** The 2026-10-07 short-slug block adds `/il26`, `/il27`, `/il28`
  but not `/il29`, while `docs/_worker.js` (code-level 301s) handles all four
  (`/il26`–`/il29`). The file's own comment notes `_redirects` is INERT in the
  API deploy path, so this is documentation-only today — but any non-API
  deploy path that honors `_redirects` would 404 `/il29`.
- **Suggested fix:** append
  `/il29     /university/course?course=il-29-threatlocker-ai-cybersecurity-mastery 301`
  (link values owned by sibling — left untouched by this audit).

## 2. docs/_worker.js — serveCourseWithOg does a full HTML rewrite per request (perf)
- **File:** `docs/_worker.js`, `serveCourseWithOg` (~line 1065 in the
  uncommitted diff)
- **Issue:** Every GET/HEAD to `/university/course` or `/university/course.html`
  does `await env.ASSETS.fetch(request)` + `await res.text()` + string replace
  and rebuilds the Response, with no caching. The injected bytes are identical
  for a given `?course=` id, so this is repeatable edge CPU on a hot route.
- **Suggested fix:** cache the injected Response in the Cache API keyed by the
  full URL (or restrict injection to known crawler UAs and serve the static
  asset untouched to browsers). `og:image:width/height` are hardcoded
  1200x630 — verified correct: all four course OG PNGs are now 1200x630
  (see codebase-audit.md § Performance).
- Verified OK: `ogEscape` covers `&<>"`; route condition
  (`/university/course` | `/university/course.html`) matches the
  `run_worker_first` entries in `flagship-deploy-config-20261007.json`;
  short-slug 301s `/il26`–`/il29` are all present at code level.

## 3. docs/university/academy.html — no issues
- Uncommitted diff reviewed: adds `IL-26`–`IL-29` entries to the course slug
  map. Clean; no action.

## 4. docs/payment-routes.js — not deep-reviewed (owned)
- `docs/_worker.bundle.js` (built from `payment-routes.js` + `_worker.js`)
  passes `node --check`. No findings.

## 5. docs/university/data/courses/*.json — no issues
- `il-26-data-analyst-certification-senior-mastery.json` read to verify
  `clickSims[].steps[].hotspots` shape: string arrays (e.g. `["A2:A7", "cell A2"]`).
  The renderer treats every hotspot as a valid target — consistent with the
  schema. If a `correct` hotspot index is ever added to the schema, the click-sim
  renderer (`il26_renderClickSim` in `course-shell.js`) will need a grading update.
