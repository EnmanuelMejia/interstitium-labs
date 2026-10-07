# Course JSON Schema v1.0 — Interstitium Labs unified course shell

Companion to `university/course.html` + `course-shell.js` + `course-shell.css`.
The shell is **presentation only**: it renders whatever document it is given and
must never drop fields. All content is authored per-course in Phase 2 — this
file defines the contract, nothing more.

Honesty rules (UNIFIED-STANDARD §5, binding): original content only; no
invented course content, testimonials, credentials, or metrics; no vendor-exam
braindumps; source every factual third-party claim (`sourceLinks[].retrieved`).

## Data sources

1. Inline: `<script type="application/json" id="il-course-data">…</script>`
   inside `course.html` (preferred for production pages).
2. Query param: `course.html?data=<url-encoded path to course JSON>`
   (same-origin; used by preview tooling).
3. Default: `../data/courses/<courseId>.json` where `courseId` is read from
   `document.body.dataset.course` or `course.html?course=<id>`.

## Top-level document

| Field | Type | Required | Notes |
|---|---|---|---|
| `schemaVersion` | string | yes | `"1.0"` |
| `courseId` | string | yes | URL-safe slug. Progress keys: `ilc:<courseId>:<key>` |
| `code` | string | yes | Academy code, e.g. `"IL-11"` |
| `title` | string | yes | Course title |
| `tagline` | string | no | Short line under the title |
| `blurb` | string | yes | One-paragraph hero description (markdown-lite) |
| `hours` | number | no | Total estimated hours |
| `updatedAt` | string | no | ISO date, rendered in the date-line |
| `objectives` | string[] | yes | Brief tab: learning objectives |
| `arc` | `{phase,title,body}[]` | yes | Brief tab: synthesis-arc cards (3 recommended) |
| `priorities` | `{label,minutes}[]` | yes | Brief tab: priority bars with minute blocks |
| `battlePlan` | `{id,title,minutes,detail?}[]` | yes | Plan tab: timed checklist |
| `modules` | `Module[]` | yes | Study tab |
| `scriptLabs` | `ScriptLab[]` | yes (may be `[]`) | Labs tab |
| `drills` | `Drill[]` | yes (may be `[]`) | Labs tab |
| `policyDrills` | `Drill[]` | no | Labs tab (Policy sub-tab; optional extension) |
| `scenarios` | `Scenario[]` | yes (may be `[]`) | Labs tab |
| `trainers` | `Trainer[]` | yes (may be `[]`) | Labs tab |
| `terminalSims` | `TerminalSim[]` | no | Labs tab (Terminal sub-tab; optional extension) |
| `mockMinutes` | number | yes | Mock tab countdown length |
| `mockTasks` | `MockTask[]` | yes | Mock tab |
| `cheatSheets` | `CheatSheet[]` | yes (may be `[]`) | More tab |
| `answerBank` | `{q,a,ref?}[]` | yes (may be `[]`) | More tab: model answers |
| `sourceLinks` | `{name,url,note?,retrieved?}[]` | yes | More tab: source trail |
| `honestyNote` | string | no | Rendered in More; e.g. "confers no certificate" |

## Module

`{ id, code, title, weight?, summary, objectives?, notes[], cards[], quiz[] }`

- `weight` (number, default `1`): readiness uses a **weighted** module fraction.
- `notes[]`: `{ title, body, code?, lang? }` — collapsible; `body` is markdown-lite
  (see below); `code` renders in a `<pre>` block.
- `cards[]`: `{ front, back }` — tap-to-flip flashcards with a pager and
  know/again rating.
- `quiz[]`: `{ q, choices[], answer (0-based index), explain }` — MC quick-check
  with why-explanations.

## ScriptLab

`{ id, title, brief, starter, required[], hint, solution }`

- `starter`: pre-filled code in the task editor.
- `required[]`: fragment strings the submission must contain (validated live).
- `hint`: revealed on request. `solution`: revealed **only after an attempt**
  (submitted at least once).

## Drill

`{ id, title, prompt, snippet?, choices[], answer, explain }`

Quick-fire MCQs; `snippet` renders as code. Same shape is reused by `policyDrills`.

## Scenario

`{ id, title, context, steps[] }`

`steps[]`: `{ prompt, options[] }`; `options[]`: `{ text, correct, why }`.
Multi-step decision tree — each choice shows its why-explanation before the
next step. Completing all steps marks the scenario done.

## Trainer

`{ id, title, brief, kind }`

- `kind: "cidr"`: built-in random-CIDR generator (network / broadcast /
  usable-hosts / mask fields, streak + best persisted). Ships in the shell,
  works with zero course data.
- `kind: "custom"` (Phase 2): reserve for per-course generators; shell renders
  the brief plus a "coming with course data" note when unsupported.

## TerminalSim

`{ id, title, brief, prompt?, commands[] }`

- `commands[]`: `{ cmd, out }` — canned shell; exact match first, then a
  "did you mean" fuzzy suggestion, up-arrow history. `help` is built in and
  lists the canned command set.

## MockTask

`{ id, type, q|prompt, choices?, answer, explain, starter?, required?, hint? }`

- `type: "choice"` — `{ q, choices[], answer (index), explain }`.
- `type: "code"` — `{ prompt, starter, required[], answer (model text shown at
  review), explain }`; scored by required-fragment presence.
- Flag-for-review, question map, countdown timer, per-task review, best score.

## CheatSheet

`{ title, blocks[] }`; `blocks[]`: `{ h, body, code?, lang? }`.

## Markdown-lite

Allowed in `blurb`, note bodies, briefs, cheat-sheet bodies: `**bold**`,
`` `code` ``, fenced ```code blocks```, `- ` lists. Everything else is escaped.

## Progress key vocabulary (per course)

All keys are stored flat in `localStorage` under `ilc:<courseId>:<key>` and
mirrored server-side under the top-level object `<courseId>` via
`PUT /api/progress` (body `{ progress: { <courseId>: { … } } }`).

| Key | Value | Set by |
|---|---|---|
| `battle:<id>` | `"1"` | Plan checklist |
| `module:<id>` | `"1"` | Study: module marked complete |
| `quiz:<id>:<qi>` | chosen index | Study quizzes |
| `card:<mid>:<ci>` | `"know"`/`"again"` | Flashcards |
| `lab:<id>` | `"done"` | Script labs |
| `labdraft:<id>` | editor text | Script labs (drafts) |
| `drill:<id>` | `"1"` | Drills (answered correctly) |
| `policy:<i>` | `"1"` | Policy drills |
| `scenario:<id>` | `"1"` | Scenarios |
| `scenario:<id>:<step>` | chosen option index | Scenarios (audit trail) |
| `trainer:<id>:streak` | number | Trainers |
| `trainer:<id>:best` | number | Trainers |
| `term:<id>:seen` | `"1"` | Terminal sim opened |
| `mock:best` | number (0–100) | Mock best score |
| `mock:sessions` | number | Mock attempts |
| `mock:session` | JSON `{t0,acc,running,answers,flags}` | Mock timer state |

## Readiness formula (cloned verbatim from the reference shell)

```
readiness =
  battleFrac       × 20
+ moduleFrac      × 25   (weighted by Module.weight)
+ labFrac         × 35   (scriptLabs + drills + scenarios + policyDrills)
+ min(mockBest,80)/80 × 20
```

Empty denominators contribute 0 (a course with no drills does not punish the
learner). Rendered as an SVG ring, 0–100%.
