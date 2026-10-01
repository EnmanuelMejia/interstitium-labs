#!/usr/bin/env python3
"""
Interstitium Labs — local signaling bring-up helper (DEV ONLY).

Honest labels:
  - This is NOT Unreal Engine Pixel Streaming.
  - This does NOT send video, SDP offers from a UE host, or a fleet.
  - It only accepts WebSocket connections, answers a tiny health JSON,
    and echoes text frames so you can verify browser CSP + ws://localhost
    reachability before pointing the client at a REAL UE signaling server.

Usage:
  python3 scripts/pixel-streaming/dev-signaling-echo.py [--host 127.0.0.1] [--port 8888]
  # then open /immersive/pixel-stream/?signaling=ws://127.0.0.1:8888
  # Expect: socket open + health/echo frames — NEVER a live UE video track.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import signal
import sys
from datetime import datetime, timezone

BANNER = (
    "Interstitium DEV signaling echo — NOT Unreal Pixel Streaming media. "
    "No fleet. No video. Bring-up only."
)

try:
    import websockets
    from websockets.server import serve
except ImportError:
    websockets = None


async def handler(websocket):
    peer = getattr(websocket, "remote_address", None)
    hello = {
        "type": "il-dev-signaling-echo",
        "honest": True,
        "isUnrealPixelStreaming": False,
        "isFleet": False,
        "message": BANNER,
        "peer": str(peer),
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    await websocket.send(json.dumps(hello))
    try:
        async for message in websocket:
            # Echo + annotate; never invent SDP/media
            if isinstance(message, bytes):
                await websocket.send(message)
                continue
            try:
                msg = json.loads(message)
            except Exception:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "echo",
                            "isUnrealPixelStreaming": False,
                            "payload": message[:500],
                        }
                    )
                )
                continue
            # If client sends UE-like {type: connect}, reply with honest refusal of media
            t = msg.get("type") or msg.get("Type") or ""
            if t == "connect":
                await websocket.send(
                    json.dumps(
                        {
                            "type": "il-dev-health",
                            "ok": True,
                            "isUnrealPixelStreaming": False,
                            "isFleet": False,
                            "note": "Signaling path reachable. Start a real UE Pixel Streaming host for SDP/media.",
                            "ts": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                )
            else:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "echo",
                            "isUnrealPixelStreaming": False,
                            "echoOf": t or "unknown",
                            "payload": msg,
                        }
                    )
                )
    except Exception:
        pass


async def main_async(host: str, port: int):
    if websockets is None:
        print(
            "ERROR: websockets package missing.\n"
            "  pip install websockets\n"
            "Or use docker-compose in docs/ops/pixel-streaming/ (still NOT UE media).",
            file=sys.stderr,
        )
        return 1
    print(BANNER)
    print(f"Listening ws://{host}:{port} — health/echo only. Ctrl+C to stop.")
    async with serve(handler, host, port):
        stop = asyncio.Future()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, stop.set_result, None)
            except NotImplementedError:
                pass
        await stop
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="IL DEV signaling echo (NOT UE Pixel Streaming)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8888)
    args = ap.parse_args(argv)
    return asyncio.run(main_async(args.host, args.port))


if __name__ == "__main__":
    raise SystemExit(main())
