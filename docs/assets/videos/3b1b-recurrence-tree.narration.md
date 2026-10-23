# The Recurrence Tree — Narration Script

**Course:** IL-13 · Software Engineering Interview Prep  
**Video:** `3b1b-recurrence-tree.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

T(n) = 2T(n/2) + n unfolds into a tree: every level does exactly n work, and there are log n levels.

## Voiceover cues

- `[0:04–0:10]` T(n) = 2T(n/2) + n — divide, conquer, combine
- `[0:10–0:16]` Each level splits: 1, 2, 4, 8 subproblems
- `[0:16–0:22]` But every level does exactly n total work
- `[0:22–0:26]` log n levels × n work = O(n log n)

## Full script

Welcome to Interstitium Labs. T(n) = 2T(n/2) + n — divide, conquer, combine Each level splits: 1, 2, 4, 8 subproblems But every level does exactly n total work log n levels × n work = O(n log n) This is a captioned preview; full voiceover ships with the next render pass.
