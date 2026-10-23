# rundll32: True Positive or Admin? — Narration Script

**Course:** SECOPS · Blue Team Operations  
**Video:** `bc-bbg-secops-sigma-rule.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

A detection pipeline diagram for the rundll32 Sigma hit: event, rule match, enrichment, verdict — a detection without context is a coin flip.

## Voiceover cues

- `[0:04–0:10]` Event: rundll32.exe with a javascript payload
- `[0:10–0:16]` Sigma rule fires: signed-binary proxy execution
- `[0:16–0:22]` Enrichment: parent explorer, user helpdesk-04 — benign admin
- `[0:22–0:26]` Tune, don't block — enrich before you verdict

## Full script

Welcome to Interstitium Labs. Event: rundll32.exe with a javascript payload Sigma rule fires: signed-binary proxy execution Enrichment: parent explorer, user helpdesk-04 — benign admin Tune, don't block — enrich before you verdict This is a captioned preview; full voiceover ships with the next render pass.
