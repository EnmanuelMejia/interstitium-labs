# Enterprise audit — Interstitium Labs (Learning OS)

Date: 2026-09-21 (America/New_York). Operator path; `robots.txt` disallows `/ops/`.

## Findings → remediations (this pass)

| Area | Finding | Remediation |
|------|---------|-------------|
| Brand privacy | Public `/brand/` kit, marks gallery, campaign plates, guidelines | Masters live under local `private/brand/` (gitignored blobs); public chrome slimmed to `docs/assets/chrome/`; `/brand/` stub → `/about/` with `noindex`; stripped Brand nav/i18n; sitemap/robots/headers updated |
| Enroll | `paymentsLive: false` risked placeholder checkout UX | Enterprise empty-state: “Registration opening soon” + waitlist `mailto:edmejia@pm.me`; placeholder Stripe/PayPal URLs never rendered as buy buttons |
| Admin / insights | Operator surfaces indexable | `noindex` meta + `X-Robots-Tag` via `_headers`; Operator-only banner; **recommend Cloudflare Access** (not configured in-repo — no invented Access config) |
| Home / nav IA | Footer SPA link sprawl; public mark-system section | Slim Learning OS IA (About, Founders, Learn, Prep, Paths, SuperLab, Enroll); removed public mark-kit section |
| SuperLab | Flagship lab at `/labs/superlab/` | Linked from home featured tracks, nav, footers, sitemap |
| Security headers | `_headers` present | Confirmed CSP/HSTS/frame denial; `/admin/*`, `/brand/*`, `/ops/*` noindex; ops/brand disallows in robots |
| Copy | Public “Mark system” / brand kit CTAs | Removed from home/about |

## Residual risks
1. **Payments off** — `docs/enroll/config.js` keeps `paymentsLive: false`. No invented Stripe keys. Waitlist CTA only until operator pastes live Payment Links.
2. **Cloudflare Access not configured** — `/admin/` and `/ops/` remain URL-reachable. Set Access policies in the Cloudflare dashboard before treating them as confidential.
3. **Workflow / CI scope** — GitHub Actions secrets and Worker bindings are out of band; this pass does not invent secrets or widen workflow permissions.
4. **CSP `style-src` debt** — still allows `https://fonts.googleapis.com` + `'unsafe-inline'` until fonts are self-hosted.
5. **Brand blob storage** — `private/` is gitignored so full-res masters are **not** on the public GitHub remote. Operators must back up the local vault (or a separate private store). Only `private/brand/README.md` is tracked.
6. **SPA route sprawl** — hashed SPA chunks may still expose desk/academy/etc. routes; static chrome IA was slimmed. Full SPA IA cleanup needs an app-source rebuild.
7. **`_imports/` prose** — some curriculum pages mention import paths for provenance; not linked as a UI kit; robots-disallowed.

## Honesty banners
Keep existing honesty copy (portfolio SuperLab, study-path ≠ employment). Do not invent tenure or live payments.
