# TikTok-Style Cinematic Card Buildout — 2026-10-09

**User order:** 2026-10-09 ~01:48 EDT — TikTok IL-29 card style is now the STANDARD for all project cards sitewide.

## Source Style Analysis

From shared TikTok video (720×1280, 10s, 24fps):
- Dark cyberpunk background with HUD panels, circuit patterns
- Central hexagonal badge with circuit-board texture, thematic icon
- Rotating text ring (e.g., "ALLOWLIST"/"DENYLIST" alternating)
- Typography: project code (huge cyan), partner (huge orange), subtitle (cyan),
  main title (huge cyan + orange), "INTERSTITIUM LABS" branding with corner brackets
- Particle systems, glitch effects, glowing accents

## Projects (10)

| Key | Code | Partner | Icon | Accent | Secondary |
|-----|------|---------|------|--------|-----------|
| il-26 | IL-26 | DATA ANALYST | chart | cyan | blue |
| il-28 | IL-28 | DEVSECOPS | cloud | cyan | purple |
| il-29 | IL-29 | THREATLOCKER | lock | cyan | orange |
| devops-superlab | SUPERLAB | DEVOPS | terminal | green | cyan |
| rhel-fabric | RHEL-10 | RED HAT | server | red | cyan |
| bootcamp-catalog | 68× | INTERSTITIUM | cap | cyan | orange |
| tl-interview | TL-INT | THREATLOCKER | shield | cyan | orange |
| tl-assessment | TL-ASM | THREATLOCKER | checklist | cyan | orange |
| ai-vision | AIV | INTERSTITIUM | eye | purple | cyan |
| lps-enrollment | LPS | LAWRENCE PUBLIC SCHOOLS | chart | blue | cyan |

## Render Status

- [x] Generator built: `cinematic_card_gen.py`
- [x] Batch script: `batch_render.py`
- [ ] 9:16 renders (10) — IN PROGRESS
- [ ] 16:9 renders (10) — PENDING
- [ ] LinkedIn PNGs 1200×627 (10) — PENDING
- [ ] Posters verified — PENDING

## Deployment Plan

### 1. Portfolio (enmanueldmejia.com)
- Replace project card preview images with cinematic card videos (16:9 embeds with poster fallbacks)
- Worker: `enmanuel-mejia` via `~/workspace/portfolio-deploy-config.json`

### 2. Flagship (interstitiumlabs.dev)
- Update project sections sitewide with new cards
- Create `/cards/` library page with all 10 cards (video + download links)
- Worker: `solitary-sound-015a` via `.work/flagship-deploy-config-20261008.json`

### 3. LinkedIn
- Generate 1200×627 PNGs for each project
- User uploads via LinkedIn interface (cannot automate)
- Provide clear instructions

## Files
- Generator: `~/workspace/apex-audit/.work/tiktok-cards/cinematic_card_gen.py`
- Batch: `~/workspace/apex-audit/.work/tiktok-cards/batch_render.py`
- Output: `/tmp/card_renders/final/` → deploy to `~/workspace/apex-audit/docs/assets/cards/`

## Log
- 2026-10-09 01:50 EDT: Generator built, test render OK, batch started
- 2026-10-09 01:56 EDT: il-26 9:16 complete, style verified, text fitting fixed
- 2026-10-09 02:05 EDT: il-26 complete (5 files), il-28 9:16 done
- 2026-10-09 02:10 EDT: il-26, il-28 complete. il-29 9:16 in progress. 12/50 files done.
- 2026-10-09 02:25 EDT: /tmp cleared, lost renders. Restarted with workspace output dir. Scripts safe.
- 2026-10-09 02:35 EDT: All 50 files rendered (10 projects × 5 assets). Deployed to flagship.
- 2026-10-09 02:40 EDT: Portfolio updated with cinematic cards (featured + 10 individual cards). Deployed.
- 2026-10-09 02:45 EDT: All assets verified 200. COMPLETE.
