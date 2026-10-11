# Multi-AZ Failover: Surviving the Fire — Narration Script

**Course:** AWS SAA · Solutions Architect  
**Video:** `bc-bbg-aws-saa-failover.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

RDS Multi-AZ keeps a synchronous standby in another zone; when the primary fails, DNS flips and the standby promotes in about a minute. The exam loves the RTO number — know it cold.

## Voiceover cues

- `[0:04–0:10]` Primary serves writes in AZ-a — standby syncs in AZ-b
- `[0:10–0:16]` Failure detected — automated, no human paged
- `[0:16–0:22]` DNS flips to the standby — promotion in ~60 seconds
- `[0:22–0:26]` RTO ~1 minute, RPO ~zero — know the numbers cold

## Full script

Welcome to Interstitium Labs. Primary serves writes in AZ-a — standby syncs in AZ-b Failure detected — automated, no human paged DNS flips to the standby — promotion in ~60 seconds RTO ~1 minute, RPO ~zero — know the numbers cold This is a captioned preview; full voiceover ships with the next render pass.
