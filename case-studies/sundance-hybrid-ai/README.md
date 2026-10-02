# Sovereign Hybrid AI for Print and Packaging Manufacturing
**Enmanuel D. Mejia | Interstitium Labs | September–October 2026**

**Project type:** Independently authored architecture research and candidate presentation prepared for SunDance USA. **Deliverables completed:** 37-page AI Implementation UltraPlan and 17-slide executive vision deck (PDF and editable PowerPoint originals retained by the author). **Scope:** Proposed design, not a SunDance contract, implementation, paid consulting role or claimed production result.

[View the public portfolio case study](https://interstitiumlabs.dev/projects/sundance-ai-architecture/)

## Executive problem
Explore an AI-first operating model for a commercial print and packaging manufacturer using publicly documented equipment and processes. Address client-artwork confidentiality, IT/OT separation, measurable automation, operator approval, integration with existing manufacturing software and a practical rollout.

## Proposed sovereign hybrid AI architecture
- **Tier 1, on-prem inference:** Self-hosted open-weight models on segregated, company-controlled GPU infrastructure for sensitive customer artwork, Tharstern MIS records, job tickets, color profiles and logs. Unclassified or sensitive data must fail closed and never be routed to third-party models.
- **Tier 2, authorized frontier APIs:** A model gateway sends explicitly approved and sanitized tasks to suitable cloud models for reasoning, automation-code assistance and documentation; routing accounts for task, sensitivity, latency, cost and performance.
- **Structured decision layer:** A *proposed, conditional pilot* of TypeSafe Jev for typed order-priority and anomaly decisions with measurable calibration, human escalation and an on-prem classifier fallback. Jev access and vendor data terms were not verified or deployed.
- **Governance and evaluation:** Policy gateway, model/prompt versioning, execution logs, cost attribution, regression evaluations, human approvals, disaster recovery and reversible changes. No autonomous press actuation.

**Principle:** LLMs generate, the evaluated decision model scores, deterministic software governs, and humans approve consequential actions.

## Manufacturing and enterprise systems analysis
Mapped a potential cross-vendor workflow around publicly documented **Tharstern MIS, Heidelberg Prinect, Suprasetter CtP, Speedmaster CD 102, HP Indigo, Enfocus Switch/PitStop and Aleyant Pressero**, including opportunities for prepress automation, job-status visibility and equipment monitoring. JDF/XJDF/JMF exchanges and internal network topology were identified as *typical integration hypotheses requiring on-site confirmation*, not verified SunDance configurations.

## Four proposed, permission-bounded agents
1. **Prepress preflight:** Read approved artwork intake and automated preflight outputs, flag exceptions and draft responses. The prepress operator approves releases.
2. **JDF/MIS monitoring:** Read permitted tickets and status events, suggest corrections and alert on anomalies. A supervisor authorizes ticket changes.
3. **IT troubleshooting copilot:** Read selected logs, alerts and approved runbooks, then propose recovery steps. The IT administrator executes changes.
4. **Documentation agent:** Convert reviewed incident resolutions into versioned runbook drafts. A team lead approves publication.

Each design includes input boundaries, read/write limits, approval gates and rollback or prior-version recovery.

## Delivery and outcomes
**Completed work:** A researched 37-page UltraPlan; a 17-slide executive deck; source-graded findings; systems map; hybrid architecture; four agent specifications; risk register; proposed 90-day vision and Phase 0–4 roadmap; evaluation and data-protection criteria.

**Not claimed:** Employer authorization, SunDance credentials, deployments, production operations, contractual consulting, measured savings or real performance KPIs. Dashboard figures in the original deck were illustrative.

## Skills demonstrated
AI solution architecture, enterprise systems research, local/cloud LLM trade-offs, data residency, IT/OT security, model routing, agent permission design, manufacturing workflow analysis, technical writing, risk analysis, phased delivery and executive communication.

*Source artifacts: SunDance-AI-UltraPlan.pdf (September 29, 2026); SunDance-AI-Vision-Deck.pdf and .pptx (October 2, 2026). Original branded artifacts are not redistributed in this public repository.*
