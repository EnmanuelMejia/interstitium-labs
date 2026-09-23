# Noah 3D — voice-reactive stage

**Ship:** voice-driven WebGL familiar on `/coach/` (and cinema Muse pane).  
**Claim (honest):** exceeds Meta Muse–class **flat/soft avatar motion** with a crystalline Dee/Monas orrery that reacts to mic + TTS. Original Interstitium art — **not** Meta assets, **not** a photoreal scraped portrait.

## Why this beats flat Noahs

| | Meta Muse–class (public) | Noah 3D |
|--|--------------------------|-------------|
| Form | Soft 2D / simple avatar chrome | Crystalline Monas + orrery rings + particle field |
| Voice | Soft status chrome | `idle \| listening \| thinking \| speaking` drives shaders, glow, spin, particles |
| Listening | Indicator | Mic `AnalyserNode` when Permissions-Policy allows; else procedural pulse |
| Speaking | Rarely lip-synced | `speechSynthesis` **boundary** events + utterance-progress amplitude → emissive beat |
| Mobile | Often desktop-first | DPR-capped WebGL, 30–60fps target; Capacitor via `sync-mobile-web.sh` |
| Reduced motion | Varies | `prefers-reduced-motion` → CSS 3D monas fallback (no canvas) |

We do **not** claim Meta’s product, models, or connectors. Interaction patterns remain Muse-inspired; graphics are Interstitium original.

## Assets

| File | Role |
|------|------|
| `/assets/il-muse-3d.js` | Self-contained WebGL stage (`ILMuse3D`). CSP-safe — **no** esm.sh/CDN (site CSP is `script-src 'self'`). |
| `/assets/il-muse-3d.css` | Stage chrome, HDR cyan `#5EEAD4` / gold `#D4A853` / void `#070B16`, cinema + shell sizing, reduced-motion |
| `/assets/il-muse.js` | Mounts slot, syncs `data-status`, emits `il-muse-speak-boundary` / `il-muse-speak-amp` |
| `/assets/il-muse-avatar-*.svg` | **Picker + header fallback** — Dee default theme still selectable |

## Wire

- `/coach/index.html` — CSS + `il-muse-3d.js` before `il-muse.js`
- `/cinema/index.html` — same; `ILMuse3D.syncFromApp` detects `.il-cinema-muse-host`
- Slot: `.il-muse-3d-slot[data-muse-3d-slot]` inside the Muse stage (above live strip)
- Canvas host **survives** Muse `innerHTML` re-renders via reattach registry

## Status → motion

| Status | Visual |
|--------|--------|
| `idle` | Slow orrery drift, low emissive (alive in first seconds) |
| `listening` | Gold-leaning pulse; AnalyserNode or procedural amp |
| `thinking` | Fast spin + dense orbital particles / glyph rotation |
| `speaking` | Cyan emissive beat from TTS boundaries + progress amp |

## Do not break

- Model router (`il-model-router.js`, catalog, analytics) — untouched
- Dee SVG picker — remains; 3D is **default stage**, SVG is header mark + settings picker + reduced-motion fallback
- Interstitium lockup — untouched
- No fake API keys / Meta connectors

## Demo (voice → 3D)

1. Open https://interstitiumlabs.dev/coach/ on a phone (or desktop Chrome/Edge).
2. First ~3s: WebGL monas should already drift/glow (idle vitality).
3. Tap **🎙** → status `listening` → stage pulses (gold). Grant mic if prompted (Analyser optional; procedural still reacts).
4. Send a stuck question (or speak one) → `thinking` orbital field.
5. With **🔊** on → `speaking` emissive lip-sync-ish beat while TTS reads the reply.
6. Settings → avatar picker still switches Dee/Sigil/Cap accents; SVG header mark updates.
7. Cinema: `/cinema/` Muse pane mounts the same stage in compact mode.
8. `prefers-reduced-motion: reduce` → CSS familiar, no WebGL.

## Honesty notes

- Site `Permissions-Policy` may include `microphone=()` on some edges — STT/Analyser then degrade; procedural listening pulse still ships.
- Not Three.js CDN (blocked by CSP); lightweight self-hosted WebGL with Three-class mesh/lighting depth.
- “Generations ahead” = motion/reactivity vs flat assistant-class chrome — not a claim about Meta’s private roadmap.

## Sync

```bash
./scripts/sync-mobile-web.sh
```


## vs curriculum immersive (`il-immersive-3d`)

| | `il-muse-3d` | `il-immersive-3d` |
|--|--------------|-------------------|
| Job | Coach / cinema **voice avatar** | **Lectures, labs, cert sims, non-cert** scenes |
| Surfaces | `/coach/`, `/cinema/` Muse pane | Prep · labs · paths · adapt · learn |
| Driven by | Mic + TTS status | Orbit · anim clips · captions · glTF/procedural |
| Engines | Self-contained WebGL familiar | `three` (default) · `godot` · `unreal` (policy) |

**Do not merge canvases.** Product law is 3D-first for curriculum (`IMMERSIVE-3D-CURRICULUM.md`); Muse 3D does not satisfy that law by itself.

