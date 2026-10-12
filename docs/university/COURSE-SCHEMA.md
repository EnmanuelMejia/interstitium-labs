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
| `glossary` | `{term,definition}[]` | no | More tab: course glossary (student resources) |
| `faq` | `{q,a}[]` | no | More tab: student FAQ (student resources) |
| `honestyNote` | string | no | Rendered in More; e.g. "confers no certificate" |
| `crosswalk` | `{cert,trackModule,framing,moduleSequence,readinessChecklist,domains[]}[]` | no | Crosswalk tab: earn-readiness mapping per certification. `domains[]` = `{domain,weight?,modules[],coverage, practice?, note?}` |
| `certGates` | `{id,cert,trackModule,framing,format,minutes,questionCount,domainWeights[],readinessRule,questions[]}[]` | no | Crosswalk tab: timed practice-exam gates. `questions[]` = `{q,choices[],answer,explain,domain}` |
| `readinessDashboard` | `{title,framing,concept,formula,thresholds,statusLabels,howToUse[],certs[]}` | no | Crosswalk tab: live readiness % per cert (60% modules + 40% gate best) |
| `studyGuide` | `{title,totalHours,totalMinutes,pacing,whenStuck,examOrder,timeFormula}` | no | IL-26: rendered as the course's first Study section. `pacing` = `{dailyMinutes,daysPerWeek,estimatedWeeks,plan[],note}`; `whenStuck` = `{title,steps[]}` (re-check → drills → videos → cross-links); `examOrder` = `{title,thresholds{ready,nearlyReady},rule,order[{gateId,cert,why}]}`; `timeFormula` documents the per-module minute formula. |
| `toolLabs` | `{id,title,chain,moduleId,requiresInstall[],requiresLab,brief,steps[],deliverable,checkpoint,datasetRef}[]` | no | IL-26 Labs pane. `requiresInstall[]` gates the lab on install-lab checkpoints. Progress: `toollab:<id>:done`. |
| `installLabs` | `{id,tool,category,moduleId,estimatedMinutes,gates[],platforms{windows,macos,linux},checkpoints[{command,expected}],troubleshoot[],costNote}[]` | no | IL-26 Labs pane. Progress: `install:<id>:cp:<i>`, derived `install:<id>:done`. |
| `installPrereqOrder` | `string[]` | no | IL-26: install sequence order (ids into `installLabs`). |
| `installSteps` | `{id,title,summary,commands[]}[]` | no | IL-26: condensed install quick-steps companion to `installLabs`. |
| `multicloudLabs` | `{id,title,cloud,brief,steps[],workload,costGuardrails,cleanup,checkpoint}[]` | no | IL-26 Labs pane. |
| `sampleDatasets` | `{name,format,columns[],rows[][],note?}[]` | no | IL-26 Labs pane; also feeds SQL playground tables. |
| `sqlPlaygrounds` | `{id,moduleId,title,dataset,tasks[{prompt,starterSQL,solutionSQL,expectedRows?,hint?}]}[]` | no | IL-26 Labs pane. Runs DuckDB-WASM from CDN; graceful fallback to static solution display. Progress: `sqlpg:<id>:<ti>`. |
| `pythonExercises` | `{id,moduleId,title,tasks[{prompt,starterCode,solutionCode,checks[{description,test}]}]}[]` | no | IL-26 Labs pane. Runs Pyodide from CDN; graceful fallback to static check display. Progress: `pyex:<id>:<ti>`. |
| `daxPlaygrounds` | `{id,moduleId,title,tasks[{prompt,table?,expectedDAX,accept[],explain?}]}[]` | no | IL-26 Labs pane. Local grading: whitespace/case normalized, matched against accept list. Progress: `dax:<id>:<ti>`. |
| `terminalSims` | `TerminalSim[]` (two shapes) | no | Labs tab (Terminal sub-tab). Canned shape `{id,title,brief,prompt?,commands[{cmd,out}]}` (existing renderer); graded shape `{id,moduleId,title,scenario,gradedCommands[{command ("a|b" variants),response,hint}]}` (IL-26 renderer: hint after 2 failures). Progress: `gterm:<id>:<i>`, `gterm:<id>:done`. |
| `branchingScenarios` | `{id,moduleId,title,start,nodes{<id>:{text,choices[{label,next?,feedback?}]}}}[]` | no | IL-26 Labs pane. Progress: `branch:<id>:done`. |
| `clickSims` | `{id,moduleId,tool,title,steps[{screen,instruction,hotspots[],feedback}]}[]` | no | IL-26 Labs pane: mock UI screens with hotspots. Progress: `clicksim:<id>:<i>`, `clicksim:<id>:done`. |
| `interactivityAudit` | `{moduleId,elementCount,elements[{id,type}],gatePass}[]` | no | IL-26: per-module interactive-element audit; gate requires `elementCount >= 2`. |
| `employerMappings` | `{objective,moduleId,certification,certDomain,employer,competency,evidence}[]` | no | IL-26 Crosswalk tab: 3-column view (competency | course evidence | cert domain), grouped by employer. Independent mapping; no employer affiliation. |
| `jdMatrix` | `{postingTitle,postingUrl,employer,urlStatus,requirement,modules,certDomain,portfolioArtifact}[]` | no | IL-26 Crosswalk tab: job-posting requirement matrix. |
| `employerCompetencies` | `…[]` | no | IL-26: competency definitions backing `employerMappings` (from crosswalk-v2 framing). |
| `dossierUrl` | string | no | IL-26: relative URL of the graduate evidence dossier (HTML; PDF alongside). Rendered in Crosswalk tab. |

## Module

`{ id, code, title, weight?, summary, objectives?, notes[], cards[], quiz[] }`

- `weight` (number, default `1`): readiness uses a **weighted** module fraction.
- `notes[]`: `{ title, body, code?, lang? }` — collapsible; `body` is markdown-lite
  (see below); `code` renders in a `<pre>` block.
- `cards[]`: `{ front, back }` — tap-to-flip flashcards with a pager and
  know/again rating.
- `quiz[]`: `{ q, choices[], answer (0-based index), explain }` — MC quick-check
  with why-explanations.
- `videos[]` (IL-26): `{ title, url, source?, durationMin?, order?, watchBefore?, blurb?, verifiedUtc?, httpStatus? }`
  — third-party videos are linked, not hosted. `watchBefore` ∈ `notes|drill|lab`.
- `drills[]` (IL-26): `{ id, title, items[{q,choices[],answer,explain}] }` —
  drill quick-checks with instant why-explanations. Progress: `drill:<mid>:<di>:<ii>`.
- `handsOnLab` (IL-26): `{ id, title, brief, steps[], deliverable, checkpoint }`.
  Progress: `labdone:<mid>`.
- `mockTask` (IL-26): `{ id, type:"choice", q, choices[], answer, explain }`.
  Progress: `mocktask:<mid>`.
- `crossLinks[]` (IL-26): intra-course module-id strings, `IL26-TL-*` tool-lab
  ids, or cross-catalog `{course,moduleId,topic,why}` objects.
- `prerequisiteFor[]`: module ids this module is a prerequisite for.
- `prerequisiteForLabs[]` (IL-26): tool-lab ids this module is a prerequisite for.
- `estimatedMinutes` (IL-26): honest per-module estimate; course `hours` is the
  rounded sum.

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

IL-26 extension keys (same `ilc:<courseId>:` prefix):

| Key | Value | Set by |
|---|---|---|
| `video:<mid>:<i>` | `"1"` | Module videos watched |
| `note:<mid>:<i>` | `"1"` | Notes expanded (reading stage) |
| `drill:<mid>:<di>:<ii>` | chosen index | Module drill items |
| `labdone:<mid>` | `"1"` | Hands-on lab marked complete |
| `mocktask:<mid>` | chosen index | Module mock task |
| `install:<id>:cp:<i>` | `"1"` | Install-lab verification checkpoints |
| `install:<id>:done` | `"1"` | Derived when all checkpoints ticked |
| `toollab:<id>:done` | `"1"` | Tool lab marked complete (requiresInstall-gated) |
| `sqlpg:<id>:<ti>` | `"1"` | SQL playground task (row count matched) |
| `pyex:<id>:<ti>` | `"1"` | Python exercise (all checks passed) |
| `dax:<id>:<ti>` | `"1"` | DAX measure accepted |
| `gterm:<id>:<i>` / `gterm:<id>:done` | `"1"` | Graded terminal sim steps |
| `branch:<id>:done` | `"1"` | Branching scenario completed |
| `clicksim:<id>:<i>` / `clicksim:<id>:done` | `"1"` | Click-through sim steps |
| `mathlab:check:<mid>` | `"1"`/`"0"` | Adaptive math lab knowledge check |
| `mathlab:mastery:<mid>` | 0–100 | Adaptive math lab topic mastery |
| `mathlab:level:<mid>` | 1–3 | Adaptive math lab difficulty level |
| `mathlab:streak:<mid>` | number | Consecutive correct (level-up at 3) |
| `mathlab:last:<mid>` | epoch ms | Last practice (14-day decay re-check) |

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
