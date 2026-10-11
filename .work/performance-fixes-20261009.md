# Site-Wide Performance Fixes — 2026-10-09

All 5 bugs from `performance-bugs-sitewide-20261009.md` fixed and deployed.

## BUG 1: Noah scripts double-loaded (CRITICAL) — FIXED
- **Root cause:** `noah-full.js` injected capability modules without `data-noah-*`
  attributes; `noah-ai.js` auto-inject guards ran at its parse time (before the
  loader injected the modules), so voice/personas/adaptive each loaded twice —
  causing the duplicate Tutor/General rows, avatar pickers, color pickers, and
  mic buttons the user screenshotted.
- **Fix:**
  - `assets/noah-full.js`: sets `window.__noahFullLoader = true` before injecting
    anything; injected scripts now carry `data-noah-voice/personas/adaptive` attrs.
  - `assets/noah-ai.js`: all three auto-inject blocks now skip when
    `window.__noahFullLoader` is set.
- **Verified live:** `__noahFullLoader` in served noah-full.js; 3 guards in served
  noah-ai.js; no pages load noah-ai.js directly; all module files 200.

## BUG 2: 17 script requests on topic pages (MAJOR) — FIXED
- Created `assets/il-topic-bundle.js` (312KB, 15 deferred scripts concatenated in
  original order; syntax-checked).
- `il-theme.js` intentionally left separate — must run synchronously before first
  paint (sets `data-theme`, prevents FOUC).
- `noah-full.js` intentionally left separate (ordered capability loader).
- Updated 14 pages (12 topic pages + /topics/ + /cinema/): 17 requests → 3.

## BUG 3: Missing loading="lazy" (MAJOR) — FIXED
- Added `loading="lazy"` to 379 `<img>` tags across 188 HTML files.
- Skipped images with `fetchpriority` (above-fold heroes).

## BUG 4: Images missing width/height (MODERATE) — FIXED
- Added explicit width/height to 59 `<img>` tags (dimensions read from actual
  files via PIL/SVG parsing; template-placeholder srcs skipped).

## BUG 5: Canvas rAF running off-screen/hidden (MODERATE) — FIXED
- Created global rAF governor: wraps `requestAnimationFrame`/`cancelAnimationFrame`;
  queues callbacks while `document.hidden`, flushes on `visibilitychange`.
- Prepended to `assets/il-theme.js` (covers 190/193 pages); standalone
  `assets/il-raf-governor.js` added to the 3 pages without il-theme.js
  (rhel-fabric, pdf-library, cards).
- Note: `university/js/hero.js` pantheon canvas already had IntersectionObserver
  + visibility pausing from an earlier pass.

## Deploy
- Flagship `solitary-sound-015a` deployed twice:
  - 10:56:19Z — Noah double-load fix (urgent)
  - 10:58:00Z — all remaining fixes (etag d727b43a347a)
- All fixes verified live via curl after each deploy.
