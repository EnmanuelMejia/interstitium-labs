# HQ Card Re-render — Original Pipeline

**User order:** 2026-10-09 ~02:50 EDT — "Yes do this recursively site wide across all my websites please never downscale or implement subpar features or modules only improvements or upscaled Implementations"

**Coordinator task:** Re-render all 10 project cards through the ORIGINAL media generation pipeline (`media.generate_video`) at full quality.

## Pipeline Verification (2026-10-09)

**Original pipeline identified:** `media.generate_video` (Muse structured media pipeline)

**Original specs (verified via ffprobe):**
| File | Resolution | FPS | Duration | Video codec | Bitrate | Audio |
|---|---|---|---|---|---|---|
| `il-29-launch/il29-tiktok-launch.mp4` | 720×1280 (9:16) | 24 | 10.0s | h264 (yuv420p) | 4.88 Mbps | AAC 24kHz |
| `il-28-launch/media-generation-il28-tiktok-launch-*.mp4` | 720×1280 (9:16) | 24 | 10.0s | h264 | 3.73 Mbps | AAC 24kHz |

**Quality gap confirmed:** Current 50 programmatic cards are silent (no audio track) and PIL-rendered. Originals have AAC audio beds and AI-generated cinematic motion. User correctly identified the gap.

## Current Assets to Replace

Location: `~/workspace/apex-audit/docs/assets/cards/` (14MB, 50 files)

| Project | Current 9:16 | Current 16:9 | Current poster | Current LinkedIn |
|---|---|---|---|---|
| IL-26 | `il-26_9x16.mp4` | `il-26_16x9.mp4` | `il-26_9x16-poster.png` | `il-26_linkedin_1200x627.png` |
| IL-28 | `il-28_9x16.mp4` | `il-28_16x9.mp4` | `il-28_9x16-poster.png` | `il-28_linkedin_1200x627.png` |
| IL-29 | `il-29_9x16.mp4` | `il-29_16x9.mp4` | `il-29_9x16-poster.png` | `il-29_linkedin_1200x627.png` |
| DevOps SuperLab | `devops-superlab_9x16.mp4` | `devops-superlab_16x9.mp4` | `devops-superlab_9x16-poster.png` | `devops-superlab_linkedin_1200x627.png` |
| RHEL Fabric | `rhel-fabric_9x16.mp4` | `rhel-fabric_16x9.mp4` | `rhel-fabric_9x16-poster.png` | `rhel-fabric_linkedin_1200x627.png` |
| Bootcamp Catalog | `bootcamp-catalog_9x16.mp4` | `bootcamp-catalog_16x9.mp4` | `bootcamp-catalog_9x16-poster.png` | `bootcamp-catalog_linkedin_1200x627.png` |
| TL Interview | `tl-interview_9x16.mp4` | `tl-interview_16x9.mp4` | `tl-interview_9x16-poster.png` | `tl-interview_linkedin_1200x627.png` |
| TL Assessment | `tl-assessment_9x16.mp4` | `tl-assessment_16x9.mp4` | `tl-assessment_9x16-poster.png` | `tl-assessment_linkedin_1200x627.png` |
| AI Vision Deck | `ai-vision_9x16.mp4` | `ai-vision_16x9.mp4` | `ai-vision_9x16-poster.png` | `ai-vision_linkedin_1200x627.png` |
| LPS Enrollment | `lps-enrollment_9x16.mp4` | `lps-enrollment_16x9.mp4` | `lps-enrollment_9x16-poster.png` | `lps-enrollment_linkedin_1200x627.png` |

## Generation Prompts

Ready in `~/workspace/apex-audit/.work/hq-cards/prompts/`:
1. `01-il29-threatlocker.txt` — hex badge, ALLOWLIST/DENYLIST ring, cyan/orange
2. `02-il28-devsecops.txt` — circuit traces, 50 modules badge
3. `03-il26-data-analyst.txt` — charts/graphs, ocean-deep data theme
4. `04-devops-superlab.txt` — infrastructure stack building
5. `05-rhel-fabric.txt` — bare-metal server, red/cyan
6. `06-bootcamp-catalog.txt` — 68-bootcamp mosaic, 2,444 scenarios
7. `07-tl-interview.txt` — Mr. Robot green, shield badge
8. `08-tl-assessment.txt` — Mr. Robot green, checklist badge
9. `09-ai-vision-deck.txt` — neural network, purple/cyan, Ex Machina
10. `10-lps-enrollment.txt` — bar charts, gold/cyan, Alexandria theme

## Phased Execution Plan

**Constraint:** `media.generate_video` allows max 6 videos per user message. 10 videos needed (9:16). 16:9 has no aspect-ratio parameter in the pipeline — output format is pipeline-determined (originals are 9:16).

**Phase 1** (6 videos, 9:16): IL-29, IL-28, IL-26, DevOps SuperLab, RHEL Fabric, Bootcamp Catalog
**Phase 2** (4 videos, 9:16): TL Interview, TL Assessment, AI Vision Deck, LPS Enrollment
**Phase 3** (posters + LinkedIn): Extract via ffmpeg from generated videos — poster frame at t=3s (1280×720 for 16:9 display), LinkedIn 1200×627 crop from center. No additional generation needed.
**Phase 4** (16:9 web versions): TBD — pipeline has no aspect-ratio control. Options: (a) verify if pipeline supports widescreen via prompt, (b) keep programmatic 16:9 as fallback, (c) generate 16:9 natively if pipeline allows.

**Post-generation steps per video:**
1. Verify: 720×1280, ~24fps, ~10s, h264, has audio track
2. Extract poster: `ffmpeg -ss 3 -i <video> -vframes 1 -q:v 2 <poster>.png`
3. LinkedIn: `ffmpeg -i <video> -ss 3 -vframes 1 -vf "scale=1200:627:force_original_aspect_ratio=increase,crop=1200:627" <linkedin>.png`
4. Replace files in `docs/assets/cards/` (keep same filenames)
5. Deploy flagship + portfolio workers, verify 200s

## Sites to Update (recursive sitewide)

- [ ] Portfolio `enmanueldmejia.com` (worker: `enmanuel-mejia`)
- [ ] Flagship `interstitiumlabs.dev` (worker: `solitary-sound-015a`)
- [ ] Cards library `interstitiumlabs.dev/cards/`
- [ ] `learn.interstitiumlabs.dev` (inherits flagship assets)
- [ ] `app.interstitiumlabs.dev` (inherits flagship assets)

## Quality Standard (user directive)

"Never downscale or implement subpar features or modules — only improvements or upscaled implementations."

- Every re-render must be ≥ original quality (720×1280, 24fps, 10s, h264, AAC audio)
- If pipeline output is below spec, flag it — do not ship
- No compression artifacts, no reduced resolution, no simplified effects

## Status

- [x] Pipeline located and verified
- [x] Original specs confirmed via ffprobe
- [x] 10 generation prompts written
- [x] Output dirs created
- [x] Tracker written
- [ ] **BLOCKED: Awaiting explicit video budget from parent** (see below)

## Blocker: Video Budget Required

Per `media.generate_video` schema: "When your task came from another agent, check that the task says how many videos you may make. If it does not, make none and say so in your result."

The coordinator task does not contain an explicit numeric video budget statement. **Zero videos have been generated.** All preparatory work is complete and ready.

**To proceed, parent must reply with an explicit budget**, e.g.: "You may make 6 videos" (Phase 1). Each subsequent phase needs its own budget within its own user message (6-video cap per message).

## DEPLOYMENT COMPLETE — 2026-10-09 ~06:57 UTC

All 10 HQ pipeline-rendered videos deployed and verified live.

**Assets** (~/workspace/apex-audit/docs/assets/cards/hq/):
- 10× `hq-{slug}_9x16.mp4` — 720×1280, h264, 24fps, 10s, AAC audio (all spec-verified)
- 10× `hq-{slug}_poster.png` — first-frame posters
- 10× `hq-{slug}_linkedin.png` — 1200×627 LinkedIn crops

**Wiring:**
- Portfolio (enmanueldmejia.com): 50 refs swapped from programmatic 16:9 to HQ 9:16 (verified 40 hq refs live on homepage)
- Cards library (interstitiumlabs.dev/cards/): PROJECTS entries now carry `hq` slug field; video/poster/download links point to `/assets/cards/hq/` (200 verified)

**Deploys:**
- Flagship `solitary-sound-015a`: etag=de43e33e40e4, 2026-10-09T06:56:57Z
- Portfolio `enmanuel-mejia`: 2026-10-09T06:57:07Z

**Verification:** 10/10 HQ MP4s return HTTP 200 at https://interstitiumlabs.dev/assets/cards/hq/

**Note:** 16:9 programmatic versions retained as fallback per plan (pipeline has no 16:9 param; no cropping performed per no-downscale directive). TTS still down — videos carry pipeline ambient audio beds; voiceover narration pending TTS restore.

## Voiceover Update (2026-10-09 ~03:10 EDT)
TTS service restored. All 10 HQ cards now have voiceover narration mixed with ambient audio (voice prominent, ambient at 0.3 weight).
- Scripts: 10-second narrations per card (project name + tagline + "Interstitium Labs")
- Audio: TTS-generated MP3s, muxed via ffmpeg amix
- Deployed: flagship solitary-sound-015a + portfolio enmanuel-mejia
- Verified: 200s on sampled HQ MP4s
- Standing "Preview — narration coming" watermark no longer applies to these 10 cards.

## Widescreen 16:9 Deployment (2026-10-09 ~03:10 EDT)

**Source:** 10 widescreen MP4s from `~/workspace/apex-audit/.work/hq-cards/widescreen/`:
- Projects 1–6: max-fidelity batch (`media-generation-hq-widescreen-*`, per user's "force highest fidelity" directive; batch-1 standard files retained in work dir as fallback)
- Projects 7–10: `media-generation-ws-07` through `ws-10` (TL Interview, TL Assessment, AI Vision, LPS)

**Assets:** copied to `docs/assets/cards/hq/` as `hq-{slug}_16x9.mp4` (slugs: il29, il28, il26, superlab, rhel, catalog, tl-interview, tl-assessment, ai-vision, lps). All spec-verified: 1280×720, h264, 24fps, 10.0s.

**Voiceover:** muxed the same 10 TTS narration MP3s (from /tmp/vo-*.mp3) into all 16:9 versions via ffmpeg amix (voice prominent, ambient 0.3 weight, video stream copied). All 10 confirmed AAC audio post-mux.

**Posters:** extracted `hq-{slug}_16x9_poster.png` (frame at t=1s) for all 10.

**Portfolio** (`~/workspace/portfolio-site/index.html`): all video refs swapped `_9x16.mp4` → `_16x9.mp4` (30 refs across project-card embeds + cinematic section); poster refs swapped to `_16x9_poster.png` (20 refs). LinkedIn profile links untouched. Backup: `index.html.bak-widescreen`.

**Cards library** (`docs/cards/index.html`): preview video + poster now 16:9 HQ; downloads relabeled "16:9 Widescreen (HQ)" (points to hq/ 16:9), "9:16 TikTok (HQ)", "LinkedIn PNG". Old programmatic `/assets/cards/{key}_16x9.mp4` download links replaced.

**Deploys:**
- Flagship `solitary-sound-015a`: etag=de43e33e40e4, 2026-10-09T07:10:26Z (21 files)
- Portfolio `enmanuel-mejia`: 2026-10-09T07:09:39Z (2 files)

**Verification:** 10/10 `hq-{slug}_16x9.mp4` return HTTP 200 (il29/il28 needed ~60s CDN propagation on first check, confirmed 200 on retry). Cards library page 200, portfolio homepage 200.
