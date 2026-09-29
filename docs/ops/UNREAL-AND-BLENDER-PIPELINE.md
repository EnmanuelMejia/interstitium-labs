# Unreal + Blender pipeline (P920)

_Last updated: 2026-09-29 ~09:15 EDT (America/New_York)._  
_Authoring host:_ Lenovo ThinkStation **P920** · _Site delivery:_ Cloudflare Pages `docs/`

## Goal

Author **real** 3D curriculum (not CSS cards). Ship light assets to the open web; reserve Unreal for cinematic / heavy certification sims.

```
┌─────────────┐     glTF/.glb      ┌──────────────────┐
│   Blender   │ ─────────────────► │ Godot HTML5/WASM │  pipeline B
│  (author)   │                    │  or Three player │
└──────┬──────┘                    └──────────────────┘
       │ FBX / USD / Datasmith
       ▼
┌─────────────┐   Pixel Streaming  ┌──────────────────┐
│   Unreal    │ ─────────────────► │ Browser lab view │  pipeline A
│  (cinematic)│   or packaged .exe │ / LAN viewer     │
└─────────────┘                    └──────────────────┘
```

## Musk gate

**Skipping Blender/Unreal (and not substituting Blender→glTF→Godot/Three) = fail Elon test.**  
See `IMMERSIVE-3D-CURRICULUM.md`.

## GPU honesty (do not wallpaper)

| Hardware | Honest role |
|----------|-------------|
| P920 + Quadro **P1000** (typical) | Blender modeling / mid poly; Unreal **editor** for layout & blueprint; **not** AAA Nanite/Lumen cinematics at full fidelity |
| P920 + stronger GPU (if upgraded) | Heavier Unreal preview; local Pixel Streaming experiments |
| Pages / phone clients | Procedural WebGL or compressed `.glb` only — never assume desktop dGPU |

**P1000 limits packaged complexity:** keep Unreal lab viewers mid-poly, baked lighting, LODs, no unbounded ray tracing. Prefer Pixel Streaming from a lab GPU host when fidelity must exceed what P1000 can package smoothly.

## Blender → open web (default)

1. Model / UV / animate in Blender (metric units; origin at stage floor).
2. Export **glTF 2.0** binary (`.glb`):
   - Apply modifiers; triangulate if needed
   - Embed textures (KTX2/Basis when toolchain ready; PNG/JPEG OK for v1)
   - Name action clips clearly (`idle`, `fail`, `heal`, `scale`)
3. Drop under `docs/assets/immersive/<scene>.glb`.
4. Point lecture/lab JSON:

```json
"immersive": {
  "mode": "3d-first",
  "engine": "three",
  "asset": "/assets/immersive/k8s-cluster.glb"
}
```

5. Optional: Godot 4 import `.glb` → Export HTML5 for interaction-heavy labs (`engine: "godot"`).

### Naming

| Asset | Suggested file |
|-------|----------------|
| Hermetica / Monas lecture | `hermetic-monas.glb` |
| Server rack / DC | `rack-19u.glb` |
| Kubernetes cluster | `k8s-cluster.glb` |

**2026-09-29:** Kit-authored `.glb` files live under `docs/assets/immersive/` (see README + `scripts/author_immersive_glb.py`). Open/polish in Blender on P920. `il-immersive-3d.js` loads via native `ILSceneKit.parseGlb` (no Three CDN); on 404/parse fail → **procedural** of same family with honest caption. Provenance: kit glTF, not hand-sculpted Blender UI sets yet.

## Unreal → cinematic / cert sims

1. Block out in Blender or Unreal directly; keep collision simple for lab clicks.
2. Datasmith / FBX for prop kits; prefer master materials with few variants (P1000-friendly).
3. **Lab viewer packaging:** Shipping target Windows/Linux packaged build **or** Pixel Streaming.
4. Wire `engine: "unreal"` + URL when streaming endpoint exists:

```json
"immersive": {
  "mode": "3d-first",
  "engine": "unreal",
  "asset": "unreal:pixel://labs.internal/cka-sim"
}
```

5. Until Pixel Streaming is live, do **not** fake an Unreal iframe — keep `three` procedural/glTF on docs and link “Open heavy sim (LAN)” only when the host is real.

### Pixel Streaming (client path live; streamer host later)

- **Browser client:** `/immersive/pixel-stream/` — reads `?signaling=` / `data-ps-signaling` / `localStorage.il-ps-signaling`.
- Without signaling: honest stub (never fake a live stream video).
- With `wss://` signaling: minimal WebRTC handshake attempt (UE PS subset); with http(s) player URL: iframe via `ILSceneKit.pixelStreamEmbed`.
- Host streamer on lab GPU box (not Pages). STUN/TURN as needed.
- **CSP (do NOT widen live today without a real host):** when streaming goes live, allowlist the stream subdomain in `connect-src` (WebSocket/signaling) + `frame-src` / `media-src` as needed. Exact future exception documented in `ENTERPRISE-SECURITY.md` §5.3. Until then Pages CSP stays tight.

## In-page player (now)

| File | Notes |
|------|-------|
| `docs/assets/il-immersive-3d.js` | Orbit, captions, clip play, procedural + **native GLB render** |
| `docs/assets/il-scene-kit.js` | `parseGlb` / `loadGltf` / `pixelStreamEmbed` |
| `docs/assets/il-immersive-3d.css` | Stage chrome + reduced-motion |
| `docs/immersive/pixel-stream/` | UE Pixel Streaming client shell |
| `scripts/author_immersive_glb.py` | Kit authoring (glTF 2.0 binary) |

CSP forbids CDN Three → native `parseGlb` ships meshes without Three. Optional vendored Three/GLTFLoader still under `/assets/vendor/` with `script-src 'self'`.

## QA checklist

- [x] Stage visible on lecture/lab without console CDN errors  
- [x] `prefers-reduced-motion` shows static fallback + captions  
- [x] Real `.glb` committed under `/assets/immersive/`; 404/parse → procedural same family (no blank)  
- [x] Native `parseGlb` draws authored meshes (caption: authored .glb vs procedural fallback)  
- [x] Noah (`il-muse-3d`) not double-mounted inside curriculum stage  
- [x] Pixel Streaming **client path** at `/immersive/pixel-stream/` — no fake live stream  
- [ ] Live UE5 streamer + signaling host on lab GPU (not yet)  
- [ ] P920 Blender polish pass on kit meshes (not yet)  
- [ ] CSP allowlist for stream subdomain at go-live only  

## Related

- `IMMERSIVE-3D-CURRICULUM.md` — product law + dual pipeline  
- `LAB-MUSE-3D.md` — voice avatar only  
- `MUSK-BAR-RECURSIVE.md` — Elon gate scorecard  
