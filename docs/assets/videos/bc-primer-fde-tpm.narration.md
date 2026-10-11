# TPM Unlock: The Boot Handshake — Narration Script

**Course:** FDE · Disk Encryption  
**Video:** `bc-primer-fde-tpm.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

The TPM unlock flow: measure the boot, compare against sealed values, release the key only if the boot is clean. The chip vouches for the boot — tamper and the key stays locked.

## Voiceover cues

- `[0:04–0:10]` Measure: hash every boot stage
- `[0:10–0:16]` Compare: sealed values must match
- `[0:16–0:22]` Release: key only on a clean boot
- `[0:22–0:26]` Tamper and the key stays locked — by design

## Full script

Welcome to Interstitium Labs. Measure: hash every boot stage Compare: sealed values must match Release: key only on a clean boot Tamper and the key stays locked — by design This is a captioned preview; full voiceover ships with the next render pass.
