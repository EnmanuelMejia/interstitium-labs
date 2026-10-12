# Cloudflare Audit — 2026-10-09

Account: `T3ch49@outlook.com's Account` (`bb1baf6bc6c34d30fadc402b420fa3c2`)
Zone: `interstitiumlabs.dev` (`3f705489afbb4d6ed20b777e2d027047`) — active
Method: API via `cf-api` (dashboard was CAPTCHA-blocked)

## Fixes Applied

### 1. `/bootcamps/` 401 → FIXED ✅
**Problem:** `https://interstitiumlabs.dev/bootcamps/` returned 401. Root cause: the zone route
`interstitiumlabs.dev/bootcamps/*` → `interstitium-course-gateway` intercepted the request, and the
gateway worker 401s on index paths (it only serves individual bootcamp slugs like `/bootcamps/tl-interview/`).

**Fix:** Added exact route `interstitiumlabs.dev/bootcamps/` → `solitary-sound-015a` (route id `36adbfbb5c33477c9a0f695e7240af5b`).
Exact routes beat wildcards in Cloudflare's matching. The flagship worker already had redirect logic
(`/bootcamps/` → `/bootcamp-catalog/`).

**Verified:** `/bootcamps/` now 301 → `https://interstitiumlabs.dev/bootcamp-catalog/` ✅
Individual bootcamps (`/bootcamps/tl-interview/`) still 200 via gateway ✅

### 2. Auto Minify → ENABLED ✅
**Was:** css/js/html all `off`
**Now:** all `on`
Saves bandwidth on every HTML/CSS/JS response at the edge.

### 3. Security Level → MEDIUM ✅
**Was:** `essentially_off` (almost no challenge)
**Now:** `medium`
Better bot/abuse protection while staying invisible to normal users.

### 4. TLS Minimum → 1.2 ✅
Explicitly set minimum TLS 1.2 (was unset/default).

## Verified Already Good (no changes)

| Setting | Value | Status |
|---|---|---|
| SSL/TLS | `strict` (Full Strict) | ✅ correct |
| Cache level | `aggressive` | ✅ good for static assets |
| Brotli | `on` | ✅ |
| Early Hints | `on` | ✅ |
| HTTP/2 | `on` | ✅ |
| HTTP/3 | `on` | ✅ |
| Always Use HTTPS | `on` | ✅ |
| Apex domain | custom domain on `solitary-sound-015a` | ✅ correct |
| Bot Fight Mode | `off` | ✅ (leave off — can break legit crawlers) |
| Page Rules | none | ✅ (none needed; Workers handle routing) |
| Cache Rules | none | ✅ (worker sets cache headers; aggressive level covers the rest) |

## DNS — All Correct ✅

| Type | Name | Target | Proxied |
|---|---|---|---|
| AAAA | `interstitiumlabs.dev` | `100::` | yes |
| AAAA | `www.interstitiumlabs.dev` | `100::` | yes |
| AAAA | `api.interstitiumlabs.dev` | `100::` | yes |
| AAAA | `app.interstitiumlabs.dev` | `100::` | yes |
| CNAME | `learn.interstitiumlabs.dev` | `interstitium-labs-university.t3ch49.workers.dev` | yes |
| TXT | `interstitiumlabs.dev` | `v=spf1 include:_spf.mxvault.net ~all` | no |

`100::` is Cloudflare's discard prefix — standard for Workers-only setups. No stale records.

## Worker Routes — Full Map

| Pattern | Worker |
|---|---|
| `interstitiumlabs.dev` (custom domain) | `solitary-sound-015a` |
| `www.interstitiumlabs.dev/*` | `solitary-sound-015a` |
| `app.interstitiumlabs.dev/*` | `solitary-sound-015a` |
| `api.interstitiumlabs.dev/*` | `solitary-sound-015a` |
| `learn.interstitiumlabs.dev/*` | `solitary-sound-015a` |
| `interstitiumlabs.dev/bootcamps/` **(NEW)** | `solitary-sound-015a` |
| `interstitiumlabs.dev/bootcamps/*` | `interstitium-course-gateway` |
| `interstitiumlabs.dev/bootcamp/*` | `interstitium-course-gateway` |
| `interstitiumlabs.dev/assessments/*` | `interstitium-course-gateway` |
| `interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/*` | `interstitium-course-gateway` |
| `learn.interstitiumlabs.dev/assessments/*` | `interstitium-course-gateway` |
| `learn.interstitiumlabs.dev/bootcamp/*` | `interstitium-course-gateway` |
| `learn.interstitiumlabs.dev/bootcamps/*` | `interstitium-course-gateway` |
| `learn.interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/*` | `interstitium-course-gateway` |

**Note:** `learn.interstitiumlabs.dev/*` → `solitary-sound-015a` looks odd (DNS points learn to the
university worker via CNAME), but the more-specific gateway routes take precedence for their paths.
The university worker is served via the CNAME to `*.workers.dev`. This is working — no change made.

## Workers in Account (10 total)

All recently modified (Oct 2026), no stale workers found:
`cert-bootcamps`, `enmanuel-mejia`, `full-spectrum-bootcamp`, `interstitium-course-gateway`,
`interstitium-labs`, `interstitium-labs-university`, `interstitium-private-release`,
`solitary-sound-015a`, `threatlocker-assessment-prep-cbt`, `threatlocker-bootcamp`

## Open Items (need user or dashboard)

1. **`/assessments/` 401** — same gateway index issue as `/bootcamps/` was. Same fix pattern applies
   (add exact route → flagship) if the user wants it. Left alone for now since the user only asked about `/bootcamps/`.
2. **Dashboard CAPTCHA** — dash.cloudflare.com is behind a human-verification challenge. API works fine
   as an alternative for all settings audited here.
3. **WAF custom rules** — none configured. The free plan includes managed rules; none were added since
   the site is primarily static + Workers. Not urgent.
