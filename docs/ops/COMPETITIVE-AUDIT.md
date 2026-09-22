# Competitive audit — Interstitium Labs vs peer Learning OS

_Last updated: 2026-09-21 (America/New_York)._  
_Static root:_ `docs/` · _Live:_ https://interstitiumlabs.dev  
_Peers scored:_ **KodeKloud (primary)**, ALEKS, Brilliant.org, Khan Academy.

Brand kit stays **private** (`private/brand/`, `docs/ops/BRAND-PRIVATE.md`). Payments stay placeholder-honest. No invented Stripe/LLM keys. Enterprise security headers preserved.

---

## 1. Inventory — what Interstitium actually has today

| Surface | Path | Status |
|---------|------|--------|
| Home + Why-vs-video-LMS strip | `/` `#why-interstitium` | Shipped; P0 elevates differentiation |
| Founders Learning OS | `/founders/` | Student Zero, skills radar, weekly OS, quests, proof wall |
| Curriculum OS | `/learn/` + `/learn/skills/` | Outcome cards, sigil pillars (honest forthcoming), skills taxonomy |
| Prep sprint | `/prep/` (+ math / programming / devops / drills) | 3-phase JD-mapped interview crush |
| Paths | `/paths/*` | DevSecOps Mastery, BNY Full-Stack, FDE, DS certs, NVIDIA AI, Enochian+code |
| Labs hub + SuperLab | `/labs/`, `/labs/superlab/` | Flagship cloneable lab — **not** 800 cloud playgrounds |
| Play XP | `/play/` | Local XP / quests / `il.game.v1` |
| Enroll | `/enroll/` | UI + `config.js`; `paymentsLive: false` |
| Admin insights | `/admin/`, `/admin/insights/` | CSP-safe local insights |
| i18n | `/i18n/*.json` + `il-i18n.js` | 10 locale packs |
| Analytics | `il-analytics.js` | First-party, config-gated |
| Mobile | `apps/mobile/` Capacitor | Security docs; store publish needs Enmanuel accounts |
| Coach / AI tutor | `/coach/` | **P0:** UI shell + local rule hints (CIDR, Git, K8s pods) |
| Measure / adaptive engine | SPA fiction routes on home (`/measure`, `/desk`) | Static OS uses founders radar; reusable radar elevated P0 |
| Video LMS / CDN lectures | — | **Not shipped** (honest gap) |
| Cloud playground infra | — | **Not shipped** (honest: SuperLab is local/kind clone) |

---

## 2. Scorecard (1–5, honest)

**IL** = Interstitium baseline before this P0 polish (P0 moves Design/UI/UX/Coach/Labs hub up one notch each without fake infra).

| Dimension | IL | KodeKloud | ALEKS | Brilliant | Khan | Notes |
|-----------|---:|----------:|------:|----------:|-----:|-------|
| Design system | 3 | 4 | 3 | **5** | 4 | Void/cyan/gold tokens exist; need Brilliant hierarchy + drill chrome |
| UI polish | 3 | 4 | 3 | **5** | 4 | Cards solid; empty states & micro-feedback thin |
| UX flows | 3 | 4 | 4 | **5** | **5** | Sequencer exists; “next action” not always obvious |
| Labs | 2 | **5** | 1 | 2 | 2 | SuperLab flagship only vs KodeKloud playground fleet |
| Simulations | 2 | **5** | 2 | **5** | 3 | Interactive visuals sparse outside motion/game |
| Lectures / video | 1 | **5** | 2 | 3 | **5** | No first-party video CDN |
| AI-first tutoring | 1 | **5** | 2 | 3 | 4 | P0 ships `/coach/` shell + local rules — not a live model |
| Adaptive paths | 2 | 3 | **5** | 4 | 4 | Founders radar = seed; not ALEKS Pie engine |
| Gamification | 3 | 4 | 2 | 4 | **5** | Play XP live; keep skill signal > Gems noise |
| Mobile | 3 | 3 | 3 | 4 | **5** | PWA + Capacitor; store publish pending |
| a11y | 3 | 3 | 3 | 4 | **5** | Focus rings partial; Khan-grade a11y is the bar |
| Onboarding | 3 | 4 | 4 | **5** | **5** | Student Zero narrative strong; first-session loop weak |
| Search | 1 | 4 | 3 | 3 | 4 | No site search |
| Progress analytics | 3 | 4 | **5** | 4 | **5** | Local `il.progress.*` + admin insights |
| Community | 1 | **5** | 2 | 3 | 4 | No forums/Discord productized |
| Trust / honesty | **5** | 4 | 4 | 4 | **5** | Portfolio labeling; no fake BNY employment — IL lead |
| Performance | 4 | 4 | 3 | 4 | 4 | Static + CSP; heavy SPA chrome on index |
| i18n | 3 | 3 | 2 | 3 | **5** | 10 locales; chrome coverage uneven |
| Enroll / commerce | 2 | **5** | **5** | **5** | 3 | Placeholder Payment Links only (by design) |

**Composite:** IL **leads** on trust + Student Zero Learning OS. **Trails** on lab fleet, video, AI depth, Pie engine, community, commerce.

---

## 3. Competitive steal sheet (2025–2026 research)

### PRIMARY PEER — KodeKloud
- Guided labs + playgrounds + **in-lab AI Tutor** that sees lab state.
- **Steal:** Playground hub IA; scenario cards that deep-link one real lab; honest “needs infra” labels.
- **AI bar:** lab-state-aware Socratic when a real model is wired — never a wallpaper chatbot.
- **Do not fake:** 800 labs, cloud sandboxes, or live AI keys.

### Brilliant.org
- Interaction density, visual hierarchy, calm motion, micro-feedback; Koji-class **UI-grounded Socratic**.
- **Steal:** Spacing/type scale, interactive drill cards, empty states, focus rings, ask-about-what’s-on-screen hints.

### ALEKS
- Knowledge Space Theory — **Pie**, Knowledge Checks, ready-to-learn fringe.
- **Steal:** Reusable readiness radar/pie on `/learn/` + `/prep/`; Checkpoint ≈ Knowledge Check.

### Khan Academy
- Mastery states, **Missions** queue, coach overlay, a11y, Gems motivation **without drowning skill signal**.
- **Steal:** Explicit **Learn → Practice → Checkpoint** + clear next action; coach overlay UI; XP secondary to mastery.

### AI bar (industry)
Target: **lab-state-aware Socratic ∩ UI-grounded ∩ persistence coach**.  
Ship now: local rule hints + `/coach/` stub + optional `window.IL_COACH`. **No fake API keys.**

---

## 4. Gap matrix

| Gap | Leader | IL today | Pri | Owner |
|-----|--------|----------|-----|-------|
| Visual hierarchy + drill micro-feedback | Brilliant | Partial tokens | **P0** | `il-ux.css` + `il-drills.js` |
| Mastery loop UI (Learn→Practice→Checkpoint) | Khan | Implicit phases | **P0** | `il-mastery.js` on learn/prep |
| Reusable knowledge pie / readiness radar | ALEKS | Founders-only | **P0** | `il-radar.js` |
| Labs playground hub + scenario cards | KodeKloud | SuperLab only | **P0** | `/labs/` |
| AI coach UI shell + local Prep hints | KodeKloud∩Khan | Missing | **P0** | `/coach/` + `il-coach.js` |
| Home competitive strip | — | Basic | **P0** | `#why-interstitium` |
| First-party video / lecture CDN | Khan / KodeKloud | None | **P1** | Enmanuel |
| Real LLM tutor (lab-state + UI-grounded) | KodeKloud | Rules only | **P1** | Enmanuel (keys out-of-band) |
| Cloud playgrounds / multi-lab fleet | KodeKloud | SuperLab clone | **P1** | Enmanuel (infra) |
| Site search | KodeKloud / Khan | None | **P1** | Eng |
| Live Commerce | All commercial | Placeholder | **P1** | Enmanuel Payment Links |
| Store publish | Khan | Capacitor ready | **P1** | Enmanuel Apple/Google |
| Community | KodeKloud | None | **P2** | Product |
| Full ALEKS adaptive engine | ALEKS | Radar seed | **P2** | Research |
| Cohort cloud analytics | Khan / ALEKS | Local only | **P2** | Backend |

---

## 5. P0 shipped this pass

1. Design/UX — `docs/assets/il-ux.css`
2. Mastery loop — `il-mastery.js` on `/learn/` + `/prep/`
3. Readiness radar — `il-radar.js` on learn + prep
4. Labs hub — SuperLab + scenario cards (checklist → SuperLab); honest infra note
5. `/coach/` shell — “AI coach coming online” + local hints (CIDR, Git, K8s pods) + `window.IL_COACH`
6. Drill cards — `il-drills.js` micro-feedback
7. Home `#why-interstitium` strip — Learning OS + SuperLab vs video LMS (not 800 labs)

---

## 6. Residual P1 needing Enmanuel

- Video lecture hosting / CDN
- Real LLM API (`IL_COACH.endpoint`); keys never in repo
- Cloud playground / multi-lab infra
- Live Stripe + PayPal URLs (`paymentsLive: true` only after paste+test)
- Apple/Google store accounts (`STORE-PUBLISH.md`)
- Optional Cloudflare Access on `/admin/`

---

## 7. Honesty constraints

- No fake BNY employment or production tenure
- SuperLab = portfolio / interview demo
- Payments inactive until operator enables
- Brand masters stay out of public Pages
- Preserve `docs/_headers` + Worker security snippet


---

## 8. Exceed map (what we ship that peers underweight)

| Peer strength | Interstitium exceed move (shipped) |
|---------------|-------------------------------------|
| Brilliant interaction | `il-drills.js` cards + instant ok/bad feedback + tips without answer dumps |
| ALEKS Pie / ready-to-learn | `il-radar.js` on Learn + Prep + Founders; clickable self-rate; mid-band fringe copy |
| Khan mastery queue | `il-mastery.js` Learn→Practice→Checkpoint + persistent next-action CTA |
| KodeKloud playgrounds | `/labs/#playground` guided vs playground split + scenario cards → SuperLab; honest infra note |
| KodeKloud in-lab AI | `/coach/` local Socratic rules (CIDR/Git/K8s/Terraform/CI/Linux); `window.IL_COACH` stub; no fake keys |
| Trust | Portfolio honesty, placeholder payments, private brand kit, CSP headers preserved |

**Still behind (P1 — Enmanuel):** hosted cloud playground fleet, real LLM tutor with lab-state, video CDN, live Stripe links, store publish.
