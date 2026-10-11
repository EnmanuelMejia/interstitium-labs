# IL-04 · Systems, Linux, Windows & Networks — v4 Audit

**Result: PASS** — 16/16 checks passed.
File: `docs/university/data/courses/il-04-systems-linux-windows-networks.json`
updatedAt: 2026-10-09 · schemaVersion: '4' · hours: 34 · modules: 6 · certGates: 4

## Checks
| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | schemaVersion == '4' (string) | PASS | '4' |
| 2 | hours == round(sum min / 60) | PASS | declared=34 sum=2070 -> 34 |
| 3 | declared hours match spec | PASS | 34 |
| 4 | module count matches spec | PASS | 6 |
| 5 | all v4 top-level keys present | PASS | missing=[] |
| 6 | all modules have all v4 keys | PASS | [] |
| 7 | expected certGates present | PASS | found=['gate-rhcsa', 'gate-rhce', 'gate-linux-plus', 'gate-network-plus'] |
| 8 | every certGate has exact independent-prep framing | PASS | [] |
| 9 | no invented metrics/credentials/testimonials/braindumps/Palantir-NSA | PASS | [] |
| 10 | honestyNote present, no-affiliation + confers-no-certificate | PASS | Preparation only: Interstitium Labs confers no certificate and is not affiliated |
| 11 | prereq math supplement modules exist | PASS | [] |
| 12 | all sourceLinks have retrieved dates | PASS | links=10 missing_dates=[] |
| 13 | all crossLinks resolve to real module ids | PASS | [] |
| 14 | updatedAt == "2026-10-09" | PASS | '2026-10-09' |
| 15 | interactivityAudit counts consistent | PASS | 11 |
| 16 | no paywall/price fields in JSON | PASS | [] |

## Notes
IL-04: Network+ (N10-009) gate + crosswalk + certifications entry ADDED per task; RHCSA/RHCE/Linux+ preserved; all framings normalized to the exact template string.
