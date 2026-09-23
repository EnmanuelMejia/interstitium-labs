# Noah avatar — Dee theme

**Default avatar** for Noah (`/coach/`) is the **Dee** mark: a geometric Monas-derived SVG in Interstitium brand colors (cyan / gold / void).

## Attribution & honesty

- **Inspired by** historical John Dee (Elizabethan mathematician-mage; Monas Hieroglyphica / Hermetica energy already present in product language).
- **Artwork:** Interstitium original SVG/CSS — not a copy of any museum portrait photograph, and **not** a Meta Noah or Meta brand asset.
- Educational Socratic DevOps coach personality default: `Dee · precise · Socratic · hermetic scholar` (still a lab coach).

## Assets

| File | Role |
|------|------|
| `/assets/il-muse-avatar-dee.svg` | Default Dee / Monas mark |
| `/assets/il-muse-avatar-sigil.svg` | Alt: Interstitium orbital sigil |
| `/assets/il-muse-avatar-cap.svg` | Alt: scholar hood/cap silhouette |
| `/assets/chrome/lab-muse-dee.svg` | Same Dee mark for chrome/lockup reuse |
| `/assets/il-muse.js` | Avatar picker + `avatarId` in `il.muse.v1` |
| `/assets/il-muse.css` / `il-muse-mobile.css` | Idle / listening / thinking / speaking glow |

## Status states

CSS drives cyan/gold glow on `.il-muse-avatar__ring` and mark drop-shadow from `data-status` on `.il-muse-app`: `idle` · `listening` · `thinking` · `speaking`.

## Do not break

Model router paths (`il-model-router.js`, catalog, analytics) and coach mount `[data-il-muse]` are unchanged. Avatar is presentation-only.

## 3D stage (default)

Voice-reactive WebGL Monas/orrery is the **default stage** — see [LAB-MUSE-3D.md](./LAB-MUSE-3D.md). SVG marks remain the picker + header fallback + reduced-motion path.

