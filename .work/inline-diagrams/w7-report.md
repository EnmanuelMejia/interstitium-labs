# W7 Report — Animate 530 Legacy Static SVGs In Place

Date: 2026-10-09 ~02:30 EDT
Source list: `~/workspace/apex-audit/.work/inline-diagrams/w6-static-remaining.txt`
Script: `~/workspace/apex-audit/.work/inline-diagrams/w7-inject.py`

## Result

| Metric | Count |
|---|---|
| Total in list | 530 |
| Animated | 530 |
| Skipped (already animated) | 0 |
| Errors | 0 |

Note: `wc -l` shows 529 because the list's final line has no trailing newline; the
actual file count processed was 530 (deduped earlier at 530 unique).

## What was done (CSS-only, non-destructive injection)

For each SVG:
1. Read the file.
2. Pre-screened: none of the 530 files used `transform=` attributes (so the
   scale-based entrance cannot clobber existing attribute transforms), and none
   were already animated.
3. Backed up to `<file>.w7bak` (only if no `.w7bak` existed).
4. Inserted a `<style>` block immediately after the opening `<svg …>` tag with:
   - `@keyframes il-pop` — opacity + scale(.85→1) entrance, `transform-box: fill-box`
   - `@keyframes il-dash` — flowing dashes for dashed lines/paths (`stroke-dashoffset`)
   - `@keyframes il-pulse` — defined for future use
   - Staggered entrances: base rule on all direct children plus
     `svg.il-anim > :nth-child(2..60)` with delays `(n-2)×0.07s` capped at 2s
   - Infinite dash flow: `svg.il-anim line[stroke-dasharray], svg.il-anim path[stroke-dasharray]`
   - `prefers-reduced-motion: reduce` — disables all animations, forces opacity 1
5. Appended `il-anim` to the root `<svg>` class (preserving existing classes).
6. Validated each file with `xml.etree` parse; on failure the backup would be
   restored (no failures occurred).

No diagram structure, content, or geometry was modified — animation only.

## Validation

- Per-file XML validation during injection: 530/530 valid.
- Spot-check of 5 random files (dotnet-entity-framework, platform-engineering,
  aws-scs-iam, ides-tooling-terminal-tasks, nsa-codebreaker-net-analysis):
  `<style>` present, `il-anim` class present, `@keyframes il-pop` present,
  XML valid, `.w7bak` backup present — all 5 pass.

## Open items / follow-ups

- NOT deployed (per instructions). Deployment is the parent's call.
- If any SVG renders oddly post-injection (e.g. an entrance flash on load),
  restore from `<file>.w7bak`.
- The 1,821 W6 animated SVGs were not touched by this workstream.
