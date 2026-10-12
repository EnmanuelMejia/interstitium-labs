# Move: Steal, Don't Copy — Narration Script

**Course:** C++ · Systems & Performance  
**Video:** `bc-bbg-cpp-move.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Move semantics: std::move transfers the pointer instead of copying the bytes — copy is O(n), move is O(1). Steal the guts, leave the husk.

## Voiceover cues

- `[0:04–0:10]` A huge string — copy would duplicate every byte
- `[0:10–0:16]` std::move: transfer the pointer, not the bytes
- `[0:16–0:22]` Copy: O(n) — move: O(1) pointer swap
- `[0:22–0:26]` Move semantics: steal the guts, leave the husk

## Full script

Welcome to Interstitium Labs. A huge string — copy would duplicate every byte std::move: transfer the pointer, not the bytes Copy: O(n) — move: O(1) pointer swap Move semantics: steal the guts, leave the husk This is a captioned preview; full voiceover ships with the next render pass.
