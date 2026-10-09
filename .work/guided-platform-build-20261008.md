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
- Committed: "Guided platform: story wiring + guided engine + Noah tutor + KodeKloud 10X (user order 2026-10-08)"
- Deployed: solitary-sound-015a, etag d72314b37c05, 2026-10-08T23:51:49Z (14 files uploaded)
- Live verification (curl, 2026-10-08 ~19:52 EDT): homepage 200; course page (IL-29) 200 with all 6 JS (il-progress/stories/guided/noah-tutor/mastery/diagnostic) + 2 CSS includes; academy 200 with Mastery + Repair queue sections; stories _index.json 200; IL-29 stories JSON 200 (free); IL-01 stories JSON 402 (gated ✓); IL-01 course JSON 402 / IL-29 course JSON 200 (paywall intact ✓). One transient 404 on il-guided.js immediately post-deploy resolved on retry (edge propagation).
- Note: no live-browser interactive test was possible (subagent constraint); DOM integration validated via node harnesses only. Recommend parent run a browser smoke test: Study tab → story card → answer quiz → compare button → repair queue → diagnostic → Noah nudge.

## Resume fix — "Continue where you left off" (2026-10-08 ~19:55 EDT, commit 8dba916)
- Smoke test found no explicit resume button (banner existed but CTA read "Resume").
- `university/js/il-progress.js`: default CTA is now literally "Continue where you left off"; added `startPathHTML()` ("Start your guided path" → IL-01, with hardcoded fallback) and unified `paintResume()` (progress → continue banner; fresh device → start variant).
- `university/course-shell.js`: Brief-tab injection uses paintResume semantics; re-render guard preserved.
- `university/academy.html`, `docs/index.html`, `university/index.html`: all switched to `paintResume`.
- `university/css/il-progress.css`: prominent hero-grade banner styling (gold glow button, green start variant), dark-safe, reduced-motion respected.
- "YOU ARE HERE" wayfinding untouched (additive only). Gating unchanged (resume into gated course hits paywall).
- Deployed solitary-sound-015a (etag d72314b37c05). Live verified: il-progress.js, academy.html, course-shell.js/css, course.html all serve new code.

## Tips + legends + Next buttons (2026-10-08 ~20:00 EDT, commit 88f4be6)
- `tips[]`: 6 per course × 29 courses = 174 tips, generated from each course's real data (cert names from certGates, math module titles, hours, lab presence). Study-strategy only — no invented exam specifics. Time tip fixed for large courses (10h/week framing).
- `legends{}`: 13-entry shared map per course (✓ Complete/Mastered/Tested out, ● You are here, → Up next, 🔒 Locked, ⚠ Mastery gate, Readiness ring, Noah, Continue, Next →, Mark complete, FREE/lock badge) — all verified against actual player UI strings.
- Player wiring: "Study tips" card in Brief tab (buildBrief); "Legend" button in player header → dialog popover with COURSE.legends (Esc closes); explicit "Next →" button in every module foot — advances via goToModule() honoring guided lock (disabled with reason when locked: mastery-gate ≥70% or complete-module requirement); hidden on last module; repainted in Guided.refresh().
- CSS: .legend-btn/.legend-dlg/.ilgd-next-btn in course-shell.css, dark-safe, reduced-motion respected.
- node --check clean on both JS files. Deployed solitary-sound-015a. Live verified: tips+legends in served JSON (IL-29: 6/13), legend-btn in course.html, new JS/CSS served. Paywall intact (IL-01 JSON 402, IL-29 200).
- Interactive browser verification (button click-through, quiz→resume flow) not possible from subagent — recommend parent run a live browser task.
