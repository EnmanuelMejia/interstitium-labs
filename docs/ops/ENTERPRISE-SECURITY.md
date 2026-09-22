# Enterprise security — Interstitium Labs (all builds)

**Single source of truth** for web, Cloudflare edge, PWA, Capacitor mobile, supply chain, and CI.  
**Domain:** `interstitiumlabs.dev`  
**Principle:** Security gates features. Do not ship convenience that weakens controls.

| Surface | Detail doc |
| --- | --- |
| This file | Controls, headers, supply chain, CI gates |
| [MOBILE-SECURITY.md](./MOBILE-SECURITY.md) | OWASP MASVS hybrid shell threat model |
| [STORE-PUBLISH.md](./STORE-PUBLISH.md) | App Store / Play (Enmanuel account steps) |
| [payments.md](./payments.md) | No Stripe secrets in client |
| [ANALYTICS.md](./ANALYTICS.md) | First-party only |

---

## 1. Control objectives (enterprise baseline)

1. **Confidentiality** — no secrets in git or client binaries; Payment Links only.
2. **Integrity** — pinned deps, audit gate, signed store binaries (operator-held keys).
3. **Transport** — HTTPS everywhere; HSTS at Cloudflare; cleartext off on Android; ATS strict on iOS.
4. **Isolation** — CSP + `frame-ancestors`; WebView `allowNavigation` allowlist; no open redirects into shell.
5. **Privacy** — first-party analytics default; no third-party ad/tracker SDKs in native shell.
6. **Supply chain** — lockfiles, `npm audit` CI fail-on-high, Dependabot, secret scanning.

---

## 2. Web / static (`docs/`)

### 2.1 HTTP security headers (shipped)

Canonical file: **`docs/_headers`** (Cloudflare Pages / Workers static assets).  
Mirror the same values in any Worker (e.g. solitary-sound) via `response.headers.set(...)`.

| Header | Value (summary) |
| --- | --- |
| `Content-Security-Policy` | Default-src `'self'`; script-src `'self'`; style-src `'self' 'unsafe-inline' https://fonts.googleapis.com`; font-src `'self' https://fonts.gstatic.com`; img-src `'self' data: blob:`; connect-src `'self'`; frame-ancestors `'none'`; base-uri `'self'`; form-action `'self' https://buy.stripe.com https://www.paypal.com`; object-src `'none'`; upgrade-insecure-requests |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` (**also enable in Cloudflare SSL/TLS → Edge Certificates**) |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()` |
| `X-Frame-Options` | `DENY` (defense in depth with CSP `frame-ancestors`) |
| `Cross-Origin-Opener-Policy` | `same-origin` |
| `Cross-Origin-Resource-Policy` | `same-origin` |
| `X-DNS-Prefetch-Control` | `off` |

**CSP notes**

- `'unsafe-inline'` for **style** is required while Google Fonts CSS + inline `<style>` blocks exist. Hardening path: self-host fonts → drop `fonts.googleapis.com` / reduce inline styles → tighten `style-src`.
- **No `'unsafe-inline'` / `'unsafe-eval'` in `script-src`.** All first-party JS must be external files under `/assets/`.
- **Trusted Types:** not enforced yet (breaks many hybrid apps). Track as Phase-2: `Require-Trusted-Types-For 'script'` in Report-Only, then enforce after DOM sinks are audited.
- Stripe/PayPal checkout is **navigate** to hosted pages (`form-action` / top-level navigation), not script embeds.

### 2.2 SRI (Subresource Integrity)

| Resource | Policy |
| --- | --- |
| First-party `/assets/*` | Same-origin; integrity via deploy pipeline + HTTPS |
| Google Fonts CSS | **No stable SRI** (URL content changes). Prefer self-host WOFF2 under `/assets/fonts/` in a hardening sprint |
| Third-party **scripts** | **Forbidden by default.** If ever added, require `integrity=` + `crossorigin="anonymous"` + CSP hash/nonce |

### 2.3 Forbidden / remove

- `grok-project-id`, `grok:app_id`, `/__grok/*` references in shipped HTML
- Third-party trackers (GA, Meta Pixel, Hotjar, etc.) unless explicitly approved + CSP allowlisted + privacy disclosure
- Secrets (`sk_live_`, webhook secrets, keystores) anywhere under `docs/`

### 2.4 PWA

- `docs/manifest.webmanifest` — Interstitium Labs (not “Grok App”)
- `docs/sw.js` — network-first HTML; never durable-cache enroll config as secrets; first-party only

---

## 3. Cloudflare Worker / edge (solitary-sound & Workers Assets)

### 3.1 Static assets path

If the project serves `docs/` as **Workers Assets** or Pages:

1. Keep `docs/_headers` committed.
2. Cloudflare dashboard → SSL/TLS → enable **Always Use HTTPS** + **HSTS**.
3. Verify with `curl -sI https://interstitiumlabs.dev/ | grep -iE 'content-security|strict-transport|x-content|referrer|permissions|x-frame'`.

### 3.2 Worker header injection (solitary-sound / custom Worker)

Apply on **every** HTML (and preferably all) responses:

```js
function applyEnterpriseSecurityHeaders(response) {
  const headers = new Headers(response.headers);
  headers.set("Content-Security-Policy", [
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data: blob:",
    "connect-src 'self'",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self' https://buy.stripe.com https://www.paypal.com",
    "object-src 'none'",
    "upgrade-insecure-requests",
  ].join("; "));
  headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()");
  headers.set("X-Frame-Options", "DENY");
  headers.set("Cross-Origin-Opener-Policy", "same-origin");
  headers.set("Cross-Origin-Resource-Policy", "same-origin");
  headers.set("X-DNS-Prefetch-Control", "off");
  // Do not weaken: no Access-Control-Allow-Origin: * for credentialed APIs
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
}
```

**Operator:** paste into the solitary-sound Worker fetch handler (or Transform Rules → Modify Response Header) so edge matches `_headers`.

### 3.3 Secrets at edge

- Stripe webhook / analytics endpoints: Cloudflare **Secrets**, never `docs/`.
- Analytics beacon Worker: authenticate or rate-limit; no open CORS `*`.

---

## 4. Mobile (Capacitor) — summary

Full model: [MOBILE-SECURITY.md](./MOBILE-SECURITY.md).

- Bundle ID: `dev.interstitiumlabs.app`
- `allowNavigation`: `interstitiumlabs.dev` + localhost only
- Android: cleartext **off** + Network Security Config
- iOS: ATS strict (`NSAllowsArbitraryLoads` false)
- No keystores / FCM / `.p8` in git
- Push + biometric: feature flags **OFF** until auth + privacy labels

---

## 5. Supply chain

| Control | Location |
| --- | --- |
| Pin Capacitor deps | `apps/mobile/package.json` + lockfile after `npm install` |
| `.npmrc` | `fund=false`, `audit=true`, prefer lockfile |
| `npm audit` | `apps/mobile` scripts + CI fail on **high**+ |
| Dependabot | `.github/dependabot.yml` |
| CODEOWNERS | `.github/CODEOWNERS` (Enmanuel) |
| Secret scanning | GitHub secret scanning + push protection (enable in repo settings); never `--force` audit ignore |
| `.gitignore` | `*.jks`, `*.keystore`, `AuthKey_*.p8`, `google-services.json`, `GoogleService-Info.plist` |

---

## 6. CI gates

| Workflow | Gate |
| --- | --- |
| `docs/ops/snippets/github-workflows/security-audit.yml` | Copy to `.github/workflows/` — `npm audit --audit-level=high`; no `--force` |
| `docs/ops/snippets/github-workflows/mobile-android-debug.yml` | Optional debug APK; copy to `.github/workflows/` |
| Secret patterns | Refuse committing keystores; document gitleaks/trufflehog as optional local pre-push |

---

## 7. Residual risks (accepted with tracking)

| Risk | Mitigation path |
| --- | --- |
| Google Fonts CDN + `style-src 'unsafe-inline'` | Self-host fonts; remove inline styles |
| Trusted Types not enforced | Report-Only → enforce |
| Client XP editable | Non-entitlement; payments on Stripe hosted |
| iOS builds need macOS | Enmanuel + Xcode; Linux CI documents only |

---

## 8. Pre-release checklist (all builds)

- [ ] `docs/_headers` present; curl verifies headers on production
- [ ] Cloudflare HSTS enabled
- [ ] No `Grok App` / `__grok` / grok meta in shipped pages
- [ ] No secrets in `git status`
- [ ] `cd apps/mobile && npm audit --audit-level=high` clean
- [ ] Mobile flags PUSH/BIOMETRIC still false unless approved
- [ ] Enroll still Payment Link placeholders or live links **without** secret keys
