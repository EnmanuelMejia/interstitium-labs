# SQL Window Functions — Narration Script

**Course:** IL-15 · Data Engineering & Analytics Interview Prep  
**Video:** `fireship-window-functions.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

RANK() OVER (PARTITION BY dept ORDER BY salary DESC): every department gets its own leaderboard without collapsing a single row.

## Voiceover cues

- `[0:04–0:10]` PARTITION BY splits the table into independent groups
- `[0:10–0:16]` ORDER BY ranks inside each group
- `[0:16–0:22]` RANK() assigns the leaderboard position
- `[0:22–0:26]` Aggregation — without losing a single row

## Full script

Welcome to Interstitium Labs. PARTITION BY splits the table into independent groups ORDER BY ranks inside each group RANK() assigns the leaderboard position Aggregation — without losing a single row This is a captioned preview; full voiceover ships with the next render pass.
