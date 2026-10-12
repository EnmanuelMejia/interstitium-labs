# Codebase audit — apex-audit (2026-10-08)

Scope: commit history, bugs, performance, dead code in `~/workspace/apex-audit`.
Sibling-owned files (`docs/university/data/courses/*.json`, `docs/payment-routes.js`,
`docs/_worker.js`, `docs/university/academy.html`) were reviewed but NOT edited —
findings there live in `.work/codebase-findings-owned-files.md`.
No deploys performed. No href/src/action URL values changed.

## 1. Commit history (289 commits reviewed)

- `git log --oneline` full review: no reverts, no WIP/draft commits, no
  broken-commit markers. History is content-buildout heavy (course JSONs,
  IL-12..IL-29 builds) plus deploy/worker fixes. Notable corrective commits
  are healthy: `fac9c30` (truncated-write artifact), `d361419` (doubled
  figure wrappers), `904943a` (competitor-name purge + syntax fix),
  `a48c76b` (ASSETS binding 500 fix), `34898c2` (bundled worker entry).
- `grep -rn "TODO\|FIXME\|HACK"` over `course-shell.js`, `il26-shell-*.js`,
  `_worker.js`, `payment-routes.js`: zero hits.
- Uncommitted changes reviewed individually (8 modified files):
  - `docs/_redirects` — /il26–/il28 short slugs (inert in API path; see
    owned-findings for the missing /il29 line).
  - `docs/_worker.js` / `docs/_worker.bundle.js` — OG edge injection +
    short-slug 301s (owned; reviewed only, bundle passes `node --check`).
  - `docs/labs/superlab/index.html` — og:image → versioned course OG PNG. Clean.
  - `docs/university/course.html` — head comment only. Clean.
  - `docs/university/COURSE-SCHEMA.md` — schema docs for IL-26 keys; matches
    the renderers. Clean.
  - `docs/university/academy.html` — IL-26..29 slug map (owned; reviewed only).
  - `docs/university/course-shell.js` — +3243 lines: IL-26/IL-27 renderers.
    This is where all the bugs below were found and fixed.

## 2. Bugs found and fixed (docs/university/course-shell.js)

### F1 — CRITICAL: stage-gate listener swallowed every stage-completion click
The IL-26 "Mark module complete" gate used a capture-phase listener matching
`e.target.closest('.btn-row .btn')` — which also matches the "Mark watched",
"Mark lab complete", "Mark tool lab complete", and "Run query" buttons. With any
stage incomplete (always true before the first completion), `stopPropagation()`
+ `preventDefault()` killed those clicks, so **no IL-26 stage could ever be
completed**. Fix: the module-complete button now carries
`data-mod-complete="1"` (set in base `moduleHTML`, line ~608) and the gate
matches `[data-mod-complete]` only (line ~3053). Verified the drill/mock `.opt`
buttons were never affected by this selector, which is why only the stage
buttons were bricked.

### F2 — CRITICAL: wrong drill answer permanently bricked the drill stage
`il26_renderModuleDrills` stored `String(ci)` on ANY click and disabled all
options, while `il26_stageDone` requires the stored value to equal the correct
answer. One wrong pick = drill/lab/mock stages locked forever, no retry.
Fix: wrong picks only flag the button and allow retry (nothing persisted);
correct picks persist. Also heals legacy wrong values already in users'
localStorage (clears them so the drill becomes retryable).

### F3 — CRITICAL: mock-task stage could never complete
`il26_renderMockTask` stored the raw picked index (`String(ci)`), but both
`il26_stageDone` and `il26_objectiveStats` check `=== '1'`. The mock stage was
unfinishable (except by luck picking index 1), and a wrong pick locked it with
no retry. Fix: store `'1'` only on a correct answer, allow retry on wrong,
heal legacy non-`'1'` values.

### F4 — Stage pills/locks went stale until page reload
Only note-toggles called `il26_refreshStages`; video/drill/mock/lab completions
did not, so the stage tracker bar and section locks never updated live. Fix:
new `il26_rebuildStagesNear(node)` helper walks up to the module wrap's
`_il26_rebuildStages`; called from the video "Mark watched", hands-on-lab,
tool-lab, drill-correct, and mock-correct handlers. No-ops safely outside
module stage hosts (Labs tab, IL-27).

### F5 — Unhandled rejection when DuckDB `connect()` rejects
The inner query chain had `.catch`, but `db.connect()` itself did not — a
connect failure produced an unhandled promise rejection. Added a `.catch`
rendering a "Database connection error" message.

### F6 — Interview-countdown interval never cleared
`il27BuildFastTrack`'s `tick()` returned early when the host detached but left
`setInterval` running forever (waking every second). Now clears the interval
and nulls `il27CdTimer` when the host is gone.

### F7 — Crosswalk gate double-start leaked interval
Starting a second cert gate without closing the first orphaned the old
`setInterval`. Now clears any existing `XW_RUN.timerId` before starting.

### F8 — Unescaped data in innerHTML (XSS hygiene)
`pg.dataset.columns.join(', ')` and `v.durationMin` were interpolated into
`innerHTML` without `esc()`. Both are author-controlled course-JSON data
(low risk), but now escaped for consistency with every other field.

### Verification
- `node --check docs/university/course-shell.js` — passes.
- Extracted the real `il26_stageList` / `il26_stageDone` / `il26_moduleToolLabs` /
  `il26_installDone` / `il26_toolLabUnlocked` from the edited file and ran a
  9-assertion contract test (fresh/progressed/legacy states for video, drill,
  lab, mock): ALL PASS.
- XSS sweep: `esc()` covers `&<>"`; no `onerror=`/`onload=`/`javascript:` in the
  shell; all course-data interpolations escaped after F8 (two fixed).
- Recent renderer fixes confirmed still holding: object-step click-sims render
  (`il26_renderClickSim`), drills/labs/videos/mock-tasks/supplemental resources
  render on module pages for IL-26 (stage-gated) and IL-27 (full sections).

## 3. Performance

- **Bundles:** `course-shell.js` 215 KB (served unminified to every course page;
  ~40% shrink available via minification — no build step exists; recommended,
  not applied), `_worker.bundle.js` 77 KB (valid syntax).
- **Worker cold path:** base `_worker.js` is header/redirect logic + ASSETS
  fallthrough — lean. `serveCourseWithOg` adds a full-HTML rewrite per course
  page hit with no cache (flagged for sibling in owned-findings).
- **OG images** (`docs/university/og/`, all referenced, originals backed up to
  `.work/og-backups/`):
  - `devops-superlab-og.png`: 2192x1152, 1927 KB → **1200x630, 784 KB**
  - `lps-enrollment-og.png`: 2240x1120, 1203 KB → **1200x630, 546 KB**
  - `sundance-ai-og.png`: 2240x1120, 1397 KB → **1200x630, 626 KB**
  - `il-26-data-analyst-og.png`: 1200x630, 701 KB (recompressed, photographic)
  - `il-27-it-infrastructure-og.png`: 1200x630, 782 KB (recompressed)
  - `il-29-threatlocker-og.png`: 1200x630, 839 KB (recompressed)
  - `il-28-devsecops-og.png`: 1200x630, 96 KB → 84 KB
  - All 7 decode cleanly at 1200x630 (verified via PIL). Photographic PNGs
    remain 700–840 KB (lossless floor; JPEG conversion would change URL
    extensions — owned by sibling, not done).
  - `media-generation-*.json` + `media-generation-last-upload-handles.json`
    in `og/` are media-pipeline bookkeeping with no code references — left in
    place (pipeline may re-read them); flagged as public-tree junk candidates.
- **Render:** stage rebuilds (`buildStages`) re-render the module's stage
  sections on completion — bounded, per-module. Countdown/gate intervals now
  self-clear (F6/F7). No unthrottled scroll/resize listeners found.

## 4. Dead code removed

- **Deleted `docs/university/il26-shell-{a,b,c,d,e}.js`** (untracked, ~81 KB
  total): the IL-26 renderers were merged into `course-shell.js` and all 42
  functions verified present there; zero references repo-wide. Note:
  `docs/university/data/courses/_il26-build/assemble_shell.py` (one-shot build
  script) listed these files as inputs — it already ran; with the parts gone it
  now fails fast on `open()` instead of its real hazard (re-running it would
  have DUPLICATED the merged block into `course-shell.js` and shadowed the
  fixes above).
- `docs/worker.js` (4 KB legacy worker entry): superseded by
  `_worker.bundle.js` (deploy config names the bundle); kept, not deleted —
  deploy-adjacent, flagged for sibling to retire.
- No duplicate vendored libraries found (single hashed React asset).

## 5. Not done / needs a sibling or the user

- Owned-file findings → `.work/codebase-findings-owned-files.md` (2 items:
  missing `/il29` in `_redirects`; uncached OG injection per request).
- `course-shell.js` minification (no build step exists).
- Browser-verified click-through of the IL-26 stage flow (logic unit-tested,
  not live-browser tested — generic subagents cannot drive the browser).
- `docs/worker.js` retirement; `og/media-generation-*.json` junk removal.
