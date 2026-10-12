# TRACK 3 — Render Audit (code-level, no live browser)

Date: 2026-10-08 ~21:45 EDT · Repo: `~/workspace/apex-audit` @ `f838c05` (docs/ = deployed source)
Method: curl of live pages + local code inspection only. No code changed.
Scratch: `~/workspace/apex-audit/.work/render-audit/` (fetched pages, audit_html.py, idcheck.py, csscheck.py)

Pages fetched live (all HTTP 200 unless noted):
- `https://interstitiumlabs.dev/` (main.html, 29,983 B)
- `https://interstitiumlabs.dev/university/` (university.html, 22,748 B)
- `https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery` (canonical IL-29 slug per `_worker.js` L296)
- `https://interstitiumlabs.dev/university/academy` (307 chain: `/university/academy.html` → 307 → `/university/academy` → 200; serves legacy academy page)
- `https://interstitiumlabs.dev/bootcamps/tl-interview/`
- `https://interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/`
- `https://learn.interstitiumlabs.dev/`, `https://app.interstitiumlabs.dev/` (both byte-identical to main)
- `https://enmanueldmejia.com/` (byte-identical to local `~/workspace/portfolio-site/index.html`)

---

## 1. VERIFIED ISSUES

### V1 — `docs/assets/il-proof.js` fails to parse (SyntaxError) → /evidence/ widget dead [HIGH]
- File: `~/workspace/apex-audit/docs/assets/il-proof.js`, **line 65**
- `node --check` output: `SyntaxError: Unexpected identifier 's'`
- Cause: single-quoted JS string literal contains an unescaped apostrophe in `Noah's turns`:
  `...Aggregates adaptive history, CotD / evidence feed, Noah's turns, checklist progress...`
- Impact: the whole script fails at parse time, so nothing in it runs. `docs/evidence/index.html` **line 58** loads it (`<script src="/assets/il-proof.js">`) to mount `[data-il-proof]` (index.html L54). The mount div contains only a `<noscript>` fallback, so **JS-enabled visitors see an empty section** and the Download .md / Copy markdown / Print buttons never render. Console shows the SyntaxError.
- Fix (not applied — audit only): escape as `Noah\'s` or switch the string to double quotes.

### V2 — `docs/university/course.html` has no favicon link [LOW]
- Verified: no `rel="icon"` in `docs/university/course.html` (nor in the live-served copy). Every other key page (`/`, `/university/`, academy, both bootcamp pages, portfolio, evidence) has one.
- Impact: course pages show the browser default icon. Minor polish issue.

### V3 — `learn.` and `app.` subdomains serve the flagship homepage byte-for-byte [MEDIUM — needs owner confirmation]
- `https://learn.interstitiumlabs.dev/` and `https://app.interstitiumlabs.dev/` return content **byte-identical** to `https://interstitiumlabs.dev/` (29,983 bytes, `diff` identical).
- If `learn.` is mid-fold into flagship this may be intentional; but `app.` serving a marketing homepage instead of an app shell looks like a placeholder/misconfiguration. Flagged for a human decision.

---

## 2. RISK LIST (suspicions, NOT verified — need live-browser confirmation)

- **R1 — Empty `alt=""` on brand images.** Decorative use is WCAG-correct, but confirm the intent: `/assets/chrome/sigil-glyph.svg` (main L45), `/assets/chrome/sigil-decor.webp` (main L94), `assets/sigil.svg` (university L42), `/assets/chrome/interstitium-logo.png` (both bootcamp pages L27), `/assets/interstitium-sigil.*.webp` ×2 (portfolio L51/L393). If the logo images are meaningful links, they should have alt text.
- **R2 — Course page is a JS app shell.** `course.html` static HTML is chrome + empty mounts; all content renders from `course-shell.js` + `/university/data/courses/*.json`. With JS disabled/blocked (or a shell-JS failure) the page is effectively empty. By design, but confirm SEO/no-JS stance is acceptable.
- **R3 — External Google Fonts stylesheet** on main/learn/app pages (`fonts.googleapis.com`). If the font CDN is slow/blocked, first paint falls back to system fonts — fine, but a browser check should confirm no layout shift breaks the hero.
- **R4 — Inline `style=` attributes** (12 on main, 14 on bootcamp pages, 8–9 on university/academy). All inspected instances are benign (margins, `display:none` toggles, `clamp()` font sizes); none override layout critically. Low risk.
- **R5 — Academy 307 chain.** `/university/academy.html` → 307 → `/university/academy` (200, legacy academy content). Not a loop, but two-step; consider a direct 301 to the canonical academy destination when the legacy page is retired.

---

## 3. MISSING-VIEWPORT LIST

None. `<meta name="viewport">` is **present** on all 8 key pages plus the academy page and the portfolio page.

---

## 4. JS CHECK RESULTS

### node --check (syntax)
| File(s) | Result |
|---|---|
| `docs/university/course-shell.js` | OK |
| `docs/university/js/*.js` (11 files: app, hero, il-diagnostic, il-guided, il-mastery, il-noah-tutor, il-progress, il-stories, noah, +2) | ALL OK |
| `docs/assets/*.js` (64 files) | 63 OK — **`il-proof.js` FAILS** (V1) |
| bootcamp `_engine/*.js` (bootcamp, terminal, learn, labs, simulations, consoles, missions — fetched live) | ALL OK |

### getElementById / querySelector(#…) hazard scan
Paired each JS file against its HTML. All "missing" ids resolved as safe:
- `course-shell.js` vs `course.html`: 52 id refs; every one is either created by the script itself (`#ilgd-rail` L1222, `#mod-list` L1223, `#mock-start` L1733, `#plan-list` L782, `#a-root` via `il27NodeBox` L4820) or null-guarded (`if (brief)` L489 for `#tab-brief`; `if (!strip) { create }` L470–475 for `#ilprog-navstrip`). Dynamic-prefix selectors (`#mod-`, `#quiz-`, `#tab-`) are intentional.
- `assets/il-theme.js` vs `index.html`: `#il-theme-toggle` self-created (L60–69, guarded `if (getElementById(...)) return`).
- `assets/noah-ai.js` vs `index.html`: all 8 `#noah-*` ids self-created (L1154–1163).
- `assets/il-pwa.js` vs `index.html`: 0 id refs.
- `university/js/*` vs `university/index.html`: `#il-mastery-css` / `#il-noah-tutor-css` self-injected with existence checks; `#noah-*` self-created by `js/noah.js` (L683–689); `il-noah-tutor.js` L147 retries `#noah-input` via guarded timeout loop.
- `_engine/bootcamp.js` vs `tl-interview.html`: 0 id refs.
- `localStorage` in `il-progress.js`: probe + try/catch with in-memory fallback (L35–48) — private-mode safe.
- No `document.write` in any main JS file.

---

## 5. MOBILE CSS SCAN

- **No bare `width:>400px` outside `@media`** in any checked CSS: `assets/il-unified.css`, `university/course-shell.css`, `university/css/*.css`, bootcamp `_engine/style.css`, portfolio `styles.css` (live 10 KB; note: local `portfolio-site/styles.css` is a 7-line stub — the deployed CSS is not in that repo).
- `.brief-grid { grid-template-columns: 280px 1fr }` (course-shell.css L151) **collapses** via `@media (max-width:760px)` (L158) — fine.
- `.table-scroll table { min-width: 560px }` (il.css L717) is wrapped in `overflow-x:auto` — intentional horizontal scroll, fine.
- `@media (max-width:900px)` in course-shell.css (L111) hides `.shell-nav`, shows `.mobile-nav` — fine.
- Media queries present in all stylesheets (portfolio: 900px/560px; engine: 4 queries).

---

## 6. OTHER STATIC CHECKS

- Stylesheet `<link>`s: present on all pages (3 on main, 4 on university, 6 on course, 2 on bootcamp pages, 1 on portfolio); all linked assets curl 200 (incl. `/assets/il-unified.css`, `/university/course-shell.css`, `/university/js/app.js`, `/assets/il-proof.js`, `/bootcamps/_engine/*`).
- `<img>` tags: none with missing/empty `src` on any page.
- Duplicate element IDs: **0** on all pages.
- Tag balance (div/section/main/table open vs close): balanced on all pages.

---

## 7. EXACT BROWSER-CHECK LIST FOR THE PARENT (live browser required)

1. **`/evidence/` — console check:** load `https://interstitiumlabs.dev/evidence/`, open devtools console, confirm `SyntaxError: Unexpected identifier 's'` from `/assets/il-proof.js` and that the "Export inspectable evidence" widget section below the link list is empty. (Post-fix: confirm widget renders and "Download .md" produces a file.)
2. **Course page at 390×844:** load `https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery` at 390px width — confirm `.shell-nav` is hidden, `.mobile-nav` appears, the Brief grid stacks to one column, and there is no horizontal overflow on the mock-exam / lab tabs.
3. **`learn.` / `app.` intent:** load `https://learn.interstitiumlabs.dev/` and `https://app.interstitiumlabs.dev/` — confirm with the owner whether serving the flagship homepage on both is intentional.
4. **Course favicon:** load any `/university/course?course=…` URL — confirm the tab shows the default/missing favicon (V2).
5. **Bootcamp pages at 390px:** load both `/bootcamps/tl-interview/` and `/bootcamps/threatlocker-assessment-prep/` at 390px — confirm the terminal/console panels and lab cards don't overflow horizontally.
6. **Portfolio at 390px:** load `https://enmanueldmejia.com/` at 390px — confirm hero/nav don't overflow (CSS has 900px/560px breakpoints).
7. **No-JS course page:** disable JavaScript, load the IL-29 course URL — confirm the empty-shell outcome is acceptable (R2).
8. **Alt-text spot check:** with a screen reader (or devtools accessibility tree), confirm the `alt=""` sigil/logo images (R1) are decorative-only and no meaningful image lacks a label.
