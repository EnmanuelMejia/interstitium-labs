# Navigation — Least-Clicks Reimagine (2026-10-10)

interstitiumlabs.dev navigation redesigned so **any content is ≤ 2 clicks / 1 gesture from anywhere**, with a global command palette as the zero-click-cost escape hatch.

## Files

| File | Role |
|---|---|
| `docs/assets/il-unified-nav.html` | Canonical nav fragment (source of truth) |
| `docs/assets/il-nav.js` | Mega-dropdown toggles + active-section marking |
| `docs/assets/il-search.js` | Command palette v2 (same filename/hook as v1 — all 70 pages get it) |
| `docs/assets/il-command-palette.css` | Palette styling (desktop panel + mobile bottom sheet) |
| `docs/assets/search-index.json` | Jump index — 111 entries (courses, bootcamps, themes, paths, practice, pages, shortcuts) |
| `docs/assets/il-unified.css` (§N) | Mega-dropdown + ⌘K chip styles |

## Structure

**Desktop pill nav (6 links, unchanged labels):** Courses · Topics · Practice · Noah AI · Jobs · About — each 1 click to its hub.

**Mega-dropdowns (desktop ≥900px, hover or caret-click):**
- **Courses ▾** — 4 flagship courses (IL-26…IL-29), bootcamps (catalog, ThreatLocker assessment prep, TL interview), All courses, Learning paths, My courses, Enroll.
- **Topics ▾** — all **16 themed worlds** directly: Cybersecurity, System Design, Networking, Cloud & DevOps, AI & ML, Data Engineering, Programming, Databases, Linux & Systems, Mathematics (Turing), Web Development, Blockchain, Cryptocurrency, Cybernetics, Esoteric, Om.
- Zero-JS fallback: the main link (Courses → `/university/`, Topics → `/topics/`) still works; the caret is inert without JS.

**Mobile (<900px):** pill links collapse to the MENU sheet, which now carries grouped sections — main 6 links, **Flagships & bootcamps** (7), **Themed worlds** (16), **Account** (Enroll, Log in). Scrollable sheet; the ⌘K palette button stays visible in the nav bar.

**Command palette (Ctrl+K / ⌘K, `/`, or tap):**
- Fuzzy search over the full index: title-start > substring > word-initials > subsequence, AND across tokens, courses/bootcamps/themes boosted.
- Empty state shows **Recent** (localStorage, max 6) + **Jump to** quick actions (IL-26…29, bootcamps, topics, drills, Noah, enroll, login).
- Keyboard: ↑/↓ navigate, ↵ open, ⌘↵ open in new tab, Esc close, light focus trap, aria-live result counts, matched-character `<mark>` highlights.
- Mobile: bottom-sheet layout, 82dvh, ≥48px rows, 16px input (no iOS zoom), safe-area padding, footer hints hidden.
- Index warms on `requestIdleCallback` so first open is instant.

**No redirect-then-render:** every nav/palette URL is the final canonical destination. IL course links point at `/university/course?course=…` (the `/il26`–`/il29` shortcuts still 301 there and keep working for typed/shared use); login points at `/account/` (the `/login` alias still works).

## Click-depth audit (homepage → destination)

| Destination | Before | After | How (after) |
|---|---|---|---|
| University catalog | 1 | 1 | Courses link |
| IL-29 course page | 2–3 | **1** | Courses ▾ → IL-29, or ⌘K "il29" |
| Any flagship (IL-26/27/28) | 2–3 | **1** | Courses ▾, or ⌘K |
| ThreatLocker assessment bootcamp | 3 (Courses → catalog → bootcamp) | **1** | Courses ▾, or ⌘K "threatlocker" |
| Bootcamp catalog | 2–3 | **1** | Courses ▾, or ⌘K "bootcamp" |
| Any of 16 theme pages | 2 (Topics → hub → theme) | **1** | Topics ▾ (all 16 listed), or ⌘K "crypto" |
| Interview drill / lab | 2 (Practice → card) | **1–2** | Practice link, or ⌘K "drill" |
| Learning path | 3+ (buried in hubs) | **1** | ⌘K (all 25 paths indexed) |
| Noah AI | 1 | 1 | Noah AI link |
| Enroll | 1 | 1 | Enroll button / ⌘K "enroll" |
| Evidence (`/proof` alias) | 2 | **1** | ⌘K "proof"/"evidence" → `/evidence/` directly |

**Deep hierarchies flattened:**
1. **Bootcamps** were catalog-gated (3 clicks) → surfaced in the Courses dropdown + palette as first-class destinations.
2. **16 themes** lost their tab strip tonight (user order) → now one hover/click away in the Topics mega-panel, all 16 in the mobile sheet, all in the palette.
3. **25 learning paths** were hub-buried → 1-gesture palette jumps (already indexed).
4. **Shortcut aliases** (`/il26-29`, `/login`, `/os`, `/proof`) still resolve, but nav/palette bypass their 301s and link final URLs.

## Preserved (untouched)

- Cinematic heroes, movie-poster preview cards, floating audio widget — none removed or restyled by this change.
- `/il26-29`, `/bootcamps/` (LinkedIn URL), `/about/`, `/os`, `/proof`, `/login` — all still resolve (worker routes unchanged).
- Dark cinematic aesthetic; IL gold accents; theme toggle injection untouched.

## Mobile-first (390×844)

- MENU sheet: grouped, scrollable, 44px+ touch targets.
- Palette = bottom sheet with grabber, 82dvh max, large rows, keyboard opens on tap-focus, Esc/backdrop-tap closes.
- ⌘K chip hidden ≤640px; the search icon button remains.

## Propagation checklist (for parent orchestrator)

The canonical fragment is updated, but **123 pages inline their own copy** of the nav (per AGENTS.md) plus `university/js/app.js` PILL_LINKS. Follow-up needed:
1. Re-propagate `il-unified-nav.html` to all inlined copies (diff carefully — some pages set `aria-current` per page).
2. Confirm `il-nav.js` loads on fragment consumers (the fragment now includes its `<script>` tag).
3. `il-command-palette.css` self-injects from `il-search.js` as a fallback, so the 70 pages loading `il-search.js` are covered even before propagation.
4. Spot-check on real viewports: 390×844 (bottom sheet, MENU sheet scroll), 1440px (dropdown hover), keyboard-only run (⌘K → type → ↵).

## Verification

- `node --check` on `il-search.js` and `il-nav.js` — pass.
- `search-index.json` — valid JSON, 111 items, types: page 33, path 25, course 19, theme 17, practice 12, bootcamp 2, job 1, ai 1, guide 1.
- Fuzzy scorer tested against the live index: `il29`→IL-29, `threatlocker`→bootcamps, `crypto`→Cryptocurrency theme, `tl`→ThreatLocker trio, `bootcamp`→catalog, `noah`→Noah AI all rank #1.
- Nav fragment: HTML well-formed (balanced tags), 40 links, all final canonical URLs (no 301-hop targets).
