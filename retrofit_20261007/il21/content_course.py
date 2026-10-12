# IL-21 retrofit — course-level content.
# New mock tasks mirror modules 10-14 quizzes (same pattern as mock-m21-01..36,
# which mirror modules 1-9 quizzes). IDs continue the sequence: mock-m21-37..56.

NEW_MOCK_TASKS = [
# --- Module 10: Rhetoric & Persuasion ---
{"id": "mock-m21-37", "type": "choice",
 "q": "Citing your team's incident-free record to support a proposal appeals to:",
 "choices": ["Logos", "Pathos", "Ethos", "Kairos"], "answer": 2,
 "explain": "Credibility of the speaker — ethos. (Module 10: Concepts.)"},
{"id": "mock-m21-38", "type": "choice",
 "q": "In Toulmin's model, the warrant is:",
 "choices": ["The final claim", "The raw data", "The inference license from grounds to claim", "The rebuttal"], "answer": 2,
 "explain": "The warrant is why the grounds support the claim — usually the contested part. (Module 10: Concepts.)"},
{"id": "mock-m21-39", "type": "choice",
 "q": "Presenting only the metrics that favor your proposal is:",
 "choices": ["Good framing", "Manipulation by selective data", "Logos", "Ethos"], "answer": 1,
 "explain": "Bypassing rational agency with selective evidence — manipulation, not persuasion. (Module 10: Concepts.)"},
{"id": "mock-m21-40", "type": "choice",
 "q": "Framing the same migration as 'risk reduction' to ops and 'feature velocity' to product is an example of:",
 "choices": ["Deception", "Framing", "A fallacy", "Abduction"], "answer": 1,
 "explain": "Framing selects which aspects are salient for an audience — honest when it foregrounds relevant aspects. (Module 10: Concepts.)"},
# --- Module 11: Economics I ---
{"id": "mock-m21-41", "type": "choice",
 "q": "A price ceiling set below equilibrium causes:",
 "choices": ["A surplus", "A shortage", "No effect", "Higher quality"], "answer": 1,
 "explain": "Quantity demanded exceeds quantity supplied at the capped price. (Module 11: Concepts.)"},
{"id": "mock-m21-42", "type": "choice",
 "q": "$2M already spent on a failing project. The next phase costs $200K for $150K of value. Rational choice?",
 "choices": ["Continue — protect the $2M", "Stop — the $2M is sunk; marginal cost exceeds marginal benefit", "Continue — sunk cost proves commitment", "Ask for $2M more"], "answer": 1,
 "explain": "Sunk costs are irrelevant; at the margin, $200K > $150K, so stop. (Module 11: Concepts.)"},
{"id": "mock-m21-43", "type": "choice",
 "q": "Software has high fixed and near-zero marginal cost, so it exhibits:",
 "choices": ["Diseconomies of scale", "Strong economies of scale", "Constant returns", "No cost structure"], "answer": 1,
 "explain": "Average cost collapses as users grow — the economics of the whole industry. (Module 11: Concepts.)"},
{"id": "mock-m21-44", "type": "choice",
 "q": "A new GPU generation halves training cost. In supply-demand terms:",
 "choices": ["Demand shifts left", "Supply shifts right; price falls, quantity rises", "No change", "Equilibrium is abolished"], "answer": 1,
 "explain": "Lower input cost shifts supply right — the standard supply-shock result. (Module 11: Concepts.)"},
# --- Module 12: Economics II ---
{"id": "mock-m21-45", "type": "choice",
 "q": "A factory's smoke harms neighbors. This is a:",
 "choices": ["Public good", "Negative externality", "Nash equilibrium", "Sunk cost"], "answer": 1,
 "explain": "A cost imposed on third parties outside the transaction. (Module 12: Concepts.)"},
{"id": "mock-m21-46", "type": "choice",
 "q": "In the prisoner's dilemma, the Nash equilibrium is:",
 "choices": ["Mutual cooperation", "Mutual defection", "Alternating", "No equilibrium exists"], "answer": 1,
 "explain": "Each player gains by defecting regardless of the other's move — defection dominates. (Module 12: Concepts.)"},
{"id": "mock-m21-47", "type": "choice",
 "q": "Tit-for-tat sustains cooperation in repeated games because:",
 "choices": ["It is forgiving only", "Retaliation makes defection unprofitable over time", "It requires a referee", "It changes the payoffs"], "answer": 1,
 "explain": "The shadow of future retaliation shifts the equilibrium toward cooperation. (Module 12: Concepts.)"},
{"id": "mock-m21-48", "type": "choice",
 "q": "Congestion pricing on a highway is an example of:",
 "choices": ["A price ceiling", "Mechanism design: pricing the externality", "A public good", "Sunk cost"], "answer": 1,
 "explain": "It charges drivers the congestion cost they impose — designing the payoff matrix. (Module 12: Concepts.)"},
# --- Module 13: Law & Policy ---
{"id": "mock-m21-49", "type": "choice",
 "q": "An open-source license (e.g., MIT) is legally:",
 "choices": ["A patent grant", "A copyright license granting permissions", "A trademark", "Not legally meaningful"], "answer": 1,
 "explain": "Copyright vests automatically; the license is the author's permission slip with conditions. (Module 13: Concepts.)"},
{"id": "mock-m21-50", "type": "choice",
 "q": "GDPR's data minimization principle requires:",
 "choices": ["Collecting everything, just in case", "Collecting only data needed for the stated purpose", "Deleting all data yearly", "Storing data only in the EU"], "answer": 1,
 "explain": "Purpose limitation + minimization: collect what the purpose needs, nothing more. (Module 13: Concepts.)"},
{"id": "mock-m21-51", "type": "choice",
 "q": "Technical standards (IETF, NIST) become binding when:",
 "choices": ["Never", "Referenced by law, contract, or procurement", "Published", "They are old enough"], "answer": 1,
 "explain": "Standards are voluntary until legislation, regulation, or contracts incorporate them. (Module 13: Concepts.)"},
{"id": "mock-m21-52", "type": "choice",
 "q": "This module's stance on legal questions is:",
 "choices": ["It constitutes legal advice", "Literacy only — consult counsel for real decisions", "Law doesn't apply to software", "Ignore compliance"], "answer": 1,
 "explain": "Stated throughout: this is orientation, not counsel. (Module 13: Concepts.)"},
# --- Module 14: Synthesis ---
{"id": "mock-m21-53", "type": "choice",
 "q": "Judgment, as developed in this course, is best described as:",
 "choices": ["Deeper technical knowledge", "The integration of multiple lenses on ends as well as means", "Faster decision-making", "Avoiding all risk"], "answer": 1,
 "explain": "Judgment = structured thinking about what is worth doing, using every lens. (Module 14: Concepts.)"},
{"id": "mock-m21-54", "type": "choice",
 "q": "When asked 'is this system fair?', the skilled response:",
 "choices": ["Redirect to accuracy metrics", "Answer it as a values question with reasons", "Say fairness is subjective", "Cite the model's F1 score"], "answer": 1,
 "explain": "Values questions deserve values reasoning — metrics alone dodge the question. (Module 14: Concepts.)"},
{"id": "mock-m21-55", "type": "choice",
 "q": "The through-line connecting all six humanities areas is:",
 "choices": ["Memorizing dates", "Structured reasoning about human ends and means", "Anti-technology sentiment", "Literary criticism"], "answer": 1,
 "explain": "Each area is a discipline of thinking about what matters and why — in service of better building. (Module 14: Concepts.)"},
{"id": "mock-m21-56", "type": "choice",
 "q": "Which habit best sustains humanities learning post-course?",
 "choices": ["Re-reading these notes yearly", "Regular reading, writing, and charitable disagreement", "Avoiding philosophy", "Only reading technical docs"], "answer": 1,
 "explain": "Practice, not review: read widely, write to think, argue well. (Module 14: Concepts.)"},
]

NEW_CHEAT_SHEETS = [
{"title": "History of Science & Technology Timeline",
 "blocks": [
  {"h": "To 1700",
   "body": "- ~700 BCE: Babylonian astronomy, base-60 arithmetic\n- ~300 BCE: Euclid's Elements — the axiomatic method\n- 3rd c. BCE: Archimedes — buoyancy, levers, pi by polygons\n- 2nd c. CE: Ptolemy's Almagest — epicycles (wrong, predictive)\n- 8th–13th c.: Al-Khwarizmi (algebra → 'algorithm'), Ibn al-Haytham (optics)\n- 1543: Copernicus — heliocentrism\n- 1609–1619: Kepler's laws from Brahe's data\n- 1609 / 1633: Galileo — telescope; house arrest\n- 1687: Newton's Principia — motion + universal gravitation"},
  {"h": "1800–present",
   "body": "- 1859: Darwin — natural selection\n- 1860s: Maxwell unifies electricity, magnetism, light; Hertz confirms (1887)\n- 1900: Planck quantizes energy\n- 1905 / 1915: Einstein — special, then general relativity\n- 1920s: quantum mechanics (Bohr, Heisenberg, Schrödinger, Dirac)\n- 1936: Turing — the universal machine\n- 1948: Shannon — information theory\n- 1945–1969: ENIAC, transistor, integrated circuits, ARPANET"},
  {"h": "Technology diffusion",
   "body": "- S-curve: slow uptake → explosive growth → saturation\n- Chasm (Moore): early adopters → early majority\n- Innovator's Dilemma (Christensen, 1997): disruption from below\n- Kodak (1975, Sasson) invented the digital camera and lost\n- Internet: ARPANET (1969) → TCP/IP (1983) → Web (1990–); open protocols won"}
 ]},
{"title": "Economics & Law Quick Reference",
 "blocks": [
  {"h": "Costs",
   "body": "- Opportunity cost: the best forgone alternative\n- Marginal analysis: decide on the next unit\n- Fixed vs variable vs sunk (sunk is ignored)\n- TCO: license + integration + ops + opportunity cost + maintenance\n- Price ceiling below equilibrium → shortage; floor above → surplus"},
  {"h": "Games & incentives",
   "body": "- Nash equilibrium: no unilateral deviation pays\n- Prisoner's dilemma: mutual defection stable, mutual cooperation better\n- Escapes: repetition (tit-for-tat), contracts, reputation, new payoffs\n- Mechanism design: set rules so self-interest yields the desired outcome\n- Externality: third-party cost/benefit; price it, assign rights (Coase), or fund it"},
  {"h": "IP & privacy",
   "body": "- Copyright: expression, automatic (MIT/GPL are copyright licenses)\n- Patent: inventions, ~20yr; Trademark: brand marks; Trade secret: secrecy\n- GDPR (EU, 2018): consent, minimization, purpose limitation, erasure\n- CCPA/CPRA: opt-out of sale/sharing, deletion; HIPAA: health; COPPA: children\n- Standards bind when referenced by law, contract, or procurement\n- Literacy, not legal advice"}
 ]}
]

# battlePlan patch: bp21-6 title/minutes update for the 56-task mock
BATTLEPLAN_PATCH = {
 "id": "bp21-6",
 "title": "Sit the 56-task timed mock; review misses against the cheat sheets",
 "minutes": 210
}
