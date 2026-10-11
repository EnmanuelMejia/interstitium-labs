# IAM Policy Evaluation: The Gauntlet — Narration Script

**Course:** AWS SCS · Security Specialty  
**Video:** `bc-bbg-aws-scs-iam.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

IAM evaluation order: explicit deny wins over everything, then explicit allow, then default deny. SCPs, identity policies, and resource policies all vote — one deny anywhere kills the request.

## Voiceover cues

- `[0:04–0:10]` Explicit deny — wins over everything, always
- `[0:10–0:16]` Explicit allow — needed from identity OR resource
- `[0:16–0:22]` Default deny — silence means no
- `[0:22–0:26]` One deny anywhere — SCP, identity, or resource — kills it

## Full script

Welcome to Interstitium Labs. Explicit deny — wins over everything, always Explicit allow — needed from identity OR resource Default deny — silence means no One deny anywhere — SCP, identity, or resource — kills it This is a captioned preview; full voiceover ships with the next render pass.
