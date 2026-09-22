# Muse AI ↔ Lab Muse mobile capability benchmark

**Product:** Lab Muse / Interstitium Labs companion (`/coach/`, Capacitor `dev.interstitiumlabs.app`)  
**Brand:** Interstitium lockup (56–80px) · cyan `#5EEAD4` · gold `#D4A853` · void `#070B16`  
**Honesty:** Muse-*class interaction patterns* from public design posts — **not** Meta’s product, logo, purple/pink palette, connectors, or assets.

Recursive score: **meet or exceed** public Muse-class companion behaviors with **local-first** Interstitium surfaces. No Gmail/Spotify/Meta connectors.

| # | Muse-class capability | Lab Muse mobile | Status | Exceed note |
|---|----------------------|-----------------|--------|-------------|
| 1 | Chat-first full-bleed shell | `il-muse-mobile.css` ≤768 / standalone / Capacitor; page chrome collapses | **Meet** | Desktop grid ≥960 untouched |
| 2 | Bottom composer + thumb mic/speak | Composer sticky; ≥44px targets; speak toggle + Web Speech | **Meet** | Keyboard-aware via `visualViewport` |
| 3 | Avatar + live status | Dee monas SVG default; ring + glow for idle/listening/thinking/speaking | **Exceed** | Dee/Hermetica original; picker (Dee/Sigil/Cap); see [LAB-MUSE-AVATAR.md](./LAB-MUSE-AVATAR.md) |
| 4 | Side chats / drawers | Swipe + Chats/Goals drawers + scrim | **Meet** | Goals/artifacts/model in panel |
| 5 | Bottom nav | Muse · Paths · Labs · OS tabnav | **Meet** | First-party routes only |
| 6 | Multi-bubble replies | `splitBubbles()` → sequential assistant parts | **Meet+** | Boot + replies; part index in meta |
| 7 | Approval cards | Local approve cards (Adaptive / SuperLab / Model panel) | **Meet+** | Explicit “no Meta connectors” copy |
| 8 | Proactive nudges | `localNudges()` from goals + `ILAdaptive` weak topics | **Exceed** | On-device only; gold chip strip |
| 9 | Voice in / out | Mic dictation + TTS; status → Listening/Speaking | **Meet** | Browser Web Speech honesty |
| 10 | Goals / ideas / artifacts | Panel tabs + library | **Meet** | Lab-linked artifacts |
| 11 | Model transparency | Demand tiers T0–T2 + health; lean default | **Exceed** | Demand-tier router; no fake API keys |
| 12 | Native / PWA home | Capacitor `/` → `/coach/` via `il-bridge`; PWA shortcut Lab Muse | **Meet** | Void status bar `#070B16` |
| 13 | Safe-area / reduce-motion | insets + `prefers-reduced-motion` | **Meet** | iOS rubber-band fixes |
| 14 | Third-party connectors | **Deliberately absent** | **Exceed (honesty)** | No Gmail/Spotify/Meta — educational lab coach |

## Recursive close-the-gap checklist

1. [x] Full-bleed `/coach/` as native home  
2. [x] Dee avatar states with cyan/gold glows  
3. [x] Multi-bubble assistant cadence  
4. [x] Local approval cards  
5. [x] Proactive local nudges  
6. [x] Interstitium lockup preserved (not Meta)  
7. [ ] Optional: richer artifact carousels (P2)  
8. [ ] Optional: haptics on approve via Capacitor Haptics (P2)  

## How to verify on phone

**PWA:** https://interstitiumlabs.dev/coach/ → Add to Home Screen  
**Capacitor:**

```bash
./scripts/sync-mobile-web.sh
cd apps/mobile && npm ci && npx cap sync
npx cap run android   # or ios on macOS
```

Cold start should land on Lab Muse. Expect Dee avatar, nudge chips, multi-bubble welcome, and an Adaptive approval card — void chrome, Interstitium lockup in header.

## Related

- [LAB-MUSE-AVATAR.md](./LAB-MUSE-AVATAR.md)  
- [STORE-PUBLISH.md](./STORE-PUBLISH.md) — Muse-class companion shell  
- `docs/assets/il-muse.js` · `il-muse-mobile.css` · `apps/mobile/src/il-bridge.js`
