# Pod Networking: Flat and Simple — Narration Script

**Course:** K8S · Associate  
**Video:** `bc-bbg-k8sa-net.mp4` (silent preview, 30s, 1280x720)  
**Status:** Preview — narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.

## Concept

Pod networking: every pod gets a real IP, all pods talk without NAT, and the CNI plugin wires the flat network. No NAT inside the cluster — that simplicity is the whole design.

## Voiceover cues

- `[0:04–0:10]` Every pod gets an IP — real, routable
- `[0:10–0:16]` No NAT inside — pods talk directly
- `[0:16–0:22]` CNI plugin: the wiring — Calico, Cilium, Flannel
- `[0:22–0:26]` Services add the stable front — kube-proxy routes

## Full script

Welcome to Interstitium Labs. Every pod gets an IP — real, routable No NAT inside — pods talk directly CNI plugin: the wiring — Calico, Cilium, Flannel Services add the stable front — kube-proxy routes This is a captioned preview; full voiceover ships with the next render pass.
