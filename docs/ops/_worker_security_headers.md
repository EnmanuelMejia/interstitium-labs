# Cloudflare Worker security headers — solitary-sound-015a

**Worker name (canonical):** `solitary-sound-015a` (also referenced as solitary-sound)  
**Keep in sync with:** [`docs/_headers`](../_headers) · [`ENTERPRISE-SECURITY.md`](./ENTERPRISE-SECURITY.md) §2–3 · [`snippets/cloudflare-worker-security-headers.js`](./snippets/cloudflare-worker-security-headers.js)

Use this when Workers Assets / Pages `_headers` are delayed or the site is fronted by a custom Worker. Paste the helper into the Worker module and wrap every response.

## Exact header block

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; worker-src 'self'; manifest-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self' https://buy.stripe.com https://www.paypal.com; object-src 'none'; upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()
X-Frame-Options: DENY
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
X-DNS-Prefetch-Control: off
```

## Worker snippet (copy-paste)

```js
import { applyEnterpriseSecurityHeaders } from "./snippets/cloudflare-worker-security-headers.js";
// or inline the function from that file

export default {
  async fetch(request, env, ctx) {
    const response = await env.ASSETS.fetch(request);
    return applyEnterpriseSecurityHeaders(response);
  },
};
```

Full helper: [`snippets/cloudflare-worker-security-headers.js`](./snippets/cloudflare-worker-security-headers.js).

## COOP note

`Cross-Origin-Opener-Policy: same-origin` isolates the browsing context. For this static Learning OS + PWA it is desired. If a future OAuth popup flow breaks, document the exception and temporarily use `same-origin-allow-popups` — do not silently drop COOP.

## CSP debt (honest)

| Directive | Current | Debt / harden path |
| --- | --- | --- |
| `script-src` | `'self'` only | Inline enroll/founders/insights scripts extracted to `/assets/il-*-ui.js`. Do **not** reintroduce inline `<script>` without hashes. |
| `style-src` | `'self' 'unsafe-inline' fonts.googleapis.com` | **Accepted debt:** Google Fonts CSS + inline `style=` / `<style>`. Harden: self-host WOFF2 → drop Google Fonts → remove inline styles → drop `'unsafe-inline'`. |
| `connect-src` | `'self'` | When analytics ingest URL is set, add that origin explicitly (never `*`). |
| Trusted Types | Not enforced | Phase-2 Report-Only then enforce. |

## Verify

```bash
curl -sI https://interstitiumlabs.dev/ | grep -iE 'content-security|strict-transport|x-content|referrer|permissions|x-frame|cross-origin-opener'
```

Also enable Cloudflare dashboard → SSL/TLS → Edge Certificates → **HSTS** (preload-ready settings match the header above).

## Meta CSP backup

Key static HTML under `docs/` ships `<meta http-equiv="Content-Security-Policy" ...>` as defense-in-depth when Worker headers lag. HTTP headers always win when present; meta is the backup.
