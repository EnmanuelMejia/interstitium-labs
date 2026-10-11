# UX Cost-Benefit Analysis — interstitiumlabs.dev
**Date:** 2026-10-09 | **Analyst:** Strategic subagent | **Scope:** read-only analysis

> Owner rules honored: no competitor names (Competitor A/B/C/D). No site modifications made.

---

## Part 1 — Section Scorecard

| Section | VALUE | COST | VERDICT | Reasoning |
|---|---|---|---|---|
| Homepage `/` | HIGH | MED | **KEEP** | Converts + orients. Needs search + consistent counts. |
| `topics/` (16 themes) | HIGH | LOW | **KEEP — make primary** | The differentiator. Cinematic heroes, tab bar. This IS the site's identity. |
| `university/` (31 courses) | HIGH | MED | **KEEP, rename label** | Core product. "Courses" nav → "Knowledge Operating System / academies" page = label mismatch. Fix terminology. |
| `paths/` (24 paths) | HIGH | MED | **KEEP** | Career/skill journeys. Overlaps university/ — clarify: paths = journeys, courses = content. |
| `prep/drills/` (Practice) | HIGH | LOW | **KEEP** | Hands-on = retention. Already absorbing labs/play/adapt. |
| `labs/` (4) | MED | LOW | **KEEP, link from Practice** | Real labs = high value. Keep URLs, surface via Practice hub. |
| `noah/` (Noah AI) | HIGH | LOW | **KEEP** | AI tutor = key differentiator vs competitors. None of A/B/C/D have this in primary nav. |
| `pdf-library/` (242 guides) | HIGH | LOW | **KEEP** | Unique asset. Theme-filterable. High retention value. |
| `bootcamp-catalog/` | MED | LOW | **MERGE → Paths** | Listing page, not a destination. Fold into Paths hub as a tab/section. |
| `jobs/` | MED | LOW | **KEEP** | Career outcome = conversion. Competitors bury this; we surface it. Differentiator. |
| `about/` | MED | LOW | **KEEP** | Trust + founder story. Required. |
| `enroll/` + `account/` | HIGH | LOW | **KEEP** | Conversion funnel. Non-negotiable. |
| `evidence/` (3) | LOW | LOW | **MERGE → About** | Social proof belongs on About, not a standalone section. 3 pages, low traffic. |
| `subject-map/` | LOW | LOW | **MERGE → Topics** | MIT-style map is a Topics hub feature, not a destination. Embed as Topics tab. |
| `cinema/` | LOW | MED | **DELETE** (in progress) | Gallery with no teaching value. Heroes already inline on themes. Owner-confirmed. |
| `learn/` | — | — | **DELETED** ✓ | Consolidated into themes. |
| `academy/` | — | — | **DELETED** ✓ | Was 11 redirect stubs. |

**Net nav after verdicts:** Courses, Topics, Paths, Practice, Noah AI, Jobs, About = **7 items**. (Cinema/Videos removed.)

---

## Part 2 — Competitor Navigation Comparison

### Competitor A (large course marketplace)
- **Nav items:** ~5 (Categories dropdown, Search bar, Teach, Cart, Login)
- **Organization:** By category (Development, IT, Data Science...) → subcategory → course. Also by "career tracks."
- **Clicks home → course:** 3 (category → subcategory → course). Search: 2.
- **Search:** Dominant — large header search bar on every page. This is the primary discovery path.
- **What they lack:** No AI tutor, no themed immersion, no jobs board in nav, no hands-on labs in primary nav.

### Competitor B (university-partnered platform)
- **Nav items:** ~4 (Explore, Degrees, Certificates, Search)
- **Organization:** By credential type first (course vs certificate vs degree), then by topic.
- **Clicks home → course:** 3. Search: 2.
- **Search:** Prominent header search.
- **What they lack:** No role-based paths in primary nav, no practice/labs emphasis, no AI tutor.

### Competitor C (tech-skills focused)
- **Nav items:** ~5 (Browse, Paths, Search, Pricing, Login)
- **Organization:** By **role** (e.g., "Cloud Engineer") and **skill** (e.g., "Kubernetes"), plus certification paths.
- **Clicks home → course:** 2–3 via role path. Search: 2.
- **Search:** Header search, always visible.
- **What they lack:** No esoteric/frontier content, no AI tutor, no jobs.

### Competitor D (cloud-training specialist)
- **Nav items:** ~4 (Learn, Hands-on, Search, Pricing)
- **Organization:** By cloud provider + certification. Heavy emphasis on hands-on labs.
- **Clicks home → course:** 2–3. Search: 2.
- **Search:** Present but secondary to guided paths.
- **What they lack:** Breadth beyond cloud, no AI tutor, no jobs.

### Comparison vs our 7-item nav

| Dimension | Competitors (A/B/C/D) | Us | Verdict |
|---|---|---|---|
| Nav item count | 4–5 | 7 | **We are worse.** 7 > 5. Target: 5–6. |
| Search prominence | Header bar, every page | **None** | **We are worse.** This is the #1 gap. |
| Clicks to course | 2–3 | 2 (Courses → course) | **We are better** (when labels match). |
| Organization | Category / role / credential | 16 cinematic themes | **We are better** (differentiated, memorable). |
| AI tutor in nav | None | Noah AI | **We are better** (unique). |
| Jobs in nav | None | Jobs | **We are better** (career outcome surfaced). |
| Hands-on in nav | D only | Practice | **We are at parity.** |
| Esoteric/frontier | None | Esoteric, Om, Cybernetics | **We are better** (blue ocean, zero competition). |

**What competitors DON'T have that we should also cut:** None of A/B/C/D has a video gallery, a separate "library" hub, an "evidence" section, or a "subject map" page. Our deletions (cinema, library, evidence, subject-map as standalone) align us with the competitive standard.

**What competitors ALL have that we lack:** Prominent sitewide search. This is the single biggest UX gap.

---

## Part 3 — Nav/Workflow Recommendations

### R1. Add sitewide search (highest ROI)
Every competitor has a header search bar. We have none. A user who knows what they want ("Turing," "XRP," "CISSP") should reach it in 1–2 clicks, not 3–4 browsing. Implementation: client-side index over course titles, theme names, path names, PDF guide titles. Place in header next to nav, keyboard shortcut `/`.

### R2. Fix label mismatches (zero-cost, high confusion)
- Nav "Courses" → page titled "Knowledge Operating System" about "academies." **Pick one word: Courses.** Rename page H1 + copy.
- Homepage "Ten academies" vs university/ "Thirty-one academies." **Fix the count.**
- "Videos" nav → "Cinema" page title (being deleted; moot after cinema removal).

### R3. Reduce to 6 nav items
Current 7: Courses, Topics, Paths, Practice, Noah AI, Jobs, About. Competitors run 4–5. Merge **Paths → Topics** as a "Learning paths" section on each theme page (paths are already theme-mappable per CONSOLIDATION_PLAN.md §5). New nav: **Courses, Topics, Practice, Noah AI, Jobs, About** = 6. Paths survive as theme-page sections, not a top-level destination.

### R4. Theme tab bar: cap visible tabs on mobile
16 tabs are correct on desktop; on mobile, show 5 + "More" overflow. Current horizontal scroll through 16 is tedious on a phone.

### R5. Unify course discovery: one catalog, not two
`university/` (courses) and `paths/` (journeys) overlap conceptually. Keep both, but add cross-links: every course page links its parent path(s); every path page lists its courses. A user should never wonder "is this a course or a path?"

### R6. Breadcrumb on every page
Competitors all breadcrumb (Home > Category > Course). Our theme pages have it; ensure every course/path/guide page does too. Cheapest orientation fix available.

---

## Part 4 — Frontier → Theme Mapping

Frontier tracks found in `paths/frontier/`:

| Frontier track | → Theme | Notes |
|---|---|---|
| Cloud DevOps (junior) | Cloud & DevOps | Direct |
| Platform basics | Cloud & DevOps | Direct |
| Kubernetes SRE | Cloud & DevOps | Direct |
| Reliability engineering | Cloud & DevOps | Could also suit System Design |
| Ops math | Mathematics (Turing) | Direct |
| CS fringe | Cybernetics | Fringe CS = systems thinking |
| DevSecOps | Cybersecurity | Direct |
| Secure supply chain | Cybersecurity | Direct |
| AWS Cloud Practitioner | Cloud & DevOps | Direct |
| Cloud fluency | Cloud & DevOps | Direct |
| Linux essentials | Linux & Systems | Direct |
| Data analyst → ML | Data Engineering | Direct |
| ML literacy | AI & ML | Direct |
| Neuroscience | **GAP** | See below |

**GAP — Neuroscience:** Does not fit any of the 16 themes cleanly. Options:
- (a) New 17th theme "Mind & Brain" — justified if 3+ neuroscience/cognitive-science items exist.
- (b) Fold into **Om** (consciousness) — philosophically adjacent but scientifically distinct; risks diluting Om.
- (c) Fold into **AI & ML** — "neural" networks are brain-inspired; weakest fit scientifically.
- **Recommendation:** (a) only if the catalog grows; for now (b) Om with a "Science of Mind" subsection, clearly labeled as science not mysticism.

**Frontier content from IL-23 (The Frontier course):** Emerging tech topics (per catalog: "Cutting-Edge Research Distilled") should be tagged per-item to themes at the content level — the theme pages, not a separate frontier section, are the discovery surface. The `paths/frontier/` index becomes a redirect to `/topics/`.

---

## Part 5 — Top 5 Highest-ROI Changes

Ranked by (value gained ÷ effort):

1. **Add sitewide search** — Value: HIGH (every competitor has it; cuts all journeys to 1–2 clicks). Effort: LOW (client-side index, no backend). **ROI: highest.**
2. **Fix Courses/academies label mismatch + counts** — Value: HIGH (removes #1 user confusion). Effort: TRIVIAL (copy edits). **ROI: highest per minute.**
3. **Merge Paths into theme pages (6-item nav)** — Value: MED-HIGH (matches competitor nav economy). Effort: MED (move path cards into theme templates). 
4. **Breadcrumbs on every page** — Value: MED (orientation, SEO). Effort: LOW (shared fragment).
5. **Mobile tab overflow for 16 theme tabs** — Value: MED (phone is primary device for owner). Effort: LOW (CSS + "More" toggle).

---

## Appendix — Click-count summary (post-consolidation)

| Journey | Clicks | Via |
|---|---|---|
| Any course | 2 | Courses → course |
| Any theme | 2 | Topics → theme |
| Themed guide | 3 | Topics → theme → pdf-library filter |
| Practice drill | 2 | Practice → drill |
| Noah AI | 1 | Nav |
| Job listing | 2 | Jobs → listing |
| Site search (proposed) | 1–2 | Search → result |
| External short link (il26 etc.) | 1 | Direct |

No journey exceeds 3 clicks. Competitive parity or better on every path.
