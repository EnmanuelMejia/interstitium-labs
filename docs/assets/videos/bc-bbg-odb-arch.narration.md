# Oracle Architecture: SGA and Friends — Narration Script

**Course:** ORACLE DB · Database Admin  
**Video:** `bc-bbg-odb-arch.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Oracle architecture: the SGA caches data and SQL, the PGA sorts per session, background processes do the writing. Memory structures plus processes — know which does what.

## Voiceover cues

- `[0:04–0:10]` SGA: shared memory — buffer cache, shared pool
- `[0:10–0:16]` PGA: per-session — sorts and hashes
- `[0:16–0:22]` DBWn writes dirty blocks — LGWR writes redo
- `[0:22–0:26]` Instance = SGA + processes — database = files

## Full script

Welcome to Interstitium Labs. SGA: shared memory — buffer cache, shared pool PGA: per-session — sorts and hashes DBWn writes dirty blocks — LGWR writes redo Instance = SGA + processes — database = files This is a captioned preview; full voiceover ships with the next render pass.
