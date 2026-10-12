# IL-27 — Audit Report (2026-10-09)

**OVERALL: PASS**

Course: il-27-it-infrastructure-specialist-threatlocker-mastery · IL-27 · IT Infrastructure Specialist — Zero Trust Infrastructure Maste · 56 modules · updatedAt 2026-10-09


## Pre-fix findings (all fixed in this run)

- FIXED: schemaVersion int 4 -> string "4"

- FIXED: added timeFormula (canonical template formula)

- FIXED: added multicloudLabs = [] (section not applicable; no content invented)

- FIXED: added sampleDatasets = [] (section not applicable; no content invented)

- FIXED: added installSteps = [] (section not applicable; no content invented)

- FIXED: added installPrereqOrder = [] (section not applicable; no content invented)

- FIXED: added employerMappings = [] (section not applicable; no content invented)

- FIXED: added sqlPlaygrounds = [] (section not applicable; no content invented)

- FIXED: added pythonExercises = [] (section not applicable; no content invented)

- FIXED: added daxPlaygrounds = [] (section not applicable; no content invented)

- FIXED: updatedAt -> 2026-10-09

- FIXED: module-level: added prerequisiteFor=[] and mockTask=null to 6 fast-track modules

- Pre-fix missing top-level keys: multicloudLabs, sampleDatasets, installSteps, installPrereqOrder, employerMappings, sqlPlaygrounds, pythonExercises, daxPlaygrounds, timeFormula


## Checks

### 1. All v4 top-level keys present — **PASS**
Missing after fix: none. (Pre-fix missing: ['multicloudLabs', 'sampleDatasets', 'installSteps', 'installPrereqOrder', 'employerMappings', 'sqlPlaygrounds', 'pythonExercises', 'daxPlaygrounds', 'timeFormula'].)

### 2. schemaVersion == "4" (string) — **PASS**
schemaVersion is now '4' (was 4 pre-fix). Site consumer (course-shell.js) uses `d.schemaVersion || "1.0"` — safe.

### 3. Hours = honest rounded sum of module estimatedMinutes — **PASS**
Declared 252; sum=15090 min = 251.50 h → rounded 252.

### 4. Every certGates entry carries independent-prep framing — **PASS**
All 5 gates carry independent-prep + non-affiliation framing. Note: IL-26/IL-27 gates use per-vendor wording ("Independent practice exam modeled on the publicly described format. Not affiliated with or endorsed by <vendor>.") instead of the canonical sentence — meaning identical, audit passes.

### 5. honestyNote present and names vendors — **PASS**
Present (373 chars); names vendors. Text: "Independent study material. Not affiliated with, endorsed by, sponsored by, or a partner of ThreatLocker or any other vendor mentioned. No certifications are co…"

### 6. Prereq math supplement exists (M00 or equivalent) — **PASS**
Math primer modules: IL-27-PM-DISCRETE, IL-27-PM-LOGIC

### 7. MERGE-PLAN cross-links (none required) — **PASS**
All required pairs present: .

### 9. No invented metrics/credentials/testimonials/braindumps; no Palantir/NSA claims — **PASS**
Standalone "NSA" hits: 0 (earlier substring hits were JSON artifacts like "n"+"sales"/"n"+"sample"). Palantir mentions are hiring-bar framing (user-authorized) + non-affiliation disclaimer list only; no affiliation or certification claim. "brain dump" appears once in an IL-27 flashcard titled "Brain dumps: why not" (anti-braindump guidance). "guarantee" hits are benign prose ("you can't guarantee"). No invented credentials, metrics, or testimonials found.

### 10. sourceLinks have retrieved dates — **PASS**
18 sourceLinks, all with retrieved dates.
