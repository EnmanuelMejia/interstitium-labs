# Competitive audit (extended) — Adaptive Learning OS

_Last updated: 2026-09-21 (America/New_York)._  
_Static root:_ `docs/` · _Live:_ https://interstitiumlabs.dev  
_Research seed:_ `/workspace/interstitium-research/competitive-research-2025-2026.md` + `gap-matrix.json`

Brand kit stays **private**. Payments stay placeholder-honest. **No invented Stripe/LLM keys. No fake 800-cloud-VM fleet.**

---

## Honest framing

| They win | We exceed (shippable now) |
|----------|---------------------------|
| Vendor portals: official certs, proctored exams, cloud accounts, hosted playgrounds | **Portfolio Learning OS** + **local adaptive engine** (CAT-like + ALEKS fringe) + **SuperLab honesty** + vendor-map orchestration |
| KodeKloud / Skills Boost / AWS: live sandboxes | One deep cloneable SuperLab + BYO-lab rubrics — labeled, not inflated |
| Codecademy / Oracle: polished lesson chrome + AI assistants | Instruction → check → Socratic feedback → next (local); AI coach stub without fake keys |
| GMAT / ALEKS: calibrated high-stakes engines | Portable 2PL + knowledge DAG in the browser; author-estimated `a,b` (not online IRT service) |

**Non-goals:** real cloud provisioning, online IRT calibration service, replacing proctored RH/AWS/LF exams.

---

## Matrix vs peers (1–5, honest)

| Dimension | IL | Codecademy | KodeKloud | DevOps.com | LF Training | Cloud Acad / Skills Boost | Red Hat | Oracle U | AWS Skill Builder | GMAT-CAT | ALEKS |
|-----------|---:|----------:|----------:|-----------:|------------:|--------------------------:|--------:|---------:|------------------:|---------:|------:|
| Lesson chrome / IDE loop | 3 | **5** | 4 | 1 | 4 | 4 | 4 | 4 | 4 | 2 | 3 |
| Lab / playground fleet | 2 | 2 | **5** | 1 | **5** | **5** | **5** | 4 | **5** | 1 | 1 |
| Official certs / proctoring | 1 | 2 | 4 | 1 | **5** | 4 | **5** | **5** | **5** | **5** | 3 |
| Adaptive personalization | **4** | 3 | 3 | 1 | 2 | 3 | 2 | 3 | 3 | **5** | **5** |
| Knowledge graph / fringe | **5** | 3 | 2 | 1 | 3 | 3 | 3 | 2 | 2 | 2 | **5** |
| Mastery gates (not watch-time) | **4** | 3 | 3 | 1 | 3 | **4** | **5** | 3 | **4** | 4 | 4 |
| Portfolio / Student Zero honesty | **5** | 2 | 3 | 2 | 3 | 2 | 3 | 2 | 2 | 1 | 1 |
| Media / community | 1 | 3 | **5** | **5** | 3 | 3 | 3 | 2 | 3 | 1 | 2 |
| Commerce polish | 2 | **5** | **5** | 2 | **5** | **5** | **5** | **5** | **5** | **5** | **5** |
| Runs offline / inspectable static | **5** | 2 | 1 | 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

**Composite read:** Vendors win on **certs + cloud accounts**. Interstitium leads on **orchestrating an adaptive local Learning OS** that deepens into those portals via `/paths/vendor-map/` — without cloning cert IP or faking infra.

---

## Gap order shipped this pass

| ID | Feature | Status |
|----|---------|--------|
| GAP-KG | Knowledge DAG + Known/Learning/Locked fringe | **Shipped** — `il-item-bank.json` concepts + `ILAdaptive.readyTopics()` |
| GAP-ITEM-BANK | Calibrated items (a,b,c, concepts, exposure) | **Shipped** — 30 concepts, 58 quality items (structure → 150) |
| GAP-CAT-NEXT | 2PL info-max next + domain quotas | **Shipped** — `selectNextItem` in `il-adaptive.js` |
| GAP-PLACE | Placement seeds KG (8–12 items) | **Shipped** — `ILAdaptive.place()` |
| GAP-GATES | Role path mastery gates | **Shipped** — 2 paths × 4 gates |
| GAP-SR | Spaced revisit on mastery decay | **P1 shipped lite** — decay nudge + due-known preference in practice |

---

## Surfaces

| Surface | Path |
|---------|------|
| Adaptive session + pie | `/adapt/` |
| Vendor deepen map | `/paths/vendor-map/` |
| Engine | `docs/assets/il-adaptive.js` |
| Bank | `docs/assets/il-item-bank.json` |
| Prior audit | `docs/ops/COMPETITIVE-AUDIT.md` |

---

## CAT + ALEKS mechanics (one paragraph)

Placement runs a short CAT-like probe: after each response we update a 2PL ability estimate θ and pick the next unused item that maximizes Fisher information near θ while balancing domains and exposure; 8–12 items (or earlier if SE shrinks) seed per-concept mastery via a BKT/Elo blend. Practice mode only prioritizes the ALEKS-style **ready-to-learn fringe** (prerequisites ≥ threshold), demotes on misses, and periodically resurfaces Known topics when mastery soft-decays over days — Knowledge Check without an online IRT service. Role paths (**Platform Associate** → **Platform Engineer**) unlock via mastery gates (and challenge tallies), never watch-time. Vendor portals remain the official cert/cloud deepeners; Interstitium is the adaptive OS that decides *what* to practice next on-device (`il.adaptive.v1`).

---

## Steal sheet (portable only)

- **Codecademy:** lesson chrome instruction → check → feedback → next (wired on `/adapt/`).
- **KodeKloud:** scenario clarity; we map to SuperLab + honest “needs infra” labels.
- **DevOps.com:** signal → skill cards later; not a news clone.
- **LF / RH / AWS / Oracle / Cloud Academy:** blueprint domains → our DAG tags + vendor-map links.
- **GMAT:** info-max selection + content quotas.
- **ALEKS:** fringe + pie + placement Knowledge Check.

---

## Residual needing Enmanuel

- Live Stripe / PayPal (`paymentsLive`)
- Real LLM coach endpoint (`IL_COACH`) — keys out-of-band
- Cloud playground fleet / multi-lab infra
- Offline IRT recalibration from anonymized response logs (optional)
- Store publish accounts
