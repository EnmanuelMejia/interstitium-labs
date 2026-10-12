# The Event Loop: One Thread, Many Waits — Narration Script

**Course:** PYTHON SYS · Systems Programming  
**Video:** `bc-primer-pys-asyncio.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

asyncio: one thread, coroutines that yield on I/O, the loop resuming whoever is ready. Never block the loop — await the waits, thread the CPU.

## Voiceover cues

- `[0:04–0:10]` Coroutines: functions that pause politely
- `[0:10–0:16]` await: yield on I/O — the loop does errands
- `[0:16–0:22]` The loop resumes whoever is ready
- `[0:22–0:26]` CPU work goes to threads — never block

## Full script

Welcome to Interstitium Labs. Coroutines: functions that pause politely await: yield on I/O — the loop does errands The loop resumes whoever is ready CPU work goes to threads — never block This is a captioned preview; full voiceover ships with the next render pass.
