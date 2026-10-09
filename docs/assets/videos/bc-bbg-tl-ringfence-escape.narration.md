# The Ringfenced Browser Tried to Escape — Narration Script

**Course:** TL-ENDPOINT · Zero Trust Endpoint Operations  
**Video:** `bc-bbg-tl-ringfence-escape.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

A ringfence diagram of the escape attempt: chrome.exe tries to spawn powershell.exe, the fence blocks it — default-deny with a guest list.

## Voiceover cues

- `[0:04–0:10]` Ringfence: chrome.exe — allowed apps only
- `[0:10–0:16]` The browser tries to spawn powershell.exe
- `[0:16–0:22]` BLOCKED: untrusted process, no exception
- `[0:22–0:26]` Allowlisting is default-deny with a guest list

## Full script

Welcome to Interstitium Labs. Ringfence: chrome.exe — allowed apps only The browser tries to spawn powershell.exe BLOCKED: untrusted process, no exception Allowlisting is default-deny with a guest list This is a captioned preview; full voiceover ships with the next render pass.
