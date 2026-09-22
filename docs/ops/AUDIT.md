# Site audit — URL map, dedupe, commerce

_Last updated: 2026-09-21 (EDT)._

## Commerce status

| Surface | Path | Status |
|---------|------|--------|
| Enroll UI | `/enroll/` | **Shipped** — CTAs driven by `config.js` |
| Config | `/enroll/config.js` | Placeholders only; `paymentsLive: false` |
| Success / cancel | `/enroll/success.html`, `/enroll/cancel.html` | Shipped |
| Admin console | `/admin/` | Shipped (GitHub + CF + checklist) |
| Payments docs | `/ops/payments.md` | Shipped |
| Live card / PayPal | — | **Inactive** until operator pastes live URLs |

No Stripe secret keys in repo (by design).

## Static career tracks (deduped)

| Track | URL | Role | Dedupe note |
|-------|-----|------|-------------|
| BNY Prep hub | `/prep/` | Interview sprint | Canonical short crush; not Mastery |
| Prep math / prog / devops | `/prep/math/`, `/programming/`, `/devops/` | Phase pages | Part of Prep |
| BNY drills | `/prep/drills/bny-interview/` | STAR / JD drills | Prep only |
| Magic Leap metrology | `/prep/drills/magic-leap-metrology/` | Separate interview aim | Keep role stories separate |
| Paths hub | `/paths/` | Index of static tracks | Not SPA academies |
| DevSecOps Mastery | `/paths/devsecops-mastery/` | 12-mo curriculum | Cross-links Prep; no syllabus clone |
| DS cert roadmap | `/paths/data-science-certs/` | DS certs only | Not DevOps ladder |
| NVIDIA AI | `/paths/nvidia-ai/` (+ `quest.html`) | Free DLI track | Not DS clone |
| FDE training | `/paths/fde-training/` | Stub for ChatGPT FDE webapp import | Awaiting `_imports/chatgpt-6ab1*` |
| Lawrence evidence | `/evidence/lawrence-enrollment/` | Portfolio write-up | Single evidence page |

SPA academies (`/academy/…`, homepage IL-01…IL-10) remain product fiction routes — **do not** mirror them as second static clones under `/prep/`.

## Core marketing / ops pages

| Page | URL |
|------|-----|
| Home | `/` |
| About | `/about/` |
| Founders | `/founders/` |
| Enroll | `/enroll/` |
| Admin | `/admin/` |
| Ops admin | `/ops/admin.md` |
| Ops payments | `/ops/payments.md` |
| Pending imports | `/ops/PENDING-IMPORTS.md` |
| This audit | `/ops/AUDIT.md` |

## Pending ChatGPT imports

See [PENDING-IMPORTS.md](./PENDING-IMPORTS.md):

- `6ab1eabe-1f24-83ea-8f55-212e35a45529` — Create FDE Training Webapp
- `6ab1eb2c-8158-83ea-baed-16b51daa823b` — sibling share

## Nav / sitemap wiring

Enroll + Admin linked from key static pages (about, founders, prep, paths, index footer/nav where edited) and `sitemap.xml`.
