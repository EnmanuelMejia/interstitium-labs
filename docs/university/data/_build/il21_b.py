"""IL-21 modules 8-14 (history of technology through synthesis)."""
MODULES_B = [
{
 "id": "m21-history-tech", "code": "IL-21", "title": "History of Technology",
 "weight": 1,
 "summary": "From the steam engine to the internet: how technologies diffuse, why incumbents miss transitions, and what the industrial revolutions teach builders.",
 "objectives": ["Name the industrial revolutions and their core technologies", "Explain technology diffusion and the S-curve", "Describe why incumbents fail at transitions", "Draw lessons for current platform shifts"],
 "notes": [
  {"title": "The industrial revolutions",
   "body": "**First** (~1760\u20131840): steam, mechanized textiles, iron \u2014 Britain's factories. **Second** (~1870\u20131914): electricity, steel, chemicals, the internal-combustion engine \u2014 mass production. **Third** (~1960s\u2013): electronics, computers, the internet \u2014 information as the factor of production. Some historians count a **fourth** (cyber-physical systems, AI) from the 2010s."},
  {"title": "Diffusion and the S-curve",
   "body": "Technologies diffuse along an **S-curve**: slow uptake, explosive growth, saturation. **Rogers'** adopter categories (innovators \u2192 laggards) and **Moore's** 'chasm' between early adopters and the early majority describe the same curve's social shape. Infrastructure (railways, grids, fiber) determines the slope \u2014 technology without distribution is a demo."},
  {"title": "Why incumbents miss it",
   "body": "**Christensen's** *Innovator's Dilemma* (1997): incumbents rationally serve their best customers with sustaining improvements \u2014 and are blindsided by **disruptive** technologies that start worse and cheaper, then climb the S-curve. Kodak invented the digital camera (1975) and still lost; the dilemma is structural, not a failure of intelligence."},
  {"title": "The internet's lesson",
   "body": "ARPANET (1969) \u2192 TCP/IP standardization (1983) \u2192 the Web (1990\u2013) \u2192 broadband \u2192 mobile: each layer enabled the next, and open protocols beat walled gardens at the infrastructure layer. The pattern for builders: bet on open layers, expect the application layer to surprise you, and remember that distribution \u2014 not just invention \u2014 decides winners."}
 ],
 "cards": [
  {"front": "The three (or four) industrial revolutions and their cores?", "back": "1st: steam/textiles/iron. 2nd: electricity/steel/chemicals/engines. 3rd: electronics/computers/internet. 4th (claimed): cyber-physical/AI."},
  {"front": "The S-curve of diffusion?", "back": "Slow start, explosive middle, saturation \u2014 adoption over time; infrastructure sets the slope."},
  {"front": "Christensen's Innovator's Dilemma (1997)?", "back": "Incumbents rationally optimize for best customers and are disrupted from below by cheaper, initially-worse tech."},
  {"front": "Kodak and the digital camera?", "back": "Kodak invented it (1975, Steve Sasson) yet lost \u2014 the dilemma is structural, not stupidity."},
  {"front": "The internet's architectural lesson?", "back": "Open protocols won the infrastructure layer; each layer enabled the next; distribution decides."}
 ],
 "quiz": [
  {"q": "The Second Industrial Revolution is associated with:",
   "choices": ["Steam and textiles", "Electricity, steel, chemicals", "The internet", "Bronze tools"],
   "answer": 1,
   "explain": "~1870\u20131914: electrification, Bessemer steel, chemical industry, internal combustion."},
  {"q": "Moore's 'chasm' lies between:",
   "choices": ["Inventors and investors", "Early adopters and the early majority", "Hardware and software", "Startups and incumbents"],
   "answer": 1,
   "explain": "Crossing from enthusiasts to the pragmatic majority is the go-to-market crux."},
  {"q": "A disruptive technology, in Christensen's sense, typically starts:",
   "choices": ["Better and more expensive", "Worse and cheaper, serving overlooked customers", "Identical to incumbents", "As a government project"],
   "answer": 1,
   "explain": "Disruption enters low-end or new markets, then moves up as performance improves."},
  {"q": "TCP/IP standardization (1983) mattered because:",
   "choices": ["It was the fastest protocol", "It created a common open layer enabling the internet's growth", "It replaced telephones", "It was proprietary"],
   "answer": 1,
   "explain": "An open, shared protocol layer let diverse networks interoperate \u2014 infrastructure for everything above."}
 ]
},
{
 "id": "m21-technical-writing", "code": "IL-21", "title": "Technical Writing",
 "weight": 1,
 "summary": "Clarity as a professional discipline: structure, precision, active voice, and documentation that people actually read.",
 "objectives": ["Structure a document for scanning, not just reading", "Write in active voice with concrete subjects", "Define terms before using them", "Produce documentation, RFCs, and status updates that get read"],
 "notes": [
  {"title": "Write for scanning",
   "body": "Readers scan: put the **conclusion first** (BLUF \u2014 bottom line up front), then evidence. Use descriptive headings, short paragraphs, and lists for parallel items. A design doc's first paragraph should let a busy reader decide whether to read the rest \u2014 if it can't, rewrite it."},
  {"title": "Precision over decoration",
   "body": "**Active voice** with concrete subjects: 'The deploy script restarts the service' beats 'The service is restarted.' Define every term before first use; never let 'it', 'this', or 'thing' carry load. Numbers beat adjectives: 'p99 latency rose from 40ms to 900ms' beats 'latency got much worse.' Delete throat-clearing ('It is important to note that...')."},
  {"title": "The core documents",
   "body": "**RFC/design doc**: problem, goals/non-goals, proposal, alternatives, risks, rollout. **Runbook**: symptoms \u2192 diagnosis \u2192 fix, tested by someone who didn't write it. **Status update**: what changed, what's blocked, what's next \u2014 three bullets, no novel. **Commit message**: what and why, not just what (the diff shows the what)."},
  {"title": "Editing is the work",
   "body": "First drafts are for the writer; editing is for the reader. Cut 20% on the second pass as a discipline. Read aloud to catch tangles. The standard: a competent stranger, interrupted twice, can still follow it. Strunk & White's *Elements of Style* (1918) remains the compact classic \u2014 'omit needless words.'"}
 ],
 "cards": [
  {"front": "BLUF?", "back": "Bottom Line Up Front \u2014 conclusion first, then evidence; write for scanners."},
  {"front": "Three rules of precise technical prose?", "back": "Active voice with concrete subjects; define terms before use; numbers over adjectives."},
  {"front": "Sections of an RFC/design doc?", "back": "Problem, goals/non-goals, proposal, alternatives considered, risks, rollout plan."},
  {"front": "What makes a good commit message?", "back": "What AND why \u2014 the diff already shows the what."},
  {"front": "Strunk & White's core maxim?", "back": "'Omit needless words.' (The Elements of Style, 1918.)"}
 ],
 "quiz": [
  {"q": "Which sentence is strongest?",
   "choices": ["The service is restarted by the script.", "The deploy script restarts the service.", "It is important to note the service gets restarted.", "Restarting of the service happens."],
   "answer": 1,
   "explain": "Concrete subject, active verb, no throat-clearing."},
  {"q": "BLUF means:",
   "choices": ["Bold, large, underlined formatting", "Bottom line up front", "Brief, lucid, useful feedback", "Build, launch, update, fix"],
   "answer": 1,
   "explain": "Lead with the conclusion so scanners can triage."},
  {"q": "A runbook is tested by:",
   "choices": ["Its author, carefully", "Someone who didn't write it, during calm", "The on-call during an incident", "Nobody \u2014 it's reference"],
   "answer": 1,
   "explain": "Only a fresh reader proves the runbook is self-sufficient; never first-test it in a real incident."},
  {"q": "'Latency got much worse' should become:",
   "choices": ["'Latency degraded significantly'", "'p99 latency rose from 40ms to 900ms'", "'Users are unhappy'", "'We must fix latency'"],
   "answer": 1,
   "explain": "Numbers beat adjectives \u2014 precise, checkable, actionable."}
 ]
},
{
 "id": "m21-rhetoric", "code": "IL-21", "title": "Rhetoric & Persuasion",
 "weight": 1,
 "summary": "Ethos, pathos, logos; the Toulmin model; framing and audience analysis \u2014 the honest craft of moving people with reasons.",
 "objectives": ["Use ethos/pathos/logos deliberately and honestly", "Structure an argument with the Toulmin model", "Analyze an audience before persuading it", "Distinguish persuasion from manipulation"],
 "notes": [
  {"title": "Ethos, pathos, logos (Aristotle)",
   "body": "Aristotle's *Rhetoric* (4th c. BCE) names three appeals: **ethos** (the speaker's credibility), **pathos** (the audience's emotions), **logos** (the argument's logic). Technical audiences over-invest in logos and starve the other two \u2014 but a correct argument from an untrusted speaker, framed without regard for stakes, still loses. All three are legitimate; the vice is substituting one for another."},
  {"title": "The Toulmin model",
   "body": "Stephen Toulmin (1958): arguments have **claims**, **grounds** (evidence), **warrants** (the inference license connecting grounds to claim), **backing** (support for the warrant), **qualifiers**, and **rebuttals**. In engineering reviews, fights are usually about *warrants* \u2014 'load tests predict production' \u2014 not about the data. Name the warrant and the debate gets productive."},
  {"title": "Audience analysis and framing",
   "body": "Persuasion starts with the audience's **values, knowledge, and decision criteria** \u2014 not your material. **Framing** selects which aspects of a situation are salient: the same migration is 'risk reduction' to ops and 'feature velocity' to product. Honest framing foregrounds relevant aspects; dishonest framing hides them."},
  {"title": "Persuasion vs manipulation",
   "body": "The line: persuasion respects the audience's rational agency \u2014 reasons they could endorse on reflection. Manipulation bypasses it \u2014 hidden agendas, manufactured urgency, selective data. The test you'd apply to others' decks, apply to your own: would this argument survive the audience knowing everything I know?"}
 ],
 "cards": [
  {"front": "Aristotle's three appeals?", "back": "Ethos (credibility), pathos (emotion), logos (logic) \u2014 Rhetoric, 4th c. BCE."},
  {"front": "Toulmin model components?", "back": "Claim, grounds, warrant, backing, qualifier, rebuttal (1958)."},
  {"front": "In engineering debates, what do people usually fight about?", "back": "Warrants \u2014 the inference licenses ('load tests predict prod'), not the raw data."},
  {"front": "Persuasion vs manipulation: the test?", "back": "Does it respect rational agency? Would the argument survive full disclosure?"},
  {"front": "What is framing?", "back": "Selecting which aspects of a situation are salient for an audience \u2014 honest when it foregrounds relevant aspects."}
 ],
 "quiz": [
  {"q": "Citing your team's incident-free record to support a proposal appeals to:",
   "choices": ["Logos", "Pathos", "Ethos", "Kairos"],
   "answer": 2,
   "explain": "Credibility of the speaker \u2014 ethos."},
  {"q": "In Toulmin's model, the warrant is:",
   "choices": ["The final claim", "The raw data", "The inference license from grounds to claim", "The rebuttal"],
   "answer": 2,
   "explain": "The warrant is *why* the grounds support the claim \u2014 usually the contested part."},
  {"q": "Presenting only the metrics that favor your proposal is:",
   "choices": ["Good framing", "Manipulation by selective data", "Logos", "Ethos"],
   "answer": 1,
   "explain": "Bypassing rational agency with selective evidence \u2014 manipulation, not persuasion."},
  {"q": "Before persuading, first analyze the audience's:",
   "choices": ["Org chart", "Values, knowledge, and decision criteria", "Calendar", "Budget"],
   "answer": 1,
   "explain": "Persuasion starts from where the audience is, not from your slides."}
 ]
},
{
 "id": "m21-economics-1", "code": "IL-21", "title": "Economics for Engineers I \u2014 Markets & Costs",
 "weight": 1,
 "summary": "Supply and demand, opportunity cost, marginal thinking, and cost structures \u2014 the economics inside every build-vs-buy and scale decision.",
 "objectives": ["Read a supply-demand diagram and predict price changes", "Apply opportunity cost and marginal analysis", "Distinguish fixed, variable, and sunk costs", "Evaluate build-vs-buy with total cost of ownership"],
 "notes": [
  {"title": "Supply, demand, equilibrium",
   "body": "**Demand** slopes down (higher price \u2192 less wanted); **supply** slopes up. **Equilibrium** is where they cross \u2014 the market-clearing price and quantity. A demand shift (tastes, income) moves price *and* quantity; a supply shift (input costs, technology) does the same in the opposite direction. Price **ceilings** below equilibrium create shortages; **floors** above it create surpluses."},
  {"title": "Opportunity cost and marginal thinking",
   "body": "**Opportunity cost**: the value of the best forgone alternative \u2014 the true cost of any choice. **Marginal analysis**: decide at the margin \u2014 is the *next* unit's benefit worth its *next* unit's cost? 'We've already spent $2M' is irrelevant to whether the next $100K is worth it (see: sunk costs)."},
  {"title": "Cost structures",
   "body": "**Fixed** costs don't vary with output (the data center lease); **variable** costs do (per-request compute). **Sunk** costs are spent and unrecoverable \u2014 rational decisions ignore them. **Economies of scale**: average cost falls as output rises (high fixed, low marginal cost \u2014 the software business in one phrase)."},
  {"title": "Build vs buy, honestly",
   "body": "**Total cost of ownership**: license + integration + operations + the opportunity cost of the engineers building it instead of the product. Buying looks expensive and building looks free because salaries are already budgeted \u2014 that is the opportunity-cost illusion. Decide on TCO over the realistic lifetime, including maintenance you will definitely pay."}
 ],
 "cards": [
  {"front": "What shifts demand vs supply?", "back": "Demand: tastes, income, substitutes. Supply: input costs, technology, number of sellers."},
  {"front": "Opportunity cost?", "back": "The value of the best alternative you give up \u2014 the true cost of a choice."},
  {"front": "Why do rational decisions ignore sunk costs?", "back": "They're unrecoverable; only future costs and benefits should decide."},
  {"front": "Economies of scale in one phrase?", "back": "Average cost falls as output rises \u2014 high fixed, low marginal cost."},
  {"front": "The build-vs-buy illusion?", "back": "Building looks free because salaries are sunk-budgeted; TCO must include opportunity cost + maintenance."}
 ],
 "quiz": [
  {"q": "A price ceiling set below equilibrium causes:",
   "choices": ["A surplus", "A shortage", "No effect", "Higher quality"],
   "answer": 1,
   "explain": "Quantity demanded exceeds quantity supplied at the capped price."},
  {"q": "$2M already spent on a failing project. The next phase costs $200K for $150K of value. Rational choice?",
   "choices": ["Continue \u2014 protect the $2M", "Stop \u2014 the $2M is sunk; marginal cost exceeds marginal benefit", "Continue \u2014 sunk cost proves commitment", "Ask for $2M more"],
   "answer": 1,
   "explain": "Sunk costs are irrelevant; at the margin, $200K > $150K, so stop."},
  {"q": "Software has high fixed and near-zero marginal cost, so it exhibits:",
   "choices": ["Diseconomies of scale", "Strong economies of scale", "Constant returns", "No cost structure"],
   "answer": 1,
   "explain": "Average cost collapses as users grow \u2014 the economics of the whole industry."},
  {"q": "A new GPU generation halves training cost. In supply-demand terms:",
   "choices": ["Demand shifts left", "Supply shifts right; price falls, quantity rises", "No change", "Equilibrium is abolished"],
   "answer": 1,
   "explain": "Lower input cost shifts supply right \u2014 the standard supply-shock result."}
 ]
},
{
 "id": "m21-economics-2", "code": "IL-21", "title": "Economics for Engineers II \u2014 Incentives & Games",
 "weight": 1,
 "summary": "Externalities, public goods, game theory basics, and mechanism design \u2014 why systems behave the way they do once humans are in the loop.",
 "objectives": ["Identify externalities and public-goods problems", "Find Nash equilibria in 2\u00d72 games", "Explain the prisoner's dilemma and its escapes", "Design incentives instead of wishing for cooperation"],
 "notes": [
  {"title": "Externalities and public goods",
   "body": "An **externality** is a cost or benefit imposed on third parties \u2014 pollution (negative), open-source software (positive). **Public goods** are non-excludable and non-rivalrous (clean air, basic research): everyone benefits, nobody wants to pay \u2014 the **free-rider problem**. Fixes: price the externality (taxes, cap-and-trade), assign property rights (Coase), or fund publicly."},
  {"title": "Game theory basics",
   "body": "A game: players, strategies, payoffs. A **Nash equilibrium** is a strategy profile where no player can *unilaterally* do better \u2014 stable, not necessarily good. Dominant strategies, best responses, and backward induction (in sequential games) are the working tools. Model the incentives before predicting the behavior."},
  {"title": "The prisoner's dilemma",
   "body": "Payoffs make mutual defection the Nash equilibrium even though mutual cooperation pays both more \u2014 the canonical model of arms races, price wars, and feature-copying. Escapes: **repetition** (tit-for-tat sustains cooperation), **contracts** with enforcement, **reputation** systems, and changing the payoffs themselves."},
  {"title": "Mechanism design: incentives as engineering",
   "body": "**Mechanism design** is reverse game theory: choose the rules so that self-interested play produces the outcome you want \u2014 auctions, congestion pricing, on-call rotations, bug bounties. The engineer's version: don't exhort people to cooperate; **design the payoff matrix** so cooperation is the equilibrium."}
 ],
 "cards": [
  {"front": "Externality? Public good? Free-rider problem?", "back": "Externality: third-party cost/benefit. Public good: non-excludable, non-rivalrous. Free-rider: benefit without paying."},
  {"front": "Nash equilibrium?", "back": "A profile where no player gains by unilaterally deviating \u2014 stable, not necessarily good."},
  {"front": "Prisoner's dilemma: equilibrium vs optimum?", "back": "Mutual defection is the Nash equilibrium; mutual cooperation pays more \u2014 the tragedy."},
  {"front": "Three escapes from the dilemma?", "back": "Repetition (tit-for-tat), enforceable contracts, reputation \u2014 or change the payoffs."},
  {"front": "Mechanism design in one line?", "back": "Choose the rules so self-interested play yields the outcome you want."}
 ],
 "quiz": [
  {"q": "A factory's smoke harms neighbors. This is a:",
   "choices": ["Public good", "Negative externality", "Nash equilibrium", "Sunk cost"],
   "answer": 1,
   "explain": "A cost imposed on third parties outside the transaction."},
  {"q": "In the prisoner's dilemma, the Nash equilibrium is:",
   "choices": ["Mutual cooperation", "Mutual defection", "Alternating", "No equilibrium exists"],
   "answer": 1,
   "explain": "Each player gains by defecting regardless of the other's move \u2014 defection dominates."},
  {"q": "Tit-for-tat sustains cooperation in repeated games because:",
   "choices": ["It is forgiving only", "Retaliation makes defection unprofitable over time", "It requires a referee", "It changes the payoffs"],
   "answer": 1,
   "explain": "The shadow of future retaliation shifts the equilibrium toward cooperation."},
  {"q": "Congestion pricing on a highway is an example of:",
   "choices": ["A price ceiling", "Mechanism design: pricing the externality", "A public good", "Sunk cost"],
   "answer": 1,
   "explain": "It charges drivers the congestion cost they impose \u2014 designing the payoff matrix."}
 ]
},
{
 "id": "m21-law-policy", "code": "IL-21", "title": "Law & Policy Literacy",
 "weight": 1,
 "summary": "Intellectual property, liability, privacy regulation, and how policy gets made \u2014 what every technologist should know without pretending to be a lawyer.",
 "objectives": ["Distinguish copyright, patent, trademark, and trade secret", "Describe how software liability generally works", "Name the major privacy regimes and their logic", "Explain how technical standards become policy"],
 "notes": [
  {"title": "Intellectual property, briefly",
   "body": "**Copyright**: protects expression (code, text), automatic on creation, long terms \u2014 open-source licenses (MIT, GPL) are copyright licenses granting permissions. **Patents**: protect inventions, require application and disclosure, ~20-year terms \u2014 software patentability varies by jurisdiction. **Trademarks**: protect brand identifiers. **Trade secrets**: protected by secrecy itself (Coca-Cola's formula). This is literacy, not legal advice \u2014 consult counsel for real decisions."},
  {"title": "Liability",
   "body": "Software has historically faced limited **liability** for defects \u2014 licenses disclaim warranties, and courts treat software as a service as much as a product. That settlement is under pressure: critical infrastructure, autonomous systems, and AI are pushing toward product-like liability. The direction matters for design: **document** safety reasoning as if a court will read it, because one might."},
  {"title": "Privacy regimes",
   "body": "The **GDPR** (EU, 2018): consent, data minimization, purpose limitation, the right to erasure, heavy fines \u2014 it reshaped global practice. **CCPA/CPRA** (California): opt-out of sale/sharing, deletion rights. Sectoral US laws cover health (HIPAA) and children (COPPA). The common logic: individuals get rights over their data; collectors get obligations. Design for data minimization from the start."},
  {"title": "How policy gets made",
   "body": "Policy moves through **legislation**, **regulation** (agencies writing rules under statutes), **standards** (IETF, W3C, NIST \u2014 often voluntary until referenced by law), and **litigation**. Technologists influence all four: writing standards, commenting on rulemakings, and \u2014 most powerfully \u2014 building the systems whose properties the law then assumes. Code is policy's raw material."}
 ],
 "cards": [
  {"front": "Copyright vs patent vs trademark vs trade secret?", "back": "Copyright: expression, automatic. Patent: inventions, applied for, ~20yr. Trademark: brand marks. Trade secret: protected by secrecy."},
  {"front": "GDPR's core principles?", "back": "Consent, data minimization, purpose limitation, erasure rights, accountability \u2014 EU, 2018."},
  {"front": "Why does software liability matter more now?", "back": "Critical infrastructure, autonomous systems, AI are pushing software toward product-like liability."},
  {"front": "Four channels of policymaking?", "back": "Legislation, agency regulation, technical standards, litigation."},
  {"front": "The engineer's policy move?", "back": "Design for data minimization; document safety reasoning; engage standards and rulemakings."}
 ],
 "quiz": [
  {"q": "An open-source license (e.g., MIT) is legally:",
   "choices": ["A patent grant", "A copyright license granting permissions", "A trademark", "Not legally meaningful"],
   "answer": 1,
   "explain": "Copyright vests automatically; the license is the author's permission slip with conditions."},
  {"q": "GDPR's data minimization principle requires:",
   "choices": ["Collecting everything, just in case", "Collecting only data needed for the stated purpose", "Deleting all data yearly", "Storing data only in the EU"],
   "answer": 1,
   "explain": "Purpose limitation + minimization: collect what the purpose needs, nothing more."},
  {"q": "Technical standards (IETF, NIST) become binding when:",
   "choices": ["Never", "Referenced by law, contract, or procurement", "Published", "They are old enough"],
   "answer": 1,
   "explain": "Standards are voluntary until legislation, regulation, or contracts incorporate them."},
  {"q": "This module's stance on legal questions is:",
   "choices": ["It constitutes legal advice", "Literacy only \u2014 consult counsel for real decisions", "Law doesn't apply to software", "Ignore compliance"],
   "answer": 1,
   "explain": "Stated throughout: this is orientation, not counsel."}
 ]
},
{
 "id": "m21-synthesis", "code": "IL-21", "title": "Synthesis \u2014 The Technologist as Citizen",
 "weight": 1,
 "summary": "Bringing it together: how philosophy, history, writing, rhetoric, economics, and law combine in the judgment of a senior technologist.",
 "objectives": ["Integrate the humanities lenses on a single case", "Write a reasoned position on a technology policy question", "Argue a technical decision to a non-technical audience", "Maintain a personal learning practice in the humanities"],
 "notes": [
  {"title": "One case, six lenses",
   "body": "Take deploying facial recognition for building access. **Ethics**: duties to subjects vs. aggregate safety. **Epistemology**: what do the accuracy claims actually establish, on what data? **History**: which past surveillance expansions are the precedent? **Economics**: who bears the costs, who captures the gains? **Law**: which regimes govern the biometric data? **Rhetoric**: how do you argue the decision to the people scanned? No single lens decides \u2014 judgment is the integration."},
  {"title": "The senior technologist's judgment",
   "body": "Senior judgment is not deeper technical knowledge \u2014 it is wider **context**: second-order effects, stakeholder legitimacy, reversibility, and the ability to say 'we should not build this' with reasons. The humanities are the training ground for exactly that: structured thinking about ends, not just means."},
  {"title": "Arguing to non-technical audiences",
   "body": "Translate without condescending: lead with **stakes** (what changes for them), then **options** with trade-offs, then your **recommendation** with reasons. Drop jargon or define it once. Expect values questions \u2014 'is this fair?' \u2014 and answer them as values questions, not as technical puzzles."},
  {"title": "A personal practice",
   "body": "The course ends; the practice doesn't. Read one serious book a quarter outside your field. Write \u2014 memos, essays, reading notes \u2014 because writing is thinking. Argue with people who disagree with you, charitably. The goal is not to become a philosopher but to become a technologist whose judgment deserves trust."}
 ],
 "cards": [
  {"front": "Apply three humanities lenses to any deployment decision.", "back": "Ethics (duties vs outcomes), epistemology (what do the claims establish?), economics (who bears costs?), law (which regimes?), history (what precedents?), rhetoric (how to argue it?)."},
  {"front": "What distinguishes senior judgment?", "back": "Wider context: second-order effects, legitimacy, reversibility \u2014 thinking about ends, not just means."},
  {"front": "Structure for arguing to non-technical audiences?", "back": "Stakes first, then options with trade-offs, then recommendation with reasons; define jargon once."},
  {"front": "A sustainable humanities practice?", "back": "One serious book a quarter outside your field; write regularly; argue charitably with disagreeing minds."}
 ],
 "quiz": [
  {"q": "Judgment, as developed in this course, is best described as:",
   "choices": ["Deeper technical knowledge", "The integration of multiple lenses on ends as well as means", "Faster decision-making", "Avoiding all risk"],
   "answer": 1,
   "explain": "Judgment = structured thinking about what is worth doing, using every lens."},
  {"q": "When asked 'is this system fair?', the skilled response:",
   "choices": ["Redirect to accuracy metrics", "Answer it as a values question with reasons", "Say fairness is subjective", "Cite the model's F1 score"],
   "answer": 1,
   "explain": "Values questions deserve values reasoning \u2014 metrics alone dodge the question."},
  {"q": "The through-line connecting all six humanities areas is:",
   "choices": ["Memorizing dates", "Structured reasoning about human ends and means", "Anti-technology sentiment", "Literary criticism"],
   "answer": 1,
   "explain": "Each area is a discipline of thinking about what matters and why \u2014 in service of better building."},
  {"q": "Which habit best sustains humanities learning post-course?",
   "choices": ["Re-reading these notes yearly", "Regular reading, writing, and charitable disagreement", "Avoiding philosophy", "Only reading technical docs"],
   "answer": 1,
   "explain": "Practice, not review: read widely, write to think, argue well."}
 ]
}
]
