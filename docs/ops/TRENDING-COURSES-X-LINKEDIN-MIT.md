# Trending advanced courses — MIT · LinkedIn · X

**Refreshed:** 2026-09-22 · 12:25 AM ET  
**Catalog:** [`/assets/il-trending-catalog.json`](../assets/il-trending-catalog.json)  
**UI:** [`/paths/frontier/`](../paths/frontier/) · ingest via [`il-trending.js`](../assets/il-trending.js)  
**Join key:** `course.frontierTrackIds[]` ↔ `il-paths.json` → `paths[].frontier_track_ids[]` (shipped in `8b1e5fa`)

## Honesty (Musk bar)

- **No piracy.** External links only. We do not host, rip, or mirror LinkedIn Learning video.
- **No invented MIT numbers.** OCW / Open Learning / public course-site IDs only.
- **No fake viral metrics.** X/public discourse rows have no fabricated likes/impressions.
- **Brand.** Interstitium lockup + cyan / gold / void. Do **not** Meta-skin Frontier or Muse chrome.
- **Muse.** Overlays deep-link `/coach/`. Do **not** edit `il-muse*` (Muse-mobile agent owns that shell).
- **Exceed primary.** Frontier is an ingest sibling; path exceed IA stays primary.

## Counts (this refresh)

| Source | Count | Notes |
|--------|------:|-------|
| MIT (OCW / Open Learning / course sites) | 9 | Real IDs: 6.8300, 6.7960, 6.S191, 6.824, 6.858, 6.033, 6.5940, Missing Semester, MITx 6.86x |
| LinkedIn Learning (public catalog pages) | 7 | LLMOps, SRE, agents/MCP, GitOps/Argo CD, AI eng — video may require a Learning seat |
| X / public discourse signal | 6 | CS329Z, CS224G, CMU MLiP, LF 2026 platform trend, AgentOps×K8s, DevOps+RAG roadmaps — **signal, not enrollables** |
| **Total** | **22** | All 20 non-empty `frontier_track_ids` placeholders covered |

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

Each card can surface **Adapt** (`/adapt/`), **Lab** (`/labs/superlab/`), **Lab Muse** (`/coach/`), plus the path `mapTarget`.  
We adapt/lab/muse around the external course — we do **not** re-host their media.

## Analytics → weekly promote/demote

Events (exact): `frontier_open` · `frontier_click` · `frontier_complete` · `frontier_thumb_up` · `frontier_thumb_down`  
Scores: `localStorage il.frontier.scores.v1`  
Feeds: `il.iterate.v1` recommendations (see `CURRICULUM-ITERATE.md`)

## Refresh playbook

See [`CURRICULUM-ITERATE.md`](./CURRICULUM-ITERATE.md).
