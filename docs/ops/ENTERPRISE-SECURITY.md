# Enterprise security — Interstitium Labs (all builds)

**Single source of truth** for web, Cloudflare edge, PWA, Capacitor mobile, supply chain, and CI.  
**Domain:** `interstitiumlabs.dev`  
**Principle:** Security gates features. Do not ship convenience that weakens controls.  
**Honesty bar:** Controls below are mapped to OWASP ASVS / MASVS where they *actually apply*. Unmet items are labeled **gap** or **N/A**, not greenwashed.

| Surface | Detail doc |
| --- | --- |
| This file | Threat model, controls matrix, ASVS/MASVS, headers, CI |
| [MOBILE-SECURITY.md](./MOBILE-SECURITY.md) | Hybrid WebView MASVS detail |
| [_worker_security_headers.md](./_worker_security_headers.md) | Worker `solitary-sound-015a` header block |
| [STORE-PUBLISH.md](./STORE-PUBLISH.md) | App Store / Play (Enmanuel account steps) |
| [payments.md](./payments.md) | No Stripe secrets in client |
| [ANALYTICS.md](./ANALYTICS.md) | First-party only |

---

## 1. Threat model (STRIDE)

### 1.1 Assets

| Asset | Sensitivity | Location |
| --- | --- | --- |
| Learning OS static content | Public | `docs/` → Cloudflare + mobile `www/` |
| Local XP / progress | Low (integrity preferred) | `localStorage` / Preferences |
| Enroll Payment Link URLs | Public placeholders until live | `docs/enroll/config.js` |
| Stripe / PayPal **secrets** | Critical | Cloudflare secrets / operator vault — **never client** |
| Signing keystores / `.p8` / `google-services.json` | Critical | Operator machine / CI secrets — gitignored |
| Future auth tokens | High | Keychain / Keystore when auth exists |

### 1.2 Trust boundaries

1. Browser / PWA → first-party origin `https://interstitiumlabs.dev`
2. Capacitor native shell → WebView → same origin (+ localhost debug only)
3. Cloudflare Worker `solitary-sound-015a` / Workers Assets → static responses
4. CI (GitHub Actions) → repo contents; no production secrets in workflow logs

### 1.3 Adversaries & threats

| STRIDE | Example | Primary control |
| --- | --- | --- |
| Spoofing | Phishing deep link into WebView | `allowNavigation` host allowlist; App Links delayed until `assetlinks` |
| Tampering | Injected script / modified APK | CSP `script-src 'self'`; Play App Signing; minimize plugins |
| Repudiation | Fake “enrolled” client state | Hosted Stripe/PayPal checkout; client never holds secrets |
| Info disclosure | Secrets in git / APK | `.gitignore`, `scripts/security-check.sh`, placeholders-only configs |
| DoS | SW cache poisoning enroll config | `no-store` on `/enroll/config.js`; network-first HTML in SW |
| Elevation | Clickjacking / `file://` WebView | `X-Frame-Options: DENY` + `frame-ancestors 'none'`; cleartext off |

---

## 2. Controls matrix (web / PWA / iOS / Android / CI)

| Control | Web | PWA | iOS | Android | CI |
| --- | --- | --- | --- | --- | --- |
| HTTPS / HSTS | Cloudflare + header | Same | ATS strict | Cleartext false + NSC | N/A (egress to prod HTTPS) |
| CSP | `_headers` + meta backup | Same (+ `worker-src`/`manifest-src`) | Via bundled HTML | Via bundled HTML | N/A |
| COOP `same-origin` | Yes | Yes (SPA OK; OAuth popups later may need `same-origin-allow-popups`) | N/A native | N/A native | N/A |
| XFO DENY / frame-ancestors | Yes | Yes | Yes (HTML) | Yes (HTML) | N/A |
| No secrets in client | Placeholders only | Same | Same + Keychain later | Same + Keystore later | `security-check.sh` fail |
| Navigation allowlist | CSP + form-action | Same | Capacitor `allowNavigation` | Same + intent filter snippets | N/A |
| Dependency audit | N/A (static) | N/A | `npm audit` mobile | `npm audit` mobile | `security-audit.yml` fail-on-high |
| Secret pattern grep | — | — | — | — | `scripts/security-check.sh` |
| Tracker ban (GA/Meta/Hotjar) | Enforced by CSP + check | Same | No third-party SDKs by default | Same | Pattern scan |
| Signed release | Cloudflare edge | Same | Apple Distribution (operator) | Play App Signing (operator) | Debug APK optional only |

---

## 3. OWASP ASVS mapping (web / API-ish static — honest)

Target profile: **ASVS L1** for a mostly-static Learning OS + public Payment Links. L2 items called out where intentional gaps remain.

| ASVS (v4.x family) | Requirement (short) | Status | Evidence / gap |
| --- | --- | --- | --- |
| V1 Architecture | Document threat model | **Met** | This doc §1 |
| V2 Authentication | Auth controls | **N/A (now)** | No user auth yet; biometric flag OFF |
| V3 Session | Session mgmt | **N/A (now)** | No server sessions |
| V4 Access control | AuthZ | **Partial** | Admin UI is static operator console, not gated by real AuthZ — **gap** until auth |
| V5 Validation / sanitization | Input handling | **Partial** | Mostly static HTML; enroll UI escapes via textContent patterns; SPA still needs ongoing review |
| V6 Cryptography | Crypto at rest/transit | **Met (transit)** | TLS everywhere; no client-side crypto theater |
| V7 Error handling | Safe errors | **Partial** | Static site; no stack traces exposed by design |
| V8 Data protection | Sensitive data | **Met** | No secrets in `docs/`; gitignore keystores |
| V9 Communications | TLS | **Met** | HSTS + HTTPS-only mobile |
| V10 Malicious code | Supply chain | **Partial** | Lockfile + `npm audit` CI; no SBOM yet — **gap** |
| V11 Business logic | Abuse cases | **Partial** | Payments off-site; XP not entitlement |
| V12 Files | Upload | **N/A** | No user uploads |
| V13 API | API security | **Partial** | Future analytics ingest must auth/rate-limit — documented |
| V14 Config | Secure config | **Met** | `_headers`, Worker snippet, placeholders |
| V15 | (reserved / version drift) | — | — |

**Not claimed:** Full ASVS L2/L3 certification, formal pen-test report, or WAF custom ruleset beyond Cloudflare defaults.

---

## 4. OWASP MASVS mapping (mobile hybrid shell — honest)

Alignment target: **MASVS-L1** + selected L2 network/storage controls for Capacitor WebView. Detail: [MOBILE-SECURITY.md](./MOBILE-SECURITY.md).

| MASVS control group | Status | Notes |
| --- | --- | --- |
| MASVS-STORAGE | **Partial** | XP in WebView storage OK; future auth → Keychain/Keystore required |
| MASVS-CRYPTO | **N/A / transit** | No custom crypto; rely on platform TLS |
| MASVS-AUTH | **N/A (now)** | Push/biometric stubs OFF |
| MASVS-NETWORK | **Met (config)** | Cleartext denied; ATS strict; NSC sample under `apps/mobile/android-security/` |
| MASVS-PLATFORM | **Partial** | `allowNavigation` allowlist; deep links `autoVerify=false` until assetlinks |
| MASVS-CODE | **Partial** | Pinned Capacitor versions + audit; release hardening checklist for Enmanuel |
| MASVS-RESILIENCE | **Gap** | No root/jailbreak detection, no anti-tamper beyond store signing — acceptable for Learning OS v1 |
| MASVS-PRIVACY | **Met (default)** | First-party analytics only; no ad/tracker SDKs |

**Not claimed:** MASVS L2 resilience suite or independent lab certification.

---

## 5. Web / static headers (`docs/`)

### 5.1 Canonical files

| File | Role |
| --- | --- |
| [`docs/_headers`](../_headers) | Cloudflare Pages / Workers Assets |
| [`docs/ops/_worker_security_headers.md`](./_worker_security_headers.md) | Exact block + Worker wiring for **solitary-sound-015a** |
| [`docs/ops/snippets/cloudflare-worker-security-headers.js`](./snippets/cloudflare-worker-security-headers.js) | Copy-paste `applyEnterpriseSecurityHeaders()` |
| Meta CSP on key HTML | Backup when Worker headers lag |

### 5.2 Header set

| Header | Value (summary) |
| --- | --- |
| `Content-Security-Policy` | `default-src 'self'`; `script-src 'self'`; `style-src 'self' 'unsafe-inline' https://fonts.googleapis.com`; `font-src 'self' https://fonts.gstatic.com`; `img-src 'self' data: blob:`; `connect-src 'self'`; `worker-src 'self'`; `manifest-src 'self'`; `frame-ancestors 'none'`; `base-uri 'self'`; `form-action 'self' https://buy.stripe.com https://www.paypal.com`; `object-src 'none'`; `upgrade-insecure-requests` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` (+ Cloudflare Edge HSTS) |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()` |
| `X-Frame-Options` | `DENY` |
| `Cross-Origin-Opener-Policy` | `same-origin` |
| `Cross-Origin-Resource-Policy` | `same-origin` |
| `X-DNS-Prefetch-Control` | `off` |

### 5.3 CSP debt (documented, not theater)

| Directive | Current | Debt |
| --- | --- | --- |
| `script-src` | `'self'` only | Inline enroll/founders/insights UI extracted to `/assets/il-*-ui.js`. Do not reintroduce bare inline `<script>` without hashes. |
| `style-src` | `'unsafe-inline'` + Google Fonts | **Accepted debt.** Harden: self-host WOFF2 → drop Google Fonts → remove inline styles → drop `'unsafe-inline'`. |
| `connect-src` | `'self'` | When analytics ingest is live, allowlist that origin explicitly (never `*`). |
| Trusted Types | Off | Phase-2 Report-Only → enforce. |
| COOP | `same-origin` | If future OAuth popup breaks SPA, switch documented exception to `same-origin-allow-popups` — do not silently drop. |

### 5.4 Forbidden / removed

- `Grok App` branding, `/__grok/*`, `grok-preview-bridge`, `grok.com` host allowlists in shipped assets
- Third-party trackers (GA, Meta Pixel, Hotjar) unless explicitly approved + CSP + privacy disclosure
- Real `sk_live_` / `sk_test_` / webhook secrets under `docs/`

### 5.5 PWA

- `docs/manifest.webmanifest` — Interstitium Labs (not Grok)
- `docs/sw.js` — first-party; never durable-cache enroll config as secrets

---

## 6. Cloudflare Worker / edge (`solitary-sound-015a`)

1. Prefer `docs/_headers` for Workers Assets / Pages.
2. If a custom Worker fronts the site, wrap responses with `applyEnterpriseSecurityHeaders` — see [_worker_security_headers.md](./_worker_security_headers.md).
3. Dashboard: Always Use HTTPS + HSTS preload-ready.
4. Verify:

```bash
curl -sI https://interstitiumlabs.dev/ | grep -iE 'content-security|strict-transport|x-content|referrer|permissions|x-frame|cross-origin-opener'
```

Secrets (Stripe webhooks, analytics ingest): Cloudflare **Secrets** only.

---

## 7. Mobile (Capacitor) — summary

| Item | Value |
| --- | --- |
| appId | `dev.interstitiumlabs.app` |
| webDir | `www/` synced from `docs/` via `scripts/sync-mobile-web.sh` |
| allowNavigation | `interstitiumlabs.dev`, localhost |
| Android | `android-security/` NSC + cleartext off snippets |
| iOS | ATS strict (`NSAllowsArbitraryLoads` false) |
| Feature flags | `IL_FEATURE_PUSH=false`, `IL_FEATURE_BIOMETRIC_LOCK=false` |
| Supply chain | `engines.node >=18`, lockfile, `npm run audit` / `audit:ci` |

Full model: [MOBILE-SECURITY.md](./MOBILE-SECURITY.md).

---

## 8. Secrets & config hygiene

| Path | Rule |
| --- | --- |
| `docs/enroll/config.js` | Payment Link **placeholders** only until live URLs pasted; `paymentsLive: false` |
| `docs/analytics/config.js` | `endpoint` / `cloudflareBeaconToken` null until real |
| `.gitignore` | `*.pem`, `*.p8`, `*.jks`, `*.keystore`, `.env`, `google-services.json`, `GoogleService-Info.plist`, … |
| Local gate | `bash scripts/security-check.sh` |

---

## 9. Supply chain & CI

| Control | Location |
| --- | --- |
| Pin Capacitor deps + lockfile | `apps/mobile/package.json` + `package-lock.json` |
| `.npmrc` | `fund=false`, `audit=true` |
| `npm audit` fail-on-high | `apps/mobile` scripts + `.github/workflows/security-audit.yml` |
| Secret / tracker grep | `scripts/security-check.sh` (CI job `secret-patterns`) |
| Dependabot | `.github/dependabot.yml` |
| CODEOWNERS | `.github/CODEOWNERS` |

---

## 10. Residual risks (accepted with tracking)

| Risk | Mitigation path |
| --- | --- |
| Google Fonts + `style-src 'unsafe-inline'` | Self-host fonts; remove inline styles |
| Admin UI not AuthZ-gated | Operator-only knowledge; add auth before sensitive ops |
| Client XP editable | Non-entitlement; payments hosted |
| MASVS resilience (root detection) | Deferred — Learning OS v1 |
| iOS archive needs macOS | Enmanuel + Xcode; Linux CI documents only |
| SPA bundle historically had Grok preview bridge | Stripped; `security-check.sh` blocks reintroduction |

---

## 11. Pre-release checklist (all builds)

- [ ] `docs/_headers` present; curl verifies production headers
- [ ] Worker solitary-sound-015a applies same block (or Assets `_headers` sufficient)
- [ ] Cloudflare HSTS enabled
- [ ] Meta CSP present on key HTML as backup
- [ ] No Grok / `__grok` / third-party trackers in shipped pages/assets
- [ ] `bash scripts/security-check.sh` passes
- [ ] `cd apps/mobile && npm audit --omit=dev --audit-level=high` clean
- [ ] Mobile PUSH/BIOMETRIC still false unless approved
- [ ] Enroll placeholders or live Payment Links **without** secret keys
