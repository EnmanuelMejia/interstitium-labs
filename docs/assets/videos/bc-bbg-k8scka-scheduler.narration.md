# Where Does the Pod Land? — Narration Script

**Course:** CKA · Advanced Kubernetes Administration  
**Video:** `bc-bbg-k8scka-scheduler.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

The kube-scheduler in action: a pod requests 2 CPU, full nodes are filtered out, the least-loaded node wins — filter, then score.

## Voiceover cues

- `[0:04–0:10]` Three nodes · one is full · the pod needs 2 CPU
- `[0:10–0:16]` Filter: the full node is out
- `[0:16–0:22]` Score: the least-loaded node wins — scheduled
- `[0:22–0:26]` Filter the infeasible, score the rest — the scheduler is an optimizer

## Full script

Welcome to Interstitium Labs. Three nodes · one is full · the pod needs 2 CPU Filter: the full node is out Score: the least-loaded node wins — scheduled Filter the infeasible, score the rest — the scheduler is an optimizer This is a captioned preview; full voiceover ships with the next render pass.
