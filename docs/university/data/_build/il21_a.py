"""IL-21 Humanities for Technologists — modules 1-7."""
MODULES_A = [
{
 "id": "m21-what-is-philosophy", "code": "IL-21", "title": "What Is Philosophy",
 "weight": 1,
 "summary": "The branches of philosophy and how each one shows up in technical work: logic in code, ethics in deployment, epistemology in science, aesthetics in design.",
 "objectives": ["Name the major branches of philosophy and their questions", "Connect each branch to a concrete technical practice", "Distinguish philosophy from science and from opinion", "Read a philosophical argument charitably before criticizing it"],
 "notes": [
  {"title": "The branches",
   "body": "Philosophy's traditional branches: **logic** (valid reasoning), **epistemology** (knowledge), **metaphysics** (what exists), **ethics** (right action), **aesthetics** (beauty and taste), **political philosophy** (justice and power). Philosophy of science, mind, language, and technology are applied branches. Each asks questions its methods can actually address \u2014 armchair speculation is not the discipline."},
  {"title": "Philosophy in technical work",
   "body": "Logic lives in type systems and formal verification. Epistemology lives in experiment design and the replication crisis. Ethics lives in every deployment decision. Philosophy of mind lives in debates about machine intelligence. Aesthetics lives in API and interface design. The branches are not electives for the curious \u2014 they are names for problems engineers already face."},
  {"title": "Argument, not opinion",
   "body": "A philosophical claim stands or falls on **argument**: premises, inference, conclusion. 'That's just your opinion' is a category error when the claim is supported by reasons \u2014 the correct response is to engage the premises or the inference. The principle of **charity**: reconstruct the strongest version of a position before attacking it."},
  {"title": "Why technologists study this",
   "body": "Technical training teaches how to build; the humanities teach what building is *for* and how to reason about it. The failure mode of pure technique is optimization without direction \u2014 precise answers to the wrong questions. Philosophy supplies the questions."}
 ],
 "cards": [
  {"front": "Name four traditional branches of philosophy and each one's central question.", "back": "Logic (valid reasoning), epistemology (what is knowledge?), metaphysics (what exists?), ethics (what is right action?)."},
  {"front": "What is the principle of charity?", "back": "Reconstruct the strongest version of an opposing position before criticizing it."},
  {"front": "How does a philosophical claim differ from a mere opinion?", "back": "It is backed by an argument \u2014 premises and inference that can be evaluated."},
  {"front": "Give one technical practice shaped by each: logic, epistemology, ethics.", "back": "Logic: type systems/verification. Epistemology: experiment design. Ethics: deployment decisions."}
 ],
 "quiz": [
  {"q": "Which branch asks 'What can we know?'",
   "choices": ["Ethics", "Epistemology", "Aesthetics", "Logic"],
   "answer": 1,
   "explain": "Epistemology is the theory of knowledge \u2014 its nature, sources, and limits."},
  {"q": "The principle of charity requires:",
   "choices": ["Agreeing with opponents", "Steel-manning a position before critique", "Avoiding controversial topics", "Citing authorities"],
   "answer": 1,
   "explain": "Charity means engaging the strongest form of the argument, not a weak caricature."},
  {"q": "Philosophy of mind is most relevant to which technical debate?",
   "choices": ["Database indexing", "Machine intelligence and consciousness", "Network protocols", "Compiler optimization"],
   "answer": 1,
   "explain": "Questions about what minds are \u2014 and whether machines could have them \u2014 are philosophy of mind."},
  {"q": "An argument consists of:",
   "choices": ["Claims plus rhetoric", "Premises, inference, conclusion", "Data plus charts", "Questions plus answers"],
   "answer": 1,
   "explain": "The logical structure: premises support the conclusion via an inference."}
 ]
},
{
 "id": "m21-logic-argument", "code": "IL-21", "title": "Logic & Argumentation",
 "weight": 1,
 "summary": "Deductive validity, inductive strength, and the classic fallacies \u2014 the toolkit for evaluating claims in specs, papers, and meetings.",
 "objectives": ["Test an argument for deductive validity", "Distinguish deduction from induction and abduction", "Identify the common informal fallacies", "Spot fallacies in technical discourse"],
 "notes": [
  {"title": "Validity and soundness",
   "body": "A **deductive** argument is **valid** if the conclusion *must* be true whenever the premises are \u2014 validity is about form, not content. It is **sound** if it is valid *and* its premises are actually true. Modus ponens (if P then Q; P; therefore Q) and modus tollens are the two workhorse valid forms."},
  {"title": "Induction and abduction",
   "body": "**Induction** generalizes from instances ('every tested build passed, so the suite is green') \u2014 strong but never certain. **Abduction** infers the best explanation ('the outage pattern matches a DNS failure'). Science and debugging run on induction and abduction; validity belongs to deduction. Confusing the three is a constant source of overclaiming."},
  {"title": "The classic fallacies",
   "body": "**Ad hominem**: attacking the person, not the argument. **Straw man**: refuting a distorted version. **Appeal to authority**: citing status instead of reasons. **False dilemma**: presenting two options when more exist. **Post hoc**: 'after, therefore because of.' **Begging the question**: smuggling the conclusion into a premise. **Slippery slope**: asserting an unargued chain of consequences."},
  {"title": "Fallacies in technical life",
   "body": "'No senior engineer would design it that way' is an appeal to authority. 'We either rewrite everything or accept the outage' is a false dilemma. 'The deploy caused the bug because it came first' is post hoc. Naming the fallacy is the start of the reply, not the whole reply \u2014 you still owe the substantive counterargument."}
 ],
 "cards": [
  {"front": "Valid vs sound argument?", "back": "Valid: conclusion must follow if premises true. Sound: valid + premises actually true."},
  {"front": "Modus ponens and modus tollens?", "back": "Ponens: P\u2192Q, P \u22a2 Q. Tollens: P\u2192Q, \u00acQ \u22a2 \u00acP."},
  {"front": "Deduction vs induction vs abduction?", "back": "Deduction: certain, form-based. Induction: generalization from instances. Abduction: best-explanation inference."},
  {"front": "Define: straw man, false dilemma, post hoc.", "back": "Straw man: attack a distortion. False dilemma: two options where more exist. Post hoc: after\u21d2because-of."},
  {"front": "Why is naming a fallacy not a complete rebuttal?", "back": "You still owe the substantive counterargument \u2014 the label diagnoses, it doesn't refute by itself."}
 ],
 "quiz": [
  {"q": "'All servers are machines; db-1 is a server; therefore db-1 is a machine' is:",
   "choices": ["Valid and sound", "Valid but unsound", "Invalid", "Inductive"],
   "answer": 0,
   "explain": "Correct form (syllogism) with true premises \u2014 valid and sound."},
  {"q": "'Either we migrate now or the system collapses' \u2014 with no evidence of collapse \u2014 is:",
   "choices": ["Ad hominem", "False dilemma", "Straw man", "Valid deduction"],
   "answer": 1,
   "explain": "It asserts only two options without ruling out the rest \u2014 the false-dilemma pattern."},
  {"q": "Inferring 'the cache is stale' as the best explanation of the symptoms is:",
   "choices": ["Deduction", "Induction", "Abduction", "Fallacy"],
   "answer": 2,
   "explain": "Best-explanation inference from evidence \u2014 abduction, the logic of debugging."},
  {"q": "'The CTO prefers Postgres, so Postgres is the right choice' is:",
   "choices": ["Sound reasoning", "Appeal to authority", "Modus ponens", "Induction"],
   "answer": 1,
   "explain": "Status substitutes for reasons \u2014 the CTO's preference is not itself an argument."}
 ]
},
{
 "id": "m21-ethics-1", "code": "IL-21", "title": "Ethics I \u2014 The Three Traditions",
 "weight": 1,
 "summary": "Virtue ethics, deontology, and consequentialism: three frameworks for 'what should I do?', each with a distinct decision procedure.",
 "objectives": ["State the core question of each tradition", "Apply each to a technical dilemma", "Compare how the three can disagree on one case", "Recognize which tradition you default to"],
 "notes": [
  {"title": "Virtue ethics (Aristotle)",
   "body": "Asks not 'what should I do?' but **'what kind of person should I be?'** Right action flows from cultivated **virtues** \u2014 honesty, courage, prudence, justice \u2014 developed by habit. Aristotle's *Nicomachean Ethics* (4th c. BCE) frames the good life as *eudaimonia*, flourishing through virtuous activity. In engineering: the craftsperson's character \u2014 care, honesty about limits, refusal to cut corners."},
  {"title": "Deontology (Kant)",
   "body": "**Duty**-based: some acts are required or forbidden regardless of consequences. Kant's **categorical imperative** (in the *Groundwork*, 1785): act only on maxims you could will as universal law, and treat humanity always as an end, never merely as a means. In engineering: duties not to deceive users, not to ship known-harmful systems, respect for autonomy \u2014 even when breaking them would 'work better.'"},
  {"title": "Consequentialism / utilitarianism",
   "body": "Judge acts by their **outcomes**: the right act maximizes good consequences. Classical **utilitarianism** (Bentham, Mill \u2014 18th\u201319th c.): maximize overall happiness/well-being. In engineering: cost-benefit analysis, risk assessment, expected-value reasoning. Its weakness: it can justify sacrificing individuals for the aggregate, and it demands consequence-predictions we rarely can make."},
  {"title": "One case, three verdicts",
   "body": "Shipping a addictive-engagement feature: the **virtue** ethicist asks whether it expresses the character of a good craftsperson; the **deontologist** asks whether it treats users as mere means; the **utilitarian** weighs aggregate engagement-happiness against aggregate harm. The traditions can and do disagree \u2014 that disagreement is the point of studying all three."}
 ],
 "cards": [
  {"front": "Virtue ethics: core question and key figure?", "back": "'What kind of person should I be?' \u2014 Aristotle; virtues cultivated by habit."},
  {"front": "Kant's categorical imperative (two formulations)?", "back": "Act only on universalizable maxims; treat humanity as an end, never merely as a means."},
  {"front": "Utilitarianism: core claim and key figures?", "back": "Right act maximizes overall well-being \u2014 Bentham, Mill."},
  {"front": "Each tradition's main vulnerability?", "back": "Virtue: vague guidance. Deontology: rigid, conflicting duties. Consequentialism: justifies sacrificing individuals; needs impossible predictions."}
 ],
 "quiz": [
  {"q": "'Would I endorse everyone doing this?' is the decision procedure of:",
   "choices": ["Virtue ethics", "Deontology", "Utilitarianism", "Egoism"],
   "answer": 1,
   "explain": "Universalizability is Kant's test \u2014 the first formulation of the categorical imperative."},
  {"q": "A utilitarian evaluates shipping a risky feature by:",
   "choices": ["Whether it expresses good character", "Whether it violates a duty", "Expected aggregate consequences", "What competitors do"],
   "answer": 2,
   "explain": "Consequentialism judges by outcomes \u2014 expected benefits weighed against expected harms."},
  {"q": "Aristotle's term for flourishing through virtuous activity?",
   "choices": ["Eudaimonia", "Ataraxia", "Nirvana", "Arete alone"],
   "answer": 0,
   "explain": "Eudaimonia \u2014 often translated flourishing \u2014 is the telos of the virtuous life. (Arete is virtue/excellence itself.)"},
  {"q": "Treating users 'merely as means' would be condemned by:",
   "choices": ["Utilitarianism", "Kant's second formulation", "Virtue ethics only", "No major tradition"],
   "answer": 1,
   "explain": "The humanity formulation: never treat rational agents merely as instruments."}
 ]
},
{
 "id": "m21-ethics-2", "code": "IL-21", "title": "Ethics II \u2014 Technology & Responsibility",
 "weight": 1,
 "summary": "Applied ethics for builders: dual use, the Collingridge dilemma, professional codes, and who answers when systems cause harm.",
 "objectives": ["Explain the Collingridge dilemma", "Analyze a dual-use technology case", "Locate responsibility in a sociotechnical system", "Use a professional code as a decision input, not an oracle"],
 "notes": [
  {"title": "The Collingridge dilemma",
   "body": "David Collingridge (1980): early in a technology's life we can shape it but cannot know its consequences; late, we know the consequences but the technology is entrenched and hard to change. This is the structural trap of technology governance \u2014 it argues for **anticipatory, reversible, humble** design rather than confident prediction."},
  {"title": "Dual use",
   "body": "**Dual-use** technologies serve benign and harmful ends with the same mechanism: cryptography, drones, facial recognition, large language models, gene editing. The dual-use framing resists two lazy answers \u2014 'technology is neutral' (it isn't; affordances shape use) and 'ban it all' (which forfeits the benefits). The serious question is always *which uses, under what controls*."},
  {"title": "Responsibility gaps",
   "body": "In sociotechnical systems, harm can emerge with no single responsible agent \u2014 the **responsibility gap**. Designers, deployers, users, and institutions each hold a piece. The engineer's move: **document** foreseeable misuses, **build in** friction against the worst ones, **instrument** for monitoring, and **preserve** human override. 'The model did it' is not an excuse a professional can offer."},
  {"title": "Professional codes",
   "body": "The ACM Code of Ethics and Professional Conduct (updated 2018) and the IEEE Code of Ethics state duties: avoid harm, be honest, respect privacy, honor confidentiality. Codes do not decide hard cases \u2014 they set the floor and give you language to escalate with. Know your profession's code; cite it when you push back."}
 ],
 "cards": [
  {"front": "The Collingridge dilemma?", "back": "Early: we can shape tech but can't foresee consequences. Late: we foresee but can't reshape \u2014 entrenchment."},
  {"front": "What is dual use?", "back": "One technology serving benign and harmful ends (crypto, drones, facial recognition, LLMs)."},
  {"front": "The responsibility gap?", "back": "Harm emerges from a sociotechnical system with no single responsible agent."},
  {"front": "The engineer's four moves against foreseeable misuse?", "back": "Document misuses, build in friction, instrument for monitoring, preserve human override."},
  {"front": "What are professional codes for (ACM 2018)?", "back": "A floor and a shared language for escalation \u2014 not an oracle for hard cases."}
 ],
 "quiz": [
  {"q": "The Collingridge dilemma implies designers should favor:",
   "choices": ["Confident long-range prediction", "Reversible, anticipatory, humble design", "Waiting until consequences are clear", "Maximum deployment speed"],
   "answer": 1,
   "explain": "Since early knowledge is poor and late change is hard, keep options open and design for reversibility."},
  {"q": "Facial recognition is best described as:",
   "choices": ["Neutral technology", "Dual-use technology", "Inherently unethical", "Solved science"],
   "answer": 1,
   "explain": "Same mechanism serves security/authentication and mass surveillance \u2014 the question is which uses under what controls."},
  {"q": "'The model did it' as a defense fails because:",
   "choices": ["Models never cause harm", "Professionals retain responsibility for foreseeable system behavior", "Only users are responsible", "Ethics doesn't apply to software"],
   "answer": 1,
   "explain": "Professional responsibility covers foreseeable misuse of systems you design and deploy."},
  {"q": "The ACM Code of Ethics (2018) is best used as:",
   "choices": ["A legal statute", "A decision oracle for hard cases", "A floor and shared language for escalation", "A marketing document"],
   "answer": 2,
   "explain": "Codes set minimums and give practitioners vocabulary to raise concerns \u2014 they don't automate judgment."}
 ]
},
{
 "id": "m21-epistemology", "code": "IL-21", "title": "Epistemology & Philosophy of Science",
 "weight": 1,
 "summary": "What counts as knowledge, how science earns its authority, and why falsifiability and paradigm shifts matter to anyone who runs experiments.",
 "objectives": ["State the classic JTB account of knowledge and its problem", "Explain falsifiability and why it matters", "Describe Kuhn's account of scientific revolutions", "Apply these ideas to experiment design and the replication crisis"],
 "notes": [
  {"title": "Knowledge: justified true belief?",
   "body": "The classic account: S **knows** p iff p is true, S believes p, and S is **justified** in believing p. Gettier's 1963 counterexamples showed justified-true-belief can be accidentally true \u2014 the 'Gettier problem' \u2014 and epistemology has debated the fix ever since. The practical residue: belief + truth isn't enough; the *route* to the belief matters."},
  {"title": "Popper: falsifiability",
   "body": "Karl Popper (*The Logic of Scientific Discovery*, 1934): science advances by **conjecture and refutation**. A theory is scientific insofar as it is **falsifiable** \u2014 it forbids some possible observations. 'This model explains everything' is not praise; an unfalsifiable claim cannot be tested. Design experiments that could prove you wrong."},
  {"title": "Kuhn: paradigms and revolutions",
   "body": "Thomas Kuhn (*The Structure of Scientific Revolutions*, 1962): science alternates between **normal science** (puzzle-solving inside a paradigm) and **revolutionary** episodes where anomalies accumulate and the paradigm itself is replaced \u2014 Copernican, Newtonian, Einsteinian, quantum. Paradigms shape what counts as a legitimate question, which is why revolutions feel like world-changes."},
  {"title": "The replication crisis",
   "body": "Across psychology, medicine, and ML-adjacent fields, landmark findings failed to replicate \u2014 driven by p-hacking, publication bias, and low power. The epistemic lesson: single studies rarely constitute knowledge; **pre-registration**, replication, and meta-analysis are how a field earns the title. Treat every striking result as a conjecture awaiting refutation."}
 ],
 "cards": [
  {"front": "JTB account of knowledge?", "back": "S knows p iff p is true, S believes p, S is justified \u2014 challenged by Gettier cases (1963)."},
  {"front": "Popper's demarcation criterion?", "back": "Falsifiability: a scientific theory must forbid some possible observations."},
  {"front": "Kuhn's normal vs revolutionary science?", "back": "Normal: puzzle-solving within a paradigm. Revolutionary: paradigm replacement after anomaly accumulation."},
  {"front": "Name two drivers of the replication crisis and two remedies.", "back": "Drivers: p-hacking, publication bias, low power. Remedies: pre-registration, replication, meta-analysis."},
  {"front": "Why is 'explains everything' not praise for a theory?", "back": "An unfalsifiable theory forbids nothing, so no observation can test it \u2014 Popper's point."}
 ],
 "quiz": [
  {"q": "A theory compatible with every possible observation is, for Popper:",
   "choices": ["The best kind of theory", "Unscientific (unfalsifiable)", "Probabilistically true", "A paradigm"],
   "answer": 1,
   "explain": "Falsifiability is the demarcation line: no forbidden observations, no science."},
  {"q": "Gettier cases show that:",
   "choices": ["Justification is unnecessary", "Justified true belief can be accidentally true", "Truth doesn't matter", "Belief is impossible"],
   "answer": 1,
   "explain": "Gettier constructed JTB cases where the belief is true by luck \u2014 intuitively not knowledge."},
  {"q": "In Kuhn's account, a paradigm determines:",
   "choices": ["Only the instruments used", "What counts as a legitimate problem and solution", "Researchers' salaries", "Nothing important"],
   "answer": 1,
   "explain": "Paradigms structure normal science \u2014 its questions, methods, and standards of success."},
  {"q": "Pre-registration primarily combats:",
   "choices": ["Small samples", "p-hacking / researcher degrees of freedom", "Expensive equipment", "Peer review"],
   "answer": 1,
   "explain": "Locking in hypotheses and analyses before seeing data removes the garden of forking paths."}
 ]
},
{
 "id": "m21-history-science-1", "code": "IL-21", "title": "History of Science I \u2014 Antiquity to Newton",
 "weight": 1,
 "summary": "From Babylonian astronomy and Greek geometry through the Scientific Revolution: how systematic knowledge of nature became possible.",
 "objectives": ["Name key figures and their contributions through 1700", "Explain what made the Scientific Revolution revolutionary", "Describe the mathematization of nature", "Connect early instruments to early theories"],
 "notes": [
  {"title": "Ancient foundations",
   "body": "**Babylonians** (by ~700 BCE): systematic astronomical records and base-60 arithmetic still in our clocks. **Euclid's** *Elements* (~300 BCE): the axiomatic method \u2014 definitions, postulates, proof \u2014 the template for rigorous mathematics ever since. **Archimedes** (3rd c. BCE): buoyancy, levers, and approximations of pi by inscribed polygons \u2014 theory married to machines."},
  {"title": "The long middle",
   "body": "**Ptolemy's** *Almagest* (2nd c. CE) modeled planetary motion with epicycles \u2014 wrong in structure, superb in prediction, dominant for 1400 years. Islamic Golden Age scholars (8th\u201313th c.) preserved and extended Greek science: **Al-Khwarizmi** (algebra \u2014 his name gives us 'algorithm'), **Ibn al-Haytham** (optics and an early experimental method)."},
  {"title": "The Scientific Revolution",
   "body": "**Copernicus** (1543) moved the sun to the center; **Kepler** (1609\u20131619) found elliptical orbits and his three laws from Tycho Brahe's data; **Galileo** (telescope, 1609; inclined-plane experiments) made motion mathematical and paid for heliocentrism with house arrest (1633). The revolution's method: mathematized hypotheses tested against precise measurement."},
  {"title": "Newton's synthesis",
   "body": "**Newton's** *Principia* (1687): three laws of motion plus universal gravitation \u2014 one mathematics for falling apples and orbiting moons. Co-inventor (with Leibniz) of the calculus. The Newtonian program \u2014 reduce phenomena to mathematical law \u2014 defined science for two centuries and still structures engineering education."}
 ],
 "cards": [
  {"front": "Euclid's Elements: contribution?", "back": "The axiomatic method \u2014 definitions, postulates, theorems proved from them (~300 BCE)."},
  {"front": "Al-Khwarizmi and Ibn al-Haytham: known for?", "back": "Al-Khwarizmi: algebra ('algorithm'). Ibn al-Haytham: optics and early experimental method."},
  {"front": "Kepler's three laws (in brief)?", "back": "Elliptical orbits (sun at focus); equal areas in equal times; T\u00b2 \u221d a\u00b3."},
  {"front": "Newton's Principia (1687): the synthesis?", "back": "Laws of motion + universal gravitation: one mathematics for terrestrial and celestial motion."},
  {"front": "What made the Scientific Revolution methodologically new?", "back": "Mathematized hypotheses tested against precise, often instrument-mediated measurement."}
 ],
 "quiz": [
  {"q": "Ptolemy's Almagest is best described as:",
   "choices": ["A heliocentric theory", "A geocentric model, predictively strong for 1400 years", "A work of pure mythology", "The first telescope manual"],
   "answer": 1,
   "explain": "Epicycles were structurally wrong but predicted planetary positions well \u2014 a lesson in prediction vs. truth."},
  {"q": "The word 'algorithm' derives from:",
   "choices": ["A Greek goddess", "Al-Khwarizmi", "A Latin verb", "Alan Turing"],
   "answer": 1,
   "explain": "The 9th-century scholar's name, Latinized, attached to his systematic procedures."},
  {"q": "Galileo's 1633 condemnation concerned:",
   "choices": ["His telescope design", "Advocacy of heliocentrism", "His inclined-plane data", "A personal feud only"],
   "answer": 1,
   "explain": "The Inquisition's trial centered on his defense of the Copernican system."},
  {"q": "Kepler derived his laws primarily from:",
   "choices": ["Pure thought", "Tycho Brahe's observational data", "Galileo's telescopes", "Newton's equations"],
   "answer": 1,
   "explain": "Brahe's unprecedentedly precise naked-eye data made the ellipses detectable."}
 ]
},
{
 "id": "m21-history-science-2", "code": "IL-21", "title": "History of Science II \u2014 1800 to the Present",
 "weight": 1,
 "summary": "Energy, evolution, electromagnetism, relativity, quantum theory, and computation: the two centuries that built the modern world.",
 "objectives": ["Trace the major 19th\u201320th century revolutions", "Explain the significance of Maxwell, Darwin, Einstein, and the quantum founders", "Describe the birth of computing", "Connect scientific revolutions to engineering practice"],
 "notes": [
  {"title": "The 19th century: energy and evolution",
   "body": "**Thermodynamics** (Carnot, Clausius, Kelvin): energy conservation and entropy \u2014 the science of engines became the science of everything. **Darwin** (*Origin of Species*, 1859): natural selection explains adaptation without design. **Maxwell** (1860s): four equations unifying electricity, magnetism, and light \u2014 predicting electromagnetic waves, confirmed by Hertz (1887)."},
  {"title": "1900\u20131930: relativity and quantum",
   "body": "**Planck** (1900) quantized energy to solve blackbody radiation; **Einstein** (1905: photoelectric effect, special relativity; 1915: general relativity) rewrote space, time, and gravity. **Bohr, Heisenberg, Schr\u00f6dinger, Dirac** (1920s) built quantum mechanics \u2014 probabilistic at its core, technologically the foundation of semiconductors and lasers."},
  {"title": "The information age",
   "body": "**Turing** (1936): the universal machine \u2014 computation's theoretical foundation, before any general-purpose computer existed. **Shannon** (1948): information theory \u2014 bits, channel capacity, the mathematics of communication. ENIAC (1945), the transistor (1947), integrated circuits (1958), ARPANET (1969): theory became infrastructure within a generation."},
  {"title": "Structure of the story",
   "body": "Notice the pattern: unification (Maxwell, Einstein), then mathematization, then instruments, then engineering. Each revolution preserved the old theory as a limiting case \u2014 Newton survives inside Einstein at low speeds. Science grows by *containing* its past, not erasing it."}
 ],
 "cards": [
  {"front": "Maxwell's achievement (1860s)?", "back": "Unifying electricity, magnetism, and light in four equations; predicting EM waves."},
  {"front": "Darwin 1859: the mechanism?", "back": "Natural selection \u2014 differential survival and reproduction of heritable variants."},
  {"front": "Einstein's 1905 'miracle year' outputs?", "back": "Photoelectric effect (light quanta), special relativity, Brownian motion (atoms)."},
  {"front": "Turing 1936 and Shannon 1948: contributions?", "back": "Turing: the universal machine (computation theory). Shannon: information theory (bits, channel capacity)."},
  {"front": "How do revolutions relate to old theories?", "back": "The old theory survives as a limiting case \u2014 e.g., Newton inside Einstein at low speeds."}
 ],
 "quiz": [
  {"q": "Maxwell's equations unified:",
   "choices": ["Gravity and electromagnetism", "Electricity, magnetism, and light", "Heat and motion", "Chemistry and physics"],
   "answer": 1,
   "explain": "One framework for electric and magnetic fields, with light as an electromagnetic wave."},
  {"q": "Hertz's 1887 experiments confirmed:",
   "choices": ["Relativity", "Maxwell's predicted electromagnetic waves", "The photoelectric effect", "Nuclear fission"],
   "answer": 1,
   "explain": "Hertz generated and detected radio waves \u2014 the waves Maxwell's theory required."},
  {"q": "Turing's 1936 paper established:",
   "choices": ["The first stored-program computer", "The theoretical model of universal computation", "Information theory", "The transistor"],
   "answer": 1,
   "explain": "The universal Turing machine defined computability before electronic computers existed."},
  {"q": "The transistor (1947) rested on which science?",
   "choices": ["Thermodynamics", "Quantum mechanics of semiconductors", "Relativity", "Classical optics"],
   "answer": 1,
   "explain": "Band theory and semiconductor physics are quantum-mechanical \u2014 1920s theory, 1940s device."}
 ]
}
]
