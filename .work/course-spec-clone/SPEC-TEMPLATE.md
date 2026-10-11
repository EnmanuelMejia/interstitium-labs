# Course Spec Sheet Template (cloned from IL-29 pattern)

Every course gets a spec sheet at `.work/course-spec-clone/specs/<code>.md` BEFORE the v4 build.
The build must match the spec sheet exactly. The audit verifies this.

## Spec Sheet Fields

```markdown
# <CODE> · <Title> — Spec Sheet

## Identity
- code: IL-XX
- courseId: <slug from existing JSON>
- title: <full title>
- tagline: <one line>
- blurb: <one paragraph hero description>

## Hours (honest math)
- Declared hours: <number> (must equal sum of module estimatedMinutes ÷ 60, rounded)
- Time formula: "estimatedMinutes per module = instruction + videos + drills + hands-on lab, set per module by the author; course total = sum of module estimates. Declared hours are the honest rounded sum."

## Prerequisites
- <list of prereq courses by code, or "None — entry level">
- Prereq math supplement: <which math modules are embedded, e.g. "M00 discrete math primer">

## Learning Outcomes (objectives)
1. <outcome 1>
... (8-10 outcomes)

## Certification Mapping (independent-prep framing)
| Cert | Modules | Notes |
|------|---------|-------|
| <Cert Name + code> | <module IDs> | Independent preparation aligned to published objectives. |

Each certGates entry MUST include:
  framing: "Independent practice and preparation. Not affiliated with, endorsed by, or sponsored by any vendor or employer; confers no certificate."

## Module Plan
| # | Module ID | Title | Est. Minutes | Cert alignment |
|---|-----------|-------|--------------|----------------|
... (one row per module)

## Honesty Note (required verbatim pattern)
"This is an independent preparation and practice course aligned to publicly published exam objectives. It is not affiliated with, endorsed by, or sponsored by <vendors>; it confers no certificate and grants no credentials. Exam facts (domains, weights, question counts, durations, passing scores) reflect publicly published objectives as of <date>."

## Merge / Cross-link Notes
- Complementary courses: <codes>
- Frontier topics folded in: <topics>
- Cross-links added: <module IDs>

## Media Inventory (required)
List every inline media asset the build ships or references (videos, animations,
infographics, audio). For each: path/URL, format, resolution, duration, audio
track (voiceover/music/silent), and which module(s) embed it. Third-party
embeds (e.g. YouTube references) are listed as `external` and are exempt from
the resolution bar but must still be cited, not mirrored.

## Media Quality Standard — HARD CONSTRAINT (user order 2026-10-09)
Reference bar: "How a neural network actually learns" by The Tech World Labs
(https://www.facebook.com/reel/1101817935674577/) — crisp vector-style 2D
motion graphics, numbered step sequence, live-updating values, music-bedded.

Every inline media-rich resource the course ships MUST meet or exceed ALL of:
1. Crisp vector-style 2D motion graphics — sharp at any resolution (SVG or
   high-bitrate render; no blurry raster, no pixelation on zoom).
2. Resolution floor: 1080×1920 minimum for vertical (9:16, mobile-first);
   1920×1080 minimum for horizontal (16:9, desktop embeds). NEVER downscale —
   only improvements or upscaled implementations.
3. Flat infographic aesthetic with mono/technical labels — clean, minimal,
   no clutter. Dark-mode inline by default (site theme).
4. ONE concept animated end-to-end — live-updating values, charts, and
   visualizations in a single continuous animation (not cuts or scene changes).
5. Punchy bold headline + one-line takeaway per animation.
6. Labeled step sequence — numbered pills/badges that highlight in sequence
   as the animation progresses.
7. Music-bedded or voiceover — never silent (ambient background loops are the
   sole exception and must still meet the resolution floor).
8. High information density — everything animates simultaneously in a calm,
   dashboard-like aesthetic.
9. Short-form friendly — ~10–20s loops for social cuts, longer form allowed
   for course embeds.

Noah AI integration: educational animations SHOULD wire a Noah TTS narration
toggle (server `/api/noah/tts` first, browser speechSynthesis fallback) so the
voiceover criterion is satisfiable inline, not only in rendered video.
```

## Schema v4 Build Requirements

The JSON build must include ALL of these top-level keys (IL-29 pattern):
code, courseId, title, tagline, blurb, hours, mockMinutes, schemaVersion ("4"),
updatedAt, honestyNote, objectives, arc, priorities, battlePlan, modules,
crosswalk, certGates, readinessDashboard, scriptLabs, drills, scenarios,
trainers, terminalSims, mockTasks, cheatSheets, answerBank, sourceLinks,
toolLabs, multicloudLabs, sampleDatasets, installSteps, installPrereqOrder,
installLabs, employerMappings, jdMatrix, sqlPlaygrounds, pythonExercises,
daxPlaygrounds, branchingScenarios, clickSims, interactivityAudit, studyGuide,
timeFormula, glossary, faq, tips, legends, topicTheme, topic

Each module must have:
id, code, title, summary, objectives, estimatedMinutes, weight,
prerequisiteFor, crossLinks, cards, quiz, drills, handsOnLab, mockTask,
videos, pdfs, notes

## Hard Constraints (audit fails if violated)
1. schemaVersion MUST be "4" (string)
2. hours MUST equal honest rounded sum of module estimatedMinutes
3. Every certGates entry MUST carry the independent-prep framing
4. NO invented metrics, credentials, testimonials, or exam braindumps
5. NO Palantir/NSA certification claims
6. honestyNote MUST be present and name the relevant vendors
7. Prereq math supplement module(s) MUST exist for technical courses
8. Paywall: IL-27/28/29 free; all others $249 (badge handled by site chrome, not JSON)
9. Dark mode default (site chrome, not JSON)
10. sourceLinks MUST have retrieved dates for third-party factual claims
11. Media Quality Standard (above) MUST be met by every inline media asset
    the build ships: resolution floor 1080×1920 vertical / 1920×1080
    horizontal; never silent (except ambient background loops); numbered step
    sequence + headline + one-line takeaway on educational animations.
    Existing assets below the bar MUST be flagged for rebuild/upscale —
    never shipped as-is at subpar quality.
12. Every spec sheet MUST carry a Media Inventory section listing all inline
    media with format, resolution, duration, and audio status.
