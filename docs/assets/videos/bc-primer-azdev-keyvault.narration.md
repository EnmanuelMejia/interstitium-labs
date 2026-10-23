# Key Vault: Secrets Never in Code — Narration Script

**Course:** AZURE DEV · Azure Developer  
**Video:** `bc-primer-azdev-keyvault.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

The Key Vault flow: the app authenticates with its managed identity — no stored credential — requests the secret, gets the value, caches briefly. Secrets never in code, never in config, rotation without redeploys.

## Voiceover cues

- `[0:04–0:10]` Managed identity: the app IS the credential
- `[0:10–0:16]` No passwords stored anywhere — nothing to leak
- `[0:16–0:22]` Request the secret — audit-logged every time
- `[0:22–0:26]` Rotate in the vault — no redeploy needed

## Full script

Welcome to Interstitium Labs. Managed identity: the app IS the credential No passwords stored anywhere — nothing to leak Request the secret — audit-logged every time Rotate in the vault — no redeploy needed This is a captioned preview; full voiceover ships with the next render pass.
