# Paxos Consensus — Narration Script

**Course:** IL-08 · Algorithms, Compilers, Distributed & Formal  
**Video:** `bbg-paxos.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

A proposer runs two phases against three acceptors: prepare/promise, then accept/accepted — quorum commits the value.

## Voiceover cues

- `[0:04–0:10]` Phase 1: the proposer sends PREPARE(n)
- `[0:10–0:16]` Acceptors reply PROMISE — no lower numbers accepted
- `[0:16–0:22]` Phase 2: ACCEPT(n, v) goes out
- `[0:22–0:26]` A majority accepts — the value is committed

## Full script

Welcome to Interstitium Labs. Phase 1: the proposer sends PREPARE(n) Acceptors reply PROMISE — no lower numbers accepted Phase 2: ACCEPT(n, v) goes out A majority accepts — the value is committed This is a captioned preview; full voiceover ships with the next render pass.
