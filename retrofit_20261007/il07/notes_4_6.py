# Module notes data, part 2: modules 4-6 (neuroai, openweight, agents)

NOTES = {}

NOTES["il07-neuroai"] = [
("Concepts",
"- **Neural coding: rate** \u2014 spikes/second: the classical view of how neurons encode information.\n"
"- **Neural coding: spike timing** \u2014 temporal codes: the precise view \u2014 still debated against rate coding; hold both views.\n"
"- **Leaky integrate-and-fire (LIF)** \u2014 membrane potential integrates inputs, leaks, spikes at threshold, resets: the workhorse model \u2014 three lines of code, endless dynamics.\n"
"- **Hodgkin-Huxley** \u2014 the biophysical gold standard: ion channels (Na+/K+) with gating variables; detailed but expensive at network scale.\n"
"- **Hebbian learning** \u2014 'fire together, wire together': correlation-based strengthening.\n"
"- **STDP** \u2014 spike-timing-dependent plasticity: pre-before-post strengthens \u2014 causality as a learning rule, with a ~20ms timing window, no teacher needed.\n"
"- **NEURON** \u2014 compartmental modeling: morphology matters \u2014 the dendrite is not a wire; active conductances compute locally.\n"
"- **Brian2** \u2014 spiking networks in Python: define equations as strings, simulate networks of thousands; the model IS the code \u2014 transparency by construction.\n"
"- **Simulation discipline** \u2014 small networks, verified dynamics, then scale: emergent bugs hide in large nets.\n"
"- **Transformer attention vs biological attention** \u2014 both select information, but softmax over tokens \u2260 thalamic gating: the honest analogy is selection mechanisms; the disanalogy is everything about implementation, learning, and energy.\n"
"- **Analogy hygiene** \u2014 say what maps and what doesn't: 'attention is like attention' explains nothing.\n"
"- **Predictive coding / Bayesian brain** \u2014 cortex as prediction machine: prediction errors drive learning; perception as inference \u2014 the framework that unifies perception, action, and learning under prediction error.\n"
"- **Spiking neural networks (SNNs)** \u2014 networks that communicate in spikes rather than dense activations.\n"
"- **Neuromorphic hardware** \u2014 Loihi, SpiNNaker: event-driven, sparse, milliwatt-scale \u2014 spikes are sparse in time, so hardware that exploits sparsity wins on power."),
("Hands-on procedure",
"1. **One neuron.** Install Brian2; define an LIF neuron as an equation string; inject a step current and plot the spike train \u2014 verify the dynamics against the LIF definition before scaling.\n"
"2. **STDP pair.** Build a two-neuron network with an STDP synapse; drive pre-before-post spike pairs and watch the weight grow; reverse the order and watch it shrink.\n"
"3. **The timing window.** Sweep the pre/post delay and plot the weight-change curve \u2014 reproduce the ~20ms window from the Concepts section.\n"
"4. **Scale carefully.** Grow to a few hundred neurons only after single-neuron dynamics verify; note where emergent bugs appear when you skip verification \u2014 the simulation-discipline lesson.\n"
"5. **Count the energy.** Count spikes per second in your network vs the dense matrix multiplies an equivalent ANN layer would perform; state the sparsity argument in your own numbers."),
("Project brief",
"Two deliverables. (1) **The simulation:** a Brian2 notebook with LIF dynamics, STDP learning the temporal order of a pattern, and the timing-window plot. (2) **The honest-analogy essay:** transformer attention vs biological attention \u2014 one page stating exactly what maps, what doesn't, and what would falsify your mapping. Deliverable: the notebook plus the essay."),
("Honesty note",
"Original practice material \u2014 labs, questions, and scenarios are authored for this course. The rate-vs-timing debate is genuinely unsettled: any source that presents it as settled is oversimplifying \u2014 good scientists hold the uncertainty. Neuromorphic efficiency claims are hardware- and workload-dependent; measure, don't quote slogans. Self-check before moving on: state the STDP rule with its window; explain why LIF scales where Hodgkin-Huxley doesn't; name one analogy and one disanalogy between transformers and brains."),
]

NOTES["il07-openweight"] = [
("Concepts",
"- **Open-source (OSI definition)** \u2014 use, study, modify, share: no field-of-use restrictions.\n"
"- **Open-weight** \u2014 weights published, terms vary: adjacent to open-source, not identical.\n"
"- **Apache 2.0 and MIT** \u2014 permissive grants: commercial use, modification, distribution, with attribution/notice.\n"
"- **Custom licenses** \u2014 some families ship bespoke terms (use restrictions, attribution requirements, commercialization conditions).\n"
"- **License card** \u2014 the card for THIS checkpoint is the source of truth: terms change between releases \u2014 license archaeology matters.\n"
"- **License inheritance** \u2014 the rule that trips everyone: distill/fine-tune variants inherit their BASE model's license \u2014 check the lineage.\n"
"- **Commercial-use questions** \u2014 read the grant, the restrictions, and the termination clauses \u2014 then ask a lawyer, not a forum.\n"
"- **Model families** \u2014 Llama, Mistral, Qwen, DeepSeek, Gemma, Phi: release by release, license by license \u2014 never assume from the family name.\n"
"- **Quantization** \u2014 lossy compression of weights: perplexity rises as bits fall; benchmark YOUR tasks.\n"
"- **GGUF** \u2014 llama.cpp's format: the practical ladder Q8_0 \u2192 Q6_K \u2192 Q5_K_M \u2192 Q4_K_M \u2192 Q3_K.\n"
"- **GPTQ / AWQ** \u2014 GPU-optimized 4-bit quantization.\n"
"- **Q4_K_M** \u2014 the sweet spot for most: ~4.4 bits/weight, minimal quality loss \u2014 measure, don't assume.\n"
"- **KV-cache** \u2014 grows with context length: the other half of the memory equation; quantize it for long context.\n"
"- **Context-length cost** \u2014 attention is quadratic: budget the KV cache before the weights.\n"
"- **Ollama** \u2014 the easy path: `ollama run`, Modelfiles, API \u2014 pick it to experiment.\n"
"- **llama.cpp** \u2014 the engine: maximum hardware reach (CPU, Metal, CUDA, Vulkan), server mode \u2014 the hacker's choice to squeeze hardware.\n"
"- **vLLM** \u2014 production serving: PagedAttention, continuous batching, OpenAI-compatible API \u2014 pick it to serve users.\n"
"- **Benchmark trio** \u2014 throughput (tokens/sec), latency (time-to-first-token), quality on YOUR eval set."),
("Hands-on procedure",
"1. **Read the card.** Pick a model family and read the license card for the exact checkpoint; record the grant, the restrictions, and the termination clauses.\n"
"2. **Quantize.** Download the weights; quantize to Q4_K_M with the llama.cpp quantize tool.\n"
"3. **Serve twice.** Serve it with Ollama (write a Modelfile) and separately with llama.cpp server mode; compare the setup friction of each.\n"
"4. **Benchmark honestly.** Measure the trio on your hardware: tokens/sec, time-to-first-token, and quality on a small eval set you write yourself.\n"
"5. **Find the KV wall.** Push context length until the KV cache dominates memory; then enable KV-cache quantization and measure the difference.\n"
"6. **Walk the ladder.** Repeat the quality measurement at Q3_K \u2014 find where YOUR tasks notice the degradation, and write the threshold down."),
("Project brief",
"The self-hosting report: one model, three serving stacks (Ollama, llama.cpp, vLLM), one honest benchmark table (throughput, latency, quality on your evals, memory footprint), plus the license-card summary for the checkpoint you used. Deliverable: the report plus a one-paragraph 'pick by need' recommendation you'd defend to a team."),
("Honesty note",
"Original practice material \u2014 labs, questions, and scenarios are authored for this course. Model families, licenses, and tool versions change fast: everything here is as-of dated \u2014 re-read the license card before any real deployment, and confirm the current checkpoint's terms. Quantization sweet spots are measured on specific hardware \u2014 your numbers will differ; that's the point of the benchmark trio. Self-check before moving on: open-source vs open-weight in one sentence; the license-inheritance rule; the benchmark trio."),
]

NOTES["il07-agents"] = [
("Concepts",
"- **Agent loop** \u2014 every agent is a loop around a model: perceive (observations) \u2192 reason \u2192 act (tools) \u2192 repeat.\n"
"- **Tool calling** \u2014 the primitive: functions the model can invoke, with JSON schemas as the contract.\n"
"- **ReAct** \u2014 Thought \u2192 Action \u2192 Observation, in a while-loop with a step budget: build this once with raw API calls.\n"
"- **Loop ingredients** \u2014 a system prompt (the role), tools (the hands), memory (the notebook), and a stop condition (the discipline).\n"
"- **Step budget** \u2014 the cheapest reliability feature: bounds the loop so a failing tool can't spin forever.\n"
"- **Tool design** \u2014 tool design is API design: clear names, strict schemas, idempotent operations \u2014 the model is only as good as its tools.\n"
"- **LangChain** \u2014 the agent-first API (`create_agent`); middleware (guardrails, retries around the loop); the integration ecosystem \u2014 breadth is why it's chosen.\n"
"- **LangGraph** \u2014 agents as nodes in a graph (Pregel lineage); durable execution (the run survives interruption); checkpoints (rewind/resume first-class); human-in-the-loop as a node.\n"
"- **LlamaIndex** \u2014 data-first: context augmentation as the identity; agents composed with event-driven Workflows; ingestion/indexing/retrieval first-class.\n"
"- **CrewAI** \u2014 the crew metaphor (roles, goals, backstories): crews (role teams) vs flows (event orchestration); memory and guardrails per agent.\n"
"- **Choose by shape** \u2014 linear tools \u2192 LangChain; branching/stateful \u2192 LangGraph; data-grounded \u2192 LlamaIndex; role teams \u2192 CrewAI.\n"
"- **Semantic Kernel** \u2014 kernel + plugins, model-agnostic, C#/Python/Java.\n"
"- **Agent Framework** \u2014 the documented successor path in the Microsoft landscape.\n"
"- **AutoGen** \u2014 conversational multi-agent research: maintenance mode \u2014 know before adopting.\n"
"- **MCP (Model Context Protocol)** \u2014 tools/resources/prompts as a standard: build once, use across harnesses.\n"
"- **DSPy** \u2014 program (don't prompt) the LM: optimize prompts like weights.\n"
"- **Evaluation** \u2014 trajectory scoring (did it take sensible steps?), tool-use accuracy, task success, cost/latency.\n"
"- **Evaluate the trajectory** \u2014 not just the answer: a lucky success teaches nothing.\n"
"- **Failure-mode field guide** \u2014 tool confusion, loop traps, context overflow, prompt injection via tool output.\n"
"- **Prompt injection via tool output** \u2014 THE agent security issue: treat tool returns as untrusted input.\n"
"- **Selection matrix** \u2014 score two frameworks on one task with a rubric: judgment is the deliverable."),
("Hands-on procedure",
"1. **Build ReAct by hand.** With raw API calls, assemble the loop: system prompt, two tools with strict JSON schemas, a memory buffer, and a step budget of 8.\n"
"2. **Watch it loop.** Give it a multi-step task; introduce a failing tool and verify the step budget catches the loop \u2014 the cheapest reliability feature, proven.\n"
"3. **Add a fallback.** On tool failure: retry once, then degrade gracefully; record how the behavior changes.\n"
"4. **Go stateful.** Wrap the same task in LangGraph: define nodes, add a checkpoint, interrupt mid-run, and resume from the checkpoint.\n"
"5. **Standardize with MCP.** Expose one tool via an MCP server; call it from two different harnesses \u2014 build once, use everywhere.\n"
"6. **Score it.** Evaluate a run against the failure-mode field guide: trajectory, tool accuracy, cost/latency \u2014 write the rubric before you score."),
("Project brief",
"The framework bake-off: implement one reference task (a research-and-summarize agent over a document set works well) in TWO frameworks of your choice, score both with a written rubric (trajectory quality, tool accuracy, task success, cost/latency), and defend your pick in writing. Deliverable: both implementations, the selection matrix, and your one-page defense."),
("Honesty note",
"Original practice material \u2014 labs, questions, and scenarios are authored for this course. Framework maintenance status is as-of dated (AutoGen's maintenance mode; Agent Framework as the documented successor path) \u2014 verify before adopting anything for production. Prompt injection via tool output is a real attack surface: treat every tool return as untrusted, in your labs and in production. Self-check before moving on: rebuild the ReAct loop from memory; state the #1 agent security rule; explain when LangGraph beats LangChain."),
]
