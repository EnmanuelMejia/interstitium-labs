# systemd — Narration Script

**Course:** IL-28 · DevSecOps & Cloud Infrastructure — Production Mastery  
**Video:** `bbg-systemd-units.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

systemd: targets boot in order — sysinit, basic, multi-user — then your app.service starts with Restart=always. Dependencies ordered, failures restarted.

## Voiceover cues

- `[0:04–0:10]` Targets: the boot order, declared
- `[0:10–0:16]` Units activate — dependencies resolved
- `[0:16–0:22]` app.service: ExecStart, Restart=always
- `[0:22–0:26]` Init done right: ordered, supervised, restarted

## Full script

Welcome to Interstitium Labs. Targets: the boot order, declared Units activate — dependencies resolved app.service: ExecStart, Restart=always Init done right: ordered, supervised, restarted This is a captioned preview; full voiceover ships with the next render pass.
