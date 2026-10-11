# 3-way mapping — AirLLM (@oliviscusAI X post)

**Seed:** `airllm-x-post` — https://x.com/oliviscusAI/status/2108786434991923251
**Verified at:** https://github.com/lyogavin/airllm

## Decision: (a) SUPPLEMENTAL KNOWLEDGE — mapped, content added

### (a) Supplemental knowledge — APPLIES

Added as a tool reference (`resources.links`) in 8 AI/ML CBTs where local LLM
deployment and GPU-constrained inference are discussed:
llm-engineering, ai-lab, nlp-engineering, nlp-advanced, deep-learning,
neuroai, nvidia-ai, il12-ai-engineering.

Also added to Noah AI knowledge base (noah-knowledge.md) under AI tooling.

### (b) Standalone CBT module — NOT APPLICABLE

A single inference tool does not warrant a standalone module. The (a) mapping
covers it.

### (c) Certification mapping — NONE

No certification is associated with this tool.

## Why

AirLLM is a concrete, verifiable open-source tool that directly answers the
question "how do I run a large model on the GPU I already have?" — a question
that recurs across IL's AI/ML content. The layer-wise inference mechanism is a
durable concept (memory/compute tradeoff), while the specific VRAM figures are
perishable edge claims attributed to the repo, not stated as settled fact.
