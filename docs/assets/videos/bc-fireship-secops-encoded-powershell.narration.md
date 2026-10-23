# Encoded PowerShell at 2 AM — Narration Script

**Course:** SECOPS · Blue Team Operations  
**Video:** `bc-fireship-secops-encoded-powershell.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

A SIEM-alert walkthrough of encoded PowerShell: the base64 blob decodes to a downloader — encoded commands are guilty until proven innocent.

## Voiceover cues

- `[0:04–0:10]` Event 4104: powershell -enc SQBFAFgA…
- `[0:10–0:16]` Decoded: a WebClient downloading from an evil host
- `[0:16–0:22]` LOLBins in play: rundll32, mshta, certutil
- `[0:22–0:26]` Block the pattern · hunt the fleet

## Full script

Welcome to Interstitium Labs. Event 4104: powershell -enc SQBFAFgA… Decoded: a WebClient downloading from an evil host LOLBins in play: rundll32, mshta, certutil Block the pattern · hunt the fleet This is a captioned preview; full voiceover ships with the next render pass.
