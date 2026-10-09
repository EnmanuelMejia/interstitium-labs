# Three-Tier Architecture — Narration Script

**Course:** AWS SAA · Solutions Architect  
**Video:** `bc-bbg-aws-saa-arch.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

The classic three-tier web architecture: Route 53 routes, the ALB balances, EC2 in an Auto Scaling group computes, RDS Multi-AZ persists. Stateless in front, stateful behind — scale the tiers independently.

## Voiceover cues

- `[0:04–0:10]` Route 53 routes — DNS with health checks
- `[0:10–0:16]` ALB balances — traffic spreads, instances stay dumb
- `[0:16–0:22]` Auto Scaling group computes — stateless, replaceable
- `[0:22–0:26]` RDS Multi-AZ persists — the stateful heart

## Full script

Welcome to Interstitium Labs. Route 53 routes — DNS with health checks ALB balances — traffic spreads, instances stay dumb Auto Scaling group computes — stateless, replaceable RDS Multi-AZ persists — the stateful heart This is a captioned preview; full voiceover ships with the next render pass.
