# Design competitive audit — Interstitium Labs

_Last updated: 2026-09-22 (America/New_York)._  
_Static root:_ `docs/` · _Live:_ https://interstitiumlabs.dev  
_Peers:_ KodeKloud · Codecademy · Brilliant · Khan Academy · ALEKS · AWS Skill Builder · Red Hat Learning · Linux Foundation Training

**P0 verdict (this ship):** We previously **lost on looking cheap** — header lockup capped at 36–40px (postage stamp on 5120×1440), flat panels, FX density over craft. That is a brand failure. Catalog depth remains an honest gap; **visual presence must not**.

---

## Scorecard (1–5, honest)

| Dimension | IL (pre-P0) | IL (post-P0 target) | KodeKloud | Codecademy | Brilliant | Khan | ALEKS | AWS Skill Builder | Red Hat Learning | LF Training |
|-----------|------------:|--------------------:|----------:|-----------:|----------:|-----:|------:|------------------:|-----------------:|------------:|
| 1. Logo size / clarity / resolution | **1** | **4** | 4 | 4 | **5** | 4 | 3 | 4 | 4 | 3 |
| 2. Visual design / aesthetics | **2** | **4** | 4 | 4 | **5** | 4 | 3 | 3 | 3 | 3 |
| 3. Motion / graphics polish | **2** | **4** | 4 | 3 | **5** | 3 | 2 | 2 | 2 | 2 |
| 4. Depth of catalog (courses/labs) | **2** | 2 | **5** | **5** | 4 | **5** | 4 | **5** | 4 | 4 |
| 5. Breadth (topics / platforms) | **3** | 3 | **5** | **5** | 4 | **5** | 3 | **5** | 4 | 4 |
| 6. Scope (certs, paths, community, enterprise) | **3** | 3 | **5** | 4 | 3 | 4 | 4 | **5** | **5** | **5** |

**Composite read:** Post-P0 we aim to **stop losing on (1)(2)(3)**. We still **lose hard on (4)(5)(6)** vs KodeKloud / Codecademy / AWS / Red Hat / LF — and that must stay labeled honestly, never faked with wallpaper cards.

---

## What we exceed

| Area | Why IL can lead |
|------|-----------------|
| Trust / honesty | No fake lab fleet, no invented AI keys, portfolio-first labeling |
| Brand mythos | Sigil + void/cyan/gold system is distinctive vs blue SaaS LMS |
| Adaptive intent | KST / inner-fringe language nearer ALEKS than video LMS peers |
| Student Zero OS | Founders radar, pathways, SuperLab as inspectable evidence |
| Static performance + CSP | Cloudflare Pages + strict headers beat many LMS shells |

## What we lose (do not paper over)

| Area | Peer bar | IL today |
|------|----------|----------|
| Catalog depth | KodeKloud / Codecademy / AWS: hundreds–thousands of modules + sandboxes | Flagship SuperLab + curated paths — **not** a fleet |
| Breadth | Multi-cloud, multi-language, multi-role coverage | Focused DevSecOps / FDE / cert grammar |
| Scope | Certs + community + enterprise LMS seats | Paths + enroll placeholder; community/enterprise thin |
| Interaction density | Brilliant lesson craft; Khan mastery UX | Cards + motion; drills still sparse |
| AI tutoring depth | KodeKloud in-lab tutor; AWS / Codecademy assistants | `/coach/` shell + local rules — not live model |

**Design rule:** Never compensate for (4)(5)(6) by looking louder. Compensate by looking **sharper**.

---

## Logo sizing — before / after

| Surface | Before (embarrassment) | After (P0 industry bar) |
|---------|------------------------|-------------------------|
| Header lockup — mobile | **36px** hard cap (`repairChrome` + CSS) | **56px** |
| Header lockup — desktop (≥640) | **40px** hard cap | **64px** |
| Header lockup — ultrawide (≥2560) | still 40px on 5120×1440 | **72px** |
| Header lockup — 5K / ≥3840 | 40px | **80px** |
| Header bar | `h-14` / `sm:h-16` (56/64) + `overflow:hidden` clipping | **min 72px / 80px** (`4.5rem` / `5rem`), overflow-x only |
| Footer lockup | ~36–40px | **48px mobile / 56px+ desktop** |
| Asset | single PNG, often CSS-shrunk | WebP `@2x`/`@3x` + full PNG srcset; `object-contain` |
| Hero sigil | decor/maskable, ~postage on UW | `sigil-hero` 720/1200, **~140–200px** desktop, up to **~280px** UW |

Industry refs (mark vs lockup): Codecademy / KodeKloud / Brilliant typically ~28–40px **mark**, but full **lockup** often **44–64px** with readable wordmark; UW deserves **72–80px**.

**Root cause of tininess:** `docs/assets/il-fx.js` → `repairChrome()` wrote inline `height: 36px/40px !important` after paint. CSS alone could not win. P0 rewrote that function.

---

## Visual system — what changed

1. **Lockup authority** — `il-chrome.css` (loads last) owns 56/64/72–80; conflicting 40px caps neutralized in `il-responsive.css` / `il-motion.css` / `il-ultrawide.css`; SPA `site-chrome-*.js` Logo `W` + header row updated; static HTML ×33 upgraded with `<picture>` srcset.
2. **Surfaces** — `.il-surface` elevated: hairline border, layered gradient panel, soft elevation, hover cyan edge (Brilliant-grade, not flat gray cards).
3. **Mesh** — intentional cyan/gold radial mesh on isolate sections; grain optional (`.il-grain` / `body.il-grain-on`), not FX spam.
4. **Motion** — particle density reduced; sigil + one hero field kept; cheap pulse placeholders hidden.
5. **Hero** — sharp `sigil-hero.webp/png` promoted from private brand marks; meaningful CSS size.

---

## Roadmap

### P0 — shipped this commit
- [x] Visible lockup 56 / 64 / 72–80 + taller header
- [x] Kill `repairChrome` 40px ceiling
- [x] Crisp `@2x`/`@3x` WebP lockup + srcset
- [x] Hero sigil sharpness + size
- [x] Surface / mesh / FX restraint pass
- [x] This audit doc

### P1 — next
- [ ] SVG lockup (vector wordmark) if studio exports; retire raster for chrome
- [ ] Rebuild SPA from source so Logo `W` defaults stay in sync without patching bundles
- [ ] Drill / lesson chrome density (Brilliant interaction, not more particles)
- [ ] Empty states + micro-feedback on `/prep/` and `/learn/`
- [ ] Honest catalog expansion: 3–5 more cloneable labs before claiming “fleet”
- [ ] Community surface (Discord/forum) labeled beta — do not fake forum depth
- [ ] Enterprise one-pager (SSO, seats) without inventing compliance badges

### P2
- [ ] Live coach model behind feature flag
- [ ] Search across paths/labs/lessons
- [ ] Video only where evidence justifies — never wallpaper LMS hours

---

## Redeploy note (Cloudflare)

Pages project tracks `origin/main` → `docs/`.

1. Confirm this commit is on `main`.
2. Cloudflare Pages: wait for automatic production deploy, **or** Dashboard → project → **Retry deployment**.
3. Hard-refresh / purge cache for `/assets/il-chrome.css`, `/assets/il-fx.js`, `/assets/site-chrome-*.js`, `/assets/chrome/canonical-lockup*`, `/assets/chrome/sigil-hero*`.
4. Smoke on **5120×1440**: lockup ≥72px, header ≥80px tall, wordmark readable at arm’s length.

---

## Sign-off

Looking cheap was a SEV for a Learning OS brand. Catalog humility stays. Visual humility does not.
