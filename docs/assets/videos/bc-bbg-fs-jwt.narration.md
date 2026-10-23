# The JWT Handshake — Narration Script

**Course:** FULLSTACK · Browser to Database  
**Video:** `bc-bbg-fs-jwt.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

POST /login returns a signed token; every request carries it in the header — the server verifies, never stores. 200 OK, or 401 when it expires.

## Voiceover cues

- `[0:04–0:10]` POST /login — credentials over the wire
- `[0:10–0:16]` The server signs a token — valid 24 hours
- `[0:16–0:22]` Every request carries it — verify, never store
- `[0:22–0:26]` 200 OK with a live token · 401 when it expires

## Full script

Welcome to Interstitium Labs. POST /login — credentials over the wire The server signs a token — valid 24 hours Every request carries it — verify, never store 200 OK with a live token · 401 when it expires This is a captioned preview; full voiceover ships with the next render pass.
