# Guided player fix round — 2026-10-08 (deployed 2026-10-09 ~00:10 UTC)

Fixes the 4 failures found by the live browser check (2026-10-08 ~20:05 EDT)
on https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery.

## Root causes

1. **No literal "Next →" label (issue 1):** `course-shell.js` repaint logic
   replaced the foot button's entire `textContent` with the gate reason
   ("⚠ Pass the mastery check (≥70%) to unlock next") when locked, so the
   literal "Next →" only existed in the unlocked state.

2. **Study tips card missing (issue 2):** `normCourse()` in `course-shell.js`
   whitelists course-JSON fields and did not include `tips` — so `COURSE.tips`
   was always `undefined` at runtime even though all 29 JSONs carry 6 tips.
   The Brief-tab render code was correct; the data was stripped before it.

3. **Legend dialog empty (issue 3):** same `normCourse()` whitelist dropped
   `legends` — `wireLegend()` reads `COURSE.legends` lazily at open time, so
   fixing the whitelist fixes the dialog with no other change.

4. **Resume banner vanished after reload (issue 4, most important):** tabs are
   lazily built — `showTab()` runs `BUILDERS.brief` (which does
   `root.innerHTML = html`, wiping the injected banner) the first time the
   Brief tab is shown, but the "Continue where you left off" injection lived
   only in `refreshILProgress()`, which `showTab('brief')` never called.
   Sequence: first load on `#/brief` → banner injected after build ✓; reload
   lands on `#/study` → banner injected into the un-built (empty) brief pane;
   user clicks Brief → `buildBrief` wipes it → no re-injection → banner gone.

## Changes (commit c5e6a3c + deploy markers e7406a4)

- `docs/university/course-shell.js`
  - `normCourse()`: added `tips: d.tips || []`, `legends: d.legends || {}`.
  - Locked-state Next button keeps literal label:
    `Next → <span class="ilgd-next__r">⚠ Pass the mastery check (≥70%) to unlock</span>`
    / `Next → <span class="ilgd-next__r">🔒 Complete this module to unlock</span>`.
  - `showTab()`: when `id === 'brief'`, call `refreshILProgress()` after the
    build step so the resume banner is re-injected after every rebuild/switch.
    (Guarded: `refreshILProgress` no-ops when COURSE/ILProgress are missing;
    boot sets COURSE before `route()`.)
- `docs/university/course-shell.css`: `.ilgd-next__r` styling for the
  locked-state reason line; dark-mode safe; reduced-motion untouched.

`node --check` clean on course-shell.js, il-progress.js, il-guided.js.

## Deploy

- Worker: `solitary-sound-015a`, etag `ea23447961dd`
  (modified 2026-10-09T00:10:47Z).
- Config rebuilt from live worker settings + `_worker.js` route surface:
  `.work/flagship-deploy-config-20261008.json` (the sibling's 20261007 config
  was not on disk). 39 exact `run_worker_first` paths covering every route
  `fetch()` handles: 12 redirect paths, 24 API paths, `/university/course`
  + `/university/course.html`, plus `*.json` wildcards for course/story JSONs.
- Deploy friction worth knowing:
  - API rejects `run_worker_first` rules ≥ 100 chars → per-file story-JSON
    paths replaced with `/university/data/courses/stories/*.json` (+ course
    `*.json`) wildcards; verified live that gating still works.
  - API rejects `secret_text` bindings without a value → ENTITLEMENT_SECRET /
    SESSION_SECRET omitted from upload metadata; verified post-deploy that
    both secrets are intact on the worker (all 8 bindings present).
  - The deploy tool needs a non-empty upload bucket to mint the completion
    JWT; two no-op runs were forced with a CSS marker comment.

## Live verification (curl, 2026-10-09 ~00:12 UTC)

- New `course-shell.js` served (`ilgd-next__r` ×2, `tips: d.tips` present).
- Paywall intact: IL-01 JSON → 402, IL-29 JSON → 200,
  IL-01 story JSON → 402 (wildcard run_worker_first works).
- Worker routes intact: `/os` → 301, `/il26` → 301, `/api/me` → 401
  (worker-handled), course page → 200.

## Per-issue confirmation

1. Literal "Next →" label now present in locked and unlocked states (code +
   CSS live; interactive click-through needs a browser pass).
2. `COURSE.tips` now survives normalization → Brief-tab "Study tips" card
   renders (data verified in JSON; DOM render needs a browser pass).
3. `COURSE.legends` now survives normalization → Legend dialog shows the
   13 entries (data verified; dialog content needs a browser pass).
4. Resume banner: root cause fixed in code and deployed — `showTab('brief')`
   now re-injects after every build. The exact failing sequence (answer quiz
   → reload on Study → open Brief) needs a browser pass to confirm visually.

## Still needs a browser pass (subagent has no live browser)

Re-run the 4 original checks on the IL-29 course URL: literal "Next →" in a
locked module foot, "Study tips" card on Brief, Legend dialog content,
and "Continue where you left off" surviving answer → reload → Brief.

## Preserved

Paywall gating (IL-01–IL-26 locked, IL-27/28/29 free), dark default,
"YOU ARE HERE" wayfinding, Noah integration, prefers-reduced-motion,
all 8 worker bindings incl. secrets, OG preview injection paths.
