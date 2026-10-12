# Template & Embed 1000% Expansion — 2026-10-09

User order: "Same for the template and embeds you really feel you built enough"

## Template audit (coordinator)

### Course renderer (docs/university/course-shell.js) — BEFORE
Rendered: videos, quiz, flashcards (cards), drills, handsOnLab, glossary, mockTask.
NOT rendered: **m.pdfs[]** (71 refs wired, all invisible), m.audio[] (unsupported).

### Course renderer — AFTER (this session)
- Added `il26_renderModulePdfs()` — "Visual guides" section per module (Open guide + Download PDF).
- Added `il26_renderModuleAudio()` — "Audio" section per module; staged message when TTS down.
- Wired into IL-27 ungated path AND the stage-gated reading stage (non-gating).
- node --check passed.

### Bootcamp engine (site/bootcamps/_engine/learn.js) — BEFORE
Rendered: media[] SVG diagrams per lesson, resources (cheatsheet/glossary/links/checklist).
NOT rendered: **pdfGuides[]** (331 refs wired, all invisible).

### Bootcamp engine — AFTER (this session)
- Added "VISUAL GUIDES" panel at top of Resources tab rendering S.content.pdfGuides[].
- node --check passed.

## Coverage baselines (pre-fill)
- Courses: 804 modules, 0 with zero embeds. PDF gaps: il-01/02/09/10/18/20/21/22/23 = 0 pdfs; others 2-6.
- Bootcamps: 135 with content.json; 532 domains, 419 (78%) with media[] diagrams; 24 bootcamps zero-media; 44 domains missing diagrams.

## Gap-fill workers (5, spawned 2026-10-09 ~01:50 EDT)
- C1 (IL-01–IL-06): PDFs + quiz/cards/drills depth
- C2 (IL-07–IL-12): PDFs + quiz/cards/drills depth
- C3 (IL-13–IL-20): PDFs + quiz/cards/drills depth
- C4 (IL-21–IL-29): PDFs + quiz/cards/drills depth
- B1 (bootcamps): SVG media[] for 24 zero-media bootcamps + 44 missing domains

Each appends its section below on completion.
---

## Worker reports

### C3 — IL-13–IL-20 PDF embed gap fill (completed 2026-10-09 ~01:53 EDT)

**Scope:** 8 courses, 327 modules. Backups: `.work/course-json-backups-embed/` (8 `.json.bak`).

**Depth check result:** every module already met the depth bar (quiz 9–12, cards 12, drills 2 per module) — verified by assertion in the fill script and re-verified against backups. No quiz/card/drill content added or changed; untouched fields byte-identical to backup (videos, handsOnLab, quiz, cards, drills).

**PDF gap fill (the only work needed):** pre-existing totals were sparse (il-13: 3, il-14: 4, il-15: 3, il-16: 3, il-17: 2, il-18: 0, il-19: 4, il-20: 0 across 327 modules). Added 962 new PDF refs via keyword→topic matching on module titles with per-course fallback priority; preserved all 19 pre-existing refs (dedupe by URL). Final: **981 PDF refs, exactly 3 per module** (avg 3.00).

Matching highlights (spot-checked): Containers and Orchestration → kubernetes/cloud-patterns/cicd-pipeline; IAM Deep Dive → oauth-flows (kept pre-existing kubernetes); Streaming Systems → stream-processing/etl-pipelines/data-warehouses; Transformer Architectures → transformers/neural-networks/ml-pipelines; Auth and Identity → oauth-flows/microservices/caching-cdn; Load Balancing & Traffic Management → load-balancing/cloud-patterns/kubernetes. Manual fixup: il-17 "Trust and Guardrails" and "Governance" swapped fallback pick for bbg-zero-trust (topic-correct). DSA/math-only modules (il-13 DSA set, il-20) use the PDF-library index fallback order per the brief.

**Per-course adds:**
- il-13-software-engineering-interview-prep: 58 modules, +171 refs
- il-14-sre-devops-cloud-security-interview-prep: 31 modules, +89 refs
- il-15-data-engineering-analytics-interview-prep: 32 modules, +93 refs
- il-16-machine-learning-ai-engineering: 46 modules, +135 refs
- il-17-agentic-ai-engineering: 45 modules, +133 refs (incl. zero-trust fixup)
- il-18-technical-leadership-interview-prep: 32 modules, +96 refs (was 0)
- il-19-multicloud-devops-ai-bootcamp: 67 modules, +197 refs
- il-20-mathematics: 16 modules, +48 refs (was 0)

**Scripts:** `.work/pdf-gapfill-20261009.py` (matcher), `.work/pdf-gapfill-fixup-20261009.py` (zero-trust swap), `.work/pdf-gapfill-20261009.log` (per-module additions, 962 lines). Every write validated with `json.load` immediately.

**Deploy:** flagship deploy-worker-assets 2026-10-09T05:46:37Z, worker solitary-sound-015a, **etag=95acb862e03f** (15 files uploaded).

**Verification:** curl → 200 on bbg-microservices.pdf, bbg-stream-processing.pdf, bbg-zero-trust.pdf. Live asset pipeline confirmed via free-course JSON (il-29 → 200, 48 modules). il-17 raw JSON curl returns 402 `payment_required` — that is the designed paywall fail-closed behavior for paid courses, not a deploy failure.

**Rules compliance:** original content only (library titles/blurbs reused verbatim); no invented facts, addresses, or credentials.

### C1 — IL-01–IL-06 PDF embed gap fill (completed 2026-10-09 ~01:55 EDT)

**Scope:** 6 courses, 47 modules. Backups: `.work/course-json-backups-embed/` (6 × `.bak.20261009`).

**Depth check result:** every module already met the depth bar (quiz 10, cards 12, drills 2 per module) — verified by assertion in the fill script; nothing added or changed there. Diff vs backup confirms **only `modules[].pdfs[]` changed**; videos, handsOnLab, quiz, cards, drills, glossary byte-identical.

**PDF gap fill (the only work needed):** pre-existing totals: il-01: 0, il-02: 0, il-03: 2, il-04: 5, il-05: 6, il-06: 5 across 47 modules. Added **76 new PDF refs** (dedupe by URL slug; all pre-existing refs preserved). Final: **94 PDF refs, exactly 2 per module** (avg 2.00).

Matching (topic-matched where the 18-guide library allows; esoteric/math modules use the pdf-library index fallback order per the brief — C3 used the same convention for il-20):
- il-01: Logic & Boolean Algebra → tcp-handshake, dns-resolution; Number Theory → pki-encryption, tls-handshake (module covers toy RSA); Hermetic Foundations → load-balancing, caching-cdn; Enochian → microservices, cloud-patterns; CCRU Seminar → stream-processing, ml-pipelines
- il-02: Logic & Boolean Algebra → tcp-handshake, dns-resolution; Probability & Statistics → ml-pipelines, data-warehouses; Unified Mathematical Spine → neural-networks, ml-pipelines; Tech Math → etl-pipelines, data-warehouses; Electrician Apprenticeship → load-balancing, caching-cdn; Quantitative Finance → stream-processing, data-warehouses
- il-03: Discrete Math (+neural-networks); Number Theory (+pki-encryption); Programming Backbone → cicd-pipeline, microservices; Systems Software → cloud-patterns, caching-cdn; MIT 6-3 Reference → tcp-handshake, dns-resolution; Generative Art → neural-networks, transformers
- il-04: Binary/Hex (+tcp-handshake); Logic (+dns-resolution); Linux (+cicd-pipeline); Windows (+oauth-flows); Networking Core (+tcp-handshake); RHCE Ansible → cicd-pipeline, kubernetes
- il-05: Probability & Statistics (+data-warehouses); Graphs (+microservices); DevOps Parity (+cicd-pipeline); K8s Cert Stack (+kubernetes); Zero-Trust Platform (+zero-trust); Terraform (+cloud-patterns); AWS SAA → cloud-patterns, load-balancing; AWS SysOps → cicd-pipeline, caching-cdn; AWS DOP → cicd-pipeline, kubernetes; AWS Security → zero-trust, pki-encryption; AZ-104 → cloud-patterns, caching-cdn; AZ-305 → cloud-patterns, load-balancing; AZ-700 → tcp-handshake, dns-resolution; OpenShift → kubernetes, microservices; Vault & Consul → pki-encryption, oauth-flows; Cloud-Native Associate → kubernetes, cloud-patterns
- il-06: Number Theory (+pki-encryption); Logic (+dns-resolution); Probability & Statistics (+ml-pipelines); Hackers-Arise Spine (+oauth-flows); Offensive Ops (+tls-handshake); Defensive Ops → zero-trust, stream-processing; Forward-Deployed Interface → microservices, cloud-patterns; Sentinel SC-200 → stream-processing, etl-pipelines

**Scripts:** `.work/il01-il06-pdf-embed.py` (assignment + assertion). Every write validated with `json.load` immediately; diff-vs-backup verified post-write.

**Deploy:** git commit `08406af`; flagship deploy-worker-assets 2026-10-09T05:47:49Z, worker solitary-sound-015a, **etag=95acb862e03f** (7 files uploaded).

**Verification:** all 18 library PDFs curl → 200 (pre-wire); post-deploy curl → 200 on bbg-pki-encryption.pdf, bbg-kubernetes.pdf, bbg-ml-pipelines.pdf. Paid-course raw JSON curl returns 402 `payment_required` — the designed paywall fail-closed behavior (confirmed in `docs/_worker.js` `json402Response`), not a deploy failure; course page and pdf-library index serve normally.

**Rules compliance:** original content only (library titles/blurbs reused verbatim); no invented facts, addresses, or credentials.
### C2 (IL-07..IL-12) — PDF gap fill (completed 2026-10-09 ~01:55 EDT)

**Scope:** all 129 modules across the 6 assigned courses now carry 2-3 visual PDF guides each (373 new `modules[].pdfs[]` entries). Depth check passed: every module already had 10 quiz / 12 cards / 2 drills (spec: 3+/5+/1+) — no additions needed. Videos, handsOnLab, glossary verified byte-identical against pre-edit backups (only `pdfs` touched).

**Method:** keyword scoring of module id+title against the 18-guide PDF library (title/url/blurb reused from existing entries; `pages:8, animated:true, source:Interstitium Labs`), existing PDFs preserved, course-level fallbacks for weak matches. Three bad matches caught on review and fixed before deploy: `rag` substring firing inside "storage" (now word-boundaried), `model` firing on "maturity model", `bi` firing inside "binary".

#### il-07: 11 modules
- **Probability & Statistics** (`il-07-data-engineering-analytics-ai-math-stats`) → Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Linear Algebra Foundations** (`il-07-data-engineering-analytics-ai-math-linalg`) → Neural Networks — Visual Guide, Data Warehouses & Lakehouses — Visual Guide
- **Document Databases: MongoDB** (`il07-mongodb`) → ETL Data Pipelines — Visual Guide, Stream Processing — Visual Guide
- **The Data-School Spine** (`il07-data-schools`) → Stream Processing — Visual Guide, Data Warehouses & Lakehouses — Visual Guide
- **Machine Learning and LLM Engineering** (`il07-ai-ml`) → ML Training Pipelines — Visual Guide, Transformers & Attention — Visual Guide
- **NeuroAI: Brain Principles in Computing** (`il07-neuroai`) → Neural Networks — Visual Guide, ETL Data Pipelines — Visual Guide
- **Open-Weight Models & Self-Hosting** (`il07-openweight`) → ETL Data Pipelines — Visual Guide, Stream Processing — Visual Guide, Data Warehouses & Lakehouses — Visual Guide
- **Agent Harnesses & Frameworks** (`il07-agents`) → ETL Data Pipelines — Visual Guide, Stream Processing — Visual Guide, Data Warehouses & Lakehouses — Visual Guide
- **Frontier AI Topics** (`il07-frontier`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **AWS Data Engineering** (`il07-aws-data`) → Cloud Architecture Patterns — Visual Guide, ETL Data Pipelines — Visual Guide, Stream Processing — Visual Guide
- **AWS ML Engineering** (`il07-aws-ml`) → Cloud Architecture Patterns — Visual Guide, ML Training Pipelines — Visual Guide, ETL Data Pipelines — Visual Guide

#### il-08: 5 modules
- **Discrete Math: Sets, Counting & Induction** (`il-08-algorithms-compilers-distributed-formal-math-discrete`) → DNS Resolution — Visual Guide, TCP 3-Way Handshake — Visual Guide
- **Logic & Boolean Algebra** (`il-08-algorithms-compilers-distributed-formal-math-logic`) → PKI & Encryption — Visual Guide, DNS Resolution — Visual Guide
- **MIT 6-3: The Distilled Core** (`il08-mit-63`) → DNS Resolution — Visual Guide, TCP 3-Way Handshake — Visual Guide, Load Balancing — Visual Guide
- **CMU: The Systems-and-Theory Spine** (`il08-cmu-cs`) → DNS Resolution — Visual Guide, TCP 3-Way Handshake — Visual Guide, Load Balancing — Visual Guide
- **Stanford: The Core Cross-Walk** (`il08-stanford-cs`) → DNS Resolution — Visual Guide, TCP 3-Way Handshake — Visual Guide, Load Balancing — Visual Guide

#### il-09: 9 modules
- **Binary, Hex & Computer Arithmetic** (`il-09-adaptive-certification-command-math-binmath`) → TCP 3-Way Handshake — Visual Guide, TLS Handshake — Visual Guide, PKI & Encryption — Visual Guide
- **Logic & Boolean Algebra** (`il-09-adaptive-certification-command-math-logic`) → PKI & Encryption — Visual Guide, TLS Handshake — Visual Guide, Zero Trust Architecture — Visual Guide
- **CompTIA Core Stack: A+, Network+, Security+** (`il09-comptia-core`) → TLS Handshake — Visual Guide, PKI & Encryption — Visual Guide, Zero Trust Architecture — Visual Guide
- **CompTIA Security Track: CySA+, PenTest+, SecurityX** (`il09-comptia-security`) → TLS Handshake — Visual Guide, PKI & Encryption — Visual Guide, Zero Trust Architecture — Visual Guide
- **CompTIA Data & Cloud: Cloud+, Linux+, Server+, Data+, DataSys+, Project+** (`il09-comptia-data-cloud`) → Cloud Architecture Patterns — Visual Guide, TLS Handshake — Visual Guide, PKI & Encryption — Visual Guide
- **Vendor AI Certifications** (`il09-vendor-ai`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Oracle: Java, SQL, and OCI** (`il09-oracle`) → Data Warehouses & Lakehouses — Visual Guide, TLS Handshake — Visual Guide, PKI & Encryption — Visual Guide
- **Linux Foundation Blockchain: HFCP and BCP** (`il09-lf-blockchain`) → PKI & Encryption — Visual Guide, TLS Handshake — Visual Guide, Zero Trust Architecture — Visual Guide
- **C++ and Python Institute Certifications** (`il09-cpp-python`) → ETL Data Pipelines — Visual Guide, TLS Handshake — Visual Guide, PKI & Encryption — Visual Guide

#### il-10: 5 modules
- **Quantitative Reasoning for Career Decisions** (`il-10-portfolio-career-professional-practice-math-quantreason`) → Data Warehouses & Lakehouses — Visual Guide, Stream Processing — Visual Guide, ML Training Pipelines — Visual Guide
- **The Forward-Deployed Career** (`il10-fde-career`) → CI/CD Pipelines — Visual Guide, ML Training Pipelines — Visual Guide, Data Warehouses & Lakehouses — Visual Guide
- **Self-Knowledge: The Humanmetrics Assessment** (`il10-humanmetrics`) → ML Training Pipelines — Visual Guide, Data Warehouses & Lakehouses — Visual Guide, Cloud Architecture Patterns — Visual Guide
- **Entrepreneurship: The Babson-Informed Track** (`il10-entrepreneurship`) → ML Training Pipelines — Visual Guide, Data Warehouses & Lakehouses — Visual Guide, Cloud Architecture Patterns — Visual Guide
- **Quantitative Finance: The Ladder** (`il10-quant-finance`) → Stream Processing — Visual Guide, Data Warehouses & Lakehouses — Visual Guide, ML Training Pipelines — Visual Guide

#### il-11: 27 modules
- **Number Theory & Modular Arithmetic** (`il-11-zero-trust-endpoint-defense-math-numtheory`) → PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Logic & Boolean Algebra** (`il-11-zero-trust-endpoint-defense-math-logic`) → Zero Trust Architecture — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **The Fall of the Perimeter** (`il11-zero-trust-foundations--zt-perimeter-fall`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **NIST SP 800-207 Tenets** (`il11-zero-trust-foundations--zt-nist-tenets`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **CISA Zero Trust Maturity Model** (`il11-zero-trust-foundations--zt-cisa-maturity`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Default-Deny Architecture** (`il11-zero-trust-foundations--zt-default-deny`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **OSI and TCP/IP Under Attack** (`il11-network-crypto-foundations--zt-osi-tcpip`) → TCP 3-Way Handshake — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **Hashing for Integrity** (`il11-network-crypto-foundations--zt-hashing`) → PKI & Encryption — Visual Guide, Zero Trust Architecture — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Encryption in Practice** (`il11-network-crypto-foundations--zt-encryption`) → PKI & Encryption — Visual Guide, Zero Trust Architecture — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **AD Structure and Trust** (`il11-active-directory-defense--zt-ad-structure`) → OAuth 2.0 & Authentication Flows — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **How AD Gets Hacked** (`il11-active-directory-defense--zt-ad-attacks`) → OAuth 2.0 & Authentication Flows — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **Hardening the Identity Plane** (`il11-active-directory-defense--zt-ad-harden`) → OAuth 2.0 & Authentication Flows — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **Application Allowlisting** (`il11-allowlisting-ringfencing--zt-allowlist`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Ringfencing Applications** (`il11-allowlisting-ringfencing--zt-ringfence`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Storage & Elevation Control** (`il11-allowlisting-ringfencing--zt-storage-elevation`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Social Engineering & Phishing** (`il11-red-blue-operations--zt-social-engineering`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Web & Application Attacks** (`il11-red-blue-operations--zt-web-attacks`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Detection & Response** (`il11-red-blue-operations--zt-blue-detect`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Full-Spectrum Review** (`il11-cyber-hero-prep--zt-hero-review`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Scenario Capstone** (`il11-cyber-hero-prep--zt-hero-scenarios`) → Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide
- **Entra ID Identity Lifecycle** (`il11-entra-identity--sc300-lifecycle`) → OAuth 2.0 & Authentication Flows — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **Zero Trust and Conditional Access** (`il11-entra-identity--sc300-zerotrust-ca`) → Zero Trust Architecture — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide, PKI & Encryption — Visual Guide
- **Authentication and Authorization** (`il11-entra-identity--sc300-auth`) → OAuth 2.0 & Authentication Flows — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **Hybrid Identity** (`il11-entra-identity--sc300-hybrid`) → OAuth 2.0 & Authentication Flows — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **Identity Governance** (`il11-entra-identity--sc300-governance`) → OAuth 2.0 & Authentication Flows — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide
- **Troubleshooting with PowerShell and KQL** (`il11-entra-identity--sc300-troubleshoot`) → OAuth 2.0 & Authentication Flows — Visual Guide, Stream Processing — Visual Guide, Zero Trust Architecture — Visual Guide
- **SC-300 Exam Prep** (`il11-entra-identity--sc300-exam-prep`) → OAuth 2.0 & Authentication Flows — Visual Guide, Zero Trust Architecture — Visual Guide, PKI & Encryption — Visual Guide

#### il-12: 72 modules
- **Linear Algebra Foundations** (`il-12-ai-engineering-math-linalg`) → Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Probability & Statistics** (`il-12-ai-engineering-math-stats`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide
- **Discrete Math: Sets, Counting & Induction** (`il-12-ai-engineering-math-discrete`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Python Core Syntax** (`aieng-python-foundations--py-syntax-core`) → ETL Data Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Objects, Modules, and Environments** (`aieng-python-foundations--py-oop-modular`) → ETL Data Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Threading and Concurrency** (`aieng-python-foundations--py-concurrency`) → ETL Data Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **GenAI-Assisted Coding Workflow** (`aieng-python-foundations--py-genai-workflow`) → ETL Data Pipelines — Visual Guide, Transformers & Attention — Visual Guide, Neural Networks — Visual Guide
- **NumPy Foundations** (`aieng-data-science--numpy-foundations`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Data Wrangling with pandas** (`aieng-data-science--pandas-wrangling`) → ETL Data Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Visualization** (`aieng-data-science--viz-matplotlib-seaborn`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Statistics for Machine Learning** (`aieng-data-science--statistics-for-ml`) → ML Training Pipelines — Visual Guide, Transformers & Attention — Visual Guide, Neural Networks — Visual Guide
- **The Model-Development Workflow** (`aieng-data-science--model-dev-workflow`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **SQL for AI Engineers: Analytical Queries and Dataset Validation** (`aieng-data-science--sql-for-ai-engineers`) → ML Training Pipelines — Visual Guide, Data Warehouses & Lakehouses — Visual Guide, ETL Data Pipelines — Visual Guide
- **Supervised Learning** (`aieng-machine-learning--supervised-learning`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Unsupervised Learning** (`aieng-machine-learning--unsupervised-learning`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Reinforcement Learning: First Contact** (`aieng-machine-learning--reinforcement-intro`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Validation and Hyperparameter Tuning** (`aieng-machine-learning--validation-tuning`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Feature Engineering** (`aieng-machine-learning--feature-engineering`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Evaluation Metrics** (`aieng-machine-learning--evaluation-metrics`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Neural Network Foundations** (`aieng-deep-learning--neural-foundations`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Backpropagation and Optimization** (`aieng-deep-learning--backprop-optimization`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Convolutional Networks** (`aieng-deep-learning--cnns`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Sequence Models: RNNs to Attention's Doorstep** (`aieng-deep-learning--sequence-models`) → Transformers & Attention — Visual Guide, Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide
- **Regularization and Hyperparameter Tuning** (`aieng-deep-learning--regularization-tuning`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **PyTorch Training Workflows** (`aieng-deep-learning--pytorch-workflows`) → Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide, Transformers & Attention — Visual Guide
- **Transformers and Attention** (`aieng-generative-ai--transformers-attention`) → Transformers & Attention — Visual Guide, ETL Data Pipelines — Visual Guide, Neural Networks — Visual Guide
- **GPT vs BERT: Two Objectives** (`aieng-generative-ai--gpt-vs-bert`) → Transformers & Attention — Visual Guide, Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide
- **GANs and VAEs** (`aieng-generative-ai--gans-vaes`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Diffusion and Image/Video Generation** (`aieng-generative-ai--diffusion-generation`) → Transformers & Attention — Visual Guide, Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide
- **Prompt Engineering** (`aieng-generative-ai--prompt-engineering`) → Transformers & Attention — Visual Guide, Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide
- **LLM APIs and Retrieval-Augmented Generation** (`aieng-generative-ai--llm-apis-rag`) → Transformers & Attention — Visual Guide, Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide
- **Vector Databases in Depth** (`aieng-generative-ai--vecdb-depth`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Advanced Retrieval: GraphRAG and Agentic Retrieval** (`aieng-generative-ai--advanced-retrieval`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Fine-Tuning: LoRA and QLoRA** (`aieng-generative-ai--genai-finetuning`) → Transformers & Attention — Visual Guide, Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide
- **Multimodal Foundation Models** (`aieng-generative-ai--multimodal-foundation-models`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Applied Vision and Speech** (`aieng-generative-ai--vision-speech-apps`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Preference Alignment: RLHF, DPO, and Reasoning Models** (`aieng-generative-ai--llm-alignment-rlhf-dpo`) → Transformers & Attention — Visual Guide, Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide
- **Text Preprocessing** (`aieng-nlp--text-preprocessing`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Tokenization and Embeddings** (`aieng-nlp--tokenization-embeddings`) → Transformers & Attention — Visual Guide, OAuth 2.0 & Authentication Flows — Visual Guide, Neural Networks — Visual Guide
- **Classic NLP with NLTK** (`aieng-nlp--nltk-classics`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Sequence Models for Language** (`aieng-nlp--sequence-models-nlp`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Hugging Face in Practice** (`aieng-nlp--hf-pipelines`) → CI/CD Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Agent Architectures** (`aieng-agentic-ai--agent-architectures`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Tool Use and Function Calling** (`aieng-agentic-ai--tool-use`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **The Protocol Layer: MCP and Agent Interoperability** (`aieng-agentic-ai--mcp-protocol`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **LangChain and AutoGen** (`aieng-agentic-ai--langchain-autogen`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Context Engineering: Compaction, Clearing, and Memory** (`aieng-agentic-ai--context-engineering`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Copilot Studio: Low-Code Agents** (`aieng-agentic-ai--copilot-studio`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Azure AI Foundry: Pro-Code Agents** (`aieng-agentic-ai--azure-ai-foundry`) → Cloud Architecture Patterns — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Azure AI Services** (`aieng-azure-ai-900--azure-ai-services`) → Cloud Architecture Patterns — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Machine Learning Concepts on Azure** (`aieng-azure-ai-900--ml-concepts-azure`) → ML Training Pipelines — Visual Guide, Cloud Architecture Patterns — Visual Guide, Neural Networks — Visual Guide
- **Responsible AI** (`aieng-azure-ai-900--responsible-ai`) → Cloud Architecture Patterns — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Cost, Governance, and Compliance** (`aieng-azure-ai-900--cost-governance`) → Cloud Architecture Patterns — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **ML Systems Design** (`aieng-production--prod-mlops-framing`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Model Serving and Deployment Patterns** (`aieng-production--prod-serving`) → Kubernetes Architecture — Visual Guide, CI/CD Pipelines — Visual Guide, Neural Networks — Visual Guide
- **Monitoring, Drift, and Retraining** (`aieng-production--prod-monitoring`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **AgentOps: Tracing and Observability for LLM Systems** (`aieng-production--agentops-observability`) → Transformers & Attention — Visual Guide, Neural Networks — Visual Guide, ML Training Pipelines — Visual Guide
- **Cost and Latency Engineering** (`aieng-production--prod-cost-latency`) → Caching & CDNs — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Red-Teaming and Evaluation Harnesses** (`aieng-production--prod-red-team`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Agent Trajectory Evaluation** (`aieng-production--trajectory-eval-agents`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **ML Pipelines and CI/CD** (`aieng-production--prod-pipelines`) → CI/CD Pipelines — Visual Guide, ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide
- **Experiment Tracking and the Model Registry** (`aieng-production--experiment-tracking-registry`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Feature Stores: Training-to-Serving Consistency** (`aieng-production--feature-stores`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Data-Centric AI: Training Data as Engineering** (`aieng-production--data-centric-ai`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Edge and On-Device AI** (`aieng-production--edge-ondevice-ai`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Problem Framing** (`aieng-capstone--capstone-framing`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **End-to-End Build** (`aieng-capstone--capstone-build`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Evaluation and Robustness** (`aieng-capstone--capstone-eval`) → ML Training Pipelines — Visual Guide, Neural Networks — Visual Guide, Transformers & Attention — Visual Guide
- **Deployment and MLOps Lite** (`aieng-capstone--capstone-deploy`) → Kubernetes Architecture — Visual Guide, CI/CD Pipelines — Visual Guide, ML Training Pipelines — Visual Guide
- **Responsible AI Review** (`aieng-capstone--capstone-rai`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **The Portfolio Piece** (`aieng-capstone--capstone-portfolio`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide
- **Agent Autonomy Ceilings: Time Horizons** (`aieng-agentic-ai--agent-autonomy-ceilings`) → Neural Networks — Visual Guide, Transformers & Attention — Visual Guide, ML Training Pipelines — Visual Guide

**Totals:** 129 modules, 373 new PDF entries.

**Backups:** `~/workspace/apex-audit/.work/course-json-backups-embed/il-*.embed20261009.bak` (pre-wire) + `wire_pdfs.py` (re-runnable wiring script) + `wire-report.json`.

**Deploy:** commit `cb8a75d`, flagship deploy `solitary-sound-015a`, etag=`95acb862e03f`, modified=2026-10-09T05:49:00Z. PDF spot-checks: bbg-etl-pipelines.pdf → 200, bbg-zero-trust.pdf → 200, bbg-transformers.pdf → 200.

---

## IL-21..IL-29 — Course embed gap fill (subagent 47b42ffb, 2026-10-09 ~05:43–05:58 UTC)

**Scope:** all 301 modules across il-21-humanities, il-22-esoteric-secret-knowledge, il-23-frontier-knowledge, il-24-threatlocker-assessment-prep-cbt, il-25-cybersecurity-professional-certificate, il-26-data-analyst-certification-senior-mastery, il-27-it-infrastructure-specialist-threatlocker-mastery, il-28-devsecops-cloud-infrastructure-mastery, il-29-threatlocker-ai-cybersecurity-mastery.

**PDFs wired:** 582 new entries, every module now has exactly 2 PDFs (modules that already had 1 kept it and got 1 more).
- il-21 (16 mods, 32 entries), il-22 (18 mods, 36), il-23 (15 mods, 30): point at `https://interstitiumlabs.dev/pdf-library/` with honest blurbs ("browse the visual guide library…"; pages=null/animated=false so the renderer shows "? pages" with no animated tag).
- il-24 (16 mods, 30 entries): zero-trust / tls-handshake / pki-encryption / oauth-flows; ML modules → ml-pipelines, transformers; UEBA/capstone → ml-pipelines.
- il-25 (27 mods, 50 entries): zero-trust / pki-encryption / tls-handshake / oauth-flows; IAM → oauth-flows; crypto → pki-encryption; SOC → etl-pipelines (SIEM log aggregation); cloud → cloud-patterns.
- il-26 (53 mods, 103 entries): data-warehouses / etl-pipelines / stream-processing first; SQL/BI → data-warehouses; ETL/dbt/Iceberg → etl-pipelines; dashboards/streaming → stream-processing.
- il-27 (56 mods, 109 entries): zero-trust / tcp-handshake / dns-resolution / tls-handshake; AD/Entra → oauth-flows; Docker → microservices+kubernetes; SIEM/monitoring → stream-processing+etl-pipelines; HA → load-balancing.
- il-28 (52 mods, 99 entries): kubernetes / cicd-pipeline / cloud-patterns / load-balancing; Docker → microservices; Terraform → cloud-patterns; Jenkins/Actions → cicd-pipeline; observability → stream-processing+etl-pipelines.
- il-29 (48 mods, 93 entries): zero-trust / tls-handshake / pki-encryption / oauth-flows; ML/LLM modules → ml-pipelines / transformers; forensics → pki-encryption (hashing); MIT 6.858 web/auth → oauth-flows / tls-handshake.
- Matching: keyword scorer (word-boundary for short tokens, title-weighted tiebreak) + 57 manual overrides for semantic misses (e.g. "Load Balancing" module forced to the load-balancing guide; "orchestration" in a data-pipeline module not mapped to Kubernetes). Review table: `.work/embed-pdf-review.txt`.

**Depth check:** every module already satisfied quiz≥3, cards≥5, drills≥1 — zero additions needed. No new questions/cards written.

**Untouched:** videos, handsOnLab, glossary, quiz, cards, drills verified byte-identical vs pre-edit backups (programmatic diff, PASS).

**Backups:** `~/workspace/apex-audit/.work/course-json-backups-embed/il-{21..29}-*.json` (md5-verified copies). Scripts: `.work/embed-pdf-match.py` (matcher), `.work/embed-pdf-apply.py` (applier, re-runnable/idempotent-ish via dedupe).

**Deploy:** commit `a56f15c` (9 files, +6700/−318 — deletions are only comma insertions where `pdfs` was appended), flagship deploy `solitary-sound-015a`, etag=`95acb862e03f`, modified=2026-10-09T05:53:25Z (293 changed-asset files uploaded). PDF spot-checks: bbg-zero-trust.pdf → 200, bbg-etl-pipelines.pdf → 200, bbg-kubernetes.pdf → 200, /pdf-library/ → 200. Live course JSONs sit behind the paywall (402 payment_required as designed), so live-content check was via deploy manifest + hash-upload counts.

**Notes for coordinator:** (1) Sibling agents concurrently editing il-13..il-20 — I committed only my 9 files; their uncommitted changes were included in my deploy's asset upload (working-tree deploy), which is expected. (2) The deploy etag matched the sibling's 05:49 deploy etag — verified it's the worker script version etag (main module unchanged), not an asset hash; the 293-file upload + new modified timestamp confirm a fresh asset deployment.

### B1 — Bootcamp SVG diagram gap fill (subagent 29e94a2f, completed 2026-10-09 ~02:05 EDT)

**Scope:** live scan of all 135 `content.json` files found **113 domains** without a matching `c-<domain_id>` media[] entry across **62 bootcamps** (24 zero-media bootcamps + 38 partial-coverage bootcamps). Final state: **all 532 domains covered, 0 gaps**.

**What was built:** 113 original SVG diagrams (600×400 viewBox, dark-theme, self-contained inline styles, `<title>`/`<desc>` for a11y), one per uncovered domain, topic-matched:
- Layouts: hub-and-spoke (concept maps), horizontal layer stacks (OSI, defense-in-depth, persistence stacks), pipelines/flows (CI/CD, IR lifecycle, troubleshooting methodologies), 3×2 concept grids, network topologies (SOHO, campus access, IP routing, enterprise 3-tier, sensor node, security graph), AD forest tree, feedback cycles, and a 3-5-5-2 neural-network diagram for deep-learning.
- Examples: `cisco-ccna/ip-connectivity` → routed topology with prefix labels; `comptia-security-plus/architecture` → 6-layer defense-in-depth; `quantum` → qubit hub (superposition, entanglement, gates, Shor/Grover, error correction, PQC); `deep-work` → time-blocking flow; `humanmetrics` → 4 dichotomies grid; `comptia-a-plus/troubleshooting` → CompTIA 6-step method.
- Each diagram stroked with its bootcamp's `accent` color. 9 renders spot-checked as PNG (quantum, deep-learning, ccna/ip-connectivity, sec+/architecture, AD tree, embedded capstone, security-graphs, net+/implementation, a+/troubleshooting) — all clean; fixed one connector-line overlap in the AD tree layout.

**Wiring:** SVGs written to `<slug>/assets/diagrams/<domain_id>.svg`; media[] entries follow the engine's actual contract — `{"id","kind":"diagram","title","svg":"assets/diagrams/<domain_id>.svg","lesson_ref":"c-<domain_id>","caption","alt"}`. (The 885 pre-existing entries are all path-references rendered as `<img src="./…">` by learn.js; 0 are inline SVG strings — inline would not render, so path-reference was used.)
- Backups: `.work/bootcamp-json-backups-embed/` (62 `.content.json` files, pre-edit).
- Safety: temp-file + `os.replace`, `json.load` re-validation, append-only assertion (every key except `media` byte-identical), lesson_ref dedupe.
- Scripts: `.work/gen_diagrams_1000pct.py` (builders + 113 specs + manifest), `.work/wire_diagrams_1000pct.py`; manifest `.work/diagram-manifest-20261009.json`.

**Deploy:** `deploy-worker-assets deploy/worker-config.json` from `~/workspace/cert-bootcamps` → worker `cert-bootcamps`: manifest 967 files, **175 uploaded** (62 content.json + 113 SVGs), live at `2026-10-09T05:55:02Z` (deployment `08922b3b`, confirmed via Cloudflare API as latest). Bindings untouched (pure static-assets deploy, no worker module). Gateway/paywall untouched.

**Verification caveat:** public `curl` of `/bootcamps/<slug>/content.json` returns **401 `{"error":"sign-in-required"}`** — the `interstitium-course-gateway` gates the entire `/bootcamps/*` tree behind sign-in (paywall by design), and the worker has no public workers.dev route (error 1042). So a live 200-with-media check is not possible without a signed session. Verified instead: (a) Cloudflare API confirms the 05:55:02Z deployment is the latest and live; (b) deploy uploaded exactly the 175 changed/new files; (c) all 62 local content.json re-validated post-wire with media[] counts correct (e.g. cisco-ccna 6, quantum 1, android-interview 7); (d) all 113 SVGs XML-valid and visually rendered. Recommend parent re-verify with a signed session when available.

**Note for coordinator:** the brief's "44 missing domains" undercounts — live scan found 113 (69 inside the 24 zero-media bootcamps + 44 elsewhere). Also, `lesson_ref` matching is by domain id (`c-<domain_id>`), and some bootcamps (e.g. android-interview, zero-trust) have lessons whose `domain_id` differs from some `domains[].id` values; entries were keyed per the brief (`c-<domain_id>`), engine degrades gracefully for any that don't match a rendered lecture.
