# Brand privacy (operator note)

**Status:** Brand IP is private. Only product chrome ships on the public site.

## Deploy boundary
- Public root: `docs/` (Cloudflare Workers Assets)
- Private vault: `private/brand/` at repo root (outside `docs/`)
- Git: `private/**` is gitignored except `private/brand/README.md`. Full-res masters stay on the operator machine / private backup — not on the public remote, not on the CDN.

## Public chrome
`/assets/chrome/*` — lockup, icons, one décor sigil, founders portraits for `/founders/`.

## Not public
- Brand system pages / mark galleries
- Campaign masters (`il-higher-os*`)
- Full-res sigil PNG/WebP masters
- Brand guidelines markdown or README kits

`/brand/` is a stub that meta-refreshes to `/about/` with `noindex`.
`robots.txt` disallows `/brand/`, `/ops/`, `/admin/`, `/_imports/`, `/analytics/`, `/measure/`.

## Residual risk
Website visitors never receive the kit. Keep masters out of the public git remote (current `.gitignore`). For shared operator access, use a private repo or encrypted store — do not re-publish under `docs/`.
