**Product law (canonical):** [`IMMERSIVE-3D-CURRICULUM.md`](./IMMERSIVE-3D-CURRICULUM.md) · **P920 authoring:** [`UNREAL-AND-BLENDER-PIPELINE.md`](./UNREAL-AND-BLENDER-PIPELINE.md)

# Immersive 3D — curriculum-wide (lectures · cert labs · sims · non-cert)

**Rule (Musk gate):** Skipping Blender **and** Unreal = fail. Open-source path (Blender / Godot / Three) ships in-browser today; Unreal Pixel Streaming is scaffolded and documented — **do not block** the web ship on a local UE install.

**Companion:** Lab Muse voice-reactive familiar (`LAB-MUSE-3D.md`) shares `ILSceneKit` with the immersive player.

## What shipped (this pass)

| Layer | Asset | Status |
|-------|-------|--------|
| Shared kit | `/assets/il-scene-kit.js` | WebGL helpers, palette, glTF loader hook, Pixel Streaming embed stub, speak-amp bus |
| Curriculum scaffold | `/assets/il-immersive-3d.js` + `.css` | **Wired** on prep/labs/paths/adapt/learn — owns `[data-il-scene]` |
| Demo player | `/assets/il-immersive.js` + `.css` | `/immersive/` + `data-kind` hosts; skips `data-il-scene` |
| Muse 3D | `/assets/il-muse-3d.js` | Voice-reactive Monas; exposes `.kit` / `.immersive` getters |
| Scene registry | `/assets/scenes/manifest.json` | Placeholders until Blender `.glb` exports land |
| Demo | `/immersive/` | Live procedural stages + engine switcher notes |
| Docs | this file | Blender → glTF, Godot, Unreal Pixel Streaming |

Honest claim: **procedural WebGL stages are live** (CSP-safe, no CDN). Photoreal Unreal rooms and authored glTF sets are **pipeline-ready**, not yet content-complete.

## Engines (pick per surface)

```
Authoring:  Blender (primary) ──glTF──► Web (Three optional / procedural fallback)
            Godot (alt open)  ──glTF──► same web player
            Unreal Engine 5   ──Pixel Streaming──► iframe / signaling URL
Runtime:    /assets/il-immersive.js  (default WebGL)
            Vendored THREE + GLTFLoader under /assets/vendor/ (optional)
            UE5 Pixel Streaming when data-ps-signaling is set
```

### Why not CDN Three?

Site CSP is `script-src 'self'`. Vendor Three when needed:

```bash
mkdir -p docs/assets/vendor
# download three.min.js + examples/jsm path built to IIFE, or use importmap+self host
```

Until vendor exists, `ILSceneKit.loadGltf()` resolves `{ ok:false, reason:'three_not_vendored' }` and the player keeps the procedural stage.

## Blender pipeline (required — do not skip)

1. Model lecture / lab / sim set in **Blender 4.x** (metric, Y-up or apply on export).
2. File → Export → **glTF 2.0** → format **GLB** (embedded buffers).
3. Name: `lecture-<slug>.glb` · `cert-<slug>.glb` · `sim-<slug>.glb` · `lab-<slug>.glb`
4. Drop into `docs/assets/scenes/` and register in `manifest.json`.
5. Wire: `<div data-il-immersive data-kind="cert" data-gltf="/assets/scenes/cert-foo.glb"></div>`
6. Keep triangle budget mobile-friendly (aim &lt;80k tris for phone stages).

Godot 4: export selected mesh as glTF; same folder conventions.

## Unreal Pixel Streaming (required path — scaffold, don’t block)

Elon gate: Unreal is first-class for high-fidelity sims. Web ship must not wait on GPU farm.

### Local / lab box (when UE5 is available)

1. UE5 project → enable **Pixel Streaming** plugin.
2. Package Linux/Win server build with `-PixelStreamingURL=ws://127.0.0.1:8888`.
3. Run [SignallingWebServer](https://github.com/EpicGames/PixelStreamingInfrastructure) (or Epic’s sample).
4. Point curriculum host:

```html
<div data-il-immersive
     data-kind="sim"
     data-engine="unreal"
     data-ps-signaling="https://stream.example/player.html"
     data-title="Cluster sim (UE5)"></div>
```

`ILSceneKit.pixelStreamEmbed()` iframes the player when URL is set; otherwise shows an honest stub (“signaling not configured”).

### Cloud GPU later

- Packaged streamer on a GPU VM (AWS g5 / CoreWeave / etc.)
- Turn credentials / STUN for students behind NAT
- Never commit stream secrets — use env / Pages encrypted bindings

## Muse hooks (shared renderer utilities)

```js
// After scripts: il-scene-kit.js → il-muse-3d.js → il-immersive.js
ILMuse3D.kit === ILSceneKit          // shared palette / mats / glTF / PS
ILMuse3D.immersive === ILImmersive   // curriculum player
ILSceneKit.onSpeakAmp(detail => …) // same bus as Muse TTS boundaries
ILImmersive.mount(el, { kind: 'lecture' })
```

Voice amp from Lab Muse (`il-muse-speak-amp` / `il-muse-speak-boundary`) drives immersive emissive when both are on-page (cinema Learn|Lab|Muse).

## Markup cheatsheet

```html
<!-- Lecture -->
<div data-il-immersive data-kind="lecture" data-title="CIDR lecture"></div>

<!-- Cert lab -->
<div data-il-immersive data-kind="cert" data-gltf="/assets/scenes/cert-cka-etcd.glb"></div>

<!-- Simulation -->
<div data-il-immersive data-kind="sim" data-engine="unreal" data-ps-signaling=""></div>

<!-- Non-cert / open lab -->
<div data-il-immersive data-kind="non-cert" data-title="SuperLab bay"></div>
```

Include:

```html
<link rel="stylesheet" href="/assets/il-immersive.css"/>
<script src="/assets/il-scene-kit.js" defer></script>
<script src="/assets/il-immersive.js" defer></script>
```

## Surfaces to light up (rollout)

| Surface | Kind | Priority |
|---------|------|----------|
| `/coach/` Muse stage | familiar (done) | P0 |
| `/immersive/` demo | all kinds | P0 |
| `/learn/*` lecture cards | lecture | P1 |
| `/labs/*` + SuperLab | cert / non-cert | P1 |
| `/cinema/` Muse pane | familiar + optional lecture | P1 |
| Path modules under `/paths/*` | lecture → cert | P2 |
| Full UE5 campus | sim | P2 (GPU) |

## Honesty

- No fake “Unreal online” without a signaling URL.
- No CDN Three (CSP).
- Procedural ≠ final art; Blender/Unreal content is the quality bar.
- Muse 3D exceeds flat Muse-class motion; curriculum immersive is the same philosophy applied to lectures/labs.

## Sync

```bash
./scripts/sync-mobile-web.sh
```
