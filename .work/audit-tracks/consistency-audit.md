# TRACK 4 — Consistency Audit (header/nav, footer, logo, theme, motto)

Date: 2026-10-08 ~21:30 EDT · Auditor: subagent (Track 4)
Repo: `~/workspace/apex-audit` (source under `docs/`; portfolio source `~/workspace/portfolio-site/`)
Method: curl of live pages + repo source comparison + deployed worker bundle inspection
(`.work/gateway-worker/interstitium-course-gateway-20261008-free-bootcamp.js`).

## Page set (12 pages, 4 hosts)

| # | URL (live) | Repo source |
|---|-----------|-------------|
| 1 | https://interstitiumlabs.dev/ | `docs/index.html` |
| 2 | https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery | `docs/university/course.html` |
| 3 | https://interstitiumlabs.dev/university/academy.html | `docs/university/academy.html` |
| 4 | https://interstitiumlabs.dev/bootcamps/tl-interview/ | separate worker — NO repo source (`.work/gateway-worker/interstitium-course-gateway-20261008-free-bootcamp.js`) |
| 5 | https://interstitiumlabs.dev/jobs/ | `docs/jobs/index.html` |
| 6 | https://learn.interstitiumlabs.dev/ | same worker as #1 (alias) |
| 7 | https://learn.interstitiumlabs.dev/university/course?course=il-29-… | same worker as #2 (alias) |
| 8 | https://learn.interstitiumlabs.dev/university/academy.html | same worker as #3 (alias) |
| 9 | https://enmanueldmejia.com/ | `~/workspace/portfolio-site/index.html` |
| 10 | https://app.interstitiumlabs.dev/ | same worker as #1 (alias) |
| 11 | https://app.interstitiumlabs.dev/university/course?course=il-29-… | same worker as #2 (alias) |
| 12 | https://app.interstitiumlabs.dev/noah/ | `docs/noah/index.html` (via same worker) |

**Host aliasing (verified):** learn.interstitiumlabs.dev and app.interstitiumlabs.dev serve byte-identical
HTML to interstitiumlabs.dev for every sampled path — the only live differences are the Cloudflare
challenge-script token and the per-host `og:url` the worker injects on `?course=` URLs. One worker
(`solitary-sound-015a`, assets `./docs`) backs all three hosts.

---

## Per-host verdicts

### interstitiumlabs.dev — MOSTLY CONSISTENT, with deviations D1–D6 below
- Nav: canonical `.il-pillnav` on `/` and the course shell (course shell also carries the documented
  `shell-header` exception, `docs/university/course.html:74`). academy.html gets the identical pillnav
  **client-side only** (JS injection, see D4). jobs/ and noah/ use a different `masthead` header (see D3).
- Footer: canonical `il-footer-canonical` byte-identical on `/`, academy, jobs, noah. Course shell adds
  one documented extra div (D7, exception not deviation).
- Theme: dark default via `/assets/il-theme.js` on all five pages; no light default, no
  `prefers-color-scheme: light` override.
- Motto: uppercase `SCIENTIA OMNIA VINCIT` in nav/footer everywhere; homepage meta description uses
  Title Case (D5).

### learn.interstitiumlabs.dev — CONSISTENT (alias of flagship)
All 3 sampled pages identical to flagship. No independent deviations.

### app.interstitiumlabs.dev — CONSISTENT (alias of flagship)
All 3 sampled pages identical to flagship. No independent deviations.

### enmanueldmejia.com — SEPARATE SITE, internally consistent
Own topbar nav, own footer, own hashed logo assets, no motto in the flagship sense (uses Title Case
`Scientia Omnia Vincit` in header/footer/alt text), dark-by-CSS default (`color-scheme:dark`, dark
palette, no light override), no `il-theme.js`. None of the flagship chrome applies — this is a
different product, so these are noted as cross-site differences, not deviations.

---

## Deviation list (each: URL + what deviates + file/line)

**D1 — Retired logo paths served live on all flagship pages.**
Per the deployed gateway worker's `brand-logo-paths.mjs`
(`.work/gateway-worker/interstitium-course-gateway-20261008-free-bootcamp.js:5-25`), the canonical
logo is `/assets/chrome/interstitium-logo.png` and the following are retired: `sigil-glyph.svg`,
`sigil-decor.webp`, `canonical-lockup*.png|webp`, `favicon.svg`, `favicon.png`, `og.jpg`, `og-sigil.jpg`,
`il-logo.js`, plus hero/icon variants. Yet live flagship pages reference:
- `/assets/chrome/sigil-glyph.svg` — nav brand img + footer logo on EVERY flagship page
  (live: `https://interstitiumlabs.dev/`, `/university/course?course=il-29-…`, `/university/academy.html`,
  `/jobs/`, `/noah/`; repo: `docs/index.html:45,461`, `docs/university/course.html:29,174`,
  `docs/university/academy.html:385`, `docs/jobs/index.html:19,166`, `docs/noah/index.html:21,173`)
- `/assets/chrome/sigil-decor.webp` — homepage (live `/`; repo `docs/index.html`, and
  `../assets/chrome/sigil-decor.webp` in `docs/university/course.html:30`-region markup)
- `/favicon.svg` + `/favicon.png` — icon links, homepage (repo `docs/index.html` head);
  `/favicon.svg` also on jobs/ and noah/
- `/og.jpg` — og:image on homepage (repo `docs/index.html` head)
The files still exist under `docs/`, so they resolve — but they are on the worker's own retired list.
Worse: the HTMLRewriter that swaps retired refs for the canonical logo exists ONLY in the
`/bootcamps/*` gateway worker (`brandDocument`/`replaceSrcset`, same file lines ~40-70); the flagship
worker (`docs/_worker.js`) does no such rewriting, so retired refs ship to browsers live.

**D2 — Homepage pillnav mislabels `/prep/drills/`.**
Live `https://interstitiumlabs.dev/` nav contains BOTH `Practice` (→ `#`?) no — it contains
`Practice & Exams` for `href="/prep/drills/"` (repo `docs/index.html:72`), while the course shell
(`docs/university/course.html` nav), the academy JS-injected nav
(`docs/university/js/app.js:227`), and the task's canonical 14-link set all label that same href
`Practice`. Same destination, two labels — the homepage is the outlier (17 link texts vs 16 elsewhere).

**D3 — jobs/ and noah/ carry a different, non-pillnav header.**
- `https://interstitiumlabs.dev/jobs/` → `<header class="masthead">` + `<nav aria-label="Site">`
  with 3 links (Learning OS, Noah AI, University) — repo `docs/jobs/index.html:18-20`. No pillnav
  markup, no JS chrome injection (its scripts are `noah-*.js` only).
- `https://app.interstitiumlabs.dev/noah/` → same `masthead` pattern with 4 links (Learning OS, Jobs,
  Paths, University) plus `<nav class="view-nav">` — repo `docs/noah/index.html:20-22,30`.
Both keep the canonical footer and `il-theme.js`, but the header is a different nav, not the pill nav.

**D4 — academy.html has no server-rendered nav (JS-injected only).**
Live `https://interstitiumlabs.dev/university/academy.html` contains zero pillnav markup; the nav is
built at runtime by `renderHeader()` in `docs/university/js/app.js:249-264` (canonical 14-link set +
Enroll, same brand lockup) into `<div id="il-header">` (repo `docs/university/academy.html:30`).
Consistent when JS runs; no-JS clients / static fetches get no nav at all. (Stylesheet
`css/il-pillnav.css` is linked at `docs/university/academy.html:24`.)

**D5 — Motto case is inconsistent (three variants live).**
Canonical per task: uppercase `SCIENTIA OMNIA VINCIT` — used in nav brand + footer on all flagship
pages (e.g. `docs/index.html:46`, `docs/university/course.html:30`).
- `https://interstitiumlabs.dev/` meta description uses Title Case `Scientia Omnia Vincit`
  (repo `docs/index.html:14`) — same page, two cases.
- `https://interstitiumlabs.dev/bootcamps/tl-interview/` uses lowercase `Scientia omnia vincit`
  (its worker's own brand standard — `MASTHEAD` in
  `.work/gateway-worker/interstitium-course-gateway-20261008-free-bootcamp.js:33`).
- `https://enmanueldmejia.com/` uses Title Case `Scientia Omnia Vincit` (header, footer, alt text —
  `~/workspace/portfolio-site/index.html:52,343,394`; separate site, noted).

**D6 — /bootcamps/tl-interview/ is a different product surface entirely.**
Served by a separate worker (`interstitium-course-gateway`, routes `/bootcamps/*`; no source in
`docs/`). Deviations vs flagship chrome, all live at
`https://interstitiumlabs.dev/bootcamps/tl-interview/`:
- Nav: `il-site-masthead`/`il-site-nav il-brand-nav` (Courses, Noah, Member sign-in, Membership) +
  bootcamp section tab nav — not the pill nav.
- Footer: `<footer class="footer">` (309 bytes: "Interstitium Labs · Certification Bootcamps ·
  built 2026-10-05 ← Esoteric Computing Studies ← All bootcamps") — not the canonical footer.
- Logo: uses the CANONICAL `/assets/chrome/interstitium-logo.png` (the only surface that does).
- Theme: NO `/assets/il-theme.js`; dark via `<meta name="color-scheme" content="dark">` +
  worker-injected `il-site-theme` class — no toggle, no persistence.
- Motto: lowercase `Scientia omnia vincit` (see D5).

**D7 — Course-shell footer extra div (documented exception, NOT a deviation).**
`docs/university/course.html:178` adds `<div class="il-fc-course" id="ft-course"></div>` to the
canonical footer (shows the course code; live footer 962 vs 910 bytes). Intentional page-type
exception.

## Non-deviations confirmed (curl + repo)
- **Theme:** dark default everywhere on flagship (`docs/assets/il-theme.js:1-20` — resolves `dark`
  unless `localStorage["il-theme"]==="light"`; sets `<html data-theme>` pre-paint). The two
  `data-theme="light"` hits on the homepage are CSS selectors (`html[data-theme="light"]{…}`), not
  defaults. No `prefers-color-scheme: light` overrides anywhere. Portfolio is dark-by-CSS
  (`color-scheme:dark`, `~/workspace/portfolio-site/styles.css:1`).
- **Footer:** canonical `il-footer-canonical` byte-identical across `/`, academy, jobs, noah on all
  three flagship hosts.
- **Worker injections (live-only, documented):** 12 OG/Twitter meta tags injected by the flagship
  worker's `serveCourseWithOg` on `?course=` URLs (per-host-correct `og:url` — verified
  `interstitiumlabs.dev` vs `learn.` vs `app.` variants differ only in host); Cloudflare
  `/cdn-cgi/challenge-platform` script appended to flagship pages. Repo `docs/university/course.html`
  head carries a comment documenting the OG injection.
- **Motto present** on every flagship page (uppercase, nav + footer).

---

## 5-line summary
1. Audited 12 pages across 4 hosts: learn. and app. are byte-identical aliases of the flagship worker — all their deviations are flagship deviations; enmanueldmejia.com is a separate, internally consistent site.
2. Biggest finding: every flagship page serves retired logo paths live (`/assets/chrome/sigil-glyph.svg` in nav+footer, `sigil-decor.webp`, `favicon.svg/png`, `og.jpg`) — all on the gateway worker's own retired list — and the flagship worker (unlike the /bootcamps/* worker) does no edge rewriting, so they reach browsers.
3. Nav deviations: jobs/ and noah/ use a different `masthead` header (no pill nav); academy.html's pill nav is JS-injected only (absent for no-JS); the homepage pillnav mislabels `/prep/drills/` as "Practice & Exams" while all other surfaces say "Practice".
4. /bootcamps/tl-interview/ is a separate worker/surface with its own nav, minimal footer, lowercase motto, no theme-boot script — but it is the only surface using the canonical `/assets/chrome/interstitium-logo.png`.
5. Motto case is inconsistent three ways (uppercase flagship nav/footer, Title Case in the homepage meta description at `docs/index.html:14`, lowercase on the bootcamp page, Title Case on the portfolio); theme is dark-default everywhere with no light-mode defaults or overrides.
