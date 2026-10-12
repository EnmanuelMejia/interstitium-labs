# ARC: Counting References — Narration Script

**Course:** IOS · Interview Prep  
**Video:** `bc-3b1b-ios-arc.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

ARC: the compiler inserts retain/release — strong keeps alive, weak goes nil, unowned assumes life. The compiler inserts the retains; you manage the graph.

## Voiceover cues

- `[0:04–0:10]` Strong: ownership — keeps it alive
- `[0:10–0:16]` Weak: no ownership — nils on death
- `[0:16–0:22]` Unowned: trust, but verify — crashes if wrong
- `[0:22–0:26]` Cycles: the leak — break with weak

## Full script

Welcome to Interstitium Labs. Strong: ownership — keeps it alive Weak: no ownership — nils on death Unowned: trust, but verify — crashes if wrong Cycles: the leak — break with weak This is a captioned preview; full voiceover ships with the next render pass.
