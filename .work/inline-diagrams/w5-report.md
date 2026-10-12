# W5 Report — Inline Diagrams, Courses IL-25 through IL-29

**Worker:** W5 (of 6) · **Date:** 2026-10-09 ~02:16 EDT
**Animation standard:** ALL diagrams animated per user order 2026-10-09 ~02:15 EDT
("All media should be animated and dynamic not static — new standard approach").
Every figure was built with `Diagram.animate()` called before `render_figure()`.

## Animation confirmation
Each of the 944 figures contains the full animation package:
- **Staggered node entrances** — `a-node` hooks with per-element `animation-delay`
  (nodes pop in one-by-one in build sequence)
- **Flowing dashes on arrows** — `a-flow` hooks (`il-dash` keyframes, data-packet motion)
- **Accessibility** — every figure carries a `prefers-reduced-motion` block with a
  static fallback (`animation:none`, full opacity)
- Verified: 944/944 figures contain `@keyframes il-pop` + reduced-motion CSS; **0 static figures**

## Files processed (in `docs/university/data/courses/`)
| File | Modules | Diagrams added | Skipped |
|---|---|---|---|
| il-25-cybersecurity-professional-certificate.json | 27 | 108 | 0 |
| il-26-data-analyst-certification-senior-mastery.json | 53 | 212 | 0 |
| il-27-it-infrastructure-specialist-threatlocker-mastery.json | 56 | 224 | 0 |
| il-28-devsecops-cloud-infrastructure-mastery.json | 52 | 208 | 0 |
| il-29-threatlocker-ai-cybersecurity-mastery.json | 48 | 192 | 0 |
| **TOTAL** | **236** | **944** | **0** |

- Each file backed up first (`<file>.diagbak`); all 5 re-validated with `json.load` after edit.
- Mid-run correction applied: the first (static) pass was fully discarded — files were
  restored from `.diagbak` and regenerated from scratch with `d.animate()`.

## Diagram templates (4 per module, all content-grounded, composites varied)
- **D1 — Module path:** `flow()` of the first 4 note titles as an ordered reading path
  (alternates with `layers()` stack of ALL note titles on odd modules for variety).
  Fig nums `{MODULE}-D1`, e.g. `IL25-M01-D1`.
- **D2 — Key vocabulary:** `concept_box()` of `**bold**` terms harvested from the
  module's own note bodies (fallback: distinctive title words). Caption names the terms.
- **D3 — Module anatomy:** `table_schema()` inventorying the module's real components
  (notes / objectives / cards / quiz / drills / videos / PDFs / lab / mock task counts).
- **D4 — Know vs Do:** `compare()` splitting objectives by lead verb (Bloom's:
  define/describe/explain → KNOW; apply/build/configure/analyze → DO); falls back to a
  `concept_box` "How mastery is checked" when one side is empty.
- Figures appended to the end of the most topically-relevant note body
  (path→note 1, terms→term-densest/concept note, anatomy→last note, know-vs-do→procedure/hands-on note),
  spread across distinct notes; each has a real explanatory caption + meaningful alt text.

## Notes for coordinator
- No deployment performed (per instructions — coordinator handles deploy).
- Generator script: `.work/inline-diagrams/w5_generate.py` (now animation-enabled;
  reusable for future courses — call pattern is `d.animate()` before `d.render_figure()`).
- No modules skipped; no blockers encountered.
