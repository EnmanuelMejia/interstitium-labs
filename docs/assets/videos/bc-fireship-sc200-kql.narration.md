# KQL in 100 Seconds — Narration Script

**Course:** SC-200 · Security Operations  
**Video:** `bc-fireship-sc200-kql.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

KQL: take the table, filter the time window, summarize by the field that matters, sort the guilty to the top. Pipe everything, summarize always — the query is the investigation.

## Voiceover cues

- `[0:04–0:10]` The table first — SigninLogs, SecurityEvent
- `[0:10–0:16]` where TimeGenerated > ago(1d) — bound the blast
- `[0:16–0:22]` summarize count() by the suspicious field
- `[0:22–0:26]` Sort descending — the guilty float up

## Full script

Welcome to Interstitium Labs. The table first — SigninLogs, SecurityEvent where TimeGenerated > ago(1d) — bound the blast summarize count() by the suspicious field Sort descending — the guilty float up This is a captioned preview; full voiceover ships with the next render pass.
