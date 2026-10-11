#!/usr/bin/env python3
"""Retrofit IL-10 modules to the IL-19 (Multicloud) course template shape.

Reads docs/university/data/courses/il-10-portfolio-career-professional-practice.json,
restructures each module (weight, instructor-voice summary, 4 titled notes sections,
expanded cards/quiz), preserves ALL existing factual content, validates, and writes
back in the template's indent=1 formatting. Touches no other file.
"""
import json
import os

PATH = os.path.expanduser(
    "~/workspace/apex-audit/docs/university/data/courses/"
    "il-10-portfolio-career-professional-practice.json"
)

import re

BAN_SUB = ["aleks", "khan academy", "coursera", "udemy", "palantir"]
BAN_WORD = ["edx", "nsa", "brilliant"]


def check_clean(text, where):
    low = text.lower()
    for b in BAN_SUB:
        assert b not in low, "banned brand %r in %s" % (b, where)
    for b in BAN_WORD:
        assert not re.search(r"\b%s\b" % b, low), "banned brand %r in %s" % (b, where)


# ---------------------------------------------------------------- module 1
M1_SUMMARY = (
    "Welcome to IL-10, Portfolio, Career & Professional Practice — the career academy "
    "of the Interstitium Labs university. I'm your instructor for this course, and my job "
    "here is different from the technical tracks: the proof of work is already in your "
    "portfolio — this course turns it into a career you run deliberately. This is Module 1: "
    "The Forward-Deployed Career. Over this module we're going to run the six-move FDE arc "
    "— discover, model, prove, integrate, operate, generalize — and build the outcome layer on "
    "top of it: AI-matched applications tracked against skills you've actually earned, a "
    "conversion funnel that diagnoses its own bottlenecks, and interview systems for technical "
    "depth, system design, behavioral stories, and offers. By the end you'll have a career "
    "operating system, not a stack of good intentions."
)

M1_CONCEPTS = (
    "The vocabulary of the forward-deployed career — every term below is a working tool, "
    "not decoration:\n"
    "- **Forward-deployed engineer (FDE)** — an engineer who ships inside the customer's "
    "environment: their compliance, their change windows, their team operating the result "
    "after handoff.\n"
    "- **Discover** — the first arc move: finding the customer's real problem beneath the "
    "stated one. Diagnose like a doctor — symptoms → tests → diagnosis.\n"
    "- **Model** — the second arc move: building a technical representation of the problem "
    "and the candidate solution.\n"
    "- **Prove** — the third arc move: the technical core. Prototype the risky parts first and "
    "prove with data, using the smallest decisive experiment.\n"
    "- **Integrate** — the fourth arc move: shipping inside the customer — their compliance, "
    "their change windows, their constraints.\n"
    "- **Operate** — the fifth arc move: running the solution inside the customer and "
    "transferring operations to their team.\n"
    "- **Generalize** — the sixth arc move: turning learnings from engagements into reusable "
    "product. The pattern across three engagements is the signal — not every engagement "
    "becomes product.\n"
    "- **AI-matched applications** — matching your proven skills to role requirements: apply "
    "where the evidence fits, not where the title flatters.\n"
    "- **Application tracking against skills earned** — every application cites portfolio proof; "
    "the catalog's nodes become resume bullets with proof links.\n"
    "- **The funnel** — applied → response → screen → onsite → offer. Conversion at each stage "
    "diagnoses the bottleneck: low response → fix the resume/portfolio; low conversion → fix "
    "the interview system; low offers → fix the close. The funnel is the strategy document.\n"
    "- **System design interview** — a conversation, not a monologue: requirements → estimates "
    "→ API → data model → scale → trade-offs, practiced aloud, clarifying questions first.\n"
    "- **Behavioral interview (the FDE story)** — STAR with forward-deployed flavor: the customer "
    "constraint, your diagnosis, the shipped outcome, the transfer — with numbers.\n"
    "- **Offer evaluation** — total comp, growth, team, and the walk-away number — decided "
    "BEFORE the offer arrives.\n"
    "- **Walk-away number** — a pre-committed compensation floor. Prevents the worst "
    "negotiation mistake: accepting from desperation."
)

M1_PROCEDURE = (
    "Run one complete FDE cycle on a real problem — even a small one. This is the procedure, "
    "in order:\n"
    "1. **Pick the problem.** A friend's business, an open-source issue, a process at a "
    "part-time job — small is fine, real is mandatory.\n"
    "2. **Discover.** Ask the key question first: 'what happens if we do nothing?' The "
    "problem's value lives in the answer. Write down the stated problem, then the diagnosed "
    "problem — they will differ.\n"
    "3. **Model and prove.** Name the riskiest assumption. Design the smallest decisive "
    "experiment that could kill it. Run it within weeks, not quarters — the FDE doesn't have "
    "quarters, they have weeks. Document the evidence.\n"
    "4. **Integrate and operate.** List the 'customer' constraints (compliance, change "
    "windows, who maintains it). Ship inside them. Write the transfer doc so their team can "
    "operate it after you — the transfer is the deliverable.\n"
    "5. **Generalize review.** Ask: which learnings compound into something reusable? File the "
    "pattern. Not every engagement becomes product; the pattern across three does.\n"
    "6. **Run the outcome layer.** Match your proven skills to five real roles (evidence, not "
    "titles). Apply with portfolio citations. Log every stage in the funnel tracker (see the "
    "course script lab), compute conversion at each stage, and fix ONLY the bottleneck stage."
)

M1_BRIEF = (
    "**Capstone: the FDE engagement dossier.** You are the forward-deployed engineer; deliver "
    "the dossier a client would pay for:\n"
    "- A **discovery memo** (one page): the stated problem, your diagnosis, and the answer to "
    "'what happens if we do nothing?'\n"
    "- **Proof**: the smallest decisive experiment you ran, the evidence it produced, and what "
    "it killed or confirmed.\n"
    "- A **funnel report**: 20+ real applications logged in the funnel tracker, conversion at "
    "each stage, and your bottleneck diagnosis with the single fix you're applying.\n"
    "- **Three STAR stories** in FDE format — customer constraint, diagnosis, shipped outcome "
    "with numbers, transfer — rehearsed aloud until tight (the course's STAR Story Builder "
    "trainer is built for this).\n"
    "- An **offer evaluation rubric**: total comp, growth, team — and your walk-away number, "
    "written down before any offer exists.\n"
    "Done right, this dossier is portfolio artifact, interview prep, and career plan in one."
)

M1_HONESTY = (
    "Everything in this module is practice material I authored for this course — the arc, the "
    "funnels, the story formats, the scenarios. Interstitium Labs confers no certificate, and "
    "nothing here is a credential, a job guarantee, or career advice about any specific "
    "employer. The interview frameworks describe how to prepare and perform; they don't certify "
    "outcomes. Track your real results in the funnel — the data is the honest part."
)

M1_CARDS = [
    {"front": "FDE arc (6)?",
     "back": "Discover → Model → Prove → Integrate → Operate → Generalize."},
    {"front": "Discovery's key question?",
     "back": "'What happens if we do nothing?' — the problem's value lives there."},
    {"front": "Prove how?",
     "back": "Smallest decisive experiment — weeks, not quarters."},
    {"front": "Funnel diagnosis?",
     "back": "Low response → resume/portfolio. Low conversion → interviews. Low offers → the close."},
    {"front": "System design framework?",
     "back": "Requirements → estimates → API → data model → scale → trade-offs. Aloud."},
    {"front": "Walk-away number?",
     "back": "Decided before the offer — prevents desperation acceptance."},
    {"front": "Integrate means?",
     "back": "Ship inside the customer's constraints — their compliance, their change windows, their team operating it after you."},
    {"front": "AI-matched applications rule?",
     "back": "Apply where the evidence fits, not where the title flatters — every application cites portfolio proof."},
]

M1_QUIZ = [
    {"q": "Customer asks for a dashboard. FDE first move?",
     "choices": ["build it",
                 "discover: what decision will it drive? what happens without it?",
                 "quote a price", "delegate"],
     "answer": 1,
     "explain": "Discover the real problem — the dashboard is a stated solution, not necessarily the need. (Concepts: Discover.)"},
    {"q": "Two weeks to prove value. Approach?",
     "choices": ["full rebuild",
                 "smallest decisive experiment on the riskiest assumption",
                 "slide deck", "wait"],
     "answer": 1,
     "explain": "Prove the risky part fast — evidence beats plans in short engagements. (Hands-on procedure: step 3.)"},
    {"q": "Engagement ends. What makes it 'generalize'?",
     "choices": ["a testimonial",
                 "learnings that compound into reusable product across engagements",
                 "a longer contract", "nothing"],
     "answer": 1,
     "explain": "Generalize = the pattern across engagements becomes product. (Concepts: Generalize.)"},
    {"q": "System design interview starts. First?",
     "choices": ["draw boxes",
                 "clarifying questions: users, scale, constraints",
                 "list technologies", "code"],
     "answer": 1,
     "explain": "Requirements first — designing without constraints is guessing. (Concepts: System design interview.)"},
    {"q": "Behavioral answer needs?",
     "choices": ["length",
                 "STAR + numbers: constraint, action, measured outcome",
                 "buzzwords", "humor"],
     "answer": 1,
     "explain": "Structure plus quantified outcomes — the FDE story format. (Concepts: Behavioral interview.)"},
    {"q": "Offer 20% below walk-away. Move?",
     "choices": ["accept, negotiate later",
                 "decline politely — the number was decided for a reason",
                 "counter at 50% more", "ghost"],
     "answer": 1,
     "explain": "The walk-away number is a pre-commitment — honor it. (Concepts: Walk-away number.)"},
    {"q": "The riskiest assumption is 'the integration will take a day.' FDE move?",
     "choices": ["plan a quarter around it",
                 "smallest decisive experiment: time-box a spike to prove or kill the assumption",
                 "ask the customer to decide", "add buffer and hope"],
     "answer": 1,
     "explain": "Prove = smallest decisive experiment on the riskiest assumption — evidence beats plans. (Hands-on procedure: step 3.)"},
    {"q": "Handoff week: the customer team can't operate what you built. Which arc move failed?",
     "choices": ["discover", "generalize",
                 "operate — the transfer was never completed", "prove"],
     "answer": 2,
     "explain": "Operate means the customer's team runs it after you — the transfer is the deliverable. (Concepts: Operate.)"},
]

# ---------------------------------------------------------------- module 2
M2_SUMMARY = (
    "Welcome back — I'm your instructor, and this is Module 2: Self-Knowledge. You can't "
    "direct a career you haven't examined, so before we build ventures or climb ladders, we're "
    "going to take the Jung-typology instrument — the Humanmetrics assessment — and treat it as "
    "exactly what it is: working-style data for career decisions. Not a box, not a destiny, not a "
    "hiring tool — data. You'll learn what the four dichotomies actually measure, how to map type "
    "to role-family fit as a hypothesis, how to compose teams from complementary styles, and how "
    "to write a development plan that grows your range instead of replacing who you are."
)

M2_CONCEPTS = (
    "The instrument and its honest interpretation — preferences as data:\n"
    "- **Jung typology** — a preference instrument measuring stable preferences in how you "
    "process information and make decisions. It measures preferences; it does NOT measure "
    "ability, intelligence, character, or destiny.\n"
    "- **Extraversion / Introversion (E/I)** — energy source: whether interaction or solitude "
    "recharges you. An introvert can present brilliantly; it just costs more energy.\n"
    "- **Sensing / Intuition (S/N)** — information: concrete detail and the present versus "
    "patterns, possibilities, and the future.\n"
    "- **Thinking / Feeling (T/F)** — decisions: impersonal logic and criteria versus values "
    "and human impact.\n"
    "- **Judging / Perceiving (J/P)** — lifestyle: settled plans and closure versus open options "
    "and flexibility.\n"
    "- **Working styles** — the 16 types read as styles of working, not boxes. Use for insight, "
    "not identity.\n"
    "- **Career-fit mapping** — type-to-role-family hypotheses: e.g., INTJ/INTP patterns in "
    "architecture and research, ESFJ/ENFJ patterns in customer-facing leadership. Fit is energy "
    "economics: where does the work energize you versus drain you? Hypothesis, not destiny — no "
    "type is 'best' for tech; the industry needs all 16.\n"
    "- **Working-style implications** — how you recharge, decide, and organize. Design your "
    "workday around the answers — and use it in interviews: 'I do my best deep work when...' is "
    "self-knowledge as a selling point.\n"
    "- **Team composition** — complementary styles: the visionary needs the finisher; the "
    "analyst needs the diplomat.\n"
    "- **Development plan** — deliberate practice of the non-preferred functions: the thinker "
    "practices naming stakeholder impact; the judger practices holding ambiguity; the introvert "
    "practices visible communication. Range, not replacement — one stretch behavior per quarter, "
    "small, observable, reviewable.\n"
    "- **Retake variance** — normal. Treat borderline dichotomies as flexible and "
    "context-dependent, not fixed labels."
)

M2_PROCEDURE = (
    "Turn the instrument into a working self-knowledge file. Steps:\n"
    "1. **Take it honestly.** Use the Humanmetrics instrument linked in this course's source "
    "links. Answer as you are, not as the job posting wants.\n"
    "2. **Record all four letters** and the strength of each preference. Flag every borderline — "
    "near-even splits are the honest answer, and they're flexible, not fixed.\n"
    "3. **Write the working-style profile** (one page): how you recharge, how you decide, how you "
    "organize — then design your workday around the answers. Which hours get deep work? Which "
    "meetings drain you, and how do you recover?\n"
    "4. **Map to role families as hypothesis.** List three role families you're considering. For "
    "each, score the energy economics: where would this work energize you, where would it drain "
    "you? Remember — hypothesis, not destiny.\n"
    "5. **Compose a team.** Design a hypothetical four-person project team with complementary "
    "styles covering vision, analysis, finishing, and diplomacy. Name what each style contributes "
    "and what breaks if one is missing.\n"
    "6. **Write the development plan.** Pick ONE non-preferred function. Define one observable "
    "stretch behavior for this quarter (e.g., 'name stakeholder impact explicitly in every "
    "proposal'). Review it quarterly. The plan lives with the career plan — self-knowledge "
    "directs the FDE arc."
)

M2_BRIEF = (
    "**Project: the self-knowledge dossier.** Deliver a four-part brief you can actually use:\n"
    "- **(1) Your result**, with borderline dichotomies flagged and interpreted as flexible — "
    "no fixed labels.\n"
    "- **(2) A one-page working-style profile** — 'I do my best deep work when...' — written in "
    "language you can use verbatim in interviews.\n"
    "- **(3) A team-composition plan** for a hypothetical four-person project: the four styles, "
    "what each contributes, and the failure mode if the finisher (or the diplomat) is missing.\n"
    "- **(4) A one-quarter development plan**: one non-preferred function, one observable stretch "
    "behavior, and the review date.\n"
    "This dossier is a career artifact: it feeds your interview answers, your team choices, and "
    "your quarterly reviews."
)

M2_HONESTY = (
    "This module is self-knowledge practice, not psychology. The instrument is a preference "
    "questionnaire — useful for reflection, working-style insight, and career-fit hypotheses; it "
    "is not a medical device, not a measure of ability or worth, and never a tool for hiring "
    "decisions about other people. Treat your type as data about yourself, hold it lightly, and "
    "retake it if life changes you. Interstitium Labs confers no certificate."
)

M2_CARDS = [
    {"front": "Four dichotomies?",
     "back": "E/I (energy), S/N (information), T/F (decisions), J/P (lifestyle)."},
    {"front": "Measures vs doesn't?",
     "back": "Measures: processing/decision preferences. Doesn't: ability, intelligence, destiny."},
    {"front": "Types as?",
     "back": "Working styles, not boxes — insight, not identity."},
    {"front": "Career-fit use?",
     "back": "Energy economics — where work energizes vs drains. Hypothesis, not destiny."},
    {"front": "Team composition rule?",
     "back": "Complementary styles — visionary + finisher, analyst + diplomat."},
    {"front": "Development = ?",
     "back": "Range, not replacement — one stretch behavior per quarter."},
    {"front": "Retake variance means?",
     "back": "Normal — borderline dichotomies are flexible and context-dependent, not fixed."},
    {"front": "Never use typology for?",
     "back": "Hiring decisions about others — or destiny claims. Insight for yourself, not judgments of people."},
]

M2_QUIZ = [
    {"q": "INTP considering sales engineering. Typology says?",
     "choices": ["forbidden",
                 "data point: weigh the energy economics, decide informed",
                 "ideal", "irrelevant"],
     "answer": 1,
     "explain": "Hypothesis, not destiny — fit is about sustainable energy, and people stretch successfully. (Concepts: Career-fit mapping.)"},
    {"q": "Borderline T/F result. Interpret?",
     "choices": ["pick one forever",
                 "flexible — context-dependent; note it",
                 "retake until clear", "ignore"],
     "answer": 1,
     "explain": "Borderlines are the honest answer — flexibility, not a fixed label. (Concepts: Retake variance.)"},
    {"q": "Team of four INTJs stalls on shipping. Diagnose?",
     "choices": ["more analysis",
                 "missing complementary styles — add a finisher/driver",
                 "fire someone", "more meetings"],
     "answer": 1,
     "explain": "Composition: analysis without execution needs its complement. (Concepts: Team composition.)"},
    {"q": "Best use in an interview?",
     "choices": ["announce your type",
                 "frame working style: 'I do best deep work when...'",
                 "hide it", "test the interviewer"],
     "answer": 1,
     "explain": "Self-knowledge as a selling point — concrete, not labeled. (Concepts: Working-style implications.)"},
    {"q": "Thinker developing Feeling range: practice?",
     "choices": ["suppress logic",
                 "name stakeholder impact explicitly in proposals",
                 "avoid people", "more data"],
     "answer": 1,
     "explain": "Range: keep the analysis, add the human impact — explicitly. (Concepts: Development plan.)"},
    {"q": "Your J/P comes back 51/49. You conclude?",
     "choices": ["you're a Judger, permanently",
                 "flexible and context-dependent — note the borderline",
                 "the test is broken", "retake until 90/10"],
     "answer": 1,
     "explain": "Near-even splits are the honest answer — treat them as flexible, not a fixed label. (Hands-on procedure: step 2.)"},
    {"q": "A hiring manager asks you to type the other candidates. You?",
     "choices": ["do it — data is data",
                 "decline — the instrument is for your own working-style insight, never hiring decisions about others",
                 "type them secretly", "ask for their star signs instead"],
     "answer": 1,
     "explain": "A preference instrument, not a selection tool — insight for yourself, not judgments of people. (Honesty note.)"},
    {"q": "Judger developing Perceiving range practices?",
     "choices": ["more detailed plans",
                 "holding ambiguity — leaving one workstream deliberately open this quarter",
                 "avoiding all structure", "switching types"],
     "answer": 1,
     "explain": "Development = range, not replacement: one observable stretch behavior per quarter. (Concepts: Development plan.)"},
]

# ---------------------------------------------------------------- module 3
M3_SUMMARY = (
    "Welcome to Module 3: Entrepreneurship — the Babson-informed track. I'm your instructor, "
    "and here's my promise for this module: we're going to treat entrepreneurship as a "
    "discipline with a literature — opportunity recognition, resource marshaling, risk "
    "management — not a mystical calling. You'll audit the Babson curriculum map against a "
    "venture's real needs, practice problem discovery (pains with budgets), run the MVP "
    "discipline as experiments instead of products, model unit economics until the spreadsheet "
    "tells you scale, fix, or kill, and learn fundraising literacy so you can read a SAFE before "
    "you ever sign one. The contemporary practitioner model — operators teaching operators — is "
    "our frame: borrow the proof-of-work, skip the credential worship."
)

M3_CONCEPTS = (
    "The venture vocabulary — each term is a decision tool:\n"
    "- **Problem discovery** — finding pains with budgets: the problem must hurt AND have a "
    "payer. Fun without a budget is a hobby, not a venture.\n"
    "- **MVP discipline** — the smallest test of the riskiest assumption. An experiment, not a "
    "product — concierge and Wizard-of-Oz tests count.\n"
    "- **Unit economics** — the per-customer math: CAC, LTV, payback period, contribution margin. "
    "The bar: LTV:CAC ≥ 3 and payback < 12 months — or the model doesn't work.\n"
    "- **CAC (customer acquisition cost)** — what you pay to win one customer.\n"
    "- **LTV (lifetime value)** — the gross profit expected from one customer over the whole "
    "relationship: ARPU × margin ÷ churn.\n"
    "- **Payback period** — CAC ÷ monthly gross profit per customer. Under 12 months is the bar.\n"
    "- **Fundraising literacy** — SAFEs and convertibles, dilution, the pitch as a story with "
    "numbers. Raise from strength or don't raise — fundraising is a tactic, not the goal.\n"
    "- **SAFE (Simple Agreement for Future Equity)** — invest now, price later. Know the cap and "
    "the discount before you sign.\n"
    "- **Default alive / default dead** — can you reach profitability on current cash? Alive = "
    "yes. Plan the path to default alive explicitly.\n"
    "- **Curriculum audit** — mapping your venture's needs against the disciplines (finance, "
    "marketing, operations): hire or learn to cover the gaps. It prevents the classic failure — "
    "a strong product with no distribution.\n"
    "- **Entrepreneurship as a discipline** — opportunity recognition, resource marshaling, risk "
    "management: teachable, not mystical. The three founder literacies are finance, marketing, "
    "and operations — read a P&L, acquire a customer, deliver the thing.\n"
    "- **Practitioner-led education** — operators teaching operators: war stories over textbooks. "
    "Borrow: practitioner instructors, project-based proof, hiring-partner integration. Avoid: "
    "credential worship, debt for signaling, curriculum as content marketing."
)

M3_WORKED = (
    "Worked estimation: the unit-economics verdict, step by step. This is the exact calculation "
    "behind the course's unit-economics script lab — follow it by hand once, then automate it:\n"
    "1. **Write down the inputs.** CAC = $120, ARPU = $25/month, gross margin = 0.8, monthly "
    "churn = 0.05.\n"
    "2. **Compute LTV.** LTV = ARPU × margin ÷ churn = 25 × 0.8 ÷ 0.05 = $400.\n"
    "3. **Compute the ratio.** LTV ÷ CAC = 400 ÷ 120 ≈ 3.3 — clears the ≥ 3 bar.\n"
    "4. **Compute payback.** Payback = CAC ÷ (ARPU × margin) = 120 ÷ 20 = 6 months — under the "
    "12-month bar.\n"
    "5. **Read the verdict.** Ratio ≥ 3 and payback < 12 → SCALE: the economics work.\n"
    "6. **Know the other branches.** Ratio ≥ 2 but a bar missed → FIX: improve retention or "
    "monetization before scale. Below that → KILL or rebuild: scaling a broken unit is just "
    "faster dying.\n"
    "7. **Apply the sanity rule.** Unit economics before scale, unit economics before virality — "
    "the spreadsheet is the strategy."
)

M3_BRIEF = (
    "**Project: the venture brief.** You're the founder; deliver the brief an honest investor "
    "would respect:\n"
    "- **(1) A problem statement** with a named payer and budget evidence — pains with budgets, "
    "not vibes.\n"
    "- **(2) An MVP experiment design** for the riskiest assumption: the smallest decisive test "
    "(concierge and Wizard-of-Oz welcome), what kills the idea, what confirms it.\n"
    "- **(3) A unit-economics model**: your CAC, LTV, payback, and contribution margin, with the "
    "verdict rule applied — scale, fix, or kill, in writing. Run the course's unit-economics "
    "script lab on your numbers.\n"
    "- **(4) A one-page fundraising-literacy memo**: SAFE terms (cap, discount), a dilution sketch, "
    "and your call — raise from strength, or run default-alive.\n"
    "- **(5) A curriculum audit**: the three founder literacies against your venture's needs — "
    "what you'll learn, what you'll hire for.\n"
    "Remember: the founder's curriculum is the venture itself."
)

M3_HONESTY = (
    "Practice material only — I authored these frameworks for this course; they're heuristics "
    "from venture practice, not laws of nature. Nothing here is investment, legal, or financial "
    "advice: SAFEs and dilution are real instruments, so get qualified counsel before signing "
    "anything, and confirm current program terms with the institutions themselves. Interstitium "
    "Labs confers no certificate and is not affiliated with Babson or Y Combinator."
)

M3_CARDS = [
    {"front": "Problem worth solving?",
     "back": "Pain + budget — hurts AND has a payer."},
    {"front": "MVP = ?",
     "back": "Smallest test of the riskiest assumption — experiment, not product."},
    {"front": "Unit economics bar?",
     "back": "LTV:CAC ≥ 3, payback < 12 months, positive contribution margin."},
    {"front": "SAFEs?",
     "back": "Simple Agreement for Future Equity — invest now, price later. Know the cap/discount."},
    {"front": "Default alive vs default dead?",
     "back": "Can you reach profitability on current cash? Alive = yes. Plan to alive."},
    {"front": "Borrow vs avoid (practitioner model)?",
     "back": "Borrow: proof-of-work, operators teaching. Avoid: credential worship, debt for signaling."},
    {"front": "Payback period = ?",
     "back": "CAC ÷ monthly gross profit per customer. Under 12 months is the bar."},
    {"front": "Raise or not?",
     "back": "Raise from strength or don't raise — fundraising is a tactic, not the goal."},
]

M3_QUIZ = [
    {"q": "Two ideas: fun with no payer vs boring with budget. Pick?",
     "choices": ["fun",
                 "boring with budget — pains with budgets",
                 "both", "neither"],
     "answer": 1,
     "explain": "Ventures need payers — fun without budget is a hobby. (Concepts: Problem discovery.)"},
    {"q": "Riskiest assumption: 'users want it'. MVP?",
     "choices": ["full app",
                 "concierge test: deliver manually to 10 users",
                 "landing page only", "pitch deck"],
     "answer": 1,
     "explain": "Test demand with the smallest decisive experiment — manual counts. (Concepts: MVP discipline.)"},
    {"q": "CAC $100, LTV $200. Verdict?",
     "choices": ["scale",
                 "broken — LTV:CAC 2 < 3; fix economics before scale",
                 "fine", "raise prices blindly"],
     "answer": 1,
     "explain": "Below the bar — scaling multiplies the loss. (Worked estimation: step 6.)"},
    {"q": "Default dead with 18 months runway. Move?",
     "choices": ["hope",
                 "path to default alive: cut, grow, or raise from strength",
                 "ignore", "pivot randomly"],
     "answer": 1,
     "explain": "18 months to alive-or-funded — plan it explicitly. (Concepts: Default alive.)"},
    {"q": "Founder can't read a P&L. Fix?",
     "choices": ["hire a CFO day one",
                 "learn the three literacies: finance, marketing, ops",
                 "ignore", "outsource thinking"],
     "answer": 1,
     "explain": "Founders need the foundations — hire to scale, not to think. (Concepts: Entrepreneurship as a discipline.)"},
    {"q": "CAC $60, ARPU $20/mo, margin 0.75, churn 0.10. LTV?",
     "choices": ["$150", "$200", "$60", "$15"],
     "answer": 0,
     "explain": "LTV = ARPU × margin ÷ churn = 20 × 0.75 ÷ 0.10 = $150. (Worked estimation: step 2.)"},
    {"q": "Ratio 3.3, payback 6 months. Verdict?",
     "choices": ["kill it",
                 "SCALE — the economics clear the bar",
                 "fix pricing first", "raise immediately"],
     "answer": 1,
     "explain": "LTV:CAC ≥ 3 and payback < 12 → SCALE. (Worked estimation: step 5.)"},
    {"q": "Offered a SAFE with no cap and no discount. Response?",
     "choices": ["sign — money is money",
                 "know the terms: cap/discount protect you — negotiate or walk; fundraising literacy first",
                 "take it and figure it out later", "refuse all SAFEs"],
     "answer": 1,
     "explain": "Fundraising literacy: know the cap and discount before signing anything. (Concepts: SAFE.)"},
]

# ---------------------------------------------------------------- module 4
M4_SUMMARY = (
    "Welcome to Module 4: Quantitative Finance — the ladder. I'm your instructor, and I want "
    "to be straight with you up front: this module is a preparation map, not a shortcut. We're "
    "going to audit the prerequisites honestly (proof-level math, probability at depth, "
    "programming), map the internship timeline — the interviews start a year before the "
    "internship — work through the MIT MicroMasters in Finance as a graduate-level on-ramp with "
    "a real proctored comprehensive exam, and finish at the fork: desk quant, researcher, or "
    "consultant. Three different games. You'll choose with your eyes open, in writing."
)

M4_CONCEPTS = (
    "The ladder's vocabulary — each term marks a rung or a gate:\n"
    "- **Prerequisite audit** — the honest inventory: proof-level calculus, linear algebra, and "
    "probability; Python (pandas/numpy) and C++ for latency-sensitive work. Gaps compound — fix "
    "them before the ladder.\n"
    "- **Probability at depth** — the interview core: the classic coins-and-dice problems, "
    "solved at depth and under time.\n"
    "- **Stochastic calculus** — the mathematics of random processes; the language derivatives "
    "pricing is written in.\n"
    "- **Itô's lemma** — the chain rule for stochastic processes: d(W²) = 2W dW + dt. The dt "
    "term is the whole point — it comes from the quadratic variation of Brownian motion, "
    "dW² = dt.\n"
    "- **MIT MicroMasters in Finance** — graduate-level finance courses: asset pricing, "
    "derivatives, financial engineering. This module maps preparation for it; it does not grant it.\n"
    "- **Proctored comprehensive exam** — the credential's teeth: identity-verified, rigorous. "
    "The filter — prepare like it matters, because it does.\n"
    "- **Degree-pathway value** — credit toward the master's: the MicroMasters as an on-ramp, not "
    "just a certificate. Do the transfer math before enrolling.\n"
    "- **Desk quant** — implements models close to P&L: implementation speed and correctness "
    "under pressure. Desk roles hire at bachelor's/master's with proof-level math and C++/Python.\n"
    "- **Researcher** — novel mathematics, publication-adjacent work. Skews PhD.\n"
    "- **Consultant** — breadth, clients, travel. The case interview is its own sport: structured "
    "problem-solving, mental math, framework first — practice cases, not just math.\n"
    "- **The internship map** — the timelines: sophomore → junior summer, and the interviews "
    "start a year before the internship."
)

M4_WORKED = (
    "Worked estimation: Itô's lemma applied to W², step by step. This is the technical heart of "
    "the module — follow it by hand until the dt term feels inevitable:\n"
    "1. **State the tool.** Itô's formula: for a smooth f and standard Brownian motion W, "
    "df = f′(W) dW + ½ f″(W) dt.\n"
    "2. **Pick the function.** f(x) = x², so f′(x) = 2x and f″(x) = 2.\n"
    "3. **Substitute.** d(W²) = 2W dW + ½·2·dt = 2W dW + dt.\n"
    "4. **Read the result.** The ordinary chain rule would give only 2W dW. Stochastic calculus "
    "adds the drift correction dt — that term is the whole point, and it comes from dW² = dt, "
    "the quadratic variation of Brownian motion.\n"
    "5. **Generalize once.** For f(x) = x³: f′ = 3x², f″ = 6x, so d(W³) = 3W² dW + 3W dt. Same "
    "machinery, every time.\n"
    "6. **Connect it.** Graduate finance is applied stochastic calculus — this is why the math "
    "module wasn't optional."
)

M4_BRIEF = (
    "**Project: the quant-ladder plan.** Deliver a written plan with five parts:\n"
    "- **(1) A prerequisite audit** with honest gap flags: calculus, linear algebra, and "
    "probability at proof level (not cookbook); Python and C++. Gaps get study blocks, not "
    "wishful thinking.\n"
    "- **(2) A 12-week probability-depth schedule**: timed problem sets, coins-and-dice at depth, "
    "code interviews where you implement the math (stochastic simulation in an hour).\n"
    "- **(3) An internship timeline** worked backward from your target summers — applications "
    "and interviews a year ahead.\n"
    "- **(4) A MicroMasters preparation map**: which IL-02/IL-10 nodes prepare each graduate "
    "course, plus a transfer-math worksheet — credit terms verified with MIT before enrolling.\n"
    "- **(5) A fork memo**: desk quant, researcher, or consultant — the game each one is, and "
    "your choice, with eyes open, in writing."
)

M4_HONESTY = (
    "This module maps preparation; it grants nothing. The MIT MicroMasters in Finance is a real "
    "credential program — confirm current requirements, pricing, and credit-transfer terms with "
    "MIT, since program details change. Interview difficulty varies by firm and by year, and "
    "nothing here guarantees outcomes. Interstitium Labs confers no certificate and is not "
    "affiliated with MIT."
)

M4_CARDS = [
    {"front": "Prerequisite audit covers?",
     "back": "Proof-level calculus/linear algebra/probability + Python/C++ — gaps compound."},
    {"front": "MicroMasters' teeth?",
     "back": "The proctored comprehensive exam — identity-verified, rigorous."},
    {"front": "Itô's lemma?",
     "back": "The chain rule for stochastic processes — dW² = dt. The quant's calculus."},
    {"front": "Desk quant vs researcher?",
     "back": "Desk: implement models near P&L. Researcher: novel mathematics. Different games."},
    {"front": "Case interview sport?",
     "back": "Structured problem-solving + mental math + framework — practice cases."},
    {"front": "Internship timeline?",
     "back": "Interviews a year before — sophomore spring for junior summer."},
    {"front": "Quadratic variation of Brownian motion?",
     "back": "dW² = dt — the source of the extra term in Itô's lemma."},
    {"front": "Ordinary chain rule vs Itô?",
     "back": "Ordinary: df = f′(W)dW. Itô adds ½f″(W)dt — the drift correction."},
]

M4_QUIZ = [
    {"q": "Biggest predictor of quant interview success?",
     "choices": ["school name",
                 "probability at depth + mental math under time",
                 "suit", "networking"],
     "answer": 1,
     "explain": "The interviews are technical — depth and speed decide. (Concepts: Probability at depth.)"},
    {"q": "Itô: d(W²)?",
     "choices": ["2W dW", "2W dW + dt", "0", "W² dt"],
     "answer": 1,
     "explain": "Itô's lemma: d(W²) = 2W dW + dt — the dt term is the whole point. (Worked estimation: step 3.)"},
    {"q": "MicroMasters value beyond learning?",
     "choices": ["none",
                 "degree-pathway credit — do the transfer math",
                 "the logo", "networking"],
     "answer": 1,
     "explain": "Credit toward the master's — verify transfer before enrolling. (Concepts: Degree-pathway value.)"},
    {"q": "Desk quant's edge?",
     "choices": ["theory",
                 "implementation speed near P&L",
                 "academia", "travel"],
     "answer": 1,
     "explain": "Desk quants ship models that trade — speed and correctness under pressure. (Concepts: Desk quant.)"},
    {"q": "Case interview first step?",
     "choices": ["answer",
                 "structure: clarify, framework, hypothesis",
                 "guess", "math"],
     "answer": 1,
     "explain": "Structure before solving — the framework is the answer's skeleton. (Concepts: Consultant.)"},
    {"q": "Itô: d(W³)?",
     "choices": ["3W² dW", "3W² dW + 3W dt", "W³ dt", "0"],
     "answer": 1,
     "explain": "Itô: df = f′dW + ½f″dt = 3W²dW + 3Wdt. (Worked estimation: step 5.)"},
    {"q": "Sophomore targeting a junior-summer quant internship. When do interviews start?",
     "choices": ["junior fall",
                 "sophomore spring — a year before",
                 "senior year", "after graduation"],
     "answer": 1,
     "explain": "The interviews start a year before the internship. (Concepts: The internship map.)"},
    {"q": "Researcher track's core edge?",
     "choices": ["implementation speed", "novel mathematics",
                 "client travel", "mental math"],
     "answer": 1,
     "explain": "Researcher = new models, publication-adjacent; desk = implementation speed near P&L. (Concepts: the fork.)"},
]


# ------------------------------------------------------------- driver
MODULE_SPECS = {
    "il10-fde-career": {
        "weight": 1, "summary": M1_SUMMARY,
        "notes": [("Concepts", M1_CONCEPTS),
                  ("Hands-on procedure", M1_PROCEDURE),
                  ("Project brief", M1_BRIEF),
                  ("Honesty note", M1_HONESTY)],
        "cards": M1_CARDS, "quiz": M1_QUIZ,
    },
    "il10-humanmetrics": {
        "weight": 1, "summary": M2_SUMMARY,
        "notes": [("Concepts", M2_CONCEPTS),
                  ("Hands-on procedure", M2_PROCEDURE),
                  ("Project brief", M2_BRIEF),
                  ("Honesty note", M2_HONESTY)],
        "cards": M2_CARDS, "quiz": M2_QUIZ,
    },
    "il10-entrepreneurship": {
        "weight": 1, "summary": M3_SUMMARY,
        "notes": [("Concepts", M3_CONCEPTS),
                  ("Worked estimation", M3_WORKED),
                  ("Project brief", M3_BRIEF),
                  ("Honesty note", M3_HONESTY)],
        "cards": M3_CARDS, "quiz": M3_QUIZ,
    },
    "il10-quant-finance": {
        "weight": 1, "summary": M4_SUMMARY,
        "notes": [("Concepts", M4_CONCEPTS),
                  ("Worked estimation", M4_WORKED),
                  ("Project brief", M4_BRIEF),
                  ("Honesty note", M4_HONESTY)],
        "cards": M4_CARDS, "quiz": M4_QUIZ,
    },
}


def main():
    with open(PATH, "r", encoding="utf-8") as f:
        d = json.load(f)  # BEFORE: must parse cleanly
    assert d["courseId"] == "il-10-portfolio-career-professional-practice"
    assert len(d["modules"]) == 4

    for m in d["modules"]:
        spec = MODULE_SPECS[m["id"]]
        m["weight"] = spec["weight"]
        m["summary"] = spec["summary"]
        m["notes"] = [{"title": t, "body": b} for t, b in spec["notes"]]
        m["cards"] = spec["cards"]
        m["quiz"] = spec["quiz"]

    # ---- validations ----
    for m in d["modules"]:
        where = m["id"]
        assert isinstance(m["weight"], int), where
        assert "I'm your instructor" in m["summary"], where
        check_clean(m["summary"], where + " summary")
        titles = [n["title"] for n in m["notes"]]
        assert titles[0] == "Concepts", where
        assert titles[1] in ("Hands-on procedure", "Worked estimation"), where
        assert titles[2] == "Project brief", where
        assert titles[3] == "Honesty note", where
        for n in m["notes"]:
            check_clean(n["body"], where + " note " + n["title"])
        concepts_body = m["notes"][0]["body"]
        glossary_lines = [l for l in concepts_body.splitlines()
                          if l.startswith("- **")]
        assert len(glossary_lines) >= 5, where + " concepts glossary too thin"
        for l in glossary_lines:
            assert " — " in l, where + " glossary line missing em dash: " + l[:60]
        assert len(m["cards"]) >= 6, where
        assert len(m["quiz"]) >= 6, where
        for qi, q in enumerate(m["quiz"]):
            assert len(q["choices"]) == 4, "%s quiz %d" % (where, qi)
            assert isinstance(q["answer"], int) and 0 <= q["answer"] <= 3, where
            assert q["explain"].strip(), where
            check_clean(q["q"] + " ".join(q["choices"]) + q["explain"],
                        "%s quiz %d" % (where, qi))
        for c in m["cards"]:
            check_clean(c["front"] + c["back"], where + " card")

    # course-level keys all present
    for key in ["arc", "priorities", "battlePlan", "mockTasks", "cheatSheets",
                "answerBank", "mockMinutes", "sourceLinks", "honestyNote"]:
        assert key in d, "missing course key " + key
    assert isinstance(d["mockMinutes"], int)
    for s in d["sourceLinks"]:
        assert s.get("retrieved"), "sourceLink missing retrieved: " + s.get("name", "?")
    check_clean(d["honestyNote"], "course honestyNote")
    # mockTasks shape
    for t in d["mockTasks"]:
        assert len(t["choices"]) == 4 if t["type"] == "choice" else True
        assert t["explain"].strip()

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)

    with open(PATH, "r", encoding="utf-8") as f:
        d2 = json.load(f)  # AFTER: must parse cleanly
    assert len(d2["modules"]) == 4
    print("OK: %d modules, notes/cards/quiz per module:" % len(d2["modules"]))
    for m in d2["modules"]:
        print("  %s weight=%s notes=%d cards=%d quiz=%d" %
              (m["id"], m["weight"], len(m["notes"]),
               len(m["cards"]), len(m["quiz"])))


if __name__ == "__main__":
    main()
