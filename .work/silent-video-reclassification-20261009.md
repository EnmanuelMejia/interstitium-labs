# Silent Video Reclassification — 2026-10-09

## Audit result: 43 silent videos out of 641 total

### Category A: Ambient background loops (14 videos) — CORRECTLY SILENT BY DESIGN
These are muted autoplay background videos. Silence is intentional and correct.
No action needed. Reclassified as "ambient".

- assets/chrome/hero-cinematic-loop.mp4 (homepage hero background)
- assets/noah/noah-neural-loop.mp4 (Noah page cinematic loop, 1920×540 intentional aspect)
- assets/topics/ai-ml-hero.mp4
- assets/topics/blockchain-hero.mp4
- assets/topics/cloud-devops-hero.mp4
- assets/topics/cybersecurity-hero.mp4
- assets/topics/data-eng-hero.mp4
- assets/topics/databases-hero.mp4
- assets/topics/linux-systems-hero.mp4
- assets/topics/math-hero.mp4
- assets/topics/networking-hero.mp4
- assets/topics/programming-hero.mp4
- assets/topics/system-design-hero.mp4
- assets/topics/web-dev-hero.mp4

### Category B: Orphaned assets (29 videos) — NOT SERVED
- assets/cinematic/courses-anim/IL-01.mp4 through IL-29.mp4
- Not referenced in any HTML, JS, or course JSON sitewide (verified via full-text search)
- Upscaled to 1920×1080 as part of the batch (for future use), but no audio work needed
  since they are not currently served to users

### Conclusion
Zero silent videos are currently served to users in a context where audio is expected.
All 598 videos with audio tracks verified intact after upscale (audio streams copied, not re-encoded).
The "no downscaling, only upscaling" constraint was honored throughout:
- Video: 1280×720 → 1920×1080 via lanczos (upscale only)
- Audio: stream copy (no re-encode, no quality loss)
- Codec: libx264, CRF 21 (high quality)
