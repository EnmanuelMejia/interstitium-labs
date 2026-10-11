#!/usr/bin/env python3
"""Fill il-23 thin drills: expand Rapid-recall (1-2 items -> 5) and Concept-check (1 -> 5)."""
import json, os

P = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-23-frontier-knowledge.json')
d = json.load(open(P))

RR_EXPLAIN = "Core vocabulary from this module's Concepts note \u2014 say it cold before moving on."
CC_EXPLAIN = "Full marks require the key terms from the Concepts note, not just the gist."

def rr(term, definition):
    return {"prompt": f"In your own words, define \u201c{term}\u201d.",
            "answer": definition, "explain": RR_EXPLAIN}

def cc(objective):
    return {"prompt": f"Explain this objective as if teaching it: {objective}",
            "answer": objective, "explain": CC_EXPLAIN}

NEW = {
 "m23-transformers": {0: [
    rr("Why attention is quadratic",
       "Computing QK\u1d5b is an n\u00d7n score matrix for sequence length n \u2014 O(n\u00b2) time and memory. That quadratic cost is the fundamental scaling limit of vanilla attention, and the motivation for FlashAttention, sparse patterns, and linear-attention variants."),
    rr("A transformer block's components",
       "A multi-head self-attention sublayer followed by a position-wise feed-forward network, each wrapped in a residual connection with layer normalization (pre-norm in modern variants). The block is repeated dozens of times \u2014 depth is where the capacity lives."),
    rr("RoPE (Rotary Position Embedding)",
       "Position is encoded by rotating the query and key vectors by an angle proportional to token position. The rotation makes attention depend on relative distance, and it extrapolates to longer sequences better than learned absolute embeddings \u2014 the standard choice in LLaMA-family models."),
    rr("KV cache",
       "During autoregressive generation, the key and value tensors of all previous tokens are cached so each new token attends over cache + itself instead of recomputing everything. The cache is the memory-bandwidth cost that bounds long-context inference."),
 ]},
 "m23-quantum": {0: [
    rr("NISQ",
       "Noisy Intermediate-Scale Quantum: the current era \u2014 tens to hundreds of physical qubits, no fault tolerance, noise caps usable circuit depth. NISQ-era algorithms (VQE, QAOA) are variational hybrids that keep circuits shallow and lean on a classical optimizer."),
    rr("Decoherence",
       "The loss of quantum information to the environment: the carefully prepared superposition or entangled state degrades into a classical mixture before the computation finishes. Coherence time is the hard budget every quantum computation spends."),
    rr("Quantum error correction",
       "Encoding one logical qubit across many physical qubits (e.g., the surface code) so errors are detected and corrected faster than they accumulate. Crossing from physical to logical qubits is the mountain between NISQ and fault-tolerant quantum computing."),
    rr("Quantum advantage vs. quantum supremacy",
       "Supremacy = a quantum device solving a (possibly contrived) problem no classical supercomputer can in reasonable time \u2014 the 2019 Sycamore claim. Advantage = a useful real-world speedup. Supremacy is a milestone; advantage is the goal."),
 ]},
 "m23-crispr": {0: [
    rr("Base editing vs. prime editing",
       "Base editors fuse a deaminase to a nickase Cas9 and convert one base to another (C\u2192T, A\u2192G) with no double-strand break. Prime editing fuses a nickase to a reverse transcriptase and writes longer precise edits from a pegRNA template \u2014 precision without breaks in both cases."),
    rr("The PAM site",
       "The protospacer-adjacent motif: a short DNA sequence that must sit next to the target for Cas9 to bind and cut. No PAM, no cut \u2014 it is the enzyme's landing check and a key specificity determinant."),
    rr("Off-target effects",
       "Cas9 cutting at unintended genomic sites with partial guide-RNA complementarity \u2014 the central technical safety concern of therapeutic editing. Mitigations: high-fidelity Cas9 variants, careful guide design, and short-lived RNP delivery."),
    rr("Somatic vs. germline editing",
       "Somatic edits affect only the treated patient and are not inherited. Germline edits are heritable \u2014 the bright line. Clinical germline editing has been globally condemned since the 2018 He Jiankui case."),
 ]},
 "m23-fusion": {0: [
    rr("Magnetic confinement (tokamak)",
       "Plasma is held by combined toroidal and poloidal magnetic fields inside a doughnut-shaped vessel, keeping 100M+\u00b0C plasma off the walls. The tokamak is the most developed confinement line \u2014 ITER is its flagship, under construction in France."),
    rr("Q (fusion gain)",
       "Fusion energy out divided by heating energy in. Q > 1 is scientific breakeven \u2014 NIF achieved it in 2022 for a single implosion. Engineering breakeven (wall-plug energy in vs. electricity out) is a far higher bar."),
    rr("The Lawson criterion",
       "The threshold on the triple product \u2014 plasma density \u00d7 temperature \u00d7 energy-confinement time \u2014 required for net fusion gain. Every confinement approach chases the same figure of merit."),
    rr("Stellarator",
       "Magnetic confinement where twisted 3D coils shape the field without driving a plasma current \u2014 steadier plasma than a tokamak at higher engineering complexity. Wendelstein 7-X is the leading machine."),
 ]},
 "m23-agents": {0: [
    rr("Prompt injection",
       "Attacker text embedded in tool outputs, webpages, or data files that the model treats as instructions. The data/instruction boundary collapses \u2014 indirect injection through untrusted content is the signature threat of the agentic era."),
    rr("The agent loop",
       "Perceive (observations from the environment) \u2192 plan \u2192 act (tool calls) \u2192 observe the results, and repeat. The loop grounds the model's reasoning in real environment feedback instead of pure text prediction."),
    rr("The ReAct pattern",
       "Reasoning + Acting: the canonical agent loop interleaving Thought, Action, and Observation steps. Each thought names the next action; each observation updates the plan \u2014 the scaffold most tool-using agents are built on."),
 ]},
 "m23-semiconductors": {0: [
    rr("Dennard scaling",
       "The observation that as transistors shrank, power density stayed roughly constant \u2014 it broke around 2005\u20132006 as leakage current refused to shrink. The 'power wall' ended free frequency gains and forced the industry multicore."),
    rr("EUV lithography",
       "Extreme-ultraviolet (13.5 nm) lithography \u2014 the only way to pattern leading-edge nodes, built by a single supplier (ASML). High-NA EUV is the next step. The tool is a geopolitical chokepoint as much as a technical one."),
    rr("The memory wall",
       "Processor speed long ago outran memory bandwidth, so AI training is gated by HBM bandwidth as much as by FLOPS. 3D-stacked high-bandwidth memory with through-silicon vias \u2014 and the advanced packaging around it \u2014 is the current answer."),
 ]},
 "m23-synbio": {0: [
    rr("DNA synthesis screening",
       "Synthesis providers screen ordered sequences against lists of sequences of concern \u2014 the biosecurity governance layer on synbio's 'writing' half. Writing DNA is dual-use by construction, so screening is where the field meets its Collingridge problem."),
    rr("CAR-T therapy",
       "A patient's own T cells are engineered ex vivo with a chimeric antigen receptor so they hunt cancer cells \u2014 the synbio-adjacent clinical milestone (first FDA approval 2017). Living cells as programmed therapeutics."),
    rr("The central dogma's engineering inversion",
       "Reading genomes (sequencing) got cheap first; writing them (synthesis) still lags. Biology is crossing from a read-only science to a read-write engineering discipline \u2014 the DBTL loop is the write path."),
    rr("The mRNA-vaccine lesson",
       "The mRNA platform proved programmable medicine: the same manufacturing line, a new sequence. The COVID vaccines were the first mass deployment \u2014 the platform argument that what works for vaccines works for therapeutics generally."),
 ]},
 "m23-bci": {1: [
    cc("Describe what neural decoding can and cannot do today"),
    cc("Name the clinical applications in trials"),
    cc("Raise the core neuroethical questions"),
    cc("Explain the BCI signal ladder: EEG \u2192 ECoG \u2192 Utah array \u2192 Stentrode"),
 ]},
 "m23-space": {1: [
    cc("Describe megaconstellations as infrastructure"),
    cc("Outline the cislunar/Artemis program"),
    cc("Name the orbital-debris problem honestly"),
    cc("Explain why propellant is the real currency of spaceflight"),
 ]},
}

changed = []
for m in d['modules']:
    if m['id'] in NEW:
        for di, items in NEW[m['id']].items():
            before = len(m['drills'][di]['items'])
            m['drills'][di]['items'].extend(items)
            after = len(m['drills'][di]['items'])
            changed.append((m['id'], di, before, after))

with open(P, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')

# validate
d2 = json.load(open(P))
print('validated OK; modules:', len(d2['modules']))
for mid, di, b, a in changed:
    print(f'{mid} drill {di}: {b} -> {a} items')
