# Immersive glTF assets

Authored via **Interstitium glTF kit** (`scripts/author_immersive_glb.py`) — **glTF 2.0 binary** (`.glb`).

Open / polish in **Blender on P920**. These are kit-authored meshes (POSITION + NORMAL, TRIANGLES, Interstitium PBR materials: cyan `#5EEAD4` · gold `#D4A853` · void `#070B16`) — **not** hand-sculpted Blender artist sets yet. Do not claim Musk YES on that alone.

Previous `.pending.json` scaffolds for these ids are **retired**. Procedural WebGL remains the fallback if fetch/parse fails (`il-immersive-3d.js`).

| File | Scene / family |
|------|----------------|
| `lecture-k8s-control-plane.glb` | Control-plane cylinder + worker boxes (`procedural:k8s`) |
| `k8s-cluster.glb` | Alias of lecture k8s control-plane |
| `cert-cka.glb` | CKA shell variant (k8s family) |
| `rack-19u.glb` | Three rack frames with bay LEDs (`procedural:rack`) |
| `hermetic-monas.glb` | Hermetica / Monas lecture (`procedural:hermetic`) |
| `sim-superlab.glb` | SuperLab sim (rack + cluster combo) |

Regenerate:

```bash
python3 scripts/author_immersive_glb.py --out docs/assets/immersive
```

Native load: `ILSceneKit.parseGlb` → `il-immersive-3d.js` (CSP-safe, no Three CDN).  
Curriculum SoT: `/curriculum-os/` · Sync: `/assets/il-curriculum-sync.js`  
Pipeline: `docs/ops/UNREAL-AND-BLENDER-PIPELINE.md` · Pixel Streaming client: `/immersive/pixel-stream/`
