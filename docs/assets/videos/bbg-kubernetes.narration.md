# Kubernetes Architecture — Narration Script

**Course:** IL-05 · Cloud, DevSecOps, Platform & SRE  
**Video:** `bbg-kubernetes.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Control plane components schedule pods onto worker nodes; a rolling update swaps v1 pods for v2 with zero downtime.

## Voiceover cues

- `[0:04–0:10]` The control plane: API server, scheduler, etcd
- `[0:10–0:16]` Worker nodes run kubelets and pods
- `[0:16–0:22]` The scheduler places pods; the kubelet keeps them alive
- `[0:22–0:26]` Desired state, continuously reconciled

## Full script

Welcome to Interstitium Labs. The control plane: API server, scheduler, etcd Worker nodes run kubelets and pods The scheduler places pods; the kubelet keeps them alive Desired state, continuously reconciled This is a captioned preview; full voiceover ships with the next render pass.
