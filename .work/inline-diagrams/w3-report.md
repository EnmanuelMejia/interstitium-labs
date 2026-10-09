# W3 Report — Inline Diagrams, Courses Batch W3 (IL-13 through IL-18)

**Worker:** W3 · **Completed:** 2026-10-09 ~02:20 EDT
**Standard:** user order 2026-10-09 ~02:15 EDT — **all diagrams animated** (staggered node entrances, flowing dashes, pulsing accents, `prefers-reduced-motion` static fallback). Every one of the 976 figures calls `d.animate()` before render.

## Totals

| File | Modules | Figures added |
|---|---|---|
| il-13-software-engineering-interview-prep.json | 58 | 232 |
| il-14-sre-devops-cloud-security-interview-prep.json | 31 | 124 |
| il-15-data-engineering-analytics-interview-prep.json | 32 | 128 |
| il-16-machine-learning-ai-engineering.json | 46 | 184 |
| il-17-agentic-ai-engineering.json | 45 | 180 |
| il-18-technical-leadership-interview-prep.json | 32 | 128 |
| **Total** | **244** | **976** |

**4 figures per module — target met, none skipped.**

## What each module got (4 animated diagrams, content derived from the module's own notes)

- **D1 — Concept stack (layers):** bold terms from the module's "Concepts" note, ordered foundation → application, subtitles from the definitions. Embedded at end of Concepts note.
- **D2 — Hands-on procedure (flow):** the module's numbered procedure steps as an animated flow with flowing dashes. Embedded at end of Hands-on procedure note.
- **D3 — Pitfalls vs strong moves (compare):** red "Pitfalls that lose points" from the pitfalls/common-mistakes note vs green "Strong moves" from the worked-example note. Embedded at end of the pitfalls note.
- **D4 — Mastery checklist (concept_box):** the module's objectives as a checklist. Embedded at end of the Project brief note.

Each figure: unique `Fig. <slug>-D1..D4` label, 1–2 sentence explanatory caption, meaningful `aria-label` alt text, dark theme, `il-diagram` figure wrapper (already preserved verbatim by `mdLite` in course-shell.js).

## Safety

- Backups: each file copied to `<file>.json.diagbak` before editing (6 backups, untouched).
- JSON validity: `json.load` validated before every `os.replace`; final sweep re-validated all 6 files — all parse.
- Formatting: files use 1-space indent; writes preserve it (verified byte-identical roundtrip on unmodified content).
- Label uniqueness: all 976 `Fig.` labels unique sitewide (3 cross-file slug collisions on the prereq `math-stats` modules fixed with `IL-13/14/15-` prefixes).
- Animation: every figure's SVG carries `class="il-anim"` (976/976 verified) with the injected keyframe CSS.

## Generator

`~/workspace/apex-audit/.work/inline-diagrams/w3_generate.py` — idempotent per-file processor; counts written to `w3-counts.json`. Reusable for other courses (uses framework composites only; no static SVGs).

## Notes for coordinator

- NOT deployed — per task, deployment is the coordinator's step.
- No modules skipped; no errors. One parser bug found and fixed during dry-run (4-char `- **` prefix strip).
- Content extraction depends on note conventions (`- **Term** — def` bullets, `1. **Step**` numbered lists) — held across all 244 modules; fallbacks (objectives/bullets) engage where a note lacks the pattern.
