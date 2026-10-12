# Media Quality Audit — 2026-10-09

**User order:** 2026-10-09 ~12:06 EDT — add media quality bar as hard constraint; audit all existing media; flag rebuilds.

**Reference bar:** "How a neural network actually learns" by The Tech World Labs
(https://www.facebook.com/reel/1101817935674577/) — verified via page fetch:
numbered 01–04 step sequence (forward pass → loss → backward pass → update),
live-updating values (loss 0.35→0.00, output 0.41→0.98 over 50 epochs),
music-bedded, single continuous animation, technical instructional tone.

**Template:** `SPEC-TEMPLATE.md` updated — new "Media Quality Standard" section
(9-point bar) + hard constraints #11 (media bar) and #12 (Media Inventory per
spec sheet). All 31 existing spec sheets predate this constraint and need a
Media Inventory section added on next touch.

## Audit results by category

### A. Social/marketing video cards (hq-*) — 22 videos — NEEDS UPSCALE
- Location: `docs/assets/cards/hq/` — 11 projects × 16:9 + 9:16
- Resolution: 1280×720 / 720×1280 (720p) — **BELOW** 1920×1080 / 1080×1920 floor
- Audio: all 22 have AAC voiceover — PASS
- Aesthetic: cinematic AI-generated footage (brand/mood cards). The bar's
  flat-infographic + step-sequence criteria target *educational explainers*;
  these are marketing assets — resolution upscale applies, style is
  category-appropriate.
- **Action: UPSCALE all 22 to 1920×1080 / 1080×1920.** Rebuilds must keep
  voiceover. Posters (`*_poster.png`, `*_linkedin.png`) regenerate at 1080p.

### B. Topic hero background loops — 12 videos — NEEDS REBUILD
- Location: `docs/assets/topics/*-hero.mp4`
- Resolution: 854×480 (480p) — **far below** floor
- Audio: silent — acceptable ONLY as ambient background loops (muted autoplay
  by design), but resolution fails regardless
- Duration: 6s loops
- **Action: REBUILD all 12 at 1920×1080 minimum.** (Or replace with
  resolution-independent canvas/CSS animation.)

### C. Local course videos — 598 MP4s — NEEDS UPSCALE
- Location: `docs/assets/videos/*.mp4` (1,765 files incl. .vtt/.narration.md)
- Resolution: 100% sampled at 1280×720 (720p) — **BELOW** 1920×1080 floor
- Audio: ~78% have audio track; ~22% silent (sampled 400/598)
- Style: many are 3b1b-style math explainers — already flat-infographic
  aesthetic, closest to the bar in spirit; they need resolution, not restyle
- Silent ones violate bar #7 unless they qualify as ambient loops
- **Action: UPSCALE all 598 to 1920×1080.** Audit silent ones: add
  music bed or voiceover, or reclassify as ambient.

### D. Inline AI algorithm animations (`il-algo-viz.js`) — 29 algorithms — NEEDS ENHANCEMENT
- Mount: `figure.aav[data-algo]`; 360×212 SVG viewBox (vector = resolution-independent — PASS)
- PASS: dark mode, mono/technical labels, live-updating values (e.g. MSE
  readout), punchy headline + one-line takeaway per algorithm (figcaption),
  one concept animated end-to-end, IntersectionObserver perf, reduced-motion support
- **GAPS vs bar:**
  1. No numbered step-sequence pills/badges (bar #6) — animations run as a
     single phase without labeled steps
  2. Silent — no music or voiceover (bar #7)
  3. Landscape-only 360×212 — no 9:16 vertical-responsive mode (bar #2)
- Injected in: IL-12, IL-16, IL-17, IL-26 course JSONs; topics ai-ml, data-eng, math pages
- **Action: ENHANCE — (1) add per-algorithm numbered step pills that highlight
  in sequence; (2) add Noah TTS narration toggle (`/api/noah/tts` first,
  speechSynthesis fallback); (3) add vertical-responsive layout for mobile.**
  The parallel 30-algorithm build MUST include these before shipping.

### E. OG images (1200×630) + LinkedIn PNGs (1200×627) — PASS
- Platform-standard sizes for link previews — correct, not subject to video bar.
- IL-30/IL-31 OG images verified 1200×630.

### F. External YouTube references — 965 module video refs — EXEMPT
- Third-party embeds: listed as `external` per template; must be cited, not
  mirrored. Out of scope for the resolution bar.

## Rebuild queue (priority order)

1. **D-enhance** — il-algo-viz step pills + narration + vertical mode (blocks the
   in-flight 30-algorithm build sign-off; highest leverage, one file)
2. **A-upscale** — 22 hq videos → 1080p + regenerate posters (user-facing social)
3. **C-upscale** — 598 course videos → 1080p (bulk; scriptable via ffmpeg
   upscale — note: pure upscale adds no detail; true "meet or exceed" for
   hero content wants re-render, upscale acceptable for back-catalog per
   "only improvements or upscaled implementations")
4. **B-rebuild** — 12 topic heroes at 1080p (480p is visibly soft on modern phones)
5. **C-audio** — identify the ~22% silent course videos; add beds/voiceover or
   reclassify

## Pipeline injection

The social-course-refresh pipeline (in build by coordinator) MUST apply this
bar to every media asset it generates: 1080×1920 floor, never silent,
numbered steps + headline + takeaway on explainers, Noah TTS narration option.
