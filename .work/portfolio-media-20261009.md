# Portfolio Animated Media Expansion — 2026-10-09

**User order:** 2026-10-09 ~01:42 EDT — "Same for byte byte go animated media you think they cover and span across the entirety of the site including my portfolio site"

## What was built

### 10 Project Explainer Videos
Original byte-byte-go style animated explainers, one per portfolio project card. Each ~6 seconds (2s title + 2×3s steps), 1280×720 H.264, with burned-in captions, SRT sidecar, and staged narration script.

| Video | Project Card | Size | Status |
|---|---|---|---|
| proj-il26.mp4 | IL-26 Data Analyst | 54K | 200 ✓ |
| proj-il28.mp4 | IL-28 DevSecOps | 48K | 200 ✓ |
| proj-il29.mp4 | IL-29 ThreatLocker AI | 77K | 200 ✓ |
| proj-superlab.mp4 | DevOps SuperLab | 42K | 200 ✓ |
| proj-rhel.mp4 | RHEL AI & Systems Fabric | 46K | 200 ✓ |
| proj-catalog.mp4 | Bootcamp Catalog (68) | 47K | 200 ✓ |
| proj-tl-interview.mp4 | ThreatLocker Interview | 46K | 200 ✓ |
| proj-tl-assess.mp4 | ThreatLocker Assessment | 51K | 200 ✓ |
| proj-aivision.mp4 | AI Vision Deck | 41K | 200 ✓ |
| proj-lps.mp4 | LPS Enrollment Analysis | 38K | 200 ✓ |

**Total:** ~490KB for all 10 videos. Lightweight by design.

### Portfolio Integration
- **10 video embeds** added to project cards — lazy-loaded via IntersectionObserver, click-to-play with "▶ Watch overview" button, muted/loop/playsinline for mobile
- **CSS** added for `.card-video` and `.video-play-btn` — dark-themed, matches portfolio aesthetic
- **JavaScript** added to app.js — lazy loading, play button handler, reduced-motion respect
- **Visual Library section** added after work grid — links to 200+ PDF guides, 29 video courses, 143 bootcamps, hands-on labs

### Deployment
- Worker: `enmanuel-mejia`
- Deployed: 2026-10-09T05:57:56Z
- All 10 videos verified HTTP 200 at `https://enmanueldmejia.com/media/videos/`
- Visual Library section confirmed live

## Design decisions
- **Lightweight over cinematic:** 38-77KB per video keeps the portfolio fast. These are animated diagrams, not film.
- **Click-to-play, not autoplay:** Respects user bandwidth and reduced-motion preferences. Videos lazy-load when scrolled into view but only play on click.
- **No TTS dependency:** All videos have burned-in captions + SRT + staged narration scripts. Ready for voiceover when TTS returns.

## Files
- Generator: `~/workspace/portfolio-site/.work/gen_portfolio_videos.py`
- Videos: `~/workspace/portfolio-site/media/videos/proj-*.mp4` (+ .srt + -script.txt)
- Framework: `~/workspace/story-videos/il_anim.py`

## Blocker (standing)
TTS voiceover down (auth token rejected 2026-10-08). All videos ship as captioned previews with narration scripts staged.
