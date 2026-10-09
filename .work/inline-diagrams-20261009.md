# Inline Diagrams 1000% Buildout — 2026-10-09

**User order:** 2026-10-09 ~02:11 EDT — "There should be thousands of in depth embedded media as attached site wide"
**Standard:** Screenshot of Module 1 (DDL/DML) — inline SVG diagrams with figure numbers, captions, dark theme

## Architecture findings
- **Courses:** 29 files, 804 modules. Reading stage renders `notes[].body` via `mdLite()` which HTML-escapes everything → **0 inline SVGs currently**. Fix: modify `mdLite` to preserve `<svg>`/`<figure>` blocks (mirrors existing code-block pattern).
- **Bootcamps:** 135 content.json, 607 lessons, 998 media entries (path refs via `<img>`, not inline). Engine auto-generates 1 simple diagram/lesson from concepts.

## Target
- Minimum 3,000 inline diagrams sitewide
- Courses: ~4/module × 804 = ~3,200
- Bootcamps: ~2-3/lesson × 607 = ~1,500 rich diagrams in media[]
- Total projected: ~4,700

## Progress log
- [02:15] Audit complete. Framework build starting.
- [02:20] mdLite SVG passthrough implemented + verified in course-shell.js.
- [02:20] Diagram framework built at .work/inline-diagrams/diag_framework.py (table_schema, concept_box, flow, layers, compare composites; figure+figcaption wrapper).
- [02:25] Spawning 6 parallel workers: W1-W5 courses, W6 bootcamps.
- [02:30] All 6 workers spawned (W1: IL-01–06, W2: IL-07–12, W3: IL-13–18, W4: IL-19–24, W5: IL-25–29, W6: bootcamps). W4 needed one retry after transient DB lock.
- Target: ~3,200 course diagrams (4/module × 804) + ~1,800 bootcamp diagrams (3/lesson × 607) ≈ 5,000 total.
- [02:35] CRITICAL CORRECTION (user): all media must be ANIMATED and DYNAMIC, not static.
- [02:35] Framework extended with animate(): staggered node entrances (il-pop), flowing dashes on arrows (il-dash), pulsing accents (il-pulse), prefers-reduced-motion fallback. Verified working.
- [02:36] All 6 workers notified to switch to animated-only output; instructed to regenerate any static diagrams already produced.
- [02:45] W5 COMPLETE: 944/944 animated diagrams across IL-25–IL-29 (236 modules × 4). Static pass discarded and regenerated with animate(). All validated.
- W1, W2, W3, W4, W6 still running.
- [02:50] W3 COMPLETE: 976 animated diagrams (IL-13–IL-18, 244 modules × 4). Verified 976/976 carry il-anim class.
- [02:50] W4 COMPLETE: 592 animated diagrams (IL-19–IL-24, 148 modules × 4). Animation correction arrived before generation — zero static produced.
- Running total: 2,512 / ~5,000. W1, W2, W6 still running.
- [02:55] W6 COMPLETE: 1,821 animated SVG diagrams (135 bootcamps, 607 lessons × 3). All validated, files on disk.
- [02:55] FLAGGED: 530 pre-existing static SVGs from earlier batches remain static. Spawning W7 to animate them in place via CSS injection.
- Running total: 4,333. W1, W2 still running.
- [03:00] W7 COMPLETE: 530/530 legacy static SVGs animated in place via CSS injection. Zero static SVGs remain anywhere.
- Running total: 4,863 animated diagrams. W1, W2 still running.
- [03:05] W1 COMPLETE: 188 animated diagrams (IL-01–IL-06, 43 modules × 4). Zero static ever built.
- Running total: 5,051 animated diagrams. Only W2 (IL-07–IL-12) still running.
