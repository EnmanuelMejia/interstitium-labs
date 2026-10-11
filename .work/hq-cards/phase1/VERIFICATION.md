# HQ Cards Phase 1 — Verification Report

**Generated:** 2026-10-09
**Pipeline:** media.generate_video (TikTok-style cinematic cards, 6/6 video budget used)
**Output dir:** `~/workspace/apex-audit/.work/hq-cards/phase1/`

## Spec compliance (all 6 PASS)

| # | Video | Size | FPS | Duration | Video | Audio | Levels |
|---|-------|------|-----|----------|-------|-------|--------|
| 1 | IL-29 ThreatLocker | 720×1280 | 24 | 10.0s | h264 | AAC | mean −17.9 dB, max −3.1 dB |
| 2 | IL-28 DevSecOps | 720×1280 | 24 | 10.0s | h264 | AAC | mean −19.2 dB, max −3.0 dB |
| 3 | IL-26 Data Analyst | 720×1280 | 24 | 10.0s | h264 | AAC | mean −18.0 dB, max −4.0 dB |
| 4 | DevOps SuperLab | 720×1280 | 24 | 10.0s | h264 | AAC | mean −16.4 dB, max −0.9 dB |
| 5 | RHEL AI & Systems Fabric | 720×1280 | 24 | 10.0s | h264 | AAC | mean −18.0 dB, max −0.3 dB |
| 6 | Bootcamp Catalog | 720×1280 | 24 | 10.0s | h264 | AAC | mean −17.3 dB, max −1.6 dB |

Audio confirmed non-silent on all (healthy levels, no flatlining). No files below spec — nothing flagged.

## Files

1. `media-generation-01-il29-threatlocker-0-65160092-f548-4290-b159-fab41a00f389.mp4` (7.25 MB)
2. `media-generation-02-il28-devsecops-0-115dd1bf-d69b-4bda-ba98-425af89a9f98.mp4` (3.67 MB)
3. `media-generation-03-il26-data-0-868dd216-1f04-4181-b3a2-ed3afef63a25.mp4` (4.90 MB)
4. `media-generation-04-devops-superlab-0-3b688f9c-11d3-4cd5-b898-5c7fb9d724d6.mp4` (4.02 MB)
5. `media-generation-05-rhel-fabric-0-a2853e31-2405-4e85-aaf7-08f79d550d89.mp4` (5.96 MB)
6. `media-generation-06-bootcamp-catalog-0-3af8a297-1ef8-41e0-881d-6a6c21c28213.mp4` (4.71 MB)

Each has a companion `.json` metadata file from the pipeline.

## Note

Prompts were passed verbatim from `~/workspace/apex-audit/.work/hq-cards/prompts/` with only an audio directive appended ("Include an ambient electronic soundtrack") per the task's "with audio" requirement. One prompt file was named `03-il26-data-analyst.txt` (not `03-il26-data.txt` as listed in the task) — used the existing file.
