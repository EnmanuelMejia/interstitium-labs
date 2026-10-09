# The DCSync Heist — Narration Script

**Course:** AD-DEFENSE · Active Directory & Identity Defense  
**Video:** `bc-bbg-ad-dcsync.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

A replication-protocol diagram of the DCSync heist: a rogue workstation asks DC-01 for GetChangesAll and 1,247 NTLM hashes flow out.

## Voiceover cues

- `[0:04–0:10]` A rogue workstation asks the domain controller for replication
- `[0:10–0:16]` DsGetNCChanges: GetChangesAll pulls every password hash
- `[0:16–0:22]` 1,247 NTLM hashes exfiltrated — no exploit, just protocol
- `[0:22–0:26]` Audit 4662, isolate tier-0, alert on replication from non-DCs

## Full script

Welcome to Interstitium Labs. A rogue workstation asks the domain controller for replication DsGetNCChanges: GetChangesAll pulls every password hash 1,247 NTLM hashes exfiltrated — no exploit, just protocol Audit 4662, isolate tier-0, alert on replication from non-DCs This is a captioned preview; full voiceover ships with the next render pass.
