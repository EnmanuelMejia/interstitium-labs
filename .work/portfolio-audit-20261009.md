# Portfolio Site Audit — 2026-10-09 ~03:30 EDT

**User order:** "Audit portfolio site everything is crazy."
**Site:** https://enmanueldmejia.com
**Source:** ~/workspace/portfolio-site/
**Worker:** enmanuel-mejia

## Issues Found and Fixed

### 1. CRITICAL: 10 videos stacked in featured card (FIXED)
- The "Interstitium Labs" featured card contained all 10 project videos stacked vertically
- Root cause: widescreen deployment subagent did a bad find/replace, duplicating all videos into the featured card
- Fix: Removed all 10 `<div class="card-video">` blocks from the featured `<article>`
- Result: Featured card now 0 videos (clean text overview); each of the 10 project cards has exactly 1 video
- Deployed: enmanuel-mejia @ 2026-10-09T07:35:13Z
- Verified live: Card 0 = 0 videos, Cards 1-10 = 1 video each

## Verified Healthy

### Videos (10/10)
- All 10 widescreen MP4s return HTTP 200 at interstitiumlabs.dev/assets/cards/hq/hq-{slug}_16x9.mp4
- Spec verified (sampled il29, il28): 1280×720, h264, 24fps, 10.0s, AAC audio
- All 10 posters return 200, real file sizes (425K–910K, not black placeholders)

### Links (26/26)
- 25/26 return HTTP 200
- 1/26 returns 999 (linkedin.com/in/enmanuelmejia — LinkedIn bot-blocking, not a real issue)

### Images
- 4 images on page, all have alt text
- Portrait (64KB), lockup (16KB), sigil (5KB) — all 200, real sizes

### Code Quality
- No duplicate IDs
- JS syntax valid (node --check passed)
- No empty hrefs, no placeholder/lorem text
- Title and meta description present
- CSS is comprehensive (minified, ~23 lines but full coverage)
- Responsive breakpoints at 900px and 560px present
- Reduced-motion support present

### Structure
- 13 articles: 1 featured + 10 project cards + 2 eco cards
- 9 sections with clear hierarchy
- Deployed version matches local source (only diff is Cloudflare bot-challenge injection)

## Notes
- Portfolio references video/poster assets from interstitiumlabs.dev (cross-domain dependency, works fine)
- Videos use lazy-loading via data-src + IntersectionObserver pattern in app.js
- The il-topic-themes.css is loaded but portfolio doesn't use topic themes (harmless)
