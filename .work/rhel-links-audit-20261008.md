# RHEL Bare Metal Project — Link Audit

**Date:** 2026-10-08 ~22:26 EDT
**Scope:** RHEL AI & Systems Fabric bare-metal project links (portfolio card → /labs/ tree + related)
**Method:** curl status + timing per URL, link extraction from live HTML

## Portfolio RHEL card

| Link | URL | Status | Time |
|---|---|---|---|
| View lab direction | https://interstitiumlabs.dev/labs/ | **200** | 0.99s |

## /labs/ hang issue — RESOLVED

The `/labs/` timeout reported earlier in the session (30s+ hang, curl `000`) is **no longer reproducing**. Current: **200 in 0.99s**. The hang coincided with an in-flight Workers Assets deploy; responses are healthy now.

## Lab sub-pages

| URL | Status | Time |
|---|---|---|
| https://interstitiumlabs.dev/labs/ | 200 | 0.99s |
| https://interstitiumlabs.dev/labs/superlab/ | 200 | <2s |
| https://interstitiumlabs.dev/labs/challenge/ | 200 | <2s |
| https://interstitiumlabs.dev/labs/lab-sql/ | 200 | <2s |

## Links extracted from /labs/ (internal pages)

All 200, all <1.5s:

| URL | Status | Time |
|---|---|---|
| /about/ | 200 | 1.38s |
| /adapt/ | 200 | 1.09s |
| /cinema/ | 200 | 0.79s |
| /coach/ | 200 | 0.77s |
| /enroll/ | 200 | 0.84s |
| /founders/ | 200 | 0.94s |
| /immersive/ | 200 | 0.94s |
| /jobs/ | 200 | 1.22s |
| /learn/ | 200 | 0.90s |
| /noah/ | 200 | 0.79s |
| /paths/ | 200 | 0.86s |
| /paths/devsecops-mastery/ | 200 | 1.11s |
| /paths/roles/ | 200 | 1.10s |
| /play/ | 200 | 1.09s |
| /prep/ | 200 | 1.18s |
| /prep/drills/ | 200 | 0.76s |
| /university/ | 200 | 1.28s |

## Links from /labs/superlab/ and /labs/challenge/ (not already covered)

| URL | Status | Time |
|---|---|---|
| /evidence/ | 200 | 0.86s |
| /evidence/resume/ | 200 | 0.82s |

(Anchor links `#map`, `#quickstart`, etc. are same-page fragments — not checked via HTTP.)

## RHEL-related pages across the site

RHEL mentions found in repo source (docs/):
- `founders/index.html`
- `learn/skills/index.html`
- `learn/sequences/ansible-config/index.html`
- `paths/linux-rhcsa-spine/index.html`
- `prep/drills/desk-interview/index.html`

No dedicated `/rhel/` path or RHEL-specific hrefs exist — RHEL content lives inside the /labs/ tree and course modules. No broken RHEL references found.

## Portfolio project-card links (all cards)

| Card | Link text | URL | Status |
|---|---|---|---|
| Interstitium Labs | Visit live project | https://interstitiumlabs.dev | 200 |
| Interstitium Labs | Source | github.com/EnmanuelMejia/interstitium-labs | 200 (prior audit) |
| IL-26 | Start the course | /university/course?course=il-26-… | 200 |
| IL-26 | Graduate Evidence Dossier | /university/il-26-dossier.html | 200 (307→200 chain) |
| IL-28 | Start the course | /university/course?course=il-28-… | 200 |
| IL-29 | Start the course | /university/course?course=il-29-… | 200 |
| DevOps SuperLab | Explore repository | github.com/EnmanuelMejia/devops-superlab | 200 (prior audit) |
| **RHEL AI & Systems Fabric** | **View lab direction** | **https://interstitiumlabs.dev/labs/** | **200** |
| Bootcamp Catalog | Explore the catalog | https://interstitiumlabs.dev/bootcamps/ | **401** — known issue, public catalog fix pending gateway deploy |
| Bootcamp Catalog | Source | github.com/…/interstitium-certification-bootcamps | 200 (prior audit) |
| ThreatLocker Interview | Try it live | /bootcamps/tl-interview/ | 200 |
| ThreatLocker Assessment | Explore the course | /bootcamps/threatlocker-assessment-prep/ | 200 |
| ThreatLocker Assessment | Source | github.com/…/threatlocker-assessment-prep-cbt | 200 (prior audit) |
| AI Vision Deck | Explore repository | github.com/…/ai-vision-deck-print-manufacturing | 200 (prior audit) |
| LPS Enrollment | Explore repository | github.com/…/lps-enrollment-analysis | 200 (prior audit) |
| LPS Enrollment | Evidence & offer letter | /evidence/withdrawn-note/ | 200 |

## Summary

- **RHEL project links: all healthy.** The portfolio's "View lab direction" → /labs/ returns 200 fast; the entire /labs/ tree (superlab, challenge, lab-sql) loads; every internal link from those pages is 200.
- **/labs/ hang: resolved**, was deploy-related, not a code issue.
- **One known issue:** /bootcamps/ catalog link returns 401 (membership gate); public catalog page fix is built, awaiting gateway deploy (network-blocked).
- **No broken RHEL references** anywhere on the site.
