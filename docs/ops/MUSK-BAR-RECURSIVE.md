# Musk bar — recursive scorecard

_Last updated: 2026-10-09 ~09:40 EDT (America/New_York)._  
_Live:_ https://interstitiumlabs.dev

## Verdict — 2026-10-08/09 Musk-bar pass

_Built 2026-10-08; that run stopped before shipping because the browser suite failed. Shipped 2026-10-09 after fixing the cause: the test read `_authored` on stages that had released their WebGL context off-screen (v1.4.0 context cap) before they woke and re-uploaded. The product path was correct; the test now waits for wake → re-upload. Also defused the fake PEM fixture in `noah-session.test.js` so `security-check.sh` passes again._

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| Recursive question | Asked | Would Elon be impressed by THIS mediocrity? After yesterday, **storage CSI, Ingress, Secrets/ConfigMaps, CNI and service mesh were still orbit-only dioramas**, and the control-plane lecture scene — the first thing every CKA learner meets — was a spinning prop with no failure drill. Audit also found sim stages **overwrote the authored-glTF provenance caption** (node count / LOD1 skipped) with the sim caption, and every keyed answer in the data was still index 0 (shuffled on screen, but the browser test only ever clicked option 0). **No.** |
| After this ship | **Closer / still NO** | **Every CKA spatial scene is now a stateful drill (11 CKA-side sims + 2 AWS)**: storage (no default StorageClass, WaitForFirstConsumer, size/accessMode/class matching, RWO Multi-Attach, pvc-protection, Retain vs Delete), Ingress (no controller, Exact vs element-wise Prefix, 503 with no ready endpoints, missing TLS Secret → controller default cert), ConfigMap/Secret propagation (volume after kubelet sync, env + subPath only on restart, immutable, missing key → CreateContainerConfigError, base64 ≠ encryption at rest), CNI (NotReady without a plugin, pod CIDR overlap, kube-proxy owns ClusterIPs, CoreDNS owns names), mesh (injection only on new pods, STRICT vs PERMISSIVE, data plane survives istiod), control plane (API down spares running pods, scheduler → Pending, kcm → no replacement and no NotReady marking, kubelet → NotReady after node-monitor-grace-period). **31 new predict-then-reveal checkpoints**, keyed answers spread across positions. Still **no live UE host**, **no hosted fleet / live cluster**. |
| Fake YES risk | Rejected | Rules engine over the existing Blender-polished glTF (no new assets). Mesh drill is labelled Istio semantics, not CKA core. Controller-specific behaviour (ingress-nginx default cert) is called out as such. |

## Scorecard (0–10, self-assessed rubric — not measured) — 2026-10-08

| Dimension | Prior (10-07) | Now | Notes |
|---|---:|---:|---|
| First-glance wow | 9.0 | 9.0 | Same scenes; more of them react |
| Live labs density | 7.0 | **7.4** | 13 interactive sims (was 7); still no hosted fleet |
| Adaptive learning | 7.6 | **7.8** | 31 more scored checkpoints feed per-sim next-drill |
| Honesty / trust | 9.9 | 9.9 | Sim captions now also keep the authored-glTF provenance |
| Curriculum SoT | 9.0 | **9.2** | 6 new published `lab-sim-*` in labs + mirror; manifest scenes carry `sim` + anchored gallery |
| Immersive / 3D gate | 9.3 | **9.5** | No CKA spatial scene is orbit-only any more |

**Musk YES? NO — Closer.** Blockers unchanged: **(B) live UE Pixel Streaming host**, **(C) hosted lab fleet / live cluster sandbox**. Next cheapest win: an exam mode that chains drills under a timer (killer.sh-style pressure) and a troubleshooting "mystery" mode where the learner must find which toggle was flipped.

## Competitor delta (2026-10-08)

Not re-researched today — the 2026-10-07 table below still stands. Today's delta: peers (KodeKloud, Killercoda, A Cloud Guru) teach PV/PVC binding, Ingress pathType, ConfigMap propagation and control-plane troubleshooting as video + terminal; IL now has a predict-then-reveal 3D drill for each, while they keep the real-cluster advantage.

## Shipped this pass (2026-10-08)

1. `il-immersive-sims.js` v1.2.0: `storage-csi`, `ingress-routing`, `config-propagation`, `cni-network`, `mesh-mtls`, `control-plane-failure` (pure helpers `storageDecide` / `ingressMatch` / `ingressDecide` / `configDecide` / `cniDecide` / `meshDecide` / `controlPlaneDecide` exported for tests)
2. Player v1.6.0: sim captions keep the authored .glb provenance
3. Wired on `/immersive/` (new `#cka-storage`, `#cka-ingress`, `#cka-cni`, `#cka-service-mesh`, `#cka-control-plane`; `#cka-secrets-configmaps` now interactive), `/labs/` links, curriculum OS labs + mirror, manifest `cka_coverage.interactive` / `sims.list` / scene `sim` fields
4. Tests: 7 new unit tests (K8s semantics per drill + wiring/answer-spread check); browser suite runs all 13 sims with the keyed answer by index, plus storage / mesh / ingress / CNI / config / control-plane toggles and a provenance-caption check on every sim stage

---

## Verdict — 2026-10-07 Musk-bar pass

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| Recursive question | Asked | Would Elon be impressed by THIS mediocrity? Yesterday made 1 of 10 CKA scenes interactive — the other nine (NetworkPolicy, RBAC, scheduling, HPA …) were still **dioramas you could only orbit**. Audit also found every predict-then-reveal question keyed to **option 0** (a learner could “master” every drill by always clicking the first button) and safe toggle states painted red. **No.** |
| After this ship | **Closer / still NO** | **5 of 10 CKA domains now interactive**: NetworkPolicy (default-deny, additive allow, egress-DNS trap, non-enforcing CNI), RBAC (RoleBinding vs ClusterRoleBinding scope, namespace, additive-only), scheduler (taint filters affinity, tolerations don't attract, cordon vs drain), HPA (`ceil(current × util / target)`, tolerance, clamp, `<unknown>` without requests). 16 new predict-then-reveal checkpoints. Options shuffle per attempt. Still **no live UE host**, **no hosted fleet / live cluster**. |
| Fake YES risk | Rejected | Rules engine over authored glTF; every caption says "sim (rules engine, not a live system)". Kubernetes semantics pinned by unit tests. |

## Scorecard (0–10) — 2026-10-07

| Dimension | Prior (10-06) | Now | Notes |
|---|---:|---:|---|
| First-glance wow | 9.0 | 9.0 | Same scenes — now they react |
| Live labs density | 6.5 | **7.0** | 7 interactive sims (was 3); still no hosted fleet |
| Adaptive learning | 7.3 | **7.6** | Predict data is now meaningful (no positional answer); next-drill per sim |
| Honesty / trust | 9.9 | 9.9 | Unchanged rules-engine disclosure |
| Curriculum SoT | 8.8 | **9.0** | 4 new published `lab-sim-*` in labs + mirror; manifest `cka_coverage.interactive` |
| Immersive / 3D gate | 9.1 | **9.3** | Half of CKA spatial domains are now stateful 3D, not static |

**Composite ~8.5/10. Musk YES? NO — Closer.** Blockers unchanged: **(B) live UE Pixel Streaming host**, **(C) hosted lab fleet / live cluster sandbox**. Next cheapest win: make CNI / Ingress / Storage CSI / Secrets / mesh interactive (5 left), then an exam-mode that chains drills under a timer.

## Competitor delta (2026-10-07, fresh check)

| Peer | Still wins | IL exceed today |
|------|------------|-----------------|
| KodeKloud Pro ($252/yr) | 3 CKA mock exams, 60+ playgrounds, AI-assisted labs | Their RBAC/NetworkPolicy/scheduling theory is video + slides; IL makes each one a stateful 3D object you break and predict |
| Killercoda (free) | 100+ instant browser K8s scenarios | Terminals without a mental model; IL shows *why* the pod is Pending / Forbidden / dropped |
| A Cloud Guru / Pluralsight | 1,800+ labs, cloud sandboxes | Catalog breadth; few K8s-specific visual drills |

## Shipped this pass (2026-10-07)

1. `il-immersive-sims.js` v1.1.0: `netpol-isolation`, `rbac-authz`, `sched-taints`, `hpa-scale` (pure helpers `netpolDecide` / `rbacDecide` / `schedDecide` / `hpaDesired` exported for tests)
2. Player v1.5.0: per-attempt option shuffle (`shuffleOrder`), toggle `risk` colouring
3. Wired on `/immersive/` (new `#cka-rbac`, `#cka-hpa` anchors), curriculum OS labs + mirror, manifest `cka_coverage.interactive`
4. Tests: 5 new unit tests (K8s semantics + shuffle permutation); browser suite runs all 7 sims + RBAC toggle

---

## Verdict — 2026-10-06 Musk-bar pass

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| Recursive question | Asked | Would Elon be impressed by THIS mediocrity? Ten CKA scenes were **static dioramas** (clips only nudged glow), AWS track was `procedural:rack` in “review”, and an audit found the /immersive/ grid drawing a procedural pedestal under a “Three/glTF” badge, `/learn/` falling back to procedural (scene-kit load order), every /immersive/ host re-stamped with one `.glb`, LOD1 duplicates double-drawn, and 18 WebGL contexts on one page (Chromium cap 16) — **no**. |
| After this ship | **Closer / still NO** | **State now changes the scene**: etcd quorum, AWS Multi-AZ failure, IAM evaluation sims with predict-then-reveal + analytics + next-drill. **AWS SAA/CCP goes 3D-first** (two new Blender-polished glTFs wired into both AWS paths + curriculum OS). Render honesty bugs fixed and covered by tests. Still **no live UE host**, **no hosted lab fleet / live AWS sandbox**. |
| Fake YES risk | Rejected | Sims are an in-browser rules engine over authored glTF and every caption says so. No AWS account, no cluster, no GPU host. |

## Scorecard (0–10) — 2026-10-06

| Dimension | Prior (10-05) | Now | Notes |
|---|---:|---:|---|
| First-glance wow | 8.8 | **9.0** | Failure re-tints the architecture live; ASG surge instances appear |
| Motion / graphics | 8.6 | **8.8** | LOD1 overdraw/z-fight + proxy slabs gone; eased per-node tint |
| Live labs density | 6.0 | **6.5** | 3 interactive sims (rules engine) — still no hosted fleet |
| Adaptive learning | 7 | **7.3** | Predict accuracy + latency → next drill; analytics events |
| Honesty / trust | 9.8 | **9.9** | Removed a false “Three/glTF” badge + silent procedural fallbacks |
| Curriculum SoT | 8.5 | **8.8** | AWS certs/labs/assets3d + manifest v5 `sims` block |
| Immersive / 3D gate | 8.8 | **9.1** | 3D-first now spans CKA **and** AWS SAA/CCP; scenes are interactive |

**Composite ~8.3/10. Musk YES? NO — Closer.** Blockers unchanged: **(B) live UE Pixel Streaming host**, **(C) hosted lab fleet / live cloud sandbox**.

## Competitor delta (2026-10-06, fresh check)

| Peer | Still wins | IL exceed today |
|------|------------|-----------------|
| AWS Cloud Quest v2.0 (Aug 11 2026) | 3D city, AI customer dialogs, 130+ live AWS builds, badges | Cloud Quest's 3D is the city; the architecture is a flat solution diagram. IL's architecture **is** the 3D object and reacts to AZ failure / IAM statements, with predict-then-reveal |
| KodeKloud SAA design challenge + AWS playground | Real AWS sandbox | Their design challenge is drag-and-drop 2D; IL ships spatial failure drills (no sandbox — honest) |
| A Cloud Guru / Pluralsight | 1,800+ labs, sandboxes | IL interactive 3D cert stages for CKA + AWS (catalog far smaller) |
| KodeKloud CKA | Hosted labs + AI Tutor | etcd quorum loss drill in 3D with Raft-correct outcomes |

## Shipped this pass (2026-10-06)

1. **AWS SAA/CCP 3D-first**: `aws-vpc-multi-az.glb`, `aws-iam-policy-eval.glb` (kit-v2 → Blender 4.2.3 CLI polish, extras now preserved) on `/immersive/`, `/paths/aws-cloud-practitioner-plus/`, `/paths/aws-cloud-ops/`; `cert-aws-cp-plus` review → published with glTF
2. **Interactive sims** (`il-immersive-sims.js` + player v1.4.0): `etcd-quorum`, `aws-az-failure`, `iam-eval` — also on `/paths/k8s-cka-exceed/` hero
3. **Render honesty fixes**: LOD1 skip, lazy WebGL contexts, scene-kit boot order, data-kind delegation, curriculum-sync stamping
4. **Tests**: `scripts/tests/immersive-sims.test.js` in `npm test` (CI); `npm run test:immersive:browser`

---

## Verdict — 2026-10-05 Musk-bar pass

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| Recursive question | Asked | Would Elon be impressed by THIS mediocrity? Weekend shipped flat AI/learn sequences with zero new spatial .glb — **no**. |
| After this ship | **Closer / still NO** | Three new Blender-polished CKA glTFs close the last flat CKA gaps: **NetworkPolicy isolation**, **Secrets vs ConfigMaps**, **Scheduling (affinity/taints/tolerations)**. `/learn/` lecture stage now loads authored `lecture-k8s-control-plane.glb` (pending/procedural-only scaffold retired). Scene manifest v4 covers every authored scene. Still **no live UE host**, **no hosted lab fleet**. |
| Fake YES risk | Rejected | Kit-v2 + Blender 4.2.3 CLI polish only. PS checklist re-run 2026-10-05 fails closed (no GPU / UE binary on box). |

## Scorecard (0–10) — 2026-10-05

| Dimension | Prior (10-02) | Now | Notes |
|---|---:|---:|---|
| First-glance wow | 8.7 | **8.8** | /learn/ hero stage is now authored glTF, not procedural |
| Motion / graphics | 8.5 | **8.6** | Translucent BLEND shield (first alpha material in kit) |
| Live labs density | 6.0 | 6.0 | Still no hosted fleet (do not fake) |
| Honesty / trust | 9.8 | 9.8 | Checklist date bumped with real fail-closed evidence |
| Curriculum SoT | 8.3 | **8.5** | assets3d + mirror certs + manifest v4 complete |
| Immersive / 3D gate | 8.5 | **8.8** | CKA spatial coverage: etcd, CNI, RBAC, mesh, CSI, Ingress, HPA, NetworkPolicy, Secrets/ConfigMaps, Scheduling |

**Composite ~8.0/10. Musk YES? NO — Closer.** Blockers unchanged: **(B) live UE Pixel Streaming host**, **(C) hosted lab fleet**.

## Competitor delta (2026-10-05)

| Peer | Still wins | IL exceed today |
|------|------------|-----------------|
| KodeKloud | Hosted labs + AI Tutor in-lab | Spatial NetworkPolicy allow/deny, Secret-vs-ConfigMap mounts, scheduler filter/score/bind — peers ship flat diagrams + terminals |
| Killercoda | Instant browser terminals | 10 CKA domains as authored 3D scenes (no fake fleet) |
| A Cloud Guru | Catalog breadth + sandboxes | 3D-first CKA graph scenes with pedagogical node labels |

---

## Verdict — 2026-10-02 Musk-bar pass

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| Recursive question | Asked | Would Elon be impressed by THIS mediocrity? |
| After this ship | **Closer / still NO** | Three new Blender-polished CKA pedagogy glTFs (storage CSI/PV, Ingress gateway, HPA) + kit polish promote (rack/hermetic/superlab) + Lab Muse 3D v1.5 amp→material/LOD + honest P920 UE host checklist. Still **no live UE host**, **no hosted lab fleet**. |
| Fake YES risk | Rejected | Provenance honest: kit-v2 + Blender 4.2.3 CLI polish. PS UE skeleton fails closed without real binary. |

## Scorecard (0–10) — 2026-10-02

| Dimension | Prior (10-01) | Now | Notes |
|---|---:|---:|---|
| First-glance wow | 8.5 | **8.7** | Storage + Ingress + HPA spatial scenes on /immersive/ |
| Motion / graphics | 8.4 | **8.5** | More Blender-CLI-polished surfaces; Muse v1.5 material amp |
| Adaptive learning | 7 | 7 | Unchanged |
| Live labs density | 6.0 | 6.0 | Still no hosted fleet (do not fake) |
| Noah | 7.6 | **7.8** | Noah career workspace already on main; Muse amp exceed |
| Model router | 5 | 5 | — |
| Career prep | 7.5 | **8.0** | Noah jobs workspace landed via PR #12 (not this pass) |
| Honesty / trust | 9.7 | **9.8** | UE host skeleton exits 1 without real binary |
| Mobile / ultrawide | 6 | 6 | sync-mobile-web after ship |
| Curriculum SoT | 8.0 | **8.3** | assets3d + mirror certs for storage/ingress/HPA |
| Immersive / 3D gate | 8.2 | **8.5** | Three flat-diagram domains now spatial + polished |

**Composite ~7.9/10. Musk YES? NO — Closer.** Remaining blockers unchanged: **(B) live UE Pixel Streaming host**, **(C) hosted lab fleet**. Optional: hand-sculpted artist polish beyond CLI.

## Shipped this pass (2026-10-02)

1. **New pedagogical glTF** (kit-v2 → Blender CLI polish → promote): `storage-csi-pv.glb`, `ingress-gateway.glb`, `hpa-autoscaling.glb`
2. **Promoted polish** on previously kit-only: `rack-19u.glb`, `hermetic-monas.glb`, `sim-superlab.glb` (`k8s-cluster.glb` already polished alias — skipped)
3. **Wired** `/immersive/` sections + `curriculum-os/assets3d.json` + `mirror.json` certs
4. **Lab Muse 3D v1.5.0** — per-node ampRole (core/accent/body/lod) → emissive boost, differential breathe, LOD hide when amp high
5. **Pixel Streaming honesty** — P920 UE host checklist in `PIXEL-STREAMING-DEV.md` + fail-closed `docker-compose.ue-host.skeleton.yml`
6. Built on main after Noah PR #12 merge (e4d5907) — no regression of Noah assets

## Competitor delta (this pass)

| Peer | Still wins | IL exceed today |
|------|------------|-----------------|
| KodeKloud | Hosted labs fleet + AI Tutor in-lab | Spatial **storage / Ingress / HPA** pedagogy peers keep as flat 2D; Muse amp→material/LOD |
| A Cloud Guru / Skillsoft / LF training | Catalog breadth + some hosted sandboxes | IL 3D-first CKA graph scenes + honest UE bring-up path |
| Killercoda | Instant browser terminals | IL spatial cert stage (no fake fleet) |
| Meta Muse | Voice UX polish / product chrome | IL authored Dee/Monas glTF with amp→emissive/scale/LOD — local/OSS, no fake cloud |

---

## Verdict — 2026-10-01 Musk-bar pass

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| Recursive question | Asked | Would Elon be impressed by THIS mediocrity? |
| After this ship | **Closer / still NO** | Blender **CLI polish** on priority + new pedagogical `.glb` landed. Pixel Streaming bring-up helpers + health/ICE. Still **no live UE host**, **no hosted lab fleet**, polish is CLI not hand-sculpted artist sets. |
| Fake YES risk | Rejected | Provenance honest: Blender 4.2.3 CLI shade-smooth/weighted-normals/LOD1 on kit meshes. Dev signaling echo labeled NOT UE media. |

## Scorecard (0–10) — 2026-10-01

| Dimension | Prior (09-30) | Now | Notes |
|---|---:|---:|---|
| First-glance wow | 8.2 | **8.5** | CNI + RBAC + mesh spatial scenes + polished surfaces |
| Motion / graphics | 8.0 | **8.4** | Real Blender CLI polish path executed (not handoff-only) |
| Adaptive learning | 7 | 7 | Unchanged |
| Live labs density | 6.0 | 6.0 | Still no hosted fleet (do not fake) |
| Noah | 7.5 | 7.6 | Muse glTF Blender-polished |
| Model router | 5 | 5 | — |
| Career prep | 7.5 | 7.5 | — |
| Honesty / trust | 9.6 | **9.7** | PS health probe distinguishes dev-echo vs UE offer |
| Mobile / ultrawide | 6 | 6 | sync-mobile-web after ship |
| Curriculum SoT | 7.5 | **8.0** | assets3d + labs/certs/lectures wired for new scenes |
| Immersive / 3D gate | 7.5 | **8.2** | Blender polish A-path closed; B/C still open |

**Composite ~7.7/10. Musk YES? NO — Closer.** Remaining blockers: (B) live UE Pixel Streaming host, (C) hosted lab fleet, plus optional hand-sculpted artist polish beyond CLI.

## Shipped this pass (2026-10-01)

1. **Blender 4.2.3 LTS** installed on authoring box; `blender_polish_glb.py` hardened (`--all`, `--promote`, fail-loud without `--write-only`)
2. **CLI-polished + promoted** `.glb`: cert-cka, cka-etcd-quorum, muse-dee-monas, lecture-k8s-control-plane, cni-pod-network, rbac-authz-graph, service-mesh-sidecar
3. **New competitive pedagogical scenes**: `cni-pod-network.glb`, `rbac-authz-graph.glb`, optional `service-mesh-sidecar.glb` — wired into curriculum OS + `/immersive/`
4. **Pixel Streaming honesty**: `scripts/pixel-streaming/dev-signaling-echo.py` + `docs/ops/pixel-streaming/`; client v1.1.0 health probe + ICE localStorage
5. Recursive competitor note updated (this file + COMPETITIVE-AUDIT)

## Competitor delta (this pass)

| Peer | Still wins | IL exceed today |
|------|------------|-----------------|
| KodeKloud | Hosted labs fleet + AI Tutor in-lab | Authored **spatial** CNI/RBAC/mesh pedagogy + Blender-polished glTF; Noah Live Assist — **no fake fleet** |
| Brilliant / Codecademy / ALEKS | Adaptive polish / path UX | IL 3D-first curriculum stages peers mostly keep flat |
| Peer LMS 3D | Mostly video / 2D diagrams | IL ships polished glTF binaries + honest UE PS bring-up path |

---

## Prior verdict — 2026-09-29 morning pass

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| Recursive question | Asked | Would Elon be impressed by THIS mediocrity? |
| After this ship | **Closer / still NO** | Kit-authored `.glb` live + native GLB→WebGL loader + Pixel Streaming **client path** shipped. Still no live UE host, no P920 Blender polish, no hosted lab fleet. |
| Fake YES risk | Rejected | Provenance honest: kit glTF (Blender-compatible), not hand-sculpted artist sets. PS page is real client shell, not wallpaper video. |

## Scorecard (0–10) — 2026-09-29

| Dimension | Prior (09-28) | Now | Notes |
|---|---:|---:|---|
| First-glance wow | 8.0 | **8.2** | Authored meshes on `/immersive/` |
| Motion / graphics | 7.5 | **8.0** | Native `parseGlb` + draw authored; procedural fallback honest |
| Adaptive learning | 7 | 7 | Adapt unchanged this pass |
| Live labs density | 6.0 | 6.0 | Still no hosted fleet (do not fake) |
| Noah | 7.5 | 7.5 | Live Assist unchanged |
| Model router | 5 | 5 | Demand-tier OSS |
| Career prep | 7.5 | 7.5 | — |
| Honesty / trust | 9.5 | **9.6** | Caption modes: authored .glb vs procedural fallback; PS stub honest |
| Mobile / ultrawide | 6 | 6 | — |
| Curriculum SoT | 7 | **7.5** | `assets3d` published + mirror asset paths → real `.glb` |
| Immersive / 3D gate | ~6.5 | **7.5** | Real glTF binaries + PS client path (no live streamer) |

**Composite ~7.4/10. Musk YES? NO — Closer.** Kit glTF + PS client path are required steps; YES still needs P920 Blender polish + live UE stream (or packaged fidelity) + hireable proof density / hosted fleet honesty.

## Shipped this pass (answer the mediocrity)

1. **Real `.glb` assets** under `/assets/immersive/` via `scripts/author_immersive_glb.py` (glTF 2.0 binary; cyan/gold/void materials)
2. Retired `.pending.json` scaffolds for those ids; README provenance honesty
3. **`ILSceneKit.parseGlb`** + `loadGltf` native path (CSP-safe, no Three CDN); VERSION 1.2.0
4. **`il-immersive-3d.js`** fetch → parse → upload → `_renderAuthored`; caption/HUD mode honesty; v1.3.0
5. **Pixel Streaming client** at `/immersive/pixel-stream/` (WebRTC signaling attempt or embed; never fake video)
6. Curriculum mirror / `assets3d.json` → `publishStatus: published`; sync stamps `data-gltf`
7. Pipeline + Enterprise Security docs: future CSP allowlist for stream subdomain — **not** widened live today

## Competitor delta (this pass)

| Peer | Delta | IL response |
|------|-------|-------------|
| KodeKloud **AI Tutor Live Assist** | Real-time in-lab help + hosted labs | Noah Live Assist remains; **still no hosted fleet** (honest) |
| Brilliant **Koji** | Adaptive tutor UI | Adapt + Noah remain CAT/fringe + Socratic; not a Koji clone |
| Peer LMS 3D | Most still flat video / 2D diagrams | IL ships **real glTF meshes** + **Pixel Streaming client path** to stay generations ahead of flat LMS |

## Immersive 3D gate (product law)

**Not using Blender/Unreal (or Blender → glTF → Godot/Three) = fail Elon test.**

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| CSS cards as “3D” | **NO** | Flat chrome ≠ spatial curriculum |
| Skip Blender/Unreal authoring forever | **NO** | Kit glTF is Blender-openable; UE PS client path real; P920 polish still open |
| Authored `.glb` + native loader + PS client | Closer | Still need live UE host + Blender artist polish for YES |

See `IMMERSIVE-3D-CURRICULUM.md` · `UNREAL-AND-BLENDER-PIPELINE.md` · `ANTI-MEDIOCRITY-ELON-GATE.md`.  
Noah (`il-muse-3d`) ≠ curriculum scenes (`il-immersive-3d`).

---

## Prior verdict (2026-09-28)

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| After 2026-09-28 ship | **Closer / still NO** | Curriculum OS + WebGPU flag + Noah Live Assist + procedural wow. No authored `.glb`, no live UE PS. |

## Prior verdict (2026-09-22)

| Checkpoint | Impressed? | Why |
|---|:---:|---|
| After 2026-09-22 ship | **NO** | Instant Demo + CotD + peer matrix + exceed paths. Still no hosted fleet / default live model. |

Do not claim yes while fleet is one SuperLab and UE streamer is offline.
