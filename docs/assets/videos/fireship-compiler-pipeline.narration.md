# How a Compiler Works — Narration Script

**Course:** IL-08 · Algorithms, Compilers, Distributed & Formal  
**Video:** `fireship-compiler-pipeline.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

main.c streams through lexing, parsing, IR, and codegen: tokens, a syntax tree, then two machine instructions.

## Voiceover cues

- `[0:04–0:10]` Lexing: characters become tokens — int, main, (, ) …
- `[0:10–0:16]` Parsing: tokens become a syntax tree
- `[0:16–0:22]` IR: one intermediate language for every target
- `[0:22–0:26]` Codegen: mov eax, 42 — the machine runs numbers

## Full script

Welcome to Interstitium Labs. Lexing: characters become tokens — int, main, (, ) … Parsing: tokens become a syntax tree IR: one intermediate language for every target Codegen: mov eax, 42 — the machine runs numbers This is a captioned preview; full voiceover ships with the next render pass.
