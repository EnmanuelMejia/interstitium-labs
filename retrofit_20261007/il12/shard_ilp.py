# IL-12 shard retrofit — second-sentence expansions for 1-sentence il_provides blurbs.
# The build script appends these to the ORIGINAL text (preserved verbatim).
# Key: "<shard>/<path>/<module-id>"

ILP_SECOND = {
"l/aieng-python-foundations/py-syntax-core":
 "I'm your instructor here, and my bar is simple: by the end you read Python the way you'd read your native language — fluently, and with suspicion toward anything you can't predict before running.",
"l/aieng-python-foundations/py-oop-modular":
 "You'll write classes with clean contracts because every ML library you'll touch — estimators, datasets, trainers — is built from exactly this shape.",
"l/aieng-data-science/numpy-foundations":
 "Get shapes, broadcasting, and vectorization fluent now, and PyTorch later will feel like a dialect you already speak.",
"l/aieng-data-science/pandas-wrangling":
 "Expect to spend most of your data hours here: the audit habit — check shapes, counts, and dtypes after every transformation — is what keeps pipelines honest.",
"l/aieng-data-science/viz-matplotlib-seaborn":
 "I teach charts as instruments with an honesty requirement: every figure states its question, labels its axes, and survives a change of framing.",
"l/aieng-data-science/statistics-for-ml":
 "You'll leave able to interrogate any evaluation table — intervals, p-values, base rates — instead of being impressed by it.",
"l/aieng-data-science/model-dev-workflow":
 "Talent picks models; discipline ships results, and this module installs the discipline: splits, pipelines, baselines, reproducibility.",
"l/aieng-machine-learning/supervised-learning":
 "Learn this vocabulary cold — tuning, metrics, and features in the modules ahead are all written in it.",
"l/aieng-machine-learning/unsupervised-learning":
 "My bar for this module is restraint: you'll cluster, then challenge every cluster with external validation before believing it.",
"l/aieng-machine-learning/reinforcement-intro":
 "You'll leave knowing which problems deserve RL — and, more valuably, the long list that don't.",
"l/aieng-machine-learning/validation-tuning":
 "Your score is only as honest as the process that produced it, and this module makes the process airtight.",
"l/aieng-machine-learning/training-data-constraints":
 "Data strategy is engineering strategy: this is the context that keeps your scaling decisions grounded instead of fashionable.",
"l/aieng-deep-learning/backprop-optimization":
 "Do the calculus once by hand with me, and autograd becomes a trusted tool instead of magic — then we learn to read what training curves are telling us.",
"l/aieng-deep-learning/cnns":
 "The one-paragraph insight — shared weights, translation equivariance — plus the transfer-learning workflow that makes small image datasets viable in practice.",
"l/aieng-deep-learning/sequence-models":
 "Read this as the prequel to the transformer: every limitation here is the reason attention was invented.",
"l/aieng-deep-learning/regularization-tuning":
 "The real lesson is experimental discipline: change one thing at a time against a fixed protocol, with a held-out set that stays held out.",
"l/aieng-deep-learning/pytorch-workflows":
 "The loop is five lines; the engineering around it — devices, checkpointing, data loading — is the module, and you'll write it until it's boring.",
"l/aieng-generative-ai/transformers-attention":
 "We'll implement attention by hand so it's an operation you own, then do the scaling math honestly: what improves, what it costs, and what the quadratic tax means.",
"l/aieng-generative-ai/gpt-vs-bert":
 "Two objectives, two destinies — and understanding the fork is what makes the decoder-only convergence legible instead of mysterious.",
"l/aieng-generative-ai/gans-vaes":
 "Literacy, not nostalgia: the conceptual toolkit — distributions, latent spaces, adversarial dynamics — transfers directly to modern generative work.",
"l/aieng-generative-ai/diffusion-generation":
 "You'll calibrate the real controls — steps, guidance, seeds — and leave with the honesty module's rule: generated media proves nothing about the world.",
"l/aieng-generative-ai/prompt-engineering":
 "Prompts are code here: versioned, tested, measured — and you'll build the failure catalog yourself, because that's where the real lessons live.",
"l/aieng-generative-ai/llm-apis-rag":
 "Retrieve, then generate — and you'll evaluate both halves, because retrieval quality bounds answer quality and no prompt fixes bad retrieval.",
"l/aieng-generative-ai/inference-economics-agent-capacity":
 "An original Interstitium lens on serving economics: the per-agent-hour cost model, dated honestly, that every production agent design should carry.",
"m/aieng-nlp/text-preprocessing":
 "Clean signal in or the model learns your dirt: you'll document every transformation, because the corpus is defined by its prep.",
"m/aieng-nlp/tokenization-embeddings":
 "We'll climb the representation ladder rung by rung — and you'll see exactly where static vectors break and context takes over.",
"m/aieng-nlp/nltk-classics":
 "The enduring lesson is inspectability: prefer systems you can debug, and keep the baseline habit for every task that follows.",
"m/aieng-nlp/sequence-models-nlp":
 "Language modeling is the constant across eras; architectures are the variable — this module is the 'before' picture the transformer completes.",
"m/aieng-nlp/hf-pipelines":
 "Pipeline first, fine-tune second, cards read before downloads: the practitioner workflow with the baseline discipline built in.",
"m/aieng-agentic-ai/agent-architectures":
 "Agents are programs and the model is the reasoning subroutine: you'll own the loop — bound it, observe it, and break it on purpose before production does.",
"m/aieng-agentic-ai/langchain-autogen":
 "Frameworks package patterns; the patterns are the curriculum — and you'll learn exactly when the hand-rolled loop beats both frameworks.",
"m/aieng-agentic-ai/copilot-studio":
 "Speed of building never excuses skipping the gate: no production data without DLP and access review, full stop.",
"m/aieng-agentic-ai/azure-ai-foundry":
 "We'll walk the full managed path — project, agent, grounding, evaluation, safety, endpoint — with the platform tradeoffs named honestly, including the exit questions.",
"m/aieng-azure-ai-900/azure-ai-services":
 "The exam is a matching game and this module drills it: workload to service, prebuilt versus custom, with the cost arithmetic to back every pick.",
"m/aieng-azure-ai-900/ml-concepts-azure":
 "Same ML you learned in the engineering path, translated into Microsoft's vocabulary: recognition and service fit, drilled to reflex.",
"m/aieng-azure-ai-900/responsible-ai":
 "Principles don't implement themselves: you'll practice harm identification until it's reflex, and carry the obligations past the exam into production.",
"m/aieng-azure-ai-900/cost-governance":
 "Pricing is scored on the exam and billed in real life: you'll estimate with shown arithmetic and govern with tags, locks, budgets, and residency decisions.",
"m/aieng-capstone/capstone-build":
 "Baseline, error analysis, iterate — with the ledger telling a story a hiring manager can follow from first commit to final demo.",
"m/aieng-capstone/capstone-eval":
 "Held-out numbers, slices, ablations, stress tests, documented limits: anything less than the full evidence bar is a demo, not a result.",
"m/aieng-capstone/capstone-deploy":
 "A served model, monitored inputs, a retraining plan, and a costed demo: MLOps at the scale one engineer can own, with the hiring-manager click as the acceptance test.",
"m/aieng-capstone/capstone-rai":
 "Self-review is the hardest review: you'll name your system's harms plainly, because documented limits build trust and hidden ones destroy it.",
"m/aieng-capstone/capstone-portfolio":
 "Designed for the ten-minute evaluation: a hygienic repo, a story README, a sub-three-minute demo, and honest limits — the career asset the whole path built toward.",
}
