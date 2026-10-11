# INTERSTITIUMLABS.DEV — MAJOR CONSOLIDATION PLAN
**Date:** 2026-10-09 | **Phase:** 1 — AUDIT ONLY (nothing deleted/moved yet)
**Goal:** All content categorized into 16 themes. Dedup. Fewest clicks. Zero broken links.

---

## 1. SUBDOMAIN VERDICTS

All 5 subdomains route to the **same worker** (`solitary-sound-015a`) serving the **same flagship docs**. Verified live — every root returns identical 30633B homepage.

| Subdomain | Worker | Content | Verdict |
|---|---|---|---|
| `interstitiumlabs.dev` (apex) | solitary-sound-015a | Everything | **KEEP** — canonical |
| `www.interstitiumlabs.dev` | solitary-sound-015a | Byte-identical mirror | **KEEP route, canonical-ize** — add 301 www → apex (SEO dedup, zero user impact) |
| `learn.interstitiumlabs.dev` | solitary-sound-015a | Byte-identical mirror (NOT the old university build; `interstitium-labs-university` worker is unrouted) | **301 → apex** — pure duplicate, no unique content |
| `app.interstitiumlabs.dev` | solitary-sound-015a | Byte-identical mirror | **301 → apex** — pure duplicate, no unique content |
| `api.interstitiumlabs.dev` | solitary-sound-015a | Byte-identical mirror (api routes work, but nothing api-only lives here) | **301 → apex** — API paths work on apex already |

**Redirect plan:** Replace the 4 mirror routes with Cloudflare Bulk Redirects (or worker-level 301s):
- `www.interstitiumlabs.dev/*` → `https://interstitiumlabs.dev/$1`
- `learn.interstitiumlabs.dev/*` → `https://interstitiumlabs.dev/$1`
- `app.interstitiumlabs.dev/*` → `https://interstitiumlabs.dev/$1`
- `api.interstitiumlabs.dev/*` → `https://interstitiumlabs.dev/$1`
- Path-preserving (`$1`) so any deep link keeps working.

**Result:** 5 subdomains → 1. No content lost (all mirrors).

---

## 2. SECTION VERDICTS (main site, ~/workspace/apex-audit/docs/)

### KEEP as-is (canonical hubs)
| Section | Pages | Role |
|---|---|---|
| `topics/` | 17 | **THE primary organization** — 16 themed worlds. Everything funnels here. |
| `university/` | 16 | Course catalog (IL courses). Linked from theme pages. |
| `paths/` | 25 | Learning paths. Categorize each path under its theme; keep URLs. |
| `pdf-library/` | 1 | Visual Guide Library. Keep; already theme-filterable. |
| `cinema/` | 1 | Videos hub (nav: "Videos"). Keep. |
| `noah/` | 1 | Noah AI workspace. Keep. |
| `jobs/` | 1 | Jobs. Keep. |
| `about/` | 1 | About. Keep. |
| `enroll/` | 4 | Checkout flow. Keep. |
| `account/` | 1 | Sign-in. Keep. |
| `bootcamp-catalog/` | 1 | Bootcamp listing. Keep; link from Paths hub. |
| `evidence/` | 3 | Proof/social proof. Keep; link from About. |
| `subject-map/` | 1 | MIT-style subject map. Keep; link from Topics hub. |

### MERGE into themes (content kept, URL 301s to theme page)
| Section | Pages | Overlap | Target |
|---|---|---|---|
| `learn/cyber/` | 1 | = Cybersecurity theme | → `/topics/cybersecurity/` |
| `learn/cybernetics/` | 1 | = Cybernetics theme | → `/topics/cybernetics/` |
| `learn/blockchain/` | 1 | = Blockchain theme | → `/topics/blockchain/` |
| `learn/cloud/` | 1 | = Cloud & DevOps theme | → `/topics/cloud-devops/` |
| `learn/data/` | 1 | = Data Engineering theme | → `/topics/data-eng/` |
| `learn/math/` | 1 | = Mathematics (Turing) theme | → `/topics/math/` |
| `learn/turing/` | 1 | = Mathematics (Turing) theme | → `/topics/math/` |
| `learn/esoteric/` | 1 | = Esoteric (John Dee) theme | → `/topics/esoteric/` |
| `learn/hermetica/` | 1 | = Esoteric theme | → `/topics/esoteric/` |
| `learn/dee-court/` | 1 | = Esoteric theme | → `/topics/esoteric/` |
| `learn/systems/` | 1 | = Linux & Systems theme | → `/topics/linux-systems/` |
| `learn/ai-lab/` | 1 | = AI & ML theme | → `/topics/ai-ml/` |
| `learn/career/` | 1 | Career content → Jobs | → `/jobs/` |
| `learn/command/` | 1 | Linux CLI → Linux & Systems | → `/topics/linux-systems/` |
| `learn/forge/` | 1 | Programming practice | → `/topics/programming/` |
| `learn/theory/` | 1 | → Topics hub | → `/topics/` |
| `learn/sequences/` | 32 | Mini-courses — categorize EACH into its theme (see §5) | → per-theme 301s |
| `learn/quantum/` | 1 | → Frontier/Om | → `/topics/om/` (consciousness) or new Frontier theme |
| `learn/philosophy/` | 1 | → Esoteric | → `/topics/esoteric/` |
| `learn/bernays/` | 1 | → Esoteric (hidden knowledge) | → `/topics/esoteric/` |
| `learn/deep-work/` | 1 | → Om (practice) | → `/topics/om/` |
| `learn/study-protocol/` | 1 | → Practice hub | → `/prep/drills/` |
| `learn/skills/` | 1 | → Topics hub | → `/topics/` |

### DELETE (pure redirect stubs — replace with worker 301s)
| Section | Pages | Notes |
|---|---|---|
| `academy/` | 11 | ALL are `<meta refresh>` stubs → /paths/ or /prep/. Replace with worker 301 rules, delete files. |

Redirects: `/academy/career/` → `/paths/`, `/academy/cloud/` → `/paths/devsecops-mastery/`, `/academy/command/` → `/paths/`, `/academy/cyber/` → `/paths/devsecops-mastery/`, `/academy/data/` → `/paths/data-science-certs/`, `/academy/forge/` → `/prep/programming/`, `/academy/hermetica/` → `/paths/enochian-programming/`, `/academy/math/` → `/prep/math/`, `/academy/systems/` → `/prep/devops/`, `/academy/theory/` → `/learn/` (→ then to `/topics/` per learn merge).

### MERGE into Practice hub (keep content, consolidate nav)
| Section | Pages | Notes |
|---|---|---|
| `coach/` | 1 | "Noah AI — your lab-aware coach" — DUPLICATE of `/noah/`. 301 → `/noah/`. |
| `play/` | 1 | Quest Board → merge into Practice hub as a section. 301 → `/prep/drills/`. |
| `adapt/` | 1 | Adaptive Learning OS → merge into Practice hub as a section. 301 → `/prep/drills/`. |
| `labs/` | 4 | Hands-on labs → keep pages, link from Practice hub (already are). No URL change. |
| `prep/` | 8 | The Practice hub itself. Keep. |

### KEEP but delist from nav (already done 2026-10-09)
`learn/` index, `library/`, `/paths/roles/`, `/labs/`, `/coach/`, `/play/`, `/adapt/` — pages stay live, linked from hubs, not in main nav.

---

## 3. DO NOT TOUCH — externally published URLs

These MUST keep working (200 or 301 to equivalent content):

| URL | Published on | Current behavior |
|---|---|---|
| `interstitiumlabs.dev/il26` | X profile | 301 → IL-26 course ✓ |
| `interstitiumlabs.dev/il27` | (short link) | 301 → IL-27 course ✓ |
| `interstitiumlabs.dev/il28` | (short link) | 301 → IL-28 course ✓ |
| `interstitiumlabs.dev/il29` | (short link) | 301 → IL-29 course ✓ |
| `interstitiumlabs.dev/bootcamps/` | LinkedIn | 301 → /bootcamp-catalog/ ✓ |
| `interstitiumlabs.dev/` | X profile | 200 homepage ✓ |
| `interstitiumlabs.dev/about/` | portfolio (enmanueldmejia.com) | 200 ✓ |
| `interstitiumlabs.dev/assets/cards/hq/*` | portfolio embeds | 200 ✓ (all card assets) |
| `/os`, `/proof`, `/login`, `/signin`, `/member` | worker shortcuts (may be published) | 301s ✓ |
| `/bootcamps/threatlocker-assessment-prep/` | (assessment links) | 200 via gateway ✓ — keep route |

**Rule:** Any consolidation redirect MUST be 301 (permanent), path-preserving where possible, and verified live before + after.

---

## 4. FULL REDIRECT MAP (to implement in Phase 2)

### Subdomains (Cloudflare route changes)
```
www.interstitiumlabs.dev/*  →  https://interstitiumlabs.dev/$1  (301)
learn.interstitiumlabs.dev/* →  https://interstitiumlabs.dev/$1  (301)
app.interstitiumlabs.dev/*   →  https://interstitiumlabs.dev/$1  (301)
api.interstitiumlabs.dev/*   →  https://interstitiumlabs.dev/$1  (301)
```

### Academy stubs → worker 301s (delete 11 files)
```
/academy/career/  → /paths/                      (301)
/academy/cloud/   → /paths/devsecops-mastery/    (301)
/academy/command/  → /paths/                     (301)
/academy/cyber/   → /paths/devsecops-mastery/    (301)
/academy/data/    → /paths/data-science-certs/   (301)
/academy/forge/   → /prep/programming/            (301)
/academy/hermetica/ → /paths/enochian-programming/ (301)
/academy/math/    → /prep/math/                   (301)
/academy/systems/ → /prep/devops/                 (301)
/academy/theory/  → /topics/                     (301)
```

### Learn merges → worker 301s (22 subdirs, content absorbed into theme pages)
```
/learn/cyber/       → /topics/cybersecurity/   (301)
/learn/cybernetics/ → /topics/cybernetics/     (301)
/learn/blockchain/  → /topics/blockchain/      (301)
/learn/cloud/       → /topics/cloud-devops/    (301)
/learn/data/        → /topics/data-eng/        (301)
/learn/math/        → /topics/math/            (301)
/learn/turing/      → /topics/math/            (301)
/learn/esoteric/    → /topics/esoteric/        (301)
/learn/hermetica/   → /topics/esoteric/        (301)
/learn/dee-court/   → /topics/esoteric/        (301)
/learn/systems/     → /topics/linux-systems/   (301)
/learn/ai-lab/      → /topics/ai-ml/           (301)
/learn/career/      → /jobs/                   (301)
/learn/command/     → /topics/linux-systems/   (301)
/learn/forge/       → /topics/programming/     (301)
/learn/theory/      → /topics/                 (301)
/learn/quantum/     → /topics/om/              (301)
/learn/philosophy/  → /topics/esoteric/        (301)
/learn/bernays/     → /topics/esoteric/        (301)
/learn/deep-work/   → /topics/om/              (301)
/learn/study-protocol/ → /prep/drills/         (301)
/learn/skills/      → /topics/                 (301)
/learn/             → /topics/                 (301)
/learn/sequences/*  → per-theme 301s (32 individual, mapped in Phase 2)
```

### Practice consolidation
```
/coach/  → /noah/          (301 — duplicate Noah AI page)
/play/   → /prep/drills/   (301 — Quest Board becomes Practice section)
/adapt/  → /prep/drills/   (301 — Adaptive becomes Practice section)
```

---

## 5. THEME MAPPING (16 themes ← content sources)

| Theme | Gets content from |
|---|---|
| Cybersecurity (Mr. Robot) | learn/cyber, paths/devsecops-mastery, sequences: ai-aided-cybersecurity, cybersecurity-projects-lab, cism, cissp |
| System Design (cyberpunk) | paths: system-design content, sequences |
| Networking (Tron) | sequences: networking content |
| Cloud & DevOps (steampunk) | learn/cloud, paths: aws-*, k8s-*, iac-terraform, sequences: ansible-config, azure-az104 |
| AI & ML (Ex Machina) | learn/ai-lab, sequences: agentic-coding-advisor, ai-aided-cybersecurity, ai-product-innovation |
| Data Engineering (ocean) | learn/data, paths/data-*, sequences: database-admin |
| Programming (circuit) | learn/forge, prep/programming, sequences: c-language, cpp-engineering, creative-coding |
| Databases (vault) | sequences: database-admin |
| Linux & Systems (terminal) | learn/systems, learn/command, paths: linux-* |
| Mathematics — Turing | learn/math, learn/turing, prep/math |
| Web Development (vaporwave) | paths: fullstack-*, frontend content |
| Blockchain (ledger) | learn/blockchain, sequences: bitcoin-protocol, crypto-protocols-2 |
| Cryptocurrency (XRP) | sequences: bitcoin-protocol, crypto-protocols-2 |
| Cybernetics (Wiener) | learn/cybernetics |
| Esoteric (John Dee) | learn/esoteric, learn/hermetica, learn/dee-court, learn/philosophy, learn/bernays, paths/enochian-programming |
| Om (consciousness) | learn/quantum, learn/deep-work |

---

## 6. CLICK-COUNT ANALYSIS

| Destination | Before | After |
|---|---|---|
| Any course | Home → Courses → course = **2** | **2** (unchanged) |
| Any theme hub | Home → Topics → theme = **2** | **2** (unchanged) |
| A learn sequence (e.g. CISSP) | Home → Library → ??? → sequence = **4+** (not in nav) | Home → Topics → Cybersecurity → CISSP = **3** |
| Videos | Home → Videos = **1** | **1** (unchanged, renamed from Cinema) |
| Noah AI | Home → Noah AI = **1** | **1** |
| Practice/drills | Home → Practice = **1** | **1** (labs/play/adapt/coach folded in) |
| ThreatLocker bootcamp | External link = **1** | **1** (route kept) |
| Old /learn/cyber/ URL | 200 (duplicate) | 301 → theme = **1** extra hop, same content |

**Net:** Worst-case paths drop from 4+ clicks to 3. No destination gets farther.

---

## 7. PHASE 2 EXECUTION CHECKLIST (not started)

- [ ] Absorb unique learn/ content into theme pages (copy text, don't just redirect)
- [ ] Map all 32 learn/sequences/* to themes (individual 301s)
- [ ] Add worker 301 rules for academy/*, learn/*, coach, play, adapt
- [ ] Delete academy/ + learn/ files AFTER redirects verified live
- [ ] Change 4 subdomain routes to 301 → apex
- [ ] Add www → apex canonical 301
- [ ] Full link audit: every internal link repointed, zero 404s
- [ ] Verify ALL "do not touch" URLs still work live
- [ ] Verify on Philips ultrawide + Pixel + Legion before declaring done
