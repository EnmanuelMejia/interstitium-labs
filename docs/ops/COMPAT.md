# Cross-browser / OS / platform compatibility

Ops note (private-ish). Public assets: `docs/assets/il-responsive.css`, `il-compat.css`, `il-compat.js`.

**Do not** re-publish the brand kit under `docs/brand/` — kit lives in `private/brand/` (gitignored). Site chrome icons/lockup: `docs/assets/chrome/`.

## Viewport

All Learning OS static pages use:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
```

`viewport-fit=cover` is required for `env(safe-area-inset-*)` on notched iOS and Capacitor.

## Asset order

1. `styles-*.css` (Tailwind build)
2. `il-motion.css` (when used)
3. `il-responsive.css`
4. `il-compat.css`
5. Scripts: `il-compat.js` (defer, early) → game/motion/pwa/analytics/i18n

## Matrix (code-reviewed; device lab where noted)

| Feature | Chromium | Firefox | Safari 15+ | Samsung Internet | iOS PWA | Capacitor WV |
|---|---|---|---|---|---|---|
| `viewport-fit=cover` + safe-area | Assumed OK | Assumed OK | **Code** | Assumed OK | **Code** | **Code** |
| `100dvh` / `svh` | Native | Native | Native 15.4+; `--il-vh` JS fallback | Native | Fallback + native | Fallback + native |
| `-webkit-backdrop-filter` | Via TW + compat | `backdrop-filter` | Prefixed + opaque `@supports` fallback | OK | OK | OK |
| Flex `gap` | Native | Native | 14.1+; margin fallback in compat | OK | OK | OK |
| `aspect-ratio` | Native | Native | 15+; padding-box fallback | OK | OK | OK |
| Input zoom ≥16px | N/A | N/A | **CSS** mobile inputs | **CSS** | **CSS** | **CSS** |
| `touch-action: manipulation` | **CSS** | **CSS** | **CSS** | **CSS** | **CSS** | **CSS** |
| `pointer:coarse` 48px targets | **CSS** | **CSS** | **CSS** | **CSS** | **CSS** | **CSS** |
| `:focus-visible` rings | **CSS** | **CSS** | **CSS** | **CSS** | **CSS** | **CSS** |
| `prefers-reduced-motion` | il-motion + compat | Same | Same | Same | Same | Same |
| Print stylesheet | Keep (responsive) | Keep | Keep | Keep | N/A | N/A |
| Ultrawide max measure | responsive + compat | Same | Same | Same | N/A | N/A |
| Landscape phone | compat media | Same | Same | Same | Same | Same |
| Foldable segments | Progressive `@media` | Progressive | Progressive | Progressive | Untested | Untested |

Legend: **Code** = implemented and reviewed in CSS/HTML/JS. **Assumed OK** = standard engine support for Safari 15+ baseline. **Untested** = no real dual-screen device in CI.

## QA checklist (manual when devices available)

- [ ] iOS Safari 17+: hero `min-h-dvh`, sticky header under notch, HUD above home indicator
- [ ] iOS Add to Home Screen (standalone): no status-bar overlap; `il-standalone` class present
- [ ] Android Chrome + Samsung Internet: backdrop on header; no horizontal scroll at 360px
- [ ] Firefox desktop: header blur or solid fallback; focus rings on Tab
- [ ] Width 320px: founders / learn / enroll / prep — no horizontal scroll on `html`
- [ ] `prefers-reduced-motion: reduce`: no sigil float / reveal motion
- [ ] Capacitor iOS/Android WebView: safe-area top/bottom after splash

## Residual risks

- Real iOS device / notch not exercised in this agent environment (Linux box only).
- Foldable `horizontal-viewport-segments` is progressive enhancement only.
- Gap / aspect-ratio fallbacks target rare pre-Safari-15 WebViews; primary baseline is Safari 15+.
- SPA `docs/index.html` shell shares the same CSS; React routes inherit via global link tags.

## Related

- `docs/ops/MOBILE-SECURITY.md` — Capacitor hardening
- `docs/ops/ITERATION.md` — do not invent analytics tokens
- `docs/assets/il-motion.css` — reduced motion source of truth for animations
