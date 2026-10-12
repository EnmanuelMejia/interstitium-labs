# Recursion in 100 Seconds — Narration Script

**Course:** IL-03 · Programming Language Forge  
**Video:** `fireship-recursion.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

fib(5) pushes frames onto the call stack, hits base cases, then unwinds with the answer: 5.

## Voiceover cues

- `[0:04–0:10]` fib(5) calls fib(4) and fib(3) — the stack grows
- `[0:10–0:16]` Base cases return: fib(1)=1, fib(0)=0 — the stack unwinds
- `[0:16–0:22]` Each frame resolves: 1, 1, 2, 3, 5
- `[0:22–0:26]` Recursion = base case + self-similar decomposition

## Full script

Welcome to Interstitium Labs. fib(5) calls fib(4) and fib(3) — the stack grows Base cases return: fib(1)=1, fib(0)=0 — the stack unwinds Each frame resolves: 1, 1, 2, 3, 5 Recursion = base case + self-similar decomposition This is a captioned preview; full voiceover ships with the next render pass.
