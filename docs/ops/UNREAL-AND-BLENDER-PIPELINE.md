# Unreal + Blender pipeline (P920)

_Last updated: 2026-09-22 ~00:41 EDT (America/New_York)._  
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

Until real files exist, `il-immersive-3d.js` uses **procedural** stand-ins (`procedural:hermetic|rack|k8s`). That is honest scaffolding — still 3D mesh/WebGL, still not a CSS card.

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

### Pixel Streaming (later)

- Host streamer on lab GPU box (not Pages).
- Signalling server + STUN/TURN as needed.
- Site CSP today is tight (`frame-ancestors`, limited `connect-src`) — streaming subdomain will need an explicit CSP exception documented in `ENTERPRISE-SECURITY.md` before go-live.

## In-page player (now)

| File | Notes |
|------|-------|
| `docs/assets/il-immersive-3d.js` | Orbit, captions, clip play, procedural scenes, glTF hook |
| `docs/assets/il-immersive-3d.css` | Stage chrome + reduced-motion |

CSP forbids CDN Three → v1 is self-contained WebGL. When vendoring Three/WebGPU + GLTFLoader, place under `/assets/vendor/` and keep `script-src 'self'`.

## QA checklist

- [ ] Stage visible on lecture/lab without console CDN errors  
- [ ] `prefers-reduced-motion` shows static fallback + captions  
- [ ] Real `.glb` path 404 → falls back to procedural of same family (no blank)  
- [ ] Muse avatar (`il-muse-3d`) not double-mounted inside curriculum stage  
- [ ] No claim of Unreal Pixel Streaming until signalling host is up  

## Related

- `IMMERSIVE-3D-CURRICULUM.md` — product law + dual pipeline  
- `LAB-MUSE-3D.md` — voice avatar only  
- `MUSK-BAR-RECURSIVE.md` — Elon gate scorecard  
