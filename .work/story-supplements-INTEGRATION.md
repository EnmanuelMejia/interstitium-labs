# Story Supplements — Integration Note

**Date:** 2026-10-08
**What:** 104 "The story behind X" narrative training supplements covering all 29 Interstitium Labs courses (IL-01–IL-29).
**Status:** Content complete and validated. Player wiring NOT implemented (left for the course-player owner).

## Files

- Story files: `docs/university/data/courses/stories/<course-slug>-stories.json` (one per course, 29 files)
- Index: `docs/university/data/courses/stories/_index.json` — maps course slug → story file, count, and per-story `{id, title, moduleId}`
- **Course JSONs were intentionally NOT modified** — a sibling worker is editing them for videos. The player must join stories at render time via `_index.json`, never by expecting a `stories` key inside course JSON.

## Story object schema

```json
{
  "id": "<course-slug>-story-<n>",
  "course": "<course-slug>",
  "moduleId": "<module id in the course JSON, or null>",
  "title": "The story behind <X>",
  "hook": "1–2 sentence opening human moment",
  "narrative": "the story, 300–600 words (all 104 validated in range)",
  "bridge": "1–2 sentences tying the story into the lesson",
  "figures": [{"name": "...", "role": "...", "dates": "..."}],
  "verifiedClaims": ["each checkable historical claim in the story"]
}
```

Every `moduleId` was verified to exist in its course JSON. `verifiedClaims` is the audit trail: each entry is a fact the author asserts is verifiable (person, date, event). If a claim is ever challenged, check it against the cited claim — not the prose.

## Recommended player surfacing

1. **Story card before module content.** When a learner opens a module that has a mapped story (`story.moduleId === module.id`), render a "The story behind X" card FIRST — hook as the headline, narrative as the body, bridge as the transition into the lesson content. The bridge is written to hand off directly ("Now let's learn…").
2. **Course-level stories.** A course's stories array may also be shown as a "Stories" rail on the course overview page.
3. **Academy catalog "Stories" section.** `_index.json` supports a cross-course Stories browser: 104 entries with course + module linkage. Good for "story of the day" features.
4. **Fallback.** If a module has no story, render nothing (no placeholder). Do not auto-generate stories client-side — historical integrity is the requirement.

## Content notes for the player team

- Tone: story-driven, historically grounded, accessible. Each story opens with a human moment, traces real history, connects to the present, and ends with the `bridge` hook into the lesson.
- Historical integrity: every person/date/event is real; uncertain details were either verified via web search during authoring or omitted. Known honest framings are inside the prose (e.g., the "bug" didn't originate with the moth; Casaubon debunked the Corpus's age; Fisher's eugenics; the Zohar's dating).
- Two courses share a topic from different angles by design: the SQL/relational story appears in IL-09 (Oracle commercialization angle) and IL-15 (analyst fluency angle).
- No lab-only stories were needed: labs live inside modules, and module mapping covers them.

## Counts per course

IL-01: 3, IL-02: 3, IL-03: 3, IL-04: 3, IL-05: 3, IL-06: 4, IL-07: 3, IL-08: 3, IL-09: 4, IL-10: 3, IL-11: 3, IL-12: 4, IL-13: 3, IL-14: 3, IL-15: 3, IL-16: 3, IL-17: 4, IL-18: 3, IL-19: 4, IL-20: 5, IL-21: 4, IL-22: 5, IL-23: 4, IL-24: 4, IL-25: 4, IL-26: 4, IL-27: 4, IL-28: 4, IL-29: 4 — **104 total**.
