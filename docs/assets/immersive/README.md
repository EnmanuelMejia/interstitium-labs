# Immersive glTF assets

Authored via **Interstitium glTF kit v2** (`scripts/author_immersive_glb.py`) — **glTF 2.0 binary** (`.glb`).

Kit-v2 adds: higher-density meshes, chamfer boxes, spheres, pedagogical `extras` on nodes, LOD1 proxy meshes, Interstitium PBR (cyan `#5EEAD4` · gold `#D4A853` · void `#070B16`).

**Blender polish (P920):** `python3 scripts/blender_polish_glb.py --in docs/assets/immersive/<scene>.glb`  
Writes a sidecar and runs `blender --background` when CLI is on PATH; otherwise prints the P920 command. Honest: kit meshes are **not** hand-sculpted Blender artist sets until that polish lands.

Native load: `ILSceneKit.parseGlb` → `il-immersive-3d.js` / `il-muse-3d.js` (CSP-safe, no Three CDN).  
Pixel Streaming client: `/immersive/pixel-stream/` · Runbook: `/ops/PIXEL-STREAMING-DEV.md`

| File | Scene / family |
|------|----------------|
| `lecture-k8s-control-plane.glb` | Control-plane + scheduler/CM + workers (`procedural:k8s`) |
| `k8s-cluster.glb` | Alias of lecture k8s control-plane |
| `cert-cka.glb` | CKA shell variant (k8s family) |
| `cka-etcd-quorum.glb` | **NEW** CKA etcd raft quorum + API front (immersive exceed) |
| `rack-19u.glb` | Three rack frames with bay LEDs (`procedural:rack`) |
| `hermetic-monas.glb` | Hermetica / Monas lecture (`procedural:hermetic`) |
| `sim-superlab.glb` | SuperLab sim (rack + cluster combo) |
| `muse-dee-monas.glb` | **NEW** Lab Muse Dee/Monas avatar (voice-reactive coach) |

Regenerate:

```bash
python3 scripts/author_immersive_glb.py --out docs/assets/immersive
python3 scripts/blender_polish_glb.py --in docs/assets/immersive/muse-dee-monas.glb --write-only
```
