# Topic Theme System Build — 2026-10-09

Sitewide themed-content CSS rollout, user order 2026-10-09.

## File created

**`~/workspace/apex-audit/docs/assets/il-topic-themes.css`** (29,203 bytes, 117/117 braces balanced)

All original work — pure CSS gradients/patterns, no external images, no copyrighted
assets (system font stacks only). Dark-mode base preserved; themes are accent layers
applied via `[data-topic-theme="..."]` on a wrapper (body or section).

Per-theme custom properties: `--th-bg`, `--th-accent` (+ `--th-accent-rgb`),
`--th-accent2` (+ `--th-accent2-rgb`), `--th-text`, `--th-glow`, `--th-font-accent`.

All 12 themes + topic→theme mapping comment at top of file:
| Topic | Theme | Signature |
|---|---|---|
| cybersecurity | mr-robot | #00ff41 on #050505, mono, scanlines, subtle glitch keyframes on headings, clip-path chamfered badges |
| system-design | cyberpunk | #ff2a6d + #05d9e8 on #0d0221, rain-streak gradient texture (animated drift), abstract geometric mark pseudo-elements (◢◣◤◥▮▯◆◇ — original marks, not real Japanese words), neon flicker |
| networking | tron | #00e5ff grid on #000, light-trail glow, chamfered neon card borders, pulse glow |
| cloud-devops | steampunk | brass #b08d57 + copper #b87333 (+ sky #87ceeb) on #1a1410, rotating conic-gradient gear emblem (pure CSS), riveted card borders |
| ai-ml | exmachina | #f5f5f5 on #0a0a0a, ultra-minimal, 1px lines, sharp edges, letterspaced uppercase |
| data-eng | oceandeep | #39ffce on #000814, layered radial wave gradients with 26s drift (current-like), bioluminescent glow |
| programming | hackers95 | #ff00ff / #ccff00 / cyan on #0a0a0a, skewed graffiti headings, sticker-style white borders + offset shadows |
| databases | alexandria | #f8f5ec + gold #d4af37 on #12100a, fluted column-strip card caps, italic serif headings |
| linux-systems | industrial | amber #ffb000 on #0c0800, chunky 4px borders, hazard-stripe header cap |
| math | sacredgeo | gold #e8c15a on #080604, 60°/−60°/0° lattice (diamond/triangle motifs), double-rule cards |
| web-dev | vaporwave | #ff71ce + #b967ff sunset on #120024, chrome gradient-text headings, animated retro grid floor |
| blockchain | goldrush | #ffd700 on #0d0b00, circuit-trace + node-dot texture with sheen drift, pickaxe-meets-circuit chevron rule |

Utilities: `.th-card`, `.th-header`, `.th-badge` (theme-agnostic skeleton + per-theme
refinements), `.th-texture` (per-theme gradient/pattern background). All 9 keyframes
(`th-glitch`, `th-flicker`, `th-rain`, `th-tronpulse`, `th-gearspin`, `th-drift`,
`th-jitter`, `th-gridscroll`, `th-sheen`) disabled under
`@media (prefers-reduced-motion: reduce)` (animation + transition: none).

## Wiring points

1. **Flagship** `~/workspace/apex-audit/docs/index.html` — added
   `<link rel="stylesheet" href="/assets/il-topic-themes.css"/>` after il-unified.css.
2. **Flagship** `~/workspace/apex-audit/docs/university/course.html` — added
   `<link rel="stylesheet" href="../assets/il-topic-themes.css">`.
   NOTE: `course-shell.js` does NOT inject stylesheets (verified by grep — no link
   creation in the file); the actual injection point is the shell HTML `course.html`,
   which is where the link went.
3. **Cert-bootcamps** — `@import url("il-topic-themes.css");` added at line 8 of BOTH
   `~/workspace/cert-bootcamps/site/bootcamps/_engine/style.css` and
   `~/workspace/cert-bootcamps/site/bootcamps/engine/style.css` (twins, byte-identical;
   HTML pages reference `engine/style.css`). `il-topic-themes.css` copied into both
   `engine/` and `_engine/` dirs so the relative @import resolves.
4. **Portfolio** — `il-topic-themes.css` copied to
   `~/workspace/portfolio-site/assets/il-topic-themes.css` (self-contained);
   `<link rel="stylesheet" href="/assets/il-topic-themes.css">` added to
   `~/workspace/portfolio-site/index.html` after `/styles.css`.

## Deploys (all exit 0)

- **Flagship**: `deploy-worker-assets .work/flagship-deploy-config-20261008.json`
  → `deployed solitary-sound-015a etag=95acb862e03f modified=2026-10-09T06:24:34Z`
  (1834 files manifest, 98 uploaded).
- **Cert-bootcamps**: `deploy-worker-assets deploy/worker-config.json`
  → `deployed cert-bootcamps modified=2026-10-09T06:26:06Z`
  (3455 files manifest, 3144 uploaded). Then ran README step 2
  `python3 deploy/create-routes.py` → **409**: route pattern already exists, owned by
  Worker `interstitium-course-gateway`. Pre-existing; left untouched (destructive to
  change). See open item below.
- **Portfolio**: `deploy-worker-assets ~/workspace/portfolio-deploy-config.json`
  → `deployed enmanuel-mejia modified=2026-10-09T06:26:34Z` (54 files, 2 uploaded).

## Verification (curl, 2026-10-09 ~02:27 EDT)

- `https://interstitiumlabs.dev/` → **200**, contains `il-topic-themes.css` link.
- `https://interstitiumlabs.dev/assets/il-topic-themes.css` → **200**, 119
  `[data-topic-theme]` selectors served.
- `https://interstitiumlabs.dev/university/course.html` → 307→**200** (trailing-slash
  normalization), contains the themes link. Themed sample page renders.
- `https://enmanueldmejia.com/` → **200**, contains the themes link.
- `https://enmanueldmejia.com/assets/il-topic-themes.css` → **200** (mr-robot
  selectors present — portfolio copy matches flagship, diff-clean).
- Cert-bootcamps on-disk: both `style.css` twins carry the @import (line 8);
  `il-topic-themes.css` copies diff-clean vs flagship.

## Open items / caveats

1. **Cert-bootcamps routes owned by another worker (pre-existing):**
   `enmanueldmejia.com/bootcamps/*`, `interstitiumlabs.dev/bootcamps/*`,
   `learn.interstitiumlabs.dev/bootcamps/*` are routed to Worker
   `interstitium-course-gateway` (409 on create-routes.py). Public checks:
   `enmanueldmejia.com/bootcamps/engine/style.css` → 308 →
   `interstitiumlabs.dev/bootcamps/engine/style.css` → **401 `{"error":"sign-in-required"}`**
   (gateway auth gate). So the freshly deployed `cert-bootcamps` worker (with the
   themes @import) is NOT reachable via the public routes until route ownership is
   resolved. Parent decision needed: repoint routes to `cert-bootcamps` or keep the
   gateway and mirror the CSS there. No workers.dev URL found in the repo to verify
   the worker directly (did not guess one).
2. CSS validation: no `node --check` equivalent for CSS; validated via brace balance
   (117/117), all-12-themes present, every used keyframe defined, mapping comment
   present. One dead rule (display:none emoji in goldrush) removed during build.
3. The full-stop (2026-10-07) stays untouched — this task was the explicitly ordered
   2026-10-09 themed-content rollout; no other workstreams were resumed.
