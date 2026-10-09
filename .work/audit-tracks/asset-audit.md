# Asset Audit — Track 2 (site audit)

**Date:** 2026-10-08 ~21:30–22:10 EDT (audit-only; no code changed)
**Repo:** `~/workspace/apex-audit` (site source in `docs/`)

## Method
1. Fetched 9 key pages with `curl -sL` (all returned **200**).
2. Parsed each HTML for asset references: `<link rel=stylesheet|icon|manifest|preconnect|canonical|alternate>`, `<script src>`, `<img src|srcset>`, `<source srcset>`, `<video>/<audio>/<track>/<embed>` src, `og:image`/`twitter:image` meta, inline `url(...)` in styles.
3. Fetched all 19 stylesheets and extracted their `url()` / `@import` references (2nd-order assets).
4. `curl -sL` status-checked every unique asset URL (anonymous, `Mozilla/5.0` UA), recording final status.
5. Cross-checked interstitiumlabs.dev asset paths against the repo `docs/` tree.

Pages audited: `/` (apex), `/university/`, `/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery`, `/university/academy.html`, `/bootcamps/tl-interview/`, `/bootcamps/threatlocker-assessment-prep/`, `/enroll.html`, `https://enmanueldmejia.com/`, `https://app.interstitiumlabs.dev/`.

## Totals
- Unique URLs extracted: **115**
- Page links, not assets (hreflang `/enroll/?lang=xx` ×10, canonical ×4, self): 15 — all 200, excluded from asset count
- `<link rel=preconnect>` origins (bare origins, 404 by design — not assets): 2
- **Assets status-checked: 102** (100 from HTML + 2 from CSS deep-dive)
- **Broken (401/403/404/500): 0**
- **200 OK: 100 / 102**; the other 2 are the preconnect origins (expected 404, not broken)

## Known-fix verifications (all anonymous curl, no auth)
| URL | Prior | Now | Referencing page |
|---|---|---|---|
| `https://interstitiumlabs.dev/bootcamps/_engine/style.css` | 401 | **200** | /bootcamps/tl-interview/ |
| `https://interstitiumlabs.dev/bootcamps/_engine/bootcamp.js` | 401 | **200** | /bootcamps/tl-interview/ |
| `https://interstitiumlabs.dev/assets/il-brand.css` | 404 | **200** | /bootcamps/tl-interview/, /bootcamps/threatlocker-assessment-prep/ |
| `https://interstitiumlabs.dev/assets/chrome/interstitium-logo.png` | 404 | **200** | /bootcamps/tl-interview/, /bootcamps/threatlocker-assessment-prep/ |

All 4 verified HELD. (Also independently confirmed via text-fetch: style.css 599 lines, bootcamp.js 1419 lines, il-brand.css 52 lines all served real content; threatlocker-assessment-prep/engine/style.css also 200.)

## Notable spot-checks (all 200)
- All 13 other bootcamp-engine JS files (`consoles|labs|learn|missions|simulations|terminal.js` ×2 engines): 200
- All favicons/manifests/OG images (`favicon.png/svg`, `manifest.webmanifest` ×3, `og.jpg`, `il-29-threatlocker-og.png`, `noah-avatar.png`, `sigil-hero-static.png`): 200
- `hero-cinematic-loop.mp4` (apex + app host): 200
- Google Fonts css2 (Inter/JetBrains Mono/Space Grotesk) AND the IBM Plex css2 imported by `course-shell.css`: 200
- `university/css/il-hero.css` — found only via `@import` inside `il.css` (not in HTML link tags): 200, and it contains no further url() refs
- `enmanueldmejia.com` assets (`styles.css`, `app.js`, 5 webp portraits, `og-enmanuel-d-mejia`, `icon.webp`, manifest): 200
- `app.interstitiumlabs.dev` assets: 200 (host serves the apex site; its home HTML is near-identical to apex home)

## Broken list
**None.** Zero assets returned 401/403/404/500.

## Couldn't-check list
1. **JS runtime-loaded data** — `https://interstitiumlabs.dev/university/data/cert-index.json` and `…/university/data/courses/` are fetched at runtime by inline JS on the academy page (found via `fetch()` grep). Status not verified statically; needs a live browser session to confirm.
2. **Runtime-loaded bootcamp content** (e.g. `content.json` per bootcamp, course module JSON) — loaded by engine JS after page load; not statically extractable.
3. **Google Fonts via the text-fetch tool** — inconclusive through that path (Google's CSS endpoint needs a browser UA; the tool's fetcher got an upstream 500). Verified 200 via curl instead.
4. **SVG `url(#fragment)` references** inside `il.css`/`il-unified.css` (`#n`, `#scoreGrad`) — fragment refs, not fetchable assets; ignored.
5. Mid-audit the curl egress proxy blocked CONNECT to the sites (~35 min, then recovered); sweep ran after recovery. One `/tmp` scratch dir was wiped by the environment mid-run — work was redone under the persistent `.work/asset-scratch/` dir; results are from the complete final run.

## Repo cross-check (interstitiumlabs.dev)
All non-bootcamp CSS/JS/images/manifests exist in `docs/`. The 16 bootcamp engine files (`bootcamps/_engine/*`, `bootcamps/threatlocker-assessment-prep/engine/*`) are **not** in the repo `docs/` tree — they are live-served from a separate deploy path — but all 16 return 200 live, so nothing is broken. Flagging for the deploy track: engine sources are not in this repo.

## 5-line summary
- 102 assets status-checked across 9 key pages on 4 sites: 100 return 200 OK, 0 broken (no 401/403/404/500).
- The only non-200s were the 2 bare Google Fonts `preconnect` origins (404 by design — not assets, not a finding).
- All 4 known fixes verified held, anonymous: `bootcamps/_engine/style.css` + `bootcamp.js` (was 401), `assets/il-brand.css` + `assets/chrome/interstitium-logo.png` (was 404) — all 200.
- CSS deep-dive caught one hidden asset (`university/css/il-hero.css` via `@import`, 200) and the IBM Plex Fonts import (200); both fine.
- Gaps: runtime-JS-loaded JSON (`/university/data/cert-index.json`, `…/data/courses/`) couldn't be statically checked — needs a live browser pass; engine files live outside the repo `docs/` tree.
