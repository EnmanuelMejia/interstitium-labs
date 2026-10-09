# Boot Targets: The systemd Flow — Narration Script

**Course:** RHCSA · Linux Admin  
**Video:** `bc-primer-rhcsa-systemd.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

systemd boot: targets pull in units, dependencies order them, and the default target decides where you land — multi-user or graphical. Dependencies, not scripts — the boot is a graph.

## Voiceover cues

- `[0:04–0:10]` Units: services, sockets, mounts — everything
- `[0:10–0:16]` Dependencies order the graph — Wants and Requires
- `[0:16–0:22]` Targets: multi-user vs graphical — the destination
- `[0:22–0:26]` systemctl: the one command to rule the boot

## Full script

Welcome to Interstitium Labs. Units: services, sockets, mounts — everything Dependencies order the graph — Wants and Requires Targets: multi-user vs graphical — the destination systemctl: the one command to rule the boot This is a captioned preview; full voiceover ships with the next render pass.
