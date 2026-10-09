# The 99.8% That Was a Lie — Narration Script

**Course:** DATA SCIENCE · ML in Production  
**Video:** `bc-bbg-dsml-feature-leak.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Churn model at 99.8% accuracy — too good to be true: cancel_date only exists after churn. Drop it and the score falls to 71%, honestly.

## Voiceover cues

- `[0:04–0:10]` Five features — one of them knows the future
- `[0:10–0:16]` Accuracy 99.8% — too good to be true is too good
- `[0:16–0:22]` cancel_date exists only AFTER churn — drop it: 71%
- `[0:22–0:26]` If it's too good, it's leaking — audit every feature's timestamp

## Full script

Welcome to Interstitium Labs. Five features — one of them knows the future Accuracy 99.8% — too good to be true is too good cancel_date exists only AFTER churn — drop it: 71% If it's too good, it's leaking — audit every feature's timestamp This is a captioned preview; full voiceover ships with the next render pass.
