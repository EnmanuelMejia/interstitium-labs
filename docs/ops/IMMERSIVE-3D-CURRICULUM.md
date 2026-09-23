# Immersive 3D curriculum — product law

_Last updated: 2026-09-22 ~00:41 EDT (America/New_York)._  
_Live:_ https://interstitiumlabs.dev · _Static root:_ `docs/`

## Product law (non-negotiable)

**3D-first** for **ALL** lectures, certification labs, simulations, **and** non-cert content.

- Authoring / heavy sim: **Unreal Engine** and/or open-source variants (**Blender** authoring, **Godot** runtime, **glTF**, **Three.js / WebGPU** in-page).
- Delivery on the static site defaults to an immersive stage — never a CSS card pretending to be 3D.
- Recursive Musk gate: **Would Elon be impressed if we skipped Blender/Unreal?** → **NO.** Document that; never wallpaper flat chrome as “immersive.”

| Fail | Pass |
|------|------|
| CSS cards / 2D diagrams labeled “3D lab” | Real mesh / procedural WebGL / glTF / Unreal Pixel Streaming |
| Screenshots of Unity/Unreal without a player | In-page `il-immersive-3d` stage or packaged / streamed viewer |
| Noah alone counted as curriculum 3D | Muse = coach familiar; curriculum scenes = separate asset lane |

## Musk gate (document forever)

> **Not using Blender/Unreal (or honest OSS stand-ins: Blender → glTF → Godot/Three) = fail Elon test.**

CSS neumorphism ≠ spatial literacy. If a lecture has no `immersive` block, it is **not shipped** under this law — scaffold the stage with a procedural placeholder scene until real `.glb` / Unreal content lands.

## Dual pipeline

### A. Cinematic (heavy sims)

| Piece | Role |
|-------|------|
| **Unreal Engine** | High-fidelity certification / rack / cluster sims |
| **Pixel Streaming** | Browser viewer for lab hours (later; GPU-backed) |
| **Packaged lab viewers** | Offline / LAN demos when streaming is overkill |

Honesty: ThinkStation **P920** authors; onboard GPU limits packaged complexity (see `UNREAL-AND-BLENDER-PIPELINE.md`). Do not claim AAA fidelity on a Quadro **P1000**.

### B. Open web (default for docs/)

```
Blender (author) → glTF / .glb → Godot export  OR  Three.js / WebGPU player in-page
```

| Engine token | When |
|--------------|------|
| `three` | Default static docs player (`il-immersive-3d.js`) — CSP-safe self-hosted / procedural v1 |
| `godot` | Exported HTML5 / WASM lab shells when interaction graph is game-like |
| `unreal` | Pixel Streaming or packaged viewer URLs for heavy sims |

## Default JSON field (every lecture / lab / path module)

```json
"immersive": {
  "mode": "3d-first",
  "engine": "three",
  "asset": "procedural:k8s",
  "captions": true,
  "fallback": "reduced-motion"
}
```

| `asset` forms | Meaning |
|---------------|---------|
| `procedural:hermetic` | Monas / hermetica procedural scene (v1) |
| `procedural:rack` | Server rack procedural scene (v1) |
| `procedural:k8s` | Cluster / control-plane procedural scene (v1) |
| `/assets/immersive/*.glb` | Real glTF when authored (optional v1) |
| `unreal:pixel://…` / packaged URL | Pipeline A |

Schema: extend path/lab items with `immersive` (`additionalProperties` already allowed on path catalog). Generator scripts and hand-authored HTML must set `data-il-immersive` + `data-il-scene`.

## Shared player

| File | Role |
|------|------|
| `/assets/il-immersive-3d.js` | Stage player: load glTF when present, else procedural scene; orbit; anim clips; captions |
| `/assets/il-immersive-3d.css` | Stage chrome (cyan `#5EEAD4` / gold `#D4A853` / void `#070B16`); reduced-motion fallback |
| `/assets/immersive/` | Optional real `.glb` / HDR / caption sidecars |

**CSP:** `script-src 'self'` — no CDN Three. v1 = self-contained WebGL (Three-class depth). Vendor Three/WebGPU under `/assets/` when glTF loader weight is justified.

## Separation: Muse vs curriculum

| Namespace | Owns | Does not own |
|-----------|------|--------------|
| **`il-muse-3d`** | Coach / cinema **avatar** (voice-reactive Monas orrery) | Lecture racks, k8s clusters, hermetic lesson scenes |
| **`il-immersive-3d`** | **Curriculum** scenes (lectures, labs, cert sims, non-cert) | Mic / TTS lip-sync familiar |

Do not merge the two canvases. Muse may *comment on* an immersive stage; it must not replace it.

## Reduced motion / a11y

- `prefers-reduced-motion: reduce` → static poster + captions, no orbit auto-spin.
- Captions / `aria-live` for clip titles.
- Keyboard: Tab to stage, arrows orbit when focused (when motion allowed).

## Surfaces (wire defaults)

Prep drills · labs (esp. SuperLab) · paths modules · adapt · learn lectures (hermetica, cloud, systems, …).  
Each mounts:

```html
<section class="il-immersive" data-il-immersive data-il-scene="k8s" data-il-engine="three"
  data-immersive='{"mode":"3d-first","engine":"three","asset":"procedural:k8s"}'>
  …
</section>
<link rel="stylesheet" href="/assets/il-immersive-3d.css"/>
<script src="/assets/il-immersive-3d.js" defer></script>
```

## EN / ES chrome

| Key | EN | ES |
|-----|----|----|
| `immersive.lecture` | 3D lecture | Clase 3D |
| `immersive.lab` | Immersive lab | Lab inmersivo |
| `immersive.kicker` | 3D-first · Blender / Unreal / Three | 3D-first · Blender / Unreal / Three |
| `immersive.fallback` | Motion reduced — static scene | Movimiento reducido — escena estática |

## Related

- `docs/ops/UNREAL-AND-BLENDER-PIPELINE.md` — P920 authoring, export, GPU honesty
- `docs/ops/LAB-MUSE-3D.md` — avatar stage only
- `docs/ops/MUSK-BAR-RECURSIVE.md` — **Not using Blender/Unreal = fail Elon test**

## Sibling artifacts (same product law)

| Path | Role |
|------|------|
| `IMMERSIVE-3D.md` | Alternate pipeline notes + Pixel Streaming embed stub |
| `/immersive/` | Demo page (sibling player `il-immersive.js` + `il-scene-kit.js`) |
| `/assets/il-immersive-3d.js` | **Canonical curriculum scaffold** wired on lecture/lab/path HTML (`data-il-scene`) |
| `/assets/il-immersive.js` | Demo / `data-kind` hosts — skips `data-il-scene` nodes |

Do not double-mount both players on the same host element.

