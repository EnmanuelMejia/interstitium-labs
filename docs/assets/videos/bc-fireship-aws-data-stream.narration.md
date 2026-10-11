# Streaming ETL in 100 Seconds — Narration Script

**Course:** AWS DATA · Data Engineer  
**Video:** `bc-fireship-aws-data-stream.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

A streaming ETL sketch: read the Kinesis shard, window events by minute, aggregate the counts, sink to S3. Four verbs, infinite data — the window is what makes streaming sane.

## Voiceover cues

- `[0:04–0:10]` Read the shard — the stream never ends
- `[0:10–0:16]` Window by event time — one-minute buckets
- `[0:16–0:22]` Aggregate inside each window — counts, sums
- `[0:22–0:26]` Sink to S3 — the window makes streaming sane

## Full script

Welcome to Interstitium Labs. Read the shard — the stream never ends Window by event time — one-minute buckets Aggregate inside each window — counts, sums Sink to S3 — the window makes streaming sane This is a captioned preview; full voiceover ships with the next render pass.
