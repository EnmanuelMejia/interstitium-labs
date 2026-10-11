# IL-26 — Audit Report (2026-10-09)

**OVERALL: PASS**

Course: il-26-data-analyst-certification-senior-mastery · IL-26 · Data Analyst Certification & Senior Mastery Bootcamp · 53 modules · updatedAt 2026-10-09


## Pre-fix findings (all fixed in this run)

- FIXED: schemaVersion int 4 -> string "4"

- FIXED: added timeFormula (canonical template formula)

- FIXED: blurb "96-hour" -> "414-hour" (stale copy; declared hours = 414)

- FIXED: tagline "certified senior" -> "senior-ready" (course confers no certificate)

- FIXED: cross-link IL26-M08 -> IL-07 added

- FIXED: updatedAt -> 2026-10-09

- FIXED: module-level: added prerequisiteFor=[] to 31 modules (variants prerequisites/prerequisiteForLabs retained)

- Pre-fix missing top-level keys: timeFormula


## Checks

### 1. All v4 top-level keys present — **PASS**
Missing after fix: none. (Pre-fix missing: ['timeFormula'].)

### 2. schemaVersion == "4" (string) — **PASS**
schemaVersion is now '4' (was 4 pre-fix). Site consumer (course-shell.js) uses `d.schemaVersion || "1.0"` — safe.

### 3. Hours = honest rounded sum of module estimatedMinutes — **PASS**
Declared 414; sum=24870 min = 414.50 h → rounded 414.

### 4. Every certGates entry carries independent-prep framing — **PASS**
All 7 gates carry independent-prep + non-affiliation framing. Note: IL-26/IL-27 gates use per-vendor wording ("Independent practice exam modeled on the publicly described format. Not affiliated with or endorsed by <vendor>.") instead of the canonical sentence — meaning identical, audit passes.

### 5. honestyNote present and names vendors — **PASS**
Present (1128 chars); names vendors. Text: "This is an independent preparation and practice course aligned to publicly described exam topic maps and hiring bars; it is not affiliated with, endorsed by, or…"

### 6. Prereq math supplement exists (M00 or equivalent) — **PASS**
Math primer modules: IL-26-PM-STATS, IL-26-PM-LINALG

### 7. MERGE-PLAN cross-links (il-07-data-engineering-analytics-ai) — **PASS**
All required pairs present: il-07-data-engineering-analytics-ai via IL26-M08→il07-data-schools, IL26-M06→il07-aws-data.

### 9. No invented metrics/credentials/testimonials/braindumps; no Palantir/NSA claims — **PASS**
Standalone "NSA" hits: 0 (earlier substring hits were JSON artifacts like "n"+"sales"/"n"+"sample"). Palantir mentions are hiring-bar framing (user-authorized) + non-affiliation disclaimer list only; no affiliation or certification claim. "brain dump" appears once in an IL-27 flashcard titled "Brain dumps: why not" (anti-braindump guidance). "guarantee" hits are benign prose ("you can't guarantee"). No invented credentials, metrics, or testimonials found.

### 10. sourceLinks have retrieved dates — **PASS**
14 sourceLinks, all with retrieved dates.
