# Cinematic Standard — Universal Visual Identity Rollout

**Mandate:** User orders 2026-10-09 ~01:48/01:51 EDT. The TikTok IL-28/IL-29 card style is the NEW STANDARD for ALL builds and ALL content — retroactively (update everything already deployed) and moving forward (all new content uses it by default). All sites: interstitiumlabs.dev, learn.interstitiumlabs.dev, app.interstitiumlabs.dev, enmanueldmejia.com.

## The Standard

**Course variant (IL-28 style):** circuit-trace bg, "INTERSTITIUM LABS · SCIENTIA OMNIA VINCIT" header, massive white glowing code, cyan line1 / orange line2 subtitles, tech-framed "N INTERACTIVE MODULES" badge (real module counts), floating binary, HUD circles, "interstitiumlabs.dev" footer with corner brackets.

**Bootcamp variant (IL-29 style):** hexagonal badge with code + thematic icon, rotating text ring with key terms, cyan code / orange accent / gray subtitle / huge cyan+orange title, "INTERSTITIUM LABS" branding, glitch effects (animated).

**Shared:** dark cyberpunk bg (circuit traces, grid, vignette), cyan/orange palette, particles, scanlines, corner-bracket HUD, SYS.ONLINE readout.

## Template module

- `~/workspace/story-videos/il_cinematic.py` — `CourseCard`, `BootcampCard`, `render_poster()`, `render_animated()`
- Sizes: (1280,720) cards, (1200,630) OG, (1080,1920) TikTok vertical
- Staging: `~/workspace/cinematic-assets/` (NOT docs/assets/videos/ — avoids the B1–B4 incident zone)

## Rollout batches

| Batch | Scope | Count | Status |
|---|---|---|---|
| C1 | 29 course posters (1280×720) | 29 | DONE 2026-10-09 ~02:00 EDT (batch C1+C2 worker) |
| C2 | 29 course OG images (1200×630) | 29 | DONE 2026-10-09 ~02:00 EDT (batch C1+C2 worker) |
| B1 | 135 bootcamp posters (1280×720) | 135 | DONE 2026-10-09 ~02:15 EDT (batch B1+B2 worker) — staged in cinematic-assets/bootcamps/ |
| B2 | 135 bootcamp OG images (1200×630) | 135 | DONE 2026-10-09 ~02:15 EDT (batch B1+B2 worker) — staged in cinematic-assets/bootcamps-og/ |
| A1 | 29 course animated title cards (6s MP4) | 29 | TODO |
| P1 | PDF cinematic cover template (reportlab) | 1 module | TODO |
| P2 | Retrofit 200+ PDF covers | 200+ | TODO — after P1 |
| S1 | Main-site hero + course/project cards (HTML/CSS) | ~15 pages | TODO |
| S2 | Video intro/outro template → cinematic | 1 patch | TODO |
| S3 | OG/Twitter card wiring sitewide | — | TODO — after C2/B2 |

## Retroactive inventory (old style → replace)

- [ ] Course card thumbnails (if any non-standard exist on /university/)
- [ ] Bootcamp card images on /bootcamps/ index
- [ ] Existing video title cards (leave rendered MP4s; new renders use cinematic intro)
- [ ] Existing PDF covers (200+ — retrofit via P2)
- [ ] Homepage hero (keep animated hero per user mandate — "Animated homepage hero stays unchanged")
- [ ] Portfolio cards (sibling agent 58762776 handling — do not duplicate)

**NOTE:** User mandate says "Animated homepage hero stays unchanged" — do NOT restyle the homepage hero.

## Moving-forward hooks

- [ ] `il_anim.py` title card → cinematic intro (patch, API-stable)
- [ ] `bbg_style.py` title_page → cinematic cover (patch, API-stable)
- [ ] New generator scripts import from il_cinematic by default

## Run log

- **2026-10-09 ~01:50 EDT:** Module built (`il_cinematic.py`), smoke-tested both variants, layout fixes applied (ring-label half-step offset, bootcamp vertical rhythm). Tracker created.
- **2026-10-09 ~01:55 EDT:** Moving-forward hooks installed and verified: `il_anim.py` title card → cinematic intro (API-stable delegate); `bbg_style.py` title_page → cinematic PDF cover via new `il_cinematic_pdf.py`. Smoke-tested both. Course metadata generated (`cinematic-assets/courses-meta.json`, 29 courses with real module counts). Dispatched 3 workers: C1+C2 (58 course PNGs), B1+B2 (286 bootcamp PNGs), A1 (29 course animated MP4s). Staging in `~/workspace/cinematic-assets/` (isolated from the B1–B4 video incident zone).
- **User directive 01:51 EDT (retroactive + forward, all sites):** Tracker updated to reflect mandate. Retroactive inventory added. Homepage animated hero explicitly EXCLUDED per standing user mandate. Portfolio cards handled by sibling agent — no duplication.
- **2026-10-09 ~02:10 EDT:** Ring-term quality fix complete — 15 cards re-rendered with word-boundary matching + 17-slug DOMAIN_OVERRIDES. All 270 bootcamp PNGs verified.
- **2026-10-09 ~02:00 EDT — BATCH C1+C2 COMPLETE:** All 29 courses × 2 sizes = 58 PNGs rendered with zero failures (render time ~68.5s). Seed = course index (varied circuit backgrounds). Staging: `cinematic-assets/courses/{CODE}.png` (1280×720), `cinematic-assets/courses-og/{CODE}-og.png` (1200×630). Verification: 29+29 files exist, zero empty files; spot-checks via ffprobe/file (IL-28, IL-12-og, IL-01, IL-29-og) all valid PNG at correct dimensions. Batch script kept at `cinematic-assets/batch_c1c2.py` for re-runs. Tracker C1/C2 marked DONE. Nothing written to apex-audit/docs/ (staged only in cinematic-assets/).
- **2026-10-09 ~02:15 EDT — BATCH B1+B2 COMPLETE:** All **135 bootcamps × 2 sizes = 270 PNGs** rendered, zero failures, zero skips. Source of truth: dirs in `cert-bootcamps/site/bootcamps/` with a `content.json` (skipped `_engine`, `engine`; includes `roles-library` and `vendor-map` content pages). Note: actual bootcamp count is 135, not the estimated 143 (143 was the raw directory listing incl. files). Card fields derived per spec: short codes (override table for cert codes, acronym fallback), vendor accent org, keyword subtitle/ring/icon/palette; seeds = 7 + 13×index (varied per bootcamp). Staging: `cinematic-assets/bootcamps/{slug}.png` (1280×720), `cinematic-assets/bootcamps-og/{slug}-og.png` (1200×630). Verification: 270/270 valid PNGs at exact dimensions, none empty (PIL load check). Spot-check aws-saa.png: hex badge + cloud icon + ring terms + cyan code / orange accent / gray subtitle / huge two-line title + INTERSTITIUM LABS branding — matches IL-29 standard. First run died at 98/135 (background session aborted, /tmp script wiped); resumed idempotently from `cinematic-assets/render_bootcamps.py` (skip-if-exists), remaining 37 rendered cleanly. Batch script kept at `cinematic-assets/render_bootcamps.py` for re-runs. Tracker B1/B2 marked DONE. Nothing written to apex-audit/docs/ or cert-bootcamps/site/ (staging only).
- **2026-10-09 ~02:30 EDT — RING-TERM FIX (substring → word-boundary matching):** Quality issue found in bootcamp posters: `render_bootcamps.py` classified ring_terms/icon/palette/accent with substring `k in s` matching, which misfired on 15 cards (e.g. "ASSOCIATE" contains "soc" → AWS-SAA got cyber terms THREAT/DEFENSE/ZERO TRUST/EDR; "training"/"certification"/"containers" contain "ai" → fde-training/docker/quantum got data/AI terms; "systems-" contains "ms-" → MICROSOFT accent on acad-systems/systems-cs/python-systems; "blockchain" contains "lock" → cyber on blockchain-dev). Fix: all keyword matching now uses regex word boundaries (`_wb()` helper), key lists hardened (added cybersecurity, encryption, hardening, endpoint, fde, devsecops, cybernetics, entrepreneurship, hermetic/hermetica, database, zerotrust keys), and a `DOMAIN_OVERRIDES` table pins known slugs explicitly (aws-saa/k8s-associate→cloud, fde-training/devsecops-mastery/m365-endpoint-admin/nice-framework→cyber, cybernetics/quantum→math, entrepreneurship/tl-interview→career, blockchain-dev→code, zerotrust→cyber+lock, acad-hermetica→esoteric, isc2-cc→cyan_red, docker→cyan_orange, accent fixes). Affected set computed by diffing old vs new logic over all 135 bootcamps = **15 cards** (acad-systems, aws-saa, blockchain-dev, cybernetics, devsecops-mastery, docker, fde-training, k8s-associate, m365-endpoint-admin, nice-framework, python-systems, quantum, systems-cs, tl-endpoint-ops, tl-interview). Deleted only those 30 PNGs (both sizes) and re-ran the idempotent script — re-rendered 30/30, zero failures, TOTAL=135 DONE=135. Verification: all 30 re-rendered PNGs valid via PIL at exact dimensions (1280×720 / 1200×630), none empty; full set still 135+135, zero empties. Nothing written outside cinematic-assets/.
