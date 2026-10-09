# Topic Tabs with Hero Parameters — 2026-10-09

User order 2026-10-09 ~02:22 EDT: "Just like the hero every topic should be have it's own tab and theme same parameters as the hero".

## What was built

12 themed topic hub pages at `/topics/<slug>/`, each replicating the homepage hero's parameters:
- Full-viewport `.il-hero` with animated looping video background (`autoplay muted loop playsinline`)
- Poster fallback image, scrim overlay, staggered text entrance animations
- H1 title, sub-tagline, dual CTAs, "SCIENTIA OMNIA VINCIT" motto, motion caption
- `prefers-reduced-motion` respected (inherited from site CSS)

Plus a `/topics/` index page ("Twelve worlds. One OS.") with themed cards linking to each hub.

## Topics + themes (from TOPIC_TO_THEME)

| # | Slug | Hub title | Theme | Hero video |
|---|------|-----------|-------|-----------|
| 1 | cybersecurity | Cybersecurity | mr-robot (terminal green, binary rain) | cybersecurity-hero.mp4 |
| 2 | system-design | System Design | cyberpunk (neon pink/cyan particles) | system-design-hero.mp4 |
| 3 | networking | Networking | tron (electric blue grid) | networking-hero.mp4 |
| 4 | cloud-devops | Cloud & DevOps | steampunk (brass gear + dust) | cloud-devops-hero.mp4 |
| 5 | ai-ml | AI & Machine Learning | exmachina (stark white lines) | ai-ml-hero.mp4 |
| 6 | data-eng | Data Engineering | oceandeep (teal wave field) | data-eng-hero.mp4 |
| 7 | programming | Programming | hackers95 (neon streaks) | programming-hero.mp4 |
| 8 | databases | Databases | alexandria (gold dust + columns) | databases-hero.mp4 |
| 9 | linux-systems | Linux & Systems | industrial (amber, hazard bar) | linux-systems-hero.mp4 |
| 10 | math | Mathematics | sacredgeo (rotating gold lattice) | math-hero.mp4 |
| 11 | web-dev | Web Development | vaporwave (sunset + grid floor) | web-dev-hero.mp4 |
| 12 | blockchain | Blockchain | goldrush (rising gold particles) | blockchain-hero.mp4 |

## Hero videos

- Renderer: `.work/topic-tabs/render_topic_heroes.py` (original code, PIL + ffmpeg)
- Format: 6s loops, 24fps, 854×480, H.264 crf 30, no audio
- Total size: ~3 MB for all 12 (46KB–1.3MB each)
- Posters: 854×480 JPGs extracted from mid-frame
- Location: `docs/assets/topics/<slug>-hero.{mp4,jpg}`

## Page structure (each hub)

1. Pill nav (with Topics link), breadcrumbs (Home → Topics → Name)
2. Themed hero (video bg + title + tagline + CTAs + motto)
3. Courses section — cards linking to `/university/course?course=<slug>`
4. Bootcamps section — up to 12 cards linking to `/bootcamps/<slug>/` (existence-verified)
5. Media & Guides — PDF library deep link (`/pdf-library/#anchor`), Cinema, Noah AI
6. Canonical footer

Course counts per hub: cybersecurity 6, cloud-devops 4, ai-ml 4, data-eng 3, programming 3, others 1–2.
Bootcamp links: only dirs verified to exist under `cert-bootcamps/site/bootcamps/`.

## Navigation

- `/topics/` added to homepage pill nav (desktop links + mobile menu sheet)
- Each hub page nav includes Topics link
- Breadcrumbs on all hub pages

## Files

- Pages: `docs/topics/<slug>/index.html` (12) + `docs/topics/index.html`
- Generator: `.work/topic-tabs/gen_topic_pages.py` (re-runnable; chrome extracted from cinema/index.html + index.html)
- Videos: `.work/topic-tabs/render_topic_heroes.py`
- Theme CSS: `docs/assets/il-topic-themes.css` (pre-existing, 695 lines, linked in all hub pages)

## Deploy

- Commit: "Topic hubs: 12 themed topic tabs with hero videos"
- Worker: `solitary-sound-015a` via `flagship-deploy-config-20261008.json`
- Static serving: `html_handling: auto-trailing-slash` — no worker route changes needed

## Verification (2026-10-09 ~02:35 EDT — all live)

- [x] 13/13 pages return 200 (12 hubs + /topics/ index)
- [x] 12/12 hero videos return 200
- [x] 12/12 posters return 200
- [x] Topics link present in homepage nav (desktop + mobile menu sheet)
- [x] Spot-check: cybersecurity hub serves themed hero video w/ poster; topics index headline live

## Themed Hero Overhaul (2026-10-09 ~03:20 EDT)
User reported topic pages looked identical to homepage — theme only touched cards, hero used generic il-hero styling.

Changes:
- New stylesheet: docs/assets/il-topic-heroes.css (~28KB, all original CSS work)
- Generator patched: .work/topic-tabs/gen_topic_pages.py now emits <header class="th-hero th-hero--<theme>">
- Each hero: full-viewport (100svh), theme tint over video, 1-2 animated CSS fx layers, theme decor elements, themed eyebrow/title/tag
- 12 distinct heroes: mr-robot (scanlines+glitch), cyberpunk (neon rain), tron (perspective grid), steampunk (gears+rivets), exmachina (hairlines), oceandeep (currents+sonar), hackers95 (static+tape), alexandria (columns), industrial (hazard+plate), sacredgeo (rotating rings), vaporwave (sun+chrome title), goldrush (circuits+glint)
- Deployed: solitary-sound-015a etag=de43e33e40e4, 2026-10-09T07:19:52Z
- Verified: 12/12 pages HTTP 200 with correct hero classes + CSS live
