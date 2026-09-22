# Paths competitive clone — architecture only

_Last updated: 2026-09-22 (America/New_York)._  
_Static root:_ `docs/` · _Live:_ https://interstitiumlabs.dev/paths/  
_Schema:_ `docs/assets/il-paths.json` · _Runner:_ `docs/assets/il-paths.js` (`il.paths.v1`)

**Policy:** Clone **path architecture** (phases, skills, outcomes, gates) — **not** proprietary course text, videos, or trademarks.  
**Musk bar:** each path’s first screen answers **what will I be able to DO?** Inevitable · fast · measurable.

---

## Matrix

| Competitor path (taxonomy) | Interstitium path id | What we clone (architecture) | How we exceed |
|----------------------------|----------------------|------------------------------|---------------|
| KodeKloud K8s / DevOps learning paths | `kubernetes-sre`, `devops-zero-to-hire`, `devsecops-mastery` | Phased skills → labs → cert-shaped outcomes; playground-centric sequencing | Adapt gates + Muse prompts + mandatory evidence portfolio; honest single SuperLab (no fake fleet) |
| ALEKS knowledge-space mastery paths | `adaptive-foundations` | Placement → ready-to-learn fringe → mastery checks | Direct handoff into hireable tech paths; local CAT already shipped; no worksheet mill |
| Brilliant guided problem paths | `adaptive-foundations` (+ drills on `/adapt/`, `/prep/drills/`) | Short problem loops, visible next action | Career DO outcomes on every card; Muse side-quests; time-to-value labels |
| Khan course mastery paths | `adaptive-foundations`, `data-analyst-to-ml`, `linux-lf-essentials` | Mastery units, clear progress | Local `il.paths.v1` phase checks + evidence notes; XP secondary to skill signal |
| Codecademy career paths | `devops-zero-to-hire`, `data-analyst-to-ml`, `bny-fullstack` | Role-shaped multi-week career arcs | JD/STAR interview surface + portfolio honesty; no binge video wall |
| Linux Foundation cert paths | `linux-lf-essentials`, `kubernetes-sre` (+ `vendor-map`) | Essentials → professional cert sequencing | Shell proof mandatory; vendor-map orchestrates official LF — never clones exam IP |
| Red Hat Learning role paths | `linux-lf-essentials`, `kubernetes-sre`, `devsecops-mastery` | Role paths (sysadmin → platform) | Local kind/SuperLab proof spine; RH content stays at vendor |
| Oracle University (role / Java / data) | `bny-fullstack`, `data-analyst-to-ml`, `vendor-map` | Role curriculum maps | JD-mapped fintech full-stack; data path prefers proof over cert bingo |
| AWS Skill Builder role / learning plans | `aws-cloud-practitioner-plus` | Role plans, CLF-shaped service map | Local conceptual twin + explicit free-tier optional; honest “no hosted AWS sandbox” |
| Cloud/DevOps.com–style tracks | `devops-zero-to-hire`, `devsecops-mastery` | Practitioner track chrome | Evidence > media signal; Student Zero narrative; no news clone |
| Coursera / Google / IBM DS ladders | `data-analyst-to-ml` (native), `data-science-certs` (reference) | Cert ladder phases | Analyst→ML literacy with model cards; cert page nested as reference only |

---

## Exceed playbook (shared)

| Lever | Implementation |
|-------|----------------|
| Clearer outcomes | Hero `hero_do` on every path page + directory card |
| Adaptive placement gates | CTAs → `/adapt/` with `adapt_topics[]` per phase |
| Lab proof hooks | CTAs → `/labs/superlab/` (+ prep labs); “Prove it” checklist |
| Muse coaching hooks | `muse_prompts[]` → `/coach/?q=` |
| Time-to-value | `duration_weeks` + `time_band` filters on directory |
| Evidence portfolio | Phase evidence strings + local evidence log (`il.paths.v1`) |
| Honesty about gaps | `honest_gaps[]` rendered on each path; vendor-map for official seats |

**Explicitly not cloned:** course transcripts, video, trademarks, exam dumps, “800 labs” wallpaper.

---

## Directory IA

Filters on `/paths/`: **role · skill · cert · time** (+ search). EN/ES via `title_es` / `tagline_es` / `hero_do_es` and chrome i18n.

**Core (featured):**  
`devops-zero-to-hire` · `kubernetes-sre` · `adaptive-foundations` · `devsecops-mastery` · `aws-cloud-practitioner-plus` · `linux-lf-essentials` · `data-analyst-to-ml`

**Nested (kept):**  
`bny-fullstack` · `fde-training` · `nvidia-ai` · `enochian-programming` · `data-science-certs` (reference) · `vendor-map` (reference)

---

## Musk verdict (paths alone)

**Closer, not YES.** Architecture now beats catalog-site path IA (phases + gates + proof + honesty). Still NO on Musk overall until live Muse, deeper lab fleet, and a 30-day hire loop proven end-to-end. Paths score: **architecture 8/10 · density 5/10 · honesty 9/10**.

---

## Sign-off

Clone structure. Ship proof. Never wallpaper course count.

---

## Frontier track mapping (sibling ingest)

Paths carry optional `frontier_track_ids[]` in `il-paths.json`. When the MIT/LinkedIn/X Frontier ingest sibling lands artifacts (e.g. `/frontier/` or ingest JSON), these IDs are the join keys.

| Path id | frontier_track_ids (placeholders) |
|---------|-----------------------------------|
| devops-zero-to-hire | frontier-cloud-devops-junior, frontier-platform-basics |
| kubernetes-sre / k8s-cka-exceed | frontier-k8s-sre, frontier-reliability |
| adaptive-foundations / aleks-ops-math | frontier-ops-math, frontier-cs-fringe |
| aws-cloud-practitioner-plus / aws-cloud-ops | frontier-aws-clf, frontier-aws-ops, frontier-cloud-fluency |
| data-analyst-to-ml | frontier-data-analyst, frontier-ml-literacy |
| … | see `il-paths.json` |

**Rule:** Exceed architecture is primary. Do not block path shipping on Frontier ingest. Blend when present.

## Parallel cohort

`il-paths-catalog.json` + `il-paths-dir.js` (sibling/prior) remain for exceed-card chrome. Canonical schema for phases/gates/Muse/evidence is **`il-paths.json` + `il-paths.js`** (`il.paths.v1`).
