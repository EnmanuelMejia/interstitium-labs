# Site-Wide Consistency Audit — 2026-10-09 06:10 EDT

User order: "What else isn't working on every page"

Pages audited: `/`, `/il29`, `/il28`, `/il26`, `/university/`, `/topics/`, `/account/`, `/bootcamp-catalog/`, `/bootcamps/tl-interview/`, `/noah/`

---

## CRITICAL

### 1. Noah capability files not loaded on ANY page
- **Pages affected:** All (homepage, course pages, /noah/, /university/, /topics/, /account/)
- **What's broken:** `noah-voice.js`, `noah-personas.js`, `noah-adaptive.js` exist on the server (200) but ZERO pages reference them in HTML. The advertised 5 voices, 5 personas, and adaptive learning engine are not loaded anywhere.
- **Severity:** Critical
- **Note:** Separate task already assigned for Noah site-wide capabilities.

### 2. Course shim pages reference 404'd Noah scripts
- **Pages affected:** `/il29`, `/il28`, `/il26`
- **What's broken:** These pages include `<script src="js/noah.js">` and `<script src="js/il-noah-tutor.js">` (relative paths). Both return 404. Additionally, the course template references `noah-tutor.js` which 404s (only `noah-full.js` at 2.2KB exists).
- **Severity:** Critical (console errors, broken Noah on course entry pages)

### 3. Social login completely non-functional
- **Pages affected:** `/account/` (and any login flow)
- **What's broken:**
  - Account page shows ONLY email magic-link sign-in — zero social login buttons in the UI
  - `/auth/oauth/{github,google,linkedin}` all return **503**
  - `/api/auth/oauth/providers` returns all providers as `"configured": false`
- **Severity:** Critical (advertised feature does not work at all)
- **Root cause:** Provider OAuth apps/credentials never configured (known, needs user's action)

### 4. `/bootcamps/` returns 401
- **Pages affected:** `/bootcamps/` (direct access)
- **What's broken:** Returns 401 Unauthorized. The `/bootcamp-catalog/` workaround exists but the canonical path is broken.
- **Severity:** Major (known unresolved issue from prior audits)

---

## MAJOR

### 5. `/bootcamp-catalog/` lacks theme system
- **Pages affected:** `/bootcamp-catalog/`
- **What's broken:** No `il-theme.js` loaded. Uses hardcoded dark-ish inline styles (`#161b22`, `#58a6ff`) but doesn't respect the user's theme preference (light/dark toggle won't affect it).
- **Severity:** Major (theme inconsistency)

### 6. `/bootcamps/tl-interview/` lacks theme system
- **Pages affected:** `/bootcamps/tl-interview/` (and likely other bootcamp pages)
- **What's broken:** No `il-theme.js`. Has `il-site-theme` class and `color-scheme: dark` meta, but doesn't integrate with the site-wide theme toggle.
- **Severity:** Major

### 7. Bootcamp pages have no video elements
- **Pages affected:** `/bootcamps/tl-interview/`
- **What's broken:** Zero `<video>` tags found in the static HTML. Course videos may be JS-loaded, but no video cards visible in the initial render.
- **Severity:** Major (if videos are supposed to be visible)

### 8. Topics index doesn't showcase individual themes
- **Pages affected:** `/topics/`
- **What's broken:** Only generic `il-topic-heroes` / `il-topic-themes` classes found. The 12 distinct cinematic themes are not visibly differentiated on the index page in static HTML (may be JS-rendered, unverified).
- **Severity:** Major (user previously confused by this)

---

## MINOR

### 9. Homepage references "paywall" in code comment only
- **Pages affected:** `/` (line 510)
- **What's broken:** Nothing visible — just a code comment about "paywall gating." No visible lock badges or paywall UI found on any audited page. Beta free state appears correct.
- **Severity:** Minor (code hygiene only)

### 10. OG images use static PNGs (not video)
- **Pages affected:** All course pages (`/il29`, etc.)
- **What's broken:** `og:image` points to `/assets/cinematic/courses-og/IL-29-og.png` (static). This is standard for social previews (OG doesn't support video), not a bug — but noted per user's "everything dynamic" preference.
- **Severity:** Minor (platform limitation, not fixable)

---

## VERIFIED WORKING

- **Dark mode default:** All main pages (`/`, `/topics/`, `/account/`, `/il29`, `/il28`, `/il26`, `/university/`) load `il-theme.js` with dark default (`#0a0f1d`).
- **Navigation links:** All checked nav paths return 200 (`/learn/`, `/paths/`, `/enroll/`, `/noah/`, `/about/`, `/labs/`, `/play/`, `/cinema/`, `/jobs/`, `/adapt/`, `/coach/`, `/founders/`, `/evidence/`, `/progress/`).
- **Video audio:** All sampled HQ videos have AAC 24kHz audio tracks (voiceover confirmed).
- **Course content:** IL-29 (48 modules), IL-28 (52 modules), IL-26 (53 modules) JSON complete.
- **No visible paywall:** No lock badges found on any audited page. Beta free state is correct.
- **Homepage hero video:** Present with proper attributes (autoplay, muted, loop, playsinline).
- **Login redirects:** `/login/`, `/signin/`, `/member/` all 301 → `/account/` (verified in prior deploy).

---

## SUMMARY

| # | Issue | Severity | Pages |
|---|-------|----------|-------|
| 1 | Noah voice/persona/adaptive JS not loaded anywhere | Critical | All |
| 2 | Course pages reference 404'd Noah scripts | Critical | il29/il28/il26 |
| 3 | Social login 503, no UI buttons | Critical | /account/ |
| 4 | `/bootcamps/` returns 401 | Major | /bootcamps/ |
| 5 | `/bootcamp-catalog/` no theme system | Major | /bootcamp-catalog/ |
| 6 | Bootcamp pages no theme system | Major | /bootcamps/*/ |
| 7 | Bootcamp pages no video in static HTML | Major | /bootcamps/*/ |
| 8 | Topics index doesn't showcase themes | Major | /topics/ |
| 9 | Paywall code comment only | Minor | / |
| 10 | OG images static (platform limit) | Minor | All courses |
