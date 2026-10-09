# System Design: URL Shortener — Narration Script

**Course:** IL-13 · Software Engineering Interview Prep  
**Video:** `bbg-url-shortener.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

A request flows client → API → cache → DB: base62 hashing mints short codes, the hot 20% lives in cache.

## Voiceover cues

- `[0:04–0:10]` POST a long URL — get back a short code
- `[0:10–0:16]` Base62 hash: the code space is enormous
- `[0:16–0:22]` Cache the hot 20% — reads dominate writes
- `[0:22–0:26]` Scale: 1B URLs fits in ~100GB

## Full script

Welcome to Interstitium Labs. POST a long URL — get back a short code Base62 hash: the code space is enormous Cache the hot 20% — reads dominate writes Scale: 1B URLs fits in ~100GB This is a captioned preview; full voiceover ships with the next render pass.
