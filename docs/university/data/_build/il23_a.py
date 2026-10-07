"""IL-23 The Frontier — 10 seed modules. All content as-of 2026-10-07; frontier = fast-moving."""
MODULES = [
{
 "id": "m23-transformers", "code": "IL-23", "title": "Transformer Architectures",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "Self-attention, the transformer block, and the architectural family tree \u2014 the established core beneath the fast-moving frontier of model design. As of October 2026.",
 "objectives": ["Explain scaled dot-product attention", "Describe the transformer block's components", "Name the major architectural variants and their motivations", "Distinguish settled core from open research questions"],
 "notes": [
  {"title": "Attention, precisely",
   "body": "**Scaled dot-product attention**: Attention(Q,K,V) = softmax(QK\u1d5b/\u221ad_k)V. Queries match keys; the scores weight the values. **Multi-head** attention runs several of these in parallel subspaces and concatenates. Cost is **quadratic in sequence length** \u2014 the fundamental scaling pressure behind every efficiency variant. (Vaswani et al., 'Attention Is All You Need,' 2017.)"},
  {"title": "The block",
   "body": "A transformer block: multi-head attention + position-wise feed-forward network, each wrapped in a **residual connection** and **normalization** (LayerNorm; many modern models use RMSNorm). **Positional information** is injected \u2014 originally sinusoidal encodings, now typically **rotary embeddings (RoPE)**. Stack N blocks: that is the model."},
  {"title": "The family tree (as of 2026)",
   "body": "Settled patterns: **decoder-only** autoregressive models dominate language modeling; **mixture-of-experts** (sparse expert routing) trades total parameters for active compute; **KV-cache** and its compressions serve long contexts. Active frontier: attention alternatives (state-space models, linear attention), ever-longer effective context, and inference-time compute scaling. Treat any specific 'best' claim as perishable."},
  {"title": "Frontier honesty for this module",
   "body": "The *mechanism* (attention, residuals, normalization) is settled textbook material. Everything about *which variant wins*, scale records, and benchmark leadership changes in months \u2014 verify against current sources before citing. This module teaches the durable core; the daily pipeline appends the moving edge."}
 ],
 "cards": [
  {"front": "Scaled dot-product attention formula?", "back": "Attention(Q,K,V) = softmax(QK\u1d5b/\u221ad_k)V."},
  {"front": "Why is attention quadratic?", "back": "The QK\u1d5b score matrix is n\u00d7n in sequence length \u2014 the core scaling pressure."},
  {"front": "Components of a transformer block?", "back": "Multi-head attention + feed-forward network, each with residual connection and normalization."},
  {"front": "RoPE?", "back": "Rotary Position Embedding \u2014 the now-standard way to inject positional information."},
  {"front": "Mixture-of-experts in one line?", "back": "Sparse routing: many total parameters, few active per token \u2014 capacity without proportional compute."}
 ],
 "quiz": [
  {"q": "The \u221ad_k scaling in attention exists to:",
   "choices": ["Speed up training", "Keep dot products from growing large and saturating softmax", "Reduce memory", "Enable multi-head"],
   "answer": 1,
   "explain": "Large dot products push softmax into flat regions with vanishing gradients; scaling counters it."},
  {"q": "A decoder-only model generates text by:",
   "choices": ["Encoding then decoding", "Autoregressive next-token prediction with causal masking", "Bidirectional infilling only", "Retrieval from a database"],
   "answer": 1,
   "explain": "Causal masking prevents attending to future tokens; generation proceeds left to right."},
  {"q": "Residual connections primarily solve:",
   "choices": ["Overfitting", "Vanishing/exploding gradients in deep stacks", "Slow inference", "Data scarcity"],
   "answer": 1,
   "explain": "Identity shortcuts let gradients flow through dozens of blocks."},
  {"q": "Which claim about model architectures is safest long-term?",
   "choices": ["Model X is the best open model", "Attention is quadratic in sequence length", "Context length records", "Benchmark leadership"],
   "answer": 1,
   "explain": "Mechanism facts are durable; leadership claims are perishable \u2014 the module's honesty rule."}
 ]
},
{
 "id": "m23-quantum", "code": "IL-23", "title": "Quantum Computing Basics",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "Qubits, superposition, entanglement, and the gate model \u2014 what quantum computers are, what they aren't, and where the field stands. As of October 2026.",
 "objectives": ["Describe a qubit and how it differs from a bit", "Explain superposition and entanglement operationally", "Name the landmark algorithms and what they actually speed up", "State the field's honest status: NISQ era, error correction frontier"],
 "notes": [
  {"title": "Qubits",
   "body": "A **qubit** is a two-level quantum system: |\u03c8\u27e9 = \u03b1|0\u27e9 + \u03b2|1\u27e9 with |\u03b1|\u00b2+|\u03b2|\u00b2 = 1. **Superposition** is not 'both values at once' in a classical sense \u2014 it is a new kind of state whose measurement statistics follow the Born rule. n qubits live in a 2\u207f-dimensional state space: that exponentiality is the resource \u2014 and the reason simulation is hard."},
  {"title": "Entanglement and gates",
   "body": "**Entanglement**: correlations between qubits stronger than any classical correlation (Bell's theorem, experimentally confirmed \u2014 Nobel Prize 2022: Aspect, Clauser, Zeilinger). The **gate model** applies unitary operations (Hadamard, CNOT, phase gates); measurement collapses to classical bits. Algorithms are interference choreography: amplify right answers, cancel wrong ones."},
  {"title": "The algorithms that matter",
   "body": "**Shor's** (1994): exponential speedup for factoring/discrete log \u2014 threatens RSA/ECC *when* large fault-tolerant machines exist. **Grover's** (1996): quadratic speedup for unstructured search. Quantum simulation (Feynman's original 1982 motivation) remains the most plausible near-term scientific win. Claims beyond these need scrutiny \u2014 most 'quantum advantage' demos are narrow and contested."},
  {"title": "Honest status (2026)",
   "body": "The field is in the **NISQ** era (noisy intermediate-scale quantum): hundreds\u2013thousands of physical qubits, high error rates. **Fault tolerance** via quantum error correction (surface codes and successors) needs roughly 10\u00b3\u201310\u2074 physical qubits per logical qubit \u2014 the central engineering mountain. Timelines for cryptographically relevant machines are expert-disputed; treat any date as a claim, not a fact."}
 ],
 "cards": [
  {"front": "Qubit state and normalization?", "back": "|\u03c8\u27e9 = \u03b1|0\u27e9+\u03b2|1\u27e9, |\u03b1|\u00b2+|\u03b2|\u00b2=1; measurement follows the Born rule."},
  {"front": "Why is n-qubit simulation hard classically?", "back": "The state space is 2\u207f-dimensional \u2014 exponential in n."},
  {"front": "Shor's vs. Grover's speedups?", "back": "Shor: exponential (factoring/discrete log). Grover: quadratic (unstructured search)."},
  {"front": "NISQ?", "back": "Noisy Intermediate-Scale Quantum \u2014 current era: many physical qubits, high errors, no fault tolerance yet."},
  {"front": "The error-correction mountain?", "back": "~10\u00b3\u201310\u2074 physical qubits per logical qubit \u2014 the central engineering challenge."}
 ],
 "quiz": [
  {"q": "Bell's theorem (Nobel 2022) established:",
   "choices": ["Faster-than-light signaling", "Quantum correlations exceeding any classical explanation", "That qubits are just bits", "Perpetual motion"],
   "answer": 1,
   "explain": "Aspect, Clauser, Zeilinger confirmed entanglement's non-classical correlations experimentally."},
  {"q": "Shor's algorithm threatens RSA because it:",
   "choices": ["Breaks all encryption today", "Factors efficiently on a large fault-tolerant quantum computer", "Is already running on laptops", "Only affects symmetric crypto"],
   "answer": 1,
   "explain": "The threat is real but conditional on fault-tolerant scale \u2014 which does not yet exist."},
  {"q": "A quantum gate must be:",
   "choices": ["Irreversible", "Unitary (reversible); measurement is the irreversible step", "Classical", "Random"],
   "answer": 1,
   "explain": "Computation is unitary evolution; only measurement collapses to classical outcomes."},
  {"q": "The most defensible near-term application:",
   "choices": ["Breaking RSA tomorrow", "Quantum simulation of physical systems", "Quantum smartphones", "Replacing all classical computing"],
   "answer": 1,
   "explain": "Feynman's 1982 motivation \u2014 simulating quantum systems with quantum systems \u2014 remains the plausible first win."}
 ]
},
{
 "id": "m23-crispr", "code": "IL-23", "title": "CRISPR & Gene Editing",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "How CRISPR-Cas9 works, what base and prime editing add, and where therapeutic gene editing stands \u2014 with the ethics up front. As of October 2026.",
 "objectives": ["Explain the CRISPR-Cas9 mechanism", "Distinguish base editing and prime editing", "Name approved/sanctioned therapeutic uses as of 2026", "Discuss germline vs. somatic editing ethics"],
 "notes": [
  {"title": "The mechanism",
   "body": "**CRISPR-Cas9**: a guide RNA (~20 nt) directs the Cas9 nuclease to a complementary DNA sequence adjacent to a **PAM** site; Cas9 makes a double-strand break. The cell's repair \u2014 error-prone NHEJ (knockout) or HDR with a template (precise edit) \u2014 does the rest. (Doudna/Charpentier, 2012; Nobel 2020.) It is programmable cut-and-paste for genomes \u2014 with off-target cuts as the central safety concern."},
  {"title": "Base and prime editing",
   "body": "**Base editors** (2016\u2013): deaminase fused to nickase-Cas9 \u2014 chemically convert one base to another (C\u2192T, A\u2192G) without double-strand breaks. **Prime editing** (2019): nickase fused to reverse transcriptase writes longer edits from an RNA template. Both reduce reliance on double-strand breaks \u2014 the field's direction is *precision without breakage*."},
  {"title": "Therapeutic status (as of 2026)",
   "body": "The first CRISPR therapy \u2014 **Casgevy (exagamglogene autotemcel)** for sickle-cell disease and beta thalassemia \u2014 was approved in late 2023 (UK/US), an *ex vivo* edit of patients' own blood stem cells. In-vivo programs (e.g., for transthyretin amyloidosis, hereditary angioedema) were in trials. This is the honest frontier: real approvals exist, most applications remain investigational \u2014 check current trial registries before citing."},
  {"title": "The ethics",
   "body": "**Somatic** editing (treated patient's body cells) is broadly accepted under regulation. **Germline** editing (heritable) remains widely condemned after He's 2018 CRISPR-babies case \u2014 international consensus (summits 2015, 2018, 2023) holds the line at no clinical germline editing. The ethical frontier: equitable access to million-dollar cures, and enhancement vs. therapy boundaries."}
 ],
 "cards": [
  {"front": "CRISPR-Cas9 mechanism in one pass?", "back": "Guide RNA directs Cas9 to a PAM-adjacent target; double-strand break; cell repair (NHEJ/HDR) makes the edit."},
  {"front": "Base editing vs. prime editing?", "back": "Base: single-letter chemical conversion, no DSB. Prime: reverse-transcriptase writes longer edits from RNA template."},
  {"front": "Casgevy: what, for what, when?", "back": "Ex vivo CRISPR therapy for sickle-cell/beta-thalassemia; approved late 2023 (UK/US) \u2014 first CRISPR approval."},
  {"front": "Somatic vs. germline editing (ethics)?", "back": "Somatic: regulated acceptance. Germline: international consensus against clinical use (post-2018)."},
  {"front": "The central technical safety concern?", "back": "Off-target cuts/edits \u2014 the field's precision drive targets exactly this."}
 ],
 "quiz": [
  {"q": "Cas9 needs, in addition to guide-RNA complementarity:",
   "choices": ["Nothing else", "A PAM site adjacent to the target", "A second Cas9", "Radioactivity"],
   "answer": 1,
   "explain": "The protospacer-adjacent motif licenses cutting \u2014 a key specificity determinant."},
  {"q": "NHEJ vs. HDR after the cut:",
   "choices": ["Both precise", "NHEnd joining: error-prone knockout; HDR: template-precise edit", "HDR is error-prone", "Neither matters"],
   "answer": 1,
   "explain": "The repair pathway decides the outcome \u2014 most therapeutic strategies wrestle with this."},
  {"q": "Prime editing's advantage over standard Cas9:",
   "choices": ["Bigger cuts", "Longer precise edits without double-strand breaks", "No guide RNA needed", "Works on RNA only"],
   "answer": 1,
   "explain": "Nickase + reverse transcriptase writes from a template \u2014 precision without breakage."},
  {"q": "The 2018 He Jiankui case concerned:",
   "choices": ["A new Cas protein", "Heritable (germline) editing of babies \u2014 globally condemned", "A sickle-cell cure", "Agricultural CRISPR"],
   "answer": 1,
   "explain": "The case that hardened the international line against clinical germline editing."}
 ]
},
{
 "id": "m23-fusion", "code": "IL-23", "title": "Fusion Energy Status",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "Magnetic vs. inertial confinement, the NIF ignition milestone, private fusion's surge \u2014 and why grid power remains the mountain. As of October 2026.",
 "objectives": ["Explain the two confinement approaches", "State what NIF's ignition did and didn't prove", "Name the leading private efforts and their approaches", "Give the honest timeline framing"],
 "notes": [
  {"title": "Two confinements",
   "body": "**Magnetic confinement** (tokamaks, stellarators): hold a 100M\u00b0C plasma with magnetic fields \u2014 ITER (France, international) is the giant; stellarators (Wendelstein 7-X) trade engineering complexity for steadier plasma. **Inertial confinement**: crush fuel pellets with lasers \u2014 NIF's approach. Both chase the same figure of merit: **Q**, fusion energy out over heating energy in."},
  {"title": "NIF ignition (2022)",
   "body": "The National Ignition Facility achieved **scientific breakeven** (December 2022, repeated since): fusion output exceeded laser energy delivered to the target. What it did *not* prove: wall-plug breakeven (lasers are inefficient), repetition rate (NIF fires ~daily; power needs ~10/second), or economics. A physics milestone, not an energy milestone \u2014 the distinction matters."},
  {"title": "Private fusion's surge",
   "body": "Since ~2020, private capital flooded in: **Commonwealth Fusion Systems** (tokamak + high-temperature superconducting magnets), **Helion** (pulsed magneto-inertial, aiming direct electricity conversion), **TAE**, **General Fusion**, and others \u2014 collectively billions raised. HTS magnets are the enabling technology story: stronger fields \u21d2 smaller, cheaper tokamaks. Company timelines cluster optimistically; treat them as targets."},
  {"title": "The honest framing",
   "body": "'Fusion is 30 years away' is a joke with a point: the physics keeps progressing (ignition was real) while *grid electricity* needs Q\u226b1 at the wall plug, materials surviving neutron bombardment, tritium breeding, and cost-competitive $/MWh. Progress is genuine; power-plant timelines remain expert-disputed. Date every claim."}
 ],
 "cards": [
  {"front": "Magnetic vs. inertial confinement?", "back": "Magnetic: tokamaks/stellarators hold hot plasma in fields. Inertial: lasers crush pellets (NIF)."},
  {"front": "Q?", "back": "Fusion energy out / heating energy in \u2014 the figure of merit."},
  {"front": "What did NIF 2022 prove \u2014 and not prove?", "back": "Scientific breakeven (target gain > 1), repeated. Not: wall-plug gain, rep rate, economics."},
  {"front": "HTS magnets: why they matter?", "back": "Stronger fields \u21d2 smaller/cheaper tokamaks \u2014 the private-fusion enabling story (CFS et al.)."},
  {"front": "The four mountains to grid power?", "back": "Wall-plug Q, neutron-surviving materials, tritium breeding, competitive $/MWh."}
 ],
 "quiz": [
  {"q": "ITER is an example of:",
   "choices": ["Inertial confinement", "Magnetic confinement (tokamak), international", "A private startup", "A fission plant"],
   "answer": 1,
   "explain": "The world's largest tokamak experiment, under construction in France."},
  {"q": "NIF's ignition means fusion power plants are:",
   "choices": ["Imminent", "Proven at the physics level; engineering/economics unproven", "Impossible", "Already on the grid"],
   "answer": 1,
   "explain": "Target gain > 1 is real physics; everything about power plants remains ahead."},
  {"q": "A stellarator differs from a tokamak mainly in:",
   "choices": ["Fuel used", "Magnetic geometry \u2014 steadier plasma at higher engineering complexity", "Size only", "Country of origin"],
   "answer": 1,
   "explain": "Wendelstein 7-X: twisted coils shape the field without tokamak plasma current."},
  {"q": "Helion's distinctive bet:",
   "choices": ["Bigger tokamaks", "Pulsed magneto-inertial fusion with direct electricity conversion", "Laser arrays", "Fission-fusion hybrid"],
   "answer": 1,
   "explain": "Skipping the steam cycle \u2014 if it works, a different economics entirely."}
 ]
},
{
 "id": "m23-bci", "code": "IL-23", "title": "Brain\u2013Computer Interfaces",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "Invasive vs. non-invasive BCIs, what decoding actually achieves today, and the clinical frontier \u2014 plus the neuroethics. As of October 2026.",
 "objectives": ["Distinguish invasive, semi-invasive, and non-invasive BCIs", "Describe what neural decoding can and cannot do today", "Name the clinical applications in trials", "Raise the core neuroethical questions"],
 "notes": [
  {"title": "The signal ladder",
   "body": "**Non-invasive** (EEG, fNIRS): scalp signals \u2014 safe, but centimeters of skull blur everything; good for coarse control. **Semi-invasive** (ECoG): electrodes on the brain surface \u2014 better signal, requires surgery. **Invasive** (Utah arrays, Neuralink-style threads): single-neuron resolution, highest bandwidth, highest risk. The trade is always **bandwidth vs. invasiveness**."},
  {"title": "What decoding does today",
   "body": "Motor BCIs let paralyzed users move cursors and robotic arms by decoded intent; **speech neuroprostheses** reconstruct intended speech from motor cortex at improving rates (2021\u20132024 papers showed striking progress). What it is *not*: mind reading \u2014 decoding works on trained tasks with cooperating subjects and heavy ML; 'thought extraction' headlines outrun the science by miles."},
  {"title": "Clinical frontier (as of 2026)",
   "body": "Trials target paralysis (motor/speech restoration), with companies (Neuralink, Synchron, Precision Neuroscience, Paradromics) and academic labs pushing implant counts and longevity. The honest state: genuine restored function for some patients, early days for scale \u2014 electrode longevity, surgical risk, and regulatory pathways are the binding constraints, not just decoding algorithms."},
  {"title": "Neuroethics",
   "body": "BCIs raise questions other tech doesn't: **mental privacy** (neural data is the most intimate data class), **agency** (who authored a decoded action?), **consent** for locked-in patients, and **enhancement** divides. The field's norm \u2014 encode these *before* the capability arrives, per the Collingridge lesson (IL-21). Regulation here is genuinely unsettled; watch it."}
 ],
 "cards": [
  {"front": "The BCI signal ladder?", "back": "Non-invasive (EEG: safe, coarse) \u2192 ECoG (surface, surgery) \u2192 invasive (single-neuron, highest bandwidth/risk)."},
  {"front": "The core trade?", "back": "Bandwidth vs. invasiveness \u2014 always."},
  {"front": "Speech neuroprostheses: state of play?", "back": "Reconstructing intended speech from motor cortex; rapid progress 2021\u20132024; trained tasks, cooperating subjects."},
  {"front": "What BCI is NOT?", "back": "Mind reading \u2014 decoding needs training, cooperation, and heavy ML on specific tasks."},
  {"front": "Three neuroethical questions?", "back": "Mental privacy, agency/authorship of decoded actions, consent \u2014 plus enhancement divides."}
 ],
 "quiz": [
  {"q": "ECoG sits between EEG and Utah arrays in:",
   "choices": ["Cost only", "Invasiveness and signal quality", "Age of the technology", "Nothing \u2014 they're equivalent"],
   "answer": 1,
   "explain": "Surface electrodes: surgery required, but far better signal than scalp EEG."},
  {"q": "A headline claims 'AI reads minds.' The informed response:",
   "choices": ["Accept it", "Decoding works on trained tasks with cooperating subjects \u2014 far from general mind reading", "Deny all BCI progress", "Buy the company's stock"],
   "answer": 1,
   "explain": "The honest position credits real progress while rejecting the extrapolation."},
  {"q": "The binding constraints on clinical BCI scale are:",
   "choices": ["Only algorithms", "Electrode longevity, surgical risk, regulation \u2014 not just decoding", "Lack of interest", "Battery size alone"],
   "answer": 1,
   "explain": "Implants must survive years in the body and clear regulators \u2014 hardware and policy, not just ML."},
  {"q": "Neural data deserves special protection because:",
   "choices": ["It's large", "It's the most intimate data class \u2014 mental privacy", "It's expensive", "It's noisy"],
   "answer": 1,
   "explain": "The neuroethical core: thoughts-adjacent data needs a higher bar."}
 ]
},
{
 "id": "m23-agents", "code": "IL-23", "title": "AI Agents & Inference-Time Compute",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "From chatbots to agents: tool use, planning loops, and the shift from training-time to inference-time scaling. As of October 2026.",
 "objectives": ["Describe the agent loop: perceive, plan, act, observe", "Explain tool use and function calling", "State the inference-time scaling thesis", "Name the evaluation and safety challenges"],
 "notes": [
  {"title": "The agent loop",
   "body": "An **AI agent** wraps a model in a loop: observe state \u2192 reason/plan \u2192 **act via tools** (APIs, code execution, browsers) \u2192 observe results \u2192 repeat. The model supplies the policy; the scaffolding supplies memory, tools, and persistence. Capabilities come from the *system*, not the weights alone \u2014 which is why evals must test systems, not just models."},
  {"title": "Tool use",
   "body": "**Function calling / tool use**: the model emits structured calls (JSON schemas), the harness executes them and returns observations. This grounds models in live data and real actions \u2014 and creates the attack surface: **prompt injection** (malicious instructions in tool outputs) is the signature vulnerability of the agent era. Treat every tool output as untrusted data."},
  {"title": "Inference-time scaling",
   "body": "The post-2024 thesis: capability also scales with **compute spent at inference** \u2014 longer chains of thought, sampling many candidates, search and verification, multi-agent debate. 'Test-time compute' became a second scaling axis alongside training compute. The economics flip: intelligence becomes *runnable* cost, and latency/cost budgets become design parameters."},
  {"title": "Evals and safety",
   "body": "Agent evals are genuinely hard: long-horizon tasks, nondeterminism, and environments that fight back. Benchmarks saturate; real deployment surprises persist. Safety work focuses on **containment** (least-privilege tools, human approval gates), **monitoring** (action logs, anomaly detection), and **alignment** of the planner itself. The frontier moves too fast for settled textbooks \u2014 read primary sources."}
 ],
 "cards": [
  {"front": "The agent loop?", "back": "Observe \u2192 plan \u2192 act via tools \u2192 observe \u2192 repeat; model = policy, scaffolding = memory/tools/persistence."},
  {"front": "Prompt injection?", "back": "Malicious instructions embedded in tool outputs/data \u2014 the signature vulnerability of tool-using agents."},
  {"front": "Inference-time scaling thesis?", "back": "Capability scales with compute spent at inference (longer reasoning, sampling, search) \u2014 a second scaling axis."},
  {"front": "Why evals must test systems, not models?", "back": "Capability lives in model + scaffolding + tools; weights-alone benchmarks miss it."},
  {"front": "Three agent-safety layers?", "back": "Containment (least privilege, approval gates), monitoring (logs, anomaly detection), planner alignment."}
 ],
 "quiz": [
  {"q": "Function calling works by:",
   "choices": ["The model browsing the web freely", "Structured calls (schemas) executed by the harness, observations returned", "Hardcoded scripts only", "Human operators typing"],
   "answer": 1,
   "explain": "JSON-schema calls the model emits; the system executes and feeds back results."},
  {"q": "Prompt injection is dangerous because:",
   "choices": ["It slows the model", "Tool outputs are data, but the model may treat embedded text as instructions", "It costs more", "It only affects images"],
   "answer": 1,
   "explain": "The data/instruction boundary collapses \u2014 untrusted content steering a trusted agent."},
  {"q": "Inference-time compute trades:",
   "choices": ["Nothing", "Latency and cost for capability \u2014 intelligence as runnable cost", "Accuracy for speed only", "Training data for parameters"],
   "answer": 1,
   "explain": "The economic flip: you can buy smarter answers per query."},
  {"q": "The hardest part of agent evaluation:",
   "choices": ["Writing the code", "Long horizons, nondeterminism, adversarial environments; benchmarks saturate", "Finding GPUs", "Naming the agent"],
   "answer": 1,
   "explain": "Real deployment keeps surprising saturated benchmarks \u2014 eval science lags capability."}
 ]
},
{
 "id": "m23-semiconductors", "code": "IL-23", "title": "Semiconductor Scaling Beyond Moore",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "Where Moore's law stands, what replaced it (chiplets, 3D stacking, new lithography), and why compute is the strategic resource. As of October 2026.",
 "objectives": ["State Moore's law and its current status", "Explain chiplets, 3D stacking, and advanced packaging", "Describe EUV lithography's role", "Connect compute to AI progress economics"],
 "notes": [
  {"title": "Moore's law, honestly",
   "body": "**Moore's law** (1965): transistor counts doubling ~every 2 years. The *economic* version (cheaper transistors) slowed around the mid-2010s as fabs hit atomic and economic limits; the *density* version continues via 3D structures (FinFET \u2192 gate-all-around). 'Moore's law is dead' and 'alive' are both slogans \u2014 the truth: single-thread scaling ended (~2005, the power wall), density scaling continues expensively."},
  {"title": "The new scaling: packaging",
   "body": "**Chiplets**: compose big chips from small dies (better yields, mix-and-match process nodes) \u2014 AMD's bet, now industry standard. **3D stacking** (HBM memory stacks, hybrid bonding): bandwidth through the vertical dimension. **Advanced packaging** (CoWoS and successors) is now as strategic as lithography \u2014 the bottleneck for AI accelerators is packaging capacity, not just wafers."},
  {"title": "Lithography",
   "body": "**EUV** (extreme ultraviolet, 13.5nm) lithography \u2014 ASML's machines, each the most complex mass-produced artifact in history \u2014 enabled sub-10nm nodes. **High-NA EUV** is the next step (finer features, eye-watering cost). One Dutch company holding the keys to the frontier is itself a geopolitical fact."},
  {"title": "Compute as strategy",
   "body": "AI progress now visibly tracks **compute**: training runs measured in tens of thousands of accelerators, datacenters as the new factories. Export controls on advanced chips (US, from 2022) made semiconductors an instrument of statecraft. For the technologist: performance engineering increasingly means *parallelism and memory hierarchy*, not waiting for faster cores."}
 ],
 "cards": [
  {"front": "Moore's law: statement and status?", "back": "Transistor doubling ~2yr (1965). Single-thread scaling ended ~2005; density continues expensively; economic doubling slowed ~2010s."},
  {"front": "Chiplets? 3D stacking?", "back": "Chiplets: small dies composed (yields, node mixing). 3D: vertical integration (HBM) for bandwidth."},
  {"front": "EUV and High-NA EUV?", "back": "13.5nm lithography enabling sub-10nm (ASML); High-NA = finer features, next step."},
  {"front": "Why is packaging now strategic?", "back": "CoWoS-class capacity bottlenecks AI accelerators \u2014 packaging rivals lithography in importance."},
  {"front": "The performance-engineering implication?", "back": "Parallelism + memory hierarchy, not faster cores \u2014 the power wall ended free single-thread gains."}
 ],
 "quiz": [
  {"q": "The 'power wall' (~2005) ended:",
   "choices": ["All progress", "Free single-thread performance gains from frequency scaling", "Transistor shrinking", "Multicore"],
   "answer": 1,
   "explain": "Dennard scaling broke; clocks stalled; the industry went multicore."},
  {"q": "Chiplets improve economics mainly via:",
   "choices": ["Faster transistors", "Better yields on small dies + mixing process nodes", "Lower power", "Simpler design"],
   "answer": 1,
   "explain": "Small dies dodge defect statistics; logic and I/O can use different nodes."},
  {"q": "HBM (high-bandwidth memory) achieves bandwidth through:",
   "choices": ["Higher clocks", "3D stacking with through-silicon vias", "Bigger caches", "Optical links"],
   "answer": 1,
   "explain": "Vertical stacking + wide interfaces \u2014 the memory wall's current answer."},
  {"q": "US chip export controls (from 2022) show:",
   "choices": ["Chips are commodities", "Compute is an instrument of statecraft", "Lithography is easy", "AI needs no hardware"],
   "answer": 1,
   "explain": "Advanced semiconductors became geopolitical \u2014 strategy, not just supply chain."}
 ]
},
{
 "id": "m23-synbio", "code": "IL-23", "title": "Synthetic Biology",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "Engineering biology: DNA synthesis and sequencing economics, the design-build-test-learn loop, and what biofoundries actually produce. As of October 2026.",
 "objectives": ["Explain the DBTL loop", "State the cost trajectories of sequencing and synthesis", "Name real synbio products and platforms", "Raise biosecurity as the field's Collingridge problem"],
 "notes": [
  {"title": "Reading and writing DNA",
   "body": "**Sequencing** cost fell ~100,000\u00d7 since 2007 (faster than Moore's law for a decade) \u2014 a human genome now costs hundreds of dollars. **Synthesis** (writing DNA) fell slower but steadily; gene-length synthesis is routine, genome-scale writing remains heroic. The gap matters: reading is cheap, writing is the frontier."},
  {"title": "The DBTL loop",
   "body": "**Design\u2013Build\u2013Test\u2013Learn**: specify a genetic construct, synthesize/assemble it, test in cells, learn from data \u2014 the engineering cycle applied to biology. **Biofoundries** automate it (liquid handling, high-throughput screening). Biology's version of the compile-run-debug loop, with evolution as the legacy codebase."},
  {"title": "What it produces (as of 2026)",
   "body": "Real products: engineered **insulin** and biologics (the old wins), **bio-based materials** (spider-silk proteins, mycelium), **fermentation-produced** chemicals displacing petrochemistry, **cell therapies** (CAR-T). mRNA vaccines (2020) proved the platform logic: *programmable* biology. Most synbio revenue is still tools and services \u2014 the application layer is early."},
  {"title": "Biosecurity",
   "body": "The Collingridge problem in a lab coat: synthesis screening, the **Australia Group** lists, and debates over publishing methods of concern. As capabilities diffuse, governance leans on **screening synthesis orders** and norms \u2014 imperfect, evolving, and genuinely contested. The field's social license depends on getting this visibly right."}
 ],
 "cards": [
  {"front": "Sequencing vs. synthesis cost trajectories?", "back": "Sequencing: ~100,000\u00d7 cheaper since 2007. Synthesis: falling, slower \u2014 writing is the frontier."},
  {"front": "The DBTL loop?", "back": "Design\u2013Build\u2013Test\u2013Learn: specify, synthesize, test in cells, learn \u2014 biology's compile-run-debug."},
  {"front": "Three real synbio product classes?", "back": "Biologics/cell therapies, bio-materials (silk proteins, mycelium), fermentation chemicals."},
  {"front": "The mRNA-vaccine lesson?", "back": "Platform logic proven: programmable biology can answer in months, not decades."},
  {"front": "The biosecurity posture?", "back": "Synthesis-order screening, control lists, publication norms \u2014 imperfect, evolving, contested."}
 ],
 "quiz": [
  {"q": "A human genome sequence in 2026 costs roughly:",
   "choices": ["Millions", "Hundreds of dollars", "Tens of thousands", "Nothing"],
   "answer": 1,
   "explain": "The ~$1,000 genome arrived in the 2010s; costs kept falling into the hundreds."},
  {"q": "The DBTL loop's 'Learn' step uses:",
   "choices": ["Textbooks", "Data from the Test step to improve the next Design", "Meditation", "Patents"],
   "answer": 1,
   "explain": "The loop is iterative \u2014 measured performance feeds redesign."},
  {"q": "Genome-scale DNA writing remains 'heroic' because:",
   "choices": ["It's illegal", "Synthesis cost and error rates scale badly with length", "No one wants it", "Sequencing is better"],
   "answer": 1,
   "explain": "Writing long perfect DNA is still expensive and error-prone \u2014 the synthesis frontier."},
  {"q": "Synthesis screening exists to:",
   "choices": ["Lower costs", "Catch orders for sequences of concern \u2014 biosecurity", "Speed delivery", "Improve quality only"],
   "answer": 1,
   "explain": "DNA synthesis providers screen against pathogen lists \u2014 the governance layer."}
 ]
},
{
 "id": "m23-space", "code": "IL-23", "title": "Space Infrastructure",
 "weight": 1, "asOf": "2026-10-07",
 "summary": "Reusable launch economics, megaconstellations, and the cislunar horizon \u2014 space as infrastructure, not spectacle. As of October 2026.",
 "objectives": ["Explain the reusable-launch cost revolution", "Describe megaconstellations as infrastructure", "Outline the cislunar/Artemis program", "Name the orbital-debris problem honestly"],
 "notes": [
  {"title": "The launch revolution",
   "body": "**SpaceX's Falcon 9** (first booster landing 2015) cut orbital launch costs roughly an order of magnitude \u2014 from ~$10,000/kg toward ~$1,000/kg-class economics. **Starship** (fully reusable, super-heavy) aims for another order of magnitude; as of 2026 it was flying test and early operational missions with full rapid reusability still in work. The lesson: *reusability*, not new physics, moved the curve."},
  {"title": "Megaconstellations",
   "body": "**Starlink** (thousands of satellites, operational since 2020) proved LEO broadband at scale \u2014 latency and coverage impossible for GEO. Competitors (OneWeb, Kuiper) follow. Consequences: astronomy's light-pollution fight, spectrum/orbit coordination crises, and a genuine connectivity layer for remote regions. Infrastructure has side effects \u2014 always."},
  {"title": "The cislunar horizon",
   "body": "NASA's **Artemis** program targets sustained lunar presence (Gateway station, surface missions) with commercial landers; China pursues parallel lunar plans (ILRS). The strategic logic: the Moon as proving ground and resource base (water ice \u2192 propellant). Timelines have slipped repeatedly \u2014 date every claim, and distinguish funded hardware from renderings."},
  {"title": "Debris",
   "body": "Tens of thousands of tracked objects, millions of lethal-but-untracked fragments; the **Kessler syndrome** (collisional cascade) is the tail risk. Megaconstellations multiply the conjunction load. Active debris removal is demonstrated in pieces, not at scale. The honest framing: orbit is a commons, and commons need governance \u2014 currently thin."}
 ],
 "cards": [
  {"front": "The Falcon 9 cost revolution?", "back": "Reusable booster (landings from 2015) cut $/kg roughly 10\u00d7 \u2014 reusability, not new physics."},
  {"front": "Starship's goal?", "back": "Fully reusable super-heavy lift; another order-of-magnitude cost cut \u2014 rapid reusability still in work as of 2026."},
  {"front": "Why LEO beats GEO for broadband?", "back": "Latency: ~500km vs ~36,000km altitude \u2014 physics, not marketing."},
  {"front": "Artemis: the strategic logic?", "back": "Sustained lunar presence; Moon as proving ground + resource base (water \u2192 propellant)."},
  {"front": "Kessler syndrome?", "back": "Collisional cascade: debris collisions breeding more debris \u2014 the orbital tail risk."}
 ],
 "quiz": [
  {"q": "Falcon 9's cost impact came mainly from:",
   "choices": ["New fuel chemistry", "First-stage reusability", "Bigger fairings", "Government subsidies"],
   "answer": 1,
   "explain": "Landing and reflying boosters amortized the expensive hardware."},
  {"q": "Starlink's key technical enabler:",
   "choices": ["Bigger satellites", "Cheap launch + mass-produced LEO satellites", "Undersea cables", "Quantum links"],
   "answer": 1,
   "explain": "The constellation business closes only with low $/kg and satellite mass production."},
  {"q": "Lunar water ice matters because:",
   "choices": ["Drinking water for tourists", "Propellant feedstock (split to H2/O2) \u2014 the cislunar economy's oil", "Scientific curiosity only", "It proves life"],
   "answer": 1,
   "explain": "In-space propellant changes the rocket equation's economics \u2014 the strategic prize."},
  {"q": "The honest way to read a 2028 lunar-base announcement:",
   "choices": ["Accept the date", "Distinguish funded hardware from renderings; timelines have slipped repeatedly", "Dismiss all space plans", "Assume it's already built"],
   "answer": 1,
   "explain": "Date every claim; hardware talks, renderings walk."}
 ]
},
{
 "id": "m23-frontier-method", "code": "IL-23", "title": "The Frontier Method",
 "weight": 1,
 "summary": "How to read the fast-moving edge honestly: preprints, benchmarks, hype detection, and the as-of discipline \u2014 the meta-skill this academy exists to teach.",
 "objectives": ["Read a preprint critically in 20 minutes", "Detect hype patterns in tech announcements", "Apply the as-of discipline to every frontier claim", "Maintain a personal frontier radar"],
 "notes": [
  {"title": "Reading a preprint in 20 minutes",
   "body": "The protocol: (1) **Abstract + claims** \u2014 what exactly is asserted? (2) **Method** \u2014 what was actually done, on what data, with what controls? (3) **Results vs. claims** \u2014 do the figures support the abstract? (4) **Baselines** \u2014 were competitors given a fair fight? (5) **Limitations** \u2014 stated or conspicuous by absence? (6) **Provenance** \u2014 who wrote it, what's their incentive? Most papers fail at step 3 or 4."},
  {"title": "Hype patterns",
   "body": "Watch for: **benchmark cherry-picking** (one metric, friendly settings); **the demo/data gap** (works on stage, untested in the wild); **category errors** ('quantum' + 'consciousness'); **timeline laundering** (a target quoted as a fact); **authority borrowing** (a famous name, no relevant expertise); **the inevitable graph** (exponential pasted onto a noisy series). Each has a question that kills it \u2014 learn the questions."},
  {"title": "The as-of discipline",
   "body": "Every frontier claim gets a **date** and a **half-life estimate**: mechanism facts (years), product claims (months), leadership claims (weeks). Write 'as of <date>' reflexively. When you cite a frontier fact older than its half-life, re-verify or qualify. This academy's modules carry asOf fields for exactly this reason \u2014 and the daily pipeline keeps them fresh."},
  {"title": "Your frontier radar",
   "body": "Maintain: 2\u20133 **primary sources** (arXiv categories, conference proceedings), 1 **aggregator** you trust, 1 **skeptic** who is usually right, and a **claim log** \u2014 predictions with dates, revisited quarterly. The log is the instrument: it converts consumption into calibration. The frontier rewards the calibrated, not the first."}
 ],
 "cards": [
  {"front": "The 20-minute preprint protocol?", "back": "Claims \u2192 method \u2192 results-vs-claims \u2192 baselines \u2192 limitations \u2192 provenance."},
  {"front": "Name four hype patterns and their killing questions.", "back": "Cherry-picking (which metrics were omitted?); demo/data gap (tested in the wild?); timeline laundering (target or fact?); authority borrowing (relevant expertise?)."},
  {"front": "The as-of discipline?", "back": "Date every claim; estimate its half-life (mechanism: years; product: months; leadership: weeks); re-verify past half-life."},
  {"front": "A personal frontier radar needs?", "back": "2\u20133 primary sources, 1 trusted aggregator, 1 good skeptic, and a dated claim log revisited quarterly."},
  {"front": "Why does the claim log matter?", "back": "It converts consumption into calibration \u2014 the frontier rewards the calibrated, not the first."}
 ],
 "quiz": [
  {"q": "A paper's abstract claims SOTA; the baselines are two years old. You:",
   "choices": ["Cite it as SOTA", "Flag unfair baselines \u2014 the claim is unsupported", "Ignore all papers", "Email the authors angrily"],
   "answer": 1,
   "explain": "Step 4 of the protocol: stale baselines invalidate leadership claims."},
  {"q": "'Quantum AI will be conscious by 2028' exhibits:",
   "choices": ["Careful forecasting", "Category error + timeline laundering", "Peer-reviewed consensus", "A testable claim"],
   "answer": 1,
   "explain": "Two hype patterns stacked \u2014 consciousness isn't operationalized, and 2028 is a wish."},
  {"q": "A frontier fact from 2023 about 'the best open model' should be:",
   "choices": ["Cited as-is", "Re-verified or qualified \u2014 past its half-life", "Deleted from memory", "Trusted more with age"],
   "answer": 1,
   "explain": "Leadership claims have week-scale half-lives; a 2023 claim is archaeology."},
  {"q": "The most valuable item in a frontier radar:",
   "choices": ["The fastest news feed", "The dated claim log, revisited", "The most followers", "The glossiest demos"],
   "answer": 1,
   "explain": "Calibration compounds; speed without calibration is just faster error."}
 ]
}
]
