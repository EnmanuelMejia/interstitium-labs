# Guided Platform Build — 2026-10-08 (Rosetta Stone clone + Noah everywhere + KodeKloud 10X)

User order ~19:32 EDT: "Wire it all — make this website a total guided Rosetta Stone clone: multicloud AI courses guided patterns, but with Noah AI integrated all along throughout. Also clone KodeKloud and improve on their design patterns, UI, UX — everything 10X. We need to become the new standard."

## Workstream 1 — Story supplement player wiring (DONE)
- `docs/university/js/il-stories.js` (new): ILStories — lazy cached _index.json, per-course fetch, getStoryForModule, storyCardHTML (semantic aside, hook headline, narrative chunked ~140 words, Cast line, bridge), enhanceModule (prepends card as first child of .mod-body), buildRail, storyOfTheDay (FNV-1a deterministic), renderCatalogStories. Free-slug gating mirrored, fail-closed.
- `docs/university/css/il-stories.css` (new): multicloud dark theme, reduced-motion guard.
- course-shell.js: outermost moduleHTML wrapper calls ILStories.enhanceModule; buildBrief appends #il-stories-rail; window.__ilOpenModule deep-opens modules.
- course.html: includes css/js. index.html (university): #stories section (story of the day + 104-entry browser).
- _worker.js: slugFromCourseJsonPath maps stories/*.json → slug so gated-course story JSONs get 402-without-entitlement; _index.json stays public. Bundle rebuilt via .work/rebuild-worker-bundle.py.
- 21-assertion harness .work/il-stories-test.js: all pass.

## Workstream 2 — Guided learning engine (DONE)
- `docs/university/js/il-guided.js` (new): sequential unlock (N+1 locked until N passed = complete AND mastery), "● You are here" wayfinding rail, guided practice with progressive hints (from question's own distractors/explain), review loops (2–3 prompts from earlier modules, missed-first), mastery gates (≥70% quiz, sticky, best-score), re-attempt, no-quiz modules unlock on completion. Schema: localStorage "il-guided-v1".
- `docs/university/css/il-guided.css` (new).
- course-shell.js: Guided section, rail in Study tab, lock enforcement + deep-link redirect, mastery recompute, gate messaging. academy.html: "Guided mastery · X of Y" per course.
- 14-assertion suite + IL-27 real-data sanity: all pass. Locks are learning-flow only — paywall untouched.

## Workstream 3 — Noah AI throughout (DONE)
- `docs/university/js/il-noah-tutor.js` (new): IL.noahTutor — askAboutLesson (per-module "◈ Ask Noah about this lesson" with course/module/section context prefill), recordAnswer (drill+quiz hooks), struggle nudge (2 consecutive wrong → inline "Stuck? Noah can walk you through this", max 1/module/session, NEVER auto-sends — student presses send), discussStory (story cards via MutationObserver), onModuleComplete (Socratic check-in offer). Every call guarded on IL.noahAI; honesty line baked in.
- course.html: script include. 11-group harness: all pass.

## Workstream 4 — KodeKloud pattern research (DONE)
- `.work/kodekloud-pattern-brief-20261008.md`: public-pages-only research, patterns abstracted (no KodeKloud content reproduced). Top 8 prioritized: skill-mastery dashboard, explain-validations, always-on solutions, env-context headers, adaptive pathing, transcript-as-index, multicloud diff labs, repair queue.

## Workstream 5 — KodeKloud 10X implementation (DONE)
- `docs/university/js/il-mastery.js` (new): heat computation/render (green≥70/yellow≥40/red/gray), repair-queue extraction, cross-course exam-readiness.
- `docs/university/js/il-diagnostic.js` (new): test-out diagnostic (first unanswered question/module from real quizzes, ≥80% → markTestOut, "Noah cleared N modules").
- `docs/university/data/cert-index.json` (new): 101 certs → courses static index.
- academy.html: Mastery section (heatmap + per-cert readiness, honest "signal not guarantee" bands) + Repair queue section.
- Quiz: always-on explanations + "◈ Noah: compare my approach" (question + learner pick vs official answer).
- Lab context bars: "YOU ARE HERE · IL-XX · … · Simulated lab · no real infrastructure" on all lab/drill/mock panes.
- 21 + 18 Node assertions: all pass. Descoped: drill/mock-task explanation reveals unchanged; readiness is demonstrated-mastery only.

## Constraints honored
Paywall (IL-27/28/29 free, IL-01–26 gated at worker), dark-mode default, multicloud theme, hero animated untouched, footer standard, $249/$999 pricing, verified facts only.

## Deployment
(See below — filled at deploy time.)
