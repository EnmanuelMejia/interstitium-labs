# Inline Everything — 2026-10-09

**User order (2026-10-09 ~02:13 EDT):** "Inline everything in PDF library as well inline all animated media and video animations such as the sample from Instagram in the thousands nothing should be obfuscated no subject matter or content should be empty"

**Coordinator session:** 493a3307-95eb-4f90-b3c8-a78f125aca36

**CRITICAL CORRECTION (2026-10-09 ~02:15 EDT):** User: "All media should be animated and dynamic not static remember new standard approach."
- PDF previews → animated page-flip cycling (IntersectionObserver, one card animates at a time), NOT static iframes.
- Video embeds → Instagram/TikTok-style autoplay muted previews on scroll into view, tap to unmute + controls. `prefers-reduced-motion` respected (no autoplay, show poster + play button).
- Both media workers updated via subagent.send; correction acknowledged pending application.

## Workstreams (3 parallel workers dispatched 2026-10-09 ~02:14 EDT)

### 1. PDF Library Inline — agent 08316336
Status: dispatched, pending.
Scope: Rebuild /pdf-library/ so all 241 PDF cards show inline previews (lazy-loaded iframes, click-to-expand full inline viewer).

### 2. Animated Media Inline — agent 7ee0b30c
Status: dispatched, pending.
Scope: Audit + fix inline <video> playback across course player, bootcamp engine, portfolio, PDF library cross-links.

### 3. Completeness Audit — agent 5988c1f8
Status: dispatched, pending.
Scope: Find and fill every empty/thin/placeholder content across courses, bootcamps, site pages, portfolio.

---

## PDF Library Inline

_(worker to append)_

## Animated Media Inline

_(worker to append)_

## Completeness Audit

_(worker to append)_

## Final verification

_(coordinator to complete after all workers report)_

## PDF Library Inline
_2026-10-09 ~02:20 EDT — subagent worker_

**User correction applied (02:15 EDT):** "All media should be animated and dynamic not static" — static iframe previews were REPLACED with animated auto-cycling previews. No static previews remain.

### What changed — `docs/pdf-library/index.html` (241 cards, 12 categories, TOC untouched)
- Each card now carries a `.pdf-preview` block with ONE iframe that **auto-cycles pages 1–4 every 2.5s** with a 280ms fade transition — the step-through-animation feel the guides were designed for. Clickable pager dots (1·2·3·4) jump to any of the 4 pages manually.
- **One-at-a-time animation:** a second IntersectionObserver keeps a ratio map of visible previews; only the most-visible card (intersectionRatio > 0.3) cycles. A pulsing green LIVE dot marks the animating card. Cycling pauses when the tab is hidden (`visibilitychange`).
- **Lazy loading:** iframe `src` is set from `data-src` only when the card nears the viewport (400px rootMargin IO) + native `loading="lazy"`. Cards outside the viewport hold no PDF download at all.
- **Expand modal:** ⤢ Expand button opens the full PDF inline in a full-screen-ish modal (no new tab, no download); Esc/backdrop/✕ closes and clears the frame src. Modal bar also has Download.
- Per-card actions: `Read the guide` (kept, original style) + secondary `Download` link (`download` attr, same-origin so it forces save).
- New live search box under the lede filters cards/descriptions/categories; empty grids + their H2 headers hide.
- Dark-theme consistent (site `il-unified.css`); responsive (modal 97%/96vh, preview 240px on ≤640px).
- Transform script: `.work/pdf-inline-transform.py` (rev 2); backup of pre-transform file: `.work/pdf-library-index.html.bak-20261009`. JS passed `node --check`.

### Deploy — flagship path
- `~/workspace/skills/cloudflare/bin/deploy-worker-assets ~/workspace/apex-audit/.work/flagship-deploy-config-20261008.json`
- Result: `deployed solitary-sound-015a etag=95acb862e03f modified=2026-10-09T06:18:18.04002Z` — manifest 1761 files, 106 changed uploaded (incl. rebuilt index.html).

### Live verification (curl)
- `https://interstitiumlabs.dev/pdf-library/` → **HTTP 200**, 228,645 bytes; 241× `class="pdf-preview"`, 241× `data-src="/assets/pdfs/"`, cycle JS present, modal present.
- Sample asset `https://interstitiumlabs.dev/assets/pdfs/bbg-jwt.pdf` → **HTTP 200**, `application/pdf`, 13,573 bytes.
- `/pdf-library` (no slash) → 307 → `/pdf-library/` (normal auto-trailing-slash).

### Caveats
- Page-fragment cycling (`#page=N` swaps on the iframe src) relies on the browser's built-in PDF viewer — solid on Chrome/Edge/Firefox desktop and Android Chrome; iOS Safari's iframe-PDF support is inconsistent, where users fall back to `Read the guide`. Could not live-browser-test the animation (subagent has no live browser); parent may want one visual pass.
- `_t.pdf` (242nd file on disk) is not referenced by the page — excluded per brief.
