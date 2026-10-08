# GenAI for PM track, part 1: genai-literacy-pm, llm-product-patterns
# quiz items: (q, [4 choices], answer_index, explain)

RETRO = {}

RETRO["genai-for-pm--genai-literacy-pm"] = {
"summary": (
"Welcome to the Generative AI for PMs track — I'm your instructor, and this is Module 1: GenAI Literacy. "
"The literacy every AI PM needs: how the models work at the altitude product decisions happen — tokens, "
"context, cost, latency — and the hype filter that separates demos from shippable products. By the end of "
"this module you will reason about LLMs at product altitude, price tokens and context windows, name model "
"capabilities and limits honestly, weigh latency and cost, choose models without hype, and tell a demo from "
"a product."
),
"concepts": """- **LLMs at product altitude** — Next-token prediction over learned patterns: fluent, probabilistic, knowledge-cutoff-bound — enough to reason about product fit.
- **Tokens** — The model's unit of text and of billing: count them — they are money.
- **Context window** — The model's finite working memory: what fits, what gets truncated, and what it costs to fill.
- **Capabilities** — What models do well: drafting, summarizing, transforming, conversing within distribution — fluency tasks with verifiable outputs.
- **Limits** — Hallucination, weak reasoning on novel problems, knowledge cutoffs — the boundaries every AI PM must design around.
- **Latency basics** — Time-to-first-token versus total time; model size versus quality — the arithmetic of AI user experience.
- **Model selection** — When the flagship is overkill: match capability to the task with evals, not hype.
- **Hype filter** — Demos versus products: the demo shows the best case; the product survives the worst case.""" ,
"procedure": """Run the GenAI literacy drill. Work each step on paper — the arithmetic is the literacy.
1. Write the product-altitude mental model in your own words: probabilistic next-token prediction, cutoff-bound — and what that implies for product fit.
2. Price a feature: pick a task (e.g. summarizing 50 tickets a day), estimate tokens in and out, and compute the monthly cost at a stated per-token price — tokens are money.
3. Fill a context window on paper: list what must fit (instructions, examples, retrieved docs, the task) and what gets truncated first — the finite working memory, managed.
4. List three capabilities and three limits for a feature you would ship: where the model is fluent and verifiable, and where hallucination or cutoffs would bite.
5. Weigh the latency tradeoff: time-to-first-token versus total, streaming versus batch — and write the UX consequence of each.
6. Run the model-selection test: would a smaller model pass your evals for this task? Write the criteria that would prove it — match capability to task, not hype.
7. Apply the hype filter to a demo you have seen: what was the best case shown, and what would the worst case cost the product?""",
"brief": """Your interview prep brief: prove GenAI literacy on a feature you would actually ship.
The scenario. Your AI PM loop asks: "We want an AI summarizer for support tickets. Walk me through the product decisions."
Deliverables.
- The product-altitude mental model, in your own words, with its product-fit implications.
- A token-and-cost estimate: tokens in/out, monthly cost at volume, the cost levers.
- A context-window plan: what fits, what truncates, what it costs.
- A capabilities-and-limits table for the feature: where the model shines, where it must be caged.
- A model-selection rationale: why this model size, proven by eval criteria — not hype.
Grading lens. AI PM rounds score altitude-appropriate literacy: can you price the feature, name the boundaries, choose the model deliberately — and tell the demo from the product?""",
"honesty": """Preparation only — this module confers no certificate and grants no credential. GenAI literacy must be practiced on real model behavior and real pricing you have actually worked with — as of late 2026, model capabilities and prices move fast, so date your claims and verify them against the providers' current documentation. Never present a demo as a shipped product.""",
"quiz": [
("The product-altitude LLM mental model is:", ["Magic", "Probabilistic next-token prediction, cutoff-bound", "A database", "A rules engine"], 1, "The Concepts glossary defines LLMs at product altitude as next-token prediction over learned patterns: fluent, probabilistic, knowledge-cutoff-bound."),
("Tokens are:", ["Words", "The model's unit of text and of billing", "Letters", "Ideas"], 1, "The Concepts note defines tokens as the model's unit of text and billing — count them; they are money."),
("Model limits include:", ["Nothing", "Hallucination, weak novel reasoning, knowledge cutoffs", "Speed", "Cost"], 1, "The Concepts glossary lists the limits: hallucination, weak reasoning on novel problems, knowledge cutoffs — the boundaries to design around."),
("The flagship model is overkill when:", ["It is always best", "A smaller model passes your evals", "Never", "The budget is high"], 1, "The Concepts note defines model selection as matching capability to the task with evals — when a smaller model passes, the flagship is overkill."),
("Latency basics:", ["Irrelevant", "Time-to-first-token versus total; size versus quality", "Constant", "Free"], 1, "The Concepts glossary defines the latency arithmetic: time-to-first-token versus total time, model size versus quality."),
("The context window is:", ["Infinite", "The model's finite working memory — managed deliberately", "A database", "Free"], 1, "The Concepts note defines the context window as finite working memory: what fits, what truncates, what it costs to fill."),
("Capabilities to design for are:", ["Everything", "Fluency tasks with verifiable outputs: drafting, summarizing, transforming", "Reasoning", "Memory"], 1, "The Concepts glossary lists capabilities as drafting, summarizing, transforming, conversing within distribution — fluency tasks with verifiable outputs."),
("The hype filter asks:", ["Is it cool", "Does this survive the worst case, or only the demo's best case", "Is it fast", "Is it cheap"], 1, "The Concepts note defines the hype filter as demos versus products: the demo shows the best case; the product survives the worst case."),
("Pricing a feature starts with:", ["The logo", "Estimating tokens in and out at volume", "The demo", "The hype"], 1, "The Hands-on procedure's step 2 prices the feature by estimating tokens in and out at volume — tokens are money."),
("AI PM rounds score:", ["Hype fluency", "Altitude-appropriate literacy: pricing, boundaries, deliberate model choice", "Demo polish", "Jargon"], 1, "The Project brief's grading lens: price the feature, name the boundaries, choose the model deliberately — and tell the demo from the product."),
]}
