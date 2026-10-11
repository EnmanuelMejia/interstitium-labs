# PDF Buildout — Animated Visual Guides (2026-10-09)

**User order:** "Insert embedded animated byte byte go pdf's sitewide and cross site wide throughout recursively" (2026-10-09 ~01:22 EDT)

## What Was Built

**18 original animated PDF guides** — 8 pages each, 144 pages total — in the visual language of byte-byte-go style explainers (clean boxes, flow arrows, numbered steps, annotations, page-transition dissolves that play as animations when stepped through). All diagrams drawn programmatically; no copied assets.

### The 18 Guides

| # | File | Topic | Category |
|---|---|---|---|
| 1 | bbg-load-balancing.pdf | Load Balancing | System Design |
| 2 | bbg-caching-cdn.pdf | Caching & CDNs | System Design |
| 3 | bbg-microservices.pdf | Microservices Architecture | System Design |
| 4 | bbg-tcp-handshake.pdf | TCP 3-Way Handshake | Networking |
| 5 | bbg-dns-resolution.pdf | DNS Resolution | Networking |
| 6 | bbg-tls-handshake.pdf | TLS Handshake | Networking |
| 7 | bbg-cloud-patterns.pdf | Cloud Architecture Patterns | Cloud |
| 8 | bbg-kubernetes.pdf | Kubernetes Architecture | Cloud |
| 9 | bbg-cicd-pipeline.pdf | CI/CD Pipelines | Cloud |
| 10 | bbg-zero-trust.pdf | Zero Trust Architecture | Security |
| 11 | bbg-pki-encryption.pdf | PKI & Encryption | Security |
| 12 | bbg-oauth-flows.pdf | OAuth 2.0 & Auth Flows | Security |
| 13 | bbg-neural-networks.pdf | Neural Networks | AI/ML |
| 14 | bbg-transformers.pdf | Transformers & Attention | AI/ML |
| 15 | bbg-ml-pipelines.pdf | ML Training Pipelines | AI/ML |
| 16 | bbg-etl-pipelines.pdf | ETL Data Pipelines | Data Eng |
| 17 | bbg-stream-processing.pdf | Stream Processing | Data Eng |
| 18 | bbg-data-warehouses.pdf | Data Warehouses & Lakehouses | Data Eng |

### PDF Structure (each)
1. Title page with "Animated Walkthrough" badge
2-7. Six numbered step pages with progressive diagrams
8. Key Takeaways summary page + cross-links

Animation mechanism: PDF page transitions (`/Dissolve`, 0.4–0.5s) + step-by-step page builds that simulate animation when flipped through in presentation mode.

## Sitewide Embedding

### Central Library
- **https://interstitiumlabs.dev/pdf-library/** — index page with all 18 guides, categorized, with descriptions (200 verified)

### Courses (flagship)
- **20 courses wired**, **71 PDF references** added to `modules[].pdfs[]`
- Courses: IL-03, IL-04, IL-05, IL-06, IL-07, IL-08, IL-11, IL-12, IL-13, IL-14, IL-15, IL-16, IL-17, IL-19, IL-24, IL-25, IL-26, IL-27, IL-28, IL-29
- Backups: `.work/pdf-buildout/course-json-backups-pdf/`

### Bootcamps (cert-bootcamps worker)
- **135 bootcamps wired**, **331 PDF references** added as `pdfGuides` in content.json
- Keyword-matched by bootcamp slug (cyber→zero-trust/pki/tls, network→tcp/dns/tls, cloud→patterns/lb/cdn, etc.)
- Backups: `.work/pdf-buildout/bootcamp-json-backups-pdf/`

## Deployment & Verification

- **Flagship** (solitary-sound-015a): deployed 2026-10-09T05:28:39Z — PDFs, library page, course JSONs
- **cert-bootcamps**: deployed 2026-10-09T05:29:25Z — 135 wired content.json files
- **Verified:** all 18 PDFs return HTTP 200 at `https://interstitiumlabs.dev/assets/pdfs/`
- **Verified:** `/pdf-library/` returns 200
- **Verified:** bootcamp `content.json` serves `pdfGuides` live (spot-checked tl-interview: 2 guides)

## Generators
- Framework: `.work/pdf-buildout/bbg_style.py`
- Batches: `gen_batch1.py` (system design), `gen_batch2.py` (networking), `gen_batch3.py` (cloud), `gen_batch4.py` (security), `gen_batch5.py` (AI/ML), `gen_batch6.py` (data eng)
- Wiring: `wire_pdfs_courses.py`, `wire_pdfs_bootcamps.py`

## Cross-Linking
- Each PDF summary page points to interstitiumlabs.dev videos/labs
- Library page cross-links all 18 guides by category
- Course JSON `pdfs` entries sit alongside `videos` entries in modules
- Bootcamp `pdfGuides` sit alongside `videos` wiring

## Notes
- TTS voiceover is down (unrelated to PDFs — PDFs are text-native, no audio needed)
- 8 bootcamps did not match any keyword rule and received default PDFs (cloud-patterns + tls-handshake)
- IL-01, IL-02, IL-09, IL-10, IL-18, IL-20, IL-21, IL-22, IL-23 have no direct PDF topic match (esoteric/humanities/math focus) — library page is linked instead

## Batch 2 — Full 242-PDF wiring (2026-10-09 ~01:51–02:00 EDT)

**User order:** wire all 242 bbg PDFs (18 original + 224 new) into library page, courses, and bootcamps; deploy; verify.

**What changed:**
- **Library page** (`docs/pdf-library/index.html`): rebuilt to index **241 guides** (12 categories) with TOC + anchor links. `_t.pdf` (1.7KB stray in the output dir, not a guide) excluded.
- **Courses:** 24 course JSONs wired, **436 new `modules[].pdfs[]` entries** (backups: `.work/pdf-buildout/course-json-backups-pdf2/`). Covered IL-02, IL-03, IL-04, IL-05, IL-06, IL-07, IL-08, IL-09, IL-11, IL-12, IL-13, IL-14, IL-15, IL-16, IL-17, IL-18, IL-19, IL-20, IL-24, IL-25, IL-26, IL-27, IL-28, IL-29. IL-01/IL-10/IL-21/IL-22/IL-23 skipped (esoteric/humanities — no topical match; library page covers them).
- **Bootcamps:** 135 bootcamps wired, **585 new `pdfGuides` entries** total (backups: `.work/pdf-buildout/bootcamp-json-backups-pdf2/`), cap 6/bootcamp, keyword rules extended (sql, linux, python/java/c, dsa/interview, blockchain, mobile, math/quant, databases, career/pmp, web/frontend). 13 defaulted bootcamps are genuinely non-technical (esoteric/humanities/meta catalogs).
- **Metadata:** new canonical table `.work/pdf-buildout/pdf_meta.py` — filename → (category, title, one-line description) for all 241 guides; generators: `build_library.py`, `wire_pdfs_courses2.py`, `wire_pdfs_bootcamps2.py`.

**Deploy & verify (2026-10-09T05:57–05:59Z):**
- Flagship `solitary-sound-015a`: deployed etag=95acb862e03f (29 changed files uploaded; rest hash-deduped).
- `cert-bootcamps` worker: deployed (135 changed content.json files uploaded; config `cert-bootcamps/deploy/worker-config.json`).
- Verified: 9/10 sampled new PDFs HTTP 200 (`bbg-big-o`, `bbg-consistent-hashing`, `bbg-terraform`, `bbg-statistics`, `bbg-blockchain`, `bbg-redis`, `bbg-mobile-arch`, `bbg-graphql`, `bbg-kubernetes`; the 10th sample was a non-existent slug, not a real file).
- Verified: `/pdf-library/` 200 with 241 "Read the guide" cards incl. new guides.
- Verified: free course JSON live (IL-27: 200, 133 pdf refs incl. new ones). Paid-course JSONs return 402 (paywall) — expected.
- Verified: bootcamp `content.json` live (tl-interview: 8 pdfGuides incl. new ones; note `learn.` host 308-redirects to `interstitiumlabs.dev`).
