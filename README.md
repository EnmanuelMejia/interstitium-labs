# Interstitium Labs

**Live:** https://interstitiumlabs.dev  
**Static root:** `docs/` (GitHub Pages / Cloudflare Workers Assets)

Knowledge OS — Learning OS (founders, learn, prep, play, paths), academies, adaptive command, evidence.

## Security (enterprise, all builds)

**Start here:** [`docs/ops/ENTERPRISE-SECURITY.md`](docs/ops/ENTERPRISE-SECURITY.md)

| | |
| --- | --- |
| Edge headers | `docs/_headers` + Worker snippet `docs/ops/snippets/cloudflare-worker-security-headers.js` |
| Mobile MASVS | `docs/ops/MOBILE-SECURITY.md` · Capacitor `apps/mobile/` |
| Store path | `docs/ops/STORE-PUBLISH.md` (Enmanuel’s Apple/Google accounts required) |
| Payments | Payment Links only — no Stripe secrets in repo |

## Local web

```bash
cd docs && python3 -m http.server 8080
```

## Mobile (Capacitor)

```bash
./scripts/sync-mobile-web.sh
cd apps/mobile && npm ci && npx cap sync
```

See `apps/mobile/README.md`.

## PWA

`docs/manifest.webmanifest` + `docs/sw.js` — Interstitium Labs / Learning OS (not legacy “Grok App”).

Independent product work by Enmanuel D. Mejia. Pair with [devops-superlab](https://github.com/EnmanuelMejia/devops-superlab).
