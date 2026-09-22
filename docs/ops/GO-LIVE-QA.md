# Go-live QA — Interstitium Labs

**Date:** 2026-09-21 (America/New_York)  
**Repo SHA at QA authoring:** see git `main` after this commit  
**Custom domain / CNAME:** `interstitiumlabs.dev` (`docs/CNAME`)  
**Production edge:** Cloudflare Workers Assets (`solitary-sound-015a`) — **not** the same as a green GitHub Pages build

## Summary

| Area | Result | Notes |
|------|--------|-------|
| HTTP major Learning OS routes (repo) | **PASS** | Files present under `docs/` |
| HTTP live edge (`interstitiumlabs.dev`) | **FAIL (P0)** | CF Assets **stale** vs `main`: `/labs/`, `/labs/superlab/`, `/manifest.webmanifest`, `/sw.js`, `/assets/chrome/*`, `/assets/il-analytics.js`, `/assets/il-superlab.js`, `/assets/il-compat.*` → **404**; `/brand/` still serves **old** full kit (CF HIT) |
| Must-not-market `/brand/` | **PASS (repo)** / **FAIL (live)** | Repo stub → `/about/` + `noindex`; live still old kit until CF redeploy |
| `/ops/`, `/admin/` noindex | **PASS (repo)** | Meta + `_headers` `X-Robots-Tag`; `robots.txt` Disallow; **live** admin lacks noindex until redeploy |
| Enroll no live PLACEHOLDER buys | **PASS (repo)** | `paymentsLive: false`; UI = waitlist / enterprise empty state; PLACEHOLDER URLs never rendered as buy links |
| Enroll live edge | **FAIL (stale)** | Live still older “Stripe inactive” button UI |
| Broken internal links (static chrome) | **PASS** | Founders `/desk` → `/learn/`; SPA deep-link stubs + `404.html` added |
| SPA academy/desk deep links | **PASS (mitigated)** | Soft redirect stubs under `docs/academy/*`, `docs/desk/`, etc. |
| JS syntax (`il-game`, `il-i18n`, `il-analytics`, `il-compat`, …) | **PASS** | `node --check` clean; jsdom boot OK (i18n `fetch` needs browser) |
| Responsive CSS + viewport | **PASS** | `il-responsive.css` + `il-compat.css`; viewports on Learning OS pages; `overflow-x: clip` |
| i18n en/es | **PASS** | `/i18n/en.json` + `es.json` load on live; catalogs parse |
| `_headers` present | **PASS (repo)** / **FAIL (live)** | File present; **live responses lack CSP/HSTS/COOP** (Worker headers not applied) |
| Secrets in repo | **PASS** | `scripts/security-check.sh` PASSED; no `sk_live` / AWS keys |
| PWA manifest name | **PASS (repo)** | “Interstitium Labs” / short “Interstitium”; icons under `/assets/chrome/` |
| PWA live | **FAIL** | `manifest.webmanifest` + `sw.js` 404 on edge |
| SuperLab content + GitHub | **PASS (repo + GH)** | Page in repo; https://github.com/EnmanuelMejia/devops-superlab → **200** |
| SuperLab live | **FAIL** | `/labs/superlab/` 404 on edge until CF redeploy |
| `/coach/`, `/tutor/` | **N/A** | Not product surfaces; 404 expected |
| `/assets/chrome/*` | **PASS (repo)** / **FAIL (live)** | Icons relocated from `/brand/` |

## HTTP matrix (live curl, 2026-09-21 ET)

| Route | Live | Expected after CF sync |
|-------|------|------------------------|
| `/` | 200 | 200 |
| `/about/` | 200 | 200 |
| `/founders/` | 200 | 200 |
| `/learn/`, `/learn/skills/` | 200 | 200 |
| `/prep/` + prep children | 200 | 200 |
| `/paths/` + path children | 200 | 200 |
| `/labs/`, `/labs/superlab/` | **404** | **200** |
| `/play/` | 200 | 200 |
| `/enroll/`, `/enroll/success`, `/enroll/cancel` | 200 | 200 |
| `/brand/` | 200 (old kit) | stub → About |
| `/admin/` | 200 | 200 + noindex |
| `/ops/` | 404 (no index) | keep unlisted |
| `/sitemap.xml`, `/robots.txt` | 200 | 200 |
| `/manifest.webmanifest`, `/sw.js` | **404** | **200** |
| `/assets/chrome/*` | **404** | **200** |
| `/favicon.svg`, `/og.jpg` | 200 | 200 |

## Bugs fixed in this QA pass (in-repo)

1. **Founders “Open Desk”** pointed at `/desk` (404 on static edge) → `/learn/` with Learn label.
2. **SPA deep-link sprawl** (`/academy/*`, `/desk`, `/code`, …) → thin `noindex` redirect stubs into Learning OS URLs.
3. **Missing `docs/404.html`** → friendly Learning OS not-found page.
4. **Brand stub** → added viewport meta.
5. **`docs/ops/admin.md`** → explicit Worker Assets vs GitHub Pages sync / verify steps.
6. **This report** → `docs/ops/GO-LIVE-QA.md`.

Prior `main` commits already addressed: brand kit privatization, enroll waitlist empty-state, hreflang `"/>/>` fix, admin/ops noindex headers, chrome asset move, SuperLab pages, compat CSS/JS.

## Go-live blockers remaining (operator)

| Priority | Blocker | Action |
|----------|---------|--------|
| **P0** | Cloudflare Workers Assets out of date | Dashboard → `solitary-sound-015a` / Assets project → deploy `docs/` from `main`; confirm `/labs/superlab/` 200 |
| **P0** | Enterprise security headers absent on live | Ensure `_headers` honored by Assets **or** wrap responses with `applyEnterpriseSecurityHeaders` (see `_worker_security_headers.md`); `curl -sI` must show CSP + HSTS |
| **P1** | GitHub Pages `https_enforced: false` | Enable HTTPS enforcement on Pages custom domain (defense in depth; CF should terminate TLS) |
| **P1** | Payments inactive | Paste live Stripe/PayPal links; set `paymentsLive: true` only after test — **do not invent keys** |
| **P2** | Cloudflare Access not on `/admin/` | Configure Access in CF dashboard |
| **P2** | SPA hashed chunks still mention legacy IA | Needs app-source rebuild; stubs mitigate deep links |
| **P2** | CSP `style-src` Google Fonts + `unsafe-inline` | Accepted debt until self-hosted fonts |

## Redeploy path (no secrets invented)

```text
1. git push origin main   # this QA commit
2. Cloudflare dashboard → Workers & Pages → solitary-sound-015a (or bound Assets project)
3. Deploy / sync asset root = docs/
4. Verify:
   curl -sI https://interstitiumlabs.dev/labs/superlab/ | head
   curl -sI https://interstitiumlabs.dev/manifest.webmanifest | head
   curl -sI https://interstitiumlabs.dev/ | grep -iE 'content-security|strict-transport|x-frame'
5. Optional: purge CF cache for /brand/ /enroll/ /labs/*
```

**This agent cannot upload Worker Assets** (no Wrangler / CF API token in environment).

## Residual risks

- Dual publish (GH Pages + CF Assets) can diverge; treat CF as source of truth for go-live.
- Meta CSP on HTML is backup only; live currently relies on it for script policy while HTTP headers are missing.
- Mobile Capacitor `www/` may lag until `scripts/sync-mobile-web.sh` is re-run after this pass.
