# Site audit — URL map, competitive notes, commerce

_Last updated: 2026-09-21 (America/New_York)._

## Competitive posture (vs KodeKloud, A Cloud Guru, Coursera, Pluralsight, Scrimba)

| Gap closed | Where shipped | Notes |
|------------|---------------|-------|
| Student Zero Learning OS | `/founders/` | Journey map IT→DevOps, skills radar, weekly OS + `il.progress.*` streak, path sequencer, proof wall, CTAs |
| Why Interstitium vs video LMS | `/` `#why-interstitium`, `/learn/`, `/paths/` | Outcome OS + honest archetype card — not binge content |
| Curriculum OS hub | `/learn/` + upgraded `/paths/` | Outcome cards: Job-ready DevOps, Full-Stack fintech, FDE, DS certs, AI infra, Hermetica+code |
| Skills taxonomy (no orphans) | `/learn/skills/` | Every static path mapped to competencies from Prep/JD/imports |
| Local progress without accounts | `/assets/il-progress.js`, Founders weekly OS, NVIDIA Quest | Keys namespaced `il.progress.*` |
| Honesty | Founders + evidence | No invented employment; portfolio labeled; a client withdrawal on record |

**What still belongs to video LMS competitors:** deep interactive KodeKloud labs, ACG clouds sandboxes, Coursera degree rails. Interstitium **exceeds** on career-changer OS, JD/STAR honesty, inspectable static curriculum, and founder-as-Student-Zero narrative.

## Commerce status

| Surface | Path | Status |
|---------|------|--------|
| Enroll UI | `/enroll/` | **Shipped** — CTAs driven by `config.js` |
| Config | `/enroll/config.js` | Placeholders only; `paymentsLive: false` |
| Success / cancel | `/enroll/success.html`, `/enroll/cancel.html` | Shipped |
| Admin console | `/admin/` | Shipped |
| Payments docs | `/ops/payments.md` | Shipped |
| Live card / PayPal | — | **Inactive** until operator pastes live URLs |

No Stripe secret keys in repo (by design).

## Static career tracks (deduped)

| Track | URL | Role | Dedupe note |
|-------|-----|------|-------------|
| Curriculum OS | `/learn/` | Outcome hub | Points into Prep/Paths/Skills |
| Skills taxonomy | `/learn/skills/` | Master map | Nothing orphaned |
| a desk Prep hub | `/prep/` | Interview sprint | Canonical short crush; not Mastery |
| Prep math / prog / devops | `/prep/math/`, `/programming/`, `/devops/` | Phase pages | Part of Prep |
| DevOps desk drills | `/prep/drills/desk-interview/` | STAR / JD drills + honest elevator | Prep only |
| Full-stack desk VP pointer | `/prep/drills/fullstack-desk/` | Points to path | Not DevOps Q&A clone |
| Full-stack desk path | `/paths/fullstack-desk/` | Full-stack study map | Separate from DevOps syllabus |
| an instrument desk | `/prep/drills/instrument-desk/` | Separate interview aim | Keep role stories separate |
| Paths hub (Curriculum OS) | `/paths/` | Outcome cards index | Not SPA academies |
| DevSecOps Mastery | `/paths/devsecops-mastery/` | 12-mo curriculum | Cross-links Prep; no syllabus clone |
| DS cert roadmap | `/paths/data-science-certs/` | DS certs only | Not DevOps ladder |
| NVIDIA AI | `/paths/nvidia-ai/` (+ `quest.html`) | Free DLI track | Progress `il.progress.nvidia.quest` |
| FDE training | `/paths/fde-training/` | FDE Forge gamified spine | From ChatGPT `6ab1eabe…` |
| Enochian + programming | `/paths/enochian-programming/` | Source-critical DH + code | From ChatGPT `6ab1eb2c…` |
| a client evidence | `/evidence/withdrawn-note/` | Portfolio write-up | Single evidence page |
| Resume highlights | `/evidence/resume/` | Sanitized public resume | No overclaims |
| Founders Learning OS | `/founders/` | Student Zero hero | Progress `il.progress.founders.*` |

SPA academies (`/academy/…`, homepage IL-01…IL-10) remain product fiction routes — **do not** mirror them as second static clones under `/prep/`.

## Core marketing / ops pages

| Page | URL |
|------|-----|
| Home | `/` |
| About | `/about/` |
| Founders (Learning OS) | `/founders/` |
| Learn (Curriculum OS) | `/learn/` |
| Skills taxonomy | `/learn/skills/` |
| Enroll | `/enroll/` |
| Admin | `/admin/` |
| Ops admin | `/ops/admin.md` |
| Ops payments | `/ops/payments.md` |
| Pending imports | `/ops/PENDING-IMPORTS.md` |
| This audit | `/ops/AUDIT.md` |

## Imports

See [PENDING-IMPORTS.md](./PENDING-IMPORTS.md) — ChatGPT FDE + Enochian **Resolved**. DeepSeek NVIDIA/a device lab + resume attachments folded into Prep/drills/evidence/Founders skills (no fake employment claims).

## Nav / sitemap wiring

Canonical static chrome: **Index · About · Founders · Prep · Paths · Learn · Enroll · Admin · Desk**. Sitemap includes `/learn/` and `/learn/skills/`.
