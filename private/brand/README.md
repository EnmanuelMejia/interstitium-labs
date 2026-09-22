# Private brand vault (not deployed)

This directory sits **outside** `docs/`, which is the Cloudflare Workers Assets public root.
Nothing here is shipped to students, recruiters, or search engines via the site.

**Git policy:** `private/**` is gitignored except this README. Keep binary masters on the operator machine or a private backup — do not force-add them to the public remote.

## What lives here (local)
- `marks/` — source key art, full-resolution sigil masters, alternate lockups
- `campaign/` — IL Higher OS campaign plates
- `guidelines/` — former public brand kit HTML/README (operators only)
- `founders-masters/` — reserved for non-runtime founder photography masters

## What ships publicly
Runtime chrome only, under `docs/assets/chrome/`:
- `canonical-lockup.png` — header/footer lockup
- `apple-touch.png`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`
- `sigil-decor.webp` — optional hero décor (not a brand kit)
- `founders/*` — founders page portraits used by product UI

## Rule
Do **not** recreate `/brand/` galleries, mark indexes, downloadable kits, or usage READMEs under `docs/`.
Product chrome is enough for the public Learning OS.

See also: `docs/ops/BRAND-PRIVATE.md` (ops path; disallowed in robots.txt).
