# Inference Serving: Tokens per Second — Narration Script

**Course:** LLM · LLM Engineering  
**Video:** `bc-primer-llm-serve.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Inference: prefill processes the prompt in parallel, decode generates one token at a time, batching and KV-cache squeeze the throughput. Prefill, then decode — the two phases have different physics.

## Voiceover cues

- `[0:04–0:10]` Prefill: the prompt, processed in parallel
- `[0:10–0:16]` Decode: one token at a time — autoregressive
- `[0:16–0:22]` KV-cache: remember the past, skip recompute
- `[0:22–0:26]` Batching: many users, one GPU — throughput

## Full script

Welcome to Interstitium Labs. Prefill: the prompt, processed in parallel Decode: one token at a time — autoregressive KV-cache: remember the past, skip recompute Batching: many users, one GPU — throughput This is a captioned preview; full voiceover ships with the next render pass.
