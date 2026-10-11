# Envelope Encryption: Keys Protect Keys — Narration Script

**Course:** AWS SCS · Security Specialty  
**Video:** `bc-primer-aws-scs-kms.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Envelope encryption: KMS guards the master key, a unique data key encrypts each object, and the encrypted data key rides alongside. Decrypt the envelope first, then the data — the master key never leaves KMS.

## Voiceover cues

- `[0:04–0:10]` KMS holds the master key — it never leaves
- `[0:10–0:16]` A unique data key encrypts each object
- `[0:16–0:22]` The encrypted data key rides with the object
- `[0:22–0:26]` Decrypt envelope first — then the data

## Full script

Welcome to Interstitium Labs. KMS holds the master key — it never leaves A unique data key encrypts each object The encrypted data key rides with the object Decrypt envelope first — then the data This is a captioned preview; full voiceover ships with the next render pass.
