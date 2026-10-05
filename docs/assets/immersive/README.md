# Immersive glTF assets

Authored via **Interstitium glTF kit v2** (`scripts/author_immersive_glb.py`) — **glTF 2.0 binary** (`.glb`).

Kit-v2: higher-density meshes, chamfer boxes, spheres, pedagogical `extras` on nodes, LOD1 proxy meshes, Interstitium PBR (cyan `#5EEAD4` · gold `#D4A853` · void `#070B16`).

## Blender polish provenance (2026-10-01 · 2026-10-02 · 2026-10-05)

**Polished via Blender CLI 4.2.3 LTS on 2026-10-01, 2026-10-02, and 2026-10-05 (America/New_York)** using `scripts/blender_polish_glb.py --all --promote`:

- shade smooth + weighted normals
- LOD1 decimate duplicates
- promoted `.polished.glb` → in-place `.glb` (kit backups are `*.kit-v2.bak.glb`, gitignored)

Honest: this is **CLI polish on kit meshes**, not hand-sculpted artist sets. Sidecars `*.blender_polish.py` remain for P920 re-runs.

```bash
python3 scripts/author_immersive_glb.py --out docs/assets/immersive
export PATH="/workspace/bin:$PATH"   # if Blender lives under /workspace/opt/blender
python3 scripts/blender_polish_glb.py --all --dir docs/assets/immersive --promote
```

Native load: `ILSceneKit.parseGlb` → `il-immersive-3d.js` / `il-muse-3d.js` (CSP-safe, no Three CDN).  
Pixel Streaming client: `/immersive/pixel-stream/` · Runbook: `/ops/PIXEL-STREAMING-DEV.md`

| File | Scene / family |
|------|----------------|
| `lecture-k8s-control-plane.glb` | Control-plane + scheduler/CM + workers (Blender-polished 2026-10-01) |
| `k8s-cluster.glb` | Alias of lecture k8s control-plane |
| `cert-cka.glb` | CKA shell variant (Blender-polished 2026-10-01) |
| `cka-etcd-quorum.glb` | CKA etcd raft quorum + API front (Blender-polished 2026-10-01) |
| `cni-pod-network.glb` | CNI / pod networking spatial pedagogy (Blender-polished 2026-10-01) |
| `rbac-authz-graph.glb` | RBAC User→Role→API spatial graph (Blender-polished 2026-10-01) |
| `service-mesh-sidecar.glb` | Sidecar data-plane vs control-plane (Blender-polished 2026-10-01) |
| `storage-csi-pv.glb` | StorageClass → CSI → PV → PVC → Pod volumeMount (Blender-polished 2026-10-02) |
| `ingress-gateway.glb` | Client → Ingress/Gateway → Service → Endpoints (Blender-polished 2026-10-02) |
| `hpa-autoscaling.glb` | metrics-server → HPA → Deployment replica stretch (Blender-polished 2026-10-02) |
| `network-policy-isolation.glb` | **NEW** Namespaces + NetworkPolicy shield, ALLOW (cyan) vs DENY (red) edges, DNS egress, CNI enforcer (Blender-polished 2026-10-05) |
| `secrets-configmaps.glb` | **NEW** Pod with Secret volume (emissive gold, tmpfs) vs ConfigMap volume (paper), env refs, etcd store (Blender-polished 2026-10-05) |
| `scheduling-affinity.glb` | **NEW** kube-scheduler filter/score/bind, node labels + taints, affinity/toleration-bound pods vs Pending pod (Blender-polished 2026-10-05) |
| `rack-19u.glb` | Three rack frames with bay LEDs (Blender-polished 2026-10-02) |
| `hermetic-monas.glb` | Hermetica / Monas lecture (Blender-polished 2026-10-02) |
| `sim-superlab.glb` | SuperLab sim (rack + cluster combo) (Blender-polished 2026-10-02) |
| `muse-dee-monas.glb` | Lab Muse Dee/Monas avatar (Blender-polished 2026-10-01) |

Translucent pedagogy shells (e.g. the NetworkPolicy shield) use `alphaMode: BLEND` + `doubleSided` — emitted automatically by the kit when `baseColorFactor` alpha < 1.

Honest scope: authored + CLI-polished open-web glTF. **No live Unreal host and no hosted lab fleet** back these scenes.
