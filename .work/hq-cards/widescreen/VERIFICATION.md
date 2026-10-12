# Widescreen Phase 2 — Verification Summary

**Generated:** 2026-10-09 via `media.generate_video` pipeline (4-video budget, all used)
**Output dir:** `~/workspace/apex-audit/.work/hq-cards/widescreen/`
**Prompts:** adapted from `~/workspace/apex-audit/.work/hq-cards/prompts/{07,08,09,10}-*.txt`, re-composed for 16:9 horizontal layout, "Include an ambient electronic soundtrack." appended

| # | Card | File | Resolution | FPS | Duration | Codec | Audio | Levels (mean/max) |
|---|------|------|-----------|-----|----------|-------|-------|--------------------|
| 7 | TL Interview Prep (Mr. Robot green) | `media-generation-ws-07-tl-interview-0-7538cb8e-9430-4cc9-8d7c-2af6e531a26e.mp4` | 1280×720 | 24 | 10.0s | h264 | AAC 24kHz | −18.4 / −0.7 dB ✓ |
| 8 | TL Assessment Prep (Mr. Robot green) | `media-generation-ws-08-tl-assessment-0-ecb565fa-586c-4cc6-8947-aa767c50cc65.mp4` | 1280×720 | 24 | 10.0s | h264 | AAC 24kHz | −20.3 / −5.9 dB ✓ |
| 9 | AI Vision Deck (purple/cyan) | `media-generation-ws-09-ai-vision-deck-0-12a542ff-5ec7-40b6-8776-f58d860fca10.mp4` | 1280×720 | 24 | 10.0s | h264 | AAC 24kHz | −18.0 / −0.5 dB ✓ |
| 10 | LPS Enrollment (blue/cyan) | `media-generation-ws-10-lps-enrollment-0-71b7a156-5afe-4b30-85d6-4069676623eb.mp4` | 1280×720 | 24 | 10.0s | h264 | AAC 24kHz | −22.6 / −9.0 dB ✓ |

**Spec check:** 1280×720 ✓ | 24fps ✓ | ~10s ✓ | h264 ✓ | AAC audio ✓
**Audio:** non-silent on all four (healthy levels, no flatlines, no clipping) ✓
**No flags — nothing below spec.**

**Note:** The pipeline honored native 16:9 widescreen composition on all four (no cropping/stretching). Files are ready for parent-side deployment (portfolio + flagship + cards library).
