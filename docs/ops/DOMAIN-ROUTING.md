# Interstitium Labs: canonical domain and release map

_Last verified against public HTTP responses and repository configuration on October 2, 2026. This document is an inventory, not an export of the authoritative Cloudflare DNS zone._

| Host / route | Canonical purpose | Public HTTP check | Source / deployment |
| --- | --- | --- | --- |
| `https://interstitiumlabs.dev/` | Primary company, public Learning OS and portfolio | Responds | `EnmanuelMejia/interstitium-labs/docs/`; `docs/CNAME` declares the apex; GitHub Pages deployment checks exist. Repo also includes `wrangler.jsonc`, but current Cloudflare proxy/Worker ownership is **not verified**. |
| `https://www.interstitiumlabs.dev/` | Redirect alias for apex | Redirects to apex | Cloudflare or hosting redirect configuration must be confirmed in the authorized DNS/edge dashboard. Do not publish a second independent copy. |
| `https://learn.interstitiumlabs.dev/` | Specialized Learning University | Responds; **was still serving its prior build after the October 2 source merge** | `EnmanuelMejia/interstitium-labs-university`, Cloudflare Worker `interstitium-labs-university` in `wrangler.jsonc`. Requires a distinct authorized Worker deployment. |
| `https://interstitiumlabs.dev/noah/` | Canonical Noah AI workspace | Responds | Primary site `docs/noah/`. The local workflow runner is not a complete remotely executed Muse-class agent. |
| `https://interstitiumlabs.dev/coach/` | Legacy contextual tutoring surface | Responds | Primary site `docs/coach/`. Keep as a learning-mode interface; do not advertise it as a separate AI identity. |
| `https://interstitiumlabs.dev/portfolio/` | Engineering and architecture portfolio | Responds | Primary site `docs/portfolio/`. |
| `https://interstitiumlabs.dev/projects/sundance-ai-architecture/` | Original manufacturing AI architecture case study | Responds | Primary site `docs/projects/sundance-ai-architecture/`. |
| `https://interstitiumlabs.dev/os/` | Time-to-hire learning workflow | Responds, including HTML fallback | Primary site `docs/os/`. |

## Unverified names

No current authoritative-zone export or authenticated Cloudflare connection is available to confirm the existence, owner, routing, or status of `app.`, `api.`, `noah.`, `labs.`, `staging.`, `dev.`, or any other potential subdomains. Do not create, redirect, remove, or advertise them based on a source-code mention.

## Release sequence

1. Snapshot and review the actual zone, proxy/CDN rules, SSL/TLS configuration, domain bindings, active Pages projects, Workers routes, and any existing DNSSEC or origin-restriction requirements.
2. Record the previous deployment identifier, linked Git commit and rollback target for each independently deployed application.
3. For the primary site, run the existing GitHub checks, merge reviewed source changes, wait for GitHub Pages or the verified primary deployment, and verify canonical apex routes.
4. For the university, run `node scripts/validate.mjs`, `node scripts/brand-check.mjs`, `node js/adaptive.selftest.mjs`, then deploy the **university Worker** through the authorized Cloudflare account using the existing `wrangler.jsonc`. A GitHub merge alone does not deploy that Worker unless an authenticated deployment integration is explicitly configured and verified.
5. Check actual HTTP response headers, canonical URLs, asset freshness, manifest metadata, HTTPS, authentication boundaries, and desktop/mobile transitions.
6. Confirm that `www` redirects to the apex and that the `learn` hostname still serves the university. Do not route the university Worker onto the apex.
7. If a release fails, restore that application's prior deployment. Avoid globally invalidating caches or resetting user browser sessions unless a measured fault requires it.

## Integrity and identity

- **Noah AI** is the canonical product identity. Historical `/coach/` routes and archived development references are not independent competing products.
- The main site currently presents **10 flagship academies**; the university's actual sharded catalog contains **11 academies, 65 paths and 349 modules**. Do not inflate one catalog using the other's figures. Content consolidation is a separate, data-migration project.
- The primary site's service worker is intentionally retired and clears old caches. Do not re-enable offline precaching without an independently tested PWA release strategy.
- Browser storage, authenticated server persistence and cloud agent execution are separate capabilities. Do not describe them interchangeably.
