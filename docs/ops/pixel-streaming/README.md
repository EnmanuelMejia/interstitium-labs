# Pixel Streaming — local bring-up helpers

_Last updated: 2026-10-01 (America/New_York)._

## Honesty

| Helper | What it is | What it is NOT |
|--------|------------|----------------|
| `scripts/pixel-streaming/dev-signaling-echo.py` | WebSocket accept + health/echo JSON | Unreal Pixel Streaming, SDP media, or a fleet |
| `docker-compose.yml` (this folder) | Same echo in a container | Hosted UE GPU stream |

Interstitium does **not** claim a live UE fleet. The open-web client at `/immersive/pixel-stream/` reconnects honestly and never invents frames.

## Quick path

```bash
# A) Python (preferred on this box)
pip install websockets
python3 scripts/pixel-streaming/dev-signaling-echo.py --port 8888

# B) Docker (optional)
cd docs/ops/pixel-streaming && docker compose up
```

Then open:

`/immersive/pixel-stream/?signaling=ws://127.0.0.1:8888`

You should see signaling open + an `il-dev-health` / echo frame. **No video track** until a real UE5 Pixel Streaming host answers with an SDP offer.

## Real host

Follow `/ops/PIXEL-STREAMING-DEV.md` — GPU box, UE5 plugin, Epic signaling. Point the same client at that `ws(s)://` URL. Optional ICE servers via `localStorage.il-ps-ice` (JSON array) — see client v1.1.0+.
