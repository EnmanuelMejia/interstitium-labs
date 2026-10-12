# How Many Replicas Survive? — Narration Script

**Course:** CKA · Advanced Kubernetes Administration  
**Video:** `bc-3b1b-k8scka-quorum.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

The math of quorum: a node dies — 3 and 5 replicas hold their majority, 1 and 2 gamble. Odd numbers win elections.

## Voiceover cues

- `[0:04–0:10]` One, two, three, five replicas — all healthy
- `[0:10–0:16]` One node dies — who still has quorum?
- `[0:16–0:22]` Three and five: majority held · one and two: lost
- `[0:22–0:26]` Odd numbers win elections — size for the failure, not the happy path

## Full script

Welcome to Interstitium Labs. One, two, three, five replicas — all healthy One node dies — who still has quorum? Three and five: majority held · one and two: lost Odd numbers win elections — size for the failure, not the happy path This is a captioned preview; full voiceover ships with the next render pass.
