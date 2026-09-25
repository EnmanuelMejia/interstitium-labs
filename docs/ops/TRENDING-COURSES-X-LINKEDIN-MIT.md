# Trending advanced courses — MIT · LinkedIn · X

**Refreshed:** 2026-09-25 · 6:45 PM ET  
**Previous:** 2026-09-22 · 12:25 AM ET  
**Catalog:** [`/assets/il-trending-catalog.json`](../assets/il-trending-catalog.json)  
**UI:** [`/paths/frontier/`](../paths/frontier/) · [`/trending/`](../trending/) · home `[data-il-trending]`  
**Join key:** `course.frontierTrackIds[]` ↔ `il-paths.json` → `paths[].frontier_track_ids[]`

## Daily fold — 25 Sep 2026

Direction is **X → Interstitium**. Nothing was posted back to X.

| Seated id | Instrument | Parent tracks | Map |
|-----------|------------|---------------|-----|
| `arxiv-2603-18387-mfdl` | Ye, Mathematical Foundations of Deep Learning (arXiv draft) | ai-infra, ml-literacy, ops-math | `/paths/nvidia-ai/` |
| `oss-from-math-to-ml` | Li, Mathematical Pathways to Machine Learning (CC BY-NC) | ops-math, ml-literacy | `/paths/aleks-ops-math/` |
| `mit-ocw-18-100b` | MIT OCW 18.100B Real Analysis notes | ops-math | `/paths/aleks-ops-math/` |
| `arxiv-2601-06108-alignment` | From RLHF to Direct Alignment | ai-infra, ml-literacy | `/paths/nvidia-ai/` |
| `arxiv-2603-15914-agentic-researcher` | The Agentic Researcher | ai-infra, fde | `/coach/` |
| `oss-hinton-pytorch` | Hinton papers replicated in PyTorch (public repo) | ai-infra, ml-literacy, python-systems | `/paths/nvidia-ai/` |
| `arxiv-2609-28835-anomalies` | Pedagogical QFT anomalies | ops-math shelf only | `/paths/aleks-ops-math/` |

Held, not seated: posts with no paper, course, or repository; one vacuum-fluctuation claim not re-checked; Capacitor 6→8 Dependabot PRs (mobile major bumps, separate from this ingest).

Counts after this fold: MIT 10 · LinkedIn 7 · X 6 · arXiv 4 · OSS 2 · total 29.

`il-trending.js` now mounts both `[data-il-frontier]` and `[data-il-trending]`, so the home page and `/trending/` render the same catalog.

## Honesty (Musk bar)

- **No piracy.** External links only. We do not host, rip, or mirror LinkedIn Learning video.
- **No invented MIT numbers.** OCW / Open Learning / public course-site IDs only.
- **No fake viral metrics.** X/public discourse rows have no fabricated likes/impressions.
- **Brand.** Interstitium lockup + cyan / gold / void. Do **not** Meta-skin Frontier or Muse chrome.
- **Muse.** Overlays deep-link `/coach/`. Do **not** edit `il-muse*` (Muse-mobile agent owns that shell).
- **Exceed primary.** Frontier is an ingest sibling; path exceed IA stays primary.

## Counts (catalog after 25 Sep 2026)

| Source | Count | Notes |
|--------|------:|-------|
| MIT (OCW / Open Learning / course sites) | 10 | Prior 9, plus 18.100B Real Analysis |
| LinkedIn Learning (public catalog pages) | 7 | Unchanged this fold |
| X / public discourse signal | 6 | Unchanged this fold |
| arXiv | 4 | Ye draft, alignment survey, agentic researcher, QFT anomalies |
| Open source / open notes | 2 | Li pathways (CC BY-NC), Hinton PyTorch repo |
| **Total** | **29** | Still joined only to existing `frontier_track_ids` |

## MIT (verified public)

| ID | Title | Level | Why advanced | Map |
|----|-------|-------|--------------|-----|
| 6.8300 | Advances in Computer Vision | Grad | Geometry + generative vision + embodied agents | `/paths/nvidia-ai/` |
| 6.7960 | Deep Learning | UG/Grad | Transformers + high-d generalization (OCW) | `/paths/nvidia-ai/` |
| 6.S191 | Intro to Deep Learning | UG advanced | IAP DL intensive gateway | `/paths/nvidia-ai/` |
| 6.824 | Distributed Computer Systems Engineering | Grad | Canonical distributed systems | `/paths/platform-sre/` |
| 6.858 | Computer Systems Security | Grad | Systems security papers → DevSecOps depth | `/paths/devsecops-mastery/` |
| 6.033 | Computer System Engineering | UG core | Complexity + reliability spine | `/paths/kubernetes-sre/` |
| 6.5940 | TinyML and Efficient AI Computing | Grad/PhD | On-device LLM deploy labs (Han Lab site) | `/paths/nvidia-ai/` |
| Missing Semester | Missing Semester of Your CS Education | Practitioner | Shell→git→debug→agentic coding | `/prep/` |
| MITx 6.86x | ML with Python: Linear Models → DL | Advanced | Verified MITx ID; edX run availability varies | `/paths/data-science-certs/` |

## LinkedIn Learning (public catalog; login gaps labeled)

| Title | Level | Map |
|-------|-------|-----|
| Advanced LLMOps: Deploying and Managing LLMs in Production | Advanced | `/coach/` |
| Site Reliability Engineering Essential Training | Intermediate→Advanced | `/paths/platform-sre/` |
| Build with AI: Agentic Applications with LlamaIndex and MCP | Intermediate | `/coach/` |
| Cloud-Based Agentic AI Design Patterns | Advanced | `/paths/platform-sre/` |
| Fundamentals of AI Engineering | Intermediate | `/paths/data-science-certs/` |
| Kubernetes: GitOps with Argo CD | Advanced | `/labs/superlab/` |
| GitOps Foundations | Intermediate | `/paths/iac-terraform-gitops/` |

**Gap:** deep lesson lists / full video often sit behind LinkedIn Learning seats. We cite public landing pages only.

## X / public discourse (signal only)

| Signal | Why it matters | Map |
|--------|----------------|-----|
| Stanford CS329Z Engineering AI Agents | Agent syllabus cited across 2025–26 discourse | `/coach/` |
| Stanford CS224G Building and Scaling LLM Apps | LLMOps production cluster | `/paths/nvidia-ai/` |
| CMU MLiP / AI Engineering (Spring 2026) | End-to-end production AI eng | `/paths/platform-sre/` |
| LF Education 2026: Linux · K8s · Platform under AI load | Official industry trend post | `/paths/k8s-cka-exceed/` |
| Enterprise AgentOps on Kubernetes | AgentOps×observability platform bar | `/paths/kubernetes-sre/` |
| DevOps + RAG + Agent AI 2026 roadmaps | Skill-cluster proxy when X APIs unavailable | `/prep/` |

## Interstitium overlays

Each card can surface **Adapt** (`/adapt/`), **Lab** (`/labs/superlab/`), **Noah** (`/coach/`), plus the path `mapTarget`.  
We adapt/lab/muse around the external course — we do **not** re-host their media.

## Analytics → weekly promote/demote

Events (exact): `frontier_open` · `frontier_click` · `frontier_complete` · `frontier_thumb_up` · `frontier_thumb_down`  
Scores: `localStorage il.frontier.scores.v1`  
Feeds: `il.iterate.v1` recommendations (see `CURRICULUM-ITERATE.md`)

## Refresh playbook

See [`CURRICULUM-ITERATE.md`](./CURRICULUM-ITERATE.md).
