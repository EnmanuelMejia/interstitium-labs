# IL-28 — Audit Report (2026-10-09)

**OVERALL: PASS**

Course: il-28-devsecops-cloud-infrastructure-mastery · IL-28 · DevSecOps & Cloud Infrastructure — Production Mastery Bootcamp · 52 modules · updatedAt 2026-10-09


## Pre-fix findings (all fixed in this run)

- FIXED: schemaVersion int 4 -> string "4"

- FIXED: cross-link IL28-M44 -> IL-05 added

- FIXED: updatedAt -> 2026-10-09


## Checks

### 1. All v4 top-level keys present — **PASS**
Missing after fix: none. (Pre-fix missing: none.)

### 2. schemaVersion == "4" (string) — **PASS**
schemaVersion is now '4' (was 4 pre-fix). Site consumer (course-shell.js) uses `d.schemaVersion || "1.0"` — safe.

### 3. Hours = honest rounded sum of module estimatedMinutes — **PASS**
Declared 473; sum=28380 min = 473.00 h → rounded 473.

### 4. Every certGates entry carries independent-prep framing — **PASS**
All 6 gates carry independent-prep + non-affiliation framing. Note: IL-26/IL-27 gates use per-vendor wording ("Independent practice exam modeled on the publicly described format. Not affiliated with or endorsed by <vendor>.") instead of the canonical sentence — meaning identical, audit passes.

### 5. honestyNote present and names vendors — **PASS**
Present (472 chars); names vendors. Text: "This is an independent preparation and practice course aligned to publicly described exam topic maps and a real interview experience; it is not affiliated with,…"

### 6. Prereq math supplement exists (M00 or equivalent) — **PASS**
Math primer modules: IL-28-PM-LOGIC, IL-28-PM-NUMTH

### 7. MERGE-PLAN cross-links (il-05-cloud-devsecops-platform-sre) — **PASS**
All required pairs present: il-05-cloud-devsecops-platform-sre via IL28-M44→il05-devops-core.

### 9. No invented metrics/credentials/testimonials/braindumps; no Palantir/NSA claims — **PASS**
Standalone "NSA" hits: 0 (earlier substring hits were JSON artifacts like "n"+"sales"/"n"+"sample"). Palantir mentions are hiring-bar framing (user-authorized) + non-affiliation disclaimer list only; no affiliation or certification claim. "brain dump" appears once in an IL-27 flashcard titled "Brain dumps: why not" (anti-braindump guidance). "guarantee" hits are benign prose ("you can't guarantee"). No invented credentials, metrics, or testimonials found.

### 10. sourceLinks have retrieved dates — **PASS**
10 sourceLinks, all with retrieved dates.
