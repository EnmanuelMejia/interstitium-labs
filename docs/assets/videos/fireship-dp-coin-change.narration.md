# DP: Coin Change — Narration Script

**Course:** IL-13 · Software Engineering Interview Prep  
**Video:** `fireship-dp-coin-change.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

The dp table fills left to right for coins [1,5,10] and amount 12: dp[a] = 1 + min of its predecessors — answer 3.

## Voiceover cues

- `[0:04–0:10]` dp[a]: the fewest coins for amount a
- `[0:10–0:16]` Fill the table left to right, bottom-up
- `[0:16–0:22]` dp[a] = 1 + min(dp[a−1], dp[a−5], dp[a−10])
- `[0:22–0:26]` Answer: 3 coins — 10 + 1 + 1

## Full script

Welcome to Interstitium Labs. dp[a]: the fewest coins for amount a Fill the table left to right, bottom-up dp[a] = 1 + min(dp[a−1], dp[a−5], dp[a−10]) Answer: 3 coins — 10 + 1 + 1 This is a captioned preview; full voiceover ships with the next render pass.
