# Pixel Streaming — local / lab GPU runbook

_Last updated: 2026-10-01 (America/New_York)._  
_Client:_ https://interstitiumlabs.dev/immersive/pixel-stream/  
_Honesty:_ this runbook does **not** claim a live Interstitium-hosted UE fleet.

## Goal

Spin a **real** Unreal Engine 5 Pixel Streaming host against the Interstitium browser client. Without a host, the client stays an honest stub with reconnect backoff — it never invents video frames.

## Prerequisites

| Piece | Notes |
|-------|-------|
| UE5 project | Pixel Streaming plugin enabled (Epic) |
| GPU host | Lab box / P920 / cloud GPU — **not** Cloudflare Pages |
| Signaling | Default Epic sample often `ws://127.0.0.1:8888` (check your UE version) |
| Browser | Chromium/Edge with WebRTC |

## Quick path (dev)

1. On the GPU host, package or PIE with **Pixel Streaming** enabled; start the signaling server that ships with your UE Pixel Streaming stack.
2. Confirm WebSocket accept: `websocat ws://127.0.0.1:8888` (or browser DevTools) — optional smoke.
3. Open the client:
   - Local Pages preview: `/immersive/pixel-stream/?signaling=ws://127.0.0.1:8888`
   - Or paste the URL into the Connect form and click **Connect** / **Save**.
4. Status should move: *Connecting signaling…* → *Signaling open* → *Live Pixel Streaming track* when an offer + media arrive.
5. On drop: client **reconnects with exponential backoff** (cap 30s). It will not claim the fleet is online.

## Client config resolution (order)

1. Query: `?signaling=` / `?ps=` / `?pixel=`
2. Form input `#ps-signaling-input`
3. `data-ps-signaling` on `#ps-host`
4. `localStorage.il-ps-signaling`
5. `window.IL_LOCAL_CONFIG.pixelStreamingSignaling` (optional local override file — never commit secrets)

## CSP

- Pages CSP today allows **localhost / 127.0.0.1** `ws` / `wss` for lab bring-up.
- A public stream subdomain requires an explicit allowlist in `ENTERPRISE-SECURITY.md` at go-live. **Do not widen CSP until the host exists.**

## Failure modes (expected)

| Symptom | Meaning |
|---------|---------|
| Scaffold / empty state | No signaling URL — correct |
| Signaling error / closed | No UE host or firewall — correct; reconnect tries again |
| SDP negotiate failed | Streamer up but protocol mismatch — check UE PS version |
| Embed iframe path | Non-`ws(s)` URL treated as player page via `ILSceneKit.pixelStreamEmbed` |

## Related

- `/immersive/pixel-stream/` — client UI + `il-pixel-stream.js`
- `UNREAL-AND-BLENDER-PIPELINE.md` — dual pipeline
- `scripts/author_immersive_glb.py` — open-web glTF path (no UE required)


## 2026-10-01 — bring-up helpers (honest)

| Path | Role |
|------|------|
| `scripts/pixel-streaming/dev-signaling-echo.py` | Local WS accept + `il-dev-health` / echo — **NOT** UE Pixel Streaming media |
| `docs/ops/pixel-streaming/docker-compose.yml` | Same echo in Docker |
| `docs/ops/pixel-streaming/README.md` | Labels + quick path |

Client **v1.1.0** (`il-pixel-stream.js`):

1. **Health probe** before/alongside connect — reports `dev-echo` vs unreachable vs UE-style offer.
2. **ICE servers** from `localStorage.il-ps-ice` (JSON array of `{urls:…}` or `{iceServers:[…]}`) or `IL_LOCAL_CONFIG.pixelStreamingIce`.
3. Clearer **host-required** UX — never claims Interstitium-hosted UE fleet.

```bash
pip install websockets
python3 scripts/pixel-streaming/dev-signaling-echo.py --port 8888
# open /immersive/pixel-stream/?signaling=ws://127.0.0.1:8888
# Expect: Dev echo reachable — NOT UE media
```


## P920 UE host checklist (2026-10-02) — fail closed without a real UE binary

Honest gate: **none of these steps invent live Pixel Streaming media.** The browser client stays a stub until a real Unreal Engine 5 streamer answers signaling with an SDP offer + media track.

| # | Check | Pass criteria | Fail behavior |
|---|-------|---------------|---------------|
| 1 | GPU host online | P920 / lab GPU box reachable; NVIDIA driver OK | Stop — do not widen CSP |
| 2 | UE5 project present | Local `.uproject` with **Pixel Streaming** plugin enabled | Stop — kit glTF path remains the open-web 3D lane |
| 3 | Signaling server | Epic/UE PS signaling listening (often `ws://127.0.0.1:8888`) | Client: Signaling error / reconnect backoff |
| 4 | Dev echo only? | If using `scripts/pixel-streaming/dev-signaling-echo.py` or `docs/ops/pixel-streaming/docker-compose.yml` | Status may say signaling open — **no video**; labeled NOT UE media |
| 5 | Real streamer | UE PIE/packaged streamer connected to same signaling | Client status → *Live Pixel Streaming track* |
| 6 | Client URL | `/immersive/pixel-stream/?signaling=ws://HOST:PORT` | Without `?signaling=` → honest empty scaffold |
| 7 | CSP | Localhost `ws`/`wss` only until public host exists | Do not widen live CSP preemptively |
| 8 | Fleet claim | Hosted lab fleet still **absent** | Never claim KodeKloud-class fleets |

### Fail-closed docker skeleton (optional)

See `docs/ops/pixel-streaming/docker-compose.ue-host.skeleton.yml`. It **exits non-zero** unless `IL_UE_PIXEL_STREAMING_BIN` points at a real UE Pixel Streaming binary on the host. It never ships a fake video loop.

### Bring-up order (honest)

1. Prove WS reachability with the **dev echo** (not media).
2. Attach a **real UE5** streamer on the GPU host.
3. Only then treat status *Live Pixel Streaming track* as truth.
4. Hosted multi-user fleet remains a separate product milestone — out of scope until provisioned.

_Last checklist pass: 2026-10-02 (America/New_York). Musk verdict still requires live UE + hosted fleet for YES._

