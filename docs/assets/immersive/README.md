# Immersive glTF assets

Authored via **Interstitium glTF kit v2** (`scripts/author_immersive_glb.py`) — **glTF 2.0 binary** (`.glb`).

Kit-v2: higher-density meshes, chamfer boxes, spheres, pedagogical `extras` on nodes, LOD1 proxy meshes, Interstitium PBR (cyan `#5EEAD4` · gold `#D4A853` · void `#070B16`).

## Blender polish provenance (2026-10-01 · 2026-10-02 · 2026-10-05 · 2026-10-06)

**Polished via Blender CLI 4.2.3 LTS on 2026-10-01, 2026-10-02, 2026-10-05, and 2026-10-06 (America/New_York)** using `scripts/blender_polish_glb.py --all --promote`:

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
| `aws-vpc-multi-az.glb` | **NEW 2026-10-06** AWS SAA/CCP: VPC across us-east-1a/1b — IGW, ALB nodes, zonal NAT, ASG EC2 (+ hidden `sim-*` surge capacity), RDS primary + synchronous standby, endpoint CNAME. Drives the `aws-az-failure` sim (Blender-polished 2026-10-06) |
| `aws-iam-policy-eval.glb` | **NEW 2026-10-06** AWS IAM evaluation gates: explicit Deny → SCP/RCP → resource policy → identity → permissions boundary → session → ALLOW / implicit / explicit deny. Drives the `iam-eval` sim (Blender-polished 2026-10-06) |
| `rack-19u.glb` | Three rack frames with bay LEDs (Blender-polished 2026-10-02) |
| `hermetic-monas.glb` | Hermetica / Monas lecture (Blender-polished 2026-10-02) |
| `sim-superlab.glb` | SuperLab sim (rack + cluster combo) (Blender-polished 2026-10-02) |
| `muse-dee-monas.glb` | Lab Muse Dee/Monas avatar (Blender-polished 2026-10-01) |

Translucent pedagogy shells (e.g. the NetworkPolicy shield) use `alphaMode: BLEND` + `doubleSided` — emitted automatically by the kit when `baseColorFactor` alpha < 1.

## Interactive sims + node naming contract (2026-10-06)

`il-immersive-sims.js` derives per-node styles from a small state object (Raft quorum, AWS Multi-AZ failover, IAM evaluation) and `il-immersive-3d.js` v1.4.0 applies them to authored nodes (`data-il-sim="etcd-quorum|aws-az-failure|iam-eval"`). Predict-then-reveal: the scene does not change until the learner commits a prediction.

- `sim-*` nodes are hidden unless a sim state reveals them (e.g. ASG surge instances).
- `*_LOD1` (Blender decimate duplicates) and `lod1-*` (kit proxies) are **never drawn** by the curriculum player — they used to overdraw/z-fight LOD0 and the kit proxy slabs cut through scenes.
- `blender_polish_glb.py` now exports with `export_extras=True`, so kit pedagogy extras (labels, kind, `simOnly`) survive polish. Scenes polished before 2026-10-06 lost their extras; node names (the sim contract) were always preserved.
- `node --test scripts/tests/immersive-sims.test.js` fails if a sim rule addresses a node that is missing from its .glb.
- 2026-10-07 / 2026-10-08: sims now cover `network-policy-isolation`, `rbac-authz-graph`, `scheduling-affinity`, `hpa-autoscaling`, `storage-csi-pv`, `ingress-gateway`, `secrets-configmaps`, `cni-pod-network`, `service-mesh-sidecar` and `lecture-k8s-control-plane` (`data-il-sim` ids in `/assets/scenes/manifest.json` → `sims.list`). **No asset was regenerated or re-polished for these drills** — they re-tint, pulse, hide or reveal the existing named nodes from the 2026-10-01/02/05 Blender CLI polish.

Honest scope: authored + CLI-polished open-web glTF. **No live Unreal host and no hosted lab fleet** back these scenes.
