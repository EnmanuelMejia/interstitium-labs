# Guided-path scope fix — 2026-10-08 (~21:05 EDT)

User order: "nothing unrelated should be tied together as a guided path";
university header/menu must match the rest of the site. All three bugs fixed,
deployed, and curl-verified live. Commit `689167e`, deployed via
`deploy-worker-assets` (worker `solitary-sound-015a`, etag `ea23447961dd` —
worker bundle unchanged; 22 asset files uploaded).

## BUG 1 — Duplicate "Start your guided path" banner (user screenshot: two stacked on IL-29, mobile)
**Root cause:** stale `.ilprog-continue` nodes from pre-fix markup/bfcache survived
outside the current `#ilprog-continue-wrap`; the sig guard only compared against
the wrapper's dataset, so a stale duplicate was never removed.
**Fix:**
- `university/course-shell.js` `refreshILProgress()`: before injecting, removes
  ALL `.ilprog-continue` nodes document-wide via `querySelectorAll` (class-based,
  catches stale variants), then injects exactly one.
- `university/js/il-progress.js` `paintResume()`/`paintContinue()`: same stale-node
  sweep inside the target container before painting.
**Verified:** `course-shell.js` served live contains the `querySelectorAll('.ilprog-continue')` sweep.

## BUG 2 — Unrelated courses tied into one guided path
**Root cause:** `curriculum-sequence.json` was a flat 29-course chain IL-01→IL-29;
every "start" banner pushed IL-01 Esoteric Foundations — including on IL-29 ThreatLocker.
**Fix:**
- `curriculum-sequence.json`: every entry now has `track`; new top-level `tracks`
  map (10 tracks): foundations-esoteric (IL-01,21,22), math (IL-02,20),
  programming (IL-03,08,12,16,17), systems-infra (IL-04,27),
  cloud-devsecops (IL-05,19,28), security (IL-06,11,24,25,29),
  data (IL-07,26), interview-prep (IL-13,14,15,18), career (IL-09,10),
  frontier (IL-23, related: IL-22). All 29 covered.
- `il-progress.js` `startPathHTML(seq, courseId, opts)` is course-aware:
  "Start the {CODE} guided path" → that course's first module
  (`?course=<slug>&module=<firstModuleId>`), eyebrow "Begin this course's
  guided sequence". No course context → returns `''` (no banner). The old
  universal-IL-01-start is gone; repo-wide grep confirms no remnants.
- `il-progress.js`: new `relatedCourses(seq, courseId, limit)` (same track,
  excl. self; frontier cross-links IL-22) and `trackName()`; `nextEntry()`
  now resolves via track.
- `course-shell.js` next-up prompt: "Course complete — continue in {track name}"
  with up to 3 same-track course links (new `.ilprog-nextup__links` CSS).
- `academy.html`: banner is course-scoped via the academy's courseId; added a
  "Continue in {track}" rail (`#ilprog-track-group`) grouping the guided-path
  display by track with per-course progress — never the flat chain.
- `university/index.html` + `docs/index.html`: `paintResume` gains `onDone`;
  with no course context a fresh device shows NOTHING (continue banner only
  when progress exists).
**Verified (node, live sequence doc):** IL-29 start banner = "Start the IL-29
guided path", zero IL-01 text, URL deep-links IL-29's first module (IL29-M01 —
all 29 first-module ids cross-checked against course JSONs); no-context start
= empty; IL-29 related = IL-06, IL-11, IL-24; IL-23 → IL-22.

## BUG 3 — University header/menu inconsistent
**Root cause:** university pages rendered a bespoke `.site-header` via
`university/js/app.js`; the main site uses the floating `.il-pillnav`.
**Fix:**
- New `university/css/il-pillnav.css`: pillnav rules extracted verbatim from
  `assets/il-unified.css` §3 + §6 buttons; theme vars scoped to `.il-pillnav`
  (never `:root`, so page themes are untouched); dark default, light opt-in;
  clearance `body:has(.il-pillnav):not(.il-home){padding-top:6rem}`;
  course-shell adaptations (sticky shell-header offsets to `top:4.75rem`,
  sidebar nav offset, legend dialog drops below the pill);
  `prefers-reduced-motion` respected.
- `university/js/app.js` `renderHeader()` now emits the identical pillnav
  markup: same brand lockup (sigil-glyph.svg + Interstitium Labs / SCIENTIA
  OMNIA VINCIT), same 14-link set + Enroll gold button, absolute URLs,
  `aria-current="page"` on University, zero-JS `<details>` mobile menu —
  same collapse behavior as the main site. `il-theme.js` injects its toggle
  into `.il-pillnav__row` automatically.
- `university/course.html`: static pillnav markup added (same links);
  shell-header with Legend button + course-code badge kept below the pill.
- All 12 app.js-driven university pages link `il-pillnav.css`.
**Verified live:** `/university/course?course=il-29…` (200) serves the pillnav;
`academy.html`, `university/index.html`, `docs/index.html` all serve it;
`il-pillnav.css` → 200; paywall intact (IL-01 JSON → 402, IL-29 → 200).

## Preserved
Paywall gating, dark default, "YOU ARE HERE" wayfinding, Noah, tips/legends/
Next buttons, reduced-motion. `node --check` clean on all JS changed.

## Remaining step for the parent (needs a live browser — subagents have none)
Mobile-viewport check of the IL-29 course page: exactly ONE start banner reading
"Start the IL-29 guided path" (fresh state), pill nav present and collapsing to
the MENU dropdown, no IL-01 anywhere on the page, shell-header Legend + IL-29
badge intact below the pill.
