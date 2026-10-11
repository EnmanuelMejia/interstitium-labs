# IL-25 — Build Audit

**Result: PASS** (16/16 checks passed)

## Checks
- [x] schemaVersion == 4 (int, IL-29 gold-standard pattern) — got 4
- [x] updatedAt == "2026-10-09" — got '2026-10-09'
- [x] hours == honest rounded sum — hours=111, sum=6660min -> 111
- [x] all required top-level keys present — missing: []
- [x] all modules carry required v4 keys — 0 modules missing keys: []
- [x] every certGates entry carries independent-prep framing — 3 gates, bad framing: []
- [x] no braindump/testimonial/guaranteed-pass language — scan clean
- [x] no Palantir/NSA certification claims — scan clean
- [x] honestyNote present + disaffiliation language — 734 chars
- [x] sourceLinks all carry retrieved/verified dates — 14 links, missing dates: []
- [x] noahTutoring present with 5 personas — 5 personas
- [x] noahTutoring: 5 natural voices + voice-first
- [x] noahTutoring: SM-2 adaptive
- [x] noahTutoring: course-aware grounding
- [x] noahTutoring: personas mapped to real module ids — all persona moduleIds resolve
- [x] IL-25 → IL-29 cross-links present — 22 IL-29 links

## Notes
- Existing content preserved; only missing v4 fields added (module crossLinks/prerequisiteFor, top-level sections).
- schemaVersion is integer 4 per the IL-26/27/28/29 gold-standard pattern (template said string; gold standard rules).
- Exam facts in pre-existing certGates (e.g., IL-19 SAA 65q/130min/720) are preserved vendor-published figures as of Oct 2026, stated via the course honestyNote; no new exam facts invented in this build.

## Post-build normalization (2026-10-09)
- schemaVersion normalized from integer 4 to string "4" per the canonical template (matches IL-26–IL-29 post-fix). JSON re-validated.

## Post-build remediation (2026-10-09)
- Title fixed: "Professional Certificate in Cybersecurity" -> "Professional Cybersecurity Certificate Prep" (was implying conferral).
- noahTutoring enriched to 13-key standard (tagline, concept, voiceFirst, bleedingEdge, houseRule, howToUse, modulePersonaMap added).
- schemaVersion normalized to string "4".
