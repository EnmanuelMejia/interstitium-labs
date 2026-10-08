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

## One site

`docs/` is what [interstitiumlabs.dev](https://interstitiumlabs.dev) serves. `/practice/` is the wing on that host: the same placement and the SQL bench, with no model call.

`apps/practice/` is the server: Noah, memory, goals, and the frontier turn. The home page links the Learning OS rooms.

The ThinkStation disk is not part of this merge. Hyper-V waits until you are at the machine.

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

`docs/manifest.webmanifest` is the install manifest. `docs/sw.js` is a one-shot kill switch: it clears the retired September precache and unregisters. It does not serve an offline shell.

Independent product work by Enmanuel D. Mejia. Pair with [devops-superlab](https://github.com/EnmanuelMejia/devops-superlab).

## Selected architecture work

- [Sovereign Hybrid AI for Print & Packaging Manufacturing](case-studies/sundance-hybrid-ai/README.md): independent SunDance USA candidate case study (September–October 2026); 37-page architecture proposal, 17-slide executive presentation, data-residency-first model routing, four proposed human-governed agents, and phased roadmap. These are authored deliverables, **not** a paid consulting engagement or production deployment. [Public project page](https://interstitiumlabs.dev/projects/sundance-ai-architecture/).
