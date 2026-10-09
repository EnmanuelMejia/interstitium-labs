# University Page Performance Fix — 2026-10-09

## Problem
/university/ page was slow when scrolling on mobile.

## Root Causes Found
1. **23 PNG posters** (120K each, ~3.5MB total) with no dimensions, no srcset
2. **Canvas rAF loop** kept scheduling frames even when off-screen (main thread saturation)
3. **No content-visibility** on cards (browser rendered all 23+ cards even off-screen)

## Fixes Applied

### 1. WebP Conversion (85% size reduction)
- Converted all 29 IL-*.png → IL-*.webp (640×360, ~18K each, was ~120K)
- Generated IL-*-hero.webp (1280×720, ~52K each) for course hero banners
- Updated `university/index.html`: poster template now uses `.webp` with `width="640" height="360"` + `decoding="async"`
- Updated `university/course-shell.js`: hero poster uses `-hero.webp` with `width="1280" height="720"` + `decoding="async"`

### 2. Canvas rAF Fix (`university/js/hero.js`)
- The `loop()` function was calling `requestAnimationFrame` unconditionally, even when `!st.visible`
- Fixed: when off-screen, sets `st.raf = 0` and `st.running = false` instead of scheduling next frame
- The existing IntersectionObserver already sets `st.visible = false` and calls `start(st)` when visible again

### 3. Content-Visibility
- `.card` in `university/css/il.css`: added `content-visibility: auto; contain-intrinsic-size: auto 300px;`
- `.il-story-card` in `university/css/il-stories.css`: added `content-visibility: auto; contain-intrinsic-size: auto 200px;`

### 4. Duplicate Scripts
- Verified: no duplicates exist. `noah-full.js` is the unified loader, no pages load individual noah-*.js files alongside it.

## Deployment
- Deployed `solitary-sound-015a` (etag `d727b43a347a`, 2026-10-09T10:53:45Z)
- Purged Cloudflare cache for WebP files (were 404-cached from pre-deploy)

## Verification (live)
- ✅ All WebP posters return 200
- ✅ All hero WebPs return 200
- ✅ Page returns 200
- ✅ WebP references in live HTML
- ✅ rAF fix in live hero.js
- ✅ content-visibility in live CSS files

## Files Changed
- `docs/university/index.html` (poster template)
- `docs/university/course-shell.js` (hero poster template)
- `docs/university/js/hero.js` (rAF loop fix)
- `docs/university/css/il.css` (.card content-visibility)
- `docs/university/css/il-stories.css` (.il-story-card content-visibility)
- `docs/assets/cinematic/courses/IL-*.webp` (29 new files)
- `docs/assets/cinematic/courses/IL-*-hero.webp` (29 new files)
