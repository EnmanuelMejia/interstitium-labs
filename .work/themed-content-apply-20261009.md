# Themed-Content Apply — 2026-10-09

Part of the sitewide themed-content rollout (user order 2026-10-09). This workstream mapped every course and bootcamp to one of the 12 topic themes and applied `topicTheme` / `data-topic-theme` so the CSS theme system (`docs/assets/il-topic-themes.css`, built in parallel) activates. All original work.

## 1. Course JSONs — 29/29 themed ✅

- Script: `.work/apply_course_themes.py` (explicit per-course map, no guessing)
- Backups: `.work/course-json-backups-themes/` (29 files, pre-edit copies)
- Added top-level `"topicTheme"` + `"topic"` to each `docs/university/data/courses/il-*.json`; every file re-validated with `json.load` after edit.

| Theme | Courses |
|---|---|
| mr-robot | 7 (IL-06, 09, 11, 24, 25, 27, 29) |
| sacredgeo | 5 (IL-01, 02, 20, 21, 22) |
| steampunk | 4 (IL-05, 14, 19, 28) |
| exmachina | 4 (IL-12, 16, 17, 23) |
| oceandeep | 3 (IL-07, 15, 26) |
| hackers95 | 3 (IL-03, 08, 13) |
| industrial | 1 (IL-04) |
| vaporwave | 1 (IL-10) |
| cyberpunk | 1 (IL-18) |
| tron / alexandria / goldrush | 0 (covered by bootcamps) |

Judgment calls (documented): IL-01/21/22 (esoteric/humanities) → sacredgeo (closest theme; topic mirrors the theme's canonical topic); IL-09 (cert command deck) → mr-robot; IL-10 (portfolio/career) → vaporwave; IL-18 (tech leadership) → cyberpunk; IL-23 (frontier research) → exmachina.

## 2. Bootcamp content.jsons — 135/135 themed ✅

- Script: `.work/apply_bootcamp_themes.py` (explicit per-bootcamp map; keyword fallback never fired, 0 unmapped)
- Backups: `.work/bootcamp-json-backups-themes/` (135 files, pre-edit copies)
- Added top-level `"topicTheme"` + `"topic"` to each `cert-bootcamps/site/bootcamps/*/content.json`; every file re-validated with `json.load`.

| Theme | Count | Theme | Count |
|---|---|---|---|
| mr-robot | 28 | steampunk | 28 |
| exmachina | 17 | sacredgeo | 17 |
| hackers95 | 12 | industrial | 10 |
| vaporwave | 10 | oceandeep | 5 |
| alexandria | 4 | tron | 3 |
| goldrush | 1 | cyberpunk | 0 |

All 12 themes are covered across courses + bootcamps combined.

## 3. Card templates — `data-topic-theme` applied ✅

Approach per template (JSON-field read preferred; JS-side map where the JSON isn't in scope):

- **`docs/university/js/app.js`** — added `TOPIC_THEME_BY_CODE` (IL-01…IL-29 → theme) + `IL.topicThemeForCode(code)` helper. Single source of truth for JS-side lookups.
- **`docs/university/index.html`** — linked `../assets/il-topic-themes.css`; `academyCard()` and `pathCard()` now set `data-topic-theme` via `IL.topicThemeForCode` (path cards use `p.academy`).
- **`docs/university/academy.html`** — linked `../assets/il-topic-themes.css`; academy path cards set `data-topic-theme` from `a.code`; related-course `ilprog-track-card`s set it from `rel[ri].code`.
- **`docs/university/course-shell.js`** — `normCourse()` whitelists `topicTheme`/`topic` (previously dropped); `boot()` sets `document.body[data-topic-theme]` from the fetched course JSON. `node --check` clean.
- **`cert-bootcamps/generator/build.py`** — `hub_card()` takes a `theme` param and emits `data-topic-theme`; `render_hub()` resolves it from `content.json`'s `topicTheme` with a slug-keyword fallback for contentless entries. `py_compile` clean. Future regens keep the attribute.
- **`cert-bootcamps/site/bootcamps/index.html`** — all **75/75** static hub cards carry `data-topic-theme` (script: `.work/patch_hub_cards.py`, idempotent; source of truth = content.json).
  - **Incident + repair (documented):** the first patch run inserted the attribute after the wrong quote (the match regex had already consumed the href closing quote), corrupting all 75 cards' `data-group` attributes (`data-group=" data-topic-theme="x"languages"` — would have broken hub group filtering). Caught on spot-check; repaired with `.work/repair_hub_cards.py` (75/75 repaired, 0 theme mismatches vs content.json, tag shape validated). Redeployed as cert-bootcamps v2026-10-09T06:45:17Z.
- **`cert-bootcamps/site/bootcamps/_engine/bootcamp.js`** (+ mirrored `engine/bootcamp.js`) — `ingest()` sets `document.body[data-topic-theme]` from `content.json`. `node --check` clean.
- `learn.js` lesson/lab cards: deliberately NOT individually tagged — the body-level attribute covers them via the CSS's `[data-topic-theme] .th-card` descendant selectors (documented decision, minimal churn).
- Dark mode preserved: themes are accent layers over the existing dark base per the CSS spec; no base colors touched.

## 4. PDF covers — theme support added, 2 samples regenerated ✅

- **`.work/pdf-buildout/il_cinematic_pdf.py`** — added `TOPIC_THEME_COLORS` (12 themes, accents matching `il-topic-themes.css`: e.g. mr-robot `#00ff41`/`#008f11`, oceandeep `#39ffce`/`#1b6f8f`), `_shade()` dimmer, `theme_palette()`; `cinematic_cover(..., theme=None)` recolors brackets/header/hex badge/eyebrow/walkthrough badge + stamps a `THEME · <KEY>` tag. `theme=None` keeps the default cyan/orange (all 16 existing gen scripts unaffected).
- **`.work/pdf-buildout/bbg_style.py`** — `title_page(..., theme=None)` passes through to the cinematic cover.
- Regenerated (backups in `.work/pdf-buildout/output-backups-themes/`):
  - `output/bbg-zero-trust.pdf` — theme **mr-robot**, 8 pages, 17,487 bytes
  - `output/bbg-etl-pipelines.pdf` — theme **oceandeep**, 8 pages, 17,970 bytes
- Verified: theme tag text present in both; primary accent colors confirmed in the page-1 content stream (fill + stroke operators) for both.
- **Future work:** full regeneration of all 241 PDFs with per-guide themes (not done here, per brief).

## 5. Deploys

- **Flagship** `solitary-sound-015a`: `deployed etag=95acb862e03f modified=2026-10-09T06:33:49Z` — 26 files uploaded. (A sibling cinematic-assets deploy ran at ~06:39 from the same tree; tree includes this workstream's changes.)
- **Cert-bootcamps** worker: first attempt no-op'd (0 buckets — sibling v39 at 06:35:10Z had already uploaded the identical tree); added a canary file and redeployed → **v40 at 2026-10-09T06:40:23Z**, 1 file uploaded, API-confirmed. Canary removed locally afterwards (stays in v40's manifest as a benign 47-byte txt; drops on the next deploy). Hub-card repair redeployed → **v2026-10-09T06:45:17Z** (repaired index.html, 1 file uploaded).

## 6. Verification (curl, live)

- `https://interstitiumlabs.dev/university/` → 200, `il-topic-themes.css` linked, `topicThemeForCode` present ✅
- `https://interstitiumlabs.dev/university/academy.html?id=IL-06` → 200, stylesheet + helper present ✅
- `https://interstitiumlabs.dev/university/course-shell.js` → 200, `topicTheme` refs present ✅
- `https://interstitiumlabs.dev/university/data/courses/il-29-...json` → 200, `topicTheme: mr-robot`, `topic: cybersecurity` ✅ (paid JSONs correctly 402-gated)
- `https://interstitiumlabs.dev/assets/il-topic-themes.css` → 200 ✅
- `https://interstitiumlabs.dev/bootcamps/_engine/bootcamp.js` → 200, **byte-identical** to the themed local file (theme ingest code live) ✅
- Hub cards: 75/75 carry `data-topic-theme` in the deployed `index.html` (verified locally; the hub HTML path is 401-gated live — pre-existing platform access control, confirmed in sibling workstream notes) ✅
- Bootcamp `content.json` `topicTheme`: 401-gated live (pre-existing); verified in all 135 local files ✅

## Caveats / flags for the coordinator

1. **cert-bootcamps workers.dev anomaly:** `https://cert-bootcamps.t3ch49.workers.dev/bootcamps/*` returns 404 (`error code: 1042`) for every asset path; only `/robots.txt` 200s (1248-byte content-signals text not present in the local tree). The public surface `interstitiumlabs.dev/bootcamps/*` serves correctly (engine JS byte-identical). Multiple sibling deploys raced on this worker today (v32–v40); worth one clean re-deploy + workers.dev check when the rollout settles.
2. **Concurrent deploy race:** sibling workstreams deployed both workers during this task (flagship cinematic deploy ~06:39, cert-bootcamps v32–v39). All deploys source the same trees, so no content was clobbered, but version churn was high.
3. **401 gating:** `/bootcamps/*.html` and `/bootcamps/*/content.json` return 401 sign-in-required on all domains — pre-existing per sibling notes; themed cards/content verified via deployed files + the public JS surface instead.
4. **Full PDF regeneration** (241 guides) is future work — framework support is in place and proven by the 2 samples.
5. The bootcamp `_engine/il-topic-themes.css` copy already contains all 12 themes (matches flagship) — no sync needed.
