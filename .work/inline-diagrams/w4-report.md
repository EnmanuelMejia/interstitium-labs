# W4 Report — Inline Diagrams, IL-19 through IL-24

**Worker:** W4 | **Date:** 2026-10-09 ~02:20 EDT
**Animation standard:** ✅ ALL 592 DIAGRAMS ANIMATED — `d.animate()` called on every diagram
before `render_figure()` (staggered node pop-in entrances, flowing-dash arrows,
`prefers-reduced-motion` static fallback). The animation correction arrived before any
generation began, so no static diagrams were ever produced — no regeneration was needed.

## Totals

| File | Modules | Diagrams added | Animated |
|---|---|---|---|
| il-19-multicloud-devops-ai-bootcamp.json | 67 | 268 | 268 |
| il-20-mathematics.json | 16 | 64 | 64 |
| il-21-humanities.json | 16 | 64 | 64 |
| il-22-esoteric-secret-knowledge.json | 18 | 72 | 72 |
| il-23-frontier-knowledge.json | 15 | 60 | 60 |
| il-24-threatlocker-assessment-prep-cbt.json | 16 | 64 | 64 |
| **TOTAL** | **148** | **592** | **592** |

**Modules skipped:** 0. **Generation failures:** 0. **Modules with ≠4 figures:** 0 (verified per-module).

## Diagram design (4/module, content-derived from each module's own text)

- **D1 — concept_box "The core idea"** → appended to the *Concepts* note. Module title + its top 3
  objectives as the competency contract. Green accent.
- **D2 — table_schema "Key vocabulary"** → appended to the *Key takeaways* note (fallback: last note).
  Parsed from the Concepts note's `**term** — definition` bullets (up to 6 rows, term left /
  meaning right). Fallback when <3 bullets: concept_box "Key ideas".
- **D3 — compare "Common trap → The discipline"** → appended to the *Common mistakes* note.
  Trap names (red) vs. first-sentence fixes (green), parsed from the mistakes bullets (up to 4 pairs).
  Fallback when <2 pairs: concept_box "Traps to avoid".
- **D4 — flow "The hands-on sequence"** → appended to the *Hands-on procedure* note.
  Numbered lab steps as animated left-to-right flow boxes (box width auto-shrinks to fit 720px).
  Fallback when <3 numbered steps: *layers* "Module roadmap" of the module's note structure.

Each figure carries a unique fig_num (`{module-id}-D1…D4`), a 1–2 sentence explanatory caption,
and meaningful alt text. Text is truncated to fit its container (no SVG overflow).

## Safety

- Backups: each file copied to `<file>.diagbak` before editing.
- Validation: `json.load()` re-parsed every file after writing — all 6 valid.
- Idempotency: generator skips modules already containing `Fig. {id}-D1` (safe to re-run).
- Generator script: `~/workspace/apex-audit/.work/inline-diagrams/w4_generate.py`

## Notes

- No deploy performed — coordinator handles deployment after all workers finish.
- Minor: on modules with no *Key takeaways* note (e.g. prereq-math modules), D2 falls back to the
  last note, so a note can occasionally host 2 figures. Within the task's distribution rules.
