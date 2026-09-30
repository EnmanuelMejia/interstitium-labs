# Pixel Streaming — local / lab GPU runbook

_Last updated: 2026-09-30 (America/New_York)._  
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
