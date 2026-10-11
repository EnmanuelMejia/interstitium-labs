# Seed summary — @oliviscusAI X post on AirLLM

**Slug:** `airllm-x-post`
**Source URL:** https://x.com/oliviscusAI/status/2108786434991923251 (surfaced 2026-10-10)
**Verification:** GitHub repo verified at https://github.com/lyogavin/airllm (2026-10-10)

## What it is

AirLLM is an open-source inference tool that runs very large language models on
small GPUs by loading the model one layer at a time ("layer-wise inference").
Instead of holding the entire model in VRAM at once, it streams layers through
memory sequentially, so a 70B-parameter model fits in roughly 4GB of VRAM with
no quantization, distillation, or pruning involved.

Reported figures from the repo (as of Oct 2026): 70B on a 4GB card; Llama 3.1
405B on ~8GB; DeepSeek-V3 (671B) on ~12GB; Kimi K3 (a 2.8T sparse mixture-of-
experts model) on under 4GB, because sparse MoE models stream one expert at a
time rather than a whole layer. Supports Llama, Qwen, and Mistral families.
Cross-platform: Linux, Windows, macOS. The project also reports support for
*training* large models on small VRAM (e.g., Qwen3 125B under 6GB).

## Why it matters here

Directly relevant to any IL content on local LLM deployment, GPU-constrained
inference, self-hosted AI, and cost-efficient AI infrastructure. Added as a
tool reference in 8 AI/ML CBTs (llm-engineering, ai-lab, nlp-engineering,
nlp-advanced, deep-learning, neuroai, nvidia-ai, il12-ai-engineering) on
2026-10-10.

## Fair-use note

All summaries above are original writing. No text copied from the X post or
the GitHub README. Figures are attributed to the repo as reported; they are
the project's claims, not independently benchmarked here.
