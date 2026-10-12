# Card Replacement Log — 2026-10-09 (subagent session d8ecf322)

User order ~05:52 EDT: "Replace all old style preview cards on Linkedin and everywhere else."

## Audit findings

**`~/workspace/apex-audit/docs/assets/cards/` (non-hq dir):** 50 old-style programmatic files found:
- `{key}_16x9.mp4`, `{key}_16x9-poster.png`, `{key}_9x16.mp4`, `{key}_9x16-poster.png`, `{key}_linkedin_1200x627.png` × 10 projects (ai-vision, bootcamp-catalog, devops-superlab, il-26, il-28, il-29, lps-enrollment, rhel-fabric, tl-assessment, tl-interview)
- Full-repo grep across `docs/` and `portfolio-site/` (html/js/json): **zero references** to any old-style file. All pages already pointed at `assets/cards/hq/`.

**`~/workspace/portfolio-site/index.html`:** 20 refs, all `assets/cards/hq/hq-*_16x9(.mp4|_poster.png)` — fully new standard. No changes needed.

**`~/workspace/apex-audit/docs/cards/index.html`:** template renders only `/assets/cards/hq/hq-${p.hq}_*` paths — fully new standard. No changes needed.

## Actions taken

1. **Archived 50 old-style files** → `~/workspace/apex-audit/.work/archived-old-cards-20261009/` (recoverable, not deleted).

2. **Noah AI HQ set created** (parent had generated pipeline videos + voiceover; normalized to hq/ naming):
   - `hq-noah_16x9.mp4` (7.1M, 1280×720, h264, 24fps, 10s, AAC 24kHz voiceover+ambient)
   - `hq-noah_9x16.mp4` (6.2M, 720×1280, h264, 10s, AAC voiceover+ambient)
   - `hq-noah_16x9_poster.png` (912K, verified non-black)
   - `hq-noah_9x16_poster.png` / `hq-noah_poster.png` (849K, verified non-black)
   - `hq-noah_linkedin.png` (869K, 1200×627, verified non-black — cinematic frame; replaces parent's earlier 54K PIL placeholder, file already swapped at 09:51 before this session)
   - Voiceover script: "Noah AI. Five natural voices. Five personas. Fourteen open-source models. Personalized tutoring with spaced repetition. Try it at Interstitium Labs."

3. **Flagship deployed**: `solitary-sound-015a`, etag=f9b06455a0ac, 2026-10-09T09:54:17Z, 5 files uploaded. (`_worker.bundle.js` verified current — newer than `_worker.js`, no rebuild needed.)

4. **Portfolio worker**: no deploy needed — `portfolio-site/index.html` unchanged in this session (already 100% HQ refs); deploy script reported 0 files to upload.

## Verification (live, this session)

- All 33 HQ assets (11 projects × 16x9 MP4 + 9x16 MP4 + LinkedIn PNG): **HTTP 200**
- Old-style URLs (`assets/cards/il-29_16x9.mp4`, `..._linkedin_1200x627.png`): **404** (gone from CDN)
- `https://interstitiumlabs.dev/cards/`: 200, template uses only hq/ paths
- `https://enmanueldmejia.com/`: 200
- Live `hq-noah_16x9.mp4` audio: AAC 24kHz confirmed

## Notes for parent

- LinkedIn browser task (36759d86) was already steered with the corrected cinematic `hq-noah_linkedin.png` before this session; local file verified as the cinematic version.
- `docs/cards/index.html` PROJECTS array does not yet include Noah — adding an 11th library entry is a product decision left to parent.
- Old files are archived (not deleted) at `.work/archived-old-cards-20261009/` if rollback is ever needed.
