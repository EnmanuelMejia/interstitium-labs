**Product law (canonical):** [`IMMERSIVE-3D-CURRICULUM.md`](./IMMERSIVE-3D-CURRICULUM.md) · **P920 authoring:** [`UNREAL-AND-BLENDER-PIPELINE.md`](./UNREAL-AND-BLENDER-PIPELINE.md)

# Immersive 3D — curriculum-wide (lectures · cert labs · sims · non-cert)

**Rule (Musk gate):** Skipping Blender **and** Unreal = fail. Open-source path (Blender / Godot / Three) ships in-browser today; Unreal Pixel Streaming is scaffolded and documented — **do not block** the web ship on a local UE install.

**Companion:** Noah voice-reactive familiar (`LAB-MUSE-3D.md`) shares `ILSceneKit` with the immersive player.

## What shipped (2026-10-06) — interactive sims + render fixes

| Layer | Change |
|-------|--------|
| `/assets/il-immersive-sims.js` (new, UMD) | Rules engines that drive authored scenes: `etcd-quorum` (Raft floor(n/2)+1), `aws-az-failure` (ALB drain · ASG rebalance · RDS Multi-AZ failover), `iam-eval` (explicit Deny → SCP/RCP → resource → identity → boundary → session). Predict-then-reveal; `immersive_sim_predict` / `immersive_sim_state` analytics; per-device mastery in `localStorage` (`il.immersiveSims.v1`) picks the next drill. |
| `/assets/il-immersive-sims.js` v1.1.0 (2026-10-07) | +4 CKA sims over existing Blender-polished glTF: `netpol-isolation` (selected pod isolated; additive allow-lists; Egress isolation blocks DNS; non-enforcing CNI ignores policy), `rbac-authz` (binding kind sets scope; RoleBinding→ClusterRole never grants cluster-scoped nodes; additive only), `sched-taints` (filter: cordon · taints · required affinity; tolerations allow, preferences only score; cordon spares running pods), `hpa-scale` (autoscaling/v2 `ceil(current × util / target)`, 10% tolerance, clamp, hold without metrics/requests). Player v1.5.0 shuffles predict options per attempt (keyed answer was always first); toggles carry `risk` so the safe state is not painted red. |
| `/assets/il-immersive-sims.js` v1.2.0 (2026-10-08) | +6 drills — every CKA spatial scene is now interactive (no new assets; rules address existing node names): `storage-csi` (no default class → Pending; WaitForFirstConsumer; class/size/accessMode matching; RWO Multi-Attach; pvc-protection; Retain vs Delete), `ingress-routing` (no controller; Exact vs element-wise Prefix, longest match; 503 without ready endpoints; missing TLS Secret → controller default cert), `config-propagation` (volume after kubelet sync; env + subPath only on restart; immutable rejects edits; missing secretKeyRef key → CreateContainerConfigError; no encryption at rest by default), `cni-network` (no plugin → NotReady; pod CIDR overlap; kube-proxy owns ClusterIPs; CoreDNS owns names), `mesh-mtls` (injection only at pod creation; STRICT vs PERMISSIVE; istiod outage spares the data plane — Istio semantics), `control-plane-failure` on `lecture-k8s-control-plane.glb` (API down spares running pods; scheduler → Pending; kcm → no replacement / no NotReady marking; kubelet → NotReady after node-monitor-grace-period). Keyed answers vary by index. Player v1.6.0 keeps the authored-glTF provenance in sim captions. |
| `/assets/il-immersive-exam.js` v1.1.0 + `/assets/il-immersive-review.js` v1.0.0 (2026-10-13) | Adaptive remediation loop. Exam papers (misses + timeouts), CKA free-play drills, and review sessions write Leitner cards (boxes 0–6: now · 10 min · 1 d · 3 d · 7 d · 16 d · 35 d; correct-but-slow >45 s holds the box) to `localStorage il.immersiveReview.v1`. `/immersive/review/` re-mounts each card's authored `.glb` with `{"review":true}` and reveals the failure mode after the learner commits; weakest evidenced domains then untested domains top up the queue; the exam lobby's *Adaptive* paper puts 60% of items on the 3 weakest evidenced domains. Player marks exam/review stages `cfg.owned` so they never double-count as drills. Not FSRS, not a trained model, no server/cohort data. |
| `/assets/il-immersive-cli.js` v1.0.0 + `il-immersive-3d.js` v1.9.0 (2026-10-16) | In-scene **CLI lab**: free-play stages for `etcd-quorum`, `control-plane-failure`, `sched-taints`, `hpa-scale`, `aws-az-failure` get a collapsible simulated shell. Real kubectl / etcdctl / crictl / systemctl / static-pod `mv` / `aws rds` / `aws elbv2` / `curl` syntax is parsed in the browser and merged into the same sim state, so the authored glTF re-tints. 11 Killercoda-style tasks (ordered event steps, latched state steps, hints). On-device `il.immersiveCli.v1`; analytics verb + exit only. **Simulated** — not a shell, container, cluster or AWS account; unmodelled commands say so. Not mounted on graded exam/review stages. |
| `il-immersive-cli.js` v1.1.0 + `il-immersive-3d.js` v1.10.0 + `il-immersive-sims.js` v1.3.0 (2026-10-19) | **Lab Muse task coach** in the CLI lab (answer to Killercoda Brain): `check` / **Check** button verifies the task and explains why the next step is not verified (out of order · right command family, wrong state · live state false · last command failed/unmodelled), grounded in the live sim caption; 2nd failed check on a step auto-offers a tip (never the command); `solution` prints the command. Each of the 42 steps names authored glTF nodes (focus regex, unit-tested against the `.glb`) — the player pulses them gold ~9 s (also in WebXR); optional **Lab Muse voice** via browser `speechSynthesis`. Deterministic rules, not an LLM, not a real terminal. **#24 Codex review fixes:** prefers-reduced-motion / no-WebGL / failed `.glb` stages still mount the full drill with the static fallback (captions lifted out of the hidden stage); `verdictTone()` maps every verdict to ok/warn/bad (badge `data-tone`), so `data-deleted`, `exposed-at-rest`, `cert-warning`, `stale`, `terminating` no longer render healthy cyan; reclaim Delete hides `backend-disk-1`/`platter-1`. Exam/review boots no longer reset a stage over an answer committed before the scene finished mounting. |
| `il-immersive-cli.js` v1.2.0 + `il-immersive-3d.js` v1.11.0 + `il-immersive-review.js` v1.2.0 (2026-10-20) | **Four new CLI packs** (now 9 packs, 23 tasks, 99 steps): **NetworkPolicy** (`netpol-isolation`: lab YAML files + `kubectl apply -f`, `kubectl exec … -- curl/nslookup` probes, `describe networkpolicy`, `fault cni flannel|calico` — tasks lock-api / egress-dns / flannel), **RBAC** (`rbac-authz`: `kubectl auth can-i … --as alice` / `--as system:serviceaccount:dev:ci-bot` with exit 0/1, `--as` Forbidden messages, create/delete role / rolebinding / clusterrolebinding — least-privilege / cluster-scope / revoke), **storage** (`storage-csi`: reclaim `Retain` via `patch pv`, `kubernetes.io/pvc-protection` Terminating, default-class annotation — retain-data / pvc-protection / no-default-sc), **Ingress API** (`ingress-routing`: `curl` 7/404/503/200/60 from the rules engine, `pathType` JSON patch, EndpointSlices + Service selector, TLS secret — exact-404 / no-endpoints / tls; states that ingress-nginx was retired 2026-03-24 and Gateway API is the successor). Every step has a coach tip that never contains its command and a focus regex on real `.glb` nodes (unit-tested). **Coach-driven review cards:** a step where the learner typed `solution` or failed `check` twice becomes a Leitner card (`sim::cli:task:step`) in the existing `il.immersiveReview.v1` store; `/immersive/review/` re-mounts the authored stage with the shell, replays the earlier steps from their own solutions, and grades the typed step (verified without `solution` = recalled; `solution` / give-up = box 0). Due-only, never top-ups; mastery stays on predict checkpoints. **Optional voice-to-command:** Web Speech `SpeechRecognition` (feature-checked, hidden when unsupported, labelled) → `fromSpeech()` normaliser; lab verbs run, commands land in the prompt and are never auto-run. Analytics: `immersive_cli_review_card` (sim/task/step/how) and `immersive_cli_voice` (sim/kind/ok) — never command text or transcripts. |
| `il-immersive-sims.js` v1.4.0 + `il-immersive-cli.js` v1.3.0 + `il-immersive-exam.js` v1.2.0 + `il-immersive-review.js` v1.3.0 (2026-10-21) | **Gateway API drill** (`gateway-api` on the authored `ingress-gateway.glb`, `/immersive/#cka-gateway-api`, 5 predict checkpoints: no controller → GatewayClass/Gateway Pending, hostname mismatch → NoMatchingListenerHostname 404, Exact path, cross-namespace backendRef without ReferenceGrant → RefNotPermitted 500, missing certificateRefs Secret → InvalidCertificateRef / TLS failure) and its **CLI pack** (gw-pending · gw-hostname · gw-refgrant · gw-cert). **ConfigMap/Secret CLI pack** on `config-propagation` (volume-vs-env · immutable · missing-key; `sleep N` for kubelet sync, real `immutable` Forbidden message, CreateContainerConfigError, etcd plaintext vs aescbc). Now 11 packs / 30 tasks / 136 steps. **CKA blueprint score:** exam result + review lobby map drills to the 5 official CNCF CKA domains and weights, show the blueprint-weighted %, and name the weakest domain by points at stake (weight × share missed) with a link into its 3D drill; Lab Muse speaks the biggest gap. Labelled a study signal, not a predicted CNCF score; `GatewayClass lab-gw` is a lab implementation, not a live Gateway. |
| `node-troubleshoot.glb` (NEW asset) + `il-immersive-sims.js` v1.5.0 + `il-immersive-cli.js` v1.4.0 + `il-immersive-3d.js` v1.12.0 (2026-10-22) | **Worker-node troubleshooting** (CKA Troubleshooting, 30%). There is a new kit-v2 `.glb` with a Blender CLI polish: a node-01 cutaway showing systemd → kubelet → kubeadm drop-in → CRI socket → containerd → CNI conf, the node Lease to the API server / node lifecycle controller, QoS-ranked pods, a nodefs gauge (`sim-disk-fill-3/4`), journal pages and `sim-taint-flag`. The `node-troubleshoot` drill (`/immersive/#cka-node-troubleshoot`) has 5 predict checkpoints: 203/EXEC, daemon-reload, containerd down, CNI not initialized, DiskPressure. The CLI pack has 4 tasks (kubelet-203 · runtime-down · cni-missing · disk-pressure) with `ssh node-01` sessions: the prompt follows the host via `ILImmersiveCLI.promptFor`, and kubectl on the worker gets localhost:8080 refused. It also models systemctl / journalctl / `sed -i` on the drop-in / crictl / df. The pack is now 12 packs / 34 tasks / 160 steps, and the blueprint counts two Troubleshooting drills. The shell is **simulated**: no VM, no real kubelet, no clock, and the journal lines are labelled representative. |
| `service-dns.glb` (NEW asset) + `il-immersive-sims.js` v1.6.0 + `il-immersive-cli.js` v1.5.0 (2026-10-23) | **Service + DNS troubleshooting** (the other half of CKA Troubleshooting, 30%). New kit-v2 `.glb` with a Blender CLI polish: namespaces shop / kube-system / data, a client pod and its `resolv.conf`, Service `api` (port → targetPort, selector) → EndpointSlice → api pods (containerPort 8080), kube-proxy, `kube-dns` → CoreDNS pods + Corefile ConfigMap, a namespace egress NetworkPolicy wall and Service `db`. The `service-dns` drill (`/immersive/#cka-service-dns`) has 5 predict checkpoints: selector matches nothing (empty EndpointSlice → refused), targetPort ≠ containerPort, Corefile typo (CoreDNS CrashLoopBackOff → lookups refused, ClusterIPs still work), default-deny egress without a 53 rule (lookups time out), short name across namespaces (NXDOMAIN). `ILImmersiveSims.svcDnsResolve` models the search list with ndots:5. The CLI pack has 4 tasks (target-port · coredns-corefile · dns-egress · cross-ns-fqdn) with a `dnsutils` debug pod (nslookup / dig `+short` `+search` / `cat /etc/resolv.conf`), CoreDNS logs, `kubectl get cm -o yaml > FILE` + `sed -i` + `apply -f`, `kubectl set env`. Now 13 packs / 38 tasks / 184 steps; the blueprint counts three Troubleshooting drills; the exam lobby says 13 drills. Player unchanged (v1.12.0). The shell is **simulated**: no live cluster, no real CoreDNS, no internet upstream, no clock. |
| `il-immersive-3d.js` v1.4.0 | `data-il-sim` panel; per-node tint/glow/pulse/reveal eased each frame; **skips `*_LOD1` / `lod1-*`** (no more double draw / z-fight / proxy slabs through scenes); **lazy WebGL contexts** (create near viewport, `WEBGL_lose_context` when off-screen — /immersive/ had hit Chromium's 16-context cap); boot waits for `ILSceneKit` (pages that loaded the kit after the player silently fell back to procedural — e.g. `/learn/`). |
| `il-scene-kit.js` v1.4.0 | `parseGlb` returns owning node `name`, `extras`, `lod` per mesh. |
| `il-immersive.js` v1.1.0 | `data-kind` hosts with an authored `.glb` delegate to the curriculum player (they previously drew a procedural pedestal while the badge said “Three/glTF”). |
| `il-curriculum-sync.js` 1.2.1 | Element's own `data-gltf`/title/kind win over the surface default (every /immersive/ host had been re-stamped with one `.glb`; the Unreal stub got a glTF). |
| Tests | `scripts/tests/immersive-sims.test.js` (rules + glb validity + sim↔node contract, in `npm test`/CI) · `npm run test:immersive:browser` (headless Chromium, WebGL, predict→reveal). |

## What shipped (2026-09-29)

| Layer | Asset | Status |
|-------|-------|--------|
| Shared kit | `/assets/il-scene-kit.js` | WebGL helpers, **`parseGlb`**, `loadGltf`, Pixel Streaming embed, speak-amp bus |
| Curriculum scaffold | `/assets/il-immersive-3d.js` + `.css` | Native GLB fetch/parse/draw + procedural fallback; owns `[data-il-scene]` |
| Kit assets | `/assets/immersive/*.glb` | **Live** kit-authored glTF 2.0 (Blender-compatible; polish on P920) |
| Authoring | `scripts/author_immersive_glb.py` | Regenerates lecture/cert/rack/hermetic/sim GLBs |
| Demo player | `/assets/il-immersive.js` + `.css` | `/immersive/` + `data-kind` hosts; skips `data-il-scene` |
| Muse 3D | `/assets/il-muse-3d.js` | Voice-reactive Monas; exposes `.kit` / `.immersive` getters |
| Pixel Streaming | `/immersive/pixel-stream/` | Honest client shell (signaling required; no fake video) |
| Docs | this file + pipeline | Blender → glTF, Godot, Unreal Pixel Streaming |

Honest claim: **authored kit `.glb` + procedural fallback are live** (CSP-safe, no CDN Three). Photoreal Unreal rooms and P920 Blender-polished artist sets are **not** YES yet — Pixel Streaming client path exists; live streamer host does not.

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

Voice amp from Noah (`il-muse-speak-amp` / `il-muse-speak-boundary`) drives immersive emissive when both are on-page (cinema Learn|Lab|Muse).

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
- Muse 3D exceeds flat assistant-class motion; curriculum immersive is the same philosophy applied to lectures/labs.

## Sync

```bash
./scripts/sync-mobile-web.sh
```
