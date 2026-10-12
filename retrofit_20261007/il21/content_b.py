# IL-21 retrofit content — modules 8-14 (of 14).
# Modules 11 and 12 use 'Worked estimation' in place of 'Hands-on procedure'
# (numbers are illustrative, labeled as such in the text).

MODULES_B = {
"m21-history-tech": {
"summary": "Welcome to Module 8. I'm your instructor. Science tells you what is true; this module tells you what *happens* — how technologies diffuse, why smart incumbents miss transitions, and what the industrial revolutions teach anyone building on a platform shift today.",
"notes": [
{"title": "Concepts", "body": """How technologies actually spread — and who gets blindsided.
- **First Industrial Revolution** (~1760–1840) — steam, mechanized textiles, iron: Britain's factories.
- **Second Industrial Revolution** (~1870–1914) — electricity, steel, chemicals, the internal-combustion engine: mass production.
- **Third Industrial Revolution** (~1960s–) — electronics, computers, the internet: information as the factor of production.
- **Fourth** (claimed, from the 2010s) — cyber-physical systems, AI; historians differ on the count.
- **S-curve** — technologies diffuse along an S-curve: slow uptake, explosive growth, saturation. Infrastructure (railways, grids, fiber) determines the slope — technology without distribution is a demo.
- **Rogers' adopter categories** — innovators → early adopters → early majority → late majority → laggards.
- **Moore's chasm** — the gap between early adopters and the early majority; crossing it is the go-to-market crux.
- **Christensen's Innovator's Dilemma** (1997) — incumbents rationally serve their best customers with sustaining improvements, and are blindsided by **disruptive** technologies that start worse and cheaper, then climb the S-curve.
- **Kodak** — invented the digital camera (1975, Steve Sasson) and still lost; the dilemma is structural, not a failure of intelligence.
- **the internet's lesson** — ARPANET (1969) → TCP/IP standardization (1983) → the Web (1990–) → broadband → mobile: each layer enabled the next, and open protocols beat walled gardens at the infrastructure layer. Bet on open layers, expect the application layer to surprise you, and remember that distribution — not just invention — decides winners."""},
{"title": "Hands-on procedure", "body": """Run a disruption self-assessment on your own product — answer in writing.
1. **Name your best customers** and the sustaining improvements you ship for them.
2. **Find the cheaper, worse entrant.** Who serves the customers you ignore, with something you'd be embarrassed to ship?
3. **Ask what job it does** for those overlooked customers — in their words, not yours.
4. **Place yourself on the S-curve.** Slow uptake, explosive middle, or saturation? What infrastructure sets your slope?
5. **Locate the chasm.** Are you selling to early adopters while the early majority waits for proof? What proof would they need?
6. **Write the incumbent's memo.** Draft the one-page warning your successor would write about you — then decide whether to act on it."""},
{"title": "Project brief", "body": """**Deliverable: a two-page transition brief.** Pick a current platform shift (AI agents, edge compute, post-quantum cryptography — your choice). Cover: S-curve position with evidence, chasm status, the incumbent most at risk and why, the open layer to bet on. One recommendation, with the reasoning a skeptic would demand."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what is the Innovator's Dilemma — and why isn't it about stupidity?
- Give Noah two cases and ask for the disruption read: (a) Kodak and the digital camera, (b) open protocols versus walled gardens at the infrastructure layer.
- *Visual learners:* "Ask Noah to sketch the S-curve, mark the chasm, and place your product on it — then defend the placement."
- *Honesty:* the S-curve is a model, not a prophecy — it organizes evidence; it does not replace it."""}
],
"quiz_explains": [
"~1870–1914: electrification, Bessemer steel, chemical industry, internal combustion. (See 'Concepts': Second Industrial Revolution.)",
"Crossing from enthusiasts to the pragmatic majority is the go-to-market crux. (See 'Concepts': Moore's chasm.)",
"Disruption enters low-end or new markets, then moves up as performance improves. (See 'Concepts': disruptive technologies.)",
"An open, shared protocol layer let diverse networks interoperate — infrastructure for everything above. (See 'Concepts': the internet's lesson.)"
]
},

"m21-technical-writing": {
"summary": "Welcome to Module 9. I'm your instructor, and this module is pure craft: technical writing as a professional discipline. Structure for scanners, precision over decoration, the core documents — and the editing pass where the real work happens.",
"notes": [
{"title": "Concepts", "body": """The working rules of prose that gets read.
- **BLUF** — Bottom Line Up Front: put the **conclusion first**, then evidence; write for scanners, not just readers. A design doc's first paragraph should let a busy reader decide whether to read the rest.
- **active voice** — with concrete subjects: "The deploy script restarts the service" beats "The service is restarted."
- **define before use** — define every term before first use; never let "it", "this", or "thing" carry load.
- **numbers over adjectives** — "p99 latency rose from 40ms to 900ms" beats "latency got much worse."
- **no throat-clearing** — delete "It is important to note that…".
- **RFC / design doc** — problem, goals/non-goals, proposal, alternatives considered, risks, rollout.
- **runbook** — symptoms → diagnosis → fix; tested by someone who didn't write it, during calm — never first-tested in a real incident.
- **status update** — what changed, what's blocked, what's next: three bullets, no novel.
- **commit message** — what *and* why; the diff already shows the what.
- **editing is the work** — first drafts are for the writer; editing is for the reader. Cut 20% on the second pass as a discipline; read aloud to catch tangles. The standard: a competent stranger, interrupted twice, can still follow it. Strunk & White's *The Elements of Style* (1918): "omit needless words"."""},
{"title": "Hands-on procedure", "body": """Rewrite a real document you shipped — a design doc, an incident review, or a status update.
1. **Pick the document** — something with a real audience, not a draft.
2. **BLUF it.** Move the conclusion to paragraph one. If the document has no conclusion, write one — that's the diagnosis.
3. **Activate the voice.** Convert every passive to active with a concrete subject.
4. **Quantify.** Replace each adjective of degree ("much worse", "significantly") with a number.
5. **Cut 20%.** Delete throat-clearing, hedged restatements, and any sentence the document survives without.
6. **Read it aloud.** Tangles you hear are tangles your reader will trip on — untangle them.
7. **Hand it to a stranger.** A competent colleague who lacks your context reads it once, interrupted twice. Where they stall, rewrite."""},
{"title": "Project brief", "body": """**Deliverable: a portfolio document set.** For a real project, produce three documents to this module's standard: (a) a one-page RFC/design doc with all six sections, (b) a runbook a stranger could execute, (c) a three-bullet status update. Each must survive the read-aloud test and the 20% cut. File them where your team will actually find them — a document nobody can find is a document you didn't write."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what does BLUF demand of your first paragraph?
- Give Noah three sentences and ask which is strongest: the passive, the active, and the throat-clearer.
- *Visual learners:* "Ask Noah to take one of your paragraphs and show the 20% cut inline — what goes, and why."
- *Honesty:* clarity is respect for the reader's time — and the standard is the interrupted stranger, not your own satisfaction."""}
],
"quiz_explains": [
"Concrete subject, active verb, no throat-clearing. (See 'Concepts': active voice.)",
"Lead with the conclusion so scanners can triage. (See 'Concepts': BLUF.)",
"Only a fresh reader proves the runbook is self-sufficient; never first-test it in a real incident. (See 'Concepts': runbook.)",
"Numbers beat adjectives — precise, checkable, actionable. (See 'Concepts': numbers over adjectives.)"
]
},

"m21-rhetoric": {
"summary": "Welcome to Module 10. I'm your instructor. Writing gave you clarity; this module gives you movement — rhetoric, the honest craft of moving people with reasons. Ethos, pathos, logos; the Toulmin model; framing and audience analysis.",
"notes": [
{"title": "Concepts", "body": """The honest craft of moving people with reasons.
- **ethos** — the speaker's credibility (Aristotle's *Rhetoric*, 4th c. BCE).
- **pathos** — the audience's emotions.
- **logos** — the argument's logic. Technical audiences over-invest in logos and starve the other two — but a correct argument from an untrusted speaker, framed without regard for stakes, still loses. All three are legitimate; the vice is substituting one for another.
- **Toulmin model** — Stephen Toulmin (1958): arguments have **claims**, **grounds** (evidence), **warrants** (the inference license connecting grounds to claim), **backing** (support for the warrant), **qualifiers**, and **rebuttals**.
- **the warrant insight** — in engineering reviews, fights are usually about *warrants* ("load tests predict production") — not about the data. Name the warrant and the debate gets productive.
- **audience analysis** — persuasion starts with the audience's **values, knowledge, and decision criteria** — not your material.
- **framing** — selecting which aspects of a situation are salient: the same migration is "risk reduction" to ops and "feature velocity" to product. Honest framing foregrounds relevant aspects; dishonest framing hides them.
- **persuasion vs. manipulation** — the line: persuasion respects the audience's rational agency — reasons they could endorse on reflection. Manipulation bypasses it: hidden agendas, manufactured urgency, selective data. The test you'd apply to others' decks, apply to your own: would this argument survive the audience knowing everything I know?"""},
{"title": "Hands-on procedure", "body": """Build a Toulmin brief for a proposal you actually care about.
1. **State your claim** in one sentence.
2. **List your grounds** — the evidence, no adjectives.
3. **Name the warrant** — why do these grounds support this claim? Write the inference license explicitly.
4. **Add backing, qualifier, rebuttal.** What supports the warrant? How strong is the claim, exactly? What is the best objection, steel-manned?
5. **Analyze the audience.** Values, knowledge, decision criteria — in their terms.
6. **Choose your appeals.** Where does this audience need ethos (why trust you), pathos (what's at stake for them), logos (the argument)?
7. **Frame honestly.** Foreground the aspects relevant to *their* decision — and include the trade-off you'd rather hide. Run the full-disclosure test."""},
{"title": "Project brief", "body": """**Deliverable: a five-minute pitch, on paper.** Write the pitch for a technical proposal to a mixed audience (engineers, a manager, one executive): stakes first, options with trade-offs, recommendation with reasons. Attach a one-page Toulmin appendix — claim, grounds, warrant, backing, qualifier, rebuttal. If the appendix and the pitch disagree, the appendix wins: fix the pitch."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, where do engineering debates usually break down — and why isn't it the data?
- Give Noah a claim — "load tests predict production behavior" — and ask: is that grounds or warrant?
- *Visual learners:* "Ask Noah to map one of your past debates onto Toulmin's six boxes, then point to the box where it actually broke."
- *Honesty:* run the full-disclosure test on your own pitch before you present it — the manipulation check applies to you first."""}
],
"quiz_explains": [
"Credibility of the speaker — ethos. (See 'Concepts': ethos.)",
"The warrant is *why* the grounds support the claim — usually the contested part. (See 'Concepts': Toulmin model.)",
"Bypassing rational agency with selective evidence — manipulation, not persuasion. (See 'Concepts': persuasion vs. manipulation.)",
"Persuasion starts from where the audience is, not from your slides. (See 'Concepts': audience analysis.)"
]
},

"m21-economics-1": {
"summary": "Welcome to Module 11. I'm your instructor. Economics for engineers, part one: markets and costs — supply and demand, opportunity cost, marginal thinking, and the cost structures inside every build-vs-buy and scale decision. We work it with numbers, not vibes.",
"notes": [
{"title": "Concepts", "body": """The economics inside every build-vs-buy and scale decision.
- **demand** — slopes down: higher price → less wanted. **Supply** — slopes up. **Equilibrium** — where they cross: the market-clearing price and quantity.
- **shifts** — demand shifts with tastes, income, substitutes; supply shifts with input costs, technology, number of sellers. A demand shift moves price *and* quantity; a supply shift does the same in the opposite direction.
- **price ceiling** — set below equilibrium, creates a **shortage**; **price floor** — set above, creates a **surplus**.
- **opportunity cost** — the value of the best forgone alternative: the true cost of any choice.
- **marginal analysis** — decide at the margin: is the *next* unit's benefit worth its *next* unit's cost? "We've already spent $2M" is irrelevant to whether the next $100K is worth it.
- **fixed costs** — don't vary with output (the data center lease). **Variable costs** — do (per-request compute).
- **sunk costs** — spent and unrecoverable; rational decisions ignore them.
- **economies of scale** — average cost falls as output rises (high fixed, low marginal cost — the software business in one phrase).
- **total cost of ownership** — license + integration + operations + the opportunity cost of the engineers building it instead of the product. Buying looks expensive and building looks free because salaries are already budgeted — that is the opportunity-cost illusion. Decide on TCO over the realistic lifetime, including maintenance you will definitely pay."""},
{"title": "Worked estimation", "body": """Estimate a build-vs-buy TCO — worked example with illustrative numbers; substitute your own figures.
1. **State the decision and the lifetime.** "Build the billing service vs. buy a SaaS billing product; 3-year horizon."
2. **Price the build.** 2 engineers × 3 months × $20k loaded cost/month = $120k to build. Maintenance: 0.25 engineer/year × $240k = $60k/year → $180k over 3 years. Build cash subtotal: $300k.
3. **Price the buy.** $4k/month license = $144k over 3 years. Integration: 1 engineer × 1 month = $20k. Ops overhead: $10k/year = $30k. Buy subtotal: $194k.
4. **Add the opportunity cost — this is the correction.** The build consumes 6 engineer-months that are already budgeted, which is exactly the illusion: the real cost is the product work forgone. (Illustrative: had those months shipped the checkout revamp worth ~$200k in margin, the build's true economic cost is $300k cash + $200k forgone = $500k.)
5. **Decide at the margin.** Compare forward-looking totals only — $500k vs. $194k at current scale. Any prototype spend to date is sunk: exclude it.
6. **Stress-test at scale.** At 10× usage the SaaS fees scale with volume while the build has near-zero marginal cost — economies of scale can flip the answer. Recompute at 3× and 10× before deciding."""},
{"title": "Project brief", "body": """**Deliverable: a build-vs-buy decision memo.** Take a real decision on your roadmap. Compute TCO over the realistic lifetime — license/fees + integration + operations + opportunity cost of diverted engineers + maintenance. Name the sunk-cost fallacy explicitly if past spend is invoked. Decide on forward-looking numbers, stress-test at 3× scale, and land a recommendation."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, why do rational decisions ignore sunk costs?
- Give Noah two figures and ask for the classification: (a) the data-center lease, (b) the $2M already spent on a failing project.
- *Worked check:* "Ask Noah to walk your current build-vs-buy line by line — cash costs, opportunity cost, sunk exclusions — and find the line you'd rather hide."
- *Honesty:* the numbers in the worked estimation are illustrative — your memo must use your real figures, sourced, with the uncertainty stated."""}
],
"quiz_explains": [
"Quantity demanded exceeds quantity supplied at the capped price. (See 'Concepts': price ceiling.)",
"Sunk costs are irrelevant; at the margin, $200K > $150K, so stop. (See 'Concepts': sunk costs; 'Worked estimation' step 5.)",
"Average cost collapses as users grow — the economics of the whole industry. (See 'Concepts': economies of scale.)",
"Lower input cost shifts supply right — the standard supply-shock result. (See 'Concepts': shifts.)"
]
},

"m21-economics-2": {
"summary": "Welcome to Module 12. I'm your instructor. Part two: incentives and games — externalities, public goods, the prisoner's dilemma, Nash equilibria, and mechanism design. Why systems behave the way they do once humans are in the loop — and how to design the loop.",
"notes": [
{"title": "Concepts", "body": """Why systems behave the way they do once humans are in the loop.
- **externality** — a cost or benefit imposed on third parties: pollution (negative), open-source software (positive).
- **public good** — non-excludable and non-rivalrous (clean air, basic research): everyone benefits, nobody wants to pay.
- **free-rider problem** — why public goods are under-provided.
- **the fixes** — price the externality (taxes, cap-and-trade), assign property rights (Coase), or fund publicly.
- **game** — players, strategies, payoffs.
- **Nash equilibrium** — a strategy profile where no player can *unilaterally* do better; stable, not necessarily good.
- **working tools** — dominant strategies, best responses, backward induction (in sequential games). Model the incentives before predicting the behavior.
- **prisoner's dilemma** — payoffs make mutual defection the Nash equilibrium even though mutual cooperation pays both more: the canonical model of arms races, price wars, and feature-copying.
- **escapes** — **repetition** (tit-for-tat sustains cooperation), **contracts** with enforcement, **reputation** systems, and changing the payoffs themselves.
- **mechanism design** — reverse game theory: choose the rules so that self-interested play produces the outcome you want — auctions, congestion pricing, on-call rotations, bug bounties. The engineer's version: don't exhort people to cooperate; **design the payoff matrix** so cooperation is the equilibrium."""},
{"title": "Worked estimation", "body": """Solve a 2×2 game — the prisoner's dilemma, worked step by step. Payoffs below are illustrative (years in prison; lower is better). Rows are your strategies, columns are theirs; each cell is (your payoff, their payoff).
1. **Find your best responses.** If they cooperate: defecting gives 0 vs. −1 for cooperating — defect. If they defect: defecting gives −2 vs. −3 — defect. Defection is your dominant strategy.
2. **Mirror it.** Their reasoning is symmetric — defection dominates for them too.
3. **Mark the Nash equilibrium.** (Defect, Defect) at (−2, −2): neither player gains by unilaterally deviating.
4. **Compare to the optimum.** (Cooperate, Cooperate) at (−1, −1) pays both more — the equilibrium is stable *and* worse. That gap is the tragedy.
5. **Design the escape.** Repeat the game (tit-for-tat: retaliation makes defection unprofitable over time), add an enforceable contract, build reputation tracking — or change the payoffs themselves. Pick one and say why it fits your case.""",
"code": "              Cooperate      Defect\nCooperate      (-1, -1)      (-3,  0)\nDefect         ( 0, -3)      (-2, -2)",
"lang": "text"},
{"title": "Project brief", "body": """**Deliverable: an incentive redesign.** Pick a cooperation failure on your team — on-call burden, code review latency, documentation debt. Model it as a game: players, strategies, payoffs. Find the Nash equilibrium and show why the bad outcome is stable. Then redesign the mechanism — rotate the burden, price the externality, add reputation — so cooperation becomes the equilibrium. One page of analysis, one page of proposed rules."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what is a Nash equilibrium — and why isn't it the same as the best outcome?
- Give Noah two mechanisms and ask what each prices or changes: congestion pricing, a bug bounty.
- *Worked check:* "Ask Noah to check your 2×2 solution — best responses, equilibrium, optimum — then to steel-man the case for defecting anyway."
- *Honesty:* the payoff numbers are illustrative scaffolding — your redesign must model your team's real incentives, observed, not assumed."""}
],
"quiz_explains": [
"A cost imposed on third parties outside the transaction. (See 'Concepts': externality.)",
"Each player gains by defecting regardless of the other's move — defection dominates. (See 'Concepts': prisoner's dilemma; 'Worked estimation' steps 1–3.)",
"The shadow of future retaliation shifts the equilibrium toward cooperation. (See 'Concepts': escapes.)",
"It charges drivers the congestion cost they impose — designing the payoff matrix. (See 'Concepts': mechanism design.)"
]
},

"m21-law-policy": {
"summary": "Welcome to Module 13. I'm your instructor. Law and policy literacy: intellectual property, liability, privacy regulation, and how policy actually gets made. What every technologist should know — without pretending to be a lawyer.",
"notes": [
{"title": "Concepts", "body": """Read law and policy as a literate citizen — orientation, not counsel.
- **copyright** — protects expression (code, text); automatic on creation; long terms. Open-source licenses (MIT, GPL) are copyright licenses granting permissions.
- **patent** — protects inventions; requires application and disclosure; ~20-year terms; software patentability varies by jurisdiction.
- **trademark** — protects brand identifiers.
- **trade secret** — protected by secrecy itself.
- **literacy, not legal advice** — consult counsel for real decisions.
- **liability** — software has historically faced limited liability for defects: licenses disclaim warranties, and courts treat software as a service as much as a product. That settlement is under pressure: critical infrastructure, autonomous systems, and AI are pushing toward product-like liability. The direction matters for design: **document** safety reasoning as if a court will read it, because one might.
- **GDPR** (EU, 2018) — consent, data minimization, purpose limitation, the right to erasure, heavy fines; reshaped global practice.
- **CCPA/CPRA** (California) — opt-out of sale/sharing, deletion rights.
- **sectoral US law** — health (HIPAA), children (COPPA).
- **the common logic** — individuals get rights over their data; collectors get obligations. Design for data minimization from the start.
- **how policy gets made** — **legislation**, **regulation** (agencies writing rules under statutes), **standards** (IETF, W3C, NIST — often voluntary until referenced by law), and **litigation**. Technologists influence all four: writing standards, commenting on rulemakings, and — most powerfully — building the systems whose properties the law then assumes. Code is policy's raw material."""},
{"title": "Hands-on procedure", "body": """Read a license like a literate citizen — do this on a dependency you actually ship.
1. **Pick a dependency** your project ships — open its license file.
2. **Identify the grant.** What permissions does the copyright holder give you, exactly?
3. **Identify the conditions.** What must you do in return (attribution, source disclosure, same-license)?
4. **Read the warranty disclaimer.** Note what the licensor disclaims — then ask who bears the risk that remains.
5. **Map it to your use.** Are you compliant as you distribute today — including in containers, SaaS, and vendored copies?
6. **Know the handoff.** Write down the fact pattern that would make you call counsel instead of deciding yourself — and keep that note with the license."""},
{"title": "Project brief", "body": """**Deliverable: a policy-impact memo.** For a system you build or plan: (a) which IP regimes touch it (your code, your brand, your dependencies' licenses), (b) which privacy regimes apply to its data and what obligations follow, (c) the liability direction and what safety reasoning you'd document today, (d) one standards body or rulemaking where your team's input would matter. Header on every page: literacy, not legal advice."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, when do voluntary technical standards become binding?
- Give Noah two artifacts and ask for the IP read: (a) your codebase, (b) your product's name.
- *Visual learners:* "Ask Noah to map the four policymaking channels — legislation, regulation, standards, litigation — onto one technology you follow, with a real example in each box."
- *Honesty:* this module is orientation, not counsel — Noah will remind you: for real decisions, consult a lawyer."""}
],
"quiz_explains": [
"Copyright vests automatically; the license is the author's permission slip with conditions. (See 'Concepts': copyright.)",
"Purpose limitation + minimization: collect what the purpose needs, nothing more. (See 'Concepts': GDPR.)",
"Standards are voluntary until legislation, regulation, or contracts incorporate them. (See 'Concepts': how policy gets made.)",
"Stated throughout: this is orientation, not counsel. (See 'Noah check-in': honesty.)"
]
},

"m21-synthesis": {
"summary": "Welcome to Module 14 — the capstone. I'm your instructor, and this is where the thirteen modules fuse: philosophy, history, writing, rhetoric, economics, and law combining in the judgment of a senior technologist. You'll run one case through all six lenses, and leave with a practice rather than a credential — because this course confers none.",
"notes": [
{"title": "Concepts", "body": """The integration — every lens, one judgment.
- **the six lenses** — ethics (duties vs. outcomes), epistemology (what do the accuracy claims actually establish, on what data?), history (which past expansions are the precedent?), economics (who bears the costs, who captures the gains?), law (which regimes govern the data and the deployment?), rhetoric (how do you argue the decision to the people affected?).
- **the worked case** — deploying facial recognition for building access, run through all six: duties to subjects vs. aggregate safety; the evidence behind the accuracy claims; surveillance-expansion precedents; cost/gain distribution; biometric data regimes; the argument to the people scanned.
- **senior judgment** — not deeper technical knowledge but wider **context**: second-order effects, stakeholder legitimacy, reversibility, and the ability to say "we should not build this" — with reasons. The humanities are the training ground for thinking about ends, not just means.
- **arguing to non-technical audiences** — translate without condescending: lead with **stakes** (what changes for them), then **options** with trade-offs, then your **recommendation** with reasons. Drop jargon or define it once. Expect values questions — "is this fair?" — and answer them as values questions, not technical puzzles.
- **a personal practice** — the course ends; the practice doesn't. Read one serious book a quarter outside your field. Write — memos, essays, reading notes — because writing is thinking. Argue with people who disagree with you, charitably. The goal is not to become a philosopher but to become a technologist whose judgment deserves trust.
- **the through-line** — structured reasoning about human ends and means: each area of this course is a discipline of thinking about what matters and why, in service of better building."""},
{"title": "Hands-on procedure", "body": """Run the six-lens review on a live decision — a deployment, a data collection, a model launch.
1. **Pick a real decision** — something pending, with stakes.
2. **Ethics pass.** Duties and outcomes: who is used as a means, what are the aggregate effects?
3. **Epistemology pass.** What do the supporting claims actually establish? Falsifiable? Replicated?
4. **History pass.** What is the precedent — and did it end well?
5. **Economics pass.** Who bears the costs, who captures the gains? What are the incentives once deployed?
6. **Law pass.** Which regimes govern? What must you document?
7. **Rhetoric pass.** Draft the argument to the affected people: stakes, options, recommendation.
8. **Integrate.** No single lens decides — write the judgment that weighs them, including what you still don't know. That paragraph is the deliverable."""},
{"title": "Project brief", "body": """**Deliverable: the citizen's memo — the course capstone.** Write a reasoned position on a technology policy question (yours, or the facial-recognition case): all six lenses in their own sections, the integration paragraph, and a recommendation — including "do not build" if the lenses land there. Then set up the personal practice: pick next quarter's serious book, start the reading notes, and schedule the charitable argument. File the memo where your future self will find it."""},
{"title": "Noah check-in", "body": """Noah probes mastery with questions like:
- In one sentence, what is judgment in this course's sense — and what is it not?
- Give Noah one case — facial recognition for building access — and ask for one question per lens.
- *Visual learners:* "Ask Noah to grade your capstone memo against the six lenses and tell you which lens is weakest — then strengthen it."
- *Honesty:* this course confers no certificate and no credential — what it offers is a practice. Ideas are paraphrased and attributed; nothing here is legal advice; the judgment, in the end, is yours."""}
],
"extra_cards": [
{"front": "Name the six lenses and the question each asks of a deployment.", "back": "Ethics: is it right (duties, outcomes)? Epistemology: what do the claims establish? History: what are the precedents? Economics: who bears costs and gains? Law: which regimes govern? Rhetoric: how do I argue it to those affected?"},
{"front": "What is the senior technologist's distinctive move, per this module?", "back": "Saying 'we should not build this' — with reasons — from wider context: second-order effects, legitimacy, reversibility. Ends, not just means."}
],
"quiz_explains": [
"Judgment = structured thinking about what is worth doing, using every lens. (See 'Concepts': the through-line.)",
"Values questions deserve values reasoning — metrics alone dodge the question. (See 'Concepts': arguing to non-technical audiences.)",
"Each area is a discipline of thinking about what matters and why — in service of better building. (See 'Concepts': the through-line.)",
"Practice, not review: read widely, write to think, argue well. (See 'Concepts': a personal practice.)"
]
}
}
