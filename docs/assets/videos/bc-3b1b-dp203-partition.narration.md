# Partitioning: Divide and Conquer — Narration Script

**Course:** DP-203 · Azure Data Engineer  
**Video:** `bc-3b1b-dp203-partition.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Partitioning: divide data by the column queries filter on — date, region — so scans skip whole partitions. Partition by the filter, not the fantasy; too many tiny files is its own disease.

## Voiceover cues

- `[0:04–0:10]` Partition column: the filter queries use
- `[0:10–0:16]` Partition pruning: skip whole directories
- `[0:16–0:22]` File size: ~1 GB sweet spot — not 10,000 tiny files
- `[0:22–0:26]` Small-file disease: compact relentlessly

## Full script

Welcome to Interstitium Labs. Partition column: the filter queries use Partition pruning: skip whole directories File size: ~1 GB sweet spot — not 10,000 tiny files Small-file disease: compact relentlessly This is a captioned preview; full voiceover ships with the next render pass.
