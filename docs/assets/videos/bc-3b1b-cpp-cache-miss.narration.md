# The Cache Miss That Cost 100x — Narration Script

**Course:** C++ · Systems & Performance  
**Video:** `bc-3b1b-cpp-cache-miss.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Row-major vs column-major on a 64x64 grid: 0.02s vs 0.31s. Cache lines are 64 bytes — traverse memory the way it lies.

## Voiceover cues

- `[0:04–0:10]` A 64x64 grid — two traversal orders
- `[0:10–0:16]` Row-major walks with the cache — 0.02s
- `[0:16–0:22]` Column-major thrashes it — 0.31s, 15x slower
- `[0:22–0:26]` Cache lines are 64 bytes — traverse memory the way it lies

## Full script

Welcome to Interstitium Labs. A 64x64 grid — two traversal orders Row-major walks with the cache — 0.02s Column-major thrashes it — 0.31s, 15x slower Cache lines are 64 bytes — traverse memory the way it lies This is a captioned preview; full voiceover ships with the next render pass.
