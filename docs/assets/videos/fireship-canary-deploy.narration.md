# Canary Deployments — Narration Script

**Course:** IL-14 · SRE, DevOps, Cloud & Security Interview Prep  
**Video:** `fireship-canary-deploy.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Traffic shifts 100/0 → 95/5 → 75/25 → 50/50 → 0/100 while metric gates watch: green promotes, red rolls back automatically.

## Voiceover cues

- `[0:04–0:10]` Route 5% of traffic to the canary
- `[0:10–0:16]` Gates watch: errors, latency, 5xx rate
- `[0:16–0:22]` Green gates → shift more traffic
- `[0:22–0:26]` Red gates → automatic rollback

## Full script

Welcome to Interstitium Labs. Route 5% of traffic to the canary Gates watch: errors, latency, 5xx rate Green gates → shift more traffic Red gates → automatic rollback This is a captioned preview; full voiceover ships with the next render pass.
