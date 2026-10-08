# IL-21 retrofit content — modules 1-7 (of 14).
# Each entry: summary (instructor voice), notes (4 titled sections), extra_cards
# (thin modules only), quiz_explains (4, same order as existing quiz).

MODULES_A = {
"m21-what-is-philosophy": {
"summary": "Welcome to Module 1 of Humanities for Technologists. I'm your instructor, and over the next fourteen modules we're going to build the disciplines of judgment that turn a capable builder into a senior technologist — someone whose decisions deserve trust. We start at the root: this module maps the branches of philosophy and shows how each one already lives in your technical work — logic in code, ethics in deployment, epistemology in science, aesthetics in design.",
"notes": [
{"title": "Concepts", "body": """Your working vocabulary for the whole course — every term below returns in later modules.
- **logic** — the study of valid reasoning; lives in type systems and formal verification.
- **epistemology** — the theory of knowledge: what it is, where it comes from, its limits; lives in experiment design and the replication crisis.
- **metaphysics** — the study of what exists.
- **ethics** — the study of right action; lives in every deployment decision.
- **aesthetics** — the study of beauty and taste; lives in API and interface design.
- **political philosophy** — the study of justice and power.
- **applied branches** — philosophy of science, philosophy of mind, philosophy of language, and philosophy of technology apply the core branches to domains (philosophy of mind, for instance, to debates about machine intelligence).
- **argument** — premises plus an inference leading to a conclusion; a philosophical claim stands or falls on its argument.
- **principle of charity** — reconstruct the strongest version of a position before attacking it; the correct response to a supported claim is to engage its premises or its inference.
- **opinion vs. argument** — "that's just your opinion" is a category error when the claim is backed by reasons.
- **the technologist's failure mode** — optimization without direction: precise answers to the wrong questions. Technical training teaches how to build; the humanities teach what building is *for*. Philosophy supplies the questions."""},
{"title": "Hands-on procedure", "body": """Branch-map your own work — thirty minutes, pen and paper or a blank document.
1. **List three recent technical decisions** you made or watched (a schema choice, a deploy approval, an experiment design).
2. **Assign each a branch.** Which was really a logic question (validity of the reasoning)? An epistemology question (what the data establishes)? An ethics question (who it affects)? An aesthetics question (clarity of the interface)?
3. **Extract one argument.** Take the most contested decision and write it as premises → inference → conclusion.
4. **Apply charity.** Rewrite the opposing position in its strongest form before you critique it — no straw men allowed.
5. **Name the missing question.** For each decision, write the question philosophy would have asked that the technical discussion skipped. That list is your study agenda for this course."""},
{"title": "Project brief", "body": """**Deliverable: a one-page Branches Audit of a live project.** Pick a system you work on. For each of the six branches — logic, epistemology, metaphysics (what the system's data model claims exists), ethics, aesthetics, political philosophy (who holds power over the system) — write two sentences on where that branch's questions show up in the project. Close with one paragraph: which branch's questions is your team currently ignoring, and what is that neglect costing? This audit becomes your personal map for the rest of the course — revisit it in Module 14."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what does the principle of charity require before you criticize a design proposal?
- Give Noah three technical practices and name the branch behind each: (a) a type-system rule, (b) an A/B test design, (c) a deployment-approval gate.
- *Visual learners:* "Ask Noah to sketch (in text) the anatomy of an argument — premises, inference, conclusion — using one of your own recent decisions as the example."
- *Honesty:* ideas in this course are paraphrased and attributed to their traditions — no quotation is fabricated, and nothing here is legal, financial, or professional advice."""}
],
"extra_cards": [
{"front": "What is the failure mode of pure technique, and what does philosophy supply?", "back": "Optimization without direction — precise answers to the wrong questions. Philosophy supplies the questions."},
{"front": "Metaphysics, aesthetics, political philosophy: the central question of each?", "back": "Metaphysics: what exists? Aesthetics: what is beauty and taste? Political philosophy: what is justice, and who holds power?"}
],
"quiz_explains": [
"Epistemology is the theory of knowledge — its nature, sources, and limits. (See 'Concepts': epistemology.)",
"Charity means engaging the strongest form of the argument, not a weak caricature. (See 'Concepts': principle of charity.)",
"Questions about what minds are — and whether machines could have them — are philosophy of mind. (See 'Concepts': applied branches.)",
"The logical structure: premises support the conclusion via an inference. (See 'Concepts': argument.)"
]
},

"m21-logic-argument": {
"summary": "Welcome to Module 2. I'm your instructor, and this is the module that sharpens every other one: deductive validity, inductive strength, and the classic fallacies. By the end you'll be able to take any claim from a spec, a paper, or a meeting — extract its argument, test its form, and spot the fallacies hiding in technical discourse.",
"notes": [
{"title": "Concepts", "body": """The toolkit for evaluating claims — learn the names, then use them on your own arguments first.
- **deductive argument** — an argument whose conclusion is claimed to follow necessarily from its premises.
- **valid** — a deductive argument is valid if the conclusion *must* be true whenever the premises are; validity is about form, not content.
- **sound** — valid *and* with premises that are actually true.
- **modus ponens** — if P then Q; P; therefore Q.
- **modus tollens** — if P then Q; not Q; therefore not P.
- **induction** — generalization from instances ("every tested build passed, so the suite is green"); strong but never certain.
- **abduction** — inference to the best explanation ("the outage pattern matches a DNS failure"); the logic of debugging.
- **ad hominem** — attacking the person instead of the argument.
- **straw man** — refuting a distorted version of a position.
- **appeal to authority** — citing status instead of reasons ("no senior engineer would design it that way").
- **false dilemma** — presenting two options when more exist ("we either rewrite everything or accept the outage").
- **post hoc** — "after, therefore because of" ("the deploy caused the bug because it came first").
- **begging the question** — smuggling the conclusion into a premise.
- **slippery slope** — asserting an unargued chain of consequences.
- **the naming caveat** — naming a fallacy is the start of the reply, not the whole reply; you still owe the substantive counterargument. Confusing deduction, induction, and abduction is a constant source of overclaiming."""},
{"title": "Hands-on procedure", "body": """Dissect a live technical argument — do this on a real claim from your work this week.
1. **Capture a claim.** Take one contested claim from a recent spec, review, or meeting — verbatim.
2. **Extract the argument.** Write its premises and conclusion explicitly. If you can't find the premises, the claim is running on implication — flag that.
3. **Classify the inference.** Deduction, induction, or abduction? Apply the right standard: validity for deduction, strength of evidence for induction, best-explanation fit for abduction.
4. **Test validity.** If deductive, check the form — does the conclusion follow even if you disagree with the premises?
5. **Test soundness.** Are the premises actually true? One false premise sinks soundness even with perfect form.
6. **Scan for fallacies.** Run the classic list: ad hominem, straw man, authority, false dilemma, post hoc, question-begging, slippery slope.
7. **Charitable rewrite.** Reconstruct the strongest version of the argument, then write your reply to *that*."""},
{"title": "Project brief", "body": """**Deliverable: a one-week fallacy log.** For five working days, log every informal fallacy you spot in meetings, docs, and chat — the verbatim claim, the fallacy name, and a one-line charitable rewrite of what the speaker should have argued. Minimum ten entries. Close with a half-page reflection: which fallacy does your own team commit most, and what process change would catch it? (Naming the fallacy never substitutes for the substantive reply — the log must include your counterargument for each entry.)"""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what is the difference between a valid argument and a sound one?
- Give Noah three workplace claims and name the fallacy: (a) "no senior engineer would design it that way", (b) "we either rewrite everything or accept the outage", (c) "the deploy caused the bug because it came first".
- *Visual learners:* "Ask Noah to lay out a modus tollens for one of your debugging hypotheses: if the cache were stale we would see X; we do not see X; therefore…"
- *Honesty:* logic is a tool for evaluating arguments, not a weapon for winning meetings — apply the fallacy list to your own claims first."""}
],
"quiz_explains": [
"Correct form (syllogism) with true premises — valid and sound. (See 'Concepts': valid, sound.)",
"It asserts only two options without ruling out the rest — the false-dilemma pattern. (See 'Concepts': false dilemma.)",
"Best-explanation inference from evidence — abduction, the logic of debugging. (See 'Concepts': abduction.)",
"Status substitutes for reasons — the CTO's preference is not itself an argument. (See 'Concepts': appeal to authority.)"
]
},

"m21-ethics-1": {
"summary": "Welcome to Module 3. I'm your instructor, and this is where judgment gets its frameworks: virtue ethics, deontology, and consequentialism — three traditions that answer 'what should I do?' with three different decision procedures. You'll apply all three to the same technical dilemma, and discover that their disagreements are the point.",
"notes": [
{"title": "Concepts", "body": """Three traditions, three decision procedures — know what each asks before you need it under pressure.
- **virtue ethics** — asks not "what should I do?" but **"what kind of person should I be?"**; right action flows from cultivated virtues (honesty, courage, prudence, justice) developed by habit.
- **Aristotle** — *Nicomachean Ethics* (4th c. BCE); the good life as *eudaimonia*, flourishing through virtuous activity. Engineering analogue: the craftsperson's character — care, honesty about limits, refusal to cut corners.
- **deontology** — duty-based: some acts are required or forbidden regardless of consequences.
- **Kant** — the **categorical imperative** (*Groundwork*, 1785): (1) act only on maxims you could will as universal law; (2) treat humanity always as an end, never merely as a means. Engineering analogue: duties not to deceive users, not to ship known-harmful systems, respect for autonomy — even when breaking them would "work better".
- **consequentialism** — judge acts by their **outcomes**; the right act maximizes good consequences.
- **utilitarianism** — the classical form (Bentham, Mill, 18th–19th c.): maximize overall happiness/well-being. Engineering analogue: cost-benefit analysis, risk assessment, expected-value reasoning.
- **each tradition's vulnerability** — virtue: vague guidance in hard cases. Deontology: rigid; duties can conflict. Consequentialism: can justify sacrificing individuals for the aggregate, and demands consequence-predictions we rarely can make.
- **one case, three verdicts** — shipping an addictive-engagement feature: the virtue ethicist asks whether it expresses the character of a good craftsperson; the deontologist asks whether it treats users as mere means; the utilitarian weighs aggregate engagement-happiness against aggregate harm. The traditions can and do disagree — that disagreement is the point of studying all three."""},
{"title": "Hands-on procedure", "body": """Run the three-traditions analysis on a real decision you are facing or recently made.
1. **State the decision** in one sentence, naming the action you are actually considering.
2. **Virtue pass.** Ask: what would the good craftsperson do here? Which virtues (honesty, care, courage) are exercised or betrayed?
3. **Deontology pass.** Ask: could I will everyone in my position to do this? Does it treat any person merely as a means?
4. **Consequentialist pass.** Ask: what are the expected aggregate outcomes — including second-order effects and the worst plausible case?
5. **Compare verdicts.** Where the traditions agree, decide with confidence. Where they disagree, write down exactly what the disagreement is about — that sentence is the real decision.
6. **Document.** File the analysis with the decision; your future self (or your reviewer) deserves the reasoning, not just the outcome."""},
{"title": "Project brief", "body": """**Deliverable: a two-page ethics review memo.** Take a real product decision — past or pending — and run all three traditions on it, following the Hands-on procedure. The memo must contain: the decision stated plainly, each tradition's analysis in its own section, the point of disagreement, and your recommendation with reasons. If all three traditions agree, say so and say why the case was easy; if they split, own the split."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what question does each tradition ask? (Virtue: what kind of person should I be? Deontology: what is my duty? Consequentialism: which act has the best outcomes?)
- Give Noah the addictive-engagement feature and ask which tradition condemns it fastest — and on what grounds.
- *Visual learners:* "Ask Noah to lay out the three verdicts side by side for a deploy decision you are facing, then point to where they disagree."
- *Honesty:* these frameworks structure judgment; they do not automate it — a memo that cites a tradition without doing the analysis is ethics theater."""}
],
"extra_cards": [
{"front": "State the decision procedure of each tradition in one line.", "back": "Virtue: what would the good craftsperson do? Deontology: could I will this as universal law, and does it treat persons as ends? Utilitarianism: which act maximizes expected good outcomes?"},
{"front": "The three verdicts on an addictive-engagement feature — one line each?", "back": "Virtue: does it express a good craftsperson's character? Deontology: does it treat users as mere means? Utilitarian: do aggregate harms outweigh engagement-happiness?"}
],
"quiz_explains": [
"Universalizability is Kant's test — the first formulation of the categorical imperative. (See 'Concepts': Kant, categorical imperative.)",
"Consequentialism judges by outcomes — expected benefits weighed against expected harms. (See 'Concepts': consequentialism.)",
"Eudaimonia — often translated flourishing — is the telos of the virtuous life. (Arete is virtue/excellence itself.) (See 'Concepts': Aristotle.)",
"The humanity formulation: never treat rational agents merely as instruments. (See 'Concepts': categorical imperative.)"
]
},

"m21-ethics-2": {
"summary": "Welcome to Module 4. I'm your instructor. Last module gave you the three traditions; this one puts them to work where you live — applied ethics for builders. Dual use, the Collingridge dilemma, responsibility gaps, and professional codes: by the end you'll know who answers when systems cause harm, and what to do before they do.",
"notes": [
{"title": "Concepts", "body": """From theory to the systems you ship — the applied vocabulary.
- **Collingridge dilemma** — David Collingridge (1980): early in a technology's life we can shape it but cannot know its consequences; late, we know the consequences but the technology is entrenched and hard to change. Implication: design that is anticipatory, reversible, and humble rather than confidently predictive.
- **dual use** — technologies serving benign and harmful ends with the same mechanism: cryptography, drones, facial recognition, large language models, gene editing. Resists two lazy answers — "technology is neutral" (it isn't; affordances shape use) and "ban it all" (which forfeits the benefits). The serious question is always *which uses, under what controls*.
- **responsibility gap** — in sociotechnical systems, harm can emerge with no single responsible agent; designers, deployers, users, and institutions each hold a piece.
- **the engineer's four moves** — **document** foreseeable misuses, **build in** friction against the worst ones, **instrument** for monitoring, and **preserve** human override. "The model did it" is not an excuse a professional can offer.
- **professional codes** — the ACM Code of Ethics and Professional Conduct (updated 2018) and the IEEE Code of Ethics state duties: avoid harm, be honest, respect privacy, honor confidentiality. Codes do not decide hard cases — they set the floor and give you language to escalate with. Know your profession's code; cite it when you push back."""},
{"title": "Hands-on procedure", "body": """Dual-use audit of a system you touch — do this on something real.
1. **Name the core mechanism** of your system in one sentence — what it does, mechanically.
2. **List benign uses** — who benefits, and how.
3. **List harmful uses of the same mechanism** — be specific and concrete; vagueness here is the evasion.
4. **Apply the four moves.** For each harmful use: what would you document, what friction would you build in, what would you instrument, where does a human keep override?
5. **Write the misuse section** of your design doc or README — foreseeable misuses, controls, and residual risks, in plain language.
6. **Cite your code.** Note which clause of the ACM or IEEE code your analysis rests on, so the escalation has standing."""},
{"title": "Project brief", "body": """**Deliverable: a responsible-deployment plan.** For a system you own (or the resume-screening case from this course's scenarios), produce: (a) the dual-use analysis, (b) the four moves implemented as concrete controls, (c) the monitoring that would catch misuse, (d) the rollback and reversibility story per Collingridge. If the honest conclusion is "do not ship", the plan says so — with the traditions from Module 3 cited."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what is the Collingridge dilemma — and what design stance does it imply?
- Give Noah two technologies and ask for the dual-use read: (a) facial recognition, (b) an open-source vision library — which uses, under what controls?
- *Visual learners:* "Ask Noah to sketch the responsibility map — designer, deployer, user, institution — and mark where each of your four moves lands."
- *Honesty:* document your reasoning as if a court, a regulator, and your future self will all read it — because each of them might."""}
],
"quiz_explains": [
"Since early knowledge is poor and late change is hard, keep options open and design for reversibility. (See 'Concepts': Collingridge dilemma.)",
"Same mechanism serves security/authentication and mass surveillance — the question is which uses under what controls. (See 'Concepts': dual use.)",
"Professional responsibility covers foreseeable misuse of systems you design and deploy. (See 'Concepts': the engineer's four moves.)",
"Codes set minimums and give practitioners vocabulary to raise concerns — they don't automate judgment. (See 'Concepts': professional codes.)"
]
},

"m21-epistemology": {
"summary": "Welcome to Module 5. I'm your instructor, and this module is about the authority science claims and how it earns it: what counts as knowledge, Popper's falsifiability, Kuhn's paradigms — and why all of it matters the next time you design an experiment, read a paper, or trust a metric.",
"notes": [
{"title": "Concepts", "body": """How knowledge claims earn (or fail to earn) your trust.
- **knowledge (JTB)** — the classic account: S *knows* p iff p is true, S believes p, and S is *justified* in believing p.
- **Gettier problem** — Gettier's 1963 counterexamples showed justified-true-belief can be accidentally true; the practical residue: belief + truth isn't enough — the *route* to the belief matters.
- **falsifiability** — Karl Popper (*The Logic of Scientific Discovery*, 1934): science advances by **conjecture and refutation**; a theory is scientific insofar as it **forbids some possible observations**. "This model explains everything" is not praise — an unfalsifiable claim cannot be tested.
- **paradigm** — Thomas Kuhn (*The Structure of Scientific Revolutions*, 1962): science alternates between **normal science** (puzzle-solving inside a paradigm) and **revolutionary** episodes where anomalies accumulate and the paradigm is replaced — Copernican, Newtonian, Einsteinian, quantum. Paradigms shape what counts as a legitimate question, which is why revolutions feel like world-changes.
- **replication crisis** — across psychology, medicine, and ML-adjacent fields, landmark findings failed to replicate — driven by **p-hacking**, **publication bias**, and low power.
- **the remedies** — **pre-registration**, replication, and **meta-analysis**: how a field earns the title of knowledge. Treat every striking result as a conjecture awaiting refutation."""},
{"title": "Hands-on procedure", "body": """Falsify your own claim before anyone else does — run this on your current most impressive result.
1. **Write the striking claim** — a metric improvement, a model result, a performance assertion.
2. **List its falsifiers.** What observations would prove it wrong? If you can't name any, the claim is unfalsifiable — restate it until it forbids something.
3. **Audit the route.** Could p-hacking, cherry-picked splits, or selection of only the good runs have produced this result?
4. **Pre-register.** Write the hypothesis, the metric, the analysis, and the decision rule *before* you run the next test — then run it.
5. **Seek replication.** Have someone else reproduce it, or reproduce it on fresh data. One unreplicated result is a conjecture, not knowledge.
6. **Report uncertainty.** Effect size with uncertainty beats a bare "significant" — and say what would change your mind."""},
{"title": "Project brief", "body": """**Deliverable: a replication-ready experiment plan.** One page: the claim, its falsification criteria, the pre-registered analysis, the sample and data plan, and the replication step. Then run it — and file the result whether it confirms or refutes. A refuted conjecture, documented, is worth more than an untested "win"."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what makes a theory scientific for Popper?
- Give Noah two claims and ask which is falsifiable: (a) "this model explains all failures", (b) "disabling the cache raises p99 above 200ms".
- *Visual learners:* "Ask Noah to draw the Kuhn cycle — normal science → anomaly → crisis → revolution → new normal — and place your field's last big shift on it."
- *Honesty:* treat every striking result as conjecture awaiting refutation — including your own, especially your own."""}
],
"quiz_explains": [
"Falsifiability is the demarcation line: no forbidden observations, no science. (See 'Concepts': falsifiability.)",
"Gettier constructed JTB cases where the belief is true by luck — intuitively not knowledge. (See 'Concepts': Gettier problem.)",
"Paradigms structure normal science — its questions, methods, and standards of success. (See 'Concepts': paradigm.)",
"Locking in hypotheses and analyses before seeing data removes the garden of forking paths. (See 'Concepts': the remedies — pre-registration.)"
]
},

"m21-history-science-1": {
"summary": "Welcome to Module 6. I'm your instructor. We now turn to context — the story of how systematic knowledge of nature became possible, from Babylonian star records to Newton's synthesis. This is History of Science I: antiquity to Newton, and the instruments and mathematics in between.",
"notes": [
{"title": "Concepts", "body": """The figures and ideas that built the method — dates are load-bearing; learn them.
- **Babylonians** (by ~700 BCE) — systematic astronomical records and base-60 arithmetic still in our clocks.
- **Euclid's *Elements*** (~300 BCE) — the **axiomatic method**: definitions, postulates, proof — the template for rigorous mathematics ever since.
- **Archimedes** (3rd c. BCE) — buoyancy, levers, approximations of pi by inscribed polygons: theory married to machines.
- **Ptolemy's *Almagest*** (2nd c. CE) — planetary motion modeled with **epicycles**: wrong in structure, superb in prediction, dominant for 1400 years.
- **Islamic Golden Age** (8th–13th c.) — preservation and extension of Greek science: **Al-Khwarizmi** (algebra — his name gives us "algorithm"), **Ibn al-Haytham** (optics and an early experimental method).
- **Copernicus** (1543) — moved the sun to the center.
- **Kepler** (1609–1619) — elliptical orbits and three laws, derived from Tycho Brahe's data.
- **Galileo** — telescope (1609), inclined-plane experiments; made motion mathematical; paid for heliocentrism with house arrest (1633).
- **Newton's *Principia*** (1687) — three laws of motion plus universal gravitation: one mathematics for falling apples and orbiting moons; co-inventor (with Leibniz) of the calculus.
- **the Revolution's method** — mathematized hypotheses tested against precise, often instrument-mediated measurement; the Newtonian program of reducing phenomena to mathematical law defined science for two centuries and still structures engineering education."""},
{"title": "Hands-on procedure", "body": """Reconstruct one link in the chain — pick a figure who is not Newton.
1. **Pick a figure** from this module's earlier centuries.
2. **State the prevailing view** they inherited, in its strongest form — charity applies to the past too.
3. **Name the anomaly or instrument** that broke it — whose data, which device.
4. **State the new claim** precisely, and name the mathematics that carried it.
5. **Name what it preserved.** Revolutions contain their past: what of the old view survived inside the new one?
6. **Draw the engineering moral.** Which of your own tools and theories are Ptolemaic epicycles — predictively strong but structurally wrong?""" },
{"title": "Project brief", "body": """**Deliverable: a "Long View" memo.** Trace one modern tool you use daily (your ML library's optimizer, your database's index, your clock's timekeeping) back through three historical layers to this module's period. One page: the modern tool, the 19th/20th-century science behind it, and the pre-1800 root. The point is not trivia — it is seeing your stack as the tip of a 2,700-year project."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what did the Scientific Revolution change methodologically?
- Give Noah three names and ask for the contribution: Euclid, Al-Khwarizmi, Kepler.
- *Visual learners:* "Ask Noah to sketch the timeline 700 BCE → 1687 with one line per figure — and mark where instruments start driving theory."
- *Honesty:* history is told from evidence, not nostalgia — attribute, date, and qualify. Ptolemy was wrong about structure and magnificent at prediction, and both facts matter."""}
],
"quiz_explains": [
"Epicycles were structurally wrong but predicted planetary positions well — a lesson in prediction vs. truth. (See 'Concepts': Ptolemy's Almagest.)",
"The 9th-century scholar's name, Latinized, attached to his systematic procedures. (See 'Concepts': Al-Khwarizmi.)",
"The Inquisition's trial centered on his defense of the Copernican system. (See 'Concepts': Galileo.)",
"Brahe's unprecedentedly precise naked-eye data made the ellipses detectable. (See 'Concepts': Kepler.)"
]
},

"m21-history-science-2": {
"summary": "Welcome to Module 7. I'm your instructor. Last module ended with Newton; this one covers the two centuries that built the modern world — energy, evolution, electromagnetism, relativity, quantum theory, and computation. History of Science II: 1800 to the present.",
"notes": [
{"title": "Concepts", "body": """Two centuries of revolutions — and the pattern they share.
- **thermodynamics** — Carnot, Clausius, Kelvin: energy conservation and **entropy**; the science of engines became the science of everything.
- **Darwin** — *On the Origin of Species* (1859): **natural selection** explains adaptation without design.
- **Maxwell** (1860s) — four equations unifying electricity, magnetism, and light; predicting electromagnetic waves, confirmed by Hertz (1887).
- **Planck** (1900) — quantized energy to solve blackbody radiation.
- **Einstein** — 1905 (photoelectric effect, special relativity; the "miracle year" also covered Brownian motion and atoms) and 1915 (general relativity): rewrote space, time, and gravity.
- **the quantum founders** — Bohr, Heisenberg, Schrödinger, Dirac (1920s): quantum mechanics, probabilistic at its core, technologically the foundation of semiconductors and lasers.
- **Turing** (1936) — the **universal machine**: computation's theoretical foundation, before any general-purpose computer existed.
- **Shannon** (1948) — **information theory**: bits, channel capacity, the mathematics of communication.
- **theory into infrastructure** — ENIAC (1945), the transistor (1947), integrated circuits (1958), ARPANET (1969): theory became infrastructure within a generation.
- **the pattern** — unification (Maxwell, Einstein), then mathematization, then instruments, then engineering. Each revolution preserved the old theory as a **limiting case** — Newton survives inside Einstein at low speeds. Science grows by *containing* its past, not erasing it."""},
{"title": "Hands-on procedure", "body": """Map one revolution end to end — Maxwell, Darwin, quantum, or computation.
1. **Pick a revolution** from this module.
2. **Name the two domains unified** (or the single orthodoxy overthrown).
3. **State the mathematics** that carried the new theory.
4. **Name the instrument or engineering** that followed — and how fast (years from theory to device).
5. **State the limiting case.** What does the old theory still correctly describe, and where does it break?
6. **Find the live analogue.** Which current orthodoxy in your field shows the same pre-revolution symptoms — anomalies accumulating, patches multiplying?""" },
{"title": "Project brief", "body": """**Deliverable: a two-page revolution case study.** Choose one: Maxwell's unification, the quantum revolution, or the birth of computation. Cover: the problem the old theory couldn't solve, the new mathematics, the confirming experiment or instrument, the engineering it enabled, and the limiting-case relationship. Close with one paragraph on what the case teaches about evaluating bold technical claims today."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, how do scientific revolutions relate to the theories they replace?
- Give Noah two dates and ask what happened: 1859, 1936.
- *Visual learners:* "Ask Noah to map the chain theory → instrument → infrastructure for one case — say, quantum theory → transistor → integrated circuits — with the dates."
- *Honesty:* dates and attributions are load-bearing in history — 1905 is not 1915, and Shannon is not Turing; precision is respect."""}
],
"quiz_explains": [
"One framework for electric and magnetic fields, with light as an electromagnetic wave. (See 'Concepts': Maxwell.)",
"Hertz generated and detected radio waves — the waves Maxwell's theory required. (See 'Concepts': Maxwell, Hertz.)",
"The universal Turing machine defined computability before electronic computers existed. (See 'Concepts': Turing.)",
"Band theory and semiconductor physics are quantum-mechanical — 1920s theory, 1940s device. (See 'Concepts': the quantum founders; theory into infrastructure.)"
]
}
}
