# Site-Wide Performance Bug Audit — 2026-10-09

**Scope:** Homepage, /university/, /account/, /noah/, /topics/ + 12 topic pages,
/il29, /il28, /il26, /bootcamp-catalog/, 3 bootcamp pages
**Method:** Static HTML analysis via curl + source code inspection
**Note:** Audit only — no fixes applied.

---

## BUG 1: Noah scripts loaded TWICE on every page (CRITICAL)

**Affected:** All 179 pages using `noah-full.js` (entire site)

**Root cause:**
- `noah-full.js` dynamically injects `noah-ai.js`, `noah-voice.js`,
  `noah-personas.js`, `noah-adaptive.js` — WITHOUT `data-noah-*` attributes
- `noah-ai.js` (lines 1300-1324) ALSO auto-injects those same 3 files, with
  guards checking `!document.querySelector('script[data-noah-voice]')` etc.
- Since `noah-full.js` doesn't set the data attributes, the guards don't fire
- Result: `noah-voice.js`, `noah-personas.js`, `noah-adaptive.js` each load TWICE

**Impact:**
- 3 redundant JS downloads + parses on every page load (~80KB wasted)
- Potential double-initialization of voice/persona/adaptive modules
- Race conditions from competing module initializations

**Fix:** Add `data-noah-voice`, `data-noah-personas`, `data-noah-adaptive`
attributes in `noah-full.js` when injecting, OR remove auto-inject from
`noah-ai.js` when loaded via `noah-full.js`.

---

## BUG 2: 17 separate script requests on topic pages (MAJOR)

**Affected:** /topics/ + all 12 topic pages

**Details:** Each topic page loads 17 individual JS files:
il-theme, il-scene-kit, il-pwa, il-noah-avatar, il-muse, il-motion,
il-model-router, il-model-panel, il-model-analytics, il-i18n, il-game,
il-compat, il-coach, il-challenge, il-analytics, analytics/config, noah-full

**Impact:** 17 HTTP requests just for JS on every topic page load.
No bundling = slow on mobile/high-latency connections.

**Fix:** Bundle into 2-3 files (core + features + noah).

---

## BUG 3: Missing `loading="lazy"` on images site-wide (MAJOR)

**Affected:** Nearly every page audited

| Page | Images without lazy |
|------|-------------------|
| /topics/ | 15/15 |
| Homepage | 3/4 |
| /university/ | 3/4 |
| /noah/ | 3/3 |
| /account/ | 2/2 |
| All 12 topic pages | 2/2 each |
| /il29, /il28, /il26 | 2/2 each |
| Bootcamp pages | 1/1 each |

**Impact:** All images load immediately, competing with critical resources.
Slows initial page load, especially on mobile.

**Fix:** Add `loading="lazy"` to all below-fold images.

---

## BUG 4: Images missing width/height (MODERATE)

**Affected:**
- Homepage: 1/4 images
- /university/: 1/4 images
- /topics/: 1/15 images

**Impact:** Layout shift (CLS) as images load. Hurts Core Web Vitals.

**Fix:** Add explicit width/height to all <img> tags.

---

## BUG 5: Continuous canvas animations (MODERATE)

**Pages with <canvas>:** /noah/, /university/, /university/lab-generative-packing.html

**JS files with requestAnimationFrame:** 10 files including il-motion.js,
il-fx.js, il-game.js, il-immersive.js, il-noah-avatar.js

**Impact:** Canvas animations run continuously even when off-screen or when
tab is backgrounded, draining battery and saturating main thread during scroll.
The /university/ "AI Pantheon" canvas was specifically flagged as causing
2.35s scroll settle times.

**Fix:** Pause rAF loops when canvas is off-screen (IntersectionObserver)
and when document is hidden (visibilitychange).

---

## BUG 6: PNG posters (already fixed)

**Status:** WebP versions exist (58 files) and /university/ already references
`.webp` in its JS template. No action needed.

---

## Summary by page

| Page | Bugs found |
|------|-----------|
| Homepage (/) | BUG 1, BUG 3, BUG 4 |
| /university/ | BUG 1, BUG 3, BUG 4, BUG 5 |
| /noah/ | BUG 1, BUG 3, BUG 5 |
| /topics/ + 12 topics | BUG 1, BUG 2, BUG 3 |
| /account/ | BUG 1, BUG 3 |
| /il29, /il28, /il26 | BUG 1, BUG 3 |
| /bootcamp-catalog/ | BUG 1 only (clean otherwise) |
| Bootcamp pages | BUG 1, BUG 3 |

**Highest priority:** BUG 1 (affects all 179 pages, wastes bandwidth on every load)
