# Seed summary — Epoch AI research corpus (capability forecasting)

**Slug:** `epoch-ai-research-corpus`
**Corpus anchor:** https://epoch.ai/publications (retrieved 2026-10-07; content verified — current through Oct 6, 2026)
**Primary sources consulted (all verified live, retrieved 2026-10-07):**
- https://epoch.ai/publications/estimating-the-agent-population — Epoch AI report, "How many AI agents could we run?", by Jason Li, dated Oct 2, 2026 (report page read in full)
- https://arxiv.org/abs/2211.04325 — Villalobos et al., "Will we run out of data? Limits of LLM scaling based on human-generated data" (arXiv v2, revised 4 Jun 2024; ICML 2024 position paper, PMLR v235). Abstract, Figure 1 caption, Table 1, Sections 1–2, and Section 5 (Conclusion) read at https://arxiv.org/html/2211.04325v2.
**Disposition:** CONSUMED — processed 2026-10-07

## What it is

Epoch AI is the research group that tracks AI's physical and statistical supply chains — compute, data, chips, and model progress — as empirical forecasting inputs. This seed covers the corpus's capability-forecasting core: the "data wall" (data-availability) debate, the new inference-capacity (agent-population) analysis, and the corpus's standing research program (compute trends, cost curves, supply-chain tracking).

## Item 1 — "How many AI agents could we run?" (Epoch AI, Oct 2, 2026)

**Method in the site's words:** Epoch builds the estimate from two terms — effective hardware supply (HBM memory shipped 2025–27, expressed in GB300 equivalents) multiplied by serving capacity (concurrent agent sessions per GB300 equivalent). For closed frontier models, concurrency is inferred from API spending per agent-hour in the TraceLab dataset of Codex/Claude Code session traces; for open models, from SemiAnalysis's AgentX serving benchmarks at fixed streaming-speed targets.

**Key findings (as of 2026-10-02, per Epoch's page):**

- HBM shipped 2025–27 could support roughly **30–170 million concurrent frontier-model agents** once deployed (16–56 million from 2025–26 shipments alone), with an 80%-style range reported as 33–171 million on the publications index.
- The same hardware could run far more efficient open-model sessions — about **1.9 billion concurrent agents** using DeepSeek V4 Pro serving benchmarks at 50 tokens/sec per user.
- Demand is the binding unknown: using just 20% of central capacity would imply **$2.6–5.3 trillion/year in API-equivalent spending**, against roughly **$1 trillion** in combined developer revenue by end-2027 at fivefold annual growth. Epoch's framing: demand could fall behind supply, creating a capacity glut.
- Hourly agent economics vary by harness: pooled TraceLab rates around **$18/hour for GPT-5.5** (Codex) and **$15.5 for GPT-5.6 Sol**, versus **$24.3 for Opus 4.8** and **$50.2 for Fable 5** (Claude Code); the report's reference point is $30/agent-hour.

**Honesty note:** model names (GPT-5.6 Sol, Opus 4.8, Fable 5, DeepSeek V4 Pro, GPT-6 Astra, GLM-5.2, Kimi K3, MiniMax M3) and figures are Epoch's 2026 estimates and assumptions — fast-moving; all carried with the Oct 2, 2026 as-of date in the module fragment.

## Item 2 — "Will we run out of data?" (Villalobos et al., ICML 2024)

**The claim, from the verified paper:** human-generated public text data cannot sustain LLM scaling beyond this decade. If current trends continue, training datasets will reach the size of the available stock of public human text **between 2026 and 2032**, one or two years earlier if frontier models are overtrained. The median projection (Figure 1 caption) is **2028**: datasets approaching ~4e14 tokens (the total effective stock of text in the indexed web), corresponding to ~5e28 FLOP of training compute for non-overtrained models.

**How the estimate is built (Sections 1–2, paraphrased):**
- Demand side: neural scaling laws (Kaplan 2020; Hoffmann/Chinchilla 2022) imply training dataset size should grow roughly with the square root of training compute, so data demand compounds.
- Supply side: the indexed web is estimated via Google's index (~250B pages) and Common Crawl's plain-text-per-page statistics (~7000 bytes/page), converted to tokens with a byte-pair tokenizer.
- Two downward adjustments: **quality filtering** (only a fraction of deduplicated web text is usable without degrading performance) and **multi-epoch training** (repeat passes stretch the effective stock by a capped multiplier). Monte Carlo simulation propagates the uncertainty.

**Stock estimates (Table 1, tokens, 95% CIs where given):** Common Crawl 130T [100T–260T]; indexed web 510T [130T–2100T]; whole web 3100T [1900T–5200T]; images 300T; video 1350T (images/video point estimates only).

**Conclusion (Section 5, paraphrased):** the current public-text paradigm likely cannot continue a decade from now — but the authors judge it likely that alternative data sources (synthetic data, transfer learning from data-rich domains, data-efficiency improvements) will be adopted before then, allowing scaling to continue. They call for further research on data-efficiency growth rates and synthetic-data performance.

**Impact statement (noted, not adopted):** the paper's own discussion of compensation for data creators and privacy risks of social-media/messaging data is summarized here as the authors' position, not the site's.

## Item 3 — The standing corpus (from the verified publications index, as of 2026-10-07)

The publications page confirms Epoch's active research program and gives this seed its "corpus" character. Current threads (characterized from Epoch's own blurbs, not reproduced):
- **"The plunging price of thought"** (Sep 22, 2026) — cost of a fixed level of benchmark performance falling ~47%/quarter (~13×/year) since 2023, faster than electricity/compute/batteries/DNA sequencing ever fell. Inference-economics anchor.
- **Chip supply-chain tracking** — AI Data Centers research mapping data centers worldwide (satellite imagery, H100-equivalents, chip types, capex); chip-shock exposure analysis (China 2.7× as exposed as the US); trade-data analysis consistent with $3B of chips routed to China via Malaysia; Huawei-vs-Nvidia projection (Huawei <4% of Nvidia's AI compute in 2026).
- **Adoption measurement** — OpenAI coding-agent usage doubling roughly monthly; ChatGPT usage explorer (8.3M messages); AI-use acknowledgments in arXiv math preprints rising 4%→25% (Apr→Aug 2026).
- **Capability benchmarks** — IKEA furniture-assembly visual-reasoning benchmark (28%→80% in 10 months; open-weight trailing ~7 months); FrontierMath benchmarking program (listed in the AI-chips topic index).

## Synthesis (original exposition)

Epoch AI's body of work is one discipline wearing several hats: **measure the physical inputs of AI progress, then project the frontier from them.** The data-wall paper asks what happens when the *data* input runs out; the agent-capacity report asks what the *chip* buildout can actually serve; the cost curves ask what each unit of capability costs over time. For IL-23's purposes, the teachable unit is the *method*: how to turn an unobservable quantity (remaining usable data, deployable agent capacity) into a bounded forecast with stated assumptions and uncertainty intervals. Two cautionary lessons recur across the corpus: (1) every number decays — the 2022 data-wall estimate was revised from ~2024 to ~2028 after web-data filtering performed better than assumed; (2) the binding constraint moves — by 2026 the debate is as much about inference economics and demand as about raw training data.

## Fair-use note

This summary describes Epoch's research program and findings in original prose with all figures attributed to Epoch and dated. No body text of any report or paper is reproduced. All prose folded into the site from this seed must be original Interstitium exposition with Epoch's pages and the arXiv paper linked as anchors.

## URL verification log (2026-10-07)

- https://epoch.ai/publications/estimating-the-agent-population — 200, report page read (695 lines).
- https://arxiv.org/abs/2211.04325 — 200, abstract + metadata + CC-BY 4.0 license verified.
- https://arxiv.org/html/2211.04325v2 — 200, abstract/Figure 1/Table 1/Sections 1–2/Conclusion read.
- https://epoch.ai/publications — 200, current index read (through Oct 6, 2026).
- Search-result URLs not opened directly (e.g. groundtruth.day, allfacts.ai) were treated as pointers only; no claims from them were recorded as verified.
